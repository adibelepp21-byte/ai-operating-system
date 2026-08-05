"""
Workflow composition — the ordered, inspectable step structure (Domain Model
§2/§4; workflow_spec §2/§5/§6/§9/§11; INV-4; Freeze §5 layer 6).

Domain Model §2 [E] defines a Workflow as *"an **explicit, inspectable**
composition of Skills (and possibly Agent Instance invocations) accomplishing a
multi-step outcome."* This module realizes that structure and the one invariant
that governs every step.

  - **INV-4** [E]: *"Every Agent Instance action produces exactly one Trace
    record — production is unconditional, never optional."* workflow_spec §9
    [E]: *"Each coordinated step is an Agent-Instance action producing exactly
    one Trace record."*

    **Enforced structurally, not by a flag.** A `WorkflowStep` requires the
    Agent Instance that performs it. A step naming no actor is not a step that
    silently skips Trace — it is not an action at all, and construction fails
    closed (`InvalidWorkflowStep`). There is no way to express an untraceable
    step, which is what "structurally enforced" means here: the absence is not
    checked, it is unrepresentable.

  - **Inspectability** — workflow_spec §6 [A]: *"Sequence/branch composition;
    validate that coordination stays within INV-13 and that each step is
    Trace-producing; **keep composition checkable**."* Steps are ordered, each
    step key is unique, and both the sequence and its participants are readable
    without executing anything.

`SkillRef` and `AgentInstanceRef` are opaque stubs carrying only a key. This
module imports **nothing** from `core.skill` or `core.agent`. workflow_spec §7
[E] does permit depending on Skill (*"composes Skills"*), so the import would
be admissible; the stub is chosen instead to match the pattern already
established by `core/capability/`'s `DepartmentRef` and `core/skill/`'s
`AgentDefinitionRef`, which keeps each boundary independently constructible and
its dependency sweep unambiguous.

Deliberately ABSENT: no execution, scheduling, dispatch, retry, branching
semantics beyond declared order, timeout, parallelism, or compensation.
workflow_spec §13/§14 [O] reserve the failure-recovery model; §12 [O] reserves
compile-time composition validation. Also absent: Trace authorship (INV-4),
persistence, mutation, registry, and any external dependency (INV-12).

Dependencies: stdlib only, plus this package's own exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from .exceptions import (
    InvalidWorkflowComposition,
    InvalidWorkflowStep,
)


@dataclass(frozen=True)
class SkillRef:
    """Reference to a Skill composed by a step.

    A stub carrying only the reference the composition needs. It models no
    Skill behaviour, version lineage, or ability — those belong to
    `core/skill/`, and this boundary does not import it."""

    skill_key: str

    def __post_init__(self) -> None:
        if not isinstance(self.skill_key, str) or not self.skill_key.strip():
            raise InvalidWorkflowStep("skill_key must be a non-empty string")


@dataclass(frozen=True)
class AgentInstanceRef:
    """Reference to the Agent Instance that performs a step.

    Required on every step: INV-4 makes the Trace an Agent-Instance action's
    product, so a step without an actor could produce none.

    Deliberately carries **no peer, target, channel, or recipient field**. INV-13
    forbids direct Instance-to-Instance collaboration, and Freeze §6 records the
    forbidden direction as *"direct Instance↔Instance"*. The absence of any such
    field is the structural enforcement: this boundary offers no type in which
    one Agent Instance can name another."""

    agent_instance_key: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.agent_instance_key, str)
            or not self.agent_instance_key.strip()
        ):
            raise InvalidWorkflowStep("agent_instance_key must be a non-empty string")


@dataclass(frozen=True)
class WorkflowStep:
    """One step of a composition: an Agent-Instance action composing a Skill.

    Both fields are required. `performed_by` is required by INV-4 — every step
    is an action, and every action produces exactly one Trace. `composes` is
    required by Domain Model §4's *Workflow contains Skill*.

    The step declares *what* is composed and *who* acts. It declares nothing
    about how the action runs, when it runs, or what it returns — that is
    Runtime's concern (workflow_spec §8)."""

    step_key: str
    performed_by: AgentInstanceRef
    composes: SkillRef

    def __post_init__(self) -> None:
        if not isinstance(self.step_key, str) or not self.step_key.strip():
            raise InvalidWorkflowStep("step_key must be a non-empty string")
        if not isinstance(self.performed_by, AgentInstanceRef):
            raise InvalidWorkflowStep(
                "performed_by must be an AgentInstanceRef — a step with no acting "
                "Agent Instance could produce no Trace (INV-4)"
            )
        if not isinstance(self.composes, SkillRef):
            raise InvalidWorkflowStep("composes must be a SkillRef")


@dataclass(frozen=True)
class WorkflowComposition:
    """The ordered steps of one Workflow — explicit and inspectable.

    Construction validates structure only: every entry must be a
    `WorkflowStep`, and no `step_key` may repeat, since a repeated key makes the
    sequence ambiguous. An empty composition is structurally valid and is
    reported by `is_empty()`, never raised on — no ratified source imposes a
    minimum step count."""

    steps: Tuple[WorkflowStep, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.steps, tuple):
            raise InvalidWorkflowComposition("steps must be a tuple")

        seen = set()
        for entry in self.steps:
            if not isinstance(entry, WorkflowStep):
                raise InvalidWorkflowComposition("every step must be a WorkflowStep")
            if entry.step_key in seen:
                raise InvalidWorkflowComposition(
                    f"step_key declared more than once: {entry.step_key!r}"
                )
            seen.add(entry.step_key)

    # -- inspectability (workflow_spec §6) --------------------------------

    def is_empty(self) -> bool:
        """Whether this composition declares no step."""
        return len(self.steps) == 0

    def ordered(self) -> Tuple[WorkflowStep, ...]:
        """Every step, in declaration order. The order *is* the sequence."""
        return self.steps

    def step_keys(self) -> Tuple[str, ...]:
        """The step keys, in declaration order — readable without executing."""
        return tuple(step.step_key for step in self.steps)

    def composed_skills(self) -> Tuple[SkillRef, ...]:
        """Every Skill this composition contains, in step order.

        Domain Model §4: *Workflow contains Skill*. Duplicates are preserved —
        the same Skill may legitimately be composed at more than one step."""
        return tuple(step.composes for step in self.steps)

    # -- INV-4: every step is a Trace-producing action ---------------------

    def acting_instances(self) -> Tuple[AgentInstanceRef, ...]:
        """The Agent Instance acting at each step, in step order.

        Each is the author of exactly one Trace for that step (INV-4). The
        Workflow authors none of its own (workflow_spec §9)."""
        return tuple(step.performed_by for step in self.steps)
