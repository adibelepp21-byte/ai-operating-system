"""Entry point — P12 F-11: a live Workflow, observed from another process.

**`WorkflowMonitor` is the canonical observation surface, and nothing outside
its own tests had ever called it.** `§12.4` / `E9-04` require that Workflow
identity, current lifecycle state, active-or-terminal, and success-or-failure be
determinable *"through the authorized public path"*, and `WorkflowMonitor`
answers exactly those four and nothing else — it deliberately carries no
transition method, so `E9-04`'s *"invalid state mutation does not silently
succeed"* holds structurally rather than by convention.

This proof reads state **through that surface** rather than from the lifecycle
directly, and publishes it so an independent process can see a Workflow that is
genuinely `RUNNING`.

The sequence, with the observer in a child interpreter that holds no lifecycle
object:

```text
define → mark_ready → enter_running   state RUNNING, in THIS process
publish (via WorkflowMonitor)         record written
child process observes                → LIVE, while the Workflow is still running
succeed()                             state SUCCEEDED
publish                               record overwritten
child process observes                → TERMINATED
```

`Runtime RUNNING` and `Workflow RUNNING` are **two vocabularies, not one**. A
Workflow can be running on a Runtime that is merely `INITIALIZED`; a Runtime can
be `RUNNING` with no Workflow at all. The projection keeps them separate.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from native_core.core.workflow import (  # noqa: E402
    Workflow, WorkflowIdentity, WorkflowLifecycle, WorkflowMonitor)
from tools.p12_runtime_observation import WORKFLOW, publish  # noqa: E402

WORKFLOW_KEY = "p12-f11-workflow-observation"

_OBSERVER = (
    "import json,sys;"
    "sys.path.insert(0, %r);"
    "from tools.p12_runtime_observation import what_is_running;"
    "print(json.dumps(what_is_running(), default=str))"
)


def _observe_independently() -> dict:
    result = subprocess.run(
        [sys.executable, "-c", _OBSERVER % str(Path(__file__).resolve().parent)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def run() -> dict:
    identity = WorkflowIdentity(workflow_key=WORKFLOW_KEY, workflow_version="1.0")
    lifecycle = WorkflowLifecycle()
    # `define` brings a Workflow under management; every later call addresses it
    # by identity. The distinction is the boundary's, not a convenience.
    lifecycle.define(Workflow(identity=identity))
    lifecycle.mark_ready(identity)
    lifecycle.enter_running(identity)

    # Read through the canonical monitoring surface, not the lifecycle itself.
    monitor = WorkflowMonitor(lifecycle)
    assert monitor.is_active(identity), monitor.state_of(identity)
    publish(WORKFLOW_KEY, str(monitor.state_of(identity).state),
            kind=WORKFLOW)
    while_running = _observe_independently()

    lifecycle.succeed(identity)
    assert monitor.is_terminal(identity) and monitor.is_success(identity)
    publish(WORKFLOW_KEY, str(monitor.state_of(identity).state),
            kind=WORKFLOW)
    after_success = _observe_independently()

    return {"while_running": while_running, "after_success": after_success}


def main() -> int:
    outcome = run()
    print("--- independent process, WHILE WORKFLOW RUNNING ---")
    print(json.dumps(outcome["while_running"]["live_by_kind"], indent=2))
    print("--- independent process, AFTER SUCCESS ---")
    print(json.dumps(outcome["after_success"]["live_by_kind"], indent=2))

    live_then = outcome["while_running"]["live_by_kind"]["workflow"]
    live_now = outcome["after_success"]["live_by_kind"]["workflow"]
    print()
    print(f"workflow live while running : {bool(live_then)}")
    print(f"workflow live after success : {bool(live_now)}")
    return 0 if (live_then and not live_now) else 1


if __name__ == "__main__":
    raise SystemExit(main())
