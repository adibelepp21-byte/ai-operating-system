"""P12-W6 — negative controls (`§19` scope: `NEGATIVE CONTROLS`).

`§19` lists `NEGATIVE CONTROLS` as a verification scope of its own, beside
`MUTATION` and `REGRESSION`. It is not the same question as either.

The question is about the **verifiers**, not the system: *can each P12
verification instrument report a negative result at all?* An instrument that
structurally cannot fail is not a verifier — it is a formatted assertion, and
its green output carries no information. `§19` closes with the sentence that
makes this scope necessary: *"P12-W6 tidak boleh dianggap selesai hanya karena
unit tests individual hijau."*

**Every negative here is driven at runtime, in this process.** Citing an
instrument's own conformance suite would establish only that two surfaces exist
— Blueprint `§48` — and would let a verifier that has since stopped being able
to fail keep its demonstration. So each control constructs the condition, calls
the instrument, and checks the value that comes back.

**Nothing resident is altered.** Where a negative needs a different world, the
instrument is pointed at a temporary one.

A `NOT DEMONSTRATED` result is a finding about that instrument, not a failure of
this module.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

DEMONSTRATED = "DEMONSTRATED"
NOT_DEMONSTRATED = "NOT DEMONSTRATED"
UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class ControlResult:
    instrument: str
    status: str
    negative_sought: str
    detail: str


def _runtime_observation() -> Tuple[bool, str]:
    """`what_is_running` must be able to answer that it cannot answer."""
    from tools import p12_runtime_observation as obs
    with tempfile.TemporaryDirectory() as tmp:
        answer = obs.what_is_running(Path(tmp))
    if not answer["answerable"]:
        return True, "an empty observation root yields answerable=False"
    return False, ("an empty observation root still reported an answer: "
                   f"{answer!r}")


def _trace_registry() -> Tuple[bool, str]:
    """`what_has_run` must report nothing when nothing has run."""
    from tools import p12_trace_registry as reg
    with tempfile.TemporaryDirectory() as tmp:
        answer = reg.what_has_run(Path(tmp))
        failures = reg.what_has_failed(Path(tmp))
    if answer["records"] == 0 and not failures:
        return True, "an empty store root yields 0 records and 0 failures"
    return False, f"an empty store root reported {answer['records']} records"


def _certified_evidence_guard() -> Tuple[bool, str]:
    """The guard must refuse to guess when certification is undeterminable."""
    from tools import p12_certified_evidence_guard as guard
    original = guard.PHASE_EVIDENCE_ROOTS
    try:
        guard.PHASE_EVIDENCE_ROOTS = {}
        try:
            guard.protected_roots()
        except guard.CertificationUndeterminable as exc:
            return True, f"raised rather than returning an empty set: {str(exc)[:50]}"
        return False, ("with no declared evidence root the guard returned a "
                       "protected set instead of refusing")
    finally:
        guard.PHASE_EVIDENCE_ROOTS = original


def _cross_phase() -> Tuple[bool, str]:
    """Cross-phase verification must be able to say NOT EXERCISED."""
    from tools import p12_cross_phase_verification as cross
    summary = cross.summary()
    if summary["not_exercised"] > 0:
        return True, (f"{summary['not_exercised']} of {summary['phases']} "
                      "canonical phases report NOT EXERCISED on the live corpus")
    return False, ("every phase reports EXERCISED; the negative is not "
                   "demonstrated by this run")


def _cross_pd() -> Tuple[bool, str]:
    """Currency checking must drift when the registry does."""
    from tools import p12_cross_pd_verification as xpd
    original = xpd.REGISTRY
    try:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "absent-registry.md"
            xpd.REGISTRY = missing
            summary = xpd.summary()
        if summary["current"] == 0 and summary["unavailable"] > 0:
            return True, ("a missing registry yields "
                          f"{summary['unavailable']} UNAVAILABLE, 0 CURRENT")
        return False, (f"a missing registry still reported "
                       f"{summary['current']} checks CURRENT")
    finally:
        xpd.REGISTRY = original


def _fresh_process() -> Tuple[bool, str]:
    """Fresh-process verification must be able to report DIVERGED."""
    from tools import p12_fresh_process_verification as fresh
    original = fresh._there
    try:
        fresh._there = lambda expr: "'a value the parent process never computed'"
        results = fresh.verify()
        diverged = [r for r in results if r.status == fresh.DIVERGED]
        if diverged:
            return True, (f"a subprocess answering differently yields "
                          f"{len(diverged)} DIVERGED of {len(results)}")
        return False, ("a subprocess answering differently was still reported "
                       "as reproduced")
    finally:
        fresh._there = original


def _mutation() -> Tuple[bool, str]:
    """The mutation suite must report MISSED where nothing detects."""
    from tools import p12_mutation_verification as mutation
    summary = mutation.summary()
    if summary["missed"] > 0:
        return True, (f"{summary['missed']} of {summary['mutations']} report "
                      f"MISSED on the live corpus: "
                      f"{', '.join(summary['missed_mutations'])}")
    return False, ("every mutation reports DETECTED; the negative is not "
                   "demonstrated by this run")


def _regression() -> Tuple[bool, str]:
    """Regression verification must reach REGRESSED when a control is lost."""
    from unittest import mock
    from tools import p12_regression_verification as regression
    before = {"a.py::C::test_one": 3, "a.py::C::test_two": 2}
    after = {"a.py::C::test_one": 3}
    with mock.patch.object(regression, "inventory", side_effect=[before, after]):
        result = regression.structural()
    if result["status"] == regression.REGRESSED and result["removed"]:
        return True, ("a removed control drives the structural comparison to "
                      f"REGRESSED: {result['removed'][0]}")
    return False, "a removed control did not drive the comparison to REGRESSED"


def _self_model() -> Tuple[bool, str]:
    """The Self-Model must answer UNKNOWN rather than echo the live corpus.

    Pointed at an empty root, the three questions answered from stores — what
    capabilities exist, what is running, what failed — must report that they
    cannot see anything. Before `§19`'s `NEGATIVE CONTROLS` scope was built they
    returned answers byte-identical to the live ones, because they read the
    other modules' root constants and ignored the parameter.

    The remaining questions are reported, not hidden: several raise against a
    root that is not a git repository, and one is answered from declared
    constants that no corpus can change.
    """
    from tools import p12_self_model as model
    store_backed = (model.capabilities, model.running, model.failed)
    others = (model.identity, model.ownership, model.authority,
              model.authoritative, model.incomplete, model.changed,
              model.stale, model.unknowns, model.decisions)

    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp)
        statuses = [fn(empty).status.upper() for fn in store_backed]
        raised = 0
        for fn in others:
            try:
                fn(empty)
            except Exception:
                raised += 1

    unknown = [s for s in statuses if s == "UNKNOWN"]
    detail = (f"{len(unknown)} of {len(store_backed)} store-backed questions "
              f"answer UNKNOWN against an empty root; {raised} of "
              f"{len(others)} others raise rather than answering")
    if len(unknown) == len(store_backed):
        return True, detail
    return False, ("a store-backed question answered from the live corpus "
                   f"while pointed at an empty root — {detail}")


def _governance_index() -> Tuple[bool, str]:
    """The index must report a source as stale once it changes underneath."""
    from tools.governance_index import GovernanceIndex, tracked_markdown
    paths = tracked_markdown(REPO_ROOT)[:12]
    index, _ = GovernanceIndex.build(paths, REPO_ROOT)
    if not index.sources:
        return False, "the index recorded no sources; staleness cannot arise"
    with tempfile.TemporaryDirectory() as tmp:
        shadow = Path(tmp)
        for relative in index.sources:
            target = shadow / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("changed underneath\n", encoding="utf-8")
        stale = index.stale_sources(shadow)
    if len(stale) == len(index.sources):
        return True, (f"all {len(stale)} sources report stale once their bytes "
                      "differ from the hash recorded at build")
    return False, (f"only {len(stale)} of {len(index.sources)} sources "
                   "reported stale after every one of them changed")


#: One entry per P12 verification instrument, with the negative each must reach.
CONTROLS: Tuple[Tuple[str, str, Callable], ...] = (
    ("p12_runtime_observation", "cannot answer what is running",
     _runtime_observation),
    ("p12_trace_registry", "nothing has run", _trace_registry),
    ("p12_certified_evidence_guard", "certification undeterminable",
     _certified_evidence_guard),
    ("p12_cross_phase_verification", "a phase is NOT EXERCISED", _cross_phase),
    ("p12_cross_pd_verification", "the registry is UNAVAILABLE", _cross_pd),
    ("p12_fresh_process_verification", "a stage DIVERGED", _fresh_process),
    ("p12_mutation_verification", "a mutation is MISSED", _mutation),
    ("p12_regression_verification", "a class REGRESSED", _regression),
    ("p12_self_model", "a question answers UNKNOWN", _self_model),
    ("governance_index", "a source is stale", _governance_index),
)


def verify() -> Tuple[ControlResult, ...]:
    results = []
    for instrument, sought, control in CONTROLS:
        try:
            demonstrated, detail = control()
        except Exception as exc:  # pragma: no cover - defensive
            results.append(ControlResult(instrument, UNAVAILABLE, sought,
                                         f"control raised: {exc}"))
            continue
        results.append(ControlResult(
            instrument, DEMONSTRATED if demonstrated else NOT_DEMONSTRATED,
            sought, detail))
    return tuple(results)


def summary() -> dict:
    results = verify()
    return {
        "instruments": len(results),
        "demonstrated": sum(1 for r in results if r.status == DEMONSTRATED),
        "not_demonstrated": sum(1 for r in results
                                if r.status == NOT_DEMONSTRATED),
        "unavailable": sum(1 for r in results if r.status == UNAVAILABLE),
        "undemonstrated_instruments": tuple(
            r.instrument for r in results if r.status != DEMONSTRATED),
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.instrument:<32} {result.status:<17} "
              f"{result.negative_sought:<34} {result.detail[:60]}")
    print()
    print("summary:", summary())
    print()
    print("This measures the verifiers, not the system. An instrument that")
    print("cannot report a negative is a formatted assertion, not a check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
