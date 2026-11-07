import asyncio 
import time
import logging
from redis.asyncio import Redis

logger = logging.getLogger(__name__)

# Lua-скрипт для атомарного Token Bucket
# KEYS[1] - ключ (например, "b24:rate:client_1")
# ARGV[1] - capacity (макс. токенов, например 5)
# ARGV[2] - refill_rate (токенов в секунду, например 2)
# ARGV[3] - now (текущий timestamp)
TOKEN_BUCKET_SCRIPT = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(bucket[1])
local last_refill = tonumber(bucket[2])

if tokens == nil then
    tokens = capacity
    last_refill = now
end

local time_passed = now - last_refill
local refills = math.floor(time_passed * refill_rate)

if refills > 0 then
    tokens = math.min(capacity, tokens + refills)
    last_refill = now
end

local allowed = 0
if tokens >= 1 then
    tokens = tokens - 1
    allowed = 1
end

redis.call('HMSET', key, 'tokens', tokens, 'last_refill', last_refill)
-- TTL, чтобы ключи не копились (например, 1 час)
redis.call('EXPIRE', key, 3600)

return {allowed, tokens}
"""


class BitrixRateLimiter:
    """Ограничитель скорости для запросов к Битрикс24."""

    def __init__(
        self,
        redis_client: Redis,
        tenant_id: str = "client_1",
        rate_per_sec: float = 2.0,  # 2 RPS для базового, 5 для Энтерпрайза
        capacity: int = 5,           # всплеск до 5 запросов
    ):
        self.redis = redis_client
        self.key_prefix = f"b24:rate:{tenant_id}"
        self.rate = rate_per_sec
        self.capacity = capacity
        self._script_sha = None

    async def acquire(self) -> bool:
        """Попытаться получить разрешение на запрос.
        Возвращает True, если можно выполнять, False — если нужно подождать.
        """
        now = time.time()
        key = self.key_prefix

        try:
            # Используем EVALSHA для кеширования скрипта
            if self._script_sha is None:
                self._script_sha = await self.redis.script_load(TOKEN_BUCKET_SCRIPT)

            result = await self.redis.evalsha(
                self._script_sha, 1, key, self.capacity, self.rate, now
            )
        except Exception as e:
            # Если скрипт не загружен (например, Redis перезапустился), загружаем заново
            logger.warning("rate_limiter: script error, reloading: %s", e)
            self._script_sha = await self.redis.script_load(TOKEN_BUCKET_SCRIPT)
            result = await self.redis.evalsha(
                self._script_sha, 1, key, self.capacity, self.rate, now
            )

        allowed = result[0] == 1
        remaining = result[1]

        if not allowed:
            logger.debug("rate_limiter: blocked, remaining=%.2f", remaining)

        return allowed

    async def wait_and_acquire(self, max_wait: float = 30.0) -> bool:
        """Ждать, пока не появится токен (с ограничением по времени)."""
        start = time.time()
        while time.time() - start < max_wait:
            if await self.acquire():
                return True
            # Ждём примерно время, за которое накопится 1 токен
            wait_time = 1.0 / self.rate
            await asyncio.sleep(wait_time)
        return False
