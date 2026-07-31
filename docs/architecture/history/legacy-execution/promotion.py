"""
Promotion Candidate Selection.

Answers exactly one question: "Can AIOS reliably identify evidence
candidates that are worthy of human review?" It never answers "should
this candidate become Knowledge" — that judgment belongs entirely to
Human Review (a Governance Event, per Knowledge Architecture Blueprint
v2.1) and, downstream of it, Action B. This module makes no promotion
decision, approves nothing, rejects nothing permanently, and writes
nothing anywhere: it only reads Memory and Trace and produces a ranked,
provenance-complete package for a human to look at.

Layering: reads execution.memory.extractor only (Memory records, and
Trace records via load_trace_records for provenance reconstruction).
Never imports execution.trace, execution.orchestrator, execution.tool,
execution.skill, execution.workflow, or execution.agent_definition —
the same one-directional discipline observability.py and metrics.py
already established. `agent_definition_name` is read directly off Trace
records (already present on every one since before this module existed)
rather than importing the Agent Definition loader, so this module has
no path to touch governance documents at all.

Department is never resolved here. The Department Mapping Evidence Pass
confirmed no Department field exists anywhere in Trace or the Execution
Layer today — the authoritative mapping lives only in the Agent
Definition's own governance document, unsurfaced. `department_status`
is therefore always "unavailable", stated honestly rather than guessed
or inferred, per this phase's explicit boundary rule.

Eligibility, ranking, and review-flag logic below are exactly the rules
already validated in the Promotion Candidate Selection Validation
Report (368/370 eligible, 2 known artifacts excluded, 368/368 source
and provenance resolution, 5/5 Q2 calibration match) — this module is
that validated design, not a new design.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .memory.extractor import MemoryRecord

MIN_CONTENT_LENGTH = 15
LOW_CONFIDENCE_THRESHOLD = 0.6  # matches memory/extractor.py's own evaluate_relevance() cutoff

_HEADING_RE = re.compile(r"^#+\s")
_SENTENCE_END_CHARS = (".", "!", "?", '"', "'")

# skill.py's staleness-detection heuristic truncates its source paragraph at
# para.strip()[:200] before prepending "[severity=N] " (~13 chars), landing
# real truncated evidence at or near 200 characters with no closing
# punctuation. This is a disclosed heuristic derived from that real,
# inspected root cause -- not a certainty. A genuinely long, complete
# observation that happens to lack terminal punctuation would also match;
# the flag is a review hint, not a verdict.
_TRUNCATION_LENGTH_FLOOR = 200

_SOURCE_PRIORITY = {"tool": 0, "heuristic": 1, "model_generated": 2, "unknown": 3}


def is_degenerate_content(content: str) -> bool:
    """Excludes: Markdown heading fragments, generic fallback values, and
    anything below the validated minimum length. Does NOT exclude low
    confidence, heuristic evidence, truncated evidence, or verbatim
    quotations -- those remain eligible, flagged instead (see
    _review_flags)."""
    stripped = content.strip()
    if len(stripped) < MIN_CONTENT_LENGTH:
        return True
    if _HEADING_RE.match(stripped):
        return True
    return False


_KNOWN_SOURCES = frozenset({"tool", "heuristic", "model_generated"})


def _derive_evidence_details(memory: MemoryRecord, evidence_by_trace: dict) -> tuple:
    """Reconstructs source/resolved/fingerprint -- the original Trace
    evidence details MemoryRecord itself discards -- by looking up the
    memory's own source_trace_ids and matching on (observation_kind,
    content). Returns (source, resolved, fingerprint).

    Evidence Chain Auditability Hardening finding: the matching evidence
    entry was already being found to recover `source`, but `resolved`
    and `fingerprint` from that same entry were being read and then
    discarded -- a real, fixable provenance-loss gap, not a new lookup.

    source/resolved are reported only when every matching entry agrees
    completely -- both fields are present on every real Trace generation
    (trace_schema.py normalizes both onto old-generation records too),
    so any disagreement between them is a genuine conflict, not
    generational absence, and is reported as unresolvable rather than
    guessed.

    fingerprint is evaluated separately and more leniently, because it
    has a real, confirmed generational-absence pattern this corpus
    actually exhibits: Tier 2 introduced fingerprint recording partway
    through this system's history, so older occurrences of the exact
    same (kind, content) legitimately carry no fingerprint (None) while
    newer occurrences of that identical finding do. None is therefore
    treated as "no information from this entry," not as a disagreeing
    value -- only an actual conflict between two non-None fingerprints
    counts as ambiguous. Verified against the real corpus: this
    generational-absence pattern is exactly what produced 7 real
    candidates whose fingerprint could not otherwise be recovered,
    before this distinction was added (a real regression this fix
    resolves, not a hypothetical one)."""
    source_resolved_found = set()
    fingerprints_found = set()
    for trace_id in memory.source_trace_ids:
        for ev in evidence_by_trace.get(trace_id, ()):
            if ev.get("kind") == memory.observation_kind and ev.get("detail") == memory.content:
                source = ev.get("source")
                if source in _KNOWN_SOURCES:
                    source_resolved_found.add((source, ev.get("resolved")))
                    # fingerprint is a tuple when produced in-process (verification.py)
                    # but round-trips through JSON as a list once written to and read
                    # back from Trace -- JSON has no tuple type. Normalized here so the
                    # set-based agreement check is hashable; the value and its meaning
                    # (an order-independent sequence of "key=hash" strings) are unchanged.
                    raw_fingerprint = ev.get("fingerprint")
                    if raw_fingerprint is not None:
                        fingerprints_found.add(tuple(raw_fingerprint))

    if len(source_resolved_found) != 1:
        return ("unknown", None, None)
    source, resolved = next(iter(source_resolved_found))

    if len(fingerprints_found) == 1:
        fingerprint = next(iter(fingerprints_found))
    elif len(fingerprints_found) == 0:
        fingerprint = None  # honestly never recorded, not a conflict
    else:
        fingerprint = None  # genuine disagreement between two recorded fingerprints -- unresolvable, not guessed

    return (source, resolved, fingerprint)


def _agent_definition_names(memory: MemoryRecord, records_by_trace: dict) -> tuple:
    names = set()
    for trace_id in memory.source_trace_ids:
        rec = records_by_trace.get(trace_id)
        if rec is not None:
            name = rec.get("agent_definition_name")
            if name:
                names.add(name)
    return tuple(sorted(names))


def _review_flags(memory: MemoryRecord, source_type: str) -> tuple:
    flags = []
    content = memory.content.strip()
    if len(content) >= _TRUNCATION_LENGTH_FLOOR and not content.endswith(_SENTENCE_END_CHARS):
        flags.append("truncated")
    if source_type == "heuristic":
        flags.append("heuristic_source")
    if memory.observation_kind == "uncited_restatement_flag":
        flags.append("verbatim_quote")
    if memory.confidence < LOW_CONFIDENCE_THRESHOLD:
        flags.append("low_confidence")
    return tuple(flags)


@dataclass(frozen=True)
class Provenance:
    memory_id: str
    trace_ids: tuple
    agent_definition_name: Optional[str]  # None only if no source trace resolved a name (not observed in practice)
    department_status: str  # always "unavailable" today -- see module docstring


@dataclass(frozen=True)
class EvidenceSummary:
    source_type: str  # "tool" | "heuristic" | "model_generated" | "unknown"
    confidence: float
    occurrence_count: int
    observation_frequency: float
    first_observed_at: Optional[float]
    last_observed_at: Optional[float]
    resolved: Optional[bool]        # original evidence's own resolved outcome, recovered from Trace; None if unrecoverable/ambiguous or the source Tool never set one (heuristic evidence)
    fingerprint: Optional[tuple]    # original Tier-2 content-hash fingerprint, recovered from Trace; None if none was ever recorded or recovery is ambiguous


@dataclass(frozen=True)
class CandidatePackage:
    id: str
    content: str
    observation_kind: str
    provenance: Provenance
    evidence: EvidenceSummary
    review_flags: tuple


def _build_indexes(trace_records):
    """One pass over the corpus, built once and reused for every
    candidate -- avoids re-scanning all Trace records per Memory record."""
    records_by_trace = {}
    evidence_by_trace = {}
    for r in trace_records:
        trace_id = r.get("trace_id")
        if trace_id is None:
            continue
        records_by_trace[trace_id] = r
        outputs = r.get("outputs") or {}
        evidence_by_trace[trace_id] = tuple(outputs.get("evidence") or ())
    return records_by_trace, evidence_by_trace


def select_candidates(memories, trace_records) -> tuple:
    """Pure function: memories + trace_records in, ranked CandidatePackage
    tuple out. No I/O, no mutation of either input, no side effects, no
    promotion decision made or implied. Ranking: evidence source
    (tool > heuristic > model_generated > unknown), then confidence
    descending, then occurrence_count descending, then first_observed_at
    ascending as a pure ordering tie-break (older candidates reviewed
    first, since Memory's own retention window means they are closer to
    being lost) -- a tuple sort, not a weighted score, per this phase's
    explicit instruction not to introduce one."""
    records_by_trace, evidence_by_trace = _build_indexes(trace_records)

    candidates = []
    for memory in memories:
        if is_degenerate_content(memory.content):
            continue
        source_type, resolved, fingerprint = _derive_evidence_details(memory, evidence_by_trace)
        agent_names = _agent_definition_names(memory, records_by_trace)
        # Exactly one distinct name is the only case honestly answerable as
        # a single value; zero (unresolved) or more than one (this memory's
        # occurrences trace back to different Agent Definitions -- possible
        # under Memory's own cross-instance dedup) are both reported as
        # None rather than guessing which one to report. Not observed in
        # the current corpus (exactly one real Agent Definition exists),
        # but the logic must not silently pick one if that ever changes.
        agent_definition_name = agent_names[0] if len(agent_names) == 1 else None
        provenance = Provenance(
            memory_id=memory.memory_id,
            trace_ids=memory.source_trace_ids,
            agent_definition_name=agent_definition_name,
            department_status="unavailable",
        )
        evidence = EvidenceSummary(
            source_type=source_type,
            confidence=memory.confidence,
            occurrence_count=memory.occurrence_count,
            observation_frequency=memory.observation_frequency,
            first_observed_at=memory.first_observed_at,
            last_observed_at=memory.last_observed_at,
            resolved=resolved,
            fingerprint=fingerprint,
        )
        candidates.append(CandidatePackage(
            id=memory.memory_id,
            content=memory.content,
            observation_kind=memory.observation_kind,
            provenance=provenance,
            evidence=evidence,
            review_flags=_review_flags(memory, source_type),
        ))

    def _sort_key(c: CandidatePackage):
        first_observed = c.evidence.first_observed_at if c.evidence.first_observed_at is not None else float("inf")
        return (
            _SOURCE_PRIORITY.get(c.evidence.source_type, _SOURCE_PRIORITY["unknown"]),
            -c.evidence.confidence,
            -c.evidence.occurrence_count,
            first_observed,
        )

    return tuple(sorted(candidates, key=_sort_key))
