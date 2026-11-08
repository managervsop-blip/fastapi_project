# core/bitrix_batch.py (Имитация реального Bitrix)
import asyncio
import time
import random

# Глобальные переменные для имитации состояния Bitrix
# (В реальном приложении это было бы в Redis, но для теста сойдет и память)
bitrix_state = {
    "tokens": 50,           # Начальный запас токенов (всплеск)
    "last_refill": time.time(),
    "operating_time": {},   # { "method_name": накопленное_время }
}

async def execute_batch(commands):
    now = time.time()
    method_name = "crm.item.add" # Предположим, мы шлем этот метод
    
    # 1. Имитация Leaky Bucket (Восстановление токенов)
    elapsed = now - bitrix_state["last_refill"]
    bitrix_state["tokens"] = min(50, bitrix_state["tokens"] + elapsed * 2) # 2 токена/сек
    bitrix_state["last_refill"] = now
    
    # 2. Проверка интенсивности
    if bitrix_state["tokens"] < 1:
        raise Exception("QUERY_LIMIT_EXCEEDED: retry_after: 2")
    
    bitrix_state["tokens"] -= 1 # Тратим токен
    
    # 3. Имитация РЕАЛЬНОЙ задержки Bitrix (1-5 секунд на batch)
    # Чем больше задач в batch, тем дольше (примерно)
    simulated_delay = random.uniform(1.0, 3.0) + (len(commands) * 0.05)
    print(f"[Mock Bitrix] Выполняю {method_name} (задач: {len(commands)}). Задержка: {simulated_delay:.2f}с")
    await asyncio.sleep(simulated_delay)
    
    # 4. Проверка таймаута 60 секунд (если задержка была бы huge)
    if simulated_delay > 60:
        raise Exception("Timeout: Request took longer than 60s")
    
    # 5. Имитация накопления operating (Ресурсоемкость)
    current_op = bitrix_state["operating_time"].get(method_name, 0)
    # В реальности operating растет от времени выполнения метода на сервере,
    # а не от задержки сети. Но для симуляции возьмем долю от задержки.
    added_op = simulated_delay * 2 # Имитируем, что метод "тяжелый"
    bitrix_state["operating_time"][method_name] = current_op + added_op
    
    if bitrix_state["operating_time"][method_name] > 400: # Близко к лимиту
        print(f"[Mock Bitrix] ⚠️ OPERATING WARNING: {bitrix_state['operating_time'][method_name]:.0f}/480 сек")
    
    if bitrix_state["operating_time"][method_name] > 480:
        # Сбрасываем, чтобы не блокировать навсегда в тесте (в реальности блок на 10 мин)
        bitrix_state["operating_time"][method_name] = 0 
        raise Exception("OPERATION_TIME_LIMIT: reset_at: " + str(int(time.time() + 600)))

    # 6. Имитация случайных ошибок Bitrix (1% шанс)
    if random.random() < 0.01:
        raise Exception("Internal Server Error (Bitrix 500)")

    # 7. Успешный ответ
    return {
        "result": {f"task_{i}": "ok" for i in range(len(commands))},
        "time": {
            "operating": bitrix_state["operating_time"][method_name],
            "operating_reset_at": int(time.time()) + 600,
        }
    }
