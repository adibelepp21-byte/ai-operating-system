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
`ACT-CC-F03-039` (`DEC-AGENT-DEPT-OWNERSHIP = OPTION A`). It carries **INV-2
clause 1 only**. Clause 2 — that a Definition *implements at least one
Capability* — needs a Definition checked against Capabilities, which is squarely
the reserved construction discipline, and is **not** represented here. The field
was absent before now for a historical reason rather than a reserved one: in
Phase 3 the Department entity did not exist, only the `DepartmentRef` stub, and
Department was realized under `ACT-CC-F03-036`.

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


class InvalidAgentDefinition(ValueError):
    """Raised when an Agent Definition cannot be constructed accountably. Fail
    closed (PR-4): an incomplete Definition is never coerced into a valid one."""


@dataclass(frozen=True)
class AgentDefinition:
    """The immutable specification/template of an Agent.

    Frozen, hashable, and comparable; carries the template's identity, its
    version, and the Department that owns it (INV-2 clause 1). Descriptive only — it holds no execution, no runtime identity, and
    no behavior."""

    agent_definition_key: str
    agent_definition_version: str
    owning_department_key: str

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
