"""
Memory lookup experiment.

Tests whether existing provisional Memory records provide useful
context when a genuinely new execution occurs — using a real new Trace
produced by actually re-running the harness, not a synthetic replay.

For each evidence entry a new Trace record produces, this module
classifies it against a memory index built from everything observed
*before* that new Trace:

  - **"reused"**   — an exact (kind, content) match exists and is not
    expired: the new run encountered exactly what a prior run already
    recorded. The new Tool/Skill invocation that produced it was, in
    principle, redundant with something already known.
  - **"outdated"** — an exact (kind, content) match exists, but
    extractor.is_expired() says it's stale (measured from the memory's
    own last_observed_at, never from extraction time): the new run's
    evidence would need re-verification rather than blind reuse.
  - **"ignored"**  — no exact match. Two real sub-cases are
    distinguished rather than silently merged: genuinely novel content,
    versus a same-kind-different-content near-miss (an existing memory
    concerns the same class of check but a different specific fact) —
    the latter is direct evidence of this experiment's exact-match
    matching being imprecise, not proof that nothing relevant existed.
"""

from dataclasses import dataclass

from .extractor import is_expired


@dataclass(frozen=True)
class LookupResult:
    kind: str
    content: str
    classification: str  # "reused" | "outdated" | "ignored"
    matched_memory_id: str
    near_miss_kind_match: bool


def build_index(memories):
    return {(m.observation_kind, m.content): m for m in memories}


def lookup_evidence(new_trace_record, memory_index, now=None):
    evidence = (new_trace_record.get("outputs") or {}).get("evidence") or []
    kinds_present = {m.observation_kind for m in memory_index.values()}
    results = []
    for ev in evidence:
        kind = ev.get("kind")
        content = ev.get("detail")
        if not kind or not content:
            continue
        memory = memory_index.get((kind, content))
        if memory is None:
            results.append(LookupResult(
                kind=kind, content=content, classification="ignored",
                matched_memory_id=None, near_miss_kind_match=kind in kinds_present,
            ))
            continue
        if is_expired(memory, now=now):
            results.append(LookupResult(
                kind=kind, content=content, classification="outdated",
                matched_memory_id=memory.memory_id, near_miss_kind_match=False,
            ))
        else:
            results.append(LookupResult(
                kind=kind, content=content, classification="reused",
                matched_memory_id=memory.memory_id, near_miss_kind_match=False,
            ))
    return results
