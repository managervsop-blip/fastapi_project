---
id: "worker/tasks.py::requeue_stale_tasks"
label: "requeue_stale_tasks"
type: "function"
source_file: "worker/tasks.py"
line_start: 66
line_end: 92
component: "worker (process_outbox_task)"
---

# requeue_stale_tasks

**Type:** `function`  
**Defined in:** [worker/tasks.py](../nodes/worker_tasks_py.md) (Lines 66-92)  
**Component:** worker (process_outbox_task)  

## Definition
```python
async def requeue_stale_tasks(ctx)
```

## Description
Watchdog: возвращает зависшие processing-задачи в pending.

**Contained in parent:** [tasks.py](worker_tasks_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> worker_tasks_py__requeue_stale_tasks["requeue_stale_tasks"]
```

### Incoming Calls (Backlinks)
- Called by [process_outbox_task](worker_tasks_py_process_outbox_task.md) (`function`)
