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
    (Blueprint §6 forbidden; Freeze §5), **no Memory lifecycle or storage**
    (`FD-P7-002 §3`), no Governance authority, and no Trace record. Runtime
    *hosts* Knowledge and, since `FD-P7-002`, Memory — hosting is not owning.
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
from ..memory.composition import MemorySubsystem
from ..infrastructure import ToolSubsystem
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

    @property
    @abc.abstractmethod
    def memory(self) -> "MemorySubsystem":
        """Controlled access to the hosted Phase 7 Memory subsystem, assembled
        via its composition root. Permitted only while RUNNING — fail closed
        otherwise.

        Authorized by **`FD-P7-002`**, which permits Runtime to depend on the
        Memory boundary *"only through a lawful Memory boundary, contract,
        facade, protocol, adapter, or equivalent abstraction"* and *"only for the
        limited purpose of lawful runtime-mediated Memory operations"*. This
        property is that abstraction: it hands back the assembled subsystem and
        nothing more.

        Runtime **hosts** Memory; it does not own Memory lifecycle. Per
        `FD-P7-002 §3` it never admits, retains, updates, consolidates, expires
        or invalidates, and never manipulates Memory internal state outside the
        lawful Memory boundary. Reaching a boundary through this property is not
        manipulating its internals, and no lifecycle operation is exposed here.
        `FD-P7-002 §6` scopes this permission to Phase 7 and makes it no
        precedent for any further Runtime dependency."""
        ...

    @property
    @abc.abstractmethod
    def tools(self) -> "ToolSubsystem":
        """Controlled access to the hosted Phase 8 Tool Ecosystem, assembled via
        its composition root. Permitted only while RUNNING — fail closed
        otherwise.

        **No architectural amendment was required for this one.** Blueprint §6
        already lists Runtime's allowed dependencies as *"agent, workflow, and
        the Tool boundary (infrastructure)"*, and Infrastructure is already a
        permitted Runtime dependency — unlike Memory, which needed `FD-P7-002`.

        Runtime is an **access host only** (`ACT-CC-P8-001 §8.3`): it does not
        own Tool registration, Tool lifecycle, Tool eligibility, or Tool
        governance policy. This property hands back the assembled subsystem and
        exposes no lifecycle mutation and no bypass — a caller reaching a Tool
        through it still passes `ToolInvocationGovernance`, because that is the
        only surface on the bundle that reaches `ToolBoundary.invoke`."""
        ...
