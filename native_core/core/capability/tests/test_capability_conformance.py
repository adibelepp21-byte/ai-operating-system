"""
Capability conformance tests (Blueprint §7/§27; capability_spec §1–§12;
Roadmap §9.6; Freeze INV-1/INV-9/INV-10/INV-11/INV-14; PR-3/PR-4).

Roadmap §9.6 fixes this boundary's completion as *"INV-1/9/10/11/14 tests
pass."* Each test below asserts one of those, or one of the boundary rules the
specification states:

  - INV-1  — a Capability is owned by exactly one Department.
  - INV-9  — every dependency is explicit and references a specific versioned
             contract.
  - INV-10 — a cross-Department dependency requires a governance record;
             silent adoption fails closed.
  - INV-11 — the graph is queryable and observable in both directions; an
             unresolvable target is an undocumented dependency and fails
             closed.
  - INV-14 — a zero-implementer Capability is *flagged*, never raised
             (Detect Don't Decide, PR-3).
  - Dependency rules — this package imports nothing from Governance, Agent,
    Skill, Workflow, Runtime, Trace, Memory, Knowledge, Optimization or
    Infrastructure, and holds no external dependency (capability_spec §7/§8;
    INV-12).
  - No execution surface — capability_spec §5/§8, Freeze §4.
  - Immutability — contracts are frozen; the graph exposes no mutable view.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.capability.tests.test_capability_conformance
"""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

from native_core.core import capability as capability_pkg
from native_core.core.capability import (
    Capability,
    CapabilityDependency,
    CapabilityGraph,
    CapabilityIdentity,
    DepartmentRef,
    GovernanceRecord,
    InvalidCapability,
    InvalidCapabilityDependency,
    UndocumentedCapabilityDependency,
    UngovernedCrossDepartmentDependency,
)

PLATFORM = DepartmentRef("platform")
OTHER = DepartmentRef("other-department")


def _identity(key: str, version: str = "v1") -> CapabilityIdentity:
    return CapabilityIdentity(key, version)


def _capability(key, department=PLATFORM, dependencies=(), version="v1"):
    return Capability(_identity(key, version), department, tuple(dependencies))


class TestInv1SingleDepartmentOwnership(unittest.TestCase):
    """INV-1 — every Capability is owned by exactly one Department."""

    def test_capability_carries_exactly_one_department(self):
        cap = _capability("alpha")
        self.assertIsInstance(cap.owning_department, DepartmentRef)
        self.assertEqual(cap.owning_department.department_key, "platform")

    def test_ownership_is_mandatory(self):
        with self.assertRaises(InvalidCapability):
            Capability(_identity("alpha"), None, ())

    def test_ownership_must_be_a_department_reference(self):
        with self.assertRaises(InvalidCapability):
            Capability(_identity("alpha"), "platform", ())

    def test_empty_department_key_fails_closed(self):
        with self.assertRaises(InvalidCapability):
            DepartmentRef("   ")

    def test_no_second_ownership_field_exists(self):
        """Exactly one owner — the contract offers no way to name a second."""
        fields = set(Capability.__dataclass_fields__)
        self.assertEqual(
            fields, {"identity", "owning_department", "dependencies"}
        )


class TestInv9ExplicitVersionedDependencies(unittest.TestCase):
    """INV-9 — dependencies are explicit and reference a versioned contract."""

    def test_dependency_target_is_a_versioned_identity(self):
        dependency = CapabilityDependency(_identity("beta", "v2"))
        self.assertEqual(dependency.depends_on.capability_version, "v2")

    def test_identity_requires_a_version(self):
        with self.assertRaises(InvalidCapability):
            CapabilityIdentity("beta", "")

    def test_identity_requires_a_key(self):
        with self.assertRaises(InvalidCapability):
            CapabilityIdentity("", "v1")

    def test_unversioned_target_is_rejected(self):
        with self.assertRaises(InvalidCapabilityDependency):
            CapabilityDependency("beta")

    def test_non_dependency_member_is_rejected(self):
        with self.assertRaises(InvalidCapabilityDependency):
            Capability(_identity("alpha"), PLATFORM, ("beta",))

    def test_self_dependency_fails_closed(self):
        """capability_spec §7 [E] admits dependencies on *other* Capabilities.

        A Capability naming itself is not depending on another Capability, so
        it fails closed (PR-4). Before this check the graph accepted it and
        reported the Capability as its own dependent."""
        with self.assertRaises(InvalidCapabilityDependency):
            _capability("alpha", dependencies=[CapabilityDependency(_identity("alpha"))])

    def test_self_dependency_is_rejected_at_construction_not_only_in_graph(self):
        """The check belongs to Capability: it is an intra-Capability fact,
        visible without assembling the rest of the graph."""
        with self.assertRaises(InvalidCapabilityDependency):
            Capability(
                _identity("solo"),
                PLATFORM,
                (CapabilityDependency(_identity("solo")),),
            )

    def test_dependency_on_a_different_capability_is_admitted(self):
        """The check must reject only self-reference, never a real dependency."""
        cap = _capability("alpha", dependencies=[CapabilityDependency(_identity("beta"))])
        self.assertEqual(cap.dependencies[0].depends_on.capability_key, "beta")

    def test_version_mismatch_is_not_a_specific_contract(self):
        beta = _capability("beta", version="v2")
        alpha = _capability(
            "alpha", dependencies=[CapabilityDependency(_identity("beta", "v1"))]
        )
        with self.assertRaises(UndocumentedCapabilityDependency):
            CapabilityGraph([alpha, beta])

    def test_matching_version_resolves(self):
        beta = _capability("beta", version="v2")
        alpha = _capability(
            "alpha", dependencies=[CapabilityDependency(_identity("beta", "v2"))]
        )
        graph = CapabilityGraph([alpha, beta])
        self.assertEqual(
            graph.dependencies_of("alpha"), (_identity("beta", "v2"),)
        )


class TestInv10CrossDepartmentGovernance(unittest.TestCase):
    """INV-10 — cross-Department dependencies require governance; never silent."""

    def test_ungoverned_cross_department_dependency_fails_closed(self):
        beta = _capability("beta", department=OTHER)
        alpha = _capability(
            "alpha", dependencies=[CapabilityDependency(_identity("beta"))]
        )
        with self.assertRaises(UngovernedCrossDepartmentDependency):
            CapabilityGraph([alpha, beta])

    def test_governed_cross_department_dependency_is_admitted(self):
        beta = _capability("beta", department=OTHER)
        alpha = _capability(
            "alpha",
            dependencies=[
                CapabilityDependency(
                    _identity("beta"), GovernanceRecord("ADR-0003")
                )
            ],
        )
        graph = CapabilityGraph([alpha, beta])
        self.assertEqual(
            graph.cross_department_dependencies(),
            ((_identity("alpha"), _identity("beta")),),
        )

    def test_same_department_dependency_needs_no_record(self):
        beta = _capability("beta")
        alpha = _capability(
            "alpha", dependencies=[CapabilityDependency(_identity("beta"))]
        )
        graph = CapabilityGraph([alpha, beta])
        self.assertEqual(graph.cross_department_dependencies(), ())

    def test_governance_record_requires_a_reference(self):
        with self.assertRaises(InvalidCapability):
            GovernanceRecord("")

    def test_governance_record_is_never_evaluated_for_authority(self):
        """Presence is asserted; authority is never interpreted (PR-3).

        Any non-empty reference is accepted — this boundary holds no rule
        about what makes a decision valid."""
        beta = _capability("beta", department=OTHER)
        alpha = _capability(
            "alpha",
            dependencies=[
                CapabilityDependency(
                    _identity("beta"), GovernanceRecord("any-reference")
                )
            ],
        )
        self.assertIsInstance(CapabilityGraph([alpha, beta]), CapabilityGraph)


class TestInv11QueryableObservableGraph(unittest.TestCase):
    """INV-11 — the graph is queryable and observable; nothing undocumented."""

    def setUp(self):
        self.gamma = _capability("gamma")
        self.beta = _capability(
            "beta", dependencies=[CapabilityDependency(_identity("gamma"))]
        )
        self.alpha = _capability(
            "alpha", dependencies=[CapabilityDependency(_identity("beta"))]
        )
        self.graph = CapabilityGraph([self.alpha, self.beta, self.gamma])

    def test_every_capability_is_queryable(self):
        self.assertEqual(
            set(self.graph.capabilities()), {"alpha", "beta", "gamma"}
        )

    def test_forward_direction_is_observable(self):
        self.assertEqual(self.graph.dependencies_of("beta"), (_identity("gamma"),))

    def test_reverse_direction_is_observable(self):
        self.assertEqual(self.graph.dependents_of("gamma"), (_identity("beta"),))
        self.assertEqual(self.graph.dependents_of("alpha"), ())

    def test_unresolvable_target_is_undocumented_and_fails_closed(self):
        alpha = _capability(
            "alpha", dependencies=[CapabilityDependency(_identity("missing"))]
        )
        with self.assertRaises(UndocumentedCapabilityDependency):
            CapabilityGraph([alpha])

    def test_unknown_capability_query_fails_closed(self):
        with self.assertRaises(InvalidCapability):
            self.graph.capability("nope")

    def test_duplicate_key_fails_closed(self):
        with self.assertRaises(InvalidCapability):
            CapabilityGraph([_capability("alpha"), _capability("alpha")])

    def test_non_capability_member_fails_closed(self):
        with self.assertRaises(InvalidCapability):
            CapabilityGraph(["alpha"])


class TestInv14OrphanCapabilitiesAreFlagged(unittest.TestCase):
    """INV-14 — zero-implementer capabilities are flagged, never raised."""

    def setUp(self):
        self.graph = CapabilityGraph([_capability("alpha"), _capability("beta")])

    def test_zero_implementers_is_flagged_not_raised(self):
        flagged = self.graph.orphan_capabilities({"alpha": 1, "beta": 0})
        self.assertEqual(flagged, (_identity("beta"),))

    def test_absent_from_mapping_counts_as_zero(self):
        self.assertEqual(
            self.graph.orphan_capabilities({}),
            (_identity("alpha"), _identity("beta")),
        )

    def test_all_implemented_flags_nothing(self):
        self.assertEqual(
            self.graph.orphan_capabilities({"alpha": 2, "beta": 1}), ()
        )

    def test_flagging_takes_no_action(self):
        """Detect Don't Decide (PR-3): the graph is unchanged by flagging."""
        before = dict(self.graph.capabilities())
        self.graph.orphan_capabilities({})
        self.assertEqual(dict(self.graph.capabilities()), before)


class TestBoundaryRules(unittest.TestCase):
    """capability_spec §5/§7/§8; Freeze §4; INV-12; Blueprint §7."""

    PACKAGE = Path(capability_pkg.__file__).parent
    FORBIDDEN_BOUNDARIES = {
        "governance",
        "agent",
        "skill",
        "workflow",
        "runtime",
        "trace",
        "memory",
        "knowledge",
        "optimization",
        "infrastructure",
    }
    EXECUTION_VERBS = {
        "execute",
        "run",
        "invoke",
        "perform",
        "call",
        "realize",
        "act",
        "start",
    }

    def _modules(self):
        return sorted(
            p for p in self.PACKAGE.rglob("*.py") if "tests" not in p.parts
        )

    def test_no_forbidden_boundary_import(self):
        """capability_spec §7: its Department and other Capabilities only."""
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    modules = [node.module or ""]
                for module in modules:
                    parts = {p for p in module.split(".") if p}
                    hit = parts & self.FORBIDDEN_BOUNDARIES
                    if hit:
                        offences.append((path.name, module, sorted(hit)))
        self.assertEqual(offences, [])

    def test_no_external_dependency(self):
        """INV-12: Tool is the only entity permitted an external dependency."""
        allowed = set(sys.stdlib_module_names) | {"native_core"}
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                modules = []
                if isinstance(node, ast.Import):
                    modules = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    if (node.level or 0) > 0:
                        continue
                    modules = [node.module or ""]
                for module in modules:
                    top = module.split(".")[0]
                    if top and top not in allowed:
                        offences.append((path.name, module))
        self.assertEqual(offences, [])

    def test_no_execution_surface(self):
        """Freeze §4 / capability_spec §5/§8: must not execute itself."""
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = node.name.lstrip("_").lower()
                    if name in self.EXECUTION_VERBS:
                        offences.append((path.name, node.name))
        self.assertEqual(offences, [])

    def test_no_async_or_threading(self):
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, (ast.AsyncFunctionDef, ast.Await)):
                    offences.append(path.name)
        self.assertEqual(offences, [])

    def test_contracts_are_frozen(self):
        for contract in (
            Capability,
            CapabilityDependency,
            CapabilityIdentity,
            DepartmentRef,
            GovernanceRecord,
        ):
            self.assertTrue(
                contract.__dataclass_params__.frozen,
                f"{contract.__name__} must be frozen",
            )

    def test_capability_is_immutable(self):
        cap = _capability("alpha")
        with self.assertRaises(Exception):
            cap.identity = _identity("other")

    def test_graph_exposes_no_mutable_capability_view(self):
        graph = CapabilityGraph([_capability("alpha")])
        with self.assertRaises(TypeError):
            graph.capabilities()["beta"] = _capability("beta")

    def test_skill_and_workflow_composition_is_not_modelled(self):
        """Freeze §10 / Blueprint §7 / capability_spec §12: Inferred, reserved."""
        surface = " ".join(dir(capability_pkg)).lower()
        self.assertNotIn("skill", surface)
        self.assertNotIn("workflow", surface)

    def test_public_surface_is_exactly_the_declared_exports(self):
        """The surface grew when the Phase-3 ownership stub was realized.

        The original set captured the boundary as built in Phase 3, where
        `NCIR §9.6` [E] recorded its Department dependency as a *"(Phase-5
        stub)"* and [O] recorded it as *"Blocked by: Department ownership
        (Phase 5) for **full realization**"*. Blueprint §4 [E] places that
        ownership context here — *"Spine (capability + the ownership context it
        lives in)"* — and Blueprint §7 [E] lists *"its Department"* among this
        package's allowed dependencies.

        The realization was authorized by FOUNDER `DEC-DEPT-REALIZATION =
        AUTHORIZE` and located here by `ACT-CC-F03-036` Outcome A. The surface
        therefore grows by the ratified Freeze §4 entities `Organization` and
        `Department` and their ownership graph — and by nothing else. No new
        entity was created; both were already two of the twelve.

        It then grew once more by `DisputedCapabilityOwnership` under
        `ACT-CC-F03-037`. That is a *named failure mode*, not an addition to
        the architecture: INV-1 [E] already requires a Capability be *"owned by
        exactly one Department"*, and `capability_spec §11` [E] already
        requires that an invalid ownership state fail closed (PR-4). Realizing
        Department ownership put INV-1 on both sides of the edge — the
        Capability's `DepartmentRef` and the Department's `owned_capabilities`
        — so the two can now contradict each other. The exception names that
        contradiction. No new invariant, entity, boundary, lifecycle or
        governance semantic accompanies it.

        It grew once more by `ConflictingAgentDefinitionOwnership` under
        `ACT-CC-F03-038`, for the same reason. Freeze §4 [E] gives a Department
        two ownership responsibilities — it *"owns Capabilities **and Agent
        Definitions**"* — and INV-2 [E] fixes the second: *"Every Agent
        Definition is owned by exactly one Department."* Realizing the half
        that was left unbuilt needs a name for its violation. Ownership is held
        as ratified `agent_definition_key` values, so no dependency on Agent is
        created (department_spec §8), and INV-2's second clause is deliberately
        not enforced — that is Agent construction discipline, [O]-reserved to
        the Architect by `agent_spec §12`/`§13`.

        `DisputedAgentDefinitionOwnership` followed under `ACT-CC-F03-039`
        (`DEC-AGENT-DEPT-OWNERSHIP = OPTION A`), when the Agent Definition side
        of the INV-2 clause 1 edge was realized and the two sides could
        therefore contradict each other for the first time."""
        self.assertEqual(
            set(capability_pkg.__all__),
            {
                # Capability — as built in Phase 3
                "Capability",
                "CapabilityDependency",
                "CapabilityError",
                "CapabilityGraph",
                "CapabilityIdentity",
                "DepartmentRef",
                "GovernanceRecord",
                "InvalidCapability",
                "InvalidCapabilityDependency",
                "UndocumentedCapabilityDependency",
                "UngovernedCrossDepartmentDependency",
                # Ownership context — Phase 5 realization (Freeze §4 entities)
                "ConflictingAgentDefinitionOwnership",
                "DisputedAgentDefinitionOwnership",
                "ConflictingCapabilityOwnership",
                "DisputedCapabilityOwnership",
                "Department",
                "DepartmentIdentity",
                "InvalidDepartment",
                "InvalidOrganization",
                "Organization",
                "OrganizationIdentity",
                "OwnershipGraph",
                "UnknownDepartment",
                "UnknownOrganization",
            },
        )


class TestDeterminism(unittest.TestCase):
    """Same input, same graph — no hidden state, no ordering surprise."""

    def test_graph_construction_is_deterministic(self):
        members = [
            _capability("gamma"),
            _capability(
                "beta", dependencies=[CapabilityDependency(_identity("gamma"))]
            ),
            _capability(
                "alpha", dependencies=[CapabilityDependency(_identity("beta"))]
            ),
        ]
        first = CapabilityGraph(members)
        second = CapabilityGraph(members)
        self.assertEqual(
            list(first.capabilities()), list(second.capabilities())
        )
        self.assertEqual(
            first.dependents_of("gamma"), second.dependents_of("gamma")
        )


if __name__ == "__main__":
    unittest.main()
