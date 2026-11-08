import asyncio
import logging
import random
import re
import time
import uuid as _uuid
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

logger = logging.getLogger(__name__)


async def ping(ctx, message: str = "pong") -> str:
    logger.info("ping task received: %s", message)
    return message


def wait_operating_reset(retry_state):
    """
    Обработка ошибок лимитов Битрикс24.
    - OPERATION_TIME_LIMIT: ждём до operating_reset_at
    - QUERY_LIMIT_EXCEEDED: экспоненциальный backoff
    - QUERYTIMELIMITEXCEPTION: ждём Retry-After
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
            logger.warning("OPERATION_TIME_LIMIT: waiting %.0f sec", wait_seconds)
            return wait_seconds

    if "QUERYTIMELIMITEXCEPTION" in error_msg:
        match = re.search(r"retry_after:\s*(\d+)", error_msg)
        if match:
            wait_seconds = int(match.group(1))
            logger.warning("QUERYTIMELIMITEXCEPTION: waiting %d sec", wait_seconds)
            return wait_seconds

    if "QUERY_LIMIT_EXCEEDED" in error_msg:
        logger.warning("QUERY_LIMIT_EXCEEDED: exponential backoff")
        return wait_exponential(multiplier=1, min=1, max=30)(retry_state)

    return wait_exponential(multiplier=1, min=1, max=30)(retry_state)


async def requeue_stale_tasks(ctx):
    """Watchdog: возвращает зависшие processing-задачи в pending."""
    from app.db import SessionLocal
    from app.models.outbox import TaskOutbox
    from datetime import timedelta

    stale_threshold = datetime.now(timezone.utc) - timedelta(minutes=5)

    async with SessionLocal() as session:
        result = await session.execute(
            update(TaskOutbox)
            .where(
                TaskOutbox.status == "processing",
                TaskOutbox.processing_started_at < stale_threshold,
            )
            .values(
                status="pending",
                processing_started_at=None,
                updated_at=datetime.now(timezone.utc),
            )
        )
        count = result.rowcount
        await session.commit()

    if count > 0:
        logger.warning("watchdog: returned %d stale processing tasks to pending", count)
    return {"ok": True, "requeued": count}


@retry(
    stop=stop_after_attempt(5),
    wait=wait_operating_reset,
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
async def process_outbox_task(ctx, task_id: str, payload: dict) -> dict:
    """Обработчик задачи из outbox с batch-оптимизацией.

    Берет до 25 pending-задач, отправляет одним batch-запросом.
    Транзакции короткие (только БД), внешние вызовы вне транзакций.
    """
    from app.db import SessionLocal
    from app.models.outbox import TaskOutbox
    from app.config import settings

    # 0. Watchdog: разгребаем зависшие задачи
    await requeue_stale_tasks(ctx)

    # 1. КОРОТКАЯ транзакция: взять пачку и пометить processing
    async with SessionLocal() as session:
        result = await session.execute(
            select(TaskOutbox)
            .where(TaskOutbox.status.in_(["pending", "enqueued"]))
            .order_by(TaskOutbox.created_at)
            .limit(25)  # было 50 — уменьшено для избежания таймаута 60с
            .with_for_update(skip_locked=True)
        )
        tasks = result.scalars().all()

        if not tasks:
            return {"ok": True, "processed": 0}

        task_ids = [t.id for t in tasks]
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
    # ← Транзакция закрыта. Соединение возвращено в пул.

    # 2. Сформировать batch-команды (вне транзакции)
    commands = {}
    task_map = {}
    for i, task in enumerate(tasks):
        cmd_id = f"task_{i}"
        commands[cmd_id] = "user.get"
        task_map[cmd_id] = task.id

    # 3. Rate limiter (Redis, вне транзакции)
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    limiter = BitrixRateLimiter(
        redis_client=redis,
        tenant_id=settings.tenant_id,
        rate_per_sec=2.0,
        capacity=50,  # Leaky Bucket: burst до 50, долгосрочно 2/сек
    )

    try:
        # 3a. Ждём токен (короткий timeout, не 30 сек!)
        allowed = await limiter.wait_and_acquire(max_wait=5.0)
        if not allowed:
            logger.warning("rate_limiter: no token in 5s, returning %d tasks to pending", len(task_ids))
            async with SessionLocal() as session:
                await session.execute(
                    update(TaskOutbox)
                    .where(TaskOutbox.id.in_(task_ids))
                    .values(
                        status="pending",
                        processing_started_at=None,
                        updated_at=datetime.now(timezone.utc),
                    )
                )
                await session.commit()
            raise TimeoutError("rate_limiter: could not acquire token in 5s")

        # 4. HTTP в Битрикс (вне транзакции)
        print(f">>> process_outbox_task: found {len(tasks)} tasks, commands={len(commands)}")
        logger.info("batch: sending %d tasks", len(commands))

        try:
            batch_result = await execute_batch(commands)

            # 4a. Проверка накопленного времени (operating) — защита от OPERATION_TIME_LIMIT
            operating = batch_result.get("time", {}).get("operating", 0)
            reset_at = batch_result.get("time", {}).get("operating_reset_at", 0)
            if operating > 400 and reset_at > time.time():
                wait_sec = min(reset_at - time.time(), 300)  # не больше 5 минут
                logger.warning(
                    "operating=%s close to limit, waiting %.0f sec", operating, wait_sec
                )
                await asyncio.sleep(wait_sec)

            # 5. КОРОТКАЯ транзакция: обновить статусы
            done_ids = []
            failed_updates = []
            for cmd_id, task_id_db in task_map.items():
                if cmd_id in batch_result.get("result_error", {}):
                    error_msg = batch_result["result_error"][cmd_id].get(
                        "error_description", "unknown"
                    )
                    failed_updates.append({"id": task_id_db, "error": error_msg[:2000]})
                else:
                    done_ids.append(task_id_db)

            async with SessionLocal() as session:
                if done_ids:
                    await session.execute(
                        update(TaskOutbox)
                        .where(TaskOutbox.id.in_(done_ids))
                        .values(
                            status="done",
                            processing_started_at=None,
                            updated_at=datetime.now(timezone.utc),
                        )
                    )
                for f in failed_updates:
                    await session.execute(
                        update(TaskOutbox)
                        .where(TaskOutbox.id == f["id"])
                        .values(
                            status="failed",
                            last_error=f["error"],
                            processing_started_at=None,
                            updated_at=datetime.now(timezone.utc),
                        )
                    )
                await session.commit()

            logger.info("batch: processed %d tasks", len(commands))
            return {"ok": True, "processed": len(commands)}

        except Exception as e:
            # Ошибка Bitrix/сети — помечаем failed
            logger.error("batch failed: %s", e)
            async with SessionLocal() as session:
                await session.execute(
                    update(TaskOutbox)
                    .where(TaskOutbox.id.in_(task_ids))
                    .values(
                        status="failed",
                        last_error=str(e)[:2000],
                        processing_started_at=None,
                        updated_at=datetime.now(timezone.utc),
                    )
                )
                await session.commit()
            raise

    finally:
        await redis.close()
