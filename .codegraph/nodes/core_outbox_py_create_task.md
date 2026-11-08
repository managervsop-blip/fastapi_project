---
id: "core/outbox.py::create_task"
label: "create_task"
type: "function"
source_file: "core/outbox.py"
line_start: 14
line_end: 45
component: "core (create_task)"
---

# create_task

**Type:** `function`  
**Defined in:** [core/outbox.py](../nodes/core_outbox_py.md) (Lines 14-45)  
**Component:** core (create_task)  

## Definition
```python
async def create_task(payload: dict, key: str | None = None) -> uuid.UUID | None
```

## Description
Записать задачу в outbox со статусом pending.

    Если key передан и уже существует — вернуть None (дубль, не создаём).
    Сохраняет trace_id текущего спана (для сквозной трассировки).

**Contained in parent:** [outbox.py](core_outbox_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  app_main_py__enqueue_test["enqueue_test"] --> core_outbox_py__create_task["create_task"]
  core_outbox_py__create_task["create_task"] --> app_models_idempotency_py__IdempotencyKey["IdempotencyKey"]
  core_outbox_py__create_task["create_task"] --> app_models_outbox_py__TaskOutbox["TaskOutbox"]
```

### Outgoing Calls
- Calls [TaskOutbox](app_models_outbox_py_TaskOutbox.md) (`class`)
- Calls [IdempotencyKey](app_models_idempotency_py_IdempotencyKey.md) (`class`)

### Incoming Calls (Backlinks)
- Called by [enqueue_test](app_main_py_enqueue_test.md) (`function`)
