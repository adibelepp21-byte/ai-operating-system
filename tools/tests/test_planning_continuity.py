"""`W5` planning continuity — the chain survives, the authority is re-earned.

`DP-01 §3 W5`: `MEMORY ≠ AUTHORITY`, and *"No memory mechanism may create,
elevate, or infer authority that has not otherwise been granted."*
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    EscalationRequired,
    Goal,
    Plan,
    PlanOrigin,
    PlanStep,
    PlanningSurface,
)
from tools.planning_continuity import (  # noqa: E402
    ContinuityError,
    persisted_goals,
    restore,
    save,
)

AUTHORITY = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"


def _provenance():
    return AuthorityProvenance("DP-01 §3 W2", AUTHORITY)


def _surface_with_history():
    surface = PlanningSurface()
    surface.declare(Goal("g", "Intent.", _provenance()))
    plan = surface.adopt(Plan(key="p", goal_key="g", authority=_provenance(),
                              steps=(PlanStep("a", "A."),
                                     PlanStep("b", "B.", depends_on=("a",)))))
    adapted = surface.adapt(plan, steps=plan.steps + (
        PlanStep("c", "C.", depends_on=("b",)),), reason="Observed a gap.")
    surface.revise(adapted, steps=(PlanStep("z", "Different approach."),),
                   reason="Approach refuted.")
    return surface


class TheChainSurvivesTheProcess(unittest.TestCase):
    def test_a_full_history_is_restored_in_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            restored = restore(path)
            history = restored.history("g")
            self.assertEqual(len(history), 3)
            self.assertEqual([p.revision for p in history], [0, 1, 2])
            self.assertEqual([p.origin for p in history],
                             [PlanOrigin.PLANNED, PlanOrigin.ADAPTED,
                              PlanOrigin.REVISED])

    def test_supersession_is_recomputed_not_read(self):
        """A stored flag could disagree with the chain; a derived one cannot."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            restored = restore(path)
            history = restored.history("g")
            self.assertTrue(restored.is_superseded(history[0]))
            self.assertTrue(restored.is_superseded(history[1]))
            self.assertFalse(restored.is_superseded(history[2]))
            self.assertIs(restored.current("g"), history[2])
            raw = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotIn("superseded", json.dumps(raw))

    def test_it_survives_a_real_process_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            proc = subprocess.run(
                [sys.executable, "-c",
                 "import sys; sys.path.insert(0, sys.argv[1]);"
                 "from pathlib import Path;"
                 "from tools.planning_continuity import restore;"
                 "s = restore(Path(sys.argv[2]));"
                 "print(len(s.history('g')), s.current('g').key)",
                 str(REPO_ROOT), str(path)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(proc.stdout.split()[0], "3")

    def test_the_restored_chain_can_continue_evolving(self):
        """Continuity that cannot be built on is an archive, not continuity."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            restored = restore(path)
            further = restored.adapt(restored.current("g"),
                                     steps=(PlanStep("z2", "Refined."),),
                                     reason="Continued after restore.")
            self.assertEqual(further.revision, 3)
            self.assertEqual(len(restored.history("g")), 4)


class MemoryDoesNotBecomeAuthority(unittest.TestCase):
    """`DP-01 §3 W5`. The property the module exists to guarantee."""

    def test_a_plan_whose_instrument_vanished_does_not_come_back(self):
        """Continuity, not resurrection.

        The citation is re-constructed on restore, so a plan formed under an
        instrument that no longer resolves fails closed rather than returning as
        a well-formed artifact asserting a source that is gone.
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["goals"][0]["chain"][0]["authority_record"] = \
                "docs/instrument-that-was-removed.md"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ContinuityError) as caught:
                restore(path)
            self.assertIn("no longer resolves", str(caught.exception))

    def test_a_goal_whose_instrument_vanished_does_not_come_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["goals"][0]["authority_record"] = "docs/gone.md"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ContinuityError):
                restore(path)

    def test_restoring_does_not_widen_what_a_plan_may_do(self):
        """Age confers nothing. A restored plan escalates exactly as it did."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            restored = restore(path)
            with self.assertRaises(EscalationRequired):
                restored.adapt(restored.current("g"),
                               steps=restored.current("g").steps,
                               reason="Surely now?", required_authority="DP-02")

    def test_a_forged_authority_in_the_file_is_refused(self):
        """Editing the file to claim a named authority is the obvious attack."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            payload = json.loads(path.read_text(encoding="utf-8"))
            for claim in ("Founder Reserved Authority", "Governance Authority"):
                payload["goals"][0]["chain"][0]["authority_instrument"] = claim
                payload["goals"][0]["chain"][0]["authority_record"] = \
                    "docs/no-such-file.md"
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.subTest(claim=claim):
                    with self.assertRaises(ContinuityError):
                        restore(path)

    def test_a_real_instrument_is_still_only_a_citation(self):
        """Stated so the control above is not mistaken for more than it is.

        Renaming the instrument to a real file restores successfully — because
        resolution proves the pointer, not the grant. What a restored plan may do
        is still bounded by what `adapt` checks, which is unchanged by restoring.
        """
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["goals"][0]["chain"][0]["authority_instrument"] = \
                "Founder Reserved Authority"
            path.write_text(json.dumps(payload), encoding="utf-8")
            restored = restore(path)
            with self.assertRaises(EscalationRequired):
                restored.adapt(restored.current("g"),
                               steps=restored.current("g").steps,
                               reason="Claimed wider authority.",
                               required_authority="DP-02")


class ContinuityIsBoundedToPlanning(unittest.TestCase):
    """`P11 ≠ P12`. This is not Unified Operational State."""

    def test_only_goals_and_plan_chains_are_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(list(payload), ["goals"])
            blob = json.dumps(payload).lower()
            for foreign in ("runtime", "workflow", "trace", "agent_instance",
                            "execution", "delegation_record"):
                self.assertNotIn(foreign, blob, foreign)

    def test_a_restored_surface_holds_planning_state_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            self.assertEqual(sorted(vars(restore(path))),
                             ["_by_key", "_chains", "_goals"])

    def test_inspection_does_not_revive(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            save(_surface_with_history(), path)
            self.assertEqual(persisted_goals(path), ("g",))


class ItFailsClosed(unittest.TestCase):
    def test_a_missing_file_is_refused(self):
        with self.assertRaises(ContinuityError):
            restore(Path("/nonexistent/planning.json"))

    def test_unreadable_state_is_refused_rather_than_partially_restored(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "planning.json"
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(ContinuityError):
                restore(path)


if __name__ == "__main__":
    unittest.main()
