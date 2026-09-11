"""`P11-W1` — the authorized `PLAN → WORKFLOW` handoff.

**This module exists because a hypothesis of mine was falsified.**

`ACT-CC-P11-007` reported `PLAN → WORKFLOW` as `AUTHORIZED + BLOCKED`, requiring
a *"unit-level delegator"*. `ACT-CC-P11-010` put that to evidence, and it does not
survive:

* the phrase appears in **no canonical instrument** — not `DP-03`, not `DP-04`,
  not `DP-01`, not `FD-P11-001`. It appears only in three documents, all mine;
* `WorkflowStep` requires ``performed_by: AgentInstanceRef`` and
  ``composes: SkillRef`` — **an actor and a skill, no delegating unit of any
  kind**;
* the resident workflow records already name their actor in exactly those terms:
  *"invoked by an Agent Instance of the Governance Artifact Integrity Agent"*.

What was actually missing was an **Agent Instance** — of which there were zero
until `FD-P11-001 §7` authorized creating one. My reasoning had a hidden step:
naming an actor *is* an allocation of work, so it needs a delegator — **and the
delegator must be a unit.** The first half is sound; the second was assumption,
and `FD-P11-001 §4.1` established a delegator that is not a unit.

**`TRANSLATION ≠ AUTHORIZATION`** (`§18`). Every field of the `WorkflowStep`
produced here is copied from something already authorized elsewhere:

    step_key      ← the Plan, via WorkPreparation
    performed_by  ← the recipient of an ACTIVE W4 Delegation
    composes      ← a Skill the recipient's Agent Definition already permits

Nothing is chosen, defaulted, or invented. If any of those is absent the handoff
**refuses**; it never fills a gap. That is what keeps this an adapter rather than
an authority: it can express a delegation that exists and cannot manufacture one
that does not.

**The governing invariant** (`§24`, `§25`) is *not* *"no handoff because no unit
delegator exists"* — an absence-of-authority premise of the kind
`ACT-CC-P11-009` found rotting in eight of my controls. It is:

    NO HANDOFF UNLESS VALID AUTHORITY PROVENANCE EXISTS

which is what every refusal below actually tests.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

from native_core.core.workflow import (
    AgentInstanceRef,
    SkillRef,
    WorkflowComposition,
    WorkflowStep,
)
from tools.agent_instance_registry import REGISTERED, AgentInstanceRegistry
from tools.planning import WorkPreparation
from tools.w4_delegation import W4Delegation

REPO_ROOT = Path(__file__).resolve().parent.parent
ORGANIZATION = REPO_ROOT / "docs/architecture/organization"

#: A permitted-skill line in an Agent Definition record, e.g.
#: ``[`skill.staleness-detection`](../../execution-catalog/skill/…)``.
PERMITTED_SKILL = re.compile(r"`skill\.([a-z0-9-]+)`")


class HandoffRefused(RuntimeError):
    """The handoff is not covered by authority that already exists.

    Raised — never returned — because a refusal that a caller can ignore is a
    handoff that happens anyway. Fail closed (`PR-4`).
    """

    def __init__(self, message: str, *, reason: str):
        super().__init__(message)
        self.reason = reason


def permitted_skills(definition_key: str,
                     root: Path = ORGANIZATION) -> Tuple[str, ...]:
    """Skills an Agent Definition **already permits**, read from its record.

    Read rather than configured. `§18`: an adapter that could be told which
    skills to allow would be granting them.
    """
    for path in sorted(root.rglob(f"agent-definitions/{definition_key}.md")):
        section = path.read_text(encoding="utf-8")
        start = section.find("## Permitted Skills")
        if start == -1:
            return ()
        end = section.find("## Permitted Workflows", start)
        return tuple(sorted(set(PERMITTED_SKILL.findall(
            section[start:end if end != -1 else None]))))
    return ()


def authorize_handoff(preparation: WorkPreparation, *,
                      delegation: W4Delegation,
                      registry: AgentInstanceRegistry,
                      skill_key: str,
                      organization_root: Path = ORGANIZATION) -> WorkflowStep:
    """Express one prepared plan step as a `WorkflowStep`, or refuse.

    Every check below rejects a *different* way the handoff could occur without
    authority. None of them is about a delegating unit.
    """
    if not isinstance(preparation, WorkPreparation):
        raise HandoffRefused(
            "only work prepared by the Planning surface may be handed off",
            reason="not-prepared-work")
    if not isinstance(delegation, W4Delegation):
        raise HandoffRefused(
            "a handoff requires an issued W4 Delegation — `§24`: no handoff "
            "unless valid authority provenance exists",
            reason="no-delegation")
    if not delegation.is_executable():
        raise HandoffRefused(
            f"delegation {delegation.delegation_id!r} is {delegation.status}; "
            "a withdrawn grant authorizes nothing",
            reason="delegation-not-executable")
    if preparation.step_key not in delegation.work_scope:
        raise HandoffRefused(
            f"step {preparation.step_key!r} is outside the delegated work "
            f"scope {delegation.work_scope}",
            reason="step-outside-scope")

    instance_key = delegation.recipient_instance
    if not registry.is_registered(instance_key):
        raise HandoffRefused(
            f"{instance_key!r} is not a registered Agent Instance — "
            "`FD-P11-001 §6.1`: an Agent Definition alone is insufficient",
            reason="instance-not-registered")
    registration = registry.get(instance_key)
    if registration.lifecycle != REGISTERED:
        raise HandoffRefused(
            f"instance {instance_key!r} is {registration.lifecycle}",
            reason="instance-not-live")

    # The Skill must already be permitted by the *Definition*, and the
    # Capability it serves must be inside the delegation. Two independent
    # facts, neither supplied by the caller's intent.
    allowed = permitted_skills(registration.definition_key, organization_root)
    if skill_key not in allowed:
        raise HandoffRefused(
            f"{registration.definition_key!r} does not permit "
            f"skill.{skill_key} — permitted: {allowed or '(none)'}",
            reason="skill-not-permitted")
    for capability in registration.permitted_capabilities:
        if capability in delegation.capability_scope:
            break
    else:
        raise HandoffRefused(
            "the delegation covers no capability this instance holds",
            reason="capability-not-delegated")

    return WorkflowStep(step_key=preparation.step_key,
                        performed_by=AgentInstanceRef(instance_key),
                        composes=SkillRef(skill_key))


def compose(preparations, *, delegation: W4Delegation,
            registry: AgentInstanceRegistry, skill_for: Dict[str, str],
            organization_root: Path = ORGANIZATION) -> WorkflowComposition:
    """Compose prepared steps into a Workflow, in the order Planning sequenced.

    Order is preserved from `prepare_for_workflow`, which preserved it from
    `sequence()`, which derived it from declared dependencies. **Nothing here
    re-orders anything** — that would be the reserved prioritization frontier
    entering through coordination.
    """
    steps = tuple(
        authorize_handoff(preparation, delegation=delegation, registry=registry,
                          skill_key=skill_for[preparation.step_key],
                          organization_root=organization_root)
        for preparation in preparations)
    return WorkflowComposition(steps=steps)
