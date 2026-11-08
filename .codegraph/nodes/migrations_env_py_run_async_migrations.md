---
id: "migrations/env.py::run_async_migrations"
label: "run_async_migrations"
type: "function"
source_file: "migrations/env.py"
line_start: 44
line_end: 54
component: "run_async_migrations"
---

# run_async_migrations

**Type:** `function`  
**Defined in:** [migrations/env.py](../nodes/migrations_env_py.md) (Lines 44-54)  
**Component:** run_async_migrations  

## Definition
```python
async def run_async_migrations() -> None
```

**Contained in parent:** [env.py](migrations_env_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  migrations_env_py__run_migrations_online["run_migrations_online"] --> migrations_env_py__run_async_migrations["run_async_migrations"]
```

### Incoming Calls (Backlinks)
- Called by [run_migrations_online](migrations_env_py_run_migrations_online.md) (`function`)
