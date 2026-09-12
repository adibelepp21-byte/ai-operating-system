"""Entry point — P12 F-4: a live runtime, observed from another process.

At the repository root because driving a real runtime reaches `native_core` and
the observation projection lives in `tools/`; the root is where regions may be
wired together.

**The property being proved is not "a state can be written to a file".** It is
that an **independent process** can establish that a runtime is running *while
it is running*, and that the same evidence stops supporting that claim once the
runtime stops. Gate I forbids letting the same in-memory object prove its own
observability, so the observation is taken by a child process that shares no
state with the runtime — it holds only the published record and its own clock.

The sequence is deliberately ordered so that the live observation cannot be a
reconstruction:

```text
runtime.start()            → state is RUNNING, in memory, in THIS process
publish(state)             → the record is written
child process observes     → LIVE, while the runtime is still up
runtime.stop()             → state is STOPPED
publish(state)             → the record is overwritten
child process observes     → TERMINATED
```

Between the two child observations nothing changes but the runtime's actual
state. The observer is the same code both times.
"""

from __future__ import annotations

import json
import tempfile
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from native_core.core.infrastructure import (  # noqa: E402
    build_default_infrastructure)
from native_core.core.runtime import AIOSRuntime, RuntimeState  # noqa: E402
from tools.p12_runtime_observation import (  # noqa: E402
    OBSERVATION_ROOT, publish, what_is_running)

RUNTIME_ID = "p12-f4-runtime-observation"

#: Run in a child interpreter. It imports nothing from this module and receives
#: no runtime object — only the published record on disk and its own clock.
_OBSERVER = (
    "import json,sys;"
    "sys.path.insert(0, %r);"
    "from tools.p12_runtime_observation import what_is_running;"
    "print(json.dumps(what_is_running(), default=str))"
)


def _observe_independently() -> dict:
    """Ask a separate process what is running."""
    result = subprocess.run(
        [sys.executable, "-c", _OBSERVER % str(Path(__file__).resolve().parent)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def run() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        bootstrap = build_default_infrastructure(base_dir=Path(tmp))
        bootstrap.establish()
        runtime = AIOSRuntime(
            runtime_id=RUNTIME_ID,
            storage=bootstrap.get("storage"),
            substrate=bootstrap.get("execution-substrate"),
        )
        runtime.initialize()
        runtime.start()
        return _observe_around(runtime)


def _observe_around(runtime) -> dict:
    """Publish and observe on both sides of the runtime's real transition."""

    # The runtime is genuinely RUNNING in this process, now.
    assert runtime.state is RuntimeState.RUNNING, runtime.state
    publish(RUNTIME_ID, str(runtime.state))
    while_running = _observe_independently()

    runtime.stop()
    assert runtime.state is RuntimeState.STOPPED, runtime.state
    publish(RUNTIME_ID, str(runtime.state))
    after_stop = _observe_independently()

    return {"while_running": while_running, "after_stop": after_stop}


def main() -> int:
    outcome = run()
    print("--- observed by an independent process WHILE RUNNING ---")
    print(json.dumps(outcome["while_running"], indent=2))
    print("--- observed by an independent process AFTER STOP ---")
    print(json.dumps(outcome["after_stop"], indent=2))

    live_then = outcome["while_running"].get("answerable") and outcome["while_running"]["live"]
    live_now = outcome["after_stop"].get("live")
    print()
    print(f"live while running : {bool(live_then)}")
    print(f"live after stop    : {bool(live_now)}")
    return 0 if (live_then and not live_now) else 1


if __name__ == "__main__":
    raise SystemExit(main())
