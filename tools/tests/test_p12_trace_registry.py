"""P12-W4 durable Trace registry conformance.

The controls that matter are that an empty registry says `UNKNOWN` rather than
"no failures", that reading is delegated to the Native Core reader rather than
re-implemented, and that `escalation` is never counted as `failure`.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.trace import TRACE_PARTITION, TraceWriter, new_record
from tools import p12_trace_registry as registry
from tools import p12_self_model as model
from tools.derived_views import UNKNOWN, VERIFIED


def _store_with(tmp: Path, name: str, *statuses: str) -> Path:
    path = tmp / name
    storage = LocalAppendOnlyStorage(path)
    storage.provision()
    writer = TraceWriter(storage)
    for index, status in enumerate(statuses):
        writer.write(new_record(
            agent_definition_version="1.0",
            agent_instance=f"instance-{index}",
            runtime="test-runtime",
            status=status,
            outputs={"index": index},
        ))
    return path


class DiscoveryIsByShapeNotByList(unittest.TestCase):
    def test_a_missing_root_discovers_nothing_and_does_not_raise(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(registry.discover(Path(tmp) / "absent"), ())

    def test_a_directory_without_a_partition_file_is_not_a_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "not-a-store").mkdir()
            self.assertEqual(registry.discover(Path(tmp)), ())

    def test_a_directory_holding_a_partition_file_is_a_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            _store_with(Path(tmp), "alpha", "success")
            stores = registry.discover(Path(tmp))
            self.assertEqual(len(stores), 1)
            self.assertEqual(stores[0].name, "alpha")
            self.assertTrue(stores[0].partition_file.is_file())

    def test_multiple_stores_are_all_discovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            _store_with(Path(tmp), "alpha", "success")
            _store_with(Path(tmp), "beta", "failure", "success")
            self.assertEqual(
                tuple(s.name for s in registry.discover(Path(tmp))), ("alpha", "beta"))


class EmptyIsNotSuccess(unittest.TestCase):
    """Zero records is absence of evidence, never evidence of absence."""

    def test_no_store_yields_no_records_and_no_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = registry.what_has_run(Path(tmp))
            self.assertEqual(summary["stores"], 0)
            self.assertEqual(summary["records"], 0)
            self.assertEqual(registry.what_has_failed(Path(tmp)), ())

    def test_the_self_model_reports_unknown_rather_than_zero_failures(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = registry.STORE_ROOT
            try:
                registry.STORE_ROOT = Path(tmp)
                answer = model.failed()
            finally:
                registry.STORE_ROOT = original
        self.assertEqual(answer.status, UNKNOWN)
        self.assertIsNone(
            answer.value,
            "reporting 0 failures from 0 records would be the cleanest possible lie",
        )


class StatusVocabularyIsTheRatifiedOne(unittest.TestCase):
    def test_escalation_is_not_counted_as_failure(self):
        """DP-02 §3 E11-03: a correct refusal is not an execution failure."""
        with tempfile.TemporaryDirectory() as tmp:
            _store_with(Path(tmp), "alpha", "escalation", "escalation")
            self.assertEqual(registry.what_has_failed(Path(tmp)), ())
            self.assertEqual(
                registry.what_has_run(Path(tmp))["by_status"], {"escalation": 2})

    def test_failure_is_counted_and_success_is_not(self):
        with tempfile.TemporaryDirectory() as tmp:
            _store_with(Path(tmp), "alpha", "failure", "success", "failure")
            self.assertEqual(len(registry.what_has_failed(Path(tmp))), 2)
            self.assertEqual(
                registry.what_has_run(Path(tmp))["by_status"],
                {"failure": 2, "success": 1})


class ReadingIsDelegatedNotReimplemented(unittest.TestCase):
    def test_records_come_back_as_native_core_trace_records(self):
        from native_core.core.trace import TraceRecord
        with tempfile.TemporaryDirectory() as tmp:
            _store_with(Path(tmp), "alpha", "success")
            record = registry.discover(Path(tmp))[0].records()[0]
            self.assertIsInstance(record, TraceRecord)

    def test_a_corrupt_record_is_refused_by_the_reader_not_smoothed_over(self):
        """The registry parses nothing itself, so an invalid record must raise
        rather than be quietly dropped into a count."""
        with tempfile.TemporaryDirectory() as tmp:
            path = _store_with(Path(tmp), "alpha", "success")
            with open(path / TRACE_PARTITION, "ab") as handle:
                handle.write(json.dumps({"not": "a trace record"}).encode() + b"\n")
            with self.assertRaises(Exception):
                registry.discover(Path(tmp))[0].records()


class TheResidentStoreCarriesRealEvidence(unittest.TestCase):
    """Against the store the root proof actually wrote."""

    def test_the_resident_store_is_discovered(self):
        self.assertGreaterEqual(len(registry.discover()), 1)

    def test_it_records_a_real_failure_and_a_real_success(self):
        by_status = registry.what_has_run()["by_status"]
        self.assertGreaterEqual(by_status.get("failure", 0), 1)
        self.assertGreaterEqual(by_status.get("success", 0), 1)

    def test_what_failed_is_answered_from_evidence(self):
        answer = model.failed()
        self.assertEqual(answer.status, VERIFIED)
        self.assertGreaterEqual(answer.value["failures"], 1)

    def test_the_trace_registry_is_not_the_source_of_the_running_answer(self):
        """A Trace says what ran, past tense. F-4 is answered from runtime
        observation instead, and this asserts the wiring never crossed."""
        running = model.running()
        self.assertNotIn("Trace", running.source)
        self.assertNotEqual(running.value, model.failed().value)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
