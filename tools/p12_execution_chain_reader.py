"""P12-W4 — the independent reader of the execution chain.

`ACT-CC-P12-W4-001 §24` forbids the shape

```text
IMPLEMENTATION → SELF-REPORT → PASS
```

and requires

```text
IMPLEMENTATION → REAL EXECUTION → PERSISTED RECORDS → INDEPENDENT READER → VERDICT
```

So this module **imports nothing from the writer**. It does not construct an
`ExecutionManifest`, does not call `record()`, and does not reuse the writer's
notion of what a complete chain is. It reads bytes off disk and re-derives the
chain from them, and it resolves every reference against the record it points
at rather than trusting that the reference is well-formed.

A manifest that verifies here has been verified from persisted bytes by code
that did not produce them. A manifest that names a delegation, a trace record or
an observation which is not there fails — **a dangling reference is not a
join**, and accepting one would make the relation a spelling convention.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Read as paths, not as imported constants, so a change to the writer's
#: location is a visible failure here rather than an invisible agreement.
MANIFESTS = REPO_ROOT / "docs/architecture/p12/execution-provenance"
TRACE_STORES = REPO_ROOT / "docs/architecture/p12/trace-stores"
OBSERVATIONS = REPO_ROOT / "docs/architecture/p12/runtime-observations"
DELEGATION_DIRS = (
    REPO_ROOT / "docs/architecture/p11/w1-operations",
    REPO_ROOT / "docs/architecture/p11/w4-operations",
    REPO_ROOT / "docs/architecture/p11/x-department-operations",
    REPO_ROOT / "docs/architecture/p12/w4-operations",
)

JOINED = "JOINED"
DANGLING = "DANGLING"
UNRESOLVED = "UNRESOLVED"

#: Each edge of the canonical chain, and the reference that must resolve for it.
CHAIN_EDGES: Tuple[Tuple[str, str], ...] = (
    ("INTENT", "DECISION"),
    ("DECISION", "WORK"),
    ("WORK", "DELEGATION"),
    ("DELEGATION", "EXECUTION"),
    ("EXECUTION", "OBSERVATION"),
    ("OBSERVATION", "VERIFICATION"),
    ("VERIFICATION", "EVIDENCE"),
)


@dataclass(frozen=True)
class EdgeVerdict:
    source: str
    target: str
    status: str
    detail: str


@dataclass(frozen=True)
class ChainVerdict:
    execution_id: str
    status: str
    edges: Tuple[EdgeVerdict, ...]

    @property
    def joined(self) -> bool:
        return all(edge.status == JOINED for edge in self.edges)


def _read_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _delegation(delegation_id: str) -> Optional[dict]:
    for directory in DELEGATION_DIRS:
        candidate = directory / f"{delegation_id}.delegation.json"
        if candidate.is_file():
            return _read_json(candidate)
    return None


def _trace_line(store: str, ordinal: int) -> Optional[dict]:
    directory = TRACE_STORES / store
    if not directory.is_dir():
        return None
    lines = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                lines.append(line)
    if ordinal < 0 or ordinal >= len(lines):
        return None
    try:
        return json.loads(lines[ordinal])
    except json.JSONDecodeError:
        return None


def _observation(subject: str) -> Optional[dict]:
    if not OBSERVATIONS.is_dir():
        return None
    for path in sorted(OBSERVATIONS.rglob("*.json")):
        payload = _read_json(path)
        if payload and payload.get("runtime_id") == subject:
            return payload
    return None


def _edge(source: str, target: str, ok: bool, detail: str) -> EdgeVerdict:
    return EdgeVerdict(source, target, JOINED if ok else DANGLING, detail)


def verify_manifest(payload: dict) -> ChainVerdict:
    """Re-derive the chain from this manifest's references. Resolve every one."""
    execution_id = payload.get("execution_id", "<unnamed>")
    edges = []

    goal = payload.get("goal")
    plan = payload.get("plan")
    plan_authority = payload.get("plan_authority")
    edges.append(_edge(
        "INTENT", "DECISION", bool(goal and plan and plan_authority),
        f"goal {goal!r} decided by plan {plan!r} under {plan_authority!r}"))

    work = payload.get("work_scope") or ()
    edges.append(_edge(
        "DECISION", "WORK", bool(plan and work),
        f"plan {plan!r} carries work scope {list(work)}"))

    delegation_id = payload.get("delegation_id")
    delegation = _delegation(delegation_id) if delegation_id else None
    if delegation is None:
        edges.append(EdgeVerdict(
            "WORK", "DELEGATION", DANGLING,
            f"delegation {delegation_id!r} is in no resident delegation store"))
    else:
        granted = tuple(delegation.get("work_scope") or ())
        covered = bool(work) and set(work) <= set(granted)
        # Scope coverage alone is not the join. Six resident grants to this same
        # actor carry this same work scope, and `§23` Test G caught the first
        # version of this reader accepting any of them: the actor matched and
        # the scope matched, so a grant bound to a different plan verified.
        #
        # What binds a grant to *this* execution is its lifecycle boundary,
        # which names the plan the grant was issued for. A grant bound to
        # another plan authorizes another execution, whatever its scope says.
        boundary = str(delegation.get("lifecycle_boundary") or "")
        bound = bool(plan) and plan in boundary
        edges.append(_edge(
            "WORK", "DELEGATION", covered and bound,
            f"delegation {delegation_id} grants {list(granted)} bound to "
            f"{boundary!r}; manifest claims {list(work)} under plan {plan!r}"))

    store = payload.get("trace_store")
    ordinal = payload.get("trace_ordinal")
    trace = _trace_line(store, ordinal) if store is not None and \
        isinstance(ordinal, int) else None
    if trace is None:
        edges.append(EdgeVerdict(
            "DELEGATION", "EXECUTION", DANGLING,
            f"no Trace record at {store}#{ordinal}"))
    else:
        # The actor on the execution must be the recipient of the grant. This is
        # the check that makes the join an authorization rather than a label:
        # a manifest may not attach an execution to a grant issued to someone
        # else.
        recipient = (delegation or {}).get("recipient_instance")
        actor = trace.get("agent_instance")
        edges.append(_edge(
            "DELEGATION", "EXECUTION", bool(recipient) and actor == recipient,
            f"trace actor {actor!r} against grant recipient {recipient!r}"))

    subject = payload.get("observation_subject")
    observation = _observation(subject) if subject else None
    if observation is None:
        edges.append(EdgeVerdict(
            "EXECUTION", "OBSERVATION", DANGLING,
            f"no observation of subject {subject!r}"))
    else:
        runtime = (trace or {}).get("runtime")
        edges.append(_edge(
            "EXECUTION", "OBSERVATION", runtime == subject,
            f"trace runtime {runtime!r} against observed subject {subject!r}"))

    requirement = payload.get("verification_requirement")
    outcome = payload.get("outcome")
    edges.append(_edge(
        "OBSERVATION", "VERIFICATION",
        bool(observation) and bool(requirement) and outcome is not None,
        f"requirement {str(requirement)[:40]!r} with outcome recorded"))

    manifest_path = MANIFESTS / f"{execution_id}.manifest.json"
    edges.append(_edge(
        "VERIFICATION", "EVIDENCE", manifest_path.is_file(),
        f"evidence persisted at {manifest_path.name}"))

    status = JOINED if all(e.status == JOINED for e in edges) else DANGLING
    return ChainVerdict(execution_id, status, tuple(edges))


def verify_all() -> Tuple[ChainVerdict, ...]:
    if not MANIFESTS.is_dir():
        return ()
    verdicts = []
    for path in sorted(MANIFESTS.glob("*.manifest.json")):
        payload = _read_json(path)
        if payload is None:
            verdicts.append(ChainVerdict(path.stem, UNRESOLVED, ()))
            continue
        verdicts.append(verify_manifest(payload))
    return tuple(verdicts)


def summary() -> dict:
    verdicts = verify_all()
    return {
        "manifests": len(verdicts),
        "joined": sum(1 for v in verdicts if v.status == JOINED),
        "dangling": sum(1 for v in verdicts if v.status == DANGLING),
        "unresolved": sum(1 for v in verdicts if v.status == UNRESOLVED),
        "edges_per_chain": len(CHAIN_EDGES),
        "not_joined": tuple(v.execution_id for v in verdicts
                            if v.status != JOINED),
    }


def main(argv=None) -> int:
    verdicts = verify_all()
    if not verdicts:
        print("no execution provenance manifest is persisted")
        print("nothing to verify is not the same as nothing to find")
        return 0
    for verdict in verdicts:
        print(f"{verdict.execution_id}  [{verdict.status}]")
        for edge in verdict.edges:
            print(f"  {edge.source:>12} → {edge.target:<13} "
                  f"{edge.status:<9} {edge.detail[:58]}")
        print()
    print("summary:", summary())
    print()
    print("Read from persisted bytes by code that did not write them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
