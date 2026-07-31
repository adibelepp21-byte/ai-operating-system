#!/usr/bin/env python3
"""
Memory consumption experiment: builds an input-keyed cache from every
real Trace record on disk, then runs Run A (normal execution) and
Run B (memory-aware execution) against the identical target and
workflow, and reports the real difference.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import orchestrator
from execution.memory.consumption import build_input_keyed_cache, run_comparison
from execution.memory.extractor import load_trace_records


def main():
    prior_records = load_trace_records()
    cache = build_input_keyed_cache(prior_records)
    print(f"Input-keyed cache built from {len(prior_records)} prior Trace records -> {len(cache)} distinct (reference_target, expected_reference) entries\n")
    for k, v in cache.items():
        print(f"  cache entry: {k} -> resolved={v['resolved']}")
    print()

    comparison = run_comparison(orchestrator, cache)
    a, b = comparison["run_a"], comparison["run_b"]

    print("=== Run A (normal execution) ===")
    print(f"Duration: {a['duration_ms']:.3f} ms")
    print(f"Real Tool calls: {len(a['call_log'])}")
    print(f"Workflow completion state: {a['result']['workflow_completion_state']}")
    for sr in a["result"]["skill_reports"]:
        print(f"  {sr['skill']}: {sr['status']}")

    print("\n=== Run B (memory-aware execution) ===")
    print(f"Duration: {b['duration_ms']:.3f} ms")
    real_calls_b = sum(1 for c in b["call_log"] if c.real_call)
    served_calls_b = sum(1 for c in b["call_log"] if not c.real_call)
    print(f"Real Tool calls: {real_calls_b}, memory-served calls: {served_calls_b}, total: {len(b['call_log'])}")
    print(f"Workflow completion state: {b['result']['workflow_completion_state']}")
    for sr in b["result"]["skill_reports"]:
        print(f"  {sr['skill']}: {sr['status']}")

    print("\n=== Comparison ===")
    total_a = len(a["call_log"])
    reduction_pct = (served_calls_b / total_a * 100) if total_a else 0.0
    print(f"Tool invocation reduction: {served_calls_b}/{total_a} calls served from Memory ({reduction_pct:.1f}%)")

    print(f"Duration: Run A {a['duration_ms']:.3f} ms vs Run B {b['duration_ms']:.3f} ms "
          f"({'faster' if b['duration_ms'] < a['duration_ms'] else 'slower or equal'})")

    if len(a["call_log"]) == len(b["call_log"]):
        matches = sum(
            1 for ca, cb in zip(a["call_log"], b["call_log"])
            if ca.resolved == cb.resolved and ca.detail == cb.detail
        )
        print(f"Execution accuracy: {matches}/{len(a['call_log'])} calls produced identical (resolved, detail) between Run A and Run B")
    else:
        print(f"Execution accuracy: N/A -- call counts differ (A={len(a['call_log'])}, B={len(b['call_log'])}), cannot pair 1:1")

    a_statuses = [sr["status"] for sr in a["result"]["skill_reports"]]
    b_statuses = [sr["status"] for sr in b["result"]["skill_reports"]]
    print(f"Decision (per-Skill status) parity: {'identical' if a_statuses == b_statuses else 'DIFFERED'} -- A={a_statuses} B={b_statuses}")
    print(f"Workflow completion state parity: {'identical' if a['result']['workflow_completion_state'] == b['result']['workflow_completion_state'] else 'DIFFERED'}")


if __name__ == "__main__":
    main()
