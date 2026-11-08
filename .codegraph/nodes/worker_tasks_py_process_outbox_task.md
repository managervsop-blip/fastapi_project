---
id: "worker/tasks.py::process_outbox_task"
label: "process_outbox_task"
type: "function"
source_file: "worker/tasks.py"
line_start: 112
line_end: 211
component: "process_outbox_task"
---

# process_outbox_task

**Type:** `function`  
**Defined in:** [worker/tasks.py](../nodes/worker_tasks_py.md) (Lines 112-211)  
**Component:** process_outbox_task  

## Definition
```python
async def process_outbox_task(ctx, task_id: str, payload: dict) -> dict
```

## Description
Обработчик задачи из outbox с batch-оптимизацией.

    Вместо одной задачи берёт до 50 pending/enqueued-задач и отправляет их одним batch-запросом.

**Contained in parent:** [tasks.py](worker_tasks_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> app_models_outbox_py__TaskOutbox["TaskOutbox"]
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> core_bitrix_batch_py__execute_batch["execute_batch"]
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> core_rate_limiter_py__BitrixRateLimiter["BitrixRateLimiter"]
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> core_rate_limiter_py__BitrixRateLimiter_wait_and_acquire["wait_and_acquire"]
```

### Outgoing Calls
- Calls [TaskOutbox](app_models_outbox_py_TaskOutbox.md) (`class`)
- Calls [BitrixRateLimiter](core_rate_limiter_py_BitrixRateLimiter.md) (`class`)
- Calls [wait_and_acquire](core_rate_limiter_py_BitrixRateLimiter_wait_and_acquire.md) (`method`)
- Calls [execute_batch](core_bitrix_batch_py_execute_batch.md) (`function`)
