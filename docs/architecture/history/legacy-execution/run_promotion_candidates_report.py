#!/usr/bin/env python3
"""
Runs Promotion Candidate Selection against the real, on-disk Memory/Trace
corpus and prints a validation report against exactly the acceptance
criteria set by the Promotion Candidate Selection Validation Report v1.0
and this implementation phase's directive. Read-only: produces no
Knowledge, approves nothing, writes nothing anywhere.
"""

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execution.memory.extractor import extract_memories, load_trace_records
from execution.promotion import select_candidates

KNOWN_ARTIFACTS = {"resolved", "## Domain Model Impact"}

CALIBRATION = {
    "A": "§6 not found anywhere in governance-artifact-integrity.md",
    "B": "paragraph mentioning 'Agent Definition' reads more similar to 'Agent Instance' (0.22 vs 0.19)",
    "C": "## Domain Model Impact",
}


def main():
    records = load_trace_records()
    memories = extract_memories(records)
    candidates = select_candidates(memories, records)

    print(f"Trace records: {len(records)}")
    print(f"Memory records: {len(memories)}")
    print(f"Eligible candidates: {len(candidates)}")
    print()

    print("=== 1. Candidate count ===")
    print(f"  Input Memory records: {len(memories)}")
    print(f"  Output eligible candidates: {len(candidates)}")
    print()

    print("=== 2. Filtering — known artifacts must remain excluded ===")
    candidate_contents = {c.content for c in candidates}
    for artifact in KNOWN_ARTIFACTS:
        excluded = artifact not in candidate_contents
        print(f"  {artifact!r}: excluded={excluded}")
    print()

    print("=== 3. Provenance reconstruction ===")
    with_trace_ids = sum(1 for c in candidates if c.provenance.trace_ids)
    with_memory_id = sum(1 for c in candidates if c.provenance.memory_id)
    print(f"  candidates with trace_ids: {with_trace_ids}/{len(candidates)}")
    print(f"  candidates with memory_id: {with_memory_id}/{len(candidates)}")
    dept_unavailable = sum(1 for c in candidates if c.provenance.department_status == "unavailable")
    print(f"  department_status == 'unavailable': {dept_unavailable}/{len(candidates)}")
    print()

    print("=== 4. Source-type resolution ===")
    source_dist = Counter(c.evidence.source_type for c in candidates)
    print(f"  distribution: {dict(source_dist)}")
    unknown_count = source_dist.get("unknown", 0)
    print(f"  resolved (non-'unknown'): {len(candidates) - unknown_count}/{len(candidates)}")
    print()

    print("=== 5. Calibration (Q2 candidates A/B/C) ===")
    for label, content in CALIBRATION.items():
        match = next((c for c in candidates if c.content == content), None)
        if label == "C":
            print(f"  {label}: excluded={match is None} (expected: excluded)")
        else:
            print(f"  {label}: eligible={match is not None}, rank={candidates.index(match) if match else None} (expected: eligible)")

    staleness_candidates = [c for c in candidates if c.observation_kind == "staleness_flag"]
    for c in staleness_candidates:
        print(f"  D-class (staleness_flag): flags={c.review_flags} (expected: includes 'truncated', 'heuristic_source')")
    uncited_candidates = [c for c in candidates if c.observation_kind == "uncited_restatement_flag"]
    for c in uncited_candidates:
        print(f"  E-class (uncited_restatement_flag): flags={c.review_flags} (expected: includes 'verbatim_quote', 'heuristic_source')")
    print()

    print("=== Review flag distribution across all eligible candidates ===")
    flag_counts = Counter(flag for c in candidates for flag in c.review_flags)
    print(f"  {dict(flag_counts)}")
    print()

    print("=== Ranking sample (top 5, bottom 5) ===")
    for c in candidates[:5]:
        print(f"  TOP    src={c.evidence.source_type} conf={c.evidence.confidence} occ={c.evidence.occurrence_count} content={c.content[:60]!r}")
    for c in candidates[-5:]:
        print(f"  BOTTOM src={c.evidence.source_type} conf={c.evidence.confidence} occ={c.evidence.occurrence_count} flags={c.review_flags} content={c.content[:60]!r}")
    print()

    print("=== Example Human Review Candidate Package (top candidate) ===")
    top = candidates[0]
    print(f"  id={top.id}")
    print(f"  content={top.content!r}")
    print(f"  observation_kind={top.observation_kind}")
    print(f"  provenance={top.provenance}")
    print(f"  evidence={top.evidence}")
    print(f"  review_flags={top.review_flags}")


if __name__ == "__main__":
    main()
