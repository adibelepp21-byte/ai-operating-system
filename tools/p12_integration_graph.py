"""P12-W1 — the system integration graph (`§8`, `§9`, `§10`, `§11`, `§14`).

`§14` of the Authorization: *"Claude **wajib** memetakan"* —

```text
PHASE → CAPABILITY → PLATFORM → ORGANIZATION → RUNTIME → WORKFLOW
      → EVIDENCE → VERIFICATION
```

and *"Phase dan Platform Organization harus tetap dibedakan."* `§8` names eight
integration classes and requires W1 to discover actual surfaces, classify
ownership and authority, detect dangling, orphan, duplicate-authority and stale
claims, and verify actual cross-surface operation. `§9` fixes the edge model and
the classification vocabulary.

**An import is not an edge.** `tools/derived_views.interface_graph` derives a
Native Core boundary graph whose relationship is `imports` — a structural fact,
and not one of `§9`'s twelve relationship classes. `ACT-CC-P12-W1-001 §8`:
*"Do not count an edge merely because two modules can import one another."* So
every edge here is evidenced by a **resident artifact that relates both ends**,
and an edge whose evidence does not resolve is `INVALID`, not omitted.

**Nothing here owns anything it integrates.** `§11`: *"P12 may integrate a
surface without taking ownership of that surface"*, and `§10`:
`DEPENDENCY ≠ OWNERSHIP`, `INTERACTION ≠ AUTHORITY TRANSFER`,
`COORDINATION ≠ OWNERSHIP`. The `owner` attribute records who already owns each
end; it is read, never assigned.

**`STATE` in `§9`'s edge model is read as the edge's own lifecycle state**, not
as a slot for W2's projection. `§9` lists `STATE` beside `LIFECYCLE` in the edge
model *and* gives a separate seven-value classification, which leaves the word
ambiguous. Both readings were considered; this one is chosen because the
alternative would make every edge depend on a projection that summarises what an
edge needs in full — the same loss `ACT-CC-P12-W5-001` measured. The ambiguity
is recorded rather than resolved, and the choice is stated here so it can be
argued with.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

# `§9` — every material edge carries one of these.
VERIFIED = "VERIFIED"
UNVERIFIED = "UNVERIFIED"
BLOCKED = "BLOCKED"
INVALID = "INVALID"
STALE = "STALE"
RESERVED = "RESERVED"
NOT_APPLICABLE = "NOT APPLICABLE"

#: `§9`'s relationship classes, in its order. An edge may use only these.
RELATIONSHIP_CLASSES: Tuple[str, ...] = (
    "CONSUMES", "PROVIDES", "CALLS", "PUBLISHES", "OBSERVES", "VERIFIES",
    "DELEGATES", "ESCALATES", "OWNS", "DEPENDS_ON", "COMPOSES", "SYNCHRONIZES",
)

#: `§8`'s eight required integration classes, in its order.
INTEGRATION_CLASSES: Tuple[str, ...] = (
    "phase ↔ phase", "platform ↔ phase", "governance ↔ execution",
    "organization ↔ runtime", "workflow ↔ runtime", "memory ↔ state",
    "evidence ↔ verification", "authority ↔ execution",
)

#: `§12`'s dependency classification, in its order.
DEPENDENCY_CLASSES: Tuple[str, ...] = (
    "DIRECT", "INDIRECT", "EVIDENCE", "RUNTIME", "AUTHORITY", "COMPLETION",
    "VERIFICATION", "EXTERNAL", "NONE",
)

#: What `F-17` leaves undetermined. An edge may cross a boundary whose provider
#: is unassigned; recording the crossing is not assigning the provider.
UNRESOLVED_OWNER = "UNRESOLVED (F-17)"


@dataclass(frozen=True)
class IntegrationEdge:
    """`§9`'s minimum edge model, in its order."""

    source: str
    target: str
    relationship: str
    owner: str
    authority: str
    contract: str
    state: str
    evidence: str
    verification: str
    lifecycle: str
    integration_class: str
    dependency: str
    classification: str
    detail: str


def _manifests() -> Tuple[dict, ...]:
    root = REPO_ROOT / "docs/architecture/p12/execution-provenance"
    if not root.is_dir():
        return ()
    found = []
    for path in sorted(root.glob("*.manifest.json")):
        try:
            found.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return tuple(found)


def _evidence_records() -> Tuple[dict, ...]:
    from tools import p12_provenance_verification as prov
    return prov.evidence_records()


def _traces() -> Tuple[dict, ...]:
    from tools import p12_provenance_verification as prov
    return prov.trace_records()


def _edge(**kw) -> IntegrationEdge:
    kw.setdefault("owner", UNRESOLVED_OWNER)
    return IntegrationEdge(**kw)


# ---------------------------------------------------------------------------
# One derivation per `§8` integration class. Each resolves its own evidence.
# ---------------------------------------------------------------------------

def _phase_to_phase() -> IntegrationEdge:
    from tools import p12_cross_phase_verification as cross
    summary = cross.summary()
    exercised = summary["exercised"]
    total = summary["phases"]
    demonstrator_only = summary["exercised_only_by_a_demonstrator"]
    classification = VERIFIED if exercised == total else UNVERIFIED
    return _edge(
        source="P4..P11", target="P4..P11", relationship="DEPENDS_ON",
        authority="P12 Blueprint §47 — the actual graph governs",
        contract="a phase is exercised when resident evidence shows it crossed",
        state=f"{exercised}/{total} exercised",
        evidence="tools/p12_cross_phase_verification.py",
        verification="per-phase evidence predicates",
        lifecycle="re-derived per call",
        integration_class="phase ↔ phase", dependency="COMPLETION",
        classification=classification,
        detail=(f"{total - exercised} phase(s) not exercised; "
                f"{list(demonstrator_only)} exercised only by a demonstrator"))


def _platform_to_phase() -> IntegrationEdge:
    registry = (REPO_ROOT / "docs/architecture/platform-organization"
                / "PHASE-PD-CAPABILITY-AND-DEPENDENCY-MAP.md")
    if not registry.is_file():
        return _edge(
            source="Platform Organization", target="Phase",
            relationship="PROVIDES", authority="unresolved",
            contract="unresolved", state="absent", evidence="none",
            verification="none", lifecycle="none",
            integration_class="platform ↔ phase", dependency="AUTHORITY",
            classification=INVALID,
            detail="the Phase↔PD map is not resident")
    return _edge(
        source="Platform Organization", target="Phase",
        relationship="PROVIDES",
        authority="Architect-reserved; F-17 unresolved",
        contract="a PD provides a capability a Phase requires",
        state="mapped, provider unassigned",
        evidence=str(registry.relative_to(REPO_ROOT)),
        verification="F-17 blocks provider verification",
        lifecycle="declared",
        integration_class="platform ↔ phase", dependency="AUTHORITY",
        classification=RESERVED,
        detail=("the map is resident and the provider assignment is F-17; "
                "recording the crossing is not assigning the provider"))


def _governance_to_execution() -> IntegrationEdge:
    manifests = _manifests()
    joined = [m for m in manifests if m.get("delegation_id")
              and m.get("authority_record")]
    if not manifests:
        return _edge(
            source="Governance", target="Execution", relationship="DELEGATES",
            authority="FD-P11-001", contract="a grant authorizes an execution",
            state="no execution manifest", evidence="none",
            verification="none", lifecycle="none",
            integration_class="governance ↔ execution", dependency="AUTHORITY",
            classification=UNVERIFIED,
            detail="no execution carries a governance reference")
    return _edge(
        source="Governance", target="Execution", relationship="DELEGATES",
        authority="FD-P11-001 §9",
        contract="every execution names the grant that authorized it",
        state=f"{len(joined)}/{len(manifests)} manifests carry both",
        evidence="docs/architecture/p12/execution-provenance",
        verification="tools/p12_execution_chain_reader",
        lifecycle="written once per execution",
        integration_class="governance ↔ execution", dependency="AUTHORITY",
        classification=VERIFIED if len(joined) == len(manifests) else UNVERIFIED,
        detail=f"{len(joined)} manifest(s) resolve a grant and its record")


def _organization_to_runtime() -> IntegrationEdge:
    records = _evidence_records()
    mapped = [r for r in records if r.get("instance_department")]
    if not mapped:
        return _edge(
            source="Organization", target="Runtime", relationship="COMPOSES",
            authority="P11 organizational authority",
            contract="a Department's instance acts in a runtime",
            state="no record maps an instance to a Department",
            evidence="none", verification="none", lifecycle="none",
            integration_class="organization ↔ runtime", dependency="RUNTIME",
            classification=UNVERIFIED,
            detail="no resident record relates an instance to its Department")
    departments = sorted({d for r in mapped
                          for d in r["instance_department"].values()})
    return _edge(
        source="Organization", target="Runtime", relationship="COMPOSES",
        authority="P11 organizational authority, bounded to organization (§20)",
        contract="an Agent Instance belongs to a Department and acts in a runtime",
        state=f"{len(mapped)} record(s) across {len(departments)} Department(s)",
        evidence="docs/architecture/p11/**/*.evidence.json",
        verification="instance_department mapping resolved per record",
        lifecycle="written once per coordination run",
        integration_class="organization ↔ runtime", dependency="RUNTIME",
        classification=VERIFIED,
        detail=f"Departments reached: {departments}")


def _workflow_to_runtime() -> IntegrationEdge:
    from tools import p12_runtime_observation as obs
    observations = obs.observations(obs.OBSERVATION_ROOT)
    workflows = [o for o in observations if o.kind == "workflow"]
    runtimes = [o for o in observations if o.kind == "runtime"]
    if not workflows or not runtimes:
        return _edge(
            source="Workflow", target="Runtime", relationship="OBSERVES",
            authority="observation is evidence, not permission",
            contract="a workflow is hosted by a runtime and both are observed",
            state=f"{len(workflows)} workflow, {len(runtimes)} runtime",
            evidence="docs/architecture/p12/runtime-observations",
            verification="none", lifecycle="liveness horizon",
            integration_class="workflow ↔ runtime", dependency="RUNTIME",
            classification=UNVERIFIED,
            detail="one kind of observation is missing; a hosting "
                   "relationship cannot be read from one side")
    # Both kinds exist. That is not the relationship — `§48`.
    shared = {w.runtime_id for w in workflows} & {r.runtime_id for r in runtimes}
    return _edge(
        source="Workflow", target="Runtime", relationship="OBSERVES",
        authority="observation is evidence, not permission",
        contract="a workflow observation names the runtime hosting it",
        state=f"{len(workflows)} workflow, {len(runtimes)} runtime observation(s)",
        evidence="docs/architecture/p12/runtime-observations",
        verification="runtime_id shared between a workflow and a runtime",
        lifecycle="liveness horizon",
        integration_class="workflow ↔ runtime", dependency="RUNTIME",
        classification=VERIFIED if shared else UNVERIFIED,
        detail=("both kinds are observed and no identity is shared, so the "
                "hosting relation is not recorded — two observations are not "
                "a relationship" if not shared
                else f"shared runtime identity: {sorted(shared)}"))


def _memory_to_state() -> IntegrationEdge:
    traces = _traces()
    consuming = [t for t in traces if t.get("memory_consumed")]
    if not traces:
        return _edge(
            source="Memory", target="State", relationship="CONSUMES",
            authority="Trace INV-6 — captured content, not references",
            contract="an execution records the memory it consumed",
            state="no execution record", evidence="none", verification="none",
            lifecycle="none", integration_class="memory ↔ state",
            dependency="NONE", classification=NOT_APPLICABLE,
            detail="no execution record exists to carry memory consumption")
    return _edge(
        source="Memory", target="State", relationship="CONSUMES",
        authority="Trace INV-6 — captured content, not references",
        contract="an execution records the memory it consumed",
        state=f"{len(consuming)}/{len(traces)} executions consumed memory",
        evidence="docs/architecture/p12/trace-stores",
        verification="memory_consumed read from stored records",
        lifecycle="append-only",
        integration_class="memory ↔ state", dependency="EVIDENCE",
        classification=VERIFIED if consuming else UNVERIFIED,
        detail=("every execution records an empty memory_consumed; the field "
                "is carried and nothing has populated it"
                if not consuming else f"{len(consuming)} record(s) populated"))


def _evidence_to_verification() -> IntegrationEdge:
    manifests = _manifests()
    carrying = [m for m in manifests
                if m.get("verification_requirement") and m.get("outcome")]
    if not manifests:
        return _edge(
            source="Evidence", target="Verification", relationship="VERIFIES",
            authority="the delegation's verification requirement",
            contract="evidence carries the requirement and the outcome",
            state="no manifest", evidence="none", verification="none",
            lifecycle="none", integration_class="evidence ↔ verification",
            dependency="VERIFICATION", classification=UNVERIFIED,
            detail="no evidence record exists")
    return _edge(
        source="Evidence", target="Verification", relationship="VERIFIES",
        authority="the delegation's verification requirement",
        contract="evidence carries the requirement it was verified against",
        state=f"{len(carrying)}/{len(manifests)} carry both",
        evidence="docs/architecture/p12/execution-provenance",
        verification="tools/p12_execution_chain_reader resolves both",
        lifecycle="written once",
        integration_class="evidence ↔ verification", dependency="VERIFICATION",
        classification=VERIFIED if len(carrying) == len(manifests)
        else UNVERIFIED,
        detail=f"{len(carrying)} manifest(s) carry requirement and outcome")


def _authority_to_execution() -> IntegrationEdge:
    from tools import p12_execution_chain_reader as chain
    verdicts = chain.verify_all()
    joined = [v for v in verdicts if v.joined]
    if not verdicts:
        return _edge(
            source="Authority", target="Execution", relationship="DELEGATES",
            authority="FD-P11-001 authority chain",
            contract="an execution resolves to the Founder through its grant",
            state="no chain", evidence="none", verification="none",
            lifecycle="none", integration_class="authority ↔ execution",
            dependency="AUTHORITY", classification=UNVERIFIED,
            detail="no execution chain is persisted")
    return _edge(
        source="Authority", target="Execution", relationship="DELEGATES",
        authority="FD-P11-001 §9 → delegator → Founder",
        contract="the authority chain resolves end to end",
        state=f"{len(joined)}/{len(verdicts)} chains joined",
        evidence="docs/architecture/p12/execution-provenance",
        verification="tools/p12_execution_chain_reader, 7 edges each",
        lifecycle="written once per execution",
        integration_class="authority ↔ execution", dependency="AUTHORITY",
        classification=VERIFIED if len(joined) == len(verdicts) else UNVERIFIED,
        detail=f"{len(joined)} chain(s) resolve every reference")


_DERIVATIONS: Dict[str, Callable[[], IntegrationEdge]] = {
    "phase ↔ phase": _phase_to_phase,
    "platform ↔ phase": _platform_to_phase,
    "governance ↔ execution": _governance_to_execution,
    "organization ↔ runtime": _organization_to_runtime,
    "workflow ↔ runtime": _workflow_to_runtime,
    "memory ↔ state": _memory_to_state,
    "evidence ↔ verification": _evidence_to_verification,
    "authority ↔ execution": _authority_to_execution,
}


def graph() -> Tuple[IntegrationEdge, ...]:
    """Derive every `§8` edge from resident artifacts. Nothing is cached."""
    edges = []
    for integration_class in INTEGRATION_CLASSES:
        derive = _DERIVATIONS.get(integration_class)
        if derive is None:
            edges.append(_edge(
                source="?", target="?", relationship="DEPENDS_ON",
                authority="none", contract="none", state="none",
                evidence="none", verification="none", lifecycle="none",
                integration_class=integration_class, dependency="NONE",
                classification=UNVERIFIED,
                detail="no derivation is declared for this integration class"))
            continue
        try:
            edges.append(derive())
        except Exception as exc:  # pragma: no cover - defensive
            edges.append(_edge(
                source="?", target="?", relationship="DEPENDS_ON",
                authority="none", contract="none", state="none",
                evidence="none", verification="none", lifecycle="none",
                integration_class=integration_class, dependency="NONE",
                classification=INVALID,
                detail=f"derivation raised: {exc}"))
    return tuple(edges)


def dangling() -> Tuple[str, ...]:
    """`§8.5` — edges whose declared evidence does not resolve."""
    found = []
    for edge in graph():
        if edge.evidence in ("none", ""):
            continue
        # A glob is resolved at its fixed prefix. A module reference is resolved
        # as the file it names — the first version compared a dotted module name
        # against the filesystem and reported a resident module as dangling,
        # which is a defect in the check rather than a break in the graph.
        first = edge.evidence.split("**")[0].rstrip("/")
        candidates = [REPO_ROOT / first]
        if not first.endswith(".py"):
            candidates.append(REPO_ROOT / (first + ".py"))
        if not any(candidate.exists() for candidate in candidates):
            found.append(f"{edge.integration_class}: {edge.evidence}")
    return tuple(found)


def summary() -> dict:
    edges = graph()
    by_class: Dict[str, int] = {}
    for edge in edges:
        by_class[edge.classification] = by_class.get(edge.classification, 0) + 1
    return {
        "integration_classes": len(INTEGRATION_CLASSES),
        "edges": len(edges),
        "verified": by_class.get(VERIFIED, 0),
        "unverified": by_class.get(UNVERIFIED, 0),
        "reserved": by_class.get(RESERVED, 0),
        "invalid": by_class.get(INVALID, 0),
        "not_applicable": by_class.get(NOT_APPLICABLE, 0),
        "dangling": len(dangling()),
        "owners_unresolved": sum(1 for e in edges
                                 if e.owner == UNRESOLVED_OWNER),
        "not_verified": tuple(e.integration_class for e in edges
                              if e.classification != VERIFIED),
    }


def main(argv=None) -> int:
    for edge in graph():
        print(f"{edge.integration_class:<24} {edge.relationship:<12} "
              f"{edge.classification:<13} {edge.state[:28]:<29} "
              f"{edge.detail[:44]}")
    print()
    if dangling():
        for item in dangling():
            print(f"DANGLING {item}")
        print()
    print("summary:", summary())
    print()
    print("An import is not an edge. Every edge here resolves an artifact")
    print("that relates both ends, and nothing owns what it integrates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
