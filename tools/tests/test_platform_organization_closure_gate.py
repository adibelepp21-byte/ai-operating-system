"""Tests for the Final Platform Organization Closure Gate (`FD-PO-004` §12–§14).

`TheLiveState` checks the repository as it is. The controls mutate a copy of
`docs/`. They prove three things:
- the gate closes only when every criterion holds;
- it can close (a positive control that applies D2 in the copy);
- it never infers a decision the Register does not record.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import platform_division_construction as pc
from tools import platform_organization_closure_gate as cg
from tools import platform_organization_gate as po

REPO_ROOT = Path(__file__).resolve().parents[2]
CLOSES = "| **Closes** | `G-01` · `FDP-P10-001` · `FDP-P10-002` |"
DECISION = ("| **Decision** | D1: *\"D1-A Certify w/ residual\"*. D2: *\"D2-A Supply volumes\"*. "
            "D3: *\"D3-A Bind\"*. D4: *\"D4-A Bind\"* |")


class TheLiveState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report = cg.evaluate()

    def test_it_reads_the_recorded_selections(self):
        self.assertEqual({"D1": "D1-A", "D2": "D2-A", "D3": "D3-A", "D4": "D4-A"},
                         self.report["selections"])

    def test_not_closed_with_exactly_the_d2_blocker(self):
        self.assertEqual(cg.NOT_CLOSED, self.report["state"])
        self.assertEqual(["ESC-C7-01", "FN-1"], self.report["open_blocking_items"])
        self.assertEqual(1, len(self.report["blockers"]))
        self.assertIn("D2-A (supply) not yet applied", self.report["blockers"][0])

    def test_every_other_criterion_passes(self):
        failing = [c["criterion"] for c in self.report["criteria"] if not c["passes"]]
        self.assertEqual(["§12.1 Construction"], failing)

    def test_every_residual_is_classified(self):
        for identifier, (kind, cls, basis) in self.report["residuals"].items():
            self.assertIn(kind, (cg.BLOCKER, cg.ACCEPTED, cg.CLASSIFIED), identifier)
            self.assertTrue(cls and basis, identifier)

    def test_it_decides_nothing(self):
        self.assertFalse(self.report["certifies"])
        self.assertFalse(self.report["grants_authority"])
        self.assertFalse(self.report["decides"])


class Controls(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # The whole tree, as the gate's own controls use: the P13 fresh
        # verification the gate consults reads beyond `docs/`.
        cls.tmp = Path(tempfile.mkdtemp(prefix="pocg-")) / "repo"
        shutil.copytree(REPO_ROOT, cls.tmp, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp.parent, ignore_errors=True)

    def setUp(self):
        self.saved = {}
        self.created = []

    def tearDown(self):
        for path, data in self.saved.items():
            path.write_bytes(data)
        for path in reversed(self.created):
            shutil.rmtree(path, ignore_errors=True)

    def _edit(self, relative, old, new):
        path = self.tmp / relative
        data = path.read_bytes()
        self.saved.setdefault(path, data)
        text = data.decode("utf-8")
        self.assertIn(old, text, f"control fixture drifted: {old[:50]!r}")
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def _append_register(self, text):
        path = self.tmp / po.REGISTER
        self.saved.setdefault(path, path.read_bytes())
        path.write_text(path.read_text(encoding="utf-8") + "\n" + text + "\n", encoding="utf-8")

    def _apply_d2(self):
        """Stand-in for Volumes 3 and 4 received, and the Founder closing the
        residency item and FN-1. Evidence of what closing requires, not a
        simulation of the real bodies."""
        for n, slug in ((3, "pd-03-governance-and-compliance"), (4, "pd-04-knowledge-and-intelligence")):
            base = self.tmp / f"docs/architecture/volume-{n}"
            self.created.append(base)
            (base / slug).mkdir(parents=True)
            (base / slug / "A1.md").write_text("# A1 — test body\n", encoding="utf-8")
        self._append_register("### FDR-TEST-D2 — Founder Decision · test\n\n| Field | Value |\n"
                              "|---|---|\n| **Identifier** | `FDR-TEST-D2` |\n"
                              "| **Decided by** | Founder |\n| **Closes** | `ESC-C7-01` · `FN-1` |")

    def _state(self):
        return cg.evaluate(self.tmp)

    def _criterion(self, report, name):
        return next(c for c in report["criteria"] if c["criterion"].startswith(name))

    def test_the_copy_matches_the_live_state(self):
        self.assertEqual(cg.NOT_CLOSED, self._state()["state"])

    def test_positive_applying_d2_closes_the_platform_organization(self):
        self._apply_d2()
        report = self._state()
        self.assertEqual([], report["blockers"])
        self.assertEqual(cg.CLOSED, report["state"])

    def test_no_decision_inferred_when_selections_are_absent(self):
        self._edit(po.REGISTER, DECISION, "| **Decision** | (none) |")
        report = self._state()
        self.assertEqual({"D1": None, "D2": None, "D3": None, "D4": None}, report["selections"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_d1_b_would_contradict_a_canonical_baseline(self):
        self._apply_d2()
        self._edit(po.REGISTER, "D1-A Certify w/ residual", "D1-B Keep non-canonical")
        report = self._state()
        self.assertEqual(cg.NOT_CLOSED, report["state"])
        self.assertFalse(self._criterion(report, "§12.3")["passes"])

    def test_binding_without_its_selection_fails_authority_integrity(self):
        self._apply_d2()
        self._edit(po.REGISTER, "D3: *\"D3-A Bind\"*", "D3: *\"D3-B Deliberately not bound\"*")
        report = self._state()
        self.assertFalse(self._criterion(report, "§12.4")["passes"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_a_certified_class_changed_fails_epistemic_integrity(self):
        self._apply_d2()
        self._edit(pc.VOLUMES["PD-10"], "**Dimension:** Authority · **Class:** UNKNOWN",
                   "**Dimension:** Authority · **Class:** DOMAIN-ADAPTATION")
        report = self._state()
        self.assertFalse(self._criterion(report, "§12.3")["passes"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_an_unclassified_open_item_fails_residual_integrity(self):
        self._apply_d2()
        original = dict(cg.CLOSURE_CLASSIFICATION)
        del cg.CLOSURE_CLASSIFICATION["G-06"]
        try:
            report = self._state()
        finally:
            cg.CLOSURE_CLASSIFICATION.clear()
            cg.CLOSURE_CLASSIFICATION.update(original)
        self.assertFalse(self._criterion(report, "§12.6")["passes"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_an_ownership_collision_fails_coherence(self):
        self._apply_d2()
        path = f"{po.DIVISIONS_DIR}/PD-07-infrastructure-and-platform.md"
        self._edit(path, "## 1. Established", "## 1. Established\n\n- PD-07 owns Runtime.")
        report = self._state()
        self.assertFalse(self._criterion(report, "§12.5")["passes"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_a_certified_root_edit_fails_protected_root_integrity(self):
        self._apply_d2()
        path = f"{po.VOLUME_2}/C8.md"
        self._edit(path, "PD-07 tetap memiliki ownership atas Infrastructure.",
                   "PD-07 tetap memiliki ownership atas Infrastructure. (edited)")
        report = self._state()
        self.assertFalse(self._criterion(report, "§12.7")["passes"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_a_phase_14_reference_fails(self):
        self._apply_d2()
        self._edit(pc.VOLUMES["PD-05"], "# PD-05 — Runtime & Execution", "# PD-05 — Runtime & Execution (Phase 14)")
        report = self._state()
        self.assertFalse(self._criterion(report, "§14")["passes"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_a_volume_failing_verification_fails_construction(self):
        self._apply_d2()
        self._edit(pc.VOLUMES["PD-06"], "B4.md` — \"PD-06 owns implementation.\"",
                   "B4.md` — \"PD-06 owns all implementation.\"")
        report = self._state()
        c121 = self._criterion(report, "§12.1")
        self.assertFalse(c121["passes"])
        self.assertTrue(any("PD-05 … PD-10 not" in b for b in c121["blockers"]))

    def test_recertifying_a_class_without_an_instrument_fails_epistemic_integrity(self):
        """Change a class in both the volume and the certification manifest: the
        verifier then agrees with itself, and only the Founder's certified
        counts (FD-PO-004 §2) catch it."""
        self._apply_d2()
        self._edit(pc.VOLUMES["PD-10"], "**Dimension:** Authority · **Class:** UNKNOWN",
                   "**Dimension:** Authority · **Class:** DOMAIN-ADAPTATION")
        path = self.tmp / pc.CANONICAL_MANIFEST
        self.saved.setdefault(path, path.read_bytes())
        manifest = json.loads(path.read_text(encoding="utf-8"))
        classes = manifest["volumes"]["PD-10"]["classes"]
        self.assertIn(["A3", "UNKNOWN"], classes)
        classes[classes.index(["A3", "UNKNOWN"])] = ["A3", "DOMAIN-ADAPTATION"]
        text = (self.tmp / pc.VOLUMES["PD-10"]).read_text(encoding="utf-8")
        manifest["volumes"]["PD-10"]["sections_sha256"] = hashlib.sha256(
            pc.section_text(text).encode("utf-8")).hexdigest()
        (self.tmp / pc.CANONICAL_MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
        self._refresh_construction_manifest()
        report = self._state()
        self.assertEqual([], [e for e in pc.verify(self.tmp)["errors"]], "the verifier agrees")
        c123 = self._criterion(report, "§12.3")
        self.assertFalse(c123["passes"])
        self.assertTrue(any("classification counts" in b for b in c123["blockers"]))

    def _refresh_construction_manifest(self):
        path = self.tmp / pc.MANIFEST
        self.saved.setdefault(path, path.read_bytes())
        data = json.loads(path.read_text(encoding="utf-8"))
        for cpid, rel in pc.VOLUMES.items():
            data["volumes"][cpid]["sha256"] = hashlib.sha256((self.tmp / rel).read_bytes()).hexdigest()
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_the_ownership_conflict_itself_is_named(self):
        self._apply_d2()
        path = f"{po.DIVISIONS_DIR}/PD-07-infrastructure-and-platform.md"
        self._edit(path, "## 1. Established", "## 1. Established\n\n- PD-07 owns Runtime.")
        blockers = self._criterion(self._state(), "§12.5")["blockers"]
        self.assertTrue(any(b.startswith("ownership conflicts") for b in blockers), blockers)

    def test_an_open_d2_item_keeps_it_not_closed_even_when_residency_is_closed(self):
        self._apply_d2()
        self._edit(po.REGISTER, "| **Closes** | `ESC-C7-01` · `FN-1` |", "| **Closes** | `ESC-C7-01` |")
        report = self._state()
        self.assertTrue(self._criterion(report, "§12.1")["passes"])
        self.assertEqual(["FN-1"], report["open_blocking_items"])
        self.assertEqual(cg.NOT_CLOSED, report["state"])

    def test_selections_count_only_when_decided_by_the_founder(self):
        text = (self.tmp / po.REGISTER).read_text(encoding="utf-8")
        block = text[text.index("### FD-PO-004 — Founder Decision"):]
        self._edit(po.REGISTER, block[:block.index("| **Decided by** | Founder |") + 28],
                   block[:block.index("| **Decided by** | Founder |")] + "| **Decided by** | Claude Code |")
        self.assertEqual({"D1": None, "D2": None, "D3": None, "D4": None}, self._state()["selections"])

    def test_a_coherence_reason_not_accepted_is_a_blocker(self):
        self._apply_d2()
        original = dict(cg.CLOSURE_CLASSIFICATION)
        cg.CLOSURE_CLASSIFICATION["G-02"] = (cg.CLASSIFIED, "test", "test")
        try:
            report = self._state()
        finally:
            cg.CLOSURE_CLASSIFICATION.clear()
            cg.CLOSURE_CLASSIFICATION.update(original)
        blockers = self._criterion(report, "§12.5")["blockers"]
        self.assertTrue(any(b.startswith("coherence: G-02 open") for b in blockers), blockers)

    def test_a_ceo_record_cannot_apply_d2(self):
        for n, slug in ((3, "pd-03-x"), (4, "pd-04-x")):
            base = self.tmp / f"docs/architecture/volume-{n}"
            self.created.append(base)
            (base / slug).mkdir(parents=True)
            (base / slug / "A1.md").write_text("# test\n", encoding="utf-8")
        self._append_register("### FDR-TEST-CEO — CEO Record · test\n\n| **Decided by** | Claude Code |\n"
                              "| **Closes** | `ESC-C7-01` · `FN-1` |")
        report = self._state()
        self.assertEqual(cg.NOT_CLOSED, report["state"])
        self.assertIn("ESC-C7-01", report["open_blocking_items"])


if __name__ == "__main__":
    unittest.main()
