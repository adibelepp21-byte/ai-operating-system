"""
Workflow declaration — the Agent-Definition-to-Workflow relation (Domain Model
§4; §7 invariant 15; workflow_spec §3; ADR-0007; ADR-0004).

Domain Model §4 [E]: *"Agent Definition **specifies** Skill, Workflow (what it
is permitted/required to use)."* workflow_spec §3 [A] repeats the cardinality:
composition structure is *"declared by Agent Definitions (0+ per Definition,
INV-15)"*. This module models that declaration and the one invariant governing
it.

  - **INV-15** [E]: *"An Agent Definition may specify zero or more Skills and
    zero or more Workflows. An empty Skill declaration, an empty Workflow
    declaration, or both empty declarations represent a valid architectural
    state. No minimum cardinality is required for either relationship."*
    Resolved by **ADR-0007**, whose decision text is explicit that this rests
    on operational evidence: *"the Governance Artifact Integrity Agent,
    functioning with zero Skills and zero Workflows, its authorization carried
    entirely by its independently-mandatory Behavior and Permissions field."*
    `WorkflowDeclaration` therefore accepts an empty declaration and **never**
    raises on one.

  - **PR-4 / fail closed** — workflow_spec §11 [E]: a Workflow *"halts rather
    than proceeds"* on an unmet precondition. `resolve()` raises
    `UnresolvedWorkflow`; it returns no default, retries nothing, and falls
    back to nothing.

**Declaration confers no ownership.** ADR-0004 [E] is explicit: *"That Agent
Definition specifies Workflow (§4) does not imply shared ownership between the
two entities — specification and ownership are separate concerns in the Domain
Model, exactly as Agent Definition's specifies relationship to Skill does not
make Skill Department-owned either."* Workflow remains owned centrally
regardless of which Definitions declare it.

`AgentDefinitionRef` carries an opaque key and nothing more. This module imports
**nothing** from `core.agent`: Agent depends on Workflow, never the reverse.
Holding an opaque reference keeps the declaration modellable without inverting
that edge. The same stub pattern is used by `core/skill/`'s
`AgentDefinitionRef` and `core/capability/`'s `DepartmentRef`.

Deliberately ABSENT: no registry, lookup index, or discovery mechanism.
`resolve()` searches only the declaration it was given — a declared set, not a
system-wide catalogue. Also absent: execution, Trace authorship (INV-4),
persistence, mutation, and any external dependency (INV-12).

Dependencies: stdlib only, plus this package's own models and exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from .exceptions import (
    DuplicateWorkflowDeclaration,
    InvalidWorkflowDeclaration,
    UnresolvedWorkflow,
)
from .models import WorkflowIdentity


@dataclass(frozen=True)
class AgentDefinitionRef:
    """Reference to the Agent Definition that declares a set of Workflows.

    A stub carrying only the reference the declaration needs. It models no
    Agent Definition behaviour, version lineage, or ownership — those belong
    to `core/agent/`, and this boundary does not import it."""

    agent_definition_key: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.agent_definition_key, str)
            or not self.agent_definition_key.strip()
        ):
            raise InvalidWorkflowDeclaration(
                "agent_definition_key must be a non-empty string"
            )


@dataclass(frozen=True)
class WorkflowDeclaration:
    """The Workflows one Agent Definition specifies it is permitted to use.

    Per INV-15 and ADR-0007, `workflows` may be empty — that is a valid
    architectural state, not an incomplete one. Construction validates
    structure only: every entry must be a `WorkflowIdentity`, and no
    `workflow_key` may repeat, since a repeated key makes the declared set
    ambiguous."""

    declared_by: AgentDefinitionRef
    workflows: Tuple[WorkflowIdentity, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.declared_by, AgentDefinitionRef):
            raise InvalidWorkflowDeclaration(
                "declared_by must be an AgentDefinitionRef"
            )
        if not isinstance(self.workflows, tuple):
            raise InvalidWorkflowDeclaration("workflows must be a tuple")

        seen = set()
        for entry in self.workflows:
            if not isinstance(entry, WorkflowIdentity):
                raise InvalidWorkflowDeclaration(
                    "every declared workflow must be a WorkflowIdentity"
                )
            if entry.workflow_key in seen:
                raise DuplicateWorkflowDeclaration(
                    f"workflow_key declared more than once: {entry.workflow_key!r}"
                )
            seen.add(entry.workflow_key)

    # -- INV-15 / ADR-0007: zero is valid ---------------------------------

    def is_empty(self) -> bool:
        """Whether this Agent Definition declares no Workflow.

        A true result is a **valid architectural state** (INV-15; ADR-0007),
        reported so callers can observe it — never treated as an error here."""
        return len(self.workflows) == 0

    def declared(self) -> Tuple[WorkflowIdentity, ...]:
        """Every Workflow this Agent Definition declares, in declaration order."""
        return self.workflows

    # -- PR-4: fail closed ------------------------------------------------

    def resolve(self, workflow_key: str) -> WorkflowIdentity:
        """The declared `WorkflowIdentity` for `workflow_key`, or fail closed.

        workflow_spec §11 [E]: an unmet precondition halts the Workflow rather
        than proceeding. Raises `UnresolvedWorkflow` — it returns no default
        and substitutes nothing.

        This searches **only this declaration**. It is not a registry: no
        system-wide lookup exists in this boundary."""
        for entry in self.workflows:
            if entry.workflow_key == workflow_key:
                return entry
        raise UnresolvedWorkflow(
            f"{self.declared_by.agent_definition_key!r} declares no workflow "
            f"named {workflow_key!r} (workflow_spec §11: fail closed, PR-4)"
        )
