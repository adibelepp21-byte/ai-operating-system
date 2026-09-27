"""Logical backup and restore of the AIOS store (`FS-DP-01` point 6; FS-09).

The free Supabase plan offers no downloadable backup, so the ratified fallback
is an **operator-run logical export**, and a restore drill is an FS-09
criterion. This module is that export's format and its restore.

An export is JSON Lines, one store record per line::

    {"format": "fullstack.backup/1", "seq": 33, "partition": "fullstack-runs",
     "position": 0, "sha256": "<of the record's bytes>", "record": "<its UTF-8 text>"}

* ``position`` is the record's place in its partition, from 0, with no gap:
  a partition's order is what every reader of the store depends on.
* ``seq`` is the source's global sequence when the source has one
  (`aios_records.seq`); a line from a store without one carries ``null``.
  Lines are in source order; ``seq``, where present, strictly increases.
* ``record`` holds the bytes as text when they are UTF-8, otherwise
  ``record_base64`` holds them. ``sha256`` is checked on every read.

A partition's **joined digest**, ``sha256(b"\\n".join(records))``, is the value
the database computes with
``encode(sha256(string_agg(record, '\\x0a'::bytea order by seq)), 'hex')``, so an
export can be checked against the live table without moving a byte.

Restore appends through the `StorageFacility` contract, which has no edit or
delete. It refuses a target that already holds any of the exported
partitions: a restore makes a **fresh** store, it never merges into one.
Credentials are not part of the store and never enter an export.
"""

from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass
from typing import Dict, Iterable, Iterator, List, Optional, Sequence

from native_core.core.infrastructure.storage import StorageFacility

FORMAT = "fullstack.backup/1"
_FIELDS = {"format", "seq", "partition", "position", "sha256"}


class ExportError(ValueError):
    """An export line is malformed, out of order, or does not match its digest."""


class RestoreRefused(RuntimeError):
    """The restore target is not fresh."""


@dataclass(frozen=True)
class Entry:
    seq: Optional[int]
    partition: str
    position: int
    record: bytes


def line_for(entry: Entry) -> str:
    """One export line, keys sorted, no spaces."""
    body = {"format": FORMAT, "seq": entry.seq, "partition": entry.partition,
            "position": entry.position,
            "sha256": hashlib.sha256(entry.record).hexdigest()}
    try:
        body["record"] = entry.record.decode("utf-8")
    except UnicodeDecodeError:
        body["record_base64"] = base64.b64encode(entry.record).decode("ascii")
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def export_store(storage: StorageFacility,
                 partitions: Optional[Sequence[str]] = None) -> List[Entry]:
    """Every record of `storage`, partition by partition. The facility exposes
    no global sequence, so ``seq`` is None."""
    names = list(partitions) if partitions is not None else list(storage.partitions())
    return [Entry(None, name, position, bytes(record))
            for name in names
            for position, record in enumerate(storage.read(name))]


def parse(lines: Iterable[str]) -> List[Entry]:
    """Read an export, refusing anything that is not exactly well formed."""
    entries: List[Entry] = []
    next_position: Dict[str, int] = {}
    last_seq: Optional[int] = None
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            body = json.loads(line)
        except json.JSONDecodeError as error:
            raise ExportError(f"line {number}: not JSON ({error.msg})") from None
        if not isinstance(body, dict):
            raise ExportError(f"line {number}: not an object")
        keys = set(body)
        payload = keys - _FIELDS
        if not _FIELDS <= keys or payload not in ({"record"}, {"record_base64"}):
            raise ExportError(f"line {number}: fields {sorted(keys)} are not an export line")
        if body["format"] != FORMAT:
            raise ExportError(f"line {number}: format {body['format']!r} is not {FORMAT}")
        partition, position, seq = body["partition"], body["position"], body["seq"]
        if not isinstance(partition, str) or not partition:
            raise ExportError(f"line {number}: no partition")
        if not isinstance(position, int) or isinstance(position, bool):
            raise ExportError(f"line {number}: position is not an integer")
        if position != next_position.get(partition, 0):
            raise ExportError(f"line {number}: {partition} position {position}, "
                              f"expected {next_position.get(partition, 0)}")
        if seq is not None:
            if not isinstance(seq, int) or isinstance(seq, bool):
                raise ExportError(f"line {number}: seq is not an integer")
            if last_seq is not None and seq <= last_seq:
                raise ExportError(f"line {number}: seq {seq} does not follow {last_seq}")
            last_seq = seq
        if "record" in body:
            if not isinstance(body["record"], str):
                raise ExportError(f"line {number}: record is not text")
            record = body["record"].encode("utf-8")
        else:
            try:
                record = base64.b64decode(body["record_base64"], validate=True)
            except (TypeError, ValueError):
                raise ExportError(f"line {number}: record_base64 is not base64") from None
        if hashlib.sha256(record).hexdigest() != body["sha256"]:
            raise ExportError(f"line {number}: the record does not match its sha256")
        next_position[partition] = position + 1
        entries.append(Entry(seq, partition, position, record))
    return entries


def by_partition(entries: Iterable[Entry]) -> Dict[str, List[bytes]]:
    grouped: Dict[str, List[bytes]] = {}
    for entry in entries:
        grouped.setdefault(entry.partition, []).append(entry.record)
    return grouped


def joined_sha256(records: Sequence[bytes]) -> str:
    return hashlib.sha256(b"\n".join(records)).hexdigest()


def summary(entries: Iterable[Entry]) -> Dict[str, dict]:
    """Per partition: record count, byte total and joined digest."""
    return {name: {"records": len(records), "bytes": sum(len(r) for r in records),
                   "sha256_joined": joined_sha256(records)}
            for name, records in sorted(by_partition(entries).items())}


def restore(entries: Sequence[Entry], storage: StorageFacility) -> int:
    """Append every entry, in export order, to a store holding none of its
    partitions. Returns the number of records appended."""
    wanted = set(by_partition(entries))
    occupied = sorted(name for name in wanted if next(iter(storage.read(name)), None) is not None)
    if occupied:
        raise RestoreRefused("the target already holds " + ", ".join(occupied)
                             + "; a restore makes a fresh store and never merges")
    for entry in entries:
        storage.append(entry.partition, entry.record)
    return len(entries)


def differences(entries: Sequence[Entry], storage: StorageFacility) -> List[str]:
    """Where the store's partitions differ from the export. Empty when they are
    byte-identical in content and order."""
    found: List[str] = []
    for name, expected in sorted(by_partition(entries).items()):
        actual = list(storage.read(name))
        if len(actual) != len(expected):
            found.append(f"{name}: {len(actual)} records, export has {len(expected)}")
        for position, (a, e) in enumerate(zip(actual, expected)):
            if a != e:
                found.append(f"{name}: record {position} differs")
    return found


def read_file(path) -> List[Entry]:
    with open(path, encoding="utf-8") as handle:
        return parse(handle)


def write_lines(entries: Iterable[Entry]) -> Iterator[str]:
    for entry in entries:
        yield line_for(entry) + "\n"
