"""
Dedicated unit tests for execution/trace.py.

Foundation Test Coverage Hardening phase. Verifies observable behavior
only: append-only writes, real file I/O, record shape -- never
implementation internals. Uses a temporary directory for every write so
the real execution/traces/ corpus is never touched.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import trace


class _FakeInstance:
    instance_id = "instance-fake"
    agent_definition_name = "Fake Agent"
    agent_definition_version = "1.0"


class _FakeRuntime:
    canonical_key = "runtime.fake"


class NewRecordTest(unittest.TestCase):
    def test_new_record_populates_from_instance_and_runtime(self):
        record = trace.new_record(_FakeInstance(), _FakeRuntime(), outputs={"event": "spawned"})
        self.assertEqual(record.agent_definition_name, "Fake Agent")
        self.assertEqual(record.agent_definition_version, "1.0")
        self.assertEqual(record.agent_instance_id, "instance-fake")
        self.assertEqual(record.runtime, "runtime.fake")
        self.assertEqual(record.schema_version, trace.SCHEMA_VERSION)
        self.assertEqual(record.status, "success")

    def test_new_record_defaults_empty_collections_not_none(self):
        record = trace.new_record(_FakeInstance(), _FakeRuntime())
        self.assertEqual(record.skills_used, ())
        self.assertEqual(record.tools_used, ())
        self.assertEqual(record.knowledge_consumed, ())
        self.assertEqual(record.memory_consumed, ())

    def test_new_record_generates_unique_trace_ids(self):
        r1 = trace.new_record(_FakeInstance(), _FakeRuntime())
        r2 = trace.new_record(_FakeInstance(), _FakeRuntime())
        self.assertNotEqual(r1.trace_id, r2.trace_id)
        self.assertTrue(r1.trace_id.startswith("trace-"))

    def test_new_record_accepts_arbitrary_status(self):
        record = trace.new_record(_FakeInstance(), _FakeRuntime(), status="escalation")
        self.assertEqual(record.status, "escalation")


class TraceWriterTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.patcher = mock.patch.object(trace, "TRACE_DIR", Path(self.tmpdir.name))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.tmpdir.cleanup()

    def test_write_creates_file_and_returns_record(self):
        writer = trace.TraceWriter()
        record = trace.new_record(_FakeInstance(), _FakeRuntime(), outputs={"event": "spawned"})
        returned = writer.write(record)
        self.assertEqual(returned, record)
        self.assertTrue(writer.path.is_file())

    def test_write_appends_not_overwrites(self):
        writer = trace.TraceWriter()
        r1 = trace.new_record(_FakeInstance(), _FakeRuntime(), outputs={"event": "spawned"})
        r2 = trace.new_record(_FakeInstance(), _FakeRuntime(), outputs={"event": "terminated"})
        writer.write(r1)
        writer.write(r2)
        lines = writer.path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(json.loads(lines[0])["trace_id"], r1.trace_id)
        self.assertEqual(json.loads(lines[1])["trace_id"], r2.trace_id)

    def test_written_record_round_trips_through_json(self):
        writer = trace.TraceWriter()
        record = trace.new_record(_FakeInstance(), _FakeRuntime(), outputs={"event": "spawned"}, skills_used=("skill.a",))
        writer.write(record)
        line = writer.path.read_text(encoding="utf-8").splitlines()[0]
        loaded = json.loads(line)
        self.assertEqual(loaded["trace_id"], record.trace_id)
        self.assertEqual(loaded["skills_used"], ["skill.a"])  # tuple -> list via JSON, expected

    def test_distinct_writers_get_distinct_files_by_default(self):
        w1 = trace.TraceWriter()
        w2 = trace.TraceWriter()
        self.assertNotEqual(w1.path, w2.path)

    def test_explicit_run_id_is_used_verbatim(self):
        writer = trace.TraceWriter(run_id="run-explicit-test")
        self.assertEqual(writer.path.name, "run-explicit-test.jsonl")

    def test_write_never_deletes_or_truncates_prior_content(self):
        writer = trace.TraceWriter()
        for i in range(5):
            writer.write(trace.new_record(_FakeInstance(), _FakeRuntime(), outputs={"n": i}))
        self.assertEqual(len(writer.path.read_text(encoding="utf-8").splitlines()), 5)


if __name__ == "__main__":
    unittest.main()
