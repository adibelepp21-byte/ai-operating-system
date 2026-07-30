"""
Knowledge Version Domain Model (Blueprint §12; knowledge_spec §4/§6; Domain
Model §6; Phase 3.289 §8/§14; Phase 3.306 D1/D2; Phase 3.308 B4; INV-7).

The canonical immutable domain objects of the Knowledge subsystem. This module
holds **only** the domain model — no repository, storage, admission, retrieval,
versioning-allocation, or persistence behavior, and no Governance/Memory/Trace/
Infrastructure interaction (Phase 3.311 scope).

Field grounding (verified directly against frozen sources):
  - A Knowledge Version's **content** and its governed **validity conditions**
    are fixed at admission (Phase 3.289 §14; knowledge_spec §6/§22).
  - Version **identity** is `(knowledge_item_key, version_sequence)` — a
    governance-ordered pair, authority- and content-independent (Phase 3.306 D1).
  - **Canonical status** (Active/Superseded) is **DERIVED from the append-only
    governed-decision sequence — NOT a mutable field edited on a version**
    (Phase 3.306 D2; Phase 3.309 P4). It is therefore deliberately NOT a stored
    field on `KnowledgeVersion`: storing it would require mutating or re-creating
    an immutable prior version on supersession, which the frozen architecture
    forbids. `CanonicalStatus` is defined here as the enum the derivation layer
    (a later authorized phase) assigns; the immutable version records carry
    identity + content + validity conditions only.

Structural invariants enforced (structural only — no business logic):
  immutable after construction · no setters · no mutable collections · deeply
  immutable nested content · no hidden caches · no lazy loading · no runtime
  mutation (INV-7; 3.308 B4).

Dependencies: none outside the Knowledge package — stdlib only (dataclasses,
enum, types, typing) plus this package's own exceptions. No external dependency
(INV-12); no Trace/Memory/Governance/Infrastructure reference (they are wired
only in later behavior phases).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

from .exceptions import InvalidKnowledgeVersion


def _freeze(value: Any) -> Any:
    """Deeply immutable snapshot: mapping -> read-only mapping, list/tuple ->
    tuple, recursively; scalars unchanged. Structural immutability enforcement
    only (precedent: TraceRecord/MemoryRecord). Runs once at construction; it
    computes no domain logic and mutates nothing thereafter."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


class CanonicalStatus(Enum):
    """The binary canonical status of a Knowledge Version (Domain Model §6;
    knowledge_spec §4; Phase 3.289 §8). Exactly two designations — no third
    state, no trust score, confidence, ranking, or probability (deferred by the
    Domain Model).

    `CANDIDATE` is intentionally absent: a candidate belongs to Memory, not
    Knowledge (Phase 3.289 §2). This status is **derived** by a later authorized
    phase from the append-only sequence (Phase 3.306 D2); it is not stored on a
    version record."""

    ACTIVE = "active"
    SUPERSEDED = "superseded"


@dataclass(frozen=True, order=True)
class VersionIdentity:
    """Immutable identity of a Knowledge Version: `(knowledge_item_key,
    version_sequence)` (Phase 3.306 D1).

    Frozen, hashable, and comparable. Carries **no** generated UUID, timestamp,
    storage identifier, or runtime metadata — it encodes only ownership-scoped
    identity and governed ordering (Phase 3.306 D1). The lexical form and the
    allocation of `version_sequence` are reserved to a later phase; this model
    validates structure only (it does not allocate)."""

    knowledge_item_key: str
    version_sequence: int

    def __post_init__(self):
        if not isinstance(self.knowledge_item_key, str) or not self.knowledge_item_key.strip():
            raise InvalidKnowledgeVersion("knowledge_item_key must be a non-empty string")
        # bool is a subclass of int; reject it explicitly.
        if not isinstance(self.version_sequence, int) or isinstance(self.version_sequence, bool):
            raise InvalidKnowledgeVersion("version_sequence must be an integer")
        if self.version_sequence < 0:
            raise InvalidKnowledgeVersion("version_sequence must be a non-negative integer")


@dataclass(frozen=True)
class KnowledgeVersion:
    """One immutable Knowledge Version — its identity, its content, and its
    governed validity conditions, all fixed at admission (Phase 3.289 §14;
    knowledge_spec §6; INV-7).

    Deeply immutable: `content` and `validity_conditions` are frozen recursively
    at construction, so no nested collection is mutable. There is no status
    field (status is derived — Phase 3.306 D2), and no forbidden metadata
    (no uuid/hash/checksum/signature/timestamp/created_at/updated_at/author/
    confidence/trust/probability/ranking/score, and no Trace/Memory/Governance
    pointer or object). `content` is a **captured value** (INV-6 capture,
    don't reference), never a pointer to Memory or Trace."""

    identity: VersionIdentity
    content: Any
    validity_conditions: Mapping = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self):
        if not isinstance(self.identity, VersionIdentity):
            raise InvalidKnowledgeVersion("identity must be a VersionIdentity")
        if self.content is None:
            raise InvalidKnowledgeVersion("a KnowledgeVersion requires content")
        if not isinstance(self.validity_conditions, Mapping):
            raise InvalidKnowledgeVersion("validity_conditions must be a mapping")
        # Deep-freeze content-bearing fields (structural immutability, INV-7).
        object.__setattr__(self, "content", _freeze(self.content))
        object.__setattr__(self, "validity_conditions", _freeze(dict(self.validity_conditions)))

    def __hash__(self) -> int:
        """Hash by identity. Version identity is globally unique (Phase 3.306
        D1), so it fully determines the version; this keeps a version hashable
        even when its captured content contains mappings."""
        return hash(self.identity)
