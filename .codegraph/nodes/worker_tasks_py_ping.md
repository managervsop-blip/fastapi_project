---
id: "worker/tasks.py::ping"
label: "ping"
type: "function"
source_file: "worker/tasks.py"
line_start: 80
line_end: 82
component: "process_outbox_task"
---

# ping

**Type:** `function`  
**Defined in:** [worker/tasks.py](../nodes/worker_tasks_py.md) (Lines 80-82)  
**Component:** process_outbox_task  

## Definition
```python
async def ping(ctx, message: str = "pong") -> str
```

**Contained in parent:** [tasks.py](worker_tasks_py.md) (`file`)
