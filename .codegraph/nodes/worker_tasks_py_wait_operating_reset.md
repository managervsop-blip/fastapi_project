---
id: "worker/tasks.py::wait_operating_reset"
label: "wait_operating_reset"
type: "function"
source_file: "worker/tasks.py"
line_start: 31
line_end: 63
component: "worker (process_outbox_task)"
---

# wait_operating_reset

**Type:** `function`  
**Defined in:** [worker/tasks.py](../nodes/worker_tasks_py.md) (Lines 31-63)  
**Component:** worker (process_outbox_task)  

## Definition
```python
def wait_operating_reset(retry_state)
```

## Description
Обработка ошибок лимитов Битрикс24.
    - OPERATION_TIME_LIMIT: ждём до operating_reset_at
    - QUERY_LIMIT_EXCEEDED: экспоненциальный backoff
    - QUERYTIMELIMITEXCEPTION: ждём Retry-After

**Contained in parent:** [tasks.py](worker_tasks_py.md) (`file`)
