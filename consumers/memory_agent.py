"""
Phase 7 — the Agent side of the Memory lifecycle (`E7-03`).

`FD-P7-001 §6` fixes `E7-03` on a path, not a function call:

```text
Agent → Execution → Runtime (RUNNING) → Memory Retrieval → Result
```

This module is the consumer that makes that path traversable. It adds no
capability to the Memory subsystem and holds no authority over it; it is the
missing *caller*, exactly as `KnowledgeConsumingAgent` was for Phase 6.

**Why it lives here and not in `native_core/core/agent/`.** That is a contract
boundary whose conformance suite pins it shut, and `DEC-P6-042` established the
alternative: the consumer moves out rather than the boundary being weakened to
let it in. `native_core/` gains no knowledge that this file exists.

**Authority direction, which this module must not disturb.** `FD-P7-001 §5` lets
an Agent *"produce Information"* and *"generate or propose a Memory Candidate"*,
and withholds authority to *"directly admit Memory"* or *"directly mutate
admitted Memory lifecycle state."* So this Agent:

  - **forms** Candidates, which confer nothing — a Candidate has no lifecycle
    state to admit itself with;
  - **proposes** them to `MemoryLifecycle`, which decides admission and may
    refuse;
  - **reads** through `MemoryRetrieval`, which returns only eligible Memory;
  - **never transitions.** It exposes no expire, invalidate, update or
    consolidate. Those are the lifecycle boundary's, and an Agent that could
    reach them would be the Memory authority `FD-P7-001 §5` says it must not
    become.

A refusal is returned, not swallowed: `admit` returns `None` when the retention
rule declines, and this Agent surfaces that rather than retrying or fabricating a
Memory. An invalid lifecycle operation raises out of the boundary and this module
lets it raise — catching it would convert a fail-closed lifecycle into a
fail-open one.

**How it reaches Memory.** Two modes, and the second is the architectural one.
Collaborators may be injected directly, useful for focused unit evidence; or
omitted, in which case `participate` resolves them from the Execution it is
handed — `execution.runtime.memory`. That property is RUNNING-gated by the
Runtime itself under `FD-P7-002`, so a consumer reaching Memory through the
Runtime hosting it adds no authority and bypasses nothing.

Dependencies: the `Agent` contract and the Memory public surface. No Runtime type
is imported and the hosting Runtime is never named.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from native_core.core.agent import Agent
from native_core.core.memory import (
    MemoryCandidate,
    MemoryItem,
    MemoryLifecycle,
    MemoryProvenance,
    MemoryRetrieval,
)


class MemoryConsumingAgent(Agent):
    """A concrete `Agent` that proposes Memory Candidates and reads eligible
    Memory through the lawful lifecycle boundary.

    Construction takes the two Memory collaborators by injection — the lifecycle
    boundary and the read surface — or neither, in which case both are resolved
    from the hosting Runtime at participation time.
    """

    def __init__(
        self,
        lifecycle: "Optional[MemoryLifecycle]" = None,
        retrieval: "Optional[MemoryRetrieval]" = None,
        memory_key: Optional[str] = None,
        proposal: "Optional[tuple]" = None,
    ) -> None:
        if lifecycle is not None and not isinstance(lifecycle, MemoryLifecycle):
            raise TypeError("a Memory-consuming Agent requires a MemoryLifecycle")
        if retrieval is not None and not isinstance(retrieval, MemoryRetrieval):
            raise TypeError("a Memory-consuming Agent requires a MemoryRetrieval")
        self._lifecycle = lifecycle
        self._retrieval = retrieval
        self._key = memory_key
        self._proposal = proposal
        self._read: List[MemoryItem] = []
        self._admitted: List[MemoryItem] = []
        self._refused: List[MemoryCandidate] = []

    # -- observation ------------------------------------------------------

    @property
    def memory_read(self) -> Tuple["MemoryItem", ...]:
        """Eligible Memory this Agent obtained, in order. Ordinary in-memory
        evidence for its own callers — **not** a Trace. Trace is authored by the
        Runtime under INV-4 and nothing here writes or substitutes for it."""
        return tuple(self._read)

    @property
    def memory_admitted(self) -> Tuple["MemoryItem", ...]:
        """Memories admitted as a result of this Agent's proposals. The admission
        was the lifecycle boundary's; the proposal was this Agent's."""
        return tuple(self._admitted)

    @property
    def proposals_refused(self) -> Tuple["MemoryCandidate", ...]:
        """Candidates the retention rule declined. Surfaced rather than hidden:
        a refusal the Agent could not observe would be indistinguishable from a
        Memory that was admitted and then vanished."""
        return tuple(self._refused)

    # -- Information → Candidate ------------------------------------------

    def form_candidate(
        self, key: str, payload: "object", source: str = "agent-instance"
    ) -> MemoryCandidate:
        """*Information → Memory Candidate* (`E7-01.8`).

        Constructing a Candidate is all this does. It reaches no boundary, needs
        no lifecycle, and confers no admission — `E7-01.9` requires exactly that,
        and the Candidate type carries no state that could pretend otherwise.
        """
        return MemoryCandidate(
            key=key, payload=payload, provenance=MemoryProvenance(source)
        )

    # -- proposal and retrieval -------------------------------------------

    def propose(self, candidate: MemoryCandidate) -> Optional[MemoryItem]:
        """Propose a Candidate to the lifecycle boundary and let it decide.

        Returns the admitted Memory, or `None` when the boundary refuses. The
        refusal is recorded and returned rather than retried: a consumer that
        re-proposed until something stuck would be manufacturing the admission
        the boundary withheld.
        """
        if self._lifecycle is None:
            raise RuntimeError("propose requires an injected MemoryLifecycle; "
                               "otherwise propose through participate(execution)")
        return self._propose_through(self._lifecycle, candidate)

    def read(self, memory_key: str) -> Optional[MemoryItem]:
        """Obtain the eligible Memory for a key, or `None`.

        Delegates to the read surface and adds nothing. Ineligible Memory —
        expired, invalidated, superseded, never admitted — is not reachable
        through this path at all, which is what makes what it returns *active*.
        """
        if self._retrieval is None:
            raise RuntimeError("read requires an injected MemoryRetrieval; "
                               "otherwise read through participate(execution)")
        return self._read_through(self._retrieval, memory_key)

    def history(self, memory_key: str) -> Tuple["MemoryItem", ...]:
        """The retained version line for a key, through the same surface."""
        if self._retrieval is None:
            raise RuntimeError("history requires an injected MemoryRetrieval")
        return self._retrieval.history(memory_key)

    # -- internal ----------------------------------------------------------

    def _propose_through(self, lifecycle, candidate):
        admitted = lifecycle.admit(candidate)
        if admitted is None:
            self._refused.append(candidate)
        else:
            self._admitted.append(admitted)
        return admitted

    def _read_through(self, retrieval, key):
        item = retrieval.active(key)
        if item is not None:
            self._read.append(item)
        return item

    def _resolve(self, execution: "object"):
        """Return the (lifecycle, retrieval) pair this participation will use.

        Injected collaborators win when present. Otherwise the pair comes from
        the Runtime hosting this Execution — `execution.runtime.memory` — which
        is RUNNING-gated by the Runtime itself under `FD-P7-002`. This consumer
        adds no access control and bypasses none: if the Runtime is not RUNNING,
        the Runtime refuses and the refusal propagates.
        """
        if self._lifecycle is not None and self._retrieval is not None:
            return self._lifecycle, self._retrieval
        subsystem = execution.runtime.memory
        return subsystem.lifecycle, subsystem.retrieval

    # -- the Agent contract ------------------------------------------------

    def participate(self, execution: "object") -> None:
        """Participate in one bound Execution: propose the configured Candidate,
        then read the configured key — both **during** that Execution.

        This is the `E7-03` path in one method. Completion is defined negatively,
        per `agent_execution_semantics_spec` §13.3: participation completes when
        this returns without raising. There is no result value because no result
        model is ratified; what was read is read from `memory_read`.
        """
        lifecycle, retrieval = self._resolve(execution)
        if self._proposal is not None:
            key, payload = self._proposal
            self._propose_through(
                lifecycle,
                MemoryCandidate(
                    key=key, payload=payload,
                    provenance=MemoryProvenance("agent-instance"),
                ),
            )
        if self._key is not None:
            self._read_through(retrieval, self._key)
