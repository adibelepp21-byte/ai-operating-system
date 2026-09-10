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


class TheRootIsDerivedFromTheDomainModel(unittest.TestCase):
    """**Narrowed 2026-09-10.** These three tests previously asserted that the
    loader *refuses* because no Organization instance was established.

    That was an over-reading and it is corrected rather than kept. The Canonical
    Domain Model's own entity table defines Organization as *"The whole of AIOS.
    Single root identity; ultimate accountable body"* — for an entity so
    defined, the type and its sole instance coincide. `organization_spec §12`
    reserves *"Multi-Organization topology **beyond a single root**"*, which
    presupposes the root it reserves everything past.

    **What the tests assert now is the property that actually matters:** the root
    is *derived from the Domain Model*, never chosen, and the derivation fails
    closed the moment its premise is gone.
    """

    def test_the_root_comes_from_the_domain_model_row(self):
        self.assertEqual(organization_key(), "aios")

    def test_the_derivation_fails_closed_without_the_row(self):
        import tools.organization_catalog as mod

        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "no-domain-model.md"
            empty.write_text("# nothing here\n", encoding="utf-8")
            original = mod.DOMAIN_MODEL
            mod.DOMAIN_MODEL = empty
            try:
                with self.assertRaises(OrganizationRootNotEstablished):
                    organization_key()
            finally:
                mod.DOMAIN_MODEL = original

    def test_the_derivation_fails_closed_without_a_single_root_assertion(self):
        import tools.organization_catalog as mod

        with tempfile.TemporaryDirectory() as tmp:
            altered = Path(tmp) / "domain-model.md"
            altered.write_text(
                "| **Organization** | The whole of AIOS. Many roots. |\n",
                encoding="utf-8",
            )
            original = mod.DOMAIN_MODEL
            mod.DOMAIN_MODEL = altered
            try:
                with self.assertRaises(OrganizationRootNotEstablished):
                    organization_key()
            finally:
                mod.DOMAIN_MODEL = original

    def test_the_graph_now_constructs_over_the_real_population(self):
        result = report()
        self.assertTrue(result["graph_constructed"])
        self.assertEqual(result["inv1_unowned_capabilities"], [])
        self.assertEqual(result["inv1_disputed"], [])
        self.assertEqual(result["inv2_unowned_agent_definitions"], [])
        self.assertEqual(
            result["resolutions"],
            {
                "governance-artifact-integrity": "platform",
                "engineering-intelligence": "engineering",
                "cognitive-intelligence": "engineering",
            },
        )

    def test_a_supplied_root_constructs_a_graph_over_a_temp_corpus(self):
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
