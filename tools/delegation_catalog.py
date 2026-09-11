"""Read the resident organizational delegation records and verify their bounds.

**This is the first Phase 11 construction step**, authorized by `DP-01 §20` —
*"Following issuance, Claude Code may begin P11 construction within this
authorization surface"* — under work package `§3 W3` Organizational Delegation.

**The record shape is not mine.** `DP-04 §8.3` fixes it:

    AUTHORITY SOURCE → AUTHORIZED SCOPE → DELEGATED ACTOR / UNIT
                     → BOUNDARY → ACCOUNTABILITY → VERIFICATION

so the organizational layer may state *"A delegates B for capability/work X
within authority boundary Y under accountability condition Z"* without
introducing a Native Core subsystem. `DP-03 §8.2` fixes the surface as an
``ORGANIZATIONAL-LAYER GOVERNED RECORD / RELATION`` and permits reuse of the
established P10 record/loader pattern, adding that **the reuse "does not
authorize creation of a Native Core entity or subsystem."** This module adds no
boundary: Native Core Blueprint `§4` fixes the core region at *"exactly the
eleven frozen subsystem boundaries — no more"*, and a loader that reads
documentation is not one of them.

**What this module refuses to do is author a delegation.** `DP-01 §3 W3` says
delegation *"does not create authority"* and *"does not authorize itself"*;
`DP-04 §8.3` forbids it to *"create authority that does not already exist."*
Writing a record that says *"Engineering delegates X"* is not
a technical act — it is an exercise of the very authority being delegated, and I
hold none of it. So the mechanism is built and the resident population is
**empty and reported as 0**. That mirrors P10, where the ownership loader existed
before `FD-P10-003` authorized the population it would read. A manufactured
record would make the count look like progress and would be the one thing this
module exists to make impossible.

**Every check below is structural.** None matches prose. A delegation that
violates a `DP-04 §8.3` prohibition is caught because two independent statements
in the corpus disagree, not because a sentence contained a forbidden word.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.organization_catalog import (  # noqa: E402
    ORGANIZATION_ROOT,
    _slug,
    read_departments,
)

DELEGATION_ROOT = ORGANIZATION_ROOT / "delegations"

#: The six elements `DP-04 §8.3` fixes, plus one.
#:
#: ``Authorizing Instrument`` is **not** a seventh concept. `DP-04 §8.3` lists
#: what a delegation *records*; this section is how the record is made to obey
#: `DP-01 §3 W3`'s prohibition *"does not authorize itself"* — a clause that
#: appears in `DP-01`, **not** in `DP-04 §8.3`, whose nearest item is *"create
#: authority that does not already exist."* A record carrying no pointer to an
#: instrument outside itself
#: **is** a self-authorizing delegation, and without this section that condition
#: is unrepresentable, so it could never be detected.
REQUIRED_SECTIONS = (
    "Authority Source",
    "Authorized Scope",
    "Delegated Actor",
    "Boundary",
    "Accountability",
    "Verification",
    "Authorizing Instrument",
)

#: Sections whose body is a key naming something in the organizational
#: population, rather than prose. These are the ones a cross-check can resolve.
KEYED_SECTIONS = ("Authority Source", "Authorized Scope", "Delegated Actor",
                  "Accountability")

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _section(text: str, heading: str) -> Optional[str]:
    """The body of ``## <heading>`` up to the next heading, or None if absent.

    Returns None for an absent section and ``""`` for a present but empty one —
    **the two are different defects** and collapsing them would let a record
    satisfy the structure while saying nothing.
    """
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)", re.M | re.S)
    match = pattern.search(text)
    return None if match is None else match.group(1).strip()


def _key_of(body: str) -> Optional[str]:
    """The slug a keyed section names, reading through a markdown link if used."""
    if not body:
        return None
    first = body.split("\n")[0].strip()
    link = MD_LINK.search(first)
    if link:
        label = first[:link.start()].strip() or first
        label = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", label).strip()
        return _slug(label) if label else None
    return _slug(first)


@dataclass(frozen=True)
class DelegationRecord:
    """One delegation as its resident record states it — nothing added."""

    key: str
    record: str
    authority_source: Optional[str]
    authorized_scope: Optional[str]
    delegated_actor: Optional[str]
    accountability: Optional[str]
    sections: Tuple[str, ...]


def read_delegations(root: Path = DELEGATION_ROOT) -> List[DelegationRecord]:
    """Every delegation that has a resident record. No inference, no defaults.

    ``README.md`` is the directory's own explanatory record, not a delegation,
    and is skipped by name.
    """
    records: List[DelegationRecord] = []
    if not root.is_dir():
        return records
    for path in sorted(root.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        present = tuple(h for h in REQUIRED_SECTIONS if _section(text, h) is not None)
        try:
            relative = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            relative = path.as_posix()
        records.append(
            DelegationRecord(
                key=_slug(path.stem),
                record=relative,
                authority_source=_key_of(_section(text, "Authority Source") or ""),
                authorized_scope=_key_of(_section(text, "Authorized Scope") or ""),
                delegated_actor=_key_of(_section(text, "Delegated Actor") or ""),
                accountability=_key_of(_section(text, "Accountability") or ""),
                sections=present,
            )
        )
    return records


#: An authority source established by an *instrument* rather than by being an
#: organizational unit. `FD-P11-001 §4.1` names Claude Code the authorized W4
#: operational delegator, and `§5` explicitly **rejects** Engineering or Platform
#: becoming that delegator by virtue of being labels.
#:
#: **This entry corrects an over-constraint of mine, not the architecture's.**
#: `DP-04 §8.3` fixes the record shape as ``AUTHORITY SOURCE → AUTHORIZED SCOPE →
#: DELEGATED ACTOR / UNIT → BOUNDARY → ACCOUNTABILITY → VERIFICATION` and
#: **nowhere requires the source to be a Department.** I imposed that under
#: `ACT-CC-P11-005`, citing `FD-P10-003 §5`, and it was right at the time: the
#: only conceivable delegators were Departments, and demanding an established one
#: kept authority from arising out of nowhere.
#:
#: `FD-P11-001` then established a delegator that is not a unit. The constraint
#: did not become wrong — it became **narrower than the architecture it
#: implements**, which is why `FD-P11-001 §20` could say W3 *"is the
#: organizational mechanism through which the authorized Delegation record is
#: represented and tracked"* while W3 structurally rejected that very record.
#:
#: Admitting this source creates no authority. `§20` requires that W3 *"must not
#: manufacture authority absent valid provenance"*, so a record naming it must
#: still cite the instrument that established it — checked below.
INSTRUMENT_ESTABLISHED_SOURCES = {
    "claude-code-aios-co-founder": "FD-P11-001",
}

#: Where registered Agent Instances are persisted. A W4 delegation's actor is an
#: Agent *Instance*, which is neither a Department nor an Agent Definition — the
#: distinction `FD-P11-001 §6.1` makes mandatory.
#:
#: **Every operational root, not one.** This read `w4-operations` alone until
#: `ACT-CC-P11-013`, and the single root was invisible for as long as no W3
#: record named a W1 instance. The moment reconciliation projected the live W1
#: grant, the loader reported its recipient as `actor-unknown` — an instance
#: that has been registered on disk since `ACT-CC-P11-011`, reported absent
#: because the loader was looking in one of the two places instances live.
#:
#: A population loader that knows some of the population does not fail; it
#: **passes, on the part it can see**, which is why nothing surfaced this for
#: two Acts.
P11_OPERATIONS = REPO_ROOT / "docs/architecture/p11"


def operation_roots(base: Path = P11_OPERATIONS) -> Tuple[Path, ...]:
    """Every directory under `docs/architecture/p11/` holding operational record.

    **Discovered, not listed.** Two hand-maintained root lists have already gone
    stale in this programme — one read `w4-operations` only and reported a live
    W1 instance as `actor-unknown`, and a second refused to project a grant
    written to a new root the day that root was created. A list someone must
    remember to extend is the same defect twice.

    A directory qualifies by containing a record, so a new operational root
    joins the population by being written to rather than by being declared.
    """
    if not base.is_dir():
        return ()
    found = {path.parent for pattern in ("*.instance.json", "*.delegation.json",
                                         "*.escalation.json", "*.evidence.json")
             for path in base.glob(f"*/{pattern}")}
    return tuple(sorted(found))


#: The discovered population, under its historical name. **Not a literal list.**
#:
#: It was retained as a hardcoded pair when `operation_roots()` replaced it, on
#: the reasoning that nothing used it any more. Nothing did — which made it a
#: trap rather than a courtesy: the next reader to import it would have got the
#: stale two-root answer the discovery function exists to prevent. Bound to the
#: function under `ACT-CC-P11-017`.
INSTANCE_ROOTS = operation_roots()

#: Retained: the primary root, and the argument default callers already pass.
INSTANCE_RECORDS = INSTANCE_ROOTS[0]


def registered_instances(root=None) -> Dict[str, dict]:
    """Agent Instances that have actually been registered, read from record.

    Empty when none exist, exactly as the Department loader returns nothing for
    an absent tree. An instance that is not on disk is not a valid actor.

    ``root`` accepts one path or several; omitted, every operational root is
    read, so the answer does not depend on which proof happened to persist the
    instance.
    """
    if root is None:
        roots: Tuple[Path, ...] = operation_roots()
    elif isinstance(root, (str, Path)):
        roots = (Path(root),)
    else:
        roots = tuple(Path(r) for r in root)
    found: Dict[str, dict] = {}
    for one in roots:
        if not one.is_dir():
            continue
        for path in sorted(one.glob("*.instance.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            key = record.get("instance_key")
            if key:
                found[key] = record
    return found


def _population(org_root: Path, instance_root=None):
    """``(capabilities_by_department, source_keys, actor_keys, instances)``."""
    departments = read_departments(org_root)
    owned = {r.key: set(r.capabilities) for r in departments}
    department_keys = set(owned)
    instances = registered_instances(instance_root)
    source_keys = department_keys | set(INSTRUMENT_ESTABLISHED_SOURCES)
    actors = set(department_keys) | set(instances)
    for record in departments:
        actors.update(record.agent_definitions)
    return owned, source_keys, actors, instances


def verify(delegations, org_root: Path = ORGANIZATION_ROOT,
           root: Path = DELEGATION_ROOT):
    """Check every delegation against the organizational population it names.

    Returns a list of ``(kind, delegation_key, detail)``. **Defects are
    returned, never raised**: `PR-3` is detect-don't-decide, and refusing to
    load would hide the finding rather than surface it — the same rule the
    frozen `OwnershipGraph` and the P10 loader both follow.

    Each kind implements one `DP-04 §8.3` prohibition structurally:

    ``scope-not-owned``
        The authority source delegates a Capability it does not own. This is the
        load-bearing one. `DP-01 §3 W3`: delegation *"does not create
        authority"*. `DP-04 §8.3` forbids it to *"create authority that does not
        already exist"* or to *"expand constitutional or Founder authority"*. A
        unit cannot delegate what it never held, so a record asserting otherwise
        is authority manufactured by writing it down.
    ``authority-source-unknown``
        The delegator is not an established Department. `FD-P10-003 §5` fixes
        ``CANONICAL DEPARTMENT = EXPLICITLY ESTABLISHED ORGANIZATIONAL UNIT``;
        anything else delegating is authority from nowhere.
    ``actor-unknown``
        The delegate is not in the population, so the boundary has no subject.
    ``self-delegation``
        Source and actor are the same unit. Such a record creates no boundary
        while presenting as one — it is indistinguishable from an authority
        assertion, which is what `DP-01 §3 W3`'s *"does not create authority"*
        forbids.
    ``accountability-transferred``
        The accountability holder **is** the delegated actor. `DP-04 §8.3` lists
        *"transfer ultimate accountability"* among the things delegation
        *"shall NOT"* do; `DP-01 §3 W3` states it as *"does not transfer
        ultimate Founder accountability."* Naming the delegate accountable is
        that transfer, stated structurally rather than in prose.
    ``missing-section`` / ``empty-section``
        A required element absent, or present and saying nothing.
    ``authorizing-instrument-unresolvable`` / ``verification-unresolvable``
        The record points at an instrument or verification mechanism that is not
        on disk. A pointer that resolves to nothing is not evidence, which is the
        same rule the citation audit applies to the rest of this corpus.
    """
    owned, source_keys, actors, instances = _population(org_root)
    defects: List[Tuple[str, str, Optional[str]]] = []
    for record in delegations:
        path = REPO_ROOT / record.record
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for heading in REQUIRED_SECTIONS:
            body = _section(text, heading)
            if body is None:
                defects.append(("missing-section", record.key, heading))
            elif not body:
                defects.append(("empty-section", record.key, heading))

        source, scope = record.authority_source, record.authorized_scope
        actor = record.delegated_actor

        if source is not None:
            if source not in source_keys:
                defects.append(("authority-source-unknown", record.key, source))
            elif source in INSTRUMENT_ESTABLISHED_SOURCES:
                # An instrument-established source owns no Capability, so the
                # ownership graph cannot bound its scope. What bounds it instead
                # is the recipient: `FD-P11-001 §16` fixes delegated ≤ available,
                # and the instance's permitted surface is what it may hold.
                instrument = INSTRUMENT_ESTABLISHED_SOURCES[source]
                body = text
                if instrument not in body:
                    defects.append(("source-instrument-not-cited", record.key,
                                    f"{source} requires {instrument}"))
                permitted = set(instances.get(actor, {})
                                .get("permitted_capabilities", ()))
                if actor in instances and scope is not None \
                        and scope not in permitted:
                    defects.append(("scope-beyond-recipient", record.key,
                                    f"{actor} ∌ {scope}"))
            elif scope is not None and scope not in owned[source]:
                defects.append(("scope-not-owned", record.key, f"{source} ∌ {scope}"))
        if actor is not None and actor not in actors:
            defects.append(("actor-unknown", record.key, actor))
        if source is not None and actor is not None and source == actor:
            defects.append(("self-delegation", record.key, source))
        if record.accountability is not None and actor is not None \
                and record.accountability == actor:
            defects.append(("accountability-transferred", record.key, actor))

        for heading, kind in (("Authorizing Instrument",
                               "authorizing-instrument-unresolvable"),
                              ("Verification", "verification-unresolvable")):
            body = _section(text, heading)
            if not body:
                continue
            targets = MD_LINK.findall(body)
            if not targets:
                defects.append((kind, record.key, "no resolvable pointer"))
                continue
            for target in targets:
                target = target.split("#")[0].strip()
                if not target:
                    continue
                if not (path.parent / target).resolve().is_file():
                    defects.append((kind, record.key, target))
    return defects


def report(org_root: Path = ORGANIZATION_ROOT, root: Path = DELEGATION_ROOT) -> dict:
    delegations = read_delegations(root)
    return {
        "delegations": delegations,
        "defects": verify(delegations, org_root, root),
        "population_empty": not delegations,
    }


def main(argv: List[str]) -> int:
    result = report()
    print(f"delegation records   : {len(result['delegations'])}")
    for record in result["delegations"]:
        print(f"  {record.key:<28} {record.authority_source} → "
              f"{record.delegated_actor} for {record.authorized_scope}")
    defects = result["defects"]
    print(f"defects              : {len(defects)}")
    for kind, key, detail in defects:
        print(f"    {kind.upper()} — {key}" + (f" ({detail})" if detail else ""))
    if result["population_empty"]:
        print()
        print("POPULATION EMPTY — 0 delegations, and that is the honest count.")
        print("  The mechanism is authorized (DP-01 §3 W3); authoring a delegation")
        print("  is not a technical act but an exercise of the authority being")
        print("  delegated, which this executor does not hold. See module docstring.")
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
