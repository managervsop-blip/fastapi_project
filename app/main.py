from fastapi import FastAPI, HTTPException, Response
from sqlalchemy import text, select, func
import uuid

from app.db import SessionLocal
from app.models.outbox import TaskOutbox
from core import outbox

from app.telemetry import setup_tracing, instrument_app

from app.logging_config import setup_logging
setup_logging()

from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title="Bitrix24 Integration")

# --- OpenTelemetry ---
setup_tracing()
instrument_app(app)

# Метрики FastAPI (RPS, latency, errors)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
# ---------------------


# ============================================================
# Health checks
# ============================================================

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
async def health_db():
    try:
        async with SessionLocal() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"DB error: {e}")


@app.get("/")
def root():
    return {"message": "FastAPI project is running"}


# ============================================================
# Test endpoints (для нагрузочного теста)
# ============================================================

@app.post("/test/enqueue")
async def enqueue_test(key: str | None = None):
    task_id = await outbox.create_task(
        {"type": "ping", "message": "hello from FastAPI"},
        key=key,
    )
    if task_id is None:
        return {"status": "duplicate", "message": "task with this key already exists"}
    return {"task_id": str(task_id), "status": "pending"}


@app.get("/test/status/{task_id}")
async def get_task_status(task_id: str):
    """Проверка статуса задачи для end-to-end нагрузочного теста."""
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task_id format")

    async with SessionLocal() as session:
        result = await session.execute(
            select(TaskOutbox).where(TaskOutbox.id == task_uuid)
        )
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "id": str(task.id),
            "status": task.status,
            "last_error": task.last_error,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "processing_started_at": (
                task.processing_started_at.isoformat()
                if task.processing_started_at else None
            ),
        }


# ============================================================
# Metrics
# ============================================================

@app.get("/metrics/queue")
async def queue_metrics():
    """Метрики очереди в формате Prometheus."""
    async with SessionLocal() as session:
        pending = await session.scalar(
            select(func.count()).where(TaskOutbox.status == "pending")
        )
        enqueued = await session.scalar(
            select(func.count()).where(TaskOutbox.status == "enqueued")
        )
        done = await session.scalar(
            select(func.count()).where(TaskOutbox.status == "done")
        )
        failed = await session.scalar(
            select(func.count()).where(TaskOutbox.status == "failed")
        )
        processing = await session.scalar(
            select(func.count()).where(TaskOutbox.status == "processing")
        )

    lines = [
        "# HELP tasks_outbox_count Количество задач по статусам",
        "# TYPE tasks_outbox_count gauge",
        f'tasks_outbox_count{{status="pending"}} {pending}',
        f'tasks_outbox_count{{status="enqueued"}} {enqueued}',
        f'tasks_outbox_count{{status="done"}} {done}',
        f'tasks_outbox_count{{status="failed"}} {failed}',
        f'tasks_outbox_count{{status="processing"}} {processing}',
    ]
    return Response(content="\n".join(lines), media_type="text/plain")
