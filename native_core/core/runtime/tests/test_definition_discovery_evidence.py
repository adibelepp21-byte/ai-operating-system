"""
Behavioural evidence for Runtime-side Agent Definition discovery (ACT-CC-P6-047).

Produced under `ACT-CC-P6-047` §11. This suite evidences what the discovery
capability *does*; the Baseline 04B conformance suite continues to evidence what
the Runtime boundary *is*, and is unmodified by this Act.

Scope A — discovery by name.
Scope B — fail-closed behaviour (PR-4).
Scope C — determinism (Blueprint §26).
Scope D — the acyclic graph: no Agent import, no module loading.
Scope E — no reflection or dynamic import.
Scope F — the boundary stops short of the Architect-reserved Agent Factory.
"""

import ast
import subprocess
import sys
import unittest
from pathlib import Path

from native_core.core.runtime.discovery import (
    DefinitionCatalog,
    HostDeclaration,
    MalformedDeclaration,
    UndeclaredDefinition,
    UnknownHost,
)

MODULE = Path(__file__).resolve().parent.parent / "discovery.py"

BATCH = "runtime.batch-governance-review-substrate"
INTERACTIVE = "runtime.interactive-governance-session-substrate"
TEXTUAL = "runtime.textual-reasoning-execution-substrate"
INTEGRITY = "Governance Artifact Integrity Agent"


def _catalog():
    """Three declared hosts, mirroring the shape of the governed catalog."""
    return DefinitionCatalog(
        [
            HostDeclaration(TEXTUAL, (INTEGRITY, "Reasoning Agent")),
            HostDeclaration(BATCH, (INTEGRITY,)),
            HostDeclaration(INTERACTIVE, ("Session Agent",)),
        ]
    )


# --------------------------------------------------------------------------
# Scope A — discovery by name
# --------------------------------------------------------------------------


class TestDiscoveryByName(unittest.TestCase):
    def test_a_declared_definition_resolves_to_a_declaring_host(self):
        resolved = _catalog().resolve(INTEGRITY)
        self.assertIsInstance(resolved, HostDeclaration)
        self.assertTrue(resolved.declares(INTEGRITY))

    def test_a_selector_binds_the_named_host(self):
        self.assertEqual(TEXTUAL, _catalog().resolve(INTEGRITY, selector=TEXTUAL).runtime_key)

    def test_the_definition_arrives_as_a_name_not_a_type(self):
        """Category F: the parameter is a string. No Agent type crosses here."""
        source = ast.parse(MODULE.read_text())
        resolve = next(
            node
            for node in ast.walk(source)
            if isinstance(node, ast.FunctionDef) and node.name == "resolve"
        )
        self.assertEqual(
            ["self", "definition_name", "selector"],
            [argument.arg for argument in resolve.args.args],
        )

    def test_a_host_reports_what_it_declares(self):
        declaration = HostDeclaration(BATCH, (INTEGRITY,))
        self.assertTrue(declaration.declares(INTEGRITY))
        self.assertFalse(declaration.declares("Session Agent"))


# --------------------------------------------------------------------------
# Scope B — fail closed (PR-4)
# --------------------------------------------------------------------------


class TestFailsClosed(unittest.TestCase):
    def test_an_unknown_definition_does_not_resolve_to_an_arbitrary_host(self):
        with self.assertRaises(UndeclaredDefinition):
            _catalog().resolve("No Such Agent")

    def test_an_unknown_selector_raises(self):
        with self.assertRaises(UnknownHost):
            _catalog().resolve(INTEGRITY, selector="runtime.absent")

    def test_a_host_that_does_not_declare_the_name_raises(self):
        """Selecting a real host is not enough; it must declare the name."""
        with self.assertRaises(UndeclaredDefinition):
            _catalog().resolve(INTEGRITY, selector=INTERACTIVE)

    def test_an_empty_name_raises(self):
        for name in ("", "   "):
            with self.assertRaises(UndeclaredDefinition):
                _catalog().resolve(name)

    def test_an_empty_catalog_resolves_nothing(self):
        with self.assertRaises(UndeclaredDefinition):
            DefinitionCatalog([]).resolve(INTEGRITY)

    def test_every_halt_is_a_runtime_subsystem_error(self):
        """The taxonomy is the boundary's own (runtime_spec §11)."""
        from native_core.core.runtime.exceptions import RuntimeSubsystemError

        for error in (UndeclaredDefinition, UnknownHost, MalformedDeclaration):
            self.assertTrue(issubclass(error, RuntimeSubsystemError))

    def test_a_malformed_declaration_is_never_coerced(self):
        for key, names in (("", (INTEGRITY,)), ("  ", ()), (None, ())):
            with self.assertRaises(MalformedDeclaration):
                HostDeclaration(key, names)
        with self.assertRaises(MalformedDeclaration):
            HostDeclaration(BATCH, [INTEGRITY])
        with self.assertRaises(MalformedDeclaration):
            HostDeclaration(BATCH, (INTEGRITY, INTEGRITY))
        with self.assertRaises(MalformedDeclaration):
            HostDeclaration(BATCH, ("",))

    def test_a_duplicate_host_is_rejected(self):
        with self.assertRaises(MalformedDeclaration):
            DefinitionCatalog(
                [HostDeclaration(BATCH, (INTEGRITY,)), HostDeclaration(BATCH, ("Other",))]
            )

    def test_a_catalog_holds_declarations_only(self):
        with self.assertRaises(MalformedDeclaration):
            DefinitionCatalog([{"runtime_key": BATCH}])

    def test_records_missing_a_field_raise_rather_than_being_skipped(self):
        for record in ({"runtime_key": BATCH}, {"definition_names": []}, "not-a-mapping"):
            with self.assertRaises(MalformedDeclaration):
                DefinitionCatalog.from_records([record])

    def test_records_carrying_a_non_sequence_raise(self):
        with self.assertRaises(MalformedDeclaration):
            DefinitionCatalog.from_records(
                [{"runtime_key": BATCH, "definition_names": INTEGRITY}]
            )


# --------------------------------------------------------------------------
# Scope C — determinism (Blueprint §26)
# --------------------------------------------------------------------------


class TestDeterministicResolution(unittest.TestCase):
    def test_equivalent_catalog_state_resolves_identically(self):
        first, second = _catalog(), _catalog()
        self.assertEqual(
            first.resolve(INTEGRITY).runtime_key, second.resolve(INTEGRITY).runtime_key
        )

    def test_insertion_order_does_not_change_resolution(self):
        """Ordering is by `runtime_key`, so a shuffled catalog resolves the same."""
        forward = DefinitionCatalog(
            [HostDeclaration(TEXTUAL, (INTEGRITY,)), HostDeclaration(BATCH, (INTEGRITY,))]
        )
        reverse = DefinitionCatalog(
            [HostDeclaration(BATCH, (INTEGRITY,)), HostDeclaration(TEXTUAL, (INTEGRITY,))]
        )
        self.assertEqual(
            forward.resolve(INTEGRITY).runtime_key, reverse.resolve(INTEGRITY).runtime_key
        )

    def test_the_default_is_the_first_declaring_host_in_key_order(self):
        """A stated default, not incidental first-match."""
        self.assertEqual(BATCH, _catalog().resolve(INTEGRITY).runtime_key)

    def test_declarations_are_exposed_in_key_order(self):
        self.assertEqual(
            [BATCH, INTERACTIVE, TEXTUAL],
            [declaration.runtime_key for declaration in _catalog().declarations],
        )

    def test_repeated_resolution_is_stable(self):
        catalog = _catalog()
        self.assertEqual(
            {catalog.resolve(INTEGRITY).runtime_key for _ in range(25)}, {BATCH}
        )

    def test_a_declaration_is_immutable_and_compares_by_value(self):
        declaration = HostDeclaration(BATCH, (INTEGRITY,))
        with self.assertRaises(Exception):
            declaration.runtime_key = "other"
        self.assertEqual(HostDeclaration(BATCH, (INTEGRITY,)), declaration)

    def test_the_catalog_cannot_be_mutated_through_its_declarations(self):
        catalog = _catalog()
        self.assertIsInstance(catalog.declarations, tuple)
        self.assertEqual(3, len(catalog.declarations))


# --------------------------------------------------------------------------
# Scope D — the acyclic graph (Blueprint §21)
# --------------------------------------------------------------------------


class TestNoAgentDependency(unittest.TestCase):
    def test_the_module_imports_nothing_from_agent(self):
        for node in ast.walk(ast.parse(MODULE.read_text())):
            if isinstance(node, ast.ImportFrom):
                self.assertNotIn("agent", (node.module or "").lower())
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn("agent", alias.name.lower())

    def test_discovery_does_not_load_the_agent_module(self):
        """The proof ACT-CC-P6-046 measured, pinned as a regression.

        Run in a fresh interpreter so no other suite's imports can mask it.
        """
        program = (
            "import sys;"
            "from native_core.core.runtime.discovery import DefinitionCatalog, HostDeclaration;"
            f"c = DefinitionCatalog([HostDeclaration({BATCH!r}, ({INTEGRITY!r},))]);"
            f"assert c.resolve({INTEGRITY!r}).runtime_key == {BATCH!r};"
            "loaded = [m for m in sys.modules if 'core.agent' in m];"
            "print('AGENT_MODULES=' + repr(loaded))"
        )
        root = Path(__file__).resolve().parents[4]
        result = subprocess.run(
            [sys.executable, "-c", program],
            capture_output=True,
            text=True,
            cwd=str(root),
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("AGENT_MODULES=[]", result.stdout)


# --------------------------------------------------------------------------
# Scope E — no reflection, no dynamic import
# --------------------------------------------------------------------------


class TestNoReflection(unittest.TestCase):
    FORBIDDEN = frozenset(
        {
            "importlib",
            "__import__",
            "eval",
            "exec",
            "compile",
            "globals",
            "locals",
            "vars",
            "setattr",
            "delattr",
            "getattr",
            "inspect",
        }
    )

    def test_no_forbidden_mechanism_appears(self):
        tree = ast.parse(MODULE.read_text())
        found = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        found |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found |= {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom):
                found.add((node.module or "").split(".")[0])
        self.assertEqual(frozenset(), found & self.FORBIDDEN)

    def test_discovery_is_dynamic_in_time_not_in_python(self):
        """A name unknown at construction resolves against data supplied later."""
        late = DefinitionCatalog([HostDeclaration(BATCH, ("Defined Later Agent",))])
        self.assertEqual(BATCH, late.resolve("Defined Later Agent").runtime_key)


# --------------------------------------------------------------------------
# Scope F — stops short of the Architect-reserved Agent Factory
# --------------------------------------------------------------------------


class TestStopsShortOfTheFactory(unittest.TestCase):
    def test_resolution_yields_a_declaration_never_an_instance(self):
        """agent_spec §12/§13 reserve governed construction to the Architect."""
        resolved = _catalog().resolve(INTEGRITY)
        self.assertIsInstance(resolved, HostDeclaration)
        self.assertEqual({"runtime_key", "definition_names"}, set(vars(resolved)))

    def test_the_module_constructs_no_entity(self):
        names = {
            node.name
            for node in ast.walk(ast.parse(MODULE.read_text()))
            if isinstance(node, ast.ClassDef)
        }
        for word in ("Agent", "Instance", "Capability", "Department", "Factory"):
            for name in names:
                self.assertNotIn(word, name)


if __name__ == "__main__":
    unittest.main()
