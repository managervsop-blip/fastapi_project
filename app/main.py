from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.db import SessionLocal
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


@app.post("/test/enqueue")
async def enqueue_test(key: str | None = None):
    task_id = await outbox.create_task(
        {"type": "ping", "message": "hello from FastAPI"},
        key=key,
    )
    if task_id is None:
        return {"status": "duplicate", "message": "task with this key already exists"}
    return {"task_id": str(task_id), "status": "pending"}
from fastapi import Response
from sqlalchemy import select, func
from app.models.outbox import TaskOutbox

@app.get("/metrics/queue")
async def queue_metrics():
    """Метрики очереди в формате Prometheus."""
    async with SessionLocal() as session:
        pending = await session.scalar(select(func.count()).where(TaskOutbox.status == "pending"))
        enqueued = await session.scalar(select(func.count()).where(TaskOutbox.status == "enqueued"))
        done = await session.scalar(select(func.count()).where(TaskOutbox.status == "done"))
        failed = await session.scalar(select(func.count()).where(TaskOutbox.status == "failed"))

    lines = [
        "# HELP tasks_outbox_count Количество задач по статусам",
        "# TYPE tasks_outbox_count gauge",
        f'tasks_outbox_count{{status="pending"}} {pending}',
        f'tasks_outbox_count{{status="enqueued"}} {enqueued}',
        f'tasks_outbox_count{{status="done"}} {done}',
        f'tasks_outbox_count{{status="failed"}} {failed}',
    ]
    return Response(content="\n".join(lines), media_type="text/plain")
