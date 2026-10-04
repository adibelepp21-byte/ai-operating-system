"""FR-2 construction (FD-FR2-001): one delegated Agency execution, through the Runtime.

`FD-FR2-001 §12` requires fresh-process verification that Agency work actually
enters the Runtime and is traced, manifested and reconstructable from the
Founder Goal to the Plan Outcome. That needs one real execution on the
authorized path. This is it, and it is shaped like the resident Agency runs
(S-4, MR-S5-1), with one difference: the delegated step runs inside a Runtime
Execution (`tools/w4_runtime_execution.py`), not as a plain call.

* **Founder Goal** — a verbatim line of `FD-FR2-001 §2`: *"The existing
  provenance model must be used rather than replaced."* Refused unless the
  citation reaches the registered Founder content.
* **Plan** — adopted by the CEO: one delegated step, then the CEO review.
* **Delegation** — issued from the plan by the authorized delegator, under the
  existing `FD-P11-001 §9` authority, to the already-registered
  `engineering-intelligence-instance-001`. No new authority, capability, Agent
  or instance: the instance is registered in memory only, and its record on disk
  is not written (as in MR-S5-1).
* **Work** — real: `EngineeringIntelligenceAgent.verify` checks that the
  integration module uses the existing mechanisms the Goal names, one criterion
  per mechanism. The result is whatever the module carries.
* **Runtime / Trace / Manifest** — a real Runtime, started and observed under
  ``agency-runtime-<grant>``; one Trace record under the recipient instance in
  the live store; one `ExecutionManifest` in the live root.
* **Evidence / Verification / Decision / Plan Outcome** — the resident W4
  writers and readers: `persist_evidence` (with the runtime facts as details),
  `review_result` (CEO decision, `FD-AGENCY-001` Q4-A), `plan_outcome`.

Writes only the grant, the evidence, the plan state, the live ledger, and the
live Runtime / Trace / manifest roots, all outside every certified root.
Refuses to run twice. Imports nothing from P12-W2 or P13.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

import tools  # noqa: E402,F401  -- installs the certified-write barrier before anything runs
from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from tools import authority_citation as ac  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools import w4_runtime_execution as rx  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402
from tools.p12_trace_registry import LIVE_STORE_ROOT  # noqa: E402
from tools.planning import AuthorityProvenance, Goal, Plan, PlanStep  # noqa: E402
from tools.w4_execution import ExecutionReport, persist_evidence  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"
ACT_ID = "FD-FR2-001-AGENCY-RUNTIME-TRACE-INTEGRATION-AUTHORIZATION"
ACT = f"docs/governance/acts/{ACT_ID}.md"
INSTANCE = "engineering-intelligence-instance-001"
CEO = AuthorityProvenance(
    "Co-Founder V2 A01 Executive Command",
    "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
GOAL_KEY = "founder-fr2-runtime-trace"
STATEMENT = "The existing provenance model must be used rather than replaced."
STEP = "verify-runtime-path-mechanisms"
SUBJECT = "tools/w4_runtime_execution.py"
#: One criterion per existing mechanism `FD-FR2-001 §3` / `§7` names, each the
#: line that shows the module using it rather than replacing it.
CRITERIA = tuple(ConformanceCriterion(name=name, required_text=text) for name, text in (
    ("agent-enters-through-the-execution-contract", "class DelegatedStep(Agent):"),
    ("execution-layer-issues-each-step", "execution = create_execution_layer(self._runtime)"),
    ("runtime-built-by-the-composition-root", "runtime = create_runtime(runtime_id"),
    ("w4-executor-re-checks-the-grant", "self._executor = W4Executor(delegation, registry)"),
    ("trace-written-by-traced-action-under-the-instance",
     "with TracedAction(self._writer, agent_instance=self._instance_key,"),
    ("runtime-observation-published", "observation.publish(runtime_id, str(runtime.state),"),
    ("existing-execution-manifest", "manifest = ExecutionManifest("),
    ("manifest-written-by-the-existing-writer", "return record(manifest, root=root)"),
))


def main() -> int:
    if is_protected(ROOT) or is_protected(LIVE_STORE_ROOT) or is_protected(rx.LIVE_MANIFEST_ROOT):
        sys.exit("refusing: a target root is certified evidence")
    refused = ac.founder_goal_refusal(ACT_ID, ACT, STATEMENT)
    if refused:
        sys.exit(f"refusing: not a Founder Goal: {refused}")
    surface = planning_continuity.restore(ROOT / "planning.state.json")
    if GOAL_KEY in surface._goals:  # noqa: SLF001
        sys.exit("refusing: the FR-2 goal is already on this surface; it runs once")
    on_disk = json.loads((ROOT / f"{INSTANCE}.instance.json").read_text(encoding="utf-8"))
    if on_disk.get("lifecycle") != "REGISTERED" or \
            on_disk.get("definition_key") != SELECTED_DEFINITION.agent_definition_key:
        sys.exit(f"refusing: {INSTANCE} is not a registered instance of this root")
    registry = AgentInstanceRegistry(None)        # in memory: the record on disk stands
    registry.register(instance_key=INSTANCE, definition=SELECTED_DEFINITION,
                      permitted_capabilities=("engineering-intelligence",),
                      created_by=w4.AUTHORIZED_DELEGATOR,
                      authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                      accountable_to=w4.AUTHORIZED_DELEGATOR)
    delegations = w4.W4DelegationRegistry(registry, ROOT)

    # FOUNDER GOAL → PLAN
    surface.declare(Goal(key=GOAL_KEY, statement=STATEMENT,
                         authority=AuthorityProvenance(ACT_ID, ACT)))
    plan = surface.adopt(Plan(key=f"{GOAL_KEY}-plan-0", goal_key=GOAL_KEY, authority=CEO, steps=(
        PlanStep(STEP, f"Establish that {SUBJECT} routes delegated work through the existing "
                       "Execution Contract, Execution Layer, Runtime, runtime observation, "
                       "TracedAction and ExecutionManifest, reporting each mechanism "
                       "satisfied or not.", requires_delegation=True),
        PlanStep("ceo-review-verification",
                 "Review the verification evidence and record the operational decision "
                 "(Co-Founder / CEO, V2 A09 / A11; not Founder acceptance).",
                 depends_on=(STEP,)))))

    # PLAN STEP → DELEGATION → AGENT INSTANCE
    grant = w4.issue_from_plan(
        delegations, surface, plan, STEP, delegator=w4.AUTHORIZED_DELEGATOR,
        recipient_instance=INSTANCE, authority=FD9,
        capability_scope=("engineering-intelligence",),
        resource_boundary=f"read-only access to {SUBJECT}; nothing written but the evidence",
        output_expectation="one conformance result per named mechanism",
        verification_requirement="every named mechanism reported, each satisfied",
        escalation_condition="any step outside the delegated work scope, a revoked "
                             "delegation, or a retired instance")

    # EXECUTION → RUNTIME → TRACE
    agent = EngineeringIntelligenceAgent()
    artifact = Artifact(name=SUBJECT, lines=tuple(
        (REPO / SUBJECT).read_text(encoding="utf-8").split("\n")))
    findings = {}

    def perform(step):
        findings.update({r.criterion_name: r.satisfied for r in agent.verify(artifact, CRITERIA)})
        carried = sum(findings.values())
        missing = sorted(k for k, ok in findings.items() if not ok)
        if missing:
            raise AssertionError(f"{carried} of {len(findings)} mechanisms used; "
                                 f"not used: {missing}")
        return f"{carried} of {len(findings)} mechanisms used"

    runtime_id = f"agency-runtime-{grant.delegation_id}"
    store = LIVE_STORE_ROOT / rx.AGENCY_TRACE_STORE
    with rx.hosted_runtime(runtime_id) as runtime:
        executor = rx.RuntimeHostedExecutor(grant, registry, runtime, rx.trace_writer(store))
        hosted = executor.execute_step(plan.step(STEP), perform)

    # MANIFEST → RESULT → EVIDENCE
    unsatisfied = sorted(k for k, ok in findings.items() if not ok)
    manifest = rx.record_manifest(
        hosted, grant, goal=GOAL_KEY, plan=plan.key,
        plan_authority=f"{CEO.instrument} ({CEO.record})",
        agent_definition_version=SELECTED_DEFINITION.agent_definition_version,
        outcome={"step": STEP, "status": hosted.outcome.status,
                 "detail": hosted.outcome.detail, "criteria": len(findings),
                 "satisfied": len(findings) - len(unsatisfied), "unsatisfied": unsatisfied})
    evidence = persist_evidence(
        ROOT, plan.key, grant, ExecutionReport(outcomes=[hosted.outcome]),
        subject=SUBJECT, criteria=findings,
        performed_by="consumers/engineering_intelligence_agent.py "
                     "EngineeringIntelligenceAgent.verify, hosted by "
                     "tools/w4_runtime_execution.py DelegatedStep",
        runtime=dict(hosted.runtime_details(),
                     execution_manifest=str(manifest.relative_to(REPO))))

    # VERIFICATION → CEO DECISION → PLAN OUTCOME
    log = {"goal": GOAL_KEY, "plan": plan.key, "step": STEP, "grant": grant.delegation_id,
           "result": hosted.outcome.status, "detail": hosted.outcome.detail,
           "runtime": hosted.runtime_details(), "manifest": str(manifest.relative_to(REPO)),
           "evidence": str(evidence.relative_to(REPO))}
    if hosted.outcome.status == "success":
        decision = w4.review_result(
            ROOT, grant.delegation_id, surface=surface, decision=w4.ACCEPT,
            reviewer=w4.AUTHORIZED_DELEGATOR,
            reason="the evidence shows every named existing mechanism used, and the "
                   "execution ran inside a Runtime Execution with its Trace and manifest")
        log["decision"] = {k: decision[k] for k in ("decision", "verification", "resulting_plan")}
    else:
        log["decision"] = None                    # left for the CEO; nothing is decided here
    planning_continuity.save(surface, ROOT / "planning.state.json")
    outcome = w4.plan_outcome(surface, GOAL_KEY, ROOT)
    (ROOT / "fr2-runtime-run.result.json").write_text(json.dumps(
        {"executed_at": datetime.now(timezone.utc).isoformat(), "log": log,
         "plan_outcome": outcome}, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8")
    print(json.dumps(log, indent=1, ensure_ascii=False, default=str))
    print({"completed": outcome["completed"], "current_plan": outcome["current_plan"],
           "decision_faults": outcome["decision_faults"]})
    return 0 if hosted.outcome.status == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
