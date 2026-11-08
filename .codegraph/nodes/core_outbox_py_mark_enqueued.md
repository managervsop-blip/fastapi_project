---
id: "core/outbox.py::mark_enqueued"
label: "mark_enqueued"
type: "function"
source_file: "core/outbox.py"
line_start: 60
line_end: 68
component: "core (create_task)"
---

# mark_enqueued

**Type:** `function`  
**Defined in:** [core/outbox.py](../nodes/core_outbox_py.md) (Lines 60-68)  
**Component:** core (create_task)  

## Definition
```python
async def mark_enqueued(task_id: uuid.UUID) -> None
```

## Description
Отметить, что задача положена в Redis.

**Contained in parent:** [outbox.py](core_outbox_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  core_publisher_py__publish_pending["publish_pending"] --> core_outbox_py__mark_enqueued["mark_enqueued"]
```

### Incoming Calls (Backlinks)
- Called by [publish_pending](core_publisher_py_publish_pending.md) (`function`)
