"""
Memory extractor — experimental, not a Memory Framework, not an
implementation of the Memory entity.

Reads real Trace records (via trace_schema.normalize_record, which this
phase extended to also normalize the top-level `outputs` shape across
every generation currently on disk — see trace_schema.py) and derives
provisional MemoryRecord entries from evidence an Agent Instance
encountered during execution. This tests whether Domain Model's
Agent-Instance-produces-Memory relationship (§4) — never yet exercised
by this harness; every TraceRecord.memory_consumed field has been an
honestly-empty tuple across all prior phases — has any operational value
if exercised against execution data already on hand.

Why this does not represent a governed Memory entity (see also the
Memory Foundation Experiment's Architecture Report):

  - **Scope is looser than Domain Model §5 requires.** Real Memory is
    "owned/scoped by the Agent Instance... that produced it" — one
    instance. This extractor deduplicates identical observations
    *across* Agent Instances (across separate runs), because the same
    fact re-observed identically many times is not a new experience
    worth a new record. That is a deliberate, useful design choice for
    an experiment, but it means a MemoryRecord here is scoped to
    `agent_instance_ids` (plural) — evidence, not an accident, that
    naive cross-run extraction does not trivially fit Domain Model's
    single-instance scope model without further design.
  - **Expiry is computed, never enforced.** `retention_seconds` and
    `is_expired()` exist; nothing deletes an expired record. Domain
    Model §6 requires "Promote or expire" as real lifecycle behavior;
    this module only reports whether a record *would* be expired if
    asked.
  - **Promotion is never attempted.** Memory-promotes-to-Knowledge
    (§4, invariant 8) requires governed review. This module has no
    reviewer, simulates none, and status is never anything but
    "provisional" or "expired" — "promoted" does not appear anywhere in
    this module's vocabulary.

Memory Lifecycle Validation Experiment additions (confidence,
frequency, first/last observed):

  - **confidence** is a transparent, explicitly heuristic formula, not a
    statistical model: `0.5 + 0.05*occurrence_count + 0.05*distinct
    instances`, capped at 1.0. Base 0.5 reflects genuine uncertainty for
    a single occurrence; repetition and independent re-derivation across
    separate Agent Instances both raise it, since a fact re-observed
    only once could be noise, while one seen many times by many separate
    runs is stronger evidence of a stable, real condition rather than a
    one-off artifact of a specific execution.
  - **observation_frequency** = occurrences / distinct source traces —
    how often, on average, one run's execution encounters this
    observation. Not a time-based rate: this session's traces span
    minutes, not a meaningful duration to rate against.
  - **first_observed_at / last_observed_at** are derived from the
    *source Trace records' own* `timestamp` field — not from when the
    extractor happened to run. This is a real correction: the prior
    phase's `created_at` was always "now" at extraction time, which
    made `is_expired()` structurally incapable of ever returning True
    (nothing can be older than "now" minus a nonzero retention window
    measured from itself). `is_expired()` below now measures from
    `last_observed_at`, the only reference against which expiry is a
    meaningful question.
"""

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ..trace_schema import normalize_record

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TRACE_DIR = REPO_ROOT / "execution" / "traces"
MEMORY_RECORDS_DIR = REPO_ROOT / "execution" / "memory" / "records"

DEFAULT_RETENTION_SECONDS = 3600  # experimental default; no ratified retention policy exists anywhere


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    agent_instance_ids: tuple
    source_trace_ids: tuple
    observation_kind: str
    content: str
    occurrence_count: int
    observation_frequency: float  # occurrences / distinct source traces
    confidence: float             # experimental heuristic — see module docstring
    first_observed_at: float      # earliest contributing Trace record's own timestamp
    last_observed_at: float       # latest contributing Trace record's own timestamp
    created_at: float             # when this MemoryRecord was computed (extraction wall-clock)
    retention_seconds: float
    status: str  # "provisional" | "expired" -- "promoted" deliberately does not exist here


def is_expired(record: MemoryRecord, now=None) -> bool:
    now = now if now is not None else time.time()
    reference = record.last_observed_at if record.last_observed_at is not None else record.created_at
    return (now - reference) > record.retention_seconds


def evaluate_relevance(record: MemoryRecord, now=None) -> str:
    """A minimal, explicitly heuristic relevance label — not a scoring
    system. "stale" beats "low_confidence" beats "fresh" in severity;
    this is a coarse triage, not a ranked score."""
    if is_expired(record, now=now):
        return "stale"
    if record.confidence < 0.6:
        return "low_confidence"
    return "fresh"


def load_trace_records():
    records = []
    for f in sorted(TRACE_DIR.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(normalize_record(json.loads(line)))
    return records


def extract_memories(trace_records=None, retention_seconds=DEFAULT_RETENTION_SECONDS):
    """Identifies reusable observations across the given (or all
    on-disk) Trace records and returns provisional MemoryRecords,
    deduplicated by (observation_kind, content). A "reusable
    observation" is any evidence entry an executed Skill or Tool
    actually produced — not every Trace event qualifies: spawn/
    terminate/escalation events carry no evidence and produce nothing."""
    if trace_records is None:
        trace_records = load_trace_records()

    grouped = {}  # (kind, content) -> {"agent_instance_ids", "trace_ids", "count", "first_ts", "last_ts"}
    for record in trace_records:
        evidence = (record.get("outputs") or {}).get("evidence") or []
        ts = record.get("timestamp")
        for ev in evidence:
            kind = ev.get("kind")
            content = ev.get("detail")
            if not kind or not content:
                continue
            key = (kind, content)
            bucket = grouped.setdefault(key, {
                "agent_instance_ids": set(), "trace_ids": set(), "count": 0,
                "first_ts": None, "last_ts": None,
            })
            bucket["agent_instance_ids"].add(record.get("agent_instance_id"))
            bucket["trace_ids"].add(record.get("trace_id"))
            bucket["count"] += 1
            if ts is not None:
                if bucket["first_ts"] is None or ts < bucket["first_ts"]:
                    bucket["first_ts"] = ts
                if bucket["last_ts"] is None or ts > bucket["last_ts"]:
                    bucket["last_ts"] = ts

    now = time.time()
    memories = []
    for (kind, content), bucket in grouped.items():
        trace_count = len(bucket["trace_ids"])
        frequency = bucket["count"] / trace_count if trace_count else 0.0
        confidence = round(min(1.0, 0.5 + 0.05 * bucket["count"] + 0.05 * len(bucket["agent_instance_ids"])), 2)
        memories.append(MemoryRecord(
            memory_id=f"memory-{uuid.uuid4().hex[:12]}",
            agent_instance_ids=tuple(sorted(bucket["agent_instance_ids"])),
            source_trace_ids=tuple(sorted(bucket["trace_ids"])),
            observation_kind=kind,
            content=content,
            occurrence_count=bucket["count"],
            observation_frequency=round(frequency, 2),
            confidence=confidence,
            first_observed_at=bucket["first_ts"],
            last_observed_at=bucket["last_ts"],
            created_at=now,
            retention_seconds=retention_seconds,
            status="provisional",
        ))
    return memories


class MemoryStore:
    """Deliberately disposable — analogous to trace.py's TraceWriter,
    not a persistence contract. A real Memory entity's actual storage,
    retention enforcement, and scoping model remain entirely undefined;
    this exists only so this experiment's output is inspectable, not
    because this shape is proposed as a convention."""

    def __init__(self, run_id=None):
        self.run_id = run_id or f"memrun-{uuid.uuid4().hex[:12]}"
        MEMORY_RECORDS_DIR.mkdir(parents=True, exist_ok=True)
        self.path = MEMORY_RECORDS_DIR / f"{self.run_id}.jsonl"

    def write_all(self, records):
        with open(self.path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(asdict(r), default=str) + "\n")
        return self.path
