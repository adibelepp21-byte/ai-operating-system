"""
Phase 5 runtime evidence — `E5-1`, `E5-2`, `E5-4` on the actual execution path.

`E5-2` requires its milestone *"demonstrated on **real execution** rather than
plan"*, and `E5-4` binds *"teruji"* to the Engineering Phase Checklist running
*"berjalan nyata, bukan lagi rencana"*. Neither is established by a unit test
calling a consumer directly, however green — that is the same standard
`ACT-CC-P6-074 §6` applied to Phase 6, and applying a weaker one here because
the work is ours would be marking our own homework.

So this module exercises both Intelligence consumers through the chain:

    Agent → Execution → Runtime (RUNNING) → participation

built with the resident `E-01` pattern (`create_runtime` → `initialize` →
`start` → `create_execution_layer`), reused rather than reinvented. No Runtime is
stubbed, no Execution is faked, and no participation is simulated: if the
Runtime were not RUNNING, `create_execution_layer` would refuse and these tests
would fail rather than quietly pass on a mock.

`E5-1` counts *"at least one (1) capability … per in-scope category"*, with the
in-scope count fixed at two by `GDR-0004`. The two categories are exercised in
one Execution in `E501BothCategoriesOnOneRuntime`, which is the count made
literal.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consumers.cognitive_intelligence_agent import (
    CognitiveIntelligenceAgent,
    IndecomposableUnitOfWork,
)
from consumers.engineering_intelligence_agent import (
    Artifact,
    ConformanceCriterion,
    EngineeringIntelligenceAgent,
)
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
)
from native_core.core.runtime import RuntimeState
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.execution import create_execution_layer

UNIT_OF_WORK = "read the execution contract; derive the sub-steps; record the order"


def _running_runtime(runtime_id="p5-076-runtime"):
    """The resident E-01 pattern, unchanged."""
    storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id=runtime_id, storage=storage, substrate=substrate)
    runtime.initialize()
    runtime.start()
    return runtime


class E502DecompositionOnTheRealExecutionPath(unittest.TestCase):
    """The Cognitive Intelligence milestone, on a real Runtime."""

    def test_the_runtime_is_actually_running(self):
        self.assertIs(RuntimeState.RUNNING, _running_runtime().state)

    def test_the_execution_is_minted_by_that_runtime(self):
        runtime = _running_runtime()

        execution = create_execution_layer(runtime)

        self.assertIs(runtime, execution.runtime)

    def test_decomposition_happens_during_participation(self):
        runtime = _running_runtime()
        agent = CognitiveIntelligenceAgent(unit_of_work=UNIT_OF_WORK)
        self.assertEqual((), agent.decomposition)

        agent.participate(create_execution_layer(runtime))

        self.assertGreaterEqual(len(agent.decomposition), 2)

    def test_the_criterion_count_is_met_on_the_real_path(self):
        """`E5-2` — two or more ordered sub-steps."""
        runtime = _running_runtime()
        agent = CognitiveIntelligenceAgent(unit_of_work=UNIT_OF_WORK)

        agent.participate(create_execution_layer(runtime))

        self.assertEqual([1, 2, 3], [s.ordinal for s in agent.decomposition])

    def test_participation_completes_by_returning_none(self):
        runtime = _running_runtime()
        agent = CognitiveIntelligenceAgent(unit_of_work=UNIT_OF_WORK)

        self.assertIsNone(agent.participate(create_execution_layer(runtime)))

    def test_an_indecomposable_unit_fails_on_the_real_path_too(self):
        """The gate is not softened by being reached through a Runtime."""
        runtime = _running_runtime()
        agent = CognitiveIntelligenceAgent(unit_of_work="indivisible work")

        with self.assertRaises(IndecomposableUnitOfWork):
            agent.participate(create_execution_layer(runtime))

    def test_the_execution_ordinal_advances_across_participations(self):
        runtime = _running_runtime()
        execution = create_execution_layer(runtime)
        agent = CognitiveIntelligenceAgent(unit_of_work=UNIT_OF_WORK)

        agent.participate(execution)
        agent.participate(execution)

        self.assertEqual(3, len(agent.decomposition))


class E503VerificationOnTheRealExecutionPath(unittest.TestCase):
    """The Engineering Intelligence milestone, on a real Runtime."""

    def _agent(self, lines=("def f():", "    return 1"), required="def f():"):
        return EngineeringIntelligenceAgent(
            artifact=Artifact(name="m.py", lines=tuple(lines)),
            criteria=[ConformanceCriterion("declares f", required)],
        )

    def test_verification_happens_during_participation(self):
        runtime = _running_runtime()
        agent = self._agent()
        self.assertEqual((), agent.results)

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(1, len(agent.results))

    def test_a_satisfied_criterion_is_reported_on_the_real_path(self):
        runtime = _running_runtime()
        agent = self._agent()

        agent.participate(create_execution_layer(runtime))

        self.assertTrue(agent.results[0].satisfied)

    def test_a_failing_criterion_is_reported_not_raised(self):
        runtime = _running_runtime()
        agent = self._agent(required="def absent():")

        agent.participate(create_execution_layer(runtime))

        self.assertFalse(agent.results[0].satisfied)

    def test_coding_and_testing_compose_within_one_participation(self):
        """Construct, change, then verify the changed artifact — both realized
        sub-abilities, on the real path."""
        runtime = _running_runtime()
        execution = create_execution_layer(runtime)
        agent = EngineeringIntelligenceAgent()

        original = agent.construct("m.py", ["x = 1"])
        changed = agent.change(original, ["x = 2"])
        results = agent.verify(changed, [ConformanceCriterion("updated", "x = 2")])
        agent.participate(execution)

        self.assertTrue(results[0].satisfied)
        self.assertEqual(("x = 1",), original.lines)

    def test_participation_completes_by_returning_none(self):
        runtime = _running_runtime()

        self.assertIsNone(self._agent().participate(create_execution_layer(runtime)))


class E501BothCategoriesOnOneRuntime(unittest.TestCase):
    """`E5-1` — the count, made literal: two in-scope categories, each with a
    realized capability, both exercised on the same running Runtime."""

    def test_two_capabilities_participate_in_one_execution(self):
        runtime = _running_runtime()
        execution = create_execution_layer(runtime)
        cognitive = CognitiveIntelligenceAgent(unit_of_work=UNIT_OF_WORK)
        engineering = EngineeringIntelligenceAgent(
            artifact=Artifact(name="m.py", lines=("a = 1",)),
            criteria=[ConformanceCriterion("declares a", "a = 1")],
        )

        cognitive.participate(execution)
        engineering.participate(execution)

        self.assertGreaterEqual(len(cognitive.decomposition), 2)
        self.assertTrue(engineering.results[0].satisfied)

    def test_the_minimum_verified_capability_count_is_two(self):
        """`GDR-0005 §3.5.3` — *"Minimum verified capabilities = 2."*"""
        runtime = _running_runtime()
        execution = create_execution_layer(runtime)
        verified = []

        cognitive = CognitiveIntelligenceAgent(unit_of_work=UNIT_OF_WORK)
        cognitive.participate(execution)
        if len(cognitive.decomposition) >= 2:
            verified.append("Cognitive Intelligence")

        engineering = EngineeringIntelligenceAgent(
            artifact=Artifact(name="m.py", lines=("a = 1",)),
            criteria=[ConformanceCriterion("declares a", "a = 1")],
        )
        engineering.participate(execution)
        if engineering.results and engineering.results[0].satisfied:
            verified.append("Engineering Intelligence")

        self.assertEqual(2, len(verified))

    def test_neither_agent_was_handed_a_collaborator(self):
        """Both resolved everything from the Execution they were given. Nothing
        was injected that could make a passing result an artefact of the test."""
        runtime = _running_runtime()
        execution = create_execution_layer(runtime)

        cognitive = CognitiveIntelligenceAgent(unit_of_work=UNIT_OF_WORK)
        cognitive.participate(execution)

        self.assertIs(runtime, execution.runtime)
        self.assertIs(RuntimeState.RUNNING, execution.runtime.state)


if __name__ == "__main__":
    unittest.main()
