"""P12-W2 — the independent verifier of unified operational state (`§33`).

`ACT-CC-P12-W2-001 §33` forbids a verifier that depends on the implementation
writer. This module therefore **imports nothing from
`tools.p12_operational_state`**. It re-declares what a source must satisfy,
resolves every declared read path against the filesystem itself, and checks the
properties the Act names — provenance, ownership, freshness, authority
containment — against the projection's *output* rather than against its code.

**One dependency is unavoidable and is disclosed**: the verifier must obtain the
projection in order to judge it, so it imports the module's `project` and
`SOURCES` **as data**, by name, through `importlib`, and asserts nothing about
how they were produced. `§33` requires disclosure where a shared dependency
cannot be avoided; this is that disclosure. Every *property* checked below is
re-derived here — the read paths are resolved by this module, the freshness
vocabulary is re-declared here, and the authority-containment check is written
here and does not call the writer's own `is_authority`.

A verdict of `VERIFIED` means these named properties held on this projection at
this moment. It does not mean the state is correct.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

VERIFIED = "VERIFIED"
VIOLATED = "VIOLATED"
UNAVAILABLE = "UNAVAILABLE"

#: Re-declared here rather than imported, so a change to the writer's vocabulary
#: is a visible failure instead of an invisible agreement.
PERMITTED_STATUSES = frozenset({"CURRENT", "STALE", "UNKNOWN", "CONFLICTING",
                                "RESERVED", "BLOCKED"})

#: What `F-17` leaves undetermined. Re-declared for the same reason.
UNRESOLVED_MARKER = "UNRESOLVED"

#: Words that would make a projected value read as a permission. `§28`:
#: `SYSTEM-READABLE STATE ≠ GOVERNANCE AUTHORITY`.
AUTHORITY_WORDS = ("authorized", "authorised", "certified", "ratified",
                   "approved", "permitted", "granted_authority")


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def _surface():
    return importlib.import_module("tools.p12_operational_state")


def _check_declared_paths_resolve() -> Check:
    """Every declared source must point at something that exists."""
    module = _surface()
    missing = [s.state_id for s in module.SOURCES
               if not (REPO_ROOT / s.read_path).exists()]
    if missing:
        return Check("declared read paths resolve", VIOLATED,
                     f"{len(missing)} declared source(s) point at nothing: "
                     f"{missing}")
    return Check("declared read paths resolve", VERIFIED,
                 f"all {len(module.SOURCES)} declared read paths exist")


def _check_every_entry_has_provenance() -> Check:
    """`§36` — where did this state come from, when, by what transformation."""
    module = _surface()
    incomplete = []
    for entry in module.project():
        if not (entry.source and entry.observed_at and entry.transformation
                and entry.authority):
            incomplete.append(entry.state_id)
    if incomplete:
        return Check("every entry carries provenance", VIOLATED,
                     f"{len(incomplete)} entries lack provenance: {incomplete}")
    return Check("every entry carries provenance", VERIFIED,
                 "source, observed_at, transformation and authority on each")


def _check_observed_at_is_fresh() -> Check:
    """A projection re-derived on each call cannot carry an old timestamp.

    This is the property that distinguishes a projection from a store: if any
    entry's `observed_at` predates this verification run, something cached it.
    """
    started = datetime.now(timezone.utc)
    module = _surface()
    entries = module.project()
    stale = []
    for entry in entries:
        try:
            observed = datetime.fromisoformat(entry.observed_at)
        except ValueError:
            stale.append(entry.state_id)
            continue
        if observed < started:
            stale.append(entry.state_id)
    if stale:
        return Check("projection is re-derived, not cached", VIOLATED,
                     f"{len(stale)} entries carry a timestamp older than this "
                     f"run: {stale}")
    return Check("projection is re-derived, not cached", VERIFIED,
                 f"all {len(entries)} entries observed after this run began")


def _check_statuses_are_distinct() -> Check:
    """`§14` — CURRENT / STALE / UNKNOWN must stay semantically separate."""
    module = _surface()
    unknown_words = [e.state_id for e in module.project()
                     if e.status not in PERMITTED_STATUSES]
    if unknown_words:
        return Check("status vocabulary is the declared one", VIOLATED,
                     f"statuses outside {sorted(PERMITTED_STATUSES)}: "
                     f"{unknown_words}")
    return Check("status vocabulary is the declared one", VERIFIED,
                 f"every status is one of {sorted(PERMITTED_STATUSES)}")


def _check_absence_is_not_negative() -> Check:
    """`§14` of the Act — absence must not be projected as a negative state."""
    module = _surface()
    offenders = [e.state_id for e in module.project()
                 if e.value is None and e.status != "UNKNOWN"]
    if offenders:
        return Check("absence yields UNKNOWN, not a negative", VIOLATED,
                     f"{offenders} carry no value but are not UNKNOWN")
    return Check("absence yields UNKNOWN, not a negative", VERIFIED,
                 "every entry with no value is UNKNOWN")


def _check_no_entry_reads_as_authority() -> Check:
    """`§28` — nothing projected may read as a permission.

    Written here, and it does not call the writer's own `is_authority`: a
    surface asserting its own harmlessness proves nothing.
    """
    module = _surface()
    offenders = []
    for entry in module.project():
        for key in (entry.state_id, str(entry.value)):
            lowered = key.lower()
            for word in AUTHORITY_WORDS:
                if f"{word}=true" in lowered.replace(" ", "") or \
                        f"'{word}': true" in lowered:
                    offenders.append((entry.state_id, word))
    if offenders:
        return Check("no projected value reads as a permission", VIOLATED,
                     f"{offenders}")
    return Check("no projected value reads as a permission", VERIFIED,
                 "no entry asserts an authorization or certification")


def _check_providers_unresolved() -> Check:
    """`§17`/`§18` — `F-17` must not be resolved by this surface."""
    module = _surface()
    assigned = [s.state_id for s in module.SOURCES
                if UNRESOLVED_MARKER not in s.provider.upper()]
    if assigned:
        return Check("F-17 is not resolved by this surface", VIOLATED,
                     f"{len(assigned)} source(s) assign a provider: {assigned}")
    return Check("F-17 is not resolved by this surface", VERIFIED,
                 f"all {len(module.SOURCES)} providers remain unresolved")


def _check_sources_declare_their_portion() -> Check:
    """A claim nobody states cannot be checked against anyone else's."""
    module = _surface()
    silent = [s.state_id for s in module.SOURCES
              if not s.owns_within_class.strip()]
    if silent:
        return Check("every source states what it owns", VIOLATED,
                     f"{silent} claim a class without stating a portion")
    return Check("every source states what it owns", VERIFIED,
                 "each source names the portion of its class it owns")


def _check_no_duplicate_portion() -> Check:
    """`§17` — two sources must not claim the same portion of one class."""
    module = _surface()
    seen = {}
    duplicates = []
    for source in module.SOURCES:
        key = (source.state_class, source.owns_within_class.strip().lower())
        if key in seen:
            duplicates.append((seen[key], source.state_id))
        seen[key] = source.state_id
    if duplicates:
        return Check("no two sources claim one portion", VIOLATED,
                     f"{duplicates}")
    return Check("no two sources claim one portion", VERIFIED,
                 "each portion of each class has exactly one claimant")


CHECKS = (
    _check_declared_paths_resolve,
    _check_sources_declare_their_portion,
    _check_no_duplicate_portion,
    _check_every_entry_has_provenance,
    _check_observed_at_is_fresh,
    _check_statuses_are_distinct,
    _check_absence_is_not_negative,
    _check_no_entry_reads_as_authority,
    _check_providers_unresolved,
)


def verify() -> Tuple[Check, ...]:
    results = []
    for check in CHECKS:
        try:
            results.append(check())
        except Exception as exc:  # pragma: no cover - defensive
            results.append(Check(check.__name__, UNAVAILABLE,
                                 f"check raised: {exc}"))
    return tuple(results)


def summary() -> dict:
    results = verify()
    return {
        "checks": len(results),
        "verified": sum(1 for r in results if r.status == VERIFIED),
        "violated": sum(1 for r in results if r.status == VIOLATED),
        "unavailable": sum(1 for r in results if r.status == UNAVAILABLE),
        "not_verified": tuple(r.name for r in results if r.status != VERIFIED),
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.name:<42} {result.status:<12} {result.detail[:54]}")
    print()
    print("summary:", summary())
    print()
    print("Properties re-derived here, judged against the projection's output.")
    print("VERIFIED means these named properties held. Not that state is right.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
