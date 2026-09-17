"""`P12-W5` — the phase authorization state, read from the Founder decision body.

`ACT-CC-P12-007 §3` fixes the chain this module exists to hold open:

```text
ACTUAL FOUNDER DECISION BODY → ACTUAL P13 AUTHORIZATION STATE → SELF-MODEL
```

and `§17` fixes the direction: `AUTHORITY SOURCE → SELF-MODEL`, never the
inverse. **This module creates no authority.** It reads a structured block the
Founder already wrote and returns what it says. Delete it and no authorization
changes; only AIOS's ability to report the authorization state is lost. That is
why it lives beside `p12_self_model.py` rather than inside it — the self-model
consumes an authoritative source here, exactly as it does for its other nine
source-backed questions, and does not become the source.

**Why the instrument is discovered from its body rather than named by path.**
`§3`: *"Do not rely solely on filename, decision identifier, registry row,
index, previous Return Package, previous Claude report."* A constant path would
make the filename the authority. Instead the curated governance-acts directory
is scanned and an instrument is recognised only by carrying, in its body, both

- a `FINAL FOUNDER DECISION` section whose own body states `Status: ISSUED`, and
- a `FINAL STATE TRANSITION` section carrying the structured state block.

The directory is curated for the reason `tools/p12_provenance_verification.py`
curates its delegation roots: an arbitrary directory must not be able to
manufacture a Founder decision. Body plus curated root, not one or the other.

**The instrument contradicts itself, and that is disclosed rather than hidden.**
`P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md` carries a stale template header
reading `Status: PENDING FOUNDER DECISION` (line 97) and, in `§35`'s own body,
`Status: ISSUED`. The persisted provenance block at the top of that file
discloses the contradiction and determines ISSUED, reasoning that a decision is
made by its decision section and not by a template line above it. This module
anchors on the `FINAL FOUNDER DECISION` **section body** for exactly that
reason, and `issuance_contradiction()` reports the stale header rather than
quietly winning the argument. A reader who disagrees with the determination can
see what was overruled.

**Nothing here is a substring search for a phase token.** `ACT-CC-P12-006`
found the `§49` control detecting P13's authorization state with
`if "P13" in value`, which the same instrument defeats twice over: `§38` writes
`P12 ≠ P13` as three consecutive lines, and the word appears in prose
throughout. A phase is recognised here only as a line that is *nothing but* the
phase token, inside the state-transition section, and a dimension only as a
`NAME = TRUE|FALSE` line beneath it. `ACT-CC-P12-007 §37`: ``TEXT MATCH ≠
AUTHORITY``.

**Unstated is not FALSE.** The Founder states seven dimensions for P12 and
exactly one for P13. `§4` forbids normalizing that away, and `§9` forbids
inferring a state from anything but an authoritative source — so the six
dimensions P13 does not carry are reported as `unstated_dimensions` and not as
`False`. An unauthorized phase is very probably not constructed; *probably* is
not what a self-model may report.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, Tuple

from tools.planning import AuthorityProvenance

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The curated root. An instrument outside it is not a Founder decision here,
#: however convincingly it is written — the same discipline
#: `p12_provenance_verification.DELEGATION_ROOTS` applies to grants.
DECISION_ROOT = Path("docs/governance/acts")

#: The two sections an issued phase-authorization instrument must carry, matched
#: as section headings rather than as text anywhere in the file.
ISSUANCE_SECTION = "FINAL FOUNDER DECISION"
STATE_SECTION = "FINAL STATE TRANSITION"

ISSUED = "ISSUED"

#: A numbered section heading: ``37. FINAL STATE TRANSITION``. The number is not
#: hard-coded — an instrument that renumbers its sections is still readable.
#:
#: The heading is recognised by *case*, not by an allow-list of punctuation. The
#: first version spelled the allowed characters out and silently failed on
#: ``29. P12 → P13 RULE``, folding that section's body into `§28` and attributing
#: `§29`'s words to the wrong section — a provenance defect, in the one Act whose
#: subject is provenance. Requiring every cased letter to be uppercase keeps
#: numbered prose (``1. P12 authorization is explicit.``) out without predicting
#: which dashes and arrows a Founder will type. A sub-numbered line such as
#: ``13.5 P13 Construction`` has no space after its dot and is not a section.
_HEADING = re.compile(r"^(\d+)\.\s+(\S.*\S)\s*$")


def _is_heading_text(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)
#: A line that is *nothing but* a phase token.
_PHASE = re.compile(r"^(P\d+)$")
#: ``AUTHORIZED = FALSE`` — a declared dimension, not prose that mentions one.
_DIMENSION = re.compile(r"^([A-Z][A-Z ]*[A-Z])\s*=\s*(TRUE|FALSE)$")
#: ``Status: ISSUED``
_STATUS = re.compile(r"^Status:\s*(.+?)\s*$")


class PhaseAuthorizationUnresolved(Exception):
    """No single issued instrument could be recognised.

    Raised rather than returning an empty result, for the reason
    `tools/p12_certified_evidence_guard.py` raises: *"certification
    undeterminable"* and *"nothing is authorized"* are different answers, and a
    caller that cannot tell them apart will read the second for the first.
    """


@dataclass(frozen=True)
class PhaseState:
    """One phase's authorization state, as the Founder decision states it.

    `ACT-CC-P12-007 §6` requires entity, authorization state, authoritative
    source, provenance and — where required — interpretation to be distinct.
    They are five fields here rather than one string for that reason: a caller
    cannot read the status without also being handed what it rests on.

    `§8` requires the state dimensions not be collapsed into one value, which is
    why `dimensions` is a mapping and `authorized` is only a convenience over
    the one dimension named `AUTHORIZED`.
    """

    entity: str
    dimensions: Mapping[str, bool]
    authority: AuthorityProvenance
    stated_in: str
    corroborated_by: Tuple[str, ...]
    unstated_dimensions: Tuple[str, ...]

    @property
    def authorized(self) -> Optional[bool]:
        """`True`/`False` as stated; `None` when the source does not say.

        `None` is not `False`. `§9`: authorization is not inferred from the
        absence of a statement any more than from the presence of a document.
        """
        return self.dimensions.get("AUTHORIZED")

    def as_reported(self) -> dict:
        """The shape the self-model publishes. Plain data, no behaviour."""
        return {
            "entity": self.entity,
            "authorized": self.authorized,
            "dimensions": dict(self.dimensions),
            "unstated_dimensions": self.unstated_dimensions,
            "stated_in": self.stated_in,
            "corroborated_by": self.corroborated_by,
            "authority": self.authority.cited(),
            "authority_record": self.authority.record,
        }


def _sections(text: str) -> Tuple[Tuple[str, str, Tuple[str, ...]], ...]:
    """Split a decision body into `(number, heading, lines)` sections."""
    found, number, heading, body = [], None, None, []
    for line in text.splitlines():
        match = _HEADING.match(line.strip())
        if match and _is_heading_text(match.group(2)):
            if heading is not None:
                found.append((number, heading, tuple(body)))
            number, heading, body = match.group(1), match.group(2), []
            continue
        if heading is not None:
            body.append(line.rstrip())
    if heading is not None:
        found.append((number, heading, tuple(body)))
    return tuple(found)


def _section(sections, heading: str):
    for number, found, body in sections:
        if found == heading:
            return number, found, body
    return None


def _is_issued(sections) -> bool:
    """Issuance is read from the decision section's own body.

    Not from a file-wide search: the resident instrument carries a stale
    `Status: PENDING FOUNDER DECISION` in its template header, and a file-wide
    match would find whichever came first.
    """
    section = _section(sections, ISSUANCE_SECTION)
    if section is None:
        return False
    for line in section[2]:
        match = _STATUS.match(line.strip())
        if match:
            return match.group(1).upper() == ISSUED
    return False


def _states_in(body: Tuple[str, ...]) -> Tuple[Tuple[str, dict], ...]:
    """Parse the state-transition block into `(entity, dimensions)` pairs.

    A phase opens only on a line that is nothing but its token, and a dimension
    is only a `NAME = TRUE|FALSE` line. Prose inside the section — *"This is the
    intended state transition."* — matches neither and is ignored.
    """
    found, entity, dimensions = [], None, {}
    for line in body:
        stripped = line.strip()
        phase = _PHASE.match(stripped)
        if phase:
            if entity is not None:
                found.append((entity, dimensions))
            entity, dimensions = phase.group(1), {}
            continue
        dimension = _DIMENSION.match(stripped)
        if dimension and entity is not None:
            dimensions[dimension.group(1)] = dimension.group(2) == "TRUE"
    if entity is not None:
        found.append((entity, dimensions))
    return tuple(found)


def _corroborating(sections, entity: str, authorized: Optional[bool]
                   ) -> Tuple[str, ...]:
    """Other sections of the same body that assert the same state.

    **Supporting evidence, never the authority.** The structured block in
    `STATE_SECTION` is what this module reads a state from; this reports which
    other sections agree, so a single altered line is visibly at odds with the
    rest of the instrument rather than silently authoritative. Only the
    unauthorized direction is recognised, because that is the only assertion the
    resident vocabulary makes in prose — a section that *granted* authorization
    would have to do it in the structured block to count.
    """
    if authorized is not False:
        return ()
    token = re.compile(rf"(?:^|[^A-Za-z0-9]){entity}(?:[^A-Za-z0-9]|$)")
    negated = re.compile(r"\b(?:tetap\s+unauthorized|NOT\s+AUTHORIZED"
                         r"|remains?\s+unauthorized|tidak\s+authorized)\b",
                         re.IGNORECASE)
    agreeing = []
    for number, heading, body in sections:
        if heading == STATE_SECTION:
            continue
        for index, line in enumerate(body):
            if not token.search(line):
                continue
            window = " ".join(body[index:index + 4])
            if negated.search(window):
                agreeing.append(f"§{number} {heading}".rstrip())
                break
    return tuple(agreeing)


def decision_instrument(root: Path = REPO_ROOT) -> Path:
    """The one issued instrument carrying a structured phase-state block.

    Raises when there is not exactly one. Two would mean the corpus disagrees
    with itself about phase authorization, which a reader must not resolve by
    picking the first — `§9`, and `ACT-CC-P11-005 §36`:
    ``IDENTIFIER ≠ DECISION BODY``.
    """
    directory = root / DECISION_ROOT
    if not directory.is_dir():
        raise PhaseAuthorizationUnresolved(
            f"the governance acts root does not resolve: {DECISION_ROOT}")
    found = []
    for path in sorted(directory.glob("*.md")):
        try:
            sections = _sections(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        if _section(sections, STATE_SECTION) and _is_issued(sections):
            found.append(path)
    if not found:
        raise PhaseAuthorizationUnresolved(
            "no issued instrument in the curated governance acts root carries "
            f"a '{STATE_SECTION}' section; phase authorization state is "
            "undeterminable, which is not the same as unauthorized")
    if len(found) > 1:
        names = ", ".join(p.name for p in found)
        raise PhaseAuthorizationUnresolved(
            f"{len(found)} issued instruments carry a phase-state block "
            f"({names}); which one governs is a Founder question, not a "
            "parsing one")
    return found[0]


def phase_states(root: Path = REPO_ROOT) -> Tuple[PhaseState, ...]:
    """Every phase the issued instrument states a state for, in its order."""
    instrument = decision_instrument(root)
    sections = _sections(instrument.read_text(encoding="utf-8"))
    number, heading, body = _section(sections, STATE_SECTION)
    parsed = _states_in(body)
    declared = {name for _, dimensions in parsed for name in dimensions}
    record = instrument.relative_to(root).as_posix()
    authority = AuthorityProvenance(
        f"P12 Authorization Founder Decision §{number} {heading}", record)
    states = []
    for entity, dimensions in parsed:
        states.append(PhaseState(
            entity=entity,
            dimensions=dict(dimensions),
            authority=authority,
            stated_in=f"§{number} {heading}",
            corroborated_by=_corroborating(
                sections, entity, dimensions.get("AUTHORIZED")),
            unstated_dimensions=tuple(sorted(declared - set(dimensions)))))
    return tuple(states)


def state_of(entity: str, root: Path = REPO_ROOT) -> Optional[PhaseState]:
    """One phase's state, or `None` when the instrument states none for it."""
    for state in phase_states(root):
        if state.entity == entity:
            return state
    return None


def issuance_contradiction(root: Path = REPO_ROOT) -> Optional[dict]:
    """The stale header this instrument carries, reported rather than hidden.

    Returns `None` when the body is self-consistent.
    """
    instrument = decision_instrument(root)
    text = instrument.read_text(encoding="utf-8")
    sections = _sections(text)
    decision = _section(sections, ISSUANCE_SECTION)
    preamble = text.split(f"{decision[0]}. {ISSUANCE_SECTION}")[0]
    stale = [line.strip() for line in preamble.splitlines()
             if _STATUS.match(line.strip())
             and _STATUS.match(line.strip()).group(1).upper() != ISSUED]
    if not stale:
        return None
    return {
        "instrument": instrument.relative_to(root).as_posix(),
        "authoritative": f"§{decision[0]} {ISSUANCE_SECTION}: Status: {ISSUED}",
        "stale_header": tuple(stale),
        "determination": ("the decision section governs; the header is "
                          "unchanged template text from the surface sent for "
                          "signature. Disclosed, not resolved away"),
    }


def summary(root: Path = REPO_ROOT) -> dict:
    states = phase_states(root)
    return {
        "instrument": decision_instrument(root).relative_to(root).as_posix(),
        "phases": len(states),
        "states": {s.entity: s.authorized for s in states},
        "unstated": {s.entity: s.unstated_dimensions for s in states},
        "issuance_contradiction": issuance_contradiction(root) is not None,
    }


def main(argv=None) -> int:
    import json
    print(json.dumps(summary(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
