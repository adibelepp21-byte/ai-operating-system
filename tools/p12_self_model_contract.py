"""P12-W5 — the self-model semantic contract (`§18`, `§36`–`§41`).

`§18` of the Authorization names **twelve** questions the self-model must answer
with evidence, and closes: `SELF-MODEL ≠ AUTHORITY`. `§36` adds that *"the
canonical question set must be preserved in full"* and that *"no shortened
substitute set may silently replace the canonical model."* `§41`: *"Self-model
operational state must derive from current authoritative state sources."*

**This module verifies the contract; it does not answer the questions.** The
answers live in `tools/p12_self_model`. What is established here is the thing
`ACT-CC-P12-W5-001 §25` asks for and an answer alone cannot give:

```text
WHY THIS ANSWER IS THE CORRECT SELF-MODEL ANSWER
```

so each question is bound to the source it reads, the authority that source
carries, the freshness that source supports, and whether that source is
**authoritative** in `§41`'s sense or a projection over one.

**The distinction `§10` of the Act singles out is enforced here.**

```text
NO INTERNAL CACHE  ≠  NO STALE SOURCE
```

A surface that re-derives on every call has fresh *projection* state. That says
nothing about whether the underlying source is current, and a self-model that
inferred the second from the first would report a stale world as a live one.
`projection_freshness_is_not_source_freshness()` is the control for it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

AUTHORITATIVE = "AUTHORITATIVE SOURCE"
PROJECTION = "PROJECTION OVER SOURCES"
DECLARED = "DECLARED CONSTANT"
DERIVED_INTERNALLY = "DERIVED FROM THIS MODEL"

BOUND = "BOUND"
UNBOUND = "UNBOUND"


@dataclass(frozen=True)
class QuestionContract:
    """One canonical question, and why its answer is the right one."""

    question: str
    answered_by: str
    reads: str
    source_kind: str
    source_authority: str
    freshness: str
    why_correct: str


#: `§18`'s twelve, in its order, each bound to what actually answers it.
#:
#: `reads` names the module the answer function actually imports — measured
#: from the read path, not assumed from the question's wording.
CONTRACT: Tuple[QuestionContract, ...] = (
    QuestionContract(
        "What am I?", "identity", "tools.derived_views",
        DECLARED,
        "P12 Blueprint §37; system identity is not organization, agent or "
        "process identity",
        "changes only when canonical architecture changes",
        "identity is declared by canonical architecture, not observed; a "
        "runtime that reported its own identity would be reporting a process"),
    QuestionContract(
        "What do I own?", "ownership", "tools.derived_views",
        DECLARED,
        "P11 organizational authority, bounded to organization (§20)",
        "changes only by organizational record",
        "ownership is an organizational fact; reading it from runtime state "
        "would make whatever happened to run look like what is owned"),
    QuestionContract(
        "What authority do I have?", "authority", "declared constants",
        DECLARED,
        "Founder and Architect instruments; §40 — no self-model field may "
        "create authority merely by representing it",
        "changes only when an instrument changes",
        "authority must come from the instrument. A state surface that "
        "answered this would become the authority by being read"),
    QuestionContract(
        "What capabilities exist?", "capabilities", "tools.organization_catalog",
        AUTHORITATIVE,
        "Department records under docs/architecture/organization",
        "declared; re-read on each call",
        "§39 separates DEFINED from EXECUTABLE; the records establish what is "
        "declared, and the answer is INFERRED because declaration is not "
        "runtime availability"),
    QuestionContract(
        "What is running?", "running", "tools.p12_runtime_observation",
        AUTHORITATIVE,
        "published runtime observations; observation is evidence, not "
        "permission",
        "liveness horizon; LIVE / STALE / TERMINATED / UNKNOWN",
        "only an observation can answer a present-tense question; a Trace "
        "record says what ran, past tense, and answering with one would "
        "substitute F-3 evidence for an F-4 question"),
    QuestionContract(
        "What failed?", "failed", "tools.p12_trace_registry",
        AUTHORITATIVE,
        "durable Trace records; ratified vocabulary",
        "durable and historical; a record never becomes stale",
        "failures are execution facts and must come from execution records; "
        "an empty registry is UNKNOWN, because zero records is no evidence "
        "rather than zero failures"),
    QuestionContract(
        "What is incomplete?", "incomplete", "tools.derived_views",
        AUTHORITATIVE,
        "Register headings and resident escalation records",
        "re-read on each call",
        "INFERRED deliberately: an unbridged gate is evidence a bridge was "
        "not recorded, which is not evidence that work is unfinished"),
    QuestionContract(
        "What is authoritative?", "authoritative", "declared constants",
        DECLARED,
        "P12 Blueprint §2.1 authority hierarchy",
        "changes only when the hierarchy changes",
        "the hierarchy is canonical text; deriving it from what happens to be "
        "readable would let implementation decide precedence"),
    QuestionContract(
        "What changed?", "changed", "tools.stale_state_audit",
        AUTHORITATIVE,
        "Register §4 External Corpus Synchronization Ledger",
        "recorded supersessions; a file mtime is not a governance change",
        "change is a governance fact. Filesystem timestamps would report "
        "edits, not changes of state"),
    QuestionContract(
        "What is stale?", "stale", "tools.derived_views",
        AUTHORITATIVE,
        "Register §4 synchronization ledger",
        "open synchronizations",
        "staleness here means an unsynchronized external corpus, which is a "
        "different fact from an index whose content hash has drifted"),
    QuestionContract(
        "What do I not know?", "unknowns", "this model's own answers",
        DERIVED_INTERNALLY,
        "the twelve answers themselves",
        "recomputed whenever the answers are",
        "the only honest source for what is unknown is the set of questions "
        "this model could not answer; any other source would be asserting an "
        "absence it cannot see"),
    QuestionContract(
        "What decisions are recorded?", "decisions", "tools.derived_views",
        AUTHORITATIVE,
        "the governance register and decision instruments",
        "re-read on each call",
        "decisions are governance records. A projection could report their "
        "count; only the records establish what was decided"),
)


def canonical_questions() -> Tuple[str, ...]:
    """`§18`'s set, read from the self-model rather than restated here."""
    from tools import p12_self_model as model
    return tuple(model.QUESTIONS)


def contract_is_complete() -> dict:
    """`§36` — the canonical set in full, no shortened substitute."""
    declared = canonical_questions()
    covered = tuple(c.question for c in CONTRACT)
    return {
        "canonical": len(declared),
        "contracted": len(covered),
        "in_order": list(declared) == list(covered),
        "missing": tuple(q for q in declared if q not in covered),
        "extra": tuple(q for q in covered if q not in declared),
    }


def source_kinds() -> dict:
    """`§41` — which answers derive from an authoritative source."""
    kinds: dict = {}
    for item in CONTRACT:
        kinds.setdefault(item.source_kind, []).append(item.answered_by)
    return {kind: tuple(names) for kind, names in sorted(kinds.items())}


def answers_bound_to_their_source() -> Tuple[Tuple[str, str], ...]:
    """Does each answer function actually read the module the contract names?

    Measured from the syntax tree. A contract that merely asserted a binding
    would document an intention; this reports whether the binding is there.

    **Module-level aliases and one level of helper delegation are followed.**
    The first version inspected only imports written *inside* each function and
    reported `incomplete`, `stale` and `decisions` as `UNBOUND`. All three read
    `derived_views` through a module-level alias by way of the `_projection`
    helper, so all three were bound and the checker could not see it. A binding
    check that misses the way this module is actually written reports a defect
    in the code it is reading when the defect is its own.
    """
    import ast
    source = (REPO_ROOT / "tools" / "p12_self_model.py").read_text(
        encoding="utf-8")
    tree = ast.parse(source)

    # Module-level aliases: `from tools import derived_views as views` binds the
    # name `views` to that module for every function in the file.
    aliases: dict = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                aliases[alias.asname or alias.name] = (
                    f"{node.module}.{alias.name}")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name] = alias.name

    def modules_reached(node: ast.FunctionDef, functions: dict,
                        depth: int = 1) -> set:
        found = set()
        for inner in ast.walk(node):
            if isinstance(inner, ast.ImportFrom) and inner.module:
                found.update(f"{inner.module}.{a.name}" for a in inner.names)
                found.add(inner.module)
            elif isinstance(inner, ast.Import):
                found.update(a.name for a in inner.names)
            elif isinstance(inner, ast.Name) and inner.id in aliases:
                found.add(aliases[inner.id])
            elif isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name):
                helper = functions.get(inner.func.id)
                if helper is not None and depth > 0:
                    found |= modules_reached(helper, functions, depth - 1)
        return found

    functions = {n.name: n for n in tree.body
                 if isinstance(n, ast.FunctionDef)}
    reads = {name: modules_reached(node, functions)
             for name, node in functions.items()}

    results = []
    for item in CONTRACT:
        if item.source_kind in (DECLARED, DERIVED_INTERNALLY):
            results.append((item.answered_by, BOUND))
            continue
        imported = reads.get(item.answered_by, set())
        expected = item.reads.rsplit(".", 1)[-1]
        bound = any(expected in name for name in imported)
        results.append((item.answered_by, BOUND if bound else UNBOUND))
    return tuple(results)


def projection_freshness_is_not_source_freshness() -> dict:
    """`ACT §10` — the distinction a re-derived projection cannot establish.

    W2 re-derives on every call, so its `observed_at` is always now. That is
    **projection** freshness. Whether the underlying source is current is a
    separate question its own source answers, and the two are measured
    separately here so neither can stand in for the other.
    """
    from tools import p12_operational_state as w2
    from tools import p12_runtime_observation as obs

    entries = {e.state_id: e for e in w2.project()}
    runtime = entries["runtime.observed"]
    observations = obs.observations(obs.OBSERVATION_ROOT)
    live = [o for o in observations if o.classification == "LIVE"]
    stale_or_done = [o for o in observations
                     if o.classification in ("STALE", "TERMINATED")]
    return {
        "projection_observed_at": runtime.observed_at,
        "projection_status": runtime.status,
        "source_observations": len(observations),
        "source_live": len(live),
        "source_stale_or_terminated": len(stale_or_done),
        "distinct": bool(stale_or_done) and runtime.status == w2.CURRENT,
        "detail": ("the projection reports CURRENT because it was just "
                   f"re-derived, while {len(stale_or_done)} of "
                   f"{len(observations)} underlying observations are stale or "
                   "terminated; a self-model inferring source freshness from "
                   "projection freshness would report a stopped world as live"),
    }


def self_model_is_not_authority() -> dict:
    """`§18` / `§40` — the self-model may represent authority, never create it."""
    import ast
    source = (REPO_ROOT / "tools" / "p12_self_model.py").read_text(
        encoding="utf-8")
    names = [node.name for node in ast.walk(ast.parse(source))
             if isinstance(node, ast.FunctionDef)]
    creating = [name for name in names
                if name.lower().startswith(("authorize", "authorise", "certify",
                                            "approve", "permit", "grant",
                                            "ratify"))]
    from tools import p12_self_model as model
    answer = model.authority()
    return {
        "authority_creating_functions": tuple(creating),
        "authority_answer_status": answer.status,
        "authority_answer_is_representation": answer.value is not None,
        "detail": ("the authority answer represents what instruments say; no "
                   "function here creates authority by naming it"),
    }


def summary() -> dict:
    complete = contract_is_complete()
    bindings = answers_bound_to_their_source()
    unbound = tuple(name for name, status in bindings if status == UNBOUND)
    freshness = projection_freshness_is_not_source_freshness()
    authority = self_model_is_not_authority()
    return {
        "canonical_questions": complete["canonical"],
        "contracted": complete["contracted"],
        "in_order": complete["in_order"],
        "missing": complete["missing"],
        "unbound_answers": unbound,
        "source_kinds": {k: len(v) for k, v in source_kinds().items()},
        "projection_freshness_distinct": freshness["distinct"],
        "authority_creating_functions": authority[
            "authority_creating_functions"],
    }


def main(argv=None) -> int:
    for item in CONTRACT:
        print(f"{item.question:<31} {item.answered_by:<14} "
              f"{item.source_kind:<24} {item.reads}")
    print()
    print("bindings:", dict(answers_bound_to_their_source()))
    print()
    freshness = projection_freshness_is_not_source_freshness()
    print(f"projection freshness ≠ source freshness: {freshness['distinct']}")
    print(f"  {freshness['detail'][:120]}")
    print()
    print("summary:", summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
