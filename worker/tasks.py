import logging
import random

from opentelemetry import trace
from opentelemetry.trace import SpanContext, TraceFlags
from sqlalchemy import select
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from redis.asyncio import Redis
from core.rate_limiter import BitrixRateLimiter
from core import outbox

logger = logging.getLogger(__name__)


async def ping(ctx, message: str = "pong") -> str:
    logger.info("ping task received: %s", message)
    return message

def wait_operating_reset(retry_state):
    """
    Если пришла OPERATION_TIME_LIMIT — ждём до operating_reset_at.
    Иначе — экспоненциальная задержка (1, 2, 4 сек...).
    """
    exception = retry_state.outcome.exception()
    if exception is None:
        return wait_exponential(multiplier=1, min=1, max=30)(retry_state)

    # Проверяем, есть ли в тексте ошибки reset_at (мы пробрасываем его из bitrix_batch)
    error_msg = str(exception)
    if "OPERATION_TIME_LIMIT" in error_msg:
        # Пытаемся вытащить reset_at из сообщения (например: "reset_at: 1743058253")
        import re
        match = re.search(r"reset_at:\s*(\d+)", error_msg)
        if match:
            reset_at = int(match.group(1))
            wait_seconds = max(1, reset_at - time.time() + 1)
            logger.warning("OPERATION_TIME_LIMIT: waiting %.0f sec until reset", wait_seconds)
            return wait_seconds

@retry(
    stop=stop_after_attempt(5),
    wait=wait_operating_reset, 
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
async def process_outbox_task(ctx, task_id: str, payload: dict) -> dict:
    """Обработчик задачи из outbox с batch-оптимизацией.

    Вместо одной задачи берёт до 50 pending-задач и отправляет их одним batch-запросом.
    """
    import uuid as _uuid
    from app.db import SessionLocal
    from app.models.outbox import TaskOutbox
    from core.bitrix_batch import execute_batch
    from sqlalchemy import select, update
import logging
import random
import re
import time
from datetime import datetime, timezone

from opentelemetry import trace
from opentelemetry.trace import SpanContext, TraceFlags
from sqlalchemy import select, update
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from redis.asyncio import Redis

from core.rate_limiter import BitrixRateLimiter
from core.bitrix_batch import execute_batch
from core import outbox

logger = logging.getLogger(__name__)


async def ping(ctx, message: str = "pong") -> str:
    logger.info("ping task received: %s", message)
    return message


def wait_operating_reset(retry_state):
    """
    Если пришла OPERATION_TIME_LIMIT — ждём до operating_reset_at.
    Иначе — экспоненциальная задержка (1, 2, 4 сек...).
    """
    exception = retry_state.outcome.exception()
    if exception is None:
        return wait_exponential(multiplier=1, min=1, max=30)(retry_state)

    error_msg = str(exception)
    if "OPERATION_TIME_LIMIT" in error_msg:
        match = re.search(r"reset_at:\s*(\d+)", error_msg)
        if match:
            reset_at = int(match.group(1))
            wait_seconds = max(1, reset_at - time.time() + 1)
            logger.warning("OPERATION_TIME_LIMIT: waiting %.0f sec until reset", wait_seconds)
            return wait_seconds

    return wait_exponential(multiplier=1, min=1, max=30)(retry_state)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_operating_reset,
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
async def process_outbox_task(ctx, task_id: str, payload: dict) -> dict:
    """Обработчик задачи из outbox с batch-оптимизацией.

    Вместо одной задачи берёт до 50 pending/enqueued-задач и отправляет их одним batch-запросом.
    """
    import uuid as _uuid
    from app.db import SessionLocal
    from app.models.outbox import TaskOutbox
    from app.config import settings

    # 1. Получить пачку задач и сразу пометить их processing
    async with SessionLocal() as session:
        result = await session.execute(
            select(TaskOutbox)
            .where(TaskOutbox.status.in_(["pending", "enqueued"]))
            .order_by(TaskOutbox.created_at)
            .limit(50)
            .with_for_update(skip_locked=True)
        )
        tasks = result.scalars().all()

        if not tasks:
            return {"ok": True, "processed": 0}

        # Сразу обновить статус на processing (в той же транзакции)
        task_ids = [t.id for t in tasks]
        await session.execute(
            update(TaskOutbox)
            .where(TaskOutbox.id.in_(task_ids))
            .values(status="processing", updated_at=datetime.now(timezone.utc))
        )
        await session.commit()

    # 2. Сформировать batch-команды
    commands = {}
    task_map = {}

    for i, task in enumerate(tasks):
        cmd_id = f"task_{i}"
        # В реальности: crm.item.add с полями из task.payload
        commands[cmd_id] = "user.get"
        task_map[cmd_id] = task.id

    # 3. Rate Limiter
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    limiter = BitrixRateLimiter(
        redis_client=redis,
        tenant_id=settings.tenant_id,
        rate_per_sec=2.0,
        capacity=5,
    )

    try:
        allowed = await limiter.wait_and_acquire(max_wait=30.0)
        if not allowed:
            logger.warning("rate_limiter: timeout waiting for token, task %s", task_id)
            raise TimeoutError("rate_limiter: could not acquire token")

        # 4. Отправить batch
        print(f">>> process_outbox_task: found {len(tasks)} tasks, commands={len(commands)}")
        logger.info("batch: sending %d tasks", len(commands))

        try:
            batch_result = await execute_batch(commands)

            # 5. Обновить статусы задач
            async with SessionLocal() as session:
                for cmd_id, task_id_db in task_map.items():
                    if cmd_id in batch_result.get("result_error", {}):
                        error_msg = batch_result["result_error"][cmd_id].get("error_description", "unknown")
                        await session.execute(
                            update(TaskOutbox)
                            .where(TaskOutbox.id == task_id_db)
                            .values(status="failed", last_error=error_msg[:2000], updated_at=datetime.now(timezone.utc))
                        )
                    else:
                        await session.execute(
                            update(TaskOutbox)
                            .where(TaskOutbox.id == task_id_db)
                            .values(status="done", updated_at=datetime.now(timezone.utc))
                        )
                await session.commit()

            logger.info("batch: processed %d tasks", len(commands))
            return {"ok": True, "processed": len(commands)}

        except Exception as e:
            logger.error("batch failed: %s", e)
            async with SessionLocal() as session:
                for task_id_db in task_map.values():
                    await session.execute(
                        update(TaskOutbox)
                        .where(TaskOutbox.id == task_id_db)
                        .values(status="failed", last_error=str(e)[:2000], updated_at=datetime.now(timezone.utc))
                    )
                await session.commit()
            raise

    finally:
        await redis.close()
