"""FS-09 backup and restore drill (`FS-DP-01` point 6; `FS-ARCH-RAT-001` `§3.3`).

The operator's logical export of the live store, persisted as evidence, is
restored here into fresh stores: the certified local backend and
`SupabaseStorage` over the in-memory PostgREST. The application must read the
restored state exactly as the source held it. The evidence files are only
read, never written.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fullstack.backend.aios import AIOSApplication, RUNS_PARTITION
from fullstack.backend.security import AUDIT_PARTITION, AuditLedger
from fullstack.deploy import backup
from fullstack.tests.support import OPERATOR_TOKEN, REPO_ROOT, Harness
from fullstack.tests.test_deployment import supabase
from native_core.core.infrastructure import LocalAppendOnlyStorage

EVIDENCE = REPO_ROOT / "docs/fullstack/evidence"
EXPORT = EVIDENCE / "FS-09-BACKUP-EXPORT-2026-09-27.jsonl"
MANIFEST = EVIDENCE / "FS-09-BACKUP-MANIFEST-2026-09-27.json"


def fresh_local(test):
    tmp = tempfile.TemporaryDirectory()
    test.addCleanup(tmp.cleanup)
    store = LocalAppendOnlyStorage(Path(tmp.name) / "storage")
    store.provision()
    return Path(tmp.name), store


class TheExportMatchesTheLiveStore(unittest.TestCase):
    """The persisted export against the digests the database computed."""

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
                self.assertEqual(expected["sha256_joined_server"],
                                 summary[name]["sha256_joined"])

    def test_the_whole_table_matches_in_seq_order(self):
        table = self.manifest["table"]
        records = [e.record for e in self.entries]
        self.assertEqual(table["records"], len(records))
        self.assertEqual(table["sha256_joined_server"], backup.joined_sha256(records))
        seqs = [e.seq for e in self.entries]
        self.assertEqual(sorted(seqs), seqs)
        for name, expected in self.manifest["partitions"].items():
            own = [e.seq for e in self.entries if e.partition == name]
            self.assertEqual((expected["seq_first"], expected["seq_last"]), (own[0], own[-1]))

    def test_the_export_file_is_the_one_the_manifest_names(self):
        import hashlib
        self.assertEqual(self.manifest["export"]["sha256"],
                         hashlib.sha256(EXPORT.read_bytes()).hexdigest())

    def test_the_export_holds_no_credential(self):
        text = EXPORT.read_text(encoding="utf-8").lower()
        for needle in ("sb_" + "secret_", "ey" + "j", "bearer", "apikey", "service_role",
                       "authorization", "aios_operator_" + "tokens"):
            self.assertNotIn(needle, text)
        subjects = {json.loads(e.record)["subject"] for e in self.entries
                    if e.partition == AUDIT_PARTITION}
        self.assertEqual({None, "founder"}, subjects)


class TheRestoreIsByteIdentical(unittest.TestCase):

    def setUp(self):
        self.entries = backup.read_file(EXPORT)

    def test_into_a_fresh_local_store(self):
        _, store = fresh_local(self)
        self.assertEqual(80, backup.restore(self.entries, store))
        self.assertEqual([], backup.differences(self.entries, store))
        self.assertEqual(backup.summary(self.entries),
                         backup.summary(backup.export_store(store)))

    def test_into_a_fresh_supabase_store(self):
        store, fake = supabase()
        backup.restore(self.entries, store)
        self.assertEqual([], backup.differences(self.entries, store))
        self.assertEqual(80, len(fake.rows))

    def test_a_diverging_store_is_reported(self):
        _, store = fresh_local(self)
        altered = [backup.Entry(e.seq, e.partition, e.position,
                                e.record + b" " if e.position == 4 and e.partition == "trace"
                                else e.record)
                   for e in self.entries]
        backup.restore(altered, store)
        self.assertEqual(["trace: record 4 differs"], backup.differences(self.entries, store))
        _, short = fresh_local(self)
        backup.restore(self.entries[:-1], short)
        self.assertEqual(["fullstack-audit: 40 records, export has 41"],
                         backup.differences(self.entries, short))

    def test_a_second_export_round_trips(self):
        _, store = fresh_local(self)
        backup.restore(self.entries, store)
        again = backup.parse(backup.write_lines(backup.export_store(store)))
        self.assertEqual(backup.by_partition(self.entries), backup.by_partition(again))


class TheApplicationReadsTheRestoredState(unittest.TestCase):

    def setUp(self):
        self.entries = backup.read_file(EXPORT)
        self.data_dir, store = fresh_local(self)
        backup.restore(self.entries, store)
        self.source = backup.by_partition(self.entries)
        self.aios = AIOSApplication(self.data_dir, REPO_ROOT)
        self.aios.start()
        self.addCleanup(self.aios.stop)

    def test_the_runs_are_the_exported_runs(self):
        exported = [json.loads(r) for r in self.source[RUNS_PARTITION]]
        runs = self.aios.runs()
        self.assertEqual(10, len(runs))
        self.assertEqual(list(reversed(exported)), runs)
        self.assertEqual(10, len({r["run_id"] for r in runs}))
        self.assertEqual({"succeeded": 9, "failed": 1},
                         {s: sum(r["state"] == s for r in runs) for s in ("succeeded", "failed")})

    def test_every_run_resolves_its_own_trace(self):
        for run in self.aios.runs():
            with self.subTest(run=run["run_id"]):
                trace = self.aios.run_trace(run["run_id"])
                self.assertEqual(run["trace"]["count"], len(trace))
                self.assertEqual({run["runtime_id"]}, {t["runtime"] for t in trace})
                self.assertIn([run["workflow_identity"]["key"]],
                              [t["skills_used"] for t in trace])

    def test_the_audit_is_the_exported_audit_in_order(self):
        entries = list(AuditLedger(self.aios.storage).entries())
        exported = [json.loads(r) for r in self.source[AUDIT_PARTITION]]
        self.assertEqual(exported, [{k: v for k, v in e.items() if k != "position"}
                                    for e in entries])
        self.assertEqual(list(range(41)), [e["position"] for e in entries])
        self.assertEqual({("refused", 401): 21, ("allowed", 200): 20},
                         {k: sum((e["decision"], e["status"]) == k for e in entries)
                          for k in (("refused", 401), ("allowed", 200))})

    def test_the_trace_is_the_exported_trace_in_order(self):
        traces = self.aios.traces(0, 1000)
        self.assertEqual(29, traces["total"])
        exported = [json.loads(r) for r in self.source["trace"]]
        self.assertEqual([t["runtime"] for t in exported],
                         [t["runtime"] for t in traces["records"]])

    def test_the_restored_store_stays_append_only(self):
        before = {p: list(self.aios.storage.read(p)) for p in self.source}
        self.aios.start_run("document-conformance-review",
                            {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                             "criteria": ["INV-4"]}, "drill")
        for name, records in before.items():
            with self.subTest(partition=name):
                after = list(self.aios.storage.read(name))
                self.assertEqual(records, after[:len(records)])
        self.assertEqual(11, len(self.aios.runs()))
        offered = {m for m in dir(self.aios.storage) if not m.startswith("_")}
        self.assertFalse(offered & {"update", "delete", "remove", "truncate", "overwrite"})


class TheAPIServesTheRestoredState(unittest.TestCase):

    def test_runs_and_audit_through_the_api(self):
        entries = backup.read_file(EXPORT)
        data_dir, store = fresh_local(self)
        backup.restore(entries, store)
        harness = Harness(data_dir=data_dir)
        self.addCleanup(harness.close)
        status, _, body = harness.call("GET", "/api/v1/runs", OPERATOR_TOKEN)
        self.assertEqual(200, status)
        self.assertEqual(10, len(body["runs"]))
        last = body["runs"][-1]["run_id"]
        status, _, run = harness.call("GET", f"/api/v1/runs/{last}", OPERATOR_TOKEN)
        self.assertEqual((200, last), (status, run["run_id"]))
        status, _, audit = harness.call("GET", "/api/v1/audit?offset=0&limit=100",
                                        OPERATOR_TOKEN)
        self.assertEqual(200, status)
        # the 41 restored entries, then the drill's own three reads
        self.assertEqual(44, len(audit["entries"]))
        self.assertEqual("a39aee0ac323c557", audit["entries"][0]["request_id"])


class TheOperatorCommands(unittest.TestCase):
    """`python -m fullstack.backend backup-restore | backup-verify`, the runbook's steps."""

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
        code, out, _ = self.run_main("backup-restore", "--export", str(EXPORT),
                                     "--data-dir", target)
        self.assertEqual(0, code)
        self.assertTrue(json.loads(out)["identical"])
        code, out, _ = self.run_main("backup-verify", "--export", str(EXPORT),
                                     "--data-dir", target)
        self.assertEqual((0, True), (code, json.loads(out)["identical"]))
        code, _, err = self.run_main("backup-restore", "--export", str(EXPORT),
                                     "--data-dir", target)
        self.assertEqual(2, code)
        self.assertIn("never merges", err)

    def test_verify_reports_an_empty_store_as_different(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        code, _, err = self.run_main("backup-verify", "--export", str(EXPORT),
                                     "--data-dir", tmp.name)
        self.assertEqual(1, code)
        self.assertIn("fullstack-runs: 0 records, export has 10", err)


class TheRestoreRefusesWhatItMustNotDo(unittest.TestCase):

    def setUp(self):
        self.lines = EXPORT.read_text(encoding="utf-8").splitlines()

    def test_it_never_merges_into_an_occupied_store(self):
        _, store = fresh_local(self)
        store.append("trace", b'{"already":"here"}')
        with self.assertRaises(backup.RestoreRefused):
            backup.restore(backup.parse(self.lines), store)
        self.assertEqual([b'{"already":"here"}'], list(store.read("trace")))
        self.assertEqual([], list(store.read(RUNS_PARTITION)))

    def mutated(self, index, change):
        lines = list(self.lines)
        body = json.loads(lines[index])
        change(body)
        lines[index] = json.dumps(body, sort_keys=True, separators=(",", ":"))
        return lines

    def test_a_changed_record_is_refused(self):
        def tamper(body):
            body["record"] = body["record"].replace("founder", "intruder", 1) + " "
        with self.assertRaisesRegex(backup.ExportError, "sha256"):
            backup.parse(self.mutated(0, tamper))

    def test_a_missing_record_is_refused(self):
        lines = list(self.lines)
        del lines[3]
        with self.assertRaisesRegex(backup.ExportError, "position"):
            backup.parse(lines)

    def test_reordered_records_are_refused(self):
        lines = list(self.lines)
        lines[0], lines[1] = lines[1], lines[0]
        with self.assertRaises(backup.ExportError):
            backup.parse(lines)

    def test_a_backwards_seq_is_refused(self):
        with self.assertRaisesRegex(backup.ExportError, "seq"):
            backup.parse(self.mutated(5, lambda b: b.update(seq=1)))

    def test_an_unknown_format_or_field_is_refused(self):
        with self.assertRaisesRegex(backup.ExportError, "format"):
            backup.parse(self.mutated(0, lambda b: b.update(format="fullstack.backup/0")))
        with self.assertRaisesRegex(backup.ExportError, "fields"):
            backup.parse(self.mutated(0, lambda b: b.update(token="x")))
        with self.assertRaises(backup.ExportError):
            backup.parse(["not json"])

    def test_non_utf8_records_round_trip_as_base64(self):
        entry = backup.Entry(None, "p", 0, b"\x00\xff\xfe")
        line = backup.line_for(entry)
        self.assertIn("record_base64", line)
        self.assertEqual([entry], backup.parse([line]))


if __name__ == "__main__":
    unittest.main()
