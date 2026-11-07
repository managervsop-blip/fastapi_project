import logging

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from app.config import settings

logger = logging.getLogger(__name__)


def setup_tracing(service_name: str = "fastapi-project"):
    """Настраивает TracerProvider и отправляет спаны в OTel Collector."""
    tenant_id = getattr(settings, "tenant_id", "client_1")

    resource = Resource.create({
        "service.name": service_name,
        "tenant.id": tenant_id,
    })
    provider = TracerProvider(resource=resource)

    # Отправлять в Collector (OTLP gRPC на localhost:4317)
    exporter = OTLPSpanExporter(
        endpoint="http://localhost:4317",
        insecure=True,
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)
    logger.info("tracing: OTLP exporter enabled (service=%s, tenant=%s)", service_name, tenant_id)


def instrument_app(app):
    """Подключает автоинструментацию FastAPI, httpx, SQLAlchemy."""
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        FastAPIInstrumentor.instrument_app(app, excluded_urls="health,health/db")
        logger.info("tracing: FastAPI instrumented")
    except ImportError:
        logger.warning("tracing: FastAPI instrumentor not available")

    try:
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
        HTTPXClientInstrumentor().instrument()
        logger.info("tracing: httpx instrumented")
    except ImportError:
        logger.warning("tracing: httpx instrumentor not available")

    try:
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
        logger.info("tracing: SQLAlchemy instrumentor ready (deferred)")
    except ImportError:
        logger.warning("tracing: SQLAlchemy instrumentor not available")
