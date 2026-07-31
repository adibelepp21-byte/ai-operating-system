"""
Execution Metrics — Tier 4.

Pure, read-only aggregation over Observability's already-extracted
telemetry events (execution/observability.py). Never reads Trace files
directly — the layering is strict and one-directional: Trace →
Observability (extraction) → Metrics (aggregation). This module has no
call site anywhere in the execution path (orchestrator.py, skill.py,
tool.py, tool_executor.py) — nothing computed here can ever influence
execution behavior. Verified by an automated layering test
(execution/tests/test_metrics.py) that inspects this file's own import
statements, not just documentation claiming it.

Implements only metrics classified "Computable Now" in the approved
Tier 4 specification. Explicitly NOT implemented, per that
classification: retry rate (nothing retries yet — Tier 1's
ToolExecutor._apply_retry_policy is a documented no-op), cost/resource
metrics (cost_resource_metadata has been empty in every real Trace
record produced so far), per-Runtime breakdown (Observability doesn't
expose `runtime` on SkillTelemetryEvent yet), Tool-level duration
(never separately timed), any Memory/Knowledge-correlated metric, SLA
alerting, or trend/time-series analysis.

Every function here is a pure function: no state, no I/O, no side
effects, and no mutation of its inputs. Given the same list of events,
every function returns byte-identical output — verified directly by a
determinism test.
"""

import statistics
from dataclasses import dataclass
from typing import Optional


def _percentile(sorted_values, pct):
    """Nearest-rank percentile (no interpolation) — the simplest,
    most transparent definition, adequate at this corpus's current
    sample sizes. `sorted_values` must already be sorted ascending."""
    if not sorted_values:
        return None
    n = len(sorted_values)
    rank = max(1, int(round(pct / 100 * n)))
    return sorted_values[min(rank, n) - 1]


def _duration_stats(events):
    durations = sorted(e.duration_ms for e in events if e.duration_ms is not None)
    if not durations:
        return None, None, None, None
    return (
        statistics.fmean(durations),
        statistics.median(durations),
        _percentile(durations, 95),
        durations[-1],
    )


@dataclass(frozen=True)
class SkillMetrics:
    skill_key: str
    total_invocations: int
    success_count: int
    failure_count: int
    not_implemented_count: int
    success_rate: Optional[float]      # not_implemented excluded from both numerator and denominator
    avg_duration_ms: Optional[float]
    median_duration_ms: Optional[float]
    p95_duration_ms: Optional[float]
    max_duration_ms: Optional[float]


@dataclass(frozen=True)
class ToolMetrics:
    tool_key: str
    total_calls: int
    cache_hit_count: int                  # cache_status == "hit" (verified, served without a live call)
    cache_invalidated_count: int          # cache_status == "invalidated" (entry found, rejected, live call ran)
    cache_no_entry_count: int             # cache_status == "no_entry" (cache attached, key absent)
    cache_not_applicable_count: int       # cache_status == "not_applicable" (no cache attached at all)
    cache_unknown_count: int              # cache_status is None -- pre-Tier-2 Trace, verification_status never recorded
    # hit / (hit + invalidated + no_entry): the fraction of calls where a cache was
    # actually consulted that were served without a live execution. Deliberately
    # excludes not_applicable and unknown from the denominator -- including them (the
    # pre-hardening behavior) let calls that never had a cache in play dominate this
    # rate, making it read as "caching barely helps" when the real story was "caching
    # was rarely even attempted." None if no calls ever had a cache consulted.
    cache_hit_rate: Optional[float]
    live_execution_rate: Optional[float]  # 1 - cache_hit_rate, None under the same condition
    verified_count: int
    invalidated_count: int
    verification_rate: Optional[float]


@dataclass(frozen=True)
class WorkflowMetrics:
    workflow_key: str
    total_runs: int
    completed_count: int
    escalated_count: int
    failed_count: int
    success_rate: Optional[float]
    avg_duration_ms: Optional[float]
    median_duration_ms: Optional[float]
    p95_duration_ms: Optional[float]
    max_duration_ms: Optional[float]


@dataclass(frozen=True)
class BottleneckEntry:
    skill_key: str
    avg_duration_ms: float
    sample_count: int
    rank: int


def compute_skill_metrics(skill_events):
    """Groups by skill_key. Pure: does not mutate `skill_events`."""
    by_skill = {}
    for e in skill_events:
        by_skill.setdefault(e.skill_key, []).append(e)

    results = []
    for skill_key, events in sorted(by_skill.items()):
        total = len(events)
        success = sum(1 for e in events if e.status == "success")
        not_impl = sum(1 for e in events if e.failure_class == "not_implemented")
        failure = sum(1 for e in events if e.status == "failure") - not_impl
        denom = total - not_impl
        success_rate = (success / denom) if denom > 0 else None

        avg, median, p95, dmax = _duration_stats(events)

        results.append(SkillMetrics(
            skill_key=skill_key, total_invocations=total, success_count=success,
            failure_count=failure, not_implemented_count=not_impl, success_rate=success_rate,
            avg_duration_ms=avg, median_duration_ms=median, p95_duration_ms=p95, max_duration_ms=dmax,
        ))
    return results


def compute_tool_metrics(skill_events):
    """Aggregates ToolCallTelemetry across every skill_event's
    tool_calls tuple. Pure: does not mutate `skill_events`."""
    by_tool = {}
    for e in skill_events:
        for tc in e.tool_calls:
            if tc.tool_key is None:
                continue
            by_tool.setdefault(tc.tool_key, []).append(tc)

    results = []
    for tool_key, calls in sorted(by_tool.items()):
        total = len(calls)
        hits = sum(1 for c in calls if c.cache_status == "hit")
        invalidated_cache = sum(1 for c in calls if c.cache_status == "invalidated")
        no_entry = sum(1 for c in calls if c.cache_status == "no_entry")
        not_applicable = sum(1 for c in calls if c.cache_status == "not_applicable")
        unknown = total - hits - invalidated_cache - no_entry - not_applicable

        cache_consulted = hits + invalidated_cache + no_entry
        cache_hit_rate = (hits / cache_consulted) if cache_consulted > 0 else None
        live_execution_rate = (1 - cache_hit_rate) if cache_hit_rate is not None else None

        verified = sum(1 for c in calls if c.verification_status == "verified")
        invalidated = sum(1 for c in calls if c.verification_status == "invalidated")
        v_denom = verified + invalidated
        verification_rate = (verified / v_denom) if v_denom > 0 else None

        results.append(ToolMetrics(
            tool_key=tool_key, total_calls=total,
            cache_hit_count=hits, cache_invalidated_count=invalidated_cache,
            cache_no_entry_count=no_entry, cache_not_applicable_count=not_applicable,
            cache_unknown_count=unknown, cache_hit_rate=cache_hit_rate,
            live_execution_rate=live_execution_rate,
            verified_count=verified, invalidated_count=invalidated, verification_rate=verification_rate,
        ))
    return results


def compute_workflow_metrics(workflow_events):
    """Groups by workflow key. Pure: does not mutate `workflow_events`."""
    by_wf = {}
    for e in workflow_events:
        key = e.workflow or "(unknown)"
        by_wf.setdefault(key, []).append(e)

    results = []
    for workflow_key, events in sorted(by_wf.items()):
        total = len(events)
        completed = sum(1 for e in events if e.final_status == "completed")
        escalated = sum(1 for e in events if e.final_status == "escalated")
        failed = sum(1 for e in events if e.final_status == "failed")
        success_rate = (completed / total) if total > 0 else None

        avg, median, p95, dmax = _duration_stats(events)

        results.append(WorkflowMetrics(
            workflow_key=workflow_key, total_runs=total, completed_count=completed,
            escalated_count=escalated, failed_count=failed, success_rate=success_rate,
            avg_duration_ms=avg, median_duration_ms=median, p95_duration_ms=p95, max_duration_ms=dmax,
        ))
    return results


def bottleneck_report(skill_events, top_n=5):
    """Formalizes the ranking Tier 3's report script did ad hoc.
    Pure: derives entirely from compute_skill_metrics()."""
    metrics = compute_skill_metrics(skill_events)
    ranked = sorted((m for m in metrics if m.avg_duration_ms is not None), key=lambda m: -m.avg_duration_ms)
    return [
        BottleneckEntry(skill_key=m.skill_key, avg_duration_ms=m.avg_duration_ms, sample_count=m.total_invocations, rank=i + 1)
        for i, m in enumerate(ranked[:top_n])
    ]
