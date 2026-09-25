"""`FDR-6` `CR-1`/`CR-2` — P13 prepared for certification, and not certified.

`FDR-6` `§10` requires the machinery to:

* recognize P13 as authorized;
* continue recognizing P13 as uncertified;
* reject premature certification;
* require the proper Founder Certification Decision for certification;
* preserve the integrity guard and the certified-root model.

*"No test update may itself constitute certification."* Every test that makes
P13 look certified does so in a disposable copy of the tree. The real acts,
Register and index are only read.
"""

from __future__ import annotations

import fnmatch
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import certified_evidence_integrity as integrity
from tools import certified_write_barrier as barrier
from tools import p12_certified_evidence_guard as sentinel
from tools import p12_phase_authorization as phases

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = "docs/architecture/p13"
BLUEPRINT = f"{ROOT}/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md"
PREPARED = "docs/governance/AIOS_P13_CERTIFICATION_MANIFEST_v1.0.json"
INDEX = "docs/governance/AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_v1.0.json"
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
FDR6 = "docs/governance/acts/FDR-6-P13-CERTIFICATION-GATE-FOUNDER-DECISION.md"
#: The registered index, as `GOAL-V2-004` recorded it (Decision Register).
INDEX_SHA256 = "34f9673a7a2fcd0ed6bd075d67b3dc5059f739085496886f6a5913a9ea44eb8e"


def _certification_body(phase: int) -> str:
    """The `FD-P12-006` decision-field form the guard recognises. Built here,
    for disposable copies only, and never written into the real acts root."""
    return "FOUNDER DECISION:\n" + f"P{phase} CERTIFICATION" + " = CERTIFY\n"


class P13IsAuthorizedPreparedAndNotCertified(unittest.TestCase):
    """The live tree."""

    def test_p13_is_authorized(self):
        p13 = {s["entity"]: s for s in phases.current_states()}["P13"]
        self.assertIs(True, p13["authorized"])
        self.assertEqual(FDR6, p13["authority_record"])

    def test_p13_is_not_certified(self):
        self.assertEqual(frozenset({10, 11, 12}), sentinel.certified_phases())
        self.assertNotIn("P13", phases.certifications()["phases"])
        self.assertNotIn("P13", integrity.verify().phases)

    def test_the_prepared_manifest_holds(self):
        report = integrity.verify()
        self.assertTrue(report.holds, json.dumps(report.as_reported(), indent=1))
        self.assertEqual((BLUEPRINT,), report.prepared["P13"].intact)

    def test_the_manifest_enumerates_the_actual_root(self):
        """`FDQ-5`: *"the actual contents of the certified root"*, and no
        supplementary evidence added into it."""
        record = json.loads((REPO_ROOT / PREPARED).read_text(encoding="utf-8"))
        on_disk = {Path(os.path.relpath(os.path.join(base, name), REPO_ROOT)).as_posix()
                   for base, _, names in os.walk(REPO_ROOT / ROOT) for name in names}
        self.assertEqual(on_disk, set(record["files"]))
        self.assertEqual(ROOT, record["evidence_root"])

    def test_the_manifest_is_its_commit_not_a_claim(self):
        from tools import p12_certified_evidence_manifest as rebuild
        record = json.loads((REPO_ROOT / PREPARED).read_text(encoding="utf-8"))
        rebuilt = rebuild.from_commit(record["prepared_commit"], evidence_root=ROOT)
        if rebuilt is None:
            self.skipTest("prepared commit not present in this clone")
        self.assertEqual(rebuilt, record["files"])

    def test_the_manifest_claims_no_certification(self):
        record = json.loads((REPO_ROOT / PREPARED).read_text(encoding="utf-8"))
        self.assertTrue(record["status"].startswith("PREPARED"))
        self.assertIn("NOT CERTIFIED", record["status"])
        self.assertIsNone(record["certifying_instrument"])
        self.assertIsNone(record["certified_commit"])

    def test_preparing_protects_nothing(self):
        """A manifest the barrier matched would protect the root at once: a
        certification in effect, made by a file name."""
        self.assertFalse(fnmatch.fnmatch(Path(PREPARED).name, barrier.MANIFEST_GLOB))
        self.assertFalse(barrier.refuses(REPO_ROOT / BLUEPRINT))
        self.assertFalse(barrier.refuses(REPO_ROOT / PREPARED))
        roots, _, _ = barrier.determine(REPO_ROOT)
        self.assertNotIn(os.path.realpath(REPO_ROOT / ROOT), roots)
        self.assertNotIn((REPO_ROOT / ROOT).resolve(),
                         [r.resolve() for r in sentinel.protected_roots()])

    def test_the_registered_index_is_unchanged(self):
        self.assertEqual(INDEX_SHA256, integrity.sha256_file(REPO_ROOT / INDEX))
        self.assertEqual({"P10", "P11", "P12"}, set(integrity.load_index()["phases"]))


def _copy(tmp: Path) -> Path:
    """A disposable copy of everything detection and the guard read."""
    repo = tmp / "repo"
    for relative in ("docs/architecture/platform-organization",
                     "docs/architecture/p11", "docs/architecture/p12", ROOT):
        shutil.copytree(REPO_ROOT / relative, repo / relative,
                        ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REPO_ROOT / "docs/governance/acts", repo / "docs/governance/acts")
    for manifest in (REPO_ROOT / "docs/governance").glob("AIOS_*MANIFEST*.json"):
        shutil.copyfile(manifest, repo / "docs/governance" / manifest.name)
    shutil.copyfile(REPO_ROOT / REGISTER, repo / REGISTER)
    return repo


class PrematureCertificationIsRejected(unittest.TestCase):
    """Disposable copies. The real tree is compared before and after."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = _copy(Path(self._tmp.name))
        self.before = integrity.verify()

    def tearDown(self):
        self._tmp.cleanup()
        self.assertEqual(integrity.verify(), self.before,
                         "a control changed the real tree")
        self.assertEqual(frozenset({10, 11, 12}), sentinel.certified_phases())

    def _verify(self):
        return integrity.verify(repo_root=self.repo)

    def _certify(self, *, registered: bool, name: str = "FD-P13-901-TEST-CERTIFICATION.md"):
        (self.repo / "docs/governance/acts" / name).write_text(
            _certification_body(13), encoding="utf-8")
        if registered:
            register = self.repo / REGISTER
            register.write_text(register.read_text(encoding="utf-8")
                                + f"\n| **Record** | `acts/{name}` |\n",
                                encoding="utf-8")

    def _certified(self):
        return sentinel.certified_phases(self.repo / "docs/governance/acts",
                                         self.repo / REGISTER)

    def test_the_pristine_copy_holds_with_p13_prepared(self):
        report = self._verify()
        self.assertTrue(report.holds, json.dumps(report.as_reported(), indent=1))
        self.assertIn("P13", report.prepared)

    def test_a_changed_p13_root_is_detected(self):
        (self.repo / BLUEPRINT).write_text("rewritten", encoding="utf-8")
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertEqual((BLUEPRINT,), report.prepared["P13"].modified)

    def test_supplementary_evidence_added_to_the_root_is_unexpected(self):
        """`FDQ-5`: *"No supplementary evidence may be silently added into the
        certified root."*"""
        added = f"{ROOT}/SUPPORTING-EVIDENCE.md"
        (self.repo / added).write_text("support", encoding="utf-8")
        self.assertEqual((added,), self._verify().prepared["P13"].unexpected)

    def test_an_unregistered_certification_is_rejected(self):
        self._certify(registered=False)
        self.assertNotIn(13, self._certified())
        report = self._verify()
        self.assertNotIn("P13", report.phases)
        self.assertTrue(report.holds, report.faults)
        roots, _, _ = barrier.determine(self.repo)
        self.assertNotIn(os.path.realpath(self.repo / ROOT), roots)

    def test_phase_authorization_is_not_certification(self):
        """The authorizing instrument itself certifies nothing."""
        self.assertNotIn(13, self._certified())
        self.assertEqual((), tuple(
            p for p, name in sentinel.certification_provenance(
                self.repo / "docs/governance/acts") if name.startswith("FDR-6")))

    def test_a_certification_without_promotion_is_a_fault(self):
        """What a real Founder Certification Decision would trigger: the guard
        recognises P13 and protects its root, and detection refuses to hold
        until the prepared manifest is promoted."""
        self._certify(registered=True)
        self.assertIn(13, self._certified())
        self.assertIn((self.repo / ROOT).resolve(), [
            r.resolve() for r in sentinel.protected_roots(
                self.repo, register=self.repo / REGISTER)])
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertIn("P13 is certified but its manifest is only prepared; it "
                      "must be promoted into an index under the certification "
                      "decision", report.faults)

    def test_promotion_adds_files_and_rewrites_no_certified_reference(self):
        self._certify(registered=True)
        index_before = (self.repo / INDEX).read_bytes()
        prepared = json.loads((self.repo / PREPARED).read_text(encoding="utf-8"))
        instrument = "docs/governance/acts/FD-P13-901-TEST-CERTIFICATION.md"
        certified = {**prepared, "manifest": "AIOS P13 Certified Evidence Manifest",
                     "status": "CERTIFIED", "certifying_instrument": instrument,
                     "certified_commit": prepared["prepared_commit"]}
        manifest = self.repo / "docs/governance/AIOS_P13_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"
        manifest.write_text(json.dumps(certified, indent=2) + "\n", encoding="utf-8")
        supplement = {"phases": {"P13": {
            "manifest": manifest.relative_to(self.repo).as_posix(),
            "manifest_sha256": integrity.sha256_file(manifest),
            "evidence_root": ROOT,
            "certified_commit": certified["certified_commit"],
            "certifying_instrument": instrument,
            "certifying_instrument_sha256": integrity.sha256_file(self.repo / instrument),
            "file_count": len(certified["files"]), "declared_additions": {}}}}
        path = self.repo / "docs/governance/AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_P13_v1.0.json"
        path.write_text(json.dumps(supplement, indent=2) + "\n", encoding="utf-8")
        report = self._verify()
        self.assertIn("index supplement sha256 is not recorded in the Decision "
                      f"Register: {path.name}", report.faults)
        register = self.repo / REGISTER
        register.write_text(register.read_text(encoding="utf-8")
                            + f"\n{integrity.sha256_file(path)}\n", encoding="utf-8")
        report = self._verify()
        self.assertTrue(report.holds, json.dumps(report.as_reported(), indent=1))
        self.assertEqual((BLUEPRINT,), report.phases["P13"].intact)
        self.assertNotIn("P13", report.prepared)
        self.assertEqual(index_before, (self.repo / INDEX).read_bytes())
        roots, files, _ = barrier.determine(self.repo)
        self.assertIn(os.path.realpath(self.repo / ROOT), roots)
        self.assertIn(os.path.realpath(path), files)

    def test_a_phase_indexed_twice_is_a_fault(self):
        index = json.loads((self.repo / INDEX).read_text(encoding="utf-8"))
        path = self.repo / "docs/governance/AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_X_v1.0.json"
        path.write_text(json.dumps({"phases": {"P12": index["phases"]["P12"]}}),
                        encoding="utf-8")
        self.assertIn(f"P12 is indexed more than once ({path.name})",
                      self._verify().faults)

    def test_a_prepared_manifest_that_claims_certification_is_a_fault(self):
        path = self.repo / PREPARED
        record = json.loads(path.read_text(encoding="utf-8"))
        record["certified_commit"] = record["prepared_commit"]
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        faults = self._verify().prepared["P13"].reference_faults
        self.assertIn(f"a prepared manifest claims a certification: {path.name}", faults)
        self.assertIn("prepared manifest sha256 is not recorded in the Decision "
                      f"Register: {path.name}", faults)

    def test_a_prepared_manifest_for_an_unauthorized_phase_is_a_fault(self):
        (self.repo / FDR6).unlink()
        faults = " ".join(self._verify().prepared["P13"].reference_faults)
        self.assertIn("P13 has a prepared manifest but is not phase-authorized", faults)

    def test_a_prepared_manifest_on_another_root_is_a_fault(self):
        path = self.repo / PREPARED
        record = json.loads(path.read_text(encoding="utf-8"))
        record["evidence_root"] = "docs/architecture/p13-preparation"
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        faults = " ".join(self._verify().prepared["P13"].reference_faults)
        self.assertIn("is not P13's root 'docs/architecture/p13'", faults)


if __name__ == "__main__":
    unittest.main()
