"""`ACT-CC-P11-008` — the first real W4 execution.

`§21`: *"Claude SHALL run the first real W4 execution through the actual
execution path. Test-only execution does not satisfy this gate."* This module is
that run: it registers a real Agent Instance, issues a real bounded Delegation,
binds real authorized work, executes it through the resident consumer, and
persists the evidence.

**`§8` — the Agent Definition selection, and the evidence for it.**

Three definitions exist. Each was read at body level:

* **Cognitive Intelligence Agent** — *"reasoning about, decomposing, sequencing,
  and reviewing work"*, realized boundary *"task decomposition and ordered
  planning only"*. **NOT VALID FOR W4.** Its realized capability is
  planning-shaped, and `FD-P11-001 §19` keeps Planning authority with Planning.
  Delegating *execution* to a decomposition-and-ordering agent would blur
  `PLAN ≠ EXECUTE` at the first opportunity.
* **Governance Artifact Integrity Agent** — *"review and proposal work only; it
  does not itself constitute governance authority"*. **VALID FOR W4**, ranked
  second: its subject matter is governance artifacts, and `§14` asks the first
  delegation to be the *safest observable* proof, not the most consequential.
* **Engineering Intelligence Agent** — *"constructing, changing, verifying, and
  safeguarding AIOS's own engineered artifacts"*, realized boundary *"the Coding
  and Testing sub-abilities only"*. **SELECTED.**

`§8.3`/`§8.4` — the capability is `engineering-intelligence`, and its Testing
sub-ability is *"Verify engineered artifacts against their stated conformance
criteria"*, which is exactly the shape of the bounded work below.

`§8.5` — the negative boundary, from the capability record: Architecture,
Security, Review, Refactoring and Documentation *"are not realized"*, and the
Capability *"does not cover governance-artifact maintenance"*. The delegation
below grants **Testing only** — narrower than the definition, which is narrower
than the capability. `§14`: minimum necessary scope.

`§8.6` — `FD-P11-001 §8` permits selecting an existing definition on evidence and
forbids inventing one. Nothing was invented: all three already existed, and the
resident consumer `consumers/engineering_intelligence_agent.py` — which
*"realizes the Coding and Testing sub-abilities only"* and *"holds no
authority"* — is the actual machinery `§21` requires.

**`§19` — the work is real, not a placeholder.** The bound work verifies that
`tools/w4_delegation.py`, the module this Act's own authority chain runs
through, actually contains the elements `FD-P11-001 §13` requires it to enforce.
That is a genuine conformance question about an engineered artifact, asked of the
agent whose realized capability is asking it. **It is deliberately a check whose
answer I did not know before running it** — a verification with a foregone
conclusion would be a placeholder wearing real work's clothes.

**What this run does not do.** It writes no governance artifact, changes no
architecture, and creates no authority. `§31`: real execution does not make P11
operational, and `§33` keeps the eight P11 dimensions from collapsing into this
one.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from native_core.core.agent.definition import AgentDefinition  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry
from tools.planning import (
    AuthorityProvenance,
    Goal,
    Plan,
    PlanStep,
    PlanningSurface,
)
from tools.w4_delegation import AUTHORIZED_DELEGATOR, W4DelegationRegistry
from tools.w4_execution import W4Executor

REPO_ROOT = Path(__file__).resolve().parent.parent
OPERATIONS = REPO_ROOT / "docs/architecture/p11/w4-operations"

FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
DP01_RECORD = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"

#: Read from the resident Agent Definition record, not invented here.
#: `engineering-intelligence-agent.md` — Version 1.0, Status Active, owned by
#: Engineering, implementing the Engineering Intelligence Capability.
SELECTED_DEFINITION = AgentDefinition(
    agent_definition_key="engineering-intelligence-agent",
    agent_definition_version="1.0",
    owning_department_key="engineering",
    implemented_capabilities=("engineering-intelligence",),
    specified_skills=(), specified_workflows=())

INSTANCE_KEY = "engineering-intelligence-instance-001"

#: The conformance criteria the bound work checks, as plain names. Derived from
#: `FD-P11-001 §13`, which lists what every Delegation must define.
#:
#: Held as names rather than as the consumer's `ConformanceCriterion` objects
#: because **this module may not import that region** — see the residency note
#: in the docstring. The performer converts them into whatever its own
#: verification surface expects.
CRITERION_NAMES = (
    "delegation_id", "delegator", "recipient_instance", "objective",
    "capability_scope", "work_scope", "lifecycle_boundary",
    "resource_boundary", "output_expectation", "verification_requirement",
    "escalation_condition", "accountable_party", "termination_condition",
)

SUBJECT = REPO_ROOT / "tools" / "w4_delegation.py"


def _plan() -> Tuple[PlanningSurface, Plan]:
    """Real authorized work on the P11 planning surface (`§19`, `§20`).

    Planning states the work; the Delegation grants bounded authority to perform
    it; execution performs it. Three objects, `§20`'s required separation.
    """
    authority = AuthorityProvenance("DP-01 §3 W2", DP01_RECORD)
    surface = PlanningSurface()
    surface.declare(Goal(
        key="w4-first-execution-proof",
        statement="Verify that the W4 delegation module enforces the elements "
                  "FD-P11-001 §13 requires of every Delegation.",
        authority=authority))
    plan = surface.adopt(Plan(
        key="w4-first-execution-proof-plan-0",
        goal_key="w4-first-execution-proof", authority=authority,
        steps=(
            PlanStep("verify-delegation-elements",
                     "Verify tools/w4_delegation.py against the FD-P11-001 §13 "
                     "conformance criteria."),
            PlanStep("report-conformance",
                     "Report which criteria were satisfied.",
                     depends_on=("verify-delegation-elements",)),
        )))
    return surface, plan


def _revoke_stale_grants(root: Path, instance_key: str) -> Tuple[str, ...]:
    """Withdraw any live grant left by an earlier run of this same proof.

    **Added because re-running this module left orphans.** Three runs — an API
    correction, a dependency inversion, and the move to a root entry point —
    each issued a fresh Delegation and left the previous one `ACTIVE`. Nothing
    was using them, and nothing would have withdrawn them.

    That is the failure `FD-P11-001 §29` names: a Delegation is *"a controlled
    lifecycle object rather than a permanent authority grant"*, and a grant
    nobody ends is permanent in practice however carefully its terms describe an
    ending. `§13` item 14 requires a termination condition; **a condition with no
    mechanism to apply it is a description.**

    Superseding rather than deleting: the record stays readable, marked
    `REVOKED` with the reason, exactly as the escalation register and the plan
    chain preserve what they retire.
    """
    revoked = []
    for path in sorted(root.glob("*.delegation.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record.get("status") != "ACTIVE" or \
                record.get("recipient_instance") != instance_key:
            continue
        record["status"] = "REVOKED"
        record["revocation_reason"] = (
            "Superseded by a later run of the same first-execution proof. The "
            "grant was never terminated by its own condition, so it is "
            "withdrawn here — FD-P11-001 §29: a delegation is a controlled "
            "lifecycle object, not a permanent grant.")
        record["revoked_at"] = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        revoked.append(record["delegation_id"])
    return tuple(revoked)


def run(perform_verification, *, persist: bool = True) -> dict:
    """Perform the first real W4 execution and return its evidence.

    ``perform_verification(artifact_lines, criterion_names) -> {name: bool}``
    is **injected**, and that is an architectural requirement rather than a
    convenience. `consumers/tests/test_reference_agent.py` asserts that `tools/`
    imports nothing from `consumers/`, and three consumer suites assert the
    reverse — the two regions are **mutually isolated**, so neither may wire
    itself to the other.

    My first version imported the consumer directly and the invariant caught it.
    Injecting the performer is the correct resolution and a better design
    besides: a Delegation names an **instance and a capability**, never an
    implementation, so the machinery that enforces the authority chain has no
    business knowing which module does the work.
    """
    OPERATIONS.mkdir(parents=True, exist_ok=True)
    root = OPERATIONS if persist else None

    # ── stage 1: Agent Instance (§9) ──────────────────────────────────────
    registry = AgentInstanceRegistry(root)
    registration = registry.register(
        instance_key=INSTANCE_KEY,
        definition=SELECTED_DEFINITION,
        permitted_capabilities=("engineering-intelligence",),
        created_by=AUTHORIZED_DELEGATOR,
        authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
        accountable_to=AUTHORIZED_DELEGATOR)

    # ── stage 2: bounded Delegation (§13, §14) ────────────────────────────
    delegations = W4DelegationRegistry(registry, root)
    superseded = _revoke_stale_grants(root, INSTANCE_KEY) if persist else ()
    delegation = delegations.issue(
        delegator=AUTHORIZED_DELEGATOR,
        recipient_instance=registration.instance_key,
        authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD),
        objective="Verify tools/w4_delegation.py against the FD-P11-001 §13 "
                  "conformance criteria, and report the result.",
        capability_scope=("engineering-intelligence",),
        work_scope=("verify-delegation-elements", "report-conformance"),
        lifecycle_boundary="one execution of plan "
                           "w4-first-execution-proof-plan-0",
        resource_boundary="read-only access to tools/w4_delegation.py; "
                          "no network; no governance artifact is written",
        output_expectation="one conformance result per criterion",
        verification_requirement="every criterion reported satisfied or not, "
                                 "and every outcome carrying a ratified status",
        escalation_condition="any step outside the delegated work scope, or a "
                             "revoked delegation, or a retired instance",
        accountable_party=AUTHORIZED_DELEGATOR,
        termination_condition="on completion of the bound plan, or on "
                              "revocation by the authorized delegator")

    # ── stage 3: bound real work and execute it (§19, §21) ────────────────
    surface, plan = _plan()
    lines = tuple(SUBJECT.read_text(encoding="utf-8").split("\n"))
    findings: dict = {}

    def perform(step: PlanStep) -> str:
        """The delegated work. Runs only for steps inside the work scope."""
        if step.key == "verify-delegation-elements":
            findings.update(perform_verification(lines, CRITERION_NAMES))
            return f"verified {len(findings)} criteria"
        unsatisfied = sorted(k for k, ok in findings.items() if not ok)
        satisfied = [k for k, ok in findings.items() if ok]
        return (f"{len(satisfied)} satisfied, {len(unsatisfied)} not: "
                f"{unsatisfied or 'none'}")

    report = W4Executor(delegation, registry).execute_plan(plan, perform)

    # ── stage 4: evidence (§22, §46) ──────────────────────────────────────
    evidence = {
        "act": "ACT-CC-P11-008",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "authority_chain": list(delegation.authority_chain()),
        "agent_definition": registration.definition_key,
        "agent_definition_version":
            registration.instance.agent_definition.agent_definition_version,
        "agent_instance": registration.instance_key,
        "instance_lifecycle": registration.lifecycle,
        "delegation_id": delegation.delegation_id,
        "delegation_status": delegation.status,
        "delegator": delegation.delegator,
        "accountable_party": delegation.accountable_party,
        "authority_instrument": delegation.authority.instrument,
        "authority_record": delegation.authority.record,
        "capability_scope": list(delegation.capability_scope),
        "work_scope": list(delegation.work_scope),
        "goal": plan.goal_key,
        "plan": plan.key,
        "plan_authority": plan.authority_provenance(),
        "subject_artifact": str(SUBJECT.relative_to(REPO_ROOT)),
        "criteria_total": len(CRITERION_NAMES),
        "criteria_satisfied": sum(1 for ok in findings.values() if ok),
        "criteria_unsatisfied": sorted(k for k, ok in findings.items()
                                       if not ok),
        "outcomes": [{"step": o.step_key, "status": o.status,
                      "detail": o.detail, "instance": o.instance_key,
                      "delegation": o.delegation_id, "at": o.at}
                     for o in report.outcomes],
        "refusals": [str(r) for r in report.refusals],
        "boundary_crossed": bool(report.refusals),
        "superseded_grants": list(superseded),
    }
    if persist:
        (OPERATIONS / "first-execution.evidence.json").write_text(
            json.dumps(evidence, indent=2), encoding="utf-8")
    return evidence


# No entry point here, and none may be added.
#
# Wiring the performer requires importing `consumers/`, and
# `consumers/tests/test_reference_agent.py` asserts that **no file under
# `tools/` imports that region** — by AST, so a `__main__`-guarded import
# violates it exactly as a top-level one does. That strictness is correct: an
# import inside a guard is still an edge in the dependency graph, and a region
# boundary that only held at module scope would not be a boundary.
#
# The entry point is therefore `w4_first_execution.py` at the repository root —
# the only place outside both isolated regions. See its docstring.
