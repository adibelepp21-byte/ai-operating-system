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

    def test_the_fs09_packages_are_ratifiable_by_their_exact_ids(self):
        entry = ("### X-R — Architect Decision · fixture\n\n| **Decided by** | Architect |\n"
                 "| **Ratifies** | {} |\n")
        self.assertEqual({"FS-09-ENV", "FS-09-RUNTIME"},
                         set(ratified(entry.format("FS-09-ENV, FS-09-RUNTIME"))))
        self.assertEqual({}, ratified(entry.format("FS-09-ENVX, FS-09-RUNTIMES")))

    def test_the_ratified_packages_today(self):
        """FS-DP-01 and FS-DP-04 by FS-ARCH-RAT-001 (Register `§68`); FS-DP-05 and
        FS-DP-02 by their Architect decisions (`§79`, `§81`); the other five by the
        Founder in ACT-004 (`§93`, DG-01 to DG-05)."""
        today = ratified(readiness.REGISTER.read_text(encoding="utf-8"))
        self.assertEqual(sorted(PACKAGES), sorted(today))
        self.assertEqual({"FS-DP-01": "FS-ARCH-RAT-001", "FS-DP-04": "FS-ARCH-RAT-001",
                          "FS-DP-05": "FS-DP-05-ARCHITECT-DECISION",
                          "FS-DP-02": "FS-DP-02-ARCHITECT-DECISION",
                          "FS-DP-03": "ACT-004-DG-01", "FS-DP-06": "ACT-004-DG-02",
                          "FS-DP-07": "ACT-004-DG-03", "FS-09-ENV": "ACT-004-DG-04",
                          "FS-09-RUNTIME": "ACT-004-DG-05"},
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
        self.assertEqual(["ALERTING-SELECTION", "E1-DEPLOYMENT-WIRING", "SCENARIO-A-RESIDUAL"],
                         self.live["awaiting"])
        self.assertEqual([], [n for n, c in self.by_name.items() if c["status"] == FAIL])
        self.assertEqual(["Functionality: agent creation (Scenario A)", "Observability: alerting",
                          "Data: environment separation"],
                         [n for n, c in self.by_name.items() if c["status"] == BLOCKED])

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
        self.assertIn("a4a11cf", auth["evidence"])
        self.assertEqual({"file": "docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-28.json",
                          "date": "2026-09-28", "commit": "a4a11cf",
                          "deployment": "dpl_8Znqrn818NgYy66RU7hz819t4ZTj", "current": True},
                         self.live["preview_evidence"])
        self.assertTrue(readiness.FS08_EVIDENCE.is_file(), "the FS-08 recording stays as history")

    def test_a_local_result_never_passes_a_live_criterion(self):
        """Without the recorded Preview checks, the live criteria fail even though
        every local measurement passes."""
        empty = dict(readiness.preview_record(), passed=set())
        gate = readiness.evaluate(runs=1, preview=empty)
        live = [c for c in gate["criteria"] if readiness.PREVIEW in c["evidence_class"]
                and c["status"] != OBSERVED]
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
        live = [c for c in gate["criteria"] if readiness.PREVIEW in c["evidence_class"]
                and c["status"] != OBSERVED]
        self.assertEqual({FAIL}, {c["status"] for c in live})
        self.assertIn("served code changed", live[0]["evidence"])

    def test_the_served_code_is_what_the_preview_was_verified_on(self):
        self.assertTrue(readiness.preview_record()["current"])

    def test_rollback_rests_on_the_recorded_drill_and_names_the_floors(self):
        rollback = self.by_name["Reliability: rollback of a deployment"]
        self.assertEqual(PASS, rollback["status"])
        self.assertEqual([readiness.PREVIEW], rollback["evidence_class"])
        self.assertIn("rollback drill", rollback["evidence"])
        for text in ("0706446", "215248f", "8d088fb", "duplicate run ids",
                     "authenticates nobody", "production-safe", "Founder-only"):
            self.assertIn(text, rollback["residual"])

    def test_backup_and_restore_rest_on_the_drill(self):
        drill = self.by_name["Data: backup and restore"]
        self.assertEqual(PASS, drill["status"])
        self.assertEqual([readiness.OPERATOR, readiness.LOCAL], drill["evidence_class"])
        self.assertIn("each environment", drill["residual"])

    def test_performance_is_observed_without_an_invented_requirement(self):
        perf = self.by_name["Performance: latency of Scenario B (local, in-process)"]
        self.assertEqual(OBSERVED, perf["status"])
        self.assertIn("No canonical workload or latency requirement", perf["evidence"])
        self.assertIn("OBSERVED is not PASS", perf["evidence"])

    def test_the_live_403_residual_is_stated(self):
        self.assertIn("403", self.by_name["Security: authorization and least privilege"]
                      ["residual"])

    def test_what_remains_is_named_not_taken(self):
        self.assertEqual(set(readiness.OTHER_DECISIONS), set(self.live["other_decisions"]))
        others = self.live["other_decisions"]
        self.assertTrue(others["ALERTING-SELECTION"].startswith("Founder as Architect"))
        self.assertIn("R2 is the readiness signal", others["ALERTING-SELECTION"])
        self.assertTrue(others["SCENARIO-A-RESIDUAL"].startswith("Founder"))
        self.assertTrue(others["E1-DEPLOYMENT-WIRING"].startswith("Execution permission"))
        for package in readiness.PACKAGES:
            self.assertTrue(self.live["decision_packages"][package].startswith("RATIFIED"))

    def test_the_act_004_rows_pass_on_their_own_evidence(self):
        for name in ("Observability: logging (L1)", "Observability: metrics (M1)",
                     "Observability: readiness signal (R2)",
                     "Reproducibility: runtime version pinned",
                     "Reproducibility: reproducible deployment",
                     "Operations: operational ownership", "Functionality: A1: no route creates an Agent",
                     "Data: migration"):
            with self.subTest(criterion=name):
                self.assertEqual(PASS, self.by_name[name]["status"])
        self.assertEqual(["ALERTING-SELECTION"],
                         self.by_name["Observability: alerting"]["blocked_by"])

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
                         "alerting is unresolved"):
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

    def by_name_of(self, gate):
        return {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}

    def test_an_unpinned_or_other_runtime_fails_the_pin(self):
        import tempfile
        from pathlib import Path
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            other = Path(tmp) / ".python-version"
            other.write_text("3.11\n", encoding="utf-8")
            with mock.patch.object(readiness, "PYTHON_VERSION", other):
                gate = readiness.evaluate(runs=1)
        self.assertEqual(FAIL, self.by_name_of(gate)["Reproducibility: runtime version pinned"]
                         ["status"])

    def test_an_ownership_model_missing_a_section_fails(self):
        import tempfile
        from pathlib import Path
        from unittest import mock
        text = readiness.OWNERSHIP.read_text(encoding="utf-8").replace(
            "## 2. Credentials", "## 2. Keys")
        with tempfile.TemporaryDirectory() as tmp:
            partial = Path(tmp) / "ownership.md"
            partial.write_text(text, encoding="utf-8")
            with mock.patch.object(readiness, "OWNERSHIP", partial):
                gate = readiness.evaluate(runs=1)
        row = self.by_name_of(gate)["Operations: operational ownership"]
        self.assertEqual((FAIL, "missing sections: Credentials"), (row["status"], row["evidence"]))

    def test_a_request_without_its_log_line_fails_l1(self):
        from unittest import mock
        real = readiness._measure

        def one_line_lost(runs):
            measured = real(runs)
            measured["log_lines"] = measured["log_lines"][1:]
            return measured
        with mock.patch.object(readiness, "_measure", one_line_lost):
            gate = readiness.evaluate(runs=1)
        self.assertEqual(FAIL, self.by_name_of(gate)["Observability: logging (L1)"]["status"])

    def test_the_gate_never_releases(self):
        self.assertIn("never releases", self.live["release"])
        self.assertIn("D4-A", self.live["release"])

    def test_external_dependencies_are_named(self):
        self.assertEqual(["EXT-02", "EXT-03", "EXT-04"],
                         [d["id"] for d in self.live["external_dependencies"]])


if __name__ == "__main__":
    unittest.main()
