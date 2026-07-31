"""
Trace production.

Implements Domain Model §2.1's required-content shape and Constitution
§14.2's unconditional-production rule ("Produce a Trace for every
action, without exception") as real, executable code.

Capability Hardening Phase adds two fields as a deliberate, real schema
evolution test (see trace_schema.py for the compatibility-handling
half of this experiment):

  - `schema_version` — the shape version this record was written under.
    Every record from this phase onward carries "1.1"; records written
    by earlier phases have no such field at all (plain absence, not a
    null), since the field didn't exist yet. That real gap is what
    trace_schema.normalize_record() is exercised against.
  - `duration_ms` — how long the traced action took, an "additional
    field" introduced without coordinating with, or breaking, any
    existing consumer: old records simply lack the key, and
    memory/history.py already tolerates missing keys via .get().

Still deliberately not a Trace Framework: no governance document is
created or implied, and the storage format (append-only JSON Lines
under execution/traces/) remains an explicit, disposable implementation
choice, not a ratified convention.
"""

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = REPO_ROOT / "execution" / "traces"

SCHEMA_VERSION = "1.1"


@dataclass(frozen=True)
class TraceRecord:
    trace_id: str
    schema_version: str
    agent_definition_name: str
    agent_definition_version: str
    agent_instance_id: str
    runtime: str
    workflow: Optional[str]
    skills_used: tuple
    tools_used: tuple
    knowledge_consumed: tuple
    memory_consumed: tuple
    inputs: Any
    outputs: Any
    cost_resource_metadata: dict
    status: str  # "success" | "failure" | "escalation"
    duration_ms: Optional[float] = None
    timestamp: float = field(default_factory=time.time)


class TraceWriter:
    """Append-only by construction: write() only ever appends a new
    line to the run's file, matching Domain Model §7 invariant 5
    ('Trace is immutable and append-only; once written, never edited or
    deleted') as a real behavioral property of this code, not only a
    governance statement about a concept."""

    def __init__(self, run_id=None):
        self.run_id = run_id or f"run-{uuid.uuid4().hex[:12]}"
        TRACE_DIR.mkdir(parents=True, exist_ok=True)
        self.path = TRACE_DIR / f"{self.run_id}.jsonl"

    def write(self, record: TraceRecord):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(record), default=str) + "\n")
        return record


def new_record(
    agent_instance, runtime, workflow=None,
    skills_used=(), tools_used=(), inputs=None, outputs=None, status="success",
    duration_ms=None,
):
    return TraceRecord(
        trace_id=f"trace-{uuid.uuid4().hex[:12]}",
        schema_version=SCHEMA_VERSION,
        agent_definition_name=agent_instance.agent_definition_name,
        agent_definition_version=agent_instance.agent_definition_version,
        agent_instance_id=agent_instance.instance_id,
        runtime=runtime.canonical_key,
        workflow=workflow,
        skills_used=tuple(skills_used),
        tools_used=tuple(tools_used),
        knowledge_consumed=(),
        memory_consumed=(),
        inputs=inputs,
        outputs=outputs,
        cost_resource_metadata={},
        status=status,
        duration_ms=duration_ms,
    )
