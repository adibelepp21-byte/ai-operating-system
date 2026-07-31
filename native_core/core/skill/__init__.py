"""
Skill boundary (Native Core Blueprint §3 root tree, §9 Skill Package;
skill_spec; Domain Model §1/§2/§4/§5/§6/§7; Freeze §5 layer 5;
INV-4/INV-12/INV-15).

Skill is one of the **eleven frozen subsystem boundaries** — Blueprint §3 fixes
the tree as `core/{trace, memory, knowledge, governance, runtime, agent,
capability, skill, workflow, infrastructure, optimization}`, and §4 states the
core region *"contains exactly the eleven frozen subsystem boundaries — no
more."* No entity and no subsystem is introduced here.

Domain Model §2 [E]: a Skill is *"a discrete, reusable, bounded unit of
executable ability, invoked by an Agent Instance or Workflow."* skill_spec §2
[E] fixes its character: *"Be a facility, not an actor — it authors no
independent Trace (INV-4) and holds no external dependency (INV-12)."*

What this boundary realizes, per skill_spec §1/§2/§11 and Roadmap §9.7:

    Skill             —is—        a reusable unit of ability, owned centrally
    Agent Definition  —declares→  zero or more Skills            (INV-15)
    unresolved Skill  —halts→     the invoking action, closed    (PR-4)

Public surface:
  - models:       SkillIdentity · Skill
  - declaration:  AgentDefinitionRef · SkillDeclaration
  - exceptions:   SkillError · InvalidSkill · InvalidSkillDeclaration ·
                  UnresolvedSkill · DuplicateSkillDeclaration

NOT implemented here, and reserved by the frozen architecture:
  - **Registry and discovery** — skill_spec §13 [O] reserves *"Skill registry
    discipline and discovery model ... to later phases and the Architect"*, and
    §14 [O] lists *"Registry facility scope"* as an open question. Blueprint §9
    marks registry/discovery a reserved future extension. `SkillDeclaration.
    resolve()` searches only the declaration it is given; there is no
    system-wide catalogue, index, or lookup facility in this package.
  - **Execution of any kind** — no `execute`/`run`/`invoke`/`perform`. A Skill
    *is* executable ability in the model; running one is an Agent Instance
    action (Domain Model §4), and not this boundary's responsibility.
  - **Trace authorship** — INV-4 gives each Agent Instance action exactly one
    Trace; skill_spec §9 [E] makes a Skill's use accountable *"through the
    invoking Agent-Instance action's Trace ... never a Trace of the Skill
    itself."*
  - **Tool reference** — Domain Model §4 carries `Skill invokes Tool`, but
    INV-12 makes Tool the sole holder of an external dependency; that edge is
    outside this Objective and is not modelled.
  - **Skill↔Capability/Workflow composition** — skill_spec §14 [O] leaves it
    unratified (Inferred). Not modelled.
  - **Skill instances** — none is created here. This package models the entity
    type only, exactly as `core/capability/` does.

Ownership: this boundary owns **only the Skill contract and the Agent-Definition
Skill declaration**. Domain Model §5 [E] places Skill under *"Owned
centrally"*, so a Skill carries no owning Department — the load-bearing
difference from Capability. Agent owns definition and instance identity ·
Workflow owns composition · Tool owns external boundaries · Runtime owns
hosting · Governance owns authority · Trace owns history · Infrastructure owns
facilities. No ownership transfer.

Dependencies: stdlib only. This package imports nothing from Agent, Workflow,
Tool, Runtime, Capability, Governance, Trace, Memory, Knowledge, Optimization
or Infrastructure, and holds no external dependency (INV-12; skill_spec
§7/§8). Blueprint §9 [A] describes Skill as *"used by agent; composed in
workflow"* — inbound relations held by those boundaries, never dependencies
Skill itself holds.
"""

from .declaration import AgentDefinitionRef, SkillDeclaration
from .exceptions import (
    DuplicateSkillDeclaration,
    InvalidSkill,
    InvalidSkillDeclaration,
    SkillError,
    UnresolvedSkill,
)
from .models import Skill, SkillIdentity

__all__ = [
    "AgentDefinitionRef",
    "DuplicateSkillDeclaration",
    "InvalidSkill",
    "InvalidSkillDeclaration",
    "Skill",
    "SkillDeclaration",
    "SkillError",
    "SkillIdentity",
    "UnresolvedSkill",
]
