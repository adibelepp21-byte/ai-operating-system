"""
R2-C — three derived connective views over sources AIOS already holds
(`ACT-CC-R2BC-IMPL-001 §19`–`§29`).

`ACT-CC-R1-SYSTEMIC-001` classified the remaining connective gaps as *absent
views, not absent sources*. Decision lineage, the interface graph and system
self-knowledge were all answerable from information the repository already
carried — nobody had ever asked. This module asks.

**The rule that shapes every function here: a derived view is not a second
source of truth** (`§19`, `§25`, `§29`). Nothing below stores a fact. Every
answer is recomputed from its authoritative source on each call:

```text
Register / governance index   →  decision lineage
the import graph itself       →  interface graph
index + Ledger + Trace        →  self-knowledge projection
```

Delete this module and AIOS loses no truth — only the ability to see it
conveniently. That is the property that keeps it a projection.

**Evidence status is never collapsed.** `§28` requires `VERIFIED`, `INFERRED`
and `UNKNOWN` to stay distinguishable, and `§27` states plainly that returning
`UNKNOWN` is *correct* when evidence is absent. So this module answers with
`Fact` values that carry their own status, and it declines to guess. A question
the sources cannot answer comes back `UNKNOWN` rather than filled in.

Dependencies: the existing governance index and the Trace reader. No new
storage, no cache that could drift, no schema.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from tools.governance_index import (
    GovernanceIndex,
    REPO_ROOT,
    _SUBRECORD_RE,
    tracked_markdown,
)

#: Evidence status, kept distinct per `§28`. `VERIFIED` means a source states it
#: literally; `INFERRED` means it was derived structurally from a source but is
#: not stated; `UNKNOWN` means the sources do not support an answer.
VERIFIED = "VERIFIED"
INFERRED = "INFERRED"
UNKNOWN = "UNKNOWN"

REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"


@dataclass(frozen=True)
class Fact:
    """One projected answer, carrying its own evidence status and locator.

    `§28` forbids collapsing evidence status into an undifferentiated value, so
    the status travels with the answer rather than beside it. A caller that
    reads `.value` without reading `.status` is reading half the record, and the
    type makes that visible.
    """

    question: str
    value: Any
    status: str
    source: str = ""

    @property
    def is_known(self) -> bool:
        return self.status != UNKNOWN


# --------------------------------------------------------------------------
# View A — decision lineage (§20–§22)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class LineageEdge:
    """A gate identifier and the record that registered it.

    `ACT-CC-R1-003` established that AIOS registers Founder Decisions under two
    identifier systems — an `FD-n` *gate* and a `GDR-nnnn` *registration* — with
    nothing bridging them. That is why 41 referenced identifiers looked like 31
    unregistered ones. The bridge is derivable: a GDR heading names the gate it
    resolves.
    """

    gate: str
    registered_as: str
    heading: str
    source: str


def decision_lineage(root: Path = REPO_ROOT) -> List[LineageEdge]:
    """Derive `FD-n ↔ GDR-nnnn` from the Register's own headings.

    Reads only what a heading literally states. `§21` forbids reconstructing an
    identity relationship that is not provable, so a gate registered under a
    heading that does not name it produces no edge here — it stays unproven
    rather than being guessed at from subject matter.
    """
    register = root / REGISTER
    edges: List[LineageEdge] = []
    for number, line in enumerate(register.read_text(encoding="utf-8").splitlines(), 1):
        match = _SUBRECORD_RE.match(line)
        if match is None or not match.group("identifier").startswith("GDR-"):
            continue
        heading = line.lstrip("#").strip()
        for token in _fd_tokens(heading):
            edges.append(
                LineageEdge(
                    gate=token,
                    registered_as=match.group("identifier"),
                    heading=heading,
                    source=f"{REGISTER}:{number}",
                )
            )
    return edges


def _fd_tokens(text: str) -> List[str]:
    """`FD-…` identifiers literally present in a heading, in order."""
    import re

    return re.findall(r"\bFD-[A-Z0-9][A-Za-z0-9]*(?:[.-][A-Z0-9][A-Za-z0-9]*)*", text)


def unbridged_gates(root: Path = REPO_ROOT) -> List[str]:
    """Gate identifiers referenced in the corpus with no derivable registration.

    Reported as **unproven**, never as missing. `ACT-CC-R1-003` found that most
    of these are open decision gates that were never decided — an absent
    registration is the correct state for a question nobody has answered.
    """
    bridged = {edge.gate for edge in decision_lineage(root)}
    heading_registered = set()
    register = (root / REGISTER).read_text(encoding="utf-8")
    for line in register.splitlines():
        if line.startswith("### FD-"):
            heading_registered.add(line.split()[1])
    referenced = set()
    for path in tracked_markdown(root):
        referenced |= set(_fd_tokens(path.read_text(encoding="utf-8")))
    return sorted(referenced - bridged - heading_registered)


# --------------------------------------------------------------------------
# View B — interface graph (§23–§25)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class BoundaryEdge:
    """One cross-boundary dependency, derived from the import graph."""

    source: str
    target: str
    relationship: str = "imports"


def _boundaries(root: Path) -> List[str]:
    core = root / "native_core" / "core"
    return sorted(
        d.name for d in core.iterdir() if d.is_dir() and not d.name.startswith("__")
    )


def interface_graph(root: Path = REPO_ROOT) -> List[BoundaryEdge]:
    """Derive the cross-boundary dependency graph from source.

    `§25` requires the graph be regenerable from source rather than
    hand-maintained, and `§23` forbids creating a manual interface registry.
    This reads the actual imports, so the graph cannot describe an idealised
    architecture that the code does not have — it reports what is there.

    `§24` requires structural and semantic relationships stay distinct. This is
    the **structural** graph: it reports that one boundary imports another, and
    claims nothing about ownership or contract, which the imports do not state.
    """
    core = root / "native_core" / "core"
    names = _boundaries(root)

    def boundary_of(module: str) -> Optional[str]:
        for part in module.split("."):
            if part in names:
                return part
        return None

    edges = set()
    for boundary in names:
        for path in (core / boundary).rglob("*.py"):
            if "tests" in path.parts:
                continue
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                modules: Sequence[str] = ()
                if isinstance(node, ast.ImportFrom):
                    if node.level and node.level >= 2:
                        modules = (node.module or "",)
                    elif node.level == 0 and node.module:
                        modules = (node.module,)
                    else:
                        continue
                elif isinstance(node, ast.Import):
                    modules = tuple(alias.name for alias in node.names)
                for module in modules:
                    target = boundary_of(module)
                    if target and target != boundary:
                        edges.add((boundary, target))
    return [BoundaryEdge(source=s, target=t) for s, t in sorted(edges)]


def graph_is_acyclic(root: Path = REPO_ROOT) -> bool:
    """Whether the derived graph has no cycle — the invariant every Act since
    P1 has preserved, now answerable as a query rather than only as a test."""
    adjacency: Dict[str, set] = {}
    for edge in interface_graph(root):
        adjacency.setdefault(edge.source, set()).add(edge.target)
    seen, stack = set(), set()

    def visit(node: str) -> bool:
        if node in stack:
            return False
        if node in seen:
            return True
        seen.add(node)
        stack.add(node)
        ok = all(visit(child) for child in adjacency.get(node, ()))
        stack.discard(node)
        return ok

    return all(visit(node) for node in list(adjacency))


def boundary_consumers(root: Path = REPO_ROOT) -> Mapping[str, Tuple[str, ...]]:
    """Which boundaries depend on each boundary. A boundary with no consumer is
    reported as such and interpreted by nobody here — `capability`, `skill` and
    `optimization` are unconsumed *by canonical design*, which this view has no
    standing to relabel."""
    incoming: Dict[str, List[str]] = {name: [] for name in _boundaries(root)}
    for edge in interface_graph(root):
        incoming[edge.target].append(edge.source)
    return {name: tuple(sorted(sources)) for name, sources in incoming.items()}


# --------------------------------------------------------------------------
# View C — self-knowledge projection (§26–§29)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SelfKnowledge:
    """What AIOS can currently establish about itself, from its own sources.

    Not a Self-Model. `§26` forbids building one, and this is what `§20` of the
    native synthesis called for instead: a **projection** that consumes
    authoritative sources and owns none of them. Each answer is a `Fact`
    carrying its evidence status, so an absent answer is visibly absent.
    """

    facts: Tuple[Fact, ...] = field(default_factory=tuple)

    def answer(self, question: str) -> Fact:
        for fact in self.facts:
            if fact.question == question:
                return fact
        return Fact(question=question, value=None, status=UNKNOWN)

    @property
    def questions(self) -> Tuple[str, ...]:
        return tuple(fact.question for fact in self.facts)

    def unknowns(self) -> Tuple[Fact, ...]:
        return tuple(f for f in self.facts if not f.is_known)


def self_knowledge(
    root: Path = REPO_ROOT, trace_reader: "Optional[object]" = None
) -> SelfKnowledge:
    """Project what the system can currently establish about itself.

    `§27` lists the questions and states that a projection returning `UNKNOWN`
    is *correct* when evidence is absent. Two of them are answered `UNKNOWN`
    here on purpose, and the reason is architectural rather than incidental:

      - **what has run / failed** needs a `TraceReader`. R2-A made durable Trace
        evidence real, but a Trace store is per-`StorageFacility`; there is no
        cross-process registry of them, so this function answers only when a
        reader is handed in.
      - **what is running** has no source at all. Runtime state is per-process
        and nothing observes it from outside, which `ACT-CC-R1-SYSTEMIC-001`
        recorded and this Act does not change.
    """
    index, _ = GovernanceIndex.build(tracked_markdown(root), root)
    register_text = (root / REGISTER).read_text(encoding="utf-8")
    facts: List[Fact] = []

    identified = {r.identifier for r in index.records if r.identifier != "ABSENT"}
    facts.append(
        Fact(
            "what exists",
            {"records": len(index.records), "identified": len(identified)},
            VERIFIED,
            "governance index over tracked markdown",
        )
    )

    decisions = sorted(i for i in identified if i.startswith(("FD-", "GDR-")))
    facts.append(
        Fact("what decisions are recorded", decisions, VERIFIED, REGISTER)
    )

    boundaries = _boundaries(root)
    facts.append(
        Fact(
            "what is verified",
            {"boundaries": len(boundaries), "acyclic": graph_is_acyclic(root)},
            VERIFIED,
            "derived import graph",
        )
    )

    open_sync = [
        line.split("|")[1].strip()
        for line in register_text.splitlines()
        if line.startswith("| S-") and line.rstrip().endswith("| Open |")
    ]
    facts.append(
        Fact(
            "what is stale",
            {"open_synchronizations": open_sync},
            VERIFIED,
            f"{REGISTER} §4 External Corpus Synchronization Ledger",
        )
    )

    facts.append(
        Fact(
            "what is unbridged",
            unbridged_gates(root),
            INFERRED,
            "derived from Register headings; absence of a bridge is not absence "
            "of a decision",
        )
    )

    if trace_reader is None:
        facts.append(
            Fact(
                "what has run",
                None,
                UNKNOWN,
                "no TraceReader supplied; Trace stores are per-StorageFacility "
                "and no cross-process registry exists",
            )
        )
        facts.append(Fact("what has failed", None, UNKNOWN, "as above"))
    else:
        records = list(trace_reader.read())
        facts.append(
            Fact("what has run", len(records), VERIFIED, "TraceReader (R2-A evidence)")
        )
        facts.append(
            Fact(
                "what has failed",
                [r for r in records if r.status == "failure"],
                VERIFIED,
                "TraceReader (R2-A evidence)",
            )
        )

    facts.append(
        Fact(
            "what is running",
            None,
            UNKNOWN,
            "Runtime state is per-process and unobserved from outside; recorded "
            "by ACT-CC-R1-SYSTEMIC-001 and unchanged by this Act",
        )
    )
    return SelfKnowledge(facts=tuple(facts))
