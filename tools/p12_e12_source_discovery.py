"""`ACT-CC-P12-018 §5` — where `E12-01`…`E12-05` actually come from.

Two different questions are asked about `E12` in this corpus, and conflating
them is how a preparation package turns into a decision:

```text
p12_e12_criteria          what has the Founder DECIDED?   (today: nothing)
p12_e12_source_discovery  what does the corpus SAY the requirement and the
                          existing proposal are?          (this module)
```

**This module resolves provenance, and provenance is not authority.**
`AuthorityProvenance` states the rule this is built around: *"a resolved
citation proves the pointer is real, not that the cited source supports the
claim made about it."* So each criterion's cited section is opened and its body
checked for the requirement the package attributes to it. A citation that
resolves to a section which does not contain the claim is `CONTRADICTION`, not
`RESOLVED`.

**Bare `§n` is ambiguous in this corpus and the ambiguity is load-bearing here.**
`ACT-CC-P12-016` found two different `§19`s — the Blueprint's *"Staleness /
Conflict / Reconciliation"* and the Founder Authorization's *"P12-W6 System-wide
Verification Authority"*. The same split runs through `§14`–`§18`: the Blueprint's
are `State Model`, `State Sources`, `State Consumers`, `State Authority`,
`State Lifecycle`, while the Founder Authorization's are the five workstream
authorities `E12-01`…`E12-05` are actually derived from. Reading the wrong
document would attribute each criterion to the wrong requirement, so the
citation target is named explicitly here and verified by body.

**Nothing here selects.** It reports what exists, and `EXISTING PROPOSAL` is the
only status a proposal can carry — `§6`: *"Jika hanya ada satu proposed
interpretation, Claude tetap harus menyajikannya sebagai EXISTING PROPOSAL,
bukan SELECTED INTERPRETATION."* `ONE CANDIDATE ≠ A SELECTION`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The instrument the five canonical requirements actually live in. Named, not
#: inferred: a bare `§14` resolves differently in the Blueprint.
REQUIREMENT_SOURCE = Path(
    "docs/governance/acts/P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md")

#: The package that carries the existing proposals. This is the **resident**
#: one; a document of the same name may exist elsewhere and be a different
#: document. `FILENAME ≠ CANONICAL STATUS`.
PROPOSAL_SOURCE = Path(
    "docs/architecture/p12/E12-RATIFICATION-DECISION-PACKAGE.md")

#: Criterion → the Founder Authorization section that states its requirement,
#: and the workstream it authorizes. Taken from the proposal package's own
#: `Canonical definition` cells and verified against the section bodies.
CITED_SECTION: Dict[str, Tuple[int, str]] = {
    "E12-01": (14, "P12-W1 — SYSTEM INTEGRATION AUTHORITY"),
    "E12-02": (15, "P12-W2 — UNIFIED OPERATIONAL STATE AUTHORITY"),
    "E12-03": (16, "P12-W3 — GOVERNANCE INTEGRATION AUTHORITY"),
    "E12-04": (17, "P12-W4 — EXECUTION INTEGRATION AUTHORITY"),
    "E12-05": (18, "P12-W5 — AIOS SELF-MODEL AUTHORITY"),
}

RESOLVED = "RESOLVED"
SOURCE_GAP = "SOURCE-GAP"
AUTHORITY_GAP = "AUTHORITY-GAP"
CONTRADICTION = "CONTRADICTION"
UNKNOWN = "UNKNOWN"

#: A quotation the package attributes to its cited section: *"…"*.
_QUOTED = re.compile(r"\*\"([^\"]{8,})\"\*")


@dataclass(frozen=True)
class Discovery:
    """`§5`'s twelve fields for one criterion, each read or explicitly absent."""

    criterion: str
    status: str
    originating_artifact: str
    section: str
    requirement_body: str
    existing_proposal: str
    existing_boundary: str
    authority: str
    provenance: str
    current_status: str
    detail: str

    def as_reported(self) -> dict:
        return {
            "criterion": self.criterion,
            "status": self.status,
            "originating_artifact": self.originating_artifact,
            "section": self.section,
            "existing_proposal": self.existing_proposal,
            "authority": self.authority,
            "provenance": self.provenance,
            "current_status": self.current_status,
            "detail": self.detail,
        }


def _section_body(text: str, number: int) -> Optional[Tuple[str, str]]:
    """`(heading, body)` for a numbered section, or `None` if absent."""
    start = re.search(rf"^{number}\.\s+(\S.*)$", text, re.M)
    if start is None:
        return None
    following = re.search(rf"^{number + 1}\.\s+\S.*$", text[start.end():], re.M)
    end = start.end() + (following.start() if following else len(text))
    return start.group(1).strip(), text[start.end():end]


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def discover(root: Path = REPO_ROOT) -> Tuple[Discovery, ...]:
    """Resolve each criterion from actual bodies. Reports; never raises."""
    from tools import p12_e12_criteria as criteria

    requirement_path = root / REQUIREMENT_SOURCE
    proposal_path = root / PROPOSAL_SOURCE
    requirement_text = (requirement_path.read_text(encoding="utf-8")
                        if requirement_path.is_file() else "")
    proposals = criteria.proposed_interpretations(root)

    found = []
    for criterion, (number, expected_heading) in CITED_SECTION.items():
        proposal = proposals.get(criterion, {})
        proposed = proposal.get("proposed", "")
        definition = proposal.get("canonical_definition", "")

        if not requirement_text:
            found.append(Discovery(
                criterion, SOURCE_GAP, REQUIREMENT_SOURCE.as_posix(),
                f"§{number}", "", proposed, "", "", "unresolved", UNKNOWN,
                "the instrument stating the canonical requirement does not "
                "resolve in this corpus"))
            continue
        if not proposed:
            found.append(Discovery(
                criterion, SOURCE_GAP, REQUIREMENT_SOURCE.as_posix(),
                f"§{number}", "", "", "", "Founder P12 Authorization",
                "unresolved", UNKNOWN,
                f"{PROPOSAL_SOURCE.as_posix()} carries no proposed "
                "interpretation for this criterion"))
            continue

        section = _section_body(requirement_text, number)
        if section is None:
            found.append(Discovery(
                criterion, SOURCE_GAP, REQUIREMENT_SOURCE.as_posix(),
                f"§{number}", "", proposed, "", "Founder P12 Authorization",
                "cited section absent", UNKNOWN,
                f"§{number} is cited but no such section exists in "
                f"{REQUIREMENT_SOURCE.name}"))
            continue

        heading, body = section
        if _normalise(expected_heading) not in _normalise(heading):
            found.append(Discovery(
                criterion, CONTRADICTION, REQUIREMENT_SOURCE.as_posix(),
                f"§{number} {heading}", body, proposed, "",
                "Founder P12 Authorization", "heading mismatch", UNKNOWN,
                f"§{number} is {heading!r}, not {expected_heading!r}; a bare "
                "section number resolves differently across instruments"))
            continue

        # Provenance: every phrase the package quotes must actually appear in
        # the cited section. A pointer that resolves is not a pointer that
        # supports the claim.
        quoted = _QUOTED.findall(definition)
        missing = [q for q in quoted if _normalise(q) not in _normalise(body)]
        if missing:
            found.append(Discovery(
                criterion, CONTRADICTION, REQUIREMENT_SOURCE.as_posix(),
                f"§{number} {heading}", body, proposed, "",
                "Founder P12 Authorization", "quotation not in cited body",
                UNKNOWN,
                f"{len(missing)} quotation(s) attributed to §{number} do not "
                f"appear in its body: {missing}"))
            continue

        found.append(Discovery(
            criterion=criterion,
            status=RESOLVED,
            originating_artifact=REQUIREMENT_SOURCE.as_posix(),
            section=f"§{number} {heading}",
            requirement_body=body.strip(),
            existing_proposal=proposed,
            existing_boundary=_boundary_elements(proposal_path, criterion),
            authority="Founder P12 Authorization — ISSUED",
            provenance=(f"{len(quoted)} quotation(s) verified present in "
                        f"§{number}; proposal read from "
                        f"{PROPOSAL_SOURCE.as_posix()}"),
            current_status="EXISTING PROPOSAL — NOT RATIFIED",
            detail="requirement and proposal both resolve to actual bodies"))
    return tuple(found)


def _boundary_elements(path: Path, criterion: str) -> str:
    """The package's own `Evidence source` / `Verification method` /
    `Negative control` / `Failure semantics` rows for a criterion.

    These are what `§7` calls the existing acceptance boundary: the package
    states them beside the proposal, and nothing here composes one.
    """
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8")
    heading = re.search(rf"^###\s+`{re.escape(criterion)}`\s*[—–-].*$",
                        text, re.M)
    if heading is None:
        return ""
    following = re.search(r"^###\s+`E12-0\d`", text[heading.end():], re.M)
    end = heading.end() + (following.start() if following else len(text))
    block = text[heading.end():end]
    rows = []
    for label in ("Evidence source", "Verification method", "Negative control",
                  "Failure semantics"):
        row = re.search(rf"^\|\s*{label}\s*\|\s*(.+?)\s*\|\s*$", block, re.M)
        if row:
            rows.append(f"{label}: {row.group(1)}")
    return " · ".join(rows)


def summary(root: Path = REPO_ROOT) -> dict:
    found = discover(root)
    return {
        "criteria": len(found),
        "resolved": sum(1 for d in found if d.status == RESOLVED),
        "source_gaps": tuple(d.criterion for d in found
                             if d.status == SOURCE_GAP),
        "contradictions": tuple(d.criterion for d in found
                                if d.status == CONTRADICTION),
        "authority_gaps": tuple(d.criterion for d in found
                                if d.status == AUTHORITY_GAP),
        # Every proposal is an EXISTING PROPOSAL and none is ratified. This key
        # exists so the distinction is in the machine output, not only prose.
        "ratified": (),
        "all_existing_proposals_unratified": all(
            d.current_status == "EXISTING PROPOSAL — NOT RATIFIED"
            for d in found),
    }


def main(argv=None) -> int:
    for discovery in discover():
        print(f"--- {discovery.criterion}  [{discovery.status}]")
        print(f"    artifact   {discovery.originating_artifact}")
        print(f"    section    {discovery.section}")
        print(f"    proposal   {discovery.existing_proposal[:120]}")
        print(f"    provenance {discovery.provenance}")
        print(f"    status     {discovery.current_status}")
    print()
    print("summary:", summary())
    print()
    print("EXISTING PROPOSAL, not SELECTED INTERPRETATION.")
    print("ONE CANDIDATE != A SELECTION.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
