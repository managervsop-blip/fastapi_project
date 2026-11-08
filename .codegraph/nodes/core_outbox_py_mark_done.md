---
id: "core/outbox.py::mark_done"
label: "mark_done"
type: "function"
source_file: "core/outbox.py"
line_start: 87
line_end: 95
component: "core (create_task)"
---

# mark_done

**Type:** `function`  
**Defined in:** [core/outbox.py](../nodes/core_outbox_py.md) (Lines 87-95)  
**Component:** core (create_task)  

## Definition
```python
async def mark_done(task_id: uuid.UUID) -> None
```

## Description
Отметить, что задача выполнена.

**Contained in parent:** [outbox.py](core_outbox_py.md) (`file`)
