"""
Agent conformance tests (Blueprint §3/§8/§26/§27/§31; agent_spec §1–§14;
Freeze §4/§5 layer 3; INV-2/INV-3/INV-4/INV-8/INV-12/INV-13; PR-3/PR-4).

Baseline 04C — a **verification** baseline. It verifies the existing structure
of the Agent boundary and introduces no behavior.

Each test asserts one ratified requirement, or one boundary rule the
specification states:

  - INV-2  — Definition ownership and Capability implementation are **reserved**
             (agent_spec §12/§13, Agent Factory). The suite verifies the
             reservation is intact, not that the bindings exist.
  - INV-3  — an Agent Instance instantiates exactly one Agent Definition,
             enforced structurally. Its second clause (hosted by exactly one
             Runtime) is deliberately unmodelled; that absence is verified.
  - INV-4  — Agent authors no Trace. Trace's ratified field names are mirrored
             exactly, and the dependency runs in neither direction.
  - INV-12 — no external dependency; the sole cross-boundary import is the
             `ExecutionConsumer` contract.
  - INV-13 — the sole entry point is `participate(execution)`; no peer channel
             exists.
  - PR-4   — fail closed: an incomplete Definition or Instance is refused,
             never coerced.

Verification is structural (AST, dataclass, signature, abstract-interface and
public-API inspection) in preference to runtime simulation.

**No source file is modified by this suite.** Findings are reported as evidence.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.agent.tests.test_agent_conformance
"""

from __future__ import annotations

import ast
import dataclasses
import inspect
import sys
import unittest
from pathlib import Path

from native_core.core import agent as agent_pkg
from native_core.core.agent import Agent
from native_core.core.agent.definition import AgentDefinition, InvalidAgentDefinition
from native_core.core.agent.instance import AgentInstance, InvalidAgentInstance
from native_core.core.runtime.execution.consumer import ExecutionConsumer
from native_core.core.trace.record import REQUIRED_FIELDS

PACKAGE = Path(agent_pkg.__file__).parent
CORE = PACKAGE.parent
BOUNDARY = "agent"
ROOT_PACKAGE = "native_core.core"


# --------------------------------------------------------------------------
# structural helpers
# --------------------------------------------------------------------------


def _modules():
    """Every non-test source module of this boundary."""
    return sorted(p for p in PACKAGE.rglob("*.py") if "tests" not in p.parts)


def _tree(path):
    return ast.parse(path.read_text())


def _dotted(path):
    parts = path.relative_to(PACKAGE).with_suffix("").parts
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join((ROOT_PACKAGE, BOUNDARY) + parts)


def _containing_package(path):
    dotted = _dotted(path)
    return dotted if path.name == "__init__.py" else dotted.rsplit(".", 1)[0]


def _resolve(path, module, level):
    """Resolve one import to an absolute module name.

    `level` is the number of leading dots. Resolving it is what distinguishes
    `from .definition import` (level 1 — the SAME boundary) from
    `from ..runtime.execution.consumer import` (level 2 — another boundary).
    Substring matching cannot make that distinction and reports the first as a
    cross-boundary import."""
    if level == 0:
        return module
    base = _containing_package(path).split(".")
    if level > 1:
        base = base[: -(level - 1)]
    return ".".join(base + ([module] if module else []))


def _import_records():
    """(path, resolved_module, names) for every import in the boundary."""
    records = []
    for path in _modules():
        for node in ast.walk(_tree(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    records.append((path, alias.name, (alias.name,)))
            elif isinstance(node, ast.ImportFrom):
                resolved = _resolve(path, node.module or "", node.level or 0)
                records.append((path, resolved, tuple(a.name for a in node.names)))
    return records


def _boundary_of(dotted):
    prefix = ROOT_PACKAGE + "."
    if not dotted.startswith(prefix):
        return None
    return dotted[len(prefix) :].split(".")[0]


def _cross_boundary_records():
    return [
        (path, module, names)
        for path, module, names in _import_records()
        if _boundary_of(module) not in (None, BOUNDARY)
    ]


def _definitions():
    """(filename, node) for every class and function defined in the boundary."""
    for path in _modules():
        for node in ast.walk(_tree(path)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                yield path.name, node


def _identifiers():
    """(filename, identifier) for every name, attribute, argument, and
    definition name. Docstrings and comments are excluded by construction."""
    for path in _modules():
        for node in ast.walk(_tree(path)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                yield path.name, node.name
            elif isinstance(node, ast.Name):
                yield path.name, node.id
            elif isinstance(node, ast.Attribute):
                yield path.name, node.attr
            elif isinstance(node, ast.arg):
                yield path.name, node.arg


def _class_node(filename, class_name):
    for name, node in _definitions():
        if name == filename and isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise AssertionError(f"{class_name} not found in {filename}")


def _field_types(klass):
    """(name, annotation-as-text). Source modules use postponed annotations, so
    field types arrive as strings; normalising keeps assertions readable."""
    return [
        (f.name, f.type if isinstance(f.type, str) else f.type.__name__)
        for f in dataclasses.fields(klass)
    ]


def _definition(key="analyst", version="1.0.0"):
    return AgentDefinition(agent_definition_key=key, agent_definition_version=version)


# --------------------------------------------------------------------------
# Agent contract integrity
# --------------------------------------------------------------------------


class TestAgentContractIntegrity(unittest.TestCase):
    """agent_spec §1; Blueprint §8 — the contract answers exactly one question:
    how an Agent enters the execution system."""

    def test_an_agent_is_an_execution_consumer(self):
        self.assertTrue(issubclass(Agent, ExecutionConsumer))

    def test_the_contract_is_abstract_and_cannot_be_instantiated(self):
        self.assertTrue(inspect.isabstract(Agent))
        with self.assertRaises(TypeError):
            Agent()

    def test_participate_is_the_sole_abstract_responsibility(self):
        self.assertEqual({"participate"}, set(Agent.__abstractmethods__))

    def test_participate_is_inherited_not_redeclared(self):
        """Agent adds nothing to the consumer contract — it *is* one. The entry
        point resolves to the consumer's own declaration, not a copy."""
        self.assertNotIn("participate", vars(Agent))
        self.assertIs(ExecutionConsumer.participate, Agent.participate)

    def test_the_sole_entry_point_takes_only_the_bound_execution(self):
        """INV-13: the one parameter is the Execution boundary, so there is no
        second route in and no route to a peer."""
        self.assertEqual(
            ["self", "execution"],
            list(inspect.signature(Agent.participate).parameters),
        )

    def test_the_contract_declares_no_member_of_its_own(self):
        """AST: the class body is a docstring and nothing else — no identity, no
        metadata, no state, no lifecycle, no policy, no model."""
        node = _class_node("agent.py", "Agent")
        self.assertEqual(1, len(node.body))
        self.assertIsInstance(node.body[0], ast.Expr)
        self.assertIsInstance(node.body[0].value, ast.Constant)

    def test_the_contract_exposes_no_public_attribute(self):
        public = {n for n in vars(Agent) if not n.startswith("_")}
        self.assertEqual(set(), public)

    def test_the_contract_is_not_a_data_carrier(self):
        """A behavioural abstraction, not a record: no fields, no dataclass."""
        self.assertFalse(dataclasses.is_dataclass(Agent))


class TestAgentEntersOnlyThroughExecution(unittest.TestCase):
    """agent_spec §1; Blueprint §8 — Agent reaches Runtime only via Execution,
    so no `Runtime → Agent` dependency and no cycle can arise."""

    def test_the_only_cross_boundary_import_is_the_consumer_contract(self):
        records = _cross_boundary_records()
        self.assertEqual(1, len(records), records)
        _, module, names = records[0]
        self.assertEqual(f"{ROOT_PACKAGE}.runtime.execution.consumer", module)
        self.assertEqual(("ExecutionConsumer",), names)

    def test_the_runtime_contract_is_never_imported_directly(self):
        """Importing `Runtime` here would let an Agent bypass the Execution
        boundary."""
        for path, module, names in _import_records():
            self.assertNotEqual(f"{ROOT_PACKAGE}.runtime.contract", module, path.name)
            self.assertNotEqual(f"{ROOT_PACKAGE}.runtime", module, path.name)
            self.assertNotIn("Runtime", names, path.name)
            self.assertNotIn("AIOSRuntime", names, path.name)

    def test_no_runtime_identifier_exists_in_the_boundary(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(
                identifier,
                ("Runtime", "AIOSRuntime", "runtime", "runtime_id"),
                f"{filename}: {identifier}",
            )

    def test_the_execution_layer_is_never_reached_beyond_the_consumer(self):
        """The Execution session, context, and composition root are not imported
        — an Agent receives the boundary, it does not build one."""
        for path, module, names in _import_records():
            for forbidden in (
                "ExecutionSession",
                "ExecutionContext",
                "create_execution_layer",
                "Execution",
            ):
                self.assertNotIn(forbidden, names, f"{path.name} imports {forbidden}")


# --------------------------------------------------------------------------
# Agent Definition — immutable data contract
# --------------------------------------------------------------------------


class TestAgentDefinitionDataContract(unittest.TestCase):
    """agent_spec §3/§4 — a Definition answers *what kind of Agent is this*, and
    nothing else."""

    def test_it_is_a_frozen_dataclass(self):
        self.assertTrue(dataclasses.is_dataclass(AgentDefinition))
        self.assertTrue(AgentDefinition.__dataclass_params__.frozen)
        self.assertFalse(inspect.isabstract(AgentDefinition))

    def test_it_carries_exactly_identity_and_version(self):
        self.assertEqual(
            [("agent_definition_key", "str"), ("agent_definition_version", "str")],
            _field_types(AgentDefinition),
        )

    def test_it_cannot_be_mutated(self):
        definition = _definition()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            definition.agent_definition_key = "other"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            definition.agent_definition_version = "2.0.0"

    def test_it_is_hashable_and_compared_by_value(self):
        self.assertEqual(_definition(), _definition())
        self.assertEqual(1, len({_definition(), _definition()}))
        self.assertNotEqual(_definition(version="1.0.0"), _definition(version="2.0.0"))

    def test_it_fails_closed_on_an_incomplete_specification(self):
        """PR-4: an incomplete Definition is refused, never coerced."""
        for kwargs in (
            {"agent_definition_key": "", "agent_definition_version": "1"},
            {"agent_definition_key": "   ", "agent_definition_version": "1"},
            {"agent_definition_key": None, "agent_definition_version": "1"},
            {"agent_definition_key": 1, "agent_definition_version": "1"},
            {"agent_definition_key": "k", "agent_definition_version": ""},
            {"agent_definition_key": "k", "agent_definition_version": "   "},
            {"agent_definition_key": "k", "agent_definition_version": None},
            {"agent_definition_key": "k", "agent_definition_version": 1},
        ):
            with self.assertRaises(InvalidAgentDefinition):
                AgentDefinition(**kwargs)

    def test_both_fields_are_required(self):
        with self.assertRaises(TypeError):
            AgentDefinition(agent_definition_key="k")
        for field in dataclasses.fields(AgentDefinition):
            self.assertIs(dataclasses.MISSING, field.default, field.name)
            self.assertIs(dataclasses.MISSING, field.default_factory, field.name)

    def test_a_definition_is_descriptive_and_never_acts(self):
        """Only an Agent Instance acts. A Definition declares no behaviour."""
        node = _class_node("definition.py", "AgentDefinition")
        methods = [
            n.name for n in node.body if isinstance(n, ast.FunctionDef)
        ]
        self.assertEqual(["__post_init__"], methods)
        for verb in (
            "participate",
            "execute",
            "run",
            "invoke",
            "think",
            "reason",
            "plan",
            "schedule",
            "act",
        ):
            self.assertFalse(hasattr(AgentDefinition, verb), verb)

    def test_a_definition_is_not_an_execution_consumer(self):
        self.assertFalse(issubclass(AgentDefinition, ExecutionConsumer))
        self.assertFalse(issubclass(AgentDefinition, Agent))


# --------------------------------------------------------------------------
# Agent Instance — INV-3
# --------------------------------------------------------------------------


class TestAgentInstanceIdentityContract(unittest.TestCase):
    """INV-3 — *"Every Agent Instance instantiates exactly one Agent
    Definition"*, expressed structurally rather than checked at runtime."""

    def test_it_is_a_frozen_dataclass(self):
        self.assertTrue(dataclasses.is_dataclass(AgentInstance))
        self.assertTrue(AgentInstance.__dataclass_params__.frozen)

    def test_it_carries_exactly_identity_and_one_definition(self):
        self.assertEqual(
            [("agent_instance", "str"), ("agent_definition", "AgentDefinition")],
            _field_types(AgentInstance),
        )

    def test_exactly_one_definition_is_structurally_required(self):
        """INV-3: the field is a single required `AgentDefinition` — not
        optional, not defaulted, and not a collection. An Instance realising
        zero or many Definitions is unrepresentable."""
        field = {f.name: f for f in dataclasses.fields(AgentInstance)}["agent_definition"]
        self.assertEqual("AgentDefinition", field.type)
        self.assertIs(dataclasses.MISSING, field.default)
        self.assertIs(dataclasses.MISSING, field.default_factory)
        with self.assertRaises(TypeError):
            AgentInstance(agent_instance="i")

    def test_a_collection_of_definitions_is_refused(self):
        """Many-Definitions is refused at construction, closing the runtime path
        the type annotation closes structurally."""
        for value in (
            [_definition()],
            (_definition(), _definition()),
            {_definition()},
            None,
            "analyst",
        ):
            with self.assertRaises(InvalidAgentInstance):
                AgentInstance(agent_instance="i", agent_definition=value)

    def test_it_fails_closed_on_an_incomplete_identity(self):
        for value in ("", "   ", None, 1, True):
            with self.assertRaises(InvalidAgentInstance):
                AgentInstance(agent_instance=value, agent_definition=_definition())

    def test_it_cannot_be_mutated(self):
        instance = AgentInstance(agent_instance="i", agent_definition=_definition())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            instance.agent_instance = "other"
        with self.assertRaises(dataclasses.FrozenInstanceError):
            instance.agent_definition = _definition(key="other")

    def test_it_is_hashable_and_compared_by_value(self):
        first = AgentInstance(agent_instance="i", agent_definition=_definition())
        second = AgentInstance(agent_instance="i", agent_definition=_definition())
        self.assertEqual(first, second)
        self.assertEqual(1, len({first, second}))

    def test_the_realized_definition_is_preserved_unchanged(self):
        definition = _definition()
        self.assertIs(
            definition,
            AgentInstance(agent_instance="i", agent_definition=definition).agent_definition,
        )

    def test_the_hosting_clause_of_inv3_is_deliberately_unmodelled(self):
        """INV-3's second clause — *hosted by exactly one Runtime* — is not
        represented here.

        `instance.py` states the reason directly: binding an Instance to its
        host is Runtime's concern, and modelling it here would either create the
        forbidden `Agent Instance → Runtime` dependency or add a speculative
        field. This test verifies the absence as found; it does not assert that
        the absence is correct or that it should be filled."""
        names = {f.name for f in dataclasses.fields(AgentInstance)}
        for absent in ("runtime", "runtime_id", "host", "hosted_by", "hosting_runtime"):
            self.assertNotIn(absent, names)
        instance_imports = [
            module for path, module, _ in _import_records() if path.name == "instance.py"
        ]
        self.assertEqual([f"{ROOT_PACKAGE}.agent.definition"], [
            m for m in instance_imports if _boundary_of(m) is not None
        ])

    def test_an_instance_is_not_itself_an_actor_here(self):
        """Only an Agent Instance acts — but *acting* is declared by the Agent
        contract's `participate`, realised in a future phase, not here."""
        self.assertFalse(issubclass(AgentInstance, ExecutionConsumer))
        self.assertFalse(issubclass(AgentInstance, Agent))
        for verb in ("participate", "execute", "run", "invoke", "activate", "deactivate"):
            self.assertFalse(hasattr(AgentInstance, verb), verb)


# --------------------------------------------------------------------------
# INV-4 / OQ-2 — Agent authors no Trace
# --------------------------------------------------------------------------


class TestTraceIndependenceAndFieldAlignment(unittest.TestCase):
    """INV-4; Domain Model §2.1 — Trace records the acting Definition version
    and Instance, and depends on nothing here."""

    def test_no_trace_identifier_exists_in_the_boundary(self):
        for filename, identifier in _identifiers():
            self.assertNotIn("trace", identifier.lower(), f"{filename}: {identifier}")

    def test_no_trace_boundary_import_exists(self):
        for path, module, _ in _import_records():
            self.assertNotEqual("trace", _boundary_of(module), path.name)

    def test_trace_imports_nothing_from_agent(self):
        """The dependency runs in neither direction: Trace records identity that
        is handed to it as arguments, so no `Trace → Agent` edge exists."""
        trace_package = CORE / "trace"
        for path in sorted(trace_package.rglob("*.py")):
            if "tests" in path.parts:
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom):
                    self.assertNotIn("agent", node.module or "", path.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertNotIn("agent", alias.name, path.name)

    def test_the_ratified_trace_field_names_are_mirrored_exactly(self):
        """No terminology drift: the identity fields declared here are named
        identically to the Trace required contents that record them."""
        self.assertIn("agent_definition_version", REQUIRED_FIELDS)
        self.assertIn("agent_instance", REQUIRED_FIELDS)
        self.assertIn(
            "agent_definition_version", {f.name for f in dataclasses.fields(AgentDefinition)}
        )
        self.assertIn("agent_instance", {f.name for f in dataclasses.fields(AgentInstance)})


# --------------------------------------------------------------------------
# INV-13 — no peer channel
# --------------------------------------------------------------------------


class TestNoAgentToAgentChannel(unittest.TestCase):
    """INV-13 — coordination runs through Workflow only. Nothing here carries
    one Agent Instance to another."""

    FORBIDDEN = frozenset(
        {
            "peer",
            "peers",
            "peer_instance",
            "target_agent",
            "to_agent",
            "from_agent",
            "collaborator",
            "channel",
            "send",
            "receive",
            "notify",
            "broadcast",
            "dispatch",
            "publish",
            "subscribe",
            "mailbox",
            "inbox",
            "outbox",
        }
    )

    def test_no_peer_channel_identifier_exists(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.FORBIDDEN, filename)

    def test_no_agent_holds_a_reference_to_another_agent(self):
        """No field of any contract here is typed as an Agent or Instance."""
        for klass in (AgentDefinition, AgentInstance):
            for name, annotation in _field_types(klass):
                self.assertNotIn(annotation, ("Agent", "AgentInstance"), name)

    def test_no_workflow_or_skill_dependency_is_taken(self):
        """Collaboration is Workflow's concern; this boundary does not reach it."""
        for path, module, _ in _import_records():
            self.assertNotIn(
                _boundary_of(module), ("workflow", "skill", "capability"), path.name
            )


# --------------------------------------------------------------------------
# dependency direction — INV-12 and module isolation
# --------------------------------------------------------------------------


class TestDependencyDirection(unittest.TestCase):
    """Blueprint §26; INV-12 — the boundary depends only on the Execution
    consumer contract, holds no external dependency, and closes no cycle."""

    PERMITTED_BOUNDARIES = frozenset({"runtime"})
    FORBIDDEN_BOUNDARIES = frozenset(
        {
            "knowledge",
            "memory",
            "governance",
            "trace",
            "infrastructure",
            "capability",
            "skill",
            "workflow",
            "optimization",
        }
    )
    STDLIB = frozenset({"__future__", "dataclasses"})

    def test_cross_boundary_imports_are_only_the_permitted_one(self):
        reached = {_boundary_of(m) for _, m, _ in _cross_boundary_records()}
        self.assertEqual(self.PERMITTED_BOUNDARIES, reached)

    def test_no_forbidden_boundary_is_imported(self):
        for path, module, _ in _cross_boundary_records():
            self.assertNotIn(
                _boundary_of(module),
                self.FORBIDDEN_BOUNDARIES,
                f"{path.name} imports {module}",
            )

    def test_no_external_dependency_exists(self):
        """INV-12: Tool is the only entity permitted an external dependency."""
        for path, module, _ in _import_records():
            if _boundary_of(module) is not None:
                continue
            root = module.split(".")[0]
            self.assertIn(root, self.STDLIB, f"{path.name} imports {module}")
            self.assertTrue(
                root in sys.stdlib_module_names or root == "__future__",
                f"{root} is not standard library",
            )

    def test_internal_relative_imports_stay_in_boundary(self):
        """Anti-false-positive: `from .definition import` (level 1) is a
        same-boundary import. Resolving the relative level distinguishes it from
        `from ..runtime… import` (level 2); substring matching does not."""
        internal = [
            (path.name, module)
            for path, module, _ in _import_records()
            if _boundary_of(module) == BOUNDARY
        ]
        self.assertTrue(internal, "the boundary must have internal wiring")
        for filename, module in internal:
            self.assertTrue(module.startswith(f"{ROOT_PACKAGE}.{BOUNDARY}"), filename)

    def test_no_boundary_outside_agent_depends_on_agent(self):
        """No reverse edge, therefore no cycle: Runtime and every other boundary
        remain unaware of Agent."""
        offenders = []
        for path in sorted(CORE.rglob("*.py")):
            relative = path.relative_to(CORE).parts
            if "tests" in relative or (relative and relative[0] == BOUNDARY):
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom) and "agent" in (node.module or ""):
                    offenders.append((str(path), node.module))
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if "agent" in alias.name:
                            offenders.append((str(path), alias.name))
        self.assertEqual([], offenders)

    def test_the_boundary_never_re_enters_itself_absolutely(self):
        """Internal wiring is relative throughout. This inspects the import **as
        written** (`level == 0`), not the resolved name, which by design is
        always `native_core.core.agent.*` for internal imports."""
        for path in _modules():
            for node in ast.walk(_tree(path)):
                if isinstance(node, ast.Import):
                    written = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom) and (node.level or 0) == 0:
                    written = [node.module or ""]
                else:
                    continue
                for module in written:
                    self.assertFalse(
                        module.startswith(f"{ROOT_PACKAGE}.{BOUNDARY}"), path.name
                    )


# --------------------------------------------------------------------------
# public API surface — and recorded finding F-3
# --------------------------------------------------------------------------


class TestPublicApiSurface(unittest.TestCase):
    """Blueprint §26 — the boundary exposes exactly its declared surface."""

    def test_exports_are_exactly_the_declared_name(self):
        self.assertEqual(["Agent"], list(agent_pkg.__all__))
        self.assertTrue(hasattr(agent_pkg, "Agent"))

    def test_no_export_leaks_another_boundary(self):
        for name in agent_pkg.__all__:
            module = getattr(getattr(agent_pkg, name), "__module__", "")
            self.assertTrue(
                module.startswith(f"{ROOT_PACKAGE}.{BOUNDARY}"),
                f"{name} is exported from {module}",
            )

    def test_the_declared_surface_matches_the_documented_surface(self):
        for name in agent_pkg.__all__:
            self.assertIn(name, agent_pkg.__doc__ or "")

    def test_recorded_finding_f3_the_data_contracts_are_off_the_public_surface(self):
        """**RECORDED FINDING F-3 — Category B, pre-recorded evidence.**

        The package declares `Public surface: agent: Agent` and exports `Agent`
        alone, while `definition.py` and `instance.py` define four further
        public names — `AgentDefinition`, `InvalidAgentDefinition`,
        `AgentInstance`, `InvalidAgentInstance` — that are reachable only
        through their own modules.

        This test records the state as found. It is **not** a repair and **not**
        a judgement that the exports are required; P7-I19 reserves disposition
        to the Architect. Source is unmodified by this baseline."""
        defined = {
            node.name
            for _, node in _definitions()
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
        }
        undeclared = sorted(defined - set(agent_pkg.__all__))
        self.assertEqual(
            [
                "AgentDefinition",
                "AgentInstance",
                "InvalidAgentDefinition",
                "InvalidAgentInstance",
            ],
            undeclared,
        )
        for name in undeclared:
            self.assertFalse(hasattr(agent_pkg, name), name)


# --------------------------------------------------------------------------
# reserved construction discipline — INV-2 and the Agent Factory
# --------------------------------------------------------------------------


class TestReservedConstructionDiscipline(unittest.TestCase):
    """agent_spec §12/§13 place governed construction of Definitions and
    Instances — the *Agent Factory* — in Phase 4, **[O] reserved to the
    Architect**. These tests verify the reservation is intact: nothing
    unreserved was introduced in its place."""

    def test_no_composition_root_exists(self):
        self.assertFalse((PACKAGE / "composition.py").exists())

    def test_no_bootstrap_entry_exists(self):
        self.assertFalse((PACKAGE / "bootstrap.py").exists())

    def test_no_module_level_function_exists_anywhere(self):
        """No factory, no builder, no registrar — the boundary declares types
        only. (Method definitions inside a class are unaffected.)"""
        module_level = [
            (path.name, node.name)
            for path in _modules()
            for node in _tree(path).body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        self.assertEqual([], module_level)

    def test_no_factory_or_registry_identifier_exists(self):
        forbidden = frozenset(
            {
                "create_agent",
                "build_agent",
                "make_agent",
                "factory",
                "registry",
                "register",
                "lookup",
                "resolve",
                "instantiate",
            }
        )
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, forbidden, filename)

    def test_inv2_bindings_remain_unmodelled(self):
        """INV-2 — a Definition is owned by exactly one Department and
        implements at least one Capability. Neither binding is declared here;
        both belong to the reserved Agent Factory.

        This records the reservation as found. It does not assert that the
        absence is correct — INV-2 conformance cannot be verified until the
        reserved phase supplies the bindings, and that gap is reported as
        evidence, not resolved here."""
        names = {f.name for f in dataclasses.fields(AgentDefinition)}
        for absent in (
            "department",
            "owner",
            "owned_by",
            "capabilities",
            "capability",
            "implements",
            "skills",
            "workflows",
            "tools",
        ):
            self.assertNotIn(absent, names)

    def test_no_model_provider_or_prompt_surface_exists(self):
        """Agent behaviour, reasoning, prompts, and model invocation belong to
        later authorized phases and are absent."""
        forbidden = frozenset(
            {
                "model",
                "provider",
                "prompt",
                "prompts",
                "llm",
                "inference",
                "temperature",
                "system_prompt",
                "reason",
                "think",
            }
        )
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, forbidden, filename)


# --------------------------------------------------------------------------
# fail-closed taxonomy — PR-4
# --------------------------------------------------------------------------


class TestFailClosedTaxonomy(unittest.TestCase):
    """PR-4; agent_spec §11 — an incomplete contract is refused, never coerced."""

    def test_both_errors_are_value_errors(self):
        for error in (InvalidAgentDefinition, InvalidAgentInstance):
            self.assertTrue(issubclass(error, ValueError), error.__name__)

    def test_the_errors_are_distinct(self):
        self.assertFalse(issubclass(InvalidAgentDefinition, InvalidAgentInstance))
        self.assertFalse(issubclass(InvalidAgentInstance, InvalidAgentDefinition))

    def test_every_halt_message_is_a_string(self):
        """AST: each raise passes a single string, so no halt reaches an
        operator as a structured object needing interpretation."""
        raises = 0
        for path in _modules():
            for node in ast.walk(_tree(path)):
                if not isinstance(node, ast.Raise) or not isinstance(node.exc, ast.Call):
                    continue
                raises += 1
                for argument in node.exc.args:
                    self.assertIsInstance(
                        argument,
                        (ast.Constant, ast.JoinedStr),
                        f"{path.name}:{node.lineno}",
                    )
                    if isinstance(argument, ast.Constant):
                        self.assertIsInstance(argument.value, str)
        self.assertEqual(4, raises, "one guard per declared field")

    def test_nothing_is_caught_or_suppressed(self):
        """Fail closed: the boundary swallows no exception and degrades
        nothing."""
        for path in _modules():
            for node in ast.walk(_tree(path)):
                self.assertNotIsInstance(node, ast.ExceptHandler, path.name)
                self.assertNotIsInstance(node, ast.Try, path.name)


# --------------------------------------------------------------------------
# deterministic architecture
# --------------------------------------------------------------------------


class TestDeterministicArchitecture(unittest.TestCase):
    """Blueprint §26 — no clock, no randomness, no hidden state, no reflection,
    no concurrency, no mutation."""

    NONDETERMINISM = frozenset(
        {
            "random",
            "secrets",
            "uuid",
            "time",
            "datetime",
            "threading",
            "asyncio",
            "multiprocessing",
            "concurrent",
            "socket",
            "importlib",
            "os",
            "subprocess",
        }
    )
    DYNAMIC = frozenset(
        {
            "eval",
            "exec",
            "compile",
            "globals",
            "locals",
            "vars",
            "__import__",
            "setattr",
            "delattr",
            "getattr",
        }
    )

    def test_no_source_of_nondeterminism_is_imported(self):
        for path, module, _ in _import_records():
            self.assertNotIn(module.split(".")[0], self.NONDETERMINISM, path.name)

    def test_no_reflection_or_dynamic_import_is_used(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.DYNAMIC, filename)

    def test_no_concurrency_construct_is_declared(self):
        for path in _modules():
            for node in ast.walk(_tree(path)):
                for forbidden in (ast.AsyncFunctionDef, ast.Await, ast.AsyncFor, ast.AsyncWith):
                    self.assertNotIsInstance(node, forbidden, path.name)

    def test_module_level_state_is_limited_to_the_export_declaration(self):
        """No singleton, no registry, no service locator, no module cache."""
        for path in _modules():
            for node in _tree(path).body:
                if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    self.assertIsInstance(target, ast.Name, path.name)
                    self.assertEqual(
                        "__all__", target.id, f"{path.name}: module state {target.id!r}"
                    )

    def test_the_boundary_performs_no_assignment_at_all(self):
        """Beyond the export declaration nothing is assigned anywhere — the
        boundary declares types and validates them; it stores nothing and
        mutates nothing."""
        assignments = [
            (path.name, node)
            for path in _modules()
            for node in ast.walk(_tree(path))
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign))
            and not (
                isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "__all__"
            )
        ]
        non_field = [
            (filename, node)
            for filename, node in assignments
            if not (isinstance(node, ast.AnnAssign) and node.value is None)
        ]
        self.assertEqual([], non_field, "only bare field annotations may remain")

    def test_no_state_carrying_attribute_is_written(self):
        """Frozen contracts: nothing assigns to `self`, so `__post_init__`
        validates without ever normalising or coercing a value."""
        for path in _modules():
            for node in ast.walk(_tree(path)):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        self.assertNotIsInstance(target, ast.Attribute, path.name)


# --------------------------------------------------------------------------
# repository structural conformance
# --------------------------------------------------------------------------


class TestRepositoryStructuralConformance(unittest.TestCase):
    """Blueprint §3/§8/§31 — Agent is one of the eleven frozen subsystem
    boundaries and a sibling of Runtime, not a child of it."""

    def test_agent_is_a_direct_child_of_the_core_region(self):
        self.assertEqual("core", CORE.name)
        self.assertEqual(BOUNDARY, PACKAGE.name)
        self.assertEqual(CORE, PACKAGE.parent)

    def test_agent_is_a_sibling_of_runtime_not_nested_inside_it(self):
        """Runtime does not own Agent: there is no `core/runtime/agent/`."""
        self.assertTrue((CORE / "runtime").is_dir())
        self.assertFalse((CORE / "runtime" / "agent").exists())
        self.assertNotIn("runtime", PACKAGE.relative_to(CORE).parts)

    def test_the_boundary_consists_of_exactly_its_declared_modules(self):
        self.assertEqual(
            ["__init__.py", "agent.py", "definition.py", "instance.py"],
            [p.name for p in _modules()],
        )

    def test_the_boundary_introduces_no_subpackage(self):
        """Blueprint §31: no new entity or subsystem is introduced here."""
        subpackages = [
            p.name
            for p in PACKAGE.iterdir()
            if p.is_dir() and p.name not in ("tests", "__pycache__")
        ]
        self.assertEqual([], subpackages)

    def test_no_entity_outside_the_agent_category_is_declared(self):
        forbidden = ("Runtime", "Knowledge", "Memory", "Trace", "Governance",
                     "Workflow", "Skill", "Capability", "Department", "Tool")
        for filename, node in _definitions():
            if not isinstance(node, ast.ClassDef):
                continue
            for word in forbidden:
                self.assertNotIn(word, node.name, f"{filename}:{node.name}")


if __name__ == "__main__":
    unittest.main()
