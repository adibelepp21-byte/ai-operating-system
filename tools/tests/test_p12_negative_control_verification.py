"""P12-W6 negative-control conformance (`§19` scope: `NEGATIVE CONTROLS`).

Ten `DEMONSTRATED` is what a module returning a constant would print. These
controls establish that each result is driven by the instrument's actual return
value, that `NOT DEMONSTRATED` is reachable, and that no resident state is
disturbed by a run.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_negative_control_verification as neg


class TheScopeIsEveryP12Verifier(unittest.TestCase):
    def test_every_p12_verification_module_is_covered(self):
        """A verifier missing from the list is a verifier nothing checks."""
        covered = {name for name, _, _ in neg.CONTROLS}
        exempt = {
            # Not verifiers: these are the observation and self-description
            # surfaces the verifiers read. Each is still covered above, but by
            # the instrument that consumes it where that is the real check.
            "p12_negative_control_verification",
        }
        resident = {path.stem
                    for path in (neg.REPO_ROOT / "tools").glob("p12_*.py")}
        self.assertEqual(sorted(resident - covered - exempt), [])

    def test_each_entry_names_the_negative_it_seeks(self):
        for name, sought, _ in neg.CONTROLS:
            with self.subTest(name):
                self.assertTrue(sought.strip())


class NotDemonstratedIsReachable(unittest.TestCase):
    """Without this, ten DEMONSTRATED is a constant, not a measurement."""

    def test_a_control_that_fails_is_reported_not_demonstrated(self):
        with mock.patch.object(
                neg, "CONTROLS",
                (("some_instrument", "some negative",
                  lambda: (False, "it answered anyway")),)):
            result = neg.verify()[0]
            summary = neg.summary()
        self.assertEqual(result.status, neg.NOT_DEMONSTRATED)
        self.assertEqual(summary["undemonstrated_instruments"],
                         ("some_instrument",))

    def test_a_raising_control_is_unavailable_not_demonstrated(self):
        def explode():
            raise RuntimeError("the instrument could not be loaded")

        with mock.patch.object(
                neg, "CONTROLS",
                (("some_instrument", "some negative", explode),)):
            result = neg.verify()[0]
            summary = neg.summary()
        self.assertEqual(result.status, neg.UNAVAILABLE)
        self.assertIn("some_instrument", summary["undemonstrated_instruments"])

    def test_unavailable_is_never_counted_as_demonstrated(self):
        def explode():
            raise RuntimeError("boom")

        with mock.patch.object(
                neg, "CONTROLS",
                (("a", "n", explode), ("b", "n", lambda: (True, "ok")))):
            summary = neg.summary()
        self.assertEqual(summary["demonstrated"], 1)
        self.assertEqual(summary["unavailable"], 1)


class EachNegativeIsDrivenNotCited(unittest.TestCase):
    def test_the_runtime_negative_uses_an_empty_root(self):
        demonstrated, detail = neg._runtime_observation()
        self.assertTrue(demonstrated)
        self.assertIn("answerable=False", detail)

    def test_the_guard_negative_raises_rather_than_returning_empty(self):
        demonstrated, detail = neg._certified_evidence_guard()
        self.assertTrue(demonstrated)
        self.assertIn("raised", detail)

    def test_the_guard_is_restored_after_the_negative_runs(self):
        from tools import p12_certified_evidence_guard as guard
        before = dict(guard.PHASE_EVIDENCE_ROOTS)
        neg._certified_evidence_guard()
        self.assertEqual(guard.PHASE_EVIDENCE_ROOTS, before)
        self.assertTrue(guard.protected_roots())

    def test_the_fresh_process_negative_restores_the_subprocess_hook(self):
        from tools import p12_fresh_process_verification as fresh
        before = fresh._there
        neg._fresh_process()
        self.assertIs(fresh._there, before)
        self.assertEqual(fresh.summary()["diverged"], 0)

    def test_the_cross_pd_negative_restores_the_registry(self):
        from tools import p12_cross_pd_verification as xpd
        before = xpd.REGISTRY
        neg._cross_pd()
        self.assertIs(xpd.REGISTRY, before)
        self.assertEqual(xpd.summary()["unavailable"], 0)

    def test_the_governance_negative_changes_bytes_not_only_paths(self):
        demonstrated, detail = neg._governance_index()
        self.assertTrue(demonstrated)
        self.assertIn("hash recorded at build", detail)


class TheSelfModelHonoursItsRootParameter(unittest.TestCase):
    """The finding this scope produced, held closed."""

    def test_store_backed_questions_answer_unknown_against_an_empty_root(self):
        from tools import p12_self_model as model
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp)
            for fn in (model.capabilities, model.running, model.failed):
                with self.subTest(fn.__name__):
                    self.assertEqual(fn(empty).status.upper(), "UNKNOWN")

    def test_they_do_not_return_the_live_answer_for_an_empty_root(self):
        from tools import p12_self_model as model
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp)
            for fn in (model.capabilities, model.running, model.failed):
                with self.subTest(fn.__name__):
                    self.assertNotEqual(repr(fn(empty)), repr(fn()))

    def test_a_redirected_module_root_is_honoured_as_given(self):
        """How the resident suites isolate; re-basing it would break them."""
        from tools import p12_runtime_observation as obs
        from tools.p12_self_model import _under
        with tempfile.TemporaryDirectory() as tmp:
            redirected = Path(tmp)
            self.assertEqual(_under(neg.REPO_ROOT, redirected, obs.REPO_ROOT),
                             redirected)

    def test_a_root_inside_the_repository_is_rebased_onto_it(self):
        from tools import p12_runtime_observation as obs
        from tools.p12_self_model import _under
        with tempfile.TemporaryDirectory() as tmp:
            elsewhere = Path(tmp)
            self.assertEqual(
                _under(elsewhere, obs.OBSERVATION_ROOT, obs.REPO_ROOT),
                elsewhere / obs.OBSERVATION_ROOT.relative_to(obs.REPO_ROOT))

    def test_the_live_coverage_is_unchanged_by_the_fix(self):
        from tools import p12_self_model as model
        self.assertEqual(
            model.coverage(),
            {"questions": 12, "verified": 10, "inferred": 2, "unknown": 0})


class WhatThisSuiteDoesNotEstablish(unittest.TestCase):
    def test_a_demonstrated_negative_is_not_a_correctness_claim(self):
        """That an instrument *can* fail says nothing about whether it should."""
        for result in neg.verify():
            with self.subTest(result.instrument):
                self.assertTrue(result.negative_sought)
                self.assertNotIn("correct", result.negative_sought.lower())


if __name__ == "__main__":
    unittest.main()
