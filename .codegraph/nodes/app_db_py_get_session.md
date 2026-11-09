---
id: "app/db.py::get_session"
label: "get_session"
type: "function"
source_file: "app/db.py"
line_start: 33
line_end: 35
component: "TaskOutbox"
---

# get_session

**Type:** `function`  
**Defined in:** [app/db.py](../nodes/app_db_py.md) (Lines 33-35)  
**Component:** TaskOutbox  

## Definition
```python
async def get_session() -> AsyncGenerator[AsyncSession, None]
```

**Contained in parent:** [db.py](app_db_py.md) (`file`)
