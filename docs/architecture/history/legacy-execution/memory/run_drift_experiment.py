#!/usr/bin/env python3
"""
Runs the Memory Drift Experiment end to end — the exact same scenario
used pre-Tier-2 (real Tool calls against real, self-contained scratch
files outside docs/, a genuine file edit introduced between Run A and
Run B) — now exercised through the real Evidence Verification Layer
(tool_executor.ToolExecutor + verification.py) instead of a hand-rolled
cache check, so the reported findings reflect actually-observed
behavior, not narrative text written in advance.

The Trace-record wrapper around each real call is constructed directly
here (this is an isolated diagnostic, not a full orchestrator run
through a real Agent Definition/Workflow) — but the call itself, its
evidence, the fingerprint, and the file edit between Run A and Run B
are all real, not fabricated.
"""

import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution.memory import drift_experiment as drift
from execution.memory.extractor import extract_memories, is_expired
from execution.memory.consumption import build_input_keyed_cache
from execution.tool import ToolRequest
from execution.tool_executor import ToolExecutor


def _make_trace_record(execution, timestamp):
    ev = execution.evidence or {}
    return {
        "trace_id": f"trace-{uuid.uuid4().hex[:12]}",
        "schema_version": "1.1",
        "agent_instance_id": f"instance-drift-{uuid.uuid4().hex[:8]}",
        "agent_definition_name": "drift-experiment",
        "agent_definition_version": "n/a",
        "runtime": "n/a",
        "workflow": None,
        "skills_used": (),
        "tools_used": (execution.request.tool_canonical_key,),
        "outputs": {
            "evidence": [{
                "source": "tool", "kind": "cross_reference_check",
                "tool_key": execution.request.tool_canonical_key,
                "resolved": ev.get("resolved"),
                "detail": execution.error or ev.get("failure_reason") or "resolved",
                "parameters": dict(execution.request.parameters),
                "fingerprint": execution.fingerprint,  # Tier 2: required for verification to be possible at all
            }],
        },
        "status": "success" if execution.succeeded else "failure",
        "timestamp": timestamp,
    }


def main():
    citing, cited = drift.setup_scratch()

    print("=== Run A: real Tool call against initial state ===")
    execution_a = drift.call_tool(citing, cited)
    ev_a = execution_a.evidence or {}
    print(f"resolved={ev_a.get('resolved')} detail={ev_a.get('failure_reason') or 'resolved'}")
    print(f"fingerprint recorded: {execution_a.fingerprint}")
    record_a = _make_trace_record(execution_a, timestamp=time.time())

    memories = extract_memories([record_a], retention_seconds=3600)
    print(f"\nMemory extracted: {len(memories)} record(s)")
    for m in memories:
        print(f"  confidence={m.confidence} content={m.content!r}")

    cache = build_input_keyed_cache([record_a])
    print(f"\nInput-keyed cache: {cache}")

    print("\n=== Controlled change: cited.md genuinely edited (adds heading '## 9.') ===")
    drift.introduce_controlled_change(cited)

    print("\n=== Run B: memory-aware call through the real Evidence Verification Layer ===")
    from execution import tool as tool_mod
    executor = ToolExecutor(tool_mod._registry(), cache=cache)
    request_b = ToolRequest(
        tool_canonical_key="tool.cross-reference-link-validator-interface",
        action="verify_cross_reference",
        parameters={
            "citing_document": str(citing),
            "repository_path": str(drift.REPO_ROOT),
            "reference_target": str(cited),
            "expected_reference": "§9",
        },
    )
    result_b = executor.execute(request_b)
    print(f"verification_status={result_b.verification_status} from_cache={result_b.from_cache}")
    print(f"Result: resolved={result_b.raw.get('resolved')} detail={result_b.raw.get('failure_reason') or 'resolved'}")

    print("\n=== Live ground truth (independent real call, for comparison only) ===")
    execution_b_live = drift.call_tool(citing, cited)
    ev_b = execution_b_live.evidence or {}
    print(f"resolved={ev_b.get('resolved')} detail={ev_b.get('failure_reason') or 'resolved'}")

    print("\n=== Findings (driven by the actual result above, not pre-written) ===")
    detected = result_b.verification_status == "invalidated"
    returned_stale = result_b.from_cache and result_b.raw.get("resolved") != ev_b.get("resolved")
    live_triggered = not result_b.from_cache
    result_matches_current = result_b.raw.get("resolved") == ev_b.get("resolved")

    print(f"1. Did Memory detect the outdated information?  {'YES' if detected else 'NO'} -- "
          f"verification_status={result_b.verification_status!r}.")
    print(f"2. Did Memory incorrectly reuse stale evidence?  {'YES' if returned_stale else 'NO'} -- "
          f"from_cache={result_b.from_cache}, returned resolved={result_b.raw.get('resolved')} "
          f"vs live resolved={ev_b.get('resolved')}.")
    print(f"3. Was live Tool execution triggered on the stale entry?  {'YES' if live_triggered else 'NO'} -- "
          f"from_cache={result_b.from_cache} (False means a live call ran instead of trusting the cache).")
    print(f"4. Does the final result match the current repository state?  {'YES' if result_matches_current else 'NO'} -- "
          f"{result_b.raw.get('resolved')} == {ev_b.get('resolved')}.")

    success = detected and not returned_stale and live_triggered and result_matches_current
    print(f"\nTier 2 acceptance criteria met: {success}")


if __name__ == "__main__":
    main()
