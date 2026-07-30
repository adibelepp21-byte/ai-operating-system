"""
Execution-layer composition root (Phase 4.2) — dependency wiring only.

The single construction point for an execution boundary. It assembles an
`ExecutionSession` by **constructor injection only** and contains no execution
logic, planning, scheduling, queueing, retries, or business logic.

Wiring:

    Runtime (injected, must be RUNNING)
      └─► runtime.create_context()      → RuntimeContext  (identity issued by Runtime)
            └─► ExecutionContext(runtime_id, execution_sequence)
                  └─► ExecutionSession(runtime, context)

Identity discipline: the Execution layer **never generates identity**. The
execution ordinal is issued by the Runtime's own canonical `create_context()`
(Phase 4.0, unchanged), so there is no second counter, no hidden state, no
clock, no UUID, and no randomness — construction is deterministic and the
Runtime remains the sole owner of hosting/identity issuance.

Access discipline: `create_context()` is RUNNING-only, so building an execution
boundary against a Runtime that is not RUNNING fails closed through the
Runtime's own control — this layer weakens nothing.

Freshness: every call constructs a **new** execution graph. No caching, no reuse
across calls, no memoization, no lazy wiring, no module state, no singleton, no
registry, no service locator, no reflection, no dynamic import.
"""

from __future__ import annotations

from ..contract import Runtime
from .context import ExecutionContext
from .contract import Execution
from .exceptions import InvalidExecutionConfiguration
from .session import ExecutionSession


def create_execution_layer(runtime: "Runtime") -> "Execution":
    """Assemble a fresh execution boundary bound to the given Runtime.

    Fail closed on a missing or wrong-typed Runtime; and, because the execution
    identity is issued by `Runtime.create_context()`, also fail closed (via the
    Runtime) when the Runtime is not RUNNING.
    """
    if not isinstance(runtime, Runtime):
        raise InvalidExecutionConfiguration("create_execution_layer requires a Runtime")

    runtime_context = runtime.create_context()
    context = ExecutionContext(
        runtime_id=runtime_context.runtime_id,
        execution_sequence=runtime_context.execution_sequence,
    )
    return ExecutionSession(_runtime=runtime, _context=context)
