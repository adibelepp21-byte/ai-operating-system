"""
Runtime conformance tests (Blueprint §6/§26/§27/§31; runtime_spec §1–§14;
Roadmap §9.10; Freeze §4/§5 layer 2; INV-3/INV-4/INV-12/INV-13; OQ-2; PR-4).

Baseline 04B — a **verification** baseline. It verifies the existing structure
of the Runtime boundary and introduces no behavior.

Each test asserts one ratified requirement, or one boundary rule the
specification states:

  - INV-3  — Runtime hosts Agent Instances. Hosting is expressed through the
             *inverted* `ExecutionConsumer` contract, so no `Runtime → Agent`
             dependency and no hosting registry exists.
  - INV-4  — every Agent-Instance action produces exactly one Trace. Runtime
             authors none of its own (OQ-2): no Trace identifier exists here.
  - INV-12 — Tool is the only entity permitted an external dependency. This
             boundary holds none; its cross-boundary imports are limited to the
             Infrastructure public surface and the Knowledge composition root.
  - INV-13 — coordination runs through Workflow only. Runtime exposes no
             channel by which one Agent Instance could reach another.
  - PR-4   — fail closed: invalid lifecycle transitions and out-of-state access
             are refused, never degraded. Every halt is a
             `RuntimeSubsystemError`.

together with the structural contracts runtime_spec states: Runtime is a
**facility, not an actor** (§1); it **owns no Knowledge** (§8; Freeze §5); it
makes no governance decision (§10); and the Execution layer is Runtime-owned
internal structure, not a twelfth boundary (Blueprint §31).

Verification is structural (AST, dataclass, signature, abstract-interface and
public-API inspection) in preference to runtime simulation.

**Observation O-1 is record-only.** runtime_spec §12/§14 reserve the Runtime
lifecycle state model to the Architect. These tests verify the state model **as
implemented** — its determinism, completeness, and fail-closed behaviour. They
neither ratify nor question the reservation.

**No source file is modified by this suite.** Findings are reported as evidence.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.runtime.tests.test_runtime_conformance
"""

from __future__ import annotations

import abc
import ast
import dataclasses
import inspect
import unittest
from pathlib import Path
from types import MappingProxyType

from native_core.core import runtime as runtime_pkg
from native_core.core.infrastructure import ExecutionSubstrate, StorageFacility
from native_core.core.knowledge.composition import KnowledgeSubsystem
from native_core.core.runtime import (
    VALID_TRANSITIONS,
    AIOSRuntime,
    InvalidLifecycleTransition,
    InvalidRuntimeConfiguration,
    Runtime,
    RuntimeContext,
    RuntimeNotRunning,
    RuntimeState,
    RuntimeSubsystemError,
    is_valid_transition,
    require_transition,
)
from native_core.core.runtime import execution as execution_pkg
from native_core.core.runtime.bootstrap import bootstrap_runtime
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.execution import (
    Execution,
    ExecutionContext,
    ExecutionError,
    ExecutionSession,
    InvalidExecutionConfiguration,
    create_execution_layer,
)
from native_core.core.runtime.execution.consumer import ExecutionConsumer

PACKAGE = Path(runtime_pkg.__file__).parent
BOUNDARY = "runtime"
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
    """The fully-qualified module name of one source file."""
    parts = path.relative_to(PACKAGE).with_suffix("").parts
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join((ROOT_PACKAGE, BOUNDARY) + parts)


def _containing_package(path):
    """The package a module lives in — the base a relative import resolves
    against. For `__init__.py` that is the package the file *defines*."""
    dotted = _dotted(path)
    if path.name == "__init__.py":
        return dotted
    return dotted.rsplit(".", 1)[0]


def _resolve(path, module, level):
    """Resolve one import to an absolute module name.

    `level` is the number of leading dots. Level 1 resolves against the
    module's own package; each further level strips one more component. This
    resolution is what distinguishes `from ..contract import` inside
    `runtime/execution/` (which lands on `runtime.contract`, the SAME boundary)
    from `from ..knowledge.composition import` inside `runtime/` (which lands on
    another boundary). Substring matching cannot make that distinction.
    """
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
    """The Native Core boundary a module belongs to, or None if it is outside
    `native_core.core`."""
    prefix = ROOT_PACKAGE + "."
    if not dotted.startswith(prefix):
        return None
    return dotted[len(prefix) :].split(".")[0]


def _cross_boundary_records():
    """Every import that leaves this boundary."""
    out = []
    for path, resolved, names in _import_records():
        other = _boundary_of(resolved)
        if other is not None and other != BOUNDARY:
            out.append((path, resolved, names))
    return out


def _definitions():
    """(filename, node) for every class and function defined in the boundary."""
    for path in _modules():
        for node in ast.walk(_tree(path)):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                yield path.name, node


def _identifiers():
    """(filename, identifier) for every name, attribute, argument, and
    definition name in the boundary. Docstrings and comments are excluded by
    construction — only real identifiers are visited."""
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
            elif isinstance(node, ast.keyword) and node.arg:
                yield path.name, node.arg


def _field_types(klass):
    """(name, annotation-as-text) for each dataclass field.

    Source modules use `from __future__ import annotations`, so annotations
    arrive as strings; normalising here keeps the assertions readable and
    independent of that choice."""
    return [
        (f.name, f.type if isinstance(f.type, str) else f.type.__name__)
        for f in dataclasses.fields(klass)
    ]


def _is_declaration_only(node):
    """A body of nothing but a docstring and/or `...` — no behavior."""
    for statement in node.body:
        if not isinstance(statement, ast.Expr):
            return False
        if not isinstance(statement.value, ast.Constant):
            return False
    return True


# --------------------------------------------------------------------------
# hermetic test doubles (this suite; no repository source is modified)
# --------------------------------------------------------------------------


class _MemoryStorage(StorageFacility):
    """An in-process StorageFacility, so the suite touches no filesystem.
    It implements exactly the abstract facility surface and nothing more."""

    name = "storage.conformance-memory"

    def __init__(self):
        super().__init__()
        self._records = {}

    def _provision(self) -> None:
        return None

    def append(self, partition, record):
        self.require_ready()
        self._records.setdefault(partition, []).append(bytes(record))

    def read(self, partition):
        self.require_ready()
        return iter(tuple(self._records.get(partition, ())))

    def partitions(self):
        self.require_ready()
        return iter(sorted(self._records))


class _Substrate(ExecutionSubstrate):
    """An ExecutionSubstrate whose availability the test fixes explicitly."""

    name = "execution-substrate.conformance"

    def __init__(self, available=True):
        super().__init__()
        self._available = available

    def _provision(self) -> None:
        return None

    def is_available(self) -> bool:
        return self._available


def _facilities(available=True):
    storage = _MemoryStorage()
    storage.provision()
    substrate = _Substrate(available)
    substrate.provision()
    return storage, substrate


def _runtime(runtime_id="conformance-runtime", available=True):
    storage, substrate = _facilities(available)
    return AIOSRuntime(runtime_id=runtime_id, storage=storage, substrate=substrate)


def _running_runtime(runtime_id="conformance-runtime"):
    instance = _runtime(runtime_id)
    instance.initialize()
    instance.start()
    return instance


def _stopped_runtime():
    instance = _running_runtime()
    instance.stop()
    return instance


# --------------------------------------------------------------------------
# Runtime contract integrity
# --------------------------------------------------------------------------


class TestRuntimeContractIntegrity(unittest.TestCase):
    """runtime_spec §1/§4/§5/§10 — the contract declares; it does not behave."""

    # `memory` added under **`FD-P7-002`**, the Founder architectural amendment
    # permitting Runtime to depend on the Phase 7 Memory boundary for lawful
    # runtime-mediated Memory operations. This is an enumeration guard: it fired
    # when the surface changed, which is its purpose, and the change is declared
    # here rather than worked around. Runtime remains a non-owner — the added
    # member is a read-only property returning the assembled subsystem, and no
    # lifecycle operation is exposed on Runtime.
    # `tools` added under **`ACT-CC-P8-001 §12`**, which authorizes Runtime to
    # expose lawful Tool access as an *access host only*. Unlike `memory`, this
    # needed no architectural amendment: Blueprint §6 already lists Runtime's
    # allowed dependencies as "agent, workflow, and the Tool boundary
    # (infrastructure)". The guard fired because the surface changed, which is
    # its purpose; the change is declared here rather than worked around.
    # `workflows` added under **`FD-P9-001`**, whose determination
    # `ACT-CC-P9-001 §8.1` permits Runtime to *"depend on and access the
    # Workflow capability for authorized execution hosting, without becoming the
    # owner of Workflow semantics."* Like `tools` and unlike `memory`, this
    # needed no amendment to Blueprint §6 or runtime_spec §7 — both already
    # named `workflow` among Runtime's allowed dependencies. What it needed was
    # the discharge of the `[O]` relationship reservation that had kept the edge
    # Inferred, and the correction of the conformance rule below that had
    # contradicted those two documents. The guard fired because the surface
    # changed, which is its purpose; the change is declared here rather than
    # worked around, and Runtime remains a non-owner — a read-only property
    # returning the assembled subsystem, exposing no lifecycle operation.
    EXPECTED_ABSTRACT = frozenset(
        {"state", "initialize", "start", "stop", "create_context", "knowledge",
         "memory", "tools", "workflows"}
    )

    def test_runtime_is_an_abstract_contract(self):
        self.assertTrue(issubclass(Runtime, abc.ABC))
        self.assertTrue(inspect.isabstract(Runtime))

    def test_runtime_cannot_be_instantiated(self):
        """A contract hosts nothing; only a realization can."""
        with self.assertRaises(TypeError):
            Runtime()

    def test_abstract_surface_is_exactly_the_declared_six(self):
        """No hidden operation, and none missing."""
        self.assertEqual(self.EXPECTED_ABSTRACT, set(Runtime.__abstractmethods__))

    def test_state_and_knowledge_are_read_only_properties(self):
        """Neither is a setter surface: hosting state and hosted subsystems are
        exposed, never assigned through the contract."""
        for name in ("state", "knowledge", "memory", "tools"):
            member = Runtime.__dict__[name]
            self.assertIsInstance(member, property, name)
            self.assertIsNone(member.fset, f"{name} must expose no setter")
            self.assertIsNone(member.fdel, f"{name} must expose no deleter")

    def test_every_contract_member_is_declaration_only(self):
        """AST: each member's body is a docstring and `...` — no behavior, so
        the contract cannot silently host, decide, or execute."""
        contract = PACKAGE / "contract.py"
        klass = next(
            n
            for n in _tree(contract).body
            if isinstance(n, ast.ClassDef) and n.name == "Runtime"
        )
        members = [n for n in klass.body if isinstance(n, ast.FunctionDef)]
        self.assertEqual(len(self.EXPECTED_ABSTRACT), len(members))
        for member in members:
            self.assertTrue(
                _is_declaration_only(member),
                f"Runtime.{member.name} must declare only",
            )

    def test_contract_declares_no_class_level_state(self):
        """A contract carries no data: no class attribute, no default, no
        mutable shared object."""
        contract = PACKAGE / "contract.py"
        klass = next(
            n
            for n in _tree(contract).body
            if isinstance(n, ast.ClassDef) and n.name == "Runtime"
        )
        assignments = [
            n for n in klass.body if isinstance(n, (ast.Assign, ast.AnnAssign))
        ]
        self.assertEqual([], assignments)

    def test_no_contract_member_accepts_a_consumer(self):
        """INV-3/INV-13: the contract takes no Agent, Workflow, Skill, or peer
        argument — hosting is inverted, never passed inward."""
        for name in sorted(self.EXPECTED_ABSTRACT):
            member = Runtime.__dict__[name]
            function = member.fget if isinstance(member, property) else member
            self.assertEqual(
                ["self"],
                list(inspect.signature(function).parameters),
                f"Runtime.{name} must take no argument beyond self",
            )


# --------------------------------------------------------------------------
# AIOSRuntime public contract
# --------------------------------------------------------------------------


class TestAIOSRuntimePublicContract(unittest.TestCase):
    """runtime_spec §1–§4 — the realization implements the contract and adds no
    execution surface."""

    EXPECTED_PUBLIC = frozenset(
        {
            "state",
            "runtime_id",
            "initialize",
            "start",
            "stop",
            "create_context",
            "knowledge",
            "memory",  # FD-P7-002
            "tools",  # ACT-CC-P8-001 §12
            "workflows",  # FD-P9-001 / ACT-CC-P9-001 §8.1
        }
    )

    def test_aios_runtime_realizes_the_contract(self):
        self.assertTrue(issubclass(AIOSRuntime, Runtime))
        self.assertFalse(inspect.isabstract(AIOSRuntime))
        self.assertEqual(frozenset(), frozenset(AIOSRuntime.__abstractmethods__))

    def test_public_surface_is_exactly_the_contract_plus_identity(self):
        """The only public addition to the contract is the inspectable injected
        identity. Nothing else is reachable without an underscore."""
        public = {n for n in dir(AIOSRuntime) if not n.startswith("_")}
        self.assertEqual(self.EXPECTED_PUBLIC, public)

    def test_construction_is_by_injection_only(self):
        """Constructor injection: every dependency is required and supplied by
        the caller — no default, no lookup, no discovery."""
        signature = inspect.signature(AIOSRuntime.__init__)
        self.assertEqual(
            ["self", "runtime_id", "storage", "substrate"],
            list(signature.parameters),
        )
        for name, parameter in signature.parameters.items():
            if name == "self":
                continue
            self.assertIs(
                inspect.Parameter.empty,
                parameter.default,
                f"{name} must be required (no default, no implicit source)",
            )

    def test_construction_fails_closed_on_an_unusable_configuration(self):
        """PR-4: an unconfigurable Runtime is refused, never coerced."""
        storage, substrate = _facilities()
        for kwargs in (
            {"runtime_id": "", "storage": storage, "substrate": substrate},
            {"runtime_id": "   ", "storage": storage, "substrate": substrate},
            {"runtime_id": 1, "storage": storage, "substrate": substrate},
            {"runtime_id": "r", "storage": object(), "substrate": substrate},
            {"runtime_id": "r", "storage": storage, "substrate": object()},
        ):
            with self.assertRaises(InvalidRuntimeConfiguration):
                AIOSRuntime(**kwargs)

    def test_identity_is_injected_never_generated(self):
        self.assertEqual("named-runtime", _runtime("named-runtime").runtime_id)


# --------------------------------------------------------------------------
# public API surface
# --------------------------------------------------------------------------


class TestPublicApiSurface(unittest.TestCase):
    """Blueprint §26 — the boundary exposes exactly its declared surface."""

    EXPECTED_EXPORTS = (
        "Runtime",
        "AIOSRuntime",
        "RuntimeState",
        "VALID_TRANSITIONS",
        "is_valid_transition",
        "require_transition",
        "RuntimeContext",
        "RuntimeSubsystemError",
        "InvalidLifecycleTransition",
        "RuntimeNotRunning",
        "InvalidRuntimeConfiguration",
    )

    def test_exports_are_exactly_the_declared_names(self):
        self.assertEqual(list(self.EXPECTED_EXPORTS), list(runtime_pkg.__all__))

    def test_every_export_resolves(self):
        for name in runtime_pkg.__all__:
            self.assertTrue(hasattr(runtime_pkg, name), name)

    def test_no_export_leaks_another_boundary(self):
        """Blueprint §26: re-exporting a foreign type would make this boundary a
        back-door into another one."""
        for name in runtime_pkg.__all__:
            module = getattr(getattr(runtime_pkg, name), "__module__", None)
            if module is None:
                continue
            self.assertTrue(
                module.startswith(f"{ROOT_PACKAGE}.{BOUNDARY}"),
                f"{name} is exported from {module}, outside this boundary",
            )

    def test_declared_surface_matches_the_documented_surface(self):
        """The package docstring's `Public surface` section and `__all__` do not
        drift apart."""
        docstring = runtime_pkg.__doc__ or ""
        for name in runtime_pkg.__all__:
            self.assertIn(name, docstring, f"{name} is exported but undocumented")

    def test_no_knowledge_memory_governance_or_trace_type_is_exported(self):
        forbidden = ("Knowledge", "Memory", "Governance", "Trace", "Agent", "Workflow")
        for name in runtime_pkg.__all__:
            for word in forbidden:
                self.assertNotIn(word, name, f"{name} exposes {word} from Runtime")


# --------------------------------------------------------------------------
# lifecycle state model — verified AS IMPLEMENTED (Observation O-1 record-only)
# --------------------------------------------------------------------------


class TestLifecycleStateModel(unittest.TestCase):
    """runtime_spec §12/§14 reserve the state model to the Architect
    (**Observation O-1 — record-only**). These tests verify the model *as
    implemented*: determinism, completeness, and fail-closed refusal. They
    neither ratify nor question the reservation."""

    EXPECTED_STATES = ("CREATED", "INITIALIZED", "RUNNING", "STOPPING", "STOPPED")

    def test_the_state_set_is_complete_and_closed(self):
        """No hidden lifecycle state: the enum is the whole set."""
        self.assertEqual(
            list(self.EXPECTED_STATES), [s.name for s in RuntimeState]
        )
        for state in RuntimeState:
            self.assertEqual(state.name.lower(), state.value)

    def test_the_transition_table_is_an_immutable_mapping(self):
        self.assertIsInstance(VALID_TRANSITIONS, MappingProxyType)
        with self.assertRaises(TypeError):
            VALID_TRANSITIONS[RuntimeState.STOPPED] = frozenset({RuntimeState.CREATED})

    def test_every_state_appears_in_the_table_exactly_once(self):
        """Completeness: no state is missing a rule, so no transition is decided
        by omission."""
        self.assertEqual(set(RuntimeState), set(VALID_TRANSITIONS))
        for state, successors in VALID_TRANSITIONS.items():
            self.assertIsInstance(successors, frozenset, state.name)
            for successor in successors:
                self.assertIsInstance(successor, RuntimeState)

    def test_the_lifecycle_is_linear_and_terminal(self):
        """Each state permits at most one successor, and STOPPED permits none —
        a stopped Runtime is never restarted."""
        for state, successors in VALID_TRANSITIONS.items():
            self.assertLessEqual(len(successors), 1, state.name)
        self.assertEqual(frozenset(), VALID_TRANSITIONS[RuntimeState.STOPPED])

    def test_no_state_can_return_to_an_earlier_state(self):
        """Acyclic: walking the table from any state terminates without
        revisiting a state."""
        for start in RuntimeState:
            seen = []
            current = start
            while True:
                self.assertNotIn(current, seen, f"cycle reachable from {start.name}")
                seen.append(current)
                successors = VALID_TRANSITIONS[current]
                if not successors:
                    break
                current = next(iter(successors))

    def test_the_predicate_is_deterministic_and_pure(self):
        """The same pair always yields the same answer, and asking changes
        nothing."""
        before = {k: set(v) for k, v in VALID_TRANSITIONS.items()}
        answers = {
            (a, b): is_valid_transition(a, b)
            for a in RuntimeState
            for b in RuntimeState
        }
        for _ in range(3):
            for (a, b), expected in answers.items():
                self.assertIs(expected, is_valid_transition(a, b))
        self.assertEqual(before, {k: set(v) for k, v in VALID_TRANSITIONS.items()})

    def test_the_predicate_agrees_with_the_table(self):
        for a in RuntimeState:
            for b in RuntimeState:
                self.assertEqual(b in VALID_TRANSITIONS[a], is_valid_transition(a, b))

    def test_require_transition_returns_the_target_when_permitted(self):
        for a, successors in VALID_TRANSITIONS.items():
            for b in successors:
                self.assertIs(b, require_transition(a, b))

    def test_require_transition_fails_closed_on_every_invalid_pair(self):
        """PR-4: refusal, never a degraded or coerced transition."""
        for a in RuntimeState:
            for b in RuntimeState:
                if is_valid_transition(a, b):
                    continue
                with self.assertRaises(InvalidLifecycleTransition):
                    require_transition(a, b)

    def test_a_refused_transition_names_both_states(self):
        with self.assertRaises(InvalidLifecycleTransition) as caught:
            require_transition(RuntimeState.CREATED, RuntimeState.RUNNING)
        message = str(caught.exception)
        self.assertIn("created", message)
        self.assertIn("running", message)


# --------------------------------------------------------------------------
# lifecycle behaviour — fail closed
# --------------------------------------------------------------------------


class TestLifecycleFailsClosed(unittest.TestCase):
    """runtime_spec §11; PR-4 — invalid transitions and out-of-state access are
    refused, and the state is left unchanged."""

    def test_construction_performs_no_implicit_startup(self):
        self.assertIs(RuntimeState.CREATED, _runtime().state)

    def test_the_full_lifecycle_advances_in_order(self):
        instance = _runtime()
        self.assertIs(RuntimeState.CREATED, instance.state)
        instance.initialize()
        self.assertIs(RuntimeState.INITIALIZED, instance.state)
        instance.start()
        self.assertIs(RuntimeState.RUNNING, instance.state)
        instance.stop()
        self.assertIs(RuntimeState.STOPPED, instance.state)

    def test_starting_before_initializing_is_refused(self):
        instance = _runtime()
        with self.assertRaises(InvalidLifecycleTransition):
            instance.start()
        self.assertIs(RuntimeState.CREATED, instance.state)

    def test_initializing_twice_is_refused(self):
        instance = _runtime()
        instance.initialize()
        with self.assertRaises(InvalidLifecycleTransition):
            instance.initialize()
        self.assertIs(RuntimeState.INITIALIZED, instance.state)

    def test_a_stopped_runtime_is_terminal(self):
        """No resurrection: every lifecycle operation is refused after STOPPED,
        and the state stays STOPPED."""
        instance = _stopped_runtime()
        for operation in (instance.initialize, instance.start, instance.stop):
            with self.assertRaises(InvalidLifecycleTransition):
                operation()
            self.assertIs(RuntimeState.STOPPED, instance.state)

    def test_an_unavailable_substrate_refuses_startup(self):
        """runtime_spec §11: detect, do not silently degrade. The refusal leaves
        the Runtime in its prior state rather than half-started."""
        instance = _runtime(available=False)
        instance.initialize()
        with self.assertRaises(RuntimeSubsystemError):
            instance.start()
        self.assertIs(RuntimeState.INITIALIZED, instance.state)

    def test_context_creation_is_refused_outside_running(self):
        for instance in (_runtime(), _stopped_runtime()):
            with self.assertRaises(RuntimeNotRunning):
                instance.create_context()
        initialized = _runtime()
        initialized.initialize()
        with self.assertRaises(RuntimeNotRunning):
            initialized.create_context()

    def test_subsystem_access_is_refused_outside_running(self):
        """The hosted subsystem is unreachable before start and after stop —
        the access boundary is a state guard, not a convenience."""
        for instance in (_runtime(), _stopped_runtime()):
            with self.assertRaises(RuntimeNotRunning):
                instance.knowledge
        initialized = _runtime()
        initialized.initialize()
        with self.assertRaises(RuntimeNotRunning):
            initialized.knowledge

    def test_every_halt_is_a_runtime_subsystem_error(self):
        for error in (
            InvalidLifecycleTransition,
            RuntimeNotRunning,
            InvalidRuntimeConfiguration,
            ExecutionError,
            InvalidExecutionConfiguration,
        ):
            self.assertTrue(issubclass(error, RuntimeSubsystemError), error.__name__)

    def test_the_error_base_does_not_shadow_the_builtin(self):
        self.assertTrue(issubclass(RuntimeSubsystemError, RuntimeError))
        self.assertIsNot(RuntimeSubsystemError, RuntimeError)

    def test_every_halt_message_is_a_string(self):
        """AST: each raise passes a single string, so no halt reaches an
        operator as a structured object needing interpretation."""
        for path in _modules():
            for node in ast.walk(_tree(path)):
                if not isinstance(node, ast.Raise) or not isinstance(
                    node.exc, ast.Call
                ):
                    continue
                for argument in node.exc.args:
                    self.assertIsInstance(
                        argument,
                        (ast.Constant, ast.JoinedStr),
                        f"{path.name}:{node.lineno} passes a non-string halt argument",
                    )
                    if isinstance(argument, ast.Constant):
                        self.assertIsInstance(argument.value, str)


# --------------------------------------------------------------------------
# immutable value objects
# --------------------------------------------------------------------------


class TestImmutableContexts(unittest.TestCase):
    """runtime_spec §3/§6 — a context is immutable execution metadata, never a
    channel to a subsystem."""

    CONTEXTS = (RuntimeContext, ExecutionContext)
    ERRORS = {
        RuntimeContext: InvalidRuntimeConfiguration,
        ExecutionContext: InvalidExecutionConfiguration,
    }

    def test_contexts_are_frozen_dataclasses(self):
        for klass in self.CONTEXTS:
            self.assertTrue(dataclasses.is_dataclass(klass), klass.__name__)
            self.assertTrue(klass.__dataclass_params__.frozen, klass.__name__)

    def test_contexts_carry_exactly_two_metadata_fields(self):
        """No subsystem reference, no clock, no identifier generator — so a
        context can never become a back-door around the access boundary."""
        for klass in self.CONTEXTS:
            self.assertEqual(
                [("runtime_id", "str"), ("execution_sequence", "int")],
                _field_types(klass),
                klass.__name__,
            )

    def test_contexts_cannot_be_mutated(self):
        for klass in self.CONTEXTS:
            instance = klass(runtime_id="r", execution_sequence=0)
            with self.assertRaises(dataclasses.FrozenInstanceError):
                instance.runtime_id = "other"
            with self.assertRaises(dataclasses.FrozenInstanceError):
                instance.execution_sequence = 1

    def test_contexts_are_hashable_and_compared_by_value(self):
        for klass in self.CONTEXTS:
            self.assertEqual(
                klass(runtime_id="r", execution_sequence=2),
                klass(runtime_id="r", execution_sequence=2),
            )
            self.assertEqual(
                len({klass(runtime_id="r", execution_sequence=2)} | {
                    klass(runtime_id="r", execution_sequence=2)
                }),
                1,
            )

    def test_contexts_fail_closed_on_invalid_metadata(self):
        for klass in self.CONTEXTS:
            error = self.ERRORS[klass]
            for kwargs in (
                {"runtime_id": "", "execution_sequence": 0},
                {"runtime_id": "  ", "execution_sequence": 0},
                {"runtime_id": 7, "execution_sequence": 0},
                {"runtime_id": "r", "execution_sequence": -1},
                {"runtime_id": "r", "execution_sequence": "0"},
            ):
                with self.assertRaises(error):
                    klass(**kwargs)

    def test_a_boolean_is_not_an_execution_ordinal(self):
        """`bool` subclasses `int`; accepting it would let a flag masquerade as
        an ordinal."""
        for klass in self.CONTEXTS:
            with self.assertRaises(self.ERRORS[klass]):
                klass(runtime_id="r", execution_sequence=True)


# --------------------------------------------------------------------------
# dependency direction — INV-12 and module isolation
# --------------------------------------------------------------------------


class TestDependencyDirection(unittest.TestCase):
    """Blueprint §26; INV-12 — the boundary depends only on what is beneath it,
    and holds no external dependency."""

    # Canonically permitted, per the four sources cited below: infrastructure
    # (Tool boundary and facilities beneath), knowledge, and agent. Asserted as
    # an **upper bound**: canon states what Runtime *may* depend on, never that
    # it must reach all of them. The former equality also pinned a lower bound
    # no canonical source requires (ADR-0016).
    PERMITTED_BOUNDARIES = frozenset(
        {"infrastructure", "knowledge", "agent", "memory", "workflow"}
    )
    # `memory` moved from forbidden to permitted under **`FD-P7-002`**, which
    # decides that *"the Runtime boundary may depend on the Phase 7 Memory
    # boundary for the limited purpose of lawful runtime-mediated Memory
    # operations."* Same shape as the `agent` correction below: the edge is
    # permitted by a governance instrument, not by implementation convenience.
    #
    # RECORDED DIVERGENCE, not resolved here: Blueprint §6 and `runtime_spec §7`
    # still enumerate Runtime's allowed dependencies without naming Memory.
    # `FD-P7-002` is the governing amendment; synchronising those texts is an
    # architecture-authority documentation act, recorded in the Register entry
    # for `FD-P7-002` rather than performed here.
    # `agent` is NOT forbidden. Freeze §5 layer 2 lists Runtime's dependencies
    # as *"Agent, Workflow, Tool"*; Freeze §6 gives `Runtime hosts Agent
    # Instance` as allowed `Runtime→Instance` with **no** forbidden direction;
    # Blueprint §6 lists Runtime's allowed dependencies as *"agent, workflow,
    # and the Tool boundary"*; runtime_spec §7 says Runtime *"depends on Agent
    # Definitions, Workflows, and the Tool boundary."* Each source's own
    # forbidden list enumerates knowledge ownership, OQ-2, INV-13 and INV-12 —
    # and none of them names agent. Corrected under `DEC-P6-038`; see ADR-0016.
    # `workflow` moved from forbidden to permitted under **`FD-P9-001`**, whose
    # Runtime↔Workflow determination `ACT-CC-P9-001 §8.1` states as *"Runtime
    # MAY depend on and access the Workflow capability for authorized execution
    # hosting, without becoming the owner of Workflow semantics."*
    #
    # This entry was not merely unratified — it **contradicted the two canonical
    # sources quoted in this class's own comment above**, which give Runtime's
    # allowed dependencies as *"agent, workflow, and the Tool boundary"*
    # (Blueprint §6 [A]) and *"Agent Definitions, Workflows, and the Tool
    # boundary"* (runtime_spec §7 [E]). The prohibition was the outlier, not the
    # documents, so nothing in Blueprint §6 or runtime_spec §7 needed amending
    # for this edge. `ACT-CC-P9-001 §8.2` forbids resolving that disagreement
    # silently through implementation and requires this deliberate, minimal
    # correction instead.
    #
    # The edge stays one-directional. Workflow models no Runtime relationship,
    # and `test_runtime_relationship_is_not_modelled` in the Workflow suite
    # still asserts exactly that — which is how `§8.3`'s prohibition on
    # ownership inversion is held structurally rather than promised in prose.
    FORBIDDEN_BOUNDARIES = frozenset(
        {
            "governance",
            "trace",
            "capability",
            "skill",
            "optimization",
        }
    )
    STDLIB = frozenset({"__future__", "abc", "dataclasses", "enum", "types", "typing"})

    def test_cross_boundary_imports_stay_within_the_permitted_set(self):
        reached = {_boundary_of(m) for _, m, _ in _cross_boundary_records()}
        self.assertLessEqual(reached, self.PERMITTED_BOUNDARIES)

    def test_no_forbidden_boundary_is_imported(self):
        """INV-13 and OQ-2 rest on this: no Trace dependency, and no edge to a
        boundary Runtime does not canonically depend on. `agent` is not among
        them — Freeze §5/§6, Blueprint §6 and runtime_spec §7 all list it as an
        allowed Runtime dependency (ADR-0016)."""
        for path, module, _ in _cross_boundary_records():
            self.assertNotIn(
                _boundary_of(module),
                self.FORBIDDEN_BOUNDARIES,
                f"{path.name} imports {module}",
            )

    def test_relative_imports_inside_the_execution_subpackage_stay_in_boundary(self):
        """Anti-false-positive: `from ..contract import` inside
        `runtime/execution/` resolves to `runtime.contract` — the SAME boundary.
        Substring matching reports it as a cross-boundary import; resolving the
        relative level does not."""
        subpackage = PACKAGE / "execution"
        records = [
            (path, module)
            for path, module, _ in _import_records()
            if subpackage in path.parents
        ]
        self.assertTrue(records, "the execution subpackage must have imports")
        for path, module in records:
            boundary = _boundary_of(module)
            if boundary is None:
                continue
            self.assertEqual(
                BOUNDARY,
                boundary,
                f"{path.name} reaches {module}, outside the Runtime boundary",
            )

    def test_infrastructure_is_reached_only_through_its_public_surface(self):
        """Blueprint §26: no boundary reaches into another's internals."""
        for path, module, names in _cross_boundary_records():
            if _boundary_of(module) != "infrastructure":
                continue
            self.assertEqual(
                f"{ROOT_PACKAGE}.infrastructure",
                module,
                f"{path.name} reaches an Infrastructure internal module",
            )
            for name in names:
                # `ToolSubsystem` / `create_tool_subsystem` added under
                # `ACT-CC-P8-001 §12`. The rule itself is unchanged and was
                # obeyed rather than relaxed: Runtime still reaches
                # Infrastructure only through the package's public surface, and
                # the Tool Ecosystem is assembled via its composition root.
                self.assertIn(
                    name,
                    ("StorageFacility", "ExecutionSubstrate",
                     "ToolSubsystem", "create_tool_subsystem"),
                    path.name,
                )

    def test_knowledge_is_reached_only_through_its_composition_root(self):
        """runtime.py §composition boundary: hosted subsystems are assembled
        only via their composition roots, never by constructing internals."""
        for path, module, names in _cross_boundary_records():
            if _boundary_of(module) != "knowledge":
                continue
            self.assertEqual(
                f"{ROOT_PACKAGE}.knowledge.composition",
                module,
                f"{path.name} bypasses the Knowledge composition root",
            )
            for name in names:
                self.assertIn(
                    name, ("KnowledgeSubsystem", "create_knowledge_subsystem"), path.name
                )

    def test_no_external_dependency_exists(self):
        """INV-12: Tool is the only entity permitted an external dependency."""
        for path, module, _ in _import_records():
            if _boundary_of(module) is not None:
                continue
            root = module.split(".")[0]
            self.assertIn(
                root,
                self.STDLIB,
                f"{path.name} imports {module}, which is not standard library",
            )

    def test_the_boundary_never_re_enters_itself_absolutely(self):
        """Internal wiring is relative throughout, so no module can re-enter the
        boundary through an absolute path that bypasses package structure.

        This inspects the import **as written** (`level == 0`), not the resolved
        module name: every internal import here resolves to
        `native_core.core.runtime.*` by design, so testing the resolved name
        would flag correct relative wiring."""
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
                        module.startswith(f"{ROOT_PACKAGE}.{BOUNDARY}"),
                        f"{path.name} imports its own boundary absolutely: {module}",
                    )


# --------------------------------------------------------------------------
# Knowledge ownership prohibition
# --------------------------------------------------------------------------


class TestKnowledgeOwnershipProhibition(unittest.TestCase):
    """Blueprint §6 forbidden; Freeze §5; INV-8 — Runtime hosts Knowledge; it
    owns no Knowledge semantics and holds no promotion authority."""

    KNOWLEDGE_VERBS = frozenset(
        {
            "admit",
            "revise",
            "supersede",
            "promote",
            "promotion",
            "derive_status",
            "canonical_status",
            "version",
            "versioning",
        }
    )
    AUTHORITY_VERBS = frozenset(
        {"authorize", "authorization", "approve", "deny", "grant", "revoke", "permit"}
    )

    def test_no_knowledge_semantic_operation_is_defined(self):
        for filename, node in _definitions():
            self.assertNotIn(node.name, self.KNOWLEDGE_VERBS, f"{filename}:{node.name}")

    def test_no_knowledge_semantic_operation_is_invoked(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.KNOWLEDGE_VERBS, filename)

    def test_no_governance_authority_is_held(self):
        """runtime_spec §10; §6.2 invariant 2 — Runtime enforces isolation, not
        policy. It neither decides nor carries an authorization surface."""
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.AUTHORITY_VERBS, filename)

    def test_hosted_knowledge_is_returned_unchanged(self):
        """Runtime hands back exactly what the composition root assembled — it
        wraps, filters, and decorates nothing."""
        instance = _running_runtime()
        subsystem = instance.knowledge
        self.assertIsInstance(subsystem, KnowledgeSubsystem)
        self.assertIs(subsystem, instance.knowledge)

    def test_knowledge_is_released_at_shutdown_not_retained(self):
        """Runtime owns transient hosting state only: after stop, the hosted
        reference is gone and unreachable."""
        instance = _running_runtime()
        instance.stop()
        with self.assertRaises(RuntimeNotRunning):
            instance.knowledge

    def test_runtime_constructs_no_knowledge_internal(self):
        """AST: the only Knowledge name the boundary calls is the composition
        root."""
        called = {
            node.func.id
            for path in _modules()
            for node in ast.walk(_tree(path))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        knowledge_calls = {n for n in called if "nowledge" in n}
        self.assertEqual({"create_knowledge_subsystem"}, knowledge_calls)


# --------------------------------------------------------------------------
# facility, not actor — INV-4 / OQ-2
# --------------------------------------------------------------------------


class TestFacilityNotActor(unittest.TestCase):
    """runtime_spec §1/§9; OQ-2; INV-4 — Runtime hosts and coordinates; it does
    not act, and it authors no independent Trace."""

    def test_no_trace_identifier_exists_in_the_boundary(self):
        """INV-4 assigns exactly one Trace to each Agent-Instance action.
        Runtime authors none: no Trace type is imported, constructed, or
        named anywhere. (Identifiers only — prose is not evidence.)"""
        for filename, identifier in _identifiers():
            self.assertNotIn("trace", identifier.lower(), f"{filename}: {identifier}")

    def test_no_trace_boundary_import_exists(self):
        for path, module, _ in _import_records():
            self.assertNotEqual("trace", _boundary_of(module), path.name)

    def test_no_action_verb_is_defined(self):
        """A facility exposes lifecycle and access, not actions. `start`/`stop`
        are lifecycle transitions of the facility itself, not work it performs."""
        forbidden = frozenset(
            {
                "execute",
                "run",
                "perform",
                "act",
                "invoke",
                "call_tool",
                "decide",
                "plan",
                "schedule",
                "enqueue",
                "dequeue",
                "submit",
                "spawn",
                "retry",
                "poll",
                "tick",
            }
        )
        for filename, node in _definitions():
            self.assertNotIn(node.name, forbidden, f"{filename}:{node.name}")

    def test_no_agent_workflow_or_skill_entity_is_defined_here(self):
        """Blueprint §31: no new entity or subsystem is introduced by this
        boundary."""
        forbidden = ("Agent", "Workflow", "Skill", "Capability", "Department", "Tool")
        for filename, node in _definitions():
            if not isinstance(node, ast.ClassDef):
                continue
            for word in forbidden:
                self.assertNotIn(word, node.name, f"{filename}:{node.name}")

    def test_runtime_holds_only_transient_hosting_state(self):
        """runtime_spec §3 — its instance state is exactly identity, injected
        facilities, lifecycle state, the hosted reference, and the ordinal. No
        registry of hosted actors exists."""
        instance = _running_runtime()
        self.assertEqual(
            {
                "_runtime_id",
                "_storage",
                "_substrate",
                "_state",
                "_knowledge",
                "_memory",  # FD-P7-002 — a hosted reference, released on stop
                "_tools",  # ACT-CC-P8-001 §12 — hosted, released on stop
                "_workflows",  # ACT-CC-P9-001 §8.1 — hosted, released on stop
                "_execution_sequence",
            },
            set(instance.__dict__),
        )

    def test_runtime_does_not_own_the_facilities_it_is_given(self):
        """Injected Infrastructure facilities outlive the Runtime: `stop()`
        releases Runtime's own references and tears nothing down."""
        storage, substrate = _facilities()
        instance = AIOSRuntime(
            runtime_id="conformance-runtime", storage=storage, substrate=substrate
        )
        instance.initialize()
        instance.start()
        instance.stop()
        self.assertTrue(storage.is_ready)
        self.assertTrue(substrate.is_available())


# --------------------------------------------------------------------------
# INV-3 and INV-13 — hosting is inverted, and there is no peer channel
# --------------------------------------------------------------------------


class TestHostingIsInverted(unittest.TestCase):
    """INV-3 — Runtime hosts Agent Instances. The dependency runs the other way:
    a consumer depends on the Execution boundary, never Runtime on a consumer."""

    def test_the_consumer_contract_is_abstract_and_generic(self):
        self.assertTrue(inspect.isabstract(ExecutionConsumer))
        self.assertEqual({"participate"}, set(ExecutionConsumer.__abstractmethods__))
        with self.assertRaises(TypeError):
            ExecutionConsumer()

    def test_a_consumer_receives_only_the_bound_execution(self):
        """The sole entry parameter is the Execution boundary, so every future
        consumer necessarily enters Runtime through it."""
        self.assertEqual(
            ["self", "execution"],
            list(inspect.signature(ExecutionConsumer.participate).parameters),
        )

    def test_the_consumer_contract_declares_only(self):
        consumer = PACKAGE / "execution" / "consumer.py"
        klass = next(
            n
            for n in _tree(consumer).body
            if isinstance(n, ast.ClassDef) and n.name == "ExecutionConsumer"
        )
        for member in klass.body:
            if isinstance(member, ast.FunctionDef):
                self.assertTrue(_is_declaration_only(member), member.name)

    def test_runtime_never_learns_of_a_consumer(self):
        """No Runtime module imports or references the consumer contract, so no
        `Runtime → Agent/Workflow/Skill` dependency can arise."""
        importers = [
            path.name
            for path, _, names in _import_records()
            if "ExecutionConsumer" in names
        ]
        self.assertEqual([], importers)

    def test_no_hosting_registry_exists(self):
        """INV-3 hosting is structural, not a mutable collection of instances."""
        forbidden = frozenset(
            {
                "register",
                "registry",
                "instances",
                "hosted",
                "attach",
                "detach",
                "add_agent",
                "agents",
            }
        )
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, forbidden, filename)


class TestNoAgentToAgentChannel(unittest.TestCase):
    """INV-13 — coordination runs through Workflow only. Nothing here can carry
    one Agent Instance to another."""

    #: Names that could only denote a route from one Agent Instance to another.
    #: Deliberately excludes generic words such as `target` and `other`: in
    #: `require_transition(current, target)` the target is a *lifecycle state*,
    #: not a peer, and a bare-word blacklist would report that as a violation.
    FORBIDDEN = frozenset(
        {
            "peer",
            "peers",
            "peer_instance",
            "target_agent",
            "to_agent",
            "from_agent",
            "channel",
            "send",
            "receive",
            "notify",
            "broadcast",
            "dispatch",
            "publish",
            "subscribe",
            "message",
            "mailbox",
            "inbox",
            "outbox",
        }
    )

    def test_no_peer_channel_identifier_exists(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.FORBIDDEN, filename)

    def test_the_execution_boundary_exposes_only_runtime_and_identity(self):
        """The one object a consumer receives carries no route to another
        consumer."""
        self.assertEqual({"runtime", "context"}, set(Execution.__abstractmethods__))
        self.assertEqual(
            {"runtime", "context"},
            {n for n in dir(ExecutionSession) if not n.startswith("_")},
        )

    def test_the_execution_context_carries_no_reference(self):
        """Identity metadata only — two scalars, so it cannot be a channel."""
        for name, annotation in _field_types(ExecutionContext):
            self.assertIn(annotation, ("str", "int"), name)


# --------------------------------------------------------------------------
# Execution layer structure
# --------------------------------------------------------------------------


class TestExecutionLayerStructure(unittest.TestCase):
    """Blueprint §31; runtime_spec §5/§6/§10 — the Execution layer is
    Runtime-owned internal structure, not a twelfth boundary."""

    EXPECTED_EXPORTS = (
        "Execution",
        "ExecutionSession",
        "ExecutionContext",
        "create_execution_layer",
        "ExecutionError",
        "InvalidExecutionConfiguration",
    )

    def test_the_layer_lives_inside_the_runtime_boundary(self):
        """It is a subdirectory of `core/runtime/`, not a sibling of the eleven
        frozen boundaries under `core/`."""
        subpackage = Path(execution_pkg.__file__).parent
        self.assertEqual(PACKAGE, subpackage.parent)
        self.assertEqual("execution", subpackage.name)

    def test_its_errors_extend_the_runtime_taxonomy(self):
        """A parallel error hierarchy would make it a separate boundary."""
        self.assertTrue(issubclass(ExecutionError, RuntimeSubsystemError))

    def test_the_execution_contract_is_abstract_and_lifecycle_neutral(self):
        self.assertTrue(inspect.isabstract(Execution))
        with self.assertRaises(TypeError):
            Execution()
        for name in ("initialize", "start", "stop"):
            self.assertNotIn(name, dir(Execution), f"Execution must not own {name}")

    def test_the_session_is_an_immutable_binding(self):
        self.assertTrue(dataclasses.is_dataclass(ExecutionSession))
        self.assertTrue(ExecutionSession.__dataclass_params__.frozen)
        self.assertEqual(
            ["_runtime", "_context"],
            [f.name for f in dataclasses.fields(ExecutionSession)],
        )

    def test_the_session_realizes_the_contract(self):
        instance = _running_runtime()
        session = create_execution_layer(instance)
        self.assertIsInstance(session, Execution)
        self.assertIs(instance, session.runtime)
        self.assertIsInstance(session.context, ExecutionContext)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            session._context = ExecutionContext(runtime_id="r", execution_sequence=0)

    def test_the_composition_root_fails_closed_on_a_non_runtime(self):
        for value in (None, object(), "runtime"):
            with self.assertRaises(InvalidExecutionConfiguration):
                create_execution_layer(value)

    def test_the_composition_root_fails_closed_through_the_runtime(self):
        """Building an execution boundary against a Runtime that is not RUNNING
        is refused by the Runtime's own access control — this layer weakens
        nothing."""
        with self.assertRaises(RuntimeNotRunning):
            create_execution_layer(_runtime())

    def test_identity_is_issued_by_the_runtime_never_generated_here(self):
        """AST: the composition root obtains identity from
        `runtime.create_context()`; there is no second counter."""
        source = PACKAGE / "execution" / "composition.py"
        attributes = {
            node.attr
            for node in ast.walk(_tree(source))
            if isinstance(node, ast.Attribute)
        }
        self.assertIn("create_context", attributes)
        self.assertEqual(
            [],
            [n for n in ast.walk(_tree(source)) if isinstance(n, ast.AugAssign)],
        )

    def test_the_issued_identity_matches_the_hosting_runtime(self):
        instance = _running_runtime("identity-runtime")
        first = create_execution_layer(instance)
        second = create_execution_layer(instance)
        self.assertEqual("identity-runtime", first.context.runtime_id)
        self.assertEqual(0, first.context.execution_sequence)
        self.assertEqual(1, second.context.execution_sequence)

    def test_exports_are_exactly_the_declared_names(self):
        self.assertEqual(list(self.EXPECTED_EXPORTS), list(execution_pkg.__all__))
        for name in execution_pkg.__all__:
            self.assertTrue(hasattr(execution_pkg, name), name)

    def test_recorded_finding_f4_consumer_contract_is_off_the_public_surface(self):
        """**RECORDED FINDING F-4 — export/declaration drift.**

        `consumer.py` declares `ExecutionConsumer` to be *"the canonical consumer
        boundary: the single interface every future execution consumer ...
        implements"*, yet the Execution package's public surface — its
        `__all__` and its docstring's `Public surface` list — omits it. The
        contract is reachable only as
        `native_core.core.runtime.execution.consumer.ExecutionConsumer`.

        This test records the state as found. It is **not** a repair and **not**
        a judgement that the export is required — the resolution is the
        Architect's. Source is unmodified by this baseline."""
        self.assertNotIn("ExecutionConsumer", execution_pkg.__all__)
        self.assertFalse(hasattr(execution_pkg, "ExecutionConsumer"))
        self.assertNotIn("ExecutionConsumer", execution_pkg.__doc__ or "")


# --------------------------------------------------------------------------
# deterministic architecture
# --------------------------------------------------------------------------


class TestDeterministicArchitecture(unittest.TestCase):
    """Blueprint §26; runtime_spec §3 — no clock, no randomness, no hidden
    state, no reflection, no concurrency."""

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
        }
    )

    def test_no_source_of_nondeterminism_is_imported(self):
        for path, module, _ in _import_records():
            root = module.split(".")[0]
            self.assertNotIn(root, self.NONDETERMINISM, f"{path.name} imports {module}")

    def test_no_reflection_or_dynamic_import_is_used(self):
        for filename, identifier in _identifiers():
            self.assertNotIn(identifier, self.DYNAMIC, filename)

    def test_no_concurrency_construct_is_declared(self):
        for path in _modules():
            for node in ast.walk(_tree(path)):
                self.assertNotIsInstance(node, ast.AsyncFunctionDef, path.name)
                self.assertNotIsInstance(node, ast.Await, path.name)
                self.assertNotIsInstance(node, ast.AsyncFor, path.name)
                self.assertNotIsInstance(node, ast.AsyncWith, path.name)

    def test_module_level_state_is_limited_to_immutable_declarations(self):
        """No singleton, no registry, no service locator, no module cache.

        `__all__` is the export declaration; an UPPER_CASE name bound to an
        immutable literal, a `frozenset(...)`, or a `MappingProxyType(...)` is a
        constant, not state. Anything else at module scope is flagged."""
        allowed_calls = ("frozenset", "MappingProxyType")
        for path in _modules():
            for node in _tree(path).body:
                if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    self.assertIsInstance(target, ast.Name, path.name)
                    if target.id == "__all__":
                        continue
                    self.assertTrue(
                        target.id.isupper(),
                        f"{path.name}: module-level state {target.id!r}",
                    )
                    value = node.value
                    constant = isinstance(value, ast.Constant)
                    read_only_call = (
                        isinstance(value, ast.Call)
                        and isinstance(value.func, ast.Name)
                        and value.func.id in allowed_calls
                    )
                    self.assertTrue(
                        constant or read_only_call,
                        f"{path.name}: {target.id!r} is not an immutable declaration",
                    )

    def test_exactly_one_mutation_of_the_execution_ordinal_exists(self):
        """The Runtime is the sole issuer of execution identity: one increment,
        in `AIOSRuntime.create_context`, and nowhere else."""
        increments = [
            (path.name, node)
            for path in _modules()
            for node in ast.walk(_tree(path))
            if isinstance(node, ast.AugAssign)
        ]
        self.assertEqual(1, len(increments), increments)
        filename, node = increments[0]
        self.assertEqual("runtime.py", filename)
        self.assertEqual("_execution_sequence", node.target.attr)

    def test_composition_produces_a_fresh_graph_every_call(self):
        """No caching, no memoization, no reuse across calls."""
        storage, substrate = _facilities()
        first = create_runtime(runtime_id="r", storage=storage, substrate=substrate)
        second = create_runtime(runtime_id="r", storage=storage, substrate=substrate)
        self.assertIsNot(first, second)
        self.assertIs(RuntimeState.CREATED, first.state)
        self.assertIs(RuntimeState.CREATED, second.state)

    def test_the_ordinal_sequence_is_reproducible(self):
        """Two identically constructed Runtimes issue identical contexts — no
        clock, no randomness, no shared counter."""
        first = [_running_runtime("same-id").create_context() for _ in range(1)]
        second = _running_runtime("same-id")
        self.assertEqual(
            [RuntimeContext(runtime_id="same-id", execution_sequence=0)], first
        )
        self.assertEqual(
            [RuntimeContext(runtime_id="same-id", execution_sequence=i) for i in range(3)],
            [second.create_context() for _ in range(3)],
        )


# --------------------------------------------------------------------------
# composition and bootstrap discipline
# --------------------------------------------------------------------------


class TestCompositionAndBootstrap(unittest.TestCase):
    """Phase 4.1 — one composition root, one bootstrap entry, no lifecycle
    policy embedded."""

    def test_the_composition_root_performs_no_transition(self):
        storage, substrate = _facilities()
        instance = create_runtime(runtime_id="r", storage=storage, substrate=substrate)
        self.assertIs(RuntimeState.CREATED, instance.state)

    def test_bootstrap_initializes_but_never_starts(self):
        """Lifecycle policy stays with the caller: exactly one transition."""
        storage, substrate = _facilities()
        instance = bootstrap_runtime(
            runtime_id="r", storage=storage, substrate=substrate
        )
        self.assertIs(RuntimeState.INITIALIZED, instance.state)

    def test_bootstrap_fails_closed_at_the_entry_point(self):
        storage, substrate = _facilities()
        for kwargs in (
            {"runtime_id": "", "storage": storage, "substrate": substrate},
            {"runtime_id": "r", "storage": object(), "substrate": substrate},
            {"runtime_id": "r", "storage": storage, "substrate": object()},
        ):
            with self.assertRaises(InvalidRuntimeConfiguration):
                bootstrap_runtime(**kwargs)

    def test_bootstrap_retains_nothing(self):
        """It holds no reference, no state, no cache after returning."""
        source = PACKAGE / "bootstrap.py"
        self.assertEqual(
            [],
            [n for n in _tree(source).body if isinstance(n, (ast.Assign, ast.AnnAssign))],
        )

    def test_the_composition_root_constructs_only_the_runtime(self):
        """Infrastructure facilities are injected, never constructed here."""
        source = PACKAGE / "composition.py"
        constructed = {
            node.func.id
            for node in ast.walk(_tree(source))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertEqual({"AIOSRuntime"}, constructed)


if __name__ == "__main__":
    unittest.main()
