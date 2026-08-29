"""
`E7-03` evidence — Memory on the real execution path.

`FD-P7-001 §6` requires the path itself:

```text
Agent → Execution → Runtime (RUNNING) → Memory Retrieval → Result
```

and `ACT-CC-P7-002 §7.5` requires it *"exercised in real execution, not only
through mocks"*, with `§15.2` adding that unit tests alone are insufficient. So
this module builds a real Runtime with the resident `E-01` pattern
(`create_runtime` → `initialize` → `start` → `create_execution_layer`), and every
Memory the Agent touches is the **Runtime's own hosted subsystem** — several
tests assert identity against `runtime.memory.store` so a passing result cannot
come from a collaborator the test handed in.

`FD-P7-002 §7` additionally forbids satisfying `E7-03` through a bypass: no
direct `Agent → Memory` access, no Execution ownership of Memory state, no mocked
Runtime presented as real execution, and **no dormant path that fails to enforce
RUNNING**. `TheRunningGateIsReal` is the negative control for that last one.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from consumers.memory_agent import MemoryConsumingAgent
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
)
from native_core.core.memory import MemoryItem, MemoryState
from native_core.core.runtime import RuntimeState
from native_core.core.runtime.composition import create_runtime
from native_core.core.runtime.exceptions import RuntimeNotRunning
from native_core.core.runtime.execution import create_execution_layer

KEY = "p7-memory-key"


def _runtime(runtime_id="p7-002-runtime", start=True):
    """The resident E-01 pattern, unchanged."""
    storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id=runtime_id, storage=storage, substrate=substrate)
    runtime.initialize()
    if start:
        runtime.start()
    return runtime


class E703RetrievalThroughTheRuntime(unittest.TestCase):
    """The path, link by link."""

    def test_the_runtime_is_actually_running(self):
        self.assertIs(RuntimeState.RUNNING, _runtime().state)

    def test_the_execution_is_minted_by_that_runtime(self):
        runtime = _runtime()

        execution = create_execution_layer(runtime)

        self.assertIs(runtime, execution.runtime)

    def test_the_full_chain_is_traversed_and_the_agent_receives_memory(self):
        runtime = _runtime()
        agent = MemoryConsumingAgent(memory_key=KEY, proposal=(KEY, "observed"))

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(1, len(agent.memory_read))
        self.assertIsInstance(agent.memory_read[0], MemoryItem)
        self.assertEqual("observed", agent.memory_read[0].payload)

    def test_the_memory_came_from_the_runtimes_hosted_subsystem(self):
        """The Agent was given no collaborators. Everything it touched was
        resolved from `execution.runtime.memory`."""
        runtime = _runtime()
        agent = MemoryConsumingAgent(memory_key=KEY, proposal=(KEY, "observed"))

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(
            list(runtime.memory.retrieval.history(KEY)),
            list(agent.memory_admitted),
        )
        self.assertIs(runtime.memory.retrieval.active(KEY), agent.memory_read[0])

    def test_what_was_read_is_eligible_memory(self):
        runtime = _runtime()
        agent = MemoryConsumingAgent(memory_key=KEY, proposal=(KEY, "observed"))

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(MemoryState.RETAINED, agent.memory_read[0].state)
        self.assertTrue(agent.memory_read[0].is_eligible)

    def test_retrieval_is_deterministic_across_participations(self):
        """`E7-03.2` — the same request against the same eligible state."""
        runtime = _runtime()
        execution = create_execution_layer(runtime)
        MemoryConsumingAgent(proposal=(KEY, "observed")).participate(execution)

        first = MemoryConsumingAgent(memory_key=KEY)
        second = MemoryConsumingAgent(memory_key=KEY)
        first.participate(execution)
        second.participate(execution)

        self.assertEqual(first.memory_read[0], second.memory_read[0])

    def test_reading_an_unknown_key_yields_an_explicit_absence(self):
        runtime = _runtime()
        agent = MemoryConsumingAgent(memory_key="never-admitted")

        agent.participate(create_execution_layer(runtime))

        self.assertEqual((), agent.memory_read)

    def test_participation_completes_by_returning_none(self):
        runtime = _runtime()
        agent = MemoryConsumingAgent(memory_key=KEY, proposal=(KEY, "v"))

        self.assertIsNone(agent.participate(create_execution_layer(runtime)))

    def test_the_execution_ordinal_advances_across_participations(self):
        runtime = _runtime()
        execution = create_execution_layer(runtime)
        agent = MemoryConsumingAgent(proposal=(KEY, "v"))

        agent.participate(execution)
        agent.participate(execution)

        self.assertEqual(2, len(agent.memory_admitted))


class TheRunningGateIsReal(unittest.TestCase):
    """`FD-P7-002 §7` — the negative control. A dormant path that did not
    enforce RUNNING would satisfy nothing."""

    def test_memory_is_refused_before_the_runtime_is_running(self):
        runtime = _runtime(start=False)

        with self.assertRaises(RuntimeNotRunning):
            runtime.memory

    def test_no_execution_can_be_minted_before_running(self):
        runtime = _runtime(start=False)

        with self.assertRaises(RuntimeNotRunning):
            create_execution_layer(runtime)

    def test_memory_is_refused_after_the_runtime_stops(self):
        runtime = _runtime()
        runtime.stop()

        with self.assertRaises(RuntimeNotRunning):
            runtime.memory

    def test_the_gate_is_the_runtimes_own_not_the_consumers(self):
        """The consumer adds no access control: the refusal comes from the
        Runtime before any consumer code runs."""
        runtime = _runtime(start=False)
        agent = MemoryConsumingAgent(memory_key=KEY)

        with self.assertRaises(RuntimeNotRunning):
            agent._resolve(type("E", (), {"runtime": runtime})())


class E705IneligibleMemoryIsNotReturnedOnTheRealPath(unittest.TestCase):
    """`E7-05.4` proven where it matters — through the Runtime, not only in a
    unit test of the boundary."""

    def test_expired_memory_is_not_returned_through_the_runtime(self):
        runtime = _runtime()
        execution = create_execution_layer(runtime)
        MemoryConsumingAgent(proposal=(KEY, "v")).participate(execution)
        runtime.memory.lifecycle.expire(KEY)

        reader = MemoryConsumingAgent(memory_key=KEY)
        reader.participate(execution)

        self.assertEqual((), reader.memory_read)

    def test_invalidated_memory_is_not_returned_through_the_runtime(self):
        runtime = _runtime()
        execution = create_execution_layer(runtime)
        MemoryConsumingAgent(proposal=(KEY, "v")).participate(execution)
        runtime.memory.lifecycle.invalidate(KEY)

        reader = MemoryConsumingAgent(memory_key=KEY)
        reader.participate(execution)

        self.assertEqual((), reader.memory_read)

    def test_an_updated_memory_returns_the_successor_not_the_predecessor(self):
        runtime = _runtime()
        execution = create_execution_layer(runtime)
        MemoryConsumingAgent(proposal=(KEY, "v1")).participate(execution)
        runtime.memory.lifecycle.update(KEY, "v2")

        reader = MemoryConsumingAgent(memory_key=KEY)
        reader.participate(execution)

        self.assertEqual("v2", reader.memory_read[0].payload)


class TheAgentHoldsNoMemoryAuthority(unittest.TestCase):
    """`FD-P7-001 §5` — Agent proposes; it does not decide."""

    def test_the_agent_exposes_no_lifecycle_transition(self):
        agent = MemoryConsumingAgent()

        for forbidden in ("expire", "invalidate", "update", "consolidate", "admit"):
            self.assertFalse(hasattr(agent, forbidden), forbidden)

    def test_a_refused_proposal_is_surfaced_and_admits_nothing(self):
        """The retention rule is the boundary's; the Agent cannot overrule it."""
        runtime = _runtime()
        runtime.memory.lifecycle._retention_rule = lambda c: False  # boundary policy
        agent = MemoryConsumingAgent(memory_key=KEY, proposal=(KEY, "v"))

        agent.participate(create_execution_layer(runtime))

        self.assertEqual(1, len(agent.proposals_refused))
        self.assertEqual((), agent.memory_admitted)
        self.assertEqual((), agent.memory_read)

    def test_forming_a_candidate_reaches_no_boundary(self):
        candidate = MemoryConsumingAgent().form_candidate("k", "v")

        self.assertFalse(hasattr(candidate, "state"))


if __name__ == "__main__":
    unittest.main()
