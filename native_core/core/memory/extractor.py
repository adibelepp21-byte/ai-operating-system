"""
Memory extraction (memory_spec §2, §5a, §6.1; Freeze INV-5).

Derives Memory records from Trace records — the "derive-from-Trace" capability
(memory_spec §5a). Pure and deterministic: given the same Trace records it
produces the same Memory records, in Trace append order. It reads Trace
evidence and never mutates it (INV-5); it holds no storage, no promotion, and
no governance.

Memory derives *exclusively* from Trace evidence — never from Agents, Runtime,
Workflow, or Tools directly (memory_spec §1/§9). The Trace records passed here
are expected to come from `TraceReader` (the only authoritative source); this
function does not reach for any other input.
"""

from __future__ import annotations

from typing import Iterable, Tuple

from .record import MemoryRecord, derive_from_trace


def extract(trace_records: Iterable) -> Tuple[MemoryRecord, ...]:
    """Derive one Memory record per Trace record, in order. Pure: no I/O, no
    mutation of the input, no side effects, no promotion decision."""
    return tuple(derive_from_trace(r) for r in trace_records)
