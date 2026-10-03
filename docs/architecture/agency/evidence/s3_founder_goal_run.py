"""S-3 representative execution: Founder Goal → CEO plan → delegation → agent.

Directive: docs/governance/acts/DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING.md.

* The Founder Goal is that directive itself, a registered verbatim Founder
  instrument, quoted, not paraphrased.
* The CEO plans under its own authority (Co-Founder V2 A01), distinct from the
  goal's.
* The executive-function target is a **non-canonical annotation** in the run
  result; no planning contract field exists for it, and none is added
  (FD-AGENCY-001 Q6-A).
* No candidate executive is created or registered. The delegation goes to an
  existing Agent Definition's instance.

Writes only to a non-certified operational root, and refuses to run twice.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from tools import authority_citation as ac  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402
from tools.planning import AuthorityProvenance, Goal, Plan, PlanningSurface, PlanStep  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

ROOT = REPO / "docs/architecture/agency/operations/w4-s3-founder-goal"
S3_ID = "DIR-AIOS-AGENCY-S3-FOUNDER-GOAL-TO-PLANNING"
S3_RECORD = f"docs/governance/acts/{S3_ID}.md"
STATEMENT = "S-3 — Connect Founder Goal to the CEO Planning Surface"
GOAL = "founder-s3-connect-goal-to-planning"
PLAN = f"{GOAL}-plan-0"
INSTANCE = "engineering-intelligence-instance-001"
CEO = AuthorityProvenance(
    "Co-Founder V2 A01 Executive Command",
    "docs/governance/AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md")

#: The directive's `§2` table, verbatim: vocabulary, not entities.
CANDIDATES = (
    ("Monkey D. Luffy", "CEO / Executive Leadership"),
    ("Nami", "CFO / Finance"),
    ("Roronoa Zoro", "COO / Production"),
    ("Usopp", "Creative Director / Copywriter & Storyteller"),
    ("Nico Robin", "Research & Strategy / Legal"),
    ("Franky", "CTO / Engineering"),
    ("Tony Tony Chopper", "HRD / People & Culture"),
    ("Sanji", "Hospitality / Client Relations"),
    ("Jinbe", "Project Management / Risk Management"),
    ("Brook", "PR / Social Media"),
)
#: Resident capability counterpart per function: the FD-AGENCY-001 decision
#: record, `§4` and `§4.1` (Q5-C mapping). Only CTO has a resident Capability.
COUNTERPART = {
    "CEO / Executive Leadership": (None, "held by the Co-Founder / CEO office; not available (FD-AGENCY-001)"),
    "CTO / Engineering": ("engineering-intelligence", "department engineering"),
}

if is_protected(ROOT):
    sys.exit(f"refusing: {ROOT} is certified evidence")
if ROOT.is_dir() and any(ROOT.glob("*.delegation.json")):
    sys.exit("refusing: this root already holds a grant; a re-run would accumulate authority")

# 1. The CEO reads the Founder Goal: it must quote a registered Founder instrument.
refused = ac.founder_goal_refusal(S3_ID, S3_RECORD, STATEMENT)
if refused:
    sys.exit(f"refusing: not a Founder Goal: {refused}")
surface = PlanningSurface()
goal = surface.declare(Goal(key=GOAL, statement=STATEMENT,
                            authority=AuthorityProvenance(S3_ID, S3_RECORD)))

# 2. The CEO plans the HOW under its own authority.
plan = surface.adopt(Plan(key=PLAN, goal_key=GOAL, authority=CEO, steps=(
    PlanStep("verify-founder-goal-intake",
             "Verify tools/authority_citation.py founder_goal_refusal against S-3 "
             "§12 negative controls 1, 4 and 7, reporting each satisfied or not.",
             requires_delegation=True),
    PlanStep("review-founder-goal-verification",
             "Review the verification result and accept, reject or send it back "
             "(Co-Founder / CEO, A11).",
             depends_on=("verify-founder-goal-intake",)),
    PlanStep("report-to-founder",
             "Report the S-3 result to the Founder (Co-Founder / CEO, A18).",
             depends_on=("review-founder-goal-verification",)),
)))
requirements = surface.delegation_requirements(plan)

# 3. Executive-function targeting, against what is actually resident.
instances = sorted({p.stem.replace(".instance", "")
                    for p in REPO.glob("docs/**/*.instance.json")})


def mapping(name, function):
    cap, basis = COUNTERPART.get(function, (None, "no resident counterpart (FD-AGENCY-001 §4.1)"))
    token = name.lower().replace(" ", "-")
    named = [i for i in instances if any(part in i for part in token.split("-") if len(part) > 3)]
    return {"candidate": name, "function": function,
            "canonical_status": "CANDIDATE ONLY — NOT CANONICAL — NOT REGISTERED — NOT ACTIVATED",
            "agent_instance_named_after_candidate": named or None,
            "instance_status": "CANDIDATE — NO ACTIVE INSTANCE" if not named else "UNEXPECTED",
            "resident_capability": cap, "basis": basis}


candidate_map = [mapping(n, f) for n, f in CANDIDATES]
target = next(m for m in candidate_map if m["candidate"] == "Franky")

# 4. Recipient: the existing definition's instance (minimum non-certified fixture).
registry = AgentInstanceRegistry(ROOT)
registry.register(
    instance_key=INSTANCE, definition=SELECTED_DEFINITION,
    permitted_capabilities=(target["resident_capability"],),
    created_by=w4.AUTHORIZED_DELEGATOR,
    authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
    accountable_to=w4.AUTHORIZED_DELEGATOR)

# 5. The CEO issues the delegation for the marked step.
grant = w4.issue_from_plan(
    w4.W4DelegationRegistry(registry, ROOT), surface, plan, "verify-founder-goal-intake",
    delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance=INSTANCE,
    authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
    capability_scope=(target["resident_capability"],),
    resource_boundary="read-only over tools/authority_citation.py and the S-3 directive; "
                      "no network; no governance artifact is written",
    output_expectation="one result per negative control, satisfied or not",
    verification_requirement="controls 1, 4 and 7 each reported satisfied or not, "
                             "with the code location that establishes it",
    escalation_condition="any step outside the delegated work scope, a revoked "
                         "delegation, or a retired instance")
planning_continuity.save(surface, ROOT / "planning.state.json")

result = {
    "executed_at": datetime.now(timezone.utc).isoformat(),
    "root": str(ROOT.relative_to(REPO)),
    "founder_goal": {"key": GOAL, "statement": STATEMENT, "authority": goal.authority.cited(),
                     "verified": "VERIFIED"},
    "ceo_plan": {"key": PLAN, "authority": plan.authority.cited(),
                 "steps": [{"key": s.key, "delegated": s.requires_delegation} for s in plan.steps]},
    "delegation_requirements": [{"plan_key": r.plan_key, "step_key": r.step_key}
                                for r in requirements],
    # Non-canonical annotation (FD-AGENCY-001 Q6-A): the planning contract has
    # no field for it, and none was added.
    "executive_target": {"step": "verify-founder-goal-intake",
                         "function": target["function"], "candidate": target["candidate"],
                         "candidate_instance_status": target["instance_status"],
                         "required_capability": target["resident_capability"],
                         "actual_recipient": INSTANCE,
                         "note": "delegated to an existing instance; the candidate is not an agent"},
    "candidate_map": candidate_map,
    "delegation": grant.to_payload(),
}
(ROOT / "s3-run.result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("founder_goal", "ceo_plan", "executive_target")}, indent=1))
print("delegation", grant.delegation_id)
