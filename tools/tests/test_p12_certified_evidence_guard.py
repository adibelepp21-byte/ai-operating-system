"""P12-W3 — certification enforced across layers (`F-12`).

The controls that matter are that certification is read from **instrument
bodies** rather than prose or filenames, that the guard fails **closed** when
governance cannot be read, and that the set of writers it covers is **verified
rather than remembered** — a hand-kept list of guarded call sites is the same
stale-population defect this programme has corrected repeatedly.
"""

from __future__ import annotations

import ast
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
