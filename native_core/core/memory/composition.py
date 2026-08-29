"""
Phase 7 Memory composition root — dependency wiring only.

Mirrors the resident Knowledge composition root (`knowledge/composition.py`)
rather than inventing a second assembly style: it instantiates the lifecycle
components and wires them by constructor injection, contains no business logic,
and holds no state after returning.

Wiring graph (constructor injection only):

    MemoryLifecycleStore                      (retention + lifecycle sequence)
        ├─► MemoryLifecycle(store, rule)      (admission, update, expiry, ...)
        └─► MemoryRetrieval(store)            (eligibility-filtered reads)

Ownership after construction is unchanged: the store owns retention; the
lifecycle boundary owns every lifecycle decision; retrieval owns eligibility on
read. The composition root owns none of them, and the Runtime that will hold this
bundle owns none of them either — `FD-P7-002 §3` keeps Runtime a non-owner of
Memory lifecycle and storage, and handing it an assembled bundle is what lets
that stay true.

Dependencies: this package and stdlib. No Infrastructure facility is required
because Phase 7 mandates no persistence (`FD-P7-001 §9`).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .admission import MemoryLifecycle, RetentionRule
from .retrieval import MemoryRetrieval
from .store import MemoryLifecycleStore


@dataclass(frozen=True)
class MemorySubsystem:
    """The assembled Phase 7 Memory subsystem — an immutable bundle of the wired
    components. Exposes exactly the three collaborators and nothing else: no
    helper, no business operation, no lifecycle shortcut that would let a holder
    of the bundle bypass the boundary."""

    lifecycle: MemoryLifecycle
    retrieval: MemoryRetrieval
    store: MemoryLifecycleStore


def create_memory_subsystem(
    retention_rule: "Optional[RetentionRule]" = None,
) -> MemorySubsystem:
    """Assemble the Phase 7 Memory subsystem by constructor injection only.

    An optional retention rule is the one policy input; everything else is
    structure. Repeated calls produce an identical graph topology over
    independent state.
    """
    store = MemoryLifecycleStore()
    return MemorySubsystem(
        lifecycle=MemoryLifecycle(store, retention_rule),
        retrieval=MemoryRetrieval(store),
        store=store,
    )
