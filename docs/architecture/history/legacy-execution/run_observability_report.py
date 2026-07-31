#!/usr/bin/env python3
"""
Runs the Execution Observability Layer against every real Trace record
on disk and prints a raw telemetry summary — evidence for the Tier 3
completion report, not a metrics dashboard (that's Tier 4's job).
"""

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execution.memory.extractor import load_trace_records
from execution.observability import extract_skill_events, extract_workflow_events


def main():
    records = load_trace_records()
    skill_events = extract_skill_events(records)
    workflow_events = extract_workflow_events(records)

    print(f"Trace records: {len(records)}")
    print(f"Skill telemetry events: {len(skill_events)}")
    print(f"Workflow telemetry events: {len(workflow_events)}")
    print()

    print("=== Skill status distribution ===")
    print(dict(Counter(e.status for e in skill_events)))
    print()

    print("=== Failure class distribution (status=failure only) ===")
    print(dict(Counter(e.failure_class for e in skill_events if e.status == "failure")))
    print()

    tool_calls = [tc for e in skill_events for tc in e.tool_calls]
    print(f"=== Tool call telemetry ({len(tool_calls)} total calls) ===")
    print("cache_status distribution:", dict(Counter(tc.cache_status for tc in tool_calls)))
    print("verification_status distribution:", dict(Counter(tc.verification_status for tc in tool_calls)))
    print("resolved distribution:", dict(Counter(tc.resolved for tc in tool_calls)))
    print()

    print("=== Duration by Skill (avg ms, sample count) ===")
    by_skill = {}
    for e in skill_events:
        if e.duration_ms is not None:
            by_skill.setdefault(e.skill_key, []).append(e.duration_ms)
    for skill, durations in sorted(by_skill.items(), key=lambda kv: -sum(kv[1]) / len(kv[1])):
        avg = sum(durations) / len(durations)
        print(f"  {skill}: avg={avg:.4f}ms n={len(durations)} max={max(durations):.4f}ms")
    print()

    print("=== Workflow duration (ms) ===")
    for e in sorted(workflow_events, key=lambda w: -(w.duration_ms or 0))[:10]:
        print(f"  {e.workflow}: {e.duration_ms:.3f}ms, {e.skill_event_count} skill(s), final={e.final_status}")


if __name__ == "__main__":
    main()
