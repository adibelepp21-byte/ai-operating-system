"""
Knowledge boundary (Native Core Blueprint §12; knowledge_spec; Freeze §8/INV-7/INV-8).

Knowledge is durable, authoritative, versioned understanding, entered ONLY
through governed promotion (INV-7/8). It admits a Memory candidate solely on a
human-authorized governed promotion recorded by Governance; it is versioned
rather than edited and superseded rather than deleted (INV-7); it holds NO
authority of its own (Governance decides — 3.289 §13); and it fails closed on
any absence of authorization (PR-4).

SKELETON PHASE (Phase 3.310): this package is architecture-complete but
behavior-empty. Every surface below is an abstract contract (`@abstractmethod`
/ `...`) or a placeholder; there is NO business logic, persistence, storage,
serialization, admission, retrieval, versioning, Governance call, Memory
interaction, or Trace interaction. Concrete behavior — and the concrete Version
Model — are built in later authorized phases (the Version Model in Phase 3.311).

Module isolation (Blueprint §26): when realized, this boundary may depend only
on Memory (candidate source), Governance (promotion authorization), and an
Infrastructure storage facility beneath it — nothing else. It imports nothing
from Trace, Runtime, Agent, Workflow, Capability, Execution, Identity, or
Authentication; holds no external dependency (INV-12); authors no Trace (OQ-2).
In this skeleton phase it imports none of its permitted future dependencies —
only its own intra-package contracts.

Public surface (contracts only, no behavior):
  - models:      KnowledgeVersion, VersionIdentity, CanonicalStatus (placeholders)
  - versioning:  KnowledgeVersioning
  - storage:     KnowledgeStore
  - repository:  KnowledgeRepository
  - admission:   KnowledgeAdmission
  - retrieval:   KnowledgeRetrieval
  - exceptions:  KnowledgeError, UnauthorizedPromotion, InvalidKnowledgeVersion,
                 VersionNotFound, KnowledgeStorageUnavailable
"""

from .admission import KnowledgeAdmission
from .exceptions import (
    InvalidKnowledgeVersion,
    KnowledgeError,
    KnowledgeStorageUnavailable,
    UnauthorizedPromotion,
    VersionNotFound,
)
from .models import CanonicalStatus, KnowledgeVersion, VersionIdentity
from .repository import KnowledgeRepository
from .retrieval import KnowledgeRetrieval
from .storage import KnowledgeStore
from .versioning import KnowledgeVersioning

__all__ = [
    "KnowledgeVersion",
    "VersionIdentity",
    "CanonicalStatus",
    "KnowledgeVersioning",
    "KnowledgeStore",
    "KnowledgeRepository",
    "KnowledgeAdmission",
    "KnowledgeRetrieval",
    "KnowledgeError",
    "UnauthorizedPromotion",
    "InvalidKnowledgeVersion",
    "VersionNotFound",
    "KnowledgeStorageUnavailable",
]
