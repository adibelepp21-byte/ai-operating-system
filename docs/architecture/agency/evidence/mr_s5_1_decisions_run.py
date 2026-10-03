"""MR-S5-1 representative execution: ACCEPT, REWORK and REJECT, each recorded with
explicit decision provenance.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-MR-S5-1-DECISION-PROVENANCE.md (`§19`).
Each Founder Goal is a verbatim, registered line of the directive:

* P1 ACCEPT — *"Use an existing valid Agent → Result → Verification path."*
  ``tools/w4_delegation.py`` carries the fourteen `FD-P11-001 §13` elements;
  the CEO verifies and accepts.
* P2 REWORK — *"Use a genuine verification failure."* ``tools/w4_continuity.py``
  does not carry the fourteen. The CEO sends the work back as one new delegated
  step (the rework target), which is then performed and accepted.
* P3 REJECT — *"Use a bounded operational refusal that does not require Founder
  authority."* ``tools/w4_execution.py`` does not carry the fourteen either;
  the CEO refuses the path — an execution module is not where the delegation
  record lives — and the plan proceeds with different work, which is performed
  and accepted. The rejected check is not redone.

The work continues in the S-4 operational root, where the existing
``engineering-intelligence-instance-001`` is already registered on disk; it is
registered here **in memory only**, so no instance record is written or
rewritten (MR-S5-1 `§24`: the Agent registry is unchanged). The S-4 goals on the
planning surface are restored and saved unchanged. Writes only grants, evidence,
the plan state and the live ledger, outside every certified root; refuses to
run twice.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from tools import authority_citation as ac  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402
from tools.planning import AuthorityProvenance, Goal, Plan, PlanStep  # noqa: E402
from tools.w4_execution import ExecutionReport, W4Executor, persist_evidence  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"
ACT_ID = "DIR-AIOS-AGENCY-MR-S5-1-DECISION-PROVENANCE"
ACT = f"docs/governance/acts/{ACT_ID}.md"
INSTANCE = "engineering-intelligence-instance-001"
CEO = AuthorityProvenance(
    "Co-Founder V2 A01 Executive Command",
    "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
CRITERIA = tuple(ConformanceCriterion(name=n, required_text=n) for n in w4.REQUIRED_ELEMENTS)
GOALS = {
    "P1": ("founder-mr-s5-1-accept", "Use an existing valid Agent → Result → Verification path."),
    "P2": ("founder-mr-s5-1-rework", "Use a genuine verification failure."),
    "P3": ("founder-mr-s5-1-reject",
           "Use a bounded operational refusal that does not require Founder authority."),
}


def establish(key, subject):
    return PlanStep(key, f"Establish that {subject} carries all fourteen FD-P11-001 §13 "
                         "delegation elements, reporting each criterion satisfied or not.",
                    requires_delegation=True)


def review(*deps):
    return PlanStep("ceo-review-verification",
                    "Review the verification evidence and record the operational decision "
                    "(Co-Founder / CEO, V2 A09 / A11; not Founder acceptance).",
                    depends_on=tuple(deps))


SUBJECT = {"verify-delegation-elements": "tools/w4_delegation.py",
           "verify-continuity-elements": "tools/w4_continuity.py",
           "report-continuity-elements": "tools/w4_continuity.py",
           "verify-execution-elements": "tools/w4_execution.py",
           "verify-delegation-record-elements": "tools/w4_delegation.py"}
REPORT_ONLY = {"report-continuity-elements"}


def main() -> int:
    if is_protected(ROOT):
        sys.exit(f"refusing: {ROOT} is certified evidence")
    surface = planning_continuity.restore(ROOT / "planning.state.json")
    if any(g in surface._goals for g, _ in GOALS.values()):  # noqa: SLF001
        sys.exit("refusing: the MR-S5-1 goals are already on this surface; it runs once")
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
    agent = EngineeringIntelligenceAgent()
    log = []

    def run(goal_key, step_key):
        """Delegate one step of the goal's current plan, execute it, persist evidence."""
        plan = surface.current(goal_key)
        subject = SUBJECT[step_key]
        grant = w4.issue_from_plan(
            delegations, surface, plan, step_key, delegator=w4.AUTHORIZED_DELEGATOR,
            recipient_instance=INSTANCE, authority=FD9,
            capability_scope=("engineering-intelligence",),
            resource_boundary=f"read-only access to {subject}; nothing written but the evidence",
            output_expectation="one conformance result per FD-P11-001 §13 element",
            verification_requirement=("each element reported" if step_key in REPORT_ONLY
                                      else "all fourteen elements reported, each satisfied"),
            escalation_condition="any step outside the delegated work scope, a revoked "
                                 "delegation, or a retired instance")
        findings = {}
        artifact = Artifact(name=subject, lines=tuple(
            (REPO / subject).read_text(encoding="utf-8").split("\n")))

        def perform(step):
            findings.update({r.criterion_name: r.satisfied
                             for r in agent.verify(artifact, CRITERIA)})
            carried = sum(findings.values())
            if step_key in REPORT_ONLY:
                return f"{carried} of {len(findings)} elements carried (reported)"
            missing = sorted(k for k, ok in findings.items() if not ok)
            if missing:
                raise AssertionError(f"{carried} of {len(findings)} elements carried; "
                                     f"not carried: {missing}")
            return f"{carried} of {len(findings)} elements carried"

        report = ExecutionReport(outcomes=[W4Executor(grant, registry).execute_step(
            plan.step(step_key), perform)])
        persist_evidence(ROOT, plan.key, grant, report, subject=subject, criteria=findings,
                         performed_by="consumers/engineering_intelligence_agent.py "
                                      "EngineeringIntelligenceAgent.verify")
        log.append({"goal": goal_key, "plan": plan.key, "step": step_key,
                    "grant": grant.delegation_id, "result": report.outcomes[0].status,
                    "detail": report.outcomes[0].detail})
        return grant

    def decide(goal_key, grant, decision, reason, **kw):
        result = w4.review_result(ROOT, grant.delegation_id, surface=surface, decision=decision,
                                  reviewer=w4.AUTHORIZED_DELEGATOR, reason=reason, **kw)
        log.append({"goal": goal_key, "grant": grant.delegation_id,
                    **{k: result[k] for k in ("decision", "verification", "resulting_plan",
                                              "rework_target")}})

    for key, (goal_key, statement) in GOALS.items():
        refused = ac.founder_goal_refusal(ACT_ID, ACT, statement)
        if refused:
            sys.exit(f"refusing: not a Founder Goal: {refused}")
        surface.declare(Goal(key=goal_key, statement=statement,
                             authority=AuthorityProvenance(ACT_ID, ACT)))

    # P1 — ACCEPT
    g = GOALS["P1"][0]
    surface.adopt(Plan(key=f"{g}-plan-0", goal_key=g, authority=CEO, steps=(
        establish("verify-delegation-elements", "tools/w4_delegation.py"),
        review("verify-delegation-elements"))))
    decide(g, run(g, "verify-delegation-elements"), w4.ACCEPT,
           "the evidence shows all fourteen elements carried")

    # P2 — REWORK, then the rework performed and accepted
    g = GOALS["P2"][0]
    surface.adopt(Plan(key=f"{g}-plan-0", goal_key=g, authority=CEO, steps=(
        establish("verify-continuity-elements", "tools/w4_continuity.py"),
        review("verify-continuity-elements"))))
    failed = run(g, "verify-continuity-elements")
    decide(g, failed, w4.REWORK,
           "the result is a genuine finding: the continuity module does not carry the "
           "fourteen. The work is redone as a report of which elements it carries",
           rework_target="report-continuity-elements",
           rework_steps=(PlanStep("report-continuity-elements",
                                  "Report which of the fourteen FD-P11-001 §13 delegation "
                                  "elements tools/w4_continuity.py carries, each satisfied "
                                  "or not.", requires_delegation=True),
                         review("report-continuity-elements")))
    decide(g, run(g, "report-continuity-elements"), w4.ACCEPT,
           "the report covers all fourteen elements, each satisfied or not")

    # P3 — REJECT, and the different path performed and accepted
    g = GOALS["P3"][0]
    surface.adopt(Plan(key=f"{g}-plan-0", goal_key=g, authority=CEO, steps=(
        establish("verify-execution-elements", "tools/w4_execution.py"),
        review("verify-execution-elements"))))
    refused_path = run(g, "verify-execution-elements")
    decide(g, refused_path, w4.REJECT,
           "an execution module does not hold the delegation record, so this check's "
           "premise is wrong; it is not redone. The plan proceeds with the check of the "
           "module that holds the record",
           resulting_steps=(establish("verify-delegation-record-elements",
                                      "tools/w4_delegation.py"),
                            review("verify-delegation-record-elements")))
    decide(g, run(g, "verify-delegation-record-elements"), w4.ACCEPT,
           "the evidence shows all fourteen elements carried")

    planning_continuity.save(surface, ROOT / "planning.state.json")
    outcomes = {k: w4.plan_outcome(surface, v[0], ROOT) for k, v in GOALS.items()}
    (ROOT / "mr-s5-1-run.result.json").write_text(json.dumps(
        {"executed_at": datetime.now(timezone.utc).isoformat(), "log": log,
         "plan_outcomes": outcomes}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for entry in log:
        print(json.dumps(entry, ensure_ascii=False))
    print({k: (v["completed"], v["current_plan"], v["decision_faults"]) for k, v in outcomes.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
