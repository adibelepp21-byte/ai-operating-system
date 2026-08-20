"""
Ownership-context conformance tests (Freeze §4 Spine; Blueprint §4/§7;
department_spec; organization_spec; INV-1; PR-3/PR-4).

Blueprint §4 [E] defines the Spine as *"capability + the ownership context it
lives in"*, and §7 [E] lists this package's allowed dependencies as *"its
Department; other Capabilities via governed versioned contracts"*. These tests
assert the realization matches Freeze §4's ratified definitions of Organization
and Department, and adds nothing to them:

  - Freeze §4 — a Department is owned by an Organization; an Organization is
    the hierarchy root with nothing above it.
  - INV-1  — a Capability is owned by *exactly one* Department; two claimants
    fail closed.
  - INV-2  — clause 1 only: an Agent Definition is owned by *exactly one*
    Department. Clause 2 (*implements ≥1 Capability*) is Agent construction
    discipline, [O]-reserved to the Architect by `agent_spec §12`/`§13`.
  - PR-3   — unowned and unresolvable references are *flagged*, never raised,
    when the corpus is surveyed.
  - PR-4   — malformed structure and unresolvable references fail closed.
  - R-4    — `DepartmentRef` resolves to a realized Department, and the two
    sides of the ownership edge must agree before it is treated as ownership.
  - No new boundary — realization lives inside the capability package; the core
    region still holds exactly eleven boundaries.
  - Reserved structure absent — no roles, workforce, budgets, KPIs, lifecycle
    states or Department nesting.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.capability.tests.test_ownership_conformance
"""

from __future__ import annotations

import unittest
from pathlib import Path

from native_core.core.capability import (
    Capability,
    CapabilityIdentity,
    ConflictingAgentDefinitionOwnership,
    ConflictingCapabilityOwnership,
    Department,
    DisputedCapabilityOwnership,
    DepartmentIdentity,
    DepartmentRef,
    InvalidDepartment,
    InvalidOrganization,
    Organization,
    OrganizationIdentity,
    OwnershipGraph,
    UnknownDepartment,
    UnknownOrganization,
)

ORG = OrganizationIdentity("aios")


def _org(key: str = "aios") -> Organization:
    return Organization(OrganizationIdentity(key))


def _dept(
    key: str, organization: str = "aios", capabilities=(), definitions=()
) -> Department:
    return Department(
        DepartmentIdentity(key),
        OrganizationIdentity(organization),
        tuple(capabilities),
        tuple(definitions),
    )


def _capability(key: str, department: str) -> Capability:
    return Capability(CapabilityIdentity(key, "v1"), DepartmentRef(department))


class TestFreezeSpineParentEdge(unittest.TestCase):
    """Freeze §4 — a Department is owned by an Organization."""

    def test_department_names_exactly_one_organization(self):
        self.assertEqual(_dept("platform").organization, ORG)

    def test_organization_parent_is_mandatory(self):
        with self.assertRaises(InvalidDepartment):
            Department(DepartmentIdentity("platform"), None)

    def test_organization_parent_must_be_an_organization_identity(self):
        with self.assertRaises(InvalidDepartment):
            Department(DepartmentIdentity("platform"), "aios")

    def test_unresolvable_parent_fails_closed(self):
        with self.assertRaises(UnknownOrganization):
            OwnershipGraph([_org("aios")], [_dept("platform", "absent-org")])

    def test_organization_has_nothing_above_it(self):
        """Freeze §4: *"Dependencies: none above it."*"""
        self.assertEqual(set(Organization.__dataclass_fields__), {"identity"})

    def test_empty_keys_fail_closed(self):
        with self.assertRaises(InvalidOrganization):
            OrganizationIdentity("")
        with self.assertRaises(InvalidDepartment):
            DepartmentIdentity("")


class TestInv1ExactlyOneOwningDepartment(unittest.TestCase):
    """INV-1 — every Capability is owned by exactly one Department."""

    def test_single_owner_resolves(self):
        graph = OwnershipGraph([_org()], [_dept("platform", capabilities=["cap.a"])])
        self.assertEqual(graph.owner_of("cap.a").identity, DepartmentIdentity("platform"))

    def test_two_departments_claiming_one_capability_fails_closed(self):
        with self.assertRaises(ConflictingCapabilityOwnership):
            OwnershipGraph(
                [_org()],
                [
                    _dept("platform", capabilities=["cap.a"]),
                    _dept("other", capabilities=["cap.a"]),
                ],
            )

    def test_a_department_may_not_claim_the_same_capability_twice(self):
        with self.assertRaises(InvalidDepartment):
            _dept("platform", capabilities=["cap.a", "cap.a"])

    def test_capability_with_no_owner_fails_closed_on_lookup(self):
        graph = OwnershipGraph([_org()], [_dept("platform")])
        with self.assertRaises(UnknownDepartment):
            graph.owner_of("cap.a")

    def test_duplicate_department_key_fails_closed(self):
        with self.assertRaises(InvalidDepartment):
            OwnershipGraph([_org()], [_dept("platform"), _dept("platform")])

    def test_duplicate_organization_key_fails_closed(self):
        with self.assertRaises(InvalidOrganization):
            OwnershipGraph([_org(), _org()], [])

    def test_non_department_member_fails_closed(self):
        with self.assertRaises(InvalidDepartment):
            OwnershipGraph([_org()], ["platform"])

    def test_non_organization_member_fails_closed(self):
        with self.assertRaises(InvalidOrganization):
            OwnershipGraph(["aios"], [])


class TestPr3DetectDontDecide(unittest.TestCase):
    """PR-3 — gaps are flagged for governance, never raised mid-survey."""

    def setUp(self):
        self.graph = OwnershipGraph([_org()], [_dept("platform", capabilities=["cap.a"])])

    def test_unowned_capabilities_are_flagged_not_raised(self):
        self.assertEqual(self.graph.unowned_capabilities(["cap.a", "cap.b"]), ("cap.b",))

    def test_fully_owned_corpus_flags_nothing(self):
        self.assertEqual(self.graph.unowned_capabilities(["cap.a"]), ())

    def test_dangling_references_surveyed_without_halting(self):
        capabilities = [_capability("cap.a", "platform"), _capability("cap.z", "absent")]
        self.assertEqual(self.graph.unresolved_ownership(capabilities), ("cap.z",))


class TestQueryableOwnership(unittest.TestCase):
    """department_spec §5 — resolvable and queryable."""

    def setUp(self):
        self.graph = OwnershipGraph(
            [_org()], [_dept("platform", capabilities=["cap.a"]), _dept("other")]
        )

    def test_department_resolves_from_a_reference(self):
        self.assertEqual(
            self.graph.department("platform").identity, DepartmentIdentity("platform")
        )

    def test_unknown_reference_fails_closed(self):
        with self.assertRaises(UnknownDepartment):
            self.graph.department("absent")

    def test_organization_owns_its_departments(self):
        self.assertEqual(
            self.graph.departments_of("aios"),
            (DepartmentIdentity("other"), DepartmentIdentity("platform")),
        )

    def test_unknown_organization_query_fails_closed(self):
        with self.assertRaises(UnknownOrganization):
            self.graph.departments_of("absent")

    def test_views_are_immutable(self):
        with self.assertRaises(TypeError):
            self.graph.departments()["injected"] = None
        with self.assertRaises(TypeError):
            self.graph.organizations()["injected"] = None


class TestR4DepartmentRefBinding(unittest.TestCase):
    """R-4 — `DepartmentRef` resolves to its realized referent."""

    def setUp(self):
        self.graph = OwnershipGraph([_org()], [_dept("platform", capabilities=["cap.a"])])

    def test_reference_resolves_to_its_referent(self):
        capability = _capability("cap.a", "platform")
        (resolved, department), = self.graph.resolve([capability])
        self.assertIs(resolved, capability)
        self.assertEqual(department.identity, DepartmentIdentity("platform"))

    def test_dangling_reference_fails_closed(self):
        with self.assertRaises(UnknownDepartment):
            self.graph.resolve([_capability("cap.z", "absent")])

    def test_binding_rejects_non_capabilities(self):
        with self.assertRaises(UnknownDepartment):
            self.graph.resolve(["not-a-capability"])

    def test_stub_still_accepts_any_key_without_a_graph(self):
        """The stub alone cannot verify INV-1 — that is what realization adds."""
        self.assertEqual(DepartmentRef("anything-at-all").department_key, "anything-at-all")


class TestOwnershipEdgeAgreement(unittest.TestCase):
    """INV-1 is represented on both sides; the two must agree.

    A Capability names its owner (`DepartmentRef`) and a Department names what
    it owns (`owned_capabilities`). Two representations of one fact can
    contradict each other, and *"owned by exactly one Department"* is not
    satisfied by a claim the named owner does not acknowledge."""

    def setUp(self):
        self.graph = OwnershipGraph(
            [_org()],
            [
                _dept("platform", capabilities=["cap.b", "cap.c"]),
                _dept("research"),
            ],
        )

    def test_agreeing_edge_resolves(self):
        (_, department), = self.graph.resolve([_capability("cap.c", "platform")])
        self.assertEqual(department.identity, DepartmentIdentity("platform"))

    def test_named_owner_that_does_not_claim_it_fails_closed(self):
        """PR-4 — the contradiction is not resolved by preferring a side."""
        with self.assertRaises(DisputedCapabilityOwnership):
            self.graph.resolve([_capability("cap.b", "research")])

    def test_dispute_names_both_sides(self):
        with self.assertRaises(DisputedCapabilityOwnership) as raised:
            self.graph.resolve([_capability("cap.b", "research")])
        message = str(raised.exception)
        self.assertIn("research", message)
        self.assertIn("platform", message)
        self.assertIn("INV-1", message)

    def test_disputes_are_surveyed_not_halted_on(self):
        """PR-3 — a reconciliation pass sees every dispute, not just the first."""
        disputes = self.graph.disputed_ownership(
            [
                _capability("cap.b", "research"),
                _capability("cap.c", "platform"),
            ]
        )
        self.assertEqual(disputes, (("cap.b", "research", "platform"),))

    def test_survey_reports_no_claimant_as_none(self):
        graph = OwnershipGraph([_org()], [_dept("research")])
        self.assertEqual(
            graph.disputed_ownership([_capability("cap.q", "research")]),
            (("cap.q", "research", None),),
        )

    def test_unresolvable_reference_is_not_reported_as_a_dispute(self):
        """Naming no Department at all is a different condition."""
        corpus = [_capability("cap.z", "absent")]
        self.assertEqual(self.graph.disputed_ownership(corpus), ())
        self.assertEqual(self.graph.unresolved_ownership(corpus), ("cap.z",))

    def test_claims_with_no_capability_behind_them_are_flagged_never_raised(self):
        """PR-3 — over a partial corpus this is incompleteness, not a verdict."""
        self.assertEqual(
            self.graph.unbacked_ownership_claims([_capability("cap.b", "platform")]),
            (("platform", "cap.c"),),
        )

    def test_a_fully_reconciled_corpus_reports_nothing(self):
        corpus = [_capability("cap.b", "platform"), _capability("cap.c", "platform")]
        self.assertEqual(self.graph.disputed_ownership(corpus), ())
        self.assertEqual(self.graph.unresolved_ownership(corpus), ())
        self.assertEqual(self.graph.unbacked_ownership_claims(corpus), ())
        self.assertEqual(len(self.graph.resolve(corpus)), 2)


class TestInv2AgentDefinitionOwnership(unittest.TestCase):
    """INV-2 clause 1 — an Agent Definition is owned by exactly one Department.

    Freeze §4 [E] gives a Department both ownership responsibilities: it *"owns
    Capabilities **and Agent Definitions**"*. Ownership is held as ratified
    `agent_definition_key` values, so this package never imports Agent."""

    def setUp(self):
        self.graph = OwnershipGraph(
            [_org()],
            [
                _dept("platform", capabilities=["cap.a"],
                      definitions=["ad.builder", "ad.linter"]),
                _dept("research", definitions=["ad.prober"]),
            ],
        )

    def test_definition_resolves_to_its_owning_department(self):
        owner = self.graph.owner_of_agent_definition("ad.linter")
        self.assertEqual(owner.identity, DepartmentIdentity("platform"))

    def test_two_departments_claiming_one_definition_fails_closed(self):
        with self.assertRaises(ConflictingAgentDefinitionOwnership):
            OwnershipGraph(
                [_org()],
                [
                    _dept("platform", definitions=["ad.linter"]),
                    _dept("ops", definitions=["ad.linter"]),
                ],
            )

    def test_one_department_claiming_a_definition_twice_fails_closed(self):
        with self.assertRaises(InvalidDepartment):
            _dept("platform", definitions=["ad.a", "ad.a"])

    def test_unknown_definition_fails_closed(self):
        with self.assertRaises(UnknownDepartment):
            self.graph.owner_of_agent_definition("ad.absent")

    def test_definitions_of_a_department_are_queryable(self):
        self.assertEqual(
            self.graph.agent_definitions_of("platform"), ("ad.builder", "ad.linter")
        )

    def test_unowned_definitions_are_flagged_never_raised(self):
        """PR-3 — the caller supplies the keys, so no capability→agent edge."""
        self.assertEqual(
            self.graph.unowned_agent_definitions(["ad.builder", "ad.ghost"]),
            ("ad.ghost",),
        )

    def test_ownership_defaults_to_empty(self):
        self.assertEqual(_dept("platform").owned_agent_definitions, ())

    def test_definition_keys_must_be_non_empty_text(self):
        with self.assertRaises(InvalidDepartment):
            _dept("platform", definitions=[""])
        with self.assertRaises(InvalidDepartment):
            _dept("platform", definitions=[None])

    def test_capability_and_definition_ownership_are_independent(self):
        """The same key may name a Capability and a Definition; the two sets
        are distinct namespaces and must not collide with each other."""
        graph = OwnershipGraph(
            [_org()],
            [
                _dept("platform", capabilities=["shared.key"]),
                _dept("research", definitions=["shared.key"]),
            ],
        )
        self.assertEqual(graph.owner_of("shared.key").identity.department_key, "platform")
        self.assertEqual(
            graph.owner_of_agent_definition("shared.key").identity.department_key,
            "research",
        )

    def test_inv2_second_clause_is_not_enforced_here(self):
        """`agent_spec §12`/`§13` [O] reserve Agent construction discipline —
        validating a Definition against Capabilities — to the Architect. A
        Department owning a Definition while owning no Capability at all is
        therefore accepted by this boundary, and that silence is deliberate."""
        graph = OwnershipGraph([_org()], [_dept("research", definitions=["ad.prober"])])
        self.assertEqual(graph.agent_definitions_of("research"), ("ad.prober",))
        self.assertEqual(graph.departments()["research"].owned_capabilities, ())

    def test_no_agent_import_is_introduced(self):
        """department_spec §8 [E] — must not depend on Agent."""
        source = (Path(__file__).resolve().parents[1] / "ownership.py").read_text()
        self.assertNotIn("import agent", source)
        self.assertNotIn("from native_core.core.agent", source)


class TestNoNewBoundary(unittest.TestCase):
    """Blueprint §4 — the core region holds exactly eleven boundaries."""

    def test_core_region_still_holds_eleven_boundaries(self):
        core = Path(__file__).resolve().parents[2]
        self.assertEqual(core.name, "core")
        present = {
            p.name for p in core.iterdir() if p.is_dir() and not p.name.startswith("__")
        }
        self.assertEqual(len(present), 11, f"core boundaries: {sorted(present)}")

    def test_ownership_lives_inside_the_capability_boundary(self):
        package = Path(__file__).resolve().parents[1]
        self.assertEqual(package.name, "capability")
        self.assertTrue((package / "ownership.py").is_file())


class TestReservedStructureAbsent(unittest.TestCase):
    """Reserved structure must not be invented during realization."""

    def test_no_reserved_field_on_department(self):
        reserved = {
            "roles", "workforce", "budget", "kpis", "state", "lifecycle",
            "parent_department", "skills", "workflows",
        }
        fields = set(Department.__dataclass_fields__)
        self.assertEqual(fields & reserved, set())

    def test_department_has_exactly_the_freeze_shape(self):
        """Freeze §4 [E]: a Department *"owns Capabilities **and Agent
        Definitions**"*, and is *"owned by Organization"*. Both ownership sets
        are named by the ratified entry, and INV-2 [E] fixes the second —
        *"Every Agent Definition is owned by exactly one Department."*

        `owned_agent_definitions` was added under `ACT-CC-F03-038`. It is not
        new structure: the earlier expectation encoded only half of the shape
        this test's own authority states. Nothing beyond those two ownership
        sets and the identity/parent edge may appear here."""
        self.assertEqual(
            set(Department.__dataclass_fields__),
            {
                "identity",
                "organization",
                "owned_capabilities",
                "owned_agent_definitions",
            },
        )

    def test_entities_expose_no_execution_surface(self):
        banned = {"run", "execute", "act", "invoke", "call", "perform", "start"}
        for entity in (Organization, Department, OwnershipGraph):
            self.assertEqual({n for n in dir(entity) if not n.startswith("_")} & banned, set())


if __name__ == "__main__":
    unittest.main()
