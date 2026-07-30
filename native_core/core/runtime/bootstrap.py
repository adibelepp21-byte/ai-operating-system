"""
Runtime bootstrap (Phase 4.1) — the canonical construction entry point.

Exactly one bootstrap entry for the Runtime subsystem. Its responsibilities are
**only**: validate the injected dependencies, build the Runtime graph via the
Runtime composition root, initialize the Runtime, and return it.

Bootstrap owns **nothing** after returning: it holds no reference, no state, no
cache, and no module-level data. It contains no runtime logic, no lifecycle
policy, no authorization, no persistence, and no scheduling.

Lifecycle policy stays with the caller: bootstrap performs exactly one
transition — `CREATED → INITIALIZED` — and deliberately does **not** start the
Runtime. Deciding when to `start()` and `stop()` remains the caller's, so no
lifecycle policy is embedded here.

Validation is a fail-closed entry-point guard (PR-4). `AIOSRuntime.__init__`
retains its own guard (Phase 4.0, unchanged); this is defense in depth at the
entry point, not a relocation of that responsibility — both raise the same
`InvalidRuntimeConfiguration`.

Prohibited here and absent: singleton, registry, service locator, reflection,
dynamic import, lazy wiring, module state, cache, timestamp, UUID, randomness,
thread, async, scheduler, executor, Agent, Workflow, planner, Skill, model
adapter, automation.
"""

from __future__ import annotations

from ..infrastructure import ExecutionSubstrate, StorageFacility
from .composition import create_runtime
from .contract import Runtime
from .exceptions import InvalidRuntimeConfiguration


def bootstrap_runtime(
    runtime_id: str,
    storage: "StorageFacility",
    substrate: "ExecutionSubstrate",
) -> "Runtime":
    """Validate, build, initialize, and return the Runtime.

    Returns a Runtime in the `INITIALIZED` state (hosted subsystems assembled
    through their composition roots). It is **not** started — starting is the
    caller's lifecycle decision.

    Fail closed on any missing or wrong-typed dependency; on an initialization
    failure the error propagates and nothing is returned.
    """
    if not isinstance(runtime_id, str) or not runtime_id.strip():
        raise InvalidRuntimeConfiguration("bootstrap requires a non-empty runtime_id")
    if not isinstance(storage, StorageFacility):
        raise InvalidRuntimeConfiguration("bootstrap requires an Infrastructure StorageFacility")
    if not isinstance(substrate, ExecutionSubstrate):
        raise InvalidRuntimeConfiguration("bootstrap requires an Infrastructure ExecutionSubstrate")

    runtime = create_runtime(runtime_id=runtime_id, storage=storage, substrate=substrate)
    runtime.initialize()
    return runtime
