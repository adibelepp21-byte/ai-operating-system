"""
Infrastructure conformance tests (Blueprint §27; infrastructure_spec).

Each test asserts a governance property, not an implementation nicety:

  - INV-12 : the only external-integration point is the Tool boundary, and
             the Infrastructure source imports nothing external.
  - OQ-2   : facilities author no Trace (there is no Trace-writing surface).
  - PR-4   : fail closed — unprovisioned use, append-only violations, cyclic
             or unmet dependencies all halt rather than degrade.
  - append-only: storage offers no edit/delete and rejects newline records.
  - lifecycle : provision/use/release order is enforced.

Standard-library `unittest` only (no external framework — Blueprint §27, [O]).
Run:  python -m unittest native_core.core.infrastructure.tests.test_infrastructure_conformance
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

from native_core.core import infrastructure as infra
from native_core.core.infrastructure.bootstrap import Bootstrap, BootstrapError
from native_core.core.infrastructure.facility import (
    Facility,
    FacilityState,
    FacilityUnavailable,
)
from native_core.core.infrastructure.filesystem import FilesystemFacility, PathEscapesRoot
from native_core.core.infrastructure.storage import LocalAppendOnlyStorage
from native_core.core.infrastructure.substrate import LocalExecutionSubstrate
from native_core.core.infrastructure.tool_boundary import (
    ToolAlreadyRegistered,
    ToolBoundary,
    ToolNotRegistered,
)
from native_core.shared import Failure, Success

_INFRA_DIR = Path(infra.__file__).resolve().parent

# The complete set of module names an external/vendor/network dependency
# would import. INV-12: none may appear anywhere in the Infrastructure source.
_FORBIDDEN_EXTERNAL_IMPORTS = {
    "requests", "urllib", "urllib2", "urllib3", "http", "httpx", "aiohttp",
    "socket", "ssl", "asyncio", "openai", "anthropic", "boto3", "botocore",
    "google", "cohere", "langchain", "llama_index", "llama_cpp", "litellm",
    "transformers", "torch", "psycopg2", "psycopg", "sqlalchemy", "sqlite3",
    "redis", "pymongo", "kafka", "grpc", "paramiko", "smtplib", "ftplib",
}


class TestNoExternalDependency(unittest.TestCase):
    """INV-12: Infrastructure holds no external dependency; the Tool boundary
    is the only place external coupling may ever attach."""

    def test_source_imports_nothing_external(self):
        offenders = []
        for py in _INFRA_DIR.rglob("*.py"):
            tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [a.name.split(".")[0] for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [(node.module or "").split(".")[0]]
                else:
                    continue
                for n in names:
                    if n in _FORBIDDEN_EXTERNAL_IMPORTS:
                        offenders.append((py.name, n))
        self.assertEqual(offenders, [], f"external imports found: {offenders}")

    def test_tool_boundary_holds_nothing_external_on_provision(self):
        tb = ToolBoundary()
        tb.provision()
        # A freshly provisioned boundary has registered no Tools and opened no
        # external handle; it is simply ready to accept registrations.
        self.assertTrue(tb.is_ready)
        self.assertFalse(tb.is_registered("anything"))


class TestFailClosed(unittest.TestCase):
    """PR-4 / spec §11: facilities halt rather than degrade."""

    def test_use_before_provision_raises(self):
        s = LocalAppendOnlyStorage(base_dir=Path(tempfile.mkdtemp()) / "s")
        with self.assertRaises(FacilityUnavailable):
            list(s.read("p"))

    def test_filesystem_resolve_before_provision_raises(self):
        fs = FilesystemFacility()
        with self.assertRaises(FacilityUnavailable):
            fs.resolve("x")

    def test_failed_provision_marks_facility_failed(self):
        class _Bad(Facility):
            name = "bad"

            def _provision(self):
                raise RuntimeError("boom")

        b = _Bad()
        with self.assertRaises(RuntimeError):
            b.provision()
        self.assertIs(b.state, FacilityState.FAILED)
        self.assertFalse(b.is_ready)

    def test_bootstrap_detects_cycle(self):
        boot = Bootstrap()
        boot.register("a", LocalExecutionSubstrate(), depends_on=("b",))
        boot.register("b", LocalExecutionSubstrate(), depends_on=("a",))
        with self.assertRaises(BootstrapError):
            boot.establish()

    def test_bootstrap_unknown_dependency(self):
        boot = Bootstrap()
        boot.register("a", LocalExecutionSubstrate(), depends_on=("missing",))
        with self.assertRaises(BootstrapError):
            boot.establish()


class TestAppendOnlyStorage(unittest.TestCase):
    """Storage offers append and read only — no edit, no delete (the discipline
    the Trace entity will later require; here offered generically)."""

    def setUp(self):
        self.base = Path(tempfile.mkdtemp()) / "store"
        self.s = LocalAppendOnlyStorage(base_dir=self.base)
        self.s.provision()

    def test_append_then_read_preserves_order(self):
        self.s.append("p", b"first")
        self.s.append("p", b"second")
        self.assertEqual(list(self.s.read("p")), [b"first", b"second"])

    def test_no_edit_or_delete_surface(self):
        # The facility exposes no mutation/removal capability at all.
        for forbidden in ("edit", "update", "delete", "remove", "truncate", "overwrite"):
            self.assertFalse(hasattr(self.s, forbidden), f"storage must not expose {forbidden}")

    def test_newline_record_rejected(self):
        with self.assertRaises(ValueError):
            self.s.append("p", b"has\nnewline")

    def test_partition_name_cannot_escape(self):
        for bad in ("../evil", "a/b", ".", ""):
            with self.assertRaises(ValueError):
                self.s.append(bad, b"x")


class TestFilesystemBounds(unittest.TestCase):
    def test_resolve_cannot_escape_root(self):
        root = Path(tempfile.mkdtemp())
        fs = FilesystemFacility(root=root)
        fs.provision()
        with self.assertRaises(PathEscapesRoot):
            fs.resolve("..", "..", "etc")


class TestToolBoundaryContract(unittest.TestCase):
    def test_duplicate_and_unknown_are_fail_closed(self):
        tb = ToolBoundary()
        tb.provision()

        class _T(infra.ExternalTool):
            @property
            def canonical_key(self):
                return "tool.example"

            def invoke(self, action, parameters):
                return Success(value={"action": action})

        tb.register(_T())
        with self.assertRaises(ToolAlreadyRegistered):
            tb.register(_T())
        with self.assertRaises(ToolNotRegistered):
            tb.invoke("tool.unknown", "act", {})
        out = tb.invoke("tool.example", "act", {"k": "v"})
        self.assertIsInstance(out, Success)


class TestDefaultBootstrapAssembly(unittest.TestCase):
    def test_default_infrastructure_establishes_in_order(self):
        # Hermetic (Phase 3.26 finding F-4): root all storage in an isolated
        # temp directory that is removed after the test, so repeated runs never
        # accumulate state and no repository artifact is left behind.
        with tempfile.TemporaryDirectory() as tmp:
            boot = infra.build_default_infrastructure(
                storage_subdir="probe_store", base_dir=Path(tmp)
            )
            self.assertFalse(boot.established)  # nothing established on assembly
            boot.establish()
            self.assertTrue(boot.established)
            # Every facility provisioned.
            for name, state in boot.states().items():
                self.assertIs(state, FacilityState.PROVISIONED, f"{name} not provisioned")
            # Storage is usable and append-only through the established graph.
            storage = boot.get("storage")
            storage.append("probe", b"ok")
            self.assertEqual(list(storage.read("probe")), [b"ok"])
            boot.teardown()
            self.assertFalse(boot.established)


if __name__ == "__main__":
    unittest.main()
