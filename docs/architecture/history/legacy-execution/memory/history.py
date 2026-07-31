"""
Memory experiment: execution-history aggregation.

Tests whether execution history provides operational value — the
question Domain Model's Memory concept (§2: "Dynamic, experiential,
scoped record of what an Agent Instance has encountered") raises —
without creating any Memory entity, persistence contract, retention
policy, or promotion path. This module only reads the disposable,
already-produced JSON Lines Trace files under execution/traces/; it
defines no scope model and writes nothing.

Capability Hardening Phase change: every loaded record is now passed
through trace_schema.normalize_record() before aggregation. The prior
phase's Memory Experiment Report found that aggregation silently
excluded 8 of 12 recorded Tool invocations because they were written
under the pre-1.1 evidence-key shape ("resolves" vs "resolved"). That
was fixed, but a second, undetected instance of the same class of bug
was found during this phase's audit (Memory Foundation Experiment,
task 1): tool_resolution_rate below read `outputs["tool_executions"]`
directly, which the Capability Hardening Phase's own newest-generation
records never had (they carry `outputs["evidence"]` only) — so this
metric had been silently blind to every record from that generation
since it was introduced, undetected because no report had reason to
notice a metric quietly excluding the newest data. Fixed here by
reading the uniform `outputs["evidence"]` list that
trace_schema.normalize_record() now guarantees for every generation
(see trace_schema.py's _normalize_outputs), rather than re-deriving
generation-specific parsing here.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

from ..trace_schema import normalize_record

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TRACE_DIR = REPO_ROOT / "execution" / "traces"


def load_all_records():
    records = []
    for f in sorted(TRACE_DIR.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(normalize_record(json.loads(line)))
    return records


@dataclass
class ExecutionSummary:
    total_records: int = 0
    schema_version_counts: dict = field(default_factory=dict)
    status_counts: dict = field(default_factory=dict)
    skill_invocation_counts: dict = field(default_factory=dict)
    tool_invocation_counts: dict = field(default_factory=dict)
    tool_resolution_rate: dict = field(default_factory=dict)  # evidence kind -> "resolved/total"


def summarize(records):
    summary = ExecutionSummary(total_records=len(records))
    resolved_totals = {}

    for r in records:
        summary.schema_version_counts[r["schema_version"]] = summary.schema_version_counts.get(r["schema_version"], 0) + 1
        summary.status_counts[r["status"]] = summary.status_counts.get(r["status"], 0) + 1
        for s in r.get("skills_used", []) or []:
            summary.skill_invocation_counts[s] = summary.skill_invocation_counts.get(s, 0) + 1
        for t in r.get("tools_used", []) or []:
            summary.tool_invocation_counts[t] = summary.tool_invocation_counts.get(t, 0) + 1
        for ev in (r.get("outputs") or {}).get("evidence", []) or []:
            if ev.get("source") == "tool" and ev.get("resolved") is not None:
                kind = ev.get("kind", "unknown")
                resolved_totals.setdefault(kind, [0, 0])
                resolved_totals[kind][1] += 1
                if ev["resolved"]:
                    resolved_totals[kind][0] += 1

    summary.tool_resolution_rate = {k: f"{v[0]}/{v[1]}" for k, v in resolved_totals.items()}
    return summary
