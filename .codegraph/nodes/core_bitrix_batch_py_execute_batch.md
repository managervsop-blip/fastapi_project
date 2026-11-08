---
id: "core/bitrix_batch.py::execute_batch"
label: "execute_batch"
type: "function"
source_file: "core/bitrix_batch.py"
line_start: 11
line_end: 96
component: "core (execute_batch)"
---

# execute_batch

**Type:** `function`  
**Defined in:** [core/bitrix_batch.py](../nodes/core_bitrix_batch_py.md) (Lines 11-96)  
**Component:** core (execute_batch)  

## Definition
```python
async def execute_batch(commands: dict[str, str]) -> dict[str, Any]
```

## Description
Выполняет batch-запрос к Битрикс24.

**Contained in parent:** [bitrix_batch.py](core_bitrix_batch_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  worker_tasks_py__process_outbox_task["process_outbox_task"] --> core_bitrix_batch_py__execute_batch["execute_batch"]
```

### Incoming Calls (Backlinks)
- Called by [process_outbox_task](worker_tasks_py_process_outbox_task.md) (`function`)
