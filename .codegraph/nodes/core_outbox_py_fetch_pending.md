---
id: "core/outbox.py::fetch_pending"
label: "fetch_pending"
type: "function"
source_file: "core/outbox.py"
line_start: 48
line_end: 57
component: "core (create_task)"
---

# fetch_pending

**Type:** `function`  
**Defined in:** [core/outbox.py](../nodes/core_outbox_py.md) (Lines 48-57)  
**Component:** core (create_task)  

## Definition
```python
async def fetch_pending(limit: int = 100) -> list[TaskOutbox]
```

## Description
Взять пачку pending-задач.

**Contained in parent:** [outbox.py](core_outbox_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  core_publisher_py__publish_pending["publish_pending"] --> core_outbox_py__fetch_pending["fetch_pending"]
```

### Incoming Calls (Backlinks)
- Called by [publish_pending](core_publisher_py_publish_pending.md) (`function`)
