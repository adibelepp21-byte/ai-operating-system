"""P12-W6 — execution provenance verification (`§19` scope: `PROVENANCE`).

`§34` requires that execution provenance identify, where applicable: actor,
delegator, authority, objective, work scope, capability, workflow, runtime,
result, evidence, verification. It closes: *"Provenance is part of system
integrity."*

**This reads stored records, not class definitions.** A dataclass field proves
that a field can be written; only a stored record proves one was. The two
diverge in exactly the case that matters here — `TraceRecord.from_mapping`
reconstructs only the ten required fields, so any additional key written into a
Trace record is **silently dropped on read**. A schema inspection would report a
carrier that a corpus inspection shows is not there.

**The question `§34` asks is not "does each element appear somewhere".** It is
whether provenance can be *assembled* for an execution. An element carried on
one record and another element carried on a different record is provenance only
if the two records can be joined. So this module reports two different things
and never merges them: per-element coverage, and whether any actual execution
has an assemblable chain.

`ABSENT` and `NOT ASSEMBLABLE` are findings about the system, not failures of
this module.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Where resident delegation records live.
DELEGATION_ROOTS: Tuple[Path, ...] = (
    REPO_ROOT / "docs/architecture/p11/w1-operations",
    REPO_ROOT / "docs/architecture/p11/w4-operations",
    REPO_ROOT / "docs/architecture/p11/x-department-operations",
    # P12-W4 grants. Omitted at first, which made the new execution's manifest
    # name a delegation this module could not find — the module reported the
    # join missing because it was not looking where the grant was written.
    REPO_ROOT / "docs/architecture/p12/w4-operations",
)

#: Where durable Trace records live.
TRACE_ROOT = REPO_ROOT / "docs/architecture/p12/trace-stores"

#: Where P11 execution **evidence records** live. These were missing from the
#: first version of this module, and their absence produced a finding that was
#: true of the two surfaces measured and false as a statement about the system:
#: an evidence record carries `goal`, `plan`, `plan_authority`, the step-to-grant
#: mapping, `delegation_id` and `authority_chain` in one artifact, which is
#: precisely the join the module reported missing. Found by trying to falsify
#: the finding rather than reproduce it.
EVIDENCE_ROOTS: Tuple[Path, ...] = (
    REPO_ROOT / "docs/architecture/p11",
)

#: Where P12-W4 execution provenance manifests live. A manifest joins a Trace
#: record to the delegation that authorized it, which `TraceRecord` cannot carry
#: — its reader reconstructs only the ten required fields, so a delegation key
#: written into a Trace record is dropped on read. Counting a Trace record as
#: joined therefore means resolving the manifest that names it, not looking for
#: a key inside it.
MANIFEST_ROOT = REPO_ROOT / "docs/architecture/p12/execution-provenance"

CARRIED = "CARRIED"
ABSENT = "ABSENT"

ASSEMBLABLE = "ASSEMBLABLE"
NOT_ASSEMBLABLE = "NOT ASSEMBLABLE"
NO_EXECUTIONS = "NO EXECUTIONS"

#: `§34`'s eleven, in its order.
PROVENANCE_ELEMENTS: Tuple[str, ...] = (
    "actor", "delegator", "authority", "objective", "work scope",
    "capability", "workflow", "runtime", "result", "evidence", "verification",
)

#: Which stored key, on which record kind, carries each element. A mapping
#: entry is a claim that is checked against real records, not a description.
_DELEGATION_KEYS: Dict[str, str] = {
    "actor": "recipient_instance",
    "delegator": "delegator",
    "authority": "authority_record",
    "objective": "objective",
    "work scope": "work_scope",
    "capability": "capability_scope",
    "verification": "verification_requirement",
}
_TRACE_KEYS: Dict[str, str] = {
    "actor": "agent_instance",
    "runtime": "runtime",
    "result": "outputs",
}
#: An execution evidence record. `workflow` and `evidence` were reported ABSENT
#: while this surface was outside the measured population; both are carried here.
_EVIDENCE_KEYS: Dict[str, str] = {
    "actor": "agent_instance",
    "delegator": "accountable_party",
    "authority": "authority_chain",
    "objective": "goal",
    "work scope": "work_scope",
    "capability": "capability_scope",
    "workflow": "workflow_steps",
    "runtime": "coordination",
    "result": "outcomes",
    "evidence": "executed_at",
    "verification": "criteria_total",
}


@dataclass(frozen=True)
class ElementResult:
    element: str
    status: str
    carriers: Tuple[str, ...]
    detail: str


def delegation_records() -> Tuple[dict, ...]:
    """Every resident delegation record, as stored."""
    found = []
    for root in DELEGATION_ROOTS:
        if not root.is_dir():
            continue
        for path in sorted(root.glob("*.delegation.json")):
            try:
                found.append(json.loads(path.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                continue
    return tuple(found)


def trace_records() -> Tuple[dict, ...]:
    """Every durable Trace record, as stored on disk.

    Read as raw JSON rather than through `TraceReader`, because the question is
    what the corpus holds — and the reader reconstructs only the ten required
    fields, which would hide any key the writer had added.
    """
    found = []
    if not TRACE_ROOT.is_dir():
        return ()
    for store in sorted(p for p in TRACE_ROOT.iterdir() if p.is_dir()):
        ordinal = 0
        for path in sorted(p for p in store.rglob("*") if p.is_file()):
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # The address a manifest uses. Carried alongside the record so a
                # join can be resolved by address rather than by matching the
                # runtime name — which is the same name-match this module exists
                # to reject, and which an earlier version of the manifest check
                # committed: one manifest appeared to join two records because
                # both ran under the same runtime identity.
                record["__store"] = store.name
                record["__ordinal"] = ordinal
                ordinal += 1
                found.append(record)
    return tuple(found)


def evidence_records() -> Tuple[dict, ...]:
    """Every resident execution evidence record, as stored."""
    found = []
    for root in EVIDENCE_ROOTS:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.evidence.json")):
            try:
                found.append(json.loads(path.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                continue
    return tuple(found)


def manifest_records() -> Tuple[dict, ...]:
    """Every persisted execution provenance manifest, as stored."""
    if not MANIFEST_ROOT.is_dir():
        return ()
    found = []
    for path in sorted(MANIFEST_ROOT.glob("*.manifest.json")):
        try:
            found.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return tuple(found)


def _populated(records: Tuple[dict, ...], key: str) -> int:
    """Records in which `key` is present **and** carries a value.

    A key present with an empty value is not provenance. `skills_used: []`
    identifies no skill, and counting it as coverage is how an empty field comes
    to look like a filled one.
    """
    total = 0
    for record in records:
        if key not in record:
            continue
        value = record[key]
        if value in (None, "", [], (), {}):
            continue
        total += 1
    return total


def elements(delegations=None, traces=None, evidence=None
             ) -> Tuple[ElementResult, ...]:
    delegations = delegation_records() if delegations is None else delegations
    traces = trace_records() if traces is None else traces
    evidenced = evidence_records() if evidence is None else evidence

    results = []
    for element in PROVENANCE_ELEMENTS:
        carriers = []
        details = []
        for label, records, keys in (
                ("delegation", delegations, _DELEGATION_KEYS),
                ("trace", traces, _TRACE_KEYS),
                ("evidence", evidenced, _EVIDENCE_KEYS)):
            key = keys.get(element)
            if key is None:
                continue
            count = _populated(records, key)
            if count:
                carriers.append(label)
                details.append(f"{label}.{key} populated in {count}/"
                               f"{len(records)}")
            else:
                details.append(f"{label}.{key} present in 0/{len(records)}")
        status = CARRIED if carriers else ABSENT
        detail = "; ".join(details) if details else (
            "no resident record type declares a key for this element")
        results.append(ElementResult(element, status, tuple(carriers), detail))
    return tuple(results)


def assembly(delegations=None, traces=None, evidence=None,
             manifests=None) -> dict:
    """Can provenance be assembled for an actual execution?

    An execution is a stored record of work having run. Two resident surfaces
    hold such records and they behave differently, so both are counted and the
    result names which is which:

    * an **evidence record** carries `delegation_id` in the same artifact as the
      goal, plan and outcome — the join is present;
    * a **Trace record** carries actor, runtime and outputs and nothing that
      names the grant under which it ran.

    The actor name is on both sides and is **not** a join: one Agent Instance
    holds many grants, so an actor match identifies a set, not the grant in
    force.
    """
    delegations = delegation_records() if delegations is None else delegations
    traces = trace_records() if traces is None else traces
    evidenced = evidence_records() if evidence is None else evidence
    joins = manifest_records() if manifests is None else manifests

    known = {d.get("delegation_id") for d in delegations}
    # A manifest joins one Trace record, addressed by store and ordinal. Only
    # manifests whose delegation actually resolves are counted: a manifest
    # naming a grant nobody issued is a claim, not a join.
    manifest_joined = {
        (m.get("trace_store"), m.get("trace_ordinal"))
        for m in joins if m.get("delegation_id") in known}
    evidence_joined = sum(
        1 for record in evidenced if record.get("delegation_id") in known)

    if not traces and not evidenced:
        return {"status": NO_EXECUTIONS, "executions": 0, "joined": 0,
                "evidence_executions": 0, "evidence_joined": 0,
                "trace_executions": 0, "trace_joined": 0,
                "detail": "no execution record of either kind exists"}

    joined = 0
    ambiguous = 0
    for trace in traces:
        link = trace.get("delegation_id") or trace.get("delegation")
        if link and any(d.get("delegation_id") == link for d in delegations):
            joined += 1
            continue
        if (trace.get("__store"), trace.get("__ordinal")) in manifest_joined:
            joined += 1
            continue
        actor = trace.get("agent_instance")
        candidates = [d for d in delegations
                      if d.get("recipient_instance") == actor]
        if len(candidates) == 1:
            # Still not a join: it is unique by accident of how many grants this
            # actor happens to hold, and a second grant would silently make the
            # same execution ambiguous.
            ambiguous += 1
        elif len(candidates) > 1:
            ambiguous += 1

    total = len(traces) + len(evidenced)
    total_joined = joined + evidence_joined
    common = {
        "executions": total,
        "joined": total_joined,
        "evidence_executions": len(evidenced),
        "evidence_joined": evidence_joined,
        "trace_executions": len(traces),
        "trace_joined": joined,
    }
    if total_joined == total:
        return dict(common, status=ASSEMBLABLE,
                    detail="every execution names the delegation that "
                           "authorized it")
    return dict(
        common, status=NOT_ASSEMBLABLE,
        detail=(
            f"{total_joined}/{total} executions name their delegation: "
            f"{evidence_joined}/{len(evidenced)} evidence records do, "
            f"{joined}/{len(traces)} Trace records do; {ambiguous} could only "
            "be matched by actor name, which identifies a set of grants rather "
            "than the one in force"))


def summary() -> dict:
    results = elements()
    joinable = assembly()
    return {
        "elements": len(results),
        "carried": sum(1 for r in results if r.status == CARRIED),
        "absent": sum(1 for r in results if r.status == ABSENT),
        "absent_elements": tuple(r.element for r in results
                                 if r.status == ABSENT),
        "assembly": joinable["status"],
        "executions": joinable["executions"],
        "executions_joined": joinable["joined"],
        "evidence_joined": f"{joinable['evidence_joined']}/"
                           f"{joinable['evidence_executions']}",
        "trace_joined": f"{joinable['trace_joined']}/"
                        f"{joinable['trace_executions']}",
        "manifests": len(manifest_records()),
    }


def main(argv=None) -> int:
    for result in elements():
        print(f"{result.element:<13} {result.status:<9} "
              f"{','.join(result.carriers) or '—':<18} {result.detail[:66]}")
    print()
    joinable = assembly()
    print(f"assembly: {joinable['status']} — {joinable['detail']}")
    print()
    print("summary:", summary())
    print()
    print("An element carried on one record and another on a different record")
    print("is provenance only if the two records can be joined.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
