"""FR-2 (`FD-FR2-001`) — one delegated plan step, as an execution participant.

The Agent side of the Runtime-hosted Agency path. `tools/w4_runtime_execution`
holds the authority side (the grant, the per-step re-check, the manifest, the
escalation wiring) and builds a fresh `Execution` for every step. The two
regions may not import each other (`consumers/tests/test_reference_agent.py`
and the consumer suites assert both directions), so the authority side is
handed in here as ``run_step``, and this module never learns which machinery
authorized the step. The wiring lives at the repository root
(`agency_runtime_execution.py`), as `w4_first_execution.py` does for W4.

**What this adds: no subsystem, no boundary, no schema field.** It is an `Agent`
(an `ExecutionConsumer`) whose `participate` does exactly one thing: run the
delegated work inside one `TracedAction`, under the **Agent Instance** the
delegation names and the runtime identity read from the `Execution` it was
handed.

* **Only through an Execution.** Anything that is not a real `Execution` whose
  Runtime is RUNNING is refused before any work, so a step cannot run outside a
  Runtime, nor be traced as if it had.
* **Authorization first.** ``run_step`` is the authority side's per-step check
  and call. It receives the traced action, and calls it only once the grant,
  the instance and the scope have been re-checked. A refused step raises before
  any work and writes no Trace: the record is of an action that happened.
* **The existing status mapping** (`consumers/observation.py`): the work
  returns → `success`; the work raises → `failure`. `escalation` keeps no
  producer (G7), as before.
"""

from __future__ import annotations

from typing import Any, Callable, List

from native_core.core.agent import Agent
from native_core.core.runtime import RuntimeNotRunning, RuntimeState
from native_core.core.runtime.execution import Execution
from native_core.core.trace import TraceWriter

from .observation import TracedAction


class DelegatedStep(Agent):
    """One delegated step, taking part in one bound Execution.

    ``run_step(action)`` is the authority side: it re-checks the delegation and
    then calls ``action(step)``, which is this participant's traced wrapper
    around ``perform``. Whatever it returns is kept as the step's outcome.
    """

    def __init__(self, run_step: Callable[[Callable[[Any], str]], Any],
                 instance_key: str, perform: Callable[[Any], str],
                 writer: TraceWriter, agent_definition_version: str) -> None:
        if not isinstance(writer, TraceWriter):
            raise TypeError("a delegated step is traced: it requires a TraceWriter")
        if not instance_key:
            raise ValueError("a delegated step is taken by a named Agent Instance")
        self._run_step = run_step
        self._instance_key = instance_key
        self._perform = perform
        self._writer = writer
        self._version = agent_definition_version
        self.outcome: Any = None
        self.traced = False

    def participate(self, execution: Execution) -> None:
        if not isinstance(execution, Execution):
            raise TypeError("a delegated step enters only through an Execution "
                            "issued by a Runtime")
        if execution.runtime.state is not RuntimeState.RUNNING:
            raise RuntimeNotRunning(
                f"runtime {execution.context.runtime_id!r} is "
                f"{execution.runtime.state}; a delegated step runs only while "
                "its Runtime is RUNNING")
        runtime_id = execution.context.runtime_id
        actions: List[TracedAction] = []

        def traced(step: Any) -> str:
            with TracedAction(self._writer, agent_instance=self._instance_key,
                              runtime=runtime_id,
                              agent_definition_version=self._version) as action:
                actions.append(action)
                detail = self._perform(step)
                action.produced({"step": getattr(step, "key", str(step)),
                                 "detail": detail})
            return detail

        try:
            self.outcome = self._run_step(traced)
        finally:
            self.traced = any(a.written for a in actions)
