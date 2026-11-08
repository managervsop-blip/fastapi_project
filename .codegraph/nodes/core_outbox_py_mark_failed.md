---
id: "core/outbox.py::mark_failed"
label: "mark_failed"
type: "function"
source_file: "core/outbox.py"
line_start: 98
line_end: 111
component: "core (create_task)"
---

# mark_failed

**Type:** `function`  
**Defined in:** [core/outbox.py](../nodes/core_outbox_py.md) (Lines 98-111)  
**Component:** core (create_task)  

## Definition
```python
async def mark_failed(task_id: uuid.UUID, error: str) -> None
```

## Description
Отметить, что задача упала, и сохранить текст ошибки.

**Contained in parent:** [outbox.py](core_outbox_py.md) (`file`)
