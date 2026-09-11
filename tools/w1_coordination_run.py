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
from tools.plan_to_workflow import compose  # noqa: E402
from tools.planning import (  # noqa: E402
    AuthorityProvenance, Goal, Plan, PlanStep, PlanningSurface)
from tools.w4_delegation import AUTHORIZED_DELEGATOR, W4DelegationRegistry  # noqa: E402
from tools.w4_execution import W4Executor  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
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
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
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


def run(perform, *, coordinate=None, persist: bool = True) -> dict:
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
    # `perform` is supplied by the caller and drives the resident
    # `WorkflowParticipatingAgent`, because `tools/` may not import
    # `consumers/`. It returns the terminal lifecycle state, or None.
    terminal = coordinate(composition) if coordinate else None

    evidence = {
        "act": "ACT-CC-P11-010",
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
        "outcomes": [{"step": o.step_key, "status": o.status,
                      "detail": o.detail} for o in report.outcomes],
        "refusals": [str(r) for r in report.refusals],
        "boundary_crossed": bool(report.refusals),
    }
    if persist:
        (OPERATIONS / "w1-coordination.evidence.json").write_text(
            json.dumps(evidence, indent=2), encoding="utf-8")
    return evidence


def WorkflowCoordinationProbe(composition) -> bool:
    """Whether the composition coordinates more than one acting instance.

    `§19`: coordination is not proven merely because a Workflow can be
    instantiated. Reported honestly — a single-instance composition is a
    **handoff**, and calling it cross-agent coordination would overstate it.
    """
    return len(set(composition.acting_instances())) > 1
