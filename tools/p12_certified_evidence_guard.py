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


def certified_phases(acts_root: Path = ACTS_ROOT) -> FrozenSet[int]:
    """Phase numbers certified by a resident instrument's own body."""
    if not acts_root.is_dir():
        raise CertificationUndeterminable(
            f"governance acts root is not readable: {acts_root}"
        )
    phases = set()
    for path in sorted(acts_root.glob("*.md")):
        body = path.read_text(encoding="utf-8")
        for match in _CERTIFIES.finditer(body):
            for group in match.groups():
                if group:
                    phases.add(int(group))
    return frozenset(phases)


def protected_roots(
    repo_root: Path = REPO_ROOT, acts_root: Optional[Path] = None
) -> Tuple[Path, ...]:
    """Evidence roots belonging to a certified phase, that actually exist."""
    phases = certified_phases(acts_root or (repo_root / "docs/governance/acts"))
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


def is_protected(
    path: Path, repo_root: Path = REPO_ROOT, acts_root: Optional[Path] = None
) -> bool:
    """Whether `path` lies inside a certified phase's evidence root."""
    resolved = Path(path).resolve()
    for root in protected_roots(repo_root, acts_root):
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        return True
    return False


def guard(
    path: Path, repo_root: Path = REPO_ROOT, acts_root: Optional[Path] = None
) -> Path:
    """Refuse a persisting write into certified-phase evidence.

    Returns the path unchanged when the write is permitted, so it reads as a
    checkpoint at the call site rather than as a separate step someone can
    forget to perform.
    """
    if is_protected(path, repo_root, acts_root):
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
