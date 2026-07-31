"""
Memory extraction quality evaluation — four experiments, run against the
real MemoryRecords extractor.py produces. None of these define a
governance concept; all four are diagnostic functions over data already
in hand.

1. Confidence calibration — checks whether the existing heuristic
   confidence formula (extractor.py) actually correlates with
   occurrence_count/instance-diversity in the real data, and reports the
   correlation honestly rather than assuming the formula is meaningful
   just because it's monotonic by construction.
2. Observation diversity — how much of the memory store is actually
   distinct information versus repeated instances of a small number of
   underlying facts.
3. Recency weighting — an alternative, time-decayed confidence score,
   compared side by side against the raw heuristic confidence.
4. Duplicate-pattern evaluation — clusters memories by a normalized
   *template* (section numbers and filenames replaced with
   placeholders), separate from extractor.py's exact-content dedup, to
   measure how many truly distinct patterns exist beneath the exact
   distinct values.

Memory Expansion Validation Phase additions (5-10), run against a
corpus now spanning 6 Skill categories and 3 Tool categories rather
than the original single Skill/Tool pair:

5. Retrieval accuracy — of everything a new execution's evidence
   produces, what fraction resolves against the memory index at all
   (as "reused" or "outdated"), versus "ignored" (no matching record
   exists). A recall-style metric over lookup.py's real classifications.
6. Stale memory detection — what fraction of the current memory store
   is_expired() right now, given real elapsed time and each memory's
   own retention window.
7. Cross-skill diversity — breaks distinct evidence kinds down by which
   Skill's handler produced them, the direct numeric answer to whether
   Memory generalizes beyond the original governance-cross-reference
   scenario.
8. Memory reuse rate — from a real Run A/B consumption comparison,
   generalized across whichever Skills/Tools are included: what
   fraction of live Tool calls Run B actually served from Memory.
"""

import math
import re
import time
from dataclasses import dataclass

TEMPLATE_SECTION_RE = re.compile(r"§\d+")
TEMPLATE_FILENAME_RE = re.compile(r"[\w\-]+\.md")


def confidence_calibration(memories):
    """Compares each memory's assigned confidence against its raw
    occurrence_count, reporting Pearson correlation. With this session's
    small corpus (typically 3-4 memories) this is explicitly too small a
    sample for a real statistical claim — reported as a descriptive
    number, not evidence of a validated model."""
    if len(memories) < 2:
        return {"n": len(memories), "correlation": None, "note": "fewer than 2 memories; correlation undefined"}

    xs = [m.occurrence_count for m in memories]
    ys = [m.confidence for m in memories]
    n = len(xs)
    mean_x, mean_y = sum(xs) / n, sum(ys) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    var_x = sum((x - mean_x) ** 2 for x in xs)
    var_y = sum((y - mean_y) ** 2 for y in ys)
    if var_x == 0 or var_y == 0:
        correlation = None
        note = "zero variance in occurrence_count or confidence (all memories identical on one axis) — correlation undefined, not zero"
    else:
        correlation = cov / math.sqrt(var_x * var_y)
        note = "descriptive only; n is too small for a statistical claim" if n < 10 else "n sufficient for a directional read"
    return {"n": n, "correlation": correlation, "note": note}


def observation_diversity(memories):
    """Distinct-kind ratio and distinct-referenced-file count, as a
    proxy for how much of the memory store is genuinely different
    information versus repeated instances of few underlying facts."""
    if not memories:
        return {"distinct_kinds": 0, "kind_diversity_ratio": None, "distinct_files_referenced": 0}
    kinds = {m.observation_kind for m in memories}
    files = set()
    for m in memories:
        files.update(TEMPLATE_FILENAME_RE.findall(m.content))
    return {
        "total_memories": len(memories),
        "distinct_kinds": len(kinds),
        "kind_diversity_ratio": round(len(kinds) / len(memories), 2),
        "distinct_files_referenced": len(files),
        "files": sorted(files),
    }


@dataclass(frozen=True)
class RecencyWeightedScore:
    memory_id: str
    raw_confidence: float
    recency_weighted_confidence: float
    age_seconds: float


def recency_weighting(memories, now=None):
    """An alternative confidence score that decays with age since
    last_observed_at, using an exponential half-life equal to
    retention_seconds — a real, different scoring approach compared
    side-by-side against the raw heuristic, not a replacement for it."""
    now = now if now is not None else time.time()
    results = []
    for m in memories:
        reference = m.last_observed_at if m.last_observed_at is not None else m.created_at
        age = now - reference
        half_life = m.retention_seconds or 1.0
        decay = 0.5 ** (age / half_life)
        results.append(RecencyWeightedScore(
            memory_id=m.memory_id,
            raw_confidence=m.confidence,
            recency_weighted_confidence=round(m.confidence * decay, 4),
            age_seconds=round(age, 2),
        ))
    return results


def _template(kind, content):
    normalized = TEMPLATE_SECTION_RE.sub("§N", content)
    normalized = TEMPLATE_FILENAME_RE.sub("<FILE>", normalized)
    return (kind, normalized)


def duplicate_pattern_evaluation(memories):
    """Clusters memories by a normalized template (section numbers and
    filenames replaced with placeholders) — a second, coarser dedup
    layer beneath extractor.py's exact-content dedup, showing how many
    truly distinct *patterns* of observation exist versus how many
    distinct exact values extractor.py already reports."""
    clusters = {}
    for m in memories:
        key = _template(m.observation_kind, m.content)
        clusters.setdefault(key, []).append(m)
    return {
        "exact_distinct_memories": len(memories),
        "template_distinct_patterns": len(clusters),
        "clusters": [
            {"template": f"{k[0]}: {k[1]}", "member_count": len(v), "members": [m.memory_id for m in v]}
            for k, v in clusters.items()
        ],
    }


def retrieval_accuracy(lookup_results):
    """Of every evidence entry a lookup was attempted for, what
    fraction resolved against the memory index at all (reused or
    outdated) versus found nothing (ignored). Methodology: a direct
    tally over real lookup.LookupResult classifications — not a
    precision/recall model against ground truth, since "ground truth"
    for whether something *should* have a memory match isn't itself
    defined anywhere. Limitation: this measures index coverage, not
    whether a "reused" classification was actually correct to reuse —
    that's a separate question the consumption experiment's accuracy
    check answers instead."""
    if not lookup_results:
        return {"n": 0, "resolved_rate": None, "reused": 0, "outdated": 0, "ignored": 0}
    counts = {"reused": 0, "outdated": 0, "ignored": 0}
    for r in lookup_results:
        counts[r.classification] = counts.get(r.classification, 0) + 1
    resolved = counts["reused"] + counts["outdated"]
    return {"n": len(lookup_results), "resolved_rate": round(resolved / len(lookup_results), 3), **counts}


def stale_memory_detection(memories, now=None):
    """What fraction of the current memory store is_expired() right
    now. Methodology: direct application of extractor.is_expired() to
    every memory using each one's own retention_seconds and
    last_observed_at — the same function actually used elsewhere in
    this harness, not a re-derived approximation. Limitation: "stale"
    here means only "past its retention window," a purely time-based
    signal; it says nothing about whether the underlying fact actually
    changed (that's what the Drift Experiment tests directly)."""
    from .extractor import is_expired
    if not memories:
        return {"n": 0, "stale_count": 0, "stale_rate": None}
    stale = [m for m in memories if is_expired(m, now=now)]
    return {"n": len(memories), "stale_count": len(stale), "stale_rate": round(len(stale) / len(memories), 3)}


def cross_skill_diversity(trace_records):
    """Breaks distinct evidence kinds down by which Skill produced them
    — the direct, numeric answer to whether Memory generalizes beyond
    the original governance-cross-reference-scan-only scenario.
    Methodology: for each Trace record with evidence, associate every
    evidence kind found with the record's own skills_used. Limitation:
    a record with more than one skill in skills_used (never occurs in
    this harness's current orchestrator, which writes one Trace record
    per Skill) would have its evidence misattributed across all of
    them; noted for completeness even though not currently reachable."""
    by_skill = {}
    for record in trace_records:
        skills = record.get("skills_used") or []
        evidence = (record.get("outputs") or {}).get("evidence") or []
        kinds = {ev.get("kind") for ev in evidence if ev.get("kind")}
        for s in skills:
            by_skill.setdefault(s, set()).update(kinds)
    return {
        "distinct_skills_with_evidence": len(by_skill),
        "kinds_per_skill": {s: sorted(k) for s, k in by_skill.items()},
        "total_distinct_kinds": len({k for kinds in by_skill.values() for k in kinds}),
    }
