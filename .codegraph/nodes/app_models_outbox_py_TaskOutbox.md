---
id: "app/models/outbox.py::TaskOutbox"
label: "TaskOutbox"
type: "class"
source_file: "app/models/outbox.py"
line_start: 11
line_end: 29
component: "TaskOutbox"
---

# TaskOutbox

**Type:** `class`  
**Defined in:** [app/models/outbox.py](../nodes/app_models_outbox_py.md) (Lines 11-29)  
**Component:** TaskOutbox  

## Definition
```python
class TaskOutbox(Base)
```

**Contained in parent:** [outbox.py](app_models_outbox_py.md) (`file`)

## Inherits / Implements
- [Base](app_db_py_Base.md) (`class`)

## Call Graph
```mermaid
flowchart TD
  core_outbox_py__create_task["create_task"] --> app_models_outbox_py__TaskOutbox["TaskOutbox"]
  core_outbox_py__mark_processing["mark_processing"] --> app_models_outbox_py__TaskOutbox["TaskOutbox"]
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> app_models_outbox_py__TaskOutbox["TaskOutbox"]
```

### Incoming Calls (Backlinks)
- Called by [create_task](core_outbox_py_create_task.md) (`function`)
- Called by [mark_processing](core_outbox_py_mark_processing.md) (`function`)
- Called by [process_outbox_task](worker_tasks_py_process_outbox_task.md) (`function`)
