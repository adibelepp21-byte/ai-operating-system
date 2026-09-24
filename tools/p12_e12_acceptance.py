"""`E12-06` measured against the **ratified** acceptance boundary.

`FD-P12-001` (`ACT-CC-P12-013`) ratified `E12` and selected `§C = R1`:

```text
R1 — CONSUMPTION BY REAL SYSTEM WORK
```

and `§5` closes the hole every weaker reading would have left open:

> *"The existence of a component, provisioned capability, **demonstrator**, test
> fixture, or merely callable surface is not by itself sufficient evidence of
> consumption by real system work."*

**This module applies that boundary and nothing else.** `§6` names `R2`
(provisioning by a real execution) and `R3` (dormancy legitimate) **NOT
SELECTED**, and forbids combining them with `R1` to make a broader rule — so a
phase provisioned by every runtime but consumed by no execution does **not**
pass here, and neither does one crossed only by a proof written to show the
surface works.

**The decision does not predetermine the result.** `§12`: *"The Founder
Decision does not predetermine which result the evidence will produce."* This
module was written to report whatever the corpus says, and `§20`'s falsification
suite exists to catch it reporting a pass it has not earned.

**Why a phase is the unit.** `§C` asked: *"Must a canonical phase be exercised
for `E12-06` to be satisfied, and what counts as exercise?"* `R1` answers the
second half. The first half is answered by the question's own framing, which
`§5`'s acceptance chain repeats: `REAL SYSTEM WORK → REAL CONSUMPTION → …
→ E12-06 DETERMINATION`.

**This module creates no authority.** It reads the ratified boundary out of the
persisted instrument, and if that instrument cannot be found it raises rather
than falling back on a default — an acceptance boundary nobody ratified is not
one this office may supply.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The persisted Founder instrument. Located in the curated governance-acts
#: root and recognised by its body, the discipline `p12_phase_authorization`
#: already applies to the P12 authorization.
DECISION_ROOT = Path("docs/governance/acts")

SATISFIED = "SATISFIED"
NOT_SATISFIED = "NOT SATISFIED"
UNKNOWN = "UNKNOWN"

#: `R1`'s two failure modes, named separately because they are different facts
#: about the system and collapsing them would hide which one applies.
NOT_EXERCISED_AT_ALL = "NOT CONSUMED — no execution ever recorded"
DEMONSTRATOR_ONLY = "NOT CONSUMED BY REAL WORK — crossed only by a demonstrator"
CONSUMED = "CONSUMED BY REAL SYSTEM WORK"


class AcceptanceBoundaryUnresolved(Exception):
    """No ratified acceptance boundary could be read.

    Raised rather than defaulting to a reading. `§9` forbids selecting `R2` or
    `R3` or creating a fourth interpretation, and silently assuming one would be
    all three at once.
    """


@dataclass(frozen=True)
class PhaseAcceptance:
    phase: str
    name: str
    verdict: str
    detail: str
    evidence: str

    @property
    def accepted(self) -> bool:
        return self.verdict == CONSUMED


@dataclass(frozen=True)
class Boundary:
    reading: str
    instrument: str
    not_selected: Tuple[str, ...]
    demonstrator_insufficient: bool


def ratified_boundary(root: Path = REPO_ROOT) -> Boundary:
    """Read `§C`'s ratified reading from the persisted Founder instrument.

    Recognised by body content — a `§C ACCEPTANCE INTERPRETATION` section naming
    a `FOUNDER SELECTION`, and an authentication section stating `ISSUED` — not
    by filename. `IDENTIFIER ≠ ACTUAL DECISION BODY`.
    """
    directory = root / DECISION_ROOT
    if not directory.is_dir():
        raise AcceptanceBoundaryUnresolved(
            f"the governance acts root does not resolve: {DECISION_ROOT}")
    found = []
    for path in sorted(directory.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if "ACCEPTANCE INTERPRETATION" not in text:
            continue
        if not re.search(r"^Decision Status:\s*FINAL\s*/\s*ISSUED\s*$",
                         text, re.M):
            continue
        selection = re.search(
            r"^FOUNDER SELECTION\s*$\s*^(R\d)\s*[—-]\s*(.+?)\s*$",
            text, re.M)
        if selection is None:
            continue
        not_selected = tuple(sorted(set(re.findall(
            r"^(R\d)\s*[—-]\s*.+?\s*=\s*NOT SELECTED\s*$", text, re.M))))
        found.append(Boundary(
            reading=f"{selection.group(1)} — {selection.group(2)}",
            instrument=path.relative_to(root).as_posix(),
            not_selected=not_selected,
            demonstrator_insufficient="demonstrator" in text))
    if len(found) != 1:
        raise AcceptanceBoundaryUnresolved(
            f"{len(found)} issued instruments carry a ratified §C acceptance "
            "interpretation; exactly one must. Which boundary governs is a "
            "Founder question, not a parsing one")
    return found[0]


def phases(root: Path = REPO_ROOT) -> Tuple[PhaseAcceptance, ...]:
    """Every canonical phase, judged against the ratified boundary.

    The exercise measurement and the demonstrator attribution both come from
    `p12_cross_phase_verification`, which has reported them since long before
    ratification. **Nothing was re-measured to suit the decision** — the same
    figures that read `6 exercised` under no boundary read `4 consumed` under
    `R1`, because `R1` asks a stricter question of the same evidence.
    """
    from tools import p12_cross_phase_verification as cross

    boundary = ratified_boundary(root)
    if not boundary.reading.startswith("R1"):
        raise AcceptanceBoundaryUnresolved(
            f"the ratified reading is {boundary.reading!r}; this module "
            "implements R1 only and must not be applied to another reading")

    results = cross.verify(root)
    demonstrator_only = set(cross.summary(root)["exercised_only_by_a_demonstrator"])
    accepted = []
    for result in results:
        if result.status != cross.EXERCISED:
            verdict, detail = NOT_EXERCISED_AT_ALL, result.evidence
        elif result.phase in demonstrator_only:
            verdict = DEMONSTRATOR_ONLY
            detail = ("§5: a demonstrator is not by itself sufficient evidence "
                      "of consumption by real system work")
        else:
            verdict, detail = CONSUMED, "crossed by an execution of real work"
        accepted.append(PhaseAcceptance(result.phase, result.name, verdict,
                                        detail, result.evidence))
    return tuple(accepted)


def determination(root: Path = REPO_ROOT) -> dict:
    """`E12-06` under the ratified boundary. Reports, never promotes."""
    boundary = ratified_boundary(root)
    results = phases(root)
    consumed = [r.phase for r in results if r.accepted]
    not_consumed = [r.phase for r in results if not r.accepted]
    return {
        "criterion": "E12-06 — System-wide Verification",
        "ratified_reading": boundary.reading,
        "instrument": boundary.instrument,
        "not_selected": boundary.not_selected,
        "phases": len(results),
        "consumed_by_real_work": consumed,
        "not_consumed": not_consumed,
        "by_reason": {
            "no execution ever recorded":
                [r.phase for r in results if r.verdict == NOT_EXERCISED_AT_ALL],
            "demonstrator only":
                [r.phase for r in results if r.verdict == DEMONSTRATOR_ONLY],
        },
        "verdict": SATISFIED if not not_consumed else NOT_SATISFIED,
    }


def summary(root: Path = REPO_ROOT) -> dict:
    return determination(root)


def main(argv=None) -> int:
    import json
    print(json.dumps(determination(), indent=2, default=str))
    for result in phases():
        print(f"  {result.phase:<4} {result.name:<14} {result.verdict}")
    return 0


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
