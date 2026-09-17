"""P12-W6 state verification conformance (`§17`, `§19` scope `STATE`)."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

from tools import p12_state_verification as sv


class TheScopeIsSection17s(unittest.TestCase):
    def test_the_chain_is_section_17s_in_order(self):
        self.assertEqual(list(sv.STATE_CHAIN),
                         ["STATE", "AUTHORITATIVE SOURCE", "PROJECTION",
                          "CONSUMER"])

    def test_every_link_has_a_probe(self):
        self.assertEqual(set(sv._LINKS), set(sv.STATE_CHAIN))


class W6ReadsW2AsDataAndStaysDiagnostic(unittest.TestCase):
    """`§22`: `W2 ≠ W6`. The verifier builds nothing and repairs nothing."""

    def test_the_surface_is_not_imported_at_module_scope(self):
        import ast
        source = (sv.REPO_ROOT / "tools" / "p12_state_verification.py"
                  ).read_text(encoding="utf-8")
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        self.assertNotIn("tools.p12_operational_state", imported)

    def test_it_writes_nothing(self):
        import ast
        source = (sv.REPO_ROOT / "tools" / "p12_state_verification.py"
                  ).read_text(encoding="utf-8")
        names = {n.func.attr for n in ast.walk(ast.parse(source))
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        for forbidden in ("write_text", "mkdir", "unlink", "replace"):
            self.assertNotIn(forbidden, names)


class AConformanceSuiteIsNotAConsumer(unittest.TestCase):
    """Counting tests is how a surface nothing uses looks integrated."""

    def test_test_modules_are_excluded(self):
        found = sv.consumers_of("tools.p12_operational_state")
        self.assertFalse([c for c in found if "test" in c])

    def test_the_evidenced_consumer_set_is_exactly_this(self):
        """Pinned, so the set cannot drift in either direction unnoticed.

        Its predecessor asserted the set was **empty** and said in its own
        message: *"if a consumer has been wired, the STATE item's
        classification must be updated rather than this control relaxed."*
        `ACT-CC-P12-008` did the first half — no consumer was wired, a
        measurement defect was corrected — and this is the second half. The
        assertion is still exact, so a consumer appearing or disappearing still
        fails here.

        `ACT-CC-P12-019` added the third: `p12_e12_measurement` reads the
        surface in its `E12-02` clause. It was **registered with the
        independent consumer verifier** at the same time, so the consumption is
        observed rather than merely claimed — a static importer the dynamic
        harness cannot drive would otherwise read as a permanent DISAGREES."""
        self.assertEqual(
            sv.consumers_of("tools.p12_operational_state"),
            ("tools/p12_e12_measurement.py",
             "tools/p12_negative_control_verification.py",
             "tools/p12_self_model_contract.py"))

    def test_an_importer_that_never_reads_is_not_counted(self):
        """`§16`: *"Each claimed consumer requires evidence that it actually
        consumes the state."* `tools/p12_mutation_verification.py` imports the
        surface and calls its projection only over a substituted source set —
        it reads its own fixture, never the system's state."""
        target = "tools.p12_operational_state"
        self.assertIn("tools/p12_mutation_verification.py",
                      sv.importers_of(target))
        self.assertNotIn("tools/p12_mutation_verification.py",
                         sv.consumers_of(target))
        evidence = {e.module: e for e in sv.consumption_evidence(target)}
        probe = evidence["tools/p12_mutation_verification.py"]
        self.assertEqual((), probe.reads)
        self.assertEqual(("conflicts",), probe.fixture_reads)

    def test_a_real_consumer_is_found_when_one_exists(self):
        """The check must be able to report SATISFIED — on a read, not on an
        import, which is the whole of what `ACT-CC-P12-008` corrected."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "surface.py").write_text("def project():\n    return ()\n",
                                             encoding="utf-8")
            (root / "reader.py").write_text(
                "import surface\nENTRIES = surface.project()\n",
                encoding="utf-8")
            (root / "importer.py").write_text("import surface\n",
                                              encoding="utf-8")
            with mock.patch.object(sv, "REPO_ROOT", root):
                self.assertEqual(sv.consumers_of("surface"), ("reader.py",))
                self.assertEqual(sv.importers_of("surface"),
                                 ("importer.py", "reader.py"))


class EachLinkCanBeDrivenToUnsatisfied(unittest.TestCase):
    """Three satisfied links is a measurement only if they can fail."""

    def test_the_consumer_link_is_satisfied_on_the_live_corpus(self):
        result = {r.link: r for r in sv.verify()}["CONSUMER"]
        self.assertEqual(result.status, sv.SATISFIED)
        self.assertIn("evidenced consumer", result.detail)

    def test_the_consumer_link_is_unsatisfied_when_nothing_reads(self):
        """The direction this class exists for. Driven down two ways, because
        an empty corpus and a corpus of importers-that-never-read are different
        failures and only the second exercises `§16`'s evidence requirement."""
        importer_only = (sv.ConsumerEvidence("tools/never-reads.py",
                                             reads=(), fixture_reads=()),)
        with mock.patch.object(sv, "consumption_evidence",
                               return_value=importer_only):
            result = sv._link_consumer()
        self.assertEqual(result.status, sv.UNSATISFIED)
        self.assertIn("import it without reading it", result.detail)
        with mock.patch.object(sv, "consumption_evidence", return_value=()):
            self.assertEqual(sv._link_consumer().status, sv.UNSATISFIED)

    def test_an_unresolved_source_path_breaks_the_source_link(self):
        from tools import p12_operational_state as state
        broken = state.SOURCES + (state.StateSource(
            state_id="ghost", state_class="RUNTIME",
            semantics=state.SOURCE_OF_TRUTH, owner="none",
            canonical_source="none", read_path="no/such/place",
            authority="none", freshness_model="none",
            owns_within_class="nothing"),)
        with mock.patch.object(state, "SOURCES", broken):
            self.assertEqual(sv._link_authoritative_source().status,
                             sv.UNSATISFIED)

    def test_a_projection_without_provenance_breaks_the_projection_link(self):
        from tools import p12_operational_state as state
        stripped = tuple(
            state.StateEntry(
                state_id=e.state_id, state_class=e.state_class,
                status=e.status, value=e.value, source="",
                observed_at=e.observed_at, transformation=e.transformation,
                authority=e.authority, provider=e.provider,
                semantics=e.semantics)
            for e in state.project())
        with mock.patch.object(state, "project", return_value=stripped):
            self.assertEqual(sv._link_projection().status, sv.UNSATISFIED)

    def test_a_raising_link_is_unavailable_not_satisfied(self):
        def explode():
            raise RuntimeError("surface unreadable")

        with mock.patch.dict(sv._LINKS, {"CONSUMER": explode}):
            result = {r.link: r for r in sv.verify()}["CONSUMER"]
        self.assertEqual(result.status, sv.UNAVAILABLE)


class TheItemIsClosedByMeasurementNotByAssumption(unittest.TestCase):
    """`ACT-CC-P12-W2-001 §48`: W2 must not be **assumed** to close it.

    That rule is about who decides and on what basis, and it is still honoured:
    W2 built the surface and claimed nothing; W6 measured it and decided. What
    changed under `ACT-CC-P12-008` is the measurement, not the standard — the
    fourth link reported UNSATISFIED for as long as the instrument could not
    see the shape every resident importer actually uses.
    """

    def test_the_chain_is_complete(self):
        summary = sv.summary()
        self.assertTrue(summary["chain_complete"])
        self.assertEqual(summary["broken_links"], ())

    def test_four_of_four_links_are_satisfied(self):
        self.assertEqual(sv.summary()["satisfied"], 4)

    def test_closure_rests_on_evidence_that_can_be_withdrawn(self):
        """Four of four is a measurement only if the fourth can still fail."""
        with mock.patch.object(sv, "consumption_evidence", return_value=()):
            summary = sv.summary()
        self.assertFalse(summary["chain_complete"])
        self.assertEqual(summary["broken_links"], ("CONSUMER",))

    def test_no_authority_conflict_is_outstanding(self):
        self.assertEqual(sv.summary()["authority_conflicts"], 0)
        self.assertEqual(sv.summary()["undeclared_claims"], 0)


if __name__ == "__main__":
    unittest.main()
