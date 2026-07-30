"""
Agent Instance contract — IMMUTABLE DATA CONTRACT (Blueprint §8 Agent Package;
agent_spec §1/§3/§4; Freeze INV-3/INV-4; Domain Model §2.1/§5/§6).

Declares the canonical **Agent Instance**: one runtime realization of exactly one
Agent Definition. It answers exactly one question:

    "Which running Agent is this?"

It is **purely an immutable identity contract**. It does not execute, does not
participate, does not host, and owns no lifecycle — only an Agent Instance *acts*
(agent_spec §1), but acting is declared by the Agent Contract's
`participate(execution)` and realized in future authorized phases, not here.

**Not abstract.** Blueprint requires no abstraction; a Definition/Instance is
descriptive, so this follows the established Native Core frozen-dataclass
convention (`AgentDefinition`, `VersionIdentity`, `RuntimeContext`,
`ExecutionContext`). `__post_init__` performs *structural* fail-closed validation
only (PR-4), never domain logic.

Fields — each justified by direct frozen evidence, none invented:
  - `agent_instance` — the **ratified frozen field name**: one of Trace's ten
    required contents (Domain Model §2.1), recording which Instance acted. Named
    identically to avoid terminology drift.
  - `agent_definition` — the Definition this Instance realizes. **INV-3** [E]:
    "Every Agent Instance instantiates **exactly one** Agent Definition"; holding
    exactly one immutable `AgentDefinition` expresses that invariant structurally.
    This is the single dependency the architecture permits here.

**Deliberately not modelled:** INV-3's second clause — "and is hosted by exactly
one Runtime" — is *not* represented. Binding an Instance to its host is Runtime's
concern (agent_spec §4: "Runtime creates Instance"), and modelling it here would
either create the forbidden `Agent Instance → Runtime` dependency or add a
speculative field. Recorded rather than invented.

Deliberately ABSENT — no lifecycle, activation/deactivation, execution,
`participate` override, state machine, queues, retries, scheduling,
orchestration, workflow, skill, planner, registry, singleton, reflection, dynamic
import, metadata bag, configuration, provider, model, prompts, memory,
governance, or hidden state. Only immutable structural identity.

**Construction discipline is reserved.** agent_spec §12/§13 place governed
construction of Definitions/Instances (the *Agent Factory*) in Phase 4, "[O]
reserved to the Architect", and §14 leaves instance attribution details [O] open.
This module declares the shape of an Instance and nothing about how Instances are
created, activated, registered, or hosted.

Ownership: this contract owns **only runtime identity**. The Agent Contract owns
behavioral participation; Agent Definition owns definition identity; Trace records
execution history (and merely *records* `agent_instance` — Trace depends on
nothing here); Execution owns the execution boundary; Runtime owns hosting;
Knowledge owns semantics; Memory owns promotion candidates; Governance owns
authority; Infrastructure owns facilities. No ownership transfer.

Dependencies: `definition` from THIS package only — the single permitted
`Agent Instance → Agent Definition` edge. It imports nothing from Runtime,
Execution, Knowledge, Memory, Governance, Trace, Infrastructure, Workflow, Skill,
Planner, or Scheduler. Stdlib otherwise; no external library.
"""

from __future__ import annotations

from dataclasses import dataclass

from .definition import AgentDefinition


class InvalidAgentInstance(ValueError):
    """Raised when an Agent Instance cannot be constructed accountably. Fail
    closed (PR-4): an incomplete Instance is never coerced into a valid one."""


@dataclass(frozen=True)
class AgentInstance:
    """One runtime realization of exactly one Agent Definition.

    Frozen, hashable, and comparable; carries only this Instance's identity and
    the immutable Definition it realizes. Identity only — no execution, no
    hosting, no lifecycle, no behavior."""

    agent_instance: str
    agent_definition: AgentDefinition

    def __post_init__(self):
        if not isinstance(self.agent_instance, str) or not self.agent_instance.strip():
            raise InvalidAgentInstance("agent_instance must be a non-empty string")
        if not isinstance(self.agent_definition, AgentDefinition):
            raise InvalidAgentInstance(
                "agent_definition must be an AgentDefinition (INV-3: exactly one Definition)"
            )
