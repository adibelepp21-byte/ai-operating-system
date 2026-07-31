"""
Skill domain model — IMMUTABLE DATA CONTRACTS (Blueprint §9 Skill Package;
skill_spec §1–§11; Domain Model §2/§4/§5/§6/§7; Freeze §4/§5 layer 5;
INV-4/INV-12/INV-15).

Declares the canonical **Skill**. Domain Model §2 [E]: *"A discrete, reusable,
bounded unit of executable ability, invoked by an Agent Instance or Workflow."*

**Not abstract, and not an actor.** skill_spec §2 [E]: *"Be a facility, not an
actor — it authors no independent Trace (INV-4) and holds no external
dependency (INV-12)."* These are frozen dataclasses following the established
Native Core convention (`CapabilityIdentity`, `AgentDefinition`,
`VersionIdentity`). `__post_init__` performs *structural* fail-closed
validation only (PR-4), never domain logic and never authority evaluation.

Contracts declared here:

  - `SkillIdentity` — `(skill_key, skill_version)`. Domain Model §6 [E] lists
    Skill as *"Versioned independently; may evolve as long as the interface is
    preserved."* **No version format is imposed** — no ratified source defines
    one, so the version is an opaque non-empty string.

  - `Skill` — identity plus nothing further. Ownership is **not** a field:
    Domain Model §5 [E] places Skill under *"Owned centrally"*, so there is no
    owning Department to reference. This is the load-bearing difference from
    Capability, which carries `owning_department` because INV-1 requires it.

Deliberately ABSENT, each for a stated reason:

  - **No registry, lookup, or discovery.** skill_spec §14 [O] lists *"Registry
    facility scope"* as an open question and §13 [O] reserves *"Skill registry
    discipline and discovery model ... to later phases and the Architect."*
    Blueprint §9 marks registry/discovery *"Future extension [O] — reserved."*
    Building one would decide a reserved question.
  - **No execution, invocation, or ability body** — no `execute`/`run`/
    `invoke`/`perform`. A Skill *is* executable ability in the model; running
    one is an Agent Instance action (Domain Model §4), not this boundary's.
  - **No Trace authorship.** INV-4 [E]: every Agent Instance action produces
    exactly one Trace record. skill_spec §9 [E]: a Skill's use is accountable
    *"through the invoking Agent-Instance action's Trace ... never a Trace of
    the Skill itself."*
  - **No Tool reference.** Domain Model §4 has `Skill invokes Tool`, but INV-12
    makes Tool the sole holder of an external dependency; modelling that edge
    here is outside this boundary's Objective and is not attempted.
  - **No Workflow composition.** skill_spec §14 [O] leaves
    *"Skill↔Capability/Workflow composition"* unratified (Inferred).

Dependencies: stdlib only. This module imports nothing from Agent, Workflow,
Tool, Runtime, Capability, Governance, Trace, Memory, Knowledge, Optimization,
or Infrastructure. Blueprint §9 [A] states Skill is *"used by agent; composed
in workflow"* — inbound relations held by those boundaries, not dependencies
Skill holds (INV-12; skill_spec §7/§8).
"""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import InvalidSkill


def _require_text(value: object, label: str, error: type) -> None:
    """Fail closed on anything that is not a non-empty string (PR-4)."""
    if not isinstance(value, str) or not value.strip():
        raise error(f"{label} must be a non-empty string")


@dataclass(frozen=True, order=True)
class SkillIdentity:
    """The stable identity of a Skill: its key and its version.

    Frozen, hashable and comparable. Domain Model §6 versions Skill
    independently; no version scheme is imposed, because none is ratified."""

    skill_key: str
    skill_version: str

    def __post_init__(self) -> None:
        _require_text(self.skill_key, "skill_key", InvalidSkill)
        _require_text(self.skill_version, "skill_version", InvalidSkill)


@dataclass(frozen=True)
class Skill:
    """A reusable, bounded unit of executable ability.

    Owned centrally (Domain Model §5) — deliberately carries no owner
    reference, because no Department owns a Skill. Descriptive only: it holds
    no ability body, authors no Trace (INV-4), and holds no external
    dependency (INV-12)."""

    identity: SkillIdentity

    def __post_init__(self) -> None:
        if not isinstance(self.identity, SkillIdentity):
            raise InvalidSkill("identity must be a SkillIdentity")
