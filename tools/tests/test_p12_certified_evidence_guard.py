"""P12-W3 — certification enforced across layers (`F-12`).

The controls that matter are that certification is read from **instrument
bodies** rather than prose or filenames, that the guard fails **closed** when
governance cannot be read, and that the set of writers it covers is **verified
rather than remembered** — a hand-kept list of guarded call sites is the same
stale-population defect this programme has corrected repeatedly.
"""

from __future__ import annotations

import ast
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import p12_certified_evidence_guard as sentinel

REPO_ROOT = Path(__file__).resolve().parents[2]


class CertificationComesFromInstrumentBodies(unittest.TestCase):
    def test_the_resident_certified_phases_are_ten_and_eleven(self):
        self.assertEqual(sentinel.certified_phases(), frozenset({10, 11}))

    def test_a_filename_alone_certifies_nothing(self):
        """IDENTIFIER ≠ DECISION BODY."""
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            (acts / "FD-P99-999-CERTIFICATION-OF-PHASE-99.md").write_text(
                "This instrument proposes certification. Nothing is certified.",
                encoding="utf-8")
            self.assertEqual(sentinel.certified_phases(acts), frozenset())

    def test_a_negated_register_sentence_does_not_certify(self):
        """The Register contains "It does **not** establish PHASE 8 — CERTIFIED /
        COMPLETE". A guard fooled by a negation is worse than no guard, so the
        certification pattern matches a *statement*, not the phrase."""
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            (acts / "register-like.md").write_text(
                "It does not establish PHASE 8 — CERTIFIED / COMPLETE, which "
                "remains a separate determination.", encoding="utf-8")
            self.assertNotIn(8, sentinel.certified_phases(acts))

    def test_an_actual_certification_statement_is_recognised(self):
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            (acts / "fd.md").write_text(
                "PHASE 7 — MEMORY ECOSYSTEM IS CERTIFIED.", encoding="utf-8")
            self.assertIn(7, sentinel.certified_phases(acts))


class FailsClosed(unittest.TestCase):
    def test_unreadable_governance_raises_rather_than_permitting(self):
        """An undeterminable boundary is not an absent one."""
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "no-such-acts"
            with self.assertRaises(sentinel.CertificationUndeterminable):
                sentinel.certified_phases(missing)


class TheGuardRefusesTheRightWrites(unittest.TestCase):
    def test_certified_phase_evidence_is_refused(self):
        target = REPO_ROOT / "docs/architecture/p11/w1-operations/w1-coordination.evidence.json"
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            sentinel.guard(target)

    def test_uncertified_phase_evidence_is_permitted(self):
        target = REPO_ROOT / "docs/architecture/p12/anything.json"
        self.assertEqual(sentinel.guard(target), target)

    def test_the_guard_returns_the_path_so_it_reads_as_a_checkpoint(self):
        target = REPO_ROOT / "docs/architecture/p12/x.json"
        self.assertEqual(sentinel.guard(target), Path(target))

    def test_p11_is_protected_and_p12_is_not(self):
        roots = [r.name for r in sentinel.protected_roots()]
        self.assertIn("p11", roots)
        self.assertNotIn("p12", roots)


class EveryWriterIntoCertifiedEvidenceIsGuarded(unittest.TestCase):
    """The covered population is measured, not listed.

    If a module gains a write into a certified phase's evidence root without
    routing it through the guard, this fails. That converts a hand-maintained
    set of call sites into a verified one — the drift becomes detectable instead
    of silent, which is the whole lesson of the identifier-class and
    citation-root defects.
    """

    @staticmethod
    def _modules():
        for path in sorted(REPO_ROOT.glob("tools/*.py")):
            yield path
        for path in sorted(REPO_ROOT.glob("*.py")):
            yield path

    def test_no_unguarded_writer_targets_a_certified_phase_root(self):
        certified = sentinel.certified_phases()
        markers = tuple(f"docs/architecture/p{n}" for n in sorted(certified))
        offenders = []
        for path in self._modules():
            source = path.read_text(encoding="utf-8")
            if not any(marker in source for marker in markers):
                continue
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if not (isinstance(node, ast.Attribute)
                        and node.attr in ("write_text", "write_bytes")):
                    continue
                # Per call site, not per module. The first version of this test
                # asked only whether the module imported the guard, and passed
                # while `_revoke_stale` mutated a certified delegation record
                # in place. A module-level check cannot see an unguarded call
                # inside a guarded module.
                receiver = node.value
                guarded = (
                    isinstance(receiver, ast.Call)
                    and isinstance(receiver.func, ast.Name)
                    and receiver.func.id == "guard"
                )
                if not guarded:
                    offenders.append(
                        f"{path.relative_to(REPO_ROOT)}:{node.lineno}")
        self.assertEqual(
            offenders, [],
            "these modules write into certified-phase evidence without the guard",
        )

    def test_the_check_can_actually_fail(self):
        """A conformance test that cannot fail proves nothing."""
        certified = sentinel.certified_phases()
        self.assertTrue(certified, "no certified phase — the check would be vacuous")
        markers = [f"docs/architecture/p{n}" for n in sorted(certified)]
        hits = [
            p.name for p in self._modules()
            if any(m in p.read_text(encoding="utf-8") for m in markers)
        ]
        self.assertTrue(hits, "no module references a certified root — vacuous")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()


class EveryCertifiedPhaseResolvesToARoot(unittest.TestCase):
    """A certified phase with no resolvable evidence root must fail loudly.

    P10 is certified, has no `docs/architecture/p10/`, and its certification
    package sits under `platform-organization/`. The first version of
    `protected_roots` skipped that phase silently and reported success — the
    guard's own failure mode, inside the guard.
    """

    def test_p10_evidence_root_is_protected(self):
        target = (REPO_ROOT / "docs/architecture/platform-organization"
                  / "E10-VERIFICATION-AND-P10-CERTIFICATION-PACKAGE.md")
        self.assertTrue(target.is_file(), "P10's certification package moved")
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            sentinel.guard(target)

    def test_both_certified_phases_have_a_protected_root(self):
        roots = sentinel.protected_roots()
        self.assertEqual(
            len(roots), len(sentinel.certified_phases()),
            "every certified phase must resolve to exactly one evidence root",
        )

    def test_an_unresolvable_certified_phase_raises_rather_than_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            (acts / "fd.md").write_text(
                "PHASE 99 — SOMETHING IS CERTIFIED.", encoding="utf-8")
            with self.assertRaises(sentinel.CertificationUndeterminable):
                sentinel.protected_roots(REPO_ROOT, acts)

    def test_the_declared_mapping_is_only_for_non_conventional_roots(self):
        """P11 follows `p{N}` and must not need a declaration."""
        self.assertNotIn(11, sentinel.PHASE_EVIDENCE_ROOTS)
        self.assertIn(10, sentinel.PHASE_EVIDENCE_ROOTS)


class AttributionAndAnomalyDetection(unittest.TestCase):
    """`ACT-CC-P12-022` — detection, explicitly not authentication.

    These establish a narrow property and its exact limit. Nothing here closes
    the forgery finding, and the last test exists to make sure no later reader
    believes it does.
    """

    def test_each_certified_phase_is_attributed_to_its_instrument(self):
        provenance = dict(sentinel.certification_provenance())
        self.assertEqual(set(provenance), {10, 11})
        self.assertTrue(provenance[10].startswith("FD-P10-005"))
        self.assertTrue(provenance[11].startswith("FD-P11-002"))

    def test_the_resident_corpus_raises_no_anomaly(self):
        """A detector that fires on the real corpus is noise, not a control."""
        self.assertEqual(sentinel.certification_anomalies(), ())

    def test_a_lone_planted_instrument_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            (acts / "FD-P42-001-FABRICATED.md").write_text(
                "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.",
                encoding="utf-8")
            anomalies = sentinel.certification_anomalies(acts)
        self.assertEqual(len(anomalies), 1)
        self.assertIn("phase 42", anomalies[0])

    def test_an_unreadable_register_makes_everything_anomalous(self):
        """`cannot check` and `checked and clean` are different answers."""
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "no-such-register.md"
            self.assertEqual(
                len(sentinel.certification_anomalies(
                    sentinel.ACTS_ROOT, missing)),
                len(sentinel.certification_provenance()))

    def test_a_bare_prefix_cannot_stand_in_for_an_instrument_identity(self):
        """`FD` appears in the Register constantly; it identifies nothing."""
        self.assertIsNone(sentinel._register_identity("FD", "FD everywhere"))
        self.assertIsNone(sentinel._register_identity("FORGED", "FORGED"))
        self.assertEqual(
            sentinel._register_identity("FD-P10-005-CERT", "see FD-P10-005 §1"),
            "FD-P10-005")

    def test_a_coordinated_forgery_still_defeats_it(self):
        """The limit, pinned so it is never quietly forgotten.

        `ACT-CC-P12-021` rejected a Register cross-check as a *resolution* and
        that rejection stands: the Register is a document in the same
        unprotected store. This raises the forgery's cost from one artifact to
        two. It does not authenticate, and `certified_phases` still believes
        the planted instrument.
        """
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp) / "acts"
            acts.mkdir()
            (acts / "FD-P42-001-FABRICATED.md").write_text(
                "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.",
                encoding="utf-8")
            register = Path(tmp) / "register.md"
            register.write_text("| `FD-P42-001` | forged | ISSUED |\n",
                                encoding="utf-8")
            self.assertEqual(sentinel.certification_anomalies(acts, register), ())
            self.assertIn(42, sentinel.certified_phases(acts))

    def test_no_forged_certification_relaxes_protection(self):
        """Monotonicity: injection expands the prohibition set or fails closed."""
        targets = [root / "probe.md" for root in sentinel.protected_roots()]
        baseline = [sentinel.is_protected(t) for t in targets]
        self.assertTrue(all(baseline))
        for statement in ("PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.",
                          "PHASE 12 — AI OPERATING SYSTEM IS CERTIFIED.",
                          "PHASE 11 — ANYTHING AT ALL IS CERTIFIED."):
            with tempfile.TemporaryDirectory() as tmp:
                copy = Path(tmp) / "acts"
                shutil.copytree(sentinel.ACTS_ROOT, copy)
                (copy / "FORGED.md").write_text(statement, encoding="utf-8")
                try:
                    after = [sentinel.is_protected(t, sentinel.REPO_ROOT, copy)
                             for t in targets]
                except sentinel.CertificationUndeterminable:
                    continue          # fail-closed: nothing became permitted
            self.assertTrue(all(after), f"protection relaxed by: {statement}")


class TheWarrantIsProtectedAndNotOnlyTheEvidence(unittest.TestCase):
    """`ACT-CC-P12-025 §4 A2` — the gap in `F-12`'s own artifact.

    The guard protected every certified phase's evidence and left the
    instruments conferring that certification writable. Overwrite
    `FD-P11-002` and `docs/architecture/p11` stops being protected at all: the
    evidence was guarded and its warrant was not.
    """

    def test_both_certifying_instruments_are_protected(self):
        for instrument in sentinel.protected_instruments():
            with self.subTest(instrument.name):
                with self.assertRaises(sentinel.CertifiedEvidenceProtected):
                    sentinel.guard(instrument)

    def test_the_set_is_derived_from_what_certifies_not_listed(self):
        derived = {p.name for p in sentinel.protected_instruments()}
        stated = {name for _, name in sentinel.certification_provenance()}
        self.assertEqual(derived, stated)
        source = Path(sentinel.__file__).read_text(encoding="utf-8")
        self.assertNotIn("FD-P11-002-P11-CERTIFICATION.md\"", source)

    def test_an_instrument_becomes_protected_by_certifying(self):
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            planted = acts / "FD-P42-001-NEW.md"
            planted.write_text("PHASE 42 — SOMETHING IS CERTIFIED.",
                               encoding="utf-8")
            self.assertIn(planted, sentinel.protected_instruments(acts))

    def test_an_ordinary_act_stays_writable(self):
        """Protecting the whole acts root would refuse the corpus's own work."""
        ordinary = (sentinel.ACTS_ROOT
                    / "ACT-CC-P12-019-P12-COMPLETION-AUTHORITY-DELEGATION.md")
        self.assertTrue(ordinary.is_file())
        self.assertEqual(sentinel.guard(ordinary), ordinary)

    def test_p12_working_files_stay_writable(self):
        working = sentinel.REPO_ROOT / "docs/architecture/p12/probe.md"
        self.assertEqual(sentinel.guard(working), working)

    def test_this_does_not_touch_the_forgery_finding(self):
        """Overwriting an instrument and planting one are different acts.

        Pinned so no later reader reads this as progress on `§6.8` or `§6.9`.
        A planted instrument is still believed; only overwriting an existing
        certifying one is now refused.
        """
        with tempfile.TemporaryDirectory() as tmp:
            acts = Path(tmp)
            (acts / "FD-P42-001-FABRICATED.md").write_text(
                "PHASE 42 — FABRICATED ECOSYSTEM IS CERTIFIED.",
                encoding="utf-8")
            self.assertIn(42, sentinel.certified_phases(acts))
