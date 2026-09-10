"""`P11-W5` — planning continuity. The chain survives; the authority does not travel.

Authorized by `DP-01 §3 W5`, which permits *"bounded organizational continuity
required for P11 operation"* including *"planning continuity"* and *"evidence
continuity"*, and which fixes the constraint the whole module is shaped around:

    MEMORY ≠ AUTHORITY

and *"No memory mechanism may create, elevate, or infer authority that has not
otherwise been granted."*

**Selected because it depends on nothing that is blocked.** `ACT-CC-P11-007 §17`
found W4 Autonomous Execution `AUTHORIZED + BLOCKED`: its loop runs
`PLAN → DELEGATE → EXECUTE → …`, and the `DELEGATE` step is not traversable
because no legitimate delegator exists. Planning continuity sits entirely
upstream of that gate.

**The property that makes this safe: authority is re-validated on restore, not
restored.**

A `PlanningSurface` is in-memory, so a plan chain vanishes with the process. The
naive fix is to serialize it and read it back — and that would quietly turn
storage into a source of authority: a plan whose citation was valid last week
would come back asserting it, whether or not the cited instrument still exists.

So restoring **re-constructs** `AuthorityProvenance`, which refuses a record that
does not resolve. If the instrument a plan was formed under has since been
removed, **the plan does not come back.** It fails closed, loudly, rather than
returning as a well-formed artifact citing a source that is gone.

    persisted plan  ──restore──▶  citation re-validated  ──▶  plan, or refusal

That is the difference between continuity and resurrection. Continuity carries
what was decided; it does not carry permission across time.

**What is deliberately not persisted:** nothing derived, nothing summarized. Only
the versions as they were written. Supersession is recomputed from the chain's
shape on load, exactly as `PlanningSurface` derives it in memory, so a restored
history cannot disagree with itself about which version is current.

**Bounded to planning.** `ACT-CC-P11-007 §35`: `P11 ≠ P12`. This persists goals
and plan chains and nothing else — no runtime, workflow, trace or execution
state. A continuity module that began answering *"what is the organization
doing"* would be P12 Unified Operational State, built early and unauthorized.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from tools.planning import (
    AuthorityProvenance,
    Goal,
    Plan,
    PlanOrigin,
    PlanStep,
    PlanningSurface,
)


class ContinuityError(RuntimeError):
    """Fail closed (`PR-4`)."""


def _plan_payload(plan: Plan) -> dict:
    return {
        "key": plan.key,
        "goal_key": plan.goal_key,
        "origin": plan.origin.value,
        "revision": plan.revision,
        "supersedes": plan.supersedes,
        "reason": plan.reason,
        "evidence": list(plan.evidence),
        "authority_instrument": plan.authority.instrument,
        "authority_record": plan.authority.record,
        "steps": [{"key": s.key, "statement": s.statement,
                   "depends_on": list(s.depends_on),
                   "requires_delegation": s.requires_delegation}
                  for s in plan.steps],
    }


def save(surface: PlanningSurface, path: Path) -> Path:
    """Write every goal and its full plan chain. Versions only, nothing derived."""
    goals = []
    for goal_key in sorted(surface._goals):                # noqa: SLF001
        goal = surface.goal(goal_key)
        goals.append({
            "key": goal.key,
            "statement": goal.statement,
            "authority_instrument": goal.authority.instrument,
            "authority_record": goal.authority.record,
            "chain": [_plan_payload(p) for p in surface.history(goal_key)],
        })
    path.write_text(json.dumps({"goals": goals}, indent=2), encoding="utf-8")
    return path


def restore(path: Path) -> PlanningSurface:
    """Rebuild a surface, **re-validating every authority citation**.

    The citation is re-constructed rather than trusted, so a plan whose
    instrument no longer resolves does not come back. `DP-01 §3 W5`: memory may
    not *"create, elevate, or infer authority that has not otherwise been
    granted"* — and returning a plan that asserts a vanished source would be
    inferring exactly that.

    The chain is rebuilt in recorded order and supersession is **recomputed**
    from its shape, never read from the file. A stored "is superseded" flag could
    disagree with the chain it describes; a derived one cannot.
    """
    if not path.is_file():
        raise ContinuityError(f"no persisted planning state at {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContinuityError(f"planning state is unreadable: {exc}") from exc

    surface = PlanningSurface()
    for entry in payload.get("goals", []):
        try:
            goal_authority = AuthorityProvenance(
                instrument=entry["authority_instrument"],
                record=entry["authority_record"])
        except Exception as exc:
            raise ContinuityError(
                f"goal {entry.get('key')!r} cites an authority that no longer "
                f"resolves — refusing to restore it: {exc}") from exc
        surface.declare(Goal(key=entry["key"], statement=entry["statement"],
                             authority=goal_authority))

        for index, stored in enumerate(entry.get("chain", [])):
            try:
                authority = AuthorityProvenance(
                    instrument=stored["authority_instrument"],
                    record=stored["authority_record"])
            except Exception as exc:
                raise ContinuityError(
                    f"plan {stored.get('key')!r} cites an authority that no "
                    f"longer resolves — refusing to restore it: {exc}") from exc
            steps = tuple(PlanStep(key=s["key"], statement=s["statement"],
                                   depends_on=tuple(s["depends_on"]),
                                   requires_delegation=s["requires_delegation"])
                          for s in stored["steps"])
            plan = Plan(key=stored["key"], goal_key=stored["goal_key"],
                        steps=steps, authority=authority,
                        origin=PlanOrigin(stored["origin"]),
                        revision=stored["revision"],
                        supersedes=stored["supersedes"],
                        reason=stored["reason"],
                        evidence=tuple(stored["evidence"]))
            if index == 0:
                surface.adopt(plan)
            else:
                # Appended directly: `adapt`/`revise` would author a *new*
                # version, and restoring history must reproduce it rather than
                # continue it. Supersession is still derived from the chain.
                surface._chains[plan.goal_key].append(plan)   # noqa: SLF001
                surface._by_key[plan.key] = plan              # noqa: SLF001
    return surface


def persisted_goals(path: Path) -> Tuple[str, ...]:
    """Goal keys in a saved file, without restoring — inspection is not revival."""
    if not path.is_file():
        return ()
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(sorted(g["key"] for g in payload.get("goals", [])))
