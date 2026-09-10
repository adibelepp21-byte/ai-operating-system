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
    w4_chain,
    w4_continuity,
    WorkEntry,
    WorkEntryUnresolved,
    resolve_work_entry,
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


class TheW4ChainClosesAndCanFail(unittest.TestCase):
    """`P10-W4`: DEPARTMENT → CAPABILITY → AGENT DEFINITION.

    `ACT-CC-P10-003 §28`: *"negative controls"*. Each planted defect below
    changes exactly one thing and must be seen — a chain check that cannot
    report a break is not evidence that the chain is unbroken.
    """

    def test_the_real_chain_closes_with_no_defects(self):
        links, defects = w4_chain(read_departments())
        self.assertEqual(defects, [])
        self.assertEqual(len(links), 3)
        self.assertIn(
            ("platform", "governance-artifact-integrity",
             "governance-artifact-integrity-agent"), links,
        )

    def _corpus(self, tmp, *, declared_dept="Platform", declared_cap="Cap One",
                owned=("cap-one",)):
        root = Path(tmp)
        dept = root / "platform"
        (dept / "capabilities").mkdir(parents=True)
        (dept / "agent-definitions").mkdir(parents=True)
        (dept / "README.md").write_text(
            "# Platform\n\nThis Department was established by [ADR-0003](x).\n"
            "\n## Name\n\nPlatform\n", encoding="utf-8")
        for key in owned:
            (dept / "capabilities" / f"{key}.md").write_text(
                f"# {key}\n\n## Name\n\n{key}\n", encoding="utf-8")
        (dept / "agent-definitions" / "some-agent.md").write_text(
            "# Some Agent\n\n## Owning Department\n\n"
            f"[{declared_dept}](../README.md)\n\n## Implemented Capability\n\n"
            f"[{declared_cap}](../capabilities/x.md)\n", encoding="utf-8")
        return root

    def test_a_declared_department_that_contradicts_the_nesting_is_seen(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._corpus(tmp, declared_dept="Engineering")
            _, defects = w4_chain(read_departments(root), root)
            self.assertIn("department-mismatch", [d[0] for d in defects], defects)

    def test_a_capability_the_department_does_not_own_is_seen(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self._corpus(tmp, declared_cap="Not Owned At All")
            _, defects = w4_chain(read_departments(root), root)
            self.assertIn("capability-not-owned", [d[0] for d in defects], defects)

    def test_a_capability_with_no_implementer_is_seen(self):
        """`INV-14` — a Capability with zero implementers as a steady state."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._corpus(tmp, owned=("cap-one", "cap-two"))
            _, defects = w4_chain(read_departments(root), root)
            kinds = [(d[0], d[1]) for d in defects]
            self.assertIn(("capability-unimplemented", "cap-two"), kinds, defects)

    def test_the_positive_control_passes_on_the_same_fixture_shape(self):
        """Guard: the fixture must be capable of producing zero defects."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._corpus(tmp)
            links, defects = w4_chain(read_departments(root), root)
            self.assertEqual(defects, [], "fixture is broken, not the checker")
            self.assertEqual(len(links), 1)


class TheChainContinuesIntoWorkflowAndCanFail(unittest.TestCase):
    """`FD-P10-004 §8` — DEPARTMENT → ... → WORKFLOW → SKILL, as one chain.

    `w4_chain` ended at the Agent Definition and the Agent Integration Validator
    began there. Both passed, and **neither joined them**, so the composed path
    a Department originates was evidenced only by two verified halves lying
    adjacent. These tests are the join, and the negative controls are what make
    it evidence: `FD-P10-004 §10` condition 5 requires them, and condition 4
    requires the mechanism to *"actually test the claimed invariants."*
    """

    def test_the_real_continuity_closes_with_no_defects(self):
        links, _ = w4_chain(read_departments())
        chains, terminal, defects = w4_continuity(links)
        self.assertEqual(defects, [])
        self.assertEqual(len(chains), 5, chains)
        self.assertEqual(
            {c[3] for c in chains},
            {"governance-corpus-health-check", "governance-synchronization-review",
             "post-amendment-consistency-sweep", "pre-ratification-validation",
             "terminology-audit"},
        )

    def test_every_contained_skill_is_one_the_invoker_permits(self):
        """The invariant itself, stated over the real corpus rather than a fixture."""
        links, _ = w4_chain(read_departments())
        chains, _, _ = w4_continuity(links)
        contained = {skill for chain in chains for skill in chain[4]}
        self.assertEqual(len(contained), 10, sorted(contained))

    def test_the_engineering_chains_are_terminal_and_that_is_not_a_defect(self):
        """`Domain Model INV-15` / `ADR-0007`: an empty declaration is valid.

        This is asserted so that a later change which quietly manufactures a
        Workflow to lengthen these chains fails a test instead of passing one —
        `FD-P10-004 §27` forbids exactly that construction.
        """
        links, _ = w4_chain(read_departments())
        _, terminal, defects = w4_continuity(links)
        self.assertEqual({t[0] for t in terminal}, {"engineering"}, terminal)
        self.assertEqual(len(terminal), 2, terminal)
        self.assertNotIn("workflow-missing", [d[0] for d in defects])

    def _corpus(self, tmp, *, invoker_link="../../platform/agent-definitions/some-agent.md",
                invoker_phrase="an Agent Instance of the",
                contains_skill="skill-one", declare_workflow=True,
                permitted_skills=("skill-one",), workflow_exists=True):
        root = Path(tmp)
        dept = root / "platform"
        (dept / "capabilities").mkdir(parents=True)
        (dept / "agent-definitions").mkdir(parents=True)
        catalog = root / "execution-catalog"
        (catalog / "workflow").mkdir(parents=True)
        (catalog / "skill").mkdir(parents=True)
        (dept / "README.md").write_text(
            "# Platform\n\nThis Department was established by [ADR-0003](x).\n"
            "\n## Name\n\nPlatform\n", encoding="utf-8")
        (dept / "capabilities" / "cap-one.md").write_text(
            "# cap-one\n\n## Name\n\ncap-one\n", encoding="utf-8")
        for skill in ("skill-one", "skill-two"):
            (catalog / "skill" / f"{skill}.md").write_text(
                f"# {skill}\n", encoding="utf-8")
        permitted = "\n".join(
            f"- [{k}](../../execution-catalog/skill/{k}.md)" for k in permitted_skills)
        workflows = (
            "- [wf-one](../../execution-catalog/workflow/wf-one.md)"
            if declare_workflow else "None declared.")
        (dept / "agent-definitions" / "some-agent.md").write_text(
            "# Some Agent\n\n## Owning Department\n\n[Platform](../README.md)\n\n"
            "## Implemented Capability\n\n[Cap One](../capabilities/cap-one.md)\n\n"
            f"## Permitted Skills\n\n{permitted}\n\n"
            f"## Permitted Workflows\n\n{workflows}\n\n## Runtime Requirements\n\nx\n",
            encoding="utf-8")
        if workflow_exists:
            (catalog / "workflow" / "wf-one.md").write_text(
                "# wf-one\n\n## Composed Elements\n\n"
                f"- **Contains Skill:**\n  [s](../skill/{contains_skill}.md)\n"
                f"- **Invokes Agent Instance:** invoked by {invoker_phrase}\n"
                f"  [Some Agent]({invoker_link})\n\n## Compatibility\n\nx\n",
                encoding="utf-8")
        return root

    def _run(self, root):
        links, _ = w4_chain(read_departments(root), root)
        return w4_continuity(links, root)

    def test_the_positive_control_passes_on_the_same_fixture_shape(self):
        """Guard: the fixture must be capable of producing zero defects."""
        with tempfile.TemporaryDirectory() as tmp:
            chains, terminal, defects = self._run(self._corpus(tmp))
            self.assertEqual(defects, [], "fixture is broken, not the checker")
            self.assertEqual(len(chains), 1)
            self.assertEqual(terminal, [])

    def test_a_declared_workflow_with_no_record_is_seen(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, _, defects = self._run(self._corpus(tmp, workflow_exists=False))
            self.assertIn("workflow-missing", [d[0] for d in defects], defects)

    def test_a_workflow_that_does_not_cite_its_declarer_back_is_seen(self):
        """Reciprocity: without it the join is assumed rather than evidenced."""
        with tempfile.TemporaryDirectory() as tmp:
            _, _, defects = self._run(self._corpus(
                tmp, invoker_link="../../platform/agent-definitions/other-agent.md"))
            self.assertIn("workflow-not-reciprocal", [d[0] for d in defects], defects)

    def test_a_workflow_invoking_a_definition_rather_than_an_instance_is_seen(self):
        """`FD-P10-004 §6` — an Agent Instance must not be read as a Definition.

        `Domain Model §4` fixes the relationship as Workflow-invokes-Agent-*
        Instance*. A record naming the Definition as its direct invoker has
        collapsed the two, which is the misclassification the Decision forbids.
        """
        with tempfile.TemporaryDirectory() as tmp:
            _, _, defects = self._run(self._corpus(
                tmp, invoker_phrase="the Agent Definition"))
            self.assertIn(
                "workflow-invokes-definition-directly", [d[0] for d in defects], defects)

    def test_a_workflow_that_names_no_invoker_at_all_is_seen(self):
        """The remaining branch. A defect kind never shown to fire is not evidence."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._corpus(tmp)
            workflow = root / "execution-catalog/workflow/wf-one.md"
            body = workflow.read_text(encoding="utf-8")
            workflow.write_text(
                body[:body.index("- **Invokes Agent Instance:**")]
                + "\n## Compatibility\n\nx\n", encoding="utf-8")
            _, _, defects = self._run(root)
            self.assertEqual(
                [d[0] for d in defects], ["workflow-names-no-invoker"], defects)

    def test_a_workflow_containing_a_skill_its_invoker_may_not_use_is_seen(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, _, defects = self._run(self._corpus(tmp, contains_skill="skill-two"))
            self.assertIn("skill-not-permitted", [d[0] for d in defects], defects)

    def test_an_agent_definition_declaring_no_workflow_is_terminal_not_defective(self):
        with tempfile.TemporaryDirectory() as tmp:
            chains, terminal, defects = self._run(
                self._corpus(tmp, declare_workflow=False))
            self.assertEqual(defects, [], defects)
            self.assertEqual(chains, [])
            self.assertEqual(len(terminal), 1, terminal)

    def test_prose_citations_in_a_permission_section_are_not_read_as_declarations(self):
        """An ADR citation inside ``## Permitted Workflows`` is not a Workflow."""
        with tempfile.TemporaryDirectory() as tmp:
            root = self._corpus(tmp, declare_workflow=False)
            record = root / "platform/agent-definitions/some-agent.md"
            record.write_text(record.read_text(encoding="utf-8").replace(
                "## Permitted Workflows\n\nNone declared.",
                "## Permitted Workflows\n\nNone declared. Per "
                "[ADR-0007](../../../adr/decisions/ADR-0007.md) an empty "
                "declaration is valid."), encoding="utf-8")
            chains, terminal, defects = self._run(root)
            self.assertEqual(defects, [], defects)
            self.assertEqual(len(terminal), 1, terminal)


class WorkEntersTheDepartmentEcosystem(unittest.TestCase):
    """`P10-W8` test 1 (*work masuk*) and test 2 (*capability dipilih*).

    The Blueprint calls its ten integration tests *"Uji minimal"*. This closes
    the one that had no Department-side answer.
    """

    def test_every_owned_capability_resolves_to_an_accountable_department(self):
        for record in read_departments():
            for capability in record.capabilities:
                entry = resolve_work_entry(capability)
                self.assertEqual(entry.department, record.key)
                self.assertTrue(entry.agent_definition)
                self.assertRegex(entry.establishing_adr, r"^ADR-\d{4}$")

    def test_an_unknown_capability_fails_closed(self):
        """`INV-1` requires exactly one owner; a partial entry is not returned."""
        with self.assertRaises(WorkEntryUnresolved):
            resolve_work_entry("no-such-capability-anywhere")

    def test_the_entry_names_the_department_that_actually_owns_it(self):
        entry = resolve_work_entry("governance-artifact-integrity")
        self.assertEqual(entry.department, "platform")
        self.assertEqual(entry.agent_definition, "governance-artifact-integrity-agent")
        self.assertEqual(entry.establishing_adr, "ADR-0003")

    def test_it_is_not_a_work_entity(self):
        """`Freeze §4`: *"No new entity."*

        A resolution result is recomputed from records on every call and stores
        nothing. If this class ever gained identity, ownership, versioning, a
        lifecycle or a Trace, it would have become an entity — so the test
        asserts it has none of them.
        """
        entry = resolve_work_entry("engineering-intelligence")
        for forbidden in ("identity", "owner", "version", "lifecycle",
                          "state", "trace", "key"):
            self.assertFalse(
                hasattr(entry, forbidden),
                f"WorkEntry gained {forbidden!r} — it would now be an entity",
            )
        self.assertEqual(
            set(entry.__dataclass_fields__),
            {"capability", "department", "agent_definition", "establishing_adr"},
        )

    def test_it_is_recomputed_not_stored(self):
        a = resolve_work_entry("cognitive-intelligence")
        b = resolve_work_entry("cognitive-intelligence")
        self.assertEqual(a, b)
        self.assertIsNot(a, b, "a cached instance would be stored state")
