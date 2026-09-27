"""FS-09 — the readiness gate: evaluated live, and ratification is read, not assumed."""

from __future__ import annotations

import unittest

from fullstack import readiness
from fullstack.readiness import (BLOCKED, FAIL, NOT_READY, OBSERVED, PACKAGES, PASS,
                                 ratified)

RATIFY_ALL = "\n".join(
    f"### {p}-R — Architect Decision · test fixture\n\n| Field | Value |\n|---|---|\n"
    f"| **Identifier** | `{p}-R` |\n| **Decided by** | Architect |\n| **Ratifies** | {p} |\n"
    for p in PACKAGES)


class Ratification(unittest.TestCase):
    def test_only_a_decided_register_entry_ratifies(self):
        self.assertEqual({}, ratified("### X — Proposal\n\n| **Ratifies** | FS-DP-01 |\n"))
        self.assertEqual({}, ratified("| **Decided by** | Architect |\n| **Ratifies** | FS-DP-01 |\n"))
        self.assertEqual(set(PACKAGES), set(ratified(RATIFY_ALL)))

    def test_a_section_does_not_borrow_the_previous_entrys_decider(self):
        text = ("### FD-X — Founder Decision\n\n| **Decided by** | Founder |\n\n"
                "## 99. Later section\n\n| **Ratifies** | FS-DP-01 |\n")
        self.assertEqual({}, ratified(text))

    def test_the_ratified_packages_today(self):
        """FS-DP-01 and FS-DP-04 by FS-ARCH-RAT-001 (Register `§68`); FS-DP-05 and
        FS-DP-02 by their Architect decisions (`§79`, `§81`). The other packages
        stay proposed."""
        today = ratified(readiness.REGISTER.read_text(encoding="utf-8"))
        self.assertEqual(["FS-DP-01", "FS-DP-02", "FS-DP-04", "FS-DP-05"], sorted(today))
        self.assertEqual({"FS-DP-01": "FS-ARCH-RAT-001", "FS-DP-04": "FS-ARCH-RAT-001",
                          "FS-DP-05": "FS-DP-05-ARCHITECT-DECISION",
                          "FS-DP-02": "FS-DP-02-ARCHITECT-DECISION"},
                         {p: h.split(" ")[0] for p, h in today.items()})

    def test_a_decision_package_cannot_ratify_itself(self):
        for path in (readiness.REPO_ROOT / "docs/fullstack/decision-packages").glob("*.md"):
            with self.subTest(package=path.name):
                self.assertEqual({}, ratified(path.read_text(encoding="utf-8")))


class TheGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.live = readiness.evaluate(runs=2)
        cls.by_name = {f"{c['area']}: {c['criterion']}": c for c in cls.live["criteria"]}

    def test_it_is_not_ready_and_says_exactly_why(self):
        self.assertEqual(NOT_READY, self.live["result"])
        self.assertEqual(["ENVIRONMENT-SEPARATION", "FS-DP-03", "FS-DP-06", "FS-DP-07",
                          "OPERATIONAL-OWNERSHIP", "PYTHON-RUNTIME-VERSION"],
                         self.live["awaiting"])
        # Not a decision but a gap: no deployment rollback has been exercised.
        self.assertEqual(["Reliability: rollback of a deployment"],
                         [n for n, c in self.by_name.items() if c["status"] == FAIL])

    def test_every_measurable_criterion_passes(self):
        measured = [c for c in self.live["criteria"] if c["status"] not in (BLOCKED, FAIL)]
        self.assertEqual({"PASS", "OBSERVED"}, {c["status"] for c in measured})

    def test_every_criterion_names_its_evidence_class(self):
        for name, c in self.by_name.items():
            with self.subTest(criterion=name):
                if c["status"] == BLOCKED:
                    self.assertTrue(c["blocked_by"])
                else:
                    self.assertTrue(set(c["evidence_class"]) <= {
                        readiness.LOCAL, readiness.PREVIEW, readiness.OPERATOR,
                        readiness.LOCAL_RECORDED})
                    self.assertTrue(c["evidence_class"])

    def test_recorded_live_evidence_is_labelled_historical_not_local(self):
        auth = self.by_name["Security: authentication"]
        self.assertEqual(PASS, auth["status"])
        self.assertEqual([readiness.LOCAL, readiness.PREVIEW], auth["evidence_class"])
        self.assertIn("recorded, not re-measured", auth["evidence"])
        self.assertIn("6469269", auth["evidence"])
        self.assertEqual({"file": "docs/fullstack/evidence/FS-08-LIVE-PREVIEW-2026-09-27.json",
                          "date": "2026-09-27", "commit": "6469269",
                          "deployment": "dpl_Gi3MbQkzo14aW4TriGwQ9TYMudgL", "current": True},
                         self.live["preview_evidence"])

    def test_a_local_result_never_passes_a_live_criterion(self):
        """Without the recorded Preview checks, the live criteria fail even though
        every local measurement passes."""
        empty = dict(readiness.preview_record(), passed=set())
        gate = readiness.evaluate(runs=1, preview=empty)
        live = [c for c in gate["criteria"] if readiness.PREVIEW in c["evidence_class"]]
        self.assertTrue(live)
        self.assertEqual({FAIL}, {c["status"] for c in live})
        self.assertIn("not recorded PASS", live[0]["evidence"])

    def test_recorded_live_evidence_never_covers_a_local_failure(self):
        record = readiness.preview_record()
        check = ["authenticated POST creates a run"]
        self.assertEqual(PASS, readiness._live("A", "c", True, "ok", check, record)["status"])
        self.assertEqual(FAIL, readiness._live("A", "c", False, "no", check, record)["status"])
        preview_only = readiness._live("A", "c", None, "", check, record)
        self.assertEqual((PASS, [readiness.PREVIEW]),
                         (preview_only["status"], preview_only["evidence_class"]))

    def test_a_stale_recording_does_not_count(self):
        stale = dict(readiness.preview_record(), current=False)
        gate = readiness.evaluate(runs=1, preview=stale)
        live = [c for c in gate["criteria"] if readiness.PREVIEW in c["evidence_class"]]
        self.assertEqual({FAIL}, {c["status"] for c in live})
        self.assertIn("served code changed", live[0]["evidence"])

    def test_the_served_code_is_what_the_preview_was_verified_on(self):
        self.assertTrue(readiness.preview_record()["current"])

    def test_rollback_is_not_verified_and_names_both_floors(self):
        rollback = self.by_name["Reliability: rollback of a deployment"]
        self.assertEqual(FAIL, rollback["status"])
        for text in ("NOT VERIFIED", "0706446", "215248f", "duplicate run ids",
                     "authenticates nobody", "production-safe"):
            self.assertIn(text, rollback["evidence"])

    def test_backup_and_restore_rest_on_the_drill(self):
        drill = self.by_name["Data: backup and restore"]
        self.assertEqual(PASS, drill["status"])
        self.assertEqual([readiness.OPERATOR, readiness.LOCAL], drill["evidence_class"])
        self.assertIn("ENVIRONMENT-SEPARATION", drill["residual"])

    def test_performance_is_observed_without_an_invented_requirement(self):
        perf = self.by_name["Performance: latency of Scenario B (local, in-process)"]
        self.assertEqual(OBSERVED, perf["status"])
        self.assertIn("No canonical workload or latency requirement", perf["evidence"])
        self.assertIn("Founder decision", perf["evidence"])

    def test_the_live_403_residual_is_stated(self):
        self.assertIn("403", self.by_name["Security: authorization and least privilege"]
                      ["residual"])

    def test_decisions_are_named_not_taken(self):
        self.assertEqual(set(readiness.OTHER_DECISIONS), set(self.live["other_decisions"]))
        self.assertTrue(self.live["other_decisions"]["OPERATIONAL-OWNERSHIP"]
                        .startswith("Founder"))
        for d in ("ENVIRONMENT-SEPARATION", "PYTHON-RUNTIME-VERSION"):
            self.assertTrue(self.live["other_decisions"][d].startswith("Architect"))

    def test_ratification_alone_does_not_make_it_ready(self):
        """Every decision taken still leaves unimplemented work: BLOCKED becomes FAIL."""
        gate = readiness.evaluate(runs=1, register_text=RATIFY_ALL,
                                  decisions=list(readiness.OTHER_DECISIONS))
        self.assertEqual(NOT_READY, gate["result"])
        self.assertEqual([], gate["awaiting"])
        self.assertTrue([c for c in gate["criteria"] if c["status"] == FAIL])

    def test_the_runbook_covers_every_required_section(self):
        self.assertEqual(PASS, self.by_name["Operations: runbook"]["status"])
        self.assertEqual([], readiness._runbook_sections())
        text = readiness.RUNBOOK.read_text(encoding="utf-8")
        for required in ("reintroduces the historical concurrency risk",
                         "changes the authentication posture",
                         "Data compatibility does not make a rollback target safe",
                         "waits on `FS-DP-06`"):
            self.assertIn(required, text)

    def test_a_runbook_missing_a_section_fails(self):
        import tempfile
        from pathlib import Path
        from unittest import mock
        text = readiness.RUNBOOK.read_text(encoding="utf-8").replace(
            "## 8. Restore", "## 8. Recovery notes")
        with tempfile.TemporaryDirectory() as tmp:
            partial = Path(tmp) / "runbook.md"
            partial.write_text(text, encoding="utf-8")
            with mock.patch.object(readiness, "RUNBOOK", partial):
                self.assertEqual(["Restore"], readiness._runbook_sections())
            with mock.patch.object(readiness, "RUNBOOK", Path(tmp) / "absent.md"):
                self.assertEqual(list(readiness.RUNBOOK_SECTIONS),
                                 readiness._runbook_sections())

    def test_a_drill_against_other_digests_fails(self):
        import json
        import tempfile
        from pathlib import Path
        from unittest import mock
        manifest = json.loads(readiness.BACKUP_MANIFEST.read_text(encoding="utf-8"))
        manifest["partitions"]["trace"]["sha256_joined_server"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            other = Path(tmp) / "manifest.json"
            other.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(readiness, "BACKUP_MANIFEST", other):
                drill = readiness._restore_drill()
        self.assertFalse(drill["ok"])
        self.assertFalse(drill["digests_match_server"])
        self.assertTrue(drill["restored_identical"])

    def test_the_gate_never_releases(self):
        self.assertIn("never releases", self.live["release"])
        self.assertIn("D4-A", self.live["release"])

    def test_external_dependencies_are_named(self):
        self.assertEqual(["EXT-02", "EXT-03", "EXT-04"],
                         [d["id"] for d in self.live["external_dependencies"]])


if __name__ == "__main__":
    unittest.main()
