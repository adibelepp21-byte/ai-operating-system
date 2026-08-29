"""
Phase 7 Memory lifecycle exceptions (`FD-P7-001 §6`).

Every condition the lifecycle names as invalid raises here rather than being
coerced into a usable value — `PR-4`, fail closed. That matters more than usual
in this boundary: `E7-02.7` requires that *"invalid lifecycle bypass is
rejected"* and `E7-05.3`/`.4` require that ineligible Memory is not treated as
active. A lifecycle that returned a soft failure instead of raising would let a
caller proceed on Memory the boundary had already refused.

**Deliberately absent: an exception for retrieving nothing.** A key with no
eligible Memory is an ordinary, lawful outcome and yields `None` — an explicit
absence. Raising there would make "this Memory expired" indistinguishable from
"this operation was invalid", and `E7-05` needs those to be different.

Named separately from the errors of other boundaries so that a caller can tell a
Memory lifecycle refusal from an Infrastructure or Trace failure. Stdlib only.
"""

from __future__ import annotations


class MemoryLifecycleError(Exception):
    """Base for every Phase 7 Memory lifecycle failure."""


class InvalidMemoryItem(MemoryLifecycleError, ValueError):
    """A Memory, Candidate, identity or provenance is malformed.

    Raised at construction, so a malformed Memory never exists to be stored,
    retrieved or transitioned. `E7-01` requires identity, payload, state,
    provenance and lifecycle metadata; an object missing one of them is not a
    Memory, and pretending otherwise would make the criterion unmeasurable.
    """


class InvalidMemoryTransition(MemoryLifecycleError):
    """A lifecycle transition is not lawful from the current state.

    Covers both an undefined transition (`expired → retained`) and a backwards
    move in lifecycle sequence. `E7-04` forbids *"contradictory lifecycle
    state"*; this is where that is enforced rather than merely documented.
    """


class MemoryNotFound(MemoryLifecycleError):
    """An operation names a Memory the lifecycle does not hold.

    Distinct from retrieving nothing: asking to expire a Memory that was never
    admitted is an invalid *operation*, whereas reading a key with no eligible
    Memory is a valid question with an empty answer.
    """


class UnauthorizedMemoryMutation(MemoryLifecycleError):
    """A caller attempted to change admitted Memory state outside the lifecycle
    boundary.

    `FD-P7-001 §5` withholds this from Agent and Execution in terms: they *"must
    not... directly mutate admitted Memory lifecycle state"*, and `FD-P7-002 §3`
    withholds it from Runtime, which *"must not... directly manipulate Memory
    internal state outside the lawful Memory boundary."* This is the named
    failure for that boundary being crossed.
    """
