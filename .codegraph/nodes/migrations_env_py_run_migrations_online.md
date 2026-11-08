---
id: "migrations/env.py::run_migrations_online"
label: "run_migrations_online"
type: "function"
source_file: "migrations/env.py"
line_start: 57
line_end: 58
component: "run_async_migrations"
---

# run_migrations_online

**Type:** `function`  
**Defined in:** [migrations/env.py](../nodes/migrations_env_py.md) (Lines 57-58)  
**Component:** run_async_migrations  

## Definition
```python
def run_migrations_online() -> None
```

## Call Graph
```mermaid
flowchart TD
  migrations_env_py["env.py"] --> migrations_env_py__run_migrations_online["run_migrations_online"]
  migrations_env_py__run_migrations_online["run_migrations_online"] --> migrations_env_py__run_async_migrations["run_async_migrations"]
```

### Outgoing Calls
- Calls [run_async_migrations](migrations_env_py_run_async_migrations.md) (`function`)

### Incoming Calls (Backlinks)
- Called by [env.py](migrations_env_py.md) (`file`)
