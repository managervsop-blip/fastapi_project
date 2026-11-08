---
id: "app/main.py::enqueue_test"
label: "enqueue_test"
type: "function"
source_file: "app/main.py"
line_start: 57
line_end: 64
component: "app (enqueue_test)"
---

# enqueue_test

**Type:** `function`  
**Defined in:** [app/main.py](../nodes/app_main_py.md) (Lines 57-64)  
**Component:** app (enqueue_test)  

## Definition
```python
async def enqueue_test(key: str | None = None)
```

**Contained in parent:** [main.py](app_main_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  app_main_py__enqueue_test["enqueue_test"] --> core_outbox_py__create_task["create_task"]
```

### Outgoing Calls
- Calls [create_task](core_outbox_py_create_task.md) (`function`)
