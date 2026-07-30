"""
Runtime contract — ABSTRACTION ONLY (Blueprint §6; runtime_spec §1/§4/§5/§10).

Declares the Runtime public interface: startup, shutdown, lifecycle state,
execution-context creation, and the controlled subsystem-access boundary. Every
operation is an `@abstractmethod`/abstract property with a `...` body — this
module implements no behavior.

Runtime is a **facility, not an actor** (Domain Model; runtime_spec §1). It
hosts and coordinates; it does not decide.

Deliberately ABSENT (Phase 4.0 is foundation only): scheduling, concurrency
engine, task queue, Agent execution, Workflow engine, Skill, planner, executor,
model adapter, or any automation logic.

Frozen constraints this contract preserves:
  - Runtime owns transient hosting state only; it **owns no Knowledge**
    (Blueprint §6 forbidden; Freeze §5), no Memory, no Governance authority, and
    no Trace record.
  - Runtime authors **no independent Trace** (OQ-2; runtime_spec §9) — nothing
    here produces a Trace.
  - Runtime enforces isolation, not policy — it makes no governance decision
    (runtime_spec §10; §6.2 invariant 2).
  - Fail closed (PR-4; runtime_spec §11): invalid lifecycle transitions and
    out-of-state access are refused, never degraded.

Ownership: Runtime. Dependencies: this package's `context`/`lifecycle` and the
Knowledge composition bundle type (for the access boundary's return type only).
Stdlib otherwise.
"""

from __future__ import annotations

import abc

from ..knowledge.composition import KnowledgeSubsystem
from .context import RuntimeContext
from .lifecycle import RuntimeState


class Runtime(abc.ABC):
    """The Runtime public interface: lifecycle, execution context, and a
    controlled boundary to hosted subsystems."""

    @property
    @abc.abstractmethod
    def state(self) -> "RuntimeState":
        """The current lifecycle state. The complete state set is
        `RuntimeState`; there is no hidden state."""
        ...

    @abc.abstractmethod
    def initialize(self) -> None:
        """CREATED → INITIALIZED. Assemble hosted subsystems from their
        composition roots. No implicit startup: this never runs on construction
        or import. Fail closed on an invalid transition."""
        ...

    @abc.abstractmethod
    def start(self) -> None:
        """INITIALIZED → RUNNING. Makes hosted subsystems accessible. Fail closed
        on an invalid transition."""
        ...

    @abc.abstractmethod
    def stop(self) -> None:
        """RUNNING → STOPPING → STOPPED. Deterministic controlled shutdown;
        after it, subsystem access is refused and the Runtime is terminal (never
        restarted). Fail closed on an invalid transition."""
        ...

    @abc.abstractmethod
    def create_context(self) -> "RuntimeContext":
        """Issue an immutable execution context (runtime identity + monotonic
        execution ordinal). Permitted only while RUNNING — fail closed
        otherwise. Carries execution metadata only."""
        ...

    @property
    @abc.abstractmethod
    def knowledge(self) -> "KnowledgeSubsystem":
        """Controlled access to the hosted Knowledge subsystem, assembled via its
        composition root. Permitted only while RUNNING — fail closed otherwise.

        Runtime **hosts** Knowledge; it does not own Knowledge semantics: it
        never admits, revises, supersedes, derives status, or authorizes
        promotion. Governance remains the sole authority (INV-8)."""
        ...
