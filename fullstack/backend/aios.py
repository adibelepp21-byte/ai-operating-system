"""The application layer's single adapter onto AIOS contracts (FS-02 `§2`).

```text
API  →  AIOSApplication  →  Runtime · Execution · Workflow · Tools · Trace
```

**What this module owns:** one Runtime's hosting lifetime in this process, the
Workflow catalog the application offers, and the application's run records.

**What it does not own, and never decides:**

* whether a Workflow transition is lawful: `WorkflowLifecycle` decides, asked
  by `WorkflowParticipatingAgent`;
* whether a Tool may run: `ToolInvocationGovernance` decides, asked by
  `ToolProposingAgent`;
* what a Trace says: each acting Agent authors its own, once (INV-4).

It imports public surfaces only: `native_core.core.<boundary>` exports and the
`consumers` agents. It imports nothing from `tools/`.

**Persistence** goes through the certified `StorageFacility` (FS-04): Trace in
its own partition, run records in `fullstack-runs`. No database is introduced
(`FS-DP-01`).
"""

from __future__ import annotations

import json
import secrets
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from consumers.engineering_intelligence_agent import (
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from consumers.tool_agent import ToolProposingAgent
from consumers.workflow_agent import StepFailed, WorkflowParticipatingAgent
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage, LocalExecutionSubstrate, StorageFacility)
from native_core.core.runtime import RuntimeState
from native_core.core.runtime.bootstrap import bootstrap_runtime
from native_core.core.runtime.execution import create_execution_layer
from native_core.core.trace import TraceReader, TraceWriter
from native_core.core.workflow import (
    AgentInstanceRef, SkillRef, Workflow, WorkflowComposition, WorkflowIdentity,
    WorkflowStep)

from . import docs_tool

RUNS_PARTITION = "fullstack-runs"
#: The run record format. A later format is a successor version read beside
#: this one, never a rewrite of records already appended (FS-04 `§4`).
RUN_FORMAT = "fullstack.run/1"
MAX_CRITERIA = 20
MAX_CRITERION_CHARS = 200
MAX_PATH_CHARS = 300


class ApplicationError(Exception):
    """Base of the adapter's refusals. The API maps each to a status."""


class InvalidRunRequest(ApplicationError):
    pass


class UnknownWorkflow(ApplicationError):
    pass


class NotRunning(ApplicationError):
    pass


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


@dataclass(frozen=True)
class CatalogEntry:
    key: str
    version: str
    title: str
    description: str
    composition: WorkflowComposition
    inputs: Mapping[str, Any]

    def describe(self) -> dict:
        return {"key": self.key, "version": self.version, "title": self.title,
                "description": self.description, "inputs": dict(self.inputs),
                "steps": [{"step_key": s.step_key,
                           "actor": s.performed_by.agent_instance_key,
                           "skill": s.composes.skill_key}
                          for s in self.composition.ordered()]}


READ_STEP, VERIFY_STEP = "read-document", "verify-criteria"
TOOL_AGENT = "tool-proposing-agent"
ENGINEERING_AGENT = "engineering-intelligence-agent"

DOCUMENT_CONFORMANCE_REVIEW = CatalogEntry(
    key="document-conformance-review",
    version="1",
    title="Document conformance review",
    description=("Reads a document under docs/ through the governed docs.read "
                 "Tool, then verifies it against stated criteria with the "
                 "Engineering Intelligence Testing sub-ability."),
    composition=WorkflowComposition(steps=(
        WorkflowStep(READ_STEP, AgentInstanceRef(TOOL_AGENT), SkillRef(docs_tool.KEY)),
        WorkflowStep(VERIFY_STEP, AgentInstanceRef(ENGINEERING_AGENT),
                     SkillRef("engineering.testing")),
    )),
    inputs={
        "document": {"type": "string", "description": "a .md or .txt path under docs/",
                     "max_length": MAX_PATH_CHARS},
        "criteria": {"type": "array", "items": "string", "min_items": 1,
                     "max_items": MAX_CRITERIA, "item_max_length": MAX_CRITERION_CHARS,
                     "description": "texts the document must contain"},
    },
)

CATALOG: Dict[str, CatalogEntry] = {DOCUMENT_CONFORMANCE_REVIEW.key: DOCUMENT_CONFORMANCE_REVIEW}


def validate_inputs(inputs: Any) -> Tuple[str, Tuple[str, ...]]:
    """The catalog's input contract. Refuses rather than coerces."""
    if not isinstance(inputs, dict):
        raise InvalidRunRequest("inputs must be an object")
    unknown = set(inputs) - {"document", "criteria"}
    if unknown:
        raise InvalidRunRequest(f"unknown input(s): {sorted(unknown)}")
    document, criteria = inputs.get("document"), inputs.get("criteria")
    if not isinstance(document, str) or not document.strip() or len(document) > MAX_PATH_CHARS:
        raise InvalidRunRequest("document must be a path of 1 to "
                                f"{MAX_PATH_CHARS} characters")
    if not isinstance(criteria, list) or not 1 <= len(criteria) <= MAX_CRITERIA:
        raise InvalidRunRequest(f"criteria must be a list of 1 to {MAX_CRITERIA} texts")
    for text in criteria:
        if not isinstance(text, str) or not text.strip() or len(text) > MAX_CRITERION_CHARS:
            raise InvalidRunRequest("each criterion must be a text of 1 to "
                                    f"{MAX_CRITERION_CHARS} characters")
    return document, tuple(criteria)


class AIOSApplication:
    """One Runtime, hosted for the life of this object, and the runs made on it."""

    def __init__(self, data_dir: Path, repo_root: Path,
                 clock: Callable[[], str] = _utc, boot_id: Optional[str] = None):
        self._data_dir = Path(data_dir)
        self._repo_root = Path(repo_root)
        self._clock = clock
        self._boot_id = boot_id or (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                                    + "-" + secrets.token_hex(3))
        self._lock = threading.RLock()
        self._runtime = None
        self._storage: Optional[StorageFacility] = None
        self._booted_at: Optional[str] = None
        self._run_count = 0

    # -- lifecycle ----------------------------------------------------------

    @property
    def runtime_id(self) -> str:
        return f"aios-fullstack/{self._boot_id}"

    @property
    def storage(self) -> StorageFacility:
        if self._storage is None:
            raise NotRunning("the application has not started")
        return self._storage

    def start(self) -> None:
        with self._lock:
            storage = LocalAppendOnlyStorage(self._data_dir / "storage")
            storage.provision()
            substrate = LocalExecutionSubstrate()
            substrate.provision()
            runtime = bootstrap_runtime(self.runtime_id, storage, substrate)
            runtime.start()
            tools = runtime.tools
            # Operator configuration, not an Agent act: the application's
            # composition defines, registers and enables its one Tool. Agents
            # still reach it only through governance (`FD-P8-001 §4.6`).
            tools.registry.define(docs_tool.IDENTITY, docs_tool.CONTRACT,
                                  docs_tool.METADATA)
            tools.registry.register(docs_tool.KEY)
            tools.registry.enable(docs_tool.KEY)
            tools.boundary.register(docs_tool.DocsReadTool(self._repo_root))
            self._storage, self._runtime = storage, runtime
            self._trace_writer = TraceWriter(storage)
            self._trace_reader = TraceReader(storage)
            self._run_count = sum(1 for _ in storage.read(RUNS_PARTITION))
            self._booted_at = self._clock()

    def stop(self) -> None:
        with self._lock:
            if self._runtime is not None and self._runtime.state is RuntimeState.RUNNING:
                self._runtime.stop()

    def _require_running(self):
        if self._runtime is None or self._runtime.state is not RuntimeState.RUNNING:
            raise NotRunning("the AIOS Runtime is not running")
        return self._runtime

    # -- reads --------------------------------------------------------------

    def health(self) -> dict:
        state = self._runtime.state.value if self._runtime is not None else "absent"
        return {"status": "ok" if state == RuntimeState.RUNNING.value else "unavailable",
                "runtime_state": state}

    def runtime_status(self) -> dict:
        with self._lock:
            runtime = self._require_running()
            hosted = {}
            for name in ("knowledge", "memory", "tools", "workflows"):
                try:
                    hosted[name] = getattr(runtime, name) is not None
                except Exception:  # a refusal is reported as not hosted
                    hosted[name] = False
            return {"runtime_id": runtime.runtime_id, "state": runtime.state.value,
                    "booted_at": self._booted_at, "hosted": hosted}

    def tools(self) -> List[dict]:
        with self._lock:
            registry = self._require_running().tools.registry
            described = []
            for key in registry.keys():
                d = registry.describe(key)
                described.append({
                    "key": key, "version": d.identity.version, "state": d.state.value,
                    "invocable": d.is_invocable, "actions": list(d.contract.actions),
                    "required_parameters": {a: list(p) for a, p in
                                            d.contract.required_parameters.items()},
                    "metadata": _plain(d.metadata)})
            return described

    def invocations(self) -> List[dict]:
        with self._lock:
            ledger = self._require_running().tools.ledger
            return [{"invocation_id": r.invocation_id, "tool_key": r.tool_key,
                     "caller": r.caller.value,
                     "lifecycle_state": r.lifecycle_state.value if r.lifecycle_state else None,
                     "governance_admitted": r.governance_admitted,
                     "execution_attempted": r.execution_attempted,
                     "disposition": r.disposition.value, "reason": r.reason}
                    for r in ledger.records]

    def catalog(self) -> List[dict]:
        return [entry.describe() for entry in CATALOG.values()]

    def runs(self) -> List[dict]:
        records = [json.loads(raw.decode("utf-8"))
                   for raw in self.storage.read(RUNS_PARTITION)]
        return list(reversed(records))

    def run(self, run_id: str) -> Optional[dict]:
        return next((r for r in self.runs() if r["run_id"] == run_id), None)

    def traces(self, offset: int = 0, limit: int = 50) -> dict:
        records, total = [], 0
        for position, record in enumerate(self._trace_reader.read()):
            total += 1
            if offset <= position < offset + limit:
                mapping = record.to_mapping()
                mapping["position"] = position
                records.append(mapping)
        return {"total": total, "offset": offset, "limit": limit, "records": records}

    def _trace_count(self) -> int:
        return sum(1 for _ in self._storage.read("trace"))

    # -- the one act: a Workflow run ----------------------------------------

    def start_run(self, workflow_key: str, inputs: Any, requested_by: str) -> dict:
        entry = CATALOG.get(workflow_key)
        if entry is None:
            raise UnknownWorkflow(f"no workflow {workflow_key!r} in the catalog")
        document, criteria = validate_inputs(inputs)
        with self._lock:
            runtime = self._require_running()
            run_id = f"run-{self._run_count + 1:05d}"
            identity = WorkflowIdentity(f"{entry.key}/{run_id}", entry.version)
            requested_at = self._clock()
            trace_from = self._trace_count()
            execution = create_execution_layer(runtime)
            steps: Dict[str, dict] = {}
            carried: Dict[str, Any] = {}

            def perform(step: WorkflowStep) -> None:
                try:
                    if step.step_key == READ_STEP:
                        self._read(step, execution, document, steps, carried)
                    elif step.step_key == VERIFY_STEP:
                        self._verify(step, execution, document, criteria, steps, carried)
                    else:
                        raise StepFailed(f"no performer for step {step.step_key!r}")
                except StepFailed:
                    raise
                except Exception as error:
                    # An unexpected error still ends the Workflow lawfully, in
                    # FAILED, rather than leaving it RUNNING with no terminal
                    # state. Its type is reported; its internals are not.
                    steps[step.step_key] = {"status": "failed",
                                            "error": type(error).__name__}
                    raise StepFailed(f"{step.step_key}: internal error "
                                     f"({type(error).__name__})") from error

            agent = WorkflowParticipatingAgent(
                workflow=Workflow(identity), composition=entry.composition,
                performer=perform, trace_writer=self._trace_writer)
            agent.participate(execution)
            terminal = runtime.workflows.monitor.state_of(identity)
            trace_to = self._trace_count()
            record = {
                "format": RUN_FORMAT,
                "run_id": run_id,
                "workflow": {"key": entry.key, "version": entry.version},
                "workflow_identity": {"key": identity.workflow_key,
                                      "version": identity.workflow_version},
                "runtime_id": runtime.runtime_id,
                "execution_sequence": execution.context.execution_sequence,
                "requested_by": requested_by,
                "requested_at": requested_at,
                "completed_at": self._clock(),
                "inputs": {"document": document, "criteria": list(criteria)},
                "states": [s.state.value for s in agent.observed_states],
                "state": terminal.state.value,
                "succeeded": terminal.is_success,
                "failure_reason": terminal.detail.get("reason"),
                "steps": [dict({"step_key": s.step_key,
                                "actor": s.performed_by.agent_instance_key,
                                "skill": s.composes.skill_key},
                               **steps.get(s.step_key, {"status": "not_run"}))
                          for s in entry.composition.ordered()],
                "outcome": carried.get("outcome"),
                "trace": {"from": trace_from, "to": trace_to,
                          "count": trace_to - trace_from},
            }
            self._storage.append(RUNS_PARTITION, json.dumps(
                record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            self._run_count += 1
            return record

    def _read(self, step, execution, document, steps, carried) -> None:
        agent = ToolProposingAgent(
            proposal=(docs_tool.KEY, docs_tool.ACTION, {"path": document}),
            trace_writer=self._trace_writer)
        agent.participate(execution)
        result = agent.results[-1]
        detail = {"disposition": result.disposition.value,
                  "execution_attempted": result.execution_attempted}
        if not result.is_success:
            steps[step.step_key] = dict(detail, status="failed", reason=result.reason)
            raise StepFailed(f"{docs_tool.KEY} {result.disposition.value}: {result.reason}")
        value = result.value
        steps[step.step_key] = dict(detail, status="completed", bytes=value["bytes"],
                                    sha256=value["sha256"], lines=len(value["lines"]))
        carried["lines"] = tuple(value["lines"])

    def _verify(self, step, execution, document, criteria, steps, carried) -> None:
        stated = tuple(ConformanceCriterion(name=f"criterion-{i + 1}", required_text=text)
                       for i, text in enumerate(criteria))
        agent = EngineeringIntelligenceAgent(
            artifact=Artifact(name=document, lines=carried["lines"]),
            criteria=stated, trace_writer=self._trace_writer)
        agent.participate(execution)
        checked = [{"name": c.name, "required_text": c.required_text,
                    "satisfied": r.satisfied} for c, r in zip(stated, agent.results)]
        satisfied = sum(1 for c in checked if c["satisfied"])
        steps[step.step_key] = {"status": "completed", "criteria": checked}
        carried["outcome"] = {"conformant": satisfied == len(checked),
                              "satisfied": satisfied, "total": len(checked)}


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value
