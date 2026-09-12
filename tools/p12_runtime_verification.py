"""P12-W6 — runtime integration verification (`§19` scope: `RUNTIME`).

`§30` requires discovery of nine things: runtime entry points, runtime state,
runtime-hosted workflows, execution actors, state transitions, observation,
verification, failure, persistence. It closes: *"Claims about runtime
integration require runtime evidence where runtime evidence is the relevant
proof."*

**Two questions, reported separately.** Discovery asks whether each of the nine
has resident runtime evidence. Reachability asks something `§30` implies and
does not spell out: whether the runtime is entered by the system, or only by
hand. A runtime nobody reaches is discovered and not integrated, and merging the
two would let nine green discoveries describe a system that never runs.

**Reachability is measured from the import graph, not from file names.**
Classifying an entry point as a demonstrator because it is called
`..._proof.py` would be inference from a name — the thing this programme
repeatedly has to undo. The measurable question is whether any surface other
than the script itself reaches it.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

DISCOVERED = "DISCOVERED"
ABSENT = "ABSENT"

REACHED = "REACHED"
HAND_INVOKED = "HAND-INVOKED ONLY"

#: `§30`'s nine required discovery items, in its order.
RUNTIME_ITEMS: Tuple[str, ...] = (
    "runtime entry points", "runtime state", "runtime-hosted workflows",
    "execution actors", "state transitions", "observation", "verification",
    "failure", "persistence",
)


@dataclass(frozen=True)
class ItemResult:
    item: str
    status: str
    count: int
    detail: str


@dataclass(frozen=True)
class EntryPoint:
    module: str
    status: str
    reached_by: Tuple[str, ...]


def entry_points() -> Tuple[EntryPoint, ...]:
    """Every root-level runnable module, and what reaches it.

    Root level because that is where `tools/` and `consumers/` may be wired
    together — the only place in this architecture where a whole run can be
    assembled, and therefore the only place a runtime can be entered.
    """
    roots = sorted(p for p in REPO_ROOT.glob("*.py"))
    names = {p.stem for p in roots}
    reached: Dict[str, set] = {name: set() for name in names}

    for path in sorted(REPO_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module.split(".")[0]]
            for module in modules:
                if module in names and path.stem != module:
                    reached[module].add(
                        path.relative_to(REPO_ROOT).as_posix())

    found = []
    for path in roots:
        callers = tuple(sorted(reached[path.stem]))
        # A caller that is itself only hand-invoked does not make this entry
        # point reachable by the system; it makes two hand-invoked scripts.
        system_callers = tuple(
            c for c in callers
            if not (REPO_ROOT / c).parent == REPO_ROOT)
        found.append(EntryPoint(
            module=path.name,
            status=REACHED if system_callers else HAND_INVOKED,
            reached_by=callers))
    return tuple(found)


def _runtime_entry_points() -> ItemResult:
    points = entry_points()
    if not points:
        return ItemResult("runtime entry points", ABSENT, 0,
                          "no root-level runnable module exists")
    hand = [p for p in points if p.status == HAND_INVOKED]
    return ItemResult(
        "runtime entry points", DISCOVERED, len(points),
        f"{len(points)} root entry points, {len(hand)} reached by nothing "
        "but a hand-run script")


def _runtime_state() -> ItemResult:
    from tools import p12_runtime_observation as obs
    found = obs.observations(obs.OBSERVATION_ROOT)
    runtime = [o for o in found if o.kind == "runtime"]
    if not runtime:
        return ItemResult("runtime state", ABSENT, 0,
                          "no runtime observation has been published")
    return ItemResult("runtime state", DISCOVERED, len(runtime),
                      f"{len(runtime)} published runtime observation(s)")


def _hosted_workflows() -> ItemResult:
    from tools import p12_runtime_observation as obs
    found = [o for o in obs.observations(obs.OBSERVATION_ROOT)
             if o.kind == "workflow"]
    if not found:
        return ItemResult("runtime-hosted workflows", ABSENT, 0,
                          "no workflow observation has been published")
    return ItemResult("runtime-hosted workflows", DISCOVERED, len(found),
                      f"{len(found)} workflow observation(s)")


def _execution_actors() -> ItemResult:
    from tools import p12_provenance_verification as prov
    actors = {r.get("agent_instance") for r in prov.trace_records()}
    actors.discard(None)
    if not actors:
        return ItemResult("execution actors", ABSENT, 0,
                          "no execution record names an actor")
    return ItemResult("execution actors", DISCOVERED, len(actors),
                      f"{len(actors)} distinct actor(s) in durable records: "
                      f"{sorted(actors)}")


def _state_transitions() -> ItemResult:
    from tools import p12_runtime_observation as obs
    found = obs.observations(obs.OBSERVATION_ROOT)
    states = {o.state for o in found}
    if len(states) < 2:
        return ItemResult(
            "state transitions", ABSENT, len(states),
            f"observations record {len(states)} distinct state(s); a single "
            "state is a reading, not a transition")
    return ItemResult("state transitions", DISCOVERED, len(states),
                      f"{len(states)} distinct observed states: {sorted(states)}")


def _observation() -> ItemResult:
    from tools import p12_runtime_observation as obs
    answer = obs.what_is_running(obs.OBSERVATION_ROOT)
    # `observations` is a count, not a sequence. The first version of this probe
    # called `len()` on it and the item reported ABSENT with the TypeError as
    # its reason — an observation surface that works, reported as missing by a
    # defect in the thing measuring it.
    count = int(answer.get("observations", 0))
    if not answer["answerable"] and count == 0:
        return ItemResult("observation", ABSENT, 0,
                          f"no observation to read: {answer.get('reason')}")
    return ItemResult(
        "observation", DISCOVERED, count,
        f"answerable={answer['answerable']}, {count} observation(s), "
        f"scope={answer.get('scope')}")


def _verification() -> ItemResult:
    """Verification **as a runtime state**, not as a document."""
    from native_core.core.trace import VALID_STATUSES
    if "verified" in VALID_STATUSES:
        return ItemResult("verification", DISCOVERED, 1,
                          "an execution record can hold a verified state")
    return ItemResult(
        "verification", ABSENT, 0,
        f"the ratified execution vocabulary is {sorted(VALID_STATUSES)}; no "
        "runtime record can say an execution was verified")


def _failure() -> ItemResult:
    from tools import p12_trace_registry as traces
    failures = traces.what_has_failed(traces.STORE_ROOT)
    if not failures:
        return ItemResult("failure", ABSENT, 0,
                          "no durable record of a runtime failure exists")
    return ItemResult("failure", DISCOVERED, len(failures),
                      f"{len(failures)} durable failure record(s)")


def _persistence() -> ItemResult:
    from tools import p12_runtime_observation as obs
    from tools import p12_trace_registry as traces
    stores = traces.discover(traces.STORE_ROOT)
    observed = obs.OBSERVATION_ROOT.is_dir()
    if not stores and not observed:
        return ItemResult("persistence", ABSENT, 0,
                          "neither a trace store nor an observation root exists")
    return ItemResult(
        "persistence", DISCOVERED, len(stores),
        f"{len(stores)} durable trace store(s); observation root "
        f"{'present' if observed else 'absent'}")


_ITEMS = {
    "runtime entry points": _runtime_entry_points,
    "runtime state": _runtime_state,
    "runtime-hosted workflows": _hosted_workflows,
    "execution actors": _execution_actors,
    "state transitions": _state_transitions,
    "observation": _observation,
    "verification": _verification,
    "failure": _failure,
    "persistence": _persistence,
}


def verify() -> Tuple[ItemResult, ...]:
    results = []
    for item in RUNTIME_ITEMS:
        try:
            results.append(_ITEMS[item]())
        except Exception as exc:  # pragma: no cover - defensive
            results.append(ItemResult(item, ABSENT, 0, f"probe raised: {exc}"))
    return tuple(results)


def reachability() -> dict:
    points = entry_points()
    reached = [p for p in points if p.status == REACHED]
    return {
        "entry_points": len(points),
        "reached_by_the_system": len(reached),
        "hand_invoked_only": len(points) - len(reached),
        "status": REACHED if reached else HAND_INVOKED,
        "detail": (
            "no root entry point is reached from any surface other than a "
            "hand-run script: there is no service, scheduler, or dispatcher "
            "that enters the runtime"
            if not reached else
            f"{len(reached)} entry point(s) are reached by a non-root surface"),
    }


def summary() -> dict:
    results = verify()
    reach = reachability()
    return {
        "items": len(results),
        "discovered": sum(1 for r in results if r.status == DISCOVERED),
        "absent": sum(1 for r in results if r.status == ABSENT),
        "absent_items": tuple(r.item for r in results if r.status == ABSENT),
        "entry_points": reach["entry_points"],
        "reachability": reach["status"],
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.item:<25} {result.status:<11} {result.count:>3}  "
              f"{result.detail[:62]}")
    print()
    reach = reachability()
    print(f"reachability: {reach['status']} — {reach['detail']}")
    for point in entry_points():
        print(f"  {point.module:<40} {point.status:<18} "
              f"{', '.join(point.reached_by) or '—'}")
    print()
    print("summary:", summary())
    print()
    print("A runtime nobody reaches is discovered, not integrated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
