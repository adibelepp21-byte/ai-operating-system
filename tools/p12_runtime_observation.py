"""P12-W2 / P12-W5 — external observability of live Runtime state.

Authorized by the Founder P12 Authorization `§15` (Unified Operational State)
and `§18`, which requires *"What is running?"* to be answered evidence-backed.

**What discovery found, before any construction.** The hypothesis that AIOS has
no runtime observation is **false**. `native_core/core/runtime` carries a
canonical lifecycle — `RuntimeState` with five members, `VALID_TRANSITIONS`
enforcing `CREATED → INITIALIZED → RUNNING → STOPPING → STOPPED`, and
`AIOSRuntime.state` exposing it — and two resident root proofs already drive a
real runtime and read that state while it is genuinely `RUNNING`.

What is absent is **externalization**. `self._state` is an in-memory instance
attribute; nothing outside the owning process can see it, which is exactly what
`derived_views` recorded: *"Runtime state is per-process and unobserved from
outside."* So this module does not create observation. It projects an
observation that already exists across a process boundary, and adds the one
thing a projection of live state cannot do without:

```text
FRESHNESS
```

**Why freshness is the whole problem.** A published record saying `RUNNING` is
evidence that a runtime *was* running when the record was written. Reading it an
hour later and answering *"what is running"* with it would be
`HISTORICAL EVIDENCE` dressed as `LIVE RUNTIME STATE` — the substitution the
governing Act names first. So an observation is only reported as live while it
is fresh, and a `RUNNING` record past its horizon degrades to `STALE`, which
answers *"is it running?"* with **UNKNOWN** rather than yes or no.

```text
TRACE OF WHAT RAN   ≠  OBSERVATION OF WHAT IS RUNNING
RUNNING + FRESH     →  LIVE
RUNNING + EXPIRED   →  STALE        (not "running", and not "stopped")
STOPPED             →  TERMINATED
no record           →  UNKNOWN      (not "0 running")
```

**Native Core is untouched.** The runtime boundary already owns `RuntimeState`
and remains its only producer; this reads what it exposes. `§11` freezes eleven
boundaries and expressly permits integration layers outside them.

**Observation grants nothing.** `§18`: `SELF-MODEL ≠ AUTHORITY`. Nothing here
returns a permission, starts or stops a runtime, or alters any state it reads.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Where published runtime observations are kept. One file per runtime id.
OBSERVATION_ROOT = REPO_ROOT / "docs/architecture/p12/runtime-observations"

#: How long a `RUNNING` observation may be trusted as live. Beyond this a record
#: is `STALE`: the runtime may still be up, or may have died without publishing
#: a terminal state, and the observation cannot distinguish the two. The horizon
#: is short deliberately — a generous one would let a long-dead runtime read as
#: live, which is the failure this module exists to prevent.
LIVE_HORIZON_SECONDS = 30.0

LIVE = "LIVE"
STALE = "STALE"
TERMINATED = "TERMINATED"
UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Observation:
    """One published runtime observation, with the freshness that qualifies it."""

    runtime_id: str
    state: str
    observed_at: str
    pid: int
    age_seconds: float
    classification: str

    @property
    def is_live(self) -> bool:
        return self.classification == LIVE


def _now() -> datetime:
    return datetime.now(timezone.utc)


def publish(
    runtime_id: str,
    state: str,
    root: Path = OBSERVATION_ROOT,
    now: Optional[datetime] = None,
) -> Path:
    """Publish the runtime's *current* state so another process can read it.

    `state` is the value the runtime itself reports. This function never
    computes, guesses or defaults a state: a caller that cannot read a real
    runtime has nothing to publish, and publishing a fabricated state would
    manufacture exactly the certainty the governing Act forbids.
    """
    root.mkdir(parents=True, exist_ok=True)
    moment = (now or _now()).isoformat()
    path = root / f"{runtime_id}.observation.json"
    path.write_text(
        json.dumps(
            {
                "runtime_id": runtime_id,
                "state": state,
                "observed_at": moment,
                "pid": os.getpid(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _classify(state: str, age: float, horizon: float) -> str:
    """Freshness-qualified classification. The only place the rule lives."""
    normalized = state.rsplit(".", 1)[-1].strip().upper()
    if normalized in ("STOPPED", "STOPPING"):
        return TERMINATED
    if normalized == "RUNNING":
        return LIVE if age <= horizon else STALE
    # CREATED / INITIALIZED are real lifecycle states that are *not* running,
    # and are not terminal either. Reporting them as either would be a lie in
    # one direction or the other.
    return UNKNOWN if age > horizon else normalized


def observations(
    root: Path = OBSERVATION_ROOT,
    now: Optional[datetime] = None,
    horizon: float = LIVE_HORIZON_SECONDS,
) -> Tuple[Observation, ...]:
    """Every published observation, each qualified by its own age."""
    if not root.is_dir():
        return ()
    moment = now or _now()
    found = []
    for path in sorted(root.glob("*.observation.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        observed_at = datetime.fromisoformat(payload["observed_at"])
        age = (moment - observed_at).total_seconds()
        found.append(
            Observation(
                runtime_id=payload["runtime_id"],
                state=payload["state"],
                observed_at=payload["observed_at"],
                pid=int(payload["pid"]),
                age_seconds=age,
                classification=_classify(payload["state"], age, horizon),
            )
        )
    return tuple(found)


def what_is_running(
    root: Path = OBSERVATION_ROOT,
    now: Optional[datetime] = None,
    horizon: float = LIVE_HORIZON_SECONDS,
) -> dict:
    """Answer *"what is running?"* — or say the evidence cannot answer it.

    Returns `answerable: False` when no observation exists **and** when every
    observation is stale. Both are `UNKNOWN`, and for the same reason: the
    evidence does not establish what is running now. An empty result is never
    reported as "nothing is running".
    """
    found = observations(root, now=now, horizon=horizon)
    if not found:
        return {
            "answerable": False,
            "reason": "no runtime observation published; absence is not zero",
            "live": (),
            "observations": 0,
        }
    live = tuple(o for o in found if o.is_live)
    stale = tuple(o for o in found if o.classification == STALE)
    if not live and stale:
        return {
            "answerable": False,
            "reason": (
                f"{len(stale)} observation(s) report RUNNING but exceed the "
                f"{horizon:g}s liveness horizon; a stale record cannot establish "
                "current state"
            ),
            "live": (),
            "stale": tuple(o.runtime_id for o in stale),
            "observations": len(found),
        }
    return {
        "answerable": True,
        # The scope is part of the answer, not a caveat in a docstring. This
        # establishes the state of runtimes that **publish** observations, and
        # says nothing about any runtime that does not. An empty `live` means
        # "none of the observed runtimes is live" — never "nothing is running".
        # `ONE REAL PATH ≠ SYSTEM-WIDE COVERAGE`.
        "scope": "runtimes that publish observations; unobserved runtimes are not covered",
        "live": tuple(
            {"runtime_id": o.runtime_id, "age_seconds": round(o.age_seconds, 3)}
            for o in live
        ),
        "terminated": tuple(
            o.runtime_id for o in found if o.classification == TERMINATED
        ),
        "observations": len(found),
    }


def main(argv=None) -> int:
    answer = what_is_running()
    print(json.dumps(answer, indent=2, default=str))
    for observation in observations():
        print(
            f"  {observation.runtime_id:<28} {observation.state:<28} "
            f"{observation.classification:<12} age={observation.age_seconds:.1f}s"
        )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
