"""`FDR-G1` `FD-G3`: the certification baseline, reported as accepted.

The live tree must report exactly the `§40` model. Controls on disposable
copies show that evidence disagreeing with the accepted tier is reported as a
discrepancy. It is never silently reclassified: no retroactive certification
(`§23`, NC-06) and no upgrade of P4–P9 to machine-protected (`§25`, NC-07).
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from tools import certification_baseline as baseline
from tools import certified_evidence_integrity as integrity
from tools import p12_self_model as model

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTER = baseline.REGISTER

TIERS = {"P1–P3": "NO CERTIFICATION RECORD IDENTIFIED",
         "P4–P9": "CERTIFIED VIA FOUNDER DECISIONS / REGISTER",
         "P10–P13": "CERTIFIED + MACHINE-PROTECTED"}


def _copy(tmp: Path) -> Path:
    repo = tmp / "repo"
    for relative in ("docs/architecture/platform-organization", "docs/architecture/p11",
                     "docs/architecture/p12", "docs/architecture/p13"):
        shutil.copytree(REPO_ROOT / relative, repo / relative,
                        ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REPO_ROOT / "docs/governance/acts", repo / "docs/governance/acts")
    for manifest in (REPO_ROOT / "docs/governance").glob("AIOS_*MANIFEST*.json"):
        shutil.copyfile(manifest, repo / "docs/governance" / manifest.name)
    shutil.copyfile(REPO_ROOT / REGISTER, repo / REGISTER)
    return repo


class TheLiveBaseline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = baseline.baseline()

    def test_it_is_the_founder_accepted_model(self):
        self.assertTrue(self.result["holds"], self.result)
        self.assertTrue(self.result["accepted"])
        self.assertEqual(TIERS, self.result["tiers"])
        self.assertEqual([], self.result["discrepancies"])

    def test_every_phase_has_its_accepted_tier(self):
        expected = {**{f"P{n}": TIERS["P1–P3"] for n in (1, 2, 3)},
                    **{f"P{n}": TIERS["P4–P9"] for n in range(4, 10)},
                    **{f"P{n}": TIERS["P10–P13"] for n in range(10, 14)}}
        self.assertEqual(expected, {p: v["tier"] for p, v in self.result["phases"].items()})

    def test_the_uniform_claim_is_named_as_not_canonical(self):
        self.assertEqual("P1–P13 Certified Baseline", self.result["not_a_canonical_claim"])

    def test_the_self_model_reports_it_beside_what_the_guard_reads(self):
        answer = model.authority()
        self.assertEqual(TIERS, answer.value["certification_baseline"]["tiers"])
        self.assertEqual({"P10", "P11", "P12", "P13"},
                         set(answer.value["phase_authorization"]["certification"]["phases"]))


class DisagreementIsReportedNotReclassified(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = _copy(Path(self._tmp.name))
        self.before = integrity.verify()

    def tearDown(self):
        self._tmp.cleanup()
        self.assertEqual(integrity.verify(), self.before, "a control changed the real tree")

    def _append(self, text: str) -> None:
        with (self.repo / REGISTER).open("a", encoding="utf-8") as register:
            register.write(f"\n{text}\n")

    def _phase(self, phase: str) -> dict:
        return baseline.baseline(self.repo)["phases"][phase]

    def test_the_copy_holds(self):
        self.assertTrue(baseline.baseline(self.repo)["holds"])

    def test_a_certification_record_for_p2_is_a_discrepancy_not_a_certification(self):
        self._append("### FD-P2-999 — Founder Decision · Phase 2 Certification (test)")
        phase = self._phase("P2")
        self.assertEqual(baseline.DISCREPANCY, phase["tier"])
        self.assertEqual(TIERS["P1–P3"], phase["accepted_tier"])

    def test_a_missing_register_certification_is_a_discrepancy(self):
        path = self.repo / REGISTER
        text = path.read_text(encoding="utf-8")
        heading = "### FD-P7-003 — Founder Decision · Phase 7 Certification"
        self.assertIn(heading, text)
        path.write_text(text.replace(heading, "### FD-P7-003 — (heading removed)"),
                        encoding="utf-8")
        self.assertEqual(baseline.DISCREPANCY, self._phase("P7")["tier"])

    def test_a_machine_certification_of_p5_is_not_an_upgrade(self):
        (self.repo / "docs/governance/acts/FD-P5-999-TEST.md").write_text(
            "FOUNDER DECISION: CERTIFY P5.\n", encoding="utf-8")
        self._append("| FD-P5-999 | test |")
        phase = self._phase("P5")
        self.assertEqual(baseline.DISCREPANCY, phase["tier"])
        self.assertNotEqual(TIERS["P10–P13"], phase["tier"])

    def test_a_certified_phase_without_detection_is_not_machine_protected(self):
        (self.repo / "docs/governance/AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_P13_v1.0.json"
         ).unlink()
        phase = self._phase("P13")
        self.assertEqual(baseline.DISCREPANCY, phase["tier"])
        self.assertEqual(TIERS["P10–P13"], phase["accepted_tier"])

    def test_without_the_registered_acceptance_it_does_not_hold(self):
        path = self.repo / REGISTER
        path.write_text(path.read_text(encoding="utf-8").replace("FDR-G1", "FDR-XX"),
                        encoding="utf-8")
        result = baseline.baseline(self.repo)
        self.assertFalse(result["accepted"])
        self.assertFalse(result["holds"])

    def test_an_unreadable_register_is_unresolved(self):
        (self.repo / REGISTER).unlink()
        self.assertFalse(baseline.baseline(self.repo)["resolved"])


if __name__ == "__main__":
    unittest.main()
