"""
Runtime lifecycle model (Blueprint §6 "[O] lifecycle-states — reserved";
runtime_spec §12/§14 "[O] Runtime state model (which lifecycle states)").

The Runtime state model was an **[O] item reserved to the Architect**
(Blueprint §6 future extension; runtime_spec §14 open question). The Phase 4.0
directive exercises that reservation and fixes the states below; this module
only encodes the Architect's decision — it invents no state.

State model (Architect-decided, Phase 4.0):

    CREATED ──initialize──► INITIALIZED ──start──► RUNNING ──stop──► STOPPING ──► STOPPED

Discipline:
  - **Deterministic transitions** — the permitted set is a fixed, explicit map;
    the same current state always permits exactly the same successors.
  - **Invalid transitions fail closed** (PR-4) — refused with
    `InvalidLifecycleTransition`; the current state is left unchanged.
  - **No hidden lifecycle state** — the enum below is the complete set.
  - **No implicit startup** — nothing transitions on construction or on import;
    every transition is an explicit, caller-driven operation.

Ownership: Runtime owns transient hosting state only (Blueprint §6). This module
holds no runtime state itself — it is a pure state-transition rule table.
Dependencies: this package's `exceptions` only (stdlib otherwise). No authority,
no scheduling, no concurrency.
"""

from __future__ import annotations

from enum import Enum
from types import MappingProxyType

from .exceptions import InvalidLifecycleTransition


class RuntimeState(Enum):
    """The complete set of Runtime lifecycle states. No other state exists."""

    CREATED = "created"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"


#: The complete, immutable transition table. Any (from → to) pair absent here is
#: invalid and fails closed. STOPPED is terminal — a stopped Runtime is never
#: restarted (no implicit startup, no resurrection).
VALID_TRANSITIONS = MappingProxyType(
    {
        RuntimeState.CREATED: frozenset({RuntimeState.INITIALIZED}),
        RuntimeState.INITIALIZED: frozenset({RuntimeState.RUNNING}),
        RuntimeState.RUNNING: frozenset({RuntimeState.STOPPING}),
        RuntimeState.STOPPING: frozenset({RuntimeState.STOPPED}),
        RuntimeState.STOPPED: frozenset(),
    }
)


def is_valid_transition(current: RuntimeState, target: RuntimeState) -> bool:
    """Pure predicate: whether `current → target` is a permitted transition.
    Deterministic; consults only the fixed table above."""
    return target in VALID_TRANSITIONS.get(current, frozenset())


def require_transition(current: RuntimeState, target: RuntimeState) -> RuntimeState:
    """Return `target` if `current → target` is permitted; otherwise fail closed
    with `InvalidLifecycleTransition` (PR-4). Mutates nothing — the caller
    applies the returned state, so a refused transition leaves state unchanged."""
    if not is_valid_transition(current, target):
        raise InvalidLifecycleTransition(
            f"invalid lifecycle transition {current.value!r} -> {target.value!r}"
        )
    return target
