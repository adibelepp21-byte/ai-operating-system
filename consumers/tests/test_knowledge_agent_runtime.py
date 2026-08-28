"""
Phase 6 runtime integration evidence — `ACT-CC-P6-074 §6`–`§10`.

The Founder-ratified criteria require the Knowledge path to be exercised
*"during an actual execution path"*. `ACT-CC-P6-074 §6` fixes what that means:

    Agent → Execution → Runtime (RUNNING) → Knowledge → Governance admission → Active

and rules out a direct call, a stub Runtime, a mocked Agent, or a unit test
invoking the consumer directly as *sole* evidence. This module supplies the
chain itself.

**No production path was invented for it.** The Execution contract already names
the route — *"Reaching Knowledge through `runtime.knowledge` still passes the
Runtime's own RUNNING-only access control — Execution adds no authority and
bypasses nothing"* — and `Runtime.knowledge` is RUNNING-gated. The Runtime is
built with the resident `E-01` pattern (`create_runtime` → `initialize` →
`start` → `create_execution_layer`), per `§7`'s instruction to reuse it rather
than invent another mechanism.

The Knowledge the Agent touches here is the **Runtime's own hosted subsystem**,
never an injected one: several tests assert identity against
`runtime.knowledge.repository` so that a passing result cannot come from a
collaborator the test handed in.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consumers.knowledge_agent import KnowledgeConsumingAgent
from native_core.core.governance import GovernanceReview, HumanAuthority, ReviewDecision
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
)
from native_core.core.knowledge.exceptions import UnauthorizedPromotion
from native_core.core.knowledge.models import KnowledgeVersion
from native_core.core.memory import MemoryReader
from native_core.core.runtime import RuntimeState
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.execution import create_execution_layer
from native_core.core.trace import TraceReader, TraceWriter, new_record

SCOPE = "p6-074-runtime-scope"


def _running_runtime(runtime_id="p6-074-runtime"):
    """The resident E-01 pattern, unchanged."""
    storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id=runtime_id, storage=storage, substrate=substrate)
    runtime.initialize()
    runtime.start()
    return runtime


def _governance(*observations):
    """The resident governance/tests stack: Infrastructure → Trace → Memory →
    Governance, in a temp directory. Produces real candidates under one scope."""
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


def _approve(review, candidate, who="alice"):
    review.record_decision(
        ReviewDecision(candidate, "approve", HumanAuthority(who), "P6-074 runtime evidence")
    )


class E601AgentRetrievalThroughTheRuntime(unittest.TestCase):
    """§8 — the ten required links of the retrieval chain."""

    def test_the_full_chain_is_traversed_and_the_agent_receives_knowledge(self):
        runtime = _running_runtime()
        review, candidates = _governance("runtime-observed-value")
        candidate = candidates[0]
        _approve(review, candidate)

        # 3, 4 — a Runtime exists and is actually RUNNING.
        self.assertIs(RuntimeState.RUNNING, runtime.state)
        # 2 — an Execution exists, minted by that Runtime.
        execution = create_execution_layer(runtime)
        self.assertIs(runtime, execution.runtime)
        # 1 — an Agent Instance exists.
        agent = KnowledgeConsumingAgent(
            knowledge_item_key=SCOPE, proposal=(candidate, review)
        )
        # 5 — the Agent participates in that Execution; 6-9 happen inside.
        agent.participate(execution)

        # 7, 9 — the requested Knowledge exists and the Agent received it.
        self.assertEqual(1, len(agent.knowledge_read))
        received = agent.knowledge_read[0]
        self.assertIsInstance(received, KnowledgeVersion)
        # 8 — it is Active through the T-12 gate: it is what admission produced.
        self.assertEqual(agent.knowledge_admitted[0], received)
        # 10 — not a mocked result: it is the Runtime's own hosted Knowledge.
        self.assertIn(received, runtime.knowledge.repository.history(SCOPE))

    def test_the_knowledge_came_from_the_runtimes_hosted_subsystem(self):
        """The Agent was given no collaborators. Everything it touched was
        resolved from `execution.runtime.knowledge`."""
        runtime = _running_runtime()
        review, candidates = _governance("runtime-observed-value")
        _approve(review, candidates[0])
        agent = KnowledgeConsumingAgent(
            knowledge_item_key=SCOPE, proposal=(candidates[0], review)
        )

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(
            list(runtime.knowledge.repository.history(SCOPE)),
            list(agent.knowledge_admitted),
        )
        self.assertEqual(runtime.knowledge.retrieval.active(SCOPE), agent.knowledge_read[0])

    def test_the_execution_context_records_the_hosting_runtime(self):
        runtime = _running_runtime(runtime_id="p6-074-identity")
        execution = create_execution_layer(runtime)
        agent = KnowledgeConsumingAgent(knowledge_item_key=SCOPE)

        agent.participate(execution)

        self.assertEqual("p6-074-identity", execution.context.runtime_id)
        self.assertEqual(0, execution.context.execution_sequence)

    def test_the_ordinal_advances_across_participations(self):
        runtime = _running_runtime()
        agent = KnowledgeConsumingAgent(knowledge_item_key=SCOPE)
        sequences = []
        for _ in range(3):
            execution = create_execution_layer(runtime)
            agent.participate(execution)
            sequences.append(execution.context.execution_sequence)
        self.assertEqual([0, 1, 2], sequences)

    def test_a_runtime_that_is_not_running_yields_no_execution_at_all(self):
        """The RUNNING gate is the Runtime's, and it holds before a consumer is
        reached — there is no path by which this Agent could bypass it."""
        storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
        storage.provision()
        substrate = LocalExecutionSubstrate()
        substrate.provision()
        runtime = create_runtime(runtime_id="not-running", storage=storage, substrate=substrate)
        runtime.initialize()
        self.assertIsNot(RuntimeState.RUNNING, runtime.state)

        with self.assertRaises(Exception):
            create_execution_layer(runtime)


class E602AgentUpdateThroughTheRuntime(unittest.TestCase):
    """§9 — the update chain, ending in Active Knowledge."""

    def test_agent_update_during_participation_produces_an_active_version(self):
        runtime = _running_runtime()
        review, candidates = _governance("first-runtime-value")
        _approve(review, candidates[0])
        agent = KnowledgeConsumingAgent(
            knowledge_item_key=SCOPE, proposal=(candidates[0], review)
        )

        agent.participate(create_execution_layer(runtime))

        admitted = agent.knowledge_admitted[0]
        self.assertEqual(1, admitted.identity.version_sequence)
        self.assertEqual(SCOPE, admitted.identity.knowledge_item_key)
        self.assertEqual(admitted, runtime.knowledge.retrieval.active(SCOPE))

    def test_a_second_participation_updates_and_preserves_the_prior_version(self):
        runtime = _running_runtime()
        review, candidates = _governance("first-runtime-value", "second-runtime-value")
        first, second = candidates[0], candidates[1]
        _approve(review, first)
        _approve(review, second)

        KnowledgeConsumingAgent(proposal=(first, review)).participate(
            create_execution_layer(runtime)
        )
        KnowledgeConsumingAgent(proposal=(second, review)).participate(
            create_execution_layer(runtime)
        )

        history = runtime.knowledge.repository.history(SCOPE)
        self.assertEqual(2, len(history))
        self.assertEqual(1, history[0].identity.version_sequence)
        self.assertEqual(2, history[1].identity.version_sequence)
        self.assertEqual(history[1], runtime.knowledge.retrieval.active(SCOPE))

    def test_unauthorized_update_during_participation_is_refused(self):
        """§9's negative case: no valid T-12 authorization, no Active Knowledge."""
        runtime = _running_runtime()
        review, candidates = _governance("unauthorized-value")
        self.assertFalse(review.promotion_authorized(candidates[0]))
        agent = KnowledgeConsumingAgent(proposal=(candidates[0], review))

        with self.assertRaises(UnauthorizedPromotion):
            agent.participate(create_execution_layer(runtime))

        self.assertEqual((), runtime.knowledge.repository.history(SCOPE))
        self.assertIsNone(runtime.knowledge.retrieval.active(SCOPE))

    def test_a_rejected_candidate_during_participation_is_refused(self):
        runtime = _running_runtime()
        review, candidates = _governance("rejected-value")
        review.record_decision(
            ReviewDecision(candidates[0], "reject", HumanAuthority("bob"), "not admissible")
        )
        agent = KnowledgeConsumingAgent(proposal=(candidates[0], review))

        with self.assertRaises(UnauthorizedPromotion):
            agent.participate(create_execution_layer(runtime))

        self.assertEqual((), runtime.knowledge.repository.history(SCOPE))


class E603ValidatedThroughTheGate(unittest.TestCase):
    """§10 — every qualifying version is Active *because* T-12 admitted it."""

    def test_every_version_the_agent_read_is_active_via_admission(self):
        runtime = _running_runtime()
        review, candidates = _governance("v1", "v2")
        for candidate in candidates:
            _approve(review, candidate)
            KnowledgeConsumingAgent(proposal=(candidate, review)).participate(
                create_execution_layer(runtime)
            )
        reader = KnowledgeConsumingAgent(knowledge_item_key=SCOPE)
        reader.participate(create_execution_layer(runtime))

        admitted = runtime.knowledge.repository.history(SCOPE)
        self.assertEqual(1, len(reader.knowledge_read))
        self.assertIn(reader.knowledge_read[0], admitted)
        self.assertEqual(admitted[-1], reader.knowledge_read[0], "reads the Active version")

    def test_no_qualifying_path_bypassed_the_gate(self):
        """Nothing becomes readable without passing admission first."""
        runtime = _running_runtime()
        review, candidates = _governance("gate-value")
        reader = KnowledgeConsumingAgent(knowledge_item_key=SCOPE)

        reader.participate(create_execution_layer(runtime))
        self.assertEqual((), reader.knowledge_read, "unadmitted candidate is not readable")

        _approve(review, candidates[0])
        KnowledgeConsumingAgent(proposal=(candidates[0], review)).participate(
            create_execution_layer(runtime)
        )
        reader.participate(create_execution_layer(runtime))
        self.assertEqual(1, len(reader.knowledge_read))

    def test_the_agent_holds_no_admission_authority_on_the_runtime_path(self):
        runtime = _running_runtime()
        review, candidates = _governance("authority-value")
        agent = KnowledgeConsumingAgent(proposal=(candidates[0], review))

        with self.assertRaises(UnauthorizedPromotion):
            agent.participate(create_execution_layer(runtime))
        self.assertFalse(hasattr(agent, "approve"))
        self.assertFalse(hasattr(agent, "record_decision"))


if __name__ == "__main__":
    unittest.main()
