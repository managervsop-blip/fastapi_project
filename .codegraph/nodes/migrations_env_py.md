---
id: "migrations/env.py"
label: "env.py"
type: "file"
source_file: "migrations/env.py"
line_start: 1
line_end: 64
component: "run_async_migrations"
---

# env.py

**Type:** `file`  
**File path:** `migrations/env.py`  
**Component:** run_async_migrations  

## Definition
```python
module env.py
```

## Contains Symbols
- [do_run_migrations](migrations_env_py_do_run_migrations.md) (`function`)
- [run_async_migrations](migrations_env_py_run_async_migrations.md) (`function`)

## Imports
- [config.py](app_config_py.md)
- [db.py](app_db_py.md)
- [__init__.py](app_models___init___py.md)

## Call Graph
```mermaid
flowchart TD
  migrations_env_py["env.py"] --> migrations_env_py__run_migrations_offline["run_migrations_offline"]
  migrations_env_py["env.py"] --> migrations_env_py__run_migrations_online["run_migrations_online"]
```

### Outgoing Calls
- Calls [run_migrations_offline](migrations_env_py_run_migrations_offline.md) (`function`)
- Calls [run_migrations_online](migrations_env_py_run_migrations_online.md) (`function`)
