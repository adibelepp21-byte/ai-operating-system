"""
Runtime execution context (Blueprint §6; runtime_spec §3/§6).

A `RuntimeContext` carries **execution metadata only** — the identity of the
hosting Runtime and a deterministic execution identifier. It is transient
hosting state (runtime_spec §3), immutable once created.

Deliberately carries **no**: business knowledge, Memory contents, Governance
decisions, Agent state, Knowledge objects, or any subsystem reference. A context
is metadata about an execution, never a channel to a subsystem — so it can never
become a back-door around the Runtime's controlled access boundary.

**No timestamp.** The Phase 4.0 directive permits a timestamp only "if already
approved by architecture". Verified directly against source: no timestamp exists
anywhere in the frozen Native Core — Trace deliberately omits one (its schema is
exactly the ten Domain Model §2.1 fields, and "no timestamp field is introduced"
to supply ordering). No approval exists, so none is introduced here; a clock
would also make execution non-deterministic.

**No UUID / randomness.** `execution_sequence` is a monotonic ordinal issued by
the hosting Runtime, so contexts are deterministic and reproducible.

Ownership: Runtime. Dependencies: stdlib only. No authority, no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InvalidRuntimeConfiguration


@dataclass(frozen=True)
class RuntimeContext:
    """Immutable execution metadata issued by a hosting Runtime.

    `runtime_id` identifies the hosting Runtime; `execution_sequence` is a
    monotonic ordinal within that Runtime. Frozen, hashable, comparable — and
    carrying nothing but these two facts."""

    runtime_id: str
    execution_sequence: int

    def __post_init__(self):
        if not isinstance(self.runtime_id, str) or not self.runtime_id.strip():
            raise InvalidRuntimeConfiguration("runtime_id must be a non-empty string")
        # bool is a subclass of int; reject it explicitly.
        if not isinstance(self.execution_sequence, int) or isinstance(self.execution_sequence, bool):
            raise InvalidRuntimeConfiguration("execution_sequence must be an integer")
        if self.execution_sequence < 0:
            raise InvalidRuntimeConfiguration("execution_sequence must be non-negative")
