"""P12-W5 — the AIOS self-model.

Authorized by the Founder P12 Authorization Decision `§18`, which names the
twelve questions this module must answer **evidence-backed**, and by `§10`'s
single bounded `W1`–`W6` mandate.

**This module owns no truth.** Every answer is recomputed from an authoritative
source on each call; nothing is stored, cached, or promoted. Delete it and AIOS
loses no fact — only the ability to ask itself twelve questions in one place.
That is the property that keeps a self-model a *representation* rather than a
second source of truth, and it is what `§18` requires when it says:

```text
SELF-MODEL ≠ AUTHORITY
```

`§18` adds the sharper form: the self-model *"tidak dapat mengotorisasi dirinya
sendiri berdasarkan informasi yang ditemukannya."* Nothing here returns a
permission, and `authority()` reports **who holds** authority — never that the
caller has any.

**Why this is a new module rather than an extension of `derived_views`.** That
module's docstring records a `§26` prohibition on building a Self-Model, citing
`ACT-CC-R2BC-IMPL-001` — **which is not resident in this repository**. The
prohibition can be neither verified nor dismissed, so it is honoured: the
projection there stays a projection, and the self-model P12 authorizes is built
here, consuming it as one source among several.

**`UNKNOWN` is a correct answer.** Three of the twelve questions have no source
in this repository, and each returns `UNKNOWN` naming the absent source rather
than a plausible guess. `§23` of the Decision fixes the rule this depends on:

```text
MEASUREMENT ≠ PREDICTION
```
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Tuple

from tools import derived_views as views
from tools.derived_views import INFERRED, REPO_ROOT, UNKNOWN, VERIFIED

#: The twelve questions, in the order the Decision's `§18` lists them. The order
#: is part of the citation: a reader checking this module against `§18` should
#: be able to read straight down.
QUESTIONS: Tuple[str, ...] = (
    "What am I?",
    "What do I own?",
    "What authority do I have?",
    "What capabilities exist?",
    "What is running?",
    "What failed?",
    "What is incomplete?",
    "What is authoritative?",
    "What changed?",
    "What is stale?",
    "What do I not know?",
    "What decisions are recorded?",
)


@dataclass(frozen=True)
class Answer:
    """One answer, carrying its own evidence status and the source it came from.

    A caller reading `.value` without `.status` is reading half the record, so
    the status travels with the value rather than beside it.
    """

    question: str
    value: Any
    status: str
    source: str

    @property
    def is_known(self) -> bool:
        return self.status in (VERIFIED, INFERRED) and self.value is not None


def _projection(root: Path) -> dict:
    return {f.question: f for f in views.self_knowledge(root).facts}


def identity(root: Path = REPO_ROOT) -> Answer:
    """What am I? — established from frozen architecture, not from self-description.

    The honest answer is structural: AIOS is the system whose Native Core is
    these eleven frozen subsystem boundaries. Naming itself from a document that
    calls it AIOS would be circular; counting its own frozen boundaries is not.
    """
    boundaries = views._boundaries(root)
    return Answer(
        "What am I?",
        {
            "system": "AIOS",
            "native_core_boundaries": len(boundaries),
            "boundaries": boundaries,
            "frozen": True,
        },
        VERIFIED,
        "native_core/core/ directory structure; Native Core frozen at 11",
    )


def ownership(root: Path = REPO_ROOT) -> Answer:
    """What do I own? — the governance corpus it can account for."""
    fact = _projection(root)["what exists"]
    return Answer("What do I own?", fact.value, fact.status, fact.source)


def authority(root: Path = REPO_ROOT) -> Answer:
    """What authority do I have? — reported, never exercised.

    Returns the *holders* of authority and the matters that remain reserved.
    Representing a reserved matter here does not resolve it, and representing a
    delegation does not widen it.
    """
    return Answer(
        "What authority do I have?",
        {
            "founder_reserved": (
                "phase authorization", "phase certification", "E-criteria ratification",
                "constitutional boundary", "Native Core expansion",
                "FDP-P10-001 Security", "FDP-P10-002 Quality", "FDP-P10-003 Governance",
            ),
            "architect_reserved": (
                "ADP-P10-001 entity semantics", "prioritization/ranking/heuristics",
                "escalation entity semantics",
            ),
            "delegated_to_co_founder": (
                "discover", "design within issued architecture", "implement",
                "integrate", "test", "verify", "persist", "reconcile", "document",
            ),
            "self_model_authority": None,
        },
        VERIFIED,
        "DP-01 §8; FD-P11-001 §12; FD-P10-005 §4; P12 Authorization §13",
    )


def capabilities(root: Path = REPO_ROOT) -> Answer:
    """What capabilities exist? — declared capabilities, not proven ones.

    A declaration is not runtime availability, so the status is `INFERRED`: the
    records are read directly, but that a Capability is *declared* does not
    establish that it is executable.
    """
    from tools import organization_catalog as org

    # `read_departments` takes the ORGANIZATION root, not the repository root.
    # The first version of this function passed `root` and received an empty
    # list without raising, then reported `INFERRED` over nothing — a guard that
    # passes because it cannot see. The empty case is now an explicit `UNKNOWN`.
    departments = org.read_departments(org.ORGANIZATION_ROOT)
    if not departments:
        return Answer(
            "What capabilities exist?",
            None,
            UNKNOWN,
            "no Department records readable under docs/architecture/organization",
        )
    declared = tuple(sorted(
        capability for d in departments for capability in d.capabilities
    ))
    return Answer(
        "What capabilities exist?",
        {
            "declared": declared,
            "count": len(declared),
            "departments": len(departments),
        },
        INFERRED,
        "Department records; a declaration is not runtime availability",
    )


def running(root: Path = REPO_ROOT) -> Answer:
    """What is running? — from freshness-qualified runtime observation.

    Deliberately **not** answered from the Trace registry. A Trace record says
    what *ran*, past tense; reading one back is not observation of a live
    process, and answering `F-4` with `F-3`'s evidence would be the substitution
    this model exists to refuse.

    `UNKNOWN` in two distinct cases, and the distinction is the point: no
    observation has been published, or every published observation is stale.
    Neither is "nothing is running" — a runtime can die without publishing a
    terminal state, and the evidence cannot tell that apart from one still up.
    """
    from tools import p12_runtime_observation as runtime_obs

    answer = runtime_obs.what_is_running(runtime_obs.OBSERVATION_ROOT)
    if not answer["answerable"]:
        return Answer(
            "What is running?",
            None,
            UNKNOWN,
            answer["reason"],
        )
    return Answer(
        "What is running?",
        {
            "live": answer["live"],
            "live_by_kind": answer["live_by_kind"],
            "terminated": answer.get("terminated", ()),
            "observations": answer["observations"],
            "scope": answer["scope"],
        },
        VERIFIED,
        f"runtime observation within a "
        f"{runtime_obs.LIVE_HORIZON_SECONDS:g}s liveness horizon",
    )


def failed(root: Path = REPO_ROOT) -> Answer:
    """What failed? — from durable Trace records where any exist.

    Answered `UNKNOWN` until P12-W4 gave the Trace boundary a durable store to
    write into. It is still `UNKNOWN` when no store exists: an empty registry
    means *no evidence*, not *no failures*, and reporting zero failures from
    zero records would be the cleanest possible lie.

    `escalation` is not counted here. The ratified vocabulary keeps it distinct
    from `failure`, and `DP-02 §3 E11-03` settled that a correct refusal is not
    an execution failure.
    """
    from tools import p12_trace_registry as traces

    summary = traces.what_has_run(traces.STORE_ROOT)
    if summary["stores"] == 0:
        return Answer(
            "What failed?",
            None,
            UNKNOWN,
            "no durable Trace store exists; absence of records is not absence of failures",
        )
    failures = traces.what_has_failed(traces.STORE_ROOT)
    return Answer(
        "What failed?",
        {
            "failures": len(failures),
            "outputs": tuple(f.outputs for f in failures),
            "records_examined": summary["records"],
        },
        VERIFIED,
        f"durable Trace records across {summary['stores']} store(s)",
    )


def incomplete(root: Path = REPO_ROOT) -> Answer:
    """What is incomplete? — open escalations and unbridged governance gates.

    `INFERRED`, deliberately. An unbridged gate is evidence that a bridge was
    not recorded, which is not the same as evidence that work is unfinished, and
    collapsing the two would manufacture certainty `§23` forbids.
    """
    unbridged = views.unbridged_gates(root)
    escalations = tuple(sorted(
        p.stem.replace(".escalation", "")
        for p in (root / "docs/architecture/p11").rglob("*.escalation.json")
    ))
    return Answer(
        "What is incomplete?",
        {"unbridged_gates": len(unbridged), "open_escalations": escalations},
        INFERRED,
        "Register headings; escalation records under docs/architecture/p11",
    )


def authoritative(root: Path = REPO_ROOT) -> Answer:
    """What is authoritative? — the source hierarchy, named from canon.

    Broader than *"what decisions are recorded"*: a decision is one kind of
    authority, and the Constitution and Canonical Architecture outrank it.
    """
    return Answer(
        "What is authoritative?",
        {
            "hierarchy": (
                "Mission / Constitution",
                "Canonical Architecture",
                "Master Program",
                "Canonical P10-P13 Blueprint",
                "Ratified Founder Decisions",
                "Ratified Architect Decisions",
                "Current repository / implementation",
                "Current evidence / verification",
            ),
            "canonical_architecture_adopted": False,
        },
        VERIFIED,
        "P12 Blueprint §2.1; candidate architecture adoption remains Founder-reserved",
    )


def changed(root: Path = REPO_ROOT) -> Answer:
    """What changed? — supersession recorded in the Register, not file mtimes.

    A filesystem timestamp records that bytes moved, which is not a governance
    change. Only recorded supersession is reported.
    """
    # The first version returned the *staleness* fact relabelled as
    # "recorded_supersessions". The value was the open-synchronization list, so
    # the label described something the data was not. Supersession is read from
    # the Register, which is its authority.
    from tools import stale_state_audit as stale_audit

    claims = stale_audit.superseded_claims(root)
    return Answer(
        "What changed?",
        {
            "recorded_supersessions": len(claims),
            "claims": tuple(c.get("claim", c.get("id", "?")) for c in claims),
        },
        VERIFIED,
        "Register §4 External Corpus Synchronization Ledger; "
        "a file mtime is not a governance change",
    )


def stale(root: Path = REPO_ROOT) -> Answer:
    """What is stale? — open external synchronizations."""
    fact = _projection(root)["what is stale"]
    return Answer("What is stale?", fact.value, fact.status, fact.source)


def unknowns(root: Path = REPO_ROOT) -> Answer:
    """What do I not know? — the questions this model cannot answer.

    Computed from the answers themselves rather than listed by hand, so it can
    never disagree with them. A hand-maintained list of one's own ignorance is
    the first thing to go stale.
    """
    unknown = tuple(
        a.question for a in _answers(root) if a.question != "What do I not know?"
        and a.status == UNKNOWN
    )
    return Answer(
        "What do I not know?",
        {"unanswered_questions": unknown, "count": len(unknown)},
        VERIFIED,
        "derived from this model's own answers",
    )


def decisions(root: Path = REPO_ROOT) -> Answer:
    """What decisions are recorded? — from the Register."""
    fact = _projection(root)["what decisions are recorded"]
    return Answer(
        "What decisions are recorded?",
        {"identifiers": fact.value, "count": len(fact.value)},
        fact.status,
        fact.source,
    )


_ANSWERERS = (
    identity, ownership, authority, capabilities, running, failed,
    incomplete, authoritative, changed, stale, unknowns, decisions,
)


def _answers(root: Path) -> Tuple[Answer, ...]:
    """Every answer except `unknowns`, which is derived from these."""
    return tuple(f(root) for f in _ANSWERERS if f is not unknowns)


def self_model(root: Path = REPO_ROOT) -> Tuple[Answer, ...]:
    """All twelve answers, in the Decision's `§18` order."""
    answers = {a.question: a for a in _answers(root)}
    answers["What do I not know?"] = unknowns(root)
    return tuple(answers[q] for q in QUESTIONS)


def coverage(root: Path = REPO_ROOT) -> dict:
    """How many of the twelve are answered from evidence, and how many are not."""
    model = self_model(root)
    return {
        "questions": len(QUESTIONS),
        "verified": sum(1 for a in model if a.status == VERIFIED),
        "inferred": sum(1 for a in model if a.status == INFERRED),
        "unknown": sum(1 for a in model if a.status == UNKNOWN),
    }


def main(argv: Optional[list] = None) -> int:
    for answer in self_model():
        value = str(answer.value)
        if len(value) > 88:
            value = value[:85] + "..."
        print(f"{answer.status:<8} | {answer.question:<28} | {value}")
    print()
    print("coverage:", coverage())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
