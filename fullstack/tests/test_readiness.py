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
        Founder in ACT-004 (`§93`, DG-01 to DG-05); FS-DP-07 was re-decided by the
        delegated decision ACT-008-DG-01 (`§101`)."""
        today = ratified(readiness.REGISTER.read_text(encoding="utf-8"))
        self.assertEqual(sorted(PACKAGES), sorted(today))
        self.assertEqual({"FS-DP-01": "FS-ARCH-RAT-001", "FS-DP-04": "FS-ARCH-RAT-001",
                          "FS-DP-05": "FS-DP-05-ARCHITECT-DECISION",
                          "FS-DP-02": "FS-DP-02-ARCHITECT-DECISION",
                          "FS-DP-03": "ACT-004-DG-01", "FS-DP-06": "ACT-004-DG-02",
                          "FS-DP-07": "ACT-008-DG-01", "FS-09-ENV": "ACT-004-DG-04",
                          "FS-09-RUNTIME": "ACT-004-DG-05"},
                         {p: h.split(" ")[0] for p, h in today.items()})

    def test_a_decision_package_cannot_ratify_itself(self):
        for path in (readiness.REPO_ROOT / "docs/fullstack/decision-packages").glob("*.md"):
            with self.subTest(package=path.name):
                self.assertEqual({}, ratified(path.read_text(encoding="utf-8")))


class TheGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The gate's logic when the recording covers the tree. Whether it really
        # does is a separate fact, tested in `TheRecordingAsItStandsToday`.
        cls.recorded = readiness.preview_record()
        cls.covering = dict(cls.recorded, current=True,
                            passed=set(cls.recorded["passed"]) | {readiness.SCENARIO_A_LIVE})
        cls.live = readiness.evaluate(runs=2, preview=cls.covering)
        cls.by_name = {f"{c['area']}: {c['criterion']}": c for c in cls.live["criteria"]}

    def test_with_a_recording_that_covers_the_tree_nothing_else_blocks_the_gate(self):
        """A hypothetical: the recorded live checks cover this tree. Whether they
        do is a separate fact (`TheRecordingAsItStandsToday`). Every decision is
        taken, the wiring is measured, the bypass is revoked: nothing else stands
        between the gate and READY, and READY is not a release (FD-FS-001 D4-A)."""
        self.assertEqual([], self.live["awaiting"])
        self.assertEqual([], [n for n, c in self.by_name.items() if c["status"] in (FAIL, BLOCKED)])
        self.assertEqual(readiness.READY, self.live["result"])

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
        self.assertIn("297e8b8", auth["evidence"])
        self.assertEqual({"file": "docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-30.json",
                          "date": "2026-09-30", "commit": "297e8b8",
                          "deployment": "dpl_FjjGC9Hg54RGzGSugwidwHdRTrwM", "current": True,
                          "access_revoked": False,
                          "after_revocation": "not yet: the bypass is active (see access)"},
                         self.live["preview_evidence"])
        self.assertTrue(readiness.FS08_EVIDENCE.is_file(), "the FS-08 recording stays as history")
        self.assertTrue(readiness.FS09_A4A11CF_EVIDENCE.is_file(),
                        "the a4a11cf recording stays as history")

    def test_a_local_result_never_passes_a_live_criterion(self):
        """Without the recorded Preview checks, the live criteria fail even though
        every local measurement passes."""
        empty = dict(readiness.preview_record(), passed=set(), current=True)
        gate = readiness.evaluate(runs=1, preview=empty)
        live = [c for c in gate["criteria"] if readiness.PREVIEW in c["evidence_class"]
                and c["status"] != OBSERVED]
        self.assertTrue(live)
        self.assertEqual({FAIL}, {c["status"] for c in live})
        self.assertIn("not recorded PASS", live[0]["evidence"])

    def test_recorded_live_evidence_never_covers_a_local_failure(self):
        record = self.covering
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
        # Not verified is not failed (ACT-007 15): BLOCKED on a named dependency,
        # never PASS and never FAIL.
        self.assertEqual({BLOCKED}, {c["status"] for c in live})
        self.assertEqual({("LIVE-REVERIFICATION",)}, {tuple(c["blocked_by"]) for c in live})
        self.assertIn("served code changed", live[0]["evidence"])
        self.assertIn("LIVE-REVERIFICATION", gate["awaiting"])
        self.assertEqual(NOT_READY, gate["result"])

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
        # Scenario A (A2) and alerting (H3) are decided by the ACT-008 entries (Register 101);
        # E1 wiring is measured; the bypass is recorded revoked; the stale-recording
        # dependency applies only while the recording is stale.
        self.assertEqual({}, self.live["other_decisions"])
        self.assertTrue(readiness.OTHER_DECISIONS["BYPASS-REVOCATION"].startswith(
            "Execution permission"))
        self.assertIn("R2 is the readiness signal", readiness.OTHER_DECISIONS["ALERTING-SELECTION"])
        self.assertNotIn("E1-DEPLOYMENT-WIRING", readiness.OTHER_DECISIONS)
        for package in readiness.PACKAGES:
            self.assertTrue(self.live["decision_packages"][package].startswith("RATIFIED"))

    def test_the_act_004_rows_pass_on_their_own_evidence(self):
        for name in ("Observability: logging (L1)", "Observability: metrics (M1)",
                     "Observability: readiness signal (R2)",
                     "Reproducibility: runtime version pinned",
                     "Reproducibility: reproducible deployment",
                     "Operations: operational ownership",
                     "Functionality: A2: instances are registered, Definitions are never authored",
                     "Data: migration"):
            with self.subTest(criterion=name):
                self.assertEqual(PASS, self.by_name[name]["status"])
        for name in ("Observability: alerting", "Functionality: agent creation (Scenario A)"):
            self.assertEqual(PASS, self.by_name[name]["status"], name)

    def test_ratification_alone_does_not_make_it_ready(self):
        """Every decision taken still leaves unimplemented work: BLOCKED becomes FAIL."""
        gate = readiness.evaluate(runs=1, register_text=RATIFY_ALL, preview=self.covering,
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
                         "alerting is H3 (none; manual checks"):
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

    def test_an_unrevoked_bypass_blocks_and_a_recorded_revocation_passes(self):
        row = "Security: temporary access revoked"
        unrevoked = {"revoked": False, "why": "no revocation record"}
        gate = readiness.evaluate(runs=1, preview=self.covering, revocation=unrevoked)
        self.assertEqual((BLOCKED, ["BYPASS-REVOCATION"]),
                         (self.by_name_of(gate)[row]["status"],
                          self.by_name_of(gate)[row]["blocked_by"]))
        self.assertIn("NC-16", self.by_name_of(gate)[row]["evidence"])
        self.assertEqual(["BYPASS-REVOCATION"], gate["awaiting"])
        self.assertIn("BYPASS-REVOCATION", gate["other_decisions"])
        taken = readiness.evaluate(runs=1, preview=self.covering, revocation=unrevoked,
                                   decisions=["BYPASS-REVOCATION"])
        self.assertEqual(FAIL, self.by_name_of(taken)[row]["status"],
                         "a decision alone does not revoke the bypass")
        self.assertEqual((PASS, [readiness.OPERATOR]),
                         (self.by_name[row]["status"], self.by_name[row]["evidence_class"]))

    def test_the_old_recordings_own_flag_is_history_not_a_revocation(self):
        """The 297e8b8 recording says `access_revoked: false`: true when made. A
        later revocation is a later fact, recorded elsewhere."""
        self.assertIs(False, self.recorded["access_revoked"])
        self.assertTrue(readiness.revocation_record()["revoked"])

    def test_the_gate_never_releases(self):
        self.assertIn("never releases", self.live["release"])
        self.assertIn("D4-A", self.live["release"])

    def test_external_dependencies_are_named(self):
        self.assertEqual(["EXT-02", "EXT-03", "EXT-04"],
                         [d["id"] for d in self.live["external_dependencies"]])


DELEGATED_ENTRY = (
    "### ACT-007-DG-{n} — Delegated Decision · fixture\n\n| Field | Value |\n|---|---|\n"
    "| **Decided by** | {by} |\n| **Ratifies** | {ident} |\n| **Decision** | {decision} |\n")


class TheRevocationRecord(unittest.TestCase):
    """A revocation counts only with the control's own response, protection
    still on, and the revoked secret refused at the edge."""

    GOOD = {"bypass_revocation": {
        "note": "x", "revoked_at": "t", "control_response": {"protectionBypass": {}},
        "protection_enabled": True, "old_secret_http_status": {"a": 302, "b": 302}}}

    def record(self, **changes):
        import json
        import tempfile
        from pathlib import Path
        data = json.loads(json.dumps(self.GOOD))
        data["bypass_revocation"].update(changes)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "e.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return readiness.revocation_record(path)

    def test_a_complete_record_counts(self):
        self.assertTrue(self.record()["revoked"])

    def test_each_missing_proof_defeats_it(self):
        for change in ({"control_response": {"protectionBypass": {"k": {}}}},
                       {"control_response": None}, {"protection_enabled": False},
                       {"protection_enabled": None}, {"old_secret_http_status": {}},
                       {"old_secret_http_status": {"a": 302, "b": 200}},
                       {"old_secret_http_status": None}):
            with self.subTest(change=change):
                self.assertFalse(self.record(**change)["revoked"])

    def test_no_file_is_no_revocation(self):
        from pathlib import Path
        self.assertFalse(readiness.revocation_record(Path("/nonexistent/e.json"))["revoked"])

    def test_the_real_record_holds_no_secret(self):
        import re
        text = readiness.REVOCATION_EVIDENCE.read_text(encoding="utf-8")
        self.assertEqual([], [t for t in re.findall(r"\b[A-Za-z0-9]{32}\b", text)
                              if not re.fullmatch(r"[0-9a-f]{32}", t)])


class DelegatedDecisions(unittest.TestCase):
    """ACT-007 5 and 6, ACT-008 7 and 8: Scenario A and alerting can be decided by
    a Register entry that names ACT-007 or ACT-008, and by nothing else."""

    def entry(self, ident, decision, by="Claude Code, under the delegated authority of ACT-007 3"):
        return DELEGATED_ENTRY.format(n=1, by=by, ident=ident, decision=decision)

    def test_an_act_007_entry_is_read_with_its_option(self):
        found = readiness.delegated(
            self.entry("SCENARIO-A-RESIDUAL", "**A1 applies and stays in force**")
            + self.entry("ALERTING-SELECTION", "**Alerting = H3.** Residual stated"))
        self.assertEqual({"SCENARIO-A-RESIDUAL": "A1", "ALERTING-SELECTION": "H3"},
                         {k: v["option"] for k, v in found.items()})

    def test_an_entry_that_does_not_name_act_007_decides_nothing(self):
        for by in ("Architect", "Founder", "Claude Code"):
            with self.subTest(by=by):
                self.assertEqual({}, readiness.delegated(
                    self.entry("ALERTING-SELECTION", "**Alerting = H3.**", by=by)))

    def test_a_proposal_or_a_neighbouring_id_decides_nothing(self):
        self.assertEqual({}, readiness.delegated(
            "### X\n\n| **Ratifies** | ALERTING-SELECTION |\n| **Decision** | **H3** |\n"))
        self.assertEqual({}, readiness.delegated(
            self.entry("ALERTING-SELECTIONS", "**H3**") + self.entry("XSCENARIO-A-RESIDUAL", "**A1**")))

    def test_the_register_holds_both_decisions_today(self):
        found = readiness.delegated(readiness.REGISTER.read_text(encoding="utf-8"))
        self.assertEqual({"SCENARIO-A-RESIDUAL": "A2", "ALERTING-SELECTION": "H3"},
                         {k: v["option"] for k, v in found.items()})
        self.assertTrue(all(v["entry"].startswith("ACT-008-DG-") for v in found.values()))

    def test_without_the_entries_both_rows_wait(self):
        record = dict(readiness.preview_record(), current=True)
        gate = readiness.evaluate(runs=1, register_text=RATIFY_ALL, preview=record)
        by = {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}
        self.assertEqual(BLOCKED, by["Functionality: agent creation (Scenario A)"]["status"])
        self.assertEqual(BLOCKED, by["Observability: alerting"]["status"])
        self.assertEqual({"SCENARIO-A-RESIDUAL", "ALERTING-SELECTION"},
                         {d for c in gate["criteria"] for d in c["blocked_by"]} - {"BYPASS-REVOCATION"})

    def test_the_scenario_a_classification_needs_the_absences_to_hold(self):
        from unittest import mock
        record = dict(readiness.preview_record(), current=True)
        record["passed"] = set(record["passed"]) | {readiness.SCENARIO_A_LIVE}
        with mock.patch.object(readiness, "_a2_holds", return_value=False):
            gate = readiness.evaluate(runs=1, preview=record)
        by = {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}
        self.assertEqual(FAIL, by["Functionality: agent creation (Scenario A)"]["status"])
        self.assertEqual(
            FAIL, by["Functionality: A2: instances are registered, Definitions are never authored"]
            ["status"])

    def test_the_scenario_a_row_is_executed_locally_and_needs_the_live_check(self):
        """A2 is executed: measured now, in-process, and PASS only with the
        live check recorded on code the Preview still serves."""
        record = dict(readiness.preview_record(), current=True)
        record["passed"] = set(record["passed"]) | {readiness.SCENARIO_A_LIVE}
        name = "Functionality: agent creation (Scenario A)"
        row = {f"{c['area']}: {c['criterion']}": c
               for c in readiness.evaluate(runs=1, preview=record)["criteria"]}[name]
        self.assertEqual(PASS, row["status"])
        self.assertIn("registered in-process: 201", row["evidence"])
        self.assertNotIn("NOT executed", row["evidence"])
        self.assertIn("A2", row["residual"])
        self.assertIn("AGENT INSTANCE ≠ AUTHORITY", row["residual"])
        missing = dict(record, passed=set(record["passed"]) - {readiness.SCENARIO_A_LIVE})
        row = {f"{c['area']}: {c['criterion']}": c
               for c in readiness.evaluate(runs=1, preview=missing)["criteria"]}[name]
        self.assertEqual(FAIL, row["status"])
        self.assertIn(readiness.SCENARIO_A_LIVE, row["evidence"])
        stale = dict(missing, current=False)
        row = {f"{c['area']}: {c['criterion']}": c
               for c in readiness.evaluate(runs=1, preview=stale)["criteria"]}[name]
        self.assertEqual((BLOCKED, ["LIVE-REVERIFICATION"]), (row["status"], row["blocked_by"]))

    def test_a1_and_a3_do_not_execute_scenario_a(self):
        for option in ("A1", "A3"):
            row = readiness._scenario_a_row({"option": option, "entry": "X — y"}, {}, True, {})
            self.assertEqual(FAIL, row["status"], option)


class TheAlertingSelection(unittest.TestCase):

    def setUp(self):
        self.record = dict(readiness.preview_record(), current=True)

    def row(self, **patches):
        from unittest import mock
        with mock.patch.multiple(readiness, **patches) if patches else mock.patch.dict({}):
            gate = readiness.evaluate(runs=1, preview=self.record)
        return {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}["Observability: alerting"]

    def test_h3_passes_with_its_residual_stated(self):
        row = self.row()
        self.assertEqual(PASS, row["status"])
        self.assertIn("H3", row["evidence"])
        self.assertIn("no automatic alert", row["residual"])
        self.assertIn("R2 is readiness, not alerting", row["residual"])

    def missing_after(self, marker):
        """What `_h3_missing` reports when the runbook loses `marker`."""
        import tempfile
        from pathlib import Path
        from unittest import mock
        text = readiness.RUNBOOK.read_text(encoding="utf-8").replace(marker, "REMOVED")
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "runbook.md"
            mutated.write_text(text, encoding="utf-8")
            with mock.patch.object(readiness, "RUNBOOK", mutated):
                return readiness._h3_missing()

    def test_h3_fails_when_the_runbook_loses_its_manual_checks(self):
        missing = self.missing_after("### 12.1 Manual monitoring checks (H3)")
        self.assertEqual(["### 12.1 Manual monitoring checks (H3)"], missing)
        row = readiness._alerting_row({"entry": "ACT-007-DG-02 — x", "option": "H3"}, missing)
        self.assertEqual(FAIL, row["status"])
        self.assertIn("### 12.1 Manual monitoring checks (H3)", row["evidence"])
        self.assertEqual([], readiness._h3_missing())

    def test_each_manual_check_is_required(self):
        for marker in readiness.H3_MARKERS:
            with self.subTest(marker=marker):
                self.assertEqual([marker], self.missing_after(marker))

    def test_h1_and_h2_are_not_implementable_inside_fs09(self):
        for option in ("H1", "H2"):
            with self.subTest(option=option):
                row = readiness._alerting_row({"entry": "ACT-007-DG-02 — x", "option": option}, [])
                self.assertEqual(FAIL, row["status"])
                self.assertIn("Founder-reserved", row["evidence"])

    def test_the_runbook_keeps_readiness_and_alerting_apart(self):
        text = readiness.RUNBOOK.read_text(encoding="utf-8")
        self.assertIn("R2 is readiness, not alerting", text)
        self.assertIn("never tells anyone unasked", text)


class TheEnvironmentWiring(unittest.TestCase):

    def setUp(self):
        self.record = dict(readiness.preview_record(), current=True)

    def row(self, **patches):
        from unittest import mock
        from fullstack.deploy import vercel
        with mock.patch.multiple(vercel, **patches):
            gate = readiness.evaluate(runs=1, preview=self.record)
        return {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}["Data: environment separation"]

    def test_the_wiring_is_measured_from_the_real_resolver(self):
        measured = readiness._environment_wiring()
        self.assertTrue(measured["ok"])
        self.assertEqual("5 of 5", measured["unresolved_refused"])
        gate = readiness.evaluate(runs=1, preview=self.record)
        row = {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}[
            "Data: environment separation"]
        self.assertEqual(PASS, row["status"])
        self.assertEqual([readiness.LOCAL, readiness.PREVIEW], row["evidence_class"])
        self.assertIn("not live", row["residual"])

    def test_two_environments_on_one_project_fail(self):
        same = {"preview": readiness.PREVIEW_PROJECT, "production": readiness.PREVIEW_PROJECT}
        self.assertEqual(FAIL, self.row(SUPABASE_PROJECTS=same)["status"])

    def test_the_projects_swapped_fail(self):
        swapped = {"preview": readiness.PRODUCTION_PROJECT, "production": readiness.PREVIEW_PROJECT}
        self.assertEqual(FAIL, self.row(SUPABASE_PROJECTS=swapped)["status"])

    def test_an_environment_that_falls_back_to_preview_fails(self):
        from fullstack.deploy import vercel
        real = vercel.SUPABASE_PROJECTS

        def lenient(environment=None):
            return real.get((environment or {}).get("VERCEL_ENV"), real["preview"])
        self.assertEqual(FAIL, self.row(project_url_for=lenient)["status"])


class TheRecordingAsItStandsToday(unittest.TestCase):
    """The Preview recording is a fact about a commit. When the served code has
    outgrown it, the gate must say so, and must not pass on it."""

    def test_a_recording_the_code_has_outgrown_is_never_hidden(self):
        recorded = readiness.preview_record()
        gate = readiness.evaluate(runs=1)
        live = [c for c in gate["criteria"] if readiness.PREVIEW in c["evidence_class"]
                and c["status"] != OBSERVED]
        self.assertTrue(live)
        if recorded["current"]:
            self.assertNotIn("LIVE-REVERIFICATION", gate["awaiting"])
            self.assertEqual({PASS}, {c["status"] for c in live})
        else:
            self.assertIn("LIVE-REVERIFICATION", gate["awaiting"])
            self.assertEqual({BLOCKED}, {c["status"] for c in live})
            self.assertEqual(NOT_READY, gate["result"])
            self.assertIn("LIVE-REVERIFICATION", gate["other_decisions"])
            self.assertIn("forbid creating a new bypass",
                          gate["other_decisions"]["LIVE-REVERIFICATION"])

    def test_the_decision_rows_do_not_depend_on_the_recording(self):
        gate = readiness.evaluate(runs=1)
        by = {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}
        for name in ("Observability: alerting",
                     "Functionality: A2: instances are registered, Definitions are never authored"):
            self.assertEqual(PASS, by[name]["status"], name)
        # Scenario A is executed, so it is a live row: it follows the recording.
        scenario = by["Functionality: agent creation (Scenario A)"]
        expected = PASS if readiness.preview_record()["current"] is True and \
            readiness.SCENARIO_A_LIVE in readiness.preview_record()["passed"] else BLOCKED
        self.assertEqual(expected, scenario["status"])


if __name__ == "__main__":
    unittest.main()
