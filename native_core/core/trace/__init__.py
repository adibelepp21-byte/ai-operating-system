"""
Trace boundary (Native Core Blueprint §13; trace_spec; Freeze INV-4/5/6).

Trace is the immutable, append-only, unconditional record of one
Agent-Instance action — the single permanent source of truth, and AIOS's
accountability substrate. It is categorically NOT logging, telemetry,
metrics, observability, a callback, a checkpoint, or an event bus (Freeze
AD-8; Vocabulary Freeze §4/§5). Trace is accountability; never observability.

Module isolation (Blueprint §26): this boundary exposes only its permitted
interactions. It depends only on an Infrastructure storage facility beneath
it (trace_spec §7); it imports nothing from Memory, Knowledge, or
Optimization (they derive from Trace — Blueprint §20/§21); it holds no
external dependency (INV-12); and it authors no Trace of its own writing
(OQ-2; trace_spec §9).

Public surface (the only names other boundaries may depend on):
  - record: TraceRecord, new_record, from_mapping, VALID_STATUSES, REQUIRED_FIELDS, InvalidTraceRecord
  - write:  TraceWriter
  - read:   TraceReader
"""

from .reader import TraceReader
from .record import (
    REQUIRED_FIELDS,
    VALID_STATUSES,
    InvalidTraceRecord,
    TraceRecord,
    from_mapping,
    new_record,
)
from .writer import TRACE_PARTITION, TraceWriter

__all__ = [
    "TraceRecord",
    "new_record",
    "from_mapping",
    "VALID_STATUSES",
    "REQUIRED_FIELDS",
    "InvalidTraceRecord",
    "TraceWriter",
    "TraceReader",
    "TRACE_PARTITION",
]
