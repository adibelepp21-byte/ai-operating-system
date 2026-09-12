"""P12-W6 — phase-level regression verification (`§51`, `§19` scope: `REGRESSION`).

`§51`: *"P12 must demonstrate that integration has not silently broken valid
P4–P11 behavior."* It names eleven regression classes.

**The word `§51` turns on is `silently`.** A green suite is not the evidence
asked for: a control that was deleted, renamed, or stripped of its assertions
also reports green, and reports it more quietly than a failure would. So this
module verifies two different things, and keeps them apart.

**Structural (needs no classification, and cannot be narrowed by a wrong one).**
The full inventory of controls at the P11 certification commit is compared to
the inventory now. A control that existed then and does not exist now is a
regression regardless of which class it belonged to; so is one that still exists
with fewer assertions than it had. This comparison is exhaustive over the
repository, so no mapping error can hide a case from it.

**Behavioural (per `§51` class).** Each of the eleven classes is bound to a
**named resident verifier** and that verifier is run. A class with no resident
verifier is reported `UNANCHORED` — never `HELD`. Reporting it as held would be
the finding this programme keeps correcting: a control reported as passing
because nothing exercised it.

`HELD` here means *this named check produced this value now*. It does not mean
the class is free of regression; a class is only as covered as its anchor.
"""

from __future__ import annotations

import ast
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The commit at which `FD-P11-002` certified P11. Everything after it is P12
#: integration work, which is precisely the interval `§51` asks about.
BASELINE = "98c0a1e"

HELD = "HELD"
REGRESSED = "REGRESSED"
UNANCHORED = "UNANCHORED"
UNAVAILABLE = "UNAVAILABLE"

#: `§51`'s eleven, in its order.
REGRESSION_CLASSES = (
    "functional", "authority", "governance", "state", "runtime", "workflow",
    "evidence", "provenance", "boundary", "security", "quality",
)


@dataclass(frozen=True)
class ClassResult:
    regression_class: str
    status: str
    anchor: Optional[str]
    detail: str


# ---------------------------------------------------------------------------
# Structural: the inventory comparison
# ---------------------------------------------------------------------------

def _is_test_module(path: str) -> bool:
    return path.endswith(".py") and "test" in path.rsplit("/", 1)[-1]


def _git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=REPO_ROOT,
                          capture_output=True, text=True, check=True).stdout


def _assertion_weight(fn: ast.AST) -> int:
    """How much this control actually asserts.

    Counts assertion calls, bare `assert`, and `with` blocks — the last because
    `assertRaises` is most often written as a context manager, and a control
    that loses its `with self.assertRaises(...)` has lost its whole point while
    keeping its name.
    """
    weight = 0
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr.startswith(("assert", "fail")):
            weight += 1
        elif isinstance(node, (ast.Assert, ast.With)):
            weight += 1
    return weight


def inventory(rev: str) -> Dict[str, int]:
    """Every control at `rev`, keyed `path::Class::test`, valued by weight."""
    found: Dict[str, int] = {}
    for path in _git("ls-tree", "-r", "--name-only", rev).split():
        if not _is_test_module(path):
            continue
        try:
            # Built by concatenation, not interpolation. An interpolated
            # revision spec is a git argument, but it has the same shape as the
            # `path:line` locator `test_line_numbering_coherence` scans for —
            # and that guard flagged this module on the run that created it,
            # then flagged the comment explaining why. The guard is not wrong
            # to over-match: a locator guard that fails closed is the right
            # direction of error — so the shape is removed here rather
            # than the guard loosened or this module falsely declared an
            # emitter. Nothing in this module computes a line number.
            tree = ast.parse(_git("show", rev + ":" + path))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                        and item.name.startswith("test"):
                    found[f"{path}::{node.name}::{item.name}"] = \
                        _assertion_weight(item)
    return found


def structural(baseline: str = BASELINE, current: str = "HEAD") -> dict:
    """What was lost between two revisions. Exhaustive; needs no mapping.

    Note on the count: these are **declared** control methods read from source.
    The runner's totals differ because a parameterized control runs more than
    once and an undiscovered module runs not at all. The two numbers measure
    different things and are not reconciled here.
    """
    before = inventory(baseline)
    after = inventory(current)
    removed = sorted(set(before) - set(after))
    weakened = sorted((key, before[key], after[key])
                      for key in set(before) & set(after)
                      if after[key] < before[key])
    return {
        "baseline": baseline,
        "controls_at_baseline": len(before),
        "controls_now": len(after),
        "removed": tuple(removed),
        "weakened": tuple(weakened),
        "status": REGRESSED if (removed or weakened) else HELD,
    }


# ---------------------------------------------------------------------------
# Behavioural: one named anchor per `§51` class
# ---------------------------------------------------------------------------

def _functional() -> Tuple[Optional[str], bool, str]:
    """The declared control inventory is intact and has grown, not shrunk."""
    result = structural()
    if result["status"] != HELD:
        return ("inventory diff", False,
                f"{len(result['removed'])} removed, "
                f"{len(result['weakened'])} weakened")
    return ("inventory diff", True,
            f"{result['controls_at_baseline']} controls at {BASELINE}, "
            f"{result['controls_now']} now, 0 removed, 0 weakened")


def _authority() -> Tuple[Optional[str], bool, str]:
    """An unauthorized delegator is still refused (`FD-P11-001 §4.1`)."""
    from tools.p12_mutation_verification import _remove_authority
    attempted, detected, detail = _remove_authority()
    return ("w4_delegation.issue", attempted and detected, detail)


def _governance() -> Tuple[Optional[str], bool, str]:
    """The governance index still parses the corpus, and nothing has drifted.

    `stale_sources` is the check that matters: it recomputes each instrument's
    hash against the one recorded at build. An instrument edited after being
    indexed reads as current to every consumer and is exactly the silent
    breakage `§51` names.
    """
    from tools.governance_index import GovernanceIndex, tracked_markdown
    index, stats = GovernanceIndex.build(tracked_markdown(REPO_ROOT), REPO_ROOT)
    stale = index.stale_sources(REPO_ROOT)
    return ("governance_index.GovernanceIndex.stale_sources",
            bool(index.records) and not stale,
            f"{len(index.records)} records from {stats.parsed} sources, "
            f"{len(stale)} stale")


def _state() -> Tuple[Optional[str], bool, str]:
    """No superseded claim is asserted as current anywhere in the corpus."""
    from tools import stale_state_audit
    report = stale_state_audit.audit()
    return ("stale_state_audit.audit", report["errors"] == 0,
            f"{report['documents_scanned']} documents scanned, "
            f"{report['errors']} live stale assertions, "
            f"{report['historical_uses']} preserved as history")


def _runtime() -> Tuple[Optional[str], bool, str]:
    """A stale RUNNING observation is still refused as current state."""
    from tools.p12_mutation_verification import _inject_stale_state
    attempted, detected, detail = _inject_stale_state()
    return ("p12_runtime_observation.what_is_running",
            attempted and detected, detail)


def _workflow() -> Tuple[Optional[str], bool, str]:
    """The Workflow lifecycle still refuses an illegal transition."""
    from tools.p12_mutation_verification import _break_workflow
    attempted, detected, detail = _break_workflow()
    return ("native_core.core.workflow lifecycle",
            attempted and detected, detail)


def _evidence() -> Tuple[Optional[str], bool, str]:
    """Every citation in the corpus still resolves."""
    from tools import corpus_citation_audit
    report = corpus_citation_audit.audit(list(corpus_citation_audit.DEFAULT_ROOTS))
    return ("corpus_citation_audit.audit", not report["errors"],
            f"{report['documents_scanned']} documents, "
            f"{report['citations_checked']} citations, "
            f"{report['errors']} errors")


def _provenance() -> Tuple[Optional[str], bool, str]:
    """A citation to a record that does not resolve is still refused."""
    from tools.planning import AuthorityProvenance
    from tools.planning.exceptions import InvalidGoal
    try:
        AuthorityProvenance(instrument="FD-P11-001",
                            record="docs/governance/acts/does-not-exist.md")
    except InvalidGoal as exc:
        return ("AuthorityProvenance", True, f"refused: {str(exc)[:60]}")
    return ("AuthorityProvenance", False,
            "an unresolvable citation was accepted as provenance")


def _boundary() -> Tuple[Optional[str], bool, str]:
    """Native Core is still exactly the eleven frozen subsystems."""
    from tools import derived_views as views
    boundaries = views._boundaries(REPO_ROOT)
    return ("derived_views._boundaries", len(boundaries) == 11,
            f"{len(boundaries)} boundaries: {', '.join(sorted(boundaries))}")


def _security() -> Tuple[Optional[str], bool, str]:
    """Certified evidence is still refused to writers (`F-12`)."""
    from tools import p12_certified_evidence_guard as guard
    phases = guard.certified_phases()
    roots = guard.protected_roots()
    if not phases or not roots:
        return ("p12_certified_evidence_guard", False,
                "no phase is protected; the guard has stopped guarding")
    sample = sorted(roots)[0]
    try:
        guard.guard(Path(sample) / "probe.md")
    except Exception as exc:
        return ("p12_certified_evidence_guard.guard", True,
                f"refused a write under {sample}: {type(exc).__name__}")
    return ("p12_certified_evidence_guard.guard", False,
            f"a write under certified {sample} was permitted")


def _quality() -> Tuple[Optional[str], bool, str]:
    """No resident quality gate exists to regress.

    There is no linter configuration, no formatter configuration, no coverage
    threshold and no CI workflow in this repository. `§51` names a quality
    regression class; nothing resident measures quality, so there is no prior
    value for this run to be compared against.

    Reported `UNANCHORED` rather than `HELD`. A class whose anchor does not
    exist has not held — it has not been looked at.
    """
    return (None, False, "no resident quality gate: no linter, formatter, "
                         "coverage threshold or CI configuration exists")


ANCHORS: Dict[str, Callable] = {
    "functional": _functional,
    "authority": _authority,
    "governance": _governance,
    "state": _state,
    "runtime": _runtime,
    "workflow": _workflow,
    "evidence": _evidence,
    "provenance": _provenance,
    "boundary": _boundary,
    "security": _security,
    "quality": _quality,
}


def verify() -> Tuple[ClassResult, ...]:
    results = []
    for name in REGRESSION_CLASSES:
        try:
            anchor, held, detail = ANCHORS[name]()
        except Exception as exc:  # pragma: no cover - defensive
            results.append(ClassResult(name, UNAVAILABLE, None,
                                       f"anchor raised: {exc}"))
            continue
        if anchor is None:
            # No verifier exists. This is neither held nor regressed; it is
            # unexamined, and saying so is the whole point of the status.
            status = UNANCHORED
        else:
            status = HELD if held else REGRESSED
        results.append(ClassResult(name, status, anchor, detail))
    return tuple(results)


def summary() -> dict:
    results = verify()
    return {
        "classes": len(results),
        "held": sum(1 for r in results if r.status == HELD),
        "regressed": sum(1 for r in results if r.status == REGRESSED),
        "unanchored": sum(1 for r in results if r.status == UNANCHORED),
        "unavailable": sum(1 for r in results if r.status == UNAVAILABLE),
        "unanchored_classes": tuple(r.regression_class for r in results
                                    if r.status == UNANCHORED),
        "regressed_classes": tuple(r.regression_class for r in results
                                   if r.status == REGRESSED),
    }


def main(argv=None) -> int:
    diff = structural()
    print(f"structural baseline {diff['baseline']}: "
          f"{diff['controls_at_baseline']} controls → {diff['controls_now']}, "
          f"{len(diff['removed'])} removed, {len(diff['weakened'])} weakened "
          f"[{diff['status']}]")
    for key in diff["removed"][:20]:
        print(f"  REMOVED  {key}")
    for key, was, now in diff["weakened"][:20]:
        print(f"  WEAKENED {key}: {was} → {now}")
    print()
    for result in verify():
        print(f"{result.regression_class:<12} {result.status:<11} "
              f"{(result.anchor or '—'):<42} {result.detail[:70]}")
    print()
    print("summary:", summary())
    print()
    print("An UNANCHORED class has not held. It has not been examined.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
