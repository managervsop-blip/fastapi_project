import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select, update

from app.db import SessionLocal
from app.models.idempotency import IdempotencyKey
from app.models.outbox import TaskOutbox

logger = logging.getLogger(__name__)


async def create_task(payload: dict, key: str | None = None) -> uuid.UUID | None:
    """Записать задачу в outbox со статусом pending.

    Если key передан и уже существует — вернуть None (дубль, не создаём).
    Сохраняет trace_id текущего спана (для сквозной трассировки).
    """
    from opentelemetry import trace

    current_span = trace.get_current_span()
    trace_id = None
    if current_span and current_span.get_span_context().is_valid:
        trace_id = format(current_span.get_span_context().trace_id, "032x")

    async with SessionLocal() as session:
        if key:
            existing = await session.execute(
                select(IdempotencyKey).where(IdempotencyKey.key == key)
            )
            if existing.scalar_one_or_none():
                logger.info("outbox: duplicate key %s, skipping", key)
                return None

        task = TaskOutbox(payload=payload, status="pending", trace_id=trace_id)
        session.add(task)

        if key:
            session.add(IdempotencyKey(key=key))

        await session.commit()
        await session.refresh(task)
        logger.info("outbox: created task %s (key=%s, trace_id=%s)", task.id, key, trace_id)
        return task.id


async def fetch_pending(limit: int = 100) -> list[TaskOutbox]:
    """Взять пачку pending-задач."""
    async with SessionLocal() as session:
        result = await session.execute(
            select(TaskOutbox)
            .where(TaskOutbox.status == "pending")
            .order_by(TaskOutbox.created_at)
            .limit(limit)
        )
        return list(result.scalars().all())


async def mark_enqueued(task_id: uuid.UUID) -> None:
    """Отметить, что задача положена в Redis."""
    async with SessionLocal() as session:
        await session.execute(
            update(TaskOutbox)
            .where(TaskOutbox.id == task_id)
            .values(status="enqueued", updated_at=datetime.now(timezone.utc))
        )
        await session.commit()


async def mark_processing(task_ids: list[uuid.UUID]) -> None:
    if not task_ids:
        return
    async with SessionLocal() as session:
        await session.execute(
            update(TaskOutbox)
            .where(TaskOutbox.id.in_(task_ids))
            .values(
                status="processing",
                processing_started_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
        )
        await session.commit()
    logger.info("outbox: marked %d tasks as processing", len(task_ids))

async def mark_done(task_id: uuid.UUID) -> None:
    """Отметить, что задача выполнена."""
    async with SessionLocal() as session:
        await session.execute(
            update(TaskOutbox)
            .where(TaskOutbox.id == task_id)
            .values(status="done", updated_at=datetime.now(timezone.utc))
        )
        await session.commit()


async def mark_failed(task_id: uuid.UUID, error: str) -> None:
    """Отметить, что задача упала, и сохранить текст ошибки."""
    async with SessionLocal() as session:
        await session.execute(
            update(TaskOutbox)
            .where(TaskOutbox.id == task_id)
            .values(
                status="failed",
                last_error=error[:2000],
                updated_at=datetime.now(timezone.utc),
            )
        )
        await session.commit()
    logger.error("outbox: task %s failed: %s", task_id, error)
