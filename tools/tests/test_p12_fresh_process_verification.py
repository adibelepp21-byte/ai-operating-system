"""P12-W6 fresh-process verification conformance.

Eight stages reproducing on the first run is the result a broken comparator
would also produce. The controls here exist to tell those two apart.
"""

from __future__ import annotations

import unittest
from unittest import mock

from tools import p12_fresh_process_verification as fresh


#: Eight subprocesses per call. Cached for the tests that use the *real*
#: comparison; the mutation controls patch `_there` and must not reuse it.
_REAL = None


def _real():
    global _REAL
    if _REAL is None:
        _REAL = fresh.verify()
    return _REAL


class AllEightStagesAreCovered(unittest.TestCase):
    def test_the_stages_are_section_52s_eight_in_order(self):
        self.assertEqual(
            tuple(name for name, _ in fresh.STAGES),
            ("repository", "canonical sources", "registries", "state",
             "decisions", "integration graph", "runtime", "evidence"),
        )

    def test_every_stage_is_derived_twice_and_compared(self):
        for result in _real():
            self.assertTrue(result.in_process, f"{result.stage} has no in-process value")
            self.assertTrue(result.fresh_process, f"{result.stage} has no fresh value")


class TheComparatorCanActuallyFail(unittest.TestCase):
    """Mutation control. A comparator that always agrees proves nothing."""

    def test_an_injected_divergence_is_detected(self):
        real = fresh._there

        def _diverge(expr):
            return "DELIBERATELY DIFFERENT"

        with mock.patch.object(fresh, "_there", _diverge):
            results = fresh.verify()
        self.assertTrue(
            all(r.status == fresh.DIVERGED for r in results),
            "the comparator failed to notice a value that differs from every stage",
        )
        self.assertEqual(fresh._there, real)

    def test_a_child_failure_is_unavailable_not_reproduced(self):
        """A subprocess that cannot run must never read as agreement."""
        with mock.patch.object(fresh, "_there", lambda expr: "<child failed: x>"):
            results = fresh.verify()
        self.assertTrue(all(r.status == fresh.UNAVAILABLE for r in results))
        self.assertFalse(any(r.status == fresh.REPRODUCED for r in results))

    def test_summary_counts_divergence(self):
        with mock.patch.object(fresh, "_there", lambda expr: "DIFFERENT"):
            summary = fresh.summary()
        self.assertEqual(summary["diverged"], summary["stages"])
        self.assertEqual(summary["reproduced"], 0)
        self.assertEqual(len(summary["diverged_stages"]), summary["stages"])


class TheCurrentCorpusReproduces(unittest.TestCase):
    def test_no_stage_diverges(self):
        diverged = [r.stage for r in _real() if r.status == fresh.DIVERGED]
        self.assertEqual(diverged, [], f"session-dependent claims: {diverged}")

    def test_no_stage_is_unavailable(self):
        self.assertEqual(
            [r.stage for r in _real() if r.status == fresh.UNAVAILABLE], [])

    def test_the_child_shares_no_state_with_this_process(self):
        """The child imports from the repository path only — it receives no
        object, no module reference and no value from here."""
        self.assertIn("sys.path.insert", fresh._CHILD)
        self.assertNotIn("pickle", fresh._CHILD)


class ReproducibilityIsNotAdequacy(unittest.TestCase):
    def test_the_module_asserts_no_threshold(self):
        """Whether these values satisfy E12-06 is Founder-reserved (§53, F-16)."""
        source = fresh.__doc__ or ""
        self.assertIn("reports reproducibility, not adequacy", source)

    def test_no_stage_returns_a_pass_or_fail_verdict(self):
        for result in _real():
            self.assertIn(result.status,
                          (fresh.REPRODUCED, fresh.DIVERGED, fresh.UNAVAILABLE))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
