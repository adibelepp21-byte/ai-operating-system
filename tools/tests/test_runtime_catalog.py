"""
Evidence for the Runtime hosting-declaration reader (ACT-CC-P6-052).

Scope A — reading the governed catalog.
Scope B — section scoping and link classification.
Scope C — fail-closed behaviour (PR-4).
Scope D — determinism.
Scope E — end-to-end into the Native Core DefinitionCatalog.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.runtime_catalog import CatalogReadError, host_declarations

DEFINITION = """# Some Agent

## Metadata

- **Name:** Governance Artifact Integrity Agent
- **Version:** 1.0
"""

ENTRY = """# Substrate

## Metadata

- **Canonical Key:** `runtime.{slug}` — assigned per EARC.

## Purpose / Description

Prose citing the [Agent Definition Framework](../../agent-definitions.md).

## Hosted Relationship

- **Hosts Agent Instance:** may host an Agent Instance of the
  [{label}](../../platform/agent-definitions/{target}) (Domain Model §4).

## Compatibility Boundary Representation

Prose citing [another definition](../../platform/agent-definitions/other.md).

## Version History
"""


class _Catalog:
    """A synthetic governed catalog laid out like the real one."""

    def __init__(self, *entries, definition=DEFINITION, extra=None):
        self._entries, self._definition, self._extra = entries, definition, extra

    def __enter__(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.runtime_dir = root / "execution-catalog" / "runtime"
        self.runtime_dir.mkdir(parents=True)
        defs = root / "platform" / "agent-definitions"
        defs.mkdir(parents=True)
        if self._definition is not None:
            (defs / "target.md").write_text(self._definition)
        (defs / "other.md").write_text("# Other\n\n- **Name:** Other Agent\n")
        for slug, body in self._entries:
            (self.runtime_dir / f"{slug}.md").write_text(body)
        return self.runtime_dir

    def __exit__(self, *exc):
        self._tmp.cleanup()
        return False


def _entry(slug, label="Target Agent", target="target.md"):
    return slug, ENTRY.format(slug=slug, label=label, target=target)


# --------------------------------------------------------------------------
# Scope A — the real governed catalog
# --------------------------------------------------------------------------


class TestReadsTheGovernedCatalog(unittest.TestCase):
    def test_every_governed_runtime_entry_is_read(self):
        records = host_declarations()
        self.assertEqual(3, len(records))
        for record in records:
            self.assertTrue(record["runtime_key"].startswith("runtime."))

    def test_the_declared_definition_is_identified_by_its_own_name(self):
        for record in host_declarations():
            self.assertEqual(
                ["Governance Artifact Integrity Agent"], record["definition_names"]
            )

    def test_records_are_shaped_for_the_native_core_catalog(self):
        for record in host_declarations():
            self.assertEqual({"runtime_key", "definition_names"}, set(record))


# --------------------------------------------------------------------------
# Scope B — section scoping and classification
# --------------------------------------------------------------------------


class TestScopingAndClassification(unittest.TestCase):
    def test_only_the_hosted_relationship_section_is_read(self):
        """A definition linked from another section is not a hosting declaration."""
        with _Catalog(_entry("a")) as directory:
            self.assertEqual(
                ["Governance Artifact Integrity Agent"],
                host_declarations(directory)[0]["definition_names"],
            )

    def test_a_framework_link_is_not_a_definition_reference(self):
        """`agent-definitions.md` is the Framework, not an instance."""
        slug, body = _entry("b")
        body = body.replace(
            "## Hosted Relationship\n",
            "## Hosted Relationship\n\nSee [Framework](../../agent-definitions.md).\n",
        )
        with _Catalog((slug, body)) as directory:
            self.assertEqual(
                ["Governance Artifact Integrity Agent"],
                host_declarations(directory)[0]["definition_names"],
            )

    def test_an_entry_declaring_nothing_is_kept_with_an_empty_list(self):
        """Declaring nothing differs from being absent."""
        slug, body = _entry("c")
        body = body.replace(
            "  [Target Agent](../../platform/agent-definitions/target.md) (Domain Model §4).",
            "  no Agent Definition at this time.",
        )
        with _Catalog((slug, body)) as directory:
            self.assertEqual([], host_declarations(directory)[0]["definition_names"])

    def test_a_repeated_link_is_declared_once(self):
        slug, body = _entry("d")
        body = body.replace(
            "(Domain Model §4).",
            "and again [Target Agent](../../platform/agent-definitions/target.md).",
        )
        with _Catalog((slug, body)) as directory:
            self.assertEqual(1, len(host_declarations(directory)[0]["definition_names"]))


# --------------------------------------------------------------------------
# Scope C — fail closed (PR-4)
# --------------------------------------------------------------------------


class TestFailsClosed(unittest.TestCase):
    def test_a_missing_canonical_key_raises(self):
        slug, body = _entry("e")
        body = body.replace("- **Canonical Key:** `runtime.e` — assigned per EARC.", "")
        with _Catalog((slug, body)) as directory:
            with self.assertRaises(CatalogReadError):
                host_declarations(directory)

    def test_an_unresolvable_hosting_link_raises(self):
        with _Catalog(_entry("f", target="absent.md")) as directory:
            with self.assertRaises(CatalogReadError):
                host_declarations(directory)

    def test_a_definition_without_a_name_raises(self):
        with _Catalog(_entry("g"), definition="# No Metadata Here\n") as directory:
            with self.assertRaises(CatalogReadError):
                host_declarations(directory)

    def test_a_missing_directory_raises(self):
        with self.assertRaises(CatalogReadError):
            host_declarations("/nonexistent/runtime/catalog")


# --------------------------------------------------------------------------
# Scope D — determinism
# --------------------------------------------------------------------------


class TestDeterminism(unittest.TestCase):
    def test_repeated_reads_agree(self):
        self.assertEqual(host_declarations(), host_declarations())

    def test_records_are_ordered_by_runtime_key(self):
        keys = [record["runtime_key"] for record in host_declarations()]
        self.assertEqual(sorted(keys), keys)

    def test_filesystem_order_does_not_change_the_result(self):
        with _Catalog(_entry("zzz"), _entry("aaa")) as directory:
            self.assertEqual(
                ["runtime.aaa", "runtime.zzz"],
                [r["runtime_key"] for r in host_declarations(directory)],
            )


# --------------------------------------------------------------------------
# Scope E — end to end into the Native Core
# --------------------------------------------------------------------------


class TestEndToEnd(unittest.TestCase):
    def test_the_governed_catalog_resolves_a_host(self):
        from native_core.core.runtime.discovery import (
            DefinitionCatalog,
            UndeclaredDefinition,
        )

        catalog = DefinitionCatalog.from_records(host_declarations())
        resolved = catalog.resolve("Governance Artifact Integrity Agent")
        self.assertEqual("runtime.batch-governance-review-substrate", resolved.runtime_key)
        with self.assertRaises(UndeclaredDefinition):
            catalog.resolve("No Such Agent")

    def test_a_selector_binds_a_named_governed_host(self):
        from native_core.core.runtime.discovery import DefinitionCatalog

        catalog = DefinitionCatalog.from_records(host_declarations())
        target = "runtime.textual-reasoning-execution-substrate"
        self.assertEqual(
            target,
            catalog.resolve("Governance Artifact Integrity Agent", selector=target).runtime_key,
        )

    def test_the_reader_imports_nothing_from_the_native_core(self):
        """Representation stays in tools; meaning stays in Runtime (ADR-0021).

        Checked by AST, not substring: the module's docstring names
        `native_core` in prose precisely to say it does not import it, and a
        bare substring search reports that sentence as a violation."""
        import ast

        source = (Path(__file__).resolve().parent.parent / "runtime_catalog.py").read_text()
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
            elif isinstance(node, ast.Import):
                imported |= {alias.name.split(".")[0] for alias in node.names}
        self.assertNotIn("native_core", imported)
        self.assertEqual({"re", "pathlib", "validators"}, imported)

    def test_the_whole_path_loads_no_agent_module(self):
        program = (
            "import sys;"
            "from tools.runtime_catalog import host_declarations;"
            "from native_core.core.runtime.discovery import DefinitionCatalog;"
            "c = DefinitionCatalog.from_records(host_declarations());"
            "assert c.resolve('Governance Artifact Integrity Agent');"
            "print('AGENT_MODULES=' + repr([m for m in sys.modules if 'core.agent' in m]))"
        )
        root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            [sys.executable, "-c", program], capture_output=True, text=True, cwd=str(root)
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("AGENT_MODULES=[]", result.stdout)


if __name__ == "__main__":
    unittest.main()
