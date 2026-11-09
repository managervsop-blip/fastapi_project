---
type: "component"
cohesion: 0.2
members_count: 6
---

# worker (process_outbox_task)

**Internal Cohesion:** 0.2 (density score)  
**Members count:** 6 nodes  

## Members
- [ping](../nodes/worker_tasks_py_ping.md) (`function` in `worker/tasks.py`)
- [process_outbox_task](../nodes/worker_tasks_py_process_outbox_task.md) (`function` in `worker/tasks.py`)
- [requeue_stale_tasks](../nodes/worker_tasks_py_requeue_stale_tasks.md) (`function` in `worker/tasks.py`)
- [retry_failed_tasks](../nodes/worker_tasks_py_retry_failed_tasks.md) (`function` in `worker/tasks.py`)
- [tasks.py](../nodes/worker_tasks_py.md) (`file` in `worker/tasks.py`)
- [wait_operating_reset](../nodes/worker_tasks_py_wait_operating_reset.md) (`function` in `worker/tasks.py`)

## Component Dependencies

- Depends on [TaskOutbox](TaskOutbox.md) (5 calls/connections)
- Depends on [core (BitrixRateLimiter)](core_BitrixRateLimiter_.md) (3 calls/connections)
- Depends on [core (execute_batch)](core_execute_batch_.md) (2 calls/connections)
