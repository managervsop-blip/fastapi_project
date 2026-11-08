---
id: "app/logging_config.py::setup_logging"
label: "setup_logging"
type: "function"
source_file: "app/logging_config.py"
line_start: 5
line_end: 12
component: "app (setup_logging)"
---

# setup_logging

**Type:** `function`  
**Defined in:** [app/logging_config.py](../nodes/app_logging_config_py.md) (Lines 5-12)  
**Component:** app (setup_logging)  

## Definition
```python
def setup_logging(level: str = "INFO") -> None
```

## Description
Настроить логирование: время, уровень, модуль, сообщение.

**Contained in parent:** [logging_config.py](app_logging_config_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  app_main_py["main.py"] --> app_logging_config_py__setup_logging["setup_logging"]
  worker_settings_py["settings.py"] --> app_logging_config_py__setup_logging["setup_logging"]
```

### Incoming Calls (Backlinks)
- Called by [settings.py](worker_settings_py.md) (`file`)
- Called by [main.py](app_main_py.md) (`file`)
