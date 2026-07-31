#!/usr/bin/env python3
"""
Runs the Execution Metrics Layer (execution/metrics.py) against every
real Trace record on disk, via Observability, and prints a metrics
report — the Tier 4 evidence artifact, mirroring the style of
run_observability_report.py (Tier 3).

Metrics never reads Trace directly; this script performs the Trace ->
Observability step itself and hands Observability's event objects to
Metrics, preserving the same one-directional layering Metrics itself
enforces internally.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from execution.memory.extractor import load_trace_records
from execution.observability import extract_skill_events, extract_workflow_events
from execution import metrics


def _fmt(value, digits=4):
    return "n/a" if value is None else f"{value:.{digits}f}"


def main():
    records = load_trace_records()
    skill_events = extract_skill_events(records)
    workflow_events = extract_workflow_events(records)

    skill_metrics = metrics.compute_skill_metrics(skill_events)
    tool_metrics = metrics.compute_tool_metrics(skill_events)
    workflow_metrics = metrics.compute_workflow_metrics(workflow_events)
    bottlenecks = metrics.bottleneck_report(skill_events, top_n=5)

    print(f"Trace records: {len(records)}")
    print(f"Skill telemetry events: {len(skill_events)}")
    print(f"Workflow telemetry events: {len(workflow_events)}")
    print()

    print("=== Skill Metrics ===")
    for m in skill_metrics:
        print(f"  {m.skill_key}")
        print(f"    invocations={m.total_invocations} success={m.success_count} "
              f"failure={m.failure_count} not_implemented={m.not_implemented_count} "
              f"success_rate={_fmt(m.success_rate, 3)}")
        print(f"    duration_ms: avg={_fmt(m.avg_duration_ms)} median={_fmt(m.median_duration_ms)} "
              f"p95={_fmt(m.p95_duration_ms)} max={_fmt(m.max_duration_ms)}")
    print()

    print("=== Tool Metrics ===")
    for m in tool_metrics:
        print(f"  {m.tool_key}")
        print(f"    total_calls={m.total_calls} cache_hit={m.cache_hit_count} "
              f"cache_invalidated={m.cache_invalidated_count} cache_no_entry={m.cache_no_entry_count} "
              f"cache_not_applicable={m.cache_not_applicable_count} cache_unknown={m.cache_unknown_count}")
        print(f"    cache_hit_rate={_fmt(m.cache_hit_rate, 3)} live_execution_rate={_fmt(m.live_execution_rate, 3)}")
        print(f"    verified={m.verified_count} invalidated={m.invalidated_count} "
              f"verification_rate={_fmt(m.verification_rate, 3)}")
    print()

    print("=== Workflow Metrics ===")
    for m in workflow_metrics:
        print(f"  {m.workflow_key}")
        print(f"    total_runs={m.total_runs} completed={m.completed_count} "
              f"escalated={m.escalated_count} failed={m.failed_count} "
              f"success_rate={_fmt(m.success_rate, 3)}")
        print(f"    duration_ms: avg={_fmt(m.avg_duration_ms)} median={_fmt(m.median_duration_ms)} "
              f"p95={_fmt(m.p95_duration_ms)} max={_fmt(m.max_duration_ms)}")
    print()

    print("=== Bottleneck Ranking (top 5 Skills by avg duration) ===")
    for b in bottlenecks:
        print(f"  #{b.rank} {b.skill_key}: avg={b.avg_duration_ms:.4f}ms n={b.sample_count}")


if __name__ == "__main__":
    main()
