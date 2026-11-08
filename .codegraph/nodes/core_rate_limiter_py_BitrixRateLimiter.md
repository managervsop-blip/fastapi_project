---
id: "core/rate_limiter.py::BitrixRateLimiter"
label: "BitrixRateLimiter"
type: "class"
source_file: "core/rate_limiter.py"
line_start: 50
line_end: 106
component: "core (BitrixRateLimiter)"
---

# BitrixRateLimiter

**Type:** `class`  
**Defined in:** [core/rate_limiter.py](../nodes/core_rate_limiter_py.md) (Lines 50-106)  
**Component:** core (BitrixRateLimiter)  

## Definition
```python
class BitrixRateLimiter
```

## Description
Ограничитель скорости для запросов к Битрикс24.

**Contained in parent:** [rate_limiter.py](core_rate_limiter_py.md) (`file`)

## Contains Symbols
- [__init__](core_rate_limiter_py_BitrixRateLimiter___init__.md) (`method`)
- [acquire](core_rate_limiter_py_BitrixRateLimiter_acquire.md) (`method`)
- [wait_and_acquire](core_rate_limiter_py_BitrixRateLimiter_wait_and_acquire.md) (`method`)

## Call Graph
```mermaid
flowchart TD
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> core_rate_limiter_py__BitrixRateLimiter["BitrixRateLimiter"]
```

### Incoming Calls (Backlinks)
- Called by [process_outbox_task](worker_tasks_py_process_outbox_task.md) (`function`)
