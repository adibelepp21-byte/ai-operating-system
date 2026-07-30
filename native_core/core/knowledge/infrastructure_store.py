"""
Infrastructure-backed Knowledge storage (Phase 3.329). Realizes the certified
`KnowledgeStore` contract (Phase 3.313 / 3.317) over an Infrastructure
`StorageFacility`. Blueprint §12/§14; knowledge_spec §7; Phase 3.306 D3; Phase
3.308 B6; INV-7; OQ-2.

This is an **adapter in the Knowledge boundary**: Knowledge depends downward on
the Infrastructure storage facility beneath it (Blueprint §12; knowledge_spec §7;
3.306 D3). It does NOT live in Infrastructure — Infrastructure is the base and
must never import Knowledge (dependency direction preserved). It realizes exactly
`append` / `load` / `load_history` / `exists`; no additional public method, no
query/search/index/cache/registry/singleton, no authority, no lifecycle, no
status derivation, no version-identity allocation.

Persistence bridge: the Infrastructure facility stores **bytes** in an
append-only partition. This adapter serializes each `KnowledgeVersion` to bytes
on append and reconstructs it on read, using the **standard library** `json`
(the same stdlib serializer the Trace writer uses). `sort_keys` makes the
encoding deterministic; json escapes newlines, so no raw newline breaks the
facility's one-record-per-line append discipline. `content` is a captured value
(INV-6) — the encoding stores the value, never a reference. No external library,
cache, index, hidden state, async, thread, global, or dynamic import.

Append-only + no overwrite (INV-7): the facility is append-only (no edit/delete);
this adapter additionally refuses to store an already-stored identity. Status is
never derived here (that is Versioning's). Ownership: Infrastructure owns physical
persistence; Knowledge owns the version data.

Dependencies: `storage` (the KnowledgeStore contract), `models`, `exceptions`
from THIS package, and the Infrastructure `StorageFacility` + `FacilityUnavailable`
(the sanctioned Knowledge → Infrastructure storage edge). Imports nothing from
Memory, Governance, Trace, Runtime, Agent, Workflow, or Capability; holds no
external dependency (INV-12); authors no Trace (OQ-2). Stdlib only.
"""

from __future__ import annotations

import json
from types import MappingProxyType
from typing import Any, Iterator, Mapping

from ..infrastructure import FacilityUnavailable, StorageFacility
from .exceptions import InvalidKnowledgeVersion, KnowledgeStorageUnavailable, VersionNotFound
from .models import KnowledgeVersion, VersionIdentity
from .storage import KnowledgeStore

# Single append-only partition holding Knowledge version records, in append order.
KNOWLEDGE_PARTITION = "knowledge_versions"


def _to_plain(value: Any) -> Any:
    """Read-only mapping -> dict, tuple -> list, recursively — JSON-native.
    The stored bytes are a plain projection; the in-memory record stays frozen."""
    if isinstance(value, Mapping):
        return {k: _to_plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_plain(v) for v in value]
    return value


def _encode(version: "KnowledgeVersion") -> bytes:
    """Deterministic stdlib-json encoding of a version's identity + captured
    content + validity conditions. `sort_keys` makes it deterministic; json
    escapes newlines so the bytes contain none. Adds no schema field."""
    payload = {
        "knowledge_item_key": version.identity.knowledge_item_key,
        "version_sequence": version.identity.version_sequence,
        "content": _to_plain(version.content),
        "validity_conditions": _to_plain(version.validity_conditions),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _decode(raw: bytes) -> "KnowledgeVersion":
    """Reconstruct a `KnowledgeVersion` from its stored bytes. The record's
    `__post_init__` re-freezes content, so a read record is exactly as immutable
    as a written one."""
    m = json.loads(raw.decode("utf-8"))
    identity = VersionIdentity(m["knowledge_item_key"], m["version_sequence"])
    return KnowledgeVersion(
        identity=identity,
        content=m["content"],
        validity_conditions=m.get("validity_conditions", {}),
    )


class InfrastructureKnowledgeStore(KnowledgeStore):
    """`KnowledgeStore` realized over an injected Infrastructure `StorageFacility`.

    Append-only, no overwrite, no delete (INV-7). Holds no records of its own and
    no cache/index — every read re-reads the facility partition and reconstructs
    records (a single in-order pass to realize the contract, not a query engine).
    Owns no authority, no lifecycle, and no derivation."""

    def __init__(self, storage: "StorageFacility", partition: str = KNOWLEDGE_PARTITION):
        if not isinstance(storage, StorageFacility):
            raise KnowledgeStorageUnavailable(
                "InfrastructureKnowledgeStore requires an Infrastructure StorageFacility"
            )
        self._storage = storage
        self._partition = partition

    def append(self, record: "KnowledgeVersion") -> None:
        if not isinstance(record, KnowledgeVersion):
            raise InvalidKnowledgeVersion("append requires a KnowledgeVersion")
        # Append-only + no overwrite: a stored identity is never replaced.
        if self.exists(record.identity):
            raise InvalidKnowledgeVersion(
                f"version {record.identity!r} already stored; append-only, never overwrite"
            )
        try:
            self._storage.append(self._partition, _encode(record))
        except FacilityUnavailable as exc:
            # Fail closed: surface the Knowledge contract's storage failure.
            raise KnowledgeStorageUnavailable(str(exc))

    def load(self, identity: "VersionIdentity") -> "KnowledgeVersion":
        for version in self._read_all():
            if version.identity == identity:
                return version
        # Fail closed: never fabricate a default-authoritative value.
        raise VersionNotFound(f"no version for identity {identity!r}")

    def load_history(self, knowledge_item_key: str) -> "tuple":
        # Single in-order pass (append order); returns an immutable tuple.
        return tuple(
            v for v in self._read_all()
            if v.identity.knowledge_item_key == knowledge_item_key
        )

    def exists(self, identity: "VersionIdentity") -> bool:
        return any(v.identity == identity for v in self._read_all())

    def _read_all(self) -> "Iterator[KnowledgeVersion]":
        try:
            for raw in self._storage.read(self._partition):
                yield _decode(raw)
        except FacilityUnavailable as exc:
            raise KnowledgeStorageUnavailable(str(exc))
