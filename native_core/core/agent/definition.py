"""
Agent Definition contract — IMMUTABLE DATA CONTRACT (Blueprint §8 Agent Package;
agent_spec §1/§3/§4; Freeze INV-2/INV-3; Domain Model §2.1/§5/§6).

Declares the canonical **Agent Definition**: the governed, persistent *template*
of an Agent. It answers exactly one question:

    "What kind of Agent is this?"

It does **not** answer "which Agent instance is running?" — that belongs to the
future Agent Instance layer (agent_spec §14 leaves Instance identity/attribution
[O] open). It is not a runtime actor, it does not execute, and it does not
participate in Runtime execution: only an Agent Instance acts (Blueprint §8;
agent_spec §1).

**Not abstract.** Blueprint requires no abstraction here — a Definition is
descriptive, so this is an immutable data contract with no behavior, following
the established Native Core convention for frozen data contracts
(`VersionIdentity`, `RuntimeContext`, `ExecutionContext`). `__post_init__`
performs *structural* fail-closed validation only (PR-4), never domain logic.

Fields — each added only on direct evidence, none invented:
  - `agent_definition_version` — the **ratified frozen field name**: one of
    Trace's ten required contents (Domain Model §2.1), recording which
    Definition version acted. Named identically to avoid any terminology drift.
  - `owning_department_key` — the Department that owns this Definition. **[E]
    Ratified owned data**, stated by three canonical sources and reserved by
    none: `agent_spec §3 Owned Data` — *"Agent Definitions owned by exactly one
    Department (INV-2)"*; Freeze §4's Agent Definition entry — *"Ownership:
    exactly one Department"*; and Domain Model §5's Ownership Rules table —
    `Agent Definition → Exactly one Platform Division` (*"Historical alias:
    Department"*, ADR-0010). Held as a **plain key**, not as a reference object,
    so that no import of the Capability boundary is taken (see *Dependencies*).
    Required, because INV-2 admits no unowned Definition and PR-4 fails closed.
  - `implemented_capabilities` — the Capabilities this Definition implements.
    **[E] INV-2 clause 2**: *"…and implements **at least one Capability**."*
    Corroborated by `agent_spec §2` — *"An Agent Definition implements ≥1
    Capability (INV-2)"* — and by Freeze §4's Capability entry, which lists
    *"be implemented by Agent Definitions"* among a Capability's allowed
    relations. **At least one**, so an empty tuple fails closed; distinct keys,
    since implementing the same Capability twice is not implementing two.
    Plain keys again, for the same dependency reason.
  - `specified_skills`, `specified_workflows` — what this Definition is
    permitted to use. **[E] INV-15**: *"An Agent Definition may specify zero or
    more Skills and zero or more Workflows … **No minimum cardinality is
    required** for either relationship."* Resolved by **ADR-0007**. Domain Model
    §2 [E] names them among what an Agent Definition carries — *"which
    Capabilities it implements, which Platform Division owns it, **what
    behavior/permissions/Skills/Workflows it is allowed to use**"* — and
    Blueprint's Agent package assigns the responsibility here: **[E]** *"may
    declare 0+ Skills/Workflows (INV-15)."* Plain keys, same reason as above.
  - `agent_definition_key` — the template's stable identity. Required because
    INV-3 fixes that an Agent Instance instantiates *exactly one* Agent
    Definition (which presupposes Definitions are distinguishable) and Domain
    Model §5 / INV-2 fix that a Definition is owned by exactly one Department
    (ownership presupposes identity). Named per the ratified `*_key` convention
    already established for canonical identity (`knowledge_item_key`, 3.306 D1).

Deliberately ABSENT — no Capability/Skill/Workflow/Tool declarations, no
runtime identity, no execution state, no lifecycle, no
memory, no trace history, no governance authority, no scheduling, no planning,
no model/provider/prompt, no metadata bag, no configuration system, no registry,
no factory. In particular **no `participate`/`execute`/`run`/`invoke`/`think`/
`reason`/`plan`/`schedule`** — a Definition is descriptive only.

**Construction discipline is reserved.** agent_spec §12/§13 place governed
construction of Definitions/Instances (the *Agent Factory*) in Phase 4, "[O]
reserved to the Architect". This module therefore declares the shape of a
Definition and nothing about how Definitions are governed, validated against
Capabilities (INV-2/INV-14), created, or registered.

That reservation covers construction — *"governed, validated against
Capabilities, created, or registered"* — and **not ownership**, which the three
sources above ratify as `[E]`. `owning_department_key` was added under
`ACT-CC-F03-039` (`DEC-AGENT-DEPT-OWNERSHIP = OPTION A`), carrying **INV-2
clause 1**. The field had been absent for a historical reason rather than a
reserved one: in Phase 3 the Department entity did not exist, only the
`DepartmentRef` stub, and Department was realized under `ACT-CC-F03-036`.

`specified_skills` and `specified_workflows` followed under `ACT-CC-F03-050`
(`DEC-F03-050 = OPTION A`), carrying **INV-15**. Only the Skills/Workflows part
of Domain Model §2's clause is built: *behavior*, *permissions* and *Runtime
requirements* are named in the same sentence and are **not** authorized here.

The relationship is also modelled from the other side — `core/skill/`'s
`SkillDeclaration` and `core/workflow/`'s `WorkflowDeclaration` each hold *"the
Skills/Workflows one Agent Definition specifies"*, keyed by `AgentDefinitionRef`.
Those are the owned entity's view; this is the Definition's own, which Blueprint
assigns to this package. Neither is derived from the other, and — exactly as with
INV-1 and INV-2 — reconciling the two views belongs to a caller that can see
both, since neither boundary may import the other.

`implemented_capabilities` followed under `ACT-CC-F03-040`
(`DEC-AGENT-FACTORY-INV2-CLAUSE2 = OPTION A`), carrying **INV-2 clause 2**.
That clause *was* genuinely behind the reservation: a Definition declaring which
Capabilities it implements is the *"validated against Capabilities"* surface the
Agent Factory reserves. The Founder opened exactly that, and nothing else — the
reservation stands over governed **creation, registration and lifecycle** of
Definitions, which remain unbuilt and unrepresented here.

**What this contract does and does not assert.** It fixes that a Definition
declares **at least one** Capability, which is the whole of INV-2 clause 2 as
stated. Whether those Capabilities *exist*, and whether every Capability has an
implementer (INV-14), are corpus-level facts invisible to a single Definition —
they are reconciled by a caller that can see both sides, exactly as ownership is.

Ownership: this contract owns **only Agent specification identity**. The Agent
Contract owns behavioral participation; Agent Instance (future) will own runtime
identity; Trace owns history (and merely *records* `agent_definition_version` —
Trace depends on nothing here); Execution owns the execution boundary; Runtime
owns hosting; Knowledge owns semantics; Memory owns promotion candidates;
Governance owns authority; Infrastructure owns facilities. No ownership transfer.

Dependencies: **none** — stdlib only. A descriptive data contract needs no import
of the Agent contract, so the permitted `Agent Definition → Agent Contract` edge
is deliberately not created (no unused import). Ownership is carried as a plain
`str` key rather than the Capability boundary's `DepartmentRef`, which keeps
that property intact: `Blueprint §26` and this boundary's dependency-direction
conformance place `capability` among the boundaries Agent must not import, and
holding a key rather than a reference means the ratified relation is expressed
without taking the edge. Resolving that key to a Department is therefore done by
a caller that can see both sides, never by either boundary reaching into the
other. It imports nothing from Runtime,
Execution, Knowledge, Memory, Governance, Trace, Infrastructure, Workflow, Skill,
Planner, or Scheduler. No external dependency, no dynamic import, no hidden
state, no singleton, no registry, no global mutable state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


class InvalidAgentDefinition(ValueError):
    """Raised when an Agent Definition cannot be constructed accountably. Fail
    closed (PR-4): an incomplete Definition is never coerced into a valid one."""


@dataclass(frozen=True)
class AgentDefinition:
    """The immutable specification/template of an Agent.

    Frozen, hashable, and comparable; carries the template's identity, its
    version, the Department that owns it (INV-2 clause 1), the Capabilities it
    implements (INV-2 clause 2), and the Skills and Workflows it is permitted to
    use (INV-15). Descriptive only — it holds no execution, no runtime identity, and
    no behavior."""

    agent_definition_key: str
    agent_definition_version: str
    owning_department_key: str
    implemented_capabilities: Tuple[str, ...]
    specified_skills: Tuple[str, ...]
    specified_workflows: Tuple[str, ...]

    def __post_init__(self):
        if not isinstance(self.agent_definition_key, str) or not self.agent_definition_key.strip():
            raise InvalidAgentDefinition("agent_definition_key must be a non-empty string")
        if not isinstance(self.agent_definition_version, str) or not self.agent_definition_version.strip():
            raise InvalidAgentDefinition("agent_definition_version must be a non-empty string")
        # INV-2 clause 1 [E]: "Every Agent Definition is owned by exactly one
        # Department." Exactly one, so the key is required and single-valued;
        # an unowned or unnamed Definition fails closed (PR-4) rather than
        # being coerced into an ownerless one. Whether the named Department
        # exists, and whether it agrees, is not knowable here — that is the
        # caller's reconciliation, not this contract's.
        if not isinstance(self.owning_department_key, str) or not self.owning_department_key.strip():
            raise InvalidAgentDefinition(
                "owning_department_key must be a non-empty string (INV-2: every "
                "Agent Definition is owned by exactly one Department)"
            )
        # INV-2 clause 2 [E]: "...and implements at least one Capability."
        # "At least one" is the invariant, so an empty declaration fails closed
        # (PR-4) rather than being accepted as a Definition that implements
        # nothing. Duplicates are refused because implementing the same
        # Capability twice is not implementing two.
        if not isinstance(self.implemented_capabilities, tuple):
            raise InvalidAgentDefinition(
                "implemented_capabilities must be a tuple"
            )
        if not self.implemented_capabilities:
            raise InvalidAgentDefinition(
                "implemented_capabilities must name at least one Capability "
                "(INV-2: every Agent Definition implements at least one "
                "Capability)"
            )
        for capability_key in self.implemented_capabilities:
            if not isinstance(capability_key, str) or not capability_key.strip():
                raise InvalidAgentDefinition(
                    "every implemented capability_key must be a non-empty string"
                )
        # Expressed without a local binding: this boundary stores nothing and
        # mutates nothing, so the duplicate check is a comparison rather than
        # an accumulator.
        if len(set(self.implemented_capabilities)) != len(
            self.implemented_capabilities
        ):
            raise InvalidAgentDefinition(
                "a Capability is declared more than once; implementing one "
                "Capability twice is not implementing two"
            )
        # INV-15 [E]: "zero or more Skills and zero or more Workflows … No
        # minimum cardinality is required." ADR-0007 is explicit that an empty
        # declaration — either or both — is "a valid architectural state", so
        # emptiness is never an error here. What is refused is a malformed
        # declaration: a non-tuple, a non-text key, or a repeated key, which
        # would make the declared set ambiguous.
        #
        # The fields are required rather than defaulted, unlike
        # `SkillDeclaration.skills`. Every other field of this contract is
        # required and a conformance guard asserts it, so an author states the
        # declaration explicitly — writing `()` for "none" — rather than
        # omitting it. That is a construction-discipline choice, not a
        # cardinality one: INV-15 governs how many may be named, not whether
        # the declaration must be stated.
        for declared, field_name, noun in (
            (self.specified_skills, "specified_skills", "skill"),
            (self.specified_workflows, "specified_workflows", "workflow"),
        ):
            if not isinstance(declared, tuple):
                raise InvalidAgentDefinition(f"{field_name} must be a tuple")
            for key in declared:
                if not isinstance(key, str) or not key.strip():
                    raise InvalidAgentDefinition(
                        f"every declared {noun}_key must be a non-empty string"
                    )
            if len(set(declared)) != len(declared):
                raise InvalidAgentDefinition(
                    f"a {noun} is declared more than once; a repeated key makes "
                    "the declared set ambiguous"
                )
