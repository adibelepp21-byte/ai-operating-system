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
          participant.participate(execution)               ← Agent / ExecutionConsumer
          (agency_runtime_execution.py DelegatedStep, injected)
                                     │
                      TracedAction(writer, agent_instance=<grant recipient>,
                                   runtime=<the Execution's runtime>)
                                     │
                                  perform(step)            ← the delegated work
```

**Two regions, one wiring.** `tools/` may not import `consumers/`, and the
consumer region may not import `tools/` (both asserted by AST). So this module
holds the authority side and takes the participant **by injection**: a factory
returning a native-core `Agent`. The resident one, `DelegatedStep`, is defined
and bound at the repository root in `agency_runtime_execution.py` (it uses
`consumers.observation.TracedAction`), the way `w4_first_execution.py` binds
W4's performer. This module never names the implementation that does the work.

**The boundary (`§3`).** The step enters as an `Agent`, which is an
`ExecutionConsumer`, through the `Execution` the Runtime issued. Nothing here
reaches Runtime internals: the runtime identity and execution sequence are read
from the `Execution`'s context, and the Runtime is driven only through its
public lifecycle and the composition roots.

**No bypass (`§12`).** This module never calls `perform`: it only hands it to
the participant, which must be a native-core `Agent` and is called only through
`participate(execution)`. `RuntimeHostedExecutor` builds a fresh `Execution` for
every step through `create_execution_layer`, which refuses a Runtime that is not
RUNNING, and the resident participant refuses anything that is not a real
`Execution` of a RUNNING Runtime. A step can neither run outside a Runtime nor
be traced as if it had.

**Identity (`§6`).** The participant is built with the grant's
`recipient_instance` as its actor: the Agent Instance the delegation names,
never the definition key or a capability name. FR-2 found `EngineeringIntelligenceAgent.participate` tracing its
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
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.execution import create_execution_layer
from native_core.core.trace import TraceWriter

from tools import p12_runtime_observation as observation
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.p12_certified_evidence_guard import guard
from tools.p12_execution_provenance import (
    LIVE_MANIFEST_ROOT, ExecutionManifest, record)
from tools.p12_governance_escalation_join import join_refusals_to_grants
from tools.p12_trace_registry import LIVE_STORE_ROOT
from tools.planning import AuthorityProvenance, Plan, PlanStep, sequence
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


#: Builds the participant for one step: ``(run_step, instance_key, perform,
#: writer, agent_definition_version) -> Agent``. ``run_step(action)`` re-checks
#: the delegation and calls ``action(step)``; the participant decides nothing
#: about authority.
Participant = Callable[..., Agent]


class RuntimeHostedExecutor:
    """Executes a delegation's plan steps, each inside a Runtime Execution.

    Same contract as `W4Executor` (it delegates to one), with one difference:
    every step is a participation in a fresh `Execution` of ``runtime``, and is
    traced under the grant's recipient instance.
    """

    def __init__(self, delegation: W4Delegation, registry: AgentInstanceRegistry,
                 runtime, writer: TraceWriter, *, participant: Participant,
                 trace_store: str = AGENCY_TRACE_STORE,
                 store_path: Optional[Path] = None) -> None:
        self._executor = W4Executor(delegation, registry)
        self._participant = participant
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
        participant = self._participant(
            lambda action: self._executor.execute_step(step, action),
            self._delegation.recipient_instance, perform, self._writer,
            registration.instance.agent_definition.agent_definition_version)
        if not isinstance(participant, Agent):
            raise TypeError("a delegated step is taken by an Agent, which enters the "
                            "Runtime only through participate(execution)")
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


def run_hosted_plan(delegation: W4Delegation, registry: AgentInstanceRegistry, runtime,
                    writer: TraceWriter, plan: Plan, perform: Callable[[PlanStep], str], *,
                    participant: Participant, root: Optional[Path], authority_record: str,
                    store_path: Optional[Path] = None
                    ) -> Tuple[ExecutionReport, Tuple[HostedStep, ...], Tuple[str, ...]]:
    """The hosted **run path**: a plan executed inside the Runtime, its
    refusals made organizational escalations.

    `RuntimeHostedExecutor`, like `W4Executor`, keeps no handle on persistence.
    The run path is where refusals reach organizational state, through the one
    existing wiring (`join_refusals_to_grants`, `ACT-CC-P12-005`), exactly as
    `tools/w4_first_run.py` and the `tools/w1_*_run.py` paths do. Every refusal
    here was raised under the one delegation the plan executes under. With
    ``root`` None nothing is recorded, matching that wiring's own convention.
    """
    executor = RuntimeHostedExecutor(delegation, registry, runtime, writer,
                                     participant=participant, store_path=store_path)
    report, hosted = executor.execute_plan(plan, perform)
    escalations = join_refusals_to_grants(
        root, report.refusals,
        subject=f"plan {plan.key} / delegation {delegation.delegation_id}",
        authority=AuthorityProvenance("FD-P11-001 §9", authority_record),
        delegation_for=lambda refusal: delegation.delegation_id)
    return report, hosted, tuple(escalations)


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
