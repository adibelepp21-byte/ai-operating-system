"""
Workflow conformance tests (Blueprint §3/§25/§27; workflow_spec §1–§14;
Roadmap §9.8; Freeze §4/§5/§6, AD-9; INV-13/INV-4/INV-15/INV-12; ADR-0004;
ADR-0007; PR-3/PR-4).

Roadmap §9.8 fixes this boundary's completion as *"INV-13/4 tests pass."*
Baseline 02 adds INV-15, INV-12, ADR-0004 and ADR-0007 as gates. Each test
below asserts one of those, or one of the boundary rules the specification
states:

  - INV-13 — Workflow is the **sole** sanctioned multi-agent channel. Direct
             Instance-to-Instance collaboration is structurally
             unrepresentable, not merely rejected.
  - INV-4  — every step is an Agent-Instance action producing exactly one
             Trace; a step naming no actor cannot be constructed.
  - INV-15 — an Agent Definition may declare zero or more Workflows; empty is
             a valid architectural state (ADR-0007).
  - INV-12 — Tool is the only entity permitted an external dependency, so this
             boundary holds none.
  - ADR-0004 — Workflow is owned centrally (no owner field) and versioned
             independently (no version format imposed).
  - PR-4   — fail closed; PR-3 — detect, do not decide.
  - Reserved scope stays unbuilt — no execution, registry, retry, recovery.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.workflow.tests.test_workflow_conformance
"""

from __future__ import annotations

import ast
import sys
import unittest
from pathlib import Path

from native_core.core import workflow as workflow_pkg
from native_core.core.workflow import (
    AgentDefinitionRef,
    AgentInstanceRef,
    DirectCollaborationForbidden,
    DuplicateWorkflowDeclaration,
    InvalidWorkflow,
    InvalidWorkflowComposition,
    InvalidWorkflowDeclaration,
    InvalidWorkflowStep,
    SkillRef,
    UnresolvedWorkflow,
    Workflow,
    WorkflowComposition,
    WorkflowCoordination,
    WorkflowDeclaration,
    WorkflowError,
    WorkflowIdentity,
    WorkflowStep,
)

ALICE = AgentInstanceRef("instance-alice")
BOB = AgentInstanceRef("instance-bob")
CODING = SkillRef("coding")
TESTING = SkillRef("testing")


def _identity(key: str, version: str = "v1") -> WorkflowIdentity:
    return WorkflowIdentity(key, version)


def _workflow(key: str = "review-cycle", version: str = "v1") -> Workflow:
    return Workflow(_identity(key, version))


def _step(key: str, actor: AgentInstanceRef = ALICE, skill: SkillRef = CODING):
    return WorkflowStep(key, actor, skill)


class TestInv13SoleMultiAgentChannel(unittest.TestCase):
    """INV-13 — Workflow is the only sanctioned multi-agent channel."""

    def test_coordination_requires_a_workflow(self):
        """No Workflow, no coordination — the binding is the enforcement."""
        with self.assertRaises(DirectCollaborationForbidden):
            WorkflowCoordination(None, WorkflowComposition())

    def test_coordination_rejects_a_non_workflow_channel(self):
        with self.assertRaises(DirectCollaborationForbidden):
            WorkflowCoordination("direct-channel", WorkflowComposition())

    def test_multi_agent_coordination_is_legal_through_a_workflow(self):
        composition = WorkflowComposition(
            (_step("s1", ALICE), _step("s2", BOB, TESTING))
        )
        coordination = WorkflowCoordination(_workflow(), composition)
        self.assertTrue(coordination.is_multi_agent())
        self.assertEqual(len(coordination.participants()), 2)

    def test_agent_instance_ref_has_no_peer_field(self):
        """Structural enforcement: one Instance cannot name another.

        Freeze §6 forbids the `direct Instance↔Instance` direction. The
        absence of any peer/target/channel field makes that direction
        unrepresentable rather than merely disallowed."""
        self.assertEqual(
            set(AgentInstanceRef.__dataclass_fields__), {"agent_instance_key"}
        )

    def test_no_contract_exposes_a_peer_target_or_channel_field(self):
        forbidden = ("peer", "target", "recipient", "channel", "destination", "to_")
        for contract in (
            AgentInstanceRef,
            WorkflowStep,
            WorkflowComposition,
            WorkflowCoordination,
            Workflow,
            WorkflowIdentity,
            WorkflowDeclaration,
            AgentDefinitionRef,
            SkillRef,
        ):
            for field in contract.__dataclass_fields__:
                for term in forbidden:
                    self.assertNotIn(term, field.lower(), f"{contract.__name__}.{field}")

    def test_participants_are_derived_never_supplied(self):
        """A participant set cannot be asserted independently of a Workflow."""
        self.assertEqual(
            set(WorkflowCoordination.__dataclass_fields__),
            {"workflow", "composition"},
        )

    def test_participants_are_deduplicated_in_first_step_order(self):
        composition = WorkflowComposition(
            (_step("s1", ALICE), _step("s2", BOB), _step("s3", ALICE, TESTING))
        )
        coordination = WorkflowCoordination(_workflow(), composition)
        self.assertEqual(
            [p.agent_instance_key for p in coordination.participants()],
            ["instance-alice", "instance-bob"],
        )

    def test_single_agent_coordination_is_not_multi_agent(self):
        coordination = WorkflowCoordination(
            _workflow(), WorkflowComposition((_step("s1", ALICE),))
        )
        self.assertFalse(coordination.is_multi_agent())

    def test_coordinates_reports_membership_without_deciding(self):
        """PR-3: detect, don't decide. Membership is reported, not granted."""
        coordination = WorkflowCoordination(
            _workflow(), WorkflowComposition((_step("s1", ALICE),))
        )
        self.assertTrue(coordination.coordinates("instance-alice"))
        self.assertFalse(coordination.coordinates("instance-bob"))

    def test_no_message_event_channel_or_delegation_surface(self):
        """Domain Model §9: no Message/Event entity; no direct channel exists."""
        surface = " ".join(workflow_pkg.__all__).lower()
        for term in (
            "message",
            "event",
            "channel",
            "queue",
            "mailbox",
            "broadcast",
            "subscribe",
            "delegate",
            "handoff",
            "route",
        ):
            self.assertNotIn(term, surface)


class TestInv4EveryStepIsATraceProducingAction(unittest.TestCase):
    """INV-4 — every coordinated step is an action producing exactly one Trace."""

    def test_step_requires_an_acting_agent_instance(self):
        """A step with no actor could produce no Trace — unrepresentable."""
        with self.assertRaises(InvalidWorkflowStep):
            WorkflowStep("s1", None, CODING)

    def test_step_actor_must_be_an_agent_instance_ref(self):
        with self.assertRaises(InvalidWorkflowStep):
            WorkflowStep("s1", "instance-alice", CODING)

    def test_step_requires_a_composed_skill(self):
        with self.assertRaises(InvalidWorkflowStep):
            WorkflowStep("s1", ALICE, None)

    def test_step_fields_are_exactly_key_actor_and_skill(self):
        self.assertEqual(
            set(WorkflowStep.__dataclass_fields__),
            {"step_key", "performed_by", "composes"},
        )

    def test_every_step_yields_exactly_one_acting_instance(self):
        composition = WorkflowComposition(
            (_step("s1", ALICE), _step("s2", BOB), _step("s3", ALICE))
        )
        self.assertEqual(len(composition.acting_instances()), len(composition.ordered()))

    def test_empty_agent_instance_key_fails_closed(self):
        with self.assertRaises(InvalidWorkflowStep):
            AgentInstanceRef("   ")

    def test_empty_skill_key_fails_closed(self):
        with self.assertRaises(InvalidWorkflowStep):
            SkillRef("")

    def test_workflow_authors_no_trace(self):
        """workflow_spec §9: the step's actor authors the Trace, not the Workflow."""
        for contract in (Workflow, WorkflowIdentity, WorkflowComposition, WorkflowStep):
            for field in contract.__dataclass_fields__:
                self.assertNotIn("trace", field.lower())
        self.assertNotIn("trace", " ".join(workflow_pkg.__all__).lower())


class TestCompositionIsExplicitAndInspectable(unittest.TestCase):
    """Domain Model §2; workflow_spec §6 — 'keep composition checkable'."""

    def setUp(self):
        self.composition = WorkflowComposition(
            (_step("s1", ALICE, CODING), _step("s2", BOB, TESTING))
        )

    def test_order_is_preserved(self):
        self.assertEqual(self.composition.step_keys(), ("s1", "s2"))

    def test_composed_skills_are_readable(self):
        self.assertEqual(self.composition.composed_skills(), (CODING, TESTING))

    def test_duplicate_skill_across_steps_is_permitted(self):
        composition = WorkflowComposition((_step("s1", ALICE), _step("s2", BOB)))
        self.assertEqual(composition.composed_skills(), (CODING, CODING))

    def test_repeated_step_key_fails_closed(self):
        with self.assertRaises(InvalidWorkflowComposition):
            WorkflowComposition((_step("s1"), _step("s1", BOB)))

    def test_non_step_member_fails_closed(self):
        with self.assertRaises(InvalidWorkflowComposition):
            WorkflowComposition(("s1",))

    def test_non_tuple_composition_fails_closed(self):
        with self.assertRaises(InvalidWorkflowComposition):
            WorkflowComposition([_step("s1")])

    def test_empty_composition_is_valid(self):
        composition = WorkflowComposition()
        self.assertTrue(composition.is_empty())
        self.assertEqual(composition.ordered(), ())

    def test_empty_coordination_is_valid(self):
        coordination = WorkflowCoordination(_workflow(), WorkflowComposition())
        self.assertTrue(coordination.is_empty())
        self.assertEqual(coordination.participants(), ())
        self.assertFalse(coordination.is_multi_agent())


class TestInv15AndAdr0007DeclarationCardinality(unittest.TestCase):
    """INV-15 / ADR-0007 — zero or more Workflows; empty is valid."""

    AGENT = AgentDefinitionRef("engineering-intelligence-agent")

    def test_zero_declared_workflows_is_valid(self):
        declaration = WorkflowDeclaration(self.AGENT)
        self.assertTrue(declaration.is_empty())
        self.assertEqual(declaration.declared(), ())

    def test_empty_declaration_never_raises(self):
        try:
            WorkflowDeclaration(self.AGENT, ())
        except WorkflowError as exc:  # pragma: no cover - failure path
            self.fail(f"empty declaration must be valid, raised {exc!r}")

    def test_one_and_many_declarations_are_valid(self):
        one = (_identity("review-cycle"),)
        many = (_identity("review-cycle"), _identity("release"), _identity("triage"))
        self.assertEqual(WorkflowDeclaration(self.AGENT, one).declared(), one)
        self.assertEqual(WorkflowDeclaration(self.AGENT, many).declared(), many)

    def test_declaration_order_is_preserved(self):
        declared = (_identity("release"), _identity("review-cycle"))
        self.assertEqual(WorkflowDeclaration(self.AGENT, declared).declared(), declared)

    def test_declaring_agent_definition_is_mandatory(self):
        with self.assertRaises(InvalidWorkflowDeclaration):
            WorkflowDeclaration(None, ())

    def test_empty_agent_definition_key_fails_closed(self):
        with self.assertRaises(InvalidWorkflowDeclaration):
            AgentDefinitionRef("   ")

    def test_non_identity_member_fails_closed(self):
        with self.assertRaises(InvalidWorkflowDeclaration):
            WorkflowDeclaration(self.AGENT, ("review-cycle",))

    def test_non_tuple_declaration_fails_closed(self):
        with self.assertRaises(InvalidWorkflowDeclaration):
            WorkflowDeclaration(self.AGENT, [_identity("review-cycle")])

    def test_repeated_workflow_key_fails_closed(self):
        with self.assertRaises(DuplicateWorkflowDeclaration):
            WorkflowDeclaration(
                self.AGENT, (_identity("release"), _identity("release", "v2"))
            )

    def test_declaration_confers_no_ownership(self):
        """ADR-0004: specification and ownership are separate concerns."""
        self.assertNotIn("owner", " ".join(Workflow.__dataclass_fields__).lower())
        self.assertNotIn(
            "department", " ".join(Workflow.__dataclass_fields__).lower()
        )


class TestPr4FailClosedResolution(unittest.TestCase):
    """workflow_spec §11 — halt rather than proceed (PR-4)."""

    AGENT = AgentDefinitionRef("cognitive-intelligence-agent")

    def test_declared_workflow_resolves(self):
        declaration = WorkflowDeclaration(self.AGENT, (_identity("release", "v2"),))
        self.assertEqual(declaration.resolve("release"), _identity("release", "v2"))

    def test_undeclared_workflow_raises_rather_than_defaulting(self):
        with self.assertRaises(UnresolvedWorkflow):
            WorkflowDeclaration(self.AGENT, (_identity("release"),)).resolve("triage")

    def test_resolution_against_an_empty_declaration_fails_closed(self):
        with self.assertRaises(UnresolvedWorkflow):
            WorkflowDeclaration(self.AGENT).resolve("release")

    def test_failure_names_the_declaring_agent_definition(self):
        with self.assertRaises(UnresolvedWorkflow) as raised:
            WorkflowDeclaration(self.AGENT).resolve("release")
        self.assertIn("cognitive-intelligence-agent", str(raised.exception))

    def test_resolution_is_declaration_scoped_not_system_wide(self):
        WorkflowDeclaration(
            AgentDefinitionRef("other-agent"), (_identity("release"),)
        )
        with self.assertRaises(UnresolvedWorkflow):
            WorkflowDeclaration(self.AGENT).resolve("release")

    def test_every_failure_is_a_workflow_error(self):
        for error in (
            InvalidWorkflow,
            InvalidWorkflowStep,
            InvalidWorkflowComposition,
            InvalidWorkflowDeclaration,
            UnresolvedWorkflow,
            DuplicateWorkflowDeclaration,
            DirectCollaborationForbidden,
        ):
            self.assertTrue(issubclass(error, WorkflowError))


class TestAdr0004OwnershipAndLifecycle(unittest.TestCase):
    """ADR-0004 — owned centrally; versioned independently."""

    def test_workflow_carries_no_owning_department(self):
        """Owned centrally (ADR-0004) — the load-bearing difference from Capability."""
        self.assertEqual(set(Workflow.__dataclass_fields__), {"identity"})

    def test_workflow_carries_a_versioned_identity(self):
        self.assertEqual(_workflow("release", "v2").identity.workflow_version, "v2")

    def test_identity_requires_a_key_and_a_version(self):
        with self.assertRaises(InvalidWorkflow):
            WorkflowIdentity("", "v1")
        with self.assertRaises(InvalidWorkflow):
            WorkflowIdentity("release", "   ")

    def test_identity_must_be_an_identity(self):
        with self.assertRaises(InvalidWorkflow):
            Workflow("release")

    def test_no_version_format_is_imposed(self):
        for version in ("v1", "1.0", "2026-08-01", "draft"):
            self.assertEqual(
                WorkflowIdentity("release", version).workflow_version, version
            )


class TestInv12NoExternalDependency(unittest.TestCase):
    """INV-12 — Tool is the only entity permitted an external dependency."""

    PACKAGE = Path(workflow_pkg.__file__).parent
    FORBIDDEN_BOUNDARIES = {
        "runtime",
        "agent",
        "skill",
        "capability",
        "governance",
        "trace",
        "memory",
        "knowledge",
        "optimization",
        "infrastructure",
    }

    def _modules(self):
        return sorted(p for p in self.PACKAGE.rglob("*.py") if "tests" not in p.parts)

    def _imported(self, path):
        modules = []
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Import):
                modules += [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                if (node.level or 0) > 0:
                    continue
                modules.append(node.module or "")
        return modules

    def test_no_external_dependency(self):
        """Standard library only — nothing installed, fetched, or vendored."""
        allowed = set(sys.stdlib_module_names) | {"native_core"}
        offences = [
            (p.name, m)
            for p in self._modules()
            for m in self._imported(p)
            if m.split(".")[0] and m.split(".")[0] not in allowed
        ]
        self.assertEqual(offences, [])

    def test_no_other_core_boundary_import(self):
        """workflow_spec §8; Blueprint §26: no cross-boundary coupling."""
        offences = []
        for path in self._modules():
            for module in self._imported(path):
                hit = {p for p in module.split(".") if p} & self.FORBIDDEN_BOUNDARIES
                if hit:
                    offences.append((path.name, module, sorted(hit)))
        self.assertEqual(offences, [])

    def test_no_network_filesystem_or_process_access(self):
        forbidden = {
            "socket",
            "http",
            "urllib",
            "subprocess",
            "shutil",
            "os",
            "pathlib",
            "sqlite3",
            "asyncio",
            "threading",
        }
        offences = [
            (p.name, m)
            for p in self._modules()
            for m in self._imported(p)
            if m.split(".")[0] in forbidden
        ]
        self.assertEqual(offences, [])


class TestReservedScopeIsNotBuilt(unittest.TestCase):
    """workflow_spec §8/§12/§13/§14; Blueprint §25; Freeze §4/§6."""

    PACKAGE = Path(workflow_pkg.__file__).parent
    EXECUTION_VERBS = {
        "execute",
        "run",
        "invoke",
        "perform",
        "call",
        "act",
        "start",
        "apply",
        "dispatch",
        "schedule",
    }
    RESERVED_TERMS = ("registry", "register", "catalog", "discover", "index")
    RECOVERY_TERMS = ("retry", "rollback", "compensate", "recover", "timeout")

    def _modules(self):
        return sorted(p for p in self.PACKAGE.rglob("*.py") if "tests" not in p.parts)

    def _defs(self):
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    yield path.name, node.name

    def test_no_execution_surface(self):
        """workflow_spec §8: a Workflow 'is not the Runtime'."""
        offences = [
            (f, n) for f, n in self._defs() if n.lstrip("_").lower() in self.EXECUTION_VERBS
        ]
        self.assertEqual(offences, [])

    def test_no_registry_or_discovery(self):
        offences = [
            (f, n)
            for f, n in self._defs()
            for t in self.RESERVED_TERMS
            if t in n.lower()
        ]
        self.assertEqual(offences, [])

    def test_no_failure_recovery_model(self):
        """workflow_spec §13/§14 [O]: reserved; fail-closed baseline holds."""
        offences = [
            (f, n)
            for f, n in self._defs()
            for t in self.RECOVERY_TERMS
            if t in n.lower()
        ]
        self.assertEqual(offences, [])

    def test_no_async_or_threading(self):
        offences = []
        for path in self._modules():
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, (ast.AsyncFunctionDef, ast.Await)):
                    offences.append(path.name)
        self.assertEqual(offences, [])

    def test_no_module_level_mutable_state(self):
        """No registry can hide in module state — none exists to hide in."""
        offences = []
        for path in self._modules():
            for node in ast.parse(path.read_text()).body:
                targets = []
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                for target in targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("__"):
                        offences.append((path.name, target.id))
        self.assertEqual(offences, [])

    def test_capability_composition_is_not_modelled(self):
        """`Workflow realizes Capability` is **canonical** since `DEC-F03-046`
        (Freeze §6 frozen table; Domain Model §4; `workflow_spec §7` synchronized
        under `DEC-F03-047` S-1). This guard's basis therefore changed: it no
        longer holds a reservation open, it holds the **construction gate**.

        The relationship being ratified does **not** authorize modelling it —
        `ACT-CC-F03-047 §6` expressly withholds authority to create
        `WorkflowCapabilityRef` or any equivalent runtime structure, and Blueprint
        §10 admits the relation **by reference only, with no import of
        `core/capability/`**. Until a construction Act grants that authority the
        package must still expose nothing named for it. **The assertion below is
        unchanged; only this cited authority was corrected.**"""
        self.assertNotIn("capability", " ".join(workflow_pkg.__all__).lower())

    def test_runtime_relationship_is_not_modelled(self):
        """workflow_spec §14 [O]: Runtime↔Workflow is Inferred, not frozen."""
        self.assertNotIn("runtime", " ".join(workflow_pkg.__all__).lower())

    def test_public_surface_is_exactly_the_declared_exports(self):
        self.assertEqual(
            set(workflow_pkg.__all__),
            {
                "AgentDefinitionRef",
                "AgentInstanceRef",
                "DirectCollaborationForbidden",
                "DuplicateWorkflowDeclaration",
                "InvalidWorkflow",
                "InvalidWorkflowComposition",
                "InvalidWorkflowDeclaration",
                "InvalidWorkflowStep",
                "SkillRef",
                "UnresolvedWorkflow",
                "Workflow",
                "WorkflowComposition",
                "WorkflowCoordination",
                "WorkflowDeclaration",
                "WorkflowError",
                "WorkflowIdentity",
                "WorkflowStep",
            },
        )


class TestImmutabilityAndDeterminism(unittest.TestCase):
    """Frozen contracts; same input, same result — no hidden state."""

    CONTRACTS = (
        Workflow,
        WorkflowIdentity,
        WorkflowStep,
        WorkflowComposition,
        WorkflowCoordination,
        WorkflowDeclaration,
        AgentDefinitionRef,
        AgentInstanceRef,
        SkillRef,
    )

    def test_contracts_are_frozen(self):
        for contract in self.CONTRACTS:
            self.assertTrue(
                contract.__dataclass_params__.frozen,
                f"{contract.__name__} must be frozen",
            )

    def test_workflow_is_immutable(self):
        wf = _workflow()
        with self.assertRaises(Exception):
            wf.identity = _identity("other")

    def test_composition_is_immutable(self):
        composition = WorkflowComposition()
        with self.assertRaises(Exception):
            composition.steps = (_step("s1"),)

    def test_identity_is_hashable_and_comparable(self):
        self.assertEqual(_identity("release"), _identity("release"))
        self.assertEqual(len({_identity("release"), _identity("release")}), 1)
        self.assertLess(_identity("release"), _identity("triage"))

    def test_coordination_is_deterministic(self):
        composition = WorkflowComposition((_step("s1", ALICE), _step("s2", BOB)))
        first = WorkflowCoordination(_workflow(), composition)
        second = WorkflowCoordination(_workflow(), composition)
        self.assertEqual(first.participants(), second.participants())
        self.assertEqual(first.participants(), first.participants())


if __name__ == "__main__":
    unittest.main()
