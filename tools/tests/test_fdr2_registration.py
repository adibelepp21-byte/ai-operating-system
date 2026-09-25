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
        """`FDR-1` → `FDR-6` certify nothing. `FDR-7` is the Founder's
        certification of P13, and it is the only `FDR` act the guard reads a
        certification from."""
        self.assertEqual(sentinel.certified_phases(), frozenset({10, 11, 12, 13}))
        self.assertEqual(sentinel.certification_anomalies(), ())
        from_fdr = {(phase, name) for phase, name in sentinel.certification_provenance()
                    if name.startswith("FDR-")}
        self.assertEqual({(13, "FDR-7-P13-FOUNDER-CERTIFICATION-AND-FINAL-SYSTEM-ACCEPTANCE.md")}, from_fdr)

    def test_the_phase_snapshot_is_not_rewritten_by_later_decisions(self):
        """P12 `§37`'s snapshot still says P13 AUTHORIZED: FALSE. `P13-018`
        authorizes *construction* with bounded scope and states no phase
        authorization, so nothing here may read it as one.

        `FDR-6` `FDQ-1` is a phase authorization. The current state is `True`
        and is cited to `FDR-6` only. The snapshot is kept as written and is
        reported as superseded."""
        self.assertIs(phases.state_of("P13").authorized, False)
        p13 = {s["entity"]: s for s in phases.current_states()}["P13"]
        self.assertIs(p13["authorized"], True)
        superseded = p13["superseded_by_authorization"]
        self.assertEqual(superseded["dimensions"], {"AUTHORIZED": False})
        self.assertTrue(superseded["superseded_by"].endswith(
            "FDR-6-P13-CERTIFICATION-GATE-FOUNDER-DECISION.md"))
        self.assertNotIn("P13-018", p13["authority_record"])

    def test_native_core_is_still_eleven(self):
        core = REPO_ROOT / "native_core/core"
        boundaries = [d for d in core.iterdir()
                      if d.is_dir() and not d.name.startswith("__")]
        self.assertEqual(len(boundaries), 11)

    def test_p13_code_exists_only_under_the_registered_construction_gate(self):
        """Pinned absent under FDR-2 (`D10`). Built after `P13-018` `D-1`, which
        the Register records; the pin now holds that order."""
        self.assertTrue((REPO_ROOT / "tools/p13/cycle.py").is_file())
        self.assertRegex(REGISTER.read_text(encoding="utf-8"),
                         r"### P13-018 — Founder Decision · P13 Construction Authority Gate")
        self.assertFalse((REPO_ROOT / "native_core/core/p13").exists())

    def test_the_p13_document_root_is_protected_once_certified(self):
        """Unprotected until `FDR-7` certified P13; protected from then on."""
        self.assertTrue(barrier.refuses(
            REPO_ROOT / "docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md"))

    def test_the_blueprint_and_gate_keep_their_text_and_record_the_decision(self):
        """Both said *not authorized* when written, and still do: that is their
        history. Each now also records `P13-018`, and neither claims more than
        bounded construction."""
        for path in (REPO_ROOT / "docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md",
                     REPO_ROOT / "docs/architecture/p13-preparation/"
                                 "P13-018-CONSTRUCTION-AUTHORITY-GATE.md"):
            with self.subTest(path.name):
                text = path.read_text(encoding="utf-8")
                self.assertTrue(re.search(r"not authorized", text, re.IGNORECASE))
                self.assertIn("APPROVED WITH BOUNDED INITIAL AUTHORITY", text)
                self.assertIn("acts/P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md",
                              text)


if __name__ == "__main__":
    unittest.main()
