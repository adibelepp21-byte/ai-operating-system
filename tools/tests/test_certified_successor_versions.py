"""`FDR-G1` `FD-G1`: certified successor versions, on disposable copies.

The Founder approved the model *"VERSIONED SUCCESSOR + IMMUTABLE HISTORICAL
BASELINE + RE-CERTIFICATION"*. Before it, detection allowed one certified
manifest per phase, so a legitimately certified successor would have been a
fault. These tests hold what the machinery now accepts and what it refuses.

No successor exists. Every successor here is built in a temporary copy, and
the real tree is compared before and after each test. Nothing here certifies,
supersedes or promotes anything; the copies only show how detection reads a
successor once the Founder has certified one.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import certified_evidence_integrity as integrity
from tools import certified_write_barrier as barrier
from tools import p12_certified_evidence_guard as sentinel

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
V1_MANIFEST = "docs/governance/AIOS_P13_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"
V1_ROOT = "docs/architecture/p13"
V2_ROOT = "docs/architecture/p13-successor-v2"
V2_FILE = f"{V2_ROOT}/AIOS_P13_CANONICAL_BLUEPRINT_v2.0.md"
V2_MANIFEST = "docs/governance/AIOS_P13_CERTIFIED_EVIDENCE_MANIFEST_v2.0.json"
V2_PREPARED = "docs/governance/AIOS_P13_CERTIFICATION_MANIFEST_v2.0.json"
V2_SUPPLEMENT = "docs/governance/AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_P13_V2_v1.0.json"
CERTIFYING = "docs/governance/acts/FDR-991-TEST-P13-SUCCESSOR-CERTIFICATION.md"
AUTHORIZING = "docs/governance/acts/FDR-990-TEST-P13-CHANGE-AUTHORIZATION.md"
VERIFICATION = "docs/governance/TEST_P13_V2_VERIFICATION_RECORD.md"
FDR7 = "docs/governance/acts/FDR-7-P13-FOUNDER-CERTIFICATION-AND-FINAL-SYSTEM-ACCEPTANCE.md"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _copy(tmp: Path) -> Path:
    """A disposable copy of everything detection, the guard and the barrier read."""
    repo = tmp / "repo"
    for relative in ("docs/architecture/platform-organization",
                     "docs/architecture/p11", "docs/architecture/p12", V1_ROOT):
        shutil.copytree(REPO_ROOT / relative, repo / relative,
                        ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REPO_ROOT / "docs/governance/acts", repo / "docs/governance/acts")
    for manifest in (REPO_ROOT / "docs/governance").glob("AIOS_*MANIFEST*.json"):
        shutil.copyfile(manifest, repo / "docs/governance" / manifest.name)
    shutil.copyfile(REPO_ROOT / REGISTER, repo / REGISTER)
    return repo


class Successor:
    """Builds a P13 v2 in a copy. Each keyword breaks one rule."""

    def __init__(self, repo: Path):
        self.repo = repo

    def _write(self, relative: str, text: str) -> str:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return _sha(path.read_bytes())

    def _register(self, text: str) -> None:
        with (self.repo / REGISTER).open("a", encoding="utf-8") as register:
            register.write(f"\n{text}\n")

    def instruments(self, *, certify_phase: int = 13, register_certifying: bool = True,
                    register_authorizing: bool = True) -> None:
        self._write(CERTIFYING, "# test successor certification\n\n"
                    f"FOUNDER DECISION: CERTIFY P{certify_phase}.\n")
        self._write(AUTHORIZING, "# test change authorization\n\nAPPROVED.\n")
        if register_certifying:
            self._register("| FDR-991 | test successor certification |")
        if register_authorizing:
            self._register("| FDR-990 | test change authorization |")

    def root(self, root: str = V2_ROOT) -> dict:
        relative = f"{root}/AIOS_P13_CANONICAL_BLUEPRINT_v2.0.md"
        return {relative: self._write(relative, "# P13 Blueprint v2 (test)\n")}

    def entry(self, files: dict, *, root: str = V2_ROOT, version=2,
              supersedes: dict = None, certifying: str = CERTIFYING,
              omit: tuple = (), verification_sha: str = None) -> dict:
        manifest = {"manifest": "AIOS P13 Certified Evidence Manifest", "version": "2.0",
                    "phase": "13", "certifying_instrument": certifying,
                    "certified_commit": "0" * 40, "evidence_root": root, "files": files}
        manifest_sha = self._write(V2_MANIFEST, json.dumps(manifest, indent=2))
        verification = self._write(VERIFICATION, "# verification of P13 v2 (test)\n")
        v1_sha = _sha((self.repo / V1_MANIFEST).read_bytes())
        entry = {
            "manifest": V2_MANIFEST, "manifest_sha256": manifest_sha,
            "evidence_root": root, "certified_commit": "0" * 40,
            "certifying_instrument": certifying,
            "certifying_instrument_sha256": _sha((self.repo / certifying).read_bytes()),
            "declared_additions": {},
            "certified_version": version,
            "supersedes_certified": supersedes or {"manifest": V1_MANIFEST,
                                                   "manifest_sha256": v1_sha},
            "change_authorization": {
                "instrument": AUTHORIZING,
                "instrument_sha256": _sha((self.repo / AUTHORIZING).read_bytes())},
            "supersession_reason": "test: the successor changes the Blueprint",
            "verification_record": {"path": VERIFICATION,
                                    "sha256": verification_sha or verification},
        }
        for name in omit:
            entry.pop(name)
        return entry

    def index(self, *entries: dict, register: bool = True,
              name: str = V2_SUPPLEMENT) -> None:
        body = {"index": "test successor supplement",
                "phases": {"P13": entries[0]}} if len(entries) == 1 else None
        if body is None:
            # Two entries for one phase need two files: a JSON object holds
            # one key per phase.
            for number, entry in enumerate(entries):
                self.index(entry, register=register,
                           name=name.replace("_v1.0", f"_{number}_v1.0"))
            return
        sha = self._write(name, json.dumps(body, indent=2))
        if register:
            self._register(f"| test supplement | `{sha}` |")

    def build(self, **breaks) -> None:
        self.instruments(**{k: breaks.pop(k) for k in list(breaks)
                            if k in ("certify_phase", "register_certifying",
                                     "register_authorizing")})
        register = breaks.pop("register_index", True)
        files = self.root(breaks.get("root", V2_ROOT))
        self.index(self.entry(files, **breaks), register=register)


class _Sandbox(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = _copy(Path(self._tmp.name))
        self.successor = Successor(self.repo)
        self.before = integrity.verify()

    def tearDown(self):
        self._tmp.cleanup()
        self.assertEqual(integrity.verify(), self.before, "a control changed the real tree")

    def _verify(self):
        return integrity.verify(repo_root=self.repo)

    def assertFault(self, report, text, *, v1_current: bool = True):
        self.assertFalse(report.holds)
        self.assertTrue(any(text in fault for fault in report.faults), report.faults)
        if v1_current:
            self.assertEqual([(1, integrity.CURRENT, V1_MANIFEST)],
                             [(v["version"], v["state"], v["manifest"])
                              for v in report.versions["P13"]],
                             "nothing after a fault is current")


class TheLiveTreeHasOneVersionPerPhase(unittest.TestCase):

    def test_every_certified_phase_is_version_one_and_current(self):
        report = integrity.verify()
        self.assertTrue(report.holds, report.faults)
        self.assertEqual({"P10", "P11", "P12", "P13"}, set(report.versions))
        for phase, chain in report.versions.items():
            with self.subTest(phase):
                self.assertEqual(1, len(chain))
                self.assertEqual((1, integrity.CURRENT, None),
                                 (chain[0]["version"], chain[0]["state"],
                                  chain[0]["superseded_by"]))
        self.assertEqual({}, report.historical)

    def test_no_successor_or_prepared_successor_is_resident(self):
        for path in (REPO_ROOT / "docs/governance").glob("AIOS_*.json"):
            with self.subTest(path.name):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("supersedes_certified", text)
                self.assertNotIn("certified_version", text)


class ACertifiedSuccessorIsAccepted(_Sandbox):

    def test_v2_is_current_and_v1_stays_verified_as_superseded(self):
        self.successor.build()
        report = self._verify()
        self.assertTrue(report.holds, json.dumps(report.as_reported(), indent=1))
        chain = report.versions["P13"]
        self.assertEqual([(1, integrity.SUPERSEDED, V2_MANIFEST),
                          (2, integrity.CURRENT, None)],
                         [(v["version"], v["state"], v["superseded_by"]) for v in chain])
        self.assertEqual((V2_FILE,), report.phases["P13"].intact)
        self.assertEqual(("docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md",),
                         report.historical["P13 v1"].intact)
        self.assertEqual(frozenset({10, 11, 12, 13}),
                         sentinel.certified_phases(self.repo / "docs/governance/acts",
                                                   self.repo / REGISTER))

    def test_the_superseded_baseline_is_still_immutable(self):
        """Superseded is historical, not editable (`FDR-G1` `§5`, `§13`)."""
        self.successor.build()
        blueprint = self.repo / V1_ROOT / "AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md"
        blueprint.write_text(blueprint.read_text(encoding="utf-8") + "edit\n",
                             encoding="utf-8")
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertEqual((f"{V1_ROOT}/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md",),
                         report.historical["P13 v1"].modified)

    def test_the_barrier_keeps_both_roots_and_both_manifests(self):
        """Nothing is unprotected by supersession, and the successor's root is
        protected from its certified manifest on."""
        self.successor.build()
        roots, files, _ = barrier.determine(self.repo)
        for root in (V1_ROOT, V2_ROOT):
            self.assertIn(str((self.repo / root).resolve()), {str(Path(r).resolve())
                                                              for r in roots})
        names = {Path(f).name for f in files}
        self.assertIn(Path(V1_MANIFEST).name, names)
        self.assertIn(Path(V2_MANIFEST).name, names)


class ASuccessorIsRefusedWithoutItsWarrant(_Sandbox):
    """`FDR-G1` `§7`: no successor without Founder certification. Each control
    removes one condition; the successor must never become current."""

    def test_citing_the_earlier_certification_is_refused(self):
        self.successor.build(certifying=FDR7)
        self.assertFault(self._verify(), "needs its own Founder certification")

    def test_an_instrument_certifying_another_phase_is_refused(self):
        self.successor.build(certify_phase=12)
        self.assertFault(self._verify(), "does not certify P13")

    def test_an_unregistered_certification_is_refused(self):
        self.successor.build(register_certifying=False)
        self.assertFault(self._verify(), "does not certify P13")

    def test_an_unregistered_change_authorization_is_refused(self):
        self.successor.build(register_authorizing=False)
        self.assertFault(self._verify(), "change authorization instrument resolves "
                                         "against no Register entry")

    def test_an_unregistered_index_is_a_fault(self):
        self.successor.build(register_index=False)
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertTrue(any("not recorded in the Decision Register" in f
                            for f in report.faults), report.faults)


class ABrokenChainIsRefused(_Sandbox):

    def test_a_wrong_predecessor_is_refused(self):
        self.successor.build(supersedes={"manifest": V1_MANIFEST, "manifest_sha256": "0" * 64})
        self.assertFault(self._verify(), "does not supersede v1's manifest")

    def test_a_gap_is_refused(self):
        self.successor.build(version=3)
        self.assertFault(self._verify(), "P13 v3 has no v2 before it")

    def test_a_fork_is_refused(self):
        self.successor.instruments()
        files = self.successor.root()
        first = self.successor.entry(files)
        second = dict(first, supersession_reason="a competing successor")
        self.successor.index(first, second)
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertTrue(any("P13 v2 is indexed more than once" in f
                            for f in report.faults), report.faults)

    def test_an_unversioned_second_entry_is_still_refused(self):
        """What held before `FDR-G1` still holds: a phase indexed twice is a
        fault. Which of the two entries is read first depends only on file
        order, as it always did, so the fault is what this holds, not which
        entry survives it."""
        self.successor.build(omit=("certified_version",))
        self.assertFault(self._verify(), "P13 is indexed more than once",
                         v1_current=False)

    def test_reusing_or_nesting_in_the_earlier_root_is_refused(self):
        for root in (V1_ROOT, f"{V1_ROOT}/v2"):
            with self.subTest(root):
                self.successor.build(root=root)
                self.assertFault(self._verify(), "a successor never edits a certified "
                                                 "baseline")

    def test_missing_provenance_is_refused(self):
        for field in integrity.SUCCESSOR_FIELDS:
            with self.subTest(field):
                self.successor.build(omit=(field,))
                self.assertFault(self._verify(), f"P13 v2 lacks {field}")

    def test_an_altered_verification_record_is_refused(self):
        self.successor.build(verification_sha="0" * 64)
        self.assertFault(self._verify(), "verification record altered")


class APreparedSuccessorClaimsNothing(_Sandbox):

    def _prepare(self, *, root: str = V2_ROOT, certify: bool = False,
                 supersedes_sha: str = None, register: bool = True) -> None:
        self.successor.instruments()
        files = self.successor.root(root)
        v1_sha = _sha((self.repo / V1_MANIFEST).read_bytes())
        record = {"manifest": "AIOS P13 Certification Manifest", "version": "2.0",
                  "phase": "13", "status": "PREPARED — NOT CERTIFIED",
                  "certifying_instrument": FDR7 if certify else None,
                  "certified_commit": None, "evidence_root": root,
                  "certified_version": 2,
                  "supersedes_certified": {"manifest": V1_MANIFEST,
                                           "manifest_sha256": supersedes_sha or v1_sha},
                  "change_authorization": {
                      "instrument": AUTHORIZING,
                      "instrument_sha256": _sha((self.repo / AUTHORIZING).read_bytes())},
                  "files": files}
        sha = self.successor._write(V2_PREPARED, json.dumps(record, indent=2))
        if register:
            self.successor._register(f"| test prepared successor | `{sha}` |")

    def test_a_prepared_successor_is_verified_and_protects_nothing(self):
        self._prepare()
        report = self._verify()
        self.assertTrue(report.holds, json.dumps(report.as_reported(), indent=1))
        self.assertEqual((V2_FILE,), report.prepared["P13 v2"].intact)
        self.assertEqual(1, len(report.versions["P13"]), "preparing supersedes nothing")
        roots, _, _ = barrier.determine(self.repo)
        self.assertNotIn(str((self.repo / V2_ROOT).resolve()),
                         {str(Path(r).resolve()) for r in roots})

    def test_a_prepared_successor_that_claims_certification_is_a_fault(self):
        self._prepare(certify=True)
        self.assertIn("claims a certification",
                      " ".join(self._verify().prepared["P13 v2"].reference_faults))

    def test_a_prepared_successor_inside_the_certified_root_is_a_fault(self):
        self._prepare(root=f"{V1_ROOT}/v2")
        self.assertIn("reuses or nests with the certified root",
                      " ".join(self._verify().prepared["P13 v2"].reference_faults))

    def test_a_prepared_successor_of_the_wrong_version_is_a_fault(self):
        self._prepare(supersedes_sha="0" * 64)
        self.assertIn("is not prepared as the successor",
                      " ".join(self._verify().prepared["P13 v2"].reference_faults))

    def test_an_unregistered_prepared_successor_is_a_fault(self):
        self._prepare(register=False)
        self.assertIn("not recorded in the Decision Register",
                      " ".join(self._verify().prepared["P13 v2"].reference_faults))


if __name__ == "__main__":
    unittest.main()
