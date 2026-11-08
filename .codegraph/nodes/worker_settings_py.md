---
id: "worker/settings.py"
label: "settings.py"
type: "file"
source_file: "worker/settings.py"
line_start: 1
line_end: 27
component: "instrument_app"
---

# settings.py

**Type:** `file`  
**File path:** `worker/settings.py`  
**Component:** instrument_app  

## Definition
```python
module settings.py
```

## Contains Symbols
- [WorkerSettings](worker_settings_py_WorkerSettings.md) (`class`)

## Imports
- [config.py](app_config_py.md)
- [logging_config.py](app_logging_config_py.md)
- [publisher.py](core_publisher_py.md)
- [tasks.py](worker_tasks_py.md)
- [telemetry.py](app_telemetry_py.md)

## Call Graph
```mermaid
flowchart TD
  worker_settings_py["settings.py"] --> app_logging_config_py__setup_logging["setup_logging"]
  worker_settings_py["settings.py"] --> app_telemetry_py__setup_tracing["setup_tracing"]
```

### Outgoing Calls
- Calls [setup_logging](app_logging_config_py_setup_logging.md) (`function`)
- Calls [setup_tracing](app_telemetry_py_setup_tracing.md) (`function`)
