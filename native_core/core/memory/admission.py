"""
The Phase 7 Memory lifecycle boundary (`FD-P7-001 §5`, `§6` — `E7-02`, `E7-04`,
`E7-05`).

`FD-P7-001 §5` assigns this boundary a specific and exclusive set of
responsibilities: *"admission, retention, retrieval eligibility, update,
consolidation, supersession, expiry and invalidation."* Everything here is one of
those. Nothing else is.

**What this boundary is not.** `FD-P7-001 §10` fixes `Memory ≠ Knowledge` and
*"Memory admission ≠ Knowledge promotion."* The admission below moves a Candidate
into retained Memory. It confers no Knowledge status, invokes no Governance
authority, and touches nothing T-12 governs. `memory_spec`'s standing rule —
Memory is non-authoritative and never self-promoting to Knowledge — is unchanged:
`PromotionCandidate` and `generate_candidates` remain the only Knowledge-facing
surface, they remain observations, and Governance still decides them.

**Who may call, and what that does not confer.** `FD-P7-001 §5` lets Agent and
Execution *"produce Information"* and *"generate or propose a Memory Candidate"*,
while withholding authority to *"directly admit Memory"* or *"directly mutate
admitted Memory lifecycle state."* That separation is structural here, not
advisory: a Candidate carries no state to admit itself with, admission is a
method on this boundary, and `MemoryItem` is frozen so no caller can transition
one by assignment. `FD-P7-002 §3` withholds the same from Runtime, which may
reach this boundary but *"must not... directly manipulate Memory internal state
outside the lawful Memory boundary"* — and reaching a boundary through a property
is not manipulating its internals.

**Retention decides; it does not merely record.** `E7-02.3` requires retention to
be *"lifecycle-governed"*. A retention rule is supplied at construction and
consulted on every admission; refusing a Candidate is a lawful outcome and
produces no Memory at all, which is what makes admission a decision rather than a
formality.

Dependencies: this package and stdlib. Nothing from Governance, Knowledge, Agent,
Runtime, Execution or any other boundary.
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple

from .exceptions import (
    InvalidMemoryItem,
    InvalidMemoryTransition,
    MemoryNotFound,
)
from .lifecycle import (
    MemoryCandidate,
    MemoryIdentity,
    MemoryItem,
    MemoryProvenance,
    MemoryState,
)
from .store import MemoryLifecycleStore

#: A retention rule: given a Candidate, may it be retained? The default retains
#: every well-formed Candidate — Memory is *"dynamic, provisional"* substrate and
#: a restrictive default would be a policy this Decision does not state. Callers
#: with a real retention policy supply it; `E7-02` requires the decision to exist
#: at this boundary, not that it be strict.
RetentionRule = Callable[[MemoryCandidate], bool]


def retain_everything(candidate: "MemoryCandidate") -> bool:
    """The default retention rule. Named rather than a lambda so that what is
    being decided, and by whom, is visible in a stack trace."""
    return True


class MemoryLifecycle:
    """The single authority over a Memory's lifecycle.

    Constructed over a store and a retention rule. It holds no Agent, no
    Execution, no Runtime and no Governance collaborator — it cannot ask
    permission of anything, and nothing can instruct it to skip a transition.
    """

    def __init__(
        self,
        store: MemoryLifecycleStore,
        retention_rule: "Optional[RetentionRule]" = None,
    ) -> None:
        if not isinstance(store, MemoryLifecycleStore):
            raise InvalidMemoryItem("the Memory lifecycle requires a lifecycle store")
        self._store = store
        self._retention_rule: RetentionRule = retention_rule or retain_everything

    # -- E7-01: Information → Candidate -----------------------------------

    @staticmethod
    def form_candidate(
        key: str, payload: "object", source: str, detail: "object" = None
    ) -> MemoryCandidate:
        """Form a Memory Candidate from Information (`E7-01.7`, `E7-01.8`).

        Deliberately a `@staticmethod`: forming a Candidate requires no lifecycle
        state and confers none. A caller that can form Candidates has gained
        nothing it can admit with, which is `E7-01.9` made structural rather than
        promised.
        """
        return MemoryCandidate(
            key=key, payload=payload, provenance=MemoryProvenance(source, detail)
        )

    # -- E7-02: admission and retention ------------------------------------

    def admit(self, candidate: MemoryCandidate) -> Optional[MemoryItem]:
        """Decide admission of a Candidate, and retain it if admitted.

        Returns the retained Memory, or `None` when the retention rule refuses —
        an explicit refusal, never a silently unretained item the caller might
        mistake for success. Refusal produces no Memory: there is no
        half-admitted state, because `E7-02` distinguishes *candidate proposed*
        from *Memory admitted / retained* and a third state between them would
        blur exactly what the criterion separates.
        """
        if not isinstance(candidate, MemoryCandidate):
            raise InvalidMemoryItem("only a MemoryCandidate can be admitted")
        if not self._retention_rule(candidate):
            return None
        at = self._store.next_sequence()
        ordinal = len(self._store.line(candidate.key)) + 1
        item = MemoryItem(
            identity=MemoryIdentity(candidate.key, ordinal),
            payload=candidate.payload,
            state=MemoryState.RETAINED,
            provenance=candidate.provenance,
            recorded_at=at,
            updated_at=at,
        )
        self._store.retain(item)
        return item

    # -- E7-04: update and consolidation -----------------------------------

    def update(self, key: str, payload: "object") -> MemoryItem:
        """Supersede the eligible Memory at `key` with a new retained version.

        The predecessor moves to `SUPERSEDED` and is **kept**; the successor
        records what it supersedes. `E7-04` forbids silent mutation and dangling
        references, so neither the old payload nor the link to it is discarded.
        """
        current = self._eligible_or_raise(key)
        at = self._store.next_sequence()
        self._store.replace(current.transition_to(MemoryState.SUPERSEDED, at))
        successor = MemoryItem(
            identity=MemoryIdentity(key, current.identity.ordinal + 1),
            payload=payload,
            state=MemoryState.RETAINED,
            provenance=current.provenance,
            recorded_at=at,
            updated_at=at,
            supersedes=current.identity,
        )
        self._store.retain(successor)
        return successor

    def consolidate(
        self, keys: "Tuple[str, ...]", into_key: str, payload: "object"
    ) -> MemoryItem:
        """Consolidate several eligible Memories into one (`E7-04`).

        Every source must be eligible; if any is not, nothing is consolidated and
        nothing is transitioned. Partial consolidation is precisely the
        *"contradictory lifecycle state"* `E7-04` prohibits — some sources
        retired into a Memory that was never created.

        Sources move to `SUPERSEDED`. When the destination is one of the sources,
        it supersedes itself in the ordinary way: the line continues, so no
        identity is reused and no version is lost.
        """
        if not keys:
            raise InvalidMemoryTransition("consolidation requires at least one source")
        sources = [self._eligible_or_raise(k) for k in keys]  # all-or-nothing
        at = self._store.next_sequence()
        for source in sources:
            self._store.replace(source.transition_to(MemoryState.SUPERSEDED, at))
        ordinal = len(self._store.line(into_key)) + 1
        consolidated = MemoryItem(
            identity=MemoryIdentity(into_key, ordinal),
            payload=payload,
            state=MemoryState.RETAINED,
            provenance=MemoryProvenance(
                source="consolidation", detail=tuple(str(s.identity) for s in sources)
            ),
            recorded_at=at,
            updated_at=at,
            supersedes=sources[0].identity,
        )
        self._store.retain(consolidated)
        return consolidated

    # -- E7-05: expiry and invalidation -------------------------------------

    def expire(self, key: str) -> MemoryItem:
        """Expire the eligible Memory at `key` (`E7-05.1`).

        Expiry is an explicit lifecycle operation, invoked by whoever holds a
        retention policy. `FD-P7-001 §6` states that automatic scheduling is not
        required — no cron, worker, scheduler or TTL daemon — and none is created
        here. Introducing one would also mean building a Scheduler, which the
        Phase 3 residual leaves explicitly unauthorized.
        """
        current = self._eligible_or_raise(key)
        expired = current.transition_to(MemoryState.EXPIRED, self._store.next_sequence())
        self._store.replace(expired)
        return expired

    def invalidate(self, key: str) -> MemoryItem:
        """Invalidate the eligible Memory at `key` (`E7-05.2`).

        Distinct from expiry: expiry says the Memory's time passed, invalidation
        says it should not have been relied upon. Both end eligibility; keeping
        them separate preserves *why*, which a single terminal state would lose.
        """
        current = self._eligible_or_raise(key)
        invalid = current.transition_to(
            MemoryState.INVALIDATED, self._store.next_sequence()
        )
        self._store.replace(invalid)
        return invalid

    # -- internal ----------------------------------------------------------

    def _eligible_or_raise(self, key: str) -> MemoryItem:
        """The eligible Memory at `key`, or a refusal naming why.

        Fails closed: an operation against a key with no eligible Memory is
        invalid, and returning `None` here would let a caller proceed as though
        it had transitioned something.
        """
        newest = self._store.newest(key)
        if newest is None:
            raise MemoryNotFound(f"no Memory is retained at {key!r}")
        if not newest.is_eligible:
            raise InvalidMemoryTransition(
                f"{newest.identity} is {newest.state.value!r} and is not eligible "
                f"for a lifecycle operation"
            )
        return newest
