---
type: "component"
cohesion: 0.21
members_count: 7
---

# instrument_app

**Internal Cohesion:** 0.21 (density score)  
**Members count:** 7 nodes  

## Members
- [WorkerSettings](../nodes/worker_settings_py_WorkerSettings.md) (`class` in `worker/settings.py`)
- [instrument_app](../nodes/app_telemetry_py_instrument_app.md) (`function` in `app/telemetry.py`)
- [logging_config.py](../nodes/app_logging_config_py.md) (`file` in `app/logging_config.py`)
- [settings.py](../nodes/worker_settings_py.md) (`file` in `worker/settings.py`)
- [setup_logging](../nodes/app_logging_config_py_setup_logging.md) (`function` in `app/logging_config.py`)
- [setup_tracing](../nodes/app_telemetry_py_setup_tracing.md) (`function` in `app/telemetry.py`)
- [telemetry.py](../nodes/app_telemetry_py.md) (`file` in `app/telemetry.py`)

## Component Dependencies

- Depends on [TaskOutbox](TaskOutbox.md) (3 calls/connections)
- Depends on [worker (process_outbox_task)](worker_process_outbox_task_.md) (1 calls/connections)
