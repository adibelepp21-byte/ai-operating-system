"""
Execution layer boundary (Phase 4.2) — Runtime-owned internal structure.

The canonical bridge between Runtime and every future execution consumer:

    Infrastructure → Knowledge → Runtime → **Execution Layer** → Agent (future)
                                                              → Workflow (future)
                                                              → Skill (future)

Every future execution consumer is intended to execute through this boundary;
Runtime never executes them directly.

**Not a new subsystem or entity.** The Native Core's core region contains
exactly the eleven frozen subsystem boundaries and no new entity/subsystem may
be introduced (Blueprint §31). This layer is therefore *internal structure of
the Runtime boundary* (`core/runtime/execution/`), owned by Runtime — it is not
a twelfth boundary and not a Domain-Model entity. The name matches the frozen
Domain-Model **category** "Execution (runtime, agent, skill, workflow, and the
Tool boundary in infrastructure)" (Blueprint §31).

Ownership: a **transient execution boundary** only. It owns no business logic,
no AI behavior, no planning, no scheduling, no queue, no knowledge, and no
authority. Runtime keeps hosting lifecycle; Knowledge keeps semantic knowledge;
Infrastructure keeps physical facilities; Governance keeps authority; Memory
keeps candidate generation; Trace keeps immutable history.

NOT implemented here (later authorized phases): Agent, Workflow, Skill, Planner,
Scheduler, Queue, Executor, tool execution, model execution, retries, parallel
execution, event loop, async, threads, futures, timers.

Dependency direction: Execution depends on Runtime (upward within the Runtime
boundary); Runtime does **not** depend on Execution — no reverse dependency, no
cycle, and no Runtime→Agent or Runtime→Workflow dependency exists.

Public surface:
  - contract:    Execution
  - session:     ExecutionSession
  - context:     ExecutionContext
  - composition: create_execution_layer
  - exceptions:  ExecutionError, InvalidExecutionConfiguration
"""

from .composition import create_execution_layer
from .context import ExecutionContext
from .contract import Execution
from .exceptions import ExecutionError, InvalidExecutionConfiguration
from .session import ExecutionSession

__all__ = [
    "Execution",
    "ExecutionSession",
    "ExecutionContext",
    "create_execution_layer",
    "ExecutionError",
    "InvalidExecutionConfiguration",
]
