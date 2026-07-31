#!/usr/bin/env python3
"""
Runs Governance Observation Stabilization measurements against the real,
on-disk Trace corpus. Read-only: produces no recommendation, no
correctness judgment, no ranking -- descriptive measurement only.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execution.memory.extractor import load_trace_records
from execution.human_review_observation import (
    decision_distribution, extract_human_review_events, optional_field_usage,
    rationale_stats, review_flag_interaction,
)


def main():
    records = load_trace_records()
    events = extract_human_review_events(records)

    print(f"Trace records: {len(records)}")
    print(f"Real human_review_decision_recorded events: {len(events)}")
    print()

    dist = decision_distribution(events)
    print("=== Decision distribution ===")
    print(f"  approve={dist.approve} reject={dist.reject} edit={dist.edit} (total={dist.total})")
    print()

    rs = rationale_stats(events)
    print("=== Rationale length distribution ===")
    print(f"  n={rs.count} lengths={rs.lengths}")
    print(f"  min={rs.min_length} max={rs.max_length} mean={rs.mean_length} median={rs.median_length}")
    print(f"  events whose rationale references an evidence-related keyword: {rs.events_referencing_evidence_keywords}/{rs.count}")
    print()

    flags = review_flag_interaction(events)
    print("=== Review flag interaction ===")
    print(f"  events reviewing a flagged candidate: {flags.events_with_flagged_candidate}/{len(events)}")
    print(f"  of those, rationale referenced a flag: {flags.events_with_flagged_candidate_referencing_a_flag_in_rationale}/{flags.events_with_flagged_candidate}" if flags.events_with_flagged_candidate else "  (no flagged candidates reviewed yet)")
    print()

    opt = optional_field_usage(events)
    print("=== Optional field usage ===")
    print(f"  reviewer_identity values used: {opt.reviewer_identity_values}")
    print(f"  department_override used: {opt.department_override_used}/{opt.total}")
    print(f"  reviewer_confidence used: {opt.reviewer_confidence_used}/{opt.total}")
    print(f"  additional_notes used: {opt.additional_notes_used}/{opt.total}")


if __name__ == "__main__":
    main()
