"""
Runtime foundation implementation (Phase 4.0). Blueprint §6; runtime_spec
§1–§4, §7, §9–§11; Infrastructure spec §5c; PR-4.

`AIOSRuntime` realizes the `Runtime` contract: lifecycle management, dependency
hosting, execution context, resource ownership, and controlled shutdown. It is a
**facility, not an actor** — it hosts and coordinates; it decides nothing.

FOUNDATION ONLY: there is no Agent, Workflow, Skill, planner, executor, model
adapter, scheduler, task queue, concurrency engine, or automation logic here.

Composition boundary (directive §4): hosted subsystems are assembled **only via
their composition roots**. Knowledge is obtained from
`create_knowledge_subsystem(storage_facility)`; this module never constructs
Knowledge internals, never bypasses the composition root, and never touches
Knowledge private objects.

Ownership discipline:
  - Runtime owns **transient hosting state only** (runtime_spec §3): its
    lifecycle state, its execution ordinal, and references to hosted subsystems.
  - Runtime **owns no Knowledge semantics** (Blueprint §6 forbidden; Freeze §5) —
    it never admits/revises/supersedes/derives status/authorizes promotion.
  - Runtime owns no Memory, no Governance authority, no Trace record, and
    authors **no Trace** of its own (OQ-2; runtime_spec §9).
  - Injected Infrastructure facilities are **not** owned by Runtime: their
    lifecycle belongs to the Infrastructure Bootstrap that established them, so
    `stop()` releases Runtime's own references and never tears them down.

Determinism & injection: constructor injection only — no singleton, no global
registry, no service locator, no reflection, no dynamic import, no hidden cache,
no mutable global state, no randomness, no UUID, no timestamp, no clock.

Dependencies: `..infrastructure` (`StorageFacility`, `ExecutionSubstrate` — the
substrate is the facility Infrastructure provides *to Runtime*, spec §5c) and
`..knowledge.composition` (composition root). Imports nothing from Memory,
Governance, or Trace, and nothing from Agent/Workflow/Capability (they do not
exist). Stdlib otherwise.
"""

from __future__ import annotations

from typing import Optional

from ..infrastructure import ExecutionSubstrate, StorageFacility
from ..knowledge.composition import KnowledgeSubsystem, create_knowledge_subsystem
from ..memory.composition import MemorySubsystem, create_memory_subsystem
from .context import RuntimeContext
from .contract import Runtime
from .exceptions import InvalidRuntimeConfiguration, RuntimeNotRunning, RuntimeSubsystemError
from .lifecycle import RuntimeState, require_transition


class AIOSRuntime(Runtime):
    """The foundational AIOS Runtime: deterministic lifecycle, dependency
    hosting via composition roots, execution context, and controlled shutdown."""

    def __init__(
        self,
        runtime_id: str,
        storage: "StorageFacility",
        substrate: "ExecutionSubstrate",
    ):
        # Constructor injection only; fail closed on an unusable configuration.
        if not isinstance(runtime_id, str) or not runtime_id.strip():
            raise InvalidRuntimeConfiguration("runtime_id must be a non-empty string")
        if not isinstance(storage, StorageFacility):
            raise InvalidRuntimeConfiguration("Runtime requires an Infrastructure StorageFacility")
        if not isinstance(substrate, ExecutionSubstrate):
            raise InvalidRuntimeConfiguration("Runtime requires an Infrastructure ExecutionSubstrate")
        self._runtime_id = runtime_id
        self._storage = storage
        self._substrate = substrate
        # Transient hosting state. No implicit startup: construction only marks
        # CREATED; nothing is assembled or started here.
        self._state = RuntimeState.CREATED
        self._knowledge: Optional[KnowledgeSubsystem] = None
        self._memory: Optional[MemorySubsystem] = None
        self._execution_sequence = 0

    # --- lifecycle ---

    @property
    def state(self) -> "RuntimeState":
        return self._state

    @property
    def runtime_id(self) -> str:
        """The injected identity of this Runtime (inspectable, never generated)."""
        return self._runtime_id

    def initialize(self) -> None:
        """CREATED → INITIALIZED: assemble hosted subsystems from their
        composition roots. Fail closed on an invalid transition; on assembly
        failure the error propagates and the state is left unchanged."""
        target = require_transition(self._state, RuntimeState.INITIALIZED)
        # Composition root only — never construct Knowledge or Memory internals.
        self._knowledge = create_knowledge_subsystem(self._storage)
        # Memory is assembled the same way, under `FD-P7-002`. Runtime holds the
        # assembled bundle and no lifecycle collaborator of its own, which is how
        # hosting stays distinct from owning (`FD-P7-002 §3`).
        self._memory = create_memory_subsystem()
        self._state = target

    def start(self) -> None:
        """INITIALIZED → RUNNING: make hosted subsystems accessible. Fail closed
        if the execution substrate cannot host execution (detect, don't
        silently degrade — runtime_spec §11)."""
        target = require_transition(self._state, RuntimeState.RUNNING)
        if not self._substrate.is_available():
            raise RuntimeSubsystemError(
                "execution substrate is not available; runtime cannot start"
            )
        self._state = target

    def stop(self) -> None:
        """RUNNING → STOPPING → STOPPED: deterministic controlled shutdown.

        Releases only Runtime's own hosted references. Injected Infrastructure
        facilities are NOT torn down here — their lifecycle belongs to the
        Bootstrap that established them. STOPPED is terminal."""
        self._state = require_transition(self._state, RuntimeState.STOPPING)
        self._knowledge = None
        self._memory = None
        self._state = require_transition(self._state, RuntimeState.STOPPED)

    # --- execution context ---

    def create_context(self) -> "RuntimeContext":
        """Issue an immutable execution context. RUNNING only (fail closed).
        The ordinal is monotonic per Runtime — deterministic, no clock, no
        randomness."""
        self._require_running("create_context")
        context = RuntimeContext(
            runtime_id=self._runtime_id,
            execution_sequence=self._execution_sequence,
        )
        self._execution_sequence += 1
        return context

    # --- controlled subsystem access ---

    @property
    def knowledge(self) -> "KnowledgeSubsystem":
        """The hosted Knowledge subsystem. RUNNING only (fail closed). Runtime
        hosts it; Knowledge retains all its own semantics and Governance retains
        all authority."""
        self._require_running("knowledge")
        assert self._knowledge is not None  # guaranteed by the lifecycle
        return self._knowledge

    @property
    def memory(self) -> "MemorySubsystem":
        """The hosted Phase 7 Memory subsystem. RUNNING only (fail closed).

        Authorized by `FD-P7-002`. Runtime hosts it; the Memory boundary retains
        every lifecycle decision — admission, retention, update, consolidation,
        expiry, invalidation and retrieval eligibility. Nothing on this Runtime
        performs any of them, and this property exposes no operation that could.

        The RUNNING gate is the same one Knowledge passes and is not weakened
        for Memory: `FD-P7-002 §7` requires that the gate stay meaningful, so a
        Runtime that is not RUNNING refuses here exactly as it does elsewhere."""
        self._require_running("memory")
        assert self._memory is not None  # guaranteed by the lifecycle
        return self._memory

    # --- internal ---

    def _require_running(self, what: str) -> None:
        if self._state is not RuntimeState.RUNNING:
            raise RuntimeNotRunning(
                f"{what} requires state {RuntimeState.RUNNING.value!r}; "
                f"runtime is {self._state.value!r}"
            )
