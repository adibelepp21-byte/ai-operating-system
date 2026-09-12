"""`P11-W1` — the first real `PLAN → WORKFLOW → COORDINATION` proof.

`ACT-CC-P11-010 §20`. Uses **only authority that already exists**: `FD-P11-001`
authorizes the delegator and instance creation; the Agent Definition, its
permitted Skills and its Workflows are resident P10 records; the Plan comes from
the W2 surface. `§20`: *"No new authority may be created solely to make the test
pass."*

**The Agent Definition selected here differs from W4's, and that is the finding.**
`ACT-CC-P11-008` selected `engineering-intelligence-agent`, correctly, because
`§14` there asked for the safest observable first proof. That definition declares
*"Permitted Skills: None declared"* — so nothing it does can be expressed as a
`WorkflowStep`, which requires a Skill. `governance-artifact-integrity-agent`
carries **ten** permitted Skills and **five** permitted Workflows, and the
resident workflow record already names its actor as *"an Agent Instance of the
Governance Artifact Integrity Agent"*.

So the coordination blocker was never a missing delegator. It was a missing
**instance of a Skill-bearing definition** — and `FD-P11-001 §7` authorizes
creating one.

`§21` — the run is bounded (one plan, two steps), reversible (the grant is
revocable and superseded on re-run), observable, persisted, attributable, and
safe to repeat.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from native_core.core.agent.definition import AgentDefinition  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.delegation_reconciliation import project  # noqa: E402
from tools.escalation_register import record_refusals  # noqa: E402
from tools.plan_to_workflow import compose  # noqa: E402
from tools.planning import (  # noqa: E402
    AuthorityProvenance, Goal, Plan, PlanStep, PlanningSurface)
from tools.w4_delegation import AUTHORIZED_DELEGATOR, W4DelegationRegistry  # noqa: E402
from tools.w4_execution import W4Executor  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
from tools.p12_certified_evidence_guard import guard  # noqa: E402

OPERATIONS = REPO_ROOT / "docs/architecture/p11/w1-operations"
FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
DP01_RECORD = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

#: Read from the resident record: Version 1.1, Active, owned by Platform.
DEFINITION = AgentDefinition(
    agent_definition_key="governance-artifact-integrity-agent",
    agent_definition_version="1.1",
    owning_department_key="platform",
    implemented_capabilities=("governance-artifact-integrity",),
    specified_skills=(), specified_workflows=())

INSTANCE_KEY = "governance-artifact-integrity-instance-001"

#: Two of the Skills the Definition already permits, and the two the resident
#: `workflow.governance-corpus-health-check` record says that Workflow contains.
STEP_SKILLS = {
    "review-open-items": "open-item-tracking-review",
    "summarize-diffs": "governance-artifact-diff-summary",
}


def _revoke_stale(root: Path, instance_key: str) -> Tuple[str, ...]:
    """`§35`: a re-run reconciles rather than accumulating live grants."""
    revoked = []
    for path in sorted(root.glob("*.delegation.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("status") != "ACTIVE" or \
                record.get("recipient_instance") != instance_key:
            continue
        record["status"] = "REVOKED"
        record["revocation_reason"] = (
            "Superseded by a later W1 coordination run. RE-RUN ≠ NEW UNBOUNDED "
            "AUTHORITY (ACT-CC-P11-010 §35).")
        record["revoked_at"] = datetime.now(timezone.utc).isoformat()
        # `F-12`: revocation *mutates* a certified-phase delegation record —
        # ACTIVE becomes REVOKED in place. That is a rewrite of frozen evidence,
        # and it was the write this guard's first wiring missed: the module
        # imported the guard, so a module-level conformance check passed while
        # this call site stayed open.
        guard(path).write_text(json.dumps(record, indent=2), encoding="utf-8")
        revoked.append(record["delegation_id"])
    return tuple(revoked)


def _plan():
    authority = AuthorityProvenance("DP-01 §3 W2", DP01_RECORD)
    surface = PlanningSurface()
    surface.declare(Goal(
        key="w1-coordination-proof",
        statement="Coordinate a governance corpus health check through the "
                  "sanctioned Workflow surface.",
        authority=authority))
    plan = surface.adopt(Plan(
        key="w1-coordination-proof-plan-0", goal_key="w1-coordination-proof",
        authority=authority,
        steps=(PlanStep("review-open-items", "Review open governance items."),
               PlanStep("summarize-diffs", "Summarize governance artifact "
                        "differences.", depends_on=("review-open-items",)))))
    return surface, plan


def run(perform, *, coordinate=None, persist: bool = True,
        act: str = "ACT-CC-P11-011") -> dict:
    """`PLAN → HANDOFF → WORKFLOW → COORDINATION → EXECUTION`."""
    OPERATIONS.mkdir(parents=True, exist_ok=True)
    root = OPERATIONS if persist else None
    superseded = _revoke_stale(OPERATIONS, INSTANCE_KEY) if persist else ()

    registry = AgentInstanceRegistry(root)
    registration = registry.register(
        instance_key=INSTANCE_KEY, definition=DEFINITION,
        permitted_capabilities=("governance-artifact-integrity",),
        created_by=AUTHORIZED_DELEGATOR,
        authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
        accountable_to=AUTHORIZED_DELEGATOR)

    delegations = W4DelegationRegistry(registry, root)
    delegation = delegations.issue(
        delegator=AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE_KEY,
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
        objective="Coordinate a governance corpus health check.",
        capability_scope=("governance-artifact-integrity",),
        work_scope=tuple(STEP_SKILLS),
        lifecycle_boundary="one execution of plan w1-coordination-proof-plan-0",
        resource_boundary="read-only over resident governance records",
        output_expectation="one outcome per coordinated step",
        verification_requirement="every step expressed as a WorkflowStep whose "
                                 "actor and skill are already authorized",
        escalation_condition="any step the delegation does not cover",
        accountable_party=AUTHORIZED_DELEGATOR,
        termination_condition="on completion of the bound plan, or revocation")

    surface, plan = _plan()
    prepared = surface.prepare_for_workflow(plan)

    # ── the handoff under test ────────────────────────────────────────────
    composition = compose(prepared, delegation=delegation, registry=registry,
                          skill_for=STEP_SKILLS)

    report = W4Executor(delegation, registry).execute_plan(plan, perform)

    # ── coordination: drive the composed Workflow through its lifecycle ───
    #
    # `coordinate` is supplied by the caller and drives the resident
    # `WorkflowParticipatingAgent` on the **resident Runtime**, because
    # `tools/` may not import `consumers/`. It returns
    # ``(terminal_state, coordination_facts)``.
    #
    # `ACT-CC-P11-011 §8`: the injected-subsystem result from `ACT-CC-P11-010`
    # remains valid for what it proved and is **not** the resident Runtime path.
    # `§36` requires every stage to be labelled, so the caller reports which it
    # used and the label is persisted rather than inferred.
    terminal, facts = coordinate(composition) if coordinate else (None, {})

    # ── refusals become organizational escalations (ACT-CC-P11-014) ──────
    #
    # **This path had no escalation home at all.** `ACT-CC-P11-009 §13` drew the
    # distinction — a refusal satisfies only `ACTION BLOCKED`, and an
    # `ExecutionOutcome` in an evidence file is transient to that run, with no
    # lifecycle, no accountable party and no way to resolve. The fix landed on
    # W4 and this module, written afterwards under `ACT-CC-P11-010`, did not
    # carry it: a coordination refusal would have survived only as a string in
    # `evidence["refusals"]`.
    #
    # It went unnoticed because **no W1 refusal has ever occurred**, so the
    # population was empty for a reason unrelated to the wiring — the same shape
    # as a loader that passes on the part of the population it can see.
    #
    # `DP-01 §3 W1` lists *"escalation"* among the coordination capabilities, so
    # W1 is if anything the more canonical home of the two.
    escalations = list(record_refusals(
        OPERATIONS if persist else None, report.refusals,
        subject=f"plan {plan.key} / delegation {delegation.delegation_id}",
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD)))

    evidence = {
        # The Act this *run* happened under, supplied by the caller.
        #
        # It was hardcoded to the Act that first wrote this module, so the
        # `ACT-CC-P11-011` run labelled itself `010` — a small defect with a
        # familiar shape: a field that was correct when written and silently
        # wrong once something else used it. `§36` requires labels not be
        # promoted silently; a stale label demotes just as quietly.
        "act": act,
        "module_constructed_under": "ACT-CC-P11-010",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "superseded_grants": list(superseded),
        "authority_chain": list(delegation.authority_chain()),
        "agent_definition": registration.definition_key,
        "agent_instance": registration.instance_key,
        "delegation_id": delegation.delegation_id,
        "delegation_status": delegation.status,
        "accountable_party": delegation.accountable_party,
        "goal": plan.goal_key, "plan": plan.key,
        "plan_authority": plan.authority_provenance(),
        "prepared_steps": [p.step_key for p in prepared],
        "workflow_steps": [s.step_key for s in composition.ordered()],
        "acting_instances": [r.agent_instance_key
                             for r in composition.acting_instances()],
        "composed_skills": [r.skill_key for r in composition.composed_skills()],
        "is_multi_agent": WorkflowCoordinationProbe(composition),
        "workflow_terminal_state": str(terminal) if terminal else None,
        "coordination": facts,
        "outcomes": [{"step": o.step_key, "status": o.status,
                      "detail": o.detail} for o in report.outcomes],
        "refusals": [str(r) for r in report.refusals],
        "escalations": list(escalations),
        "boundary_crossed": bool(report.refusals),
    }
    if persist:
        # `F-12`: P11 is certified, so this record is historical. The guard
        # refuses the overwrite rather than letting a re-run quietly rewrite
        # evidence that certification froze. Execution itself is untouched —
        # run with `persist=False` to observe without writing.
        guard(OPERATIONS / "w1-coordination.evidence.json").write_text(
            json.dumps(evidence, indent=2), encoding="utf-8")
        # `ACT-CC-P11-013 §14` — grant rotation must leave W3 tracking correct.
        #
        # The rotation above revoked this instance's previous grant and issued a
        # successor. Until this call existed, the organizational projection kept
        # naming the grant that had just been withdrawn, which is exactly how
        # the W3 record found by `ACT-CC-P11-012` went stale: the mechanism
        # built to stop grants accumulating is what orphaned it.
        #
        # `§15` leaves the timing open and this is the choice: **immediately
        # after the evidence is persisted**, so the projection's verification
        # link resolves to the run that produced the grant. The projection
        # creates no authority — `project()` refuses any grant that is not
        # `ACTIVE` with resolvable provenance — and a `HISTORICAL` record is
        # never rewritten (`§16`).
        project(delegation.delegation_id)
    return evidence


def WorkflowCoordinationProbe(composition) -> bool:
    """Whether the composition coordinates more than one acting instance.

    `§19`: coordination is not proven merely because a Workflow can be
    instantiated. Reported honestly — a single-instance composition is a
    **handoff**, and calling it cross-agent coordination would overstate it.
    """
    return len(set(composition.acting_instances())) > 1
