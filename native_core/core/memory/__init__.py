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

Public surface:
  - record:    MemoryRecord, derive_from_trace
  - extract:   extract
  - retention: apply_retention, DEFAULT_RETENTION_WINDOW
  - candidate: PromotionCandidate, generate_candidates
  - read:      MemoryReader
"""

from .candidate import PromotionCandidate, generate_candidates
from .extractor import extract
from .reader import MemoryReader
from .record import MemoryRecord, derive_from_trace
from .retention import DEFAULT_RETENTION_WINDOW, apply_retention

__all__ = [
    "MemoryRecord",
    "derive_from_trace",
    "extract",
    "apply_retention",
    "DEFAULT_RETENTION_WINDOW",
    "PromotionCandidate",
    "generate_candidates",
    "MemoryReader",
]
