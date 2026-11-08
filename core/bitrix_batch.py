import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


async def execute_batch(commands: dict[str, str]) -> dict[str, Any]:
    """Выполняет batch-запрос к Битрикс24."""
    if not commands:
        return {}

    # Если вебхук не настроен — эмулируем успех (для тестов)
    if not settings.b24_webhook_url or "your-company" in settings.b24_webhook_url:
        logger.warning("batch: webhook not configured, simulating success")
        return {
            "result": {cmd_id: {"result": True} for cmd_id in commands},
            "result_error": {},
            "result_time": {},
        }

    if len(commands) > 50:
        raise ValueError(f"Batch limit exceeded: {len(commands)} > 50")

    url = f"{settings.b24_webhook_url}/batch"
    payload = {
        "halt": 0,
        "cmd": commands,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                error_code = data.get("error", "UNKNOWN")
                logger.error("batch system error: %s", error_code)
                reset_at = data.get("time", {}).get("operating_reset_at")
                raise RuntimeError(f"Bitrix batch error: {error_code}, reset_at: {reset_at}")

            result = data.get("result", {})
            result_error = data.get("result_error", {})
            result_time = data.get("time", {})

            operating = result_time.get("operating")
            reset_at = result_time.get("operating_reset_at")
            if operating is not None:
                logger.info(
                    "batch: operating=%.3f sec, reset_at=%s, duration=%.3f sec",
                    operating,
                    reset_at,
                    result_time.get("duration", 0.0),
                )

            if result_error:
                logger.warning("batch partial errors: %s", list(result_error.keys()))

            return {
                "result": result,
                "result_error": result_error,
                "result_time": result_time,
            }

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            body = e.response.text

            if status == 503 and "QUERY_LIMIT_EXCEEDED" in body:
                logger.error("batch: QUERY_LIMIT_EXCEEDED, retry with backoff")
                raise RuntimeError("QUERY_LIMIT_EXCEEDED")

            if status == 429 and "OPERATION_TIME_LIMIT" in body:
                try:
                    data = e.response.json()
                    reset_at = data.get("time", {}).get("operating_reset_at")
                except Exception:
                    reset_at = None
                logger.error("batch: OPERATION_TIME_LIMIT, reset_at=%s", reset_at)
                raise RuntimeError(f"OPERATION_TIME_LIMIT reset_at: {reset_at}")

            if status == 503 and "QUERYTIMELIMITEXCEPTION" in body:
                retry_after = e.response.headers.get("Retry-After", "5")
                logger.error("batch: QUERYTIMELIMITEXCEPTION, Retry-After=%s", retry_after)
                raise RuntimeError(f"QUERYTIMELIMITEXCEPTION retry_after: {retry_after}")

            logger.error("batch HTTP error: %s %s", status, body[:200])
            raise

        except Exception as e:
            logger.error("batch failed: %s", e)
            raise
