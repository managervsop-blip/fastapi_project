# Codebase Knowledge Graph

Welcome to the codebase knowledge graph of this workspace. This index represents files, classes, structs, methods, and functions as nodes, with call and dependency relationships between them.

## Statistics
- **Files Scanned:** 22
- **Symbols Extracted:** 47
- **Call/Relation Edges:** 96
- **Edge Resolution:** 106/632 resolved (16.8%)
- **Unresolved Edges:** 526
- **Internal Resolution:** 106/112 (94.6%), internal unresolved=6
- **Unresolved by Category:** external=241, builtin=84, attribute=195, internal=6
- **Relation Mix:** calls=22, contains=44, imports=28, inherits=2

## Architecture Overview
This project is built using a modular software system design. The static parser performs a full scan of the codebase to generate the underlying dependency network, and the knowledge graph groups symbols into logical components using a community detection algorithm (Component-level clustering).

### Physical Structure & Layout
- **`app/`** : contains 8 source files (e.g., `config.py`, `logging_config.py`, `telemetry.py` etc.).
- **`migrations/`** : contains 5 source files (e.g., `env.py`, `dc3cd7a06e30_add_trace_id_to_tasks_outbox.py`, `7ed6f6d1f417_create_outbox_and_idempotency_tables.py` etc.).
- **`core/`** : contains 4 source files (e.g., `rate_limiter.py`, `publisher.py`, `bitrix_batch.py` etc.).
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
  comp_1["instrument_app"] -->|2| comp_15["app (setup_logging)"]
  comp_1["instrument_app"] -->|1| comp_8["TaskOutbox"]
  comp_1["instrument_app"] -->|1| comp_7["worker (process_outbox_task)"]
  comp_2["app (enqueue_test)"] -->|1| comp_5["app (Base)"]
  comp_2["app (enqueue_test)"] -->|1| comp_8["TaskOutbox"]
  comp_2["app (enqueue_test)"] -->|3| comp_1["instrument_app"]
  comp_2["app (enqueue_test)"] -->|2| comp_15["app (setup_logging)"]
  comp_2["app (enqueue_test)"] -->|1| comp_3["core (create_task)"]
  comp_3["core (create_task)"] -->|3| comp_5["app (Base)"]
  comp_3["core (create_task)"] -->|3| comp_8["TaskOutbox"]
  comp_4["run_async_migrations"] -->|1| comp_1["instrument_app"]
  comp_4["run_async_migrations"] -->|1| comp_5["app (Base)"]
  comp_5["app (Base)"] -->|1| comp_1["instrument_app"]
  comp_7["worker (process_outbox_task)"] -->|3| comp_6["core (BitrixRateLimiter)"]
  comp_7["worker (process_outbox_task)"] -->|2| comp_16["core (execute_batch)"]
  comp_7["worker (process_outbox_task)"] -->|1| comp_5["app (Base)"]
  comp_7["worker (process_outbox_task)"] -->|2| comp_8["TaskOutbox"]
  comp_7["worker (process_outbox_task)"] -->|1| comp_1["instrument_app"]
  comp_8["TaskOutbox"] -->|1| comp_1["instrument_app"]
  comp_8["TaskOutbox"] -->|3| comp_5["app (Base)"]
  comp_8["TaskOutbox"] -->|2| comp_3["core (create_task)"]
  comp_16["core (execute_batch)"] -->|1| comp_1["instrument_app"]
```

## Logical Components Summary
The codebase has been automatically clustered into logical components based on coupling and call density:

| Component | Cohesion (Density) | Size (Nodes) |
|---|---|---|
| [instrument_app](components/instrument_app.md) | 0.21 | 7 |
| [app (enqueue_test)](components/app_enqueue_test_.md) | 0.14 | 7 |
| [core (create_task)](components/core_create_task_.md) | 0.14 | 7 |
| [run_async_migrations](components/run_async_migrations.md) | 0.2 | 6 |
| [app (Base)](components/app_Base_.md) | 0.25 | 5 |
| [core (BitrixRateLimiter)](components/core_BitrixRateLimiter_.md) | 0.25 | 5 |
| [worker (process_outbox_task)](components/worker_process_outbox_task_.md) | 0.25 | 5 |
| [TaskOutbox](components/TaskOutbox.md) | 0.25 | 4 |
| [e2eCheck (Component 9)](components/e2eCheck_Component_9_.md) | 0.33 | 3 |
| [e2eCheck (Component 10)](components/e2eCheck_Component_10_.md) | 0.33 | 3 |
| [migrations/versions (downgrade) (downgrade)](components/migrations_versions_downgrade_downgrade_.md) | 0.33 | 3 |
| [migrations/versions (downgrade) (downgrade)](components/migrations_versions_downgrade_downgrade_.md) | 0.33 | 3 |
| [migrations/versions (downgrade) (downgrade)](components/migrations_versions_downgrade_downgrade_.md) | 0.33 | 3 |
| [migrations/versions (downgrade) (downgrade)](components/migrations_versions_downgrade_downgrade_.md) | 0.33 | 3 |
| [app (setup_logging)](components/app_setup_logging_.md) | 0.5 | 2 |
| [core (execute_batch)](components/core_execute_batch_.md) | 0.5 | 2 |
| [tests](components/tests.md) | 0 | 1 |

## God Nodes (Top Core Abstractions)
These symbols have the highest degrees (most connections) in the codebase. Test paths are excluded. Modifying them may have wide-reaching effects:

| Symbol | Type | Degree | In | Out | File |
|---|---|---|---|---|---|
| [main.py](nodes/app_main_py.md) | `file` | 13 | 0 | 13 | `app/main.py` |
| [db.py](nodes/app_db_py.md) | `file` | 10 | 7 | 3 | `app/db.py` |
| [tasks.py](nodes/worker_tasks_py.md) | `file` | 10 | 1 | 9 | `worker/tasks.py` |
| [outbox.py](nodes/core_outbox_py.md) | `file` | 9 | 0 | 9 | `core/outbox.py` |
| [config.py](nodes/app_config_py.md) | `file` | 8 | 7 | 1 | `app/config.py` |
| [settings.py](nodes/worker_settings_py.md) | `file` | 8 | 0 | 8 | `worker/settings.py` |
| [env.py](nodes/migrations_env_py.md) | `file` | 7 | 0 | 7 | `migrations/env.py` |
| [outbox.py](nodes/app_models_outbox_py.md) | `file` | 6 | 4 | 2 | `app/models/outbox.py` |
| [process_outbox_task](nodes/worker_tasks_py_process_outbox_task.md) | `function` | 6 | 1 | 5 | `worker/tasks.py` |
| [telemetry.py](nodes/app_telemetry_py.md) | `file` | 5 | 2 | 3 | `app/telemetry.py` |

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
| `external` | `imports` | `app/telemetry.py` | `logging` |
| `external` | `imports` | `app/telemetry.py` | `opentelemetry` |
| `external` | `imports` | `app/telemetry.py` | `opentelemetry.sdk.trace` |
| `external` | `imports` | `app/telemetry.py` | `opentelemetry.sdk.trace.export` |
| `external` | `imports` | `app/telemetry.py` | `opentelemetry.sdk.resources` |
| `external` | `imports` | `app/telemetry.py` | `opentelemetry.exporter.otlp.proto.grpc.trace_exporter` |
| `attribute` | `calls` | `app/telemetry.py::setup_tracing` | `Resource.create` |
| `attribute` | `calls` | `app/telemetry.py::setup_tracing` | `provider.add_span_processor` |
| `attribute` | `calls` | `app/telemetry.py::setup_tracing` | `trace.set_tracer_provider` |
| `attribute` | `calls` | `app/telemetry.py::instrument_app` | `HTTPXClientInstrumentor().instrument` |
| `attribute` | `calls` | `app/models/idempotency.py::IdempotencyKey` | `func.now` |
| `attribute` | `calls` | `core/rate_limiter.py::BitrixRateLimiter.acquire` | `self.redis.script_load` |
| `attribute` | `calls` | `core/rate_limiter.py::BitrixRateLimiter.acquire` | `self.redis.evalsha` |
| `attribute` | `calls` | `core/rate_limiter.py::BitrixRateLimiter.acquire` | `self.redis.script_load` |

## Circular Import Dependencies
No circular imports detected. Perfect modularity!

## AI Architectural Insights
> 💡 **Tip**: AI architectural insights have not been generated yet. Please use your AI Agent (e.g., Antigravity, Claude Code, Codex) to read the prompt in `.codegraph/AGENT_PROMPT.md` and fill in the analysis results here.
