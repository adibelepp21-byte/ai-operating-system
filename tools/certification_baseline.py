"""The AIOS certification baseline, reported as the Founder accepted it (`FDR-G1` `FD-G3`).

`FDR-G1` `§40` sets the authoritative reporting model:

```text
P1–P3    NO CERTIFICATION RECORD IDENTIFIED
P4–P9    CERTIFIED VIA FOUNDER DECISIONS / REGISTER
P10–P13  CERTIFIED + MACHINE-PROTECTED
```

Its `§28` adds that the phrase *"P1–P13 Certified Baseline"* is not an
accepted canonical claim.

Before this module, the system's self-model reported certification only as the
guard reads it: P10–P13, and nothing about P1–P9. It never claimed that P1–P13
were certified. It did leave P4–P9's certification unreported, and a reader
could take that silence for "uncertified". `§34` authorizes accurate
non-certified reporting, and this module provides it.

**Each tier is checked against its evidence, not only restated:**

| Tier | Check |
|---|---|
| P10–P13 | the guard reads a Register-resolving certification, and integrity detection indexes a current version |
| P4–P9 | the Register holds the certifying entry named for the phase. The identifiers are declared below, because the Register cannot be parsed for them unambiguously |
| P1–P3 | no Register heading and no guard-read instrument certifies the phase |

If a check disagrees with the accepted tier, the phase is reported as a
`DISCREPANCY`. It is never silently reclassified. This module certifies
nothing, protects nothing and reconstructs nothing (`§23`, `§25`, `§27`).
P0 is outside `§40`'s model and is not reported.

Nothing here authorizes anything, and nothing here writes.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
FDRG1 = "docs/governance/acts/FDR-G1-POST-P13-GOVERNANCE-FOUNDATION.md"

NO_RECORD = "NO CERTIFICATION RECORD IDENTIFIED"
REGISTER_CERTIFIED = "CERTIFIED VIA FOUNDER DECISIONS / REGISTER"
MACHINE_PROTECTED = "CERTIFIED + MACHINE-PROTECTED"
DISCREPANCY = "DISCREPANCY"

#: `FDR-G1` `§40`: the accepted tier of each phase.
ACCEPTED = {**{n: NO_RECORD for n in (1, 2, 3)},
            **{n: REGISTER_CERTIFIED for n in range(4, 10)},
            **{n: MACHINE_PROTECTED for n in range(10, 14)}}

#: The Register entries certifying P4–P9. Declared, and verified on every call
#: against the Register's own headings.
REGISTER_CERTIFICATIONS = {4: "GDR-0002", 5: "FD-P5-001", 6: "FD-P6-002",
                           7: "FD-P7-003", 8: "FD-P8-002", 9: "FD-P9-002"}

#: `FDR-G1` `§28`.
FORBIDDEN_CLAIM = "P1–P13 Certified Baseline"


def _certifying_headings(register_text: str) -> Dict[int, List[str]]:
    """Register entry headings that name a phase and a certification."""
    found: Dict[int, List[str]] = {}
    for line in register_text.splitlines():
        if not line.startswith("### ") or "certif" not in line.lower():
            continue
        for match in re.finditer(r"\bPhase (\d+)\b", line):
            found.setdefault(int(match.group(1)), []).append(line[4:].strip())
    return found


def baseline(root: Path = REPO_ROOT) -> Dict[str, object]:
    """Each phase's accepted tier, and whether the evidence agrees with it."""
    from tools import certified_evidence_integrity as integrity
    from tools import p12_certified_evidence_guard as sentinel
    try:
        register_text = (root / REGISTER).read_text(encoding="utf-8")
    except OSError as error:
        return {"resolved": False, "detail": f"Decision Register unreadable: {error}"}
    try:
        acceptance = (root / FDRG1).read_text(encoding="utf-8")
    except OSError:
        acceptance = ""
    accepted = (sentinel._register_identity(Path(FDRG1).stem, register_text) is not None
                and "P1–P3\nNO CERTIFICATION RECORD IDENTIFIED" in acceptance)
    try:
        guarded = sentinel.certified_phases(root / "docs/governance/acts",
                                            root / REGISTER)
    except sentinel.CertificationUndeterminable as error:
        return {"resolved": False, "detail": str(error)}
    report = integrity.verify(root)
    indexed = {int(phase[1:]) for phase in report.versions}
    headings = _certifying_headings(register_text)

    phases: Dict[str, dict] = {}
    for number, tier in sorted(ACCEPTED.items()):
        evidence: List[str] = []
        agrees = True
        if tier == MACHINE_PROTECTED:
            agrees = number in guarded and number in indexed
            evidence.append(f"guard certifies: {number in guarded}; "
                            f"integrity indexes a current version: {number in indexed}")
        elif tier == REGISTER_CERTIFIED:
            identifier = REGISTER_CERTIFICATIONS[number]
            named = [h for h in headings.get(number, ())
                     if h.startswith(f"{identifier} ")]
            agrees = bool(named) and number not in guarded
            evidence.append(f"Register: {named[0]}" if named
                            else f"Register holds no certifying heading for {identifier}")
        else:
            agrees = number not in headings and number not in guarded
            evidence.append("no Register certification heading and no guard-read "
                            "certification" if agrees else
                            f"a certification record exists: {headings.get(number)}")
        phases[f"P{number}"] = {"tier": tier if agrees else DISCREPANCY,
                                "accepted_tier": tier, "evidence": evidence}

    discrepancies = sorted(p for p, v in phases.items() if v["tier"] == DISCREPANCY)
    return {
        "resolved": True,
        "accepted_by": "FDR-G1 FD-G3 (§22, §40)",
        "accepted": accepted,
        "tiers": {"P1–P3": NO_RECORD, "P4–P9": REGISTER_CERTIFIED,
                  "P10–P13": MACHINE_PROTECTED},
        "phases": phases,
        "discrepancies": discrepancies,
        "holds": accepted and not discrepancies,
        "not_a_canonical_claim": FORBIDDEN_CLAIM,
    }


def main() -> int:
    import json
    result = baseline()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("holds") else 1


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
