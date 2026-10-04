"""FR-2 (`FD-FR2-001`) — the Agent side of the Runtime-hosted Agency path, and its wiring.

**Why this file is at the repository root.** The path needs two things that
live in mutually isolated regions: the authority side in `tools/`
(`tools/w4_runtime_execution.py`: the grant, the per-step re-check, the
Runtime, the manifest, the escalation wiring) and the Trace wire in
`consumers/` (`consumers/observation.TracedAction`). Neither region may import
the other (`consumers/tests/test_reference_agent.py` and the consumer suites
assert both directions), so the participant and its binding live outside both,
as `w4_first_execution.py` does for W4 and `p12_w4_integrated_execution.py`
does for P12-W4.

It is also outside the **served tree** (`fullstack/readiness.py`
`SERVED_PATHS`, which counts every module under `consumers/`). A new module
there would change what the paused deployment serves and make its recorded
Preview verification stale. `FD-FR2-001 §11` keeps deployment paused, and FR-2
changes nothing the deployment serves.

**What it adds: no subsystem, no boundary, no schema field.** `DelegatedStep` is
an `Agent` (an `ExecutionConsumer`) whose `participate` does exactly one thing:
run the delegated work inside one `TracedAction`, under the **Agent Instance**
the delegation names and the runtime identity read from the `Execution` it was
handed.

* **Only through an Execution.** Anything that is not a real `Execution` whose
  Runtime is RUNNING is refused before any work, so a step cannot run outside a
  Runtime, nor be traced as if it had.
* **Authorization first.** ``run_step`` is the authority side's per-step check
  and call. It receives the traced action and calls it only once the grant, the
  instance and the scope have been re-checked. A refused step raises before any
  work and writes no Trace: the record is of an action that happened.
* **The existing status mapping** (`consumers/observation.py`): the work
  returns → `success`; the work raises → `failure`. `escalation` keeps no
  producer (G7), as before.

`hosted_executor` and `run_hosted_plan` are the `tools/` functions of the same
name with this participant supplied; they bind and decide nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from native_core.core.agent import Agent  # noqa: E402
from native_core.core.runtime import RuntimeNotRunning, RuntimeState  # noqa: E402
from native_core.core.runtime.execution import Execution  # noqa: E402
from native_core.core.trace import TraceWriter  # noqa: E402

from consumers.observation import TracedAction  # noqa: E402
from tools import w4_runtime_execution as _hosted  # noqa: E402


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


PARTICIPANT = DelegatedStep


def hosted_executor(delegation, registry, runtime, writer, **options):
    """`RuntimeHostedExecutor` with the resident participant."""
    return _hosted.RuntimeHostedExecutor(delegation, registry, runtime, writer,
                                         participant=PARTICIPANT, **options)


def run_hosted_plan(delegation, registry, runtime, writer, plan, perform, **options):
    """`run_hosted_plan` (the hosted run path) with the resident participant."""
    return _hosted.run_hosted_plan(delegation, registry, runtime, writer, plan, perform,
                                   participant=PARTICIPANT, **options)
