---
id: "worker/tasks.py::retry_failed_tasks"
label: "retry_failed_tasks"
type: "function"
source_file: "worker/tasks.py"
line_start: 273
line_end: 337
component: "worker (process_outbox_task)"
---

# retry_failed_tasks

**Type:** `function`  
**Defined in:** [worker/tasks.py](../nodes/worker_tasks_py.md) (Lines 273-337)  
**Component:** worker (process_outbox_task)  

## Definition
```python
async def retry_failed_tasks(ctx)
```

## Description
Автоматический retry для упавших задач.
    
    Логика:
    - Первые 5 попыток: retry каждые 5 минут (быстрые сбои).
    - Следующие 20 попыток: retry каждые 30 минут (медленные сбои).
    - После 25 попыток: задача уходит в 'dead' (не удаляется, но не мешает).

**Contained in parent:** [tasks.py](worker_tasks_py.md) (`file`)
