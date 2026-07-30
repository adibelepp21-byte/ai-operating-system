"""
Storage facility (Infrastructure spec §2, §5a, §12; Blueprint §14).

Provides persistence facilities *beneath* the substrate subsystems
(Trace, Memory, Knowledge — Infrastructure spec §2). This module supplies
the storage *capability* only; it knows nothing about Trace, Memory, or
Knowledge semantics, and it must not — those entities are out of scope for
Stage I and own their own meaning. Infrastructure serves them a place to
persist; it does not model what they persist.

Two capabilities are exposed as abstractions, with one local backend each:
  - append-only storage: write records that can only be appended, never
    edited or deleted through this facility. This is the storage discipline
    the Trace entity will later require (INV-5 immutability is a Trace
    property; here it is simply an append-only backend, offered generically).
  - the backend is replaceable beneath the entities (Infrastructure spec §12,
    [O]): `StorageFacility` is abstract; `LocalAppendOnlyStorage` is the
    stdlib, filesystem-backed implementation.

Strictly local. Holds NO external dependency (INV-12): it uses only the
Python standard library against the local filesystem. Owns no Knowledge,
makes no governance decision, authors no Trace (Infrastructure spec §8-§10).

Fail Closed (PR-4; Infrastructure spec §11): a write that cannot be
completed raises; there is no partial-success return. Deletion/mutation are
not offered at all — the facility cannot be asked to violate append-only.
"""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Iterator

from .facility import Facility


class StorageFacility(Facility):
    """Abstract storage capability offered to substrate subsystems.

    Concrete backends are replaceable (Infrastructure spec §12). A backend
    offers append and read; it deliberately offers NO edit and NO delete —
    the facility is incapable of mutating persisted records, so no consumer
    can use it to do so.
    """

    name = "storage"

    @abc.abstractmethod
    def append(self, partition: str, record: bytes) -> None:
        """Append one record to a named partition. Raises on failure."""

    @abc.abstractmethod
    def read(self, partition: str) -> Iterator[bytes]:
        """Yield the records of a partition in append order."""

    @abc.abstractmethod
    def partitions(self) -> Iterator[str]:
        """Yield the names of existing partitions."""


class LocalAppendOnlyStorage(StorageFacility):
    """Filesystem-backed append-only storage.

    Each partition is one append-only file under `base_dir`. Records are
    stored one per line (newline-delimited); a record therefore must not
    contain a raw newline — the facility rejects such a record (fail closed)
    rather than corrupt the partition boundary. Consumers that need to store
    newline-bearing payloads encode them (e.g. escape) before appending;
    that encoding is the consumer's concern, not the facility's.

    `base_dir` is supplied by the bootstrap orchestrator (typically resolved
    through the filesystem facility). The facility provisions the directory;
    it never resolves outside the path it was given.
    """

    name = "storage.local-append-only"

    _NEWLINE = b"\n"

    def __init__(self, base_dir: Path):
        super().__init__()
        self._base_dir = Path(base_dir)

    def _provision(self) -> None:
        # Establish the storage area. mkdir is idempotent; failure (e.g.
        # unwritable parent) propagates and marks the facility FAILED.
        self._base_dir.mkdir(parents=True, exist_ok=True)
        if not self._base_dir.is_dir():
            raise NotADirectoryError(f"storage base is not a directory: {self._base_dir}")

    def _partition_path(self, partition: str) -> Path:
        if not partition or "/" in partition or "\\" in partition or partition in (".", ".."):
            # Fail closed: a partition name must be a single, safe segment;
            # it may not be used to escape the storage area.
            raise ValueError(f"invalid partition name: {partition!r}")
        return self._base_dir / partition

    def append(self, partition: str, record: bytes) -> None:
        self.require_ready()
        if not isinstance(record, (bytes, bytearray)):
            raise TypeError("record must be bytes")
        if self._NEWLINE in record:
            raise ValueError("record must not contain a raw newline; encode it before appending")
        path = self._partition_path(partition)
        # Open in binary append mode: the facility offers no seek, no
        # truncate, no overwrite — appification only.
        with open(path, "ab") as f:
            f.write(bytes(record) + self._NEWLINE)

    def read(self, partition: str) -> Iterator[bytes]:
        self.require_ready()
        path = self._partition_path(partition)
        if not path.is_file():
            return iter(())
        return self._read_lines(path)

    @staticmethod
    def _read_lines(path: Path) -> Iterator[bytes]:
        with open(path, "rb") as f:
            for line in f:
                yield line.rstrip(b"\n")

    def partitions(self) -> Iterator[str]:
        self.require_ready()
        if not self._base_dir.is_dir():
            return iter(())
        return (p.name for p in sorted(self._base_dir.iterdir()) if p.is_file())
