"""
Optimization Proposal — IMMUTABLE VALUE OBJECT (Blueprint §15;
optimization_spec §2/§4/§5/§10; PR-3; INV-8).

An `OptimizationProposal` is the passive object Optimization publishes for
**optional future consumption**. It is a proposal in the plain sense: something
put forward, resting on recorded observations, addressed to nobody.

Per the P7-I27 Conflict A ruling, Optimization **does not submit proposals to
Governance**. There is no Governance dependency in this boundary, no submit,
send, notify, or request operation anywhere, and no promotion path. A proposal
is published and left; Governance may later read it through its own mechanisms
if a future authorized baseline permits, and that integration does not exist
today.

Evidence-bearing by construction: a proposal cannot be built without at least
one observation behind it, so an ungrounded proposal is **unrepresentable**
rather than merely discouraged.

Deliberately ABSENT — no score, rating, rank, priority, weight, confidence,
severity, urgency, recommendation, suggested action, or decision. Those belong
to the reserved evaluation-scoring, prioritization, and recommendation models
(optimization_spec §14; P7-I27 Conflict B ruling), and none is implemented here.
A proposal also carries no authority: it authorizes nothing, promotes nothing,
and decides nothing (PR-3; INV-8; §6.2 invariant 2).

Ownership: Optimization. Dependencies: this package's `observation` and
`exceptions` only (stdlib otherwise). No authority, no business logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .exceptions import InvalidProposal
from .observation import OptimizationObservation


@dataclass(frozen=True)
class OptimizationProposal:
    """Something put forward, resting on the observations behind it.

    Frozen, hashable, and comparable by value. Carries its own identity and the
    immutable observations it rests on — and nothing that ranks, scores, or
    decides."""

    proposal_key: str
    observations: Tuple[OptimizationObservation, ...]

    def __post_init__(self):
        if not isinstance(self.proposal_key, str) or not self.proposal_key.strip():
            raise InvalidProposal("proposal_key must be a non-empty string")
        if not isinstance(self.observations, tuple):
            raise InvalidProposal(
                "observations must be a tuple; a mutable sequence would let the "
                "evidence behind a proposal change after it was put forward"
            )
        if not self.observations:
            raise InvalidProposal(
                "a proposal requires at least one observation; a proposal with no "
                "evidence behind it is never constructed"
            )
        for item in self.observations:
            if not isinstance(item, OptimizationObservation):
                raise InvalidProposal(
                    "every element of observations must be an OptimizationObservation"
                )
