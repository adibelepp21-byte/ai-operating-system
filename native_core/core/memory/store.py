"""
Phase 7 Memory lifecycle store — retention of lifecycle-governed Memory.

Holds Memory items and the monotonic lifecycle sequence. It stores; it does not
decide. Every admission, supersession, expiry and invalidation decision belongs
to the lifecycle boundary (`admission.py`) — `FD-P7-001 §5` places admission,
retention, retrieval eligibility, update, consolidation, supersession, expiry
and invalidation with *"the Memory lifecycle boundary"*, and a store that also
decided would be that boundary in a second place.

**In-process by design, not by omission.** `FD-P7-001 §9` is explicit that
*"persistence across process restart is not an initial Phase 7 exit gate"* and
that persistent Memory is *"SUPPORTING / FUTURE CAPABILITY — NOT A PHASE 7
CERTIFICATION PREREQUISITE."* `ACT-CC-P7-002 §10` goes further and forbids
introducing database or persistence architecture. So this retains Memory for the
relevant execution lifecycle and names no storage engine, vendor or format. A
durable store may later replace it behind the same surface without any lifecycle
rule changing — which is the point of keeping the decision out of here.

**Append-only within a key.** A Memory's line of versions is retained in order
and prior versions are never removed or edited: `E7-04` forbids *"dangling
references"* and silent mutation, and supersession that erased its predecessor
would destroy the evidence that a supersession happened.

Dependencies: this package and stdlib. No Infrastructure facility is used —
Phase 7 requires no persistence, so importing one would create a dependency the
criteria do not need.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .exceptions import MemoryNotFound
from .lifecycle import MemoryIdentity, MemoryItem


class MemoryLifecycleStore:
    """Retention for lifecycle-governed Memory, keyed by Memory key.

    Owns two things and nothing else: the retained items, and the monotonic
    lifecycle sequence that stamps them. It exposes no admission, no expiry and
    no eligibility rule — those are the boundary's.
    """

    def __init__(self) -> None:
        self._lines: Dict[str, List[MemoryItem]] = {}
        self._sequence: int = 0

    # -- lifecycle sequence -----------------------------------------------

    def next_sequence(self) -> int:
        """Advance and return the monotonic lifecycle sequence.

        The *"timestamps or equivalent lifecycle metadata"* of `FD-P7-001 §4`.
        Monotonic and caller-independent, so ordering is a property of the
        lifecycle rather than of how fast a caller ran.
        """
        self._sequence += 1
        return self._sequence

    @property
    def sequence(self) -> int:
        """The current sequence, without advancing it."""
        return self._sequence

    # -- retention ---------------------------------------------------------

    def retain(self, item: MemoryItem) -> None:
        """Retain a Memory as the newest version of its key.

        Appends; never replaces. A caller that hands in an item whose ordinal
        does not continue the line is refused, because a line with a gap or a
        repeat is a contradictory lifecycle state.
        """
        line = self._lines.setdefault(item.key, [])
        expected = len(line) + 1
        if item.identity.ordinal != expected:
            raise MemoryNotFound(
                f"{item.identity} does not continue the retained line for "
                f"{item.key!r}; expected ordinal {expected}"
            )
        line.append(item)

    def replace(self, item: MemoryItem) -> None:
        """Record a state transition of an already-retained Memory.

        Replaces the stored item **at its own ordinal** with the transitioned
        one. This is not an in-place edit of a Memory — `MemoryItem` is frozen
        and `transition_to` produced a new value; this records which value is
        current for that ordinal. The identity is unchanged, so nothing is lost.
        """
        line = self._lines.get(item.key)
        if not line or item.identity.ordinal > len(line):
            raise MemoryNotFound(f"{item.identity} is not retained")
        line[item.identity.ordinal - 1] = item

    # -- reads (no eligibility rule applied here) ---------------------------

    def get(self, identity: MemoryIdentity) -> MemoryItem:
        """The retained item at an identity, in whatever state it holds."""
        line = self._lines.get(identity.key)
        if not line or identity.ordinal > len(line):
            raise MemoryNotFound(f"{identity} is not retained")
        return line[identity.ordinal - 1]

    def line(self, key: str) -> Tuple[MemoryItem, ...]:
        """The full retained version line for a key, oldest first.

        Every version, in every state — the boundary decides what is eligible,
        and a caller auditing a lifecycle needs to see the states it passed
        through, not only the survivor.
        """
        return tuple(self._lines.get(key, ()))

    def newest(self, key: str) -> Optional[MemoryItem]:
        """The most recent version of a key, in whatever state, or `None`."""
        line = self._lines.get(key)
        return line[-1] if line else None

    def keys(self) -> Tuple[str, ...]:
        """Every key the store retains, in insertion order."""
        return tuple(self._lines)
