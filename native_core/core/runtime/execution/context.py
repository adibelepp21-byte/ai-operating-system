"""
Execution context (Blueprint §6; runtime_spec §3/§6).

`ExecutionContext` represents **execution identity only** — the hosting Runtime's
identity and the execution ordinal it issued. It is transient, immutable, and
carries nothing else.

Fields are exactly the two the architecture already ratifies (they mirror the
Phase 4.0 `RuntimeContext`, which is the canonical issuer):
  - `runtime_id`
  - `execution_sequence`

`execution_id` is **deliberately absent**: the directive permits it "only if
already ratified by architecture", and verification against source shows no
`execution_id` exists anywhere in the frozen Native Core. None is invented.

Forbidden and absent: timestamps, clocks, UUID generation, randomness, mutable
collections, and any subsystem reference. A context is identity metadata, never
a channel to a subsystem — so it can never become a back-door around the
Runtime's controlled access boundary.

Ownership: the Execution layer (Runtime-owned). Dependencies: this package's
`exceptions` only. Stdlib otherwise. No authority, no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InvalidExecutionConfiguration


@dataclass(frozen=True)
class ExecutionContext:
    """Immutable execution identity. Frozen, hashable, comparable; carries only
    the hosting Runtime's identity and the Runtime-issued execution ordinal."""

    runtime_id: str
    execution_sequence: int

    def __post_init__(self):
        if not isinstance(self.runtime_id, str) or not self.runtime_id.strip():
            raise InvalidExecutionConfiguration("runtime_id must be a non-empty string")
        # bool is a subclass of int; reject it explicitly.
        if not isinstance(self.execution_sequence, int) or isinstance(self.execution_sequence, bool):
            raise InvalidExecutionConfiguration("execution_sequence must be an integer")
        if self.execution_sequence < 0:
            raise InvalidExecutionConfiguration("execution_sequence must be non-negative")
