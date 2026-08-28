"""
Phase 6 behavioural evidence — *"Agent dapat mengambil dan memperbarui
pengetahuan tervalidasi"* (Master Program Volume II §4.3).

Five demonstrations, per `ACT-CC-P6-073 §13`:

  1. an Agent obtains an admitted Knowledge version;
  2. an Agent updates Knowledge through the governed path;
  3. unauthorized updates are rejected;
  4. unadmitted knowledge cannot be treated as validated;
  5. version and history semantics remain intact.

BOUNDARIES OBSERVED.
  - The Knowledge and Agent boundaries are **not modified**. This module adds a
    caller and observes it; every collaborator is an existing certified
    implementation, constructed through its own public surface.
  - The Governance stack is the resident `governance/tests/` convention —
    Infrastructure → Trace → Memory → Governance in a temp directory — because
    `GovernanceReview` cannot be constructed without a `StorageFacility` and
    `admit` requires a real `GovernanceReview` by `isinstance`. That is the
    established convention, not new storage architecture, and it ratifies
    nothing about `T12-D-004`.
  - The Knowledge side is assembled from **in-memory** reference
    implementations. No Knowledge persistence is created.
  - Evidence is taken from **call paths and observed state**, never from method
    names (`§13`).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consumers.knowledge_agent import KnowledgeConsumingAgent
from native_core.core.governance import GovernanceReview, HumanAuthority, ReviewDecision
from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.knowledge.admission import InMemoryKnowledgeAdmission
from native_core.core.knowledge.exceptions import UnauthorizedPromotion
from native_core.core.knowledge.models import KnowledgeVersion
from native_core.core.knowledge.repository import InMemoryKnowledgeRepository
from native_core.core.knowledge.retrieval import InMemoryKnowledgeRetrieval
from native_core.core.knowledge.storage import InMemoryKnowledgeStore
from native_core.core.knowledge.versioning import InMemoryKnowledgeVersioning
from native_core.core.memory import MemoryReader
from native_core.core.trace import TraceReader, TraceWriter, new_record

SCOPE = "phase6-agent-scope"


def _governance(*observations):
    """The resident Infrastructure→Trace→Memory→Governance stack in a temp
    directory. Writes one Trace record per observation, all under one scope, so
    that successive candidates target the same Knowledge item."""
    tmp = Path(tempfile.mkdtemp())
    trace_storage = LocalAppendOnlyStorage(base_dir=tmp / "trace")
    trace_storage.provision()
    gov_storage = LocalAppendOnlyStorage(base_dir=tmp / "gov")
    gov_storage.provision()
    writer = TraceWriter(trace_storage)
    for value in observations:
        writer.write(
            new_record(
                agent_definition_version="1",
                agent_instance=SCOPE,
                runtime="rt",
                outputs={"finding": value},
            )
        )
    review = GovernanceReview(MemoryReader(TraceReader(trace_storage)), gov_storage)
    candidates = review.pending_candidates()
    assert candidates, "the established stack must surface at least one candidate"
    return review, candidates


def _knowledge():
    """Knowledge assembled from in-memory reference implementations, plus the
    read surface the Agent consumes through."""
    store = InMemoryKnowledgeStore()
    versioning = InMemoryKnowledgeVersioning()
    repository = InMemoryKnowledgeRepository(store, versioning)
    admission = InMemoryKnowledgeAdmission(repository, versioning)
    retrieval = InMemoryKnowledgeRetrieval(repository)
    return admission, retrieval, repository


def _approve(review, candidate, who="alice"):
    review.record_decision(
        ReviewDecision(candidate, "approve", HumanAuthority(who), "phase 6 evidence")
    )


def _agent(key=None):
    admission, retrieval, repository = _knowledge()
    return KnowledgeConsumingAgent(retrieval, admission, key), admission, retrieval, repository


class DemonstrationOneAgentRetrieval(unittest.TestCase):
    """§13.1 — an Agent obtains an admitted Knowledge version."""

    def test_agent_reads_the_admitted_version_through_the_consumption_surface(self):
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent()
        _approve(review, candidates[0])
        admitted = agent.propose(candidates[0], review)

        obtained = agent.read(candidates[0].scope)

        self.assertIsInstance(obtained, KnowledgeVersion)
        self.assertEqual(admitted, obtained)
        self.assertEqual((obtained,), agent.knowledge_read)

    def test_the_obtained_version_carries_the_admitted_content(self):
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent()
        _approve(review, candidates[0])
        agent.propose(candidates[0], review)

        obtained = agent.read(candidates[0].scope)

        self.assertEqual(candidates[0].observed_content, obtained.content)

    def test_participate_completes_by_reading_its_configured_item(self):
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent(key=SCOPE)
        _approve(review, candidates[0])
        agent.propose(candidates[0], review)

        outcome = agent.participate(object())

        self.assertIsNone(outcome, "completion is defined negatively — no result model")
        self.assertEqual(1, len(agent.knowledge_read))

    def test_reading_an_item_with_no_active_version_yields_explicit_absence(self):
        agent, _, _, _ = _agent()
        self.assertIsNone(agent.read("no-such-item"))
        self.assertEqual((), agent.knowledge_read)


class DemonstrationTwoAgentUpdate(unittest.TestCase):
    """§13.2 — an Agent updates Knowledge through the governed path."""

    def test_agent_update_produces_a_new_admitted_version(self):
        review, candidates = _governance("first-value", "second-value")
        agent, _, _, _ = _agent()
        first, second = candidates[0], candidates[1]
        self.assertEqual(first.scope, second.scope, "both candidates target one item")

        _approve(review, first)
        v1 = agent.propose(first, review)
        _approve(review, second)
        v2 = agent.propose(second, review)

        self.assertEqual(1, v1.identity.version_sequence)
        self.assertEqual(2, v2.identity.version_sequence)
        self.assertEqual((v1, v2), agent.knowledge_admitted)

    def test_after_update_the_agent_reads_the_new_active_version(self):
        review, candidates = _governance("first-value", "second-value")
        agent, _, _, _ = _agent()
        _approve(review, candidates[0])
        agent.propose(candidates[0], review)
        _approve(review, candidates[1])
        v2 = agent.propose(candidates[1], review)

        self.assertEqual(v2, agent.read(candidates[0].scope))

    def test_the_update_goes_through_the_existing_admission_gate(self):
        """No second promotion authority (§12): the version the Agent obtains is
        the one the certified admission produced, recorded in the repository."""
        review, candidates = _governance("observed-value")
        agent, _, _, repository = _agent()
        _approve(review, candidates[0])

        admitted = agent.propose(candidates[0], review)

        self.assertEqual([admitted], list(repository.history(candidates[0].scope)))


class DemonstrationThreeUnauthorizedRejected(unittest.TestCase):
    """§13.3 — unauthorized updates are rejected, and nothing is written."""

    def test_absent_decision_refuses_and_writes_nothing(self):
        review, candidates = _governance("observed-value")
        agent, _, _, repository = _agent()
        self.assertFalse(review.promotion_authorized(candidates[0]))

        with self.assertRaises(UnauthorizedPromotion):
            agent.propose(candidates[0], review)

        self.assertEqual((), repository.history(candidates[0].scope))
        self.assertEqual((), agent.knowledge_admitted)

    def test_recorded_reject_refuses(self):
        review, candidates = _governance("observed-value")
        agent, _, _, repository = _agent()
        review.record_decision(
            ReviewDecision(candidates[0], "reject", HumanAuthority("bob"), "not admissible")
        )

        with self.assertRaises(UnauthorizedPromotion):
            agent.propose(candidates[0], review)

        self.assertEqual((), repository.history(candidates[0].scope))

    def test_reject_after_approve_still_refuses(self):
        """Reject is absolute at the Governance boundary; the Agent reflects it
        rather than deciding anything."""
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent()
        _approve(review, candidates[0])
        review.record_decision(
            ReviewDecision(candidates[0], "reject", HumanAuthority("bob"), "withdrawn")
        )

        with self.assertRaises(UnauthorizedPromotion):
            agent.propose(candidates[0], review)

    def test_the_agent_does_not_soften_the_fail_closed_gate(self):
        """The refusal propagates out of `propose`. A consumer that returned a
        soft failure would convert a fail-closed gate into a fail-open one."""
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent()

        with self.assertRaises(UnauthorizedPromotion):
            agent.propose(candidates[0], review)


class DemonstrationFourValidatedOnly(unittest.TestCase):
    """§13.4 — unadmitted knowledge cannot be treated as validated."""

    def test_an_unadmitted_candidate_is_not_reachable_through_the_read_path(self):
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent()
        # A real candidate exists in Governance and was never approved.
        self.assertTrue(candidates)
        self.assertFalse(review.promotion_authorized(candidates[0]))

        self.assertIsNone(agent.read(candidates[0].scope))
        self.assertEqual((), agent.knowledge_read)

    def test_a_refused_proposal_leaves_nothing_readable(self):
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent()
        with self.assertRaises(UnauthorizedPromotion):
            agent.propose(candidates[0], review)

        self.assertIsNone(agent.read(candidates[0].scope))

    def test_everything_the_agent_reads_is_an_admitted_version(self):
        review, candidates = _governance("first-value", "second-value")
        agent, _, _, repository = _agent()
        for candidate in candidates:
            _approve(review, candidate)
            agent.propose(candidate, review)
        agent.read(candidates[0].scope)

        admitted = set(repository.history(candidates[0].scope))
        for version in agent.knowledge_read:
            self.assertIn(version, admitted)


class DemonstrationFiveVersionAndHistory(unittest.TestCase):
    """§13.5 — version and history semantics remain intact."""

    def test_history_is_append_only_and_ordered(self):
        review, candidates = _governance("first-value", "second-value")
        agent, _, _, _ = _agent()
        _approve(review, candidates[0])
        v1 = agent.propose(candidates[0], review)
        _approve(review, candidates[1])
        v2 = agent.propose(candidates[1], review)

        history = agent.history(candidates[0].scope)

        self.assertEqual((v1, v2), history)

    def test_the_prior_version_is_retained_after_update(self):
        review, candidates = _governance("first-value", "second-value")
        agent, _, _, _ = _agent()
        _approve(review, candidates[0])
        v1 = agent.propose(candidates[0], review)
        _approve(review, candidates[1])
        agent.propose(candidates[1], review)

        self.assertIn(v1, agent.history(candidates[0].scope))

    def test_update_creates_a_new_version_never_edits_in_place(self):
        review, candidates = _governance("first-value", "second-value")
        agent, _, _, _ = _agent()
        _approve(review, candidates[0])
        v1 = agent.propose(candidates[0], review)
        first_content = v1.content
        _approve(review, candidates[1])
        agent.propose(candidates[1], review)

        self.assertEqual(first_content, v1.content, "the admitted version is immutable")
        self.assertEqual(2, len(agent.history(candidates[0].scope)))


class TheAgentHoldsNoAuthority(unittest.TestCase):
    """The direction is strictly Governance → Knowledge. This consumer proposes;
    it never decides."""

    def test_the_agent_module_names_no_governance_decision_type(self):
        import ast
        from pathlib import Path

        source = Path("consumers/knowledge_agent.py").read_text(encoding="utf-8")
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.update(f"{node.module}.{a.name}" for a in node.names)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        joined = " ".join(imported)
        for forbidden in ("ReviewDecision", "HumanAuthority", "GovernanceReview"):
            self.assertNotIn(forbidden, joined)

    def test_the_agent_cannot_authorize_its_own_proposal(self):
        review, candidates = _governance("observed-value")
        agent, _, _, _ = _agent()
        self.assertFalse(hasattr(agent, "approve"))
        self.assertFalse(hasattr(agent, "record_decision"))
        with self.assertRaises(UnauthorizedPromotion):
            agent.propose(candidates[0], review)

    def test_construction_fails_closed_on_malformed_collaborators(self):
        admission, retrieval, _ = _knowledge()
        with self.assertRaises(TypeError):
            KnowledgeConsumingAgent(object(), admission)
        with self.assertRaises(TypeError):
            KnowledgeConsumingAgent(retrieval, object())


if __name__ == "__main__":
    unittest.main()
