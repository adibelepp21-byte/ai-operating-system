"""
Phase 7 Memory lifecycle representation (`FD-P7-001 §4`, `§6` — `E7-01`).

`FD-P7-001` fixes Phase 7 as *"a Memory Ecosystem as a lifecycle capability, not
merely as storage"*, with the canonical lifecycle:

```text
Information → Memory Candidate → Admission/Retention → Retrieval
            → Update/Consolidation → Expiry/Invalidation
```

This module defines what a Memory **is** across that lifecycle. It holds no
store, no boundary logic and no retrieval; those are siblings.

**Why this is additive and not a redefinition.** The resident `MemoryRecord`
(`record.py`) is a Trace-derived observation that is *"deliberately without a
stable identity across derivations"* — that is its design, and Phase 7 does not
touch it. `E7-01` requires something the observation record deliberately is not:
a thing with **identity** and **lifecycle state** that persists across
transitions. So Phase 7 adds `MemoryItem` alongside `MemoryRecord` rather than
mutating it. A `MemoryRecord` is a natural *Information* input to candidate
formation; it is not itself a lifecycle-governed Memory.

**The T-12 distinction, stated because it is easy to blur.** `FD-P7-001 §10` is
explicit: `Memory ≠ Knowledge`, and *"Memory admission ≠ Knowledge promotion."*
The admission modelled here is **Memory's own lifecycle admission** — a Candidate
becoming a retained Memory. It is not the T-12 Knowledge gate, confers no
Knowledge status, and gives Memory no authority it did not have. Memory remains
what `memory_spec` says it is: non-authoritative, never self-promoting to
Knowledge. `PromotionCandidate` (`candidate.py`) remains the *Knowledge*
promotion observation and is untouched by this module.

**Timestamps.** `FD-P7-001 §4` requires *"timestamps or equivalent lifecycle
metadata"*. A monotonic logical sequence is used rather than a wall clock: it is
technology-neutral (Constitution §6.2 invariant 1 forbids naming an
infrastructure dependency, and a clock source is one), and it is what makes
`E7-03`'s *"deterministic-core behavior"* achievable — the same request against
the same eligible state cannot vary because time moved.

Dependencies: stdlib only. Nothing from Governance, Knowledge, Agent, Runtime,
Execution, Workflow, Skill, Capability or Optimization — the Memory boundary's
isolation rule is unchanged by Phase 7.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Optional, Tuple

from .exceptions import InvalidMemoryItem, InvalidMemoryTransition


class MemoryState(Enum):
    """The lifecycle states a Memory occupies.

    `CANDIDATE` is pre-admission: proposed, not retained, and never eligible for
    retrieval. `RETAINED` is the single eligible state. The three terminal
    states are distinct on purpose — `E7-04` and `E7-05` ask for supersession,
    expiry and invalidation as separate capabilities, and collapsing them would
    lose the reason a Memory stopped being eligible.
    """

    CANDIDATE = "candidate"
    RETAINED = "retained"
    SUPERSEDED = "superseded"
    EXPIRED = "expired"
    INVALIDATED = "invalidated"


#: The only state in which a Memory is eligible for ordinary retrieval
#: (`E7-03.3`, `E7-05.3`/`.4`). Everything else — including a Candidate that was
#: never admitted — is ineligible.
ELIGIBLE_STATES: Tuple[MemoryState, ...] = (MemoryState.RETAINED,)

#: Lawful transitions. A Candidate may be admitted or invalidated; a retained
#: Memory may be superseded, expire, or be invalidated. Terminal states have no
#: outgoing transition: `E7-05` requires that lifecycle transitions be *valid*,
#: and resurrecting an expired or invalidated Memory would make "ineligible"
#: mean nothing.
LAWFUL_TRANSITIONS: Mapping[MemoryState, Tuple[MemoryState, ...]] = MappingProxyType({
    MemoryState.CANDIDATE: (MemoryState.RETAINED, MemoryState.INVALIDATED),
    MemoryState.RETAINED: (
        MemoryState.SUPERSEDED,
        MemoryState.EXPIRED,
        MemoryState.INVALIDATED,
    ),
    MemoryState.SUPERSEDED: (),
    MemoryState.EXPIRED: (),
    MemoryState.INVALIDATED: (),
})


def _freeze(value: Any) -> Any:
    """Deeply immutable snapshot, local to Memory so the boundary stays
    self-contained. Mirrors `record.py`'s helper rather than importing it, for
    the same module-isolation reason that one exists."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class MemoryProvenance:
    """Where a Memory came from (`E7-01.5`).

    `source` names the origin kind — an Agent Instance scope, a Trace
    derivation, a caller. `detail` carries whatever that origin needs to
    identify itself. Provenance is recorded, never interpreted: Memory does not
    rank or trust its sources, which would be a judgement it holds no authority
    to make.
    """

    source: str
    detail: Any = None

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source.strip():
            raise InvalidMemoryItem("provenance must name a source")
        object.__setattr__(self, "detail", _freeze(self.detail))


@dataclass(frozen=True)
class MemoryCandidate:
    """Information proposed as Memory, before any lifecycle decision (`E7-01.7`).

    A Candidate is **not** a Memory. It carries no lifecycle state and no
    identity, because neither has been conferred yet — conferring them is the
    lifecycle boundary's act, and a Candidate that already looked admitted would
    let a proposer manufacture admission by construction. `E7-01.9` requires
    exactly this: forming a Candidate *"does not itself grant direct admission
    authority to Agent or Execution."*
    """

    key: str
    payload: Any
    provenance: MemoryProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.key, str) or not self.key.strip():
            raise InvalidMemoryItem("a Memory Candidate must carry a key")
        if not isinstance(self.provenance, MemoryProvenance):
            raise InvalidMemoryItem("a Memory Candidate must carry provenance")
        object.__setattr__(self, "payload", _freeze(self.payload))


@dataclass(frozen=True)
class MemoryIdentity:
    """A Memory's stable identity (`E7-01.2`, `E7-05.7`).

    `key` groups the lifecycle line — successive versions of the same Memory
    share it. `ordinal` distinguishes them within that line. Together they
    remain valid *"throughout its applicable lifecycle"*: a superseded Memory
    keeps the identity it had, which is what makes supersession traceable rather
    than a silent overwrite.
    """

    key: str
    ordinal: int

    def __post_init__(self) -> None:
        if not isinstance(self.key, str) or not self.key.strip():
            raise InvalidMemoryItem("a Memory identity must carry a key")
        if not isinstance(self.ordinal, int) or self.ordinal < 1:
            raise InvalidMemoryItem("a Memory ordinal is 1-based")

    def __str__(self) -> str:
        return f"{self.key}#{self.ordinal}"


@dataclass(frozen=True)
class MemoryItem:
    """A lifecycle-governed Memory — the `E7-01` representation.

    Carries all five required elements: **identity**, **payload**, **lifecycle
    state**, **provenance**, and lifecycle **timestamps** (a monotonic logical
    sequence, see the module header). Frozen: a Memory whose state could be
    edited in place by whoever holds a reference would make every lifecycle
    guarantee unenforceable, so transitions produce new items instead
    (`transition_to`).
    """

    identity: MemoryIdentity
    payload: Any
    state: MemoryState
    provenance: MemoryProvenance
    recorded_at: int
    updated_at: int
    supersedes: Optional[MemoryIdentity] = field(default=None)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, MemoryIdentity):
            raise InvalidMemoryItem("a Memory must carry a MemoryIdentity")
        if not isinstance(self.state, MemoryState):
            raise InvalidMemoryItem("a Memory must carry a MemoryState")
        if not isinstance(self.provenance, MemoryProvenance):
            raise InvalidMemoryItem("a Memory must carry provenance")
        if not isinstance(self.recorded_at, int) or self.recorded_at < 0:
            raise InvalidMemoryItem("lifecycle metadata must carry a sequence")
        if not isinstance(self.updated_at, int) or self.updated_at < self.recorded_at:
            raise InvalidMemoryItem("a Memory cannot be updated before it was recorded")
        object.__setattr__(self, "payload", _freeze(self.payload))

    @property
    def key(self) -> str:
        return self.identity.key

    @property
    def is_eligible(self) -> bool:
        """Whether ordinary retrieval may return this Memory (`E7-05.3`)."""
        return self.state in ELIGIBLE_STATES

    def transition_to(self, state: "MemoryState", at: int) -> "MemoryItem":
        """Produce the same Memory in a new lawful state.

        Refuses an unlawful transition rather than coercing it (`E7-04`: no
        *"silent state mutation"*, no *"contradictory lifecycle state"*). The
        identity is preserved, so a Memory remains the same Memory across its
        lifecycle even as its eligibility changes.
        """
        if not isinstance(state, MemoryState):
            raise InvalidMemoryTransition("a transition target must be a MemoryState")
        allowed = LAWFUL_TRANSITIONS[self.state]
        if state not in allowed:
            raise InvalidMemoryTransition(
                f"{self.identity} cannot move {self.state.value!r} → {state.value!r}; "
                f"lawful targets are {tuple(s.value for s in allowed)!r}"
            )
        if at < self.updated_at:
            raise InvalidMemoryTransition(
                f"{self.identity} cannot transition backwards in lifecycle sequence"
            )
        return MemoryItem(
            identity=self.identity,
            payload=self.payload,
            state=state,
            provenance=self.provenance,
            recorded_at=self.recorded_at,
            updated_at=at,
            supersedes=self.supersedes,
        )
