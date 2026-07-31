"""
Memory Governance Layer — Tier 3.

Answers "when can AIOS trust a Memory record, and when must it reduce or
withdraw that trust?" Purely derived, read-only: computes a governance
view over existing extract_memories() output and existing real
human_review_decision_recorded Trace events. Adds no new persistent
storage, no new Trace event type, and no mutable field on MemoryRecord —
consistent with the Memory Governance Readiness Report finding that
memory_id is not a stable identity across extraction runs (it
regenerates via uuid every time extract_memories() runs); the only
stable identity a MemoryRecord actually has is its (observation_kind,
content) dedup key, which is what every governance lookup below keys on
instead.

Two independent axes, not one collapsed linear state machine, because
that is what the real evidence supports — the directive's own example
model (OBSERVED -> VALIDATED -> TRUSTED -> DEGRADED -> INVALIDATED) was
evaluated against real data and not adopted; see the Memory Lifecycle
Design Proposal for why.

  - relevance: fresh / low_confidence / stale — unchanged, delegates to
    extractor.evaluate_relevance(), already implemented and already
    exercised against real data (100% of the current real corpus is
    "stale" under the existing 1-hour default retention window — a
    real, measured finding, not a hypothetical).
  - review_state: unreviewed / approved / rejected / edited — derived by
    matching (observation_kind, content) against real
    human_review_decision_recorded Trace events, the same cross-
    reference technique promotion.py's _derive_evidence_details already
    uses for evidence recovery.

trust_decision() combines them with exactly one override rule: a real
human `reject` always wins, regardless of freshness — a human veto is
absolute, matching Domain Model invariant 8's "never automatic" spirit.
Approval and edit do not bypass relevance: nothing in real evidence
shows a prior approval should immunize a memory against later-detected
staleness, so this deliberately does not invent that exemption.

edited_content is surfaced by preferred_content() as a value a caller
may prefer; it never mutates memory.content. The original evidence
remains exactly as extract_memories() produced it, always.

Conflict detection reuses each Tool's own registered cache_key_fn
(tool.py's CACHE_KEY_FNS) as the "same subject" key — the identical
mechanism Tier 1/2 already use to decide two calls concern the same
thing — rather than inventing a new subject-matching heuristic. Two
memories conflict if they share that key but disagree on `resolved`. No
real conflicting pair exists in the corpus today (checked directly
against all 370 real memories before writing this); detect_conflicts()
is validated against a real, disclosed, controlled scenario instead
(Experiment 5), the same pattern already accepted for the Tier 2 drift
experiment. No resolution is attempted here — every detected conflict
is returned for human review, exactly like every other unresolved
evidence question in this system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import tool as tool_mod
from .memory.extractor import MemoryRecord, evaluate_relevance

REVIEW_STATES = frozenset({"unreviewed", "approved", "rejected", "edited"})


def _human_review_events(trace_records):
    events = []
    for r in trace_records:
        outputs = r.get("outputs") or {}
        if outputs.get("event") == "human_review_decision_recorded":
            events.append(r)
    return events


def _matching_review_events(memory: MemoryRecord, review_events):
    matches = []
    for r in review_events:
        snap = (r.get("outputs") or {}).get("candidate_snapshot") or {}
        if snap.get("observation_kind") == memory.observation_kind and snap.get("content") == memory.content:
            matches.append(r)
    return matches


@dataclass(frozen=True)
class ReviewState:
    state: str  # one of REVIEW_STATES
    decision_trace_ids: tuple  # every matching real decision event, oldest first by decision_timestamp
    edited_content: Optional[str]  # from the latest edit decision, if any; None otherwise


def review_state(memory: MemoryRecord, trace_records) -> ReviewState:
    """Derives review_state purely from real human_review_decision_recorded
    events whose candidate_snapshot exactly matches this memory's
    (observation_kind, content). No inference, no guessing: a memory
    with no matching real decision is "unreviewed", period.

    Precedence when multiple real decisions exist for the same content
    (append-only Trace permits this — see the accidental-resubmission
    case this session already encountered): any real `reject` makes the
    state "rejected", full stop — a rejection is never quietly
    outvoted by an earlier or later approval. Otherwise the latest
    `edit` (by decision_timestamp) wins over `approve`, since an edit is
    a more specific, more recent human judgment about the content
    itself."""
    events = _matching_review_events(memory, _human_review_events(trace_records))
    if not events:
        return ReviewState(state="unreviewed", decision_trace_ids=(), edited_content=None)

    events_sorted = sorted(events, key=lambda r: (r.get("outputs") or {}).get("decision_timestamp") or 0)
    trace_ids = tuple(r.get("trace_id") for r in events_sorted)
    decisions = [(r.get("outputs") or {}).get("decision") for r in events_sorted]

    if "reject" in decisions:
        return ReviewState(state="rejected", decision_trace_ids=trace_ids, edited_content=None)

    edit_events = [r for r in events_sorted if (r.get("outputs") or {}).get("decision") == "edit"]
    if edit_events:
        latest_edit = edit_events[-1]
        return ReviewState(
            state="edited", decision_trace_ids=trace_ids,
            edited_content=(latest_edit.get("outputs") or {}).get("edited_content"),
        )

    if "approve" in decisions:
        return ReviewState(state="approved", decision_trace_ids=trace_ids, edited_content=None)

    return ReviewState(state="unreviewed", decision_trace_ids=trace_ids, edited_content=None)


def trust_decision(memory: MemoryRecord, trace_records, now=None) -> str:
    """"do_not_use" if a real human ever rejected this exact content —
    absolute, regardless of freshness. Otherwise defers entirely to
    evaluate_relevance() ("fresh" / "low_confidence" / "stale"):
    approval and edit are not freshness exemptions."""
    if review_state(memory, trace_records).state == "rejected":
        return "do_not_use"
    return evaluate_relevance(memory, now=now)


def preferred_content(memory: MemoryRecord, trace_records) -> str:
    """The text a caller should prefer: the human-edited replacement if
    one is on record, otherwise the original. Never mutates
    memory.content — the original evidence is always still there."""
    rs = review_state(memory, trace_records)
    if rs.state == "edited" and rs.edited_content:
        return rs.edited_content
    return memory.content


@dataclass(frozen=True)
class MemoryConflict:
    subject_key: tuple
    memory_a: MemoryRecord
    memory_b: MemoryRecord
    resolved_a: Optional[bool]
    resolved_b: Optional[bool]


def _evidence_by_trace(trace_records):
    by_trace = {}
    for r in trace_records:
        evs = (r.get("outputs") or {}).get("evidence") or []
        if evs:
            by_trace[r.get("trace_id")] = evs
    return by_trace


def _subject_key_and_resolved(memory: MemoryRecord, evidence_by_trace):
    """Reuses each Tool's own registered cache_key_fn (tool.py) as the
    "same subject" identifier — exactly what Tier 1/2 already use to
    decide two calls concern the same thing, so this introduces no new
    subject-matching heuristic. Returns (subject_key, resolved), or
    (None, None) if no tool_key/cache_key_fn is recoverable for this
    memory (e.g. heuristic-sourced observations, which have no
    registered Tool at all)."""
    for trace_id in memory.source_trace_ids:
        for ev in evidence_by_trace.get(trace_id, ()):
            if ev.get("kind") != memory.observation_kind or ev.get("detail") != memory.content:
                continue
            tool_key = ev.get("tool_key")
            if tool_key is None:
                continue
            registration = tool_mod._registry().get(tool_key)
            if registration is None or registration.cache_key_fn is None:
                continue
            params = ev.get("parameters") or {}
            request = tool_mod.ToolRequest(tool_canonical_key=tool_key, action="", parameters=params)
            return (registration.cache_key_fn(request), ev.get("resolved"))
    return (None, None)


def detect_conflicts(memories, trace_records) -> tuple:
    """Two memories conflict if they resolve to the same Tool-derived
    subject key but disagree on `resolved`. No auto-resolution and no
    priority rule: every detected conflict is returned as-is, for human
    review, the same way every other unresolved evidence question in
    this system is handled — this function decides nothing."""
    evidence_by_trace = _evidence_by_trace(trace_records)
    by_subject = {}
    for m in memories:
        key, resolved = _subject_key_and_resolved(m, evidence_by_trace)
        if key is None:
            continue
        by_subject.setdefault(key, []).append((m, resolved))

    conflicts = []
    for key, entries in by_subject.items():
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                m_a, r_a = entries[i]
                m_b, r_b = entries[j]
                if r_a != r_b:
                    conflicts.append(MemoryConflict(
                        subject_key=key, memory_a=m_a, memory_b=m_b, resolved_a=r_a, resolved_b=r_b,
                    ))
    return tuple(conflicts)
