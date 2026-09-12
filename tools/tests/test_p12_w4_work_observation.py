"""P12-W4 `F-10′` — the work ↔ observation relationship.

`§17` requires execution integration to prove the relationship *between*
surfaces, not each surface's existence. These controls hold the distinction that
made the earlier closures narrower than they read:

```text
DEMONSTRATOR   ≠   SYSTEM WORK
SURFACE EXISTS ≠   WORK ↔ OBSERVATION RELATIONSHIP
LIVE CATCH     ≠   WORK ↔ OBSERVATION RELATIONSHIP
```
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from tools import p12_runtime_observation as obs
from tools import p12_certified_evidence_guard as sentinel

REPO_ROOT = Path(__file__).resolve().parents[2]
WORK_PATH = REPO_ROOT / "w1_coordination_proof.py"
WORK_RUNTIME_ID = "p11-w1-runtime"


class TheResidentWorkPathPublishes(unittest.TestCase):
    """Regression: if the publish calls are removed, the relationship dies
    silently and every other test here would still pass."""

    def test_the_work_path_calls_publish(self):
        tree = ast.parse(WORK_PATH.read_text(encoding="utf-8"))
        calls = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "publish"
        ]
        self.assertGreaterEqual(
            len(calls), 2,
            "the work path must publish while running and after stopping",
        )

    def test_the_work_path_is_not_a_demonstrator(self):
        """It performs real coordination work, which is what distinguishes it
        from the observation proofs."""
        source = WORK_PATH.read_text(encoding="utf-8")
        self.assertIn("WorkflowParticipatingAgent", source)
        self.assertIn("participate(", source)


class TheWorkReachedTheObservationSurface(unittest.TestCase):
    def test_the_work_runtime_is_present_in_the_observed_population(self):
        ids = {o.runtime_id for o in obs.observations()}
        self.assertIn(
            WORK_RUNTIME_ID, ids,
            "the observed population must contain real system work, not only "
            "the demonstrators that prove the surface functions",
        )

    def test_the_observed_population_is_no_longer_only_demonstrators(self):
        ids = {o.runtime_id for o in obs.observations()}
        demonstrators = {
            "p12-f4-runtime-observation", "p12-f11-workflow-observation"
        }
        self.assertTrue(
            ids - demonstrators,
            "F-13: an observed population made only of demonstrators is true "
            "and useless",
        )


class TheClaimIsNotOverstated(unittest.TestCase):
    """The work's RUNNING window is 0.9 ms. No live external catch is claimed,
    and none should be introduced later without re-measuring that window."""

    def test_the_proof_does_not_assert_a_live_catch(self):
        source = (REPO_ROOT / "p12_w4_observed_work_proof.py").read_text(
            encoding="utf-8")
        self.assertIn("LIVE CATCH ≠ WORK ↔ OBSERVATION RELATIONSHIP", source)
        self.assertNotIn("caught_live", source)

    def test_a_terminated_observation_is_not_reported_as_running(self):
        answer = obs.what_is_running()
        self.assertNotIn(WORK_RUNTIME_ID, answer["live_by_kind"]["runtime"])
        self.assertIn(WORK_RUNTIME_ID, answer["terminated"])


class CertifiedEvidenceStaysFrozen(unittest.TestCase):
    """The observed run persists nothing into P11. F-12 remains intact and was
    neither bypassed nor weakened to make this increment possible."""

    def test_the_guard_still_refuses_p11_evidence(self):
        target = REPO_ROOT / "docs/architecture/p11/w1-operations/w1-coordination.evidence.json"
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            sentinel.guard(target)

    def test_observations_are_written_outside_certified_roots(self):
        self.assertFalse(
            sentinel.is_protected(obs.OBSERVATION_ROOT / "x.observation.json"),
            "observation must not be written into a certified phase root",
        )

    def test_the_observed_work_entry_point_persists_nothing(self):
        source = (REPO_ROOT / "p12_w4_observed_work_proof.py").read_text(
            encoding="utf-8")
        self.assertIn("persist=False", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
