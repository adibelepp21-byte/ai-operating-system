"""
Governance Observation Stabilization — read-only measurement of real
human_review_decision_recorded events.

Pure, read-only, no side effects: reads Trace records, extracts every
real Human Review Decision event, and computes descriptive measurements
only. Never scores reviewer quality, never infers correctness, never
suggests or ranks a decision -- this module answers "what happened,"
never "what should happen" or "was that right."

Every function here is intentionally simple relative to the sample size
this measures against: with very few real events, a sophisticated
statistic would imply more confidence than the data supports. Measures
are reported with their sample size attached, not asserted as trends.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Optional

# Substring presence only -- a disclosed heuristic proxy for "does the
# rationale text reference an evidence field," not a semantic judgment
# of whether the reference is accurate or meaningful.
_EVIDENCE_KEYWORDS = (
    "confidence", "occurrence", "tool", "heuristic", "resolved",
    "fingerprint", "flag", "provenance", "trace", "source",
)


def extract_human_review_events(trace_records) -> tuple:
    """Every real Trace record whose outputs.event is
    human_review_decision_recorded, in on-disk order. Read-only."""
    events = []
    for r in trace_records:
        outputs = r.get("outputs") or {}
        if outputs.get("event") == "human_review_decision_recorded":
            events.append(r)
    return tuple(events)


@dataclass(frozen=True)
class DecisionDistribution:
    total: int
    approve: int
    reject: int
    edit: int


def decision_distribution(events) -> DecisionDistribution:
    counts = {"approve": 0, "reject": 0, "edit": 0}
    for r in events:
        d = (r.get("outputs") or {}).get("decision")
        if d in counts:
            counts[d] += 1
    return DecisionDistribution(total=len(events), **counts)


@dataclass(frozen=True)
class RationaleStats:
    count: int
    lengths: tuple  # raw character-length per event, for full transparency at low n
    min_length: Optional[int]
    max_length: Optional[int]
    mean_length: Optional[float]
    median_length: Optional[float]
    events_referencing_evidence_keywords: int


def rationale_stats(events) -> RationaleStats:
    lengths = []
    referencing = 0
    for r in events:
        rationale = (r.get("outputs") or {}).get("rationale") or ""
        lengths.append(len(rationale))
        lowered = rationale.lower()
        if any(kw in lowered for kw in _EVIDENCE_KEYWORDS):
            referencing += 1
    if not lengths:
        return RationaleStats(0, (), None, None, None, None, 0)
    return RationaleStats(
        count=len(lengths), lengths=tuple(lengths),
        min_length=min(lengths), max_length=max(lengths),
        mean_length=statistics.fmean(lengths), median_length=statistics.median(lengths),
        events_referencing_evidence_keywords=referencing,
    )


@dataclass(frozen=True)
class ReviewFlagInteraction:
    events_with_flagged_candidate: int
    events_with_flagged_candidate_referencing_a_flag_in_rationale: int


def review_flag_interaction(events) -> ReviewFlagInteraction:
    flagged = 0
    referenced = 0
    for r in events:
        outputs = r.get("outputs") or {}
        snap = outputs.get("candidate_snapshot") or {}
        flags = snap.get("review_flags") or []
        if flags:
            flagged += 1
            rationale = (outputs.get("rationale") or "").lower()
            # substring presence of the flag's own name (e.g. "truncated"),
            # same disclosed-heuristic posture as evidence-keyword matching
            if any(flag.replace("_", " ") in rationale or flag in rationale for flag in flags):
                referenced += 1
    return ReviewFlagInteraction(flagged, referenced)


@dataclass(frozen=True)
class OptionalFieldUsage:
    total: int
    reviewer_identity_values: tuple
    department_override_used: int
    reviewer_confidence_used: int
    additional_notes_used: int


def optional_field_usage(events) -> OptionalFieldUsage:
    identities = []
    dept = 0
    conf = 0
    notes = 0
    for r in events:
        outputs = r.get("outputs") or {}
        identities.append(outputs.get("reviewer_identity"))
        if outputs.get("department_override"):
            dept += 1
        if outputs.get("reviewer_confidence") is not None:
            conf += 1
        if outputs.get("additional_notes"):
            notes += 1
    return OptionalFieldUsage(
        total=len(events), reviewer_identity_values=tuple(identities),
        department_override_used=dept, reviewer_confidence_used=conf, additional_notes_used=notes,
    )
