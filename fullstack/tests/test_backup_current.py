"""FS-09 final backup and restore drill on current data (ACT-008 `§12`).

The export `FS-09-BACKUP-EXPORT-2026-09-30.jsonl` is the Preview store at
seq <= 510 after the final live suites: 505 records in four partitions,
including the Agent Instance registrations of Scenario A. It is restored into
fresh stores and the application reads it. The 2026-09-27 export
(`test_backup_restore.py`) stays as the historical control.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from fullstack.backend.agents import AGENTS_PARTITION, AgentRegistry, GovernedDefinitions
from fullstack.backend.aios import AIOSApplication, RUNS_PARTITION
from fullstack.backend.security import AUDIT_PARTITION, AuditLedger
from fullstack.deploy import backup
from fullstack.tests.support import OPERATOR_TOKEN, REPO_ROOT, Harness
from fullstack.tests.test_deployment import supabase
from native_core.core.infrastructure import LocalAppendOnlyStorage

EVIDENCE = REPO_ROOT / "docs/fullstack/evidence"
EXPORT = EVIDENCE / "FS-09-BACKUP-EXPORT-2026-09-30.jsonl"
MANIFEST = EVIDENCE / "FS-09-BACKUP-MANIFEST-2026-09-30.json"


def fresh_local(test):
    tmp = tempfile.TemporaryDirectory()
    test.addCleanup(tmp.cleanup)
    store = LocalAppendOnlyStorage(Path(tmp.name) / "storage")
    store.provision()
    return Path(tmp.name), store


class TheCurrentExportMatchesTheLiveStore(unittest.TestCase):

    def setUp(self):
        self.entries = backup.read_file(EXPORT)
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_every_partition_matches_the_server_digest(self):
        summary = backup.summary(self.entries)
        self.assertEqual(set(self.manifest["partitions"]), set(summary))
        for name, expected in self.manifest["partitions"].items():
            with self.subTest(partition=name):
                self.assertEqual(expected["records"], summary[name]["records"])
                self.assertEqual(expected["bytes"], summary[name]["bytes"])
                self.assertEqual(expected["sha256_joined_server"], summary[name]["sha256_joined"])

    def test_the_whole_table_matches_in_seq_order(self):
        table = self.manifest["table"]
        self.assertEqual(505, table["records"])
        self.assertEqual(table["sha256_joined_server"],
                         backup.joined_sha256([e.record for e in self.entries]))
        seqs = [e.seq for e in self.entries]
        self.assertEqual(sorted(seqs), seqs)
        self.assertLessEqual(seqs[-1], 510)

    def test_the_export_file_is_the_one_the_manifest_names(self):
        self.assertEqual(self.manifest["export"]["sha256"], hashlib.sha256(EXPORT.read_bytes()).hexdigest())

    def test_it_is_current_not_historical(self):
        """It holds the Scenario A registrations, which the 2026-09-27 control cannot."""
        self.assertIn(AGENTS_PARTITION, backup.summary(self.entries))
        old = backup.read_file(EVIDENCE / "FS-09-BACKUP-EXPORT-2026-09-27.jsonl")
        self.assertGreater(len(self.entries), 5 * len(old))

    def test_the_export_holds_no_credential(self):
        text = EXPORT.read_text(encoding="utf-8").lower()
        for needle in ("sb_" + "secret_", "ey" + "j", "bearer", "apikey", "service_role",
                       "authorization", "aios_operator_" + "tokens"):
            self.assertNotIn(needle, text)
        subjects = {json.loads(e.record)["subject"] for e in self.entries if e.partition == AUDIT_PARTITION}
        self.assertEqual({None, "founder"}, subjects)


class TheCurrentRestoreIsByteIdentical(unittest.TestCase):

    def setUp(self):
        self.entries = backup.read_file(EXPORT)

    def test_into_a_fresh_local_store(self):
        _, store = fresh_local(self)
        self.assertEqual(505, backup.restore(self.entries, store))
        self.assertEqual([], backup.differences(self.entries, store))
        self.assertEqual(backup.summary(self.entries), backup.summary(backup.export_store(store)))

    def test_into_a_fresh_supabase_store(self):
        store, fake = supabase()
        backup.restore(self.entries, store)
        self.assertEqual([], backup.differences(self.entries, store))
        self.assertEqual(505, len(fake.rows))

    def test_a_diverging_store_is_reported(self):
        _, store = fresh_local(self)
        altered = [backup.Entry(e.seq, e.partition, e.position,
                                e.record + b" " if e.position == 4 and e.partition == AGENTS_PARTITION
                                else e.record) for e in self.entries]
        backup.restore(altered, store)
        self.assertEqual([f"{AGENTS_PARTITION}: record 4 differs"], backup.differences(self.entries, store))


class TheApplicationReadsTheCurrentRestoredState(unittest.TestCase):

    def setUp(self):
        self.entries = backup.read_file(EXPORT)
        self.data_dir, self.store = fresh_local(self)
        backup.restore(self.entries, self.store)
        self.source = backup.by_partition(self.entries)
        self.aios = AIOSApplication(self.data_dir, REPO_ROOT)
        self.aios.start()
        self.addCleanup(self.aios.stop)

    def test_the_runs_are_the_exported_runs(self):
        exported = [json.loads(r) for r in self.source[RUNS_PARTITION]]
        runs = self.aios.runs()
        self.assertEqual(66, len(runs))
        self.assertEqual(list(reversed(exported)), runs)
        self.assertEqual(66, len({r["run_id"] for r in runs}))

    def test_every_run_resolves_its_own_trace(self):
        for run in self.aios.runs():
            trace = self.aios.run_trace(run["run_id"])
            self.assertEqual(run["trace"]["count"], len(trace), run["run_id"])

    def test_the_audit_and_trace_are_the_exported_ones_in_order(self):
        entries = list(AuditLedger(self.aios.storage).entries())
        exported = [json.loads(r) for r in self.source[AUDIT_PARTITION]]
        self.assertEqual(exported, [{k: v for k, v in e.items() if k != "position"} for e in entries])
        self.assertEqual(list(range(245)), [e["position"] for e in entries])
        self.assertEqual(189, self.aios.traces(0, 1000)["total"])

    def test_the_agent_registrations_are_readable_through_the_registry(self):
        registry = AgentRegistry(self.store, GovernedDefinitions(REPO_ROOT))
        exported = [json.loads(r) for r in self.source[AGENTS_PARTITION]]
        instances = registry.instances()
        self.assertEqual(5, len(exported))
        self.assertEqual(len({i["instance_key"] for i in exported}), len(instances))
        for record in instances:
            self.assertEqual("REGISTERED", record["lifecycle"])
            self.assertIs(False, record["grants_authority"])
            self.assertEqual("founder", record["created_by"])
        self.assertIsNotNone(registry.instance(instances[0]["instance_key"]))

    def test_the_restored_store_stays_append_only(self):
        before = {p: list(self.aios.storage.read(p)) for p in self.source}
        self.aios.start_run("document-conformance-review",
                            {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                             "criteria": ["INV-4"]}, "drill")
        for name, records in before.items():
            self.assertEqual(records, list(self.aios.storage.read(name))[:len(records)], name)
        self.assertEqual(67, len(self.aios.runs()))


class TheAPIServesTheCurrentRestoredState(unittest.TestCase):

    def test_runs_instances_and_audit_through_the_api(self):
        data_dir, store = fresh_local(self)
        backup.restore(backup.read_file(EXPORT), store)
        harness = Harness(data_dir=data_dir)
        self.addCleanup(harness.close)
        status, _, body = harness.call("GET", "/api/v1/runs", OPERATOR_TOKEN)
        self.assertEqual((200, 66), (status, len(body["runs"])))
        status, _, body = harness.call("GET", "/api/v1/agent-instances", OPERATOR_TOKEN)
        self.assertEqual(200, status)
        self.assertGreaterEqual(len(body["instances"]), 1)
        key = body["instances"][0]["instance_key"]
        self.assertEqual(200, harness.call("GET", f"/api/v1/agent-instances/{key}", OPERATOR_TOKEN)[0])
        status, _, audit = harness.call("GET", "/api/v1/audit?offset=240&limit=50", OPERATOR_TOKEN)
        self.assertEqual(200, status)
        exported = [json.loads(r) for r in backup.by_partition(backup.read_file(EXPORT))[AUDIT_PARTITION]]
        restored = [e for e in audit["entries"] if e["position"] < 245]
        self.assertEqual(exported[240:], [{k: v for k, v in e.items() if k != "position"} for e in restored])
        self.assertGreaterEqual(len(audit["entries"]), 245 - 240 + 2)    # then this test's own reads


class TheOperatorCommandsOnTheCurrentExport(unittest.TestCase):

    def run_main(self, *argv):
        import contextlib
        import io
        from fullstack.backend.__main__ import main
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_restore_then_verify_then_refuse_a_second_restore(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        target = str(Path(tmp.name) / "drill")
        code, out, _ = self.run_main("backup-restore", "--export", str(EXPORT), "--data-dir", target)
        self.assertEqual((0, True), (code, json.loads(out)["identical"]))
        code, out, _ = self.run_main("backup-verify", "--export", str(EXPORT), "--data-dir", target)
        self.assertEqual((0, True), (code, json.loads(out)["identical"]))
        code, _, err = self.run_main("backup-restore", "--export", str(EXPORT), "--data-dir", target)
        self.assertEqual(2, code)
        self.assertIn("never merges", err)


if __name__ == "__main__":
    unittest.main()
