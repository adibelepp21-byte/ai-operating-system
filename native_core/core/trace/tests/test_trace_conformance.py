"""
Trace conformance tests (Blueprint §27; trace_spec; Freeze INV-4/5/6).

Each test asserts a governance property:
  - INV-4 : one record per write; production is unconditional (no enable flag).
  - INV-5 : records are immutable (frozen, deeply); the boundary exposes no
            edit/update/delete anywhere; storage is append-only.
  - INV-6 : knowledge/memory consumed are captured content that survives a
            round-trip in full; a read record is self-contained.
  - schema: exactly the ten Domain Model §2.1 fields; no trace_id/timestamp/
            schema_version was added.
  - determinism: the same record encodes to identical bytes.
  - fail closed: unprovisioned storage, invalid status, and missing required
            fields all raise.
  - dependencies: no external import; no import of Memory/Knowledge/
            Optimization; no import of legacy execution/.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.trace.tests.test_trace_conformance
"""

from __future__ import annotations

import ast
import dataclasses
import tempfile
import unittest
from pathlib import Path

from native_core.core import trace as trace_pkg
from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.infrastructure.facility import FacilityUnavailable
from native_core.core.trace import (
    REQUIRED_FIELDS,
    InvalidTraceRecord,
    TraceReader,
    TraceRecord,
    TraceWriter,
    from_mapping,
    new_record,
)
from native_core.core.trace.writer import _encode

_TRACE_DIR = Path(trace_pkg.__file__).resolve().parent

_FORBIDDEN_EXTERNAL = {
    "requests", "urllib", "http", "httpx", "aiohttp", "socket", "ssl",
    "asyncio", "openai", "anthropic", "boto3", "google", "langchain",
    "llama_index", "litellm", "transformers", "torch", "psycopg", "sqlalchemy",
    "sqlite3", "redis", "pymongo", "grpc",
}
# Trace must not depend on subsystems that derive from it (Blueprint §20/§21),
# nor on the legacy harness.
_FORBIDDEN_INTERNAL = {"memory", "knowledge", "optimization", "execution"}


def _fresh_storage():
    s = LocalAppendOnlyStorage(base_dir=Path(tempfile.mkdtemp()) / "trace_store")
    s.provision()
    return s


def _sample(**overrides):
    base = dict(
        agent_definition_version="1.0",
        agent_instance="instance-abc",
        runtime="runtime.local",
        outputs={"event": "did-something"},
        status="success",
    )
    base.update(overrides)
    return new_record(**base)


class TestRequiredContents(unittest.TestCase):
    """Domain Model §2.1: exactly ten fields, nothing added."""

    def test_exactly_the_ten_required_fields(self):
        names = tuple(f.name for f in dataclasses.fields(TraceRecord))
        self.assertEqual(set(names), set(REQUIRED_FIELDS))
        self.assertEqual(len(names), 10)

    def test_no_schema_extension_fields(self):
        # No trace_id, timestamp, or schema_version — those are reserved to a
        # governed Domain-Model change (trace_spec §3/§12).
        names = {f.name for f in dataclasses.fields(TraceRecord)}
        for forbidden in ("trace_id", "timestamp", "schema_version", "id", "created_at"):
            self.assertNotIn(forbidden, names)


class TestImmutability(unittest.TestCase):
    """INV-5: records are immutable; no edit/delete surface."""

    def test_record_is_frozen(self):
        r = _sample()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.agent_instance = "other"  # type: ignore[misc]

    def test_nested_content_is_deeply_immutable(self):
        r = _sample(cost_resource_metadata={"nested": {"k": 1}})
        # cost_resource_metadata is a read-only mapping; mutation raises.
        with self.assertRaises(TypeError):
            r.cost_resource_metadata["nested"] = {}  # type: ignore[index]

    def test_no_edit_or_delete_methods_anywhere(self):
        for obj in (TraceRecord, TraceWriter, TraceReader):
            for forbidden in ("edit", "update", "delete", "remove", "truncate", "overwrite", "set"):
                self.assertFalse(hasattr(obj, forbidden), f"{obj.__name__} must not expose {forbidden}")

    def test_direct_construction_is_deeply_immutable(self):
        # Phase 3.25 finding F-1 / Phase 3.26 closure: the public constructor
        # must yield the same deep immutability as new_record — no construction
        # path may produce a mutable record.
        r = TraceRecord(
            agent_definition_version="1",
            agent_instance="i",
            runtime="rt",
            outputs={"nested": [1, 2]},
            cost_resource_metadata={"k": {"x": 1}},
        )
        # Nested content is frozen: append and key-injection both fail.
        with self.assertRaises(AttributeError):
            r.outputs["nested"].append(3)
        with self.assertRaises(TypeError):
            r.outputs["injected"] = "no"  # type: ignore[index]
        with self.assertRaises(TypeError):
            r.cost_resource_metadata["k"]["x"] = 2  # type: ignore[index]

    def test_all_construction_paths_have_identical_immutability(self):
        made = {
            "direct": TraceRecord(
                agent_definition_version="1", agent_instance="i", runtime="rt",
                outputs={"a": [1]},
            ),
            "factory": new_record(
                agent_definition_version="1", agent_instance="i", runtime="rt",
                outputs={"a": [1]},
            ),
            "reader": from_mapping(
                new_record(
                    agent_definition_version="1", agent_instance="i", runtime="rt",
                    outputs={"a": [1]},
                ).to_mapping()
            ),
        }
        for label, rec in made.items():
            with self.assertRaises(AttributeError, msg=f"{label} outputs mutable"):
                rec.outputs["a"].append(2)


class TestUnconditionalOnePerWrite(unittest.TestCase):
    """INV-4 / §14.2: one record per write; production cannot be disabled."""

    def test_write_appends_exactly_one_record(self):
        storage = _fresh_storage()
        writer = TraceWriter(storage)
        writer.write(_sample())
        writer.write(_sample(status="failure"))
        records = list(TraceReader(storage).read())
        self.assertEqual(len(records), 2)

    def test_write_has_no_enable_or_conditional_parameter(self):
        import inspect
        params = set(inspect.signature(TraceWriter.write).parameters) - {"self"}
        self.assertEqual(params, {"record"})  # only the record; nothing to disable production


class TestCaptureNotReference(unittest.TestCase):
    """INV-6 / PR-5: knowledge/memory consumed are captured content, self-contained."""

    def test_captured_content_survives_roundtrip_in_full(self):
        knowledge = ({"item": "K1", "content": "the full captured text of K1"},)
        memory = ({"item": "M1", "content": "captured memory content"},)
        storage = _fresh_storage()
        TraceWriter(storage).write(_sample(knowledge_consumed=knowledge, memory_consumed=memory))
        (read_back,) = list(TraceReader(storage).read())
        # Content is embedded in the record, not a reference — it comes back in full.
        self.assertEqual(read_back.knowledge_consumed[0]["content"], "the full captured text of K1")
        self.assertEqual(read_back.memory_consumed[0]["content"], "captured memory content")

    def test_record_is_self_contained_no_external_lookup(self):
        # from_mapping reconstructs a complete record from its own bytes alone.
        r = _sample(knowledge_consumed=({"content": "x"},))
        rebuilt = from_mapping(r.to_mapping())
        self.assertEqual(rebuilt, r)


class TestDeterminism(unittest.TestCase):
    def test_same_record_encodes_identically(self):
        r = _sample(cost_resource_metadata={"b": 2, "a": 1})
        self.assertEqual(_encode(r), _encode(r))
        # Field order in the source dict must not change the encoding.
        r2 = _sample(cost_resource_metadata={"a": 1, "b": 2})
        self.assertEqual(_encode(r), _encode(r2))


class TestFailClosed(unittest.TestCase):
    def test_write_to_unprovisioned_storage_raises(self):
        storage = LocalAppendOnlyStorage(base_dir=Path(tempfile.mkdtemp()) / "np")
        # not provisioned
        with self.assertRaises(FacilityUnavailable):
            TraceWriter(storage).write(_sample())

    def test_invalid_status_raises(self):
        with self.assertRaises(InvalidTraceRecord):
            _sample(status="ok")

    def test_missing_identity_field_raises(self):
        with self.assertRaises(InvalidTraceRecord):
            new_record(agent_definition_version="1.0", agent_instance="", runtime="r")

    def test_from_mapping_missing_field_raises(self):
        m = _sample().to_mapping()
        del m["status"]
        with self.assertRaises(InvalidTraceRecord):
            from_mapping(m)

    def test_write_requires_a_trace_record(self):
        storage = _fresh_storage()
        with self.assertRaises(TypeError):
            TraceWriter(storage).write({"not": "a record"})  # type: ignore[arg-type]


class TestDependencies(unittest.TestCase):
    def test_no_forbidden_imports(self):
        offenders = []
        for py in _TRACE_DIR.rglob("*.py"):
            tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    mods = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    mods = [node.module or ""]
                else:
                    continue
                for m in mods:
                    head = m.split(".")[0]
                    tail = set(m.split("."))
                    if head in _FORBIDDEN_EXTERNAL:
                        offenders.append((py.name, m, "external"))
                    if _FORBIDDEN_INTERNAL & tail:
                        # Allow the test file's own references to the forbidden
                        # NAMES in string form; here we only catch real imports.
                        offenders.append((py.name, m, "derives-from-trace/legacy"))
        # The test module imports nothing forbidden; source modules import only
        # infrastructure + shared + stdlib.
        offenders = [o for o in offenders if o[0] != "test_trace_conformance.py"]
        self.assertEqual(offenders, [], f"forbidden imports: {offenders}")

    def test_append_only_storage_has_no_mutation_surface(self):
        storage = _fresh_storage()
        for forbidden in ("edit", "update", "delete", "remove", "truncate", "overwrite"):
            self.assertFalse(hasattr(storage, forbidden))


if __name__ == "__main__":
    unittest.main()
