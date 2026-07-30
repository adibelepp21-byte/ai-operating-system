"""
Knowledge repository — abstract contract (Phase 3.312) + orchestration reference
implementation over storage + versioning (Phase 3.324; refactor of Phase 3.318).
Blueprint §12; knowledge_spec §6; Domain Model §6; Phase 3.306 D2; Phase 3.308
B2/B3/B4; INV-7.

The abstract `KnowledgeRepository` fixes the append-only history / derived-status
rules and is UNCHANGED. `InMemoryKnowledgeRepository` is a **thin orchestration
layer**: it owns NO persistent container. Persistence flows exclusively through
an injected `KnowledgeStore`; Active-version derivation is delegated exclusively
to an injected `KnowledgeVersioning`. This exactly matches the subsystem
boundaries — Storage owns persistence, Versioning owns derivation, Repository
orchestrates — while external behavior is identical to Phase 3.318.

WHAT THE REPOSITORY OWNS: orchestration only (no records, no history container,
no derived state, no cache, no index). WHAT IT DOES NOT OWN: the storage backend,
the version-derivation algorithm, admission, authority, identifier allocation,
lifecycle decisions.

THE REPOSITORY MUST NEVER: modify a KnowledgeVersion; change canonical status;
allocate identifiers; generate versions; decide admission; authorize promotion;
mutate Memory, Governance, or Trace; keep a shadow history.

APPEND-ONLY RULE: enforced by the storage facility beneath it (append-only,
no overwrite, no delete — INV-7). CANONICAL STATUS RULE: derived by versioning
from the stored history; never stored on or mutated into a version (3.306 D2).

Dependencies (injected): `KnowledgeStore`, `KnowledgeVersioning`. Imports only
`models`, `exceptions`, `storage`, `versioning` from THIS package. Imports
nothing from Memory, Governance, Trace, Infrastructure, Runtime, Agent, Workflow,
Capability, Execution, Identity, or Authentication; holds no external dependency
(INV-12); authors no Trace (OQ-2). Stdlib only.
"""

from __future__ import annotations

import abc
from typing import Optional, Tuple

from .exceptions import KnowledgeError
from .models import KnowledgeVersion, VersionIdentity
from .storage import KnowledgeStore
from .versioning import KnowledgeVersioning


class KnowledgeRepository(abc.ABC):
    """Passive contract over the append-only Knowledge version history.

    Declares responsibilities and the append-only / derived-status rules only.
    Concrete realizations orchestrate but still decide and authorize nothing."""

    @abc.abstractmethod
    def record_version(self, version: "KnowledgeVersion") -> None:
        """Append one immutable version record to the item's append-only
        history. Reached ONLY via an authorized admission/revision (INV-8) — the
        repository itself decides and authorizes nothing. Never replaces or
        deletes a prior version (append-only forever, INV-7)."""
        ...

    @abc.abstractmethod
    def active_version(self, knowledge_item_key: str) -> "Optional[KnowledgeVersion]":
        """Return the single current **Active** version for an item, **derived**
        from history (Phase 3.306 D2), or `None`. The repository delegates
        derivation; it never computes status itself."""
        ...

    @abc.abstractmethod
    def version(self, identity: "VersionIdentity") -> "KnowledgeVersion":
        """Return a specific version by identity, read-only (may be Superseded).
        Fail closed with `VersionNotFound` if absent."""
        ...

    @abc.abstractmethod
    def history(self, knowledge_item_key: str) -> "Tuple[KnowledgeVersion, ...]":
        """Return the item's full, ordered version history (audit trail),
        read-only, oldest→newest — including Superseded versions (INV-7)."""
        ...

    @abc.abstractmethod
    def exists(self, identity: "VersionIdentity") -> bool:
        """Existence query. Read-only; derives and mutates nothing."""
        ...


class InMemoryKnowledgeRepository(KnowledgeRepository):
    """Thin orchestration reference implementation over injected storage +
    versioning. Owns NO persistent container: persistence is delegated to the
    `KnowledgeStore`, and Active derivation to the `KnowledgeVersioning`. It
    keeps no shadow history, no cache, no index, and no derived state; it holds
    only its two injected collaborators."""

    def __init__(self, store: "KnowledgeStore", versioning: "KnowledgeVersioning"):
        # Dependency injection only — never instantiate collaborators internally.
        if not isinstance(store, KnowledgeStore):
            raise KnowledgeError(["repository requires a KnowledgeStore"])
        if not isinstance(versioning, KnowledgeVersioning):
            raise KnowledgeError(["repository requires a KnowledgeVersioning"])
        self._store = store
        self._versioning = versioning

    def record_version(self, version: "KnowledgeVersion") -> None:
        # Delegate persistence exclusively to storage (append-only, no overwrite,
        # no delete — enforced by the store). No shadow history is kept.
        self._store.append(version)

    def active_version(self, knowledge_item_key: str) -> "Optional[KnowledgeVersion]":
        # Read history from storage, delegate derivation to versioning.
        history = self._store.load_history(knowledge_item_key)
        return self._versioning.derive_active(history)

    def version(self, identity: "VersionIdentity") -> "KnowledgeVersion":
        # Delegate lookup to storage (fails closed with VersionNotFound).
        return self._store.load(identity)

    def history(self, knowledge_item_key: str) -> "Tuple[KnowledgeVersion, ...]":
        # Delegate to storage; no local history, filtering, or transformation.
        return self._store.load_history(knowledge_item_key)

    def exists(self, identity: "VersionIdentity") -> bool:
        return self._store.exists(identity)
