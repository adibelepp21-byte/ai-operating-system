"""P12-W3 — certification, enforced rather than merely recorded.

Authorized by the Founder P12 Authorization `§16`, whose whole point is that
governance *"dapat diterapkan lintas layer"* — applied across layers, not simply
written down in one.

**The defect this closes (`F-12`).** `tools/w1_coordination_run.py` overwrites
`w1-coordination.evidence.json`, and every run mints a fresh delegation record.
Eight exist, spanning `03:32 → 07:33` on 2026-09-11, seven `REVOKED` and one
`ACTIVE`: the path was **designed** re-runnable, and during P11 construction that
was ordinary and correct.

`FD-P11-002` certified P11 later that day. **The operation did not change; its
meaning did.** The same re-run now overwrites certified-phase evidence, and
nothing in the repository noticed — a certification that constrains documents but
not behaviour is a record, not a boundary.

```text
CERTIFIED DOCUMENT   ≠   ENFORCED BOUNDARY
```

**What it does not do.** It does not forbid *executing* a certified phase's
proof. Execution is how observation evidence is produced, and `F-10′` depends on
being able to run work paths without rewriting history. It refuses only the
**persisting write** into a certified phase's evidence root. Run freely; overwrite
nothing.

**Certification is read from instrument bodies, never from names or prose.**
`IDENTIFIER ≠ DECISION BODY`, so the phase set comes from a certification
*statement* inside a resident instrument. Deriving it from the Register's prose
was tried and rejected: the Register contains the sentence *"It does **not**
establish `PHASE 8 — CERTIFIED / COMPLETE`"*, which every naive pattern reads as
a certification. A guard fooled by a negation is worse than no guard.

**It fails closed.** If governance cannot be read, certification cannot be
determined, and an undeterminable boundary is not an absent one — the write is
refused and the reason named.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import FrozenSet, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTS_ROOT = REPO_ROOT / "docs/governance/acts"
REGISTER = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"

#: A certification *statement*, as the resident instruments actually phrase it:
#: `FD-P11-002 §1` — "PHASE 11 — AUTONOMOUS ORGANIZATION IS CERTIFIED";
#: `FD-P10-005 §16` — "Phase 10 — Department Ecosystem is hereby certified as
#: COMPLETE". Both forms are matched; neither is inferred from a filename.
_CERTIFIES = re.compile(
    r"PHASE\s+(\d+)[^\n]{0,60}\bIS\s+CERTIFIED\b"
    r"|Phase\s+(\d+)[^\n]{0,80}\bis hereby certified\b"
)


#: Evidence roots for certified phases that do **not** follow the `p{N}`
#: directory convention. P10's certified evidence lives under
#: `platform-organization/`, and there is no `docs/architecture/p10/` at all.
#:
#: **Declared, because it cannot be derived.** Neither `FD-P10-005` nor
#: `FD-P11-002` names a path in its body, so there is no instrument text to
#: anchor this on, and inferring a root from identifier density would be the
#: kind of guess this module exists to refuse. It is declared openly and made
#: *verified rather than remembered* by a conformance test that fails the moment
#: a certified phase has no resolvable root.
PHASE_EVIDENCE_ROOTS = {
    10: "docs/architecture/platform-organization",
}


class CertificationUndeterminable(RuntimeError):
    """Governance could not be read, so certification could not be established."""


class CertifiedEvidenceProtected(RuntimeError):
    """A write was refused because it targets a certified phase's evidence."""


def certified_phases(
    acts_root: Path = ACTS_ROOT, register: Path = REGISTER
) -> FrozenSet[int]:
    """Phases certified by an instrument that **resolves** against the Register.

    **The rejection is required, not merely the detection.** Under the Founder
    ruling on `D-P12-027-02`, `§49`'s `false certification` means *"the system
    must reject a certification claim that cannot resolve against an
    authoritative certification record"*, and the chain the ruling states is:

    ```text
    UNRESOLVABLE CERTIFICATION CLAIM  →  VIOLATION DETECTED  →  REJECT / BLOCK
    ```

    Before the ruling this function accepted any body carrying the sentence and
    `certification_anomalies` reported the unresolvable ones alongside it —
    detection without rejection, which is the middle of that chain and not its
    end. A certification that is reported and still believed has not been
    blocked.

    **Fails closed on an unreadable Register, and that direction matters.** If
    the Register cannot be read, nothing is rejected and
    `CertificationUndeterminable` is raised. The alternative — treating an
    unreadable Register as resolving nothing — would empty the protected set and
    leave P10 and P11 evidence writable, turning a missing file into an
    unprotection. *"Cannot check"* and *"checked and found unresolvable"* are
    different answers, and only the second may reject.

    **The ruling establishes no trust anchor and this implements none.** A forger
    who writes the Register row too still resolves; `§5` of the ruling says so in
    terms, and the residual is recorded as a supplementary control rather than
    closed.
    """
    if not acts_root.is_dir():
        raise CertificationUndeterminable(
            f"governance acts root is not readable: {acts_root}"
        )
    try:
        register_text = register.read_text(encoding="utf-8")
    except OSError as exc:
        raise CertificationUndeterminable(
            f"the certification register is not readable ({register}): "
            f"certification cannot be resolved, and an undeterminable boundary "
            f"is not an absent one"
        ) from exc

    phases = set()
    for path in sorted(acts_root.glob("*.md")):
        body = path.read_text(encoding="utf-8")
        claimed = {int(group)
                   for match in _CERTIFIES.finditer(body)
                   for group in match.groups() if group}
        if not claimed:
            continue
        if _register_identity(path.stem, register_text) is None:
            continue  # REJECT: the instrument resolves against no record
        phases.update(claimed)
    return frozenset(phases)


def certification_provenance(
    acts_root: Path = ACTS_ROOT
) -> Tuple[Tuple[int, str], ...]:
    """Which instrument each certification statement was actually read from.

    `certified_phases` answers *what* is certified and discards *where it read
    that*. Under `ACT-CC-P12-022` the discarding is the problem: an auditor
    handed `frozenset({10, 11, 42})` cannot see that `42` came from a file
    nobody issued, and neither can any other reader in this repository.

    This establishes no authority and changes no authorization. It reports
    attribution — `PR-3`, detect don't decide.
    """
    found = []
    for path in sorted(acts_root.glob("*.md")):
        body = path.read_text(encoding="utf-8")
        for match in _CERTIFIES.finditer(body):
            for group in match.groups():
                if group:
                    found.append((int(group), path.name))
    return tuple(sorted(set(found)))


def _register_identity(stem: str, register_text: str) -> Optional[str]:
    """The longest prefix of a filename the Register actually records.

    No identifier grammar is assumed, because assuming one is how a guard comes
    to believe a filename. Prefixes are tried longest-first and the first one
    the Register's own text contains is returned. A match must carry a digit and
    span at least two tokens, so that a bare `FD` — which the Register contains
    hundreds of times — can never stand in for an instrument identity.
    """
    tokens = stem.split("-")
    for length in range(len(tokens), 1, -1):
        candidate = "-".join(tokens[:length])
        if any(c.isdigit() for c in candidate) and candidate in register_text:
            return candidate
    return None


def certification_anomalies(
    acts_root: Path = ACTS_ROOT, register: Path = REGISTER
) -> Tuple[str, ...]:
    """Certification statements whose instrument the Register does not record.

    **This is detection, not authentication, and the difference is the whole
    point.** `ACT-CC-P12-021` rejected a Register cross-check as a *resolution*
    of the forgery finding, and that rejection stands: the Register is a
    document in the same unprotected store, so anyone who can plant a
    certifying instrument can plant a row describing it. Nothing here
    authenticates anything.

    What it does is make a **lone** forgery visible, which it previously was
    not. A planted document that no governance record mentions is now reported;
    before, it was silently believed. That raises the cost of the forgery from
    one consistent artifact to two, and it gives an auditor a name to look at.
    It does not close `§6.8` or `§6.9`, and this module does not claim it does
    — `certified_phases` returns exactly what it returned before.

    Fails closed: an unreadable Register makes every certification anomalous
    rather than none, because *"cannot check"* and *"checked and clean"* are
    different answers.
    """
    try:
        register_text = register.read_text(encoding="utf-8")
    except OSError:
        register_text = ""
    anomalies = []
    for phase, filename in certification_provenance(acts_root):
        identity = _register_identity(Path(filename).stem, register_text)
        if identity is None:
            anomalies.append(
                f"phase {phase} is certified by {filename}, which no entry in "
                f"{register.name} records"
            )
    return tuple(anomalies)


def protected_roots(
    repo_root: Path = REPO_ROOT, acts_root: Optional[Path] = None,
    register: Path = REGISTER,
) -> Tuple[Path, ...]:
    """Evidence roots belonging to a certified phase, that actually exist.

    `register` is parameterised for the same reason `acts_root` is: the
    resolution step the Founder ruling added is part of the fail-closed chain,
    and a chain that cannot be exercised against a constructed register cannot
    be shown to hold.
    """
    phases = certified_phases(
        acts_root or (repo_root / "docs/governance/acts"), register)
    roots = []
    for phase in sorted(phases):
        declared = PHASE_EVIDENCE_ROOTS.get(phase)
        candidate = (
            repo_root / declared if declared
            else repo_root / f"docs/architecture/p{phase}"
        )
        if candidate.is_dir():
            roots.append(candidate)
            continue
        # A certified phase whose evidence root cannot be resolved is an
        # undeterminable boundary, not an absent one. The first version of this
        # loop skipped it silently: P10 is certified, has no `p10/` directory,
        # and its certification package sat unprotected under
        # `platform-organization/` while this function reported success. That is
        # the same "guard that passes because it cannot see" shape this module
        # was written to prevent, committed inside the module itself.
        raise CertificationUndeterminable(
            f"phase {phase} is certified but its evidence root cannot be "
            f"resolved: neither PHASE_EVIDENCE_ROOTS nor docs/architecture/"
            f"p{phase} yields a directory"
        )
    return tuple(roots)


def protected_instruments(acts_root: Path = ACTS_ROOT) -> Tuple[Path, ...]:
    """The instruments that **confer** certification, which were not protected.

    **A gap in `F-12`'s own artifact, found under `ACT-CC-P12-025 §4 A2` and
    closed here.** The guard protected every certified phase's *evidence* and
    left the instruments conferring that certification writable:

    ```text
    docs/architecture/platform-organization/EVIDENCE-LEDGER.md   REFUSED
    docs/governance/acts/FD-P10-005-…CERTIFICATION….md           PERMITTED
    docs/governance/acts/FD-P11-002-P11-CERTIFICATION.md         PERMITTED
    ```

    That is the module's own founding sentence turned on itself — *"a
    certification that constrains documents but not behaviour is a record, not
    a boundary"* — because the record the boundary is computed **from** was
    outside the boundary. Overwrite `FD-P11-002` and `docs/architecture/p11`
    stops being protected at all; the evidence was guarded and its warrant was
    not.

    **This is not the forgery finding and does not touch it.** Overwriting an
    existing instrument and planting a new one are different acts: this refuses
    the first and has no bearing on the second, so `§6.8`'s `false
    certification` and `§6.9`'s `forge decision` are unchanged. It is fixed
    because it is a defect, not because it moves anything.

    **Derived, never listed.** The set is exactly the instruments
    `certification_provenance` read a certification statement from, so an
    instrument becomes protected by the act of certifying and a hand-maintained
    list cannot drift away from what the guard actually believes.

    The rest of the acts root stays writable: a new Act must be persistable, and
    protecting the whole directory would refuse the corpus's ordinary work.
    """
    return tuple(sorted({acts_root / name
                         for _, name in certification_provenance(acts_root)}))


def is_protected(
    path: Path, repo_root: Path = REPO_ROOT, acts_root: Optional[Path] = None,
    register: Path = REGISTER,
) -> bool:
    """Whether `path` is certified-phase evidence, or an instrument certifying one."""
    resolved = Path(path).resolve()
    for root in protected_roots(repo_root, acts_root, register):
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        return True
    for instrument in protected_instruments(
            acts_root or (repo_root / "docs/governance/acts")):
        if resolved == instrument.resolve():
            return True
    return False


def guard(
    path: Path, repo_root: Path = REPO_ROOT, acts_root: Optional[Path] = None,
    register: Path = REGISTER,
) -> Path:
    """Refuse a persisting write into certified-phase evidence.

    Returns the path unchanged when the write is permitted, so it reads as a
    checkpoint at the call site rather than as a separate step someone can
    forget to perform.
    """
    if is_protected(path, repo_root, acts_root, register):
        raise CertifiedEvidenceProtected(
            f"{path} lies in certified-phase evidence and may not be overwritten. "
            "The phase's evidence is historical: execute freely, but persist "
            "new evidence to a new location rather than rewriting the record "
            "certification froze."
        )
    return Path(path)


def main(argv=None) -> int:
    try:
        phases = sorted(certified_phases())
    except CertificationUndeterminable as exc:
        print(f"UNDETERMINABLE: {exc}")
        return 1
    print(f"certified phases (from instrument bodies): {phases}")
    for root in protected_roots():
        print(f"  protected: {root.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
