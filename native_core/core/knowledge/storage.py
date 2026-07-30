"""
Knowledge storage — abstract contract (Phase 3.313) + in-memory reference
implementation (Phase 3.319, under Phase 3.319A Option B). Blueprint §12/§14;
knowledge_spec §7; Phase 3.306 D3; Phase 3.308 B6; INV-7; OQ-2.

The abstract `KnowledgeStore` is the CERTIFIED contract (Phase 3.313 / 3.317)
and is UNCHANGED here: `append`, `load`, `load_history`, `exists`.
`InMemoryKnowledgeStore` is a **reference implementation only** — it exists to
prove the contract can be realized without violating the Constitution, Freeze,
dependency rules, authority rules, or lifecycle rules. It is NOT a production
store: no persistence, no filesystem/sqlite/json/yaml/pickle/network, no backend,
no serialization, no cache/registry/singleton, no secondary index, no query
engine, no sorting/optimization, no concurrency/async, no UUID/timestamp/hash.

Storage is NOT Knowledge. It owns persistence only; Knowledge owns the data;
Infrastructure owns the storage facility (Blueprint §14). Storage merely appends
and returns immutable records.

Per Phase 3.319A Option B, "no filtering" means: no arbitrary query capability,
predicate-search API, indexing, secondary index, sorting API, query engine,
cache, or generalized filtering interface is exposed. It does NOT prohibit the
simple internal iteration strictly required to realize `load_history(...)` — that
iteration is an implementation detail of an already-certified contract method,
not an architectural capability.

MANDATORY STORAGE RULES (encoded): S1 never allocates identifiers · S2 never
derives Active · S3 never derives Superseded · S4 never reads Memory · S5 never
calls Governance · S6 never imports Repository · S7 never imports Versioning ·
S8 never imports Admission · S9 never imports Retrieval · S10 no validation
beyond structural safety.

Dependencies: `models` and `exceptions` from THIS package only. Imports nothing
from Memory, Governance, Trace, Infrastructure, Runtime, Agent, Workflow,
Capability, Execution, Identity, Authentication, or from the sibling
repository/versioning/admission/retrieval modules; holds no external dependency
(INV-12); authors no Trace (OQ-2). Stdlib only.
"""

from __future__ import annotations

import abc
from typing import Dict, Tuple

from .exceptions import InvalidKnowledgeVersion, VersionNotFound
from .models import KnowledgeVersion, VersionIdentity


class KnowledgeStore(abc.ABC):
    """Passive append-only persistence contract for immutable Knowledge version
    records. Offers append, load, enumerate, and existence only — deliberately
    NO edit and NO delete (S1/S2; INV-7)."""

    @abc.abstractmethod
    def append(self, record: "KnowledgeVersion") -> None:
        """Append one immutable version record. Never replaces, edits, or
        deletes (S1/S2). Fail closed if the store is unavailable
        (`KnowledgeStorageUnavailable`). Storage decides and authorizes nothing
        (S6); it allocates no identifier (S8)."""
        ...

    @abc.abstractmethod
    def load(self, identity: "VersionIdentity") -> "KnowledgeVersion":
        """Return the immutable record for a specific `VersionIdentity`,
        read-only. Fail closed with `VersionNotFound` if absent — never
        fabricate a value. Derives no lifecycle status (S7)."""
        ...

    @abc.abstractmethod
    def load_history(self, knowledge_item_key: str) -> "Tuple[KnowledgeVersion, ...]":
        """Return all stored records for an item, in append order, read-only —
        including superseded records, which remain permanently available (S1;
        INV-7). Storage returns records; it derives no Active/Superseded status
        (S7)."""
        ...

    @abc.abstractmethod
    def exists(self, identity: "VersionIdentity") -> bool:
        """Existence check for a record identity. Read-only; mutates and derives
        nothing."""
        ...


class InMemoryKnowledgeStore(KnowledgeStore):
    """Reference implementation of `KnowledgeStore` over one private, insertion-
    ordered append-only container (`Dict[VersionIdentity, KnowledgeVersion]`).

    Append-only: a new identity is inserted; an already-stored identity may never
    be re-stored (no overwrite). Records and identities are immutable (Phase
    3.311); the store never mutates them. There is exactly ONE container and no
    secondary index; `load_history` realizes the certified contract by a single
    in-order pass (dict preserves append order), which under Phase 3.319A Option
    B is an internal detail, not a query/filter capability. It allocates no
    identity (S1), derives no status (S2/S3), reads no Memory (S4), calls no
    Governance (S5), and holds no authority. Not persistent, not thread-safe, not
    optimized — a correctness reference only."""

    def __init__(self):
        # Single private append-only store; insertion order == append order.
        self._store: Dict[VersionIdentity, KnowledgeVersion] = {}

    def append(self, record: "KnowledgeVersion") -> None:
        # S10: structural safety only.
        if not isinstance(record, KnowledgeVersion):
            raise InvalidKnowledgeVersion("append requires a KnowledgeVersion")
        # Append-only + no overwrite: a stored identity is never replaced.
        if record.identity in self._store:
            raise InvalidKnowledgeVersion(
                f"version {record.identity!r} already stored; append-only, never overwrite"
            )
        self._store[record.identity] = record

    def load(self, identity: "VersionIdentity") -> "KnowledgeVersion":
        try:
            return self._store[identity]
        except KeyError:
            # Fail closed: never fabricate a default-authoritative value.
            raise VersionNotFound(f"no version for identity {identity!r}")

    def load_history(self, knowledge_item_key: str) -> "Tuple[KnowledgeVersion, ...]":
        # Simple internal iteration in append order (S/Option B: not a query
        # engine). Returns an immutable tuple; the container is never exposed.
        return tuple(
            v for v in self._store.values()
            if v.identity.knowledge_item_key == knowledge_item_key
        )

    def exists(self, identity: "VersionIdentity") -> bool:
        return identity in self._store
