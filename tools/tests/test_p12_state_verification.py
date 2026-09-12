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

    def test_the_projection_currently_has_no_consumer(self):
        self.assertEqual(sv.consumers_of("tools.p12_operational_state"), (),
                         "if a consumer has been wired, the STATE item's "
                         "classification must be updated rather than this "
                         "control relaxed")

    def test_a_real_consumer_is_found_when_one_exists(self):
        """The check must be able to report SATISFIED."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "surface.py").write_text("X = 1\n", encoding="utf-8")
            (root / "reader.py").write_text("import surface\n", encoding="utf-8")
            with mock.patch.object(sv, "REPO_ROOT", root):
                self.assertEqual(sv.consumers_of("surface"), ("reader.py",))


class EachLinkCanBeDrivenToUnsatisfied(unittest.TestCase):
    """Three satisfied links is a measurement only if they can fail."""

    def test_the_consumer_link_is_unsatisfied_on_the_live_corpus(self):
        result = {r.link: r for r in sv.verify()}["CONSUMER"]
        self.assertEqual(result.status, sv.UNSATISFIED)
        self.assertIn("nothing reads", result.detail)

    def test_the_consumer_link_is_satisfied_when_a_consumer_exists(self):
        with mock.patch.object(sv, "consumers_of",
                               return_value=("tools/somewhere.py",)):
            self.assertEqual(sv._link_consumer().status, sv.SATISFIED)

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


class TheItemIsNotClosed(unittest.TestCase):
    """`ACT-CC-P12-W2-001 §48`: W2 must not be assumed to close it."""

    def test_the_chain_is_incomplete(self):
        summary = sv.summary()
        self.assertFalse(summary["chain_complete"])
        self.assertEqual(summary["broken_links"], ("CONSUMER",))

    def test_three_of_four_links_are_satisfied(self):
        self.assertEqual(sv.summary()["satisfied"], 3)

    def test_no_authority_conflict_is_outstanding(self):
        self.assertEqual(sv.summary()["authority_conflicts"], 0)
        self.assertEqual(sv.summary()["undeclared_claims"], 0)


if __name__ == "__main__":
    unittest.main()
