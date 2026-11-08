# Codebase Knowledge Graph

Welcome to the codebase knowledge graph of this workspace. This index represents files, classes, structs, methods, and functions as nodes, with call and dependency relationships between them.

## Statistics
- **Files Scanned:** 21
- **Symbols Extracted:** 39
- **Call/Relation Edges:** 87
- **Edge Resolution:** 99/539 resolved (18.4%)
- **Unresolved Edges:** 440
- **Internal Resolution:** 99/105 (94.3%), internal unresolved=6
- **Unresolved by Category:** external=224, builtin=51, attribute=159, internal=6
- **Relation Mix:** calls=21, contains=36, imports=28, inherits=2

## Architecture Overview
This project is built using a modular software system design. The static parser performs a full scan of the codebase to generate the underlying dependency network, and the knowledge graph groups symbols into logical components using a community detection algorithm (Component-level clustering).

### Physical Structure & Layout
- **`app/`** : contains 8 source files (e.g., `config.py`, `logging_config.py`, `idempotency.py` etc.).
- **`core/`** : contains 4 source files (e.g., `rate_limiter.py`, `bitrix_batch.py`, `publisher.py` etc.).
- **`migrations/`** : contains 4 source files (e.g., `env.py`, `dc3cd7a06e30_add_trace_id_to_tasks_outbox.py`, `8818bdcf3760_add_last_error_to_tasks_outbox.py` etc.).
- **Root directory `.`** : contains 3 configuration or source files.
- **`worker/`** : contains 2 source files (e.g., `settings.py`, `tasks.py`).

### Core Execution Entrypoints
- `instrument_app` (defined in [app/telemetry.py](nodes/app_telemetry_py.md))
- `run_migrations_offline` (defined in [migrations/env.py](nodes/migrations_env_py.md))
- `do_run_migrations` (defined in [migrations/env.py](nodes/migrations_env_py.md))
- `run_async_migrations` (defined in [migrations/env.py](nodes/migrations_env_py.md))
- `run_migrations_online` (defined in [migrations/env.py](nodes/migrations_env_py.md))

### Control Flow & Data Dependencies
Data flow and control logic in the system center around core classes and components. The main components and their logical topological call relationships are shown in the diagram below, visualizing the core component interaction model.

## Component Dependency Graph
```mermaid
flowchart TD
  comp_1["instrument_app"] -->|2| comp_12["app (setup_logging)"]
  comp_1["instrument_app"] -->|1| comp_8["TaskOutbox"]
  comp_1["instrument_app"] -->|1| comp_5["process_outbox_task"]
  comp_2["core (create_task)"] -->|3| comp_6["app (Base)"]
  comp_2["core (create_task)"] -->|3| comp_8["TaskOutbox"]
  comp_3["app (enqueue_test)"] -->|1| comp_6["app (Base)"]
  comp_3["app (enqueue_test)"] -->|3| comp_1["instrument_app"]
  comp_3["app (enqueue_test)"] -->|2| comp_12["app (setup_logging)"]
  comp_3["app (enqueue_test)"] -->|1| comp_8["TaskOutbox"]
  comp_3["app (enqueue_test)"] -->|1| comp_2["core (create_task)"]
  comp_4["run_async_migrations"] -->|1| comp_1["instrument_app"]
  comp_4["run_async_migrations"] -->|1| comp_6["app (Base)"]
  comp_5["process_outbox_task"] -->|2| comp_1["instrument_app"]
  comp_5["process_outbox_task"] -->|3| comp_7["core (BitrixRateLimiter)"]
  comp_5["process_outbox_task"] -->|1| comp_6["app (Base)"]
  comp_5["process_outbox_task"] -->|2| comp_8["TaskOutbox"]
  comp_6["app (Base)"] -->|1| comp_1["instrument_app"]
  comp_8["TaskOutbox"] -->|3| comp_6["app (Base)"]
  comp_8["TaskOutbox"] -->|1| comp_1["instrument_app"]
  comp_8["TaskOutbox"] -->|2| comp_2["core (create_task)"]
```

## Logical Components Summary
The codebase has been automatically clustered into logical components based on coupling and call density:

| Component | Cohesion (Density) | Size (Nodes) |
|---|---|---|
| [instrument_app](components/instrument_app.md) | 0.21 | 7 |
| [core (create_task)](components/core_create_task_.md) | 0.14 | 7 |
| [app (enqueue_test)](components/app_enqueue_test_.md) | 0.17 | 6 |
| [run_async_migrations](components/run_async_migrations.md) | 0.2 | 6 |
| [process_outbox_task](components/process_outbox_task.md) | 0.2 | 6 |
| [app (Base)](components/app_Base_.md) | 0.25 | 5 |
| [core (BitrixRateLimiter)](components/core_BitrixRateLimiter_.md) | 0.25 | 5 |
| [TaskOutbox](components/TaskOutbox.md) | 0.25 | 4 |
| [migrations/versions (downgrade) (downgrade)](components/migrations_versions_downgrade_downgrade_.md) | 0.33 | 3 |
| [migrations/versions (downgrade) (downgrade)](components/migrations_versions_downgrade_downgrade_.md) | 0.33 | 3 |
| [migrations/versions (downgrade) (downgrade)](components/migrations_versions_downgrade_downgrade_.md) | 0.33 | 3 |
| [app (setup_logging)](components/app_setup_logging_.md) | 0.5 | 2 |
| [load_test_batch](components/load_test_batch.md) | 0 | 1 |
| [load_test_max](components/load_test_max.md) | 0 | 1 |
| [tests](components/tests.md) | 0 | 1 |

## God Nodes (Top Core Abstractions)
These symbols have the highest degrees (most connections) in the codebase. Test paths are excluded. Modifying them may have wide-reaching effects:

| Symbol | Type | Degree | In | Out | File |
|---|---|---|---|---|---|
| [main.py](nodes/app_main_py.md) | `file` | 12 | 0 | 12 | `app/main.py` |
| [db.py](nodes/app_db_py.md) | `file` | 10 | 7 | 3 | `app/db.py` |
| [outbox.py](nodes/core_outbox_py.md) | `file` | 9 | 0 | 9 | `core/outbox.py` |
| [tasks.py](nodes/worker_tasks_py.md) | `file` | 9 | 1 | 8 | `worker/tasks.py` |
| [config.py](nodes/app_config_py.md) | `file` | 8 | 7 | 1 | `app/config.py` |
| [settings.py](nodes/worker_settings_py.md) | `file` | 8 | 0 | 8 | `worker/settings.py` |
| [env.py](nodes/migrations_env_py.md) | `file` | 7 | 0 | 7 | `migrations/env.py` |
| [outbox.py](nodes/app_models_outbox_py.md) | `file` | 6 | 4 | 2 | `app/models/outbox.py` |
| [telemetry.py](nodes/app_telemetry_py.md) | `file` | 5 | 2 | 3 | `app/telemetry.py` |
| [TaskOutbox](nodes/app_models_outbox_py_TaskOutbox.md) | `class` | 5 | 4 | 1 | `app/models/outbox.py` |

## Unresolved Edge Samples
Representative edges that could not be bound to a graph symbol, classified as internal / external / builtin / attribute:

| Category | Relation | Source | Target |
|---|---|---|---|
| `external` | `imports` | `app/config.py` | `pydantic_settings` |
| `external` | `inherits` | `app/config.py::Settings` | `BaseSettings` |
| `external` | `calls` | `app/config.py::Settings` | `SettingsConfigDict` |
| `external` | `imports` | `app/logging_config.py` | `logging` |
| `external` | `imports` | `app/logging_config.py` | `sys` |
| `external` | `calls` | `app/logging_config.py::setup_logging` | `logging.basicConfig` |
| `external` | `imports` | `app/models/idempotency.py` | `uuid` |
| `external` | `imports` | `app/models/idempotency.py` | `datetime` |
| `external` | `imports` | `app/models/idempotency.py` | `sqlalchemy` |
| `external` | `imports` | `app/models/idempotency.py` | `sqlalchemy.dialects.postgresql` |
| `external` | `imports` | `app/models/idempotency.py` | `sqlalchemy.orm` |
| `external` | `calls` | `app/models/idempotency.py::IdempotencyKey` | `mapped_column` |
| `attribute` | `calls` | `app/models/idempotency.py::IdempotencyKey` | `func.now` |
| `attribute` | `calls` | `app/telemetry.py::setup_tracing` | `Resource.create` |
| `attribute` | `calls` | `app/telemetry.py::setup_tracing` | `provider.add_span_processor` |
| `attribute` | `calls` | `app/telemetry.py::setup_tracing` | `trace.set_tracer_provider` |
| `attribute` | `calls` | `app/telemetry.py::instrument_app` | `HTTPXClientInstrumentor().instrument` |
| `attribute` | `calls` | `app/models/outbox.py::TaskOutbox` | `func.now` |
| `attribute` | `calls` | `app/models/outbox.py::TaskOutbox` | `func.now` |
| `attribute` | `calls` | `app/models/outbox.py::TaskOutbox` | `func.now` |

## Circular Import Dependencies
No circular imports detected. Perfect modularity!

## AI Architectural Insights
> 💡 **Tip**: AI architectural insights have not been generated yet. Please use your AI Agent (e.g., Antigravity, Claude Code, Codex) to read the prompt in `.codegraph/AGENT_PROMPT.md` and fill in the analysis results here.
