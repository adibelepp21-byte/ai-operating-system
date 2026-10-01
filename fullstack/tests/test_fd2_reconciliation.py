"""FD-2 Authority Reconciliation Gate (Register §123): a reconciliation record only.

Guards MI §21: FD-2 is not recorded as ratified without evidence; nothing is
selected, recommended or authorized for implementation; the records audited for
an FD-2 dependency are unchanged; no FDP-012 is created.
"""

import hashlib
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RECORD = REPO_ROOT / "docs/fullstack/FD-2-AUTHORITY-RECONCILIATION-GATE.md"
REGISTER = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"


class TheReconciliationRecordCreatesNoAuthority(unittest.TestCase):

    # sha256 of each audited record as it stood when the gate ran; the gate
    # observes dependencies, it does not rewrite them (MI §12).
    AUDITED = {
        "docs/governance/acts/FDP-009-FS-10-PRODUCTION-AUTHORITY-AND-RELEASE-BOUNDARY.md":
            "799dd656eb86c7362da22f692030c3f5fcf4281fac0a37e5bf076e8eb5728139",
        "docs/governance/acts/FDP-010-FS-10-OPERATIONAL-ACCESS-ROLLBACK-GOVERNANCE-RECONCILIATION.md":
            "2875c521234c18596c4e36f41cc368eeb0be399c56c00b7f1afccd5212c26307",
        "docs/governance/acts/FDP-011-FS-10-ESC03-PER-SESSION-X2-OPERATIONAL-ACCESS.md":
            "e888b3acfea9dcb88d82ef4ec894aa138c1ff56741edaddc82b606077a8383f7",
        "docs/governance/acts/AD-FS10-ESC03-PRODUCTION-OPERATIONAL-EDGE-ACCESS-ARCHITECTURE-DECISION.md":
            "08693770c982eaf2014c2170797ee9786b547ed669f4390e27f71559facdcf96",
        "docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-004-FS-09-PRODUCTION-READINESS-MASTER-ACT.md":
            "a5c252fd0da329008065ee1c0ad7707fbf621d0860ffd03da89f469820e207a5",
        "docs/fullstack/FS-10-ESC03-ARCHITECTURE-DECISION.md":
            "7536513f085faa19aa39c0debde3ab80e21b1f6ddedb7ccbfc3a7c853255f6cf",
        "docs/fullstack/FS-10-ESC03-MI-S0-S1-RECORD.md":
            "f98f449ffc8d58a78c3ad88d99adb2d7255726f7c9c3112a71db5100464d2542",
        "docs/fullstack/FS-10-ESC-03-AUTHORITY-RESOLUTION.md":
            "99104e064f82a5875693bd2e2c1049ed509415ff990938e5864f7c5647a695d7",
        "docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md":
            "5cef394cbd421331155ea531ae304acbacbfa553544e6f31cf704f70f77707e1",
        "docs/fullstack/decision-packages/FS-DP-03-R3-ESC-03-OPERATIONAL-EDGE-ACCESS.md":
            "74e614878084c120fa90c367444e3de49f4b85b75407b129a3a05db8cc64c3ff",
        "docs/fullstack/FS-10-PROVIDER-CREDENTIAL-INJECTION-EVIDENCE.md":
            "64f07d66e10285df851c9180261ffd46ed0fecc61bf359c5a54f519a1061fa7d",
        "docs/fullstack/decision-packages/FS-10-PROVIDER-CREDENTIAL-INJECTION-FOUNDER-DECISION-PACKAGE.md":
            "9e9a2c8162dc1e3af1db05d5924193ed53ccfc92ff8ac1871088d60288a153e1",
        "docs/fullstack/FS-09-OPERATIONAL-OWNERSHIP.md":
            "eec7e5ebfbecab206a315f6f6683d60950b1c156bb6b2574f64bc1291e2efbe2",
        "docs/governance/AIOS_APPOINTMENT_REGISTER_v1.0.md":
            "b6dfcbad3f6f0101a1ff88fd6089af6d372d7b578fd028cabe1ac7b5094a83ff",
        "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md":
            "c470593e612de02b4375362305d6933bfd81a7492fbb87ce87306c2d7696b67e",
        "docs/constitution/engineering-constitution-v1.md":
            "b73723f8af91ef7a2b8794f5945808381a08a08806ad4f5dae4337d2760a25ab",    }

    def setUp(self):
        self.text = RECORD.read_text(encoding="utf-8")

    def test_final_state_is_b_and_fd2_is_not_recorded_as_ratified(self):
        self.assertIn("STATE B — FD-2 NOT RATIFIED / IMPLIED ONLY", self.text)
        final = self.text[self.text.index("## 20. Final reconciliation state"):]
        self.assertNotRegex(final, r"STATE [ACDEF] —(?! FD-2 RATIFIED AND)")
        self.assertNotRegex(self.text, r"(?i)FD-2[^.\n|]{0,40}\b(?<!not )(?<!NOT )ratified\b(?! /)")

    def test_lifecycle_records_no_approval_canonicalization_or_activation(self):
        life = self.text[self.text.index("## 8. FD-2 lifecycle"):self.text.index("## 9.")]
        for stage in ("Approved", "Canonicalized", "Activated", "Superseded / withdrawn"):
            row = next(line for line in life.splitlines() if line.startswith(f"| {stage} "))
            self.assertRegex(row, r"\| \*\*no\*\*", stage)

    def test_every_dependency_row_has_one_class(self):
        audit = self.text[self.text.index("## 9. Dependency audit"):self.text.index("## 10.")]
        rows = [line for line in audit.splitlines() if re.match(r"\| \d+[a-z]? \|", line)]
        self.assertGreaterEqual(len(rows), 14)
        for row in rows:
            self.assertRegex(row.split("|")[3], r"\*\*[A-E]\*\*", row)

    def test_no_selection_recommendation_or_implementation_authority(self):
        self.assertNotRegex(self.text, r"(?i)\b(recommend\w*|preferred|best|optimal|safest|obvious)\b")
        self.assertNotIn("IMPLEMENTATION AUTHORIZED", self.text)
        self.assertNotRegex(self.text, r"(?i)\b(is|was|are|were|been|be)\s+selected\b")
        self.assertNotRegex(self.text, r"(?<!UN)SELECTED")

    def test_audited_records_are_unchanged(self):
        for path, digest in self.AUDITED.items():
            self.assertEqual(digest, hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest(), path)

    def test_no_fdp012_and_the_register_says_no_new_authority(self):
        self.assertEqual([], sorted((REPO_ROOT / "docs/governance/acts").glob("FDP-012*")))
        register = REGISTER.read_text(encoding="utf-8")
        entry = register[register.index("## 123. FD-2 Authority Reconciliation Gate"):]
        self.assertIn("**RECONCILIATION RECORD — NO NEW AUTHORITY CREATED.**", entry)


if __name__ == "__main__":
    unittest.main()
