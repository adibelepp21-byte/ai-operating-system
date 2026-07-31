#!/usr/bin/env python3
"""
Execution baseline capture — Tier 1 Universal Tool Contract.

Runs a fixed, representative set of (workflow, target_document) pairs
covering all 3 real Tools and 4 real Tool-invoking Skills, then captures
Tool invocation flow, Trace output, Evidence output, Memory extraction
output, and cache behavior into one JSON snapshot. Re-run after each
migration stage and diffed against the prior snapshot for regression
comparison — never trusted from memory or assumption.

Fixed scenario set (chosen for coverage, not exhaustiveness):
  1. workflow.pre-ratification-validation, default target
     -> exercises cross-reference-link-validator-interface
        (citation-discipline-verification) and authority-boundary-check.
  2. workflow.post-amendment-consistency-sweep, default target
     -> exercises document-structure-parser-interface
        (section-numbering-consistency-check).
  3. workflow.terminology-audit, ADR-0007.md
     -> exercises text-similarity-comparison-interface via both
        terminology-consistency-scan and duplicate-content-detection.
"""

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execution import orchestrator
from execution.memory.consumption import build_input_keyed_cache, run_comparison
from execution.memory.extractor import extract_memories

SCENARIOS = [
    {"workflow_key": "workflow.pre-ratification-validation", "target_document": None},
    {"workflow_key": "workflow.post-amendment-consistency-sweep", "target_document": None},
    {"workflow_key": "workflow.terminology-audit", "target_document": "docs/architecture/adr/decisions/ADR-0007.md"},
]


def _evidence_summary(skill_reports):
    return [
        {
            "skill": sr["skill"],
            "status": sr["status"],
            "failure_class": sr.get("failure_class"),
            "evidence_count": sr.get("evidence_count"),
        }
        for sr in skill_reports
    ]


def capture():
    snapshot = {"captured_at": time.time(), "scenarios": [], "consumption": {}}

    for scenario in SCENARIOS:
        result = orchestrator.run(**scenario)
        snapshot["scenarios"].append({
            "scenario": scenario,
            "workflow_completion_state": result["workflow_completion_state"],
            "skill_reports": _evidence_summary(result["skill_reports"]),
            "trace_file": result["trace_file"],
        })

    # Cache behavior: same input-keyed cache mechanism used throughout this
    # session's Memory Expansion Validation Phase, run against the current
    # on-disk trace corpus (includes what this capture just produced).
    from execution.memory.extractor import load_trace_records
    all_records = load_trace_records()
    cache = build_input_keyed_cache(all_records)
    snapshot["consumption"]["cache_entry_count"] = len(cache)
    snapshot["consumption"]["cache_keys"] = [list(k) for k in cache.keys()]

    comparison = run_comparison(orchestrator, cache, workflow_key="workflow.pre-ratification-validation")
    a, b = comparison["run_a"], comparison["run_b"]
    snapshot["consumption"]["run_a_real_calls"] = len(a["call_log"])
    snapshot["consumption"]["run_b_real_calls"] = sum(1 for c in b["call_log"] if c.real_call)
    snapshot["consumption"]["run_b_served_calls"] = sum(1 for c in b["call_log"] if not c.real_call)

    memories = extract_memories(load_trace_records())
    snapshot["memory"] = {
        "total_trace_records": len(load_trace_records()),
        "total_memories": len(memories),
        "distinct_kinds": sorted({m.observation_kind for m in memories}),
    }

    return snapshot


def main(out_path):
    snapshot = capture()
    Path(out_path).write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
    print(f"Baseline written to {out_path}")
    print(json.dumps(snapshot, indent=2, default=str))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent / "baseline" / "snapshot.json")
    main(out)
