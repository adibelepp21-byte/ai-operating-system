"""
Knowledge retrieval — abstract contract (Phase 3.316) + in-memory reference
implementation (Phase 3.322). Blueprint §12; Domain Model §8; Relationship Model;
Phase 3.306 D4; Phase 3.307; Phase 3.308 B2/B9; knowledge_spec §5; INV-7.

The abstract `KnowledgeRetrieval` is the CERTIFIED contract (Phase 3.316 / 3.317)
and is UNCHANGED here. `InMemoryKnowledgeRetrieval` is a reference implementation
of the read surface: it owns nothing and delegates **every** read to the injected
`KnowledgeRepository`. It performs no derivation, no history scan, no status
calculation, no filtering/sorting/transformation, and no caching.

Reads are ungated (Phase 3.306 D4); per-consumer read authorization is reserved
to Identity/Authentication ([O]; Freeze §10). Retrieval never mutates anything
and never calls Governance.

Dependencies (injected): `KnowledgeRepository`. Imports only `repository`,
`models`, `exceptions` from THIS package. Imports nothing from storage,
versioning, admission, Memory, Governance, Trace, Infrastructure, Runtime, Agent,
Workflow, Capability, Identity, or Authentication; holds no external dependency
(INV-12); authors no Trace (OQ-2). Stdlib only. No cache, registry, singleton,
globals, async, threads, locks, dynamic import, or reflection.
"""

from __future__ import annotations

import abc
from typing import Optional, Tuple

from .exceptions import KnowledgeError
from .models import KnowledgeVersion, VersionIdentity
from .repository import KnowledgeRepository


class KnowledgeRetrieval(abc.ABC):
    """Read-only surface over admitted Knowledge. Ungated reads; never mutates."""

    @abc.abstractmethod
    def active(self, knowledge_item_key: str) -> "Optional[KnowledgeVersion]":
        """Default read: the single current Active version for an item, or
        `None`. No Governance call; derives/mutates no status."""
        ...

    @abc.abstractmethod
    def version(self, identity: "VersionIdentity") -> "KnowledgeVersion":
        """Explicit version lookup by identity, read-only (may be Superseded).
        Fail closed with `VersionNotFound` on a miss."""
        ...

    @abc.abstractmethod
    def history(self, knowledge_item_key: str) -> "Tuple[KnowledgeVersion, ...]":
        """The item's full, ordered, immutable history, read-only — including
        Superseded (retained) versions (INV-7)."""
        ...


class InMemoryKnowledgeRetrieval(KnowledgeRetrieval):
    """Reference implementation of the read surface. Owns nothing; delegates
    every read to the injected repository. Holds no state beyond the injected
    collaborator; derives nothing, mutates nothing, caches nothing."""

    def __init__(self, repository: "KnowledgeRepository"):
        # Dependency injection only — no service locator, no internal lookup.
        if not isinstance(repository, KnowledgeRepository):
            raise KnowledgeError(["retrieval requires a KnowledgeRepository"])
        self._repository = repository

    def active(self, knowledge_item_key: str) -> "Optional[KnowledgeVersion]":
        # Delegate only; no local derivation, no history scan, no status calc.
        return self._repository.active_version(knowledge_item_key)

    def version(self, identity: "VersionIdentity") -> "KnowledgeVersion":
        # Delegate only; repository fails closed (VersionNotFound) on a miss.
        return self._repository.version(identity)

    def history(self, knowledge_item_key: str) -> "Tuple[KnowledgeVersion, ...]":
        # Delegate only; no filtering, sorting, transformation, or caching.
        return self._repository.history(knowledge_item_key)
