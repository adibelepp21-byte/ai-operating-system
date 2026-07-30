"""
Knowledge versioning — abstract contract (Phase 3.314) + in-memory reference
implementation (Phase 3.320). Blueprint §12; knowledge_spec §4/§6; Phase 3.306
D1/D2; Phase 3.308 B3/B4; Phase 3.309 P4; INV-7.

The abstract `KnowledgeVersioning` is the CERTIFIED contract (Phase 3.314 / 3.317)
and is UNCHANGED here. `InMemoryKnowledgeVersioning` is a pure, deterministic
**reference implementation** of the rules governing version relationships —
identity interpretation, sequencing, and canonical-status derivation. It exists
to prove the contract can be realized without violating the Constitution, Freeze,
dependency rules, authority rules, or lifecycle rules.

Versioning owns RULES ONLY: deterministic version derivation, chain validation,
and sequence calculation. It owns no authority, governance, admission,
repository, storage, persistence, Memory, Trace, or Runtime. It operates purely
on version records/identities supplied by the caller — it inspects no storage and
no repository, generates no UUID/timestamp/randomness, hashes nothing, caches
nothing, and holds no mutable state.

Canonical status is DERIVED (Phase 3.306 D2): the latest governed-admitted
version of an item — the one with the greatest `version_sequence` — is Active;
all priors are Superseded. Status is never stored on or written to a version
(the `KnowledgeVersion` model has no status field).

Dependencies: `models` and `exceptions` from THIS package only. Imports nothing
from Memory, Governance, Trace, Infrastructure, Runtime, Agent, Workflow,
Capability, Execution, Identity, Authentication, or the sibling
repository/storage/admission/retrieval modules; holds no external dependency
(INV-12); authors no Trace (OQ-2). Stdlib only.
"""

from __future__ import annotations

import abc
from typing import Optional, Sequence, Tuple

from .exceptions import InvalidKnowledgeVersion
from .models import KnowledgeVersion, VersionIdentity


class KnowledgeVersioning(abc.ABC):
    """Passive contract for the rules governing Knowledge version relationships:
    identity interpretation, sequencing, and canonical-status derivation.

    Operates purely on version records supplied by the caller — it inspects no
    storage and no repository. Concrete realizations (see
    `InMemoryKnowledgeVersioning`) remain pure and deterministic."""

    @abc.abstractmethod
    def derive_active(self, item_versions: "Sequence[KnowledgeVersion]") -> "Optional[KnowledgeVersion]":
        """Derive the single **Active** version for one item from its supplied
        versions — the latest governed-admitted (greatest sequence; Phase 3.306
        D2) — or `None` if none. Status is DERIVED, never stored."""
        ...

    @abc.abstractmethod
    def derive_history(self, item_versions: "Sequence[KnowledgeVersion]") -> "Tuple[KnowledgeVersion, ...]":
        """Derive the item's version history, read-only, preserving insertion
        order (oldest→newest) — including superseded versions (INV-7). No
        reorder, no filter, no mutation."""
        ...

    @abc.abstractmethod
    def next_version_identity(
        self, knowledge_item_key: str, existing: "Sequence[VersionIdentity]"
    ) -> "VersionIdentity":
        """Compute the next `(knowledge_item_key, version_sequence)` identity for
        an item from its existing identities — a monotonic governed ordinal (Phase
        3.306 D1). Pure calculation; no UUID/timestamp/storage inspection."""
        ...

    @abc.abstractmethod
    def validate_version_chain(self, item_versions: "Sequence[KnowledgeVersion]") -> None:
        """Validate that a supplied set of an item's versions forms a well-formed
        chain (single item, unique + strictly increasing sequences, exactly one
        Active derivable, append-only consistent). Raise on violation (fail
        closed); mutate nothing."""
        ...


class InMemoryKnowledgeVersioning(KnowledgeVersioning):
    """Pure, deterministic reference implementation of the versioning rules.

    Holds no state and no cache; every method is a pure function of its inputs.
    It derives Active by greatest sequence, preserves insertion order for
    history, computes the next sequence as `max(existing)+1` (base 1), and
    validates a chain structurally — failing closed on any violation, never
    repairing or mutating. It writes no status, allocates no identifier beyond
    the pure next-sequence calculation, and touches no storage/repository."""

    #: The first version sequence for a brand-new Knowledge item.
    BASE_SEQUENCE = 1

    def derive_active(self, item_versions: "Sequence[KnowledgeVersion]") -> "Optional[KnowledgeVersion]":
        versions = tuple(item_versions)
        if not versions:
            return None
        # Latest governed-admitted = greatest version_sequence (Phase 3.306 D2).
        # Deterministic: max returns the first occurrence on a tie; a valid chain
        # has unique sequences (see validate_version_chain), so there is no tie.
        return max(versions, key=lambda v: v.identity.version_sequence)

    def derive_history(self, item_versions: "Sequence[KnowledgeVersion]") -> "Tuple[KnowledgeVersion, ...]":
        # Preserve insertion order exactly; no reorder, no filter, no mutation.
        return tuple(item_versions)

    def next_version_identity(
        self, knowledge_item_key: str, existing: "Sequence[VersionIdentity]"
    ) -> "VersionIdentity":
        if not isinstance(knowledge_item_key, str) or not knowledge_item_key.strip():
            raise InvalidKnowledgeVersion("knowledge_item_key must be a non-empty string")
        sequences = [
            vid.version_sequence for vid in existing
            if vid.knowledge_item_key == knowledge_item_key
        ]
        next_seq = (max(sequences) + 1) if sequences else self.BASE_SEQUENCE
        return VersionIdentity(knowledge_item_key, next_seq)

    def validate_version_chain(self, item_versions: "Sequence[KnowledgeVersion]") -> None:
        versions = tuple(item_versions)
        if not versions:
            return None  # an empty chain is vacuously well-formed
        keys = {v.identity.knowledge_item_key for v in versions}
        if len(keys) != 1:
            raise InvalidKnowledgeVersion(
                f"a version chain must belong to a single item; found keys {sorted(keys)!r}"
            )
        seqs = [v.identity.version_sequence for v in versions]
        if len(set(seqs)) != len(seqs):
            raise InvalidKnowledgeVersion(f"duplicate version_sequence in chain: {seqs!r}")
        # Append-only consistency: supplied (append) order is strictly increasing.
        if any(seqs[i] >= seqs[i + 1] for i in range(len(seqs) - 1)):
            raise InvalidKnowledgeVersion(
                f"version chain is not strictly increasing in append order: {seqs!r}"
            )
        # Exactly one Active derivable (guaranteed by unique, strictly-increasing
        # sequences) — assert the invariant explicitly, fail closed otherwise.
        if self.derive_active(versions) is None:
            raise InvalidKnowledgeVersion("no Active version derivable from a non-empty chain")
        return None
