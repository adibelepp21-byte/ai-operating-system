"""`P11-W3` ↔ operational ledger — the relation that was never built.

`ACT-CC-P11-012` proved the gap: two `ACTIVE` operational grants, neither
represented in W3, and the one W3 record on disk pointing at a **revoked**
grant. `tools/delegation_catalog.py` reported `defects: 0` throughout, truthfully
— its eleven checks all compare a record against the organizational
*population*, and not one of them looks at the *ledger the record is supposed to
be tracking*.

`FD-P11-001 §20` is the requirement:

    W3 Delegation is the organizational mechanism through which the authorized
    Delegation record is represented and tracked.

**Which layer owns what — read off the resident implementation, not chosen.**
`W4DelegationRegistry.issue()` mints `delegation_id`, stamps `issued_at`, and is
the only place a grant comes into existence; `revoke()` is the only transition
`ACTIVE → REVOKED`; the grant carries its own `AuthorityProvenance`. A W3 record
carries none of those — it carries organizational keys and prose. So:

    AUTHORIZED DELEGATION  →  OPERATIONAL LEDGER   (identity · lifecycle · provenance)
                                     ↓
                              RECONCILIATION       (this module — comparison only)
                                     ↓
                        W3 ORGANIZATIONAL REPRESENTATION   (projection)

**One canonical delegation, one projection** (`ACT-CC-P11-013 §6`). This module
creates no second delegation model: it holds no grants, issues none, and can
change no `status`. It reads two surfaces and reports where they disagree.

**Why a separate module** (`§27`). `delegation_catalog.verify()` resolves records
against the *organizational population* — Departments, Capabilities, instances.
Reconciliation resolves them against the *ledger*. Two different reference sets,
and folding the ledger into W3's loader would make the organizational layer
depend on operational state it does not own. Hosting it in `w4_continuity.py`
was the other candidate and was rejected for the mirror reason: that module is
W5 continuity, and W5 would then own W3 correctness.

**`§13` — reconciliation creates no authority.** It may detect, classify, and
update a projection of a grant that already exists. It may not convert `REVOKED`
to `ACTIVE`, admit a grant with unresolvable provenance, or write a record for a
grant the ledger does not hold. Those are not policy here; they are the
conditions under which `project()` refuses to write anything at all.
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

from tools.delegation_catalog import (  # noqa: E402
    DELEGATION_ROOT,
    operation_roots,
    MD_LINK,
    _section,
    read_delegations,
)

#: Every operational root that holds a ledger. Both are W4-shaped grants issued
#: by the same authorized delegator; `w1-operations` is where the W1
#: coordination proof persists its own, and a reconciliation that read only one
#: would report the other's live grants as unrepresented for the wrong reason.
#: Discovered, never listed — see `delegation_catalog.operation_roots`. A
#: hardcoded pair here refused to project a grant the moment a third
#: operational root was written, which is how this was found.
LEDGER_ROOTS = operation_roots()

#: The two sections this relation needs, and the **only** shape change it makes.
#:
#: Neither is a new concept, and neither is a delegation status.
#:
#: ``Operational Grant`` is where the record names the `delegation_id` it
#: represents. That identifier already existed — `ACT-CC-P11-013 §7` forbids
#: minting a new one — but it lived in prose inside a blockquote, where the only
#: way to recover it was to pattern-match sixteen hex characters out of an
#: English sentence. Giving it a declared home is what makes *"which grant does
#: this record represent?"* a question with an answer, and therefore what makes
#: drift detectable at all.
#:
#: ``Representation`` is a property of the **record**, not of the delegation:
#: whether this projection claims to be the live one or is preserved history.
#: `ACT-CC-P11-013 §5` forbids creating *"W3 status authority"* when the ledger
#: already owns lifecycle — so W3 never states `ACTIVE` or `REVOKED`. It states
#: what it is *for*, and the lifecycle it is checked against is read from the
#: ledger every time.
RECONCILIATION_SECTIONS = ("Operational Grant", "Representation")

CURRENT, HISTORICAL = "CURRENT", "HISTORICAL"
REPRESENTATION_ROLES = (CURRENT, HISTORICAL)

#: `w4_delegation.ACTIVE` / `REVOKED` are the only statuses the resident ledger
#: writes. The remaining four are **derived by this module from resident data**,
#: never stored as a status:
#:
#: ``SUPERSEDED`` a `REVOKED` grant named in some evidence record's
#:                ``superseded_grants`` — the rotation that `§14` requires be
#:                addressed left that trail already.
#: ``INVALID``    present, but its authority record does not resolve on disk.
#: ``MISSING``    referenced by a W3 record, absent from every ledger root.
#: ``UNKNOWN``    the ledger file exists and cannot be parsed. Corruption is not
#:                absence — the distinction `w4_continuity` already keeps.
ACTIVE, REVOKED = "ACTIVE", "REVOKED"
SUPERSEDED, INVALID, MISSING, UNKNOWN = (
    "SUPERSEDED", "INVALID", "MISSING", "UNKNOWN")

GRANT_ID = re.compile(r"^[0-9a-f]{16}$")


class ReconciliationError(RuntimeError):
    """Fail closed (`PR-4`)."""


@dataclass(frozen=True)
class LedgerGrant:
    """One operational grant as its record states it, plus derived lifecycle."""

    delegation_id: str
    lifecycle: str
    recipient_instance: Optional[str]
    capability_scope: Tuple[str, ...]
    authority_instrument: Optional[str]
    authority_record: Optional[str]
    accountable_party: Optional[str]
    source: str


def read_ledger(roots: Tuple[Path, ...] = LEDGER_ROOTS,
                repo_root: Path = REPO_ROOT) -> Dict[str, LedgerGrant]:
    """Every grant on disk, with lifecycle derived — never invented.

    An unreadable record is admitted as `UNKNOWN` rather than skipped. Skipping
    it would present corruption as absence, and absence and corruption lead to
    different defects here.
    """
    superseded: set = set()
    payloads: Dict[str, Tuple[Optional[dict], str]] = {}
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.glob("*.evidence.json")):
            try:
                evidence = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            superseded.update(evidence.get("superseded_grants", ()) or ())
        for path in sorted(root.glob("*.delegation.json")):
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                payloads[path.name[:-len(".delegation.json")]] = (None, str(path))
                continue
            key = record.get("delegation_id")
            if key:
                payloads[key] = (record, str(path))

    grants: Dict[str, LedgerGrant] = {}
    for key, (record, where) in payloads.items():
        try:
            source = str(Path(where).relative_to(repo_root))
        except ValueError:
            source = where
        if record is None:
            grants[key] = LedgerGrant(key, UNKNOWN, None, (), None, None, None,
                                      source)
            continue
        status = record.get("status")
        cited = record.get("authority_record")
        if status == ACTIVE and not (cited and (repo_root / cited).is_file()):
            # `§12`: a grant does not become valid because a record exists. An
            # active grant whose provenance no longer resolves is not active.
            lifecycle = INVALID
        elif status == REVOKED:
            lifecycle = SUPERSEDED if key in superseded else REVOKED
        elif status == ACTIVE:
            lifecycle = ACTIVE
        else:
            lifecycle = UNKNOWN
        grants[key] = LedgerGrant(
            delegation_id=key, lifecycle=lifecycle,
            recipient_instance=record.get("recipient_instance"),
            capability_scope=tuple(record.get("capability_scope") or ()),
            authority_instrument=record.get("authority_instrument"),
            authority_record=cited,
            accountable_party=record.get("accountable_party"),
            source=source)
    return grants


@dataclass(frozen=True)
class Projection:
    """What one W3 record claims about one operational grant."""

    key: str
    record: str
    grant_id: Optional[str]
    role: Optional[str]
    authorized_scope: Optional[str]
    delegated_actor: Optional[str]


def read_projections(root: Path = DELEGATION_ROOT,
                     repo_root: Path = REPO_ROOT) -> List[Projection]:
    """The reconciliation-bearing view of every resident W3 record."""
    found: List[Projection] = []
    for record in read_delegations(root):
        path = repo_root / record.record
        if not path.is_file():
            path = root / f"{record.key}.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        grant = _first_line(_section(text, "Operational Grant"))
        role = _first_line(_section(text, "Representation"))
        found.append(Projection(
            key=record.key, record=record.record,
            grant_id=grant if grant and GRANT_ID.match(grant) else grant,
            role=role.upper() if role else None,
            authorized_scope=record.authorized_scope,
            delegated_actor=record.delegated_actor))
    return found


def _first_line(body: Optional[str]) -> Optional[str]:
    """The first non-empty line of a section body, links stripped.

    ``.split("\\n")`` rather than ``splitlines()``: the latter also breaks on
    form feed and the Unicode line separators, so a record containing one would
    be read differently here than by every other loader in this corpus.
    """
    if not body:
        return None
    for line in body.split("\n"):
        line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line).strip()
        if line:
            return line
    return None


#: Each class names one way the projection and the ledger can disagree, and
#: each is decided by comparing **two independent statements** — never by
#: matching prose.
DEFECT_KINDS = (
    "unrepresented-active-grant",   # ledger ACTIVE, no CURRENT projection
    "stale-active-claim",           # CURRENT projection, grant not ACTIVE
    "unknown-grant",                # projection names a grant the ledger lacks
    "grant-reference-missing",      # projection names no grant at all
    "invalid-representation-role",  # role absent or not CURRENT/HISTORICAL
    "duplicate-representation",     # two CURRENT projections of one grant
    "history-claims-live-grant",    # HISTORICAL projection of an ACTIVE grant
    "provenance-mismatch",          # projection contradicts the grant it names
)


def reconcile(projections: Optional[List[Projection]] = None,
              grants: Optional[Dict[str, LedgerGrant]] = None,
              *, root: Path = DELEGATION_ROOT,
              roots: Tuple[Path, ...] = LEDGER_ROOTS,
              repo_root: Path = REPO_ROOT) -> dict:
    """Compare the organizational projection against the operational ledger.

    **Defects are returned, never raised** — `PR-3` is detect-don't-decide, and
    the same discipline `delegation_catalog.verify()` follows.

    Pure with respect to disk: given the same two inputs it returns the same
    result, which is what makes `§17` idempotency a property of the function
    rather than a claim about how it is called.
    """
    if projections is None:
        projections = read_projections(root, repo_root)
    if grants is None:
        grants = read_ledger(roots, repo_root)

    defects: List[Tuple[str, str, str]] = []
    current_of: Dict[str, List[str]] = {}

    for projection in projections:
        if projection.role not in REPRESENTATION_ROLES:
            defects.append(("invalid-representation-role", projection.key,
                            f"{projection.role!r} is not one of "
                            f"{list(REPRESENTATION_ROLES)}"))
        if not projection.grant_id:
            defects.append(("grant-reference-missing", projection.key,
                            "names no operational grant"))
            continue

        grant = grants.get(projection.grant_id)
        if grant is None:
            # `§11`: a W3 reference to a grant the ledger does not hold is not
            # a delegation. It fails, rather than being read as one.
            defects.append(("unknown-grant", projection.key,
                            f"{projection.grant_id} is in no ledger"))
            continue

        if projection.role == CURRENT:
            current_of.setdefault(projection.grant_id, []).append(projection.key)
            if grant.lifecycle != ACTIVE:
                # `§10`: W3 must not represent a revoked grant as live. This is
                # the defect `ACT-CC-P11-012` found and nothing could report.
                defects.append(("stale-active-claim", projection.key,
                                f"{projection.grant_id} is {grant.lifecycle}"))
        elif projection.role == HISTORICAL and grant.lifecycle == ACTIVE:
            defects.append(("history-claims-live-grant", projection.key,
                            f"{projection.grant_id} is {ACTIVE}"))

        # `§12`: the chain must still hold at the point of representation. A
        # projection that contradicts the grant it names is not tracking it.
        if projection.delegated_actor and grant.recipient_instance and \
                projection.delegated_actor != grant.recipient_instance:
            defects.append(("provenance-mismatch", projection.key,
                            f"actor {projection.delegated_actor} ≠ recipient "
                            f"{grant.recipient_instance}"))
        elif projection.authorized_scope and grant.capability_scope and \
                projection.authorized_scope not in grant.capability_scope:
            defects.append(("provenance-mismatch", projection.key,
                            f"scope {projection.authorized_scope} ∉ "
                            f"{list(grant.capability_scope)}"))

    for grant_id, keys in sorted(current_of.items()):
        if len(keys) > 1:
            defects.append(("duplicate-representation", ", ".join(sorted(keys)),
                            f"{len(keys)} CURRENT projections of {grant_id}"))

    # `§9`: every operationally ACTIVE delegation must be represented. A grant
    # that is `REVOKED`, `SUPERSEDED`, `INVALID` or `UNKNOWN` needs no
    # projection — `§20`: preserved history is not corruption.
    for grant_id, grant in sorted(grants.items()):
        if grant.lifecycle == ACTIVE and grant_id not in current_of:
            defects.append(("unrepresented-active-grant", grant_id,
                            f"ACTIVE in {grant.source}, no CURRENT W3 record"))

    return {
        "projections": projections,
        "grants": grants,
        "defects": defects,
        "active_grants": sorted(k for k, g in grants.items()
                                if g.lifecycle == ACTIVE),
        "represented_active": sorted(current_of),
        "lifecycles": {k: g.lifecycle for k, g in sorted(grants.items())},
    }


#: Where a `CURRENT` projection lives: one record per **recipient instance**,
#: not one per grant.
#:
#: The alternative — a file per grant, so every rotation leaves a new
#: `HISTORICAL` record behind — was rejected. The ledger already keeps every
#: grant it ever issued, `REVOKED` and readable, and derives `SUPERSEDED` from
#: the evidence trail; a parallel history in W3 would be a **second store of
#: the same facts**, which is the duplicate delegation model `§6` forbids in the
#: shape it is easiest to build by accident.
#:
#: `§16` is satisfied by what is *not* touched: `project()` writes only the
#: `CURRENT` record for an instance and **refuses to modify any record whose
#: role is `HISTORICAL`**. History someone chose to keep stays kept; history
#: nobody wrote down is still recoverable from the ledger.
PROJECTION_STEM = "w3-current-{context}-{instance}"


def _context_of(grant: "LedgerGrant") -> str:
    """The operational line of work a grant belongs to — its ledger directory.

    **The projection key gained this under `DP-02 §11` item 10, because one
    instance can hold more than one live grant.** It could not before: each
    operational root's run revokes that instance's ACTIVE grants in that root
    before issuing, so *within a root* an instance has exactly one. Keying on
    the instance alone silently assumed there was only ever one root per
    instance, and the first cross-Department run — which reuses both existing
    instances in a third root — overwrote the W4 and W1 projections and orphaned
    two live grants. Four reconciliation controls and two completeness guards
    fired on it.
    """
    name = Path(grant.source).parent.name
    return name[:-len("-operations")] if name.endswith("-operations") else name


def _render(grant: LedgerGrant, *, instrument_link: str,
            verification_link: str, boundary: str) -> str:
    """The record text for one `CURRENT` projection. Deterministic by
    construction — same grant in, byte-identical text out (`§17`)."""
    return "\n".join((
        f"# W3 Current Projection — {grant.recipient_instance}",
        "",
        "> **Generated by `tools/delegation_reconciliation.py`.** This record",
        "> **creates no authority.** It is the organizational projection of a",
        "> grant that already exists in the operational ledger, which owns the",
        "> identity, the lifecycle and the provenance. `FD-P11-001 §20`: W3",
        "> *\"must not manufacture authority absent valid provenance\"* — the",
        "> provenance is the grant's own, cited below, and it resolves.",
        ">",
        "> **Do not edit by hand.** A rotation rewrites this file to point at the",
        "> successor grant. To preserve a specific projection as history, give it",
        "> its own record with `## Representation: HISTORICAL`, which this",
        "> module will never modify.",
        "",
        "## Operational Grant",
        "",
        grant.delegation_id,
        "",
        "## Representation",
        "",
        CURRENT,
        "",
        "## Authority Source",
        "",
        "claude-code-aios-co-founder",
        "",
        f"The delegator `{grant.authority_instrument}` names.",
        "",
        "## Authorized Scope",
        "",
        grant.capability_scope[0] if grant.capability_scope else "",
        "",
        "## Delegated Actor",
        "",
        grant.recipient_instance or "",
        "",
        "## Boundary",
        "",
        boundary,
        "",
        "## Accountability",
        "",
        grant.accountable_party or "",
        "",
        "## Verification",
        "",
        verification_link,
        "",
        "## Authorizing Instrument",
        "",
        instrument_link,
        "",
    ))


def project(grant_id: str, *, grants: Optional[Dict[str, LedgerGrant]] = None,
            root: Path = DELEGATION_ROOT,
            roots: Tuple[Path, ...] = LEDGER_ROOTS,
            repo_root: Path = REPO_ROOT,
            evidence: Optional[str] = None) -> Path:
    """Write the `CURRENT` W3 projection of one **already-authorized** grant.

    `§13` — the refusals are what make this corrective rather than creative:

    * a grant the ledger does not hold cannot be projected at all;
    * a grant that is not `ACTIVE` cannot become a `CURRENT` projection, so
      `REVOKED → ACTIVE` is unreachable through this path;
    * a grant whose authority record does not resolve on disk is `INVALID`
      before it arrives here, and is refused on that ground.

    Returns the path written. Writing is skipped when the text is unchanged, so
    repeated calls against unchanged state touch nothing (`§17`).
    """
    if grants is None:
        grants = read_ledger(roots, repo_root)
    grant = grants.get(grant_id)
    if grant is None:
        raise ReconciliationError(
            f"{grant_id!r} is in no operational ledger — `§11`: a W3 reference "
            "to an absent grant is not a delegation")
    if grant.lifecycle != ACTIVE:
        raise ReconciliationError(
            f"{grant_id!r} is {grant.lifecycle}; only an ACTIVE grant may be "
            "projected as CURRENT — `§13`: reconciliation may not convert "
            "revoked to active")
    if not grant.recipient_instance:
        raise ReconciliationError(
            f"{grant_id!r} names no recipient instance")
    if not (grant.authority_record
            and (repo_root / grant.authority_record).is_file()):
        raise ReconciliationError(
            f"{grant_id!r} cites {grant.authority_record!r}, which does not "
            "resolve — `§12`: provenance must remain valid")

    root.mkdir(parents=True, exist_ok=True)
    path = root / ("%s.md" % PROJECTION_STEM.format(
        context=_context_of(grant), instance=grant.recipient_instance))

    existing_role = None
    if path.is_file():
        existing_role = _first_line(
            _section(path.read_text(encoding="utf-8"), "Representation"))
    if existing_role and existing_role.upper() == HISTORICAL:
        raise ReconciliationError(
            f"{path.name} is preserved history and is never rewritten — `§16`")

    relative = Path(grant.authority_record)
    instrument = (f"[{relative.stem}]"
                  f"({_relative_link(path.parent, repo_root / relative)})")
    evidence_path = (repo_root / evidence if evidence
                     else _evidence_for(grant, repo_root))
    verification = (
        f"[execution evidence]({_relative_link(path.parent, evidence_path)})"
        if evidence_path and evidence_path.is_file()
        else f"[the operational grant record]"
             f"({_relative_link(path.parent, repo_root / grant.source)})")
    boundary = (
        f"Bounded by the grant's own terms, recorded at `{grant.source}`. "
        "This projection adds no boundary and relaxes none; the ledger record "
        "is authoritative for scope, lifecycle and termination.")
    text = _render(grant, instrument_link=instrument,
                   verification_link=verification, boundary=boundary)
    if not path.is_file() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
    return path


def _evidence_for(grant: LedgerGrant, repo_root: Path) -> Optional[Path]:
    """The execution evidence naming this grant, if any is resident.

    Looked up **by delegation id inside the grant's own directory**, not by
    filename. Hardcoding one evidence filename is the defect `w4_continuity`
    already carried once, where the W1 run's evidence was read as absent
    because the reader only knew the W4 run's name.
    """
    directory = (repo_root / grant.source).parent
    if not directory.is_dir():
        return None
    for path in sorted(directory.glob("*.evidence.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if record.get("delegation_id") == grant.delegation_id:
            return path
    return None


def _relative_link(from_dir: Path, target: Path) -> str:
    """A POSIX relative link from one directory to a file, without resolving
    through symlinks — the same form the hand-written records already use."""
    import os
    return Path(os.path.relpath(target, from_dir)).as_posix()


def project_all(*, root: Path = DELEGATION_ROOT,
                roots: Tuple[Path, ...] = LEDGER_ROOTS,
                repo_root: Path = REPO_ROOT,
                evidence_for=None) -> Tuple[Path, ...]:
    """Project every `ACTIVE` grant. Idempotent, and returns what it wrote."""
    grants = read_ledger(roots, repo_root)
    written = []
    for grant_id, grant in sorted(grants.items()):
        if grant.lifecycle != ACTIVE:
            continue
        evidence = evidence_for(grant) if evidence_for else None
        written.append(project(grant_id, grants=grants, root=root, roots=roots,
                               repo_root=repo_root, evidence=evidence))
    return tuple(written)


def main(argv: List[str]) -> int:
    result = reconcile()
    grants = result["grants"]
    print(f"ledger grants        : {len(grants)}")
    for key, grant in sorted(grants.items()):
        print(f"  {key}  {grant.lifecycle:<11} {grant.source}")
    print(f"W3 projections       : {len(result['projections'])}")
    for projection in result["projections"]:
        print(f"  {projection.key:<44} {projection.role} → "
              f"{projection.grant_id}")
    print(f"active grants        : {len(result['active_grants'])}")
    print(f"represented active   : {len(result['represented_active'])}")
    defects = result["defects"]
    print(f"reconciliation defects: {len(defects)}")
    for kind, key, detail in defects:
        print(f"    {kind.upper()} — {key} ({detail})")
    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
