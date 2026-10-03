"""S-4 representative execution: Founder Goal → plan → delegation → agent → result →
verification evidence → CEO decision → plan outcome.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-S4-AGENT-EVIDENCE-TO-PLAN-OUTCOME.md.

Two Founder Goals, each a verbatim, registered line of the directive:

* ACCEPT — *"Prove Agent → Verification Evidence → CEO Review/Decision → Plan
  Outcome integration"*: the agent establishes that ``tools/w4_delegation.py``
  carries the fourteen `FD-P11-001 §13` delegation elements; the CEO verifies
  the evidence (the resident `plan_completion` rule **and** an independent
  re-derivation of each criterion) and accepts.
* REWORK — *"Construct a controlled verification failure or insufficient-evidence
  case."*: the same check of ``tools/w4_continuity.py``, a continuity module
  that does not carry the fourteen. The failure is real, not injected; the CEO
  cannot accept it and sends the work back by revising the plan.

The insufficient-evidence case (accepting before any evidence exists) is
attempted first and must be refused; nothing is written by the attempt.

The agent is the existing ``engineering-intelligence-instance-001`` of the
existing definition, performed by the resident consumer. No candidate, no new
capability, no Founder acceptance. Writes only to a non-certified operational
root and the live ledger; refuses to run twice.
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
from tools.planning import AuthorityProvenance, Goal, Plan, PlanningSurface, PlanStep  # noqa: E402
from tools.w4_execution import ExecutionReport, W4Executor, persist_evidence  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"
S4_ID = "DIR-AIOS-AGENCY-S4-AGENT-EVIDENCE-TO-PLAN-OUTCOME"
S4_RECORD = f"docs/governance/acts/{S4_ID}.md"
INSTANCE = "engineering-intelligence-instance-001"
CEO = AuthorityProvenance(
    "Co-Founder V2 A01 Executive Command",
    "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)

GOALS = {
    "accept": ("founder-s4-accept",
               "Prove Agent → Verification Evidence → CEO Review/Decision → Plan Outcome integration",
               "tools/w4_delegation.py", "verify-delegation-elements"),
    "rework": ("founder-s4-rework",
               "Construct a controlled verification failure or insufficient-evidence case.",
               "tools/w4_continuity.py", "verify-continuity-elements"),
}
CRITERIA = tuple(ConformanceCriterion(name=n, required_text=n) for n in w4.REQUIRED_ELEMENTS)


def step_statement(subject):
    return (f"Establish that {subject} carries all fourteen FD-P11-001 §13 delegation "
            "elements, reporting each criterion satisfied or not.")


def ceo_review(step):
    return PlanStep("ceo-review-verification",
                    "Review the verification evidence and record the operational decision "
                    "(Co-Founder / CEO, V2 A09 / A11; not Founder acceptance).",
                    depends_on=(step,))


def independent_check(subject):
    """The CEO's own re-derivation: each criterion's text searched in the file."""
    text = (REPO / subject).read_text(encoding="utf-8")
    return {c.name: c.required_text in text for c in CRITERIA}


def main() -> int:
    if is_protected(ROOT):
        sys.exit(f"refusing: {ROOT} is certified evidence")
    if ROOT.is_dir() and any(ROOT.glob("*.delegation.json")):
        sys.exit("refusing: this root already holds grants; S-4 runs once")

    surface = PlanningSurface()
    registry = AgentInstanceRegistry(ROOT)
    registry.register(instance_key=INSTANCE, definition=SELECTED_DEFINITION,
                      permitted_capabilities=("engineering-intelligence",),
                      created_by=w4.AUTHORIZED_DELEGATOR,
                      authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                      accountable_to=w4.AUTHORIZED_DELEGATOR)
    delegations = w4.W4DelegationRegistry(registry, ROOT)
    agent = EngineeringIntelligenceAgent()
    run = {"executed_at": datetime.now(timezone.utc).isoformat(), "paths": {}}

    for path, (goal_key, statement, subject, step_key) in GOALS.items():
        refused = ac.founder_goal_refusal(S4_ID, S4_RECORD, statement)
        if refused:
            sys.exit(f"refusing: not a Founder Goal: {refused}")
        surface.declare(Goal(key=goal_key, statement=statement,
                             authority=AuthorityProvenance(S4_ID, S4_RECORD)))
        plan = surface.adopt(Plan(key=f"{goal_key}-plan-0", goal_key=goal_key, authority=CEO,
                                  steps=(PlanStep(step_key, step_statement(subject),
                                                  requires_delegation=True),
                                         ceo_review(step_key))))
        grant = w4.issue_from_plan(
            delegations, surface, plan, step_key, delegator=w4.AUTHORIZED_DELEGATOR,
            recipient_instance=INSTANCE, authority=FD9,
            capability_scope=("engineering-intelligence",),
            resource_boundary=f"read-only access to {subject}; no network; nothing written "
                              "but the evidence record",
            output_expectation="one conformance result per FD-P11-001 §13 element",
            verification_requirement="all fourteen elements reported, each satisfied",
            escalation_condition="any step outside the delegated work scope, a revoked "
                                 "delegation, or a retired instance")
        entry = {"goal": goal_key, "statement": statement, "plan": plan.key,
                 "grant": grant.delegation_id, "subject": subject}

        # Insufficient evidence: no result exists yet. ACCEPT must be refused.
        try:
            w4.review_result(ROOT, grant.delegation_id, surface=surface, decision=w4.ACCEPT,
                             reviewer=w4.AUTHORIZED_DELEGATOR, reason="premature")
            entry["accept_without_evidence"] = "NOT REFUSED"
        except w4.DelegationError as exc:
            entry["accept_without_evidence"] = f"refused: {exc}"

        # The agent's work, through the executor, under the grant.
        findings = {}
        artifact = Artifact(name=subject, lines=tuple(
            (REPO / subject).read_text(encoding="utf-8").split("\n")))

        def perform(step, artifact=artifact, findings=findings):
            results = agent.verify(artifact, CRITERIA)
            findings.update({r.criterion_name: r.satisfied for r in results})
            missing = sorted(k for k, ok in findings.items() if not ok)
            if missing:
                raise AssertionError(f"{len(findings) - len(missing)} of {len(findings)} "
                                     f"elements carried; not carried: {missing}")
            return f"{len(findings)} of {len(findings)} elements carried"

        report = ExecutionReport(outcomes=[W4Executor(grant, registry).execute_step(
            plan.step(step_key), perform)])
        evidence = persist_evidence(ROOT, plan.key, grant, report, subject=subject,
                                    criteria=findings, performed_by="consumers/"
                                    "engineering_intelligence_agent.py EngineeringIntelligenceAgent.verify")
        entry.update(result=report.outcomes[0].status, detail=report.outcomes[0].detail,
                     evidence=str(evidence.relative_to(REPO)))

        # CEO verification: the resident rule, and an independent re-derivation.
        record = json.loads((ROOT / f"{grant.delegation_id}.delegation.json").read_text())
        met, _, reasons = w4.plan_completion(ROOT, record)
        mine = independent_check(subject)
        entry["ceo_verification"] = {"plan_completion": "met" if met else list(reasons),
                                     "independent_rederivation_agrees": mine == findings,
                                     "carried": sum(mine.values()), "of": len(mine)}
        if path == "accept":
            entry["decision"] = w4.review_result(
                ROOT, grant.delegation_id, surface=surface, decision=w4.ACCEPT,
                reviewer=w4.AUTHORIZED_DELEGATOR,
                reason=(f"the evidence shows all {len(mine)} elements carried by {subject}, and "
                        "my independent re-derivation agrees"))
        else:
            try:
                w4.review_result(ROOT, grant.delegation_id, surface=surface,
                                 decision=w4.ACCEPT, reviewer=w4.AUTHORIZED_DELEGATOR,
                                 reason="attempted on a failed result")
                entry["accept_after_failure"] = "NOT REFUSED"
            except w4.DelegationError as exc:
                entry["accept_after_failure"] = f"refused: {exc}"
            entry["decision"] = w4.review_result(
                ROOT, grant.delegation_id, surface=surface, decision=w4.REWORK,
                reviewer=w4.AUTHORIZED_DELEGATOR,
                reason=(f"{subject} carries {sum(mine.values())} of {len(mine)} elements "
                        "(independently re-derived); the step's premise — that a continuity "
                        "module carries every delegation element — is wrong. Sent back as a "
                        "report of which elements it carries"),
                rework_steps=(PlanStep("report-continuity-elements",
                                       f"Report which of the fourteen FD-P11-001 §13 delegation "
                                       f"elements {subject} carries, each satisfied or not.",
                                       requires_delegation=True),
                              ceo_review("report-continuity-elements")))
        run["paths"][path] = entry

    planning_continuity.save(surface, ROOT / "planning.state.json")
    run["plan_outcomes"] = {k: w4.plan_outcome(surface, v[0], ROOT) for k, v in GOALS.items()}
    (ROOT / "s4-run.result.json").write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n",
                                             encoding="utf-8")
    print(json.dumps({k: {x: v[x] for x in ("result", "detail", "ceo_verification",
                                              "accept_without_evidence")}
                      for k, v in run["paths"].items()}, indent=1, ensure_ascii=False))
    print({k: (v["completed"], v["open_steps"]) for k, v in run["plan_outcomes"].items()})
    return 0


if __name__ == "__main__":
    sys.exit(main())
