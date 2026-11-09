---
type: "component"
cohesion: 0.14
members_count: 7
---

# core (create_task)

**Internal Cohesion:** 0.14 (density score)  
**Members count:** 7 nodes  

## Members
- [create_task](../nodes/core_outbox_py_create_task.md) (`function` in `core/outbox.py`)
- [fetch_pending](../nodes/core_outbox_py_fetch_pending.md) (`function` in `core/outbox.py`)
- [mark_done](../nodes/core_outbox_py_mark_done.md) (`function` in `core/outbox.py`)
- [mark_enqueued](../nodes/core_outbox_py_mark_enqueued.md) (`function` in `core/outbox.py`)
- [mark_failed](../nodes/core_outbox_py_mark_failed.md) (`function` in `core/outbox.py`)
- [mark_processing](../nodes/core_outbox_py_mark_processing.md) (`function` in `core/outbox.py`)
- [outbox.py](../nodes/core_outbox_py.md) (`file` in `core/outbox.py`)

## Component Dependencies

- Depends on [TaskOutbox](TaskOutbox.md) (4 calls/connections)
- Depends on [app/models (IdempotencyKey)](app_models_IdempotencyKey_.md) (2 calls/connections)
