"""
T-12 Knowledge admission — BOUNDED BEHAVIOURAL EVIDENCE (ACT-CC-P6-015).

WHAT THIS MODULE IS. Evidence infrastructure produced under `ACT-CC-P6-015`
(`DEC-P6-014 = OPTION D`, `T12-D-005 = REQUIRED FOR SPECIFIED CLAUSES ONLY`) to
close the evidence gap recorded as **T12-R-003**: before this module, `admit`
and `revise` had **zero call sites repository-wide**, so no test anywhere
performed an admission. It exercises the five behaviours `ACT-CC-P6-015 §2`
authorizes, and nothing else.

WHAT THIS MODULE IS NOT (`§5`, `§18`, `§25`).
  - It is **not** canon. A passing test here is `[E] behaviour observed under a
    specified condition` — never `[E] Phase 3.289 ratified` (`§17`).
  - It does **not** ratify the Phase 3.289 admission model; ratification is a
    separate gate (`§36`).
  - It is **disposable evidence infrastructure** unless separately adopted
    (`§5`).

BOUNDARIES OBSERVED.
  - `§4` FROZEN BASELINE: `test_knowledge_conformance.py` is **not modified**,
    appended to, or imported from. This is a separate module by design (`§16`).
  - `§6` P7-F-2: the five bounded-exception sites are constructor guards in
    `InMemoryKnowledgeAdmission.__init__`, `InMemoryKnowledgeRepository.__init__`
    and `InMemoryKnowledgeRetrieval.__init__`. **No test here exercises a
    constructor guard, and no test asserts on any halt-message text.** Every
    collaborator is constructed with a well-formed argument.
  - `§12` STORAGE: the Knowledge side is assembled from the **in-memory**
    reference implementations — no `InfrastructureKnowledgeStore`, no Knowledge
    persistence. The Governance side uses the already-established
    Infrastructure→Trace→Memory→Governance test stack in a temp directory,
    because `GovernanceReview` cannot be constructed without a `StorageFacility`
    and `admission` requires a real `GovernanceReview` by `isinstance`. That
    stack is the resident convention of `governance/tests/`, not new storage
    architecture.
  - `§13` D-001: no Knowledge consumer is created. Outcomes are observed through
    the repository history that `_record_new_version` itself consults — the
    admission-side audit trail — never through `KnowledgeRetrieval`, which is
    the consumption surface D-001 placed out of scope.
  - `§14` D-003: **`validity_conditions` is never asserted on, in either
    direction.** Its architectural meaning depends on the deferred
    validity-condition catalogue, so no expectation about it is recorded here.
  - `§15` D-006: process-scoped provenance is used as-is; nothing reconstructs
    durable provenance or replays authorization state.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.knowledge.tests.test_knowledge_admission_behavioral_evidence
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from native_core.core.governance import GovernanceReview, HumanAuthority, ReviewDecision
from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.knowledge.admission import InMemoryKnowledgeAdmission
from native_core.core.knowledge.exceptions import (
    InvalidKnowledgeVersion,
    KnowledgeError,
    UnauthorizedPromotion,
)
from native_core.core.knowledge.models import KnowledgeVersion
from native_core.core.knowledge.repository import InMemoryKnowledgeRepository
from native_core.core.knowledge.storage import InMemoryKnowledgeStore
from native_core.core.knowledge.versioning import InMemoryKnowledgeVersioning
from native_core.core.memory import MemoryReader
from native_core.core.trace import TraceReader, TraceWriter, new_record


def _governance():
    """The already-established Infrastructure→Trace→Memory→Governance test stack
    (`governance/tests/` convention), in a temp directory. Returns the review
    surface and one real Memory `PromotionCandidate` derived from one Trace
    record. Creates no Knowledge persistence (`§12`)."""
    tmp = Path(tempfile.mkdtemp())
    trace_storage = LocalAppendOnlyStorage(base_dir=tmp / "trace")
    trace_storage.provision()
    gov_storage = LocalAppendOnlyStorage(base_dir=tmp / "gov")
    gov_storage.provision()
    TraceWriter(trace_storage).write(
        new_record(
            agent_definition_version="1",
            agent_instance="evidence-scope",
            runtime="rt",
            outputs={"finding": "observed-value"},
        )
    )
    review = GovernanceReview(MemoryReader(TraceReader(trace_storage)), gov_storage)
    candidates = review.pending_candidates()
    assert candidates, "the established stack must surface at least one candidate"
    return review, candidates[0]


def _knowledge():
    """The Knowledge subsystem assembled from in-memory reference implementations
    only (`§12`). Every collaborator is well-formed, so no P7-F-2 constructor
    guard is reached (`§6`)."""
    store = InMemoryKnowledgeStore()
    versioning = InMemoryKnowledgeVersioning()
    repository = InMemoryKnowledgeRepository(store, versioning)
    admission = InMemoryKnowledgeAdmission(repository, versioning)
    return admission, repository, versioning


def _approve(review, candidate, who="alice"):
    """Record one real human `approve` through the existing Governance surface.
    Introduces no authorization semantics (`§8`, `§11`)."""
    review.record_decision(
        ReviewDecision(candidate, "approve", HumanAuthority(who), "behavioural evidence")
    )


class ScopeAAuthorizedAdmission(unittest.TestCase):
    """`§7` — an authorized candidate traverses the existing admission path."""

    def test_authorized_candidate_is_admitted_as_a_first_version(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)
        self.assertTrue(review.promotion_authorized(candidate))

        version = admission.admit(candidate, review)

        self.assertIsInstance(version, KnowledgeVersion)
        # Item identity is the candidate's scope; the sequence is the base
        # ordinal. Observed outcome only — no versioning policy is asserted
        # beyond what the existing implementation produces (§9, D-002).
        self.assertEqual(version.identity.knowledge_item_key, candidate.scope)
        self.assertEqual(version.identity.version_sequence, 1)
        # Content is the candidate's observed content, captured (INV-6), frozen.
        self.assertEqual(version.content, candidate.observed_content)

    def test_admission_records_the_version_in_the_append_only_history(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)

        version = admission.admit(candidate, review)

        history = repository.history(candidate.scope)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], version)


class ScopeBUnauthorizedRejection(unittest.TestCase):
    """`§8` — an unauthorized candidate is refused, and nothing is written."""

    def test_absent_decision_is_refused_and_writes_nothing(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        # No decision recorded at all: the default is deny.
        self.assertFalse(review.promotion_authorized(candidate))

        with self.assertRaises(UnauthorizedPromotion):
            admission.admit(candidate, review)

        self.assertEqual(repository.history(candidate.scope), ())

    def test_recorded_reject_is_refused_and_writes_nothing(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        review.record_decision(
            ReviewDecision(candidate, "reject", HumanAuthority("bob"), "not admissible")
        )

        with self.assertRaises(UnauthorizedPromotion):
            admission.admit(candidate, review)

        self.assertEqual(repository.history(candidate.scope), ())

    def test_reject_after_approve_refuses_admission(self):
        """Reject is absolute at the Governance boundary; admission reflects it
        rather than deciding anything (`§8` — no added authorization semantics)."""
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)
        review.record_decision(
            ReviewDecision(candidate, "reject", HumanAuthority("bob"), "withdrawn")
        )

        with self.assertRaises(UnauthorizedPromotion):
            admission.admit(candidate, review)

        self.assertEqual(repository.history(candidate.scope), ())


class ScopeCRevisionAndNewVersion(unittest.TestCase):
    """`§9` — revision produces a new version; ordering and refusal conditions
    are those the existing implementation already exposes."""

    def test_revision_produces_a_new_version_and_retains_the_prior(self):
        review, candidate = _governance()
        admission, repository, versioning = _knowledge()
        _approve(review, candidate)

        first = admission.admit(candidate, review)
        second = admission.revise(candidate, review)

        self.assertNotEqual(first.identity, second.identity)
        self.assertEqual(second.identity.version_sequence, 2)
        history = repository.history(candidate.scope)
        self.assertEqual(len(history), 2)
        # The prior version is retained, not overwritten (INV-7).
        self.assertIn(first, history)
        self.assertIn(second, history)

    def test_supersession_ordering_is_derived_latest_is_active(self):
        """Status is derived, never stored: the greatest sequence is Active and
        the prior is therefore Superseded. No status field is asserted, because
        none exists on the record."""
        review, candidate = _governance()
        admission, repository, versioning = _knowledge()
        _approve(review, candidate)

        first = admission.admit(candidate, review)
        second = admission.revise(candidate, review)

        active = versioning.derive_active(repository.history(candidate.scope))
        self.assertEqual(active, second)
        self.assertNotEqual(active, first)

    def test_revision_without_an_existing_version_is_refused(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)

        with self.assertRaises(InvalidKnowledgeVersion):
            admission.revise(candidate, review)

        self.assertEqual(repository.history(candidate.scope), ())


class ScopeDAppendOnlyPreservation(unittest.TestCase):
    """`§10` — a conflicting re-record leaves existing admitted state intact."""

    def test_re_recording_an_admitted_identity_is_refused(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)
        version = admission.admit(candidate, review)

        with self.assertRaises(InvalidKnowledgeVersion):
            repository.record_version(version)

    def test_existing_state_is_preserved_after_a_refused_re_record(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)
        version = admission.admit(candidate, review)
        before = repository.history(candidate.scope)

        with self.assertRaises(InvalidKnowledgeVersion):
            repository.record_version(version)

        self.assertEqual(repository.history(candidate.scope), before)
        self.assertEqual(len(repository.history(candidate.scope)), 1)


class ScopeEFailClosedAdmission(unittest.TestCase):
    """`§11` — the two specified fail-closed conditions, using the existing
    interfaces. No new authorization category is created."""

    def test_non_governance_review_authorization_is_refused(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)  # authorized at Governance — irrelevant here

        with self.assertRaises(UnauthorizedPromotion):
            admission.admit(candidate, object())

        self.assertEqual(repository.history(candidate.scope), ())

    def test_non_promotion_candidate_is_refused(self):
        review, candidate = _governance()
        admission, repository, _ = _knowledge()
        _approve(review, candidate)

        with self.assertRaises(InvalidKnowledgeVersion):
            admission.admit(object(), review)

        self.assertEqual(repository.history(candidate.scope), ())

    def test_both_fail_closed_halts_are_knowledge_errors(self):
        """Halt taxonomy observed at the behavioural path. Type only — no
        message text is asserted (`§6`)."""
        self.assertTrue(issubclass(UnauthorizedPromotion, KnowledgeError))
        self.assertTrue(issubclass(InvalidKnowledgeVersion, KnowledgeError))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
