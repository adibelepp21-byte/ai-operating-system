"""
Governance boundary (Native Core Blueprint §5; governance_spec; Freeze §8; INV-8).

Governance holds authority over decisions and the Memory→Knowledge promotion
(Freeze §8; INV-8). It makes execution accountable and is never overridable by
automation (Constitution §6.2 invariant 2). It consumes Memory observations,
receives promotion candidates as evidence, records already-made human review
decisions, and reflects those decisions to authorise or deny promotion —
deciding **nothing** automatically (PR-3), and failing closed on the absence of
an authorising human decision (PR-4).

Governance never creates Knowledge, never modifies Memory, never mutates Trace,
and never bypasses human authority. It owns its decision records (§3), stored
append-only via the Infrastructure facility.

Module isolation (Blueprint §26): depends only on Memory (candidates) and the
Infrastructure storage facility beneath it; imports nothing from Knowledge,
Capability, Skill, Workflow, Agent, Runtime, or Optimization; holds no external
dependency (INV-12); and authors no Trace (the Trace-of-a-decision via a future
Agent-Instance acting path is [O] reserved — INV-4/§9).

Public surface:
  - authority: HumanAuthority, InvalidAuthority
  - decision:  ReviewDecision, VALID_DECISIONS, validate_decision, InvalidDecision
  - review:    GovernanceReview, GovernanceError, DECISION_PARTITION
"""

from .authority import HumanAuthority, InvalidAuthority
from .decision import (
    VALID_DECISIONS,
    InvalidDecision,
    ReviewDecision,
    validate_decision,
)
from .review import DECISION_PARTITION, GovernanceError, GovernanceReview

__all__ = [
    "HumanAuthority",
    "InvalidAuthority",
    "ReviewDecision",
    "VALID_DECISIONS",
    "validate_decision",
    "InvalidDecision",
    "GovernanceReview",
    "GovernanceError",
    "DECISION_PARTITION",
]
