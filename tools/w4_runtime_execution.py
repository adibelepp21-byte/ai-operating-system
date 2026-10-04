"""FR-2 — delegated Agency work, executed through the existing Runtime path.

Authorized by `FD-FR2-001` (FQ-FR2-1 = A). FR-2 discovery found Agency W4 work
running as a plain call: `W4Executor` → caller `perform` → `persist_evidence`,
never entering the Runtime and leaving no Trace. Every mechanism the Runtime
path needs already existed. This module connects them, and adds none:

```text
Agent Instance ── Delegation ── W4Executor (grant + instance re-checked per step)
                                     │
Runtime (RUNNING) ─► create_execution_layer ─► Execution (runtime_id, sequence)
                                     │
               DelegatedStep.participate(execution)        ← Agent / ExecutionConsumer
                                     │
                      TracedAction(writer, agent_instance=<grant recipient>,
                                   runtime=<the Execution's runtime>)
                                     │
                                  perform(step)            ← the delegated work
```

**The boundary (`§3`).** The step enters as an `Agent`, which is an
`ExecutionConsumer`, through the `Execution` the Runtime issued. Nothing here
reaches Runtime internals: the runtime identity and execution sequence are read
from the `Execution`'s context, and the Runtime is driven only through its
public lifecycle and the composition roots.

**No bypass (`§12`).** `perform` is called in exactly one place, inside
`DelegatedStep.participate`, and that accepts only a real `Execution` whose
Runtime is RUNNING. `RuntimeHostedExecutor` builds a fresh `Execution` for every
step through `create_execution_layer`, which refuses a Runtime that is not
RUNNING, so a step can neither run outside a Runtime nor be traced as if it had.

**Identity (`§6`).** The Trace actor is the grant's `recipient_instance`, the
Agent Instance the delegation names, never the definition key or a capability
name. FR-2 found `EngineeringIntelligenceAgent.participate` tracing its
definition key (G4); the existing `TracedAction` takes the instance as an
argument, so the Agency path supplies the right one and that consumer is not
changed.

**What the Trace records, and when.** Authorization comes first:
`W4Executor.execute_step` re-checks the grant, the instance and the scope, and a
refusal raises before any work is done, so no Trace is written for work that
did not happen. Only `perform` runs inside the `TracedAction`, so the record is
the action itself. Its status uses the existing mapping: `perform` returns →
`success`; `perform` raises → `failure`, and W4 records the same FAILURE. That
is the existing semantics, not a new one (`§9`). `escalation` keeps no producer
(G7), and the native consumer's participation-only status (G6) is unchanged.

**Persistence (`§8`).** The runtime identity, the execution sequence and the
Trace position are returned to the caller, which persists them through existing
writers: the W4 evidence `details`, the `ExecutionManifest`, the runtime
observation. The Runtime's own state stays process-local (G3), which this module
does not change.

Writes go only to live roots outside every phase directory, through the
certified-evidence guard. This module imports nothing from P12-W2 or P13.
"""

from __future__ import annotations

import contextlib
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Optional, Tuple

from native_core.core.agent import Agent
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage, build_default_infrastructure)
from native_core.core.runtime import RuntimeNotRunning, RuntimeState
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.execution import Execution, create_execution_layer
from native_core.core.trace import TraceWriter

from consumers.observation import TracedAction
from tools import p12_runtime_observation as observation
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.p12_certified_evidence_guard import guard
from tools.p12_execution_provenance import (
    LIVE_MANIFEST_ROOT, ExecutionManifest, record)
from tools.p12_trace_registry import LIVE_STORE_ROOT
from tools.planning import Plan, PlanStep, sequence
from tools.w4_delegation import W4Delegation
from tools.w4_execution import (
    ESCALATION, ExecutionOutcome, ExecutionRefused, ExecutionReport, W4Executor)

#: The live trace store every Agency execution is written to.
AGENCY_TRACE_STORE = "agency-w4-execution"


@dataclass(frozen=True)
class HostedStep:
    """Where one delegated step ran, and where its Trace is.

    ``trace_ordinal`` is None when no Trace was written, which happens only
    when the step was refused before any work was done.
    """

    outcome: ExecutionOutcome
    runtime_id: str
    execution_sequence: int
    trace_store: str
    trace_ordinal: Optional[int]

    def runtime_details(self) -> dict:
        """The step's runtime facts, in the form W4 evidence ``details`` take."""
        return {"runtime_id": self.runtime_id,
                "execution_sequence": self.execution_sequence,
                "trace_store": self.trace_store,
                "trace_ordinal": self.trace_ordinal}


class DelegatedStep(Agent):
    """One delegated plan step, taking part in one bound Execution.

    The Agent Instance's action under its delegation. It owns nothing: the
    executor holds the grant and re-checks it, the Execution carries the
    runtime identity, and `TracedAction` writes the single record.
    """

    def __init__(self, executor: W4Executor, instance_key: str, step: PlanStep,
                 perform: Callable[[PlanStep], str], writer: TraceWriter,
                 agent_definition_version: str) -> None:
        if not isinstance(writer, TraceWriter):
            raise TypeError("a delegated step is traced: it requires a TraceWriter")
        self._executor = executor
        self._instance_key = instance_key
        self._step = step
        self._perform = perform
        self._writer = writer
        self._version = agent_definition_version
        self.outcome: Optional[ExecutionOutcome] = None
        self.traced = False

    def participate(self, execution: Execution) -> None:
        if not isinstance(execution, Execution):
            raise TypeError("a delegated step enters only through an Execution "
                            "issued by a Runtime")
        if execution.runtime.state is not RuntimeState.RUNNING:
            raise RuntimeNotRunning(
                f"runtime {execution.context.runtime_id!r} is "
                f"{execution.runtime.state}; a delegated step runs only while "
                "its Runtime is RUNNING")
        runtime_id = execution.context.runtime_id
        actions = []

        def traced(step: PlanStep) -> str:
            with TracedAction(self._writer, agent_instance=self._instance_key,
                              runtime=runtime_id,
                              agent_definition_version=self._version) as action:
                actions.append(action)
                detail = self._perform(step)
                action.produced({"step": step.key, "detail": detail})
            return detail

        try:
            self.outcome = self._executor.execute_step(self._step, traced)
        finally:
            self.traced = any(a.written for a in actions)


class RuntimeHostedExecutor:
    """Executes a delegation's plan steps, each inside a Runtime Execution.

    Same contract as `W4Executor` (it delegates to one), with one difference:
    every step is a participation in a fresh `Execution` of ``runtime``, and is
    traced under the grant's recipient instance.
    """

    def __init__(self, delegation: W4Delegation, registry: AgentInstanceRegistry,
                 runtime, writer: TraceWriter, *,
                 trace_store: str = AGENCY_TRACE_STORE,
                 store_path: Optional[Path] = None) -> None:
        self._executor = W4Executor(delegation, registry)
        self._delegation = delegation
        self._registry = registry
        self._runtime = runtime
        self._writer = writer
        self._trace_store = trace_store
        self._store_path = Path(store_path) if store_path else LIVE_STORE_ROOT / trace_store

    def execute_step(self, step: PlanStep,
                     perform: Callable[[PlanStep], str]) -> HostedStep:
        execution = create_execution_layer(self._runtime)   # RUNNING-only
        registration = self._registry.get(self._delegation.recipient_instance)
        participant = DelegatedStep(
            self._executor, self._delegation.recipient_instance, step, perform,
            self._writer,
            registration.instance.agent_definition.agent_definition_version)
        participant.participate(execution)
        return HostedStep(
            outcome=participant.outcome,
            runtime_id=execution.context.runtime_id,
            execution_sequence=execution.context.execution_sequence,
            trace_store=self._trace_store,
            trace_ordinal=(trace_ordinal(self._store_path)
                           if participant.traced else None))

    def execute_plan(self, plan: Plan, perform: Callable[[PlanStep], str]
                     ) -> Tuple[ExecutionReport, Tuple[HostedStep, ...]]:
        """`W4Executor.execute_plan`'s rule, hosted: a refused step is recorded
        as an escalation and the remaining authorized work continues."""
        report, hosted = ExecutionReport(), []
        for step in sequence(plan):
            try:
                ran = self.execute_step(step, perform)
                report.outcomes.append(ran.outcome)
                hosted.append(ran)
            except ExecutionRefused as refusal:
                report.refusals.append(refusal)
                report.outcomes.append(ExecutionOutcome(
                    step_key=step.key, status=ESCALATION, detail=str(refusal),
                    delegation_id=self._delegation.delegation_id,
                    instance_key=self._delegation.recipient_instance,
                    at=_now()))
        return report, tuple(hosted)


def trace_ordinal(store_path: Path) -> int:
    """Index of the last record in the store, counted the way the chain reader
    resolves one: non-empty lines across the store's files, in path order."""
    lines = 0
    for path in sorted(Path(store_path).rglob("*")):
        if path.is_file():
            lines += len([ln for ln in path.read_text(encoding="utf-8").splitlines()
                          if ln.strip()])
    return lines - 1


def trace_writer(store_path: Path) -> TraceWriter:
    """A writer over a live trace store, refused if the store is certified."""
    guard(Path(store_path))
    storage = LocalAppendOnlyStorage(Path(store_path))
    storage.provision()
    return TraceWriter(storage)


@contextlib.contextmanager
def hosted_runtime(runtime_id: str, *,
                   observation_root: Path = observation.OBSERVATION_ROOT,
                   base_dir: Optional[Path] = None) -> Iterator[object]:
    """A real Runtime, started for the work and observed while it runs.

    Built through the composition roots (`build_default_infrastructure`,
    `create_runtime`) and driven only through its public lifecycle. Its state is
    published to the live observation root under ``runtime_id`` when it reaches
    RUNNING and when it stops: the observation is what persists of the Runtime
    (G3), and it is what a Trace's runtime identity is joined to.

    The Runtime's storage holds Knowledge, which delegated work does not admit
    or consume, so by default it is a temporary directory.
    """
    guard(Path(observation_root))
    with contextlib.ExitStack() as stack:
        if base_dir is None:
            base_dir = Path(stack.enter_context(tempfile.TemporaryDirectory()))
        bootstrap = build_default_infrastructure(base_dir=Path(base_dir))
        bootstrap.establish()
        runtime = create_runtime(runtime_id, storage=bootstrap.get("storage"),
                                 substrate=bootstrap.get("execution-substrate"))
        runtime.initialize()
        runtime.start()
        observation.publish(runtime_id, str(runtime.state),
                            kind=observation.RUNTIME, root=observation_root)
        try:
            yield runtime
        finally:
            runtime.stop()
            observation.publish(runtime_id, str(runtime.state),
                                kind=observation.RUNTIME, root=observation_root)


def record_manifest(hosted: HostedStep, delegation: W4Delegation, *, goal: str,
                    plan: str, plan_authority: str, agent_definition_version: str,
                    outcome: dict, root: Path = LIVE_MANIFEST_ROOT) -> Path:
    """The existing `ExecutionManifest`, for one hosted step, in the live root.

    Every field is one the manifest already has (`§7`: no new schema). It joins
    goal, plan, grant, instance, Trace position, runtime and outcome. The
    observation subject is the runtime identity, which is what makes
    EXECUTION → OBSERVATION a join.
    """
    if hosted.trace_ordinal is None:
        raise ValueError("a step that wrote no Trace has no execution to record")
    manifest = ExecutionManifest(
        execution_id=f"agency-{delegation.delegation_id}-{hosted.outcome.step_key}",
        goal=goal, plan=plan, plan_authority=plan_authority,
        work_scope=delegation.work_scope,
        agent_instance=delegation.recipient_instance,
        agent_definition_version=agent_definition_version,
        delegation_id=delegation.delegation_id, delegator=delegation.delegator,
        authority_instrument=delegation.authority.instrument,
        authority_record=delegation.authority.record,
        authority_chain=delegation.authority_chain(),
        capability_scope=delegation.capability_scope,
        trace_store=hosted.trace_store, trace_ordinal=hosted.trace_ordinal,
        runtime_id=hosted.runtime_id, status=hosted.outcome.status,
        observation_subject=hosted.runtime_id, observation_kind="runtime",
        verification_requirement=delegation.verification_requirement,
        outcome=outcome, delegation_status=delegation.status)
    return record(manifest, root=root)


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()
