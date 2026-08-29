"""
Phase 7 Memory retrieval (`FD-P7-001 §6` — `E7-03`, `E7-05.4`).

The read surface. It applies exactly one rule the store does not: **eligibility**.
`E7-03.3` requires that *"ineligible Memory is not returned as eligible active
Memory"* and `E7-05.4` that *"retrieval excludes ineligible Memory"*. Enforcing
that here, on the way out, means no caller can obtain an expired, invalidated,
superseded or never-admitted Memory through the ordinary path — including a
caller that reaches this surface through the Runtime.

**Deterministic-core.** `E7-03.2` requires that *"the same request against the
same eligible state has deterministic-core behavior."* This surface holds no
clock, no randomness, no ranking, no scoring and no similarity: given the same
retained state, `active` returns the same Memory every time. `FD-P7-001 §6`
states outright that similarity retrieval, vector retrieval, embeddings, semantic
ranking and semantic search are **not required** by `E7-03`, and none is present.

**Absence is not an error.** A key with no eligible Memory yields `None`. That is
a lawful answer to a lawful question, and raising instead would make "this Memory
expired" indistinguishable from "your request was invalid" — a distinction
`E7-05` depends on.

This surface is read-only. It exposes no transition, so retrieval cannot become a
back door into the lifecycle boundary.

Dependencies: this package and stdlib.
"""

from __future__ import annotations

from typing import Optional, Tuple

from .lifecycle import MemoryItem
from .store import MemoryLifecycleStore


class MemoryRetrieval:
    """Eligibility-filtered reads over retained Memory."""

    def __init__(self, store: MemoryLifecycleStore) -> None:
        self._store = store

    def active(self, key: str) -> Optional[MemoryItem]:
        """The eligible Memory at `key`, or `None`.

        The single question `E7-03` asks. A superseded, expired or invalidated
        newest version yields `None` rather than falling back to an older
        version: falling back would resurrect a Memory the lifecycle already
        retired, which is the failure `E7-05.3` names.
        """
        newest = self._store.newest(key)
        if newest is None or not newest.is_eligible:
            return None
        return newest

    def history(self, key: str) -> Tuple[MemoryItem, ...]:
        """Every retained version of `key`, oldest first, in every state.

        Not a retrieval of active Memory and never used as one — it is how a
        lifecycle is audited. `E7-04`'s prohibition on dangling references is
        only checkable if the superseded versions remain visible.
        """
        return self._store.line(key)

    def eligible_keys(self) -> Tuple[str, ...]:
        """Every key whose newest version is currently eligible."""
        return tuple(k for k in self._store.keys() if self.active(k) is not None)
