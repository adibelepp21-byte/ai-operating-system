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

#: The same chain's **live** roots (`FD-FR2-001`; `GOAL-V2-002` W-1). P12 is
#: certified, so a new execution's trace, manifest and observation can only be
#: written outside it. These are read as their own population, origin `live`,
#: and never merged into the certified one: `verify_all()` and `summary()` still
#: answer for P12's certified evidence alone, exactly as certified, and a live
#: manifest is resolved only against live records. A certified chain therefore
#: cannot be completed by a live record, nor a live chain by a certified one.
LIVE_MANIFESTS = REPO_ROOT / "docs/operations/execution-provenance"
LIVE_TRACE_STORES = REPO_ROOT / "docs/operations/trace-stores"
LIVE_OBSERVATIONS = REPO_ROOT / "docs/operations/runtime-observations"
#: Where the Agency's grants live. Read as a path and **discovered** beneath it
#: by shape (a directory holding a grant record), as the operational readers
#: find their roots, so a grant in a new Agency root is found by existing
#: rather than by someone remembering to list it.
AGENCY_OPERATIONS = REPO_ROOT / "docs/architecture/agency/operations"

CERTIFIED = "certified-p12"
LIVE = "live"

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
    #: Which population the manifest was read from. Certified unless read live.
    origin: str = CERTIFIED

    @property
    def joined(self) -> bool:
        return all(edge.status == JOINED for edge in self.edges)


def _read_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


@dataclass(frozen=True)
class _Roots:
    manifests: Path
    trace_stores: Path
    observations: Path
    delegation_dirs: Tuple[Path, ...]


def _agency_delegation_dirs() -> Tuple[Path, ...]:
    if not AGENCY_OPERATIONS.is_dir():
        return ()
    return tuple(sorted({path.parent for path in
                         AGENCY_OPERATIONS.rglob("*.delegation.json")}))


def _roots(origin: str) -> _Roots:
    """The roots one population is resolved against. Read at call time."""
    if origin == CERTIFIED:
        return _Roots(MANIFESTS, TRACE_STORES, OBSERVATIONS, DELEGATION_DIRS)
    if origin == LIVE:
        return _Roots(LIVE_MANIFESTS, LIVE_TRACE_STORES, LIVE_OBSERVATIONS,
                      _agency_delegation_dirs())
    raise ValueError(f"unknown origin {origin!r}")


def _delegation(delegation_id: str,
                dirs: Optional[Tuple[Path, ...]] = None) -> Optional[dict]:
    for directory in (DELEGATION_DIRS if dirs is None else dirs):
        candidate = directory / f"{delegation_id}.delegation.json"
        if candidate.is_file():
            return _read_json(candidate)
    return None


def _trace_line(store: str, ordinal: int,
                root: Optional[Path] = None) -> Optional[dict]:
    directory = (TRACE_STORES if root is None else root) / store
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


def _observation(subject: str, root: Optional[Path] = None) -> Optional[dict]:
    root = OBSERVATIONS if root is None else root
    if not root.is_dir():
        return None
    for path in sorted(root.rglob("*.json")):
        payload = _read_json(path)
        if payload and payload.get("runtime_id") == subject:
            return payload
    return None


def _edge(source: str, target: str, ok: bool, detail: str) -> EdgeVerdict:
    return EdgeVerdict(source, target, JOINED if ok else DANGLING, detail)


def verify_manifest(payload: dict, origin: str = CERTIFIED) -> ChainVerdict:
    """Re-derive the chain from this manifest's references. Resolve every one.

    ``origin`` names the population the manifest belongs to, and every reference
    is resolved against that population's roots only (`FD-FR2-001 §5`).
    """
    roots = _roots(origin)
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
    delegation = (_delegation(delegation_id, roots.delegation_dirs)
                  if delegation_id else None)
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
    trace = _trace_line(store, ordinal, roots.trace_stores) \
        if store is not None and isinstance(ordinal, int) else None
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
    observation = _observation(subject, roots.observations) if subject \
        else None
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

    manifest_path = roots.manifests / f"{execution_id}.manifest.json"
    edges.append(_edge(
        "VERIFICATION", "EVIDENCE", manifest_path.is_file(),
        f"evidence persisted at {manifest_path.name}"))

    status = JOINED if all(e.status == JOINED for e in edges) else DANGLING
    return ChainVerdict(execution_id, status, tuple(edges), origin)


def _verify_root(directory: Path, origin: str) -> Tuple[ChainVerdict, ...]:
    if not directory.is_dir():
        return ()
    verdicts = []
    for path in sorted(directory.glob("*.manifest.json")):
        payload = _read_json(path)
        if payload is None:
            verdicts.append(ChainVerdict(path.stem, UNRESOLVED, (), origin))
            continue
        verdicts.append(verify_manifest(payload, origin))
    return tuple(verdicts)


def verify_all() -> Tuple[ChainVerdict, ...]:
    """P12's certified population, as certified. Live manifests are not in it."""
    return _verify_root(MANIFESTS, CERTIFIED)


def verify_live() -> Tuple[ChainVerdict, ...]:
    """The live population (`FD-FR2-001`): manifests of executions run since
    P12 was certified, resolved against live records only."""
    return _verify_root(LIVE_MANIFESTS, LIVE)


def _summarize(verdicts: Tuple[ChainVerdict, ...]) -> dict:
    return {
        "manifests": len(verdicts),
        "joined": sum(1 for v in verdicts if v.status == JOINED),
        "dangling": sum(1 for v in verdicts if v.status == DANGLING),
        "unresolved": sum(1 for v in verdicts if v.status == UNRESOLVED),
        "edges_per_chain": len(CHAIN_EDGES),
        "not_joined": tuple(v.execution_id for v in verdicts
                            if v.status != JOINED),
    }


def summary() -> dict:
    return _summarize(verify_all())


def live_summary() -> dict:
    return dict(_summarize(verify_live()), origin=LIVE)


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
    for verdict in verify_live():
        print(f"{verdict.execution_id}  [{verdict.status}] (live)")
        for edge in verdict.edges:
            print(f"  {edge.source:>12} → {edge.target:<13} "
                  f"{edge.status:<9} {edge.detail[:58]}")
        print()
    print("live summary:", live_summary())
    print()
    print("Read from persisted bytes by code that did not write them.")
    return 0


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
