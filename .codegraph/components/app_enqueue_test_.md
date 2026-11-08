---
type: "component"
cohesion: 0.14
members_count: 7
---

# app (enqueue_test)

**Internal Cohesion:** 0.14 (density score)  
**Members count:** 7 nodes  

## Members
- [enqueue_test](../nodes/app_main_py_enqueue_test.md) (`function` in `app/main.py`)
- [get_task_status](../nodes/app_main_py_get_task_status.md) (`function` in `app/main.py`)
- [health](../nodes/app_main_py_health.md) (`function` in `app/main.py`)
- [health_db](../nodes/app_main_py_health_db.md) (`function` in `app/main.py`)
- [main.py](../nodes/app_main_py.md) (`file` in `app/main.py`)
- [queue_metrics](../nodes/app_main_py_queue_metrics.md) (`function` in `app/main.py`)
- [root](../nodes/app_main_py_root.md) (`function` in `app/main.py`)

## Component Dependencies

- Depends on [instrument_app](instrument_app.md) (3 calls/connections)
- Depends on [app (setup_logging)](app_setup_logging_.md) (2 calls/connections)
- Depends on [app (Base)](app_Base_.md) (1 calls/connections)
- Depends on [TaskOutbox](TaskOutbox.md) (1 calls/connections)
- Depends on [core (create_task)](core_create_task_.md) (1 calls/connections)
