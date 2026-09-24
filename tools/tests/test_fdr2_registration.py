"""`FDR-2` registration — held as state, so that any drift is noticed.

FDR-2 closes `GAP-0001`/`0002`/`0004` *"subject to canonical registration"*.
These tests hold that the registration is real (the text is verbatim, and
its hash is in the Register), that the system can see it, and that it
conferred nothing FDR-2 withheld: no construction authorization, no
certification, no twelfth boundary.
"""

from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

from tools import certified_write_barrier as barrier
from tools import p12_certified_evidence_guard as sentinel
from tools import p12_phase_authorization as phases
from tools import p12_self_model as model
from tools.governance_index import identifiers_in

REPO_ROOT = Path(__file__).resolve().parents[2]
ACTS = REPO_ROOT / "docs/governance/acts"
REGISTER = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
FDR1 = ACTS / "FDR-1-FOUNDER-REVIEW-AND-DISPOSITION-OF-P13-BLUEPRINT-V0-4.md"
FDR2 = ACTS / "FDR-2-P13-DEFINITION-BOUNDARY-AUTONOMY-AND-EXIT-CONTRACT.md"


def _content_sha(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    body = text.split("````text\n", 1)[1].rsplit("\n````", 1)[0]
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


class TheRegistrationIsRealAndVerbatim(unittest.TestCase):

    def test_each_record_hash_is_the_one_the_register_records(self):
        register = REGISTER.read_text(encoding="utf-8")
        for path, prefix in ((FDR1, "286613a3e1b249f3"), (FDR2, "edb5e2fd7055b641")):
            with self.subTest(path.name):
                self.assertTrue(_content_sha(path).startswith(prefix))
                self.assertIn(prefix, register)

    def test_the_register_carries_the_canonical_definition_verbatim(self):
        definition = ("P13 is the Super Intelligence Ecosystem layer of AIOS in "
                      "which AIOS develops the capability to understand its own "
                      "relevant system state")
        # Both documents wrap lines, so compare with whitespace normalized.
        for path in (FDR2, REGISTER):
            with self.subTest(path.name):
                self.assertIn(definition, re.sub(r"\s+", " ", path.read_text(
                    encoding="utf-8")))


class TheSystemCanSeeTheFounderDecisions(unittest.TestCase):

    def test_the_index_recognizes_founder_decision_records_and_goals(self):
        found = identifiers_in("FDR-2 · GOAL-V2-005 · FD-P13-005 · FDR-1 §3")
        for identifier in ("FDR-2", "GOAL-V2-005", "FD-P13-005", "FDR-1"):
            self.assertIn(identifier, found)

    def test_the_self_model_lists_fdr_1_and_fdr_2_as_decisions(self):
        identifiers = model.decisions().value["identifiers"]
        self.assertIn("FDR-1", identifiers)
        self.assertIn("FDR-2", identifiers)
        self.assertFalse(any(i.startswith("GOAL-") for i in identifiers),
                         "a Goal is an instrument, not a decision")


class FDR2ConferredNothingItWithheld(unittest.TestCase):

    def test_no_certification_is_read_from_the_fdr_acts(self):
        self.assertEqual(sentinel.certified_phases(), frozenset({10, 11, 12}))
        self.assertEqual(sentinel.certification_anomalies(), ())

    def test_p13_is_still_not_authorized_for_construction(self):
        p13 = {s["entity"]: s for s in phases.current_states()}["P13"]
        self.assertIs(p13["authorized"], False)

    def test_native_core_is_still_eleven(self):
        core = REPO_ROOT / "native_core/core"
        boundaries = [d for d in core.iterdir()
                      if d.is_dir() and not d.name.startswith("__")]
        self.assertEqual(len(boundaries), 11)

    def test_no_p13_code_exists(self):
        self.assertFalse((REPO_ROOT / "tools/p13").exists())
        self.assertFalse((REPO_ROOT / "docs/operations/p13").exists())

    def test_the_p13_document_root_is_not_protected_as_certified(self):
        self.assertFalse(barrier.refuses(
            REPO_ROOT / "docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md"))

    def test_the_blueprint_and_gate_both_say_construction_is_not_authorized(self):
        for path in (REPO_ROOT / "docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md",
                     REPO_ROOT / "docs/architecture/p13-preparation/"
                                 "P13-018-CONSTRUCTION-AUTHORITY-GATE.md"):
            with self.subTest(path.name):
                self.assertTrue(re.search(r"not authorized", path.read_text(
                    encoding="utf-8"), re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
