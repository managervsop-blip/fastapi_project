---
id: "core/rate_limiter.py::BitrixRateLimiter.__init__"
label: "__init__"
type: "method"
source_file: "core/rate_limiter.py"
line_start: 53
line_end: 64
component: "core (BitrixRateLimiter)"
---

# __init__

**Type:** `method`  
**Defined in:** [core/rate_limiter.py](../nodes/core_rate_limiter_py.md) (Lines 53-64)  
**Component:** core (BitrixRateLimiter)  

## Definition
```python
def __init__(
        self,
        redis_client: Redis,
        tenant_id: str = "client_1",
        rate_per_sec: float = 2.0,  # 2 RPS для базового, 5 для Энтерпрайза
        capacity: int = 5,           # всплеск до 5 запросов
    )
```

**Contained in parent:** [BitrixRateLimiter](core_rate_limiter_py_BitrixRateLimiter.md) (`class`)
