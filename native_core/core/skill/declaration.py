"""
Skill declaration — the Agent-Definition-to-Skill relation (Domain Model §4;
§7 invariant 15; skill_spec §1/§7/§11; ADR-0007).

Domain Model §4 [E]: *"Agent Definition **specifies** Skill, Workflow (what it
is permitted/required to use)."* This module models that declaration and the
one invariant governing its cardinality.

  - **INV-15** [E]: *"An Agent Definition may specify zero or more Skills and
    zero or more Workflows. An empty Skill declaration ... represent[s] a valid
    architectural state. No minimum cardinality is required."* Resolved by
    [ADR-0007]. `SkillDeclaration` therefore accepts an empty declaration and
    **never** raises on one — a minimum would be an invented constraint.

  - **PR-4 / fail closed** — skill_spec §11 [E]: *"a Skill that cannot be
    resolved/used causes the invoking action to halt accountably, not to
    proceed silently."* `resolve()` raises `UnresolvedSkill`; it returns no
    default, retries nothing, and falls back to nothing.

`AgentDefinitionRef` carries an opaque key and nothing more. This module
imports **nothing** from `core.agent`: Blueprint §9 [A] fixes the direction as
*"used by agent"* — Agent depends on Skill, never the reverse. Holding an
opaque reference keeps the declaration modellable without inverting that edge.
The same stub pattern is used by `core/capability/`'s `DepartmentRef`.

Deliberately ABSENT: no registry, lookup index, or discovery mechanism.
`resolve()` searches only the declaration it was given — a declared set, not a
system-wide catalogue. skill_spec §13/§14 [O] reserve registry discipline and
registry facility scope to the Architect; Blueprint §9 [O] marks
registry/discovery a reserved future extension. Also absent: execution,
Workflow composition (skill_spec §14 [O], Inferred), Tool reference, Trace
authorship (INV-4), persistence, mutation, and any external dependency
(INV-12).

Dependencies: stdlib only, plus this package's own models and exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

from .exceptions import (
    DuplicateSkillDeclaration,
    InvalidSkillDeclaration,
    UnresolvedSkill,
)
from .models import SkillIdentity


@dataclass(frozen=True)
class AgentDefinitionRef:
    """Reference to the Agent Definition that declares a set of Skills.

    A stub carrying only the reference the declaration needs. It models no
    Agent Definition behaviour, version lineage, or ownership — those belong
    to `core/agent/`, and this boundary does not import it."""

    agent_definition_key: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.agent_definition_key, str)
            or not self.agent_definition_key.strip()
        ):
            raise InvalidSkillDeclaration(
                "agent_definition_key must be a non-empty string"
            )


@dataclass(frozen=True)
class SkillDeclaration:
    """The Skills one Agent Definition specifies it is permitted to use.

    Per INV-15 and ADR-0007, `skills` may be empty — that is a valid
    architectural state, not an incomplete one. Construction validates
    structure only: every entry must be a `SkillIdentity`, and no `skill_key`
    may repeat, since a repeated key makes the declared set ambiguous."""

    declared_by: AgentDefinitionRef
    skills: Tuple[SkillIdentity, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.declared_by, AgentDefinitionRef):
            raise InvalidSkillDeclaration(
                "declared_by must be an AgentDefinitionRef"
            )
        if not isinstance(self.skills, tuple):
            raise InvalidSkillDeclaration("skills must be a tuple")

        seen = set()
        for entry in self.skills:
            if not isinstance(entry, SkillIdentity):
                raise InvalidSkillDeclaration(
                    "every declared skill must be a SkillIdentity"
                )
            if entry.skill_key in seen:
                raise DuplicateSkillDeclaration(
                    f"skill_key declared more than once: {entry.skill_key!r}"
                )
            seen.add(entry.skill_key)

    # -- INV-15: zero is valid -------------------------------------------

    def is_empty(self) -> bool:
        """Whether this Agent Definition declares no Skill.

        A true result is a **valid architectural state** (INV-15; ADR-0007),
        reported so callers can observe it — never treated as an error here."""
        return len(self.skills) == 0

    def declared(self) -> Tuple[SkillIdentity, ...]:
        """Every Skill this Agent Definition declares, in declaration order."""
        return self.skills

    # -- PR-4: fail closed ----------------------------------------------

    def resolve(self, skill_key: str) -> SkillIdentity:
        """The declared `SkillIdentity` for `skill_key`, or fail closed.

        skill_spec §11 [E]: an unresolvable Skill halts the invoking action
        accountably. Raises `UnresolvedSkill` — it returns no default and
        substitutes nothing.

        This searches **only this declaration**. It is not a registry: no
        system-wide lookup exists in this boundary, because registry scope is
        reserved (skill_spec §13/§14 [O]; Blueprint §9 [O])."""
        for entry in self.skills:
            if entry.skill_key == skill_key:
                return entry
        raise UnresolvedSkill(
            f"{self.declared_by.agent_definition_key!r} declares no skill "
            f"named {skill_key!r} (skill_spec §11: fail closed, PR-4)"
        )
