# Codebase Architecture Analysis Prompt

You are a senior software architect. Using the knowledge-graph metadata and component relationships below, write a deep **AI Architectural Insights** report for this project **in English**.

**Important**: Write the full report into the `## AI Architectural Insights` section of `.codegraph/README.md` (keep this English heading so rebuilds can preserve prior insights).

## Graph statistics
- Files: 21
- Symbols (classes/functions/methods): 39
- Edges: 87
- Edge resolution: 99/539 (18.4%)
- Unresolved edges: 440
- Internal resolution: 99/105 (94.3%), internal_unresolved=6
- Unresolved by category: external=224, builtin=51, attribute=159, internal=6

## Logical components (modularity)
- instrument_app: cohesion=0.2100, members_count=7
- core (create_task): cohesion=0.1400, members_count=7
- app (enqueue_test): cohesion=0.1700, members_count=6
- run_async_migrations: cohesion=0.2000, members_count=6
- process_outbox_task: cohesion=0.2000, members_count=6
- app (Base): cohesion=0.2500, members_count=5
- core (BitrixRateLimiter): cohesion=0.2500, members_count=5
- TaskOutbox: cohesion=0.2500, members_count=4
- migrations/versions (downgrade) (downgrade): cohesion=0.3300, members_count=3
- migrations/versions (downgrade) (downgrade): cohesion=0.3300, members_count=3
- migrations/versions (downgrade) (downgrade): cohesion=0.3300, members_count=3
- app (setup_logging): cohesion=0.5000, members_count=2
- load_test_batch: cohesion=0.0000, members_count=1
- load_test_max: cohesion=0.0000, members_count=1
- tests: cohesion=0.0000, members_count=1

## Component dependency graph (Mermaid)
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

## God nodes (highest degree)
- main.py (file): degree=12, file=app/main.py
- db.py (file): degree=10, file=app/db.py
- outbox.py (file): degree=9, file=core/outbox.py
- tasks.py (file): degree=9, file=worker/tasks.py
- config.py (file): degree=8, file=app/config.py
- settings.py (file): degree=8, file=worker/settings.py
- env.py (file): degree=7, file=migrations/env.py
- outbox.py (file): degree=6, file=app/models/outbox.py
- telemetry.py (file): degree=5, file=app/telemetry.py
- TaskOutbox (class): degree=5, file=app/models/outbox.py

## File-level import cycles
No circular imports

Focus your analysis on:
1. **System architecture** — design patterns, modularity, physical vs logical alignment.
2. **Core abstractions & boundaries** — which god nodes are healthy hubs vs fat objects.
3. **Bottlenecks & refactoring** — coupling risks, cycle impact, concrete decoupling steps.

Output standard Markdown only (no surrounding ```markdown fences).
