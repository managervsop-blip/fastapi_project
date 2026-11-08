---
id: "core/outbox.py::mark_processing"
label: "mark_processing"
type: "function"
source_file: "core/outbox.py"
line_start: 71
line_end: 85
component: "core (create_task)"
---

# mark_processing

**Type:** `function`  
**Defined in:** [core/outbox.py](../nodes/core_outbox_py.md) (Lines 71-85)  
**Component:** core (create_task)  

## Definition
```python
async def mark_processing(task_ids: list[uuid.UUID]) -> None
```

**Contained in parent:** [outbox.py](core_outbox_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  core_outbox_py__mark_processing["mark_processing"] --> app_models_outbox_py__TaskOutbox["TaskOutbox"]
```

### Outgoing Calls
- Calls [TaskOutbox](app_models_outbox_py_TaskOutbox.md) (`class`)
