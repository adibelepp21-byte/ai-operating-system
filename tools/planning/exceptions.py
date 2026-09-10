"""Planning failures. **Fail closed** (`PR-4`).

Every one of these is raised rather than returned. That is deliberate and is the
opposite of the choice made in `tools/delegation_catalog.py`, which *reports*
defects because it is a detector and `PR-3` is detect-don't-decide.

The distinction: a **detector** that raises hides findings, so it returns them. A
**mutation** that would exceed authority must not complete, so it raises. Letting
`adapt()` return an error object and continue would leave the caller holding a
plan that had already changed — which is how silent authority expansion happens.
"""

from __future__ import annotations


class PlanningError(RuntimeError):
    """Base for every planning failure."""


class InvalidGoal(PlanningError):
    """A Goal that cannot stand — no statement, or no resolvable authority."""


class InvalidPlan(PlanningError):
    """A Plan that cannot stand — unknown goal, duplicate steps, bad chain."""


class UnsequenceablePlan(PlanningError):
    """Dependencies form a cycle, or name a step that does not exist.

    Reported as a failure rather than resolved by picking an order. Choosing one
    would be inventing an ordering the author never declared, which is the
    reserved prioritization frontier entered through the back door.
    """


class EscalationRequired(PlanningError):
    """The change would need authority the plan does not hold.

    `ACT-CC-P11-005 §15`: *"the system must escalate rather than silently
    expand"*, and the correct behaviour is ``DETECT → CLASSIFY → ESCALATE``, not
    ``DETECT → SELF-AUTHORIZE``.

    Carries the classification so the escalation names what is missing. An
    escalation that says only *"denied"* gives the human nothing to decide with.

    **Raising this is not an approval request that can time out into consent.**
    `SILENCE ≠ APPROVAL`.
    """

    def __init__(self, message: str, *, required: str, held: str):
        super().__init__(message)
        self.required = required
        self.held = held
