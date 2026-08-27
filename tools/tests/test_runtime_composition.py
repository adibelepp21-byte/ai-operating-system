"""
Evidence for the Runtime hosting composition root (ACT-CC-P6-053).

Scope A — the supported path composes end to end.
Scope B — fail-closed behaviour, with errors attributed to the owning layer.
Scope C — determinism and absence of hidden state.
Scope D — boundary preservation: no Agent load, no cycle, no core coupling.
"""

import ast
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from native_core.core.runtime.discovery import (
    DefinitionCatalog,
    HostDeclaration,
    MalformedDeclaration,
    UndeclaredDefinition,
    UnknownHost,
)

from tools.runtime_catalog import CatalogReadError
from tools.runtime_composition import create_definition_catalog, resolve_host

INTEGRITY = "Governance Artifact Integrity Agent"
BATCH = "runtime.batch-governance-review-substrate"
TEXTUAL = "runtime.textual-reasoning-execution-substrate"
MODULE = Path(__file__).resolve().parent.parent / "runtime_composition.py"

DEFINITION = "# D\n\n## Metadata\n\n- **Name:** {name}\n"
ENTRY = """# Substrate

## Metadata

- **Canonical Key:** `runtime.{slug}`

## Hosted Relationship

- **Hosts Agent Instance:** may host an Agent Instance of the
  [D](../../platform/agent-definitions/{target}) (Domain Model §4).

## Version History
"""


class _Catalog:
    def __init__(self, *entries, definition=DEFINITION.format(name=INTEGRITY)):
        self._entries, self._definition = entries, definition

    def __enter__(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.runtime_dir = root / "execution-catalog" / "runtime"
        self.runtime_dir.mkdir(parents=True)
        defs = root / "platform" / "agent-definitions"
        defs.mkdir(parents=True)
        if self._definition is not None:
            (defs / "target.md").write_text(self._definition)
        for slug, target in self._entries:
            (self.runtime_dir / f"{slug}.md").write_text(
                ENTRY.format(slug=slug, target=target)
            )
        return self.runtime_dir

    def __exit__(self, *exc):
        self._tmp.cleanup()
        return False


# --------------------------------------------------------------------------
# Scope A — the supported path
# --------------------------------------------------------------------------


class TestTheSupportedPath(unittest.TestCase):
    def test_one_call_resolves_a_governed_definition_to_its_host(self):
        self.assertEqual(BATCH, resolve_host(INTEGRITY).runtime_key)

    def test_a_selector_binds_the_named_governed_host(self):
        self.assertEqual(TEXTUAL, resolve_host(INTEGRITY, selector=TEXTUAL).runtime_key)

    def test_the_catalog_factory_returns_a_native_core_catalog(self):
        catalog = create_definition_catalog()
        self.assertIsInstance(catalog, DefinitionCatalog)
        self.assertEqual(3, len(catalog.declarations))

    def test_resolution_yields_a_declaration_never_an_instance(self):
        """Discovery stops short of the Architect-reserved Factory."""
        self.assertIsInstance(resolve_host(INTEGRITY), HostDeclaration)

    def test_the_path_works_against_an_arbitrary_governed_directory(self):
        with _Catalog(("solo", "target.md")) as directory:
            self.assertEqual(
                "runtime.solo", resolve_host(INTEGRITY, runtime_dir=directory).runtime_key
            )


# --------------------------------------------------------------------------
# Scope B — fail closed, attributed to the owning layer
# --------------------------------------------------------------------------


class TestFailsClosed(unittest.TestCase):
    def test_an_unknown_definition_raises_from_the_runtime_layer(self):
        with self.assertRaises(UndeclaredDefinition):
            resolve_host("No Such Agent")

    def test_an_unknown_selector_raises_from_the_runtime_layer(self):
        with self.assertRaises(UnknownHost):
            resolve_host(INTEGRITY, selector="runtime.absent")

    def test_a_host_that_does_not_declare_the_name_raises(self):
        with _Catalog(("a", "target.md"), ("b", "target.md")) as directory:
            catalog = create_definition_catalog(directory)
            self.assertEqual("runtime.a", catalog.resolve(INTEGRITY).runtime_key)
            with self.assertRaises(UndeclaredDefinition):
                catalog.resolve("Absent Agent", selector="runtime.b")

    def test_an_unreadable_catalog_raises_from_the_reader_layer(self):
        """Representation failures stay attributable to the reader."""
        with _Catalog(("a", "absent.md")) as directory:
            with self.assertRaises(CatalogReadError):
                create_definition_catalog(directory)

    def test_a_missing_catalog_directory_raises_from_the_reader_layer(self):
        with self.assertRaises(CatalogReadError):
            resolve_host(INTEGRITY, runtime_dir="/nonexistent/catalog")

    def test_a_definition_without_a_name_raises_from_the_reader_layer(self):
        with _Catalog(("a", "target.md"), definition="# No Metadata\n") as directory:
            with self.assertRaises(CatalogReadError):
                create_definition_catalog(directory)

    def test_a_duplicate_host_key_raises_from_the_runtime_layer(self):
        """Two entries with one key: the reader reports both, the core refuses."""
        with _Catalog(("a", "target.md")) as directory:
            (directory / "duplicate.md").write_text(
                ENTRY.format(slug="a", target="target.md")
            )
            with self.assertRaises(MalformedDeclaration):
                create_definition_catalog(directory)

    def test_the_two_error_families_are_not_collapsed(self):
        """Which layer refused is diagnostic and is preserved."""
        self.assertFalse(issubclass(CatalogReadError, MalformedDeclaration))
        self.assertFalse(issubclass(MalformedDeclaration, CatalogReadError))


# --------------------------------------------------------------------------
# Scope C — determinism, no hidden state
# --------------------------------------------------------------------------


class TestDeterminismAndNoHiddenState(unittest.TestCase):
    def test_repeated_resolution_is_stable(self):
        self.assertEqual({resolve_host(INTEGRITY).runtime_key for _ in range(20)}, {BATCH})

    def test_each_call_builds_a_fresh_catalog(self):
        self.assertIsNot(create_definition_catalog(), create_definition_catalog())

    def test_a_changed_catalog_is_observed_not_remembered(self):
        """No cache: the second call sees the edit the first could not."""
        with _Catalog(("zzz", "target.md")) as directory:
            self.assertEqual("runtime.zzz", resolve_host(INTEGRITY, runtime_dir=directory).runtime_key)
            (directory / "aaa.md").write_text(ENTRY.format(slug="aaa", target="target.md"))
            self.assertEqual("runtime.aaa", resolve_host(INTEGRITY, runtime_dir=directory).runtime_key)

    def test_no_module_level_mutable_state_exists(self):
        module_level = [
            node
            for node in ast.parse(MODULE.read_text()).body
            if isinstance(node, (ast.Assign, ast.AnnAssign))
        ]
        self.assertEqual([], module_level)


# --------------------------------------------------------------------------
# Scope D — boundary preservation
# --------------------------------------------------------------------------


class TestBoundariesPreserved(unittest.TestCase):
    def test_the_composition_adds_no_behaviour_of_its_own(self):
        """Assembly only: two thin functions, no classes, no logic."""
        tree = ast.parse(MODULE.read_text())
        self.assertEqual([], [n for n in tree.body if isinstance(n, ast.ClassDef)])
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
        self.assertEqual(
            ["create_definition_catalog", "resolve_host"], [f.name for f in functions]
        )

    def test_the_reader_still_imports_nothing_from_the_native_core(self):
        """The halves stay blind to each other; only this module sees both."""
        source = (MODULE.parent / "runtime_catalog.py").read_text()
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
            elif isinstance(node, ast.Import):
                imported |= {a.name.split(".")[0] for a in node.names}
        self.assertNotIn("native_core", imported)

    def test_the_native_core_imports_nothing_from_tools(self):
        core = MODULE.parent.parent / "native_core"
        for path in sorted(core.rglob("*.py")):
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("tools"):
                    self.fail(f"{path} imports tools")
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertFalse(alias.name.startswith("tools"), str(path))

    def test_the_whole_supported_path_loads_no_agent_module(self):
        program = (
            "import sys;"
            "from tools.runtime_composition import resolve_host;"
            f"assert resolve_host({INTEGRITY!r}).runtime_key == {BATCH!r};"
            "print('AGENT_MODULES=' + repr([m for m in sys.modules if 'core.agent' in m]))"
        )
        result = subprocess.run(
            [sys.executable, "-c", program],
            capture_output=True,
            text=True,
            cwd=str(MODULE.parent.parent),
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("AGENT_MODULES=[]", result.stdout)

    def test_no_reflection_is_used(self):
        forbidden = {"importlib", "__import__", "eval", "exec", "compile", "getattr"}
        tree = ast.parse(MODULE.read_text())
        found = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        found |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        self.assertEqual(set(), found & forbidden)


if __name__ == "__main__":
    unittest.main()
