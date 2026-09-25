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
from typing import Optional, Tuple

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


#: `§16 State Consumers` of the Roadmap PRD & Construction Blueprint enumerates
#: the kinds a consumer may be, verbatim and in its order. `ACT-CC-P12-008 §3`
#: required this to be read from the instrument body rather than inferred from
#: this module's own prior wording — and reading it settled a question two prior
#: Acts had recorded as open. `verification`, `self-model`, `observability` and
#: `evidence` are **named consumer kinds**. A verifier that reads the projection
#: is not disqualified for being a verifier.
CONSUMER_KINDS: Tuple[str, ...] = (
    "runtime", "workflow", "organization", "governance", "verification",
    "self-model", "observability", "evidence", "reconciliation",
)

#: The surface's projection API. `§16`'s closing sentence — *"Each claimed
#: consumer requires evidence that it actually consumes the state"* — is what
#: separates these from the rest of the module. Calling one of them reads the
#: system's state; constructing a `StateSource`, or patching `SOURCES`, uses the
#: module without consuming anything the system holds.
PROJECTION_READS: Tuple[str, ...] = ("project", "conflicts", "declares",
                                     "summary")


@dataclass(frozen=True)
class ConsumerEvidence:
    """One importer, and what `§16` evidence it carries."""

    module: str
    #: Projection entry points reached outside any substitution of the surface.
    reads: Tuple[str, ...]
    #: Projection entry points reached only over a substituted source set.
    fixture_reads: Tuple[str, ...]

    @property
    def consumes(self) -> bool:
        return bool(self.reads)


def _bound_names(tree: ast.AST, module_name: str) -> Tuple[set, set]:
    """Local names bound to `module_name`, and to members imported from it.

    Resolution is by **module identity**, never by substring. The superseded
    implementation asked ``stem in module``, which matched
    ``tools.p12_operational_state_verifier`` for a target of
    ``tools.p12_operational_state`` — so a module importing only the verifier
    counted as a consumer of the surface. That false positive and the
    false negative below were the same mistake spelled two ways: a name is not
    a prefix match.
    """
    stem = module_name.rsplit(".", 1)[-1]
    modules, members = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if not node.module:
                continue
            if node.module == module_name or node.module == stem:
                # ``from tools.p12_operational_state import project``
                members.update(alias.asname or alias.name
                               for alias in node.names)
                continue
            for alias in node.names:
                # ``from tools import p12_operational_state [as state]`` —
                # the one the superseded implementation could not see, because
                # `node.module` is ``tools`` and the surface's name is in
                # `alias.name`.
                if f"{node.module}.{alias.name}" == module_name \
                        or alias.name == stem:
                    modules.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name != module_name and alias.name != stem:
                    continue
                if alias.asname:
                    modules.add(alias.asname)          # ``import x.y as z``
                else:
                    # ``import tools.p12_operational_state`` binds the root
                    # package; the surface is reached by attribute access.
                    modules.add(alias.name.split(".", 1)[0])
    return modules, members


def _substituted_blocks(tree: ast.AST, aliases: set) -> Tuple[Tuple[int, int], ...]:
    """Line ranges of `with` blocks that substitute the surface.

    `ACT-CC-P12-008 §11`: ``TEST ≠ REAL SYSTEM WORK``. A module that replaces
    the surface's sources and then calls its projection is reading its own
    fixture. That is a legitimate thing for a negative control to do, and it is
    not evidence that the module consumes the system's state — so reads inside
    such a block are recorded separately rather than dropped or counted.
    """
    ranges = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.With, ast.AsyncWith)):
            continue
        for item in node.items:
            call = item.context_expr
            if not isinstance(call, ast.Call):
                continue
            target = call.args[0] if call.args else None
            if isinstance(target, ast.Name) and target.id in aliases:
                ranges.append((node.lineno, getattr(node, "end_lineno",
                                                    node.lineno)))
                break
    return tuple(ranges)


def _evidence_in(tree: ast.AST, module_name: str) -> Optional[ConsumerEvidence]:
    aliases, members = _bound_names(tree, module_name)
    if not aliases and not members:
        return None
    substituted = _substituted_blocks(tree, aliases)

    def inside_fixture(node) -> bool:
        return any(start <= node.lineno <= end for start, end in substituted)

    reads, fixture_reads = set(), set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = None
        if isinstance(node.func, ast.Attribute) and node.func.attr in PROJECTION_READS:
            base = node.func.value
            # ``state.project()`` and ``tools.p12_operational_state.project()``
            if isinstance(base, ast.Name) and base.id in aliases:
                name = node.func.attr
            elif isinstance(base, ast.Attribute) and base.attr == \
                    module_name.rsplit(".", 1)[-1]:
                name = node.func.attr
        elif isinstance(node.func, ast.Name) and node.func.id in members \
                and node.func.id in PROJECTION_READS:
            name = node.func.id
        if name is None:
            continue
        (fixture_reads if inside_fixture(node) else reads).add(name)
    return ConsumerEvidence("", tuple(sorted(reads)), tuple(sorted(fixture_reads)))


def consumption_evidence(module_name: str) -> Tuple[ConsumerEvidence, ...]:
    """`§16` evidence for every non-test module that imports `module_name`.

    Returns every importer, carrying what it was found to do with the surface —
    so a caller can see both the import relation and the consumption relation
    rather than being handed a single number that conflates them.
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
        evidence = _evidence_in(tree, module_name)
        if evidence is None:
            continue
        found.append(ConsumerEvidence(
            path.relative_to(REPO_ROOT).as_posix(),
            evidence.reads, evidence.fixture_reads))
    return tuple(found)


def importers_of(module_name: str) -> Tuple[str, ...]:
    """Non-test modules that import `module_name`. **Importers, not consumers.**

    Kept separate and named for what it is. `ACT-CC-P12-008 §18`:
    ``AST MATCH ≠ SEMANTIC CONSUMER``. This answers *"who binds this name"*,
    which is a real question and not the one `§16` asks.
    """
    return tuple(e.module for e in consumption_evidence(module_name))


def consumers_of(module_name: str) -> Tuple[str, ...]:
    """Non-test modules for which `§16` evidence of actual consumption exists.

    A conformance suite is excluded deliberately. A test that imports a surface
    proves the surface can be imported, which is not the same as the system
    reading it — and counting tests as consumers is how a surface nothing uses
    comes to look integrated. `§16` does not list `test` among the kinds a
    consumer may be; it does list `verification`, and the two are not the same
    thing.

    **`ACT-CC-P12-008` corrected two defects here.** The superseded
    implementation collected, for an `ast.ImportFrom`, only `[node.module]` and
    then asked ``stem in module``. That was blind to
    ``from tools import p12_operational_state as state`` — the form every
    resident importer actually uses, where `node.module` is ``tools`` — and, in
    the same expression, counted ``tools.p12_operational_state_verifier`` as the
    surface because one name is a prefix of the other. It reported zero
    consumers for a surface that has real ones, and would have reported a
    consumer that does not exist.

    **Import alone is no longer sufficient**, because `§16` says it is not:
    *"Each claimed consumer requires evidence that it actually consumes the
    state."* Correcting only the import shape would have moved this link to
    SATISFIED on three matches, one of which never reads the system's state at
    all. `importers_of()` answers the narrower question separately.
    """
    return tuple(e.module for e in consumption_evidence(module_name)
                 if e.consumes)


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
    """`§16` — a claimed consumer needs evidence that it consumes.

    The detail reports importers and evidenced consumers separately, because
    the two numbers were conflated for as long as this link was measured by
    import alone, and a reader handed only the second cannot tell whether the
    first is larger.
    """
    evidence = consumption_evidence(SURFACE)
    consuming = [e for e in evidence if e.consumes]
    if not consuming:
        importing = [e.module for e in evidence]
        return LinkResult(
            "CONSUMER", UNSATISFIED,
            "no non-test module reads the projection; a projection nothing "
            "reads is a projection, not operational state"
            + (f" — {len(importing)} module(s) import it without reading it: "
               f"{importing}" if importing else ""))
    detail = ", ".join(f"{e.module} reads {list(e.reads)}" for e in consuming)
    unread = [e.module for e in evidence if not e.consumes]
    return LinkResult(
        "CONSUMER", SATISFIED,
        f"{len(consuming)} evidenced consumer(s) of {len(evidence)} "
        f"importer(s): {detail}"
        + (f"; not counted: {unread} (reads the projection only over a "
           "substituted source set)" if unread else ""))


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
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
