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
)

#: Where durable Trace records live.
TRACE_ROOT = REPO_ROOT / "docs/architecture/p12/trace-stores"

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
    for path in sorted(TRACE_ROOT.rglob("*")):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                found.append(json.loads(line))
            except json.JSONDecodeError:
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


def elements(delegations=None, traces=None) -> Tuple[ElementResult, ...]:
    delegations = delegation_records() if delegations is None else delegations
    traces = trace_records() if traces is None else traces

    results = []
    for element in PROVENANCE_ELEMENTS:
        carriers = []
        details = []
        for label, records, keys in (
                ("delegation", delegations, _DELEGATION_KEYS),
                ("trace", traces, _TRACE_KEYS)):
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


def assembly(delegations=None, traces=None) -> dict:
    """Can provenance be assembled for an actual execution?

    An execution is a stored Trace record. Assembling `§34` for it requires
    reaching the delegation that authorized it. The actor name is on both sides
    and is **not** a join: one Agent Instance holds many grants, so an actor
    match identifies a set, not the grant under which this execution ran.
    """
    delegations = delegation_records() if delegations is None else delegations
    traces = trace_records() if traces is None else traces

    if not traces:
        return {"status": NO_EXECUTIONS, "executions": 0, "joined": 0,
                "detail": "no durable Trace record exists to assemble"}

    joined = 0
    ambiguous = 0
    for trace in traces:
        link = trace.get("delegation_id") or trace.get("delegation")
        if link and any(d.get("delegation_id") == link for d in delegations):
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

    if joined == len(traces):
        return {"status": ASSEMBLABLE, "executions": len(traces),
                "joined": joined,
                "detail": "every execution names the delegation that authorized it"}
    return {
        "status": NOT_ASSEMBLABLE,
        "executions": len(traces),
        "joined": joined,
        "detail": (
            f"{len(traces) - joined} of {len(traces)} executions carry no "
            f"delegation reference; {ambiguous} could only be matched by actor "
            "name, which identifies a set of grants rather than the one in "
            "force"),
    }


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
