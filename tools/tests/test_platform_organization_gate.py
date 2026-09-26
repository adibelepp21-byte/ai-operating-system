"""`ACT-CC-POST-P13-PLATFORM-ORG-001`: the Platform Organization gate.

The live tree is read only. Every negative control (`§45`, NC-01 … NC-15)
runs on a disposable copy of the repository, and the real tree is compared
before and after. Positive controls sit beside the negative ones, so a check
that refuses everything would fail them.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import certified_evidence_integrity as integrity
from tools import p12_certified_evidence_guard as guard
from tools import platform_organization_gate as po

REPO_ROOT = Path(__file__).resolve().parents[2]
ACTS = "docs/governance/acts"
DIV = po.DIVISIONS_DIR


def _tree(root: Path) -> dict:
    out = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for name in files:
            path = Path(base) / name
            out[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return out


class TheLiveState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report = po.evaluate()

    def _state(self, cpid):
        return self.report["divisions"][cpid]["state"]

    def test_the_outcome_is_founder_or_architect_decision_required(self):
        self.assertEqual(po.OUTCOME_D, self.report["outcome"])
        self.assertFalse(self.report["gate_passes"])

    def test_each_division_state(self):
        expected = {
            "PD-01": po.FOUNDER_DECISION, "PD-02": po.COMPLETE_RESIDUAL,
            "PD-03": po.FOUNDER_DECISION, "PD-04": po.FOUNDER_DECISION,
            **{f"PD-{n:02d}": po.BLOCKED for n in range(5, 11)},
        }
        self.assertEqual(expected, {c: self._state(c) for c in po.CPIDS})
        self.assertIn(po.ARCHITECT_DECISION, self.report["divisions"]["PD-01"]["also"])
        self.assertIn(po.CONFLICTED, self.report["divisions"]["PD-10"]["also"])

    def test_non_blocking_items_follow_their_sources(self):
        """`G-02` and `G-03` are "Blocking: NO" in the Systemic Gap Map, and the
        Founder ruled the bindings conditional-blocking in P12. They are open,
        and they are residual, not blockers."""
        blocking = {i["id"]: i["blocking"] for i in self.report["open_items"]}
        for identifier in ("G-02", "FDP-P10-001", "FDP-P10-002", "FDP-P10-003"):
            self.assertFalse(blocking[identifier], identifier)
        self.assertTrue(blocking["G-01"])
        self.assertTrue(blocking["ESC-C7-01"])
        self.assertIn("FDP-P10-001", self.report["divisions"]["PD-08"]["residual"])
        self.assertEqual((), self.report["divisions"]["PD-08"]["also"])

    def test_pd_02_is_complete_only_through_its_registered_contract(self):
        pd02 = self.report["divisions"]["PD-02"]
        self.assertIn("GDR-0026", pd02["reasons"][0])
        self.assertIn("GDR-0036", pd02["reasons"][0])
        self.assertIn("C6-A1", pd02["residual"])

    def test_scope_identity_and_the_ten_divisions(self):
        gate = {g["id"]: g for g in self.report["gate"]}
        self.assertEqual(po.PASS, gate["G1"]["status"])
        self.assertEqual(po.PARTIAL_GATE, gate["G2"]["status"])
        self.assertIn("G-02", gate["G2"]["evidence"])
        self.assertEqual(po.FAIL, gate["G10"]["status"])
        self.assertEqual(po.FAIL, gate["G14"]["status"])
        self.assertEqual(po.PASS, gate["G13"]["status"])

    def test_every_open_item_is_still_recorded_where_it_is_recorded(self):
        items = self.report["open_items"]
        self.assertEqual(len(po.OPEN_ITEMS), len(items))
        self.assertTrue(all(i["recorded"] for i in items), [i for i in items if not i["recorded"]])
        self.assertTrue(all(i["status"] == "OPEN" for i in items))

    def test_both_resident_volumes_verify(self):
        volumes = self.report["volume_integrity"]
        self.assertEqual((45, 45, True), (volumes["PD-01"]["verified"],
                                           volumes["PD-01"]["bodies"], volumes["PD-01"]["holds"]))
        self.assertEqual((50, 50, True), (volumes["PD-02"]["verified"],
                                           volumes["PD-02"]["bodies"], volumes["PD-02"]["holds"]))

    def test_ownership_has_no_conflict_and_implementation_scope_is_unknown(self):
        owners = self.report["ownership"]
        self.assertEqual({}, owners["conflicts"])
        self.assertEqual(("PD-05",), owners["claims"]["runtime"])
        self.assertEqual(("implementation",), owners["scope_unknown"])

    def test_it_decides_nothing(self):
        self.assertFalse(self.report["certifies"])
        self.assertFalse(self.report["grants_authority"])
        self.assertFalse(self.report["canonical"])
        self.assertTrue(self.report["governance"]["holds"])

    def test_it_writes_nothing(self):
        before, report = _tree(REPO_ROOT / "docs"), integrity.verify()
        po.evaluate()
        self.assertEqual(before, _tree(REPO_ROOT / "docs"))
        self.assertEqual(report, integrity.verify())
        self.assertEqual(frozenset({10, 11, 12, 13}), guard.certified_phases())


class _Copy(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name) / "repo"
        shutil.copytree(REPO_ROOT, self.repo, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.before = integrity.verify()

    def tearDown(self):
        self._tmp.cleanup()
        self.assertEqual(integrity.verify(), self.before, "a control changed the real tree")

    def _text(self, relative):
        return (self.repo / relative).read_text(encoding="utf-8")

    def _write(self, relative, text):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _register(self, text):
        self._write(po.REGISTER, self._text(po.REGISTER) + "\n" + text + "\n")

    def _decision(self, identifier, decided_by, closes):
        kind = {"Founder": "Founder Decision", "Architect": "Architect Decision"}.get(
            decided_by, "CEO Record")
        self._register(f"### {identifier} — {kind} · test\n\n| Field | Value |\n"
                       f"|---|---|\n| **Identifier** | `{identifier}` |\n"
                       f"| **Decided by** | {decided_by} |\n"
                       f"| **Closes** | {' · '.join(f'`{c}`' for c in closes)} |")

    def _eval(self):
        return po.evaluate(self.repo)

    def _item(self, report, identifier):
        (item,) = [i for i in report["open_items"] if i["id"] == identifier]
        return item["status"]


class GovernanceInvariants(_Copy):
    """NC-01 … NC-04 and NC-15: this Act cannot disturb them."""

    def test_the_copy_is_outcome_d(self):
        self.assertEqual(po.OUTCOME_D, self._eval()["outcome"])

    def test_nc01_creating_phase_14_fails(self):
        self._write(f"{ACTS}/FDR-89-TEST-PHASE-14.md", "# test\n\n1. FOUNDER DECISION\n\nAUTHORIZE PHASE 14\n")
        self._register("| FDR-89 | test |")
        report = self._eval()
        self.assertFalse(report["governance"]["holds"])
        self.assertEqual(po.OUTCOME_E, report["outcome"])

    def test_nc02_reopening_p13_fails(self):
        (self.repo / f"{ACTS}/FDR-G3-P13-CLOSURE-AND-TRANSITION-TO-GOVERNED-AIOS-OPERATION.md").unlink()
        report = self._eval()
        self.assertIn("P13 CLOSURE CLOSED", report["governance"]["failing"])
        self.assertEqual(po.OUTCOME_E, report["outcome"])

    def test_nc03_modifying_certified_architecture_fails(self):
        path = f"{DIV}/PD-05-runtime-and-execution.md"
        self._write(path, self._text(path) + "\nedited\n")
        report = self._eval()
        self.assertFalse(report["governance"]["certified_root_holds"])
        self.assertEqual(po.OUTCOME_E, report["outcome"])

    def test_nc04_an_automatic_certification_fails(self):
        self._write(f"{ACTS}/FDR-88-TEST-CERTIFY.md", "FOUNDER DECISION: CERTIFY P2.\n")
        self._register("| FDR-88 | test |")
        report = self._eval()
        self.assertFalse(report["governance"]["holds"])
        self.assertFalse(report["certifies"])

    def test_nc15_state_changing_authority_fails(self):
        path = "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
        text = self._text(path)
        self._write(path, text[:text.index("## 16. P13-ENV-02 Retirement Append")])
        report = self._eval()
        self.assertIn("STATE-CHANGING AUTHORITY NONE", report["governance"]["failing"])
        self.assertFalse(report["grants_authority"])


class NoFalseCompletion(_Copy):
    """NC-05 … NC-10, NC-14."""

    def _blind_copy(self, cpid="PD-05", name="runtime-and-execution"):
        source = self.repo / po.VOLUME_1
        target = f"docs/architecture/volume-{int(cpid[3:])}/pd-{cpid[3:]}-{name}"
        for body in sorted(source.glob("[A-E]*.md")):
            self._write(f"{target}/{body.name}",
                        body.read_text(encoding="utf-8").replace("PD-01", cpid))

    def test_nc05_a_blind_copy_of_pd_01_is_refused(self):
        self._blind_copy()
        report = self._eval()
        self.assertEqual(po.CONFLICTED, report["divisions"]["PD-05"]["state"])
        self.assertEqual(po.OUTCOME_E, report["outcome"])

    def test_nc05_positive_an_original_corpus_is_unknown_not_complete(self):
        self._write("docs/architecture/volume-5/pd-05-runtime-and-execution/A1.md",
                    "# A1 — Platform Identity\n\nPD-05 Runtime & Execution: an original body.\n")
        report = self._eval()
        self.assertEqual(po.UNKNOWN, report["divisions"]["PD-05"]["state"])
        self.assertEqual(po.OUTCOME_C, report["outcome"])

    def test_nc06_unknown_is_not_made_complete_by_the_record(self):
        path = f"{DIV}/PD-06-ai-engineering.md"
        text = self._text(path).replace("EVIDENCE-READY → **CONSTRUCTED (derived)**", "**COMPLETE**")
        self._write(path, text)
        ledger = self._text(po.LEDGER)
        self._write(po.LEDGER, ledger.replace("| ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |",
                                              "| ◆ | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ | ◆ |"))
        report = self._eval()
        self.assertEqual(po.BLOCKED, report["divisions"]["PD-06"]["state"])
        self.assertNotIn(report["outcome"], (po.OUTCOME_A, po.OUTCOME_B))

    def test_nc07_a_record_claiming_canonical_status_fails_governance(self):
        path = f"{DIV}/PD-07-infrastructure-and-platform.md"
        self._write(path, self._text(path).replace("**Status: DERIVED.**", "**Status: CANONICAL.**", 1))
        report = self._eval()
        (g12,) = [g for g in report["gate"] if g["id"] == "G12"]
        self.assertEqual(po.FAIL, g12["status"])
        self.assertIn("PD-07", g12["evidence"])

    def test_nc08_every_reserved_item_closed_still_is_not_complete(self):
        """With every open item closed by the Founder, divisions with no
        contract are INCOMPLETE, and the outcome is C, never A or B."""
        self._decision("FDR-87", "Founder", [i.identifier for i in po.OPEN_ITEMS])
        report = self._eval()
        self.assertTrue(all(i["status"].startswith("CLOSED") for i in report["open_items"]))
        self.assertEqual(po.INCOMPLETE, report["divisions"]["PD-05"]["state"])
        self.assertEqual(po.OUTCOME_C, report["outcome"])

    def test_nc08_closing_all_but_the_source_gap_leaves_it_blocked(self):
        self._decision("FDR-86", "Founder", [i.identifier for i in po.OPEN_ITEMS if i.identifier != "G-01"])
        report = self._eval()
        self.assertEqual(po.BLOCKED, report["divisions"]["PD-08"]["state"])
        self.assertNotIn(report["outcome"], (po.OUTCOME_A, po.OUTCOME_B))

    def test_nc09_two_divisions_owning_one_domain_is_a_conflict(self):
        path = f"{DIV}/PD-07-infrastructure-and-platform.md"
        text = self._text(path)
        self._write(path, text.replace("## 1. Established", "## 1. Established\n\n- PD-07 owns Runtime.", 1))
        report = self._eval()
        self.assertEqual({"runtime": ("PD-05", "PD-07")}, report["ownership"]["conflicts"])
        self.assertEqual(po.CONFLICTED, report["divisions"]["PD-05"]["state"])
        self.assertEqual(po.CONFLICTED, report["divisions"]["PD-07"]["state"])

    def test_nc10_a_business_department_is_not_a_platform_division(self):
        self._write(f"{DIV}/PD-11-finance.md",
                    "# PD-11 — Finance\n\n> **Status: DERIVED.**\n\n| | |\n|---|---|\n"
                    "| **CPID** | `PD-11` — test |\n| **Established name** | Finance |\n")
        report = self._eval()
        (g1,) = [g for g in report["gate"] if g["id"] == "G1"]
        self.assertEqual(po.FAIL, g1["status"])
        self.assertIn("PD-11", g1["evidence"])

    def test_nc14_deleting_a_gap_record_does_not_close_it(self):
        text = self._text(po.GAP_MAP)
        start = text.index("## G-01 —")
        self._write(po.GAP_MAP, text[:start] + text[text.index("## G-02 —"):])
        report = self._eval()
        (g01,) = [i for i in report["open_items"] if i["id"] == "G-01"]
        self.assertEqual(("OPEN", False), (g01["status"], g01["recorded"]))
        self.assertEqual(po.BLOCKED, report["divisions"]["PD-05"]["state"])
        self.assertEqual(po.OUTCOME_E, report["outcome"])

    def test_nc14_editing_a_pd_02_body_undoes_its_completion(self):
        path = f"{po.VOLUME_2}/C8.md"
        self._write(path, self._text(path) + "\nedited\n")
        report = self._eval()
        self.assertEqual(po.CONFLICTED, report["divisions"]["PD-02"]["state"])
        self.assertEqual(("C8.md",), report["volume_integrity"]["PD-02"]["faults"])

    def test_nc14_a_pd_01_change_with_no_authorized_act_is_refused(self):
        import json
        lineage = json.loads(self._text(po.LINEAGE))
        (body,) = [b for b in lineage["bodies"] if b["section"] == "A1"]
        body["changed_by"] = ["ACT-CC-UNKNOWN"]
        self._write(po.LINEAGE, json.dumps(lineage))
        report = self._eval()
        self.assertEqual(po.CONFLICTED, report["divisions"]["PD-01"]["state"])
        self.assertIn("A1.md: changed with no recorded authorized change",
                      report["volume_integrity"]["PD-01"]["faults"])

    def test_nc14_editing_a_pd_01_body_is_detected(self):
        path = f"{po.VOLUME_1}/B3.md"
        self._write(path, self._text(path) + "\nedited\n")
        report = self._eval()
        self.assertEqual(po.CONFLICTED, report["divisions"]["PD-01"]["state"])
        self.assertFalse(report["volume_integrity"]["PD-01"]["holds"])


class ReservedMattersCloseOnlyByTheirHolder(_Copy):
    """NC-11 … NC-13."""

    def test_nc11_an_unregistered_decision_closes_nothing(self):
        self._write(f"{ACTS}/FDR-85-TEST.md",
                    "### FDR-85 — Founder Decision · test\n\n| **Decided by** | Founder |\n"
                    "| **Closes** | `ESC-C7-01` |\n")
        self.assertEqual("OPEN", self._item(self._eval(), "ESC-C7-01"))

    def test_nc12_a_ceo_record_does_not_close_a_founder_matter(self):
        self._decision("FDR-84", "Claude Code", ["FDP-P10-001"])
        self.assertEqual("OPEN", self._item(self._eval(), "FDP-P10-001"))

    def test_nc12_positive_the_founder_closes_it(self):
        self._decision("FDR-83", "Founder", ["FDP-P10-001"])
        report = self._eval()
        self.assertEqual("CLOSED by FDR-83", self._item(report, "FDP-P10-001"))
        self.assertNotIn("FDP-P10-001", report["divisions"]["PD-08"]["residual"])

    def test_nc13_a_ceo_record_does_not_close_an_architect_matter(self):
        self._decision("FDR-82", "Claude Code", ["C6-A1", "G-10"])
        report = self._eval()
        self.assertEqual("OPEN", self._item(report, "C6-A1"))
        self.assertEqual("OPEN", self._item(report, "G-10"))

    def test_nc13_positive_the_architect_closes_an_architect_matter(self):
        self._decision("FDR-81", "Architect", ["G-10"])
        report = self._eval()
        self.assertEqual("CLOSED by FDR-81", self._item(report, "G-10"))
        self.assertNotIn(po.ARCHITECT_DECISION, report["divisions"]["PD-01"]["also"])

    def test_nc13_an_architect_cannot_close_a_founder_matter(self):
        self._decision("FDR-80", "Architect", ["ESC-C7-01"])
        self.assertEqual("OPEN", self._item(self._eval(), "ESC-C7-01"))


if __name__ == "__main__":
    unittest.main()
