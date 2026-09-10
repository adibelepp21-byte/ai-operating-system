"""Tests for the organization catalog — the P10 operationalization loader.

`FD-P10-003 §17`: *"No evidence means no completion claim."* These tests are the
evidence that the loader reads the population rather than composing one.
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.capability.ownership import DepartmentIdentity  # noqa: E402
from tools.organization_catalog import (  # noqa: E402
    ORGANIZATION_ROOT,
    OrganizationRootNotEstablished,
    build_graph,
    organization_key,
    read_departments,
    report,
)


class ItReadsTheEstablishedPopulation(unittest.TestCase):
    def test_both_established_departments_are_read(self):
        names = {d.name for d in read_departments()}
        self.assertEqual(names, {"Platform", "Engineering"}, names)

    def test_every_department_has_a_resident_record(self):
        for record in read_departments():
            self.assertTrue((REPO_ROOT / record.record).is_file(), record.record)

    def test_every_capability_key_corresponds_to_a_file(self):
        for record in read_departments():
            base = REPO_ROOT / record.record
            for key in record.capabilities:
                self.assertTrue(
                    (base.parent / "capabilities" / f"{key}.md").is_file(), key
                )

    def test_every_agent_definition_key_corresponds_to_a_file(self):
        for record in read_departments():
            base = REPO_ROOT / record.record
            for key in record.agent_definitions:
                self.assertTrue(
                    (base.parent / "agent-definitions" / f"{key}.md").is_file(), key
                )


class AMentionIsNotAnEstablishment(unittest.TestCase):
    """Regression for a defect in the first version of this loader.

    It unioned every ``ADR-NNNN`` across a Department's README and capability
    files, which attributed **ADR-0003 to Engineering** because a capability
    record cross-references it — *"belongs to Platform under ADR-0003"*.
    """

    def test_each_department_names_exactly_its_own_establishing_adr(self):
        by_name = {d.name: d for d in read_departments()}
        self.assertEqual(by_name["Platform"].establishing_adrs, ("ADR-0003",))
        self.assertEqual(by_name["Engineering"].establishing_adrs, ("ADR-0008",))

    def test_a_cross_reference_is_still_present_in_the_source(self):
        """Guard: if the cross-reference vanished, this test proves nothing."""
        text = (
            REPO_ROOT
            / "docs/architecture/organization/engineering/capabilities"
            / "engineering-intelligence.md"
        ).read_text(encoding="utf-8")
        self.assertIn("ADR-0003", text, "fixture no longer exercises the defect")


class ItNeverConvertsAPlatformDivisionIntoADepartment(unittest.TestCase):
    """`FD-P10-003 §5`: CANONICAL DEPARTMENT ≠ PD."""

    def test_no_pd_appears_in_the_population(self):
        for record in read_departments():
            self.assertNotRegex(record.key, r"^pd-\d")
            self.assertNotRegex(record.name, r"^PD-\d")

    def test_the_platform_organization_tree_is_not_consulted(self):
        import inspect

        from tools import organization_catalog

        source = inspect.getsource(organization_catalog)
        self.assertNotIn("platform-organization", source)


class ItRefusesRatherThanInventingARoot(unittest.TestCase):
    """`FD-P10-003 §4.1` / `§24` — the population may not be invented."""

    def test_no_organization_instance_is_currently_established(self):
        with self.assertRaises(OrganizationRootNotEstablished):
            organization_key()

    def test_graph_construction_refuses_without_a_root(self):
        with self.assertRaises(OrganizationRootNotEstablished):
            build_graph()

    def test_the_report_says_blocked_rather_than_empty(self):
        result = report()
        self.assertFalse(result["graph_constructed"])
        self.assertIn("blocked_reason", result)
        self.assertGreater(len(result["departments"]), 0,
                           "blocked must not be reported as an empty population")

    def test_a_supplied_root_would_construct_the_graph(self):
        """Proves the refusal is about the missing root, not a broken loader."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dept = root / "platform"
            (dept / "capabilities").mkdir(parents=True)
            (dept / "README.md").write_text(
                "# Platform\n\nThis Department was established by [ADR-0003](x).\n"
                "\n## Name\n\nPlatform\n\n## Organization\n\nAIOS\n",
                encoding="utf-8",
            )
            (dept / "capabilities" / "governance-artifact-integrity.md").write_text(
                "# Governance Artifact Integrity\n\n## Name\n\nGovernance Artifact Integrity\n",
                encoding="utf-8",
            )
            graph = build_graph(root)
            self.assertEqual(len(graph.departments()), 1)
            owner = graph.owner_of("governance-artifact-integrity")
            self.assertEqual(owner.identity, DepartmentIdentity("platform"))


class TheCountsAreMeasuredNotAsserted(unittest.TestCase):
    def test_counts_match_the_files_on_disk(self):
        result = report()
        capability_files = len(list(ORGANIZATION_ROOT.glob("*/capabilities/*.md")))
        definition_files = len(list(ORGANIZATION_ROOT.glob("*/agent-definitions/*.md")))
        self.assertEqual(result["capabilities"], capability_files)
        self.assertEqual(result["agent_definitions"], definition_files)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
