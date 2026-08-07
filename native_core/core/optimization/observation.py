"""
Optimization Observation — IMMUTABLE VALUE OBJECT (Blueprint §15;
optimization_spec §2/§3/§9; PR-3; INV-5).

An `OptimizationObservation` records **that something was observed, and where** —
nothing more. It is the passive object the boundary publishes.

It is deliberately **not** an evaluation. It carries no score, no rating, no
rank, no priority, no confidence, no severity, no recommendation, and no
suggested action. Those belong to the signal catalogue, the evaluation-scoring
model, and the prioritization model, all of which remain **Architect Reserved**
(optimization_spec §14; P7-I27 Conflict B ruling) and are absent here.

Ownership (Blueprint §15): Optimization owns **non-authoritative** derived
records only. An observation is authoritative for nothing. Trace remains the
sole immutable history (INV-5); Memory remains the derivation; Knowledge remains
the authority; Governance remains the decision-maker (PR-3).

Immutability: a frozen dataclass over immutable content. `observed` holds the
record as it was read — a frozen Trace or Memory record — and a mutable builtin
container is refused, so an observation can never alias state that changes
underneath it, and observing can never mutate what was observed (INV-5).

Ownership: Optimization. Dependencies: this package's `exceptions` only (stdlib
otherwise). No authority, no business logic, no decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .exceptions import InvalidObservation

#: The boundaries Optimization is permitted to observe (optimization_spec §7:
#: *"Reads Trace (evidence) and Memory (derivation)"*). The set is closed: an
#: observation naming any other source is refused.
TRACE_SOURCE = "trace"
MEMORY_SOURCE = "memory"
OBSERVABLE_SOURCES = frozenset({TRACE_SOURCE, MEMORY_SOURCE})

#: Builtin containers that would let an observation alias mutable state.
_MUTABLE_CONTAINERS = (list, dict, set, bytearray)


@dataclass(frozen=True)
class OptimizationObservation:
    """One immutable record that something was observed, and from where.

    Frozen and comparable by value. Carries the observed source, the subject it
    concerns, and the content exactly as read — and carries no judgement about
    any of them."""

    source: str
    subject: str
    observed: Any

    def __post_init__(self):
        if self.source not in OBSERVABLE_SOURCES:
            raise InvalidObservation(
                f"source must be one of {sorted(OBSERVABLE_SOURCES)}; got {self.source!r}"
            )
        if not isinstance(self.subject, str) or not self.subject.strip():
            raise InvalidObservation("subject must be a non-empty string")
        if isinstance(self.observed, _MUTABLE_CONTAINERS):
            raise InvalidObservation(
                "observed content must be immutable; a mutable container would let "
                "an observation alias state that changes after it was recorded"
            )
