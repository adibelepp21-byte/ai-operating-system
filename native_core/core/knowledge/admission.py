"""
Knowledge admission — abstract contract (Phase 3.315) + in-memory reference
implementation (Phase 3.321), integrated with the Memory promotion candidate
(Phase 3.326) and the Governance authorization surface (Phase 3.327, Option B).
Blueprint §5/§12; knowledge_spec §5/§7/§10/§11; Phase 3.289 §2/§4/§13; Phase
3.306; Phase 3.308 B2/B7/B8/B10; Phase 3.309 I-3309-02; INV-8; PR-3/PR-4; §6.2
invariant 2.

The abstract `KnowledgeAdmission` is the CERTIFIED contract (Phase 3.315 / 3.317)
and is UNCHANGED. `InMemoryKnowledgeAdmission` records the outcome of an
ALREADY-MADE, human-authorized governed promotion. It decides nothing
(Governance remains the sole authority — INV-8; §6.2 invariant 2), evaluates no
candidate, allocates no identity itself, and stores no record itself.

Governance integration (Phase 3.327 — Option B): authorization is the canonical
frozen mechanism `GovernanceReview.promotion_authorized(candidate) -> bool`
(Phase 3.289 §4). There is no standalone "GovernanceApproval" object (it does not
exist in the frozen architecture, and trusting a bare `ReviewDecision` would
reintroduce F-G1). Admission is handed a `GovernanceReview` (the frozen
authorization surface), asks it to verify the candidate's promotion, and admits
IFF the provenance-verified result is `True`. Admission imports ONLY
`GovernanceReview` from Governance; it never constructs approvals, never records
decisions, never reads Governance's internal decision state, and never decides —
all authority stays in Governance (F-G1/F-H1 preserved).

Memory integration (Phase 3.326): the candidate is the canonical Memory
`PromotionCandidate` (Memory's frozen public object — Phase 3.289 §2), consumed
across the sanctioned Knowledge → Memory edge. Memory owns it; Knowledge reads
only its frozen public fields (`scope`, `observed_content`), uses `occurrence_count`
for nothing (PR-3), and never mutates Memory.

Orchestration (pure delegation): identity → `KnowledgeVersioning.next_version_identity`;
persistence → `KnowledgeRepository.record_version`; a new immutable
`KnowledgeVersion` is built per admission. Admission never derives Active, never
writes status, never mutates or overwrites a prior version.

Dependencies (injected): `KnowledgeRepository`, `KnowledgeVersioning`. Imports
`models`, `repository`, `versioning`, `exceptions` from THIS package; the frozen
`PromotionCandidate` from Memory; and the frozen `GovernanceReview` from
Governance — the two sanctioned external edges (Blueprint §12; knowledge_spec §7;
Phase 3.289 §13). Imports nothing from Trace, Infrastructure, Runtime, Agent,
Workflow, or Capability; holds no external dependency (INV-12); authors no Trace
(OQ-2). Stdlib only. No globals, singleton, registry, wrapper, adapter, or
service locator.
"""

from __future__ import annotations

from typing import Tuple

import abc

from ..governance import GovernanceReview
from ..memory import PromotionCandidate
from .exceptions import InvalidKnowledgeVersion, KnowledgeError, UnauthorizedPromotion
from .models import KnowledgeVersion
from .repository import KnowledgeRepository
from .versioning import KnowledgeVersioning


class KnowledgeAdmission(abc.ABC):
    """Records the durable authoritative outcome of an authorized promotion.
    Decides nothing (INV-8; §6.2 invariant 2)."""

    @abc.abstractmethod
    def admit(self, candidate: "PromotionCandidate", authorization: "GovernanceReview") -> "KnowledgeVersion":
        """Record a NEW immutable Active Knowledge Version for `candidate` iff
        Governance authorizes its promotion; otherwise fail closed."""
        ...

    @abc.abstractmethod
    def revise(self, candidate: "PromotionCandidate", authorization: "GovernanceReview") -> "KnowledgeVersion":
        """Record a governed revision (NEW immutable version; prior retained and
        derived Superseded) under the same Governance authorization."""
        ...


class InMemoryKnowledgeAdmission(KnowledgeAdmission):
    """Reference implementation of the admission orchestration over injected
    repository + versioning. Pure delegation; holds no state beyond its injected
    collaborators; decides nothing and stores nothing itself."""

    def __init__(self, repository: "KnowledgeRepository", versioning: "KnowledgeVersioning"):
        # Dependency injection only — never instantiate collaborators internally.
        if not isinstance(repository, KnowledgeRepository):
            raise KnowledgeError(["admission requires a KnowledgeRepository"])
        if not isinstance(versioning, KnowledgeVersioning):
            raise KnowledgeError(["admission requires a KnowledgeVersioning"])
        self._repository = repository
        self._versioning = versioning

    def admit(self, candidate: "PromotionCandidate", authorization: "GovernanceReview") -> "KnowledgeVersion":
        return self._record_new_version(candidate, authorization, require_existing=False)

    def revise(self, candidate: "PromotionCandidate", authorization: "GovernanceReview") -> "KnowledgeVersion":
        # A revision supersedes an existing version; require one to exist.
        return self._record_new_version(candidate, authorization, require_existing=True)

    # --- orchestration (private) ---

    def _record_new_version(
        self, candidate: "PromotionCandidate", authorization: "GovernanceReview", require_existing: bool
    ) -> "KnowledgeVersion":
        # Authorization surface must be exactly the canonical Governance object.
        if not isinstance(authorization, GovernanceReview):
            raise UnauthorizedPromotion(
                "admission requires a GovernanceReview authorization surface"
            )
        # M2/M3: read the canonical Memory PromotionCandidate's frozen content;
        # never evaluate it, never inspect internals, never mutate Memory.
        item_key, content = self._read_candidate(candidate)
        # Consume Governance's provenance-verified authorization signal, read-only
        # (called exactly once). Governance decides; admission only reflects it.
        # Fail closed on anything but an affirmative True (PR-4; §6.2 invariant 2).
        if authorization.promotion_authorized(candidate) is not True:
            raise UnauthorizedPromotion(
                "Governance did not authorize this candidate's promotion"
            )
        # Existing identities for this item (from the repository's append-only
        # history) — input to the versioning delegation only.
        existing = tuple(v.identity for v in self._repository.history(item_key))
        if require_existing and not existing:
            raise InvalidKnowledgeVersion(
                "revise requires an existing version to supersede"
            )
        # Delegate identity allocation exclusively to versioning.
        identity = self._versioning.next_version_identity(item_key, existing)
        # Build a NEW immutable version; never edit a prior one.
        version = KnowledgeVersion(identity=identity, content=content)
        # Delegate persistence exclusively to the repository (append-only).
        self._repository.record_version(version)
        return version

    @staticmethod
    def _read_candidate(candidate: "PromotionCandidate") -> "Tuple[str, object]":
        """Read the canonical Memory `PromotionCandidate`'s frozen public fields
        (Phase 3.289 §2). Fail closed if the input is not a `PromotionCandidate`
        (M10) — duck typing removed. `scope` identifies the Knowledge item;
        `observed_content` is the version content. The non-gating
        `occurrence_count` is read for nothing (PR-3)."""
        if not isinstance(candidate, PromotionCandidate):
            raise InvalidKnowledgeVersion(
                "admission requires a Memory PromotionCandidate"
            )
        return candidate.scope, candidate.observed_content
