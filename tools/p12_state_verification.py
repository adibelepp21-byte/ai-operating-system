"""P12-W6 — state verification (`§19` scope: `STATE`, specified by `§17`).

This scope item was classified `BLOCKED — DEPENDENCY (P12-W2)` in
`P12-W6-SCOPE-DISCOVERY-AND-CLASSIFICATION.md`: `§17` state authority cannot be
verified before a state authority surface exists. W2 built one, so the item is
verifiable — **and `ACT-CC-P12-W2-001 §48` says plainly that W2 must not be
assumed to close it.** W6 decides that, not W2.

`§17` fixes the chain every state class must satisfy:

```text
STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER
```

and requires a `STATE AUTHORITY CONFLICT` between two surfaces claiming the same
system-wide state to be discovered and resolved or escalated.

**The chain has four links and the fourth is the one that decides anything.**
`§16` of the Blueprint: *"P12 shall discover actual consumers rather than assume
them. Each claimed consumer requires evidence that it actually consumes the
state."* A projection nothing reads is a projection, not operational state — so
consumers are counted from the import graph, and a module's own conformance
suite is **not** counted as a consumer of it.

This module is W6 and stays diagnostic (`§22`: `W2 ≠ W6`). It builds nothing and
repairs nothing; it reads the W2 surface as data and reports what the four links
actually carry.
"""

from __future__ import annotations

import ast
import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

SATISFIED = "SATISFIED"
UNSATISFIED = "UNSATISFIED"
UNAVAILABLE = "UNAVAILABLE"

#: `§17`'s chain, in its order.
STATE_CHAIN: Tuple[str, ...] = (
    "STATE", "AUTHORITATIVE SOURCE", "PROJECTION", "CONSUMER",
)

#: The surface under verification, addressed by name rather than imported at
#: module scope: W6 reads W2, it does not depend on it.
SURFACE = "tools.p12_operational_state"


@dataclass(frozen=True)
class LinkResult:
    link: str
    status: str
    detail: str


def _surface():
    return importlib.import_module(SURFACE)


def consumers_of(module_name: str) -> Tuple[str, ...]:
    """Non-test modules that import `module_name`.

    A conformance suite is excluded deliberately. A test that imports a surface
    proves the surface can be imported, which is not the same as the system
    reading it — and counting tests as consumers is how a surface nothing uses
    comes to look integrated.
    """
    stem = module_name.rsplit(".", 1)[-1]
    found = []
    for path in sorted(REPO_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts or "tests" in path.parts:
            continue
        if path.name.startswith("test_") or path.stem == stem:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            elif isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            if any(stem in module for module in modules):
                found.append(path.relative_to(REPO_ROOT).as_posix())
                break
    return tuple(found)


def _link_state() -> LinkResult:
    """Is there a declared set of state classes at all?"""
    surface = _surface()
    declared = {s.state_class for s in surface.SOURCES}
    if not declared:
        return LinkResult("STATE", UNSATISFIED, "no state class is declared")
    return LinkResult(
        "STATE", SATISFIED,
        f"{len(surface.SOURCES)} declared source(s) across "
        f"{len(declared)} state class(es): {sorted(declared)}")


def _link_authoritative_source() -> LinkResult:
    """Does each state name an authoritative source that resolves?"""
    surface = _surface()
    missing = [s.state_id for s in surface.SOURCES
               if not (REPO_ROOT / s.read_path).exists()]
    unstated = [s.state_id for s in surface.SOURCES
                if not s.canonical_source.strip() or not s.authority.strip()]
    if missing or unstated:
        return LinkResult(
            "AUTHORITATIVE SOURCE", UNSATISFIED,
            f"{len(missing)} path(s) unresolved, {len(unstated)} without a "
            "named canonical source or authority")
    return LinkResult(
        "AUTHORITATIVE SOURCE", SATISFIED,
        f"all {len(surface.SOURCES)} sources name a canonical source and an "
        "authority, and every read path resolves")


def _link_projection() -> LinkResult:
    """Does a projection exist for each source, and carry provenance?"""
    surface = _surface()
    entries = surface.project()
    if len(entries) != len(surface.SOURCES):
        return LinkResult("PROJECTION", UNSATISFIED,
                          f"{len(entries)} projections for "
                          f"{len(surface.SOURCES)} sources")
    without = [e.state_id for e in entries
               if not (e.source and e.observed_at and e.transformation)]
    if without:
        return LinkResult("PROJECTION", UNSATISFIED,
                          f"{len(without)} projection(s) lack provenance")
    return LinkResult(
        "PROJECTION", SATISFIED,
        f"{len(entries)} projection(s), each carrying source, observation time "
        "and transformation")


def _link_consumer() -> LinkResult:
    """`§16` — a claimed consumer needs evidence that it consumes."""
    found = consumers_of(SURFACE)
    if not found:
        return LinkResult(
            "CONSUMER", UNSATISFIED,
            "no non-test module reads the projection; a projection nothing "
            "reads is a projection, not operational state")
    return LinkResult("CONSUMER", SATISFIED,
                      f"{len(found)} consumer(s): {list(found)}")


_LINKS = {
    "STATE": _link_state,
    "AUTHORITATIVE SOURCE": _link_authoritative_source,
    "PROJECTION": _link_projection,
    "CONSUMER": _link_consumer,
}


def verify() -> Tuple[LinkResult, ...]:
    results = []
    for link in STATE_CHAIN:
        try:
            results.append(_LINKS[link]())
        except Exception as exc:  # pragma: no cover - defensive
            results.append(LinkResult(link, UNAVAILABLE,
                                      f"link raised: {exc}"))
    return tuple(results)


def authority_conflicts() -> dict:
    """`§17` — discovered and reported, never resolved here."""
    surface = _surface()
    found = surface.conflicts()
    return {
        "conflicts": sum(1 for c in found if c["kind"] == "CONFLICT"),
        "undeclared": sum(1 for c in found if c["kind"] == "UNDECLARED"),
        "detail": ("a conflict is reported for escalation; resolving one means "
                   "choosing between two authorities"),
    }


def summary() -> dict:
    results = verify()
    conflicts = authority_conflicts()
    return {
        "links": len(results),
        "satisfied": sum(1 for r in results if r.status == SATISFIED),
        "unsatisfied": sum(1 for r in results if r.status == UNSATISFIED),
        "unavailable": sum(1 for r in results if r.status == UNAVAILABLE),
        "chain_complete": all(r.status == SATISFIED for r in results),
        "broken_links": tuple(r.link for r in results
                              if r.status != SATISFIED),
        "authority_conflicts": conflicts["conflicts"],
        "undeclared_claims": conflicts["undeclared"],
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.link:<22} {result.status:<13} {result.detail[:58]}")
    print()
    print("summary:", summary())
    print()
    print("W6 decides whether W2 closed this item. W2 does not.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
