"""P12-W2 — the Unified Operational State integration surface (`§13`–`§20`).

`§13`: *"P12-W2 is the canonical integration surface for system-wide Unified
Operational State"*, with the chain

```text
P11 ORGANIZATIONAL STATE → BOUNDED ORGANIZATIONAL PROJECTION
                         → P12 UNIFIED OPERATIONAL STATE
```

and the prohibition *"P12-W2 must not create a competing constitutional or
organizational authority model."* `§15` of the Authorization grants authority to
build a **state integration surface** for sources, consumers, lifecycle,
staleness, conflict, reconciliation, provenance and cross-phase relationships,
and closes: *"Claude tidak boleh menciptakan competing system-wide state
authority."*

**So this is a projection, not a store.** The canonical text settles the
question `ACT-CC-P12-W2-001 §19` poses — it names an integration surface and a
projection chain, never a store — and nothing here holds a durable copy of
anything a source already owns. Every entry is re-derived from its source on
every call, which is what makes a stale projection structurally impossible:
there is no second copy to drift.

**Sources are declared, never discovered by inference.** A registry built by
scanning for things that look like state would silently acquire whatever
appeared next, and its owner and authority columns would be guesses. Each entry
below names its own canonical source and authority, and a conformance control
fails if a declared read path does not resolve.

**This surface holds no authority.** `§28` of the Act:
`SYSTEM-READABLE STATE ≠ GOVERNANCE AUTHORITY`. Governance facts are carried as
*what an instrument declares*, attributed to that instrument, and `declares()`
is the only accessor — there is no field anyone can read as permission. `§29`
forbids establishing certification state, so no entry asserts one.

**Provider ownership is `UNRESOLVED` wherever `F-17` applies**, which is most of
the corpus. `IMPLEMENTATION LOCATION ≠ CANONICAL PROVIDER OWNERSHIP`, and a
projection that filled the column from the directory a reader happens to live in
would resolve `F-17` by convention — exactly what `§17`/`§18` forbid.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

# `§14` — the distinctions state must preserve. Absence is never a negative.
CURRENT = "CURRENT"
STALE = "STALE"
UNKNOWN = "UNKNOWN"
CONFLICTING = "CONFLICTING"
RESERVED = "RESERVED"
BLOCKED = "BLOCKED"

#: `§14`'s minimum state domains, in its order.
STATE_CLASSES: Tuple[str, ...] = (
    "IDENTITY", "AUTHORITY", "ARCHITECTURE", "CAPABILITY", "ORGANIZATION",
    "RUNTIME", "WORK", "EXECUTION", "OBSERVATION", "VERIFICATION", "EVIDENCE",
    "GOVERNANCE", "CHANGE", "DEPENDENCY", "RISK", "UNKNOWN", "STALE",
)

#: What `F-17` leaves undetermined. Not a value, and not a placeholder to be
#: filled in later by whoever needs it — a statement that canonical authority
#: has not assigned it.
UNRESOLVED_PROVIDER = "UNRESOLVED (F-17)"

#: `SOURCE OF TRUTH` vs everything else. `§12` of the Act requires the
#: classification be explicit rather than implied by where a reader lives.
SOURCE_OF_TRUTH = "SOURCE-OF-TRUTH"
DERIVED = "DERIVED"
OBSERVATIONAL = "OBSERVATIONAL"
GOVERNANCE_DECLARED = "GOVERNANCE-DECLARED"


@dataclass(frozen=True)
class StateSource:
    """One declared state-bearing surface. Declaration, not discovery."""

    state_id: str
    state_class: str
    semantics: str
    owner: str
    canonical_source: str
    read_path: str
    authority: str
    freshness_model: str
    #: What portion of its class this source owns. Two sources may share a
    #: class without conflicting — the escalation register and the governance
    #: index are both GOVERNANCE and hold different facts — so each must say
    #: what it owns. A class collision alone is a *candidate*, and the first
    #: version of the conflict detector reported one as a conflict.
    owns_within_class: str = ""
    provider: str = UNRESOLVED_PROVIDER

    def resolves(self, root: Path = REPO_ROOT) -> bool:
        return (root / self.read_path).exists()


@dataclass(frozen=True)
class StateEntry:
    """One projected state value, with the provenance `§36` requires."""

    state_id: str
    state_class: str
    status: str
    value: object
    source: str
    observed_at: str
    transformation: str
    authority: str
    provider: str
    semantics: str

    def is_authority(self) -> bool:
        """Always false, and deliberately so.

        `§28`: `SYSTEM-READABLE STATE ≠ GOVERNANCE AUTHORITY`. A consumer that
        wants to know whether something is authorized must read the instrument,
        not this projection. The method exists so that the answer is written
        down rather than assumed.
        """
        return False


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# The declared sources
# ---------------------------------------------------------------------------

SOURCES: Tuple[StateSource, ...] = (
    StateSource(
        state_id="runtime.observed",
        state_class="RUNTIME", semantics=OBSERVATIONAL,
        owner="P12-W4 runtime observation",
        canonical_source="Blueprint §30 Runtime Integration",
        read_path="docs/architecture/p12/runtime-observations",
        authority="observation is evidence, not permission",
        freshness_model="liveness horizon; LIVE / STALE / TERMINATED / UNKNOWN",
        owns_within_class="observed liveness of runtimes and workflows"),
    StateSource(
        state_id="execution.recorded",
        state_class="EXECUTION", semantics=SOURCE_OF_TRUTH,
        owner="Native Core Trace boundary",
        canonical_source="Blueprint §29 Canonical Execution Contract",
        read_path="docs/architecture/p12/trace-stores",
        authority="ratified Trace vocabulary; append-only",
        freshness_model="durable and historical; a record never becomes stale",
        owns_within_class="durable records of executions that ran"),
    StateSource(
        state_id="execution.provenance",
        state_class="EVIDENCE", semantics=SOURCE_OF_TRUTH,
        owner="P12-W4 execution provenance",
        canonical_source="Blueprint §34 Execution Provenance",
        read_path="docs/architecture/p12/execution-provenance",
        authority="FD-P11-001 delegation chain",
        freshness_model="written once per execution; never overwritten",
        owns_within_class="the relation joining an execution to its grant"),
    StateSource(
        state_id="delegation.granted",
        state_class="AUTHORITY", semantics=SOURCE_OF_TRUTH,
        owner="FD-P11-001 authorized delegator",
        canonical_source="FD-P11-001 §9",
        read_path="docs/architecture/p11/w4-operations",
        authority="Founder Decision FD-P11-001",
        freshness_model="ACTIVE / REVOKED / SUPERSEDED, derived from records",
        owns_within_class="operational grants and their lifecycle"),
    StateSource(
        state_id="escalation.raised",
        state_class="GOVERNANCE", semantics=SOURCE_OF_TRUTH,
        owner="escalation register",
        canonical_source="ACT-CC-P11-009 §13",
        read_path="docs/architecture/p11/w4-operations",
        authority="a refusal is not an approval",
        freshness_model="OPEN unless a response record exists beside it",
        owns_within_class="refusals raised and awaiting a governance response"),
    StateSource(
        state_id="organization.declared",
        state_class="ORGANIZATION", semantics=SOURCE_OF_TRUTH,
        owner="P11 organization",
        canonical_source="Blueprint §20 P11 → P12 boundary",
        read_path="docs/architecture/organization",
        authority="P11 organizational authority, bounded to organization",
        freshness_model="declared; changes only by organizational record",
        owns_within_class="Departments and their declared capabilities"),
    StateSource(
        state_id="governance.declared",
        state_class="GOVERNANCE", semantics=GOVERNANCE_DECLARED,
        owner="governance instruments",
        canonical_source="Blueprint §26 Governance Evidence",
        read_path="docs/governance",
        authority="the instrument itself; this projection carries no authority",
        freshness_model="hash-checked against the indexed source",
        owns_within_class="decision instruments and their indexed content"),
    StateSource(
        state_id="architecture.boundaries",
        state_class="ARCHITECTURE", semantics=SOURCE_OF_TRUTH,
        owner="Native Core",
        canonical_source="Blueprint §59 Native Core = 11 Frozen Boundaries",
        read_path="native_core/core",
        authority="frozen; no twelfth subsystem",
        freshness_model="structural; read from the tree on every call",
        owns_within_class="the frozen Native Core boundary set"),
)


# ---------------------------------------------------------------------------
# Projections — each re-derived from its source, never cached
# ---------------------------------------------------------------------------

def _project_runtime(source: StateSource) -> StateEntry:
    from tools import p12_runtime_observation as obs
    answer = obs.what_is_running(obs.OBSERVATION_ROOT)
    if not answer["answerable"]:
        # `§14` of the Act: absence is not a negative state.
        return _entry(source, UNKNOWN, None, answer.get("reason", ""),
                      "what_is_running over published observations")
    return _entry(
        source, CURRENT,
        {"live": answer["live"], "terminated": answer.get("terminated", ()),
         "observations": answer["observations"]},
        f"{answer['observations']} observation(s)",
        "what_is_running within the liveness horizon")


def _project_execution(source: StateSource) -> StateEntry:
    from tools import p12_trace_registry as traces
    summary = traces.what_has_run(traces.STORE_ROOT)
    if summary["stores"] == 0:
        return _entry(source, UNKNOWN, None, "no durable Trace store exists",
                      "trace registry discovery")
    failures = traces.what_has_failed(traces.STORE_ROOT)
    return _entry(
        source, CURRENT,
        {"records": summary["records"], "stores": summary["stores"],
         "failures": len(failures)},
        f"{summary['stores']} store(s)", "durable Trace records read back")


def _project_provenance(source: StateSource) -> StateEntry:
    from tools import p12_execution_provenance as prov
    found = prov.manifests()
    if not found:
        return _entry(source, UNKNOWN, None, "no manifest is persisted",
                      "manifest discovery")
    return _entry(
        source, CURRENT,
        {"manifests": len(found),
         "statuses": sorted({m.get("status") for m in found})},
        f"{len(found)} manifest(s)", "execution provenance manifests read back")


def _project_delegation(source: StateSource) -> StateEntry:
    from tools import p12_provenance_verification as prov
    records = prov.delegation_records()
    if not records:
        return _entry(source, UNKNOWN, None, "no delegation record is resident",
                      "delegation record discovery")
    active = [d for d in records if d.get("status") == "ACTIVE"]
    return _entry(
        source, CURRENT,
        {"grants": len(records), "active": len(active)},
        f"{len(records)} record(s)", "delegation records read as stored")


def _project_escalation(source: StateSource) -> StateEntry:
    from tools import p12_failure_verification as fail
    join = fail.escalation_join()
    if not join["records"]:
        # No escalation is not "nothing was refused". It is no evidence.
        return _entry(source, UNKNOWN, None, "no escalation record is resident",
                      "escalation record discovery")
    return _entry(
        source, CURRENT, dict(join), f"{join['records']} record(s)",
        "escalation records read as stored")


def _project_organization(source: StateSource) -> StateEntry:
    from tools import organization_catalog as org
    departments = org.read_departments(org.ORGANIZATION_ROOT)
    if not departments:
        return _entry(source, UNKNOWN, None,
                      "no Department record readable", "organization catalog")
    return _entry(
        source, CURRENT,
        {"departments": len(departments),
         "capabilities": sum(len(d.capabilities) for d in departments)},
        f"{len(departments)} Department record(s)",
        "organization catalog, bounded organizational projection (§20)")


def _project_governance(source: StateSource) -> StateEntry:
    from tools.governance_index import GovernanceIndex, tracked_markdown
    index, stats = GovernanceIndex.build(tracked_markdown(REPO_ROOT), REPO_ROOT)
    stale = index.stale_sources(REPO_ROOT)
    status = STALE if stale else CURRENT
    return _entry(
        source, status,
        {"records": len(index.records), "sources": stats.parsed,
         "stale_sources": len(stale)},
        f"{stats.parsed} source(s)",
        "governance index with per-source content hashes")


def _project_architecture(source: StateSource) -> StateEntry:
    from tools import derived_views as views
    boundaries = views._boundaries(REPO_ROOT)
    return _entry(
        source, CURRENT,
        {"boundaries": len(boundaries), "names": sorted(boundaries)},
        "native_core/core", "directory structure read on each call")


_PROJECTIONS: Dict[str, Callable[[StateSource], StateEntry]] = {
    "runtime.observed": _project_runtime,
    "execution.recorded": _project_execution,
    "execution.provenance": _project_provenance,
    "delegation.granted": _project_delegation,
    "escalation.raised": _project_escalation,
    "organization.declared": _project_organization,
    "governance.declared": _project_governance,
    "architecture.boundaries": _project_architecture,
}


def _entry(source: StateSource, status: str, value, origin: str,
           transformation: str) -> StateEntry:
    return StateEntry(
        state_id=source.state_id, state_class=source.state_class,
        status=status, value=value, source=f"{source.read_path} ({origin})",
        observed_at=_now(), transformation=transformation,
        authority=source.authority, provider=source.provider,
        semantics=source.semantics)


def project() -> Tuple[StateEntry, ...]:
    """Re-derive every declared source. Nothing is cached."""
    entries = []
    for source in SOURCES:
        projector = _PROJECTIONS.get(source.state_id)
        if projector is None:
            entries.append(_entry(source, UNKNOWN, None,
                                  "no projection is declared for this source",
                                  "none"))
            continue
        try:
            entries.append(projector(source))
        except Exception as exc:  # pragma: no cover - defensive
            # A projection that raises yields UNKNOWN, never a negative value.
            entries.append(_entry(source, UNKNOWN, None,
                                  f"projection raised: {exc}", "none"))
    return tuple(entries)


def conflicts() -> Tuple[dict, ...]:
    """`§17` — two surfaces claiming authority over **the same** system-wide state.

    Reported, never resolved here. `§17` says a conflict *"must be discovered
    and resolved or escalated"*, and resolving one means choosing between two
    authorities, which this surface does not hold.

    **A class collision is not a conflict.** The first version of this function
    compared state classes alone and reported `GOVERNANCE`, because the
    escalation register and the governance index are both governance state. They
    hold different facts and neither disputes the other's. That was a false
    positive produced by my own coarseness, and the fix is not to re-label the
    sources until the detector goes quiet — it is to make each source say what
    portion of its class it owns, and to fire only when two sources claim the
    same portion.

    A source that declares no portion is reported as `UNDECLARED`, which is a
    finding rather than an exemption: an unstated claim cannot be checked for
    conflict with anyone else's.
    """
    by_class: Dict[str, list] = {}
    undeclared = []
    for source in SOURCES:
        if source.semantics not in (SOURCE_OF_TRUTH, GOVERNANCE_DECLARED):
            continue
        if not source.owns_within_class.strip():
            undeclared.append(source)
            continue
        by_class.setdefault(source.state_class, []).append(source)

    found = []
    for source in undeclared:
        found.append({
            "state_class": source.state_class,
            "kind": "UNDECLARED",
            "claimants": (source.state_id,),
            "owners": (source.owner,),
            "detail": (f"{source.state_id} claims {source.state_class} without "
                       "saying what portion it owns; an unstated claim cannot "
                       "be checked against anyone else's"),
        })

    for state_class, sources in sorted(by_class.items()):
        portions: Dict[str, list] = {}
        for source in sources:
            portions.setdefault(source.owns_within_class.strip().lower(),
                                []).append(source)
        for portion, claimants in sorted(portions.items()):
            if len(claimants) > 1:
                found.append({
                    "state_class": state_class,
                    "kind": "CONFLICT",
                    "portion": portion,
                    "claimants": tuple(s.state_id for s in claimants),
                    "owners": tuple(s.owner for s in claimants),
                    "detail": (f"{len(claimants)} sources claim the same "
                               f"portion of {state_class}; resolution requires "
                               "an authority this surface does not hold"),
                })
    return tuple(found)


def declares(state_id: str) -> Optional[dict]:
    """What an instrument *declares*, attributed — never what is authorized.

    `§28`/`§29`: a projection may report that an instrument says something. It
    may not become the thing that says it. So the return carries the instrument
    it came from and is explicitly not an authorization, and there is no
    accessor anywhere on this surface that returns a bare permission.
    """
    for entry in project():
        if entry.state_id == state_id:
            return {
                "declared_by": entry.source,
                "value": entry.value,
                "is_authority": entry.is_authority(),
                "note": "a declaration read from a record; read the instrument "
                        "for authority",
            }
    return None


def summary() -> dict:
    entries = project()
    return {
        "sources": len(SOURCES),
        "projected": len(entries),
        "current": sum(1 for e in entries if e.status == CURRENT),
        "stale": sum(1 for e in entries if e.status == STALE),
        "unknown": sum(1 for e in entries if e.status == UNKNOWN),
        "unknown_states": tuple(e.state_id for e in entries
                                if e.status == UNKNOWN),
        "conflicts": sum(1 for c in conflicts() if c["kind"] == "CONFLICT"),
        "undeclared_claims": sum(1 for c in conflicts()
                                 if c["kind"] == "UNDECLARED"),
        "class_collisions": len({s.state_class for s in SOURCES}) < len(SOURCES),
        "providers_unresolved": sum(1 for s in SOURCES
                                    if s.provider == UNRESOLVED_PROVIDER),
    }


def main(argv=None) -> int:
    for entry in project():
        print(f"{entry.state_id:<26} {entry.state_class:<14} "
              f"{entry.status:<9} {entry.semantics:<20} "
              f"{str(entry.value)[:40]}")
    print()
    for conflict in conflicts():
        print(f"{conflict['kind']} {conflict['state_class']}: "
              f"{', '.join(conflict['claimants'])}")
    print()
    print("summary:", summary())
    print()
    print("A projection, not a store. Nothing here is authority, and every")
    print("provider column stays UNRESOLVED until F-17 is decided.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
