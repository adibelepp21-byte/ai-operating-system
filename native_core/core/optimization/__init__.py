"""
Optimization boundary (Native Core Blueprint §3 root tree, §15 Optimization
Package; optimization_spec; Freeze §5 layer 10; PR-3; PR-4; INV-5; INV-8;
INV-12).

Optimization is the eleventh and last of the frozen subsystem boundaries — the
**governed learning loop**, detect-only. It observes Trace and Memory and
publishes what it observed; humans decide (Freeze §7/§10; PR-3; INV-8).

Baseline 06 establishes the **structural boundary only**:

    Trace  ─┐
            ├─► Optimization ─► Optimization Publication ─► (optional future read)
    Memory ─┘

**It depends on Governance in no way** (P7-I27 Conflict A ruling). Optimization
never submits, sends, notifies, requests, approves, promotes, authorizes, or
decides. It publishes; a consumer may later read, and no such integration exists
today. The direction is inverted, so no `Optimization → Governance` dependency
can arise and automation cannot acquire a decision path — the Critical risk the
Roadmap names for this boundary (§9.11).

NOT implemented here — **Architect Reserved** (optimization_spec §12/§14;
P7-I27 Conflict B ruling): signal catalogue · evaluation scoring · prioritization
model · optimization algorithm · recommendation engine · ranking model · decision
heuristics · promotion strategy. No scoring, ranking, or recommendation surface
exists, and none can be added without extending the contract under a future
authorization. Model-level optimization remains external and reserved
(Freeze §10) — it is not an AIOS entity.

Ownership (Blueprint §15): Optimization owns **non-authoritative** evaluation
records and candidates only. It owns no authoritative data: Trace keeps
immutable history (INV-5, never mutated here) · Memory keeps derivation ·
Knowledge keeps semantics · Governance keeps authority · Infrastructure keeps
facilities. It authors **no Trace** and introduces **no Domain Model entity**
(Roadmap §9.11 — *"Entity: (none; detect-only)"*; Blueprint §31).

Module isolation (Blueprint §26): this boundary reads only the Trace and Memory
public surfaces, holds no external dependency (INV-12), and no subsystem imports
Optimization — no inversion, no cycle.

Legacy assets (`observability.py`, `metrics.py` — REFERENCE ONLY;
`promotion.py` — CANONICAL REFERENCE) were **not imported, not copied, not
migrated, and not consulted** in building this boundary (P7-I27 Conflict C
ruling).

Public surface:
  - contract:    ObservationSource, ObservationPublication
  - observation: OptimizationObservation, OBSERVABLE_SOURCES, TRACE_SOURCE, MEMORY_SOURCE
  - proposals:   OptimizationProposal
  - composition: create_optimization, TraceObservationSource,
                 MemoryObservationSource, PassiveObservationPublication
  - exceptions:  OptimizationError, InvalidObservation, InvalidProposal,
                 InvalidOptimizationConfiguration
"""

from .composition import (
    MemoryObservationSource,
    PassiveObservationPublication,
    TraceObservationSource,
    create_optimization,
)
from .contract import ObservationPublication, ObservationSource
from .exceptions import (
    InvalidObservation,
    InvalidOptimizationConfiguration,
    InvalidProposal,
    OptimizationError,
)
from .observation import (
    MEMORY_SOURCE,
    OBSERVABLE_SOURCES,
    TRACE_SOURCE,
    OptimizationObservation,
)
from .proposals import OptimizationProposal

__all__ = [
    "ObservationSource",
    "ObservationPublication",
    "OptimizationObservation",
    "OBSERVABLE_SOURCES",
    "TRACE_SOURCE",
    "MEMORY_SOURCE",
    "OptimizationProposal",
    "create_optimization",
    "TraceObservationSource",
    "MemoryObservationSource",
    "PassiveObservationPublication",
    "OptimizationError",
    "InvalidObservation",
    "InvalidProposal",
    "InvalidOptimizationConfiguration",
]
