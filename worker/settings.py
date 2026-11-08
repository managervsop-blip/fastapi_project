from arq import cron
from arq.connections import RedisSettings

from app.config import settings
from app.logging_config import setup_logging  # ← добавьте это
setup_logging(level="DEBUG")
from core.publisher import publish_pending
from worker.tasks import ping, process_outbox_task, requeue_stale_tasks
from app.telemetry import setup_tracing

# Сначала логирование, чтобы видеть INFO-логи, потом трейсинг
setup_logging()  # ← добавьте это
setup_tracing(service_name="fastapi-worker")

class WorkerSettings:
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    functions = [ping, publish_pending, process_outbox_task, requeue_stale_tasks]
    cron_jobs = [
        # Издатель (pending -> Redis)
        cron(
            publish_pending,
            second={
                0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30,
                32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58,
            },
        ),
        # Watchdog (processing -> pending, каждые 5 минут)
        cron(
            requeue_stale_tasks,
            minute={0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55},
        ),
    ]
