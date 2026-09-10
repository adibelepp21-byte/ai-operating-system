"""Read the resident organizational records and construct the ownership graph.

**This is the Phase 10 operationalization step**, authorized by
`FD-P10-003 §12` — *"instantiate the required ownership representation; populate
the ownership graph; establish Department → Capability relationships … create or
update verification; persist the resulting evidence."*

**It invents nothing.** Every Department, Capability and Agent Definition is read
from a record under ``docs/architecture/organization/``, each of which cites the
ADR that established it. `FD-P10-003 §4.1` forbids inventing the population and
`§24` says so again: *"DO NOT INVENT THE DEPARTMENT MODEL."* A record that is not
on disk produces no entry here.

**And it does not convert Platform Divisions into Departments.** `FD-P10-003 §5`
fixes the rule as ``CANONICAL DEPARTMENT = EXPLICITLY ESTABLISHED ORGANIZATIONAL
UNIT`` and not ``PD = DEPARTMENT``. `PD-01`…`PD-10` are read from a different
tree and are deliberately not consulted by this module.

**Why this lives in ``tools/`` and not in ``native_core/``.** Native Core
Blueprint `§4` fixes the core region at *"exactly the eleven frozen subsystem
boundaries — no more"*. A loader that reads documentation is not one of them. It
imports the frozen `OwnershipGraph` and adds no boundary.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
ORGANIZATION_ROOT = REPO_ROOT / "docs/architecture/organization"

#: Directories under the organization root that record framework or catalog
#: material rather than a Department instance.
NON_DEPARTMENT_DIRS = {"execution-catalog", "platform-runtime"}

NAME_SECTION = re.compile(r"^## Name\s*\n\s*\n(.+?)\s*$", re.M)


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")


def _read_name(path: Path) -> Optional[str]:
    """The record's own ``## Name`` section, or its H1 as a fallback."""
    text = path.read_text(encoding="utf-8")
    match = NAME_SECTION.search(text)
    if match:
        return match.group(1).strip()
    for line in text.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _record_path(readme: Path) -> str:
    """Repo-relative where possible; absolute otherwise (tests use temp roots)."""
    try:
        return readme.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return readme.as_posix()


@dataclass(frozen=True)
class DepartmentRecord:
    """One Department as its resident record states it — nothing added."""

    key: str
    name: str
    record: str
    capabilities: Tuple[str, ...]
    agent_definitions: Tuple[str, ...]
    establishing_adrs: Tuple[str, ...]


#: A Department record opens by naming the decision that established it —
#: *"This Department was established by [ADR-0008](…)"*. Only that sentence is
#: an establishment.
ESTABLISHED_BY = re.compile(
    r"established by\s*\n?\s*\[?(ADR-\d{4})", re.I
)


def _establishing_adr(readme: Path) -> Tuple[str, ...]:
    """The ADR the record says established it — **not every ADR it mentions**.

    The first version unioned every ``ADR-\d{4}`` across the README and every
    capability file. That attributed **`ADR-0003` to Engineering**, because
    ``engineering-intelligence.md:47`` mentions it in a cross-reference —
    *"belongs to Platform under ADR-0003"*. **A mention is not an
    establishment**, which is the same distinction that governs citations
    elsewhere in this repository.
    """
    match = ESTABLISHED_BY.search(readme.read_text(encoding="utf-8"))
    return (match.group(1),) if match else ()


OWNER_SECTION = re.compile(r"^## Owner\s*\n\s*\n(.+?)\s*$", re.M)


def _owner_disagreements(departments, root: Path):
    """Capability records whose stated Owner differs from their nesting."""
    disagreements = []
    for record in departments:
        directory = (root / record.key / "capabilities")
        for key in record.capabilities:
            path = directory / f"{key}.md"
            if not path.is_file():
                continue
            match = OWNER_SECTION.search(path.read_text(encoding="utf-8"))
            if match is None:
                disagreements.append((key, None, record.key))
                continue
            stated = match.group(1).strip()
            # Records write "Platform Department"; the slug is the first token.
            stated_key = _slug(stated.replace(" Department", ""))
            if stated_key != record.key:
                disagreements.append((key, stated, record.key))
    return disagreements


def read_departments(root: Path = ORGANIZATION_ROOT) -> List[DepartmentRecord]:
    """Every Department that has a resident record. No inference, no defaults."""
    departments: List[DepartmentRecord] = []
    if not root.is_dir():
        return departments
    for directory in sorted(p for p in root.iterdir() if p.is_dir()):
        if directory.name in NON_DEPARTMENT_DIRS:
            continue
        readme = directory / "README.md"
        if not readme.is_file():
            continue
        name = _read_name(readme)
        if name is None:
            continue
        capability_files = sorted((directory / "capabilities").glob("*.md"))
        definition_files = sorted((directory / "agent-definitions").glob("*.md"))
        departments.append(
            DepartmentRecord(
                key=directory.name,
                name=name,
                record=_record_path(readme),
                capabilities=tuple(_slug(p.stem) for p in capability_files),
                agent_definitions=tuple(_slug(p.stem) for p in definition_files),
                establishing_adrs=_establishing_adr(readme),
            )
        )
    return departments


class OrganizationRootNotEstablished(RuntimeError):
    """The Domain Model's Organization row is absent or no longer a single root."""


DOMAIN_MODEL = REPO_ROOT / "docs/architecture/domain-model/canonical-domain-model-v1.md"

#: The Canonical Domain Model's entity row for Organization. The row must both
#: name the whole and assert a *single root identity*; either half missing means
#: the premise this derivation rests on has changed.
ORGANIZATION_ROW = re.compile(
    r"^\|\s*\*\*Organization\*\*\s*\|\s*The whole of\s+(?P<name>[^.|]+)\.\s*"
    r"(?P<rest>[^|]*)\|",
    re.M,
)


def organization_key(root: Path = ORGANIZATION_ROOT) -> str:
    """The single root Organization, **derived from the Domain Model**.

    An earlier version of this module refused here, reporting that no resident
    source established an Organization instance. **That was an over-reading, and
    it is corrected rather than kept.**

    `canonical-domain-model-v1.md` — the sole semantic authority under
    `Constitution §5` — defines the entity in its own table:

        | **Organization** | The whole of AIOS. Single root identity;
                             ultimate accountable body. |

    **For an entity whose definition is "the whole of AIOS" with a "single root
    identity", the type and its sole instance coincide.** There cannot be a
    second, so instantiating it is not choosing among alternatives and not
    creating an organizational unit. `organization_spec §12` confirms the
    direction of the reservation: what is *"not established"* is
    **"Multi-Organization topology *beyond a single root*"** — the single root
    is presupposed by the sentence that reserves everything past it.

    Representing that identity as a slug is a **projection**, not an
    establishment: `Domain Model §8` states that repository layout artifacts
    *"will be projections of this model, not extensions to it"*, and the
    Organization Framework's Naming Convention fixes slugs as *"lowercase,
    hyphenated slugs derived from their names."*

    **The reading is exposed rather than assumed.** If the Founder or Architect
    holds that instantiating the root requires its own ADR, this function is the
    single place to change, and `P10-DEPARTMENT-ECOSYSTEM-BASELINE.md` records
    the alternative reading alongside this one.

    Fails closed if the Domain Model row is absent or no longer asserts a single
    root — the premise would then be gone, and inventing a root is exactly what
    `FD-P10-003 §4.1` forbids.
    """
    if not DOMAIN_MODEL.is_file():
        raise OrganizationRootNotEstablished(f"{DOMAIN_MODEL} is not resident")
    match = ORGANIZATION_ROW.search(DOMAIN_MODEL.read_text(encoding="utf-8"))
    if match is None:
        raise OrganizationRootNotEstablished(
            "the Canonical Domain Model's Organization entity row was not found "
            "in the expected form; the derivation's premise is gone"
        )
    if "single root identity" not in match.group("rest").lower():
        raise OrganizationRootNotEstablished(
            "the Domain Model no longer asserts a single root identity for "
            "Organization; a root may not be chosen without it"
        )
    return _slug(match.group("name"))


def build_graph(root: Path = ORGANIZATION_ROOT):
    """Construct the frozen ``OwnershipGraph`` from resident records.

    Raises `OrganizationRootNotEstablished` when the root is absent, which is
    the current state. The graph is not partially built and no placeholder root
    is substituted: a Department parented to an invented Organization would be a
    fabricated ownership edge, which is the one thing `§4.1` forbids outright.
    """
    sys.path.insert(0, str(REPO_ROOT))
    from native_core.core.capability.ownership import (  # noqa: E402
        Department,
        DepartmentIdentity,
        Organization,
        OrganizationIdentity,
        OwnershipGraph,
    )

    key = organization_key(root)          # raises if not established
    organization = Organization(OrganizationIdentity(key))
    departments = tuple(
        Department(
            identity=DepartmentIdentity(record.key),
            organization=organization.identity,
            owned_capabilities=record.capabilities,
            owned_agent_definitions=record.agent_definitions,
        )
        for record in read_departments(root)
    )
    return OwnershipGraph(organizations=(organization,), departments=departments)


def report(root: Path = ORGANIZATION_ROOT) -> dict:
    departments = read_departments(root)
    result = {
        "departments": departments,
        "capabilities": sum(len(d.capabilities) for d in departments),
        "agent_definitions": sum(len(d.agent_definitions) for d in departments),
        "organization_root": None,
        "graph_constructed": False,
    }
    try:
        result["organization_root"] = organization_key(root)
    except OrganizationRootNotEstablished as exc:
        result["blocked_reason"] = str(exc)
        return result
    graph = build_graph(root)
    result["graph_constructed"] = True
    # INV-1 / INV-2 evidence, from the frozen graph's own queries — this module
    # asserts nothing about the invariants, it reports what the graph reports.
    result["inv1_unowned_capabilities"] = list(
        graph.unowned_capabilities(tuple(
            key for record in departments for key in record.capabilities
        ))
    )
    # Two-sided cross-check, done here rather than through
    # ``graph.disputed_ownership`` because that query takes Capability objects
    # and this module holds records, not entities. The property tested is the
    # same: does the Capability record's own ``## Owner`` section agree with the
    # Department directory it is nested under? `Organization Framework` calls
    # that nesting *"a direct filesystem projection of the Canonical Domain
    # Model's ownership relationship"*, so a disagreement is a real defect.
    result["inv1_disputed"] = _owner_disagreements(departments, root)
    result["inv2_unowned_agent_definitions"] = list(
        graph.unowned_agent_definitions(tuple(
            key for record in departments for key in record.agent_definitions
        ))
    )
    # ``disputed_agent_definition_ownership`` takes (definition, named-department)
    # declarations. The only declaration these records carry **is** the nesting,
    # so feeding it back would compare nesting against itself and pass by
    # construction. **A check that cannot fail is not evidence**, so it is not
    # run, and its absence is stated rather than hidden. The Capability side has
    # a real second declaration — the record's ``## Owner`` section — and is
    # cross-checked above.
    result["inv2_disputed"] = "NOT RUN — would be circular; see source"
    result["resolutions"] = {
        key: graph.owner_of(key).identity.department_key
        for record in departments for key in record.capabilities
    }
    return result


def main(argv: List[str]) -> int:
    result = report()
    print(f"departments read     : {len(result['departments'])}")
    for record in result["departments"]:
        print(f"  {record.name:<12} key={record.key:<12} "
              f"capabilities={len(record.capabilities)} "
              f"agent_definitions={len(record.agent_definitions)} "
              f"established_by={','.join(record.establishing_adrs)}")
    print(f"capabilities owned   : {result['capabilities']}")
    print(f"agent definitions    : {result['agent_definitions']}")
    print(f"organization root    : {result['organization_root'] or 'NOT ESTABLISHED'}")
    print(f"graph constructed    : {result['graph_constructed']}")
    if result["graph_constructed"]:
        print()
        print("INV-1 — every Capability owned by exactly one Department")
        print(f"  unowned            : {len(result['inv1_unowned_capabilities'])}")
        print(f"  record/nesting disagreements: {len(result['inv1_disputed'])}")
        for capability, stated, nested in result["inv1_disputed"]:
            print(f"    {capability}: record says {stated!r}, nested under {nested!r}")
        print("INV-2 — every Agent Definition owned by exactly one Department")
        print(f"  unowned            : {len(result['inv2_unowned_agent_definitions'])}")
        print(f"  disputed           : {result['inv2_disputed']}")
        print()
        print("resolved ownership:")
        for capability, department in sorted(result["resolutions"].items()):
            print(f"  {capability:<32} -> {department}")
    if not result["graph_constructed"]:
        print()
        print("BLOCKED — " + result["blocked_reason"])
        print()
        print("This is a finding, not a failure. The population is established;")
        print("the root it hangs from is not. No root was invented to proceed.")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
