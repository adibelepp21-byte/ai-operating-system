"""
Evidence for the governance record index (ACT-CC-P6-066-R2).

Scope A — parsing: what the source states, and only that.
Scope B — negative authority: what the index must refuse to conclude.
Scope C — source fidelity against the live corpus, read-only.
Scope D — the two known retrieval failures (§26).
Scope E — chronology, supersession, and the difference between them.
Scope F — incremental rebuild.
Scope G — boundaries: dependencies, location, protected state.

Every test that touches the real corpus reads it. None writes to it; Scope C
closes with a hash comparison proving the corpus is byte-identical afterwards.
"""

import ast
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import governance_index as gi
from tools.governance_index import (
    ABSENT,
    UNKNOWN,
    GovernanceIndex,
    Record,
    identifiers_in,
    is_governance_record,
    parse_source,
    sha256_of,
    tracked_markdown,
)

REPO_ROOT = gi.REPO_ROOT
MODULE_PATH = Path(gi.__file__).resolve()


def _write(root: Path, name: str, text: str) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class _Corpus(unittest.TestCase):
    """Builds the live index once; every subclass reads the same object."""

    index: GovernanceIndex

    @classmethod
    def setUpClass(cls) -> None:
        cls.index, _ = GovernanceIndex.build(tracked_markdown(REPO_ROOT), REPO_ROOT)


# ---------------------------------------------------------------- Scope A


class ParsingReadsOnlyWhatIsStated(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_several_labels_on_one_line_are_all_read(self):
        path = _write(self.root, "r.md", (
            "# Frontier\n\n"
            "**Prepared under:** FOUNDER · `ACT-CC-F03-038 §6` · **Date:** 2026-08-21\n"
            "\n---\n\nbody\n"
        ))
        record, = parse_source(path, self.root)
        self.assertEqual("2026-08-21", record.date)

    def test_a_bold_value_is_not_read_as_another_label(self):
        path = _write(self.root, "r.md", (
            "# D\n\n**Identifier:** `DEC-X-001`\n**Status:** **AUTHORIZED**\n\n---\n\nbody\n"
        ))
        record, = parse_source(path, self.root)
        self.assertEqual("AUTHORIZED", record.status)
        self.assertEqual("DEC-X-001", record.identifier)

    def test_emphasis_spanning_two_phrases_is_preserved_verbatim(self):
        path = _write(self.root, "r.md", (
            "# A\n\n- **Status:** **Approved** · Act **COMPLETE**\n\n---\n\nbody\n"
        ))
        record, = parse_source(path, self.root)
        self.assertEqual("**Approved** · Act **COMPLETE**", record.status)

    def test_metadata_is_read_only_before_the_first_rule(self):
        path = _write(self.root, "r.md", (
            "# A\n\n**Date:** 2026-01-01\n\n---\n\n**Status:** APPROVED\n"
        ))
        record, = parse_source(path, self.root)
        self.assertEqual("2026-01-01", record.date)
        self.assertEqual(ABSENT, record.status, "a status stated in prose is not metadata")

    def test_an_absent_field_stays_absent(self):
        path = _write(self.root, "r.md", "# A\n\n**Identifier:** DEC-X-002\n\n---\n\nbody\n")
        record, = parse_source(path, self.root)
        for value in (record.status, record.authority, record.date, record.decision_state):
            self.assertEqual(ABSENT, value)

    def test_a_file_stating_no_governance_evidence_is_not_a_record(self):
        path = _write(self.root, "r.md", "# Notes\n\nSome prose about nothing in particular.\n")
        self.assertFalse(is_governance_record(path.read_text(encoding="utf-8")))
        self.assertEqual([], parse_source(path, self.root))

    def test_one_identifier_heading_does_not_split_a_narrative_record(self):
        path = _write(self.root, "r.md", (
            "# Report\n\n**Date:** 2026-01-01\n\n---\n\n### DEC-X-003 — mentioned once\n\nprose\n"
        ))
        self.assertEqual(1, len(parse_source(path, self.root)))

    def test_two_identifier_headings_yield_one_record_each(self):
        path = _write(self.root, "reg.md", (
            "# Register\n\n**Status:** Append-only\n\n---\n\n"
            "### GDR-0001 — first\n\n**Date:** 2026-01-01\n\n"
            "### GDR-0002 — second\n\n**Date:** 2026-02-02\n"
        ))
        records = parse_source(path, self.root)
        self.assertEqual(3, len(records), "the file itself, plus one record per section")
        identifiers = [r.identifier for r in records]
        self.assertIn("GDR-0001", identifiers)
        self.assertIn("GDR-0002", identifiers)
        section = next(r for r in records if r.identifier == "GDR-0002")
        self.assertEqual("2026-02-02", section.date)
        self.assertGreater(section.source_line, 1, "a section points at its own line")

    def test_identifier_extraction_stops_at_a_file_extension(self):
        self.assertEqual(("ACT-CC-F03-014",), identifiers_in("see ACT-CC-F03-014.md"))

    def test_topic_identifiers_are_recognized(self):
        self.assertEqual(("T-12", "T12-D-004"), identifiers_in("T-12 and T12-D-004"))


# ---------------------------------------------------------------- Scope B


class TheIndexRefusesToConclude(_Corpus):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_it_does_not_invent_a_decision(self):
        indexed = {r.identifier for r in self.index.records if r.identifier != ABSENT}
        self.assertGreater(len(indexed), 50)
        for identifier in indexed:
            record = self.index.by_identifier(identifier)[0]
            source = (REPO_ROOT / record.source_path).read_text(encoding="utf-8")
            self.assertIn(identifier, source, f"{identifier} is not present in its own source")

    def test_it_does_not_invent_authority(self):
        for record in self.index.records:
            if record.authority == ABSENT:
                continue
            source = (REPO_ROOT / record.source_path).read_text(encoding="utf-8")
            self.assertIn(record.authority.split("\n")[0][:40], source)

    def test_it_does_not_infer_approval(self):
        path = _write(self.root, "r.md", (
            "# A\n\n**Identifier:** DEC-X-004\n**Authority:** Founder\n\n---\n\n"
            "The Founder approved this in conversation.\n"
        ))
        record, = parse_source(path, self.root)
        self.assertEqual(ABSENT, record.status)
        self.assertEqual(ABSENT, record.decision_state)

    def test_it_does_not_infer_supersession_from_date_alone(self):
        _write(self.root, "old.md", "# Old\n\n**Identifier:** DEC-X-005\n**Date:** 2026-01-01\n\n---\n\nx\n")
        _write(self.root, "new.md", "# New\n\n**Identifier:** DEC-X-006\n**Date:** 2026-09-09\n\n---\n\nx\n")
        index, _ = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root)
        self.assertEqual(UNKNOWN, index.supersession("DEC-X-005")["superseded_by"])

    def test_supersession_prose_inside_a_record_is_not_a_supersession_edge(self):
        # The wording is GDR-0028's, where the superseded thing is an item
        # inside the record -- not the record itself.
        _write(self.root, "r.md", (
            "# G\n\n**Identifier:** GDR-9999\n**Date:** 2026-08-22\n\n---\n\n"
            "> - Item 1 — Versioned Repository Discipline: EXPLICITLY SUPERSEDED by T12-D-002\n"
        ))
        index, _ = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root)
        self.assertEqual(UNKNOWN, index.supersession("GDR-9999")["superseded_by"])
        record, = index.by_identifier("GDR-9999")
        self.assertEqual((), record.superseded_by)

    def test_it_does_not_modify_source_records(self):
        path = _write(self.root, "r.md", "# A\n\n**Identifier:** DEC-X-007\n\n---\n\nbody\n")
        before = sha256_of(path)
        GovernanceIndex.build([path], self.root)
        self.assertEqual(before, sha256_of(path))

    def test_an_act_referencing_a_decision_is_not_that_decision(self):
        path = _write(self.root, "act.md", (
            "# ACT-CC-X-001 — an Act\n\n**Act ID:** ACT-CC-X-001\n\n---\n\n"
            "This Act consumes DEC-X-008 and executes under it.\n"
        ))
        record, = parse_source(path, self.root)
        self.assertEqual("ACT-CC-X-001", record.identifier)
        self.assertIn("DEC-X-008", record.mentions)
        index = GovernanceIndex([record], {record.source_path: "x"})
        self.assertEqual((), index.by_identifier("DEC-X-008"),
                         "mentioning a Decision does not make a record be it")

    def test_an_adr_claims_no_authority_unless_it_says_so(self):
        adrs = [r for r in self.index.records if r.source_path.startswith("docs/architecture/adr/")]
        self.assertTrue(adrs)
        for record in adrs:
            if record.authority == ABSENT:
                continue
            source = (REPO_ROOT / record.source_path).read_text(encoding="utf-8")
            self.assertIn("Authority", source)

    def test_the_index_declares_that_it_carries_no_authority(self):
        self.assertIn("NONE", str(self.index.to_json()["authority"]))


# ---------------------------------------------------------------- Scope C


class SourceFidelity(_Corpus):
    def test_every_indexed_hash_matches_the_file_on_disk(self):
        for source_path, digest in self.index.sources.items():
            self.assertEqual(digest, sha256_of(REPO_ROOT / source_path), source_path)

    def test_every_stated_field_is_present_in_its_source(self):
        checked = 0
        for record in self.index.records:
            source = (REPO_ROOT / record.source_path).read_text(encoding="utf-8")
            for value in (record.date, record.status, record.authority, record.issuer):
                if value == ABSENT:
                    continue
                self.assertIn(value.split(" (")[0][:30], source,
                              f"{record.source_path}: {value!r} is not in the source")
                checked += 1
        self.assertGreater(checked, 100, "the corpus should exercise this broadly")

    def test_every_record_points_at_a_line_that_exists(self):
        for record in self.index.records:
            lines = (REPO_ROOT / record.source_path).read_text(encoding="utf-8").splitlines()
            self.assertGreaterEqual(record.source_line, 1)
            self.assertLessEqual(record.source_line, len(lines), record.source_path)

    def test_a_section_record_points_at_its_own_heading(self):
        register = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        lines = (REPO_ROOT / register).read_text(encoding="utf-8").splitlines()
        sections = [r for r in self.index.records
                    if r.source_path == register and r.source_line > 1]
        self.assertGreater(len(sections), 1)
        for record in sections:
            self.assertIn(record.identifier, lines[record.source_line - 1])

    def test_the_corpus_is_byte_identical_after_every_read(self):
        for path in tracked_markdown(REPO_ROOT):
            relative = path.relative_to(REPO_ROOT).as_posix()
            if relative in self.index.sources:
                self.assertEqual(self.index.sources[relative], sha256_of(path))


# ---------------------------------------------------------------- Scope D


#: The record carrying the *decided* reading of DEC-PHASE5-SEMANTICS — the one
#: ACT-CC-P6-060 needed and missed. Named here because its identity is the
#: property under test; the records that happen to surround it in the corpus at
#: any moment are not.
DECIDED_READING = "docs/program/AIOS_CONSTRUCTION_FRONTIER_v1.0.md"
DECIDED_READING_DATE = "2026-08-21"


class KnownRetrievalFailures(_Corpus):
    """ACT-CC-P6-060 missed DEC-PHASE5-SEMANTICS; ACT-CC-P6-061 missed GDR-0028.

    Neither Act is touched here. The question these tests answer is only the one
    §26 poses: would the index have made the newer record easy to find?

    **These assertions are corpus-relative by construction, and were tightened
    under `ACT-CC-P1-6-077` after they fired.** They originally pinned the
    *newest* mention by literal date and the record at position 0 by literal
    path. Adding a newer governance record that cites this decision — which
    `ACT-CC-P1-6-076`'s closure record legitimately does — made both constants
    stale while the index remained correct. The behaviour the tests exist to
    protect is chronological surfacing and the continued findability of the
    decided reading, so that is what they now assert, in a form that survives
    the corpus growing. Nothing was relaxed: the ordering guarantees below are
    strictly stronger than the two constants they replace.
    """

    def test_dec_phase5_semantics_surfaces_its_records_newest_first(self):
        found = self.index.about("DEC-PHASE5-SEMANTICS")
        self.assertGreaterEqual(len(found), 5)
        paths = [r.source_path for r in found]
        self.assertIn("docs/program/AIOS_CONSTRUCTION_FRONTIER_v1.0.md", paths)
        # Ordering is by directness first -- a record naming the identifier in
        # its own title outranks one merely mentioning it -- and by stated date
        # within each of those tiers. So the mention tier, which is where the
        # record P6-060 needed was sitting, is what must run newest-first.
        titled = {r.source_path for r in found if "DEC-PHASE5-SEMANTICS" in r.title_identifiers}
        mentions = [r.date for r in found
                    if r.source_path not in titled and r.date != ABSENT]
        self.assertEqual(sorted(mentions, reverse=True), mentions, "chronology is surfaced")
        self.assertEqual(max(mentions), mentions[0], "the newest mention leads")
        # The record carrying the decided reading must remain *in* the surfaced
        # mention tier. Which date leads is a fact about the corpus and changes
        # as the corpus grows; that the decided reading stays findable is the
        # property P6-060 actually needed, so that is what is pinned.
        self.assertIn(DECIDED_READING_DATE, mentions)

    def test_the_record_carrying_the_decided_reading_leads_the_older_ones(self):
        found = [r for r in self.index.about("DEC-PHASE5-SEMANTICS")
                 if "DEC-PHASE5-SEMANTICS" not in r.title_identifiers]
        paths = [r.source_path for r in found]
        self.assertIn(DECIDED_READING, paths)
        position = paths.index(DECIDED_READING)
        self.assertEqual(DECIDED_READING_DATE, found[position].date)
        # Everything it outranks is genuinely older -- the ordering is earned by
        # chronology, not by position in the corpus.
        for record in found[position + 1:]:
            if record.date != ABSENT:
                self.assertLessEqual(record.date, DECIDED_READING_DATE)
        # ...and anything ahead of it is newer still, never an undated or older
        # record that merely sorted above it.
        for record in found[:position]:
            self.assertNotEqual(ABSENT, record.date)
            self.assertGreaterEqual(record.date, DECIDED_READING_DATE)

    def test_gdr_0028_is_addressable_at_its_line_in_the_register(self):
        found = self.index.by_identifier("GDR-0028")
        self.assertEqual(1, len(found))
        record, = found
        self.assertEqual("docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md",
                         record.source_path)
        self.assertEqual("2026-08-22", record.date)
        lines = (REPO_ROOT / record.source_path).read_text(encoding="utf-8").splitlines()
        self.assertIn("GDR-0028", lines[record.source_line - 1])

    def test_the_register_entry_it_calls_newest_is_genuinely_the_newest(self):
        register = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        entries = [r for r in self.index.records
                   if r.source_path == register and r.identifier.startswith("GDR-")
                   and r.date != ABSENT]
        self.assertGreater(len(entries), 5)
        newest_date = max(r.date for r in entries)
        # Which entry leads is a fact about the corpus and changes every time a
        # decision is recorded; that chronology is what *surfaces* it is the
        # property. Pinning the identifier tested the corpus, not the index, and
        # went stale twice -- GDR-0028 -> GDR-0029 -> GDR-0031 -- exactly as this
        # class's docstring describes for the two constants ACT-CC-P1-6-077
        # already replaced. Nor is a literal well-defined any longer: entries
        # state the same date as one another, and no resident source establishes
        # an ordering between entries that do, so nothing here may name one.
        # Asserting a relation among values the test itself derived would only
        # restate `max`, so the question §26 poses -- would the index have made
        # the newer record easy to find? -- is put to the index instead, through
        # the chronological query a reader would actually use.
        surfaced = self.index.since(newest_date)
        self.assertEqual(
            {r.identifier for r in entries if r.date == newest_date},
            {r.identifier for r in surfaced
             if r.source_path == register and r.identifier.startswith("GDR-")},
            "the chronological query must surface every register entry standing "
            "at the newest stated date, and no entry standing before it",
        )
        # ...and it hands them back in date order, so the newest is reached last
        # by chronology rather than by where it happens to sit in the file.
        stated = [gi._ISO_DATE_RE.search(r.date).group(0) for r in surfaced]
        self.assertEqual(sorted(stated), stated, "chronology is surfaced in order")

    def test_a_t12_enquiry_reaches_gdr_0028(self):
        found = self.index.about("T-12")
        self.assertIn("GDR-0028", [r.identifier for r in found])

    def test_those_historical_acts_were_not_rewritten(self):
        for name in ("AIOS_P6_060_PHASE_EXIT_ASSESSMENT_v1.0.md",
                     "AIOS_P6_061_D1_SOURCE_REVIEW_AND_CORRECTION_v1.0.md"):
            path = REPO_ROOT / "docs" / "program" / name
            self.assertEqual(sha256_of(path), self.index.sources[f"docs/program/{name}"])


# ---------------------------------------------------------------- Scope E


class ChronologyIsNotSupersession(unittest.TestCase):
    """§29's fixture. Two records, one older, one newer, outside the tracked tree."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _write(self.root, "a.md", (
            "# A\n\n**Identifier:** DEC-FIX-001\n**Date:** 2026-01-01\n"
            "**Status:** AUTHORIZED\n\n---\n\nolder\n"
        ))
        _write(self.root, "b.md", (
            "# B\n\n**Identifier:** DEC-FIX-002\n**Date:** 2026-09-09\n"
            "**Status:** AUTHORIZED\n\n---\n\nnewer, and unrelated\n"
        ))
        _write(self.root, "c.md", (
            "# C\n\n**Identifier:** DEC-FIX-003\n**Date:** 2026-10-10\n"
            "**Supersedes:** DEC-FIX-001\n\n---\n\nnewer, and says so\n"
        ))
        self.index, _ = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()
        self.assertFalse(self.root.exists(), "the fixture leaves no residue")

    def test_chronology_can_be_surfaced(self):
        since = self.index.since("2026-05-05")
        self.assertEqual(["DEC-FIX-002", "DEC-FIX-003"], [r.identifier for r in since])

    def test_a_newer_unrelated_record_supersedes_nothing(self):
        self.assertEqual(UNKNOWN, self.index.supersession("DEC-FIX-002")["superseded_by"])

    def test_a_declared_supersession_is_recorded_with_its_evidence(self):
        answer = self.index.supersession("DEC-FIX-001")
        self.assertNotEqual(UNKNOWN, answer["superseded_by"])
        edge, = answer["superseded_by"]
        self.assertEqual("DEC-FIX-003", edge["by"])
        self.assertEqual("declared-by-successor", edge["evidence"])
        self.assertEqual("c.md", edge["source_path"])

    def test_a_self_declared_supersession_is_recorded_as_such(self):
        _write(self.root, "d.md", (
            "# D\n\n**Identifier:** DEC-FIX-004\n**Superseded by:** DEC-FIX-005\n\n---\n\nx\n"
        ))
        index, _ = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root)
        edge, = index.supersession("DEC-FIX-004")["superseded_by"]
        self.assertEqual("DEC-FIX-005", edge["by"])
        self.assertEqual("self-declared", edge["evidence"])

    def test_absence_of_evidence_is_reported_as_such(self):
        self.assertIn("Absence of evidence", str(self.index.supersession("DEC-FIX-002")["note"]))

    def test_a_record_with_no_stated_date_is_not_placed_on_the_timeline(self):
        _write(self.root, "e.md", "# E\n\n**Identifier:** DEC-FIX-006\n\n---\n\nx\n")
        index, _ = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root)
        self.assertNotIn("DEC-FIX-006", [r.identifier for r in index.since("1900-01-01")])


# ---------------------------------------------------------------- Scope F


class IncrementalRebuild(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for name, ident in (("a.md", "DEC-INC-001"), ("b.md", "DEC-INC-002")):
            _write(self.root, name, f"# {ident}\n\n**Identifier:** {ident}\n**Date:** 2026-01-01\n\n---\n\nx\n")
        self.index, self.stats = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_the_first_build_parses_everything(self):
        self.assertEqual(2, self.stats.parsed)
        self.assertEqual(0, self.stats.reused)

    def test_an_unchanged_source_is_reused_not_reparsed(self):
        _, stats = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root, self.index)
        self.assertEqual(0, stats.parsed)
        self.assertEqual(2, stats.reused)

    def test_a_changed_source_is_reparsed_and_only_it(self):
        _write(self.root, "b.md", "# B\n\n**Identifier:** DEC-INC-002\n**Date:** 2026-07-07\n\n---\n\nx\n")
        index, stats = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root, self.index)
        self.assertEqual(1, stats.parsed)
        self.assertEqual(1, stats.reused)
        self.assertEqual("2026-07-07", index.by_identifier("DEC-INC-002")[0].date)

    def test_a_new_source_is_parsed(self):
        _write(self.root, "c.md", "# C\n\n**Identifier:** DEC-INC-003\n\n---\n\nx\n")
        _, stats = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root, self.index)
        self.assertEqual(1, stats.parsed)
        self.assertEqual(2, stats.reused)

    def test_a_deleted_source_is_removed_and_counted(self):
        (self.root / "b.md").unlink()
        index, stats = GovernanceIndex.build(sorted(self.root.glob("*.md")), self.root, self.index)
        self.assertEqual(1, stats.removed)
        self.assertEqual((), index.by_identifier("DEC-INC-002"))

    def test_a_changed_source_makes_a_written_index_report_itself_stale(self):
        _write(self.root, "b.md", "# B\n\n**Identifier:** DEC-INC-002\n**Date:** 2026-07-07\n\n---\n\nx\n")
        self.assertEqual(("b.md",), self.index.stale_sources(self.root))

    def test_a_written_index_round_trips(self):
        path = self.root / "index.json"
        self.index.write(path)
        reloaded = GovernanceIndex.read(path)
        self.assertEqual([r.as_json() for r in self.index.records],
                         [r.as_json() for r in reloaded.records])


# ---------------------------------------------------------------- Scope G


class Boundaries(unittest.TestCase):
    def test_the_module_imports_nothing_outside_the_standard_library(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported)
        self.assertLessEqual(imported, set(sys.stdlib_module_names))

    def test_the_module_imports_no_aios_core_and_no_consumer(self):
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        heads = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                heads.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                heads.add(node.module.split(".")[0])
        self.assertNotIn("native_core", heads)
        self.assertNotIn("consumers", heads)

    def test_the_tool_lives_in_tools(self):
        self.assertEqual("tools", MODULE_PATH.parent.name)

    def test_the_corpus_is_the_tracked_set_so_untracked_files_are_unreachable(self):
        tracked = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files", "--", "docs"],
            capture_output=True, check=True, text=True).stdout.split("\n")
        expected = {name for name in tracked if name.endswith(".md")}
        found = {p.relative_to(REPO_ROOT).as_posix() for p in tracked_markdown(REPO_ROOT)}
        self.assertEqual(expected, found)
        untracked = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "ls-files", "--others", "--exclude-standard", "--", "docs"],
            capture_output=True, check=True, text=True).stdout.split("\n")
        for name in untracked:
            if name.endswith(".md"):
                self.assertNotIn(name, found, "an untracked file must never enter the corpus")


class Queries(_Corpus):
    """§25 Queries A-J, each against the live corpus."""

    def test_a_what_is_the_latest_record_concerning_a_decision(self):
        found = self.index.about("DEC-P6-042")
        self.assertTrue(found)
        self.assertEqual("DEC-P6-042", found[0].identifier)

    def test_b_has_a_decision_been_superseded(self):
        answer = self.index.supersession("DEC-P6-042")
        # What the answer must be is read off the records, not pinned to the
        # corpus's present silence: an edge may be reported only where a record
        # states one, and UNKNOWN must be reported where none does. A literal
        # UNKNOWN tested the corpus rather than the query and would go stale the
        # moment a supersession was lawfully recorded.
        stated = [r for r in self.index.records
                  if (r.identifier == "DEC-P6-042" and r.superseded_by)
                  or "DEC-P6-042" in r.supersedes]
        if stated:
            self.assertNotEqual(UNKNOWN, answer["superseded_by"],
                                "a stated supersession must be reported")
        else:
            self.assertEqual(UNKNOWN, answer["superseded_by"],
                             "no record states that DEC-P6-042 was superseded")
        self.assertIn("read the canonical source", str(answer["note"]))

    def test_c_what_records_exist_for_a_phase(self):
        # by_phase "matches the stated program_phase text only", and the module
        # states that "no field is ever derived from a file's path, its name,
        # its position in the corpus, or its commit metadata". Both are checked
        # here against what the records state -- for a needle the corpus uses
        # and for one it does not -- rather than against the fact that no
        # tracked record happens to state "Phase 6" today, which is corpus state
        # and would go stale the moment one did.
        for needle in ("Phase 6", "DNA Consolidation"):
            self.assertEqual(
                tuple(r for r in self.index.records
                      if needle.casefold() in r.program_phase.casefold()),
                self.index.by_phase(needle), needle)
        self.assertTrue(self.index.by_phase("DNA Consolidation"))
        # A phase is never manufactured from a path: records filed under a
        # phase-named directory carry a phase only where they state one, and
        # the value carried is the source's own.
        filed_under_a_phase = [r for r in self.index.records
                               if re.search(r"phase[-_]?\d", r.source_path, re.IGNORECASE)]
        self.assertTrue(filed_under_a_phase)
        for record in filed_under_a_phase:
            if record.program_phase == ABSENT:
                continue
            source = (REPO_ROOT / record.source_path).read_text(encoding="utf-8")
            self.assertIn(record.program_phase.split("\n")[0][:30], source,
                          record.source_path)
        # Phase-6 Decisions are reachable instead through the identifier the
        # records themselves carry, which is evidence and not inference.
        decisions = self.index.search("DEC-P6")
        self.assertTrue(decisions)
        self.assertIn("DEC-P6-042", [r.identifier for r in decisions])

    def test_d_what_records_mention_t12(self):
        self.assertGreater(len(self.index.about("T-12")), 10)

    def test_e_what_is_relevant_to_knowledge(self):
        self.assertTrue(self.index.search("Knowledge"))

    def test_f_which_record_superseded_this_one(self):
        answer = self.index.supersession("GDR-0001")
        self.assertIn("identifier", answer)

    def test_g_when_was_a_decision_issued(self):
        record, = self.index.by_identifier("GDR-0028")
        self.assertEqual("2026-08-22", record.date)

    def test_h_what_authority_does_a_record_explicitly_claim(self):
        record, = self.index.by_identifier("DEC-P6-042")
        self.assertEqual("Founder", record.authority)

    def test_i_where_is_the_canonical_source(self):
        record, = self.index.by_identifier("GDR-0028")
        self.assertTrue((REPO_ROOT / record.source_path).exists())

    def test_j_what_changed_after_a_date(self):
        recent = self.index.since("2026-08-20")
        self.assertTrue(recent)
        self.assertEqual(sorted(r.date for r in recent), [r.date for r in recent])


if __name__ == "__main__":
    unittest.main()


# --------------------------------------------------------------------------
# Scope H — governance substrate repair (ACT-CC-R1-002; G02, G10)
# --------------------------------------------------------------------------


class SchemaNormalization(unittest.TestCase):
    """`ACT-CC-R1-002 §6` — two source forms, one internal representation.

    `ACT-CC-R1-001` measured the register carrying **both** an inline
    `**Identifier:**` form (24 entries) and a two-cell table form (14 entries),
    while this parser read only the first. Normalization happens here, at the
    tooling boundary; the canonical records are not rewritten.
    """

    def test_list_style_identifier_parses(self):
        self.assertEqual({"Identifier": "X-1"}, gi._labels(["**Identifier:** X-1"]))

    def test_table_style_identifier_parses(self):
        self.assertEqual({"Identifier": "X-1"}, gi._labels(["| **Identifier** | X-1 |"]))

    def test_both_forms_reach_the_same_representation(self):
        """The point of the repair: form is not meaning."""
        self.assertEqual(
            gi._labels(["**Identifier:** GDR-0002"]),
            gi._labels(["| **Identifier** | GDR-0002 |"]),
        )

    def test_a_mixed_corpus_yields_every_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "inline.md", "# Inline\n\n**Identifier:** GDR-9001\n\n---\n\nbody\n")
            _write(root, "table.md",
                   "# Table\n\n| Field | Value |\n|---|---|\n"
                   "| **Identifier** | GDR-9002 |\n\n---\n\nbody\n")
            index, _ = GovernanceIndex.build(sorted(root.glob("*.md")), root)
            found = {r.identifier for r in index.records}

        self.assertIn("GDR-9001", found)
        self.assertIn("GDR-9002", found)

    def test_table_parsing_is_narrow_enough_to_be_safe(self):
        """Header rows, delimiters and wider tables are not metadata. A parser
        that read them would invent labels out of ordinary content."""
        for line in ("| Field | Value |", "|---|---|", "| **A** | b | c |",
                     "| not bold | v |", "|  |  |"):
            self.assertEqual({}, gi._labels([line]), line)

    def test_the_inline_colon_rule_is_untouched(self):
        """Regression guard on the fix itself. The inline form requires a colon
        so that a bold *value* is not read as the next label; reaching table
        rows must not have relaxed that."""
        self.assertEqual(
            {"Status": "AUTHORIZED"}, gi._labels(["**Status:** **AUTHORIZED**"])
        )


class FounderDecisionsAreDiscoverable(_Corpus):
    """`ACT-CC-R1-002 §9`, `§20` — `G10` closure evidence.

    `ACT-CC-R1-001` measured 10 of 10 Founder Decisions present in the register
    and invisible to this index, because `FD` was missing from the identifier
    alternation. Discovery here runs off the real corpus through the parser —
    `§9` forbids whitelisting identifiers to make a count pass, so nothing below
    names an expected set: the register is read, and what it states is what is
    checked.
    """

    def _register_fd_identifiers(self):
        register = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        return {
            line.split()[1]
            for line in register.read_text(encoding="utf-8").splitlines()
            if line.startswith("### FD-")
        }

    def test_the_identifier_pattern_recognizes_the_founder_class(self):
        self.assertEqual(("FD-P9-002",), identifiers_in("see FD-P9-002 for the decision"))

    def test_every_founder_decision_in_the_register_is_indexed(self):
        stated = self._register_fd_identifiers()
        self.assertTrue(stated, "the register must state Founder Decisions")

        indexed = {r.identifier for r in self.index.records}

        self.assertEqual(set(), stated - indexed, "Founder Decisions missing from index")

    def test_each_one_is_retrievable_individually(self):
        for identifier in sorted(self._register_fd_identifiers()):
            self.assertTrue(
                self.index.by_identifier(identifier), f"{identifier} not retrievable"
            )

    def test_discovery_is_not_a_whitelist(self):
        """An FD identifier this repository has never used still parses, so the
        mechanism is general rather than fitted to the current corpus."""
        self.assertEqual(("FD-P42-999",), identifiers_in("FD-P42-999"))


class IndexIntegrity(_Corpus):
    """`ACT-CC-R1-002 §10`, `§12` — no silent loss, no duplicates, deterministic."""

    def test_no_identifier_is_indexed_twice(self):
        identified = [
            r.identifier for r in self.index.records if r.identifier != ABSENT
        ]

        self.assertEqual(len(identified), len(set(identified)))

    def test_every_register_subrecord_reaches_the_index(self):
        """Source count == indexed count for the register's own headings."""
        register = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        stated = {
            line.split()[1]
            for line in register.read_text(encoding="utf-8").splitlines()
            if line.startswith("### ") and gi._SUBRECORD_RE.match(line)
        }
        indexed = {r.identifier for r in self.index.records}

        self.assertEqual(set(), stated - indexed, "records dropped between source and index")

    def test_a_malformed_record_is_not_silently_absorbed(self):
        """`§11`: unparseable metadata yields ABSENT, which is visible, rather
        than a fabricated value."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write(root, "broken.md",
                   "# Broken\n\n| **Identifier** |\n\n---\n\nbody\n")
            index, _ = GovernanceIndex.build(sorted(root.glob("*.md")), root)
            records = index.records

        for record in records:
            self.assertEqual(ABSENT, record.identifier)

    def test_the_index_is_deterministic(self):
        first, _ = GovernanceIndex.build(tracked_markdown(REPO_ROOT), REPO_ROOT)
        second, _ = GovernanceIndex.build(tracked_markdown(REPO_ROOT), REPO_ROOT)

        self.assertEqual(
            [r.identifier for r in first.records],
            [r.identifier for r in second.records],
        )

    def test_repair_did_not_change_the_corpus(self):
        """The repair is tooling-only. `§4.1` forbids canonical content change,
        and this asserts it against the register itself."""
        register = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        before = sha256_of(register)
        GovernanceIndex.build(tracked_markdown(REPO_ROOT), REPO_ROOT)

        self.assertEqual(before, sha256_of(register))


# --------------------------------------------------------------------------
# Scope I — same-date chronology (`GDR-0033`; ACT-CC-R14AE)
# --------------------------------------------------------------------------


REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"


class SameDateEntriesAreUnordered(_Corpus):
    """`GDR-0033` — the Founder decided OPTION B, and this is what it forbids.

    > *"apabila dua atau lebih Governance Register entries memiliki canonical
    > stated date yang sama, seluruh entries pada maximal canonical stated date
    > **ARE EQUALLY NEWEST-BY-DATE** ... dan tidak boleh diurutkan satu terhadap
    > lainnya berdasarkan: GDR identifier; identifier sequence; file position;
    > parser order; insertion order; append order"*

    The newest-by-date answer is therefore a **date** and a **set**, never a
    single record. Nothing below names a member of that set, and nothing below
    requires it to hold exactly one -- the assumption the literal these tests
    replaced was quietly making, and the one the decision rules out. Same-date
    is not an edge case here: at the time of writing, 36 of the Register's 39
    dated entries stand inside one of ten such groups.
    """

    def _register_entries(self):
        return [r for r in self.index.records
                if r.source_path == REGISTER and r.identifier != ABSENT
                and r.date != ABSENT]

    def test_the_newest_answer_is_a_date_and_every_entry_carrying_it(self):
        entries = self._register_entries()
        self.assertGreater(len(entries), 20)
        newest_date = max(r.date for r in entries)
        newest = {r.identifier for r in entries if r.date == newest_date}
        self.assertGreaterEqual(len(newest), 1, "a maximal date always has members")
        surfaced = {r.identifier for r in self.index.since(newest_date)
                    if r.source_path == REGISTER and r.identifier != ABSENT}
        self.assertEqual(newest, surfaced,
                         "the chronological query returns the whole newest set, "
                         "no member dropped and no earlier entry admitted")

    def test_no_entry_sharing_a_date_outranks_another(self):
        """The ordering key itself must not separate them. `_recency` is what
        `about()` sorts by, so a key that varied within a group would be the
        implicit ordering `GDR-0033` prohibits, whatever any caller then did
        with it."""
        groups = {}
        for record in self._register_entries():
            groups.setdefault(record.date, []).append(record)
        shared = {date: members for date, members in groups.items() if len(members) > 1}
        self.assertGreater(len(shared), 1, "the corpus must exercise this")
        for date, members in shared.items():
            self.assertEqual({gi._recency(r) for r in members}, {date},
                             f"{date}: the sort key must not separate equals")
            surfaced = {r.identifier for r in self.index.since(date)}
            for record in members:
                self.assertIn(record.identifier, surfaced,
                              f"{record.identifier} dropped from its own date")

    def test_the_index_dates_the_register_as_the_register_states_it(self):
        """The decision speaks about *canonical* stated dates, so the maximum
        the index reports is checked against the maximum the source states --
        read here independently of the parser under test, since checking the
        index against itself would prove nothing.

        Known limitation, asserted narrowly for that reason: eleven entries
        state their date as ``Date decided`` / ``Date certified`` / ``Dates
        decided``, which `FIELD_LABELS["date"]` does not list, so the index
        carries no date for them. All eleven are older than the maximum, so the
        maximum agrees today. Should a future entry state the newest date in one
        of those forms, this assertion is what will say so.
        """
        source = (REPO_ROOT / REGISTER).read_text(encoding="utf-8")
        stated = re.findall(r"\*\*Dates?[^*]*\*\*:?\s*\|?\s*\**\s*(\d{4}-\d{2}-\d{2})",
                            source)
        self.assertGreater(len(stated), 20)
        self.assertEqual(max(stated), max(r.date for r in self._register_entries()))
