---
type: "component"
cohesion: 0.25
members_count: 5
---

# worker (process_outbox_task)

**Internal Cohesion:** 0.25 (density score)  
**Members count:** 5 nodes  

## Members
- [ping](../nodes/worker_tasks_py_ping.md) (`function` in `worker/tasks.py`)
- [process_outbox_task](../nodes/worker_tasks_py_process_outbox_task.md) (`function` in `worker/tasks.py`)
- [requeue_stale_tasks](../nodes/worker_tasks_py_requeue_stale_tasks.md) (`function` in `worker/tasks.py`)
- [tasks.py](../nodes/worker_tasks_py.md) (`file` in `worker/tasks.py`)
- [wait_operating_reset](../nodes/worker_tasks_py_wait_operating_reset.md) (`function` in `worker/tasks.py`)

## Component Dependencies

- Depends on [core (BitrixRateLimiter)](core_BitrixRateLimiter_.md) (3 calls/connections)
- Depends on [core (execute_batch)](core_execute_batch_.md) (2 calls/connections)
- Depends on [TaskOutbox](TaskOutbox.md) (2 calls/connections)
- Depends on [app (Base)](app_Base_.md) (1 calls/connections)
- Depends on [instrument_app](instrument_app.md) (1 calls/connections)
