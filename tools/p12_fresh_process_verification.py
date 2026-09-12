"""P12-W6 — fresh-process verification (`§52`, `§19` scope item `FRESH PROCESS`).

`§52`: *"Material P12 claims must survive fresh-process reconstruction where
applicable"*, across `repository → canonical sources → registries → state →
decisions → integration graph → runtime → evidence`, and — the clause that gives
the check its point — ***"without relying on hidden conversational state."***

**Why this is not ceremony.** Every P12 claim in this corpus was produced inside
one very long session. A figure computed there can be right for reasons that do
not survive the session: a module imported earlier, a file written mid-run, a
value cached in a live object. The only way to tell a reproducible claim from a
session-dependent one is to recompute it **in an interpreter that never saw the
session** and compare.

So each stage is derived twice — once in this process, once in a subprocess that
imports nothing from here and receives no state — and the two are compared. A
stage that agrees is reproducible from the repository alone. A stage that
disagrees is a claim that depended on something the repository does not carry,
which is exactly what `§52` is looking for.

**It asserts no threshold.** Whether the reproduced values are *sufficient* for
`E12-06` is a measurable interpretation that only Founder ratification can
supply (`§53`, `F-16`). This reports reproducibility, not adequacy.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

REPRODUCED = "REPRODUCED"
DIVERGED = "DIVERGED"
UNAVAILABLE = "UNAVAILABLE"

#: `§52`'s eight stages, in its order, each with the expression that derives it
#: from the repository. The expressions are deliberately small and total: a
#: stage that needs setup would be testing the setup, not the repository.
STAGES: Tuple[Tuple[str, str], ...] = (
    ("repository", "len(__import__('tools.derived_views', fromlist=['x']).tracked_markdown(R))"),
    ("canonical sources",
     "__import__('hashlib').sha256((R / 'docs/program/AIOS_PHASE_10_13_PLATFORM_ORGANIZATION_BLUEPRINT_v1.0.md').read_bytes()).hexdigest()[:16]"),
    ("registries",
     "len(__import__('tools.governance_index', fromlist=['x']).GovernanceIndex.build("
     "__import__('tools.derived_views', fromlist=['x']).tracked_markdown(R), R)[0].records)"),
    ("state", "__import__('tools.p12_self_model', fromlist=['x']).coverage()"),
    ("decisions",
     "len([f for f in __import__('tools.p12_self_model', fromlist=['x']).decisions().value['identifiers']])"),
    ("integration graph",
     "(len(__import__('tools.derived_views', fromlist=['x']).interface_graph(R)), "
     "__import__('tools.derived_views', fromlist=['x']).graph_is_acyclic(R))"),
    ("runtime",
     "__import__('tools.p12_runtime_observation', fromlist=['x']).what_is_running()['observations']"),
    ("evidence",
     "__import__('tools.p12_trace_registry', fromlist=['x']).what_has_run()['records']"),
)

_CHILD = (
    "import json,sys;"
    "sys.path.insert(0, {root!r});"
    "from pathlib import Path;"
    "R = Path({root!r});"
    "print(json.dumps(repr({expr}), default=str))"
)


@dataclass(frozen=True)
class StageResult:
    stage: str
    in_process: str
    fresh_process: str
    status: str


def _here(expr: str) -> str:
    R = REPO_ROOT  # noqa: F841 — referenced by the expression
    return repr(eval(expr))  # noqa: S307 — expressions are module constants


def _there(expr: str) -> str:
    result = subprocess.run(
        [sys.executable, "-c",
         _CHILD.format(root=str(REPO_ROOT), expr=expr)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return f"<child failed: {result.stderr.strip().splitlines()[-1:]}>"
    return json.loads(result.stdout)


def verify() -> Tuple[StageResult, ...]:
    """Derive each stage twice and compare."""
    results = []
    for stage, expr in STAGES:
        try:
            here = _here(expr)
        except Exception as exc:  # pragma: no cover - defensive
            here = f"<in-process failed: {exc}>"
        there = _there(expr)
        if here.startswith("<") or there.startswith("<"):
            status = UNAVAILABLE
        elif here == there:
            status = REPRODUCED
        else:
            status = DIVERGED
        results.append(StageResult(stage, here, there, status))
    return tuple(results)


def summary() -> dict:
    results = verify()
    return {
        "stages": len(results),
        "reproduced": sum(1 for r in results if r.status == REPRODUCED),
        "diverged": sum(1 for r in results if r.status == DIVERGED),
        "unavailable": sum(1 for r in results if r.status == UNAVAILABLE),
        "diverged_stages": tuple(r.stage for r in results if r.status == DIVERGED),
    }


def main(argv=None) -> int:
    for result in verify():
        value = result.in_process if len(result.in_process) < 60 else \
            result.in_process[:57] + "..."
        print(f"{result.stage:<20} {result.status:<12} {value}")
        if result.status == DIVERGED:
            print(f"{'':<20} fresh: {result.fresh_process[:70]}")
    print()
    print("summary:", summary())
    print()
    print("Reproducibility is not adequacy: whether these values satisfy E12-06")
    print("is a measurable interpretation only Founder ratification supplies.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
