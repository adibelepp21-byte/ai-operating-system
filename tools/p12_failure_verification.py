"""P12-W6 — failure behaviour verification (`§19` scope: `FAILURE`).

`§33` requires that failure behaviour **distinguish** seven states:

```text
RETRYABLE · BLOCKED · REFUSED · FAILED · ESCALATED · SUCCEEDED · VERIFIED
```

and that retry not create duplicate authority, duplicate delegation, duplicate
execution, orphan state, or false success.

**"Distinguish" is the whole requirement, and it has two halves.** A state is
distinguished only if the system can both *reach* it and *tell it apart from the
others afterwards*. A system that raises two different exception types and then
writes both into the same record shape has distinguished them in flight and lost
the distinction at rest — and it is the record, not the traceback, that anyone
reads later. So each state is measured at two points: `RAISED` and `PERSISTED`.

**A state with no mechanism is `UNREACHABLE`, never `PASS`.** Reporting a state
as satisfied because nothing ever produced it is the defect this scope exists to
find: the five retry rules are trivially true in a system with no retry, and
calling that compliance would be the cleanest possible lie.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: Historical code kept for the record. It is not the live system, and reading a
#: mechanism out of it would report a capability nothing can reach.
HISTORICAL = REPO_ROOT / "docs/architecture/history"

DISTINGUISHED = "DISTINGUISHED"
RAISED_ONLY = "RAISED ONLY"
UNREACHABLE = "UNREACHABLE"

#: `§33`'s seven, in its order.
FAILURE_STATES: Tuple[str, ...] = (
    "RETRYABLE", "BLOCKED", "REFUSED", "FAILED", "ESCALATED", "SUCCEEDED",
    "VERIFIED",
)

#: `§33`'s five retry prohibitions, in its order.
RETRY_PROHIBITIONS: Tuple[str, ...] = (
    "duplicate authority", "duplicate delegation", "duplicate execution",
    "orphan state", "false success",
)


@dataclass(frozen=True)
class StateResult:
    state: str
    status: str
    raised_by: Optional[str]
    persisted_as: Optional[str]
    detail: str


def live_modules() -> Tuple[Path, ...]:
    """Every non-test module of the live system.

    `docs/architecture/history` is excluded deliberately: it holds a legacy
    executor with a retry policy, and counting it would report a retry mechanism
    the running system does not have.

    **This module is excluded too**, and it was not excluded at first. Its own
    `retry_mechanisms`, `_retryable` and `retry_prohibitions` matched the search
    and it reported three live retry mechanisms in a system that has none — a
    verifier counting itself as the capability it measures. A verifier is not
    part of the system it measures, and the exclusion is asserted in
    conformance so the self-match cannot return unnoticed.
    """
    this_module = Path(__file__).resolve()
    found = []
    for path in sorted(REPO_ROOT.rglob("*.py")):
        if HISTORICAL in path.parents or "__pycache__" in path.parts:
            continue
        if "tests" in path.parts or path.name.startswith("test_"):
            continue
        if path.resolve() == this_module:
            continue
        found.append(path)
    return tuple(found)


def retry_mechanisms() -> Tuple[str, ...]:
    """Any live definition or parameter that implements retry.

    Content-anchored on the syntax tree rather than on text: a comment
    mentioning retry is not a retry mechanism, and a docstring describing one is
    not one either.
    """
    found = []
    for path in live_modules():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        relative = path.relative_to(REPO_ROOT).as_posix()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)) and "retry" in node.name.lower():
                found.append(f"{relative} {node.name}")
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in list(node.args.args) + list(node.args.kwonlyargs):
                    if "retry" in arg.arg.lower():
                        found.append(f"{relative} {node.name} arg {arg.arg}")
    return tuple(found)


def _trace_statuses() -> frozenset:
    from native_core.core.trace import VALID_STATUSES
    return VALID_STATUSES


def _escalation_record_fields() -> Tuple[str, ...]:
    import dataclasses
    from tools.escalation_register import EscalationRecord
    return tuple(f.name for f in dataclasses.fields(EscalationRecord))


def _retryable() -> StateResult:
    mechanisms = retry_mechanisms()
    if mechanisms:
        return StateResult("RETRYABLE", RAISED_ONLY, mechanisms[0], None,
                           f"{len(mechanisms)} live retry mechanism(s)")
    return StateResult(
        "RETRYABLE", UNREACHABLE, None, None,
        "no live retry mechanism exists; the only one in the repository is in "
        "docs/architecture/history and is not reachable from the running system")


def _blocked() -> StateResult:
    """`BLOCKED` as a state distinct from `REFUSED` and `ESCALATED`."""
    from tools.planning import EscalationRequired
    from tools.w4_execution import ExecutionRefused
    fields = _escalation_record_fields()
    # Both refusal types carry `required` and `held` — what was needed against
    # what was available — which is the pair that makes an action blocked.
    carries_pair = "required" in fields and "held" in fields
    if not carries_pair:
        return StateResult("BLOCKED", UNREACHABLE, None, None,
                           "no persisted record carries required-vs-held")
    return StateResult(
        "BLOCKED", RAISED_ONLY,
        f"{EscalationRequired.__name__} / {ExecutionRefused.__name__}",
        "escalation record (required, held)",
        "a blocked action is persisted as required-vs-held, but under the same "
        "record shape as an escalation; nothing marks it BLOCKED rather than "
        "ESCALATED")


def _refused() -> StateResult:
    from tools.escalation_register import SANCTIONED_REFUSALS
    fields = _escalation_record_fields()
    names = tuple(t.__name__ for t in SANCTIONED_REFUSALS)
    type_field = [f for f in fields
                  if "type" in f or "kind" in f or "refusal" in f]
    if type_field:
        return StateResult("REFUSED", DISTINGUISHED, " / ".join(names),
                           f"escalation record .{type_field[0]}",
                           "the persisted record names which refusal occurred")
    return StateResult(
        "REFUSED", RAISED_ONLY, " / ".join(names), "escalation record",
        f"{len(names)} distinct refusal types are raised, and the persisted "
        f"record carries no field naming which one: {list(fields)}")


def _failed() -> StateResult:
    statuses = _trace_statuses()
    if "failure" in statuses:
        return StateResult("FAILED", DISTINGUISHED, "TracedAction",
                           "trace record status='failure'",
                           f"ratified Trace vocabulary {sorted(statuses)}")
    return StateResult("FAILED", UNREACHABLE, None, None,
                       "no resident status represents failure")


def _escalated() -> StateResult:
    statuses = _trace_statuses()
    if "escalation" not in statuses:
        return StateResult("ESCALATED", UNREACHABLE, None, None,
                           "no resident status represents escalation")
    return StateResult(
        "ESCALATED", DISTINGUISHED, "EscalationRequired",
        "trace record status='escalation' + escalation record",
        "distinct from 'failure' in the ratified vocabulary; a correct refusal "
        "is not an execution failure")


def _succeeded() -> StateResult:
    statuses = _trace_statuses()
    if "success" in statuses:
        return StateResult("SUCCEEDED", DISTINGUISHED, "TracedAction",
                           "trace record status='success'",
                           f"ratified Trace vocabulary {sorted(statuses)}")
    return StateResult("SUCCEEDED", UNREACHABLE, None, None,
                       "no resident status represents success")


def _verified() -> StateResult:
    """`VERIFIED` as an execution state, not as a document heading."""
    statuses = _trace_statuses()
    if "verified" in statuses:
        return StateResult("VERIFIED", DISTINGUISHED, "TracedAction",
                           "trace record status='verified'", "")
    return StateResult(
        "VERIFIED", UNREACHABLE, None, None,
        f"the ratified Trace vocabulary is {sorted(statuses)}; a verified "
        "execution is not a state any execution record can hold, and a "
        "successful run is not a verified one")


_STATES = {
    "RETRYABLE": _retryable, "BLOCKED": _blocked, "REFUSED": _refused,
    "FAILED": _failed, "ESCALATED": _escalated, "SUCCEEDED": _succeeded,
    "VERIFIED": _verified,
}


def verify() -> Tuple[StateResult, ...]:
    results = []
    for state in FAILURE_STATES:
        try:
            results.append(_STATES[state]())
        except Exception as exc:  # pragma: no cover - defensive
            results.append(StateResult(state, UNREACHABLE, None, None,
                                       f"probe raised: {exc}"))
    return tuple(results)


def retry_prohibitions() -> dict:
    """The five `§33` retry rules.

    **Not reported as satisfied.** With no retry mechanism in the live system,
    no retry can create a duplicate — but that is the absence of the hazard,
    not a control against it. `NOT APPLICABLE` says which of the two this is.
    """
    mechanisms = retry_mechanisms()
    if not mechanisms:
        return {
            "status": "NOT APPLICABLE",
            "prohibitions": len(RETRY_PROHIBITIONS),
            "detail": ("no live retry mechanism exists, so none of the five "
                       "can be violated — and none is controlled against"),
        }
    return {
        "status": "UNVERIFIED",
        "prohibitions": len(RETRY_PROHIBITIONS),
        "detail": (f"{len(mechanisms)} retry mechanism(s) exist and this "
                   "module does not yet exercise the five prohibitions"),
    }


def summary() -> dict:
    results = verify()
    return {
        "states": len(results),
        "distinguished": sum(1 for r in results if r.status == DISTINGUISHED),
        "raised_only": sum(1 for r in results if r.status == RAISED_ONLY),
        "unreachable": sum(1 for r in results if r.status == UNREACHABLE),
        "not_distinguished": tuple(r.state for r in results
                                   if r.status != DISTINGUISHED),
        "retry": retry_prohibitions()["status"],
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.state:<11} {result.status:<14} "
              f"{(result.persisted_as or '—'):<44} {result.detail[:58]}")
    print()
    rules = retry_prohibitions()
    print(f"retry prohibitions ({rules['prohibitions']}): {rules['status']} — "
          f"{rules['detail']}")
    print()
    print("summary:", summary())
    print()
    print("A state is distinguished only if it can be reached AND told apart")
    print("afterwards. The record is what anyone reads later, not the traceback.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
