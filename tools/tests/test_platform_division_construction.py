"""Tests for the PD-05 … PD-10 construction volumes (ACT-003 v1.1).

`TheLiveState` checks the repository as it is. `NegativeControls` mutate a
temporary copy of `docs/` and prove that the verifier catches each violation
v1.1 `§23` names (NC-01 … NC-20) and each construction rule the verifier
enforces. The real tree is never written.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import platform_division_construction as pc
from tools import platform_organization_gate as po

REPO_ROOT = Path(__file__).resolve().parents[2]
#: The certification record of FD-PO-004 D1-A: sections and classes as
#: certified. A change needs its own Founder instrument, which updates this pin.
CANONICAL_MANIFEST_SHA = "49f203785f895899418b2a81796bac00150e75da7041703cc10870cf12174e5d"
ACT_003 = ("docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003-PLATFORM-ORGANIZATION-"
           "CONSTRUCTION-AND-CANONICALIZATION.md")

#: NC-01, NC-02: the constitutional and frozen texts construction must not
#: touch. A change to one needs its own governance instrument, and that
#: instrument updates this pin.
PINNED = {
    "docs/constitution/engineering-constitution-v1.md":
        "b73723f8af91ef7a2b8794f5945808381a08a08806ad4f5dae4337d2760a25ab",
    "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md":
        "b8e7b8d105d93863c5489104d3ceb0247c81e04b31699f1c2e6ece881c9911ee",
    "docs/architecture/domain-model/canonical-domain-model-v1.md":
        "6e273f12f79c3b2f4103ee668f1ed52e1bdb320cfca5985a7251f65535c020f2",
    "docs/architecture/AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md":
        "5e50882efdb87d42e1df00a96b8a8a0fc2a7067e7cf60ec4eefa93f5be3fefd2",
}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _construction_files() -> list:
    return sorted((REPO_ROOT / pc.CONSTRUCTION_ROOT).rglob("*")) + [
        REPO_ROOT / "tools/platform_division_construction.py"]


class TheLiveState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.report = pc.verify()
        cls.gate = po.evaluate()

    def test_every_volume_verifies(self):
        self.assertEqual([], self.report["errors"])
        self.assertTrue(self.report["passes"])
        self.assertEqual({c: pc.CANONICAL_STATE for c in pc.VOLUMES}, self.report["state"])

    def test_the_certified_classification_is_the_founders(self):
        """FD-PO-004 §2 states the counts it certifies; §9 requires them kept."""
        manifest = json.loads((REPO_ROOT / pc.CANONICAL_MANIFEST).read_text(encoding="utf-8"))
        counts = {}
        for volume in manifest["volumes"].values():
            for _, cls in volume["classes"]:
                counts[cls] = counts.get(cls, 0) + 1
        self.assertEqual({pc.SOURCE_DERIVED: 29, pc.INHERITED: 6, pc.ADAPTATION: 14,
                          pc.RECONSTRUCTION: 11, pc.UNKNOWN: 7, pc.RESERVED: 23}, counts)
        self.assertEqual(CANONICAL_MANIFEST_SHA, _sha(REPO_ROOT / pc.CANONICAL_MANIFEST))

    def test_every_volume_carries_all_eleven_dimensions(self):
        for cpid, volume in self.report["volumes"].items():
            self.assertEqual(list(pc.DIMENSIONS), volume["dimensions"], cpid)

    def test_every_section_has_a_class(self):
        for cpid, volume in self.report["volumes"].items():
            self.assertEqual(volume["sections"], sum(volume["classes"].values()), cpid)

    def test_reconciliation_passes(self):
        self.assertTrue(self.report["reconciliation"]["passes"])
        self.assertGreaterEqual(len(self.report["reconciliation"]["checks"]), 14)

    def test_every_reservation_is_still_recorded(self):
        missing = [r for r, v in pc.reservations().items() if not v["recorded"]]
        self.assertEqual([], missing)

    def test_the_gate_reports_the_certified_baseline(self):
        self.assertTrue(self.gate["construction"]["passes"])
        self.assertTrue(self.gate["construction"]["canonical"])
        self.assertEqual("FD-PO-004", self.gate["construction"]["certified_by"])
        self.assertEqual(po.OUTCOME_C, self.gate["outcome"])

    # NC-01, NC-02
    def test_nc01_nc02_constitutional_and_frozen_texts_unchanged(self):
        for path, sha in PINNED.items():
            self.assertEqual(sha, _sha(REPO_ROOT / path), path)

    # NC-03
    def test_nc03_reserved_items_open_unless_the_founder_closed_them(self):
        decided = {"G-01": "FD-PO-004", "FDP-P10-001": "FD-PO-004", "FDP-P10-002": "FD-PO-004",
                   "ESC-C7-01": "FD-PO-005"}
        for item in po.open_items():
            expected = f"CLOSED by {decided[item['id']]}" if item["id"] in decided else "OPEN"
            self.assertEqual(expected, item["status"], item["id"])
            self.assertTrue(item["recorded"], item["id"])

    # NC-04, NC-18
    def test_nc04_nc18_construction_cites_a_registered_founder_authorization(self):
        register = (REPO_ROOT / po.REGISTER).read_text(encoding="utf-8")
        self.assertIn(f"### {pc.AUTHORIZATION} — Founder Decision", register)
        entry = po._entry(register, pc.AUTHORIZATION)
        self.assertTrue(po._decided_by(entry, "Founder"))

    # NC-05, NC-06
    def test_nc05_nc06_construction_manufactures_no_decision(self):
        for path in _construction_files():
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, r"— (?:Founder|Architect) Decision", path.name)
                self.assertNotIn("**Decided by**", text, path.name)
        adr = (REPO_ROOT / "docs/architecture/adr/decisions/ADR-0029.md").read_text(encoding="utf-8")
        self.assertIn("- **Status:** **Proposed**", adr)

    # NC-11, NC-12, NC-13
    def test_nc11_nc12_nc13_frozen_divisions_are_preserved(self):
        integrity = po.volume_integrity()
        for cpid, bodies in (("PD-01", 45), ("PD-02", 50)):
            self.assertTrue(integrity[cpid]["holds"], cpid)
            self.assertEqual(bodies, integrity[cpid]["verified"], cpid)
        for volume in (po.VOLUME_1, po.VOLUME_2):
            self.assertEqual([], sorted((REPO_ROOT / volume).glob("[F-H][0-9]*.md")), volume)

    # NC-14
    def test_nc14_no_pd03_or_pd04_source_invented(self):
        """Volumes 3 and 4 are resident only as received (FD-PO-004 D2-A): every
        byte is the transmitted one, and the totals are the certified ones."""
        integrity = po.volume_integrity()
        for cpid, total in (("PD-03", 3704607), ("PD-04", 1508896)):
            self.assertTrue(integrity[cpid]["holds"], cpid)
            receipt = json.loads((REPO_ROOT / po.RECEIVED_VOLUMES[cpid] /
                                  "RECEIPT-MANIFEST.json").read_text(encoding="utf-8"))
            self.assertEqual(total, receipt["total_bytes"])
            self.assertEqual(total, receipt["certified_total_bytes"])
        self.assertEqual({"PD-03", "PD-04"}, set(po.resident_corpora()))

    # NC-15
    def test_nc15_no_constructed_volume_in_the_resident_namespace(self):
        for n in range(5, 11):
            self.assertFalse((REPO_ROOT / f"docs/architecture/volume-{n}").exists())

    # NC-16, NC-17, NC-19
    def test_nc16_nc17_nc19_canonical_only_by_the_founder_and_not_frozen_or_active(self):
        self.assertTrue(self.report["canonical"])
        self.assertEqual("FD-PO-004", self.report["closing_decisions"]["G-01"])
        self.assertFalse(self.report["certifies"])
        self.assertFalse(self.report["grants_authority"])
        for cpid in pc.VOLUMES:
            self.assertEqual(po.INCOMPLETE, self.gate["divisions"][cpid]["state"], cpid)
            header = pc.header((REPO_ROOT / pc.VOLUMES[cpid]).read_text(encoding="utf-8"))
            self.assertEqual(("NO", "NO"), (header["Frozen"], header["Activated"]), cpid)

    # NC-20
    def test_nc20_no_phase_14_and_p13_closure_holds(self):
        self.assertTrue(self.gate["governance"]["holds"])
        for path in _construction_files():
            if path.is_file():
                self.assertNotRegex(path.read_text(encoding="utf-8"), r"\bP14\b|Phase 14", path.name)


class NegativeControls(unittest.TestCase):
    """Each control mutates one file in a copy and expects the verifier to fail."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="pdc-"))
        shutil.copytree(REPO_ROOT / "docs", cls.tmp / "docs")
        cls.before = {p: _sha(p) for p in _construction_files() if p.is_file()}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)
        after = {p: _sha(p) for p in _construction_files() if p.is_file()}
        assert after == cls.before, "a control changed the real tree"

    def setUp(self):
        self.saved = {}

    def tearDown(self):
        for path, data in self.saved.items():
            if data is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(data)

    def _edit(self, relative: str, old: str, new: str, count: int = 1) -> None:
        path = self.tmp / relative
        data = path.read_bytes()
        self.saved.setdefault(path, data)
        text = data.decode("utf-8")
        self.assertIn(old, text, f"control fixture drifted: {old[:50]!r}")
        path.write_text(text.replace(old, new, count), encoding="utf-8")
        if relative in pc.VOLUMES.values():
            self._refresh_manifest()

    def _refresh_manifest(self) -> None:
        """Re-record bytes, so that a control isolates its own rule."""
        manifest = self.tmp / pc.MANIFEST
        self.saved.setdefault(manifest, manifest.read_bytes())
        data = json.loads(manifest.read_text(encoding="utf-8"))
        for cpid, path in pc.VOLUMES.items():
            data["volumes"][cpid]["sha256"] = _sha(self.tmp / path)
        manifest.write_text(json.dumps(data), encoding="utf-8")

    def _fails(self, fragment: str) -> None:
        report = pc.verify(self.tmp)
        self.assertFalse(report["passes"])
        self.assertTrue(any(fragment in e for e in report["errors"]),
                        f"expected {fragment!r} in {report['errors']}")

    def test_the_copy_verifies_before_any_control(self):
        self.assertTrue(pc.verify(self.tmp)["passes"])

    # NC-07: unknown → fact
    def test_nc07_unknown_upgraded_to_source_derived_without_source(self):
        self._edit(pc.VOLUMES["PD-10"], "**Dimension:** Authority · **Class:** UNKNOWN",
                   "**Dimension:** Authority · **Class:** SOURCE-DERIVED")
        self._fails("SOURCE-DERIVED without a Source")

    def test_nc07_unknown_that_states_nothing_unknown(self):
        self._edit(pc.VOLUMES["PD-10"], "- Unknown: any authority held by PD-10\n", "")
        self._fails("UNKNOWN states nothing unknown")

    # NC-08: proposal → canonical truth
    def _without_fd_po_004_closes(self):
        self._edit(po.REGISTER, "| **Closes** | `G-01` · `FDP-P10-001` · `FDP-P10-002` |\n", "")

    def test_nc08_canonical_header_without_the_founder_decision(self):
        self._without_fd_po_004_closes()
        self._fails("header Canonical must be 'NO'")
        self._fails("claims certification without a registered Founder decision")

    def test_nc08_positive_the_decision_makes_the_header_valid(self):
        report = pc.verify(self.tmp)
        self.assertTrue(report["passes"])
        self.assertEqual({c: pc.CANONICAL_STATE for c in pc.VOLUMES}, report["state"])

    def test_certified_sections_changed_after_certification(self):
        self._edit(pc.VOLUMES["PD-06"], "AI Engineering evolves by implementing",
                   "AI Engineering evolves quickly by implementing")
        self._fails("certified sections changed after certification")

    def test_certified_class_changed(self):
        self._edit(pc.VOLUMES["PD-07"], "**Dimension:** Capability · **Class:** BOUNDED-RECONSTRUCTION",
                   "**Dimension:** Capability · **Class:** DOMAIN-ADAPTATION")
        self._fails("differs from its certified class")

    def test_certified_by_row_removed(self):
        text = (self.tmp / pc.VOLUMES["PD-09"]).read_text(encoding="utf-8")
        row = next(l for l in text.splitlines() if l.startswith("| **Certified by** |"))
        self._edit(pc.VOLUMES["PD-09"], row + "\n", "")
        self._fails("Certified by does not cite FD-PO-004")

    def test_binding_declared_without_the_founder_decision(self):
        self._without_fd_po_004_closes()
        self._fails("declares FDP-P10-001 bound without a registered Founder decision")

    def test_binding_decided_but_not_recorded(self):
        self._edit(pc.VOLUMES["PD-09"], "Quality authority → PD-09: **BOUND** by `FD-PO-004` D4-A",
                   "Quality authority → PD-09: pending")
        self._fails("does not record FDP-P10-002 as bound by FD-PO-004")

    def test_nc08_canonical_status_asserted_in_text(self):
        self._edit(pc.VOLUMES["PD-06"], "# Part A — Identity & Mandate",
                   "Status: CANONICAL\n\n# Part A — Identity & Mandate")
        self._fails("canonical status claimed")

    # NC-09: roadmap → resident source
    def test_nc09_act_003_list_cited_as_source(self):
        self._edit(pc.VOLUMES["PD-07"], f"- Reference: `{ACT_003}` — \"C3 Compute Architecture\"",
                   f"- Source: `{ACT_003}` — \"C3 Compute Architecture\"")
        self._fails("roadmap or derived material, not source")

    def test_nc09_derived_division_record_cited_as_source(self):
        self._edit(pc.VOLUMES["PD-05"], "- Source: `docs/architecture/volume-2/pd-02-architecture-office/B7.md` — \"PD-05 owns Runtime.\"",
                   "- Source: `docs/architecture/platform-organization/divisions/PD-05-runtime-and-execution.md` — \"PD-05 owns Runtime\"")
        self._fails("roadmap or derived material, not source")

    # NC-10: reference pattern → domain content
    def test_nc10_frozen_pd01_line_copied(self):
        line = next(l for l in (self.tmp / po.VOLUME_1 / "A1.md").read_text(encoding="utf-8").splitlines()
                    if len(" ".join(l.split())) >= 60)
        self._edit(pc.VOLUMES["PD-09"], "# Part B — Organization & Capability",
                   f"{line}\n\n# Part B — Organization & Capability")
        self._fails("copied from frozen PD-01")

    # NC-15
    def test_nc15_volume_placed_in_resident_namespace(self):
        target = self.tmp / "docs/architecture/volume-5/pd-05-runtime-and-execution"
        target.mkdir(parents=True)
        self.saved[target / "VOLUME.md"] = None
        (target / "VOLUME.md").write_text("x", encoding="utf-8")
        try:
            self._fails("resident-corpus namespace")
        finally:
            shutil.rmtree(self.tmp / "docs/architecture/volume-5")
            self.saved.pop(target / "VOLUME.md")

    # NC-18: preparation → authorization
    def test_nc18_authority_row_without_the_authorizing_decision(self):
        self._edit(pc.VOLUMES["PD-08"], "authorized for execution by `FD-PO-003-01`",
                   "prepared for execution")
        self._fails("does not cite the authorizing decision")

    # NC-19: activation
    def test_nc19_volume_declares_itself_activated(self):
        self._edit(pc.VOLUMES["PD-09"], "| **Activated** | NO |", "| **Activated** | YES |")
        self._fails("header Activated")

    # Reserved bindings (FDP-P10-001/002/003, G-02, G-10)
    def test_security_owner_bound_to_pd08(self):
        self._edit(pc.VOLUMES["PD-08"], "## A1. Identity", "PD-08 is the Security Owner.\n\n## A1. Identity")
        self._fails("Security Owner bound to PD-08")

    def test_quality_authority_bound_to_pd09(self):
        self._edit(pc.VOLUMES["PD-09"], "## A1. Identity", "PD-09 is the Quality Authority.\n\n## A1. Identity")
        self._fails("Quality authority bound to PD-09")

    def test_governance_authority_bound_to_pd03(self):
        self._edit(pc.VOLUMES["PD-08"], "## A1. Identity", "PD-03 holds the Governance Authority.\n\n## A1. Identity")
        self._fails("Governance Authority bound to PD-03")

    def test_pd10_name_declared(self):
        self._edit(pc.VOLUMES["PD-10"], "| **Name** | held open — `G-02` (see A1) |",
                   "| **Name** | Developer Experience |")
        self._fails("PD-10 name must be held open")

    def test_sub_division_introduced(self):
        self._edit(pc.VOLUMES["PD-05"], "## B1. Capability", "## B1. Capability\n\nSub Division RD-01 owns hosting.")
        self._fails("Sub Division")

    def test_division_bound_to_native_core(self):
        self._edit(pc.VOLUMES["PD-05"], "## B1. Capability", "PD-05 owns `native_core/core/runtime`.\n\n## B1. Capability")
        self._fails("implementation boundary")

    def test_authority_collision(self):
        self._edit(pc.VOLUMES["PD-06"], "## B1. Capability", "PD-06 holds the Architecture Authority.\n\n## B1. Capability")
        self._fails("authority collision")

    # Evidence rules
    def test_quotation_not_in_its_source(self):
        self._edit(pc.VOLUMES["PD-05"], "B7.md` — \"PD-05 owns Runtime.\"",
                   "B7.md` — \"PD-05 owns Runtime and Execution.\"")
        self._fails("Source not found")

    def test_source_text_removed_from_the_cited_file(self):
        self._edit("docs/architecture/volume-2/pd-02-architecture-office/C8.md",
                   "PD-07 tetap memiliki ownership atas Infrastructure.", "PD-07 infrastructure.")
        self._fails("Source not found")

    def test_reservation_no_longer_recorded(self):
        self._edit("docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                   "## 10. Deferred Architecture (Architect Reserved)", "## 10. Deferred Architecture")
        self._fails("no longer recorded")

    def test_unrecorded_reservation_named(self):
        self._edit(pc.VOLUMES["PD-06"], "- Reserved: DM-8, G-10", "- Reserved: DM-8, G-99")
        self._fails("reservation G-99 is not recorded anywhere")

    def test_reserved_section_names_no_reservation(self):
        self._edit(pc.VOLUMES["PD-07"], "No internal unit is constructed. The Spine is three levels (`DM-8`), and\n"
                   "internal Capability ownership is open (`G-10`). The B1 areas are work areas\nonly.\n\n- Reserved: DM-8, G-10",
                   "No internal unit is constructed.")
        self._fails("RESERVED-DECISION names no reservation")

    def test_class_outside_the_vocabulary(self):
        self._edit(pc.VOLUMES["PD-09"], "**Dimension:** Lifecycle · **Class:** SOURCE-DERIVED",
                   "**Dimension:** Lifecycle · **Class:** ESTABLISHED")
        self._fails("not in the v1.1 §10 vocabulary")

    def test_dimension_missing(self):
        self._edit(pc.VOLUMES["PD-06"], "**Dimension:** Evolution · **Class:** DOMAIN-ADAPTATION",
                   "**Dimension:** — · **Class:** DOMAIN-ADAPTATION")
        self._fails("dimensions missing: Evolution")

    def test_bytes_differ_from_the_manifest(self):
        path = self.tmp / pc.VOLUMES["PD-05"]
        self.saved.setdefault(path, path.read_bytes())
        path.write_bytes(path.read_bytes() + b"\n")
        self._fails("do not match the manifest")

    # Cross-PD reconciliation (v1.1 §21)
    def test_reserved_binding_downgraded(self):
        self._edit(pc.VOLUMES["PD-08"], "**Dimension:** Authority · **Class:** RESERVED-DECISION",
                   "**Dimension:** Authority · **Class:** DOMAIN-ADAPTATION")
        self._fails("reserved binding kept reserved: PD-08 A3")

    def test_declared_edge_dropped(self):
        self._edit(pc.VOLUMES["PD-05"], "`X-05`", "X-05", count=5)
        self._fails("declared edge carried as undefined: X-05")

    def test_ownership_collision(self):
        self._edit(pc.VOLUMES["PD-06"], "- Source: `docs/architecture/volume-2/pd-02-architecture-office/B4.md` — \"PD-06 owns implementation.\"",
                   "- Source: `docs/architecture/volume-2/pd-02-architecture-office/B7.md` — \"PD-05 owns Runtime.\"")
        self._fails("cites PD-05's ownership")


if __name__ == "__main__":
    unittest.main()
