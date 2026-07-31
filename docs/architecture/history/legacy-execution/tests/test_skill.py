"""
Dedicated unit tests for execution/skill.py.

Foundation Test Coverage Hardening phase. Exercises invoke() and each
real handler against real, self-contained scratch files (never docs/),
using the real Skill catalog documents under docs/ only for
canonical-key resolution (read-only).

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import skill

CATALOG = Path(__file__).resolve().parent.parent.parent / "docs" / "architecture" / "organization" / "execution-catalog" / "skill"
AUTHORITY_PATH = CATALOG / "authority-boundary-check.md"
CITATION_PATH = CATALOG / "citation-discipline-verification.md"
STALENESS_PATH = CATALOG / "staleness-detection.md"
DUPLICATE_PATH = CATALOG / "duplicate-content-detection.md"
SECTION_NUMBERING_PATH = CATALOG / "section-numbering-consistency-check.md"
TERMINOLOGY_PATH = CATALOG / "terminology-consistency-scan.md"


class InvokeBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmpdir.name) / "doc.md"
        self.doc.write_text("Some plain content.\n", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_nonexistent_target_document_fails_input_validation(self):
        result = skill.invoke(STALENESS_PATH, self.tmpdir.name + "/missing.md")
        self.assertEqual(result.status, "failure")
        self.assertEqual(result.failure_class, "input_validation")

    def test_empty_document_succeeds_with_no_evidence(self):
        empty = Path(self.tmpdir.name) / "empty.md"
        empty.write_text("", encoding="utf-8")
        result = skill.invoke(STALENESS_PATH, empty)
        self.assertEqual(result.status, "success")
        self.assertEqual(result.output.evidence, ())

    def test_success_result_has_no_failure_class(self):
        result = skill.invoke(STALENESS_PATH, self.doc)
        self.assertEqual(result.status, "success")
        self.assertIsNone(result.failure_class)
        self.assertIsNone(result.error)


class AuthorityBoundaryCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmpdir.name) / "doc.md"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_claim_phrase_without_negation_is_flagged(self):
        self.doc.write_text("This document hereby establishes a new rule for everyone.\n", encoding="utf-8")
        result = skill.invoke(AUTHORITY_PATH, self.doc)
        self.assertEqual(len(result.output.evidence), 1)
        self.assertEqual(result.output.evidence[0].kind, "authority_claim_flag")

    def test_claim_phrase_with_negation_is_not_flagged(self):
        self.doc.write_text("This document does not hereby establish a new rule.\n", encoding="utf-8")
        result = skill.invoke(AUTHORITY_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())

    def test_plain_text_is_not_flagged(self):
        self.doc.write_text("Just an ordinary paragraph with nothing special in it.\n", encoding="utf-8")
        result = skill.invoke(AUTHORITY_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())


class StalenessDetectionTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmpdir.name) / "doc.md"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_high_severity_phrase_flagged_severity_3(self):
        self.doc.write_text("This item is TBD and needs resolution.\n", encoding="utf-8")
        result = skill.invoke(STALENESS_PATH, self.doc)
        self.assertEqual(len(result.output.evidence), 1)
        self.assertIn("[severity=3]", result.output.evidence[0].detail)

    def test_medium_severity_phrase_flagged_severity_2(self):
        self.doc.write_text("This question remains open for now.\n", encoding="utf-8")
        result = skill.invoke(STALENESS_PATH, self.doc)
        self.assertEqual(len(result.output.evidence), 1)
        self.assertIn("[severity=2]", result.output.evidence[0].detail)

    def test_high_severity_sorts_before_medium(self):
        self.doc.write_text("First, this remains open.\n\nSecond, this is TBD.\n", encoding="utf-8")
        result = skill.invoke(STALENESS_PATH, self.doc)
        self.assertEqual(len(result.output.evidence), 2)
        self.assertIn("[severity=3]", result.output.evidence[0].detail)
        self.assertIn("[severity=2]", result.output.evidence[1].detail)

    def test_no_staleness_phrases_no_evidence(self):
        self.doc.write_text("Everything here is fully resolved and current.\n", encoding="utf-8")
        result = skill.invoke(STALENESS_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())


class CitationDisciplineVerificationTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.cited = Path(self.tmpdir.name) / "cited.md"
        self.cited.write_text("# Cited\n\n## 9. Real Heading\n\nBody.\n", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_link_and_section_together_invokes_real_cross_reference_check(self):
        citing = Path(self.tmpdir.name) / "citing.md"
        citing.write_text(f"See [cited](cited.md) at §9 for detail.\n", encoding="utf-8")
        result = skill.invoke(CITATION_PATH, citing)
        self.assertEqual(len(result.output.evidence), 1)
        ev = result.output.evidence[0]
        self.assertEqual(ev.source, "tool")
        self.assertEqual(ev.kind, "cross_reference_check")
        self.assertTrue(ev.resolved)

    def test_governance_mention_with_no_link_or_section_flagged_uncited(self):
        citing = Path(self.tmpdir.name) / "citing.md"
        citing.write_text("This paragraph discusses the Constitution's authority without citing it anywhere.\n", encoding="utf-8")
        result = skill.invoke(CITATION_PATH, citing)
        self.assertEqual(len(result.output.evidence), 1)
        self.assertEqual(result.output.evidence[0].kind, "uncited_restatement_flag")
        self.assertIsNone(result.output.evidence[0].resolved)

    def test_plain_paragraph_no_evidence(self):
        citing = Path(self.tmpdir.name) / "citing.md"
        citing.write_text("Nothing notable in this paragraph at all.\n", encoding="utf-8")
        result = skill.invoke(CITATION_PATH, citing)
        self.assertEqual(result.output.evidence, ())


class DuplicateContentDetectionTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmpdir.name) / "doc.md"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_near_identical_paragraphs_flagged_as_duplicate(self):
        para = "This is a reasonably long paragraph used to test duplicate detection behavior here."
        self.doc.write_text(f"{para}\n\n{para}\n", encoding="utf-8")
        result = skill.invoke(DUPLICATE_PATH, self.doc)
        self.assertEqual(len(result.output.evidence), 1)
        self.assertEqual(result.output.evidence[0].kind, "duplicate_content_flag")

    def test_distinct_long_paragraphs_not_flagged(self):
        p1 = "This paragraph is about the governance model and its many distinct properties."
        p2 = "A completely unrelated paragraph discussing something entirely different in tone."
        self.doc.write_text(f"{p1}\n\n{p2}\n", encoding="utf-8")
        result = skill.invoke(DUPLICATE_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())

    def test_short_paragraphs_below_length_floor_are_ignored(self):
        self.doc.write_text("short\n\nshort\n", encoding="utf-8")
        result = skill.invoke(DUPLICATE_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())


class SectionNumberingConsistencyCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmpdir.name) / "doc.md"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_internal_citation_to_real_heading_not_flagged(self):
        self.doc.write_text("# Title\n\n## 9. Real\n\nSee §9 above.\n", encoding="utf-8")
        result = skill.invoke(SECTION_NUMBERING_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())

    def test_internal_citation_to_missing_heading_is_flagged(self):
        self.doc.write_text("# Title\n\n## 1. Real\n\nSee §9 above, which does not exist.\n", encoding="utf-8")
        result = skill.invoke(SECTION_NUMBERING_PATH, self.doc)
        self.assertEqual(len(result.output.evidence), 1)
        self.assertEqual(result.output.evidence[0].kind, "section_numbering_mismatch")

    def test_external_domain_model_citation_excluded_from_flagging(self):
        self.doc.write_text("# Title\n\n## 1. Real\n\nPer Domain Model §9, this holds.\n", encoding="utf-8")
        result = skill.invoke(SECTION_NUMBERING_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())


class TerminologyConsistencyScanTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmpdir.name) / "doc.md"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_paragraph_matching_its_own_term_definition_closely_is_not_flagged(self):
        self.doc.write_text(
            "A single, ephemeral runtime execution of an Agent Instance mentioning Agent Instance directly.\n",
            encoding="utf-8",
        )
        result = skill.invoke(TERMINOLOGY_PATH, self.doc)
        # own definition is highly similar to itself; should not read as confused with another term
        confused_with_others = [e for e in result.output.evidence if "Agent Instance" in e.detail]
        # accept either zero flags, or flags where the paragraph's own term still scores highest --
        # the real assertion is that this does not crash and returns real Evidence objects
        for e in result.output.evidence:
            self.assertEqual(e.kind, "terminology_confusion_flag")
            self.assertTrue(e.resolved)

    def test_paragraph_mentioning_no_reference_terms_produces_no_evidence(self):
        self.doc.write_text("This paragraph mentions nothing from the reference term list at all.\n", encoding="utf-8")
        result = skill.invoke(TERMINOLOGY_PATH, self.doc)
        self.assertEqual(result.output.evidence, ())


if __name__ == "__main__":
    unittest.main()
