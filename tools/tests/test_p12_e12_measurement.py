"""`ACT-CC-P12-019 §19` / `ACT-CC-P12-020 §11` — falsification of the `E12-01`…
`E12-05` measurement.

**Fifteen clauses all reading `ok` is what a module returning constants would
print**, and this module reached that state only after three defects in its own
first run were corrected. Every clause is therefore driven **down** here: the
evidence it reads is removed or corrupted and the clause must report `NO`.

The three corrected defects each get a regression test, because two of them
produced a **false FAIL** — the instrument reported the system failing when the
instrument could not read — and the corpus's standing invariant is
`UNKNOWN ≠ FALSE`.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_e12_measurement as m

REPO_ROOT = Path(__file__).resolve().parents[2]


def _clauses(results, criterion):
    return {c.letter: c for r in results if r.criterion == criterion
            for c in r.clauses}


class TheDecisionRecordIsLoadBearing(unittest.TestCase):
    """`ACT-CC-P12-020 §7` — the module supplies no boundary of its own."""

    def test_no_record_raises_rather_than_measuring(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(m.AcceptanceBoundaryUnavailable):
                m.measure(Path(tmp))

    def test_a_record_that_does_not_cite_the_delegation_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / m.DECISION_RECORD
            target.parent.mkdir(parents=True, exist_ok=True)
            body = (REPO_ROOT / m.DECISION_RECORD).read_text(encoding="utf-8")
            target.write_text(body.replace(m.DELEGATION_INSTRUMENT, "SOMETHING"),
                              encoding="utf-8")
            with self.assertRaises(m.AcceptanceBoundaryUnavailable) as raised:
                m.measure(Path(tmp))
        self.assertIn("has no authority", str(raised.exception))

    def test_a_non_ratify_decision_yields_no_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / m.DECISION_RECORD
            target.parent.mkdir(parents=True, exist_ok=True)
            body = (REPO_ROOT / m.DECISION_RECORD).read_text(encoding="utf-8")
            target.write_text(
                body.replace("| **Decision** | **RATIFY AS PROPOSED** |",
                             "| **Decision** | **DEFER** |"), encoding="utf-8")
            with self.assertRaises(m.AcceptanceBoundaryUnavailable) as raised:
                m.measure(Path(tmp))
        self.assertIn("DEFER", str(raised.exception))

    def test_the_live_record_resolves_all_five(self):
        decided = m.decided_boundaries()
        self.assertEqual(set(m.CRITERIA), set(decided))
        for criterion, record in decided.items():
            with self.subTest(criterion):
                self.assertTrue(record["decision"].upper().startswith("RATIFY"))
                self.assertEqual(3, len(record["clauses"]))


class UnreadableEvidenceIsUnknownNotFailure(unittest.TestCase):
    """The regression test for this module's own worst defect.

    Two clauses originally guessed an accessor name, guarded it with `hasattr`
    or a `.get(..., default)`, and **failed closed into a `NO`** — reporting the
    system as failing when the instrument could not read it. `UNKNOWN ≠ FALSE`.
    """

    def test_a_raising_clause_reports_unknown_not_not_satisfied(self):
        def explode(root):
            raise RuntimeError("evidence source unavailable")
        with mock.patch.dict(m._CLAUSES, {"E12-01": explode}):
            results = {r.criterion: r for r in m.measure()}
        self.assertEqual(m.UNKNOWN, results["E12-01"].verdict)
        self.assertIn("evidence unreadable", results["E12-01"].evidence)
        self.assertNotEqual(m.NOT_SATISFIED, results["E12-01"].verdict)

    def test_a_missing_contract_key_raises_rather_than_failing(self):
        from tools import p12_self_model_contract as contract
        with mock.patch.object(contract, "summary", return_value={}):
            results = {r.criterion: r for r in m.measure()}
        self.assertEqual(m.UNKNOWN, results["E12-05"].verdict)

    def test_a_clause_count_mismatch_is_unknown(self):
        def two_clauses(root):
            return (m.ClauseResult("a", True, "x"), m.ClauseResult("b", True, "y"))
        with mock.patch.dict(m._CLAUSES, {"E12-02": two_clauses}):
            results = {r.criterion: r for r in m.measure()}
        self.assertEqual(m.UNKNOWN, results["E12-02"].verdict)


class E12_01_ClausesCanFail(unittest.TestCase):
    def test_a_missing_edge_attribute_fails_clause_a(self):
        from tools import p12_integration_graph as graph
        edges = list(graph.graph())
        broken = edges[0].__class__(**{**edges[0].__dict__, "owner": ""})
        with mock.patch.object(graph, "graph", return_value=(broken,) + tuple(edges[1:])):
            clauses = _clauses(m.measure(), "E12-01")
        self.assertFalse(clauses["a"].satisfied)

    def test_removing_the_platform_edge_uncovers_a_layer_and_fails_clause_b(self):
        """The corrected clause still fails when a layer really is uncovered.

        `PLATFORM` is covered only by the `platform ↔ phase` edge endpoint
        `Platform Organization`. Drop it and the clause must report it — which
        is what proves the word-matching fix did not simply make (b) true.
        """
        from tools import p12_integration_graph as graph
        kept = tuple(e for e in graph.graph()
                     if e.integration_class != "platform ↔ phase")
        with mock.patch.object(graph, "graph", return_value=kept):
            clauses = _clauses(m.measure(), "E12-01")
        self.assertFalse(clauses["b"].satisfied)
        self.assertIn("PLATFORM", clauses["b"].observation)

    def test_a_bare_unknown_matrix_cell_fails_clause_b(self):
        from tools import p12_phase_verification_matrix as matrix
        rows = list(matrix.rows())
        bare = rows[0].__class__(**{**rows[0].__dict__, "owner": "UNKNOWN"})
        with mock.patch.object(matrix, "rows", return_value=(bare,) + tuple(rows[1:])):
            clauses = _clauses(m.measure(), "E12-01")
        self.assertFalse(clauses["b"].satisfied)

    def test_an_asserted_provider_relation_fails_clause_c(self):
        from tools import p12_integration_graph as graph
        edges = list(graph.graph())
        claimed = edges[0].__class__(**{**edges[0].__dict__,
                                        "owner": "PD-04 Knowledge"})
        with mock.patch.object(graph, "graph", return_value=(claimed,) + tuple(edges[1:])):
            clauses = _clauses(m.measure(), "E12-01")
        self.assertFalse(clauses["c"].satisfied)


class E12_02_ClausesCanFail(unittest.TestCase):
    def test_a_broken_chain_link_fails_clause_a(self):
        from tools import p12_state_verification as chain
        with mock.patch.object(chain, "summary", return_value={
                "links": 4, "satisfied": 3, "chain_complete": False,
                "broken_links": ("memory",)}):
            clauses = _clauses(m.measure(), "E12-02")
        self.assertFalse(clauses["a"].satisfied)

    def test_a_state_authority_conflict_fails_clause_b(self):
        from tools import p12_operational_state as state
        live = state.summary()
        with mock.patch.object(state, "summary",
                               return_value={**live, "conflicts": 1}):
            clauses = _clauses(m.measure(), "E12-02")
        self.assertFalse(clauses["b"].satisfied)

    def test_an_unclassified_projection_fails_clause_c(self):
        from tools import p12_operational_state as state
        live = state.summary()
        with mock.patch.object(state, "summary", return_value={
                **live, "current": live["current"] - 1}):
            clauses = _clauses(m.measure(), "E12-02")
        self.assertFalse(clauses["c"].satisfied)


class E12_03_ClausesCanFail(unittest.TestCase):
    def test_a_stale_governance_source_fails_clause_a(self):
        from tools import governance_index as index
        built, _ = index.GovernanceIndex.build(index.tracked_markdown(REPO_ROOT),
                                               REPO_ROOT)
        with mock.patch.object(built.__class__, "stale_sources",
                               return_value=("some-source.md",)):
            clauses = _clauses(m.measure(), "E12-03")
        self.assertFalse(clauses["a"].satisfied)

    def test_no_enforcement_control_fails_clause_b(self):
        from tools import p12_system_negative_controls as controls
        with mock.patch.object(controls, "verify", return_value=()):
            clauses = _clauses(m.measure(), "E12-03")
        self.assertFalse(clauses["b"].satisfied)

    def test_no_structural_join_fails_clause_c(self):
        from tools import p12_governance_join_reader as joins
        with mock.patch.object(joins, "resolve_all", return_value=()):
            clauses = _clauses(m.measure(), "E12-03")
        self.assertFalse(clauses["c"].satisfied)


class E12_04_ClausesCanFail(unittest.TestCase):
    def test_a_dangling_chain_fails_clause_a(self):
        from tools import p12_execution_chain_reader as chain
        live = chain.summary()
        with mock.patch.object(chain, "summary",
                               return_value={**live, "dangling": 1}):
            clauses = _clauses(m.measure(), "E12-04")
        self.assertFalse(clauses["a"].satisfied)

    def test_an_elided_work_scope_fails_clause_b(self):
        """The corrected clause still fails when `WORK` really is elided —
        which is what proves reading the right accessor did not simply make
        (b) true."""
        from tools import p12_execution_provenance as provenance
        live = list(provenance.manifests())
        stripped = {**live[0], "work_scope": []}
        with mock.patch.object(provenance, "manifests",
                               return_value=(stripped,) + tuple(live[1:])):
            clauses = _clauses(m.measure(), "E12-04")
        self.assertFalse(clauses["b"].satisfied)

    def test_no_manifest_at_all_fails_clause_b(self):
        from tools import p12_execution_provenance as provenance
        with mock.patch.object(provenance, "manifests", return_value=()):
            clauses = _clauses(m.measure(), "E12-04")
        self.assertFalse(clauses["b"].satisfied)

    def test_a_demonstrator_only_phase_fails_clause_c(self):
        from tools import p12_cross_phase_verification as cross
        live = cross.summary()
        with mock.patch.object(cross, "summary", return_value={
                **live, "exercised_only_by_a_demonstrator": ("P4",)}):
            clauses = _clauses(m.measure(), "E12-04")
        self.assertFalse(clauses["c"].satisfied)


class E12_05_ClausesCanFail(unittest.TestCase):
    def test_an_unanswered_question_fails_clause_a(self):
        from tools import p12_self_model as model
        with mock.patch.object(model, "coverage", return_value={
                "questions": 12, "verified": 9, "inferred": 2, "unknown": 0}):
            clauses = _clauses(m.measure(), "E12-05")
        self.assertFalse(clauses["a"].satisfied)

    def test_an_unbound_answer_fails_clause_b(self):
        """The corrected clause still fails on a real unbound answer — which is
        what proves reading the right key did not simply make (b) true."""
        from tools import p12_self_model_contract as contract
        live = contract.summary()
        with mock.patch.object(contract, "summary", return_value={
                **live, "unbound_answers": ("What is running?",)}):
            clauses = _clauses(m.measure(), "E12-05")
        self.assertFalse(clauses["b"].satisfied)

    def test_a_self_model_that_grants_a_permission_fails_clause_c(self):
        """`SELF-MODEL ≠ AUTHORITY`, driven against a source that breaks it."""
        source = (REPO_ROOT / "tools" / "p12_self_model.py").read_text(
            encoding="utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tools").mkdir(parents=True)
            (root / "tools" / "p12_self_model.py").write_text(
                source + "\n\ndef authorize_everything():\n    return True\n",
                encoding="utf-8")
            clauses = m._e12_05(root)
        self.assertFalse({c.letter: c for c in clauses}["c"].satisfied)


class TheLiveDetermination(unittest.TestCase):
    """Pinned exactly. A criterion regressing must fail here."""

    def test_all_five_are_satisfied_on_the_live_corpus(self):
        found = m.determination()
        self.assertEqual((), found["not_satisfied"])
        self.assertEqual((), found["unknown"])
        self.assertEqual(5, found["satisfied"])

    def test_every_result_carries_its_delegated_authority(self):
        found = m.determination()
        self.assertEqual("DECISION MADE UNDER ACT-CC-P12-019", found["note"])
        self.assertIn("ACT-CC-P12-019", found["authority"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
