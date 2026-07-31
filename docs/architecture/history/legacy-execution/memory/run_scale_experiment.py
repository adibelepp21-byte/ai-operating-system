#!/usr/bin/env python3
"""
Memory Expansion Validation Phase — evidence volume expansion.

Runs every real Workflow whose Skills now have handlers (including the
four implemented this phase: Staleness Detection, Duplicate Content
Detection, Section Numbering Consistency Check, Terminology Consistency
Scan) against several distinct real target documents, to generate real
Trace volume across a genuinely wider set of Skill/Tool categories than
any prior phase exercised. Skills without a handler still execute (as
"not_implemented") — real, honest evidence, not hidden.
"""

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import orchestrator

WORKFLOWS = [
    "workflow.pre-ratification-validation",
    "workflow.governance-synchronization-review",
    "workflow.post-amendment-consistency-sweep",
    "workflow.terminology-audit",
]

TARGET_DOCUMENTS = [
    None,  # default: the Agent Definition itself
    "docs/architecture/organization/execution-catalog/skill/staleness-detection.md",
    "docs/architecture/adr/decisions/ADR-0007.md",
]


def main():
    skill_categories = set()
    tool_categories = set()
    run_count = 0

    for target in TARGET_DOCUMENTS:
        for wf_key in WORKFLOWS:
            result = orchestrator.run(target_document=target, workflow_key=wf_key)
            run_count += 1
            label = target or "(Agent Definition, default)"
            print(f"[{run_count}] workflow={wf_key} target={label} -> {result['workflow_completion_state']}")
            for sr in result["skill_reports"]:
                skill_categories.add(sr["skill"])
                print(f"    {sr['skill']}: {sr['status']} (evidence_count={sr.get('evidence_count')})")

    print(f"\nTotal runs: {run_count}")
    print(f"Distinct Skill categories exercised (including not_implemented): {len(skill_categories)}")
    print(f"  {sorted(skill_categories)}")


if __name__ == "__main__":
    main()
