"""`P11-W4` — the Delegation authorized by `FD-P11-001`.

`§9`: *"Every W4 Delegation must have explicit provenance to FD-P11-001 and the
applicable authority chain."* The valid model is

    FOUNDER → FD-P11-001 → AUTHORIZED W4 DELEGATOR
            → AUTHORIZED AGENT INSTANCE → BOUNDED DELEGATION → W4 EXECUTION

and `§9` names the invalid one explicitly: `DP-01 → somehow create Delegation`.
`§10`: **`DP-01 ≠ SPECIFIC W4 DELEGATION`.**

**Why this is separate from `tools/delegation_catalog.py`.** That module is W3 —
the *organizational* delegation relation between units, read from resident
records, whose population is legitimately `0` because no unit-level delegator
exists. This is the **W4 operational** delegation from the authorized delegator
to a registered Agent Instance, which `FD-P11-001 §20` distinguishes: W3 *"may
represent and track the Delegation authorized by FD-P11-001, but W3
implementation must not manufacture authority absent valid provenance."* The two
are different relations at different levels; collapsing them would let a W4
operational grant appear as a unit-to-unit organizational delegation nobody
issued.

**`DELEGATION ≠ AUTHORITY CREATION`** (`§16`), stated formally in the Decision:

    Delegated Authority ≤ Available Delegator Authority
                        ∩ FD-P11-001 Scope
                        ∩ Canonical Boundaries

That inequality is enforced here as an intersection, not a promise: the granted
capability surface is checked against the instance's permitted surface, and a
grant exceeding it fails closed.

**`§14` — no self-authorization.** The delegator is not whoever calls this
module. It is the party `FD-P11-001 §4.1` names, and a delegation citing any
other delegator is refused. The Decision forbids the pattern where Claude
*"creates itself as delegator"*; the delegator is therefore a constant read from
the Decision, not a parameter a caller supplies freely.

**`§12.12` — no approving one's own delegation.** An instance may not be its own
accountable party, and `§17` forbids an instance authorizing another
(`NC-W4-17`, `NC-W4-18`).
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

from tools.agent_instance_registry import (
    AgentInstanceRegistry,
    InstanceRegistration,
    REGISTERED,
)
from tools import authority_citation
from tools.planning import AuthorityProvenance

#: `§4.1`. The delegator is fixed by the Decision, not chosen by a caller.
#: `§5` explicitly rejects Engineering or Platform becoming the delegator by
#: virtue of being labels, so neither may be substituted here.
AUTHORIZED_DELEGATOR = "Claude Code / AIOS Co-Founder"

#: `§15`. Ultimate human governance accountability does not move.
ULTIMATE_ACCOUNTABILITY = "Founder"

AUTHORIZING_DECISION = "FD-P11-001"

#: `§13`'s thirteen elements, **plus one that is mine and is labelled as mine.**
#:
#: `§13` lists: `DELEGATION ID · DELEGATOR · RECIPIENT AGENT INSTANCE ·
#: AUTHORITY PROVENANCE · OBJECTIVE · CAPABILITY SCOPE · WORK SCOPE ·
#: TIME / LIFECYCLE BOUNDARY · RESOURCE BOUNDARY · OUTPUT EXPECTATION ·
#: VERIFICATION REQUIREMENT · ESCALATION CONDITION · ACCOUNTABLE PARTY` — and a
#: Delegation missing any of them *"is incomplete and must not become executable
#: W4 authority."* That is **thirteen**.
#:
#: ``termination_condition`` is the fourteenth and **`§13` does not list it.**
#: This comment previously said *"`§13`, verbatim"*, which was false, and
#: elsewhere I wrote that *"`§13` item 14 requires a termination condition"* —
#: a miscount of a thirteen-item list that then propagated into six documents.
#: The instrument contains no termination requirement at all; the word does not
#: appear in it.
#:
#: The field is **kept**, because `§29` makes a Delegation *"a controlled
#: lifecycle object rather than a permanent authority grant"* and a grant with
#: no stated ending is the unbounded authority `§11` forbids. Requiring more
#: than `§13` requires is sound; **claiming `§13` requires it was not.**
#: Corrected under `ACT-CC-P11-017`.
REQUIRED_ELEMENTS = (
    "delegation_id", "delegator", "recipient_instance", "authority_provenance",
    "objective", "capability_scope", "work_scope", "lifecycle_boundary",
    "resource_boundary", "output_expectation", "verification_requirement",
    "escalation_condition", "accountable_party", "termination_condition",
)

#: `§29`: a Delegation is *"a controlled lifecycle object rather than a
#: permanent authority grant."* A grant that cannot be withdrawn is exactly the
#: unrestricted authority `FD-P11-001 §11` forbids — so revocation is not an
#: optional convenience, it is what makes the grant bounded in time as well as
#: in scope.
ACTIVE, REVOKED = "ACTIVE", "REVOKED"


class DelegationError(RuntimeError):
    """Fail closed (`PR-4`). `§26`: missing any component means `BLOCKED`."""


@dataclass(frozen=True)
class W4Delegation:
    """A bounded, provenance-bearing grant to one registered Agent Instance."""

    delegation_id: str
    delegator: str
    recipient_instance: str
    authority: AuthorityProvenance
    objective: str
    capability_scope: Tuple[str, ...]
    work_scope: Tuple[str, ...]
    lifecycle_boundary: str
    resource_boundary: str
    output_expectation: str
    verification_requirement: str
    escalation_condition: str
    accountable_party: str
    termination_condition: str
    issued_at: str
    status: str = ACTIVE

    def is_executable(self) -> bool:
        """Whether this grant may still be acted on. **Not a permission check
        for anything else** — a revoked delegation authorizes nothing, and an
        active one authorizes only what its scope names."""
        return self.status == ACTIVE

    def authority_chain(self) -> Tuple[str, ...]:
        """`§24`'s required trace, bottom-up. Evidence, not permission."""
        return (f"delegation:{self.delegation_id}",
                f"delegator:{self.delegator}",
                f"decision:{self.authority.instrument}",
                f"founder:{ULTIMATE_ACCOUNTABILITY}")

    def permits(self, capability: str) -> bool:
        """Whether this grant covers a capability. **Not an authorization check
        for anything else** — it answers only what this delegation says."""
        return capability in self.capability_scope

    def to_payload(self) -> dict:
        return {
            "delegation_id": self.delegation_id, "delegator": self.delegator,
            "recipient_instance": self.recipient_instance,
            "authority_instrument": self.authority.instrument,
            "authority_record": self.authority.record,
            "objective": self.objective,
            "capability_scope": list(self.capability_scope),
            "work_scope": list(self.work_scope),
            "lifecycle_boundary": self.lifecycle_boundary,
            "resource_boundary": self.resource_boundary,
            "output_expectation": self.output_expectation,
            "verification_requirement": self.verification_requirement,
            "escalation_condition": self.escalation_condition,
            "accountable_party": self.accountable_party,
            "termination_condition": self.termination_condition,
            "status": self.status,
            "issued_at": self.issued_at,
            "authority_chain": list(self.authority_chain()),
        }


class W4DelegationRegistry:
    """Issues delegations. Holds no authority of its own."""

    def __init__(self, registry: AgentInstanceRegistry,
                 root: Optional[Path] = None):
        self._instances = registry
        self._root = root
        if root is not None:
            root.mkdir(parents=True, exist_ok=True)
        self._issued: Dict[str, W4Delegation] = {}

    def issue(self, *, delegator: str, recipient_instance: str,
              authority: AuthorityProvenance, objective: str,
              capability_scope: Tuple[str, ...], work_scope: Tuple[str, ...],
              lifecycle_boundary: str, resource_boundary: str,
              output_expectation: str, verification_requirement: str,
              escalation_condition: str, accountable_party: str,
              termination_condition: str) -> W4Delegation:
        """Issue one bounded delegation. Every `§13` element is required."""
        # `§14`: the delegator is the one the Decision names.
        if delegator != AUTHORIZED_DELEGATOR:
            raise DelegationError(
                f"{delegator!r} is not the authorized W4 delegator — "
                f"`FD-P11-001 §4.1` names {AUTHORIZED_DELEGATOR!r}, and `§5` "
                "rejects Engineering or Platform becoming delegator by label")

        # `§24`: provenance to this Decision specifically.
        if not isinstance(authority, AuthorityProvenance):
            raise DelegationError("a delegation requires a validated citation")
        if AUTHORIZING_DECISION not in authority.instrument:
            raise DelegationError(
                f"a W4 delegation must cite {AUTHORIZING_DECISION}; "
                f"{authority.instrument!r} is insufficient — `§9`: "
                "'DP-01 → somehow create Delegation' is invalid")
        # `§24`: the chain must actually reach the Decision. A citation that
        # names it but points elsewhere produces no chain (`GOAL-V2-005`).
        unreached = authority_citation.refusal(
            authority.instrument, authority.record, AUTHORIZING_DECISION)
        if unreached:
            raise DelegationError(
                f"`§24` provenance does not reach {AUTHORIZING_DECISION}: "
                f"{unreached}")

        # `§6.1`: only a registered instance may receive.
        if not self._instances.is_registered(recipient_instance):
            raise DelegationError(
                f"{recipient_instance!r} is not a registered Agent Instance — "
                "`§6.1`: an Agent Definition alone is insufficient")
        registration: InstanceRegistration = self._instances.get(
            recipient_instance)
        if registration.lifecycle != REGISTERED:
            raise DelegationError(
                f"instance {recipient_instance!r} is {registration.lifecycle}; "
                "a delegation may only be issued to a live instance")

        # `§16`: delegated ≤ available. Enforced as an intersection.
        scope = tuple(capability_scope or ())
        if not scope:
            raise DelegationError("a delegation requires a capability scope")
        beyond = [c for c in scope
                  if c not in registration.permitted_capabilities]
        if beyond:
            raise DelegationError(
                f"delegation exceeds the instance's permitted surface: {beyond} "
                "— `§16`: a delegator may not grant more authority than the "
                "recipient may hold")

        # `§12.12` / `§15`: accountability is real and is not the recipient.
        if accountable_party == recipient_instance:
            raise DelegationError(
                "the recipient cannot be its own accountable party — "
                "`§15` fixes instance → delegator → Founder, and `§12` forbids "
                "approving one's own delegation")

        values = dict(
            delegation_id=uuid.uuid4().hex[:16], delegator=delegator,
            recipient_instance=recipient_instance,
            authority_provenance=authority, objective=objective,
            capability_scope=scope, work_scope=tuple(work_scope or ()),
            lifecycle_boundary=lifecycle_boundary,
            resource_boundary=resource_boundary,
            output_expectation=output_expectation,
            verification_requirement=verification_requirement,
            escalation_condition=escalation_condition,
            accountable_party=accountable_party,
            termination_condition=termination_condition,
        )
        missing = [name for name in REQUIRED_ELEMENTS
                   if not values.get(name)]
        if missing:
            raise DelegationError(
                f"delegation is incomplete, missing {missing} — `§13`: it "
                "'must not become executable W4 authority'")

        delegation = W4Delegation(
            delegation_id=values["delegation_id"], delegator=delegator,
            recipient_instance=recipient_instance, authority=authority,
            objective=objective, capability_scope=scope,
            work_scope=values["work_scope"],
            lifecycle_boundary=lifecycle_boundary,
            resource_boundary=resource_boundary,
            output_expectation=output_expectation,
            verification_requirement=verification_requirement,
            escalation_condition=escalation_condition,
            accountable_party=accountable_party,
            termination_condition=termination_condition,
            issued_at=datetime.now(timezone.utc).isoformat())
        self._issued[delegation.delegation_id] = delegation
        if self._root is not None:
            (self._root / f"{delegation.delegation_id}.delegation.json"
             ).write_text(json.dumps(delegation.to_payload(), indent=2),
                          encoding="utf-8")
        return delegation

    def revoke(self, delegation_id: str, *, reason: str) -> W4Delegation:
        """Withdraw a grant. `§29`: `INVALID / REVOKED → NOT EXECUTABLE`.

        Replaces the record with a revoked successor rather than editing it, so
        the terms that were in force remain readable — the same append-only
        discipline the escalation register and the plan chain both follow.

        Revocation is an act of the **delegator**, and it removes authority
        rather than granting any, so it needs no new provenance: nothing can be
        done with a revoked delegation that could not be done with none at all.
        """
        current = self.get(delegation_id)
        if not reason or not reason.strip():
            raise DelegationError("revocation must record why the grant ended")
        revoked = W4Delegation(
            **{**{f: getattr(current, f) for f in current.__dataclass_fields__},
               "status": REVOKED})
        self._issued[delegation_id] = revoked
        if self._root is not None:
            payload = revoked.to_payload()
            payload["revocation_reason"] = reason
            (self._root / f"{delegation_id}.delegation.json").write_text(
                json.dumps(payload, indent=2), encoding="utf-8")
        return revoked

    def get(self, delegation_id: str) -> W4Delegation:
        if delegation_id not in self._issued:
            raise DelegationError(f"no such delegation: {delegation_id!r}")
        return self._issued[delegation_id]

    def for_instance(self, instance_key: str) -> Tuple[W4Delegation, ...]:
        return tuple(d for d in self._issued.values()
                     if d.recipient_instance == instance_key)

    def keys(self) -> Tuple[str, ...]:
        return tuple(sorted(self._issued))


# ---- operational disposition (FD-AGENCY-001 · S-1 · Q-S1-A = A2) -------------
#
# The ledger above writes a grant's **historical status** — `ACTIVE` or
# `REVOKED` — into the delegation record itself. When that record lies in a
# certified evidence root, the status can never move again: the P11 ledger was
# certified by `FD-P11-002`, and `P12-F12` refuses every rewrite. Four grants
# there finished their work and still read `ACTIVE` (S-1, Register `§135`).
#
# The Founder's A2 decision keeps those records as immutable history and allows
# a **live operational ledger outside the certified boundary**. This is that
# ledger, and it is deliberately small:
#
# * it adds **one record per grant**, append-only, beside nothing it describes;
# * it never edits, deletes or reinterprets a delegation record. The historical
#   status stays what the record says; the disposition is a second, separate fact;
# * it accepts a disposition only over a historically `ACTIVE` grant, so a
#   `REVOKED` record is never re-read as anything else;
# * it is bound to the exact bytes of the delegation record (and, for
#   `COMPLETED`, of the evidence) it was recorded against. A reader that finds
#   those bytes changed reports a fault and does not honour it;
# * only the authorized delegator records one (`FD-P11-001 §4.1`). The accountable
#   party does not move.
#
# Semantics (documented in `docs/architecture/agency/W4-OPERATIONAL-LEDGER.md`):
#
#   COMPLETED  the grant's own termination condition "on completion of the bound
#              plan" is met, **computed here from the evidence**, never asserted
#              by a caller: the bound plan's evidence names the grant, every
#              outcome is `success`, no escalation was raised, and every step in
#              the work scope succeeded.
#   REVOKED    the delegator withdrew the grant (`§29` revocation), for a grant
#              whose record cannot be rewritten in place.

COMPLETED = "COMPLETED"
DISPOSITIONS = (COMPLETED, REVOKED)
_REPO_ROOT = Path(__file__).resolve().parent.parent
#: The live operational ledger. It must never lie inside a certified root; the
#: write is guarded, and the reader reports a fault if it ever does.
LIVE_LEDGER = _REPO_ROOT / "docs/architecture/agency/operations/w4-dispositions"
DISPOSITION_AUTHORITY = (
    "FD-AGENCY-001 S-1 Q-S1-A (A2)",
    "docs/governance/acts/FD-AGENCY-001-S1-TERMINAL-STATE-DECISION.md")
_COMPLETION_CLAUSE = "completion of the bound plan"


def _sha256(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(_REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def _bound_plan(record: dict) -> Optional[str]:
    """The plan key in a lifecycle boundary of the form '... of plan <key>'."""
    match = re.search(r"\bplan\s+(\S+)\s*$", record.get("lifecycle_boundary", ""))
    return match.group(1) if match else None


def _names_grant(evidence: dict, delegation_id: str) -> bool:
    return (evidence.get("delegation_id") == delegation_id
            or delegation_id in (evidence.get("grants") or {}).values()
            or any(o.get("delegation") == delegation_id
                   for o in evidence.get("outcomes", [])))


def plan_completion(root: Path, record: dict) -> Tuple[bool, Optional[Path], Tuple[str, ...]]:
    """Whether the grant's bound plan completed, from the root's evidence alone.

    Returns ``(met, evidence_path, reasons_not_met)``. Nothing is assumed: an
    absent, unreadable or ambiguous evidence record is a reason, not a pass.
    """
    reasons = []
    gid = record.get("delegation_id")
    if _COMPLETION_CLAUSE not in record.get("termination_condition", ""):
        reasons.append("termination condition does not name completion of the bound plan")
    plan = _bound_plan(record)
    if plan is None:
        reasons.append("lifecycle boundary names no bound plan")
    matches = []
    for path in sorted(Path(root).glob("*.evidence.json")):
        try:
            evidence = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            reasons.append(f"unreadable evidence record {path.name}")
            continue
        if evidence.get("plan") == plan and _names_grant(evidence, gid):
            matches.append((path, evidence))
    if len(matches) != 1:
        reasons.append(f"{len(matches)} evidence records name plan {plan!r} and "
                       f"grant {gid!r}; exactly one is required")
        return False, None, tuple(reasons)
    path, evidence = matches[0]
    outcomes = evidence.get("outcomes", [])
    if not outcomes:
        reasons.append("the evidence records no outcome")
    bad = [(o["step"], o["status"]) for o in outcomes if o.get("status") != "success"]
    if bad:
        reasons.append(f"not every plan step succeeded: {bad}")
    if evidence.get("escalations"):
        reasons.append(f"the plan raised escalations {evidence['escalations']}")
    terminal = evidence.get("workflow_terminal_state")
    if terminal is not None and "SUCCEEDED" not in terminal:
        reasons.append("the workflow did not reach SUCCEEDED")
    done = {o["step"] for o in outcomes if o.get("status") == "success"}
    missing = [s for s in record.get("work_scope", []) if s not in done]
    if missing:
        reasons.append(f"work-scope steps without a success outcome: {missing}")
    return not reasons, path, tuple(reasons)


def _disposition_path(ledger: Path, root: Path, delegation_id: str) -> Path:
    return Path(ledger) / Path(root).name / f"{delegation_id}.disposition.json"


def record_disposition(root: Path, delegation_id: str, *, disposition: str,
                       delegator: str, reason: str,
                       ledger: Path = LIVE_LEDGER) -> Path:
    """Record a grant's terminal operational disposition in the live ledger.

    The delegation record is read, never written. Refuses, rather than
    records, anything it cannot establish.
    """
    from tools.p12_certified_evidence_guard import guard

    if disposition not in DISPOSITIONS:
        raise DelegationError(f"{disposition!r} is not a disposition {DISPOSITIONS}")
    if delegator != AUTHORIZED_DELEGATOR:
        raise DelegationError(
            f"only {AUTHORIZED_DELEGATOR!r} records a disposition (FD-P11-001 §4.1)")
    if not reason or not reason.strip():
        raise DelegationError("a disposition must record why the grant ended")
    source = Path(root) / f"{delegation_id}.delegation.json"
    if not source.is_file():
        raise DelegationError(f"no such delegation record: {source}")
    record = json.loads(source.read_text(encoding="utf-8"))
    if record.get("delegator") != delegator:
        raise DelegationError("the recording party is not the grant's delegator")
    if record.get("status") != ACTIVE:
        raise DelegationError(
            f"historical status is {record.get('status')!r}: a disposition is "
            "recorded only over an ACTIVE grant, never over a revoked one")
    evidence = None
    if disposition == COMPLETED:
        met, evidence, reasons = plan_completion(root, record)
        if not met:
            raise DelegationError(
                "termination by completion is not established: " + "; ".join(reasons))

    target = _disposition_path(ledger, root, delegation_id)
    guard(target)                       # before any directory is created
    if target.exists():
        raise DelegationError(
            f"{delegation_id} already has a disposition; the ledger is append-only")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "delegation_id": delegation_id,
        "root": _rel(Path(root)),
        "disposition": disposition,
        "historical_status": record["status"],
        "record_sha256": _sha256(source),
        "evidence": None if evidence is None else _rel(evidence),
        "evidence_sha256": None if evidence is None else _sha256(evidence),
        "reason": reason,
        "recorded_by": delegator,
        "accountable_party": record.get("accountable_party"),
        "authority_instrument": DISPOSITION_AUTHORITY[0],
        "authority_record": DISPOSITION_AUTHORITY[1],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    guard(target).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return target


def read_dispositions(root: Path, ledger: Path = LIVE_LEDGER
                      ) -> Tuple[Dict[str, dict], Tuple[str, ...]]:
    """The dispositions the live ledger holds for ``root``, and the faults.

    A disposition is honoured only if everything it was recorded against still
    holds; otherwise it is a fault and the grant keeps its historical status.
    """
    from tools.p12_certified_evidence_guard import is_protected

    valid: Dict[str, dict] = {}
    faults = []
    folder = Path(ledger) / Path(root).name
    if not folder.is_dir():
        return valid, ()
    if is_protected(folder):
        return valid, (f"live ledger {folder} lies inside a certified root; "
                       "no disposition there is honoured",)
    for path in sorted(folder.glob("*.disposition.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            faults.append(f"{path.name}: unreadable")
            continue
        gid = item.get("delegation_id")
        source = Path(root) / f"{gid}.delegation.json"
        problems = []
        if item.get("disposition") not in DISPOSITIONS:
            problems.append(f"unknown disposition {item.get('disposition')!r}")
        if item.get("root") != _rel(Path(root)):
            problems.append(f"recorded for root {item.get('root')!r}")
        if not source.is_file():
            problems.append("its delegation record is missing")
        elif _sha256(source) != item.get("record_sha256"):
            problems.append("its delegation record changed since it was recorded")
        elif json.loads(source.read_text(encoding="utf-8")).get("status") != ACTIVE:
            problems.append("its delegation record is not historically ACTIVE")
        if item.get("recorded_by") != AUTHORIZED_DELEGATOR:
            problems.append("not recorded by the authorized delegator")
        if item.get("disposition") == COMPLETED:
            evidence = _REPO_ROOT / (item.get("evidence") or "")
            if not item.get("evidence") or not evidence.is_file():
                problems.append("its evidence record is missing")
            elif _sha256(evidence) != item.get("evidence_sha256"):
                problems.append("its evidence record changed since it was recorded")
        if path.name != f"{gid}.disposition.json":
            problems.append("file name does not match its delegation id")
        if problems:
            faults.append(f"{path.name}: " + "; ".join(problems))
        else:
            valid[gid] = item
    return valid, tuple(faults)


# ---- plan → delegation (FD-AGENCY-001 · S-2) ---------------------------------
#
# Planning identifies work that needs delegating (`PlanningSurface.
# delegation_requirements`) and, by design, can never turn it into a
# delegation: its `DelegationRequirement` has no delegator field, and
# `ACT-CC-P11-005 §11` forbids converting a plan into a delegation record. The
# conversion therefore belongs to the **delegator**, here, and to no one else.
#
# This is the only new code S-2 needs. It adds no authority, contract field,
# state or provenance store:
#
# * the requirement is re-derived from the surface, so it is genuine and its
#   plan is current (a superseded plan, or a step Planning did not mark for
#   delegation, yields nothing to issue);
# * everything that carries provenance is fixed from the requirement and cannot
#   be supplied by the caller: objective = the step statement; work scope =
#   exactly that one step; lifecycle boundary = "one execution of plan <key>",
#   the convention every W4 grant already uses (parsed by `_bound_plan`);
# * accountability and termination are fixed (`FD-P11-001 §15`; the S-1
#   completion semantics);
# * issuance itself is `W4DelegationRegistry.issue`, unchanged: the delegator,
#   the FD-P11-001 citation, the registered recipient and the capability bound
#   are all enforced there.

TERMINATION_ON_PLAN = "on completion of the bound plan, or revocation"


def issue_from_plan(delegations: W4DelegationRegistry, surface, plan, step_key: str,
                    *, delegator: str, recipient_instance: str,
                    authority: AuthorityProvenance, capability_scope: Tuple[str, ...],
                    resource_boundary: str, output_expectation: str,
                    verification_requirement: str,
                    escalation_condition: str) -> W4Delegation:
    """The delegator issues one bounded grant for one step a plan marked.

    Planning delegates nothing; this is the delegator acting on what Planning
    identified. The caller cannot widen the work, rename the plan or move
    accountability.
    """
    if delegator != AUTHORIZED_DELEGATOR:
        raise DelegationError(
            f"{delegator!r} is not the authorized W4 delegator (FD-P11-001 §4.1); "
            "a plan does not make anyone a delegator")
    requirements = {r.step_key: r for r in surface.delegation_requirements(plan)}
    if step_key not in requirements:
        raise DelegationError(
            f"plan {plan.key!r} does not mark step {step_key!r} as requiring "
            "delegation; only work Planning identified may be delegated from it")
    requirement = requirements[step_key]
    return delegations.issue(
        delegator=delegator, recipient_instance=recipient_instance,
        authority=authority, objective=requirement.scope_described,
        capability_scope=tuple(capability_scope),
        work_scope=(requirement.step_key,),
        lifecycle_boundary=f"one execution of plan {requirement.plan_key}",
        resource_boundary=resource_boundary,
        output_expectation=output_expectation,
        verification_requirement=verification_requirement,
        escalation_condition=escalation_condition,
        accountable_party=delegator,
        termination_condition=TERMINATION_ON_PLAN)


def plan_provenance(record: dict, surface) -> dict:
    """Trace a persisted grant back to the plan step it was issued for.

    Reads only existing fields: the lifecycle boundary names the plan, the work
    scope names the step. Returns what was found and every mismatch; it does not
    decide anything.
    """
    plan_key = _bound_plan(record)
    found = {"plan": plan_key, "step": None, "faults": []}
    scope = record.get("work_scope", [])
    if plan_key is None:
        found["faults"].append("the lifecycle boundary names no plan")
        return found
    plans = [p for goal in surface._goals for p in surface.history(goal)  # noqa: SLF001
             if p.key == plan_key]
    if len(plans) != 1:
        found["faults"].append(f"{len(plans)} plans named {plan_key!r} on the surface")
        return found
    plan = plans[0]
    found.update(goal=plan.goal_key, plan_authority=plan.authority.cited(),
                 plan_current=not surface.is_superseded(plan))
    if len(scope) != 1:
        found["faults"].append(f"work scope {scope} is not exactly one plan step")
        return found
    step = next((s for s in plan.steps if s.key == scope[0]), None)
    if step is None:
        found["faults"].append(f"step {scope[0]!r} is not in plan {plan_key!r}")
        return found
    found["step"] = step.key
    if not step.requires_delegation:
        found["faults"].append(f"step {step.key!r} is not marked for delegation")
    if record.get("objective") != step.statement:
        found["faults"].append("the objective is not the step statement")
    return found
