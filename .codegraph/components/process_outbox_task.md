---
type: "component"
cohesion: 0.2
members_count: 6
---

# process_outbox_task

**Internal Cohesion:** 0.2 (density score)  
**Members count:** 6 nodes  

## Members
- [bitrix_batch.py](../nodes/core_bitrix_batch_py.md) (`file` in `core/bitrix_batch.py`)
- [execute_batch](../nodes/core_bitrix_batch_py_execute_batch.md) (`function` in `core/bitrix_batch.py`)
- [ping](../nodes/worker_tasks_py_ping.md) (`function` in `worker/tasks.py`)
- [process_outbox_task](../nodes/worker_tasks_py_process_outbox_task.md) (`function` in `worker/tasks.py`)
- [tasks.py](../nodes/worker_tasks_py.md) (`file` in `worker/tasks.py`)
- [wait_operating_reset](../nodes/worker_tasks_py_wait_operating_reset.md) (`function` in `worker/tasks.py`)

## Component Dependencies

- Depends on [core (BitrixRateLimiter)](core_BitrixRateLimiter_.md) (3 calls/connections)
- Depends on [instrument_app](instrument_app.md) (2 calls/connections)
- Depends on [TaskOutbox](TaskOutbox.md) (2 calls/connections)
- Depends on [app (Base)](app_Base_.md) (1 calls/connections)
