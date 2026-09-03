"""
R2-C acceptance evidence — three derived views, and no second source of truth.

`ACT-CC-R2BC-IMPL-001 §19` fixes the property these tests exist to protect: *a
derived view is not a second source of truth.* So the suite checks two things
about every view — that it answers, and that it owns nothing. A view that
cached a fact and drifted from its source would pass the first and fail the
second, which is why both are asserted.

`§28` requires `VERIFIED`, `INFERRED` and `UNKNOWN` stay distinguishable, and
`§27` states that returning `UNKNOWN` is *correct* where evidence is absent.
`TheProjectionDeclinesToGuess` is therefore an acceptance test, not a list of
deficiencies.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.derived_views import (
    INFERRED,
    REGISTER,
    UNKNOWN,
    VERIFIED,
    BoundaryEdge,
    Fact,
    LineageEdge,
    boundary_consumers,
    decision_lineage,
    graph_is_acyclic,
    interface_graph,
    self_knowledge,
    unbridged_gates,
)
from tools.governance_index import REPO_ROOT


class DecisionLineageIsDerived(unittest.TestCase):
    """`§20`–`§22`, `§30` — the `FD-n ↔ GDR-nnnn` bridge, derived not stored."""

    def setUp(self):
        self.edges = decision_lineage()

    def test_the_bridge_exists_and_is_non_empty(self):
        self.assertTrue(self.edges, "the Register states gate registrations")

    def test_every_edge_carries_a_source_locator(self):
        """`§22` — no field is invented; each edge points at the line that
        states it."""
        for edge in self.edges:
            self.assertTrue(edge.source.startswith(REGISTER), edge.source)
            self.assertIn(":", edge.source)

    def test_each_edge_is_literally_stated_by_its_heading(self):
        """`§21` — the relationship is read, never reconstructed. Both halves of
        every edge appear verbatim in the heading it came from."""
        for edge in self.edges:
            self.assertIn(edge.gate, edge.heading)
            self.assertIn(edge.registered_as, edge.heading)

    def test_a_known_registration_is_discoverable(self):
        """`ACT-CC-R1-003` established this one from source: FD-4 was registered
        as GDR-0017. The view finds it without being told."""
        pairs = {(e.gate, e.registered_as) for e in self.edges}

        self.assertIn(("FD-4", "GDR-0017"), pairs)
        self.assertIn(("FD-3", "GDR-0018"), pairs)

    def test_unbridged_gates_are_reported_not_resolved(self):
        """`§30` — unproven relationships stay unproven. Most of these are open
        decision gates that were never decided, and an absent registration is
        the correct state for an unanswered question."""
        unbridged = unbridged_gates()

        self.assertIsInstance(unbridged, list)
        for gate in unbridged:
            self.assertNotIn(gate, {e.gate for e in self.edges})

    def test_it_creates_no_second_decision_source(self):
        """`§30` — the view holds no decision content, only identifiers and
        locators pointing back at the Register."""
        for edge in self.edges:
            self.assertEqual(
                set(LineageEdge.__dataclass_fields__),
                {"gate", "registered_as", "heading", "source"},
            )


class InterfaceGraphIsDerived(unittest.TestCase):
    """`§23`–`§25`, `§31` — regenerated from source, never hand-maintained."""

    def setUp(self):
        self.graph = interface_graph()

    def test_the_graph_is_non_empty_and_structural(self):
        self.assertTrue(self.graph)
        for edge in self.graph:
            self.assertEqual("imports", edge.relationship)

    def test_it_is_regenerable_and_deterministic(self):
        """`§25` — identical source yields identical graph, which is what makes
        it a projection rather than a stored artifact."""
        self.assertEqual(self.graph, interface_graph())

    def test_it_preserves_dependency_direction(self):
        """`§31` — direction is not symmetric. Runtime reaches Workflow; the
        reverse edge does not exist, and the graph says so."""
        pairs = {(e.source, e.target) for e in self.graph}

        self.assertIn(("runtime", "workflow"), pairs)
        self.assertNotIn(("workflow", "runtime"), pairs)

    def test_it_reports_the_acyclic_invariant(self):
        self.assertTrue(graph_is_acyclic())

    def test_no_core_boundary_reaches_trace(self):
        """The R2-A boundary result, now queryable: Trace is authored from
        `consumers/`, and no core boundary imports it."""
        pairs = {(e.source, e.target) for e in self.graph}

        for boundary in ("runtime", "workflow", "agent"):
            self.assertNotIn((boundary, "trace"), pairs)

    def test_unconsumed_boundaries_are_reported_not_judged(self):
        """`§24` — the view reports structure. That `capability`, `skill` and
        `optimization` have no consumer is canonical design, and this view has
        no standing to relabel it a defect."""
        consumers = boundary_consumers()

        self.assertEqual((), consumers["capability"])
        self.assertEqual((), consumers["skill"])
        self.assertEqual((), consumers["optimization"])

    def test_it_reflects_implementation_not_an_idealized_architecture(self):
        """`§53` — derived from real imports, so it cannot describe a boundary
        relationship the code does not actually have."""
        pairs = {(e.source, e.target) for e in self.graph}

        self.assertIn(("memory", "trace"), pairs)      # memory reads Trace
        self.assertNotIn(("trace", "memory"), pairs)   # and Trace does not read Memory


class SelfKnowledgeIsProjected(unittest.TestCase):
    """`§26`–`§29`, `§32` — a projection over sources, owning none of them."""

    def setUp(self):
        self.projection = self_knowledge()

    def test_it_answers_what_the_sources_support(self):
        for question in ("what exists", "what decisions are recorded",
                         "what is verified", "what is stale"):
            fact = self.projection.answer(question)
            self.assertEqual(VERIFIED, fact.status, question)
            self.assertIsNotNone(fact.value, question)

    def test_every_answer_names_its_source(self):
        """`§29` — the projection points at authority; it does not become one."""
        for fact in self.projection.facts:
            if fact.is_known:
                self.assertTrue(fact.source, fact.question)

    def test_staleness_comes_from_the_ledger(self):
        """`§32` — staleness is answerable because R2-B worked the Ledger. The
        projection reads it; it does not maintain its own staleness state."""
        fact = self.projection.answer("what is stale")

        self.assertIn("Ledger", fact.source)
        self.assertIn("S-9", fact.value["open_synchronizations"])
        self.assertIn("S-13", fact.value["open_synchronizations"])

    def test_evidence_status_is_not_collapsed(self):
        """`§28` — three distinct statuses, all present and meaningful."""
        statuses = {f.status for f in self.projection.facts}

        self.assertIn(VERIFIED, statuses)
        self.assertIn(INFERRED, statuses)
        self.assertIn(UNKNOWN, statuses)

    def test_an_inferred_answer_is_labelled_inferred(self):
        """The unbridged-gate list is derived, not stated, so it must not claim
        VERIFIED."""
        self.assertEqual(INFERRED, self.projection.answer("what is unbridged").status)

    def test_it_is_deterministic_over_unchanged_sources(self):
        again = self_knowledge()

        self.assertEqual(self.projection.questions, again.questions)


class TheProjectionDeclinesToGuess(unittest.TestCase):
    """`§27` — `UNKNOWN` is the correct answer where evidence is absent. These
    are acceptance criteria, not a defect list."""

    def test_what_is_running_is_unknown_and_says_why(self):
        fact = self_knowledge().answer("what is running")

        self.assertEqual(UNKNOWN, fact.status)
        self.assertIn("per-process", fact.source)

    def test_run_and_failure_history_is_unknown_without_a_reader(self):
        projection = self_knowledge()

        self.assertEqual(UNKNOWN, projection.answer("what has run").status)
        self.assertEqual(UNKNOWN, projection.answer("what has failed").status)

    def test_an_unasked_question_returns_unknown_rather_than_raising(self):
        fact = self_knowledge().answer("what will happen next")

        self.assertEqual(UNKNOWN, fact.status)
        self.assertIsNone(fact.value)

    def test_unknowns_are_enumerable(self):
        self.assertTrue(self_knowledge().unknowns())


class ItConsumesR2AEvidenceWithoutOwningIt(unittest.TestCase):
    """`§51` — the observation axis feeds the projection, and the projection
    stores nothing it was handed."""

    def _trace_reader_with(self, statuses):
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.trace import TraceReader, TraceWriter, new_record

        storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
        storage.provision()
        writer = TraceWriter(storage)
        for status in statuses:
            writer.write(
                new_record(
                    agent_definition_version="v1",
                    agent_instance="probe",
                    runtime="rt",
                    outputs={},
                    status=status,
                )
            )
        return TraceReader(storage)

    def test_run_history_becomes_known_when_a_reader_is_supplied(self):
        reader = self._trace_reader_with(("success", "failure", "success"))

        projection = self_knowledge(trace_reader=reader)

        self.assertEqual(VERIFIED, projection.answer("what has run").status)
        self.assertEqual(3, projection.answer("what has run").value)

    def test_failure_history_is_answerable_from_durable_evidence(self):
        """The R2-A property, consumed: failures persisted by an Agent action
        are readable back as system self-knowledge."""
        reader = self._trace_reader_with(("success", "failure", "failure"))

        failures = self_knowledge(trace_reader=reader).answer("what has failed")

        self.assertEqual(VERIFIED, failures.status)
        self.assertEqual(2, len(failures.value))

    def test_supplying_a_reader_does_not_make_the_projection_authoritative(self):
        """Two projections over the same reader agree because they both read it
        — not because either cached it."""
        reader = self._trace_reader_with(("success",))

        first = self_knowledge(trace_reader=reader).answer("what has run")
        second = self_knowledge(trace_reader=reader).answer("what has run")

        self.assertEqual(first.value, second.value)


class NoParallelSourceOfTruth(unittest.TestCase):
    """`§38` — derived views may exist; parallel authoritative stores may not."""

    def test_the_module_writes_nothing(self):
        """AST: no file write, no persistence call anywhere in the module."""
        import ast

        source = (REPO_ROOT / "tools" / "derived_views.py").read_text()
        forbidden = {"write", "write_text", "dump", "save", "persist"}
        called = {
            node.func.attr
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }

        self.assertEqual(set(), called & forbidden)

    def test_it_holds_no_module_level_state(self):
        """Nothing accumulates between calls, so nothing can drift from its
        source."""
        import ast

        source = (REPO_ROOT / "tools" / "derived_views.py").read_text()
        assigned = [
            target.id
            for node in ast.parse(source).body
            if isinstance(node, ast.Assign)
            for target in node.targets
            if isinstance(target, ast.Name)
        ]

        for name in assigned:
            self.assertTrue(name.isupper(), f"{name} is mutable module state")

    def test_deleting_the_view_would_lose_no_truth(self):
        """Every value the projection reports is recomputed from a source it
        names — the property that keeps it a projection."""
        for fact in self_knowledge().facts:
            if fact.is_known:
                self.assertTrue(fact.source)


if __name__ == "__main__":
    unittest.main()
