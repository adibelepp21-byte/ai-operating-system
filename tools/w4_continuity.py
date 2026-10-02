"""`P11-W5` — reconstructing W4 organizational state from persisted record alone.

`ACT-CC-P11-009 §18` asks the question that matters, and states it as *not*
*"Is evidence stored?"* but:

    Can a subsequent execution discover, understand, and correctly continue from
    the state created by previous real executions?

`§19` adds the condition that makes the answer meaningful: the second execution
*"MUST NOT rely on hidden conversational memory."* So everything here reads
**only files**. Nothing is passed in from a previous run, and nothing is cached.

**`MEMORY ≠ AUTHORITY`** (`§21`). What is reconstructed tells the system *what
happened*; it establishes nothing about *what may be authorized*. A recovered
delegation is valid only because its authority provenance is still valid, which
is re-checked rather than remembered — a revoked grant comes back **revoked**,
and a grant whose cited instrument has vanished does not come back at all.

**`§22` — the states that must stay distinguishable.** Collapsing them into
`DONE` is the failure this module exists to prevent:

    missing · stale · duplicate · revoked · superseded
    incomplete · failed · escalated · completed

Each is derived from what the records actually say, never assumed from their
presence. A file existing proves a file exists.

**Historical status and operational disposition (`FD-AGENCY-001` S-1, A2).**
By default this reader reports exactly what the delegation records say. Passed
an ``operational_ledger``, it also honours the live ledger kept outside the
certified boundary (`tools.w4_delegation.read_dispositions`). A grant with a
valid disposition leaves ``active_grants``. Its historical status is still
reported, unchanged, under ``historical_active_grants``. The two are never merged
into one field: a certified record that says `ACTIVE` is history, and the
ledger says what became of it. Semantics:
`docs/architecture/agency/W4-OPERATIONAL-LEDGER.md`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
OPERATIONS = REPO_ROOT / "docs/architecture/p11/w4-operations"


class ContinuityError(RuntimeError):
    """Fail closed (`PR-4`)."""


def _describe(root: Path) -> str:
    try:
        return str(root.relative_to(REPO_ROOT))
    except ValueError:
        return str(root)


def _load(path: Path) -> Optional[dict]:
    """Read one record, or report it unreadable rather than skipping it.

    A malformed record is **not** the same as an absent one. Silently skipping
    it would turn corruption into `missing`, which `§22` forbids collapsing.
    """
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def reconstruct(root: Path = OPERATIONS,
                operational_ledger: Optional[Path] = None,
                response_ledger: Optional[Path] = None) -> dict:
    """`§20`'s eleven items, recovered from disk and nothing else.

    ``operational_ledger`` is opt-in. Left as ``None``, the result is the
    historical reading, byte-for-byte what it was before the live ledger existed.
    ``response_ledger`` is the same for escalation responses recorded outside a
    certified root (`tools.escalation_register.LIVE_RESPONSES`).
    """
    if not root.is_dir():
        raise ContinuityError(f"no persisted W4 state at {root}")

    instances: Dict[str, dict] = {}
    unreadable: List[str] = []
    for path in sorted(root.glob("*.instance.json")):
        record = _load(path)
        if record is None:
            unreadable.append(path.name)
        else:
            instances[record["instance_key"]] = record

    grants: Dict[str, dict] = {}
    for path in sorted(root.glob("*.delegation.json")):
        record = _load(path)
        if record is None:
            unreadable.append(path.name)
        else:
            grants[record["delegation_id"]] = record

    escalations: Dict[str, dict] = {}
    for path in sorted(root.glob("*.escalation.json")):
        record = _load(path)
        if record is None:
            unreadable.append(path.name)
            continue
        answered = (root / f"{record['escalation_id']}.response.json").is_file()
        if not answered and response_ledger is not None:
            from tools.escalation_register import EscalationRegister
            answered = EscalationRegister(root, response_ledger).status(
                record["escalation_id"]) == "ANSWERED"
        escalations[record["escalation_id"]] = {
            **record, "state": "ANSWERED" if answered else "OPEN"}

    # Any evidence record, not one hardcoded filename.
    #
    # **This was a real continuity gap.** The reader looked only for
    # `first-execution.evidence.json`, so the W1 coordination run — which writes
    # `w1-coordination.evidence.json` — reconstructed its instances and grants
    # correctly while reporting `last_plan: null` and no outcomes. Recovery that
    # silently omits what it cannot name is the `§22` failure of collapsing
    # distinct states, arriving by a different route: not *stale* read as
    # *current*, but *present* read as *absent*.
    evidence_files = sorted(root.glob("*.evidence.json"))
    evidence = {}
    for path in evidence_files:
        loaded = _load(path)
        if loaded is None:
            unreadable.append(path.name)
        elif loaded.get("executed_at", "") >= evidence.get("executed_at", ""):
            evidence = loaded

    historical_active = sorted(k for k, g in grants.items()
                               if g.get("status") == "ACTIVE")
    dispositions: Dict[str, dict] = {}
    disposition_faults: Tuple[str, ...] = ()
    if operational_ledger is not None:
        from tools.w4_delegation import read_dispositions
        dispositions, disposition_faults = read_dispositions(root, operational_ledger)
    active = [k for k in historical_active if k not in dispositions]

    # Accumulation is **per recipient instance**, not per root.
    #
    # `duplicate_active` was `len(active) > 1`, which encoded "one instance per
    # operational root" — true of `w4-operations` and `w1-operations`, and false
    # of the cross-Department root, where two grants are live **by design**: one
    # per Department's instance, each bounded to its own step.
    #
    # Left as it was, `continuation_conditions` reported a permanent
    # `MORE THAN ONE LIVE GRANT` blocker against a legitimate state — a **false
    # positive in the reader a next run consults to decide whether to proceed.**
    # The true positive is preserved exactly: the same instance holding two live
    # grants in one root is still accumulation, and is still reported.
    live_by_instance: Dict[str, List[str]] = {}
    for key in active:
        live_by_instance.setdefault(
            grants[key].get("recipient_instance") or "(unnamed)", []).append(key)
    accumulated = {instance: sorted(ids)
                   for instance, ids in live_by_instance.items() if len(ids) > 1}
    revoked = sorted(k for k, g in grants.items() if g.get("status") == "REVOKED")

    # `§23`: what is still valid, what is no longer, and what remains.
    live_instances = sorted(k for k, r in instances.items()
                            if r.get("lifecycle") == "REGISTERED")
    open_escalations = sorted(k for k, e in escalations.items()
                              if e["state"] == "OPEN")

    return {
        # Repo-relative where possible, absolute otherwise. The first version
        # called `relative_to(REPO_ROOT)` unconditionally, which raised for any
        # root outside the repository — making the module **untestable against a
        # temporary root**, which is the only way the corruption states in `§22`
        # can be exercised safely.
        "source": _describe(root),
        "instances": live_instances,
        "retired_instances": sorted(k for k, r in instances.items()
                                    if r.get("lifecycle") != "REGISTERED"),
        "active_grants": active,
        "revoked_grants": revoked,
        "duplicate_active": bool(accumulated),
        "accumulated_grants": accumulated,
        "live_grants_by_instance": {k: sorted(v)
                                    for k, v in sorted(live_by_instance.items())},
        "unreadable_records": sorted(unreadable),
        "evidence_records": [p.name for p in evidence_files],
        "last_act": evidence.get("act"),
        "last_plan": evidence.get("plan"),
        "last_goal": evidence.get("goal"),
        "last_delegation": evidence.get("delegation_id"),
        "last_outcomes": [(o["step"], o["status"])
                          for o in evidence.get("outcomes", [])],
        "last_escalated": any(o["status"] == "escalation"
                              for o in evidence.get("outcomes", [])),
        "last_failed": any(o["status"] == "failure"
                           for o in evidence.get("outcomes", [])),
        "escalations": escalations,
        "open_escalations": open_escalations,
        "accountable_parties": sorted({g.get("accountable_party")
                                       for g in grants.values()
                                       if g.get("accountable_party")}),
        "authority_instruments": sorted({g.get("authority_instrument")
                                         for g in grants.values()
                                         if g.get("authority_instrument")}),
        **({} if response_ledger is None else {
            "response_ledger": _describe(Path(response_ledger))}),
        **({} if operational_ledger is None else {
            "operational_ledger": _describe(Path(operational_ledger)),
            "historical_active_grants": historical_active,
            "operational_dispositions": {k: v["disposition"]
                                         for k, v in sorted(dispositions.items())},
            "completed_grants": sorted(k for k, v in dispositions.items()
                                       if v["disposition"] == "COMPLETED"),
            "operationally_revoked_grants": sorted(
                k for k, v in dispositions.items() if v["disposition"] == "REVOKED"),
            "disposition_faults": list(disposition_faults),
        }),
    }


def continuation_conditions(state: dict) -> Tuple[str, ...]:
    """What a next run must respect, derived from the reconstructed state.

    Returned as findings rather than enforced here: `PR-3` is
    detect-don't-decide, and a continuity reader that started refusing things
    would be making operational decisions from memory — which is exactly the
    `MEMORY ≠ AUTHORITY` boundary `§21` draws.
    """
    conditions: List[str] = []
    if state["duplicate_active"]:
        conditions.append(
            f"MORE THAN ONE LIVE GRANT FOR ONE INSTANCE: "
            f"{state['accumulated_grants']} — a re-run must supersede rather "
            "than add to them (§34)")
    if state["unreadable_records"]:
        conditions.append(
            f"UNREADABLE RECORDS: {state['unreadable_records']} — corruption is "
            "not absence, and must not be read as 'no prior state' (§22)")
    if state.get("disposition_faults"):
        conditions.append(
            f"DISPOSITION FAULTS: {state['disposition_faults']} — a disposition "
            "whose basis changed is not honoured; the grant keeps its historical "
            "status until the fault is resolved")
    if state["open_escalations"]:
        conditions.append(
            f"OPEN ESCALATIONS: {state['open_escalations']} — blocked work "
            "remains blocked; an escalation is not resolved by re-running (§16)")
    if state["last_failed"]:
        conditions.append(
            "PREVIOUS RUN CONTAINED A FAILURE — replaying it without a reason "
            "would repeat work the record says did not succeed (§23)")
    if not state["instances"]:
        conditions.append(
            "NO LIVE AGENT INSTANCE — nothing may execute (§26)")
    if not conditions:
        conditions.append("NO BLOCKING CONDITION — prior state is coherent")
    return tuple(conditions)


def operational_state(root: Path = OPERATIONS) -> dict:
    """The reading that honours both live ledgers (`FD-AGENCY-001` S-1 A2, B1).

    The same reconstruction, with the delegation dispositions and the
    out-of-boundary escalation responses taken into account. ``reconstruct(root)``
    with no ledger remains the historical reading.
    """
    from tools.escalation_register import LIVE_RESPONSES
    from tools.w4_delegation import LIVE_LEDGER
    return reconstruct(root, operational_ledger=LIVE_LEDGER,
                       response_ledger=LIVE_RESPONSES)
