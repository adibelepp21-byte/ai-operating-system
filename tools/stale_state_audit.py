"""Stale-state detection — the one `§26` verifier the programme lacked.

`ACT-CC-AIOS-FULL-SYSTEM-RESOLUTION §26` lists ten properties a verifier must
itself be verified for. Nine had coverage. **Stale-state detection had none** —
and it is the defect class that reached a live verdict twice:

* `R3-P10-ENTRY-BASELINE` asserted *"Phase 9 stands at 0%"*, taken from the
  26 July Progress Tracker snapshot **after** this corpus had already labelled
  that snapshot `STALE BY DECLARATION` (`E-46`).
* `EVIDENCE-LEDGER` entry `E-60` carried the same figure in its heading as a
  standing fact.

**The corpus supplies its own superseded set.** The External Corpus
Synchronization Ledger, recorded under Founder Decision `G1'`, states in
machine-readable rows which figures are *"superseded by fact"* and against which
certification. This checker reads those rows and looks for the superseded
figures being asserted **live** anywhere else.

Evidence controls the detector: **nothing is hard-coded**. Delete a row from the
Register and the corresponding check disappears with it, which is correct — the
Register is the authority for what is superseded, not this file.

A hit is suppressed when the surrounding text marks it historical. That is not
leniency: `ACT §16` requires a historical figure to be **preserved** as history
while being **prevented** from acting as current state, so a figure inside a
correction block is the system working, not failing.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The Register is the *source* of the superseded set, so it is never a subject.
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"

#: Same containment policy as the citation auditor: untracked files under these
#: prefixes are never read. Protection is a path policy, not a staging state.
PROTECTED_UNTRACKED_PREFIXES = ("docs/program/",)

S_ROW = re.compile(r"^\|\s*(S-\d+)\s*\|")
QUOTED = re.compile(r'\*"([^"]+)"\*')
PHASE_IN_QUOTE = re.compile(r"Phase\s+(\d+)")

#: Words that mark a nearby figure as history rather than a live claim.
HISTORICAL_MARKERS = (
    "superseded", "corrected", "correction", "historical", "snapshot",
    "stale", "was:", "no longer", "withdrawn", "26 july", "26 juli",
    "bukan status realtime", "per 26",
)

#: How many lines either side may carry the marker.
WINDOW = 12

#: ``0%`` — but never the ``0%`` inside ``100%`` or ``50%``. The first version of
#: this checker had no left boundary and matched
#: *"conflict detection is currently 100%"* as a zero figure.
ZERO_FIGURE = re.compile(r"(?<![\d.])0\s*%")

#: A phase reference and a zero figure on the same line prove nothing when the
#: line is 900 characters long and states two unrelated facts. That is exactly
#: how the first false positive arose, so proximity is required.
PROXIMITY = 80


def _lines(path: Path) -> list[str]:
    """Split on newlines only — never ``str.splitlines()``.

    The same rule the citation auditor and ``derived_views`` use, so a line
    number reported here means what it means everywhere else.
    """
    return path.read_text(encoding="utf-8", errors="replace").split("\n")


class ScopeUndeterminable(RuntimeError):
    """Raised when tracked status cannot be established, so scope is unknown."""


def _tracked() -> set:
    """Paths git tracks. **Raises rather than degrading.**

    The first version returned an empty set on failure. That is *safe* in the
    containment direction — everything under a protected prefix becomes
    unreadable — but it is **not safe in the reporting direction**: the scan
    silently covered 369 documents instead of 439 and still printed
    ``0 stale assertions``. **A false clean is worse than a refusal**, and
    `ACT §19` PRIORITY 2 names *"false clean result"* as a system-integrity
    defect in its own right.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"], cwd=str(REPO_ROOT),
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ScopeUndeterminable(
            "refusing to scan: could not determine tracked files, so protected "
            "untracked paths cannot be identified"
        ) from exc
    tracked = {p for p in out.split("\0") if p}
    if not tracked:
        raise ScopeUndeterminable(
            "refusing to scan: git reported zero tracked files, which cannot be "
            "true of this repository and means scope is undeterminable"
        )
    return tracked


def _is_readable(rel: str, tracked: set) -> bool:
    if rel in tracked:
        return True
    return not rel.startswith(PROTECTED_UNTRACKED_PREFIXES)


def superseded_claims(root: Path = REPO_ROOT) -> list[dict]:
    """The superseded set, read from the Register rather than declared here."""
    register = root / REGISTER
    if not register.is_file():
        return []
    claims = []
    for line in _lines(register):
        row = S_ROW.match(line)
        if row is None or "superseded by fact" not in line:
            continue
        quote = QUOTED.search(line)
        if quote is None:
            continue  # e.g. S-6 carries no quoted figure
        phase = PHASE_IN_QUOTE.search(quote.group(1))
        if phase is None:
            continue  # only phase-figure claims are machine-checkable today
        claims.append({
            "id": row.group(1),
            "quote": quote.group(1),
            "phase": phase.group(1),
        })
    return claims


def _marked_historical(lines: list[str], index: int) -> bool:
    lo = max(0, index - WINDOW)
    hi = min(len(lines), index + WINDOW + 1)
    window = " ".join(lines[lo:hi]).lower()
    return any(marker in window for marker in HISTORICAL_MARKERS)


def audit(root: Path = REPO_ROOT) -> dict:
    claims = superseded_claims(root)
    tracked = _tracked()
    findings: list[dict] = []
    scanned = 0

    for path in sorted((root / "docs").rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if rel == REGISTER or not _is_readable(rel, tracked):
            continue
        scanned += 1
        lines = _lines(path)
        for index, line in enumerate(lines):
            zeros = [m.start() for m in ZERO_FIGURE.finditer(line)]
            if not zeros:
                continue
            for claim in claims:
                # A live assertion pairs the phase with the superseded figure
                # *close together*. Two unrelated facts sharing a long line are
                # not a claim — see PROXIMITY.
                phases = [
                    m.start() for m in
                    re.finditer(rf"Phase[\s-]*{claim['phase']}\b", line)
                ]
                if not phases:
                    continue
                if min(abs(p - z) for p in phases for z in zeros) > PROXIMITY:
                    continue
                if _marked_historical(lines, index):
                    findings.append({
                        "severity": "INFO", "source": f"{rel}:{index + 1}",
                        "claim": claim["id"],
                        "message": f"historical use of a superseded figure — {claim['id']}",
                    })
                else:
                    findings.append({
                        "severity": "ERROR", "source": f"{rel}:{index + 1}",
                        "claim": claim["id"],
                        "message": (
                            f"STALE CURRENT-STATE ASSERTION — {claim['id']} records "
                            f'"{claim["quote"]}" as superseded by fact, and nothing '
                            "nearby marks this use as historical"
                        ),
                    })
                break

    return {
        "claims_extracted": len(claims),
        "documents_scanned": scanned,
        "errors": sum(1 for f in findings if f["severity"] == "ERROR"),
        "historical_uses": sum(1 for f in findings if f["severity"] == "INFO"),
        "findings": findings,
    }


def main(argv: list[str]) -> int:
    try:
        result = audit()
    except ScopeUndeterminable as exc:
        print(exc)
        return 2
    print(f"superseded claims  : {result['claims_extracted']}  (read from the Register)")
    print(f"documents scanned  : {result['documents_scanned']}")
    print(f"stale assertions   : {result['errors']}")
    print(f"historical uses    : {result['historical_uses']}  (correct — preserved as history)")
    for finding in result["findings"]:
        if finding["severity"] == "ERROR" or "-v" in argv:
            print(f"  [{finding['severity']}] {finding['source']}  {finding['message']}")
    if result["claims_extracted"] == 0:
        print("\nNOTE: no superseded claims were extracted. The checker is inert,")
        print("      which means the Register's S-rows changed shape — not that")
        print("      the corpus is clean.")
        return 2
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
