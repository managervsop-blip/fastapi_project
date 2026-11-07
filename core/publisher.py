import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update

from arq import create_pool
from arq.connections import RedisSettings

from app.config import settings
from app.db import SessionLocal
from app.models.outbox import TaskOutbox
from core import outbox

logger = logging.getLogger(__name__)

async def publish_pending(ctx=None, limit: int = 100) -> int:
    """Издатель: читает pending из outbox и кладёт в Redis.
    
    Также возвращает в pending задачи, которые зависли в enqueued > 5 минут.
    """
    # 1. Восстановить "зависшие" enqueued (если они висят > 5 минут)
    stale_threshold = datetime.now(timezone.utc) - timedelta(minutes=5)
    async with SessionLocal() as session:
        stale_result = await session.execute(
            update(TaskOutbox)
            .where(
                TaskOutbox.status == "enqueued",
                TaskOutbox.updated_at < stale_threshold,
            )
            .values(status="pending", updated_at=datetime.now(timezone.utc))
        )
        if stale_result.rowcount > 0:
            logger.warning("publisher: returned %d stale enqueued tasks to pending", stale_result.rowcount)
        await session.commit()

    # 2. Взять pending-задачи (как обычно)
    tasks = await outbox.fetch_pending(limit=limit)
    if not tasks:
        return 0

    # 3. Положить в Redis
    redis = await create_pool(RedisSettings.from_dsn(settings.redis_url))
    published = 0
    for task in tasks:
        try:
            await redis.enqueue_job(
                "process_outbox_task",
                str(task.id),
                task.payload,
                _job_id=str(task.id),
            )
            await outbox.mark_enqueued(task.id)
            published += 1
            logger.info("publisher: enqueued task %s", task.id)
        except Exception as e:
            logger.warning("publisher: failed to enqueue task %s: %s", task.id, e)
    await redis.close()
    return published
