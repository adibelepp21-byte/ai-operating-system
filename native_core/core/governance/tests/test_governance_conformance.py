"""
Governance conformance tests (Blueprint §27; governance_spec; Constitution §3/§6.2; Freeze INV-5/8; PR-3/PR-4).

Each test asserts a governance property:
  - human authority is required; automation cannot decide (§6.2 invariant 2).
  - no automatic approval / rejection / promotion (PR-3).
  - fail closed: default deny; invalid decisions record nothing (PR-4).
  - a human `reject` is absolute.
  - Governance never creates Knowledge, never mutates Memory, never mutates Trace.
  - decisions are recorded append-only and captured in full (INV-6 discipline).
  - dependency rules: only Memory + Infrastructure; no forbidden import.
  - determinism + round-trip of recorded decisions.

Standard-library `unittest` only.
Run: python -m unittest native_core.core.governance.tests.test_governance_conformance
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

from native_core.core import governance as gov_pkg
from native_core.core.governance import (
    GovernanceError,
    GovernanceReview,
    HumanAuthority,
    ReviewDecision,
    validate_decision,
)
from native_core.core.governance.authority import InvalidAuthority
from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.memory import MemoryReader, PromotionCandidate
from native_core.core.trace import TraceReader, TraceWriter, new_record

_GOV_DIR = Path(gov_pkg.__file__).resolve().parent

_FORBIDDEN_EXTERNAL = {
    "requests", "urllib", "http", "socket", "openai", "anthropic", "torch",
    "sqlalchemy", "sqlite3", "redis", "numpy", "pandas", "grpc", "boto3",
}
# Governance may depend only on Infrastructure, Trace, Memory. Never on the
# subsystems it directs/precedes, nor legacy.
_FORBIDDEN_INTERNAL = {
    "knowledge", "capability", "skill", "workflow", "agent", "runtime",
    "optimization", "execution",
}


def _stack():
    """Build a real Infrastructure→Trace→Memory→Governance stack in temp dirs."""
    tmp = Path(tempfile.mkdtemp())
    trace_storage = LocalAppendOnlyStorage(base_dir=tmp / "trace"); trace_storage.provision()
    gov_storage = LocalAppendOnlyStorage(base_dir=tmp / "gov"); gov_storage.provision()
    writer = TraceWriter(trace_storage)
    writer.write(new_record(agent_definition_version="1", agent_instance="inst-1",
                            runtime="rt", outputs={"finding": "X"}))
    reader = MemoryReader(TraceReader(trace_storage))
    review = GovernanceReview(reader, gov_storage)
    return review, gov_storage, trace_storage


def _candidate(review):
    cands = review.pending_candidates()
    assert cands, "expected at least one candidate"
    return cands[0]


class TestSurfaceOnly(unittest.TestCase):
    def test_pending_candidates_are_memory_observations(self):
        review, _, _ = _stack()
        cands = review.pending_candidates()
        self.assertTrue(all(isinstance(c, PromotionCandidate) for c in cands))
        self.assertEqual(cands[0].scope, "inst-1")


class TestHumanAuthorityRequired(unittest.TestCase):
    def test_automation_cannot_supply_authority(self):
        # An authority requires a real human identity; empty/blank is rejected.
        for bad in ("", "   "):
            with self.assertRaises(InvalidAuthority):
                HumanAuthority(bad)

    def test_decision_without_human_authority_is_invalid(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        # Bypass the HumanAuthority type entirely -> validation rejects it.
        bogus = ReviewDecision(candidate=cand, decision="approve", authority=None, rationale="r")  # type: ignore[arg-type]
        self.assertIn("HumanAuthority", " ".join(validate_decision(bogus)))
        with self.assertRaises(GovernanceError):
            review.record_decision(bogus)


class TestNoAutomaticDecision(unittest.TestCase):
    def test_default_is_deny_no_promotion(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        # No decision recorded -> promotion NOT authorized (fail closed).
        self.assertFalse(review.promotion_authorized(cand))

    def test_approve_requires_recorded_human_decision(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        self.assertFalse(review.promotion_authorized(cand))
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("alice"), "looks right"))
        self.assertTrue(review.promotion_authorized(cand))

    def test_no_auto_approve_or_reject_method(self):
        for name in dir(GovernanceReview):
            self.assertNotIn(name, ("approve", "reject", "auto_approve", "auto_promote", "decide"))


class TestRejectAbsolute(unittest.TestCase):
    def test_reject_overrides_approve_regardless_of_order(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("alice"), "ok"))
        review.record_decision(ReviewDecision(cand, "reject", HumanAuthority("bob"), "not ok"))
        self.assertFalse(review.promotion_authorized(cand))  # reject absolute


class TestFailClosed(unittest.TestCase):
    def test_invalid_decision_value_records_nothing(self):
        review, gov_storage, _ = _stack()
        cand = _candidate(review)
        before = list(gov_storage.read("governance_decisions"))
        with self.assertRaises(GovernanceError):
            review.record_decision(ReviewDecision(cand, "maybe", HumanAuthority("a"), "r"))
        after = list(gov_storage.read("governance_decisions"))
        self.assertEqual(before, after)  # nothing written on invalid decision

    def test_missing_rationale_rejected(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        with self.assertRaises(GovernanceError):
            review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), ""))

    def test_requires_memory_reader_and_storage(self):
        with self.assertRaises(GovernanceError):
            GovernanceReview(None, LocalAppendOnlyStorage(base_dir=Path(tempfile.mkdtemp())))  # type: ignore[arg-type]
        with self.assertRaises(GovernanceError):
            GovernanceReview(MemoryReader(TraceReader(_stack()[2])), None)  # type: ignore[arg-type]


class TestNoKnowledgeNoMutation(unittest.TestCase):
    def test_never_mutates_trace(self):
        review, _, trace_storage = _stack()
        cand = _candidate(review)
        before = list(trace_storage.read("trace"))
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), "r"))
        review.promotion_authorized(cand)
        after = list(trace_storage.read("trace"))
        self.assertEqual(before, after)  # Trace untouched (INV-5)

    def test_governance_writes_only_its_own_partition_not_trace(self):
        review, gov_storage, trace_storage = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), "r"))
        # Decision landed in the governance partition, not the trace partition.
        self.assertEqual(list(trace_storage.read("governance_decisions")), [])
        self.assertEqual(len(list(gov_storage.read("governance_decisions"))), 1)

    def test_no_knowledge_surface(self):
        for name in dir(GovernanceReview):
            self.assertNotIn("knowledge", name.lower())


class TestCaptureAndDeterminism(unittest.TestCase):
    def test_decision_captures_full_candidate_snapshot(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), "r"))
        (rec,) = review.recorded_decisions()
        self.assertEqual(rec["scope"], cand.scope)
        self.assertEqual(rec["content"], dict(cand.observed_content))
        self.assertEqual(rec["decision"], "approve")
        self.assertEqual(rec["reviewer_id"], "a")

    def test_recorded_decisions_are_append_only_and_ordered(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), "r1"))
        review.record_decision(ReviewDecision(cand, "reject", HumanAuthority("b"), "r2"))
        recs = review.recorded_decisions()
        self.assertEqual([r["decision"] for r in recs], ["approve", "reject"])


class TestFG1ProvenanceHardening(unittest.TestCase):
    """Phase 3.286: forged/injected storage records must never authorize."""

    def _forge_into_storage(self, gov_storage, candidate, decision, reviewer_id):
        import json
        from native_core.core.governance.decision import _to_plain
        forged = json.dumps(
            {"scope": candidate.scope, "content": _to_plain(candidate.observed_content),
             "occurrence_count": candidate.occurrence_count, "decision": decision,
             "reviewer_id": reviewer_id, "rationale": "forged"},
            sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")
        gov_storage.append("governance_decisions", forged)

    def test_forged_storage_approval_fails(self):
        review, gov_storage, _ = _stack()
        cand = _candidate(review)
        self._forge_into_storage(gov_storage, cand, "approve", "AUTOMATION")
        # A direct forged "approve" in storage must NOT authorize promotion.
        self.assertFalse(review.promotion_authorized(cand))

    def test_fake_reviewer_identity_fails(self):
        review, gov_storage, _ = _stack()
        cand = _candidate(review)
        self._forge_into_storage(gov_storage, cand, "approve", "totally-real-human")
        self.assertFalse(review.promotion_authorized(cand))

    def test_unauthorized_storage_injection_fails(self):
        review, gov_storage, _ = _stack()
        cand = _candidate(review)
        gov_storage.append("governance_decisions", b'{"malformed":true}')
        self._forge_into_storage(gov_storage, cand, "approve", "x")
        # Neither malformed nor forged records authorize, and neither appears in outcomes.
        self.assertFalse(review.promotion_authorized(cand))
        self.assertEqual(review.recorded_decisions(), ())

    def test_promotion_authorized_rejects_untrusted_records(self):
        review, gov_storage, _ = _stack()
        cand = _candidate(review)
        # Legit approve (trusted) authorizes...
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("alice"), "ok"))
        self.assertTrue(review.promotion_authorized(cand))
        # ...but a forged reject injected into storage is untrusted and ignored:
        # the real human approve stands, the forged reject does not override it.
        self._forge_into_storage(gov_storage, cand, "reject", "attacker")
        self.assertTrue(review.promotion_authorized(cand))

    def test_reject_precedence_preserved_after_hardening(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), "ok"))
        review.record_decision(ReviewDecision(cand, "reject", HumanAuthority("b"), "no"))
        self.assertFalse(review.promotion_authorized(cand))  # trusted reject absolute

    def test_deterministic_after_hardening(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), "ok"))
        self.assertEqual(len({review.promotion_authorized(cand) for _ in range(10)}), 1)

    def test_legit_flow_still_authorizes(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        self.assertFalse(review.promotion_authorized(cand))  # default deny
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("a"), "ok"))
        self.assertTrue(review.promotion_authorized(cand))


class TestFH1SnapshotImmutability(unittest.TestCase):
    """Phase 3.288: recorded_decisions() must not expose mutable internal state."""

    def test_mutating_returned_decision_is_blocked_and_changes_nothing(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "reject", HumanAuthority("h"), "no"))
        self.assertFalse(review.promotion_authorized(cand))
        d = review.recorded_decisions()[0]
        # The exact prior exploit: flip the recorded decision through the return.
        with self.assertRaises(TypeError):
            d["decision"] = "approve"
        # Authorization is unchanged — the reject still stands.
        self.assertFalse(review.promotion_authorized(cand))

    def test_returned_object_is_not_internal_reference(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("h"), "ok"))
        rec = review.recorded_decisions()[0]
        # Read-only mapping; not the mutable internal dict.
        from types import MappingProxyType
        self.assertIsInstance(rec, MappingProxyType)

    def test_nested_mutation_blocked(self):
        review, _, _ = _stack()
        cand = _candidate(review)  # content is a dict {"finding": "X"} derived from Trace outputs
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("h"), "ok"))
        rec = review.recorded_decisions()[0]
        with self.assertRaises(TypeError):
            rec["content"]["finding"] = "tampered"

    def test_copy_mutation_is_harmless(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "reject", HumanAuthority("h"), "no"))
        # A caller may copy and mutate the copy freely; state is untouched.
        d = dict(review.recorded_decisions()[0])
        d["decision"] = "approve"
        self.assertFalse(review.promotion_authorized(cand))

    def test_repeated_reads_and_multiple_callers_consistent(self):
        review, _, _ = _stack()
        cand = _candidate(review)
        review.record_decision(ReviewDecision(cand, "approve", HumanAuthority("h"), "ok"))
        a = review.recorded_decisions()
        b = review.recorded_decisions()
        self.assertEqual([dict(x) for x in a], [dict(x) for x in b])
        self.assertTrue(all(review.promotion_authorized(cand) for _ in range(5)))

    def test_fg1_remains_closed_after_fh1_fix(self):
        review, gov_storage, _ = _stack()
        cand = _candidate(review)
        import json
        from native_core.core.governance.decision import _to_plain
        forged = json.dumps(
            {"scope": cand.scope, "content": _to_plain(cand.observed_content),
             "occurrence_count": cand.occurrence_count, "decision": "approve",
             "reviewer_id": "AUTOMATION", "rationale": "forged"},
            sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")
        gov_storage.append("governance_decisions", forged)
        self.assertFalse(review.promotion_authorized(cand))


class TestDependencies(unittest.TestCase):
    def test_no_forbidden_imports(self):
        offenders = []
        for py in _GOV_DIR.rglob("*.py"):
            if py.name == "test_governance_conformance.py":
                continue
            tree = ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    mods = [a.name for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    mods = [node.module or ""]
                else:
                    continue
                for m in mods:
                    head = m.split(".")[0]
                    parts = set(m.split("."))
                    if head in _FORBIDDEN_EXTERNAL:
                        offenders.append((py.name, m, "external"))
                    if _FORBIDDEN_INTERNAL & parts:
                        offenders.append((py.name, m, "forbidden"))
        self.assertEqual(offenders, [], f"forbidden imports: {offenders}")

    def test_cross_boundary_deps_are_memory_and_infrastructure_only(self):
        cross = set()
        for py in _GOV_DIR.glob("*.py"):
            tree = ast.parse(py.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.level == 2:
                    cross.add(node.module)
        self.assertTrue(cross <= {"memory", "infrastructure"}, f"unexpected cross-boundary: {cross}")


if __name__ == "__main__":
    unittest.main()
