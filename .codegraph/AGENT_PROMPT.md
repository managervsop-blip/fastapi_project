# Codebase Architecture Analysis Prompt

You are a senior software architect. Using the knowledge-graph metadata and component relationships below, write a deep **AI Architectural Insights** report for this project **in English**.

**Important**: Write the full report into the `## AI Architectural Insights` section of `.codegraph/README.md` (keep this English heading so rebuilds can preserve prior insights).

## Graph statistics
- Files: 22
- Symbols (classes/functions/methods): 47
- Edges: 96
- Edge resolution: 106/632 (16.8%)
- Unresolved edges: 526
- Internal resolution: 106/112 (94.6%), internal_unresolved=6
- Unresolved by category: external=241, builtin=84, attribute=195, internal=6

## Logical components (modularity)
- instrument_app: cohesion=0.2100, members_count=7
- app (enqueue_test): cohesion=0.1400, members_count=7
- core (create_task): cohesion=0.1400, members_count=7
- run_async_migrations: cohesion=0.2000, members_count=6
- app (Base): cohesion=0.2500, members_count=5
- core (BitrixRateLimiter): cohesion=0.2500, members_count=5
- worker (process_outbox_task): cohesion=0.2500, members_count=5
- TaskOutbox: cohesion=0.2500, members_count=4
- e2eCheck (Component 9): cohesion=0.3300, members_count=3
- e2eCheck (Component 10): cohesion=0.3300, members_count=3
- migrations/versions (downgrade) (downgrade): cohesion=0.3300, members_count=3
- migrations/versions (downgrade) (downgrade): cohesion=0.3300, members_count=3
- migrations/versions (downgrade) (downgrade): cohesion=0.3300, members_count=3
- migrations/versions (downgrade) (downgrade): cohesion=0.3300, members_count=3
- app (setup_logging): cohesion=0.5000, members_count=2
- core (execute_batch): cohesion=0.5000, members_count=2
- tests: cohesion=0.0000, members_count=1

## Component dependency graph (Mermaid)
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

## God nodes (highest degree)
- main.py (file): degree=13, file=app/main.py
- db.py (file): degree=10, file=app/db.py
- tasks.py (file): degree=10, file=worker/tasks.py
- outbox.py (file): degree=9, file=core/outbox.py
- config.py (file): degree=8, file=app/config.py
- settings.py (file): degree=8, file=worker/settings.py
- env.py (file): degree=7, file=migrations/env.py
- outbox.py (file): degree=6, file=app/models/outbox.py
- process_outbox_task (function): degree=6, file=worker/tasks.py
- telemetry.py (file): degree=5, file=app/telemetry.py

## File-level import cycles
No circular imports

Focus your analysis on:
1. **System architecture** — design patterns, modularity, physical vs logical alignment.
2. **Core abstractions & boundaries** — which god nodes are healthy hubs vs fat objects.
3. **Bottlenecks & refactoring** — coupling risks, cycle impact, concrete decoupling steps.

Output standard Markdown only (no surrounding ```markdown fences).
