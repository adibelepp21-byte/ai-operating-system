"""FS-04 — data and state: what persists, what does not, and what cannot change.

`docs/fullstack/FS-04-DATA-AND-STATE.md` classifies each state class. These
tests hold the classification to the running system: durable classes survive
a restart, in-process classes do not, persisted bytes are only ever appended
to, a copied store restores everything, and a corrupt record fails closed.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from fullstack.tests.support import OBSERVER_TOKEN, OPERATOR_TOKEN, Harness
from fullstack.tests.test_backend_api import RUN, run_body

DURABLE_PARTITIONS = {"trace", "fullstack-runs", "fullstack-audit"}


class _Store(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.data = Path(self._tmp.name) / "data"

    def tearDown(self):
        self._tmp.cleanup()

    def boot(self, data=None):
        return Harness(data_dir=data or self.data)

    def snapshot(self, data=None):
        store = (data or self.data) / "storage"
        return {p.name: p.read_bytes() for p in store.iterdir()}


class Durability(_Store):
    def test_runs_traces_and_audit_survive_a_restart(self):
        first = self.boot()
        run = first.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        first.close()

        second = self.boot()
        try:
            self.assertEqual(run, second.call("GET", f"{RUN}/{run['run_id']}", OBSERVER_TOKEN)[2])
            traces = second.call("GET", "/api/v1/traces", OBSERVER_TOKEN)[2]
            self.assertEqual(3, traces["total"])
            later = second.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
            self.assertEqual("run-00002", later["run_id"])
            self.assertNotEqual(run["runtime_id"], later["runtime_id"])
            audit = second.call("GET", "/api/v1/audit", OPERATOR_TOKEN)[2]["entries"]
            self.assertGreaterEqual(len(audit), 4)
        finally:
            second.close()

    def test_workflow_lifecycle_state_is_in_process_by_design(self):
        """`FD-P9-001 §12.4`: the lifecycle is in-process. The run record, not
        the monitor, is what outlives the Runtime."""
        first = self.boot()
        first.call("POST", RUN, OPERATOR_TOKEN, run_body())
        self.assertEqual(1, len(first.aios._runtime.workflows.monitor.monitored()))
        first.close()
        second = self.boot()
        try:
            self.assertEqual((), second.aios._runtime.workflows.monitor.monitored())
            self.assertEqual(1, len(second.aios.runs()))
        finally:
            second.close()

    def test_each_run_maps_to_its_own_runtimes_traces(self):
        for _ in range(2):
            h = self.boot()
            h.call("POST", RUN, OPERATOR_TOKEN, run_body())
            h.call("POST", RUN, OPERATOR_TOKEN, run_body(document="docs/absent.md"))
            h.close()
        h = self.boot()
        try:
            records = h.call("GET", "/api/v1/traces?limit=200", OBSERVER_TOKEN)[2]["records"]
            for run in h.aios.runs():
                with self.subTest(run=run["run_id"]):
                    span = records[run["trace"]["from"]:run["trace"]["to"]]
                    self.assertEqual(run["trace"]["count"], len(span))
                    self.assertEqual({run["runtime_id"]}, {r["runtime"] for r in span})
        finally:
            h.close()


class Integrity(_Store):
    def test_persisted_bytes_are_only_ever_appended_to(self):
        h = self.boot()
        h.call("POST", RUN, OPERATOR_TOKEN, run_body())
        before = self.snapshot()
        h.call("POST", RUN, OPERATOR_TOKEN, run_body(document="docs/absent.md"))
        h.call("GET", "/api/v1/runs", OBSERVER_TOKEN)
        h.close()
        after = self.snapshot()
        for name, content in before.items():
            with self.subTest(partition=name):
                self.assertTrue(after[name].startswith(content))
                self.assertGreater(len(after[name]), len(content))

    def test_no_schema_beyond_the_classified_partitions(self):
        """Act NC-14: no store is created without an owner and a requirement."""
        h = self.boot()
        h.call("POST", RUN, OPERATOR_TOKEN, run_body())
        h.call("GET", "/api/v1/runtime")
        h.close()
        self.assertEqual(DURABLE_PARTITIONS, set(self.snapshot()))

    def test_a_corrupt_record_fails_closed(self):
        h = self.boot()
        h.call("POST", RUN, OPERATOR_TOKEN, run_body())
        with open(self.data / "storage" / "fullstack-runs", "ab") as handle:
            handle.write(b"{truncated\n")
        try:
            from unittest import mock
            with mock.patch("sys.stderr"):
                status = h.call("GET", RUN, OBSERVER_TOKEN)[0]
            self.assertEqual(500, status)
        finally:
            h.close()


class BackupAndRecovery(_Store):
    def test_a_copied_store_restores_every_record(self):
        h = self.boot()
        h.call("POST", RUN, OPERATOR_TOKEN, run_body())
        h.call("POST", RUN, OPERATOR_TOKEN, run_body(document="docs/absent.md"))
        runs = h.aios.runs()
        h.close()

        backup = Path(self._tmp.name) / "backup"
        shutil.copytree(self.data, backup)
        shutil.rmtree(self.data)                      # the original is lost

        restored = self.boot(backup)
        try:
            self.assertEqual(runs, restored.aios.runs())
            self.assertEqual(3 + 2, restored.call("GET", "/api/v1/traces", OBSERVER_TOKEN)[2]["total"])
            self.assertEqual("run-00003", restored.call("POST", RUN, OPERATOR_TOKEN,
                                                        run_body())[2]["run_id"])
        finally:
            restored.close()


if __name__ == "__main__":
    unittest.main()
