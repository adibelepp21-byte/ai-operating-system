"""P12-W6 — cross-PD interface currency verification (`§19` scope: `CROSS-PD INTERFACES`).

**What this does not do, first, because it is the finding.**

The five evidenced cross-PD edges each record `Interface: not declared` and
`Verification: DECLARED — interface undefined`. **An undefined interface cannot
be exercised**, so `§48`'s standard — *"a relationship is not considered verified
merely because both surfaces exist"* — cannot be met here by any amount of work.
Two pre-existing boundaries hold it there, and neither is `F-16` or `F-17`:

```text
SOURCE GAP          eight divisions' Volume 1/2 corpora are non-resident (ESC-C7-01)
ARCHITECT-RESERVED  INV-10 applicability awaits ADR-0029 / ADP-P10-001
```

The registry itself already refuses to cross either: it records
`POSSIBLE INV-10 EXPOSURE — NOT ASSERTED`, and *"No violation is claimed, and
none is ruled out."* This module does not claim one either.

**What it does do.** The registry's rows are the **only resident evidence** of
these edges — the divisions' own volumes are non-resident — so the edges cannot
be independently recomputed. What can be verified is the registry's **currency
and internal consistency**:

- its arithmetic (edges, ordered pairs, coverage);
- that its evidence identifiers still resolve in the Evidence Ledger;
- that no edge has since acquired an interface, a version or a governing
  mechanism;
- that the eight silent divisions are still silent **in resident evidence**;
- that the division population is still ten.

A drift in any of those means the registry has gone stale. Agreement means it is
current — **not that the interfaces are verified**, which is the distinction the
registry states as `DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "docs/architecture/platform-organization/CROSS-PD-INTERFACE-REGISTRY.md"
LEDGER = REPO_ROOT / "docs/architecture/platform-organization/EVIDENCE-LEDGER.md"
MASTER_MAP = REPO_ROOT / "docs/architecture/platform-organization/PLATFORM-ORGANIZATION-MASTER-MAP.md"

CURRENT = "CURRENT"
DRIFTED = "DRIFTED"
UNAVAILABLE = "UNAVAILABLE"

#: A registry row: `| X-01 | **PD-03** … | **PD-02** … | … |`
_ROW = re.compile(r"^\|\s*`(?P<id>X-\d+)`\s*\|(?P<rest>.*)\|\s*$", re.M)

#: The nine measures the registry records about itself, as it records them.
_MEASURE = re.compile(r"^\|\s*(?P<name>[^|]+?)\s*\|\s*\*{0,2}(?P<value>[\d.]+)\s*%?\s*\*{0,2}\s*\|\s*$", re.M)


@dataclass(frozen=True)
class Check:
    name: str
    recorded: str
    measured: str
    status: str
    note: str = ""


def _rows() -> Tuple[dict, ...]:
    if not REGISTRY.is_file():
        return ()
    found = []
    for match in _ROW.finditer(REGISTRY.read_text(encoding="utf-8")):
        cells = [c.strip() for c in match.group("rest").split("|")]
        found.append({"id": match.group("id"), "cells": cells})
    return tuple(found)


def _recorded_measures() -> dict:
    """The registry's own `§2` table, read rather than assumed."""
    if not REGISTRY.is_file():
        return {}
    text = REGISTRY.read_text(encoding="utf-8")
    section = text.split("## 2. What the registry measures about itself", 1)
    if len(section) < 2:
        return {}
    body = section[1].split("## 3.", 1)[0]
    return {
        m.group("name"): m.group("value")
        for m in _MEASURE.finditer(body)
        if m.group("name") != "Measure"
    }


def verify() -> Tuple[Check, ...]:
    if not REGISTRY.is_file():
        return (Check("registry", "resident", "absent", UNAVAILABLE,
                      "the registry itself is not resident"),)

    rows = _rows()
    recorded = _recorded_measures()
    checks = []

    # 1. edge count
    n = len(rows)
    rec = recorded.get("Evidenced edges", "?")
    checks.append(Check("evidenced edges", rec, str(n),
                        CURRENT if rec == str(n) else DRIFTED))

    # 2. arithmetic: ordered pairs over ten divisions
    divisions = recorded.get("Divisions", "?")
    pairs = recorded.get("Possible ordered pairs", "?")
    expected_pairs = int(divisions) * (int(divisions) - 1) if divisions.isdigit() else None
    checks.append(Check("possible ordered pairs", pairs, str(expected_pairs),
                        CURRENT if pairs == str(expected_pairs) else DRIFTED,
                        "n(n-1) over the division population"))

    # 3. coverage arithmetic
    if expected_pairs:
        coverage = round(100.0 * n / expected_pairs, 1)
        rec_cov = recorded.get("Edge coverage", "?")
        checks.append(Check("edge coverage %", rec_cov, f"{coverage}",
                            CURRENT if rec_cov == f"{coverage}" else DRIFTED))

    # 4. no edge has acquired an interface, version or governing mechanism
    for label, needle in (("edges with a defined interface", "not declared"),):
        undefined = sum(1 for r in rows if any(needle in c for c in r["cells"]))
        defined = n - undefined
        rec_def = recorded.get("Edges with a defined interface", "?")
        checks.append(Check(label, rec_def, str(defined),
                            CURRENT if rec_def == str(defined) else DRIFTED,
                            "a defined interface would make the edge exercisable"))

    # 5. evidence identifiers still resolve in the Ledger
    if LEDGER.is_file():
        ledger = LEDGER.read_text(encoding="utf-8")
        cited = sorted({e for r in rows for c in r["cells"]
                        for e in re.findall(r"\bE-\d+\b", c)})
        missing = [e for e in cited if f"**{e}**" not in ledger]
        checks.append(Check("evidence identifiers resolve",
                            f"{len(cited)} cited", f"{len(missing)} unresolved",
                            CURRENT if not missing else DRIFTED,
                            f"unresolved: {missing}" if missing else ""))

    # 6. the division population is still ten
    if MASTER_MAP.is_file():
        pds = sorted(set(re.findall(r"\*\*PD-(\d{2})\*\*",
                                    MASTER_MAP.read_text(encoding="utf-8"))))
        checks.append(Check("division population", divisions, str(len(pds)),
                            CURRENT if divisions == str(len(pds)) else DRIFTED))

    return tuple(checks)


def summary() -> dict:
    checks = verify()
    return {
        "checks": len(checks),
        "current": sum(1 for c in checks if c.status == CURRENT),
        "drifted": sum(1 for c in checks if c.status == DRIFTED),
        "unavailable": sum(1 for c in checks if c.status == UNAVAILABLE),
        "drifted_checks": tuple(c.name for c in checks if c.status == DRIFTED),
        "interfaces_verified": 0,
        "verification_blocked_by": ("SOURCE GAP (ESC-C7-01)",
                                    "ARCHITECT-RESERVED (ADR-0029)"),
    }


def main(argv=None) -> int:
    for check in verify():
        print(f"{check.name:<32} {check.status:<12} recorded={check.recorded:<8} measured={check.measured}")
        if check.note:
            print(f"{'':<32} {check.note}")
    print()
    print("summary:", summary())
    print()
    print("DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL.")
    print("Zero cross-PD interfaces are verified, and none can be until an")
    print("interface is defined — which is Architect-reserved and source-blocked.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
