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
    """No Organization instance is canonically established.

    `Freeze §4` makes a Department *"owned by an Organization"*, and
    ``ownership.Department`` requires exactly one ``OrganizationIdentity`` and
    fails closed without one. **No resident ADR establishes an Organization
    instance**, and `organization_spec §12` records new Organizations as an
    extension mechanism rather than an existing fact.

    Naming one here would be creating an organizational unit — `FD-P10-003 §4.1`
    reserves that to an explicit Founder or Architect decision. **So this module
    refuses rather than supplying a root**, and the refusal is the finding.
    """


def organization_key(root: Path = ORGANIZATION_ROOT) -> str:
    """The canonically established Organization instance, if one exists."""
    for path in sorted(root.rglob("*.md")) if root.is_dir() else []:
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^## Organization\s*\n\s*\n(.+?)\s*$", text, re.M)
        if match:
            return _slug(match.group(1))
    raise OrganizationRootNotEstablished(
        "no resident record names an Organization instance; a Department cannot "
        "be constructed without one (Freeze §4). Establishing one is an "
        "architectural decision under Constitution §3.4 and Domain Model §6."
    )


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
    build_graph(root)
    result["graph_constructed"] = True
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
