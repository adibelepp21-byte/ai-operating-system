"""
Execution consumer contract — ABSTRACTION ONLY (Blueprint §6; runtime_spec
§5/§6/§10; Phase 4.2 Execution Layer).

Declares the canonical **consumer boundary**: the single interface every future
execution consumer (Agent, Workflow, Skill, Planner, Scheduler) implements in
order to take part in an execution.

    Runtime → Execution Layer → [ExecutionConsumer] → Agent / Workflow / Skill /
                                                       Planner / Scheduler (future)

Direction of dependency is deliberately **inverted**: a consumer depends on this
contract, never on Runtime. Runtime therefore never learns which consumer
invoked it, and no `Runtime → Agent/Workflow/Skill/Planner/Scheduler` dependency
can arise.

**Intentionally generic.** `ExecutionConsumer` represents a *generic execution
participant*. It is not an Agent, not a Workflow, not a Skill, not a Planner,
and not a Scheduler — none of those is introduced here.

**Minimum interface.** The only thing a consumer ever receives is the bound
`Execution` boundary (Phase 4.2), which carries just the hosting Runtime and the
execution identity. Because that is the sole entry parameter, every future
consumer necessarily enters Runtime *exclusively through Execution*.

Deliberately ABSENT (declaration only, no behavior): execution logic, execution
policy, lifecycle ownership, Runtime ownership, Knowledge ownership, authority,
state machine, scheduling, planning, orchestration, queues, retries, caching,
logging, metrics, timestamps, UUID, randomness, hidden state, AI behavior, model
invocation.

**Semantics are reserved.** What participation *means* — the action model, the
INV-4 "exactly one Trace per Agent-Instance action" obligation, Workflow-only
coordination (INV-13), Tool-only external access (INV-12) — belongs to the
future, separately authorized consumer phases. This module fixes only the shape
of the boundary, and weakens no frozen invariant.

Ownership: the Execution layer owns **only this abstraction**. Runtime keeps
hosting; Knowledge keeps semantics; Governance keeps authority; Infrastructure
keeps facilities; Trace keeps history; Memory keeps promotion candidates. No
ownership is transferred here.

Dependencies: this package's `contract` (for the `Execution` type) only. It
imports nothing from Runtime directly, and nothing from Knowledge, Governance,
Memory, Trace, or Infrastructure. Stdlib otherwise. No module state, no
singleton, no registry, no service locator, no reflection, no dynamic import.
"""

from __future__ import annotations

import abc

from .contract import Execution


class ExecutionConsumer(abc.ABC):
    """A generic execution participant.

    The single contract every future execution consumer implements. It declares
    one entry point and owns nothing: no lifecycle, no state, no policy, no
    authority."""

    @abc.abstractmethod
    def participate(self, execution: "Execution") -> None:
        """Take part in the given bound execution.

        `execution` is the Phase 4.2 `Execution` boundary — the consumer's only
        route to the hosting Runtime, and therefore the only way it may reach
        anything the Runtime hosts (still subject to the Runtime's own
        RUNNING-only access control, which this contract neither weakens nor
        bypasses).

        Returns `None`: no execution-result model is ratified by the frozen
        architecture, so none is invented here. Implementations are supplied by
        future authorized consumer phases; this declaration carries no
        behavior."""
        ...
