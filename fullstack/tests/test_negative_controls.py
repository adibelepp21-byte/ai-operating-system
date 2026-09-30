"""FS-09 final negative controls NC-01..NC-20 (ACT-008 `§21`).

A negative control asks whether something that must **not** have happened did
not. Each is measured on this tree against the commits named below; the
controls that concern live state (NC-07 to NC-10) are recorded in
`docs/fullstack/evidence/FS-09-ACT-008-NEGATIVE-CONTROLS-2026-09-30.json` and
checked here only for their structure. Not every control is decidable from the
repository; those say so in the evidence file.
"""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path
from unittest import mock

from fullstack import readiness
from fullstack.backend import contract
from fullstack.tests.support import REPO_ROOT

#: The commit at which the certified roots were last changed before the
#: ACT-004 to ACT-008 execution (certified-evidence integrity held there).
BASELINE = "edb3beb"
#: ACT-008 received (the verbatim Act is committed here).
ACT_008_RECEIVED = "d6afbdc"
EVIDENCE = REPO_ROOT / "docs/fullstack/evidence"


def git(*args) -> str:
    done = subprocess.run(["git", *args], cwd=str(REPO_ROOT), capture_output=True, text=True)
    return done.stdout


def available(commit: str) -> bool:
    return subprocess.run(["git", "cat-file", "-e", commit], cwd=str(REPO_ROOT),
                          capture_output=True).returncode == 0


def changed(commit: str, *paths) -> list:
    return [line for line in git("diff", "--name-status", commit, "HEAD", "--", *paths).splitlines()]


@unittest.skipUnless(available(BASELINE), "baseline commit not available")
class CertifiedRootsAndPhases(unittest.TestCase):

    def test_nc_05_no_p12_certified_root_modification(self):
        self.assertEqual([], changed(BASELINE, "tools", "consumers", "docs/architecture/p12"))

    def test_nc_04_no_p13_reopening(self):
        self.assertEqual([], changed(BASELINE, "docs/architecture/p13", "tools/p13",
                                     "docs/governance/AIOS_P13_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"))

    def test_nc_06_native_core_remains_eleven(self):
        self.assertEqual([], changed(BASELINE, "native_core"),
                         "native_core is untouched, so it is not a twelfth")
        self.assertFalse((REPO_ROOT / "native_core/core/agent/factory.py").exists())

    def test_nc_03_no_phase_14(self):
        added = [line for line in git("diff", "--name-status", BASELINE, "HEAD").splitlines()
                 if line.startswith("A") and re.search(r"phase[-_ ]?14|/p14|p14_", line, re.I)]
        self.assertEqual([], added)


@unittest.skipUnless(available(ACT_008_RECEIVED), "receipt commit not available")
class AuthorityAndActs(unittest.TestCase):

    def test_nc_02_no_unauthorized_act_creation(self):
        """Since ACT-008 was received no Act was added, edited or removed."""
        self.assertEqual([], changed(ACT_008_RECEIVED, "docs/governance/acts"))

    def test_nc_19_no_p12_measure_manipulation(self):
        """Neither the P12 test, its population nor the Acts it measures changed."""
        self.assertEqual([], changed(ACT_008_RECEIVED, "tools", "docs/governance/acts"))
        record = json.loads((EVIDENCE / "FS-09-ACT-008-P12-W6-CLASSIFICATION-2026-09-30.json")
                            .read_text(encoding="utf-8"))
        self.assertFalse(record["p12_modified"])
        self.assertIn("FAILED (failures=1)", record["raw_result"], "the raw failure is preserved")

    def test_nc_01_no_self_authorization(self):
        text = readiness.REGISTER.read_text(encoding="utf-8")
        entries = re.split(r"(?m)^### ", text[text.index("## 101."):])[1:]
        self.assertGreaterEqual(len(entries), 2)
        for entry in entries:
            if entry.startswith("ACT-008-DG-"):
                self.assertIn("Not a Founder decision", entry)
                self.assertIn("ACT-008", entry.split("| **Decided by** |")[1].split("\n")[0])
        tail = text[text.index("## 100."):]
        self.assertNotRegex(tail, r"(?i)founder release authorization (is )?(issued|granted)")

    def test_nc_07_no_unauthorized_production_release(self):
        """Nothing in the repository changes what Production serves or how."""
        self.assertEqual([], [line for line in changed(BASELINE, "vercel.json", ".vercel")
                              if "production" in git("show", "HEAD:vercel.json").lower()])
        runbook = (REPO_ROOT / "docs/fullstack/FS-09-OPERATIONAL-RUNBOOK.md").read_text(encoding="utf-8")
        self.assertIn("**Founder only**", runbook)
        ownership = json.loads((EVIDENCE / "FS-09-ACT-008-NEGATIVE-CONTROLS-2026-09-30.json")
                               .read_text(encoding="utf-8"))
        self.assertEqual("dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj",
                         ownership["live"]["production_deployments"][0])


class Secrets(unittest.TestCase):

    PATTERNS = (r"sb_secret_[A-Za-z0-9_\-]{10,}", r"eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}",
                r"(?i)bearer [A-Za-z0-9_\-\.]{24,}", r"(?i)x-vercel-protection-bypass['\"]?\s*[:=]\s*['\"]?[A-Za-z0-9]{32}")

    #: Markers of the deliberately fake values tests and scripts use.
    FAKE = ("test", "not-the", "abc", "wrong", "fake", "example", "dummy")

    def tracked(self, *prefixes):
        names = git("ls-files", *prefixes).splitlines()
        for name in names:
            path = REPO_ROOT / name
            if path.is_file() and path.stat().st_size < 4_000_000:
                try:
                    yield name, path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue

    def hits(self, *prefixes):
        found = []
        for name, text in self.tracked(*prefixes):
            for pattern in self.PATTERNS:
                real = [m.group(0) for m in re.finditer(pattern, text)
                        if not any(f in m.group(0).lower() for f in self.FAKE)]
                if real:
                    found.append((name, pattern))
        return found

    def test_nc_11_no_credentials_in_the_repository(self):
        self.assertEqual([], self.hits("fullstack", "api", "docs/fullstack", "vercel.json", "supabase"))

    def test_nc_12_no_credentials_in_evidence(self):
        self.assertEqual([], self.hits("docs/fullstack/evidence"))
        for record in ("FS-09-LIVE-PREVIEW-2026-09-30-ACT-008.json",
                       "FS-09-ACT-008-REVOCATION-2026-09-30.json"):
            data = json.loads((EVIDENCE / record).read_text(encoding="utf-8"))
            self.assertNotIn("secret_value", json.dumps(data))

    def test_nc_13_no_credentials_in_telemetry(self):
        from fullstack.tests.support import OPERATOR_TOKEN, Harness
        h = Harness()
        try:
            h.call("GET", "/api/v1/runs", OPERATOR_TOKEN)
            h.call("GET", "/api/v1/runs", "wrong-token-value-123")
            h.call("POST", "/api/v1/agent-instances", OPERATOR_TOKEN,
                   {"definition": "engineering-intelligence-agent", "instance_key": "nc-probe-01",
                    "capabilities": ["engineering-intelligence"]})
            lines = "\n".join(h.telemetry.lines)
        finally:
            h.close()
        self.assertGreaterEqual(len(h.telemetry.lines), 3)
        for needle in (OPERATOR_TOKEN, "wrong-token-value-123", "Bearer", "operator@test",
                       "nc-probe-01", "engineering-intelligence"):
            self.assertNotIn(needle, lines)
        live = json.loads((EVIDENCE / "FS-09-LIVE-PREVIEW-2026-09-30-ACT-008.json").read_text(encoding="utf-8"))
        blob = "\n".join(live["observability"]["l1_lines_from_host_log"])
        self.assertNotIn("founder", blob)
        self.assertNotIn("live-desk", blob)


class Architecture(unittest.TestCase):

    def test_nc_14_no_frontend_authority_decision(self):
        """The console holds no scope rule of its own beyond disabling a button;
        the backend refuses regardless (covered live by the e2e)."""
        app = (REPO_ROOT / "fullstack/frontend/app.js").read_text(encoding="utf-8")
        self.assertNotRegex(app, r"(?i)isAdmin|allowAll|bypass|skipAuth")
        e2e = (REPO_ROOT / "fullstack/tests/e2e/console.e2e.mjs").read_text(encoding="utf-8")
        self.assertIn("an observer cannot register an Agent Instance even with the UI bypassed", e2e)

    def test_nc_15_no_silent_architecture_expansion(self):
        """The routes are the blueprint's table and only the A2 pair writes."""
        table = (REPO_ROOT / "docs/fullstack/FS-02-FULL-STACK-ARCHITECTURE-BLUEPRINT.md").read_text(encoding="utf-8")
        for route in contract.ROUTES:
            self.assertIn(route.template.replace("/api/v1", ""), table, route.template)
        self.assertEqual([("POST", "/api/v1/runs"), ("POST", "/api/v1/agent-instances")],
                         [(r.method, r.template) for r in contract.ROUTES if r.method != "GET"])
        self.assertFalse([p for p in (REPO_ROOT / "fullstack").rglob("*.py")
                          if re.search(r"factory|planner|scheduler|orchestrator", p.name, re.I)])


class TheGateDoesNotLie(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.recorded = readiness.preview_record()
        cls.good = dict(cls.recorded, current=True)

    def row(self, gate, name):
        return {f"{c['area']}: {c['criterion']}": c for c in gate["criteria"]}[name]

    def test_nc_16_no_mandatory_scenario_downgrading(self):
        gate = readiness.evaluate(runs=1)
        for name in ("Functionality: agent creation (Scenario A)",
                     "Functionality: core functions work (Scenario B)",
                     "Functionality: failure is a meaningful state (Scenario C)"):
            self.assertEqual("PASS", self.row(gate, name)["status"], name)
        a1 = readiness._scenario_a_row({"option": "A1", "entry": "X — y"}, {}, True, self.good)
        self.assertEqual("FAIL", a1["status"], "A1 cannot classify the scenario away")
        no_check = dict(self.good, passed=self.good["passed"] - {readiness.SCENARIO_A_LIVE})
        self.assertNotEqual("PASS", self.row(readiness.evaluate(runs=1, preview=no_check),
                                             "Functionality: agent creation (Scenario A)")["status"])

    def test_nc_17_no_false_pass(self):
        for mutation, expected in (
                (dict(self.good, passed=set()), "FAIL"),
                (dict(self.good, current=False), "BLOCKED")):
            gate = readiness.evaluate(runs=1, preview=mutation)
            live = [c for c in gate["criteria"] if readiness.PREVIEW in c["evidence_class"]
                    and c["status"] != readiness.OBSERVED]
            self.assertEqual({expected}, {c["status"] for c in live}, expected)
            self.assertNotEqual(readiness.READY, gate["result"])
        claim_only = readiness.evaluate(runs=1, preview=self.good,
                                        revocation={"revoked": False, "why": "claim only"})
        self.assertNotEqual("PASS", self.row(claim_only, "Security: temporary access revoked")["status"])

    def test_nc_18_no_stale_evidence_presented_as_current(self):
        self.assertIs(True, self.recorded["current"], "the recording covers the served tree")
        with mock.patch.object(readiness.subprocess, "run",
                               return_value=subprocess.CompletedProcess([], 1, "", "")):
            self.assertIs(False, readiness.preview_record()["current"])

    def test_nc_20_no_hidden_unresolved_residual(self):
        """Every limitation the gate carries is stated in its output."""
        gate = readiness.evaluate(runs=1)
        stated = [c["residual"] for c in gate["criteria"] if c.get("residual")]
        self.assertTrue(any("no automatic alert" in r for r in stated))
        self.assertEqual([], gate["awaiting"])
        record = (REPO_ROOT / "docs/fullstack/FS-09-ACT-008-EXECUTION-RECORD.md")
        if record.is_file():
            text = record.read_text(encoding="utf-8")
            for limitation in ("automatic alert", "P12", "console", "VERCEL_ENV"):
                self.assertIn(limitation, text)


class Recorded(unittest.TestCase):

    def setUp(self):
        self.record = json.loads((EVIDENCE / "FS-09-ACT-008-NEGATIVE-CONTROLS-2026-09-30.json")
                                 .read_text(encoding="utf-8"))

    def test_the_live_controls_are_recorded_first_hand(self):
        live = self.record["live"]
        self.assertEqual(0, live["production_rows"])                       # NC-08, NC-09
        self.assertEqual(0, live["temporary_bypass_count"])                # NC-10
        self.assertTrue(live["protection_enabled"])
        self.assertEqual(["preview"], live["environment_variable_targets"])  # NC-07
        self.assertEqual(1, len(live["production_deployments"]))
        self.assertGreater(live["preview_fullstack_agents_rows"], 0)


if __name__ == "__main__":
    unittest.main()
