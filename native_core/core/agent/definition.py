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
  - `agent_definition_key` — the template's stable identity. Required because
    INV-3 fixes that an Agent Instance instantiates *exactly one* Agent
    Definition (which presupposes Definitions are distinguishable) and Domain
    Model §5 / INV-2 fix that a Definition is owned by exactly one Department
    (ownership presupposes identity). Named per the ratified `*_key` convention
    already established for canonical identity (`knowledge_item_key`, 3.306 D1).

Deliberately ABSENT — no Capability/Skill/Workflow/Tool declarations, no
Department binding, no runtime identity, no execution state, no lifecycle, no
memory, no trace history, no governance authority, no scheduling, no planning,
no model/provider/prompt, no metadata bag, no configuration system, no registry,
no factory. In particular **no `participate`/`execute`/`run`/`invoke`/`think`/
`reason`/`plan`/`schedule`** — a Definition is descriptive only.

**Construction discipline is reserved.** agent_spec §12/§13 place governed
construction of Definitions/Instances (the *Agent Factory*) in Phase 4, "[O]
reserved to the Architect". This module therefore declares the shape of a
Definition and nothing about how Definitions are governed, validated against
Capabilities (INV-2/INV-14), created, or registered.

Ownership: this contract owns **only Agent specification identity**. The Agent
Contract owns behavioral participation; Agent Instance (future) will own runtime
identity; Trace owns history (and merely *records* `agent_definition_version` —
Trace depends on nothing here); Execution owns the execution boundary; Runtime
owns hosting; Knowledge owns semantics; Memory owns promotion candidates;
Governance owns authority; Infrastructure owns facilities. No ownership transfer.

Dependencies: **none** — stdlib only. A descriptive data contract needs no import
of the Agent contract, so the permitted `Agent Definition → Agent Contract` edge
is deliberately not created (no unused import). It imports nothing from Runtime,
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

    Frozen, hashable, and comparable; carries only the template's identity and
    version. Descriptive only — it holds no execution, no runtime identity, and
    no behavior."""

    agent_definition_key: str
    agent_definition_version: str

    def __post_init__(self):
        if not isinstance(self.agent_definition_key, str) or not self.agent_definition_key.strip():
            raise InvalidAgentDefinition("agent_definition_key must be a non-empty string")
        if not isinstance(self.agent_definition_version, str) or not self.agent_definition_version.strip():
            raise InvalidAgentDefinition("agent_definition_version must be a non-empty string")
