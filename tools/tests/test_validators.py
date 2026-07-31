"""
Regression tests for tools/validators/.

Uses only the standard library (unittest) — no test dependency is added
to the repository. Most tests build a synthetic fixture catalog in a
temp directory and patch validators.catalog.CATALOG_ROOT to point at it,
so validator logic is exercised in isolation from the real corpus. One
test (RealCorpusRegressionTest) intentionally runs against the real
repository, as a regression guard confirming the actual execution
catalog stays free of error/warning findings.

Run with:
    python3 -m unittest discover -s tools/tests
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validators import agent_integration, canonical_key, duplicate_key, integrity, relative_link
from validators import catalog as catalog_mod

SKILL_TEMPLATE = """# {name}

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md).

## Metadata

- **Name:** {name}
- **Canonical Key:** `{key}`
- **Owning designation:** Owned centrally.
- **Version:** v1.0

## Purpose / Description

Test fixture.

## Interface

Test fixture.

## Permitted Invocation Context

Test fixture.

## Version History

- **v1.0** — Initial creation.
"""

WORKFLOW_TEMPLATE = """# {name}

This document is a Workflow instance, documented per the
[Workflow Framework](../../workflow-framework.md).

## Metadata

- **Name:** {name}
- **Canonical Key:** `{key}`
- **Owning designation:** Owned centrally.
- **Version:** v1.0

## Purpose / Description

Test fixture.

## Composed Elements

{composed_elements}

## Compatibility Boundary Representation

Test fixture.

## Version History

- **v1.0** — Initial creation.
"""

AGENT_DEF_TEMPLATE = """# {name}

## Metadata

- **Name:** {name}
- **Version:** 1.0
- **Status:** Active

## Purpose / Description

Test fixture.

## Owning Department

Test.

## Implemented Capability

Test.

## Behavior and Permissions

Test fixture.

## Permitted Skills

{permitted_skills}

## Permitted Workflows

{permitted_workflows}

## Runtime Requirements

Test fixture.

## Version History

- **v1.0** — Initial creation.
"""


class ValidatorFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.org_root = self.tmp
        self.catalog_root = self.tmp / "execution-catalog"
        for etype in ("skill", "workflow", "runtime", "tool"):
            (self.catalog_root / etype).mkdir(parents=True)
        self._patches = [
            mock.patch.object(catalog_mod, "CATALOG_ROOT", self.catalog_root),
            mock.patch.object(catalog_mod, "ORG_ROOT", self.org_root),
        ]
        for p in self._patches:
            p.start()

    def tearDown(self):
        for p in self._patches:
            p.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_skill(self, filename, name, key):
        path = self.catalog_root / "skill" / filename
        path.write_text(SKILL_TEMPLATE.format(name=name, key=key), encoding="utf-8")
        return path


class CanonicalKeyValidatorTests(ValidatorFixture):
    def test_valid_key_passes(self):
        self.write_skill("good.md", "Good Skill", "skill.good")
        self.assertEqual(canonical_key.run(), [])

    def test_malformed_key_flagged(self):
        self.write_skill("bad.md", "Bad Skill", "Skill_Bad!!")
        findings = canonical_key.run()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "error")

    def test_prefix_mismatch_flagged(self):
        self.write_skill("mismatched.md", "Mismatched", "tool.mismatched")
        findings = canonical_key.run()
        self.assertEqual(len(findings), 1)
        self.assertIn("prefix", findings[0].message)

    def test_missing_key_flagged(self):
        path = self.catalog_root / "skill" / "nokey.md"
        path.write_text("# No key\n\n## Metadata\n\nnothing here\n", encoding="utf-8")
        findings = canonical_key.run()
        self.assertEqual(len(findings), 1)
        self.assertIn("no Canonical Key", findings[0].message)


class DuplicateKeyDetectorTests(ValidatorFixture):
    def test_no_duplicates(self):
        self.write_skill("a.md", "A", "skill.a")
        self.write_skill("b.md", "B", "skill.b")
        self.assertEqual(duplicate_key.run(), [])

    def test_same_type_duplicate_is_error(self):
        self.write_skill("a.md", "A", "skill.dup")
        self.write_skill("b.md", "B", "skill.dup")
        findings = duplicate_key.run()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "error")

    def test_cross_type_duplicate_is_informational(self):
        self.write_skill("a.md", "A", "skill.shared")
        tool_path = self.catalog_root / "tool" / "b.md"
        tool_path.write_text(SKILL_TEMPLATE.format(name="B", key="tool.shared"), encoding="utf-8")
        findings = duplicate_key.run()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "informational")


class RelativeLinkValidatorTests(ValidatorFixture):
    def test_resolving_link_passes(self):
        (self.catalog_root.parent / "skill-framework.md").write_text("# Skill Framework\n", encoding="utf-8")
        self.write_skill("a.md", "A", "skill.a")
        self.assertEqual(relative_link.run(), [])

    def test_broken_link_flagged(self):
        path = self.write_skill("a.md", "A", "skill.a")
        text = path.read_text(encoding="utf-8").replace(
            "[Skill Framework](../../skill-framework.md)",
            "[Skill Framework](../../does-not-exist.md)",
        )
        path.write_text(text, encoding="utf-8")
        findings = relative_link.run()
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "error")


class IntegrityCheckerTests(ValidatorFixture):
    def test_complete_skill_passes(self):
        self.write_skill("a.md", "A", "skill.a")
        self.assertEqual(integrity.run(), [])

    def test_missing_section_flagged(self):
        path = self.write_skill("a.md", "A", "skill.a")
        text = path.read_text(encoding="utf-8").replace("## Interface\n\nTest fixture.\n\n", "")
        path.write_text(text, encoding="utf-8")
        findings = integrity.run()
        self.assertTrue(any("Interface" in f.message for f in findings))

    def test_missing_owning_designation_flagged(self):
        path = self.write_skill("a.md", "A", "skill.a")
        text = path.read_text(encoding="utf-8").replace("- **Owning designation:** Owned centrally.\n", "")
        path.write_text(text, encoding="utf-8")
        findings = integrity.run()
        self.assertTrue(any("Owning designation" in f.message for f in findings))


class AgentIntegrationValidatorTests(ValidatorFixture):
    def setUp(self):
        super().setUp()
        self.agent_def_dir = self.org_root / "dept" / "agent-definitions"
        self.agent_def_dir.mkdir(parents=True)

    def write_agent_def(self, permitted_skills="None declared.", permitted_workflows="None declared."):
        path = self.agent_def_dir / "agent.md"
        path.write_text(AGENT_DEF_TEMPLATE.format(
            name="Test Agent",
            permitted_skills=permitted_skills,
            permitted_workflows=permitted_workflows,
        ), encoding="utf-8")
        return path

    def write_workflow_citing_agent(self, filename, name, key):
        path = self.catalog_root / "workflow" / filename
        body = WORKFLOW_TEMPLATE.format(
            name=name, key=key,
            composed_elements="Invoked by [Test Agent](../../dept/agent-definitions/agent.md).",
        )
        path.write_text(body, encoding="utf-8")
        return path

    def test_no_agent_definitions_no_findings(self):
        self.write_skill("a.md", "A", "skill.a")
        self.assertEqual(agent_integration.run(), [])

    def test_resolving_correctly_typed_permission_passes(self):
        self.write_skill("a.md", "A", "skill.a")
        self.write_agent_def(permitted_skills="- [skill.a](../../execution-catalog/skill/a.md)")
        self.assertEqual(agent_integration.run(), [])

    def test_broken_permitted_link_is_error(self):
        self.write_agent_def(permitted_skills="- [skill.missing](../../execution-catalog/skill/missing.md)")
        findings = agent_integration.run()
        self.assertTrue(any(f.severity == "error" and "does not resolve" in f.message for f in findings))

    def test_wrong_type_permitted_link_is_error(self):
        self.write_skill("a.md", "A", "skill.a")
        self.write_agent_def(permitted_workflows="- [skill.a](../../execution-catalog/skill/a.md)")
        findings = agent_integration.run()
        self.assertTrue(any(f.severity == "error" and "expected 'workflow/'" in f.message for f in findings))

    def test_incidental_non_catalog_link_ignored(self):
        self.write_agent_def(permitted_skills="See [some doc](../../some-doc.md) for background.")
        (self.org_root / "some-doc.md").write_text("# Some doc\n", encoding="utf-8")
        self.assertEqual(agent_integration.run(), [])

    def test_reverse_gap_flagged_as_warning(self):
        self.write_agent_def()
        self.write_workflow_citing_agent("w.md", "W", "workflow.w")
        findings = agent_integration.run()
        self.assertTrue(any(f.severity == "warning" for f in findings))

    def test_reverse_gap_resolved_when_listed(self):
        self.write_workflow_citing_agent("w.md", "W", "workflow.w")
        self.write_agent_def(permitted_workflows="- [workflow.w](../../execution-catalog/workflow/w.md)")
        self.assertEqual([f for f in agent_integration.run() if f.severity == "warning"], [])


class RealCorpusRegressionTest(unittest.TestCase):
    """Runs against the real repository (not a synthetic fixture): guards
    against regressing the clean state confirmed by the Governance Freeze
    Delta / Execution Catalog Tooling Stabilization Phase evidence runs."""

    def test_real_corpus_has_no_error_or_warning_findings(self):
        from validators.runner import run_all
        report = run_all()
        if report.artifacts_scanned == 0:
            self.skipTest("execution-catalog directory not present in this checkout")
        totals = report.totals_by_severity()
        self.assertEqual(totals["error"], 0)
        self.assertEqual(totals["warning"], 0)


if __name__ == "__main__":
    unittest.main()
