"""P12-W6 — cross-platform relationship evidence over the resident corpora (`§48`).

**`§48` was revised, and the revision is what this measures.** v1.0 gave one
list that merged phase surfaces with division names and, doing so, omitted four
Platform Divisions. `AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.1 §48`
(`C-03`) splits it into two populations and restores `PD-01`, `PD-02`, `PD-06`
and `PD-07`:

```text
Platform Divisions   PD-01 … PD-10          — this module
Phase surfaces       Intelligence · Knowledge · Memory · Tools ·
                     Workflow · Organization · Runtime
                                            — p12_cross_phase_verification
```

**Why this exists beside `p12_cross_pd_verification`.** That module verifies the
`CROSS-PD-INTERFACE-REGISTRY`'s *currency* — that its five rows still say what
they said. The registry was built from the `E-33`/`E-24` propagation, both
sourced in `PD-03`/`PD-04`, so `PD-01` and `PD-02` appear in **no registry edge
at all** — while their canonical corpora have been **resident since Volume 1 and
Volume 2 landed**. `PD-01 C8` is titled *Cross Platform Governance*, carries a
Platform Relationship Model naming all nine other divisions, and declares its
Shared Responsibility table *"authoritative source"*. None of that reached any
P12 measurement. That gap is what this closes.

**What it refuses to do.** It reports what the resident bodies say and stops.
`§48`'s rule is unchanged — *"A relationship is not considered verified merely
because both surfaces exist"* — and nothing here returns `VERIFIED` or
`DEFINED`. `RECIPROCATED` is a stronger claim than *both surfaces exist*, and a
weaker one than verified: it means each division's own corpus states the
relationship in a section whose own heading is about relationships. That is
evidence of a relationship, which is what `§6.11` asks for, and it is not an
interface definition, which `F-18` still lacks.

A division whose corpus is not resident is reported `SOURCE-ABSENT`, never *no
relationship*. `UNKNOWN ≠ FALSE` (`§43`), and six of the ten are unreadable for
reasons that are not P12's: `ESC-C7-01` (PD-03, PD-04 — non-resident) and `G-01`
(PD-05 … PD-10 — absent).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = REPO_ROOT / "docs/architecture"

#: `§48` v1.1's canonical taxonomy, all ten, in its order.
#:
#: `PD-10` carries a recorded naming `CONFLICT` — *Developer Experience* versus
#: *Developer Enablement*. v1.0 resolved it silently by using one name and v1.1
#: expressly declines to; both are carried here for the same reason.
DIVISIONS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("PD-01", ("Executive",)),
    ("PD-02", ("Architecture",)),
    ("PD-03", ("Governance & Compliance",)),
    ("PD-04", ("Knowledge & Intelligence",)),
    ("PD-05", ("Runtime & Execution",)),
    ("PD-06", ("AI Engineering",)),
    ("PD-07", ("Infrastructure & Platform",)),
    ("PD-08", ("Security",)),
    ("PD-09", ("Quality & Evaluation",)),
    ("PD-10", ("Developer Experience", "Developer Enablement")),
)

RECIPROCATED = "RECIPROCATED"
SELF_DECLARED = "SELF-DECLARED"
MENTIONED = "MENTIONED"
SOURCE_ABSENT = "SOURCE-ABSENT"

#: A section whose **own heading** is about how units relate. Matched against the
#: heading, never the body: a division's Performance section mentioning another
#: division is not thereby a relationship statement, and counting it as one is
#: exactly the *"merely because both surfaces exist"* inference `§48` forbids.
_RELATIONSHIP_HEADING = re.compile(
    r"interface|relationship|cross[ -]platform|coordination|collaboration"
    r"|dependency|integration|shared responsibility",
    re.I)

_PD = re.compile(r"\bPD-(0[1-9]|10)\b")


def _section_heading(stem: str, text: str) -> str:
    """The section's own title, not the Part banner above it.

    **A defect in the first version of this module, disclosed.** It took the
    first non-empty line, which for most of `PD-02`'s corpus is the Part banner
    — *"Part C — Governance Architecture"* — while the section title sits on the
    next line. `C8 — Cross-Platform Architecture Governance` was therefore read
    as a governance section that merely mentions other divisions, and
    `PD-01 ↔ PD-02` came back `SELF-DECLARED` when both corpora state it. An
    instrument that cannot find the heading reporting a weaker state than the
    evidence supports is the `UNKNOWN ≠ FALSE` failure, committed inside the
    module built to measure evidence.

    The section's own line begins with its identifier, so that is what is
    matched, over the first few non-empty lines. The Part banner is the
    fallback, because a file with no such line still has a heading.
    """
    own = re.compile(rf"^#*\s*{re.escape(stem)}\s*[—–-]", re.I)
    lines = [line.strip(" #") for line in text.splitlines() if line.strip()]
    for line in lines[:6]:
        if own.match(line):
            return line
    return lines[0] if lines else ""


class CorpusUnavailable(RuntimeError):
    """No resident division corpus could be read (`PR-4`, fail closed)."""


@dataclass(frozen=True)
class Statement:
    """One division's corpus naming another, with where it said it."""
    source: str
    target: str
    section: str
    heading: str
    relationship_bearing: bool


def resident_corpora(root: Path = ARCHITECTURE) -> Dict[str, Path]:
    """Which divisions have a resident canonical corpus — discovered, not declared.

    Scanned rather than listed, so a Volume becoming resident is picked up by
    measurement instead of by someone remembering to edit a constant.
    """
    found: Dict[str, Path] = {}
    for volume in sorted(root.glob("volume-*")):
        for division in sorted(p for p in volume.iterdir() if p.is_dir()):
            match = re.match(r"pd-(\d{2})-", division.name)
            if match and any(f.suffix == ".md" for f in division.iterdir()):
                found[f"PD-{match.group(1)}"] = division
    return found


def statements(root: Path = ARCHITECTURE) -> Tuple[Statement, ...]:
    corpora = resident_corpora(root)
    if not corpora:
        raise CorpusUnavailable(f"no resident division corpus under {root}")
    collected = []
    for source, directory in sorted(corpora.items()):
        for path in sorted(directory.glob("*.md")):
            if path.stem.endswith("MANIFEST"):
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            heading = _section_heading(path.stem, text)
            bearing = bool(_RELATIONSHIP_HEADING.search(heading))
            for target in sorted({f"PD-{m.group(1)}" for m in _PD.finditer(text)}):
                if target != source:
                    collected.append(Statement(source, target, path.stem,
                                               heading[:72], bearing))
    return tuple(collected)


def pairs(root: Path = ARCHITECTURE) -> Dict[Tuple[str, str], str]:
    """Every ordered pair's evidence state over the ten-division population."""
    corpora = resident_corpora(root)
    said: Dict[Tuple[str, str], bool] = {}
    for statement in statements(root):
        key = (statement.source, statement.target)
        said[key] = said.get(key, False) or statement.relationship_bearing

    result: Dict[Tuple[str, str], str] = {}
    for source, _ in DIVISIONS:
        for target, _ in DIVISIONS:
            if source == target:
                continue
            if source not in corpora:
                result[(source, target)] = SOURCE_ABSENT
            elif said.get((source, target)):
                back = target in corpora and said.get((target, source))
                result[(source, target)] = RECIPROCATED if back else SELF_DECLARED
            elif (source, target) in said:
                result[(source, target)] = MENTIONED
            else:
                result[(source, target)] = SOURCE_ABSENT if target not in corpora \
                    else MENTIONED
    return result


def summary(root: Path = ARCHITECTURE) -> dict:
    corpora = resident_corpora(root)
    state = pairs(root)
    counts = {name: sum(1 for v in state.values() if v == name)
              for name in (RECIPROCATED, SELF_DECLARED, MENTIONED, SOURCE_ABSENT)}
    return {
        "divisions": len(DIVISIONS),
        "resident_corpora": tuple(sorted(corpora)),
        "source_absent_divisions": tuple(
            d for d, _ in DIVISIONS if d not in corpora),
        "ordered_pairs": len(state),
        **counts,
        "evidenced_pairs": counts[RECIPROCATED] + counts[SELF_DECLARED],
        # Stated, not computed, and stated as zero: no resident body defines an
        # interface. `F-18` is unchanged by anything in this module.
        "interfaces_defined": 0,
        "interfaces_verified": 0,
    }


def main(argv=None) -> int:
    state = pairs()
    for (source, target), value in sorted(state.items()):
        if value in (RECIPROCATED, SELF_DECLARED):
            print(f"{source} → {target:<6} {value}")
    print()
    print("summary:", summary())
    print()
    print("DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL.")
    print("A relationship is not verified merely because both surfaces exist,")
    print("and no resident body defines a cross-PD interface (F-18 unchanged).")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
