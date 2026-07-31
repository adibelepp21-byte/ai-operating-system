"""
Dedicated unit tests for execution/tool.py.

Foundation Test Coverage Hardening phase. Exercises the three real Tool
implementations against real, self-contained scratch files (never
docs/), following the same isolation pattern already established by
execution/memory/drift_experiment.py. load_canonical_key() is exercised
against the real Tool catalog documents under docs/, read-only.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import tool

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CROSS_REF_TOOL_PATH = REPO_ROOT / "docs" / "architecture" / "organization" / "execution-catalog" / "tool" / "cross-reference-link-validator-interface.md"
DOC_STRUCTURE_TOOL_PATH = REPO_ROOT / "docs" / "architecture" / "organization" / "execution-catalog" / "tool" / "document-structure-parser-interface.md"


class LoadCanonicalKeyTest(unittest.TestCase):
    def test_real_cross_reference_tool_key(self):
        key = tool.load_canonical_key(CROSS_REF_TOOL_PATH)
        self.assertEqual(key, "tool.cross-reference-link-validator-interface")

    def test_real_document_structure_tool_key(self):
        key = tool.load_canonical_key(DOC_STRUCTURE_TOOL_PATH)
        self.assertEqual(key, "tool.document-structure-parser-interface")


class CrossReferenceLinkValidatorTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.cited = self.root / "cited.md"
        self.citing = self.root / "citing.md"
        self.cited.write_text("# Cited\n\n## 9. A Real Heading\n\nBody text.\n", encoding="utf-8")
        self.citing.write_text("Cites §9 of cited.md\n", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_real_heading_match_resolves_true(self):
        execution = tool.invoke(
            CROSS_REF_TOOL_PATH, action="verify_cross_reference",
            citing_document=str(self.citing), repository_path=str(self.root),
            reference_target=str(self.cited), expected_reference="§9",
        )
        self.assertTrue(execution.succeeded)
        self.assertTrue(execution.evidence["resolved"])
        self.assertEqual(execution.evidence["evidence"]["match_type"], "heading")

    def test_missing_section_resolves_false(self):
        execution = tool.invoke(
            CROSS_REF_TOOL_PATH, action="verify_cross_reference",
            citing_document=str(self.citing), repository_path=str(self.root),
            reference_target=str(self.cited), expected_reference="§99",
        )
        self.assertTrue(execution.succeeded)
        self.assertFalse(execution.evidence["resolved"])

    def test_mention_only_not_a_heading_is_distinguished_from_no_match(self):
        self.cited.write_text("# Cited\n\nThis text mentions §9 in prose, not as a heading.\n", encoding="utf-8")
        execution = tool.invoke(
            CROSS_REF_TOOL_PATH, action="verify_cross_reference",
            citing_document=str(self.citing), repository_path=str(self.root),
            reference_target=str(self.cited), expected_reference="§9",
        )
        self.assertFalse(execution.evidence["resolved"])
        self.assertEqual(execution.evidence["evidence"]["match_type"], "mention_only")

    def test_nonexistent_target_file_is_a_clean_failure_not_a_crash(self):
        execution = tool.invoke(
            CROSS_REF_TOOL_PATH, action="verify_cross_reference",
            citing_document=str(self.citing), repository_path=str(self.root),
            reference_target=str(self.root / "does-not-exist.md"), expected_reference="§9",
        )
        self.assertTrue(execution.succeeded)  # the Tool ran successfully; the *check* failed
        self.assertFalse(execution.evidence["resolved"])
        self.assertIn("does not resolve", execution.evidence["failure_reason"])

    def test_relative_reference_target_resolved_against_repository_path(self):
        execution = tool.invoke(
            CROSS_REF_TOOL_PATH, action="verify_cross_reference",
            citing_document=str(self.citing), repository_path=str(self.root),
            reference_target="cited.md", expected_reference="§9",
        )
        self.assertTrue(execution.evidence["resolved"])

    def test_deterministic_repeat_calls(self):
        params = dict(
            citing_document=str(self.citing), repository_path=str(self.root),
            reference_target=str(self.cited), expected_reference="§9",
        )
        e1 = tool.invoke(CROSS_REF_TOOL_PATH, action="verify_cross_reference", **params)
        e2 = tool.invoke(CROSS_REF_TOOL_PATH, action="verify_cross_reference", **params)
        self.assertEqual(e1.evidence, e2.evidence)

    def test_fingerprint_is_populated_for_file_based_call(self):
        execution = tool.invoke(
            CROSS_REF_TOOL_PATH, action="verify_cross_reference",
            citing_document=str(self.citing), repository_path=str(self.root),
            reference_target=str(self.cited), expected_reference="§9",
        )
        self.assertIsNotNone(execution.fingerprint)


class DocumentStructureParserTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmpdir.name) / "doc.md"
        self.doc.write_text("# Title\n\n## 1. First\n\nBody.\n\n## 2. Second\n\nMore.\n", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_parses_real_heading_structure_in_order(self):
        execution = tool.invoke(DOC_STRUCTURE_TOOL_PATH, action="parse_structure", document_path=str(self.doc))
        self.assertTrue(execution.evidence["resolved"])
        elements = execution.evidence["elements"]
        self.assertEqual(len(elements), 3)
        self.assertEqual(elements[1]["number"], "1")
        self.assertEqual(elements[2]["number"], "2")

    def test_nonexistent_document_is_a_clean_failure(self):
        execution = tool.invoke(DOC_STRUCTURE_TOOL_PATH, action="parse_structure", document_path=str(self.doc) + "-missing")
        self.assertFalse(execution.evidence["resolved"])
        self.assertIn("does not resolve", execution.evidence["failure_reason"])

    def test_empty_document_resolves_with_zero_elements(self):
        empty = Path(self.tmpdir.name) / "empty.md"
        empty.write_text("", encoding="utf-8")
        execution = tool.invoke(DOC_STRUCTURE_TOOL_PATH, action="parse_structure", document_path=str(empty))
        self.assertTrue(execution.evidence["resolved"])
        self.assertEqual(execution.evidence["elements"], [])


class TextSimilarityComparisonTest(unittest.TestCase):
    TEXT_SIMILARITY_TOOL_PATH = REPO_ROOT / "docs" / "architecture" / "organization" / "execution-catalog" / "tool" / "text-similarity-comparison-interface.md"

    def test_identical_passages_have_similarity_one(self):
        execution = tool.invoke(self.TEXT_SIMILARITY_TOOL_PATH, action="compare_similarity", passage_a="hello world", passage_b="hello world")
        self.assertEqual(execution.evidence["similarity"], 1.0)

    def test_completely_different_passages_have_low_similarity(self):
        execution = tool.invoke(self.TEXT_SIMILARITY_TOOL_PATH, action="compare_similarity", passage_a="aaaaaaaaaa", passage_b="zzzzzzzzzz")
        self.assertLess(execution.evidence["similarity"], 0.3)

    def test_empty_passage_fails_cleanly(self):
        execution = tool.invoke(self.TEXT_SIMILARITY_TOOL_PATH, action="compare_similarity", passage_a="", passage_b="x")
        self.assertFalse(execution.evidence["resolved"])
        self.assertIsNone(execution.evidence["similarity"])


class CacheKeyFnTest(unittest.TestCase):
    def test_cross_reference_cache_key_derives_from_target_and_reference(self):
        req = tool.ToolRequest(
            tool_canonical_key="tool.cross-reference-link-validator-interface", action="x",
            parameters={"reference_target": "/a.md", "expected_reference": "§9", "citing_document": "/b.md"},
        )
        key = tool._cross_reference_cache_key(req)
        self.assertEqual(key, ("tool.cross-reference-link-validator-interface", "/a.md", "§9"))

    def test_text_similarity_cache_key_is_order_sensitive_by_position(self):
        req = tool.ToolRequest(tool_canonical_key="tool.text-similarity-comparison-interface", action="x",
                                parameters={"passage_a": "x", "passage_b": "y"})
        key = tool._text_similarity_cache_key(req)
        self.assertEqual(key, ("tool.text-similarity-comparison-interface", "x", "y"))

    def test_all_three_real_tools_have_registered_cache_key_fns(self):
        for key in (
            "tool.text-similarity-comparison-interface",
            "tool.document-structure-parser-interface",
            "tool.cross-reference-link-validator-interface",
        ):
            self.assertIn(key, tool.CACHE_KEY_FNS)


class RegistryWiringTest(unittest.TestCase):
    def test_default_registry_has_all_three_real_tools(self):
        registry = tool._registry()
        for key in tool.IMPLEMENTATIONS:
            self.assertIsNotNone(registry.get(key))

    def test_default_registry_is_a_singleton_across_calls(self):
        self.assertIs(tool._registry(), tool._registry())


if __name__ == "__main__":
    unittest.main()
