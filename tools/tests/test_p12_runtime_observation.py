"""P12 F-4 — runtime observation conformance, mutation and negative controls.

The single property under test is that freshness actually gates the answer. A
detector that reports `LIVE` for every `RUNNING` record regardless of age is not
observation of live state; it is historical evidence with a confident label.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from tools import p12_runtime_observation as obs


def _at(root: Path, runtime_id: str, state: str, age_seconds: float) -> Path:
    """Publish a record that is `age_seconds` old."""
    when = datetime.now(timezone.utc) - timedelta(seconds=age_seconds)
    return obs.publish(runtime_id, state, root=root, now=when)


def _at_kind(root: Path, subject: str, state: str, age_seconds: float,
             kind: str) -> Path:
    when = datetime.now(timezone.utc) - timedelta(seconds=age_seconds)
    return obs.publish(subject, state, root=root, now=when, kind=kind)


class FreshnessGatesTheAnswer(unittest.TestCase):
    """Gate Q — mutate the condition; the detector must change."""

    def test_running_and_fresh_is_live(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.RUNNING", age_seconds=1)
            answer = obs.what_is_running(Path(tmp))
            self.assertTrue(answer["answerable"])
            self.assertEqual(len(answer["live"]), 1)

    def test_running_and_expired_is_not_live_and_not_answerable(self):
        """MUTATION: fresh → expired. The same RUNNING record must stop
        supporting the claim that anything is running."""
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.RUNNING",
                age_seconds=obs.LIVE_HORIZON_SECONDS + 60)
            answer = obs.what_is_running(Path(tmp))
            self.assertFalse(
                answer["answerable"],
                "a stale RUNNING record must not establish current state",
            )
            self.assertEqual(answer["live"], ())
            self.assertIn("stale", answer)

    def test_stale_is_not_reported_as_stopped_either(self):
        """A dead-but-unreported runtime is UNKNOWN, not TERMINATED. Claiming
        it stopped would be as false as claiming it runs."""
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.RUNNING",
                age_seconds=obs.LIVE_HORIZON_SECONDS + 60)
            found = obs.observations(Path(tmp))
            self.assertEqual(found[0].classification, obs.STALE)
            self.assertNotEqual(found[0].classification, obs.TERMINATED)

    def test_stopped_is_terminated_at_any_age(self):
        """MUTATION: RUNNING → STOPPED. A terminal state does not decay."""
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.STOPPED", age_seconds=99999)
            found = obs.observations(Path(tmp))
            self.assertEqual(found[0].classification, obs.TERMINATED)
            self.assertEqual(obs.what_is_running(Path(tmp))["live"], ())

    def test_created_and_initialized_are_not_running(self):
        """Real lifecycle states that are neither running nor terminal."""
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.CREATED", age_seconds=1)
            _at(Path(tmp), "r2", "RuntimeState.INITIALIZED", age_seconds=1)
            answer = obs.what_is_running(Path(tmp))
            self.assertEqual(answer["live"], ())
            self.assertEqual(answer["terminated"], ())

    def test_the_detector_does_not_always_answer_the_same_thing(self):
        """Gate Q: a constant detector is not verification."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _at(root, "r1", "RuntimeState.RUNNING", age_seconds=1)
            live = obs.what_is_running(root)["answerable"]
            _at(root, "r1", "RuntimeState.RUNNING",
                age_seconds=obs.LIVE_HORIZON_SECONDS + 60)
            stale = obs.what_is_running(root)["answerable"]
            _at(root, "r1", "RuntimeState.STOPPED", age_seconds=1)
            stopped = obs.what_is_running(root)["live"]
            self.assertTrue(live)
            self.assertFalse(stale)
            self.assertEqual(stopped, ())


class EmptyIsNotZero(unittest.TestCase):
    """Gate G — absence of observation is UNKNOWN, never 'nothing is running'."""

    def test_no_root_is_unanswerable_not_empty_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            answer = obs.what_is_running(Path(tmp) / "absent")
            self.assertFalse(answer["answerable"])
            self.assertIn("absence is not zero", answer["reason"])

    def test_no_records_is_unanswerable(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(obs.what_is_running(Path(tmp))["answerable"])


class NegativeControls(unittest.TestCase):
    """Gate P — each invalid condition is actually exercised, not assumed."""

    def test_a_fabricated_running_record_still_obeys_freshness(self):
        """Writing RUNNING by hand does not make anything run. The record is
        accepted as a record and still fails the liveness horizon."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            root.mkdir(parents=True, exist_ok=True)
            (root / "ghost.observation.json").write_text(json.dumps({
                "runtime_id": "ghost",
                "state": "RuntimeState.RUNNING",
                "observed_at": (datetime.now(timezone.utc)
                                - timedelta(hours=3)).isoformat(),
                "pid": 999999,
            }), encoding="utf-8")
            self.assertFalse(obs.what_is_running(root)["answerable"])

    def test_observation_does_not_mutate_what_it_reads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = _at(root, "r1", "RuntimeState.RUNNING", age_seconds=1)
            before = path.read_text(encoding="utf-8")
            obs.what_is_running(root)
            obs.observations(root)
            self.assertEqual(before, path.read_text(encoding="utf-8"))

    def test_no_answer_grants_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.RUNNING", age_seconds=1)
            rendered = repr(obs.what_is_running(Path(tmp))).lower()
            for word in ("authorized", "permitted", "may_", "approve"):
                self.assertNotIn(word, rendered)

    def test_publish_requires_a_state_and_records_the_one_given(self):
        """`publish` never defaults or computes a state — it records what it
        was handed, so a caller with no real runtime has nothing to publish."""
        with tempfile.TemporaryDirectory() as tmp:
            path = obs.publish("r1", "RuntimeState.RUNNING", root=Path(tmp))
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["state"], "RuntimeState.RUNNING")
            self.assertEqual(payload["runtime_id"], "r1")


class TheResidentObservationIsHonestAboutItself(unittest.TestCase):
    """The committed record from the proof run is long stale by now, and must
    read as such — a permanent negative control living in the corpus."""

    def test_the_committed_observation_does_not_claim_to_be_running(self):
        answer = obs.what_is_running()
        self.assertEqual(
            answer.get("live", ()), (),
            "a committed observation must never read as a live runtime",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()


class CoverageIsStatedNotImplied(unittest.TestCase):
    """Gate L — one observed path is not system-wide coverage, and the answer
    must say so rather than let an empty `live` read as 'nothing is running'."""

    def test_an_answerable_result_carries_its_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.STOPPED", age_seconds=1)
            answer = obs.what_is_running(Path(tmp))
            self.assertTrue(answer["answerable"])
            self.assertIn("not covered", answer["scope"])
            # The scope must name both vocabularies, not just the one it began
            # with: an answer covering workflows while saying "runtimes" is the
            # stale-label defect one layer up.
            self.assertIn("workflows", answer["scope"])
            self.assertIn("runtimes", answer["scope"])

    def test_empty_live_does_not_claim_nothing_is_running(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at(Path(tmp), "r1", "RuntimeState.STOPPED", age_seconds=1)
            answer = obs.what_is_running(Path(tmp))
            self.assertEqual(answer["live"], ())
            self.assertIn("scope", answer)
            rendered = repr(answer).lower()
            for claim in ("nothing is running", "no runtimes", "system idle"):
                self.assertNotIn(claim, rendered)


class TwoVocabulariesStaySeparate(unittest.TestCase):
    """F-11 — Runtime RUNNING and Workflow RUNNING are not the same claim.

    A Workflow can run on a Runtime that is only INITIALIZED, and a Runtime can
    be RUNNING with no Workflow at all. Merging them would lose exactly the
    distinction the two boundaries were built to keep.
    """

    def test_a_live_workflow_is_not_reported_as_a_live_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at_kind(Path(tmp), "wf1", "WorkflowState.RUNNING", 1, obs.WORKFLOW)
            answer = obs.what_is_running(Path(tmp))
            self.assertEqual(answer["live_by_kind"][obs.WORKFLOW], ("wf1",))
            self.assertEqual(answer["live_by_kind"][obs.RUNTIME], ())

    def test_a_live_runtime_is_not_reported_as_a_live_workflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at_kind(Path(tmp), "rt1", "RuntimeState.RUNNING", 1, obs.RUNTIME)
            answer = obs.what_is_running(Path(tmp))
            self.assertEqual(answer["live_by_kind"][obs.RUNTIME], ("rt1",))
            self.assertEqual(answer["live_by_kind"][obs.WORKFLOW], ())

    def test_both_kinds_coexist_without_merging(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at_kind(Path(tmp), "rt1", "RuntimeState.RUNNING", 1, obs.RUNTIME)
            _at_kind(Path(tmp), "wf1", "WorkflowState.RUNNING", 1, obs.WORKFLOW)
            by_kind = obs.what_is_running(Path(tmp))["live_by_kind"]
            self.assertEqual(by_kind[obs.RUNTIME], ("rt1",))
            self.assertEqual(by_kind[obs.WORKFLOW], ("wf1",))

    def test_workflow_terminals_are_terminated_not_running(self):
        """SUCCEEDED and FAILED are the Workflow vocabulary's terminals; neither
        is translated into the Runtime vocabulary's STOPPED."""
        for terminal in ("WorkflowState.SUCCEEDED", "WorkflowState.FAILED"):
            with tempfile.TemporaryDirectory() as tmp:
                _at_kind(Path(tmp), "wf1", terminal, 1, obs.WORKFLOW)
                found = obs.observations(Path(tmp))
                self.assertEqual(found[0].classification, obs.TERMINATED)
                self.assertEqual(
                    obs.what_is_running(Path(tmp))["live_by_kind"][obs.WORKFLOW], ())

    def test_a_stale_running_workflow_is_no_more_live_than_a_stale_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            _at_kind(Path(tmp), "wf1", "WorkflowState.RUNNING",
                     obs.LIVE_HORIZON_SECONDS + 60, obs.WORKFLOW)
            self.assertFalse(obs.what_is_running(Path(tmp))["answerable"])

    def test_a_record_without_a_kind_defaults_to_runtime_explicitly(self):
        """Records predating workflow observation carry no `kind`. The default
        is stated in code rather than guessed downstream."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            root.mkdir(parents=True, exist_ok=True)
            (root / "legacy.observation.json").write_text(json.dumps({
                "runtime_id": "legacy",
                "state": "RuntimeState.RUNNING",
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "pid": 1,
            }), encoding="utf-8")
            self.assertEqual(obs.observations(root)[0].kind, obs.RUNTIME)
