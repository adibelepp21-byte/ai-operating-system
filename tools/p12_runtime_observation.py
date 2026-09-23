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

from tools.p12_certified_evidence_guard import guard  # noqa: E402

#: Where **live** runtime observations are published. One file per runtime id.
#:
#: Moved here under `GOAL-V2-002`. Until then this pointed into
#: `docs/architecture/p12/`, which became certified evidence under `FD-P12-006`.
#: An observation is a live projection (*"these files state what was last
#: observed"*), so every run rewrote the file, and certified evidence was
#: rewritten with it. That happened in commits `7f6120c` and `d18bac4`, and on
#: every run of the tools suite since.
#:
#: The live root sits outside every phase directory. Certifying a phase can
#: therefore never freeze a live projection again.
OBSERVATION_ROOT = REPO_ROOT / "docs/operations/runtime-observations"

#: P12's observations **as certified**. They are read as history and never
#: written. `publish` routes through the certified-evidence guard, which refuses
#: this root.
CERTIFIED_OBSERVATION_ROOT = REPO_ROOT / "docs/architecture/p12/runtime-observations"

#: The live root's own default, kept so that a caller passing
#: `OBSERVATION_ROOT` unpatched gets the merged view, while a test that
#: redirects `OBSERVATION_ROOT` to an isolated directory reads that directory
#: alone.
_LIVE_DEFAULT = OBSERVATION_ROOT

#: Provenance of an observation: where it was read from.
LIVE_ORIGIN = "live"
CERTIFIED_ORIGIN = "certified-p12"

#: How long a `RUNNING` observation may be trusted as live. Beyond this a record
#: is `STALE`: the runtime may still be up, or may have died without publishing
#: a terminal state, and the observation cannot distinguish the two. The horizon
#: is short deliberately — a generous one would let a long-dead runtime read as
#: live, which is the failure this module exists to prevent.
LIVE_HORIZON_SECONDS = 30.0

#: What a published observation is *about*. Two canonical live-state
#: vocabularies exist and they are not interchangeable: a Runtime can be RUNNING
#: while no Workflow is, and a Workflow can be RUNNING on a Runtime that is
#: itself only INITIALIZED. Merging them into one "is it running" would lose the
#: distinction the boundaries were built to keep.
RUNTIME = "runtime"
WORKFLOW = "workflow"

LIVE = "LIVE"
STALE = "STALE"
TERMINATED = "TERMINATED"
UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Observation:
    """One published observation, with the freshness that qualifies it."""

    runtime_id: str
    kind: str
    state: str
    observed_at: str
    pid: int
    age_seconds: float
    classification: str
    #: For a workflow observation, the identity of the Runtime hosting it.
    #: `None` for a runtime observation, and for any workflow observation
    #: published before this field existed — absence is absence, never a guess.
    hosted_by: Optional[str] = None
    #: Where the record was read from: `live`, or `certified-p12` for an
    #: observation frozen by P12's certification. A reader answering *"what is
    #: running?"* sees both, and can tell them apart.
    origin: str = LIVE_ORIGIN

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
    kind: str = RUNTIME,
    hosted_by: Optional[str] = None,
) -> Path:
    """Publish the runtime's *current* state so another process can read it.

    `state` is the value the runtime itself reports. This function never
    computes, guesses or defaults a state: a caller that cannot read a real
    runtime has nothing to publish, and publishing a fabricated state would
    manufacture exactly the certainty the governing Act forbids.

    `hosted_by` is the identity of the Runtime hosting a Workflow, supplied by
    the caller that actually holds both. **It is never inferred.** The W1 edge
    `workflow ↔ runtime` states its contract as *"a workflow observation names
    the runtime hosting it"*, and until this field existed the record had
    nowhere to put that: `runtime_id` is the subject's own identity, so a
    workflow could only have shared it by being published under the runtime's
    name and losing its own. The edge therefore read `UNVERIFIED` — correctly,
    because nothing recorded the relation — while the relation itself was real
    in every hosted run. The field is written only when supplied, so a record
    without it is a record that did not claim one.
    """
    root.mkdir(parents=True, exist_ok=True)
    moment = (now or _now()).isoformat()
    path = root / f"{runtime_id}.observation.json"
    payload = {
        "runtime_id": runtime_id,
        "kind": kind,
        "state": state,
        "observed_at": moment,
        "pid": os.getpid(),
    }
    if hosted_by is not None:
        payload["hosted_by"] = hosted_by
    # Refuses a write into certified-phase evidence. The default root is live,
    # so the guard only fires for a caller aiming at a certified root.
    guard(path).write_text(json.dumps(payload, indent=2) + "\n",
                           encoding="utf-8")
    return path


def _classify(state: str, age: float, horizon: float) -> str:
    """Freshness-qualified classification. The only place the rule lives."""
    normalized = state.rsplit(".", 1)[-1].strip().upper()
    # Runtime terminals: STOPPING/STOPPED. Workflow terminals: SUCCEEDED/FAILED.
    # Both vocabularies are read here; neither is translated into the other.
    if normalized in ("STOPPED", "STOPPING", "SUCCEEDED", "FAILED"):
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
    """Every published observation, each qualified by its own age.

    Called with the live default, this reads P12's certified observations too,
    and lets a live record supersede a certified one for the same runtime id.
    Each observation carries its `origin`. Called with any other root, it reads
    that root alone, which is how the suites isolate it.
    """
    if Path(root) == _LIVE_DEFAULT:
        sources = ((CERTIFIED_OBSERVATION_ROOT, CERTIFIED_ORIGIN),
                   (Path(root), LIVE_ORIGIN))
    else:
        sources = ((Path(root), LIVE_ORIGIN),)
    moment = now or _now()
    merged = {}
    for source, origin in sources:
        for observation in _read(source, moment, horizon, origin):
            merged[observation.runtime_id] = observation
    # Ordered as the files were always read: by file name, which is the
    # runtime id plus a fixed suffix.
    return tuple(merged[key] for key in
                 sorted(merged, key=lambda k: f"{k}.observation.json"))


def _read(root: Path, moment: datetime, horizon: float,
          origin: str) -> Tuple[Observation, ...]:
    if not root.is_dir():
        return ()
    found = []
    for path in sorted(root.glob("*.observation.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        observed_at = datetime.fromisoformat(payload["observed_at"])
        age = (moment - observed_at).total_seconds()
        found.append(
            Observation(
                runtime_id=payload["runtime_id"],
                # Records written before workflow observation existed carry no
                # `kind`. They are runtimes, and the default says so explicitly
                # rather than leaving the field to be guessed downstream.
                kind=payload.get("kind", RUNTIME),
                state=payload["state"],
                observed_at=payload["observed_at"],
                pid=int(payload["pid"]),
                age_seconds=age,
                classification=_classify(payload["state"], age, horizon),
                hosted_by=payload.get("hosted_by"),
                origin=origin,
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
        "scope": (
            "runtimes and workflows that publish observations; "
            "unobserved subjects of either kind are not covered"
        ),
        "live": tuple(
            {
                "runtime_id": o.runtime_id,
                "kind": o.kind,
                "age_seconds": round(o.age_seconds, 3),
            }
            for o in live
        ),
        "live_by_kind": {
            kind: tuple(o.runtime_id for o in live if o.kind == kind)
            for kind in (RUNTIME, WORKFLOW)
        },
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
