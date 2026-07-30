"""
Trace writer (Freeze INV-4/5; trace_spec §2, §5a, §6, §11; Constitution §14.2).

The write-once, append-only, unconditional production of Trace records. This
is the "accept-a-completed-action-record" capability (trace_spec §5a): it
takes one already-completed action record and appends it, permanently.

INV-4 / §14.2 (unconditional): `write()` has no enable flag, no threshold, no
early return, and no branch that skips writing. Every call produces exactly
one appended record. Production cannot be disabled by any caller.

INV-5 (append-only, immutable): the writer only appends, via the
Infrastructure append-only storage facility, which itself offers no edit or
delete. There is no update or delete method here — the writer is structurally
incapable of altering a written record.

Fail closed (PR-4; trace_spec §11): if the record cannot be written, the
error propagates; the writer never returns a value that could be mistaken for
a successful write. A missing Trace is a governance failure, never a silent
success — so the writer signals failure by raising, not by returning.

Dependency (trace_spec §7): the writer relies only on an Infrastructure
storage *facility* beneath it (audited through the invoking action — OQ-2).
It depends on nothing in Memory, Knowledge, or Optimization, and holds no
external dependency (INV-12). It does not itself author a Trace of its own
writing (infinite-regress excluded — trace_spec §9).
"""

from __future__ import annotations

import json

from ..infrastructure import StorageFacility
from .record import TraceRecord

# The single append-only partition holding the accountability record, in
# global append order. Retention across this partition is a governed,
# reserved parameter (trace_spec §12/§13); it is not decided here.
TRACE_PARTITION = "trace"


def _encode(record: TraceRecord) -> bytes:
    """Deterministic, compact encoding of a record's ratified contents.

    Uses the standard library only. `sort_keys` and fixed separators make the
    encoding deterministic — the same record always yields identical bytes.
    Any newline inside string content is JSON-escaped (\\n), so the encoded
    bytes contain no raw newline and never break the storage facility's
    one-record-per-line append discipline. The concrete storage encoding is an
    implementation-tier, replaceable choice (Blueprint §3 reserved); it adds
    no schema field and no protocol.
    """
    return json.dumps(
        record.to_mapping(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


class TraceWriter:
    """Appends completed action records to the immutable Trace partition.

    Constructed with an Infrastructure storage facility (dependency
    injection — the backend is replaceable beneath the entity, trace_spec
    §12). The facility must be provisioned; if it is not, `write()` fails
    closed when the append is attempted.
    """

    def __init__(self, storage: StorageFacility, partition: str = TRACE_PARTITION):
        self._storage = storage
        self._partition = partition

    def write(self, record: TraceRecord) -> None:
        """Append exactly one record, unconditionally. Raises on any failure
        to write (fail closed); returns nothing on success. There is no path
        through this method that does not append the record."""
        if not isinstance(record, TraceRecord):
            # Fail closed: only a real, validated record may be written.
            raise TypeError("write() requires a TraceRecord")
        self._storage.append(self._partition, _encode(record))
