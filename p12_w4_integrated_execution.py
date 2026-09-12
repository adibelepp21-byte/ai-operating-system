"""P12-W4 — one real execution that keeps the whole canonical contract.

`ACT-CC-P12-W4-001 §16` forbids proving W4 through unit tests, mocks, synthetic
graphs, static inspection, fabricated rows, or demonstration-only scripts. At
least one real path must be exercised where the integration relationship
genuinely occurs. This is that path.

It runs the chain `§28` names, in order, with each stage producing the artifact
the next stage refers to:

```text
INTENT        a declared Goal
DECISION      an adopted Plan carrying its authority citation
WORK          the work scope the plan needs delegating
DELEGATION    a real grant issued by the delegator FD-P11-001 §4.1 names
EXECUTION     real conformance work, written through TraceWriter to durable storage
OBSERVATION   a runtime observation published under the same runtime identity
VERIFICATION  the conformance outcome, recorded against the requirement
EVIDENCE      one execution provenance manifest joining all of the above
```

**Nothing here is fabricated.** The work performed is the same artifact
conformance verification the resident W4 path performs — real reading of a real
file against real criteria — and its result is whatever it turns out to be. The
manifest records the outcome; it does not choose it.

**The observation subject is the runtime identity of the execution**, which is
what makes `EXECUTION → OBSERVATION` a join rather than two records that happen
to exist. The resident trace stores and the resident observations share no name
at all, which is the asymmetry W6 found; this run is written so that they do.

Verification is **not** performed here. `§24` requires the verdict to come from
a reader that did not write the records, so this script persists and stops, and
`tools/p12_execution_chain_reader` is what decides whether the chain holds.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from native_core.core.infrastructure import LocalAppendOnlyStorage  # noqa: E402
from native_core.core.trace import TraceWriter  # noqa: E402
from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from consumers.observation import TracedAction  # noqa: E402

from tools.agent_instance_registry import (  # noqa: E402
    AgentDefinition, AgentInstanceRegistry)
from tools.planning import AuthorityProvenance  # noqa: E402
from tools.planning.goal import Goal  # noqa: E402
from tools.planning.plan import Plan, PlanStep  # noqa: E402
from tools.planning.surface import PlanningSurface  # noqa: E402
from tools.w4_delegation import (  # noqa: E402
    AUTHORIZED_DELEGATOR, W4DelegationRegistry)
from tools.w4_delegation import REQUIRED_ELEMENTS  # noqa: E402
from tools import p12_runtime_observation as observation  # noqa: E402
from tools.p12_execution_provenance import (  # noqa: E402
    ExecutionManifest, record)
from tools.p12_trace_registry import STORE_ROOT  # noqa: E402

FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
DP01_RECORD = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

#: Two runs, deliberately. `ACT-CC-P12-W4-001 §26`: *"W4 must not assume only
#: successful execution."* A chain that has only ever carried a success has not
#: shown it can carry anything else, and a terminal state nothing has ever
#: reached is not a state the system distinguishes.
#:
#: The second subject is chosen because the work genuinely fails against it —
#: `p12_execution_provenance.py` does not contain the `FD-P11-001 §13`
#: delegation element names — not because a failure was injected. The criteria
#: are identical in both runs. Only the artifact differs, and the outcome is
#: whatever the real verification produces.
RUNS = {
    "001": {
        "subject": REPO_ROOT / "tools" / "w4_delegation.py",
        "store": "p12-w4-integrated-execution",
        "runtime": "p12-w4-integrated-execution-runtime",
        "goal": "p12-w4-integrated-execution",
        "plan": "p12-w4-integrated-execution-plan-0",
    },
    "002": {
        "subject": REPO_ROOT / "tools" / "p12_execution_provenance.py",
        "store": "p12-w4-integrated-execution-failure",
        "runtime": "p12-w4-integrated-execution-failure-runtime",
        "goal": "p12-w4-integrated-execution-failure",
        "plan": "p12-w4-integrated-execution-failure-plan-0",
    },
}

INSTANCE_KEY = "engineering-intelligence-instance-001"

DELEGATION_ROOT = REPO_ROOT / "docs/architecture/p12/w4-operations"

DEFINITION = AgentDefinition(
    agent_definition_key="engineering-intelligence-agent",
    agent_definition_version="1.0",
    owning_department_key="engineering",
    implemented_capabilities=("engineering-intelligence",),
    specified_skills=(), specified_workflows=())

WORK_SCOPE = ("verify-delegation-elements",)


def run(run_key: str = "001", *, persist: bool = True) -> dict:
    """Execute the chain once. Returns what was produced, not a verdict."""
    config = RUNS[run_key]
    SUBJECT = config["subject"]
    STORE_NAME = config["store"]
    RUNTIME_ID = config["runtime"]
    GOAL_KEY = config["goal"]
    PLAN_KEY = config["plan"]
    EXECUTION_ID = f"p12-w4-integrated-execution-{run_key}"
    # ── INTENT ────────────────────────────────────────────────────────────
    surface = PlanningSurface()
    plan_authority = AuthorityProvenance("DP-01 §3 W2", DP01_RECORD)
    surface.declare(Goal(
        GOAL_KEY,
        "Establish that one execution can preserve the whole §29 contract.",
        plan_authority))

    # ── DECISION ──────────────────────────────────────────────────────────
    plan = surface.adopt(Plan(
        key=PLAN_KEY, goal_key=GOAL_KEY, authority=plan_authority,
        steps=(PlanStep("verify-delegation-elements",
                        "Verify tools/w4_delegation.py against the "
                        "FD-P11-001 §13 conformance criteria.",
                        requires_delegation=True),)))

    # ── WORK → DELEGATION ─────────────────────────────────────────────────
    delegation_root = DELEGATION_ROOT if persist else None
    registry = AgentInstanceRegistry(root=None)
    registration = registry.register(
        instance_key=INSTANCE_KEY, definition=DEFINITION,
        permitted_capabilities=("engineering-intelligence",),
        created_by=AUTHORIZED_DELEGATOR,
        authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
        accountable_to=AUTHORIZED_DELEGATOR)
    delegations = W4DelegationRegistry(registry, delegation_root)
    delegation = delegations.issue(
        delegator=AUTHORIZED_DELEGATOR,
        recipient_instance=registration.instance_key,
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
        objective="Verify tools/w4_delegation.py against the FD-P11-001 §13 "
                  "conformance criteria under an observable runtime.",
        capability_scope=("engineering-intelligence",),
        work_scope=WORK_SCOPE,
        lifecycle_boundary=f"one execution of plan {PLAN_KEY}",
        resource_boundary="read-only access to tools/w4_delegation.py",
        output_expectation="one conformance result per criterion",
        verification_requirement="every criterion reported satisfied or not, "
                                 "and the outcome carrying a ratified status",
        escalation_condition="any step outside the delegated work scope",
        accountable_party=AUTHORIZED_DELEGATOR,
        termination_condition=f"on completion of plan {PLAN_KEY}")

    # ── EXECUTION, under OBSERVATION ──────────────────────────────────────
    store = LocalAppendOnlyStorage(STORE_ROOT / STORE_NAME)
    store.provision()
    writer = TraceWriter(store)
    agent = EngineeringIntelligenceAgent(trace_writer=writer)

    observation_root = (observation.OBSERVATION_ROOT if persist
                        else Path("/dev/null"))
    if persist:
        observation.publish(RUNTIME_ID, "RuntimeState.RUNNING",
                            root=observation_root, kind="RUNTIME")

    lines = tuple(SUBJECT.read_text(encoding="utf-8").split("\n"))
    criteria = tuple(ConformanceCriterion(name=name, required_text=name)
                     for name in REQUIRED_ELEMENTS)

    with TracedAction(writer, agent_instance=INSTANCE_KEY, runtime=RUNTIME_ID,
                      agent_definition_version="1.1") as action:
        results = agent.verify(Artifact(name=SUBJECT.name, lines=lines),
                               criteria)
        satisfied = tuple(r.criterion_name for r in results if r.satisfied)
        unsatisfied = tuple(r.criterion_name for r in results
                            if not r.satisfied)
        action.used_skill("artifact-conformance-verification")
        action.used_tool("tools/w4_delegation.py")
        outcome = {"criteria": len(criteria), "satisfied": len(satisfied),
                   "unsatisfied": list(unsatisfied)}
        action.produced(outcome)
        if unsatisfied:
            action.failed(f"{len(unsatisfied)} criteria unsatisfied")

    if persist:
        observation.publish(RUNTIME_ID, "RuntimeState.STOPPED",
                            root=observation_root, kind="RUNTIME")

    # ── EVIDENCE ──────────────────────────────────────────────────────────
    ordinal = _trace_ordinal(STORE_ROOT / STORE_NAME)
    manifest = ExecutionManifest(
        execution_id=EXECUTION_ID,
        goal=GOAL_KEY,
        plan=plan.key,
        plan_authority=f"{plan_authority.instrument} ({plan_authority.record})",
        work_scope=WORK_SCOPE,
        agent_instance=INSTANCE_KEY,
        agent_definition_version="1.1",
        delegation_id=delegation.delegation_id,
        delegator=delegation.delegator,
        authority_instrument=delegation.authority.instrument,
        authority_record=delegation.authority.record,
        authority_chain=delegation.authority_chain(),
        capability_scope=delegation.capability_scope,
        trace_store=STORE_NAME,
        trace_ordinal=ordinal,
        runtime_id=RUNTIME_ID,
        status="failure" if unsatisfied else "success",
        observation_subject=RUNTIME_ID,
        observation_kind="runtime",
        verification_requirement=delegation.verification_requirement,
        outcome=outcome,
        delegation_status=delegation.status)

    written = record(manifest) if persist else None
    return {
        "execution_id": EXECUTION_ID,
        "delegation_id": delegation.delegation_id,
        "trace_store": STORE_NAME,
        "trace_ordinal": ordinal,
        "runtime_id": RUNTIME_ID,
        "outcome": outcome,
        "manifest": str(written) if written else None,
    }


def _trace_ordinal(store_path: Path) -> int:
    """Index of the record this run appended. Counted from what is on disk."""
    lines = 0
    for path in sorted(store_path.rglob("*")):
        if path.is_file():
            lines += len([ln for ln in
                          path.read_text(encoding="utf-8").splitlines()
                          if ln.strip()])
    return max(lines - 1, 0)


def main() -> int:
    run_key = sys.argv[1] if len(sys.argv) > 1 else "001"
    result = run(run_key, persist=True)
    for key, value in result.items():
        print(f"{key:<16} {value}")
    print()
    print("Persisted. The verdict is not this script's to give —")
    print("run `python3 -m tools.p12_execution_chain_reader`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
