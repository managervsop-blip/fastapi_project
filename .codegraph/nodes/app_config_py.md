---
id: "app/config.py"
label: "config.py"
type: "file"
source_file: "app/config.py"
line_start: 1
line_end: 28
component: "TaskOutbox"
---

# config.py

**Type:** `file`  
**File path:** `app/config.py`  
**Component:** TaskOutbox  

## Definition
```python
module config.py
```

## Imported By
- [telemetry.py](app_telemetry_py.md)
- [db.py](app_db_py.md)
- [publisher.py](core_publisher_py.md)
- [env.py](migrations_env_py.md)
- [settings.py](worker_settings_py.md)
- [tasks.py](worker_tasks_py.md)

## Call Graph
```mermaid
flowchart TD
  app_config_py["config.py"] --> app_config_py__Settings["Settings"]
```

### Outgoing Calls
- Calls [Settings](app_config_py_Settings.md) (`class`)
