---
id: "app/telemetry.py::setup_tracing"
label: "setup_tracing"
type: "function"
source_file: "app/telemetry.py"
line_start: 14
line_end: 32
component: "instrument_app"
---

# setup_tracing

**Type:** `function`  
**Defined in:** [app/telemetry.py](../nodes/app_telemetry_py.md) (Lines 14-32)  
**Component:** instrument_app  

## Definition
```python
def setup_tracing(service_name: str = "fastapi-project")
```

## Description
Настраивает TracerProvider и отправляет спаны в OTel Collector.

**Contained in parent:** [telemetry.py](app_telemetry_py.md) (`file`)

## Call Graph
```mermaid
flowchart TD
  app_main_py["main.py"] --> app_telemetry_py__setup_tracing["setup_tracing"]
  worker_settings_py["settings.py"] --> app_telemetry_py__setup_tracing["setup_tracing"]
```

### Incoming Calls (Backlinks)
- Called by [main.py](app_main_py.md) (`file`)
- Called by [settings.py](worker_settings_py.md) (`file`)
