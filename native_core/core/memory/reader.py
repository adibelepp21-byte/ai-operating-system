"""
Memory retrieval (memory_spec §2, §5b, §5c, §11; Freeze INV-5/8; PR-3/PR-4; OQ-2).

The "read scoped memory" and "offer candidates" capabilities (memory_spec
§5b/§5c). Memory is a derive-on-read view over Trace: each read derives Memory
records from Trace (via TraceReader — the only authoritative source),
optionally scopes them, and applies the bounded retention window (INV-7). It
never persists Memory (records are recomputable, §3/§11), never writes Trace
(INV-5), never writes Knowledge, and never promotes (INV-8).

Dependency: this reader relies only on a `TraceReader` beneath it (Memory MAY
depend on Trace). It reaches for no Agent, Runtime, Workflow, or Tool — Trace
is the sole source (§1/§9). Memory authors no Trace of its own derivation
(the derivation facility is infrastructure, not an independent traced actor —
OQ-2).

Fail closed (PR-4; §11): if the Trace source is unavailable, the failure
propagates — Memory is treated as absent, never fabricated or authoritative.
"""

from __future__ import annotations

from typing import Optional, Tuple

from ..trace import TraceReader
from .candidate import PromotionCandidate, generate_candidates
from .extractor import extract
from .record import MemoryRecord
from .retention import DEFAULT_RETENTION_WINDOW, apply_retention


class MemoryReader:
    """Reads scoped, retention-bounded Memory derived from Trace, and offers
    promotion candidates — proposals only."""

    def __init__(self, trace_reader: TraceReader, retention_window: int = DEFAULT_RETENTION_WINDOW):
        if trace_reader is None:
            # Fail closed: without the authoritative Trace source there is no
            # Memory to derive — never fabricate one.
            raise ValueError("MemoryReader requires a TraceReader (the only Memory source)")
        self._trace_reader = trace_reader
        self._retention_window = retention_window

    def read(self, scope: Optional[str] = None) -> Tuple[MemoryRecord, ...]:
        """Derive scoped Memory from Trace, retention-bounded. Reading Trace
        may raise if the storage facility is unavailable (fail closed); this
        reader does not swallow that into a false 'no memory'."""
        trace_records = tuple(self._trace_reader.read())
        memories = extract(trace_records)
        if scope is not None:
            memories = tuple(m for m in memories if m.scope == scope)
        return apply_retention(memories, self._retention_window)

    def candidates(self, scope: Optional[str] = None) -> Tuple[PromotionCandidate, ...]:
        """Offer promotion candidates over the scoped, retention-bounded Memory
        — observations only, for governed review to decide (INV-8; PR-3)."""
        return generate_candidates(self.read(scope))
