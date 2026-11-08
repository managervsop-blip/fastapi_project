---
id: "app/models/idempotency.py::IdempotencyKey"
label: "IdempotencyKey"
type: "class"
source_file: "app/models/idempotency.py"
line_start: 11
line_end: 20
component: "app (Base)"
---

# IdempotencyKey

**Type:** `class`  
**Defined in:** [app/models/idempotency.py](../nodes/app_models_idempotency_py.md) (Lines 11-20)  
**Component:** app (Base)  

## Definition
```python
class IdempotencyKey(Base)
```

**Contained in parent:** [idempotency.py](app_models_idempotency_py.md) (`file`)

## Inherits / Implements
- [Base](app_db_py_Base.md) (`class`)

## Call Graph
```mermaid
flowchart TD
  core_outbox_py__create_task["create_task"] --> app_models_idempotency_py__IdempotencyKey["IdempotencyKey"]
```

### Incoming Calls (Backlinks)
- Called by [create_task](core_outbox_py_create_task.md) (`function`)
