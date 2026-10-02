"""S-2 representative execution: CEO goal → plan → bounded work → delegation.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-S2-PLAN-TO-DELEGATION.md
(authority FD-AGENCY-001). Writes only to a non-certified operational root, and
refuses to run if that root is certified or already holds a grant: a second run
must not accumulate authority.

The grant is issued and persisted, not executed. Executing it is not S-2.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402
from tools.planning import AuthorityProvenance, Goal, Plan, PlanningSurface, PlanStep  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s2-plan-delegation"
PLANNING = ROOT / "planning.state.json"
S2_RECORD = "docs/governance/acts/DIR-AIOS-AGENCY-S2-PLAN-TO-DELEGATION.md"
INSTANCE = "engineering-intelligence-instance-001"
GOAL = "agency-s2-ledger-rule-verification"
PLAN = f"{GOAL}-plan-0"

if is_protected(ROOT):
    sys.exit(f"refusing: {ROOT} is certified evidence")
if ROOT.is_dir() and any(ROOT.glob("*.delegation.json")):
    sys.exit("refusing: this root already holds a grant; a re-run would accumulate authority")

# 1. CEO goal and plan, on the existing planning surface.
authority = AuthorityProvenance("FD-AGENCY-001 S-2", S2_RECORD)
surface = PlanningSurface()
surface.declare(Goal(
    key=GOAL, authority=authority,
    statement="Verify that the delegation module enforces the operational-ledger "
              "rules documented for S-1."))
plan = surface.adopt(Plan(key=PLAN, goal_key=GOAL, authority=authority, steps=(
    PlanStep("verify-ledger-rules",
             "Verify tools/w4_delegation.py against the seven rules in "
             "docs/architecture/agency/W4-OPERATIONAL-LEDGER.md §3.",
             requires_delegation=True),
    PlanStep("review-ledger-verification",
             "Review the verification result and accept, reject or send it back "
             "(Co-Founder / CEO, A11).",
             depends_on=("verify-ledger-rules",)),
)))

# 2. Bounded work selection: what the plan itself marks for delegation.
requirements = surface.delegation_requirements(plan)

# 3. Recipient: an instance of an existing Agent Definition, registered in this
#    root under FD-P11-001 §7, as every W4 root has done.
registry = AgentInstanceRegistry(ROOT)
registry.register(
    instance_key=INSTANCE, definition=SELECTED_DEFINITION,
    permitted_capabilities=("engineering-intelligence",),
    created_by=w4.AUTHORIZED_DELEGATOR,
    authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
    accountable_to=w4.AUTHORIZED_DELEGATOR)

# 4. The CEO issues the delegation for the marked step; it is persisted.
delegations = w4.W4DelegationRegistry(registry, ROOT)
grant = w4.issue_from_plan(
    delegations, surface, plan, "verify-ledger-rules",
    delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE,
    authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
    capability_scope=("engineering-intelligence",),
    resource_boundary="read-only over tools/w4_delegation.py and "
                      "docs/architecture/agency/W4-OPERATIONAL-LEDGER.md; no network; "
                      "no governance artifact is written",
    output_expectation="one result per rule, satisfied or not",
    verification_requirement="every one of the seven rules reported satisfied or not, "
                             "each with the code location that establishes it",
    escalation_condition="any step outside the delegated work scope, a revoked "
                         "delegation, or a retired instance")

# 5. The plan is persisted with its full chain.
planning_continuity.save(surface, PLANNING)

result = {
    "executed_at": datetime.now(timezone.utc).isoformat(),
    "root": str(ROOT.relative_to(REPO)),
    "goal": GOAL, "plan": PLAN,
    "plan_authority": plan.authority.cited(),
    "delegation_requirements": [
        {"plan_key": r.plan_key, "step_key": r.step_key, "scope": r.scope_described}
        for r in requirements],
    "not_delegated": [s.key for s in plan.steps if not s.requires_delegation],
    "delegation": grant.to_payload(),
}
out = ROOT / "s2-run.result.json"
out.write_text(json.dumps(result, indent=2, default=str) + "\n", encoding="utf-8")
print(json.dumps(result, indent=1, default=str))
