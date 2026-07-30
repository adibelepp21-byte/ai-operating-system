"""
Execution contract — ABSTRACTION ONLY (Blueprint §6; runtime_spec §5/§6/§10).

Declares the canonical **execution boundary**: the single architectural bridge
between Runtime and every future execution consumer (Agent, Workflow, Skill,
Scheduler, Planner, Executor). Every future consumer is intended to reach the
Runtime *through* this boundary; Runtime never executes them directly.

An `Execution` is a **transient execution facility**. It is lifecycle-neutral:
it starts nothing and stops nothing — the Runtime lifecycle (Phase 4.0) is
unchanged and remains solely the Runtime's.

The surface is deliberately minimal — it exposes only the bound Runtime and the
execution identity. It exposes **no** planning, scheduling, retries, queues,
model execution, tool execution, workflow execution, skill execution, or agent
execution; those belong to future authorized phases.

Ownership: the Execution layer owns a **transient execution boundary** only. It
owns no business logic, no AI behavior, no planning, no scheduling, no
knowledge, and no authority. Reaching Knowledge through `runtime.knowledge`
still passes the Runtime's own RUNNING-only access control — Execution adds no
authority and bypasses nothing.

Dependencies: this package's `context`, and the Runtime `contract` above it
(Runtime-owned internal structure). Stdlib otherwise.
"""

from __future__ import annotations

import abc

from ..contract import Runtime
from .context import ExecutionContext


class Execution(abc.ABC):
    """The canonical execution boundary: a transient binding of a hosting
    Runtime to an execution identity. Lifecycle-neutral; carries no execution
    verbs."""

    @property
    @abc.abstractmethod
    def runtime(self) -> "Runtime":
        """The bound hosting Runtime. Access to hosted subsystems goes through
        the Runtime's own controlled boundary — this property grants no
        additional access and no authority."""
        ...

    @property
    @abc.abstractmethod
    def context(self) -> "ExecutionContext":
        """The immutable execution identity for this boundary."""
        ...
