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
#:
#: **Every entry must name a directory that actually exists**, and a test
#: enforces that. An exclusion naming nothing is not harmless: it silently
#: suppresses whatever later takes that name, which for this module means a
#: legitimately established Department would go missing from the population —
#: the exact mirror of admitting an unauthorized one. ``platform-runtime`` was
#: such an entry, speculatively added here and never a directory anywhere in
#: this repository; it was removed once the guard was written.
#:
#: ``delegations`` holds the P11 organizational delegation records placed here
#: by `DP-04 §8.3` and `DP-03 §8.2` — the organizational layer, outside the
#: frozen Native Core. It carries a ``README.md`` with an H1, which is exactly
#: the shape this loader reads as a Department, so **without this entry the
#: first P11 construction step would have introduced an unauthorized
#: Department** — `FD-P10-004 §5` condition 3 failing silently, by a directory
#: nobody declared. The guard below caught it on the run that created the
#: directory; this entry is the fix, and it names a directory that exists.
NON_DEPARTMENT_DIRS = {"execution-catalog", "delegations"}

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
    r"""The ADR the record says established it — **not every ADR it mentions**.

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


#: An Agent Definition record states its own owner and the Capability it
#: implements — **independently of where the file sits**. That independence is
#: what makes the cross-check below capable of failing.
DECLARED_DEPARTMENT = re.compile(r"^## Owning Department\s*\n\s*\n\[?([^\]\n(]+)", re.M)
DECLARED_CAPABILITY = re.compile(r"^## Implemented Capability\s*\n\s*\n\[?([^\]\n(]+)", re.M)


def unestablished(departments, root: Path = ORGANIZATION_ROOT):
    """Departments and Capabilities that cite **no establishing ADR**.

    `FD-P10-004 §5` condition 3 requires that *"no unauthorized Department has
    been introduced"*, and until this existed that condition was evidenced only
    by the observation that the resident population happens to be clean. **An
    observation is not a mechanism.** A directory added under the organization
    root with a README that never says *"established by"* was read, counted, and
    given an empty ``establishing_adrs`` tuple — silently, with nothing to
    distinguish it from an ADR-established one.

    `FD-P10-003 §4.1` fixes the permitted sources of the population, and
    `§24` says *"DO NOT INVENT THE DEPARTMENT MODEL."* A record that names no
    establishing authority has not been established by any of those sources.

    Returns ``(departments_without_adr, capabilities_without_adr)``. Reported,
    never raised: `PR-3` is detect-don't-decide, and refusing to load the
    population would hide the finding rather than surface it.
    """
    bare_departments = [r.key for r in departments if not r.establishing_adrs]
    bare_capabilities = []
    for record in departments:
        base = root / record.key / "capabilities"
        for key in record.capabilities:
            path = base / f"{key}.md"
            if not path.is_file():
                continue
            if not ESTABLISHED_BY.search(path.read_text(encoding="utf-8")):
                bare_capabilities.append((record.key, key))
    return bare_departments, bare_capabilities


def w4_chain(departments, root: Path = ORGANIZATION_ROOT):
    """`P10-W4`: DEPARTMENT → CAPABILITY → (work → execution → verification).

    Walks every Agent Definition record and closes the loop three ways:

    1. the Department it **declares** matches the Department it is **nested
       under** — two independent statements, so a mismatch is a real defect;
    2. the Capability it **declares implementing** is one that Department
       actually **owns** — which is `INV-2`'s second clause at record level;
    3. every owned Capability is reachable from at least one Agent Definition,
       or is reported unimplemented — `INV-14` forbids a Capability *"existing
       with zero implementers as a steady state"*.

    Returns ``(links, defects)``. **Defects are returned, never raised**: `PR-3`
    is detect-don't-decide, and the frozen `OwnershipGraph` follows the same rule.
    """
    links, defects = [], []
    implemented = set()
    for record in departments:
        base = root / record.key / "agent-definitions"
        for key in record.agent_definitions:
            path = base / f"{key}.md"
            if not path.is_file():
                defects.append(("missing-record", key, record.key, None))
                continue
            text = path.read_text(encoding="utf-8")
            dept = DECLARED_DEPARTMENT.search(text)
            cap = DECLARED_CAPABILITY.search(text)
            declared_dept = _slug(dept.group(1)) if dept else None
            declared_cap = _slug(cap.group(1)) if cap else None
            if declared_dept != record.key:
                defects.append(("department-mismatch", key, record.key, declared_dept))
            if declared_cap is None:
                defects.append(("no-declared-capability", key, record.key, None))
            elif declared_cap not in record.capabilities:
                defects.append(("capability-not-owned", key, record.key, declared_cap))
            else:
                implemented.add(declared_cap)
                links.append((record.key, declared_cap, key))
    for record in departments:
        for capability in record.capabilities:
            if capability not in implemented:
                defects.append(("capability-unimplemented", capability, record.key, None))
    return links, defects


#: Section headings an Agent Definition uses to declare what it may invoke, and
#: the execution-catalog subdirectory each one must point into.
PERMITTED_SECTIONS = {"Permitted Skills": "skill", "Permitted Workflows": "workflow"}

#: The bullet a Workflow record uses to name its invoker. `Domain Model §4` fixes
#: the relationship as **Workflow-invokes-Agent-Instance** — an *Instance*, never
#: a Definition. `FD-P10-004 §6` requires that distinction be held: *"Agent
#: Instance objects that are explicitly transient and non-owned must not be
#: misclassified as Agent Definitions."*
INVOKER_BULLET = re.compile(
    r"^-\s+\*\*Invokes Agent Instance:\*\*(.*?)(?=^-\s+\*\*|\Z)", re.M | re.S)
CONTAINS_SKILL_BULLET = re.compile(
    r"^-\s+\*\*Contains Skill:\*\*(.*?)(?=^-\s+\*\*|\Z)", re.M | re.S)
INSTANCE_PHRASE = re.compile(r"Agent Instance of", re.I)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _section(text: str, heading: str) -> str:
    """The body of ``## <heading>``, up to the next ``## `` or end of document."""
    match = re.search(
        r"^##\s+" + re.escape(heading) + r"\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    return match.group(1) if match else ""


def _catalog_links(section: str, source: Path, kind: str) -> List[Path]:
    """Links in ``section`` that resolve inside ``execution-catalog/<kind>/``.

    Every other link is **ignored as incidental prose**, not treated as a
    declaration — these sections routinely cite the ADR that resolved minimum
    cardinality, and a citation is not a permission. This is the same rule
    `tools/validators/agent_integration.py` already applies; the two agree by
    construction rather than by coincidence.
    """
    found = []
    for target in MD_LINK.findall(section):
        resolved = (source.parent / target.split("#", 1)[0]).resolve()
        if resolved.parent.name == kind and resolved.parent.parent.name == "execution-catalog":
            found.append(resolved)
    return found


def w4_continuity(links, root: Path = ORGANIZATION_ROOT):
    """Continue each `w4_chain` link into WORKFLOW → SKILL, and close the join.

    `w4_chain` ends at the Agent Definition and the Agent Integration Validator
    begins there; **nothing joined them**, so the composed path a Department
    actually originates was evidenced only by two independently verified halves
    sitting next to each other. This walks the whole thing as one chain, which
    is what `FD-P10-004 §8` asks to be evidenced and what `§10` condition 4
    means by *"verification mechanisms actually test the claimed invariants."*

    Four things can fail, and each is a real structural claim:

    1. a declared Workflow has no record on disk;
    2. a declared Workflow does not cite back to the Agent Definition that
       declared it — the reciprocity that makes the join sound rather than
       assumed;
    3. a Workflow names its invoker **without** the words *Agent Instance* —
       `Domain Model §4` fixes the relationship as Workflow-invokes-*Instance*,
       and a Workflow invoking a Definition directly would be precisely the
       misclassification `FD-P10-004 §6` forbids;
    4. a Skill a Workflow **contains** is permitted by **none of the Agent
       Definitions the Workflow names as invokers** — a Workflow may not smuggle
       in a capability no invoker was ever granted.

       **Widened under `DP-02 §11` item 10, and widened rather than relaxed.**
       This required *this* Definition to permit *every* contained Skill, which
       silently assumed one invoker per Workflow. `Domain Model §4` fixes no such
       cardinality on ``Workflow invokes Agent Instance``, and its own
       ``collaborates with`` edge makes the assumption untenable: instances
       collaborate *"only through a shared Workflow"*, so a Workflow that could
       invoke only one instance would make instance collaboration impossible in
       the model that requires it.

       The check still rejects the fabrication case — a Skill no invoker
       permits — and still requires reciprocity. What it no longer does is
       demand that an Engineering Definition permit a governance Skill in order
       for the two Departments to appear in one Workflow, which would have been
       authority expansion dressed as a conformance fix.

    Returns ``(chains, terminal, defects)``. ``terminal`` lists Agent Definitions
    that declare no Workflow: that is **not a defect**. `Domain Model §7`
    invariant 15 and `ADR-0007` make an empty declaration a valid architectural
    state, and manufacturing a Workflow to lengthen a chain would be the
    cosmetic construction `FD-P10-004 §27` forbids. Defects are returned, never
    raised — `PR-3` is detect-don't-decide.
    """
    catalog = root / "execution-catalog"
    chains, terminal, defects = [], [], []
    for department, capability, agent_definition in links:
        source = root / department / "agent-definitions" / f"{agent_definition}.md"
        if not source.is_file():
            defects.append(("missing-agent-definition", agent_definition, department, None))
            continue
        text = source.read_text(encoding="utf-8")
        permitted_skills = {
            p.stem for p in _catalog_links(_section(text, "Permitted Skills"), source, "skill")}
        workflows = _catalog_links(_section(text, "Permitted Workflows"), source, "workflow")
        if not workflows:
            terminal.append((department, capability, agent_definition))
            continue
        for workflow in workflows:
            if not workflow.is_file():
                defects.append(("workflow-missing", workflow.stem, agent_definition, None))
                continue
            body = workflow.read_text(encoding="utf-8")
            invoker = INVOKER_BULLET.search(body)
            cited = set()
            if invoker is None:
                defects.append(("workflow-names-no-invoker", workflow.stem, agent_definition, None))
            else:
                cited = {
                    (workflow.parent / t.split("#", 1)[0]).resolve()
                    for t in MD_LINK.findall(invoker.group(1))
                }
                if source.resolve() not in cited:
                    defects.append(
                        ("workflow-not-reciprocal", workflow.stem, agent_definition, None))
                if not INSTANCE_PHRASE.search(invoker.group(1)):
                    defects.append(
                        ("workflow-invokes-definition-directly", workflow.stem,
                         agent_definition, None))
            contained = CONTAINS_SKILL_BULLET.search(body)
            skills = (
                [p.stem for p in _catalog_links(contained.group(1), workflow, "skill")]
                if contained else [])
            # The Skills any invoker of this Workflow permits, resolved from
            # the Workflow's own invoker citations rather than from the
            # Definition currently being walked. `cited` is the same set the
            # reciprocity check above uses, so the two cannot disagree about
            # who the invokers are.
            invoker_permitted = set(permitted_skills)
            for target in (cited if invoker is not None else ()):
                if target.is_file() and target.parent.name == "agent-definitions":
                    invoker_permitted |= {
                        q.stem for q in _catalog_links(
                            _section(target.read_text(encoding="utf-8"),
                                     "Permitted Skills"), target, "skill")}
            for skill in skills:
                if not (catalog / "skill" / f"{skill}.md").is_file():
                    defects.append(("skill-missing", skill, workflow.stem, agent_definition))
                elif skill not in invoker_permitted:
                    defects.append(
                        ("skill-not-permitted", skill, workflow.stem, agent_definition))
            chains.append((department, capability, agent_definition, workflow.stem, tuple(skills)))
    return chains, terminal, defects


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


@dataclass(frozen=True)
class WorkEntry:
    """A resolved entry point into the Department Ecosystem.

    **This is not a Work entity.** `Freeze §2` lists `Task`, `Goal` and `Event`
    among *reserved concepts with no ratified entity*, and `Freeze §4` states
    plainly *"No new entity."* Nothing here is stored, owned, versioned, traced
    or given a lifecycle — it is a **resolution result**, recomputed from the
    records on every call, and deleting this class costs AIOS no truth.

    What it answers is `P10-W8` test 1 and test 2 together — *"work masuk"* and
    *"capability dipilih"* — **from the Department side**: given a Capability a
    request names, which Department is accountable, and which Agent Definition
    implements it. Execution then proceeds through the already-certified
    Workflow path (`E9-03`); this class does not execute anything.
    """

    capability: str
    department: str
    agent_definition: str
    establishing_adr: str


class WorkEntryUnresolved(LookupError):
    """The named Capability does not resolve to an accountable Department.

    Fails closed rather than returning a partial entry: `INV-1` requires
    *exactly one* owning Department, and an entry that could not name one would
    be work entering an organization that has not accepted it.
    """


def resolve_work_entry(capability_key: str, root: Path = ORGANIZATION_ROOT) -> WorkEntry:
    """Resolve a named Capability to the Department accountable for it.

    `P10-W8` test 1 (*work masuk*) and test 2 (*capability dipilih*), answered
    from resident records and the frozen ownership graph. Raises rather than
    guessing — see `WorkEntryUnresolved`.
    """
    departments = read_departments(root)
    links, _ = w4_chain(departments, root)
    for department, capability, agent_definition in links:
        if capability != capability_key:
            continue
        record = next(r for r in departments if r.key == department)
        return WorkEntry(
            capability=capability,
            department=department,
            agent_definition=agent_definition,
            establishing_adr=record.establishing_adrs[0] if record.establishing_adrs else "",
        )
    raise WorkEntryUnresolved(
        f"{capability_key!r} resolves to no accountable Department; INV-1 "
        "requires exactly one, and a partial entry is not returned"
    )


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
    bare_departments, bare_capabilities = unestablished(departments, root)
    result["unestablished_departments"] = bare_departments
    result["unestablished_capabilities"] = bare_capabilities
    links, defects = w4_chain(departments, root)
    result["w4_links"] = links
    result["w4_defects"] = defects
    chains, terminal, continuity_defects = w4_continuity(links, root)
    result["continuity_chains"] = chains
    result["continuity_terminal"] = terminal
    result["continuity_defects"] = continuity_defects
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
    bare_d = result.get("unestablished_departments", [])
    bare_c = result.get("unestablished_capabilities", [])
    print(f"unestablished        : {len(bare_d)} department(s), {len(bare_c)} capability(ies)")
    for key in bare_d:
        print(f"    UNAUTHORIZED DEPARTMENT — {key} cites no establishing ADR")
    for dept, key in bare_c:
        print(f"    UNAUTHORIZED CAPABILITY — {dept}/{key} cites no establishing ADR")
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
        print("P10-W4 chain — DEPARTMENT -> CAPABILITY -> AGENT DEFINITION")
        print(f"  closed links       : {len(result['w4_links'])}")
        print(f"  defects            : {len(result['w4_defects'])}")
        for kind, key, dept, extra in result["w4_defects"]:
            print(f"    {kind}: {key} ({dept}) {extra or ''}")
        for dept, cap, agent in sorted(result["w4_links"]):
            print(f"    {dept} -> {cap} -> {agent}")
        print()
        print("continuity — ... -> AGENT DEFINITION -> WORKFLOW -> SKILL")
        print(f"  closed chains      : {len(result['continuity_chains'])}")
        print(f"  defects            : {len(result['continuity_defects'])}")
        for kind, key, owner, extra in result["continuity_defects"]:
            print(f"    {kind}: {key} ({owner}) {extra or ''}")
        for dept, cap, agent, workflow, skills in sorted(result["continuity_chains"]):
            print(f"    {dept} -> {cap} -> {agent} -> {workflow} -> {len(skills)} skill(s)")
        print(f"  terminal at agent definition: {len(result['continuity_terminal'])}")
        for dept, cap, agent in sorted(result["continuity_terminal"]):
            print(f"    {dept} -> {cap} -> {agent} (declares no Workflow)")
        if result["continuity_terminal"]:
            print("    ^ valid per Domain Model INV-15 / ADR-0007; not a defect,")
            print("      and no Workflow was manufactured to lengthen these chains.")
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
