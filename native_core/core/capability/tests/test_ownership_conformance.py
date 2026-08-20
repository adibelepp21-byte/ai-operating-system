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
  - PR-3   — unowned and unresolvable references are *flagged*, never raised,
    when the corpus is surveyed.
  - PR-4   — malformed structure and unresolvable references fail closed.
  - R-4    — `DepartmentRef` resolves to a realized Department.
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
    ConflictingCapabilityOwnership,
    Department,
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


def _dept(key: str, organization: str = "aios", capabilities=()) -> Department:
    return Department(
        DepartmentIdentity(key), OrganizationIdentity(organization), tuple(capabilities)
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
        self.assertEqual(
            set(Department.__dataclass_fields__),
            {"identity", "organization", "owned_capabilities"},
        )

    def test_entities_expose_no_execution_surface(self):
        banned = {"run", "execute", "act", "invoke", "call", "perform", "start"}
        for entity in (Organization, Department, OwnershipGraph):
            self.assertEqual({n for n in dir(entity) if not n.startswith("_")} & banned, set())


if __name__ == "__main__":
    unittest.main()
