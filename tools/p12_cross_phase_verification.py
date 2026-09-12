"""P12-W6 — cross-phase verification by *exercise*, not by existence.

Authorized by the Founder P12 Authorization `§19`, whose minimum verification
scope names `CROSS-PHASE CONTRACTS`, and which closes with the sentence this
module exists to honour:

> *"P12-W6 tidak boleh dianggap selesai hanya karena unit tests individual
> hijau."*

`§45`: *"W6 verifies P4–P11 as an integrated operating system. Verification must
test relationships, not only isolated components."* `§48` states the rule in the
form that matters here:

```text
A RELATIONSHIP IS NOT VERIFIED MERELY BECAUSE BOTH SURFACES EXIST
```

**So this module never reads a declaration.** An import, a registry entry, a
Capability record and a conformance test all establish that a surface *exists*.
None of them establishes that anything *crossed* it. The only admissible evidence
here is a record produced **by an execution**: a Trace record naming what an Agent
Instance actually used, or a runtime/workflow observation published by a real run.

**Two taxonomies, not one.** The canonical phase list (`P4 Runtime · P5
Intelligence · P6 Knowledge · P7 Memory · P8 Tools · P9 Workflow · P10 Department
· P11 Organization`) is **not** the eleven Native Core boundaries. `P5`, `P8`,
`P10` and `P11` have no 1:1 boundary, and `§47` says plainly that *"the actual
graph governs"*. Phases are therefore resolved to the evidence that would show
them exercised, not to a boundary name that happens to look similar.

**The expected result is not a clean sheet.** A verifier built to return
`VERIFIED` for everything would be measuring itself. Where no execution has
crossed a phase, this reports `NOT EXERCISED`, and where the evidence cannot
establish the question it reports `UNKNOWN` — neither of which is a failure of the
phase, and both of which are the honest state of a system whose integration is
being built rather than asserted.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Tuple

from tools import p12_runtime_observation as observation
from tools import p12_trace_registry as traces

REPO_ROOT = Path(__file__).resolve().parents[1]

#: `§9` of the canonical blueprint, verbatim and in order. The names are the
#: canon's, not a restatement: `P8` is *Tools*, not `skill`, even though the
#: Native Core boundary is named `skill`.
CANONICAL_PHASES: Tuple[Tuple[str, str], ...] = (
    ("P4", "Runtime"),
    ("P5", "Intelligence"),
    ("P6", "Knowledge"),
    ("P7", "Memory"),
    ("P8", "Tools"),
    ("P9", "Workflow"),
    ("P10", "Department"),
    ("P11", "Organization"),
)

#: `§9` of the P12 Blueprint's edge model. `VERIFIED` is reserved for a crossing
#: an execution actually made.
EXERCISED = "EXERCISED"
NOT_EXERCISED = "NOT EXERCISED"
UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class PhaseResult:
    phase: str
    name: str
    status: str
    evidence: str
    locator: str


def _trace_records():
    return tuple(
        record for _store, record in traces.all_records(traces.STORE_ROOT)
    )


def _runtime_exercised(records) -> Tuple[bool, str]:
    runtimes = {r.runtime for r in records if r.runtime}
    if runtimes:
        return True, f"Trace records name runtimes {sorted(runtimes)}"
    return False, "no Trace record names a runtime"


def _intelligence_exercised(records) -> Tuple[bool, str]:
    """P5 is exercised when an Intelligence Agent Instance actually acted."""
    actors = {
        r.agent_instance for r in records
        if r.agent_instance and "intelligence" in r.agent_instance
    }
    if actors:
        return True, f"Trace records authored by {sorted(actors)}"
    return False, "no Trace record names an intelligence Agent Instance"


def _knowledge_exercised(records) -> Tuple[bool, str]:
    consumed = {k for r in records for k in (r.knowledge_consumed or ())}
    if consumed:
        return True, f"knowledge_consumed {sorted(consumed)}"
    return False, "knowledge_consumed is empty in every Trace record"


def _memory_exercised(records) -> Tuple[bool, str]:
    consumed = {m for r in records for m in (r.memory_consumed or ())}
    if consumed:
        return True, f"memory_consumed {sorted(consumed)}"
    return False, "memory_consumed is empty in every Trace record"


def _tools_exercised(records) -> Tuple[bool, str]:
    used = {t for r in records for t in (r.tools_used or ())}
    skills = {s for r in records for s in (r.skills_used or ())}
    if used or skills:
        return True, f"tools_used {sorted(used)} · skills_used {sorted(skills)}"
    return False, "no Trace record records a tool or skill being used"


def _workflow_exercised(_records) -> Tuple[bool, str]:
    # `OBSERVATION_ROOT` is read at call time, not bound at import. The first
    # version used the function's default argument, which fixed the evidence
    # root at import and made these predicates impossible to point at
    # alternative evidence — so the control proving "existence is not exercise"
    # could not actually be run against an empty corpus.
    live = [o for o in observation.observations(observation.OBSERVATION_ROOT)
            if o.kind == observation.WORKFLOW]
    if live:
        return True, f"workflow observation published for {[o.runtime_id for o in live]}"
    return False, "no workflow observation has been published"


def _department_exercised(records) -> Tuple[bool, str]:
    """P10 is exercised when a delegated actor actually acted.

    **The first version of this predicate was itself a `§48` violation.** It
    returned `EXERCISED` because delegation *records* exist — a declaration that
    a Department delegated, not evidence that anything crossed the boundary. A
    verifier built to refuse "both surfaces exist" cannot accept "a record
    exists" one function later.

    The admissible evidence is the **intersection**: an actor named as a
    delegation recipient that also authored a Trace record. That is the
    Department boundary being crossed by an execution rather than described.
    """
    from tools import delegation_catalog as catalog

    delegated = {
        d.delegated_actor for d in catalog.read_delegations() if d.delegated_actor
    }
    acted = {r.agent_instance for r in records if r.agent_instance}
    crossed = delegated & acted
    if crossed:
        return True, (
            f"delegated actors that authored a Trace record: {sorted(crossed)}"
        )
    if delegated and not acted:
        return False, (
            f"{len(delegated)} delegation(s) exist but no delegated actor has "
            "authored a Trace record — a delegation record is a declaration"
        )
    return False, "no delegated actor has acted"


def _organization_exercised(_records) -> Tuple[bool, str]:
    """P11 is exercised when real organizational work reached observation."""
    observed = [
        o.runtime_id for o in observation.observations(observation.OBSERVATION_ROOT)
        if o.kind == observation.RUNTIME and o.runtime_id.startswith("p11-")
    ]
    if observed:
        return True, f"organizational work runtime observed: {observed}"
    return False, "no P11 work runtime has published an observation"


_PREDICATES: dict = {
    "P4": _runtime_exercised,
    "P5": _intelligence_exercised,
    "P6": _knowledge_exercised,
    "P7": _memory_exercised,
    "P8": _tools_exercised,
    "P9": _workflow_exercised,
    "P10": _department_exercised,
    "P11": _organization_exercised,
}


def verify(root: Path = REPO_ROOT) -> Tuple[PhaseResult, ...]:
    """Classify each canonical phase by whether an execution crossed it."""
    records = _trace_records()
    results = []
    for phase, name in CANONICAL_PHASES:
        predicate: Optional[Callable] = _PREDICATES.get(phase)
        if predicate is None:
            results.append(PhaseResult(
                phase, name, UNKNOWN, "no evidence predicate", ""))
            continue
        try:
            exercised, evidence = predicate(records)
        except Exception as exc:  # pragma: no cover - defensive
            results.append(PhaseResult(
                phase, name, UNKNOWN, f"evidence unreadable: {exc}", ""))
            continue
        results.append(PhaseResult(
            phase, name,
            EXERCISED if exercised else NOT_EXERCISED,
            evidence,
            "durable Trace records and published observations",
        ))
    return tuple(results)


#: Executions written to demonstrate a surface rather than to perform system
#: work. Named explicitly because the distinction is material and inventing a
#: general taxonomy for it is not canonically grounded (`F-13`): this is a list
#: of three known artifacts, not a classification scheme.
DEMONSTRATOR_EXECUTIONS = (
    "p12-w4-durability-proof",
    "p12-f4-runtime-observation",
    "p12-f11-workflow-observation",
)


def summary(root: Path = REPO_ROOT) -> dict:
    """Counts, plus how much of the evidence comes from a demonstrator.

    Reported because six-of-eight reads very differently depending on whether
    the crossings were made by the system's work or by proofs written to show
    the surfaces function. Suppressing that would repeat the `F-10` error, where
    a coverage figure counted its own demonstrator.
    """
    results = verify(root)
    demonstrator_only = tuple(
        r.phase for r in results
        if r.status == EXERCISED
        and any(name in r.evidence for name in DEMONSTRATOR_EXECUTIONS)
        and not any(
            marker in r.evidence for marker in ("p11-", "engineering-intelligence")
        )
    )
    return {
        "phases": len(results),
        "exercised": sum(1 for r in results if r.status == EXERCISED),
        "not_exercised": sum(1 for r in results if r.status == NOT_EXERCISED),
        "unknown": sum(1 for r in results if r.status == UNKNOWN),
        "exercised_only_by_a_demonstrator": demonstrator_only,
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.phase:<4} {result.name:<14} {result.status:<14} {result.evidence}")
    print()
    print("summary:", summary())
    print()
    print("A relationship is not verified merely because both surfaces exist.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
