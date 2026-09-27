"""P12 POPULATION GUARD SUCCESSOR, version 2.

Constructed under `FD-P12-007` (Register `§73`): D3 chose a **versioned
successor** (L2), and D5 authorized this bounded change. Specification and
verification record: `docs/fullstack/P12-POPULATION-GUARD-SUCCESSOR.md`.

**Predecessor.** The *P12 HISTORICAL POPULATION GUARD*, version 1:
`test_p12_governance_evidence_verification.TheResultDoesNotDependOnMyChoiceOfPopulation.test_the_narrower_population_is_not_better`,
introduced in `14afe69`. Its property: over each of five `§26` elements, the
Founder-act ratio is at most the corpus ratio plus 0.2. It is **not rewritten,
skipped or marked**. It keeps running and keeps failing. That failure is the
classified governance signal of `FD-P12-007` `§8`: the property it watches
inverted as the corpus grew, first failing at `20742f5`. Its two files are
pinned below byte for byte, so it cannot be silently overwritten.

**What changes in version 2, and only this.** The direction of the comparison.
The Founder-act ratio must be **at least** the corpus ratio minus 0.2. The
populations, the classifier, the five elements, the label rule and the 0.2
margin are the predecessor's, unchanged. The direction is the one observed
without interruption on all five elements since `ddc6fe3`
(`docs/fullstack/evidence/P12-POPULATION-GUARD-SERIES-2026-09-27.json`). The
margin is inherited rather than chosen, so no new threshold is introduced.

**What version 2 does not claim.** Version 1 supported a historical argument:
the corpus-wide `§26` result is not an artefact of dilution, because the
narrower population scored worse. Version 2 does **not** support that
argument, and says nothing about whether the historical guard held it
correctly. It watches the current property: that Founder instruments are not
markedly *less* machine-readable than the corpus. If that inverts, it must be
loud, exactly as version 1 was.

**Classifier** (`FD-P12-007` `§15`): option 1, **the current classifier is
preserved**. Its code and constants are fingerprinted, so a later classifier
change fails here as a semantic change that a successor version must record,
instead of mixing into corpus growth silently. That is how `76366be` mixed in,
unrecorded.

**Not certified** by being written (`FD-P12-007` `§18`, `§19`).
"""

from __future__ import annotations

import hashlib
import inspect
import unittest
from pathlib import Path
from unittest import mock

from tools import governance_index as gi
from tools import p12_governance_evidence_verification as gov
from tools.tests import test_p12_governance_evidence_verification as predecessor

REPO_ROOT = Path(__file__).resolve().parents[2]

IDENTITY = "P12 POPULATION GUARD SUCCESSOR"
VERSION = 2
AUTHORITY = "FD-P12-007 (Register §73): D3 L2 versioned successor; D5 bounded tools/ authorization"

PREDECESSOR = {
    "identity": "P12 HISTORICAL POPULATION GUARD",
    "version": 1,
    "test": ("tools/tests/test_p12_governance_evidence_verification.py::"
             "TheResultDoesNotDependOnMyChoiceOfPopulation::"
             "test_the_narrower_population_is_not_better"),
    "introduced": "14afe69",
    "first_failure": "20742f5",
    "status": "LIVING · failing · classified governance signal (FD-P12-007 §8)",
}
#: The predecessor's files, byte for byte, as they stood when this successor
#: was constructed (unchanged since `14afe69` and `67b405b`).
PREDECESSOR_FILES = {
    "tools/tests/test_p12_governance_evidence_verification.py":
        "5d778b328c095f6fe046f437f29dfb9bf8bc7bf3f00fed82597494a006b41a5e",
    "tools/p12_governance_evidence_verification.py":
        "b9ec2c92ff1be4abec6a2105ecb2c3d6b8ef399b3bfe492320fbcb67c7bae36c",
}

#: Population: the predecessor's, unchanged. Every tracked `docs/**/*.md` that
#: `governance_index.is_governance_record` accepts is the corpus; the subset
#: whose path lies under `docs/governance/acts/` is the Founder-act population.
#: Both are read through `gov.by_population()`, the function the predecessor reads.
ELEMENTS = ("decision body", "authority", "scope", "status", "current state")
MARGIN = 0.2  # the predecessor's margin, inherited unchanged

#: Classifier fingerprint at construction (`FD-P12-007` `§15`, option 1).
CLASSIFIER_FINGERPRINT = "a89ac04e3c286254fe431c56aebcf579369beeb58251e49f354c880a195d421a"

#: The five elements as the certified P12-W6 record measured them (`§3`, `§5`):
#: (corpus labelled, corpus total, Founder acts labelled, Founder acts total).
#: Dated historical figures, used only to show the predecessor's arithmetic.
HISTORICAL_W6_FIGURES = {
    "decision body": (93, 385, 5, 33),
    "authority": (107, 385, 11, 33),
    "scope": (23, 385, 1, 33),
    "status": (123, 385, 6, 33),
    "current state": (48, 385, 2, 33),
}


def successor_holds(wide: float, narrow: float) -> bool:
    """Version 2: the Founder-act ratio is not below the corpus ratio by more than the margin."""
    return narrow >= wide - MARGIN


def predecessor_holds(wide: float, narrow: float) -> bool:
    """Version 1, transcribed from the predecessor's assertion, not re-decided."""
    return narrow <= wide + MARGIN


def ratios(both: dict) -> dict:
    """element → (corpus ratio, Founder-act ratio), from `by_population()`'s shape."""
    out = {}
    for element in ELEMENTS:
        wide, narrow = both["corpus"][element], both["founder_acts"][element]
        out[element] = (wide[1] / max(wide[2], 1), narrow[1] / max(narrow[2], 1))
    return out


def classifier_fingerprint() -> str:
    """Everything `is_governance_record` decides membership with."""
    parts = [repr(gi.IDENTIFIER_CLASS_NAMES), gi.IDENTIFIER_RE.pattern, gi.TOPIC_RE.pattern,
             gi._LABEL_RE.pattern, gi._RULE_RE.pattern, repr(gi.METADATA_FALLBACK_LINES),
             repr(gi._VALUE_TRIM), repr(dict(gi.FIELD_LABELS))]
    parts += [inspect.getsource(f) for f in (
        gi.is_governance_record, gi._metadata_lines, gi.identifiers_in, gi._labels,
        gi._table_label, gi._unwrap, gi.tracked_markdown)]
    return hashlib.sha256("\n\x00\n".join(parts).encode()).hexdigest()


def _synthetic(labelled: bool) -> tuple:
    body = "# A record\n\n**Identifier:** ACT-SYN-1\n"
    if labelled:
        body += ("Decided by: F\nAuthority: F\nScope: S\nStatus: X\nDecision: D\n")
    return (Path("synthetic.md"), body + "\n---\n\nBody.\n")


def _synthetic_ratios(wide_docs, narrow_docs) -> dict:
    wide = {r.element: (r.status, r.instruments, r.population)
            for r in gov.coverage(population=wide_docs)}
    narrow = {r.element: (r.status, r.instruments, r.population)
              for r in gov.coverage(population=narrow_docs)}
    return ratios({"corpus": wide, "founder_acts": narrow})


class TheSuccessorIsIdentifiedAndBounded(unittest.TestCase):
    def test_identity_version_and_authority_are_explicit(self):
        self.assertEqual("P12 POPULATION GUARD SUCCESSOR", IDENTITY)
        self.assertEqual(2, VERSION)
        self.assertEqual(VERSION, PREDECESSOR["version"] + 1)
        self.assertIn("FD-P12-007", AUTHORITY)
        self.assertEqual("P12 HISTORICAL POPULATION GUARD", PREDECESSOR["identity"])

    def test_the_predecessor_is_preserved_byte_for_byte(self):
        for path, digest in PREDECESSOR_FILES.items():
            with self.subTest(path):
                self.assertEqual(digest, hashlib.sha256(
                    (REPO_ROOT / path).read_bytes()).hexdigest(),
                    "the historical guard changed; FD-P12-007 D3 forbids rewriting it in place")

    def test_the_predecessor_still_runs_and_is_not_suppressed(self):
        cls = predecessor.TheResultDoesNotDependOnMyChoiceOfPopulation
        method = getattr(cls, "test_the_narrower_population_is_not_better")
        for flag in ("__unittest_skip__", "__unittest_expecting_failure__"):
            self.assertFalse(getattr(method, flag, False), flag)
            self.assertFalse(getattr(cls, flag, False), flag)

    def test_it_measures_the_predecessors_populations(self):
        self.assertEqual(ELEMENTS, ("decision body", "authority", "scope", "status",
                                    "current state"))
        self.assertIn('"docs/governance/acts/"', inspect.getsource(gov.by_population))
        self.assertEqual(0.2, MARGIN)


class TheClassifierIsPreserved(unittest.TestCase):
    """`FD-P12-007` `§15`: a classifier change is a semantic change, never silent."""

    def test_the_classifier_is_the_one_this_version_declares(self):
        self.assertEqual(CLASSIFIER_FINGERPRINT, classifier_fingerprint(),
                         "the population classifier changed: record it as a new "
                         "successor version (FD-P12-007 §15)")

    def test_a_classifier_change_moves_the_fingerprint(self):
        with mock.patch.object(gi, "IDENTIFIER_CLASS_NAMES", gi.IDENTIFIER_CLASS_NAMES + ("X",)):
            self.assertNotEqual(CLASSIFIER_FINGERPRINT, classifier_fingerprint())
        with mock.patch.object(gi, "METADATA_FALLBACK_LINES", gi.METADATA_FALLBACK_LINES + 1):
            self.assertNotEqual(CLASSIFIER_FINGERPRINT, classifier_fingerprint())


class TheCurrentPropertyHolds(unittest.TestCase):
    """The successor's living check, over the current committed corpus."""

    @classmethod
    def setUpClass(cls):
        cls.live = ratios(gov.by_population())

    def test_founder_acts_are_not_markedly_less_machine_readable(self):
        for element, (wide, narrow) in self.live.items():
            with self.subTest(element):
                self.assertTrue(successor_holds(wide, narrow),
                                f"{element}: Founder acts {narrow:.3f} < corpus {wide:.3f} - {MARGIN}")


class ThePredecessorFailureIsTheClassifiedSignal(unittest.TestCase):
    """`FD-P12-007` D4: the exception covers the inversion and nothing else."""

    def test_the_predecessor_arithmetic_passes_on_the_historical_figures(self):
        """It worked as designed where the certified record says it held."""
        for element, (w, wt, n, nt) in HISTORICAL_W6_FIGURES.items():
            with self.subTest(element):
                self.assertTrue(predecessor_holds(w / wt, n / nt))

    def test_every_live_predecessor_violation_is_an_inversion(self):
        """Any element the predecessor fails on fails because Founder acts
        score *higher*, the inversion, and the successor holds on it. A
        failure of any other kind would not be covered by the exception."""
        for element, (wide, narrow) in ratios(gov.by_population()).items():
            if not predecessor_holds(wide, narrow):
                with self.subTest(element):
                    self.assertGreater(narrow, wide)
                    self.assertTrue(successor_holds(wide, narrow))

    def test_the_two_versions_can_disagree_only_in_the_expected_direction(self):
        """For any ratios, at least one version holds: the two properties
        overlap in the band |narrow - wide| <= margin, and each fails only on
        its own side of it."""
        for wide in (0.0, 0.3, 0.6, 1.0):
            for narrow in (0.0, 0.1, 0.3, 0.5, 0.7, 1.0):
                with self.subTest(wide=wide, narrow=narrow):
                    self.assertTrue(predecessor_holds(wide, narrow)
                                    or successor_holds(wide, narrow))


class TheSuccessorCanFail(unittest.TestCase):
    """Negative controls: each outcome is reachable."""

    def test_it_fails_when_founder_acts_label_far_less_than_the_corpus(self):
        narrow = [_synthetic(False) for _ in range(5)]
        wide = narrow + [_synthetic(True) for _ in range(15)]
        result = _synthetic_ratios(wide, narrow)
        self.assertTrue(result)
        for element, (w, n) in result.items():
            with self.subTest(element):
                self.assertFalse(successor_holds(w, n))
                self.assertTrue(predecessor_holds(w, n))

    def test_it_holds_when_the_populations_label_alike(self):
        docs = [_synthetic(True) for _ in range(4)] + [_synthetic(False) for _ in range(4)]
        for element, (w, n) in _synthetic_ratios(docs, docs).items():
            with self.subTest(element):
                self.assertTrue(successor_holds(w, n))

    def test_the_predecessor_fails_where_the_successor_holds(self):
        narrow = [_synthetic(True) for _ in range(5)]
        wide = narrow + [_synthetic(False) for _ in range(15)]
        for element, (w, n) in _synthetic_ratios(wide, narrow).items():
            with self.subTest(element):
                self.assertFalse(predecessor_holds(w, n))
                self.assertTrue(successor_holds(w, n))


if __name__ == "__main__":
    unittest.main()
