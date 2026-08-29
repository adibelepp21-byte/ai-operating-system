"""
Memory boundary (Native Core Blueprint §11; memory_spec; Freeze INV-5/7/8).

Memory is a dynamic, provisional, retention-bounded, non-authoritative record
of what an Agent Instance encountered, derived from Trace (Domain Model §6/§6.1).
It is substrate — never authoritative, never self-promoting, never
self-governing, never an execution actor.

It obeys the governed chain: Trace → Memory → Governance → Knowledge. Memory
identifies promotion candidates as observations only; Governance decides
(INV-8; PR-3). Memory never bypasses Governance and never writes Trace
(INV-5) or Knowledge.

Module isolation (Blueprint §26): this boundary depends only on Trace (via
`TraceReader`) beneath it; it imports nothing from Governance, Knowledge,
Capability, Skill, Workflow, Agent, Runtime, or Optimization; it holds no
external dependency (INV-12); and it authors no Trace (OQ-2).

Phase 7 adds a **lifecycle** layer above this substrate, ratified by `FD-P7-001`:

```text
Information → Memory Candidate → Admission/Retention → Retrieval
            → Update/Consolidation → Expiry/Invalidation
```

The two layers are deliberately distinct and neither redefines the other. The
Trace-derived `MemoryRecord` remains identity-less and provisional; the Phase 7
`MemoryItem` carries identity, lifecycle state, provenance and lifecycle
metadata because `E7-01` requires exactly that. A `MemoryRecord` is natural
*Information* to form a Candidate from; it is not itself lifecycle-governed
Memory.

**The lifecycle layer changes nothing about authority.** `FD-P7-001 §10` fixes
`Memory ≠ Knowledge` and *"Memory admission ≠ Knowledge promotion"*. Memory
lifecycle admission moves a Candidate into retained Memory and confers no
Knowledge status whatever. `PromotionCandidate`/`generate_candidates` remain the
only Knowledge-facing surface, remain observations, and Governance still decides
them (INV-8; PR-3). Memory is still never authoritative and never
self-promoting.

Public surface:
  - record:      MemoryRecord, derive_from_trace
  - extract:     extract
  - retention:   apply_retention, DEFAULT_RETENTION_WINDOW
  - candidate:   PromotionCandidate, generate_candidates
  - read:        MemoryReader
  - lifecycle:   MemoryItem, MemoryCandidate, MemoryIdentity, MemoryProvenance,
                 MemoryState, ELIGIBLE_STATES
  - boundary:    MemoryLifecycle, MemoryRetrieval, MemoryLifecycleStore
  - composition: MemorySubsystem, create_memory_subsystem
  - exceptions:  MemoryLifecycleError, InvalidMemoryItem,
                 InvalidMemoryTransition, MemoryNotFound,
                 UnauthorizedMemoryMutation
"""

from .admission import MemoryLifecycle
from .candidate import PromotionCandidate, generate_candidates
from .composition import MemorySubsystem, create_memory_subsystem
from .exceptions import (
    InvalidMemoryItem,
    InvalidMemoryTransition,
    MemoryLifecycleError,
    MemoryNotFound,
    UnauthorizedMemoryMutation,
)
from .extractor import extract
from .lifecycle import (
    ELIGIBLE_STATES,
    MemoryCandidate,
    MemoryIdentity,
    MemoryItem,
    MemoryProvenance,
    MemoryState,
)
from .reader import MemoryReader
from .record import MemoryRecord, derive_from_trace
from .retention import DEFAULT_RETENTION_WINDOW, apply_retention
from .retrieval import MemoryRetrieval
from .store import MemoryLifecycleStore

__all__ = [
    "MemoryRecord",
    "derive_from_trace",
    "extract",
    "apply_retention",
    "DEFAULT_RETENTION_WINDOW",
    "PromotionCandidate",
    "generate_candidates",
    "MemoryReader",
    # -- Phase 7 lifecycle (FD-P7-001) --
    "MemoryItem",
    "MemoryCandidate",
    "MemoryIdentity",
    "MemoryProvenance",
    "MemoryState",
    "ELIGIBLE_STATES",
    "MemoryLifecycle",
    "MemoryRetrieval",
    "MemoryLifecycleStore",
    "MemorySubsystem",
    "create_memory_subsystem",
    "MemoryLifecycleError",
    "InvalidMemoryItem",
    "InvalidMemoryTransition",
    "MemoryNotFound",
    "UnauthorizedMemoryMutation",
]
