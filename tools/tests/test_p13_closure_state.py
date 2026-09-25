"""`FDR-G3`: the P13 closed state, its recognition, and its negative controls.

`§27` allows the transition to CLOSED only when:
- a valid Founder Closure Decision exists;
- it is persisted and registered;
- it is authoritative and not superseded;
- the closure evidence is satisfied.

`§28` lists twelve negative controls. NC-01 … NC-06 are refused by the reader
(`closures()`). NC-07 … NC-12 are closure attempts that carry a forbidden
effect, and the post-closure verification (`post_closure()`) must fail them.

The live tree is read only. Every control runs on a disposable copy, and the
real tree is compared before and after.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import certified_evidence_integrity as integrity
from tools import p12_phase_authorization as phases
from tools import p12_phase_authorization_verifier as verifier
from tools import p13_fresh_verification as fresh

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTER = phases.REGISTER_PATH
ACTS = "docs/governance/acts"
G3 = f"{ACTS}/FDR-G3-P13-CLOSURE-AND-TRANSITION-TO-GOVERNED-AIOS-OPERATION.md"
G2 = f"{ACTS}/FDR-G2-P13-CLOSURE-RESIDUAL-GOVERNANCE-AND-POST-CLOSURE-OPERATING-MODEL.md"
EVIDENCE = "docs/governance/p13-closure"
DECISION = "The Founder hereby grants:\n\nP13 CLOSURE = GRANTED\n"


def _item(report: dict, state: str) -> str:
    (item,) = [i for i in report["items"] if i["state"] == state]
    return item["status"]


class TheLiveClosedState(unittest.TestCase):

    def test_p13_is_closed_by_fdr_g3_and_nothing_else(self):
        result = phases.closures()
        self.assertTrue(result["resolved"])
        self.assertEqual({"P13"}, set(result["phases"]))
        self.assertEqual(G3, result["phases"]["P13"]["instrument"])
        self.assertEqual("FDR-G3", result["phases"]["P13"]["register_identity"])
        self.assertEqual((), result["rejected"])
        self.assertEqual({}, result["ambiguous"])

    def test_the_stated_form_in_fdr_g2_is_a_mention_not_a_closure(self):
        self.assertIn(G2, [m["instrument"] for m in phases.closures()["mentions"]])

    def test_the_lifecycle_runs_authorized_exit_certified_closed(self):
        state = phases.lifecycle("P13")
        self.assertEqual((True, True, True, True),
                         (state["authorized"], state["exit_satisfied"],
                          state["certified"], state["closed"]))
        self.assertEqual(G3, state["closure_source"])

    def test_closure_is_not_folded_into_the_dimensions(self):
        """The independent verifier holds dimensions to their cited section."""
        (p13,) = [s for s in phases.current_states() if s["entity"] == "P13"]
        self.assertEqual({"AUTHORIZED": True}, p13["dimensions"])
        self.assertTrue(all(c.status == verifier.SATISFIED for c in verifier.verify()))

    def test_the_post_closure_verification_holds(self):
        report = fresh.post_closure()
        self.assertTrue(report["holds"],
                        [i for i in report["items"] if i["status"] != fresh.PASS])
        self.assertEqual(fresh.PASS, _item(report, "P13 CLOSURE CLOSED"))

    def test_closure_changes_no_certification_or_authority(self):
        self.assertEqual(frozenset({10, 11, 12, 13}),
                         __import__("tools.p12_certified_evidence_guard",
                                    fromlist=["x"]).certified_phases())
        self.assertEqual(("P13",), tuple(phases.authorizations()["phases"]))


class _Copy(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "repo"
        shutil.copytree(REPO_ROOT, self.repo,
                        ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.before = integrity.verify()

    def tearDown(self):
        self._tmp.cleanup()
        self.assertEqual(integrity.verify(), self.before, "a control changed the real tree")

    def _text(self, relative: str) -> str:
        return (self.repo / relative).read_text(encoding="utf-8")

    def _write(self, relative: str, text: str) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _append_register(self, text: str) -> None:
        self._write(REGISTER, self._text(REGISTER) + "\n" + text + "\n")

    def _closed(self) -> bool:
        return "P13" in phases.closures(self.repo)["phases"]

    def _without_g3(self) -> None:
        (self.repo / G3).unlink()


class TheReaderRefusesAnInvalidClosure(_Copy):
    """NC-01 … NC-06."""

    def test_the_copy_is_closed(self):
        self.assertTrue(self._closed())

    def test_nc01_no_founder_closure_decision(self):
        self._without_g3()
        self.assertFalse(self._closed())
        self.assertEqual(fresh.FAIL, _item(fresh.post_closure(self.repo), "P13 CLOSURE CLOSED"))

    def test_nc02_a_historical_mention_does_not_close(self):
        self._without_g3()
        record = "docs/governance/AIOS_P13_CERTIFICATION_RECORD_v1.0.md"
        self._write(record, self._text(record) + "\n" + DECISION)
        self.assertFalse(self._closed(), "the stated form in FDR-G2 and a record "
                                         "outside the acts root close nothing")

    def test_nc03_a_non_authoritative_act_does_not_close(self):
        self._without_g3()
        name = "FDR-97-TEST-NOT-A-FOUNDER-DECISION.md"
        self._write(f"{ACTS}/{name}", DECISION)
        # Recorded, but as a CEO record, not a Founder Decision.
        self._append_register(f"### FDR-97 — CEO Record · test\n\n| Field | Value |\n"
                              f"|---|---|\n| **Identifier** | `FDR-97` |\n"
                              f"| **Decided by** | Claude Code |\n"
                              f"| **Record** | `acts/{name}` |")
        result = phases.closures(self.repo)
        self.assertFalse(self._closed())
        self.assertIn("not recorded in the Register as a Founder Decision",
                      " ".join(r["reason"] for r in result["rejected"]))

    def test_nc03_a_founder_decision_heading_not_decided_by_the_founder(self):
        """The heading alone is not authority: the entry must record the
        Founder as the decider."""
        self._without_g3()
        name = "FDR-92-TEST-MISLABELLED-ENTRY.md"
        self._write(f"{ACTS}/{name}", DECISION)
        self._append_register(f"### FDR-92 — Founder Decision · test\n\n| Field | Value |\n"
                              f"|---|---|\n| **Identifier** | `FDR-92` |\n"
                              f"| **Decided by** | Claude Code |\n"
                              f"| **Record** | `acts/{name}` |")
        self.assertFalse(self._closed())

    def test_nc04_a_superseded_closure_does_not_close(self):
        self._append_register("### FDR-96 — Founder Decision · test\n\n| Field | Value |\n"
                              "|---|---|\n| **Identifier** | `FDR-96` |\n"
                              "| **Decided by** | Founder |\n"
                              "| **Supersedes** | `FDR-G3` |")
        result = phases.closures(self.repo)
        self.assertFalse(self._closed())
        self.assertIn("superseded", " ".join(r["reason"] for r in result["rejected"]))

    def test_nc05_a_forged_decision_does_not_close(self):
        self._without_g3()
        self._write(f"{ACTS}/FDR-95-FORGED-P13-CLOSURE.md", "# forged\n\n" + DECISION)
        result = phases.closures(self.repo)
        self.assertFalse(self._closed())
        self.assertEqual(["docs/governance/acts/FDR-95-FORGED-P13-CLOSURE.md"],
                         [r["instrument"] for r in result["rejected"]])

    def test_nc06_closure_without_valid_evidence_does_not_close(self):
        for evidence in sorted((self.repo / EVIDENCE).glob("*.json")):
            with self.subTest(evidence.name):
                saved = evidence.read_bytes()
                evidence.unlink()
                self.assertFalse(self._closed())
                evidence.write_bytes(saved)
        self.assertTrue(self._closed())

    def test_nc06_evidence_registered_after_the_decision_does_not_count(self):
        """`FDR-G2` `§6.4`: gate, then fresh verification, then the decision."""
        register = self._text(REGISTER)
        (row,) = re.findall(r"^\| \*\*Fresh verification\*\* \|.*$", register, re.MULTILINE)
        self._write(REGISTER, register.replace(row, "| **Fresh verification** | moved |")
                    + "\n" + row + "\n")
        self.assertFalse(self._closed())

    def test_nc06_an_altered_gate_result_does_not_count(self):
        (gate_file,) = (self.repo / EVIDENCE).glob("P13-CLOSURE-GATE-*.json")
        record = json.loads(gate_file.read_text(encoding="utf-8"))
        record["counts"]["EVIDENCED"] = 8  # same claim, rewritten bytes
        gate_file.write_text(json.dumps(record), encoding="utf-8")
        self.assertFalse(self._closed(), "the registered sha256 no longer matches")

    def _reregister(self, pattern: str, change) -> None:
        """Rewrite an evidence file and register its new sha256 in place of the
        old one, so only the changed content can explain the result."""
        (path,) = (self.repo / EVIDENCE).glob(pattern)
        old = hashlib.sha256(path.read_bytes()).hexdigest()
        record = json.loads(path.read_text(encoding="utf-8"))
        change(record)
        path.write_text(json.dumps(record), encoding="utf-8")
        new = hashlib.sha256(path.read_bytes()).hexdigest()
        register = self._text(REGISTER)
        self.assertIn(old, register)
        self._write(REGISTER, register.replace(old, new))

    def test_re_registered_evidence_still_counts(self):
        """The positive control for the four below."""
        self._reregister("P13-CLOSURE-GATE-*.json", lambda r: r.update(note="x"))
        self._reregister("P13-FRESH-VERIFICATION-*.json", lambda r: r.update(note="x"))
        self.assertTrue(self._closed())

    def test_nc06_a_gate_that_is_not_satisfied_does_not_count(self):
        self._reregister("P13-CLOSURE-GATE-*.json", lambda r: r.update(gate="NOT SATISFIED"))
        self.assertFalse(self._closed())

    def test_nc06_a_gate_that_claims_to_close_does_not_count(self):
        self._reregister("P13-CLOSURE-GATE-*.json", lambda r: r.update(closes=True))
        self.assertFalse(self._closed())

    def test_nc06_a_failing_fresh_verification_does_not_count(self):
        self._reregister("P13-FRESH-VERIFICATION-*.json", lambda r: r.update(holds=False))
        self.assertFalse(self._closed())

    def test_nc06_a_fresh_verification_at_another_commit_does_not_count(self):
        self._reregister("P13-FRESH-VERIFICATION-*.json",
                         lambda r: r.update(commit="0" * 40))
        self.assertFalse(self._closed())

    def test_two_valid_decisions_are_ambiguous_and_neither_applies(self):
        name = "FDR-94-TEST-SECOND-P13-CLOSURE.md"
        self._write(f"{ACTS}/{name}", DECISION)
        register = self._text(REGISTER)
        heading = register.index("### FDR-G3 — Founder Decision")
        self._write(REGISTER, register[:heading]
                    + f"### FDR-94 — Founder Decision · test\n\n| Field | Value |\n"
                      f"|---|---|\n| **Identifier** | `FDR-94` |\n"
                      f"| **Decided by** | Founder |\n| **Record** | `acts/{name}` |\n\n"
                    + register[heading:])
        result = phases.closures(self.repo)
        self.assertIn("P13", result["ambiguous"])
        self.assertFalse(self._closed())


class ForbiddenEffectsFailPostClosureVerification(_Copy):
    """NC-07 … NC-12: a closure that brings a forbidden effect fails `§30`."""

    def _post(self) -> dict:
        return fresh.post_closure(self.repo)

    def test_the_copy_holds(self):
        self.assertTrue(self._post()["holds"])

    def _revive_env_02(self) -> None:
        path = "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
        text = self._text(path)
        self._write(path, text[:text.index("## 16. P13-ENV-02 Retirement Append")])

    def test_nc07_reviving_env_02_fails(self):
        self._revive_env_02()
        report = self._post()
        self.assertFalse(report["holds"])
        self.assertEqual(fresh.FAIL, _item(report, "P13-ENV-02 RETIRED"))

    def test_nc08_state_changing_authority_fails(self):
        self._revive_env_02()
        report = self._post()
        self.assertEqual(fresh.FAIL, _item(report, "STATE-CHANGING AUTHORITY NONE"))
        self.assertEqual(fresh.FAIL, _item(report, "S-OPS HISTORICAL ONLY"))

    def test_nc09_a_closure_that_creates_phase_14_fails(self):
        # `authorizations()` reads an instrument's first FOUNDER DECISION
        # section, so the authorization is a registered instrument of its own.
        self._write(f"{ACTS}/FDR-93-TEST-CLOSURE-WITH-PHASE-14.md",
                    "# test\n\n1. FOUNDER DECISION\n\nAUTHORIZE PHASE 14\n")
        self._append_register("| FDR-93 | test |")
        report = self._post()
        self.assertFalse(report["holds"])
        self.assertEqual(fresh.FAIL, _item(report, "PHASE 14 NOT ESTABLISHED"))

    def test_a_failing_fresh_check_alone_fails_post_closure(self):
        """A registered, unanchored closure grant closes nothing, so every
        `§30` item still passes. Only V16 fails, and that alone must fail."""
        self._write(f"{ACTS}/FDR-91-TEST-P13-CLOSURE.md", "# test\n\nP13 CLOSURE = GRANTED\n")
        self._append_register("| FDR-91 | test closure |")
        report = self._post()
        self.assertEqual([], [i["state"] for i in report["items"] if i["status"] != fresh.PASS])
        self.assertFalse(report["holds"])

    def test_nc10_modifying_certified_architecture_fails(self):
        blueprint = "docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md"
        self._write(blueprint, self._text(blueprint) + "closed\n")
        report = self._post()
        self.assertFalse(report["holds"])
        self.assertEqual(fresh.FAIL, _item(report, "CERTIFIED ROOT UNCHANGED"))

    def test_nc11_retroactively_certifying_p2_fails(self):
        self._write(G3, self._text(G3) + "\nFOUNDER DECISION: CERTIFY P2.\n")
        report = self._post()
        self.assertFalse(report["holds"])
        (v15,) = [c for c in report["fresh_verification"]["checks"] if c["id"] == "V15"]
        self.assertEqual(fresh.FAIL, v15["status"])

    def test_nc12_turning_residual_into_solved_fails(self):
        path = "docs/architecture/p13-preparation/P13-015-FOUNDATIONAL-QUESTION-RECONCILIATION.json"
        matrix = json.loads(self._text(path))
        (row,) = [r for r in matrix["questions"] if r["id"] == "Q38"]
        row["category"] = "ALREADY SOLVED"
        self._write(path, json.dumps(matrix))
        report = self._post()
        self.assertFalse(report["holds"])
        self.assertEqual(fresh.FAIL, _item(report, "C5 RESIDUALS NON-BLOCKING"))


if __name__ == "__main__":
    unittest.main()
