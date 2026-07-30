"""
Runtime composition root (Phase 4.1) — dependency wiring only.

The single canonical construction point for the Runtime object graph. It
assembles the already-certified Phase 4.0 Runtime implementation by
**constructor injection only**; it contains no Runtime behavior, lifecycle
policy, scheduling, execution, planning, Agent/Workflow logic, or business
logic, and it changes no existing Runtime implementation.

Wiring graph (dependency order):

    StorageFacility ─┐                      (Infrastructure, injected)
    ExecutionSubstrate ─┤                   (Infrastructure, injected — spec §5c)
                        └─► AIOSRuntime(runtime_id, storage, substrate)
                              └─(on initialize)─► create_knowledge_subsystem(storage)
                                                    └─► KnowledgeSubsystem

The Knowledge composition root is reached through `AIOSRuntime.initialize()`
(Phase 4.0, unchanged) — this module never constructs Knowledge internals and
never bypasses the Knowledge composition root.

Infrastructure facilities are **injected, never constructed here**: their
lifecycle belongs to the Infrastructure Bootstrap that established them, so the
Runtime composition root takes no ownership of them (ownership discipline of
Phase 4.0 preserved).

Freshness: every call constructs a **new** Runtime graph. There is no caching,
no reuse across calls, no memoization, no lazy wiring, no hidden wiring, no
module state, no singleton, no registry, no service locator, no reflection, no
dynamic import, no timestamp, no UUID, no randomness, no thread, no async.
"""

from __future__ import annotations

from ..infrastructure import ExecutionSubstrate, StorageFacility
from .contract import Runtime
from .runtime import AIOSRuntime


def create_runtime(
    runtime_id: str,
    storage: "StorageFacility",
    substrate: "ExecutionSubstrate",
) -> "Runtime":
    """Assemble a fresh Runtime object graph by constructor injection.

    Returns the Runtime in its initial `CREATED` state — construction performs
    no lifecycle transition (no implicit startup). The caller (or the Runtime
    bootstrap) decides when to initialize and start.

    Dependencies are supplied by the caller; nothing is constructed here except
    the Runtime itself.
    """
    return AIOSRuntime(runtime_id=runtime_id, storage=storage, substrate=substrate)
