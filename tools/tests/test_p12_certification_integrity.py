"""`GOAL-V2-002` — P12 certification state and certified-evidence integrity.

These tests hold the relationships the Goal requires, each against the
resident tree and each shown able to fail:

```text
FD-P12-006 (decision) → Register §15 (resolution) → guard (enforcement)
                       → phase reader / self-model (representation)
                       → manifest (detection) · live root (lifecycle)
```
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tools import p12_certified_evidence_guard as sentinel
from tools import p12_certified_evidence_manifest as manifest
from tools import p12_phase_authorization as phases
from tools import p12_runtime_observation as obs

REPO_ROOT = Path(__file__).resolve().parents[2]


class TheDecisionFieldFormIsRecognised(unittest.TestCase):
    """The guard must read the certification the way `FD-P12-006` writes it,
    and must not read a condition as a decision."""

    def _certified(self, body: str) -> frozenset:
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp) / "acts"
            acts.mkdir()
            (acts / "FD-P77-001-X.md").write_text(body, encoding="utf-8")
            register = Path(tmp) / "register.md"
            register.write_text("`FD-P77-001` issued", encoding="utf-8")
            return sentinel.certified_phases(acts, register)

    def test_the_decision_field_certifies(self):
        self.assertIn(77, self._certified(
            "FOUNDER DECISION:\nP77 CERTIFICATION = CERTIFY\n"))

    def test_a_conditional_equation_does_not_certify(self):
        """`FD-P12-006 §21`: *"Certification may be marked: P12 CERTIFIED =
        YES only if …"*. A condition is not a decision."""
        self.assertNotIn(77, self._certified(
            "Certification may be marked:\n\nP77 CERTIFIED = YES\n\nonly if:\n"))

    def test_the_equation_without_the_decision_label_does_not_certify(self):
        self.assertNotIn(77, self._certified("P77 CERTIFICATION = CERTIFY\n"))

    def test_an_unregistered_decision_field_is_rejected(self):
        """`FD-P12-004`: resolution against the Register is still required."""
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp) / "acts"
            acts.mkdir()
            (acts / "FD-P77-001-X.md").write_text(
                "FOUNDER DECISION:\nP77 CERTIFICATION = CERTIFY\n",
                encoding="utf-8")
            register = Path(tmp) / "register.md"
            register.write_text("nothing recorded", encoding="utf-8")
            self.assertNotIn(77, sentinel.certified_phases(acts, register))


class ObservationsAreLiveAndCertifiedObservationsAreHistory(unittest.TestCase):

    def test_the_live_root_is_outside_every_phase_directory(self):
        relative = obs.OBSERVATION_ROOT.relative_to(obs.REPO_ROOT).as_posix()
        self.assertFalse(relative.startswith("docs/architecture/p"))
        self.assertFalse(sentinel.is_protected(obs.OBSERVATION_ROOT / "x.json"))

    def test_publishing_into_the_certified_root_is_refused(self):
        # The precondition is asserted first, and the publish is attempted only
        # when it holds. With a broken guard, this test must fail **without
        # writing**. An earlier version called `publish` unconditionally, and a
        # mutation run that disabled P12 recognition wrote a probe file into
        # certified evidence. The manifest control caught it (`GOAL-V2-002`
        # record, X-3).
        probe = obs.CERTIFIED_OBSERVATION_ROOT / "probe.observation.json"
        self.assertTrue(sentinel.is_protected(probe),
                        "the certified observation root is not protected")
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            obs.publish("probe", "RuntimeState.STOPPED",
                        root=obs.CERTIFIED_OBSERVATION_ROOT)
        self.assertFalse(probe.exists())

    def test_the_default_view_reads_certified_history_with_its_origin(self):
        found = {o.runtime_id: o for o in obs.observations(obs.OBSERVATION_ROOT)}
        self.assertIn("p12-live-verification-runtime", found)
        self.assertEqual(found["p12-live-verification-runtime"].origin,
                         obs.CERTIFIED_ORIGIN)

    def test_a_live_record_supersedes_a_certified_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            live, certified = Path(tmp) / "live", Path(tmp) / "certified"
            certified.mkdir()
            (certified / "r.observation.json").write_text(
                '{"runtime_id": "r", "state": "RuntimeState.STOPPED", '
                '"observed_at": "2026-09-18T00:00:00+00:00", "pid": 1}',
                encoding="utf-8")
            saved = (obs.OBSERVATION_ROOT, obs.CERTIFIED_OBSERVATION_ROOT,
                     obs._LIVE_DEFAULT)
            try:
                obs.CERTIFIED_OBSERVATION_ROOT = certified
                obs._LIVE_DEFAULT = live
                obs.publish("r", "RuntimeState.RUNNING", root=live)
                found = obs.observations(
                    live, now=datetime.now(timezone.utc))
            finally:
                (obs.OBSERVATION_ROOT, obs.CERTIFIED_OBSERVATION_ROOT,
                 obs._LIVE_DEFAULT) = saved
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].origin, obs.LIVE_ORIGIN)
        self.assertEqual(found[0].state, "RuntimeState.RUNNING")

    def test_an_isolated_root_is_read_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(obs.observations(Path(tmp)), ())


class TheResidentWorkPathCannotWriteCertifiedStores(unittest.TestCase):

    def test_a_run_aimed_at_the_certified_stores_is_refused_before_writing(self):
        """`D.1` / `B-02`: the corpus-health run is refused whole, and leaves
        certified evidence untouched."""
        import aios_corpus_health_run as work
        from tools.p12_trace_registry import STORE_ROOT
        # Same discipline as above. Without the precondition, a broken guard
        # lets `run()` append to the certified trace store. A mutation run did
        # exactly that, and the manifest control caught it (record, X-4).
        for target in (STORE_ROOT / work.WORKFLOW_KEY, work.KNOWLEDGE_STORE_ROOT):
            self.assertTrue(sentinel.is_protected(target),
                            f"{target} is not protected; refusing to run")
        before = manifest.verify()
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            work.run()
        self.assertEqual(manifest.verify(), before)

    def test_its_observation_root_is_a_parameter(self):
        import inspect
        import aios_corpus_health_run as work
        self.assertIn("observation_root", inspect.signature(work.run).parameters)


class CertifiedEvidenceIsIntact(unittest.TestCase):

    def test_every_certified_p12_file_holds_its_certified_bytes(self):
        """Outcome control. Whatever wrote, however it wrote, a change to
        certified P12 evidence fails here, on every run of the suite."""
        result = manifest.verify()
        self.assertEqual(result.modified, ())
        self.assertEqual(result.missing, ())
        self.assertEqual(len(result.intact), 121)

    def test_the_manifest_is_the_certified_commit_not_a_claim(self):
        record = manifest.load()
        rebuilt = manifest.from_commit(record["certified_commit"])
        if rebuilt is None:
            self.skipTest("certified commit not present in this clone")
        self.assertEqual(rebuilt, record["files"])

    def test_the_manifest_names_the_registered_certifying_instrument(self):
        record = manifest.load()
        self.assertTrue((REPO_ROOT / record["certifying_instrument"]).is_file())
        self.assertIn(Path(record["certifying_instrument"]).name,
                      dict(sentinel.certification_provenance()).values())

    def test_nothing_new_has_been_written_into_the_certified_root(self):
        """Additions are not certified evidence, but a new file inside the
        certified root is still a write into it. The resident stores that
        Native Core backends write (trace, knowledge) are invisible to the
        static writer check, so this is where such a write surfaces. The one
        legitimate addition is the certification handoff record, which was
        committed after `6968c6e`. Any other addition fails here."""
        self.assertEqual(manifest.verify().additions, (
            "docs/architecture/p12/AIOS-P12-FINAL-CERTIFICATION-AND-P13-"
            "TRANSITION-HANDOFF-RECORD.md",))

    def test_the_handoff_record_is_reported_as_an_addition_not_evidence(self):
        self.assertIn(
            "docs/architecture/p12/AIOS-P12-FINAL-CERTIFICATION-AND-P13-"
            "TRANSITION-HANDOFF-RECORD.md", manifest.verify().additions)


class ThePhaseStateNoLongerContradictsTheCertification(unittest.TestCase):

    def test_p12_is_reported_certified_by_its_instrument(self):
        certified = phases.certifications()
        self.assertTrue(certified["resolved"])
        self.assertTrue(certified["phases"]["P12"]["instrument"].endswith(
            "FD-P12-006-P12-CERTIFICATION-AND-LIVE-VERIFICATION.md"))

    def test_the_entry_snapshot_false_values_are_superseded_not_reported(self):
        p12 = {s["entity"]: s for s in phases.current_states()}["P12"]
        self.assertNotIn("CERTIFIED", p12["dimensions"])
        self.assertIs(False, p12["superseded_by_certification"]
                      ["dimensions"]["CERTIFIED"])
        self.assertIs(True, p12["dimensions"]["AUTHORIZED"])

    def test_the_raw_snapshot_is_preserved_as_history(self):
        """Historical truth is kept. `phase_states` still reads `§37` as
        written."""
        self.assertIs(False, phases.state_of("P12").dimensions["CERTIFIED"])

    def test_p13_is_not_touched(self):
        p13 = {s["entity"]: s for s in phases.current_states()}["P13"]
        self.assertIs(False, p13["authorized"])
        self.assertNotIn("superseded_by_certification", p13)

    def test_the_self_model_carries_both(self):
        from tools import p12_self_model as model
        reported = model.authority().value["phase_authorization"]
        self.assertIn("P12", reported["certification"]["phases"])
        self.assertNotIn("CERTIFIED", reported["states"]["P12"]["dimensions"])

    def test_the_self_model_and_the_guard_agree(self):
        certified = {int(k[1:]) for k in phases.certifications()["phases"]}
        self.assertEqual(certified, set(sentinel.certified_phases()))


if __name__ == "__main__":
    unittest.main()
