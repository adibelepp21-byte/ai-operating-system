"""
Review decision (governance_spec §2/§4/§5; Freeze INV-6/INV-8; PR-3/PR-4).

A ReviewDecision is an **already-made human judgment** about a promotion
candidate — approve or deny (reject). Governance *records* it; it never makes
one (governance_spec §4/§5; §6.2 invariant 2). There is no ranking, no
threshold, no confidence gate, and no automatic decision anywhere in this
module: the decision value arrives from a human, carried with that human's
authority.

Capture, don't reference (INV-6 discipline, from the CANONICAL_REFERENCE
review-decision design): a recorded decision embeds the **full candidate
snapshot** it decided on, so what the reviewer actually saw is captured
permanently, independent of any later re-derivation of Memory.

Fail closed (PR-4): a decision missing its human authority, a valid decision
value, or a rationale is invalid and records nothing.

`edit` (human-edited content before promotion) is [O] reserved — it concerns
Knowledge admission, which does not yet exist; this module implements the
authorize/deny core only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, List, Mapping

from ..memory import PromotionCandidate
from .authority import HumanAuthority

# Authorize or deny. `edit` is [O] reserved (relates to Knowledge admission).
VALID_DECISIONS = frozenset({"approve", "reject"})


class InvalidDecision(ValueError):
    """Raised when a decision cannot be recorded accountably. Fail closed."""


@dataclass(frozen=True)
class ReviewDecision:
    """One recorded human review decision over a promotion candidate."""

    candidate: PromotionCandidate  # full snapshot, captured at record time (INV-6)
    decision: str                  # "approve" | "reject"
    authority: HumanAuthority      # the human accountable for this decision
    rationale: str                 # why — required; a decision without a reason is not accountable


def validate_decision(d: ReviewDecision) -> List[str]:
    """Pure: returns the list of reasons a decision is invalid (empty = valid).
    Never guesses a missing value; never infers a decision."""
    errors: List[str] = []
    if not isinstance(d.candidate, PromotionCandidate):
        errors.append("candidate must be a PromotionCandidate snapshot")
    if d.decision not in VALID_DECISIONS:
        errors.append(f"decision must be one of {sorted(VALID_DECISIONS)}, got {d.decision!r}")
    if not isinstance(d.authority, HumanAuthority):
        errors.append("decision requires a HumanAuthority (automation may not decide)")
    if not isinstance(d.rationale, str) or not d.rationale.strip():
        errors.append("rationale is required and must be non-empty")
    return errors


def _to_plain(value: Any) -> Any:
    """Read-only mapping -> dict, tuple -> list, recursively — JSON-native."""
    if isinstance(value, Mapping):
        return {k: _to_plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_plain(v) for v in value]
    return value


def canonical_content_key(scope: str, content: Any):
    """Deterministic, hashable key identifying a candidate by (scope, content),
    used to match a decision to the candidate it decided on. Mappings sort by
    key; sequences preserve order."""
    def _h(v: Any):
        if isinstance(v, Mapping):
            return tuple(sorted((k, _h(x)) for k, x in v.items()))
        if isinstance(v, (list, tuple)):
            return tuple(_h(x) for x in v)
        return v
    return (scope, _h(content))


def to_payload(d: ReviewDecision) -> dict:
    """The full, JSON-native snapshot of a recorded decision, captured at record
    time (INV-6): the candidate it decided on, the decision, the human reviewer,
    and the rationale. Used both for the durable audit log and for Governance's
    in-memory authoritative provenance index."""
    return {
        "scope": d.candidate.scope,
        "content": _to_plain(d.candidate.observed_content),
        "occurrence_count": d.candidate.occurrence_count,
        "decision": d.decision,
        "reviewer_id": d.authority.reviewer_id,
        "rationale": d.rationale,
    }


def to_bytes(d: ReviewDecision) -> bytes:
    """Deterministic serialization of a recorded decision (stdlib json).
    Embeds the full candidate snapshot (capture at record time, INV-6)."""
    return json.dumps(to_payload(d), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def from_bytes(raw: bytes) -> dict:
    """Reconstruct a recorded decision's plain mapping from its stored bytes."""
    return json.loads(raw.decode("utf-8"))
