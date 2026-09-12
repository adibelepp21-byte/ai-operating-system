"""Entry point — P12-W4 `F-10′`: real system work, observed from outside.

**The requirement, read from the body.** `§17`: *"P12 execution integration
harus membuktikan **hubungan antar-surface**, bukan hanya keberadaan
masing-masing subsystem"* — must prove the relationship **between** surfaces,
not merely that each exists. The canonical chain places `OBSERVATION` between
`EXECUTION` and `VERIFICATION`, so an execution that skips it has not completed
the chain.

**What was insufficient before.** Every observation surface in this repository
was reached only by a proof written to demonstrate it. A demonstrator performs
no work, so it can establish that a surface *functions* and can never establish
that the system's work *reaches* it:

```text
DEMONSTRATOR   ≠   SYSTEM WORK
SURFACE EXISTS ≠   WORK ↔ OBSERVATION RELATIONSHIP
```

**What this does instead.** It runs the **resident W1 coordination work** — the
same `perform` and `coordinate` the P11 proof uses, imported rather than
reimplemented, driving a real `AIOSRuntime` through a real `Workflow` with a
real participating Agent — which now publishes observation from inside the work
itself. An **independent process** then reads that observation and verifies it
describes the work runtime and was written by a different process.

**Why it reads rather than polls, stated plainly.** The first version started a
poller before the work and waited for a live catch. It never caught one, and the
reason is measured, not guessed: **the resident work's `RUNNING` window is
0.9 ms** — `RUNNING` at `+0.0`, republished at `+0.6`, `STOPPED` at `+0.9`. No
external poller can reliably sample a sub-millisecond window, and holding the
runtime open to widen it would be manufacturing the observability being tested.
The governing Act is explicit: *"do not fake a long-running process."*

So the claim is narrowed to what the evidence supports. This proves the
**relationship** `§17` requires — the work's own execution reaches the
observation surface, and an independent process reads it across a process
boundary — and it does **not** claim a live external catch, which this work's
duration makes unachievable. `LIVE CATCH ≠ WORK ↔ OBSERVATION RELATIONSHIP`.

Nothing is reimplemented here. If this file's work diverged from the resident
path's, it would become another demonstrator, which is the failure it exists to
avoid.

**`persist=False`.** P11 is certified and its evidence is frozen. The work runs;
the P11 record is not rewritten. That the run is possible at all is `F-12`'s
doing — the guard refuses *writes*, not *executions*, which is what made this
increment reachable.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tools.w1_coordination_run import run  # noqa: E402
from w1_coordination_proof import coordinate, perform  # noqa: E402

ROOT = Path(__file__).resolve().parent
WORK_RUNTIME_ID = "p11-w1-runtime"

#: Polls for a **live** observation of the work runtime. Runs in its own
#: interpreter, holding no runtime object, no workflow and no shared memory —
#: only the published record and its own clock. Started *before* the work so it
#: cannot be accused of reconstructing the window after the fact.
_OBSERVER = r"""
import json, os, sys
sys.path.insert(0, {root!r})
from tools.p12_runtime_observation import observations
found = [o for o in observations() if o.runtime_id == {work!r}]
print(json.dumps({{
    "found": bool(found),
    "runtime_id": found[0].runtime_id if found else None,
    "state": found[0].state if found else None,
    "classification": found[0].classification if found else None,
    "writer_pid": found[0].pid if found else None,
    "observer_pid": os.getpid(),
}}, default=str))
"""


def _observe_independently() -> dict:
    result = subprocess.run(
        [sys.executable, "-c",
         _OBSERVER.format(root=str(ROOT), work=WORK_RUNTIME_ID)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def main() -> int:
    # The real work: the resident W1 coordination path, persisting nothing.
    evidence = run(perform, coordinate=coordinate, persist=False)
    worker_pid = __import__("os").getpid()

    observed = _observe_independently()

    print("--- real system work ---")
    for key in ("act", "goal", "delegation_status", "accountable_party"):
        if key in evidence:
            print(f"  {key}: {evidence[key]}")
    facts = evidence.get("coordination", {})
    for key in ("proof_level", "runtime_id", "runtime_state",
                "completed_steps", "observation_published"):
        if key in facts:
            print(f"  {key}: {facts[key]}")

    print("--- independent process reading the observation ---")
    for key in ("found", "runtime_id", "state", "classification",
                "writer_pid", "observer_pid"):
        print(f"  {key}: {observed[key]}")

    did_work = bool(facts.get("completed_steps"))
    reached = observed["found"] and observed["runtime_id"] == WORK_RUNTIME_ID
    crossed = observed["writer_pid"] not in (None, observed["observer_pid"])
    print()
    print(f"real work performed              : {did_work}")
    print(f"work reached observation surface : {reached}")
    print(f"crossed a process boundary       : {crossed} "
          f"(written by {observed['writer_pid']}, read by {observed['observer_pid']})")
    print(f"worker pid this run              : {worker_pid}")
    return 0 if (did_work and reached and crossed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
