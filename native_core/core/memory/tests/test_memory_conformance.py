"""
Memory conformance tests (Blueprint §27; memory_spec; Freeze INV-5/7/8; PR-3/PR-4).

Each test asserts a governance property:
  - derives ONLY from Trace (TraceReader is the only source).
  - never mutates Trace (INV-5) — Trace corpus unchanged after derivation.
  - candidate generation ONLY; no promote/approve/reject/authority (INV-8; PR-3).
  - candidates are prioritized, never gated (every distinct memory appears).
  - dependency rules: no import of Governance/Knowledge/…/execution/external.
  - fail closed (PR-4): no TraceReader / unavailable Trace -> raise, not fabricate.
  - deterministic + round-trip: derivation is stable and recomputable.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.memory.tests.test_memory_conformance
"""

from __future__ import annotations

import ast
import inspect
import tempfile
import unittest
from pathlib import Path

from native_core.core import memory as memory_pkg
from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.memory import (
    DEFAULT_RETENTION_WINDOW,
    MemoryReader,
    MemoryRecord,
    PromotionCandidate,
    apply_retention,
    extract,
    generate_candidates,
)
from native_core.core.trace import TraceReader, TraceWriter, new_record

_MEMORY_DIR = Path(memory_pkg.__file__).resolve().parent

_FORBIDDEN_EXTERNAL = {
    "requests", "urllib", "http", "httpx", "aiohttp", "socket", "ssl",
    "openai", "anthropic", "boto3", "google", "langchain", "llama_index",
    "litellm", "transformers", "torch", "psycopg", "sqlalchemy", "sqlite3",
    "redis", "pymongo", "grpc",
}
# Memory may depend only on Infrastructure and Trace; never on subsystems it
# feeds or that derive elsewhere, nor on the legacy harness.
_FORBIDDEN_INTERNAL = {
    "governance", "knowledge", "capability", "skill", "workflow", "agent",
    "runtime", "optimization", "execution",
}


def _trace_stack_with(records):
    storage = LocalAppendOnlyStorage(base_dir=Path(tempfile.mkdtemp()) / "trace")
    storage.provision()
    writer = TraceWriter(storage)
    for r in records:
        writer.write(r)
    return storage, TraceReader(storage)


def _rec(instance, outputs, status="success"):
    return new_record(
        agent_definition_version="1.0", agent_instance=instance,
        runtime="runtime.local", outputs=outputs, status=status,
    )


class TestDerivesFromTrace(unittest.TestCase):
    def test_memory_reads_only_via_trace_reader(self):
        storage, reader = _trace_stack_with([_rec("inst-1", {"saw": "A"})])
        mem = MemoryReader(reader).read()
        self.assertEqual(len(mem), 1)
        self.assertEqual(mem[0].scope, "inst-1")
        self.assertEqual(dict(mem[0].content), {"saw": "A"})

    def test_extract_is_pure_over_trace_records(self):
        recs = [_rec("i", {"x": 1}), _rec("j", {"y": 2})]
        _, reader = _trace_stack_with(recs)
        trace_records = tuple(reader.read())
        m1 = extract(trace_records)
        m2 = extract(trace_records)
        self.assertEqual(m1, m2)  # deterministic
        self.assertEqual(len(m1), 2)


class TestNeverMutatesTrace(unittest.TestCase):
    def test_trace_corpus_unchanged_after_derivation(self):
        storage, reader = _trace_stack_with([_rec("i", {"a": 1}), _rec("i", {"b": 2})])
        before = list(storage.read("trace"))
        mr = MemoryReader(reader)
        mr.read()
        mr.candidates()
        after = list(storage.read("trace"))
        self.assertEqual(before, after)  # Memory wrote nothing to Trace (INV-5)


class TestCandidateGenerationOnly(unittest.TestCase):
    def test_no_promote_approve_reject_authority_anywhere(self):
        surface = [memory_pkg, MemoryReader, PromotionCandidate]
        for obj in surface:
            names = dir(obj)
            for forbidden in ("promote", "approve", "reject", "govern", "authorize", "decide", "gate"):
                self.assertNotIn(forbidden, names, f"{obj} must not expose {forbidden}")

    def test_candidate_is_observation_without_decision_field(self):
        import dataclasses
        fields = {f.name for f in dataclasses.fields(PromotionCandidate)}
        self.assertEqual(fields, {"scope", "observed_content", "occurrence_count"})
        for forbidden in ("decision", "approved", "promoted", "verdict", "status"):
            self.assertNotIn(forbidden, fields)

    def test_candidates_prioritize_but_never_gate(self):
        # Every distinct observation must appear as a candidate — none filtered.
        records = [
            MemoryRecord(scope="i", content={"v": "A"}),
            MemoryRecord(scope="i", content={"v": "A"}),  # repeat -> higher count
            MemoryRecord(scope="i", content={"v": "B"}),
            MemoryRecord(scope="j", content={"v": "A"}),
        ]
        cands = generate_candidates(records)
        self.assertEqual(len(cands), 3)  # (i,A), (i,B), (j,A) — nothing gated out
        # Prioritized: the repeated (i,A) with count 2 comes first.
        self.assertEqual((cands[0].scope, cands[0].occurrence_count), ("i", 2))

    def test_generate_candidates_is_deterministic(self):
        records = [MemoryRecord(scope="i", content={"v": n % 2}) for n in range(6)]
        self.assertEqual(generate_candidates(records), generate_candidates(records))


class TestRetention(unittest.TestCase):
    def test_bounded_window_expires_oldest_per_scope(self):
        records = [MemoryRecord(scope="i", content={"n": n}) for n in range(5)]
        kept = apply_retention(records, window=2)
        self.assertEqual([dict(m.content) for m in kept], [{"n": 3}, {"n": 4}])

    def test_unbounded_window_is_fail_closed(self):
        for bad in (None, -1, "x"):
            with self.assertRaises(ValueError):
                apply_retention([MemoryRecord(scope="i", content=1)], window=bad)  # type: ignore[arg-type]


class TestImmutability(unittest.TestCase):
    def test_memory_record_is_deeply_immutable(self):
        r = MemoryRecord(scope="i", content={"nested": [1, 2]})
        import dataclasses
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.scope = "x"  # type: ignore[misc]
        with self.assertRaises(AttributeError):
            r.content["nested"].append(3)


class TestFailClosed(unittest.TestCase):
    def test_no_trace_reader_raises(self):
        with self.assertRaises(ValueError):
            MemoryReader(None)  # type: ignore[arg-type]

    def test_unavailable_trace_source_propagates(self):
        # TraceReader over an unprovisioned storage -> reading fails closed.
        from native_core.core.infrastructure.facility import FacilityUnavailable
        storage = LocalAppendOnlyStorage(base_dir=Path(tempfile.mkdtemp()) / "np")
        reader = TraceReader(storage)  # storage NOT provisioned
        with self.assertRaises(FacilityUnavailable):
            MemoryReader(reader).read()


class TestDependencies(unittest.TestCase):
    def test_no_forbidden_imports(self):
        offenders = []
        for py in _MEMORY_DIR.rglob("*.py"):
            if py.name == "test_memory_conformance.py":
                continue
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
                    parts = set(m.split("."))
                    if head in _FORBIDDEN_EXTERNAL:
                        offenders.append((py.name, m, "external"))
                    if _FORBIDDEN_INTERNAL & parts:
                        offenders.append((py.name, m, "forbidden-subsystem/legacy"))
        self.assertEqual(offenders, [], f"forbidden imports: {offenders}")

    def test_reader_cross_boundary_dependency_is_trace_only(self):
        # Parse reader.py's imports (not its prose): the only cross-boundary
        # Native-Core dependency is Trace. Memory MAY depend on Infrastructure,
        # but this design derives via TraceReader and imports no other boundary.
        tree = ast.parse((_MEMORY_DIR / "reader.py").read_text(encoding="utf-8"))
        # A sibling-boundary import is `from ..<boundary> import ...`, which ast
        # represents as level==2 with module=<boundary> (the dots are in level).
        cross_boundary = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.level == 2
        }
        self.assertEqual(cross_boundary, {"trace"}, f"unexpected cross-boundary imports: {cross_boundary}")


class TestRoundTripDerivation(unittest.TestCase):
    def test_derivation_is_recomputable_and_equal(self):
        storage, reader = _trace_stack_with([_rec("i", {"k": "v"}), _rec("i", {"k": "v"})])
        first = MemoryReader(reader).read()
        second = MemoryReader(reader).read()
        self.assertEqual(first, second)  # recomputable from Trace, identical


if __name__ == "__main__":
    unittest.main()
