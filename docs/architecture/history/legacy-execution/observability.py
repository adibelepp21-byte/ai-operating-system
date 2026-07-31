"""
Execution Observability Layer — Tier 3.

Reads existing Trace records and derives structured telemetry events.
Never writes execution behavior — this module has no call site inside
orchestrator.py, skill.py, or tool.py; it is a pure Trace reader,
exactly the same posture memory/extractor.py already has toward Trace,
applied to a different lens (execution health/performance instead of
reusable observations).

The one change this phase required in the execution path itself was
additive and disclosed in orchestrator.py: persisting `from_cache` and
`verification_status` into Trace's evidence dict, extending the exact
pattern Tier 1/2 already established for `parameters`/`tool_key`/
`fingerprint`. Without it, cache-hit/miss and verification telemetry
could not be derived from Trace at all — the data was computed
in-process and discarded at run end. Trace records written before this
addition report both fields as absent (None), honestly, not fabricated.

Granularity, disclosed precisely rather than assumed:
  - Skill-level duration: directly available (`duration_ms` has existed
    on every TraceRecord since Tier "Execution Foundation Stabilization
    Phase").
  - Tool-level duration: NOT separately derivable. Trace only ever
    timed the whole Skill invocation (skill.invoke()), never individual
    tool.invoke() calls within it — a Skill that calls a Tool 91 times
    (e.g. terminology-consistency-scan) has one duration_ms covering
    all 91 calls combined, not 91 individual timings. This module
    reports Tool call identity/count/cache-status/verification-status
    per Skill invocation, never fabricates a per-call duration that was
    never measured.
  - Workflow-level duration: derived, not directly stored — the span
    between the earliest and latest Trace record timestamp sharing the
    same agent_instance_id (one orchestrator.run() call = one Agent
    Instance = one Workflow invocation, confirmed by orchestrator.py's
    own structure).
  - Retry telemetry: always None/absent. Tier 1's ToolExecutor left
    retry as an explicit, unimplemented extension point
    (_apply_retry_policy is a no-op) — there is nothing to report
    because nothing retries yet. Reported as a real, current fact, not
    omitted.
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ToolCallTelemetry:
    tool_key: Optional[str]
    resolved: Optional[bool]
    # "hit" | "invalidated" | "no_entry" | "not_applicable" | None (verification_status
    # absent entirely -- pre-Tier-2 schema). Derived 1:1 from verification_status, not
    # from the from_cache boolean: collapsing not_applicable/no_entry/invalidated into a
    # single "miss" (the pre-hardening behavior) made cache_status indistinguishable
    # between "no cache was ever attached" and "a cache was consulted and missed" --
    # exactly the ambiguity the Execution Layer Validation Phase found made Tool
    # Metrics' cache_hit_rate misleading against the production corpus, where the vast
    # majority of calls are not_applicable (no cache attached at all).
    cache_status: Optional[str]
    verification_status: Optional[str]  # "verified" | "invalidated" | "no_entry" | "not_applicable" | None


@dataclass(frozen=True)
class SkillTelemetryEvent:
    trace_id: str
    agent_instance_id: Optional[str]
    workflow: Optional[str]
    skill_key: Optional[str]
    status: str
    failure_class: Optional[str]
    duration_ms: Optional[float]
    tool_calls: tuple
    timestamp: Optional[float]


@dataclass(frozen=True)
class WorkflowTelemetryEvent:
    agent_instance_id: Optional[str]
    workflow: Optional[str]
    duration_ms: Optional[float]
    skill_event_count: int
    final_status: Optional[str]


_VERIFICATION_TO_CACHE_STATUS = {
    "verified": "hit",
    "invalidated": "invalidated",
    "no_entry": "no_entry",
    "not_applicable": "not_applicable",
}


def _tool_call_telemetry(ev):
    verification_status = ev.get("verification_status")
    cache_status = _VERIFICATION_TO_CACHE_STATUS.get(verification_status)  # None if absent/unrecognized
    return ToolCallTelemetry(
        tool_key=ev.get("tool_key"),
        resolved=ev.get("resolved"),
        cache_status=cache_status,
        verification_status=verification_status,
    )


def extract_skill_events(trace_records):
    """One SkillTelemetryEvent per Trace record that actually represents
    a Skill invocation (skills_used non-empty) — spawn/terminate/
    escalation-only records are correctly excluded, not zero-filled."""
    events = []
    for r in trace_records:
        skills = r.get("skills_used") or []
        if not skills:
            continue
        outputs = r.get("outputs") or {}
        evidence = outputs.get("evidence") or []
        tool_calls = tuple(_tool_call_telemetry(ev) for ev in evidence if ev.get("source") == "tool")
        events.append(SkillTelemetryEvent(
            trace_id=r.get("trace_id"),
            agent_instance_id=r.get("agent_instance_id"),
            workflow=r.get("workflow"),
            skill_key=skills[0],  # orchestrator.py writes exactly one skill per Trace record, always
            status=r.get("status"),
            failure_class=outputs.get("failure_class"),
            duration_ms=r.get("duration_ms"),
            tool_calls=tool_calls,
            timestamp=r.get("timestamp"),
        ))
    return events


def extract_workflow_events(trace_records):
    """One WorkflowTelemetryEvent per distinct agent_instance_id —
    duration derived from the real timestamp span of that instance's
    own records, not a separately stored value."""
    by_instance = defaultdict(list)
    for r in trace_records:
        instance_id = r.get("agent_instance_id")
        if instance_id:
            by_instance[instance_id].append(r)

    events = []
    for instance_id, records in by_instance.items():
        records = sorted(records, key=lambda r: r.get("timestamp") or 0)
        if len(records) < 2:
            continue
        start_ts, end_ts = records[0].get("timestamp"), records[-1].get("timestamp")
        duration_ms = (end_ts - start_ts) * 1000 if start_ts is not None and end_ts is not None else None
        workflow = next((r.get("workflow") for r in records if r.get("workflow")), None)
        skill_count = sum(1 for r in records if r.get("skills_used"))
        final_status = (records[-1].get("outputs") or {}).get("workflow_completion_state")
        events.append(WorkflowTelemetryEvent(
            agent_instance_id=instance_id, workflow=workflow, duration_ms=duration_ms,
            skill_event_count=skill_count, final_status=final_status,
        ))
    return events
