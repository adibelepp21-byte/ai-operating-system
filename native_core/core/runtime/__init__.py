"""
Runtime boundary (Native Core Blueprint §6; runtime_spec; Freeze INV-3/INV-4;
OQ-2).

Runtime hosts Agent Instances and drives execution — **a facility, not an
actor** (Domain Model; runtime_spec §1). Phase 4.0 establishes the foundation
only: lifecycle management, dependency hosting, execution context, resource
ownership, and controlled shutdown.

NOT implemented here (later authorized phases): Agent, Workflow, Skill, model
execution, planner, executor, model adapter, scheduling, concurrency engine,
task queue, or any autonomous/automation behavior.

Ownership (Blueprint §6): Runtime owns **transient hosting state only**. It owns
no Knowledge semantics, no Memory, no Governance authority, and no Trace record;
it authors **no independent Trace** (OQ-2; runtime_spec §9); it makes no
governance decision (runtime_spec §10; §6.2 invariant 2).

Module isolation (Blueprint §26): this boundary depends only on Infrastructure
facilities beneath it (`StorageFacility`, and the `ExecutionSubstrate` that
Infrastructure spec §5c provides *to Runtime*) and on the Knowledge **composition
root** — hosted subsystems are only ever assembled through their composition
roots, never by constructing their internals. It imports nothing from Memory,
Governance, or Trace, holds no external dependency (INV-12), and no subsystem
imports Runtime (no inversion, no cycle).

Lifecycle state model: an **[O] item reserved to the Architect** (Blueprint §6;
runtime_spec §12/§14), exercised by the Phase 4.0 directive as
CREATED → INITIALIZED → RUNNING → STOPPING → STOPPED.

Public surface:
  - contract:  Runtime
  - runtime:   AIOSRuntime
  - lifecycle: RuntimeState, VALID_TRANSITIONS, is_valid_transition, require_transition
  - context:   RuntimeContext
  - exceptions: RuntimeSubsystemError, InvalidLifecycleTransition, RuntimeNotRunning,
                InvalidRuntimeConfiguration
"""

from .context import RuntimeContext
from .contract import Runtime
from .exceptions import (
    InvalidLifecycleTransition,
    InvalidRuntimeConfiguration,
    RuntimeNotRunning,
    RuntimeSubsystemError,
)
from .lifecycle import (
    VALID_TRANSITIONS,
    RuntimeState,
    is_valid_transition,
    require_transition,
)
from .runtime import AIOSRuntime

__all__ = [
    "Runtime",
    "AIOSRuntime",
    "RuntimeState",
    "VALID_TRANSITIONS",
    "is_valid_transition",
    "require_transition",
    "RuntimeContext",
    "RuntimeSubsystemError",
    "InvalidLifecycleTransition",
    "RuntimeNotRunning",
    "InvalidRuntimeConfiguration",
]
