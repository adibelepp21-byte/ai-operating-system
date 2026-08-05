"""
Workflow coordination — the INV-13 enforcement point (Domain Model §4/§7
invariant 13; Freeze §4/§6, AD-9; workflow_spec §1/§2/§5/§10/§11).

This is the module Baseline 02 exists for. workflow_spec §1 [E]: *"Workflow is
the governed composition and the **sole sanctioned channel** for multi-agent
coordination (Freeze INV-13)."*

  - **INV-13** [E]: *"No Agent Instance may collaborate directly with another
    Agent Instance outside of a shared Workflow, Knowledge, or scoped Memory."*
  - Freeze §6 [E] records the rule as a direction: `Workflow coordinates
    Instances` is allowed; **`direct Instance↔Instance` is forbidden**.
  - Domain Model §9 [E] closes the escape hatch: *"**Message / Event** as an
    entity for Agent-to-Agent communication — collaboration is required to
    route through Workflow, Knowledge, or scoped Memory; **no direct channel
    exists**."*
  - Freeze AD-9 [A]: free agent-to-agent delegation is a **rejected
    anti-pattern**, named by Roadmap §9.8 as this boundary's principal risk.

**How INV-13 is enforced structurally.** Three properties together, none of
which is a runtime check that could be bypassed:

  1. **No peer field exists.** `AgentInstanceRef` (composition) carries a key
     and nothing else — no target, peer, recipient, or channel. One Agent
     Instance cannot name another anywhere in this package.
  2. **Coordination requires a Workflow.** `WorkflowCoordination` cannot be
     constructed without one. There is no two-instance constructor, and no
     function in this package accepts a pair of instances.
  3. **Participation is derived, never declared.** Participants are read *from
     the composition's steps*. A participant set cannot be supplied
     independently of the Workflow that produced it, so there is no way to
     assert that two instances collaborate outside one.

The residual runtime guard — `DirectCollaborationForbidden` — covers the one
case the type system cannot: a caller passing something that is not a Workflow
where a Workflow is required. Structure first, exception second.

**What this boundary does not own.** INV-13 sanctions three channels; this
boundary owns exactly one. Knowledge and scoped Memory are owned by
`core/knowledge/` and `core/memory/`, are governed by INV-7/INV-8, and are not
reachable from here. Domain Model §4 [E] notes that *"a transient, pairwise
coordination need is satisfiable as a Memory scoped to that pair — this does not
require a new entity"*; that path runs through Memory, not through this module.

Deliberately ABSENT: no message, event, channel, queue, mailbox, transport,
broadcast, subscription, delegation, handoff, or routing of any kind. No
execution (workflow_spec §8: *"Is not the Runtime"*). No Trace authorship
(INV-4). No external dependency (INV-12).

Dependencies: stdlib only, plus this package's own models, composition, and
exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .composition import AgentInstanceRef, WorkflowComposition
from .exceptions import DirectCollaborationForbidden, InvalidWorkflowComposition
from .models import Workflow


@dataclass(frozen=True)
class WorkflowCoordination:
    """Coordination of Agent Instances, bound to exactly one Workflow.

    The binding is the point: INV-13 permits coordination *through* a Workflow
    and forbids it outside one, so this contract cannot exist without naming
    the Workflow that sanctions it.

    A coordination with an empty composition is structurally valid — it
    coordinates no one — and is reported by `is_empty()`, never raised on."""

    workflow: Workflow
    composition: WorkflowComposition

    def __post_init__(self) -> None:
        if not isinstance(self.workflow, Workflow):
            raise DirectCollaborationForbidden(
                "coordination requires a Workflow — INV-13 permits Agent-Instance "
                "collaboration only through a shared Workflow, Knowledge, or "
                "scoped Memory, and this boundary owns only the Workflow channel"
            )
        if not isinstance(self.composition, WorkflowComposition):
            raise InvalidWorkflowComposition(
                "composition must be a WorkflowComposition"
            )

    # -- INV-13: participation is derived from the Workflow ---------------

    def is_empty(self) -> bool:
        """Whether this coordination involves no Agent Instance."""
        return self.composition.is_empty()

    def participants(self) -> Tuple[AgentInstanceRef, ...]:
        """Every Agent Instance coordinated, de-duplicated, in first-step order.

        Derived from the composition's steps, never supplied independently —
        which is why a participant set cannot describe collaboration outside a
        Workflow."""
        seen = set()
        ordered = []
        for instance in self.composition.acting_instances():
            if instance.agent_instance_key not in seen:
                seen.add(instance.agent_instance_key)
                ordered.append(instance)
        return tuple(ordered)

    def is_multi_agent(self) -> bool:
        """Whether more than one Agent Instance participates.

        Reported, never acted on (PR-3). A multi-agent coordination is legal
        precisely because it is expressed through this Workflow."""
        return len(self.participants()) > 1

    def coordinates(self, agent_instance_key: str) -> bool:
        """Whether the named Agent Instance participates in this Workflow.

        Answers the INV-13 question — *is this collaboration sanctioned?* —
        for one participant. It grants nothing and decides nothing; the
        Governance boundary owns authority (PR-3)."""
        return any(
            instance.agent_instance_key == agent_instance_key
            for instance in self.participants()
        )
