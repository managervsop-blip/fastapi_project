---
id: "worker/tasks.py"
label: "tasks.py"
type: "file"
source_file: "worker/tasks.py"
line_start: 1
line_end: 337
component: "worker (process_outbox_task)"
---

# tasks.py

**Type:** `file`  
**File path:** `worker/tasks.py`  
**Component:** worker (process_outbox_task)  

## Definition
```python
module tasks.py
```

## Contains Symbols
- [ping](worker_tasks_py_ping.md) (`function`)
- [wait_operating_reset](worker_tasks_py_wait_operating_reset.md) (`function`)
- [requeue_stale_tasks](worker_tasks_py_requeue_stale_tasks.md) (`function`)
- [process_outbox_task](worker_tasks_py_process_outbox_task.md) (`function`)
- [retry_failed_tasks](worker_tasks_py_retry_failed_tasks.md) (`function`)

## Imports
- [rate_limiter.py](core_rate_limiter_py.md)
- [bitrix_batch.py](core_bitrix_batch_py.md)
- [db.py](app_db_py.md)
- [outbox.py](app_models_outbox_py.md)
- [config.py](app_config_py.md)

## Imported By
- [settings.py](worker_settings_py.md)
