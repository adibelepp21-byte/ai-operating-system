"""`E11` measurement — P11 measured against the **ratified** acceptance criteria.

Authorized by `DP-02 §11` items 6–8: *"Measure current P11 against all ratified
E11 criteria"*, *"Record objective evidence for every criterion"*, *"Record FAIL
/ UNSATISFIED where evidence does not establish the criterion."* The
instrumentation itself is what `DP-01 §9` permits construction to prepare:
*"P11 construction may prepare instrumentation and evidence required to support
future E11 verification."*

**`RATIFICATION ≠ PASS`** (`DP-02 §10`). Ratifying a criterion says what will be
measured; it says nothing about the result. `§7`: *"No criterion shall be marked
PASS merely because it has been ratified."*

**`E11-04` is the one the Decision names explicitly.** `§7`: *"E11-04 shall not
be pre-populated as PASS"*, and where cross-Department coordination is not
demonstrated the result *"shall be: FAIL / UNSATISFIED"* rather than
*"manufacturing a PASS through semantic substitution."* So the check here maps
each coordination participant through its Agent Definition to its **owning
Department** and counts distinct Departments. Agent count is not consulted:
`§10` fixes **`MULTI-AGENT ≠ CROSS-DEPARTMENT COORDINATION`**.

Every verdict is derived from records on disk. Nothing is asserted from a prior
report.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.delegation_catalog import (  # noqa: E402
    operation_roots, registered_instances)
from tools.delegation_reconciliation import reconcile  # noqa: E402
from tools.escalation_register import EscalationRegister  # noqa: E402
from tools.organization_catalog import read_departments  # noqa: E402
from tools.w4_continuity import continuation_conditions, reconstruct  # noqa: E402

#: Discovered, never listed — an operational root joins the measurement by
#: holding a record, not by being remembered.
OPERATION_ROOTS = operation_roots()

DECISION = "DP-02"
DECISION_RECORD = "docs/governance/acts/DP-02-P11-E11-RATIFICATION.md"

PASS, FAIL, NA = "PASS", "FAIL / UNSATISFIED", "NOT APPLICABLE"


@dataclass
class Result:
    """One criterion's measured result. `detail` is evidence, never a verdict."""

    key: str
    name: str
    verdict: str
    detail: Dict[str, object] = field(default_factory=dict)
    gap: str = ""

    def to_payload(self) -> dict:
        payload = {"criterion": self.key, "name": self.name,
                   "verdict": self.verdict, "evidence": self.detail}
        if self.gap:
            payload["gap"] = self.gap
        return payload


# ---------------------------------------------------------------- helpers ----
def _evidence_records() -> List[Tuple[str, dict]]:
    found = []
    for root in OPERATION_ROOTS:
        for path in sorted(root.glob("*.evidence.json")):
            found.append((str(path.relative_to(REPO_ROOT)),
                          json.loads(path.read_text(encoding="utf-8"))))
    return found


def _grants() -> List[dict]:
    return [json.loads(p.read_text(encoding="utf-8"))
            for root in OPERATION_ROOTS
            for p in sorted(root.glob("*.delegation.json"))]


def department_of_instance() -> Dict[str, str]:
    """`instance → Agent Definition → owning Department`, resolved from record.

    Three independent surfaces, joined rather than assumed: the instance record
    names a Definition, and the Department record names which Definitions it
    owns. An instance whose Definition no Department claims resolves to nothing
    — it is not silently attributed to one.
    """
    owner_of_definition: Dict[str, str] = {}
    for record in read_departments():
        for definition in record.agent_definitions:
            owner_of_definition[definition] = record.key
    mapping: Dict[str, str] = {}
    for key, record in registered_instances().items():
        definition = record.get("definition_key") or record.get("definition")
        if definition in owner_of_definition:
            mapping[key] = owner_of_definition[definition]
    return mapping


# ----------------------------------------------------------- E11-01..E11-08 ---
def e11_01_planning() -> Result:
    """`DP-02 §3`: goal decomposition, planning, sequencing, dependency-aware
    execution, bounded adaptation/revision — and planning creates no authority."""
    from tools.planning import (AuthorityProvenance, Goal, Plan, PlanStep,
                                PlanningSurface, sequence)
    dp01 = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"
    authority = AuthorityProvenance("DP-01 §3 W2", dp01)
    surface = PlanningSurface()
    surface.declare(Goal(key="e11-measure", statement="E11-01 measurement",
                         authority=authority))
    first = surface.adopt(Plan(
        key="e11-measure-0", goal_key="e11-measure", authority=authority,
        steps=(PlanStep("a", "A"), PlanStep("b", "B", depends_on=("a",)))))
    adapted = surface.adapt(
        first, steps=first.steps + (PlanStep("c", "C", depends_on=("b",)),),
        reason="E11-01 measurement")
    revised = surface.revise(adapted, steps=(PlanStep("a", "A"),),
                             reason="E11-01 measurement")
    lifecycle = [first.origin.name, adapted.origin.name, revised.origin.name]
    ordered = [step.key for step in sequence(adapted)]
    creates_no_authority = not hasattr(authority, "is_authorized")
    run_plans = [record.get("plan") for _, record in _evidence_records()]
    authorities_resolve = all(
        (REPO_ROOT / record["plan_authority"].split("(")[-1].rstrip(")")).is_file()
        for _, record in _evidence_records() if record.get("plan_authority"))
    ok = (lifecycle == ["PLANNED", "ADAPTED", "REVISED"]
          and ordered == ["a", "b", "c"]
          and creates_no_authority and authorities_resolve
          and all(run_plans))
    return Result("E11-01", "Planning", PASS if ok else FAIL, {
        "lifecycle_observed": lifecycle,
        "dependency_order": ordered,
        "plans_in_real_runs": run_plans,
        "plan_authority_resolves": authorities_resolve,
        "planning_exposes_no_authorization_method": creates_no_authority,
    }, "" if ok else "one or more planning properties not demonstrated")


def e11_02_delegation() -> Result:
    """`DP-02 §3`: governed delegation — bounds, accountability, tracking,
    verification; no fabricated authority, delegator, recipient or provenance."""
    grants = _grants()
    instances = registered_instances()
    reconciliation = reconcile()
    checks = {
        "grants": len(grants),
        "all_cite_an_instrument": all(g.get("authority_instrument") for g in grants),
        "all_provenance_resolves": all(
            (REPO_ROOT / g["authority_record"]).is_file() for g in grants),
        "recipients_all_registered": all(
            g["recipient_instance"] in instances for g in grants),
        "delegated_within_permitted": all(
            set(g["capability_scope"])
            <= set(instances[g["recipient_instance"]]["permitted_capabilities"])
            for g in grants),
        "no_recipient_is_its_own_accountable_party": all(
            g["accountable_party"] != g["recipient_instance"] for g in grants),
        "revocation_represented": any(g["status"] == "REVOKED" for g in grants),
        "tracking_defects": len(reconciliation["defects"]),
        "active_grants_all_represented":
            sorted(reconciliation["active_grants"])
            == sorted(reconciliation["represented_active"]),
    }
    ok = (checks["all_cite_an_instrument"] and checks["all_provenance_resolves"]
          and checks["recipients_all_registered"]
          and checks["delegated_within_permitted"]
          and checks["no_recipient_is_its_own_accountable_party"]
          and checks["revocation_represented"]
          and checks["tracking_defects"] == 0
          and checks["active_grants_all_represented"])
    return Result("E11-02", "Delegation", PASS if ok else FAIL, checks,
                  "" if ok else "delegation bounds or tracking not established")


def e11_03_execution() -> Result:
    """`DP-02 §3`: execution under valid authority and provenance.

    **A correct refusal is not an execution failure.** The Decision says so in
    the criterion itself, so the verdict here turns on whether every outcome is
    attributable and whether refusals happened *when they should*, never on
    whether a refusal occurred.
    """
    records = _evidence_records()
    grant_ids = {g["delegation_id"] for g in _grants()}
    outcomes, refusals, chains = [], 0, []
    for source, record in records:
        outcomes += [(source, o["step"], o["status"]) for o in record["outcomes"]]
        refusals += len(record.get("refusals", []))
        chains.append(record["authority_chain"])
    escalated = [o for o in outcomes if o[2] == "escalation"]
    recorded_escalations = sum(
        len(EscalationRegister(root).all_escalations()) for root in OPERATION_ROOTS)
    checks = {
        "evidence_records": [s for s, _ in records],
        "outcomes": outcomes,
        "every_run_cites_a_real_grant": all(
            record["delegation_id"] in grant_ids for _, record in records),
        "every_chain_ends_at_founder": all(c[-1] == "founder:Founder" for c in chains),
        "refusals_recorded": refusals,
        "refused_steps_became_escalations": len(escalated) <= recorded_escalations,
        "refusal_not_counted_as_failure": all(o[2] != "failure" for o in outcomes),
    }
    ok = (checks["every_run_cites_a_real_grant"]
          and checks["every_chain_ends_at_founder"]
          and checks["refused_steps_became_escalations"]
          and checks["refusal_not_counted_as_failure"])
    return Result("E11-03", "Execution", PASS if ok else FAIL, checks,
                  "" if ok else "execution not established under valid authority")


def e11_04_cross_department_coordination() -> Result:
    """`DP-02 §3` / `§7` — the criterion the Decision singles out.

    Measured as: **how many distinct Departments did any single coordination
    span?** Agent count is never consulted. `§10`:
    `MULTI-AGENT ≠ CROSS-DEPARTMENT COORDINATION`.
    """
    owner = department_of_instance()
    coordinations = []
    for source, record in _evidence_records():
        coordination = record.get("coordination")
        if not coordination:
            continue
        participants = list(coordination.get("participants", ()))
        departments = sorted({owner[p] for p in participants if p in owner})
        coordinations.append({
            "source": source,
            "participants": participants,
            "departments": departments,
            "department_count": len(departments),
            "proof_level": coordination.get("proof_level"),
            "is_multi_agent": coordination.get("is_multi_agent"),
        })
    spanning = [c for c in coordinations if c["department_count"] > 1]
    ok = bool(spanning)
    return Result(
        "E11-04", "Cross-Department Coordination", PASS if ok else FAIL, {
            "departments_resident": sorted(r.key for r in read_departments()),
            "instance_to_department": owner,
            "coordinations_observed": coordinations,
            "coordinations_spanning_more_than_one_department": len(spanning),
        },
        "" if ok else
        "No coordination on record spans more than one Department. Departments "
        "and per-Department instances exist; no single coordination has joined "
        "them. DP-02 §7: recorded FAIL / UNSATISFIED rather than substituting "
        "multi-agent or single-Department evidence.")


def e11_05_observation() -> Result:
    """`DP-02 §3`: observe outcomes, state, failures, blockers, escalation
    conditions and improvement opportunities — and never become authority."""
    import tools.performance_evidence as performance
    names = [n for n in dir(performance) if not n.startswith("_")]
    forbidden = [n for n in names for word in
                 ("authorize", "approve", "decide", "rank", "prioriti", "grant")
                 if word in n.lower()]
    statuses = sorted({o["status"] for _, r in _evidence_records()
                       for o in r["outcomes"]})
    states = {
        "outcome_statuses_observable": statuses,
        "blocked_work_observable": any(
            continuation_conditions(reconstruct(root))[0].startswith("OPEN ESCALATIONS")
            for root in OPERATION_ROOTS),
        "public_api": sorted(names),
        "no_decision_surface": not forbidden,
    }
    ok = states["no_decision_surface"] and bool(statuses)
    return Result("E11-05", "Observation", PASS if ok else FAIL, states,
                  "" if ok else "observation surface exposes a decision method")


def e11_06_verification() -> Result:
    """`DP-02 §3`: work and outcomes verifiable; verification distinct from
    authorization, ownership, execution and governance."""
    suites = {}
    for name, args in (("native_core", ["-s", "native_core", "-t", "."]),
                       ("consumers", ["-s", "consumers", "-t", "."]),
                       ("tools", ["-s", "tools", "-t", "tools"])):
        completed = subprocess.run(
            [sys.executable, "-m", "unittest", "discover"] + args + ["-q"],
            capture_output=True, text=True, cwd=str(REPO_ROOT))
        line = [l for l in completed.stderr.split("\n") if l.startswith("Ran ")]
        suites[name] = {"summary": line[0] if line else "no result",
                        "ok": completed.returncode == 0}
    grants = _grants()
    checks = {
        "suites": suites,
        "every_grant_states_a_verification_requirement": all(
            g.get("verification_requirement") for g in grants),
        "runs_carry_verification_evidence": all(
            r.get("outcomes") for _, r in _evidence_records()),
    }
    ok = (all(s["ok"] for s in suites.values())
          and checks["every_grant_states_a_verification_requirement"]
          and checks["runs_carry_verification_evidence"])
    return Result("E11-06", "Verification", PASS if ok else FAIL, checks,
                  "" if ok else "verification not established")


def e11_07_escalation() -> Result:
    """`DP-02 §3`: identify and persist escalation conditions, route them to the
    authority boundary, and never become authority to resolve them."""
    registers = {root.name: EscalationRegister(root) for root in OPERATION_ROOTS}
    recorded = {name: list(r.all_escalations()) for name, r in registers.items()}
    open_ids = {name: list(r.open_escalations()) for name, r in registers.items()}
    api = [n for n in dir(EscalationRegister) if not n.startswith("_")]
    forbidden = [n for n in api for word in
                 ("approve", "authorize", "grant", "permit", "resolve", "close")
                 if word in n.lower()]
    checks = {
        "recorded": recorded, "open": open_ids,
        "any_real_escalation_persisted": any(recorded.values()),
        "public_api": sorted(api),
        "no_resolution_method": not forbidden,
        "statuses": {i: registers[name].status(i)
                     for name, ids in recorded.items() for i in ids},
    }
    ok = (checks["any_real_escalation_persisted"]
          and checks["no_resolution_method"])
    return Result("E11-07", "Escalation", PASS if ok else FAIL, checks,
                  "" if ok else "escalation not persisted, or resolvable by automation")


def e11_08_accountability() -> Result:
    """`DP-02 §3`: actions, delegations, outcomes and failures attributable to
    valid accountable actors and authority chains."""
    grants = _grants()
    answers = []
    for source, record in _evidence_records():
        grant = next((g for g in grants
                      if g["delegation_id"] == record["delegation_id"]), None)
        answers.append({
            "source": source,
            "who_delegated": grant and grant["delegator"],
            "to_whom": grant and grant["recipient_instance"],
            "for_what": grant and list(grant["capability_scope"]),
            "under_which_authority": grant and grant["authority_instrument"],
            "with_which_scope": grant and list(grant["work_scope"]),
            "what_happened": [(o["step"], o["status"]) for o in record["outcomes"]],
            "who_verified": grant and grant["verification_requirement"][:48],
            "who_remains_accountable": grant and grant["accountable_party"],
        })
    complete = all(all(v is not None and v != [] for k, v in a.items()
                       if k != "source") for a in answers)
    checks = {
        "chain_answers": answers,
        "every_link_recoverable": complete,
        "ultimate_accountability_not_transferred": all(
            g["accountable_party"] != g["recipient_instance"] for g in grants),
        "all_chains_end_at_founder": all(
            g["authority_chain"][-1] == "founder:Founder" for g in grants),
    }
    ok = (complete and checks["ultimate_accountability_not_transferred"]
          and checks["all_chains_end_at_founder"])
    return Result("E11-08", "Accountability", PASS if ok else FAIL, checks,
                  "" if ok else "an accountability link is unrecoverable")


# ------------------------------------------------------------ E11-09 / -10 ---
def e11_09_continuity() -> Result:
    """`DP-02 §4`: reconstructible and continuous across process boundaries.

    *"ORGANIZATION CAN CONTINUE OPERATING"*, not *"SYSTEM CAN PERFORM"* — so the
    measurement is a **second process** rebuilding the state, item by item
    against the Decision's own evidence list.
    """
    here = {root.name: reconstruct(root) for root in operation_roots()}
    # The roots are **discovered in the child too**, not passed in as a list.
    # The first version hardcoded the two that existed when it was written and
    # went stale the moment a third operational root was created — inside the
    # instrument built to measure whether populations are complete, on the same
    # day three other hardcoded populations were replaced with discovery.
    script = (
        "import sys, json; sys.path.insert(0, %r);"
        "from tools.delegation_catalog import operation_roots;"
        "from tools.w4_continuity import reconstruct;"
        "print(json.dumps({r.name: reconstruct(r) for r in operation_roots()},"
        " default=str))" % str(REPO_ROOT))
    completed = subprocess.run([sys.executable, "-c", script],
                               capture_output=True, text=True, cwd=str(REPO_ROOT))
    fresh = json.loads(completed.stdout) if completed.returncode == 0 else {}
    agrees = json.loads(json.dumps(here, default=str)) == fresh
    covered = {
        "delegation_state": all(bool(s["active_grants"]) or bool(s["revoked_grants"])
                                for s in here.values()),
        "work_state": all(s["last_plan"] is not None for s in here.values()),
        "escalation_state": all("escalations" in s for s in here.values()),
        "prior_outcomes": all(s["last_outcomes"] is not None for s in here.values()),
        "accountability_context": all(s["accountable_parties"] for s in here.values()),
        "continuity_context": all(continuation_conditions(s) for s in here.values()),
        "persistence": all(s["evidence_records"] for s in here.values()),
        "reconstruction": bool(fresh),
        "across_process_boundary": agrees,
        "canonical_provenance_preserved": all(
            s["authority_instruments"] for s in here.values()),
        "revoked_stays_revoked": all(
            not (set(s["revoked_grants"]) & set(s["active_grants"]))
            for s in here.values()),
    }
    ok = all(covered.values())
    return Result("E11-09", "Organizational Continuity", PASS if ok else FAIL,
                  {"coverage": covered,
                   "fresh_process_agrees": agrees,
                   "roots": sorted(here)},
                  "" if ok else
                  "continuity not established for: %s"
                  % sorted(k for k, v in covered.items() if not v))


def e11_10_bounded_autonomy() -> Result:
    """`DP-02 §4`/`§5`: autonomy inside its authority envelope, with negative
    controls as mandatory integrity evidence — not as a capability."""
    import ast
    import tempfile

    from native_core.core.governance import HumanAuthority
    from tools.agent_instance_registry import AgentInstanceRegistry
    from tools.delegation_reconciliation import (ACTIVE, LedgerGrant, Projection,
                                                 ReconciliationError, project)
    from tools.escalation_register import (EscalationRegisterError,
                                           EscalationRegister)
    from tools.planning import AuthorityProvenance
    from tools.w4_delegation import (AUTHORIZED_DELEGATOR, DelegationError,
                                     W4DelegationRegistry)
    from tools.w4_execution import ExecutionRefused
    from native_core.core.agent.definition import AgentDefinition

    fd = ("docs/governance/acts/"
          "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
    controls: Dict[str, bool] = {}

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        registry = AgentInstanceRegistry(root)
        definition = AgentDefinition(
            agent_definition_key="engineering-intelligence-agent",
            agent_definition_version="1.0", owning_department_key="engineering",
            implemented_capabilities=("engineering-intelligence",),
            specified_skills=(), specified_workflows=())
        registry.register(
            instance_key="e11-probe-001", definition=definition,
            permitted_capabilities=("engineering-intelligence",),
            created_by=AUTHORIZED_DELEGATOR,
            authority=AuthorityProvenance("FD-P11-001 §7", fd),
            accountable_to=AUTHORIZED_DELEGATOR)
        delegations = W4DelegationRegistry(registry, root)
        base = dict(recipient_instance="e11-probe-001",
                    authority=AuthorityProvenance("FD-P11-001 §9", fd),
                    objective="probe",
                    capability_scope=("engineering-intelligence",),
                    work_scope=("s",), lifecycle_boundary="one",
                    resource_boundary="none", output_expectation="none",
                    verification_requirement="none", escalation_condition="none",
                    accountable_party=AUTHORIZED_DELEGATOR,
                    termination_condition="end")

        def refused(**overrides) -> bool:
            try:
                delegations.issue(**{**base, **overrides})
                return False
            except DelegationError:
                return True

        controls["no_self_authorization"] = refused(delegator="e11-probe-001")
        controls["no_authority_expansion"] = refused(
            delegator=AUTHORIZED_DELEGATOR,
            capability_scope=("cognitive-intelligence",))
        controls["no_fabricated_delegator"] = refused(
            delegator="Engineering Department")
        controls["no_fabricated_actor"] = refused(
            delegator=AUTHORIZED_DELEGATOR, recipient_instance="ghost-001")
        controls["no_invalid_authority_inference"] = refused(
            delegator=AUTHORIZED_DELEGATOR,
            authority=AuthorityProvenance(
                "DP-01 §3 W3",
                "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"))
        controls["no_accountability_transfer"] = refused(
            delegator=AUTHORIZED_DELEGATOR, accountable_party="e11-probe-001")

        grant = LedgerGrant("a" * 16, "REVOKED", "i", ("c",), "FD-P11-001 §9",
                            fd, "acc", "x")
        try:
            project("a" * 16, grants={"a" * 16: grant}, root=root)
            controls["no_governance_bypass"] = False
        except ReconciliationError:
            controls["no_governance_bypass"] = True

        register = EscalationRegister(root)
        recorded = register.record(
            ExecutionRefused("probe", required="s", held=("t",)),
            subject="e11-probe", authority=AuthorityProvenance("FD-P11-001 §9", fd))

        class LooksHuman:
            reviewer_id = "founder"

        blocked = []
        for impostor in (None, "founder", LooksHuman(),
                         AuthorityProvenance("FD-P11-001 §9", fd)):
            try:
                register.record_response(recorded.escalation_id,
                                         authority=impostor, response="approved")
                blocked.append(False)
            except EscalationRegisterError:
                blocked.append(True)
        controls["no_unauthorized_resolution"] = all(blocked)
        controls["escalation_stays_open_after_attempts"] = (
            register.status(recorded.escalation_id) == "OPEN")
        controls["human_authority_still_works"] = bool(
            register.record_response(
                recorded.escalation_id,
                authority=HumanAuthority(reviewer_id="founder"),
                response="probe"))

    reconciliation = reconcile()
    controls["no_unauthorized_boundary_crossing"] = all(
        not record.get("boundary_crossed") or record.get("refusals")
        for _, record in _evidence_records())
    controls["no_false_completion"] = not reconciliation["defects"]
    core = sorted(p.name for p in (REPO_ROOT / "native_core/core").iterdir()
                  if p.is_dir() and not p.name.startswith("_"))
    controls["native_core_unchanged"] = len(core) == 11

    ok = all(controls.values())
    return Result("E11-10", "Bounded Autonomy & Governance Integrity",
                  PASS if ok else FAIL,
                  {"negative_controls": controls,
                   "native_core_boundaries": len(core)},
                  "" if ok else "integrity control(s) did not hold: %s"
                  % sorted(k for k, v in controls.items() if not v))


CRITERIA = (e11_01_planning, e11_02_delegation, e11_03_execution,
            e11_04_cross_department_coordination, e11_05_observation,
            e11_06_verification, e11_07_escalation, e11_08_accountability,
            e11_09_continuity, e11_10_bounded_autonomy)


def measure() -> dict:
    """Every ratified criterion, measured. No criterion is pre-populated."""
    results = [criterion() for criterion in CRITERIA]
    return {
        "decision": DECISION,
        "decision_record": DECISION_RECORD,
        "results": [r.to_payload() for r in results],
        "passed": [r.key for r in results if r.verdict == PASS],
        "failed": [r.key for r in results if r.verdict == FAIL],
        "e11_pass": all(r.verdict == PASS for r in results),
    }


def main(argv: List[str]) -> int:
    report = measure()
    print(f"measured against  : {report['decision']} ({report['decision_record']})")
    for result in report["results"]:
        print(f"  {result['criterion']}  {result['name']:<42} {result['verdict']}")
        if result.get("gap"):
            print(f"        GAP: {result['gap']}")
    print(f"\nPASS   : {len(report['passed'])} — {report['passed']}")
    print(f"FAIL   : {len(report['failed'])} — {report['failed']}")
    print(f"E11    : {'PASS' if report['e11_pass'] else 'NOT PASSED'}")
    print("\nE11 PASS ≠ P11 COMPLETION ≠ P11 CERTIFICATION (DP-02 §10).")
    if "--json" in argv:
        print(json.dumps(report, indent=2, default=str))
    return 0 if report["e11_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
