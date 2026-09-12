"""`P11-W1` — coordination that spans two Departments.

Written under `DP-02 §11` item 10 and the `E11-04` directive. `DP-02 §3` fixes
the acceptance target and `§10` fixes the invariant that decides the shape:

    MULTI-AGENT ≠ CROSS-DEPARTMENT COORDINATION

so this module never counts agents. It issues **one grant per Department's
instance** — `FD-P11-001` issues each grant to exactly one recipient, and
`Domain Model §5` makes an Agent Instance *"accountable to the Platform Division
that owns its Agent Definition"* — and composes both steps into **one**
Workflow, because `Domain Model §4` says instances collaborate *"only through a
shared Workflow"*.

**The work is real and it predates this module.** Step one is the Testing
sub-ability `ADR-0008` established on 2026-07-30, implemented in
`consumers/engineering_intelligence_agent.py` on 2026-09-02, and already
exercised on 2026-09-11 against `tools/w4_delegation.py`. Step two is citation
discipline over the record step one produces. Neither was invented for `E11-04`;
the directive's `§9` forbids work *"whose sole purpose is to produce an E11-04
PASS"*, and `§5` forbids inventing a capability to obtain one.

**The dependency is an ordering constraint, not a declaration.** Step two reads
what step one wrote. Exchanging them is not possible, which is what makes this a
handoff rather than two steps that happen to be adjacent.

Both performers are **injected**, because `tools/` may not import `consumers/`.
The entry point is `cross_department_coordination_proof.py` at the repository
root — the only place outside both isolated regions.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.agent.definition import AgentDefinition  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.delegation_reconciliation import project  # noqa: E402
from tools.escalation_register import record_refusals  # noqa: E402
from tools.organization_catalog import read_departments  # noqa: E402
from tools.plan_to_workflow import compose  # noqa: E402
from tools.planning import (AuthorityProvenance, Goal, Plan, PlanStep,  # noqa: E402
                            PlanningSurface, sequence)
from tools.w4_delegation import AUTHORIZED_DELEGATOR, W4DelegationRegistry  # noqa: E402
from tools.w4_execution import (  # noqa: E402
    ExecutionOutcome, ExecutionRefused, ExecutionReport, W4Executor)

from tools.p12_certified_evidence_guard import guard  # noqa: E402

OPERATIONS = REPO_ROOT / "docs/architecture/p11/x-department-operations"
FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
DP01_RECORD = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

WORKFLOW_KEY = "cross-department-artifact-conformance-review"

#: The two participants, each read from the resident Definition record rather
#: than asserted here. Their Departments are resolved at run time through
#: `read_departments()`, never hardcoded — `§7` of the directive requires the
#: participating Departments be *"resolved from canonical organizational
#: relationships rather than inferred from agent count."*
ENGINEERING_DEFINITION = AgentDefinition(
    agent_definition_key="engineering-intelligence-agent",
    agent_definition_version="1.1",
    owning_department_key="engineering",
    implemented_capabilities=("engineering-intelligence",),
    specified_skills=("artifact-conformance-verification",),
    specified_workflows=(WORKFLOW_KEY,))

PLATFORM_DEFINITION = AgentDefinition(
    agent_definition_key="governance-artifact-integrity-agent",
    agent_definition_version="1.2",
    owning_department_key="platform",
    implemented_capabilities=("governance-artifact-integrity",),
    specified_skills=("citation-discipline-verification",),
    specified_workflows=(WORKFLOW_KEY,))

ENGINEERING_INSTANCE = "engineering-intelligence-instance-001"
PLATFORM_INSTANCE = "governance-artifact-integrity-instance-001"

#: `step → (instance, capability, skill)`. The Skill each step composes is the
#: one its performer's **Definition already permits**; `authorize_handoff`
#: re-reads that from the record and refuses if it is not there, so this mapping
#: cannot grant anything it names.
STEPS: Dict[str, Tuple[str, str, str]] = {
    "verify-artifact-conformance": (ENGINEERING_INSTANCE, "engineering-intelligence",
                                    "artifact-conformance-verification"),
    "verify-citation-discipline": (PLATFORM_INSTANCE, "governance-artifact-integrity",
                                   "citation-discipline-verification"),
}


def department_of(definition_key: str) -> str:
    """The Department that owns a Definition, read from the population.

    Returns ``""`` when no Department claims it — an unclaimed Definition is not
    quietly attributed to one, which is the only way the cross-Department count
    below can be trusted.
    """
    for record in read_departments():
        if definition_key in record.agent_definitions:
            return record.key
    return ""


def _revoke_stale(root: Path, instance_keys) -> Tuple[str, ...]:
    """Withdraw live grants left by an earlier run, for either instance."""
    revoked = []
    for path in sorted(root.glob("*.delegation.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("status") != "ACTIVE" or \
                record.get("recipient_instance") not in instance_keys:
            continue
        record["status"] = "REVOKED"
        record["revocation_reason"] = (
            "Superseded by a later cross-Department coordination run. "
            "RE-RUN ≠ NEW UNBOUNDED AUTHORITY.")
        record["revoked_at"] = datetime.now(timezone.utc).isoformat()
        # `F-12`: revocation mutates a certified-phase record in place.
        guard(path).write_text(json.dumps(record, indent=2), encoding="utf-8")
        revoked.append(record["delegation_id"])
    return tuple(revoked)


def _plan():
    authority = AuthorityProvenance("DP-01 §3 W2", DP01_RECORD)
    surface = PlanningSurface()
    surface.declare(Goal(
        key="cross-department-conformance-review",
        statement="Verify an engineered artifact against stated conformance "
                  "criteria, then verify the citation discipline of the record "
                  "that result produces.",
        authority=authority))
    plan = surface.adopt(Plan(
        key="cross-department-conformance-review-plan-0",
        goal_key="cross-department-conformance-review", authority=authority,
        steps=(PlanStep("verify-artifact-conformance",
                        "Check the artifact against its stated conformance "
                        "criteria."),
               PlanStep("verify-citation-discipline",
                        "Check that the record produced cites authority that "
                        "resolves.",
                        depends_on=("verify-artifact-conformance",)))))
    return surface, plan


def run(perform: Callable[[PlanStep], str], *, coordinate=None,
        persist: bool = True, act: str = "DP-02 §11 item 10") -> dict:
    """`PLAN → TWO GRANTS → ONE WORKFLOW → TWO DEPARTMENTS → EVIDENCE`."""
    OPERATIONS.mkdir(parents=True, exist_ok=True)
    root = OPERATIONS if persist else None
    superseded = (_revoke_stale(OPERATIONS, set(STEPS[s][0] for s in STEPS))
                  if persist else ())

    registry = AgentInstanceRegistry(root)
    registrations = {}
    for definition, instance_key, capability in (
            (ENGINEERING_DEFINITION, ENGINEERING_INSTANCE, "engineering-intelligence"),
            (PLATFORM_DEFINITION, PLATFORM_INSTANCE, "governance-artifact-integrity")):
        registrations[instance_key] = registry.register(
            instance_key=instance_key, definition=definition,
            permitted_capabilities=(capability,),
            created_by=AUTHORIZED_DELEGATOR,
            authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
            accountable_to=AUTHORIZED_DELEGATOR)

    delegations = W4DelegationRegistry(registry, root)
    grants: Dict[str, object] = {}
    for step_key, (instance_key, capability, _skill) in STEPS.items():
        grants[step_key] = delegations.issue(
            delegator=AUTHORIZED_DELEGATOR, recipient_instance=instance_key,
            authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
            objective="Perform one step of the cross-Department artifact "
                      "conformance review.",
            capability_scope=(capability,), work_scope=(step_key,),
            lifecycle_boundary="one execution of plan "
                               "cross-department-conformance-review-plan-0",
            resource_boundary="read-only over resident artifacts and records",
            output_expectation="one outcome for the step named in work scope",
            verification_requirement="the step is expressed as a WorkflowStep "
                                     "whose actor and skill are already "
                                     "authorized by the actor's Definition",
            escalation_condition="any step the grant does not cover",
            accountable_party=AUTHORIZED_DELEGATOR,
            termination_condition="on completion of the bound plan, or revocation")

    surface, plan = _plan()
    prepared = surface.prepare_for_workflow(plan)

    # One Workflow, two grants. `compose` re-checks each step against the grant
    # that covers it, so nothing here is authorized by this module.
    composition = compose(prepared, delegation=grants, registry=registry,
                          skill_for={k: v[2] for k, v in STEPS.items()})

    # Collected into an `ExecutionReport`, the same shape the single-grant paths
    # produce, so `report.refusals` is what reaches `record_refusals` here too —
    # the property `test_each_call_passes_the_executors_own_refusals` asserts,
    # and which a locally-built list would have satisfied only by accident.
    report = ExecutionReport()
    for step in sequence(plan):
        executor = W4Executor(grants[step.key], registry)
        try:
            report.outcomes.append(executor.execute_step(step, perform))
        except ExecutionRefused as refusal:
            report.refusals.append(refusal)
            report.outcomes.append(ExecutionOutcome(
                step_key=step.key, status="escalation", detail=str(refusal),
                delegation_id=grants[step.key].delegation_id,
                instance_key=grants[step.key].recipient_instance,
                at=datetime.now(timezone.utc).isoformat()))
    outcomes = report.outcomes

    terminal, facts = coordinate(composition) if coordinate else (None, {})

    participants = sorted({r.agent_instance_key
                           for r in composition.acting_instances()})
    by_department = {
        key: department_of(registrations[key].definition_key)
        for key in participants}
    departments = sorted({d for d in by_department.values() if d})

    escalations = list(record_refusals(
        OPERATIONS if persist else None, report.refusals,
        subject=f"plan {plan.key} / cross-department coordination",
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD)))

    evidence = {
        "act": act,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "superseded_grants": list(superseded),
        "workflow": WORKFLOW_KEY,
        "goal": plan.goal_key, "plan": plan.key,
        "plan_authority": plan.authority_provenance(),
        "grants": {k: g.delegation_id for k, g in grants.items()},
        "delegation_id": grants["verify-artifact-conformance"].delegation_id,
        "authority_chain": list(
            grants["verify-artifact-conformance"].authority_chain()),
        "accountable_party": AUTHORIZED_DELEGATOR,
        "agent_instances": participants,
        "instance_department": by_department,
        "departments": departments,
        "department_count": len(departments),
        "cross_department": len(departments) > 1,
        "workflow_steps": [s.step_key for s in composition.ordered()],
        "composed_skills": [r.skill_key for r in composition.composed_skills()],
        "dependency": {"verify-citation-discipline":
                       ["verify-artifact-conformance"]},
        "coordination": facts,
        "workflow_terminal_state": str(terminal) if terminal else None,
        "outcomes": [{"step": o.step_key, "status": o.status, "detail": o.detail,
                      "instance": o.instance_key, "delegation": o.delegation_id,
                      "at": o.at} for o in outcomes],
        "refusals": [str(r) for r in report.refusals],
        "boundary_crossed": bool(report.refusals),
        "escalations": escalations,
    }
    if persist:
        # `F-12`: see `w4_first_run`. Certification froze this record.
        guard(OPERATIONS / "cross-department.evidence.json").write_text(
            json.dumps(evidence, indent=2), encoding="utf-8")
        for grant in grants.values():
            project(grant.delegation_id)
    return evidence
