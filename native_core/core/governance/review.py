"""
Governed review (governance_spec §1/§2/§4/§5/§10/§11; Freeze §8; INV-5/8; PR-3/PR-4).

The governed review surface. It:
  - consumes Memory observations and receives promotion candidates as evidence
    (governance_spec §5c/§7) — detect-and-surface only, deciding nothing (PR-3);
  - records already-made human review decisions (§5a) — never making one;
  - derives whether a candidate's promotion is authorised, purely by reflecting
    recorded human decisions (§5b) — a human `reject` is absolute, and the
    default is deny (fail closed, PR-4);
  - never creates Knowledge, never modifies Memory, never mutates Trace, and
    never bypasses human authority (§6.2 invariant 2).

Governance owns its decision records (§3): they are persisted append-only via
the Infrastructure storage facility beneath it — a decision, once recorded, is
permanent, and later decisions append (as the real resubmission case requires).
This is Governance-owned data, not Trace and not Knowledge.

Provenance hardening (Phase 3.286, closes Independent-Audit finding F-G1):
promotion authorization verifies **provenance, not mere existence**. Only a
decision produced by this Governance instance's own validated `record_decision`
path is authoritative — Governance records each such decision in an in-memory
provenance index, and `promotion_authorized`/`recorded_decisions` consult that
index, never the raw storage partition. A record injected directly into storage
(bypassing the HumanAuthority validation) therefore never enters the trusted
index and can never authorize promotion: forgery fails closed. The append-only
storage log is retained as the durable §3 audit record and is forward-compatible
with the reserved Identity/Authentication architecture, which — once ratified —
would supply a persistent, cross-process trust anchor over that log. Until then,
trust is deliberately process-scoped (a restart trusts nothing it did not itself
record — fail closed), because a persistent trust anchor is exactly what Identity/
Auth reserves (Freeze §10). No cryptography, identity, or authentication system
is introduced here.

Dependencies: Memory (candidates) and Infrastructure (decision storage) —
both permitted (Infrastructure ↓ Trace ↓ Memory ↓ Governance). Governance
holds no external dependency (INV-12), imports nothing from Knowledge, Agent,
Runtime, Workflow, Skill, Capability, or Optimization, and reads Trace only
transitively through the Memory candidates it consumes.

Reserved [O]: authority tiers/delegation (Constitution §3), the Trace-of-the-
decision produced via a future Agent-Instance acting path (INV-4; §9 — Agent/
Runtime are out of scope this phase), and Knowledge admission itself.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Any, Optional, Tuple

from ..infrastructure import StorageFacility
from ..memory import MemoryReader, PromotionCandidate
from .decision import ReviewDecision, canonical_content_key, to_bytes, to_payload, validate_decision

# Governance-owned, append-only partition of recorded decisions (§3).
DECISION_PARTITION = "governance_decisions"


def _freeze(value: Any) -> Any:
    """Deeply immutable snapshot: dict -> read-only mapping, list/tuple ->
    tuple, recursively; scalars unchanged. Used so a recorded decision snapshot
    cannot be altered after creation (closes F-H1). This changes no stored
    serialization and no schema — only the mutability of the in-memory
    provenance snapshot."""
    if isinstance(value, dict):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


class GovernanceError(RuntimeError):
    """Raised when a governed action cannot proceed accountably. Fail closed."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


class GovernanceReview:
    """Surfaces promotion candidates, records human decisions, and reflects
    recorded human authorisation — never deciding automatically."""

    def __init__(self, memory_reader: MemoryReader, decision_storage: StorageFacility):
        if memory_reader is None:
            raise GovernanceError(["GovernanceReview requires a MemoryReader (candidate evidence source)"])
        if decision_storage is None:
            raise GovernanceError(["GovernanceReview requires a decision StorageFacility"])
        self._memory_reader = memory_reader
        self._storage = decision_storage
        # In-memory authoritative provenance index (F-G1 hardening): only
        # decisions this instance produced via a validated record_decision enter
        # here. Authorization consults this, never raw storage. `_trusted_log`
        # preserves record order (published outcomes); `_trusted_by_key` indexes
        # by candidate for authorization lookup.
        self._trusted_log: list = []
        self._trusted_by_key: dict = {}

    # (c) read Memory (Trace-derived) for evidence; (surface, decide nothing)
    def pending_candidates(self, scope: Optional[str] = None) -> Tuple[PromotionCandidate, ...]:
        """Surface promotion candidates for human review. Reads Memory only;
        makes no decision, filters by nothing but the caller's scope."""
        return self._memory_reader.candidates(scope)

    # (a) accept an already-made human review decision; record it accountably
    def record_decision(self, review_decision: ReviewDecision) -> None:
        """Record an already-made human decision. Fail closed: if the decision
        lacks a human authority, a valid decision value, or a rationale, it
        raises and records nothing. Never makes or infers a decision.

        The decision is appended to the durable audit log (storage) and entered
        into the in-memory authoritative provenance index — the only decisions
        promotion authorization will ever trust (F-G1)."""
        errors = validate_decision(review_decision)
        if errors:
            raise GovernanceError(errors)
        self._storage.append(DECISION_PARTITION, to_bytes(review_decision))  # durable §3 audit log
        # Authoritative provenance: this decision was produced by Governance.
        # Stored as a deeply-immutable snapshot so neither a caller (via the
        # recorded_decisions() return) nor a shared reference can alter it or
        # the authorization outcome after the fact (closes F-H1).
        snapshot = _freeze(to_payload(review_decision))
        self._trusted_log.append(snapshot)
        key = canonical_content_key(review_decision.candidate.scope, review_decision.candidate.observed_content)
        self._trusted_by_key.setdefault(key, []).append(snapshot)

    # (d) publish decision outcomes — the provenance-verified decisions only
    def recorded_decisions(self) -> Tuple[dict, ...]:
        """Every decision this Governance produced, in record order. Reflects the
        authoritative provenance index, not raw storage — so a record injected
        into storage never appears here (F-G1)."""
        return tuple(self._trusted_log)

    # (b) authorize/deny promotion — by reflecting PROVENANCE-VERIFIED human decisions only
    def promotion_authorized(self, candidate: PromotionCandidate) -> bool:
        """True iff a human `approve` produced by this Governance is on record for
        this candidate and no human `reject` is (a reject is absolute). Default is
        deny — absence of an authorising, provenance-verified human decision means
        no promotion (fail closed, §11). Consults only the authoritative provenance
        index; a forged storage entry can never authorise (F-G1). Makes no decision."""
        key = canonical_content_key(candidate.scope, candidate.observed_content)
        relevant = self._trusted_by_key.get(key, ())
        if any(d.get("decision") == "reject" for d in relevant):
            return False  # human reject is absolute
        if any(d.get("decision") == "approve" for d in relevant):
            return True
        return False  # fail closed: no authorising decision -> no promotion
