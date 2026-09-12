"""P12-W6 — workflow integration verification (`§19` scope: `WORKFLOW`).

`§31` requires that workflow connect

```text
PLAN → HANDOFF → WORK → EXECUTION → OBSERVATION → VERIFICATION
```

and states plainly: *"P12 must verify actual workflow behavior rather than
merely inspect definitions."*

**So the unit measured here is the link, not the element.** Six present elements
prove nothing about a chain; `§48` says a relationship is not verified merely
because both surfaces exist. This module measures the **five joins** between the
six elements, and each join is either evidenced by a resident artifact that
names both sides, or it is `BROKEN`.

**An element that exists is not a link.** Where the only thing connecting two
elements is that both happen to mention the same actor or the same run, the join
is reported `BY CONVENTION` — reached by matching a name rather than by a
reference either side recorded. A convention is how a chain looks joined until
two things share a name.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

EVIDENCED = "EVIDENCED"
BY_CONVENTION = "BY CONVENTION"
BROKEN = "BROKEN"

#: `§31`'s chain, in its order.
WORKFLOW_CHAIN: Tuple[str, ...] = (
    "PLAN", "HANDOFF", "WORK", "EXECUTION", "OBSERVATION", "VERIFICATION",
)

#: The five joins between them.
WORKFLOW_JOINS: Tuple[Tuple[str, str], ...] = tuple(
    (WORKFLOW_CHAIN[i], WORKFLOW_CHAIN[i + 1])
    for i in range(len(WORKFLOW_CHAIN) - 1))


@dataclass(frozen=True)
class JoinResult:
    source: str
    target: str
    status: str
    evidence: Optional[str]
    detail: str


def _delegations() -> Tuple[dict, ...]:
    from tools import p12_provenance_verification as prov
    return prov.delegation_records()


def _traces() -> Tuple[dict, ...]:
    from tools import p12_provenance_verification as prov
    return prov.trace_records()


def _plan_to_handoff() -> JoinResult:
    """A plan reaching a delegation: the grant must name the plan it binds."""
    delegations = _delegations()
    naming = [d for d in delegations
              if "plan" in str(d.get("lifecycle_boundary", "")).lower()]
    if not naming:
        return JoinResult("PLAN", "HANDOFF", BROKEN, None,
                          "no delegation names the plan it is bound to")
    return JoinResult(
        "PLAN", "HANDOFF", EVIDENCED, "delegation.lifecycle_boundary",
        f"{len(naming)}/{len(delegations)} delegations name their bound plan")


def _handoff_to_work() -> JoinResult:
    """A delegation reaching the work it authorizes."""
    delegations = _delegations()
    scoped = [d for d in delegations if d.get("work_scope")]
    if not scoped:
        return JoinResult("HANDOFF", "WORK", BROKEN, None,
                          "no delegation declares a work scope")
    return JoinResult(
        "HANDOFF", "WORK", EVIDENCED, "delegation.work_scope",
        f"{len(scoped)}/{len(delegations)} delegations declare the work "
        "they authorize")


def _work_to_execution() -> JoinResult:
    """The join `§34` provenance also needs, and the one that is missing."""
    from tools import p12_provenance_verification as prov
    assembled = prov.assembly(delegations=_delegations(), traces=_traces())
    if assembled["status"] == prov.ASSEMBLABLE:
        return JoinResult("WORK", "EXECUTION", EVIDENCED,
                          "trace.delegation_id",
                          "every execution names the work it performed")
    if assembled["executions"] == 0:
        return JoinResult("WORK", "EXECUTION", BROKEN, None,
                          "no execution record exists to join")
    joined = assembled["joined"]
    total = assembled["executions"]
    if joined:
        # Some executions carry a real reference and some do not. Reported as
        # BY CONVENTION rather than EVIDENCED, because the weakest link governs:
        # a chain in which most executions name their work and some do not is
        # not a chain that can be followed for an arbitrary execution.
        return JoinResult(
            "WORK", "EXECUTION", BY_CONVENTION,
            "evidence record / provenance manifest",
            f"{joined}/{total} executions name the work they performed; the "
            f"remaining {total - joined} share only an actor name, and one "
            "actor holds many grants")
    return JoinResult(
        "WORK", "EXECUTION", BY_CONVENTION, "actor name",
        f"{total} execution(s) carry no reference to the "
        "work they performed; only the actor name is shared, and one actor "
        "holds many grants")


def _execution_to_observation() -> JoinResult:
    """An execution reaching a published observation of it."""
    from tools import p12_runtime_observation as obs
    traces = _traces()
    observations = obs.observations(obs.OBSERVATION_ROOT)
    if not observations:
        return JoinResult("EXECUTION", "OBSERVATION", BROKEN, None,
                          "no observation has been published")
    if not traces:
        return JoinResult("EXECUTION", "OBSERVATION", BROKEN, None,
                          "no execution record exists to observe")
    # A manifest names the observation subject for its execution, and the
    # independent reader resolves it against the observation record. Where that
    # holds, the link is a resolved reference rather than a shared name.
    from tools import p12_provenance_verification as prov
    manifests = prov.manifest_records()
    observed_ids = {o.runtime_id for o in observations}
    resolved = [m for m in manifests
                if m.get("observation_subject") in observed_ids]
    if resolved:
        return JoinResult(
            "EXECUTION", "OBSERVATION", EVIDENCED,
            "manifest.observation_subject",
            f"{len(resolved)}/{len(manifests)} manifest(s) name an observation "
            "subject that resolves to a published observation")

    runtimes = {t.get("runtime") for t in traces}
    # `runtime_id`, not `subject`. The first version of this probe read a field
    # that does not exist, and the join was reported BROKEN with an
    # AttributeError as its reason — a probe defect presented as a finding about
    # the system, and in the direction that overstates the defect. Disclosed
    # rather than quietly corrected, and a conformance control now asserts the
    # field is read from the real dataclass.
    subjects = {o.runtime_id for o in observations}
    shared = runtimes & subjects
    if shared:
        return JoinResult(
            "EXECUTION", "OBSERVATION", BY_CONVENTION, "runtime name",
            f"{len(shared)} name(s) appear on both sides ({sorted(shared)}); "
            "neither record references the other")
    return JoinResult(
        "EXECUTION", "OBSERVATION", BROKEN, None,
        f"no execution runtime {sorted(r for r in runtimes if r)} matches any "
        f"observed subject {sorted(subjects)}")


def _observation_to_verification() -> JoinResult:
    """An observation reaching a verification of what it observed."""
    from native_core.core.trace import VALID_STATUSES
    from tools import p12_runtime_observation as obs
    observations = obs.observations(obs.OBSERVATION_ROOT)
    if not observations:
        return JoinResult("OBSERVATION", "VERIFICATION", BROKEN, None,
                          "no observation has been published")
    if "verified" in VALID_STATUSES:
        return JoinResult("OBSERVATION", "VERIFICATION", EVIDENCED,
                          "execution record verified state", "")

    # No *execution record* can hold a verified state, and that finding stands.
    # But a provenance manifest records the verification requirement the grant
    # imposed together with the outcome the observed execution produced, and the
    # independent reader resolves both. Where that holds, the edge is carried —
    # by the P12 integration surface rather than by the ratified vocabulary,
    # which is exactly the separation `§9` requires.
    from tools import p12_provenance_verification as prov
    observed_ids = {o.runtime_id for o in observations}
    carried = [m for m in prov.manifest_records()
               if m.get("observation_subject") in observed_ids
               and m.get("verification_requirement")
               and m.get("outcome") is not None]
    if carried:
        return JoinResult(
            "OBSERVATION", "VERIFICATION", EVIDENCED,
            "manifest.verification_requirement + outcome",
            f"{len(carried)} manifest(s) carry the requirement and the outcome "
            f"for an observed execution; the ratified execution vocabulary is "
            f"still {sorted(VALID_STATUSES)} and holds no verified state")
    return JoinResult(
        "OBSERVATION", "VERIFICATION", BROKEN, None,
        f"the ratified execution vocabulary is {sorted(VALID_STATUSES)}; "
        "nothing an observation reaches can record that it was verified")


_JOINS = {
    ("PLAN", "HANDOFF"): _plan_to_handoff,
    ("HANDOFF", "WORK"): _handoff_to_work,
    ("WORK", "EXECUTION"): _work_to_execution,
    ("EXECUTION", "OBSERVATION"): _execution_to_observation,
    ("OBSERVATION", "VERIFICATION"): _observation_to_verification,
}


def verify() -> Tuple[JoinResult, ...]:
    results = []
    for join in WORKFLOW_JOINS:
        try:
            results.append(_JOINS[join]())
        except Exception as exc:  # pragma: no cover - defensive
            results.append(JoinResult(join[0], join[1], BROKEN, None,
                                      f"probe raised: {exc}"))
    return tuple(results)


def chain_is_connected() -> bool:
    """`§31` asks whether workflow *connects* the six. One broken link is enough."""
    return all(r.status == EVIDENCED for r in verify())


def summary() -> dict:
    results = verify()
    return {
        "elements": len(WORKFLOW_CHAIN),
        "joins": len(results),
        "evidenced": sum(1 for r in results if r.status == EVIDENCED),
        "by_convention": sum(1 for r in results if r.status == BY_CONVENTION),
        "broken": sum(1 for r in results if r.status == BROKEN),
        "chain_connected": chain_is_connected(),
        "weakest": tuple(f"{r.source}→{r.target}" for r in results
                         if r.status != EVIDENCED),
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.source:>12} → {result.target:<14} {result.status:<14} "
              f"{(result.evidence or '—'):<28} {result.detail[:46]}")
    print()
    print("summary:", summary())
    print()
    print("The unit is the link, not the element. Six present elements prove")
    print("nothing about a chain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
