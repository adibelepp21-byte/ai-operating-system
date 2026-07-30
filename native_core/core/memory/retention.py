"""
Memory retention (memory_spec §2, §4, §6; Domain Model §6; Freeze INV-7).

Memory has a bounded retention window (INV-7): it is provisional and
"promote or expire" (Domain Model §6). This module computes which derived
records survive the window; the ones outside it expire — which never
compromises Trace, since Memory is recomputable and Trace is permanent
(memory_spec §11; Domain Model §6.1).

Because native Trace records carry no timestamp field (schema is exactly the
ten Domain Model §2.1 contents), the window is bounded by *recency in append
order* per scope, not by wall-clock time. The exact retention policy — the
window size and whether it is ever time-based — is [O] reserved (§12/§14);
this module provides a bounded, replaceable mechanism with a conservative
default. Fail closed (PR-4): an unbounded or invalid window is rejected, since
INV-7 requires the window to be bounded.
"""

from __future__ import annotations

from typing import Sequence, Tuple

from .record import MemoryRecord

# Bounded default window (per scope), by recency. The precise policy is [O]
# reserved; this is a replaceable parameter, not a ratified constant.
DEFAULT_RETENTION_WINDOW = 1000


def apply_retention(
    memory_records: Sequence[MemoryRecord],
    window: int = DEFAULT_RETENTION_WINDOW,
) -> Tuple[MemoryRecord, ...]:
    """Keep the most recent `window` records per scope (recency = input order);
    older records in a scope expire out of the window. Returns survivors in
    original order. Fail closed on an unbounded or negative window (INV-7
    requires a bounded window)."""
    if window is None or not isinstance(window, int) or window < 0:
        raise ValueError("retention window must be a bounded, non-negative integer (INV-7)")

    # Determine, per scope, the set of positions that fall within the last
    # `window` occurrences. Preserve overall order in the result.
    positions_by_scope: dict = {}
    for idx, rec in enumerate(memory_records):
        positions_by_scope.setdefault(rec.scope, []).append(idx)

    keep: set = set()
    for scope, positions in positions_by_scope.items():
        for idx in positions[-window:] if window > 0 else []:
            keep.add(idx)

    return tuple(rec for idx, rec in enumerate(memory_records) if idx in keep)
