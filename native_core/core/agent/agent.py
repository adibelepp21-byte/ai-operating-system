"""
Agent contract — ABSTRACTION ONLY (Blueprint §8 Agent Package; agent_spec;
Freeze INV-2/INV-3/INV-4/INV-8/INV-12/INV-13).

Declares the canonical **Agent** abstraction in its minimal form. It answers
exactly one question:

    "How does an Agent enter the execution system?"

Answer: as an execution participant. `Agent` extends the Phase 4.3
`ExecutionConsumer`, so its only entry point is the inherited
`participate(execution)` and its only route to the hosting Runtime is the Phase
4.2 `Execution` boundary. Agent therefore can never access Runtime directly,
never own Runtime, and never bypass Execution — the boundary is enforced by the
contract's shape, not by convention.

It deliberately answers **none** of: which Agent is this · which version is this ·
which instance is this · which model, provider, or prompt is this. Identity,
metadata, and versioning belong to the future **Agent Definition** (template) and
**Agent Instance** (the only actor) layers — Blueprint §8 — and this contract
remains completely independent of them. Trace requires nothing of this contract:
identity is supplied to `new_record(...)` as arguments by the caller, and the
Trace boundary imports nothing from Agent.

Deliberately ABSENT (declaration only, no behavior): identity, metadata,
versioning, configuration, state, AI behavior, reasoning, prompts, LLM/model
invocation, provider abstraction, inference, planning, workflow logic, skill
logic, scheduling, execution policy, orchestration, memory policy, knowledge
access, governance, trace authorship, infrastructure, cache, registry, lifecycle,
retries, queues, metrics, logging, timestamps, UUID, randomness.

**Semantics are reserved.** What an Agent *does* — implementing ≥1 Capability
(INV-2), instantiating exactly one Definition on exactly one Runtime (INV-3),
producing exactly one Trace per action (INV-4), collaborating only via
Workflow/Knowledge/scoped Memory (INV-13), reaching outside only via Tool
(INV-12), and proposing but never deciding promotion (INV-8; PR-3) — belongs to
future, separately authorized phases. This module fixes only the shape of the
abstraction and weakens no frozen invariant.

Ownership: this boundary owns **only the behavioral abstraction**. Agent
Definition (future) will own definition identity; Agent Instance (future) will
own runtime identity; Trace continues to own historical recording; Execution owns
the execution boundary; Runtime owns hosting; Knowledge owns semantics; Memory
owns promotion candidates; Governance owns authority; Infrastructure owns
facilities. No ownership is transferred here.

Dependencies: the `ExecutionConsumer` contract only (Agent → Execution). It
imports nothing from Knowledge, Memory, Governance, Trace, Infrastructure,
Workflow, Skill, Planner, or Scheduler. Stdlib otherwise. No module state, no
singleton, no registry, no reflection, no dynamic import.
"""

from __future__ import annotations

from ..runtime.execution.consumer import ExecutionConsumer


class Agent(ExecutionConsumer):
    """An intelligent execution participant.

    An Agent **is** an Execution Consumer — nothing more. It inherits
    `participate(execution)` as its sole required responsibility and sole entry
    point, making the `Execution` boundary its only route to the hosting Runtime.
    The contract owns nothing: no identity, no metadata, no state, no lifecycle,
    no policy, no authority, no model."""
