"""
Stored-record decoding (Blueprint §14; infrastructure_spec §2; INV-12; PR-4).

`StorageFacility` yields the bytes a partition holds. Something must turn those
bytes into structured records before an entity boundary can interpret them, and
that transformation belongs here: Infrastructure owns the storage
representation, so Infrastructure owns reading it back. Blueprint §14 places
facilities beneath entities precisely so an entity boundary is never obliged to
know how its data was written down.

The consuming boundary keeps the meaning. This module answers only *"what did
the store hold?"* — never *"what does it mean?"*. It validates that a record is
a well-formed object and nothing further: no schema, no field vocabulary, no
domain type, and no knowledge of any entity. `Runtime`, for instance, consumes
the resulting mappings through its own `DefinitionCatalog.from_records` and
applies its own rules there.

Why this is a plain transformation rather than a `Facility`: a decoder holds no
resource, opens nothing, and has no lifecycle to provision or release. Making it
a Facility would give it a readiness state it cannot meaningfully be in.
Determinism follows from purity — the same bytes always decode to the same
record (Blueprint §26).

Fail closed (PR-4): a record that cannot be decoded accountably raises. Nothing
here skips a bad record, substitutes a default, or returns a partial catalog —
a partially-read store would answer questions it has no basis to answer.

Ownership: Infrastructure. Dependencies: `json` from the standard library and
this boundary's own `StorageFacility`. Nothing external attaches here — the Tool
boundary remains the only external-integration point (INV-12).
"""

from __future__ import annotations

import json
from typing import Iterable, Iterator, Mapping

from .storage import StorageFacility


class RecordDecodeError(ValueError):
    """A stored record could not be decoded accountably (PR-4).

    Raised rather than skipping the record: a caller that silently dropped
    unreadable entries would report a complete answer drawn from incomplete
    data.
    """


def decode_record(raw: bytes) -> Mapping[str, object]:
    """Decode one stored record into a mapping.

    The record is a UTF-8 JSON object — the encoding already used across the
    core for stored records. A record that is not valid UTF-8, not valid JSON,
    or not a JSON *object* raises: a bare list or scalar is not a record.
    """
    if not isinstance(raw, (bytes, bytearray)):
        raise RecordDecodeError("a stored record is bytes")
    try:
        decoded = json.loads(bytes(raw).decode("utf-8"))
    except UnicodeDecodeError as error:
        raise RecordDecodeError("a stored record is not valid UTF-8") from error
    except ValueError as error:
        raise RecordDecodeError("a stored record is not valid JSON") from error
    if not isinstance(decoded, dict):
        raise RecordDecodeError(
            f"a stored record must be a JSON object, found {type(decoded).__name__}"
        )
    return decoded


def decode_records(raws: Iterable[bytes]) -> Iterator[Mapping[str, object]]:
    """Decode a sequence of stored records in the order the store yielded them.

    Order is preserved because storage is append-only: the order records were
    written is itself information the consuming boundary may rely on.
    """
    for raw in raws:
        yield decode_record(raw)


def read_records(
    storage: StorageFacility, partition: str
) -> Iterator[Mapping[str, object]]:
    """Read a partition through an injected facility and decode what it holds.

    The seam between stored bytes and a consuming boundary. The facility is
    supplied, never constructed here, and is left exactly as it was found —
    reading opens nothing and retains nothing.
    """
    if not isinstance(storage, StorageFacility):
        raise RecordDecodeError("records are read through a StorageFacility")
    if not isinstance(partition, str) or not partition.strip():
        raise RecordDecodeError("a partition name must be a non-empty string")
    return decode_records(storage.read(partition))
