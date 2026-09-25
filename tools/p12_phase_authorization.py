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

**A later Founder decision supersedes the snapshot; it does not rewrite it.**
`certifications()` (`GOAL-V2-002`) and `authorizations()` (`FDR-6` `CR-3`)
read later resolving instruments, and `current_states()` sets aside what they
supersede with the provenance of both. `phase_states()` keeps returning the
`§37` block exactly as the Founder wrote it.

**Closure is read beside the states (`FDR-G3`).** `closures()` recognises a
Founder closure decision under the conditions of `FDR-G3` `§27`. `lifecycle()`
reports the `§27` state machine (AUTHORIZED → EXIT SATISFIED → CERTIFIED →
CLOSED), each state from its own source. Closure is never folded into a
phase's `dimensions`, which hold only what their cited section states.
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


def certifications(root: Path = REPO_ROOT) -> dict:
    """Phase certifications that resolve against the Register, with provenance.

    Added under `GOAL-V2-002`. The state block `phase_states` reads is a
    **P12-entry snapshot** (`§37`: the state *"immediately after this decision
    is validly persisted"*). It still says `P12 CERTIFIED = FALSE`, six days
    after `FD-P12-006` certified P12 (`H-1`). A later Founder instrument decides
    a later state, and this reports it. The certifying instruments are read by
    the same resolution rule the certified-evidence guard enforces
    (`FD-P12-004`: a certification that resolves against no record is
    rejected), so the self-model and the guard cannot disagree about which
    phases are certified.

    Fails visibly: when governance cannot be read, it returns
    `resolved: False` with the reason. It never returns an empty set, which
    would read as *"nothing is certified"*.
    """
    from tools import p12_certified_evidence_guard as sentinel
    acts = root / "docs/governance/acts"
    register = root / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
    try:
        phases = sentinel.certified_phases(acts, register)
    except sentinel.CertificationUndeterminable as undeterminable:
        return {"resolved": False, "phases": {}, "detail": str(undeterminable)}
    register_text = register.read_text(encoding="utf-8")
    found = {}
    for phase, name in sentinel.certification_provenance(acts):
        if phase not in phases:
            continue
        found[f"P{phase}"] = {
            "certified": True,
            "instrument": (acts / name).relative_to(root).as_posix(),
            "register_identity": sentinel._register_identity(
                Path(name).stem, register_text),
        }
    return {"resolved": True, "phases": found}


#: A later Founder phase authorization, read under `FDR-6` (`CR-3`): the
#: section it is read from, matched as a heading, and the one line form that
#: is recognised inside it. `FDR-6 §19` writes the decision as a line that is
#: nothing but ``AUTHORIZE PHASE 13``, under ``19. FOUNDER DECISION``.
AUTHORIZATION_SECTION = "FOUNDER DECISION"
_AUTHORIZES = re.compile(r"^AUTHORIZE PHASE (\d+)$")


def authorizations(root: Path = REPO_ROOT) -> dict:
    """Phase authorizations a later Founder instrument decided, with provenance.

    Added under `FDR-6` (`CR-3`). The `§37` block is a snapshot, and its `§29`
    keeps P13 unauthorized *"until a separate valid Founder authorization"*.
    `FDR-6` `FDQ-1` is that authorization, and it asks for *"canonical
    representation melalui phase-authorization machinery"*. The machinery could
    not represent it before this: it reads exactly one state block, and
    `certifications()` never supersedes `AUTHORIZED`. This mirrors
    `certifications()` rather than adding a second state block, which
    `decision_instrument` would rightly refuse as two instruments disagreeing.

    **Recognised by body, and resolved against the Register.** An instrument
    counts only if all of these hold:

    - it is in the curated acts root;
    - a numbered section is headed exactly `FOUNDER DECISION`;
    - that section holds a line that is nothing but `AUTHORIZE PHASE <n>`;
    - it resolves against the Decision Register, under the rule the
      certified-evidence guard applies to certifications (`FD-P12-004`).

    An instrument that fails the last test is **rejected** and listed under
    `rejected`, not silently skipped. Two resolving instruments for one phase
    are reported under `ambiguous` and neither is applied.

    **Authorization is not certification.** Nothing here reads, sets or implies
    a certification, a closure or any dimension other than `AUTHORIZED`.

    Fails visibly: when governance cannot be read, it returns `resolved: False`
    with the reason. It never returns an empty set, which would read as
    *"nothing is authorized"*.
    """
    from tools import p12_certified_evidence_guard as sentinel
    acts = root / DECISION_ROOT
    register = root / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
    if not acts.is_dir():
        return {"resolved": False, "phases": {}, "ambiguous": {}, "rejected": (),
                "detail": f"the governance acts root does not resolve: {DECISION_ROOT}"}
    try:
        register_text = register.read_text(encoding="utf-8")
    except OSError as error:
        return {"resolved": False, "phases": {}, "ambiguous": {}, "rejected": (),
                "detail": (f"the Decision Register cannot be read ({error}); an "
                           "authorization cannot be resolved against it")}
    found, rejected = {}, []
    for path in sorted(acts.glob("*.md")):
        try:
            sections = _sections(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        section = _section(sections, AUTHORIZATION_SECTION)
        if section is None:
            continue
        number, heading, body = section
        claimed = sorted({f"P{match.group(1)}" for match in
                          (_AUTHORIZES.match(line.strip()) for line in body)
                          if match})
        if not claimed:
            continue
        record = path.relative_to(root).as_posix()
        identity = sentinel._register_identity(path.stem, register_text)
        if identity is None:
            rejected.append({"instrument": record, "phases": tuple(claimed),
                             "reason": "resolves against no Decision Register record"})
            continue
        for phase in claimed:
            found.setdefault(phase, []).append({
                "instrument": record, "register_identity": identity,
                "stated_in": f"§{number} {heading}"})
    phases, ambiguous = {}, {}
    for phase, instruments in found.items():
        if len(instruments) == 1:
            phases[phase] = {"authorized": True, **instruments[0]}
        else:
            ambiguous[phase] = tuple(i["instrument"] for i in instruments)
    return {"resolved": True, "phases": phases, "ambiguous": ambiguous,
            "rejected": tuple(rejected)}


#: A Founder closure decision, read under `FDR-G3` `§25`, `§27`. The line is
#: recognised only directly under the Founder's decision label, as `FDR-G3`
#: writes it in `§1` and `§36`:
#:
#:     The Founder hereby decides:
#:
#:     P13 CLOSURE = GRANTED
#:
#: `FDR-G2` `§6.4` carries the same line under *"The Closure Decision shall
#: explicitly state:"*. That is a stated form, and it is not read as a decision.
#: The guard's third certification form is anchored the same way, for the
#: same reason.
_CLOSES = re.compile(
    r"^The Founder hereby (?:decides|grants):[ \t]*\n(?:[ \t]*\n)*"
    r"[ \t]*P(\d+) CLOSURE[ \t]*=[ \t]*GRANTED[ \t]*$", re.MULTILINE)
#: Any closure line at all, anchored or not. Used only to report mentions.
_CLOSURE_LINE = re.compile(r"^[ \t]*P(\d+) CLOSURE[ \t]*=[ \t]*GRANTED[ \t]*$",
                           re.MULTILINE)
REGISTER_PATH = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"


def _founder_entry(register_text: str, record: str) -> Optional[Tuple[str, int]]:
    """The Register's Founder Decision entry recording `record`: its identifier
    and the offset of its heading. `None` if no such entry exists.

    An entry ends at the next heading of any level. Ending it only at the next
    Founder Decision heading would let the last one absorb every later entry,
    and a later entry's record would then read as decided by the Founder."""
    for heading in re.finditer(r"^### (\S+) — Founder Decision\b.*$", register_text,
                               re.MULTILINE):
        rest = register_text[heading.end():]
        following = re.search(r"^#{1,6} ", rest, re.MULTILINE)
        block = register_text[heading.start():
                              heading.end() + (following.start() if following else len(rest))]
        if (f"acts/{record}" in block
                and re.search(r"^\| \*\*Decided by\*\* \| Founder\b", block, re.MULTILINE)):
            return heading.group(1), heading.start()
    return None


def _superseded_by(register_text: str, identifier: str) -> Optional[str]:
    """The Register row that declares `identifier` superseded, if any."""
    match = re.search(r"^\| \*\*Supersedes\*\* \|[^\n]*`" + re.escape(identifier)
                      + r"`", register_text, re.MULTILINE)
    return match.group(0) if match else None


def _closure_evidence(number: str, root: Path, register_text: str,
                      before: int) -> Tuple[Optional[dict], str]:
    """The `FD-G2-C6` evidence for closing phase `number`, registered before the
    decision: a SATISFIED closure gate and a holding fresh verification, both
    taken at the same commit. Returns `(evidence, "")` or `(None, reason)`."""
    import hashlib
    import json
    directory = root / f"docs/governance/p{number}-closure"

    def registered(path: Path) -> bool:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        offset = register_text.find(digest)
        return 0 <= offset < before

    gates = {}
    for path in sorted(directory.glob(f"P{number}-CLOSURE-GATE-*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (registered(path) and record.get("gate") == "SATISFIED"
                and record.get("closes") is False):
            gates[path.stem.rsplit("-", 1)[-1]] = path
    for path in sorted(directory.glob(f"P{number}-FRESH-VERIFICATION-*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        commit = str(record.get("commit", ""))
        gate = next((g for tag, g in gates.items() if tag and commit.startswith(tag)), None)
        if registered(path) and record.get("holds") is True and gate is not None:
            return {"closure_gate": gate.relative_to(root).as_posix(),
                    "fresh_verification": path.relative_to(root).as_posix(),
                    "commit": commit}, ""
    return None, ("no registered SATISFIED closure gate with a holding fresh "
                  "verification at the same commit, registered before the "
                  "decision (FD-G2-C6)")


def closures(root: Path = REPO_ROOT) -> dict:
    """Phase closures a Founder decision granted, with provenance (`FDR-G3`).

    Closure is reported beside the phase states, never folded into them, as
    certification is. The independent verifier holds every reported dimension
    to what its cited section states, and a closure is not written there.

    **A closure counts only if every condition of `FDR-G3` `§27` holds:**

    - the decision line is anchored on the Founder's decision label (`_CLOSES`);
    - it is in the curated acts root;
    - the Register records the act's path under a `### … — Founder Decision`
      entry decided by the Founder;
    - no Register entry declares that decision superseded;
    - the `FD-G2-C6` evidence was registered before the decision
      (`_closure_evidence`).

    An instrument failing a condition is listed under `rejected`, with the
    reason. A closure line that is not a decision (a stated form, a quotation)
    is listed under `mentions` and closes nothing. Two valid decisions for one
    phase are `ambiguous`, and neither is applied.

    **Closure is not certification, and grants no authority.** Nothing here
    reads or sets any other state.

    Fails visibly: an unreadable governance source returns `resolved: False`.
    """
    acts = root / DECISION_ROOT
    try:
        register_text = (root / REGISTER_PATH).read_text(encoding="utf-8")
    except OSError as error:
        return {"resolved": False, "phases": {}, "ambiguous": {}, "rejected": (),
                "mentions": (), "detail": f"the Decision Register cannot be read ({error})"}
    if not acts.is_dir():
        return {"resolved": False, "phases": {}, "ambiguous": {}, "rejected": (),
                "mentions": (), "detail": f"the acts root does not resolve: {DECISION_ROOT}"}
    found, rejected, mentions = {}, [], []
    for path in sorted(acts.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        decided = sorted({m.group(1) for m in _CLOSES.finditer(text)})
        mentioned = sorted({m.group(1) for m in _CLOSURE_LINE.finditer(text)})
        record = path.relative_to(root).as_posix()
        if not decided:
            if mentioned:
                mentions.append({"instrument": record,
                                 "phases": tuple(f"P{n}" for n in mentioned)})
            continue
        entry = _founder_entry(register_text, path.name)
        for number in decided:
            phase = f"P{number}"
            if entry is None:
                rejected.append({"instrument": record, "phase": phase, "reason":
                                 "not recorded in the Register as a Founder Decision"})
                continue
            identifier, offset = entry
            superseded = _superseded_by(register_text, identifier)
            if superseded:
                rejected.append({"instrument": record, "phase": phase,
                                 "reason": f"superseded: {superseded}"})
                continue
            evidence, reason = _closure_evidence(number, root, register_text, offset)
            if evidence is None:
                rejected.append({"instrument": record, "phase": phase, "reason": reason})
                continue
            # Line numbers, not section names: a list item in capitals
            # (`4. ACT-CC-POST-P13-GOV-002;`) reads as a section heading to
            # `_sections`, and would misattribute the decision.
            stated = [f"line {text.count(chr(10), 0, m.end()) + 1}"
                      for m in _CLOSES.finditer(text) if m.group(1) == number]
            found.setdefault(phase, []).append({
                "instrument": record, "register_identity": identifier,
                "stated_in": tuple(stated), "evidence": evidence})
    phases, ambiguous = {}, {}
    for phase, instruments in found.items():
        if len(instruments) == 1:
            phases[phase] = {"closed": True, **instruments[0]}
        else:
            ambiguous[phase] = tuple(i["instrument"] for i in instruments)
    return {"resolved": True, "phases": phases, "ambiguous": ambiguous,
            "rejected": tuple(rejected), "mentions": tuple(mentions)}


#: `FDR-5`'s decision of the P13 exit contract, read for `lifecycle()`.
_EXIT_SATISFIED = re.compile(r"^P(\d+) Exit Contract = SATISFIED$", re.MULTILINE)


def lifecycle(entity: str = "P13", root: Path = REPO_ROOT) -> dict:
    """The `FDR-G3` `§27` state machine for one phase, from its separate sources:

    ```text
    AUTHORIZED → EXIT SATISFIED → CERTIFIED → CLOSED
    ```

    Each state is read where it is decided: authorization from
    `current_states()`; exit from a Register-recorded Founder Decision carrying
    the exit line; certification from `certifications()`; closure from
    `closures()`. It derives nothing from anything else, so a closure without
    certification, for example, is reported as exactly that.
    """
    states = {s["entity"]: s for s in current_states(root)}
    certified = certifications(root)
    closed = closures(root)
    exit_source = None
    try:
        register_text = (root / REGISTER_PATH).read_text(encoding="utf-8")
        for path in sorted((root / DECISION_ROOT).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if (any(m.group(1) == entity[1:] for m in _EXIT_SATISFIED.finditer(text))
                    and _founder_entry(register_text, path.name) is not None):
                exit_source = path.relative_to(root).as_posix()
                break
    except OSError:
        exit_source = None
    return {
        "entity": entity,
        "authorized": (states.get(entity) or {}).get("authorized"),
        "exit_satisfied": exit_source is not None,
        "exit_source": exit_source,
        "certified": entity in (certified.get("phases") or {}),
        "certification_source": ((certified.get("phases") or {}).get(entity) or {})
        .get("instrument"),
        "closed": entity in (closed.get("phases") or {}),
        "closure_source": ((closed.get("phases") or {}).get(entity) or {}).get("instrument"),
        "resolved": bool(certified.get("resolved")) and bool(closed.get("resolved")),
    }


def current_states(root: Path = REPO_ROOT) -> Tuple[dict, ...]:
    """The snapshot states, with what a later Founder instrument supersedes set aside.

    For a phase that a resolving instrument has certified, a snapshot dimension
    stated `FALSE` (other than `AUTHORIZED`) describes a state before
    certification. Such a dimension is **moved** to
    `superseded_by_certification`, which names the instrument. It is not
    deleted and not flipped to `TRUE`. Every dimension left in `dimensions` is
    still written in the cited section, so the independent check in
    `p12_phase_authorization_verifier` (reported ⊆ stated) continues to hold.
    Certification itself is reported by `certifications()`, with its own
    provenance. Two sources are never folded into one record.

    **`FDR-6` (`CR-3`).** For a phase the snapshot states `AUTHORIZED = FALSE`
    and a resolving Founder instrument authorizes (`authorizations()`), the
    reported `AUTHORIZED` is `TRUE`. The snapshot value is moved to
    `superseded_by_authorization`, with its section, record and corroboration.
    The entry's `stated_in`, `authority` and `authority_record` then cite the
    authorizing instrument, because that is where the reported value is
    written. `phase_states()` and `state_of()` still return the snapshot as the
    Founder wrote it.
    """
    certified = certifications(root)
    by_phase = certified["phases"] if certified["resolved"] else {}
    authorized = authorizations(root)
    by_authorization = authorized["phases"] if authorized["resolved"] else {}
    current = []
    for state in phase_states(root):
        reported = state.as_reported()
        authorization = by_authorization.get(state.entity)
        if authorization is not None and state.authorized is False:
            citation = AuthorityProvenance(
                f"Founder authorization {authorization['register_identity']} "
                f"{authorization['stated_in']}", authorization["instrument"])
            reported["dimensions"] = {**reported["dimensions"], "AUTHORIZED": True}
            reported["authorized"] = True
            reported["superseded_by_authorization"] = {
                "dimensions": {"AUTHORIZED": False},
                "stated_in": state.stated_in,
                "authority_record": state.authority.record,
                "corroborated_by": state.corroborated_by,
                "superseded_by": authorization["instrument"],
                "register_identity": authorization["register_identity"],
            }
            reported["stated_in"] = authorization["stated_in"]
            reported["corroborated_by"] = ()
            reported["authority"] = citation.cited()
            reported["authority_record"] = citation.record
        certification = by_phase.get(state.entity)
        if certification is not None:
            kept, superseded = {}, {}
            # The dimensions as already reported, with any later
            # authorization applied. Reading `state.dimensions` (the §37
            # snapshot) here put `AUTHORIZED = FALSE` back under a
            # certified phase that a later decision had authorized, which
            # surfaced when `FDR-7` certified P13 after `FDR-6` authorized it.
            for name, value in reported["dimensions"].items():
                if value is False and name != "AUTHORIZED":
                    superseded[name] = value
                else:
                    kept[name] = value
            reported["dimensions"] = kept
            if superseded:
                reported["superseded_by_certification"] = {
                    "dimensions": superseded,
                    "stated_in": state.stated_in,
                    "superseded_by": certification["instrument"],
                    "register_identity": certification["register_identity"],
                }
        current.append(reported)
    return tuple(current)


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
        "current": {s["entity"]: s["authorized"] for s in current_states(root)},
        "unstated": {s.entity: s.unstated_dimensions for s in states},
        "issuance_contradiction": issuance_contradiction(root) is not None,
    }


def main(argv=None) -> int:
    import json
    print(json.dumps(summary(), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
