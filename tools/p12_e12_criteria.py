"""`E12-01`…`E12-05` acceptance boundaries, read from a Founder instrument.

`FD-P12-003 §11` fixes the only admissible direction:

```text
FOUNDER SELECTS  →  ACCEPTANCE BOUNDARY  →  CLAUDE MEASURES
```

and forbids the reverse. So this module reads; it never chooses. It carries no
interpretation of its own, no default, and no fallback — `§24.14`: *"If any
selection or acceptance boundary in this record is syntactically incomplete,
contradictory, or cannot be reconciled to the actual canonical E12 package,
STOP at that decision-consumption boundary and report the exact conflict rather
than inventing a value."*

**A template placeholder is not a selection.** `FD-P12-003 §4`–`§8` are issued
with their `Founder selects:` and `Acceptance Boundary:` fields carrying
`[INSERT …]` brackets. That is a form, filled in nowhere, and this module says
so rather than resolving it — including in the case that makes resolution most
tempting: `E12-RATIFICATION-DECISION-PACKAGE.md §B` proposes **exactly one**
interpretation per criterion, so "the obvious one" is always available.
Selecting it would still be a selection, and `§11` names that prohibition four
separate ways. `RECOMMENDATION ≠ DECISION`.

**A selection is checked against the canonical package.** `§24.4` requires each
selected interpretation to correspond to an existing proposed interpretation,
and `§24.5` requires a mismatch to be **rejected, not substituted**. The
comparison is against `§B`'s resident text, read at call time.

**Fail closed.** `boundaries()` raises rather than returning a partial map: a
caller that cannot tell *"the boundary is X"* from *"no boundary was supplied"*
will read the second for the first, which is the substitution the whole chain
exists to prevent. `NECESSITY ≠ AUTHORITY`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The curated root a Founder instrument may be recognised in, and the resident
#: package that holds the proposed interpretations a selection must match.
DECISION_ROOT = Path("docs/governance/acts")
E12_PACKAGE = Path("docs/architecture/p12/E12-RATIFICATION-DECISION-PACKAGE.md")

#: The criteria this decision surface covers. `E12-06` is **not** here: it was
#: ratified separately by `FD-P12-001 §5` and is read by `p12_e12_acceptance`.
CRITERIA: Tuple[str, ...] = ("E12-01", "E12-02", "E12-03", "E12-04", "E12-05")

RESOLVED = "RESOLVED"
UNRESOLVED = "UNRESOLVED"
REJECTED = "REJECTED"

#: Shapes that are a blank waiting to be filled, not a value. Recognised
#: structurally so a new template marker is caught by the same rule.
_PLACEHOLDER = re.compile(
    r"^\s*(?:\[[^\]]*\]|_{3,}|\.{3,}|TBD|N/?A|-{3,})\s*$", re.I)
_BRACKETED = re.compile(r"\[[^\]]*\]")

#: `4. FOUNDER DECISION — E12-01` … the number is not hard-coded, so an
#: instrument that renumbers its sections is still readable.
_CRITERION_SECTION = re.compile(
    r"^\d+\.\s+FOUNDER DECISION\s*[—–-]\s*(E12-0\d)\s*$", re.M)
_ANY_SECTION = re.compile(r"^\d+\.\s+\S.*$", re.M)

#: `### `E12-01` — System Integration` in the canonical package, and the
#: `| **Proposed** interpretation | … |` row beneath it.
_PACKAGE_HEADING = re.compile(r"^###\s+`(E12-0\d)`\s*[—–-]\s*(.+?)\s*$", re.M)
_PROPOSED_ROW = re.compile(
    r"^\|\s*\*\*Proposed\*\*\s+interpretation\s*\|\s*(.+?)\s*\|\s*$", re.M)
_CANONICAL_ROW = re.compile(
    r"^\|\s*Canonical definition\s*\|\s*(.+?)\s*\|\s*$", re.M)


class AcceptanceBoundaryUnavailable(Exception):
    """No Founder-supplied acceptance boundary could be read.

    Raised rather than defaulting to the proposed interpretation. `§11`
    forbids selecting, ranking, recommending, merging or substituting one, and
    quietly adopting the only candidate would be all five at once.
    """


@dataclass(frozen=True)
class CriterionDecision:
    """One criterion's decision, exactly as the instrument states it."""

    criterion: str
    status: str
    selection: str
    boundary: str
    detail: str
    instrument: Optional[str] = None

    @property
    def usable(self) -> bool:
        return self.status == RESOLVED


def _sections(text: str) -> Dict[str, str]:
    """Each `FOUNDER DECISION — E12-0n` section body, by criterion."""
    found: Dict[str, str] = {}
    matches = list(_CRITERION_SECTION.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        following = _ANY_SECTION.search(text, start)
        end = following.start() if following else len(text)
        found[match.group(1)] = text[start:end]
    return found


def _field(body: str, label: str) -> str:
    """The value under a label, joined across its continuation lines.

    Both layouts occur: `Acceptance Boundary:` with the value on the following
    lines, and `Founder selects:` with the criterion and an arrow beneath. The
    reader accepts what a Founder actually typed and normalises whitespace
    only — never content.
    """
    lines = body.split("\n")
    collected = []
    capturing = False
    for line in lines:
        stripped = line.strip()
        if not capturing:
            if stripped.lower().startswith(label.lower()):
                capturing = True
                remainder = stripped[len(label):].lstrip(":").strip()
                if remainder:
                    collected.append(remainder)
            continue
        if not stripped:
            if collected:
                break
            continue
        if re.match(r"^(Founder Decision|Acceptance Boundary|Claude Code|"
                    r"Canonical Requirement|Founder Selection)\b", stripped,
                    re.I):
            break
        collected.append(stripped)
    return " ".join(collected).strip()


def _is_placeholder(value: str) -> bool:
    if not value:
        return True
    if _PLACEHOLDER.match(value):
        return True
    # `→ [INSERT …]` and `E12-01 → [INSERT …]` are still blanks: strip every
    # bracketed span and see whether anything of substance is left.
    residue = _BRACKETED.sub("", value)
    residue = re.sub(r"[^A-Za-z0-9]+", " ", residue).strip()
    # A residue that is only the criterion identifier restates the question.
    return residue == "" or re.fullmatch(r"E12\s*0\d", residue, re.I) is not None


def proposed_interpretations(root: Path = REPO_ROOT) -> Dict[str, dict]:
    """`§B` of the canonical package — the text a selection must match.

    These are **proposals**. The package says so in terms: *"each measurable
    interpretation is PROPOSED by this office and has no standing until
    ratified."* This module returns them so a selection can be checked against
    them, never so one can be adopted.
    """
    path = root / E12_PACKAGE
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    found: Dict[str, dict] = {}
    headings = list(_PACKAGE_HEADING.finditer(text))
    for index, heading in enumerate(headings):
        start = heading.end()
        end = (headings[index + 1].start() if index + 1 < len(headings)
               else len(text))
        block = text[start:end]
        proposed = _PROPOSED_ROW.search(block)
        canonical = _CANONICAL_ROW.search(block)
        found[heading.group(1)] = {
            "name": heading.group(2),
            "canonical_definition": canonical.group(1) if canonical else "",
            "proposed": proposed.group(1) if proposed else "",
        }
    return found


def _instruments(root: Path) -> Tuple[Path, ...]:
    """Instruments in the curated root that address this decision surface."""
    directory = root / DECISION_ROOT
    if not directory.is_dir():
        return ()
    found = []
    for path in sorted(directory.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if len(_sections(text)) >= 1:
            found.append(path)
    return tuple(found)


def decisions(root: Path = REPO_ROOT) -> Tuple[CriterionDecision, ...]:
    """What the corpus states for each criterion. Never raises; reports."""
    instruments = _instruments(root)
    proposals = proposed_interpretations(root)
    if not instruments:
        return tuple(
            CriterionDecision(
                criterion=criterion, status=UNRESOLVED, selection="",
                boundary="",
                detail="no issued Founder instrument in the curated root "
                       "states a decision for this criterion")
            for criterion in CRITERIA)
    if len(instruments) > 1:
        names = [p.name for p in instruments]
        return tuple(
            CriterionDecision(
                criterion=criterion, status=UNRESOLVED, selection="",
                boundary="",
                detail=f"{len(names)} instruments address this surface "
                       f"({names}); which governs is a Founder question")
            for criterion in CRITERIA)

    instrument = instruments[0]
    locator = instrument.relative_to(root).as_posix()
    bodies = _sections(instrument.read_text(encoding="utf-8"))
    built = []
    for criterion in CRITERIA:
        body = bodies.get(criterion)
        if body is None:
            built.append(CriterionDecision(
                criterion, UNRESOLVED, "", "",
                f"{locator} states no decision section for this criterion",
                locator))
            continue
        selection = _field(body, "Founder selects")
        boundary = _field(body, "Acceptance Boundary")
        blanks = [name for name, value in (("selection", selection),
                                           ("acceptance boundary", boundary))
                  if _is_placeholder(value)]
        if blanks:
            built.append(CriterionDecision(
                criterion, UNRESOLVED, selection, boundary,
                f"the {' and the '.join(blanks)} "
                f"{'are' if len(blanks) > 1 else 'is'} an unfilled template "
                f"placeholder; a form is not a decision", locator))
            continue
        # `§24.4` — the selection must correspond to a proposed interpretation.
        proposal = proposals.get(criterion, {}).get("proposed", "")
        if proposal and not _corresponds(selection, proposal):
            built.append(CriterionDecision(
                criterion, REJECTED, selection, boundary,
                "the selected interpretation does not correspond to the "
                "proposed interpretation in the canonical E12 package; "
                "`§24.5` requires rejection, not substitution", locator))
            continue
        built.append(CriterionDecision(
            criterion, RESOLVED, selection, boundary,
            f"selected and bounded by {locator}", locator))
    return tuple(built)


def _corresponds(selection: str, proposal: str) -> bool:
    """Whether a selection names the proposed interpretation.

    Word containment in either direction — an instrument may cite the proposal
    by identifier or quote it. It is a correspondence check, not a judgement
    about meaning, and it can only ever **reject**; it never supplies a value.
    """
    def tokens(text: str) -> frozenset:
        return frozenset(t for t in re.split(r"[^a-z0-9]+", text.lower()) if t)

    chosen, offered = tokens(selection), tokens(proposal)
    if not chosen or not offered:
        return False
    overlap = len(chosen & offered)
    return overlap >= max(3, min(len(chosen), len(offered)) // 2)


def boundaries(root: Path = REPO_ROOT) -> Dict[str, str]:
    """The five ratified acceptance boundaries — or raise. Fail closed."""
    found = decisions(root)
    unusable = [d for d in found if not d.usable]
    if unusable:
        detail = "; ".join(f"{d.criterion}: {d.detail}" for d in unusable)
        raise AcceptanceBoundaryUnavailable(
            f"{len(unusable)} of {len(found)} criteria carry no Founder-"
            f"supplied acceptance boundary — {detail}")
    return {d.criterion: d.boundary for d in found}


def summary(root: Path = REPO_ROOT) -> dict:
    found = decisions(root)
    return {
        "criteria": len(found),
        "resolved": sum(1 for d in found if d.status == RESOLVED),
        "unresolved": sum(1 for d in found if d.status == UNRESOLVED),
        "rejected": sum(1 for d in found if d.status == REJECTED),
        "measurable": all(d.usable for d in found),
        "blocked": tuple(d.criterion for d in found if not d.usable),
    }


def main(argv=None) -> int:
    for decision in decisions():
        print(f"{decision.criterion}  {decision.status:<11} {decision.detail}")
    print()
    print("summary:", summary())
    print()
    try:
        boundaries()
    except AcceptanceBoundaryUnavailable as unavailable:
        print("ACCEPTANCE BOUNDARY UNAVAILABLE")
        print(f"  {unavailable}")
        print()
        print("A form is not a decision. FOUNDER SELECTS → BOUNDARY → MEASURE;")
        print("this office does not run that chain backwards.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
