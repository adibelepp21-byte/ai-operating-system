"""
Phase 7 Memory lifecycle conformance — `E7-01`, `E7-02`, `E7-04`, `E7-05`.

`E7-03` needs a RUNNING Runtime and an Agent, so it lives with the consumer
evidence (`consumers/tests/test_memory_agent_runtime.py`). Everything provable
inside the Memory boundary is proved here.

`ACT-CC-P7-002 §15.3` requires negative controls for every material boundary and
forbids *"assertions that cannot fail."* So each criterion is asserted in both
directions: the lawful operation works, **and** the unlawful one is actually
refused.
"""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

from native_core.core.memory import (
    ELIGIBLE_STATES,
    InvalidMemoryItem,
    InvalidMemoryTransition,
    MemoryCandidate,
    MemoryIdentity,
    MemoryItem,
    MemoryNotFound,
    MemoryProvenance,
    MemoryRecord,
    MemoryState,
    PromotionCandidate,
    create_memory_subsystem,
)

_MEMORY_DIR = Path(__file__).resolve().parent.parent


def _subsystem(rule=None):
    return create_memory_subsystem(rule)


def _candidate(key="k", payload="v", source="agent-instance"):
    return MemoryCandidate(key=key, payload=payload, provenance=MemoryProvenance(source))


class E701Representation(unittest.TestCase):
    """`E7-01` — representation and candidate formation."""

    def test_a_memory_carries_all_five_required_elements(self):
        sub = _subsystem()

        item = sub.lifecycle.admit(_candidate())

        self.assertIsInstance(item.identity, MemoryIdentity)   # 1 identity
        self.assertEqual("v", item.payload)                    # 2 payload
        self.assertIsInstance(item.state, MemoryState)         # 3 lifecycle state
        self.assertEqual("agent-instance", item.provenance.source)  # 4 provenance
        self.assertIsInstance(item.recorded_at, int)           # 5 lifecycle metadata
        self.assertIsInstance(item.updated_at, int)

    def test_identity_is_stable_across_the_lifecycle(self):
        """`E7-05.7` — identity survives every transition."""
        sub = _subsystem()
        item = sub.lifecycle.admit(_candidate())
        before = item.identity

        expired = sub.lifecycle.expire("k")

        self.assertEqual(before, expired.identity)

    def test_information_can_become_a_candidate(self):
        """`E7-01.7`. A Trace-derived observation is natural Information."""
        record = MemoryRecord(scope="inst-1", content={"seen": "x"})

        candidate = _subsystem().lifecycle.form_candidate(
            key="obs", payload=record.content, source="trace-derivation"
        )

        self.assertIsInstance(candidate, MemoryCandidate)
        self.assertEqual("trace-derivation", candidate.provenance.source)

    def test_a_candidate_carries_no_lifecycle_state_or_identity(self):
        """`E7-01.9` — forming one grants no admission authority, structurally."""
        candidate = _candidate()

        self.assertFalse(hasattr(candidate, "state"))
        self.assertFalse(hasattr(candidate, "identity"))

    def test_a_memory_is_immutable(self):
        item = _subsystem().lifecycle.admit(_candidate())

        with self.assertRaises(Exception):
            item.state = MemoryState.EXPIRED

    def test_a_memory_without_provenance_is_refused(self):
        with self.assertRaises(InvalidMemoryItem):
            MemoryItem(
                identity=MemoryIdentity("k", 1), payload="v",
                state=MemoryState.RETAINED, provenance="not-provenance",
                recorded_at=1, updated_at=1,
            )

    def test_an_unnamed_provenance_source_is_refused(self):
        with self.assertRaises(InvalidMemoryItem):
            MemoryProvenance("   ")

    def test_a_candidate_without_a_key_is_refused(self):
        with self.assertRaises(InvalidMemoryItem):
            MemoryCandidate(key="  ", payload="v", provenance=MemoryProvenance("s"))

    def test_an_ordinal_is_one_based(self):
        with self.assertRaises(InvalidMemoryItem):
            MemoryIdentity("k", 0)

    def test_payload_is_deeply_frozen(self):
        item = _subsystem().lifecycle.admit(_candidate(payload={"a": [1, 2]}))

        self.assertIsInstance(item.payload["a"], tuple)


class E702AdmissionAndRetention(unittest.TestCase):
    """`E7-02` — admission decided at the boundary, retention lifecycle-governed."""

    def test_a_candidate_becomes_retained_memory(self):
        item = _subsystem().lifecycle.admit(_candidate())

        self.assertEqual(MemoryState.RETAINED, item.state)

    def test_candidate_and_admitted_memory_are_distinguishable(self):
        """The distinction `E7-02` requires the boundary to demonstrate."""
        sub = _subsystem()
        candidate = _candidate()
        self.assertIsNone(sub.retrieval.active("k"))  # proposed: nothing retained

        sub.lifecycle.admit(candidate)

        self.assertIsNotNone(sub.retrieval.active("k"))  # admitted: retained

    def test_the_retention_rule_can_refuse(self):
        """`E7-02.3` — retention is governed, not automatic."""
        sub = _subsystem(rule=lambda c: c.key != "rejected")

        self.assertIsNone(sub.lifecycle.admit(_candidate(key="rejected")))
        self.assertIsNone(sub.retrieval.active("rejected"))

    def test_a_refused_candidate_produces_no_memory_at_all(self):
        sub = _subsystem(rule=lambda c: False)

        sub.lifecycle.admit(_candidate())

        self.assertEqual((), sub.retrieval.history("k"))

    def test_only_a_candidate_can_be_admitted(self):
        with self.assertRaises(InvalidMemoryItem):
            _subsystem().lifecycle.admit("just a string")

    def test_admission_is_a_boundary_method_not_a_candidate_capability(self):
        """`E7-02.4`/`.5`: no caller holding a Candidate can admit it."""
        for name in ("admit", "retain", "expire", "invalidate", "update"):
            self.assertFalse(hasattr(_candidate(), name))

    def test_the_lifecycle_holds_no_agent_execution_or_governance_collaborator(self):
        sub = _subsystem()

        held = {type(v).__name__ for v in vars(sub.lifecycle).values()}

        for forbidden in ("Agent", "Execution", "GovernanceReview", "HumanAuthority"):
            self.assertNotIn(forbidden, held)


class E704UpdateAndConsolidation(unittest.TestCase):
    """`E7-04` — explicit, lifecycle-integrity-preserving evolution."""

    def test_update_supersedes_and_retains_the_predecessor(self):
        sub = _subsystem()
        first = sub.lifecycle.admit(_candidate(payload="v1"))

        second = sub.lifecycle.update("k", "v2")

        self.assertEqual("v2", sub.retrieval.active("k").payload)
        self.assertEqual(MemoryState.SUPERSEDED, sub.retrieval.history("k")[0].state)
        self.assertEqual(first.identity, second.supersedes)

    def test_the_predecessor_payload_is_not_destroyed(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate(payload="v1"))

        sub.lifecycle.update("k", "v2")

        self.assertEqual("v1", sub.retrieval.history("k")[0].payload)

    def test_no_reference_dangles_after_update(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())
        successor = sub.lifecycle.update("k", "v2")

        referenced = sub.store.get(successor.supersedes)

        self.assertEqual(MemoryState.SUPERSEDED, referenced.state)

    def test_consolidation_supersedes_every_source(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate(key="a", payload=1))
        sub.lifecycle.admit(_candidate(key="b", payload=2))

        merged = sub.lifecycle.consolidate(("a", "b"), into_key="ab", payload=3)

        self.assertEqual(MemoryState.RETAINED, merged.state)
        self.assertIsNone(sub.retrieval.active("a"))
        self.assertIsNone(sub.retrieval.active("b"))

    def test_consolidation_records_its_sources(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate(key="a"))
        sub.lifecycle.admit(_candidate(key="b"))

        merged = sub.lifecycle.consolidate(("a", "b"), "ab", "merged")

        self.assertEqual("consolidation", merged.provenance.source)
        self.assertEqual(2, len(merged.provenance.detail))

    def test_partial_consolidation_never_happens(self):
        """All-or-nothing: an ineligible source leaves every source untouched."""
        sub = _subsystem()
        sub.lifecycle.admit(_candidate(key="a"))

        with self.assertRaises(MemoryNotFound):
            sub.lifecycle.consolidate(("a", "missing"), "ab", "merged")

        self.assertIsNotNone(sub.retrieval.active("a"))  # untouched
        self.assertEqual((), sub.retrieval.history("ab"))  # nothing created

    def test_consolidating_nothing_is_refused(self):
        with self.assertRaises(InvalidMemoryTransition):
            _subsystem().lifecycle.consolidate((), "ab", "x")

    def test_updating_an_expired_memory_is_refused(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())
        sub.lifecycle.expire("k")

        with self.assertRaises(InvalidMemoryTransition):
            sub.lifecycle.update("k", "v2")

    def test_updating_an_unknown_key_is_refused(self):
        with self.assertRaises(MemoryNotFound):
            _subsystem().lifecycle.update("nope", "v")


class E705ExpiryInvalidationIntegrity(unittest.TestCase):
    """`E7-05` — expiry, invalidation, eligibility and lifecycle integrity."""

    def test_memory_can_expire(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())

        self.assertEqual(MemoryState.EXPIRED, sub.lifecycle.expire("k").state)

    def test_memory_can_be_invalidated(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())

        self.assertEqual(MemoryState.INVALIDATED, sub.lifecycle.invalidate("k").state)

    def test_expired_memory_is_not_retrievable_as_active(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())
        sub.lifecycle.expire("k")

        self.assertIsNone(sub.retrieval.active("k"))

    def test_invalidated_memory_is_not_retrievable_as_active(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())
        sub.lifecycle.invalidate("k")

        self.assertIsNone(sub.retrieval.active("k"))

    def test_retrieval_does_not_fall_back_to_a_superseded_version(self):
        """The failure `E7-05.3` names: an expired newest must not resurrect an
        older version."""
        sub = _subsystem()
        sub.lifecycle.admit(_candidate(payload="v1"))
        sub.lifecycle.update("k", "v2")
        sub.lifecycle.expire("k")

        self.assertIsNone(sub.retrieval.active("k"))

    def test_expiry_and_invalidation_are_distinct_states(self):
        self.assertNotEqual(MemoryState.EXPIRED, MemoryState.INVALIDATED)

    def test_only_retained_memory_is_eligible(self):
        self.assertEqual((MemoryState.RETAINED,), ELIGIBLE_STATES)

    def test_an_expired_memory_cannot_be_resurrected(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())
        expired = sub.lifecycle.expire("k")

        with self.assertRaises(InvalidMemoryTransition):
            expired.transition_to(MemoryState.RETAINED, 99)

    def test_expiring_an_already_expired_memory_is_refused(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())
        sub.lifecycle.expire("k")

        with self.assertRaises(InvalidMemoryTransition):
            sub.lifecycle.expire("k")

    def test_a_transition_cannot_move_backwards_in_sequence(self):
        sub = _subsystem()
        item = sub.lifecycle.admit(_candidate())

        with self.assertRaises(InvalidMemoryTransition):
            item.transition_to(MemoryState.EXPIRED, item.updated_at - 1)

    def test_the_lifecycle_sequence_is_monotonic(self):
        sub = _subsystem()
        a = sub.lifecycle.admit(_candidate(key="a"))
        b = sub.lifecycle.admit(_candidate(key="b"))

        self.assertLess(a.recorded_at, b.recorded_at)

    def test_eligible_keys_excludes_ineligible_memory(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate(key="live"))
        sub.lifecycle.admit(_candidate(key="dead"))
        sub.lifecycle.invalidate("dead")

        self.assertEqual(("live",), sub.retrieval.eligible_keys())

    def test_retrieval_is_deterministic_across_repeated_requests(self):
        """`E7-03.2`, provable without a Runtime: no clock, no randomness."""
        sub = _subsystem()
        sub.lifecycle.admit(_candidate())

        self.assertEqual(sub.retrieval.active("k"), sub.retrieval.active("k"))

    def test_history_is_ordered_oldest_first(self):
        sub = _subsystem()
        sub.lifecycle.admit(_candidate(payload="v1"))
        sub.lifecycle.update("k", "v2")

        history = sub.retrieval.history("k")

        self.assertEqual(["v1", "v2"], [i.payload for i in history])


class MemoryIsNotKnowledge(unittest.TestCase):
    """`FD-P7-001 §10` — the distinction the lifecycle must not blur."""

    def test_the_lifecycle_exposes_no_knowledge_promotion(self):
        sub = _subsystem()

        for name in ("promote", "promotion", "knowledge", "authorize", "approve"):
            self.assertFalse(hasattr(sub.lifecycle, name), name)

    def test_the_knowledge_promotion_candidate_is_untouched(self):
        """`PromotionCandidate` remains the Knowledge-facing observation with the
        exact fields its own conformance suite pins."""
        import dataclasses

        fields = {f.name for f in dataclasses.fields(PromotionCandidate)}

        self.assertEqual({"scope", "observed_content", "occurrence_count"}, fields)

    def test_an_admitted_memory_carries_no_knowledge_status(self):
        item = _subsystem().lifecycle.admit(_candidate())

        for name in ("canonical_status", "knowledge_state", "promoted"):
            self.assertFalse(hasattr(item, name), name)

    def test_the_memory_boundary_imports_no_knowledge_or_governance(self):
        offenders = []
        for py in _MEMORY_DIR.glob("*.py"):
            tree = ast.parse(py.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                mods = ([a.name for a in node.names] if isinstance(node, ast.Import)
                        else [node.module or ""] if isinstance(node, ast.ImportFrom)
                        else [])
                for m in mods:
                    if {"knowledge", "governance", "runtime", "agent"} & set(m.split(".")):
                        offenders.append((py.name, m))

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
