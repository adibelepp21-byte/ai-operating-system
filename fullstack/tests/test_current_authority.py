"""FDP-010-03: the current FS-10 authority layer, and the closed FS-09 gate kept as history.

Closure conditions (FDP-010 §10.5): the historical FS-09 wording is preserved;
current FS-10 authority points to FDP-009 / FDP-010; no current execution path
reads the historical wording as overriding them; the distinction is documented.
"""

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path

from fullstack.backend import security

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS = REPO_ROOT / "docs" / "fullstack"
CURRENT = json.loads((DOCS / "FS-10-CURRENT-AUTHORITY.json").read_text(encoding="utf-8"))
#: FS-09 closed here (`FS-09-ACT-008-EXECUTION-RECORD.md`); the gate is history from then on.
FS09_CLOSED = "de47057"
HISTORICAL_WORDING = "Production rollback is Founder-only (FD-FS-001 D4-A)"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True,
                          check=True).stdout


def _fenced_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    body = text[text.index("````text\n") + 8:text.rindex("\n````")]
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _current_section(path: Path) -> str:
    """A document's current state: everything before its first History heading."""
    text = path.read_text(encoding="utf-8")
    return text.split("\n# History", 1)[0]


class TheHistoricalGateIsPreserved(unittest.TestCase):

    def test_the_fs09_gate_is_byte_identical_to_its_closing_state(self):
        closed = _git("show", f"{FS09_CLOSED}:fullstack/readiness.py")
        now = (REPO_ROOT / "fullstack" / "readiness.py").read_text(encoding="utf-8")
        self.assertEqual(closed, now)

    def test_its_rollback_wording_still_exists(self):
        """FDP-010 §10.4: never pretend the old wording did not exist."""
        self.assertIn(HISTORICAL_WORDING,
                      (REPO_ROOT / "fullstack" / "readiness.py").read_text(encoding="utf-8"))
        runbook = (DOCS / "FS-09-OPERATIONAL-RUNBOOK.md").read_text(encoding="utf-8")
        history = [line for line in runbook.splitlines() if "**Founder only**" in line]
        self.assertEqual(1, len(history))
        self.assertTrue(history[0].startswith("| *History (FS-09"), history[0])


class CurrentAuthorityPointsToFdp009AndFdp010(unittest.TestCase):

    def test_both_decisions_are_named_with_their_registered_hashes(self):
        register = (REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
                    ).read_text(encoding="utf-8")
        for name, number in (("FDP-009", "§107"), ("FDP-010", "§109")):
            entry = CURRENT["decisions"][name]
            self.assertEqual(number, entry["register"])
            self.assertEqual(entry["sha256"], _fenced_sha256(REPO_ROOT / entry["record"]))
            self.assertIn(entry["sha256"], register)

    def test_rollback_is_ceo_with_boundary_and_cites_the_current_decisions(self):
        for key in ("rollback_before_release", "rollback_after_release"):
            row = CURRENT["authority"][key]
            self.assertEqual("CEO-AUTHORIZED-WITH-BOUNDARY", row["class"])
            self.assertTrue(any(s.startswith(("FDP-009", "FDP-010")) for s in row["sources"]))
            self.assertIn("verified known-good target only", row["conditions"])
        self.assertIn("FDP-010-02", CURRENT["authority"]["rollback_after_release"]["sources"])

    def test_release_live_and_acceptance_stay_with_the_founder(self):
        for key in ("production_release", "live", "final_system_acceptance"):
            self.assertEqual("FOUNDER-RESERVED", CURRENT["authority"][key]["class"])

    def test_the_historical_wording_is_listed_as_superseded_not_current(self):
        rows = CURRENT["supersedes_for_current_operation"]
        gate = [r for r in rows if r["historical"].startswith("fullstack/readiness.py")]
        self.assertEqual(1, len(gate))
        self.assertIn(HISTORICAL_WORDING, gate[0]["historical"])
        self.assertTrue(gate[0]["status"].startswith("HISTORICAL"))

    def test_current_documents_cite_fdp010_and_state_no_founder_only_rollback(self):
        for path in (DOCS / "FS-10-DEPLOYMENT.md", DOCS / "FS-10-CURRENT-AUTHORITY.md",
                     DOCS / "FS-10-RELEASE-PACKAGE.md"):
            current = _current_section(path)
            self.assertIn("FDP-010", current, path.name)
            for line in current.splitlines():
                if re.search(r"(?i)rollback[^|]*founder[- ]only", line):
                    self.assertRegex(line, r"(?i)histor|supersed|preserved|stale|closed FS-09",
                                     f"{path.name}: {line}")


class NoCurrentExecutionPathReadsTheHistoricalGate(unittest.TestCase):

    def test_nothing_but_the_gate_itself_and_tests_imports_it(self):
        importers = []
        for path in REPO_ROOT.rglob("*.py"):
            rel = path.relative_to(REPO_ROOT).as_posix()
            if "/tests/" in rel or rel == "fullstack/readiness.py" or "__pycache__" in rel:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if re.search(r"^\s*(from fullstack(\.| )import readiness|from fullstack\.readiness|"
                         r"import fullstack\.readiness)", text, re.M):
                importers.append(rel)
        self.assertEqual([], importers)

    def test_no_served_or_operational_module_carries_the_wording(self):
        carriers = [p.relative_to(REPO_ROOT).as_posix()
                    for root in ("api", "fullstack/backend", "fullstack/deploy", "fullstack/frontend")
                    for p in (REPO_ROOT / root).rglob("*") if p.is_file()
                    and p.suffix in (".py", ".js", ".html", ".json")
                    and "Founder-only" in p.read_text(encoding="utf-8", errors="replace")]
        self.assertEqual([], carriers)


class TheOperationalPrincipalIsLeastPrivilege(unittest.TestCase):

    def test_scopes_come_from_the_canonical_model_and_exclude_registration(self):
        principal = CURRENT["operational_principal"]
        self.assertEqual("aios-operator", principal["subject"])
        self.assertTrue(set(principal["scopes"]) < set(security.SCOPES))
        self.assertNotIn(security.AGENT_REGISTER, principal["scopes"])
        self.assertEqual(sorted([security.OBSERVE, security.RUN_WORKFLOW, security.AUDIT]),
                         sorted(principal["scopes"]))
        self.assertRegex(principal["sha256"], r"^[0-9a-f]{64}$")

    def test_no_plaintext_token_is_recorded(self):
        for path in (DOCS / "FS-10-CURRENT-AUTHORITY.json", DOCS / "FS-10-CURRENT-AUTHORITY.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"Bearer [A-Za-z0-9_\-]{20,}")


class TheRollbackTargetIsValid(unittest.TestCase):

    def test_the_target_is_not_the_pre_application_deployment(self):
        target = CURRENT["rollback_target"]
        self.assertNotEqual("dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj", target["designated"]["deployment"])
        self.assertIn("NOT A VALID APPLICATION ROLLBACK TARGET",
                      target["not_targets"]["dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj"])

    def test_the_target_runs_the_release_candidate_and_is_not_the_serving_deployment(self):
        target = CURRENT["rollback_target"]
        self.assertEqual("d05261cb7c02c6c489efbe5dff67ec86a22c0136", target["designated"]["commit"])
        self.assertEqual(target["designated"]["commit"], target["serving"]["commit"])
        self.assertNotEqual(target["designated"]["deployment"], target["serving"]["deployment"])


if __name__ == "__main__":
    unittest.main()
