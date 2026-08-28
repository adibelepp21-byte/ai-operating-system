"""Governance Record Index — a read-only discovery aid over governance records.

Authorized by ``ACT-CC-P6-066-R2``. The index accelerates discovery; the
canonical record retains authority. Nothing produced here is authority:

    INDEX != AUTHORITY          INDEX != CANONICAL SOURCE
    INDEX != GOVERNANCE DECISION    CHRONOLOGY != SUPERSESSION
    RETRIEVAL != AUTHORIZATION

The module reads Markdown governance records, extracts only what the source
states literally, and writes a JSON index that points back at the source. It
never rewrites a source record, never infers a missing field, and never derives
supersession from dates. A field the source does not state is reported as
``ABSENT`` -- never filled in.

Two extraction rules carry the whole design:

*Metadata is read only from the record's own metadata block* -- the lines
before the first horizontal rule. Governance records in this repository open
with bold-label lines (``**Authority:** Founder``) or bold-label list items
(``- **Status:** Approved``); prose further down the document is evidence a
reader must weigh, not metadata a parser may harvest. Reading labels from the
body would let a sentence such as "Item 1 ... EXPLICITLY SUPERSEDED by
T12-D-002" -- which supersedes an item inside a record, not the record --
silently become a supersession edge.

*Identifiers found in the body are recorded as mentions, not as claims.* A
mention says only "this token appears in this file". It is the retrieval
primitive: it makes "which records speak about X?" cheap without asserting
anything about what they say.

Usage::

    python -m tools.governance_index stats
    python -m tools.governance_index about DEC-PHASE5-SEMANTICS
    python -m tools.governance_index supersession GDR-0028
    python -m tools.governance_index since 2026-08-20
    python -m tools.governance_index --index /tmp/gi.json build

Queries build the index in memory unless ``--index`` names a saved one; a saved
index that no longer matches its sources says so on stderr before answering.
The index file itself is a generated artifact and is deliberately not tracked --
the repository's stated convention is that every tracked file is an authored
artifact -- so ``build`` has no default output path.

Dependencies: Python standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Value recorded when the source does not state a field. Never a default.
ABSENT = "ABSENT"

#: Value recorded when a relationship could not be established from evidence.
UNKNOWN = "UNKNOWN"

SCHEMA_VERSION = 1

# --------------------------------------------------------------------------
# Identifier classes
# --------------------------------------------------------------------------

# ACT-CC-P6-066-R2 §9 names DEC-*, GDR-*, ACT-*, ADR-* explicitly and invites
# "other governance identifiers discovered in the repository". The topic classes
# below were added because §25 Query D asks for records mentioning T-12. Each
# segment must open with a digit or capital so that a filename such as
# "ACT-CC-F03-014.md" does not absorb its own extension.
_SEGMENT = r"[A-Z0-9][A-Za-z0-9]*"
IDENTIFIER_RE = re.compile(r"\b(?:DEC|GDR|ADR|ACT)-" + _SEGMENT + r"(?:[.-]" + _SEGMENT + r")*")
TOPIC_RE = re.compile(r"\bT-\d+\b|\bT\d+-[A-Z]-\d+\b")

#: Identifier prefixes recognized as governance record classes.
IDENTIFIER_CLASSES = ("DEC", "GDR", "ACT", "ADR")


def identifiers_in(text: str) -> Tuple[str, ...]:
    """Return every governance identifier literally present in ``text``.

    Order of first appearance, de-duplicated. This is an evidence primitive:
    it reports tokens, and claims nothing about what the text says about them.
    """
    seen: Dict[str, None] = {}
    for match in IDENTIFIER_RE.finditer(text):
        seen.setdefault(match.group(0), None)
    for match in TOPIC_RE.finditer(text):
        seen.setdefault(match.group(0), None)
    return tuple(seen)


# --------------------------------------------------------------------------
# Metadata extraction
# --------------------------------------------------------------------------

# "**Label:** value", "- **Label:** value", "**Label**: value". Records in this
# repository also put several labels on one line, separated by a middle dot:
#
#     **Prepared under:** FOUNDER · `ACT-CC-F03-038 §6` · **Date:** 2026-08-21
#
# so labels are matched as occurrences rather than as whole lines, and a value
# runs from its label to the next label on that line or to the line's end. An
# earlier line-anchored version of this parser silently reported ABSENT for
# every date and status stated this way.
# The colon is required. Without it a bold *value* -- records write
# "**Status:** **AUTHORIZED**" -- reads as the next label, leaving the real
# label with an empty value and inventing a label named AUTHORIZED.
_LABEL_RE = re.compile(r"\*\*(?P<label>[^*\n]+?)\s*(?::\s*\*\*|\*\*\s*:)\s*")

#: Trailing separators left behind when a value is cut at the next label.
_VALUE_TRIM = " \t·-—–,;|"


def _unwrap(value: str) -> str:
    """Remove emphasis that wraps a whole value, keeping the words verbatim.

    "**AUTHORIZED**" is the word AUTHORIZED in bold, not a different status.
    The wrapper is removed only when nothing inside it is emphasized too:
    "**Approved** ... **COMPLETE**" opens and closes with the same marks but
    they belong to two spans, and stripping them would corrupt the value.
    """
    text = value.strip()
    while len(text) > 4 and text.startswith("**") and text.endswith("**") \
            and "**" not in text[2:-2]:
        text = text[2:-2].strip()
    while len(text) > 2 and text.startswith("`") and text.endswith("`") \
            and "`" not in text[1:-1]:
        text = text[1:-1].strip()
    return text

_H1_RE = re.compile(r"^#\s+(?P<title>.+?)\s*$")

# A sub-record heading: "### GDR-0028 — Founder Decision · ...". Recognized only
# where a file carries two or more of them, so that a single such heading inside
# a narrative document is not mistaken for a record boundary.
_SUBRECORD_RE = re.compile(
    r"^(?P<hashes>#{2,4})\s+(?P<identifier>(?:DEC|GDR|ACT|ADR)-" + _SEGMENT
    + r"(?:[.-]" + _SEGMENT + r")*)\s*(?P<sep>[-—–:·])"
)

_RULE_RE = re.compile(r"^\s*(?:---+|___+|\*\*\*+)\s*$")

#: How far into a record to look for the metadata block when it has no rule.
METADATA_FALLBACK_LINES = 40


def _metadata_lines(lines: Sequence[str]) -> List[str]:
    """Return the record's metadata block: everything before the first rule."""
    for position, line in enumerate(lines):
        if _RULE_RE.match(line):
            return list(lines[:position])
    return list(lines[:METADATA_FALLBACK_LINES])


def _labels(lines: Iterable[str]) -> Dict[str, str]:
    """Return ``{label: value}`` for every bold-label line, verbatim values.

    A repeated label keeps its first value; the source stated that one first and
    the parser has no basis to prefer another.
    """
    found: Dict[str, str] = {}
    for line in lines:
        matches = list(_LABEL_RE.finditer(line))
        for position, match in enumerate(matches):
            label = " ".join(match.group("label").split())
            end = matches[position + 1].start() if position + 1 < len(matches) else len(line)
            value = _unwrap(line[match.end():end].strip().strip(_VALUE_TRIM))
            if not label or not value:
                continue
            found.setdefault(label, value)
    return found


def _title(lines: Sequence[str]) -> str:
    for line in lines:
        match = _H1_RE.match(line)
        if match is not None:
            return match.group("title")
    return ABSENT


# --------------------------------------------------------------------------
# Field projection
# --------------------------------------------------------------------------

# Each indexed field is projected from an explicit list of source labels, in
# order. No field is ever derived from a file's path, its name, its position in
# the corpus, or its commit metadata -- §12 forbids exactly that.
FIELD_LABELS: Mapping[str, Tuple[str, ...]] = {
    "identifier": ("Identifier", "Act ID", "Decision ID", "Record ID", "ADR ID"),
    "record_type": ("Type", "Record Type", "Decision Type", "Instrument Type"),
    "date": ("Date", "Date recorded", "Date Recorded", "Date issued", "Date Issued"),
    "status": ("Status",),
    "authority": ("Authority", "Execution Authority", "Decision Authority", "Ratification Authority"),
    "issuer": ("Decided by", "Decided By", "Issued by", "Issued By", "Decision Owner"),
    "program_phase": ("Phase", "Program Phase", "Master Roadmap Context"),
    "related_act": ("Authorizing act", "Authorizing Act", "Related Act", "Authorizing Instrument"),
    "related_adr": ("Related ADR", "ADR", "Resulting ADR"),
    "supersedes": ("Supersedes", "Supersedes Decision", "Replaces"),
    "superseded_by": ("Superseded by", "Superseded By", "Superseded"),
    "decision_state": ("Decision", "Decision State", "Determination", "Ratification Authorization"),
}

#: Fields whose value is a list of identifiers extracted from the label value.
_IDENTIFIER_FIELDS = ("related_act", "related_adr", "supersedes", "superseded_by")

#: Labels that are date-bearing, kept separately so that §11's distinction
#: between a record date, an execution date and a reference date survives.
_DATE_LABEL_RE = re.compile(r"\bdate\b", re.IGNORECASE)

#: Labels that make an authority claim. Kept in full, with their source wording,
#: because §12 permits recording authority only as the source states it -- and a
#: record often states several ("Authority", "Execution Authority",
#: "Construction Authority: NONE"). Collapsing them to one field would lose the
#: distinction that matters most: what a record does *not* claim.
_AUTHORITY_LABEL_RE = re.compile(r"authority|delegation", re.IGNORECASE)


def _project(labels: Mapping[str, str], field_name: str) -> str:
    for label in FIELD_LABELS[field_name]:
        if label in labels:
            return labels[label]
    return ABSENT


def _normalize_identifier(value: str) -> str:
    """Strip Markdown code formatting from an identifier value.

    Records write the same identifier as ``DEC-P6-042`` or as `` `DEC-P6-042` ``.
    The backticks are presentation, not part of the identifier, and §6 permits
    normalizing metadata. Only the identifier field is normalized; every other
    value is kept in the source's own wording, as §13 requires.
    """
    return value.strip().strip("`*").strip()


def _project_identifiers(labels: Mapping[str, str], field_name: str) -> List[str]:
    for label in FIELD_LABELS[field_name]:
        if label in labels:
            return list(identifiers_in(labels[label]))
    return []


# --------------------------------------------------------------------------
# Records
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Record:
    """One governance record, as the source states it.

    ``source_path`` and ``source_hash`` together answer "where did this come
    from, and is it still the text I read?". They are provenance, never
    authority: a hash proves a file has not changed, not that its contents were
    approved.
    """

    identifier: str
    record_type: str
    title: str
    date: str
    status: str
    authority: str
    issuer: str
    program_phase: str
    related_act: Tuple[str, ...]
    related_adr: Tuple[str, ...]
    supersedes: Tuple[str, ...]
    superseded_by: Tuple[str, ...]
    decision_state: str
    source_path: str
    source_hash: str
    source_line: int
    title_identifiers: Tuple[str, ...] = ()
    mentions: Tuple[str, ...] = ()
    dates: Tuple[Tuple[str, str], ...] = ()
    authority_labels: Tuple[Tuple[str, str], ...] = ()

    def as_json(self) -> Dict[str, object]:
        data: Dict[str, object] = {}
        for name in (
            "identifier", "record_type", "title", "date", "status", "authority",
            "issuer", "program_phase", "decision_state", "source_path",
            "source_hash", "source_line",
        ):
            data[name] = getattr(self, name)
        for name in ("related_act", "related_adr", "supersedes", "superseded_by",
                     "title_identifiers", "mentions"):
            data[name] = list(getattr(self, name))
        data["dates"] = {label: value for label, value in self.dates}
        data["authority_labels"] = {label: value for label, value in self.authority_labels}
        return data

    @classmethod
    def from_json(cls, data: Mapping[str, object]) -> "Record":
        return cls(
            identifier=str(data["identifier"]),
            record_type=str(data["record_type"]),
            title=str(data["title"]),
            date=str(data["date"]),
            status=str(data["status"]),
            authority=str(data["authority"]),
            issuer=str(data["issuer"]),
            program_phase=str(data["program_phase"]),
            related_act=tuple(data.get("related_act", ())),  # type: ignore[arg-type]
            related_adr=tuple(data.get("related_adr", ())),  # type: ignore[arg-type]
            supersedes=tuple(data.get("supersedes", ())),  # type: ignore[arg-type]
            superseded_by=tuple(data.get("superseded_by", ())),  # type: ignore[arg-type]
            decision_state=str(data["decision_state"]),
            source_path=str(data["source_path"]),
            source_hash=str(data["source_hash"]),
            source_line=int(data["source_line"]),  # type: ignore[arg-type]
            title_identifiers=tuple(data.get("title_identifiers", ())),  # type: ignore[arg-type]
            mentions=tuple(data.get("mentions", ())),  # type: ignore[arg-type]
            dates=tuple(sorted((dict(data.get("dates", {}))).items())),  # type: ignore[arg-type]
            authority_labels=tuple(sorted((dict(data.get("authority_labels", {}))).items())),  # type: ignore[arg-type]
        )


_ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _recency(record: "Record") -> str:
    """Sort key: the record's stated ISO date, or the empty string.

    Ordering by this key surfaces chronology, which is what a reader needs in
    order to notice that a newer record exists. It establishes nothing about
    supersession: the newest record in a result set may be unrelated,
    supplementary or merely observational, and the index says so nowhere else.
    """
    match = _ISO_DATE_RE.search(record.date)
    return match.group(0) if match is not None else ""


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _build_record(
    *,
    lines: Sequence[str],
    body: str,
    source_path: str,
    source_hash: str,
    source_line: int,
    title_override: Optional[str] = None,
) -> Record:
    metadata = _metadata_lines(lines)
    labels = _labels(metadata)
    title = title_override if title_override is not None else _title(metadata)
    dates = {label: value for label, value in labels.items() if _DATE_LABEL_RE.search(label)}
    claims = {label: value for label, value in labels.items() if _AUTHORITY_LABEL_RE.search(label)}
    return Record(
        identifier=_normalize_identifier(_project(labels, "identifier")),
        record_type=_project(labels, "record_type"),
        title=title,
        date=_project(labels, "date"),
        status=_project(labels, "status"),
        authority=_project(labels, "authority"),
        issuer=_project(labels, "issuer"),
        program_phase=_project(labels, "program_phase"),
        related_act=tuple(_project_identifiers(labels, "related_act")),
        related_adr=tuple(_project_identifiers(labels, "related_adr")),
        supersedes=tuple(_project_identifiers(labels, "supersedes")),
        superseded_by=tuple(_project_identifiers(labels, "superseded_by")),
        decision_state=_project(labels, "decision_state"),
        source_path=source_path,
        source_hash=source_hash,
        source_line=source_line,
        title_identifiers=identifiers_in(title) if title != ABSENT else (),
        mentions=identifiers_in(body),
        dates=tuple(sorted(dates.items())),
        authority_labels=tuple(sorted(claims.items())),
    )


def _subrecord_spans(lines: Sequence[str]) -> List[Tuple[int, int, str, str]]:
    """Return ``(start, end, identifier, heading)`` for each sub-record.

    A register file states many Decisions under one path. Sub-records are
    recognized only where a file carries two or more identifier headings at the
    same depth, so that one such heading inside a narrative document does not
    fragment it.
    """
    matches: List[Tuple[int, str, str, str]] = []
    for position, line in enumerate(lines):
        match = _SUBRECORD_RE.match(line)
        if match is not None:
            matches.append((position, match.group("hashes"), match.group("identifier"), line.strip()))
    if len(matches) < 2:
        return []
    depth = matches[0][1]
    at_depth = [entry for entry in matches if entry[1] == depth]
    if len(at_depth) < 2:
        return []
    spans: List[Tuple[int, int, str, str]] = []
    for index, (start, _, identifier, heading) in enumerate(at_depth):
        end = at_depth[index + 1][0] if index + 1 < len(at_depth) else len(lines)
        spans.append((start, end, identifier, heading))
    return spans


def is_governance_record(text: str) -> bool:
    """Classify by evidence: does the record's own metadata block say so?

    A Markdown file qualifies when its metadata block either names a governance
    identifier or carries a recognized governance metadata label. Location and
    filename are deliberately not consulted -- a document is a governance record
    because of what it states, not where it sits.
    """
    lines = text.splitlines()
    metadata = _metadata_lines(lines)
    blob = "\n".join(metadata)
    if identifiers_in(blob):
        return True
    labels = _labels(metadata)
    known = {label for names in FIELD_LABELS.values() for label in names}
    return bool(known & set(labels))


def parse_source(path: Path, root: Path) -> List[Record]:
    """Parse one Markdown file into zero or more records. Reads only."""
    text = path.read_text(encoding="utf-8")
    if not is_governance_record(text):
        return []
    lines = text.splitlines()
    source_path = path.resolve().relative_to(root.resolve()).as_posix()
    source_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    spans = _subrecord_spans(lines)
    if not spans:
        return [_build_record(
            lines=lines, body=text, source_path=source_path,
            source_hash=source_hash, source_line=1,
        )]
    records = [_build_record(
        lines=lines, body=text, source_path=source_path,
        source_hash=source_hash, source_line=1,
    )]
    for start, end, identifier, heading in spans:
        section = lines[start:end]
        record = _build_record(
            lines=section[1:], body="\n".join(section), source_path=source_path,
            source_hash=source_hash, source_line=start + 1,
            title_override=heading.lstrip("#").strip(),
        )
        if record.identifier == ABSENT:
            record = replace(record, identifier=identifier)
        records.append(record)
    return records


# --------------------------------------------------------------------------
# Index
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class BuildStats:
    """What the last build actually did, so incremental behaviour is visible."""

    parsed: int = 0
    reused: int = 0
    removed: int = 0

    @property
    def total(self) -> int:
        return self.parsed + self.reused


class GovernanceIndex:
    """A read-only lookup over parsed governance records.

    Every query returns records -- that is, pointers at canonical sources. None
    returns a verdict. ``superseded_by`` reports what a record states about
    itself, and ``UNKNOWN`` where the source states nothing; it never reads a
    later date as a supersession.
    """

    def __init__(self, records: Sequence[Record], sources: Mapping[str, str]) -> None:
        self._records = tuple(records)
        self._sources = dict(sources)

    # -- construction ------------------------------------------------------

    @classmethod
    def build(
        cls,
        paths: Iterable[Path],
        root: Path,
        previous: Optional["GovernanceIndex"] = None,
    ) -> Tuple["GovernanceIndex", BuildStats]:
        """Parse ``paths``, reusing unchanged entries from ``previous``.

        A source is unchanged when its path and its SHA-256 both match. That is
        the whole staleness rule: the hash detects that a source moved on, so a
        reused entry is one the index has positively shown to be current.
        """
        by_path: Dict[str, List[Record]] = {}
        if previous is not None:
            for record in previous.records:
                by_path.setdefault(record.source_path, []).append(record)
        records: List[Record] = []
        sources: Dict[str, str] = {}
        parsed = reused = 0
        for path in sorted(paths):
            relative = path.resolve().relative_to(root.resolve()).as_posix()
            digest = sha256_of(path)
            cached = by_path.get(relative)
            if cached is not None and previous is not None and previous.source_hash(relative) == digest:
                records.extend(cached)
                sources[relative] = digest
                reused += 1
                continue
            found = parse_source(path, root)
            parsed += 1
            if found:
                records.extend(found)
                sources[relative] = digest
        removed = 0
        if previous is not None:
            removed = len([name for name in previous.sources if name not in sources])
        return cls(records, sources), BuildStats(parsed=parsed, reused=reused, removed=removed)

    # -- state -------------------------------------------------------------

    @property
    def records(self) -> Tuple[Record, ...]:
        return self._records

    @property
    def sources(self) -> Mapping[str, str]:
        return dict(self._sources)

    def source_hash(self, source_path: str) -> str:
        return self._sources.get(source_path, ABSENT)

    def stale_sources(self, root: Path) -> Tuple[str, ...]:
        """Sources whose file no longer matches the hash recorded at build."""
        stale: List[str] = []
        for relative, digest in sorted(self._sources.items()):
            path = root / relative
            if not path.exists() or sha256_of(path) != digest:
                stale.append(relative)
        return tuple(stale)

    # -- queries -----------------------------------------------------------

    def by_identifier(self, identifier: str) -> Tuple[Record, ...]:
        """Records that *are* ``identifier``."""
        return tuple(r for r in self._records if r.identifier == identifier)

    def about(self, identifier: str) -> Tuple[Record, ...]:
        """Records that are, title, or mention ``identifier``.

        Queries A, D and I. The result is where to read, ordered by how directly
        each record engages the identifier: the record itself first, then records
        naming it in their title, then records mentioning it in the body.
        """
        rank: Dict[int, List[Record]] = {0: [], 1: [], 2: []}
        for record in self._records:
            if record.identifier == identifier:
                rank[0].append(record)
            elif identifier in record.title_identifiers:
                rank[1].append(record)
            elif identifier in record.mentions:
                rank[2].append(record)
        ordered: List[Record] = []
        for tier in (0, 1, 2):
            ordered.extend(sorted(rank[tier], key=_recency, reverse=True))
        return tuple(ordered)

    def supersession(self, identifier: str) -> Dict[str, object]:
        """What the corpus *states* about the supersession of ``identifier``.

        Queries B and F. ``superseded_by`` is populated only from a record's own
        ``Superseded by`` metadata, or from another record's ``Supersedes``
        metadata naming it. Where neither exists the answer is ``UNKNOWN`` --
        which means "no evidence found", not "not superseded".
        """
        declared: List[Dict[str, str]] = []
        for record in self._records:
            if record.identifier == identifier:
                for other in record.superseded_by:
                    declared.append({"by": other, "evidence": "self-declared",
                                     "source_path": record.source_path,
                                     "source_line": str(record.source_line)})
            if identifier in record.supersedes:
                declared.append({"by": record.identifier, "evidence": "declared-by-successor",
                                 "source_path": record.source_path,
                                 "source_line": str(record.source_line)})
        return {
            "identifier": identifier,
            "superseded_by": declared or UNKNOWN,
            "note": "Absence of evidence is not evidence of currency; read the canonical source.",
        }

    def by_phase(self, phase: str) -> Tuple[Record, ...]:
        """Query C. Matches the stated ``program_phase`` text only."""
        needle = phase.casefold()
        return tuple(r for r in self._records if needle in r.program_phase.casefold())

    def search(self, text: str) -> Tuple[Record, ...]:
        """Query E. Substring match over stated title and identifier."""
        needle = text.casefold()
        return tuple(
            r for r in self._records
            if needle in r.title.casefold() or needle in r.identifier.casefold()
        )

    def since(self, date: str) -> Tuple[Record, ...]:
        """Query J. Records whose stated ISO date sorts at or after ``date``.

        Only records stating an ISO-8601 date participate. A record with no
        stated date is not silently placed on a timeline.
        """
        iso = re.compile(r"\d{4}-\d{2}-\d{2}")
        selected: List[Tuple[str, Record]] = []
        for record in self._records:
            match = iso.search(record.date)
            if match is not None and match.group(0) >= date:
                selected.append((match.group(0), record))
        selected.sort(key=lambda pair: pair[0])
        return tuple(record for _, record in selected)

    # -- serialization -----------------------------------------------------

    def to_json(self) -> Dict[str, object]:
        return {
            "schema_version": SCHEMA_VERSION,
            "authority": "NONE — discovery aid only; canonical records remain authoritative.",
            "sources": dict(sorted(self._sources.items())),
            "records": [record.as_json() for record in self._records],
        }

    @classmethod
    def from_json(cls, data: Mapping[str, object]) -> "GovernanceIndex":
        records = [Record.from_json(entry) for entry in data.get("records", [])]  # type: ignore[union-attr]
        return cls(records, dict(data.get("sources", {})))  # type: ignore[arg-type]

    def write(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_json(), indent=2, sort_keys=False) + "\n", encoding="utf-8")

    @classmethod
    def read(cls, path: Path) -> "GovernanceIndex":
        return cls.from_json(json.loads(path.read_text(encoding="utf-8")))


# --------------------------------------------------------------------------
# Corpus discovery
# --------------------------------------------------------------------------


def tracked_markdown(root: Path = REPO_ROOT, subdir: str = "docs") -> List[Path]:
    """Return tracked Markdown files under ``subdir``.

    Tracked, not merely present: ACT-CC-P6-066-R2 §7 scopes the corpus to
    "tracked location[s]", and reading the tracked set is also what keeps
    untracked working-tree material -- the thirteen protected packages among it
    -- outside this tool's reach entirely. If git cannot answer, this fails
    rather than falling back to a directory walk that would sweep them in.
    """
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--", subdir],
        capture_output=True, check=True,
    )
    names = [name for name in result.stdout.decode("utf-8").split("\0") if name]
    return [root / name for name in names if name.endswith(".md")]


# --------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------


def _print_records(records: Sequence[Record], stream) -> None:
    if not records:
        print("(no records)", file=stream)
        return
    for record in records:
        identity = record.identifier if record.identifier != ABSENT else f"({record.title})"
        print(f"{identity}  [{record.date}]  {record.status}", file=stream)
        print(f"    authority : {record.authority}", file=stream)
        print(f"    source    : {record.source_path}:{record.source_line}", file=stream)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="governance_index",
        description="Build and query the governance record index. The index is a "
                    "discovery aid; canonical records remain authoritative.",
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--index", type=Path, default=None,
                        help="Index file to read or write. Required for build; "
                             "queries build in memory when omitted.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="write the index (requires --index)")
    sub.add_parser("stats", help="report corpus and index size")
    for name, help_text in (
        ("about", "records that are, title, or mention an identifier"),
        ("supersession", "what the corpus states about supersession"),
        ("phase", "records stating a program phase"),
        ("search", "substring match over stated title and identifier"),
        ("since", "records stating an ISO date at or after a value"),
    ):
        child = sub.add_parser(name, help=help_text)
        child.add_argument("value")
    args = parser.parse_args(argv)

    if args.command == "build":
        if args.index is None:
            parser.error("build requires --index")
        previous = GovernanceIndex.read(args.index) if args.index.exists() else None
        index, stats = GovernanceIndex.build(tracked_markdown(args.root), args.root, previous)
        index.write(args.index)
        print(f"records={len(index.records)} sources={len(index.sources)} "
              f"parsed={stats.parsed} reused={stats.reused} removed={stats.removed}")
        return 0

    if args.index is not None and args.index.exists():
        index = GovernanceIndex.read(args.index)
        stale = index.stale_sources(args.root)
        if stale:
            print(f"WARNING: {len(stale)} source(s) changed since the index was built; "
                  f"rebuild before relying on it.", file=sys.stderr)
    else:
        index, _ = GovernanceIndex.build(tracked_markdown(args.root), args.root)

    if args.command == "stats":
        payload = json.dumps(index.to_json(), indent=2)
        print(f"records          : {len(index.records)}")
        print(f"sources          : {len(index.sources)}")
        print(f"index bytes      : {len(payload.encode('utf-8'))}")
        return 0
    if args.command == "about":
        _print_records(index.about(args.value), sys.stdout)
    elif args.command == "supersession":
        print(json.dumps(index.supersession(args.value), indent=2))
    elif args.command == "phase":
        _print_records(index.by_phase(args.value), sys.stdout)
    elif args.command == "search":
        _print_records(index.search(args.value), sys.stdout)
    elif args.command == "since":
        _print_records(index.since(args.value), sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
