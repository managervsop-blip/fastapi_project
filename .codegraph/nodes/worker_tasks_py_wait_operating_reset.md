---
id: "worker/tasks.py::wait_operating_reset"
label: "wait_operating_reset"
type: "function"
source_file: "worker/tasks.py"
line_start: 85
line_end: 103
component: "process_outbox_task"
---

# wait_operating_reset

**Type:** `function`  
**Defined in:** [worker/tasks.py](../nodes/worker_tasks_py.md) (Lines 85-103)  
**Component:** process_outbox_task  

## Definition
```python
def wait_operating_reset(retry_state)
```

## Description
Если пришла OPERATION_TIME_LIMIT — ждём до operating_reset_at.
    Иначе — экспоненциальная задержка (1, 2, 4 сек...).

**Contained in parent:** [tasks.py](worker_tasks_py.md) (`file`)
