"""
Trace reader (trace_spec §2, §5b; Freeze INV-5/6).

The read/derive capability (trace_spec §5b): downstream subsystems (Memory,
review state) read Trace records to derive from them. The reader is strictly
read-only — it exposes no capability to modify or delete a record (trace_spec
§5). Reading a record yields the same deeply-immutable, self-contained record
that was written, so a reader depends on nothing beyond the record itself
(INV-6: explainability never depends on later state).

Records are yielded in append order (the storage facility's order), which is
the Trace ordering discipline (trace_spec §6). The reader adds no ordering
field and no re-sorting.

Dependency (trace_spec §7): relies only on the Infrastructure storage facility
beneath it; depends on nothing in Memory/Knowledge/Optimization; holds no
external dependency (INV-12).
"""

from __future__ import annotations

import json
from typing import Iterator

from ..infrastructure import StorageFacility
from .record import TraceRecord, from_mapping
from .writer import TRACE_PARTITION


def _decode(raw: bytes) -> TraceRecord:
    """Reconstruct a record from its stored bytes. Re-validates and re-freezes
    via from_mapping, so a read record is exactly as accountable and immutable
    as a written one."""
    return from_mapping(json.loads(raw.decode("utf-8")))


class TraceReader:
    """Yields Trace records in append order. Read-only: no edit, no delete."""

    def __init__(self, storage: StorageFacility, partition: str = TRACE_PARTITION):
        self._storage = storage
        self._partition = partition

    def read(self) -> Iterator[TraceRecord]:
        """Yield every record in the Trace partition, in append order."""
        for raw in self._storage.read(self._partition):
            yield _decode(raw)
