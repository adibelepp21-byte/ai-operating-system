"""`E12-01`…`E12-05` measured against the boundaries decided under `ACT-CC-P12-019`.

**The direction of authority is the one `p12_e12_acceptance` keeps for
`E12-06`:**

```text
DECISION  →  ACCEPTANCE BOUNDARY  →  MEASUREMENT
```

`p12_e12_acceptance` reads `FD-P12-001` and raises if the ratified reading is
not `R1`. This module reads `P12-019-DELEGATED-DECISIONS.md` and raises if a
criterion's decision is absent or is not a `RATIFY`. Delete the record and
nothing here measures anything. `ACT-CC-P12-020 §7`: *"The measurement module
SHALL NOT supply, infer, invent, or silently substitute an acceptance
boundary."*

**These boundaries were decided by this office under an explicit, temporary,
Founder-issued delegation** (`ACT-CC-P12-019 §3`, `§7`, `§25`), not ratified by
the Founder in person. Every result carries `DECISION MADE UNDER
ACT-CC-P12-019`, as `§15` requires, so it can never be mistaken for a Founder
ratification.

**Four boundaries are stricter than the existing proposals; one is the proposal
unchanged.** `§8` forbids automatically choosing the proposal and equally
forbids modifying a boundary to obtain `PASS`. The modifications add clauses the
*requirement bodies* name and the proposals omit — `CAPABILITY` in Founder
Authorization `§14`, staleness in `§15`, the six-link chain in `§16`,
`SELF-MODEL ≠ AUTHORITY` in `§18`. Each added clause can fail.

**Measured, not asserted.** Every clause reads a resident verifier built before
these boundaries existed and falsifiable on its own terms. Nothing here
re-derives a measurement it could read, and nothing returns a verdict the
underlying evidence does not carry.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The delegated decision record. Read on every call; absence is fatal.
DECISION_RECORD = Path("docs/architecture/p12/P12-019-DELEGATED-DECISIONS.md")

#: The delegating instrument, so a reader finds the authority without
#: conversation memory — the corpus's own decision-recording rule.
DELEGATION_INSTRUMENT = "ACT-CC-P12-019"

CRITERIA: Tuple[str, ...] = ("E12-01", "E12-02", "E12-03", "E12-04", "E12-05")

SATISFIED = "SATISFIED"
NOT_SATISFIED = "NOT SATISFIED"
UNKNOWN = "UNKNOWN"

_DECISION_BLOCK = re.compile(
    r"^##\s+`(E12-0\d)`\s*$(.*?)(?=^##\s|\Z)", re.M | re.S)
_DECISION_FIELD = re.compile(
    r"^\|\s*\*\*Decision\*\*\s*\|\s*(.+?)\s*\|\s*$", re.M)
_CLAUSE = re.compile(r"^-\s+\*\*\((?P<letter>[a-z])\)\*\*\s", re.M)


class AcceptanceBoundaryUnavailable(Exception):
    """No decided boundary could be read for a criterion. Fail closed."""


@dataclass(frozen=True)
class ClauseResult:
    letter: str
    satisfied: bool
    observation: str


@dataclass(frozen=True)
class CriterionResult:
    criterion: str
    decision: str
    verdict: str
    clauses: Tuple[ClauseResult, ...]
    evidence: str

    @property
    def satisfied(self) -> bool:
        return self.verdict == SATISFIED


def decided_boundaries(root: Path = REPO_ROOT) -> Dict[str, dict]:
    """Each criterion's decision and clause letters, read from the record."""
    path = root / DECISION_RECORD
    if not path.is_file():
        raise AcceptanceBoundaryUnavailable(
            f"the delegated decision record does not resolve: {DECISION_RECORD}")
    text = path.read_text(encoding="utf-8")
    if DELEGATION_INSTRUMENT not in text:
        raise AcceptanceBoundaryUnavailable(
            f"{DECISION_RECORD} does not cite {DELEGATION_INSTRUMENT}; a "
            "decision without its delegating instrument has no authority")
    found: Dict[str, dict] = {}
    for block in _DECISION_BLOCK.finditer(text):
        criterion, body = block.group(1), block.group(2)
        decision = _DECISION_FIELD.search(body)
        if decision is None:
            continue
        found[criterion] = {
            "decision": decision.group(1).strip().strip("*").strip(),
            "clauses": tuple(m.group("letter") for m in _CLAUSE.finditer(body)),
        }
    missing = [c for c in CRITERIA if c not in found]
    if missing:
        raise AcceptanceBoundaryUnavailable(
            f"{DECISION_RECORD} records no decision for {missing}")
    return found


# ---------------------------------------------------------------------------
# THE CLAUSES — each reads a resident verifier
# ---------------------------------------------------------------------------

#: The eight layers Founder Authorization `§14` names, in its order.
LAYERS_14: Tuple[str, ...] = (
    "PHASE", "CAPABILITY", "PLATFORM", "ORGANIZATION", "RUNTIME", "WORKFLOW",
    "EVIDENCE", "VERIFICATION")

_EDGE_ATTRIBUTES = ("source", "target", "relationship", "owner", "authority",
                    "contract", "state", "evidence", "verification",
                    "lifecycle")


def _e12_01(root: Path = REPO_ROOT) -> Tuple[ClauseResult, ...]:
    from tools import p12_integration_graph as graph
    from tools import p12_phase_verification_matrix as matrix

    edges = graph.graph()
    vocabulary = {graph.VERIFIED, graph.UNVERIFIED, graph.BLOCKED,
                  graph.INVALID, graph.STALE, graph.RESERVED,
                  graph.NOT_APPLICABLE}
    incomplete = [e.integration_class for e in edges
                  if any(not str(getattr(e, a, "")).strip()
                         for a in _EDGE_ATTRIBUTES)]
    unclassified = [e.integration_class for e in edges
                    if e.classification not in vocabulary]
    a_ok = bool(edges) and not incomplete and not unclassified

    rows = matrix.rows(root)
    # A layer is covered when its name appears as a **word** in a matrix
    # attribute or an integration-edge endpoint.
    #
    # The first version intersected uppercased endpoint names with the layer
    # set by equality, and reported `PLATFORM` uncovered: the edge endpoint is
    # `Platform Organization`, which is the fuller name `§14` itself uses in
    # *"Phase dan Platform Organization harus tetap dibedakan"*. The corpus was
    # consistent and the matcher was wrong — the same identity-matching blind
    # spot `consumers_of` had, in the opposite direction.
    surfaces = ([a for a in matrix.ATTRIBUTES] if rows else []) \
        + [e.source for e in edges] + [e.target for e in edges]
    words = {w for surface in surfaces
             for w in re.split(r"[^A-Za-z0-9]+", surface.upper()) if w}
    covered = {layer for layer in LAYERS_14 if layer in words}
    uncovered = [l for l in LAYERS_14 if l not in covered]
    bare_unknown = [f"{row.phase}/{attribute}"
                    for row in rows
                    for attribute, value in zip(matrix.ATTRIBUTES, row.as_row())
                    if value.startswith(matrix.UNKNOWN) and "—" not in value]
    b_ok = bool(rows) and not uncovered and not bare_unknown

    asserted = [e.integration_class for e in edges
                if e.owner and "UNRESOLVED" not in e.owner.upper()
                and "F-17" not in e.owner]
    c_ok = not asserted

    return (
        ClauseResult("a", a_ok,
                     f"{len(edges)} edge(s); {len(incomplete)} missing an "
                     f"attribute; {len(unclassified)} unclassified"),
        ClauseResult("b", b_ok,
                     f"{len(LAYERS_14) - len(uncovered)}/{len(LAYERS_14)} §14 "
                     f"layers covered (uncovered: {uncovered}); "
                     f"{len(bare_unknown)} bare UNKNOWN cell(s)"),
        ClauseResult("c", c_ok,
                     f"{len(asserted)} edge(s) assert a provider relation no "
                     "resident source establishes"),
    )


def _e12_02(root: Path = REPO_ROOT) -> Tuple[ClauseResult, ...]:
    from tools import p12_operational_state as state
    from tools import p12_state_verification as chain

    links = chain.summary()
    a_ok = (links["links"] > 0 and links["chain_complete"]
            and not links["broken_links"])

    projected = state.summary()
    b_ok = (projected["conflicts"] == 0
            and projected["undeclared_claims"] == 0)

    classified = projected["current"] + projected["stale"] + projected["unknown"]
    c_ok = projected["sources"] > 0 and classified == projected["projected"]

    return (
        ClauseResult("a", a_ok,
                     f"{links['satisfied']}/{links['links']} links satisfied; "
                     f"chain_complete={links['chain_complete']}"),
        ClauseResult("b", b_ok,
                     f"{projected['conflicts']} conflict(s), "
                     f"{projected['undeclared_claims']} undeclared claim(s)"),
        ClauseResult("c", c_ok,
                     f"{classified}/{projected['projected']} projected state(s) "
                     f"classified (current {projected['current']} · stale "
                     f"{projected['stale']} · unknown {projected['unknown']})"),
    )


def _e12_03(root: Path = REPO_ROOT) -> Tuple[ClauseResult, ...]:
    from tools import governance_index as index
    from tools import p12_governance_join_reader as joins
    from tools import p12_system_negative_controls as controls

    built, _ = index.GovernanceIndex.build(index.tracked_markdown(root), root)
    stale = built.stale_sources(root)
    a_ok = bool(built.records) and not stale

    found = {c.control: c for c in controls.verify()}
    enforcing = [name for name in ("unauthorized state mutation",
                                   "unauthorized architecture mutation")
                 if name in found and found[name].status == controls.REFUSED]
    b_ok = bool(enforcing)

    joined = 0
    for directory in ("w3-operations", "w4-operations"):
        operations = root / "docs/architecture/p12" / directory
        if not operations.is_dir():
            continue
        for resolved in joins.resolve_all(operations, operations):
            if resolved.get("status") == "JOINED":
                joined += 1
    c_ok = joined > 0

    return (
        ClauseResult("a", a_ok,
                     f"{len(built.records)} record(s) from "
                     f"{len(built.sources)} source(s); {len(stale)} stale"),
        ClauseResult("b", b_ok,
                     f"enforcement demonstrated by {enforcing}" if b_ok
                     else "no control demonstrates enforcement"),
        ClauseResult("c", c_ok,
                     f"{joined} governance join(s) resolve their grant by "
                     "structural reference rather than parsed prose"),
    )


def _e12_04(root: Path = REPO_ROOT) -> Tuple[ClauseResult, ...]:
    from tools import p12_cross_phase_verification as cross
    from tools import p12_execution_chain_reader as chain

    found = chain.summary()
    a_ok = (found["manifests"] > 0 and found["joined"] == found["manifests"]
            and found["dangling"] == 0 and found["unresolved"] == 0)

    from tools import p12_execution_provenance as provenance
    # `manifests()`, not a guessed `recorded()`. The first version guarded the
    # wrong name with `hasattr` and fell back to an empty tuple, which made the
    # clause report the *system* failing when the *instrument* could not read.
    # `UNKNOWN ≠ FALSE`: a missing accessor now raises and is reported UNKNOWN.
    manifests = provenance.manifests()
    elided = [m for m in manifests if not m.get("work_scope")]
    b_ok = bool(manifests) and not elided

    demonstrator_only = cross.summary()["exercised_only_by_a_demonstrator"]
    c_ok = not demonstrator_only

    return (
        ClauseResult("a", a_ok,
                     f"{found['joined']}/{found['manifests']} chain(s) joined, "
                     f"{found['dangling']} dangling, "
                     f"{found['edges_per_chain']} edges per chain"),
        ClauseResult("b", b_ok,
                     f"{len(manifests)} manifest(s); {len(elided)} elide WORK"),
        ClauseResult("c", c_ok,
                     f"demonstrator-only phases: {list(demonstrator_only)}"),
    )


def _e12_05(root: Path = REPO_ROOT) -> Tuple[ClauseResult, ...]:
    from tools import p12_self_model as model
    from tools import p12_self_model_contract as contract

    coverage = model.coverage()
    answered = coverage["verified"] + coverage["inferred"] + coverage["unknown"]
    a_ok = coverage["questions"] == 12 and answered == 12

    # `unbound_answers` / `contracted` / `missing` are the keys the contract
    # actually publishes. The first version read `unbound` with a default of
    # `1`, so an absent key manufactured a failure rather than an UNKNOWN.
    bound = contract.summary()
    for required in ("contracted", "canonical_questions", "unbound_answers",
                     "missing"):
        if required not in bound:
            raise KeyError(f"the self-model contract publishes no {required!r}")
    b_ok = (bound["contracted"] == bound["canonical_questions"]
            and not bound["unbound_answers"] and not bound["missing"])

    source = (root / "tools" / "p12_self_model.py").read_text(encoding="utf-8")
    granting = [n.name for n in ast.walk(ast.parse(source))
                if isinstance(n, ast.FunctionDef)
                and n.name.lower().lstrip("_").startswith(
                    ("authorize", "authorise", "permit", "grant", "allow",
                     "certify", "approve", "ratify"))]
    c_ok = not granting

    return (
        ClauseResult("a", a_ok,
                     f"{coverage['questions']} question(s): "
                     f"{coverage['verified']} verified · "
                     f"{coverage['inferred']} inferred · "
                     f"{coverage['unknown']} unknown"),
        ClauseResult("b", b_ok,
                     f"{bound['contracted']}/{bound['canonical_questions']} "
                     f"contracted; {len(bound['unbound_answers'])} unbound; "
                     f"{len(bound['missing'])} missing"),
        ClauseResult("c", c_ok,
                     f"{len(granting)} self-model function(s) grant a permission"),
    )


_CLAUSES: Dict[str, Callable] = {
    "E12-01": _e12_01, "E12-02": _e12_02, "E12-03": _e12_03,
    "E12-04": _e12_04, "E12-05": _e12_05,
}


def measure(root: Path = REPO_ROOT) -> Tuple[CriterionResult, ...]:
    """Measure each criterion against its decided boundary. Raises if absent."""
    decided = decided_boundaries(root)
    results = []
    for criterion in CRITERIA:
        record = decided[criterion]
        if not record["decision"].upper().startswith("RATIFY"):
            raise AcceptanceBoundaryUnavailable(
                f"{criterion} is recorded as {record['decision']!r}; only a "
                "RATIFY decision establishes a boundary to measure against")
        try:
            clauses = _CLAUSES[criterion](root)
        except Exception as exc:  # evidence unreadable — say so, never pass
            results.append(CriterionResult(
                criterion, record["decision"], UNKNOWN, (),
                f"evidence unreadable: {type(exc).__name__}: {exc}"))
            continue
        declared = record["clauses"]
        if declared and len(declared) != len(clauses):
            results.append(CriterionResult(
                criterion, record["decision"], UNKNOWN, clauses,
                f"the record declares {len(declared)} clause(s); this module "
                f"measures {len(clauses)}"))
            continue
        verdict = SATISFIED if all(c.satisfied for c in clauses) else NOT_SATISFIED
        results.append(CriterionResult(
            criterion, record["decision"], verdict, clauses,
            " · ".join(f"({c.letter}) {c.observation}" for c in clauses)))
    return tuple(results)


def determination(root: Path = REPO_ROOT) -> dict:
    results = measure(root)
    return {
        "authority": f"delegated under {DELEGATION_INSTRUMENT}",
        "criteria": len(results),
        "satisfied": sum(1 for r in results if r.verdict == SATISFIED),
        "not_satisfied": tuple(r.criterion for r in results
                               if r.verdict == NOT_SATISFIED),
        "unknown": tuple(r.criterion for r in results if r.verdict == UNKNOWN),
        "all_satisfied": all(r.satisfied for r in results),
        "note": "DECISION MADE UNDER ACT-CC-P12-019",
    }


def main(argv=None) -> int:
    try:
        results = measure()
    except AcceptanceBoundaryUnavailable as unavailable:
        print("ACCEPTANCE BOUNDARY UNAVAILABLE")
        print(f"  {unavailable}")
        return 0
    for result in results:
        print(f"{result.criterion}  {result.verdict:<14} [{result.decision}]")
        for clause in result.clauses:
            print(f"    ({clause.letter}) {'ok ' if clause.satisfied else 'NO '}"
                  f"{clause.observation}")
    print()
    print("determination:", determination())
    print()
    print("DECISION MADE UNDER ACT-CC-P12-019 — delegated, not Founder-ratified.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
