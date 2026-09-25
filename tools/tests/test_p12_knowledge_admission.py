"""`ACT-CC-P12-015 §19`–`§21` — the admission chain, falsified.

`§20` requires an attempt to falsify one claim:

```text
P6 IS CONSUMED BY REAL SYSTEM WORK
```

so each `F-` case below drives the real code at the real refusal point. None of
them asserts that a guard exists; each one removes the thing the claim depends
on and requires the system to refuse. `§20` closes: *"the controls must remain
falsifiable and must not be weakened to produce PASS."*

`§21`'s negative control is `Case9`: the corpus's own `0 / 0 / 0` observations
must **not** produce `HEALTHY` without the admitted criteria and their
evaluation context. `OBSERVED FACTS ≠ VERDICT`.
"""

from __future__ import annotations

import ast
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import aios_corpus_health_run as work
from tools import p12_knowledge_admission as admission
from tools import p12_knowledge_admission_verifier as verifier

REPO_ROOT = Path(__file__).resolve().parents[2]

INSTRUMENT = REPO_ROOT / admission.DECISION_ROOT / \
    "FD-P12-002-P6-KNOWLEDGE-ADMISSION.md"


def _world(tmp: Path, instrument_text=None) -> Path:
    """A minimal repository world: the acts root plus the candidate source."""
    (tmp / admission.DECISION_ROOT).mkdir(parents=True, exist_ok=True)
    if instrument_text is not None:
        (tmp / admission.DECISION_ROOT / "FD.md").write_text(
            instrument_text, encoding="utf-8")
    shutil.copy(REPO_ROOT / admission.CANDIDATE_SOURCE,
                tmp / admission.CANDIDATE_SOURCE)
    return tmp


class Case1NoActiveKnowledge(unittest.TestCase):
    """`F-01` — no Active Knowledge, so no consumption may be claimed."""

    def test_the_work_withholds_its_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            outcome = work.run(store_root=Path(tmp) / "traces",
                               runtime_store=Path(tmp) / "runtime",
                               observation_root=Path(tmp) / "observations")
        self.assertFalse(outcome["knowledge_consumed"])
        self.assertEqual("WITHHELD", outcome["outputs"]["verdict"]["verdict"])

    def test_the_verifier_reports_active_knowledge_unsatisfied(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp))
            check = verifier._active_state(world)
        self.assertEqual(verifier.UNSATISFIED, check.status)

    def test_a_record_that_consumed_nothing_does_not_exercise_the_phase(self):
        from tools import p12_cross_phase_verification as cross

        class Bare:
            knowledge_consumed = ()
        exercised, _ = cross._knowledge_exercised((Bare(),))
        self.assertFalse(exercised)


class Case2FakeFounderApproval(unittest.TestCase):
    """`F-02` — an approval that is not an issued Founder decision."""

    def test_an_unissued_instrument_authorizes_nothing(self):
        text = INSTRUMENT.read_text(encoding="utf-8").replace(
            "FINAL / ISSUED", "PENDING FOUNDER DECISION")
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp), text)
            with self.assertRaises(admission.AdmissionAuthorityUnresolved):
                admission.founder_authorization(world)

    def test_a_recommendation_is_not_an_approval(self):
        text = INSTRUMENT.read_text(encoding="utf-8").replace(
            "Decision:\nAPPROVED FOR KNOWLEDGE ADMISSION",
            "Decision:\nRECOMMENDED FOR KNOWLEDGE ADMISSION")
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp), text)
            with self.assertRaises(admission.AdmissionAuthorityUnresolved):
                admission.founder_authorization(world)

    def test_a_decision_injected_into_storage_never_authorizes(self):
        """Governance's own `F-G1`: provenance, not mere existence.

        A forged record appended straight into the durable partition bypasses
        `record_decision` and its `HumanAuthority` validation, so it never
        enters the trusted index. Promotion stays denied and admission raises.
        """
        from native_core.core.governance import GovernanceReview
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.knowledge import UnauthorizedPromotion
        from native_core.core.knowledge.composition import (
            create_knowledge_subsystem)
        from native_core.core.memory import MemoryReader, PromotionCandidate
        from native_core.core.trace import TraceReader

        candidate = PromotionCandidate(
            scope=admission.KNOWLEDGE_ITEM_KEY,
            observed_content=admission.candidate_identity().content,
            occurrence_count=1)
        forged = json.dumps({
            "scope": candidate.scope,
            "content": dict(candidate.observed_content),
            "occurrence_count": 1,
            "decision": "approve",
            "reviewer_id": "not-a-real-reviewer",
            "rationale": "forged",
        }, sort_keys=True, separators=(",", ":")).encode("utf-8")
        with tempfile.TemporaryDirectory() as tmp:
            decisions = LocalAppendOnlyStorage(Path(tmp) / "decisions")
            decisions.provision()
            decisions.append("governance_decisions", forged)
            traces = LocalAppendOnlyStorage(Path(tmp) / "traces")
            traces.provision()
            knowledge = LocalAppendOnlyStorage(Path(tmp) / "knowledge")
            knowledge.provision()
            review = GovernanceReview(
                memory_reader=MemoryReader(TraceReader(traces)),
                decision_storage=decisions)
            self.assertFalse(review.promotion_authorized(candidate))
            with self.assertRaises(UnauthorizedPromotion):
                create_knowledge_subsystem(knowledge).admission.admit(
                    candidate, review)


class Case3MissingProvenance(unittest.TestCase):
    """`F-03` — a decision with no reason, and a candidate with no source."""

    def test_an_instrument_without_a_rationale_cannot_be_recorded(self):
        text = INSTRUMENT.read_text(encoding="utf-8")
        text = text.replace("The Founder authorizes the corpus-health criteria",
                            "The Founder notes the corpus-health criteria")
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp), text)
            with self.assertRaises(admission.AdmissionAuthorityUnresolved) as caught:
                admission.founder_authorization(world)
        self.assertIn("rationale", str(caught.exception))

    def test_governance_refuses_a_decision_without_a_rationale(self):
        from native_core.core.governance import (
            GovernanceError, GovernanceReview, HumanAuthority, ReviewDecision)
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.memory import MemoryReader, PromotionCandidate
        from native_core.core.trace import TraceReader

        with tempfile.TemporaryDirectory() as tmp:
            decisions = LocalAppendOnlyStorage(Path(tmp) / "d")
            decisions.provision()
            traces = LocalAppendOnlyStorage(Path(tmp) / "t")
            traces.provision()
            review = GovernanceReview(
                memory_reader=MemoryReader(TraceReader(traces)),
                decision_storage=decisions)
            with self.assertRaises(GovernanceError):
                review.record_decision(ReviewDecision(
                    candidate=PromotionCandidate("k", {"a": 1}, 1),
                    decision="approve",
                    authority=HumanAuthority(reviewer_id="Founder"),
                    rationale="   "))

    def test_an_absent_candidate_source_is_a_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / admission.DECISION_ROOT).mkdir(parents=True)
            with self.assertRaises(admission.CandidateIdentityUnresolved):
                admission.candidate_identity(Path(tmp))

    def test_the_verifier_reports_missing_provenance_elements(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp))
            check = verifier._provenance(world)
        self.assertEqual(verifier.UNRESOLVED, check.status)


class Case4WrongCandidateIdentity(unittest.TestCase):
    """`F-04` — an approval spent on something it does not name."""

    def test_an_approval_of_another_candidate_does_not_cover_this_one(self):
        text = INSTRUMENT.read_text(encoding="utf-8").replace(
            "Candidate:\nP12 Corpus-Health Assessment Criteria",
            "Candidate:\nP12 Release Notes")
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp), text)
            authorization = admission.founder_authorization(world)
            identity = admission.candidate_identity(world)
            self.assertFalse(admission.approval_covers(authorization, identity))
            with self.assertRaises(admission.AdmissionRefused):
                admission.admit(world,
                                store_root=Path(tmp) / "runtime",
                                decision_root=Path(tmp) / "decisions",
                                provenance_root=Path(tmp) / "provenance")

    def test_a_criteria_literal_naming_a_different_item_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp))
            source = world / admission.CANDIDATE_SOURCE
            source.write_text(source.read_text(encoding="utf-8").replace(
                'KNOWLEDGE_KEY = "corpus-health.criteria"',
                'KNOWLEDGE_KEY = "something-else"'), encoding="utf-8")
            with self.assertRaises(admission.CandidateIdentityUnresolved):
                admission.candidate_identity(world)

    def test_the_verifier_rejects_a_provenance_hash_that_is_not_the_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp))
            store = world / admission.PROVENANCE_STORE
            store.mkdir(parents=True)
            (store / admission.PROVENANCE_PARTITION).write_text(
                json.dumps({"candidate_immutable_identity": "0" * 64}) + "\n",
                encoding="utf-8")
            check = verifier._candidate_identity(world)
        self.assertEqual(verifier.UNSATISFIED, check.status)


class Case5LocalHardCodedCriteria(unittest.TestCase):
    """`F-05` — a worker reading its own threshold is not consuming Knowledge."""

    def test_a_worker_that_reads_its_local_literal_fails_the_consumer_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp))
            source = world / admission.CANDIDATE_SOURCE
            source.write_text(source.read_text(encoding="utf-8").replace(
                "    criteria = _active_criteria(knowledge)",
                "    criteria = CRITERIA_CONTENT"), encoding="utf-8")
            check = verifier._consumer_path(world)
        self.assertEqual(verifier.UNSATISFIED, check.status)
        self.assertIn("CRITERIA_CONTENT", check.detail)

    def test_the_resident_worker_never_reads_its_own_literal(self):
        tree = ast.parse(
            (REPO_ROOT / admission.CANDIDATE_SOURCE).read_text(encoding="utf-8"))
        loads = [n.id for n in ast.walk(tree)
                 if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)]
        self.assertNotIn(admission.CANDIDATE_IDENTIFIER, loads)


class Case6DemonstratorOnly(unittest.TestCase):
    """`F-06` — a demonstrator crossing is not `R1` consumption."""

    def test_a_demonstrator_authored_consumption_is_refused(self):
        # The record is written straight through `TraceWriter`, not through
        # `consumers.observation.TracedAction`: `tools/` may not import
        # `consumers/`, and `consumers/tests/test_reference_agent.py` enforces
        # that edge by AST over every file under `tools/`, this one included.
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.trace import TraceRecord, TraceWriter

        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp))
            store = world / verifier.TRACE_STORE
            store.mkdir(parents=True)
            storage = LocalAppendOnlyStorage(store)
            storage.provision()
            TraceWriter(storage).write(TraceRecord(
                agent_definition_version="1.0",
                agent_instance="demo-instance",
                runtime="p12-f11-workflow-observation",
                knowledge_consumed=({"key": verifier.ITEM_KEY,
                                     "content": {"a": 1}},),
                outputs={"ok": True}))
            check = verifier._real_system_work(world)
        self.assertEqual(verifier.UNSATISFIED, check.status)
        self.assertIn("demonstrator", check.detail)

    def test_the_live_corpus_carries_no_demonstrator_only_phase(self):
        from tools import p12_cross_phase_verification as cross
        self.assertEqual((), cross.summary()["exercised_only_by_a_demonstrator"])


class Case7StaleKnowledgeVersion(unittest.TestCase):
    """`F-07` — a superseded version is not the current Active one."""

    def test_the_superseded_version_is_not_reported_active(self):
        from native_core.core.governance import (
            GovernanceReview, HumanAuthority, ReviewDecision)
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.knowledge.composition import (
            create_knowledge_subsystem)
        from native_core.core.memory import MemoryReader, PromotionCandidate
        from native_core.core.trace import TraceReader

        with tempfile.TemporaryDirectory() as tmp:
            decisions = LocalAppendOnlyStorage(Path(tmp) / "d")
            decisions.provision()
            traces = LocalAppendOnlyStorage(Path(tmp) / "t")
            traces.provision()
            knowledge = LocalAppendOnlyStorage(Path(tmp) / "k")
            knowledge.provision()
            review = GovernanceReview(
                memory_reader=MemoryReader(TraceReader(traces)),
                decision_storage=decisions)
            subsystem = create_knowledge_subsystem(knowledge)
            first = PromotionCandidate(verifier.ITEM_KEY, {"limit": 0}, 1)
            second = PromotionCandidate(verifier.ITEM_KEY, {"limit": 5}, 1)
            for candidate in (first, second):
                review.record_decision(ReviewDecision(
                    candidate=candidate, decision="approve",
                    authority=HumanAuthority(reviewer_id="Founder"),
                    rationale="test"))
            v1 = subsystem.admission.admit(first, review)
            v2 = subsystem.admission.revise(second, review)
            active = subsystem.retrieval.active(verifier.ITEM_KEY)
            history = subsystem.retrieval.history(verifier.ITEM_KEY)

        self.assertEqual(v2.identity, active.identity)
        self.assertNotEqual(v1.identity, active.identity)
        self.assertIn(v1, history)

    def test_the_verifier_rejects_provenance_naming_a_superseded_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp))
            store = world / admission.PROVENANCE_STORE
            store.mkdir(parents=True)
            (store / admission.PROVENANCE_PARTITION).write_text(
                json.dumps({"resulting_knowledge_identity": {
                    "knowledge_item_key": verifier.ITEM_KEY,
                    "version_sequence": 99}}) + "\n", encoding="utf-8")
            check = verifier._admitted_version(world)
        self.assertEqual(verifier.UNSATISFIED, check.status)

    def test_re_admitting_different_content_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp), INSTRUMENT.read_text(encoding="utf-8"))
            runtime_store = Path(tmp) / "runtime"
            kwargs = dict(store_root=runtime_store,
                          decision_root=Path(tmp) / "decisions",
                          provenance_root=Path(tmp) / "provenance")
            first = admission.admit(world, **kwargs)
            self.assertTrue(first["admitted_in_this_call"])
            # Re-running with the same candidate is a no-op, not version churn.
            again = admission.admit(world, **kwargs)
            self.assertFalse(again["admitted_in_this_call"])
            self.assertEqual(1, again["active_version"]["version_sequence"])
            # A *different* candidate under the same key is a governed
            # revision this instrument does not authorize.
            source = world / admission.CANDIDATE_SOURCE
            source.write_text(source.read_text(encoding="utf-8").replace(
                '"citation_errors_max": 0', '"citation_errors_max": 7'),
                encoding="utf-8")
            with self.assertRaises(admission.AdmissionRefused):
                admission.admit(world, **kwargs)


class Case8AdmissionWithoutHumanAuthority(unittest.TestCase):
    """`F-08` — no human authority, no admission."""

    def test_an_empty_reviewer_identity_cannot_hold_authority(self):
        from native_core.core.governance import HumanAuthority
        from native_core.core.governance.authority import InvalidAuthority
        for identity in ("", "   "):
            with self.assertRaises(InvalidAuthority):
                HumanAuthority(reviewer_id=identity)

    def test_an_instrument_naming_no_human_authority_authorizes_nothing(self):
        text = INSTRUMENT.read_text(encoding="utf-8").replace(
            "HumanAuthority:\nFounder", "HumanAuthority:\n")
        with tempfile.TemporaryDirectory() as tmp:
            world = _world(Path(tmp), text)
            with self.assertRaises(admission.AdmissionAuthorityUnresolved):
                admission.founder_authorization(world)

    def test_automation_may_not_supply_the_authority(self):
        from native_core.core.governance import (
            GovernanceError, GovernanceReview, ReviewDecision)
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.memory import MemoryReader, PromotionCandidate
        from native_core.core.trace import TraceReader

        class NotAHuman:
            reviewer_id = "automation"

        with tempfile.TemporaryDirectory() as tmp:
            decisions = LocalAppendOnlyStorage(Path(tmp) / "d")
            decisions.provision()
            traces = LocalAppendOnlyStorage(Path(tmp) / "t")
            traces.provision()
            review = GovernanceReview(
                memory_reader=MemoryReader(TraceReader(traces)),
                decision_storage=decisions)
            with self.assertRaises(GovernanceError):
                review.record_decision(ReviewDecision(
                    candidate=PromotionCandidate("k", {"a": 1}, 1),
                    decision="approve", authority=NotAHuman(),
                    rationale="automation decided"))

    def test_the_admission_module_names_no_reviewer_identity_of_its_own(self):
        """`§9` — the reviewer is read out of the instrument, never authored.

        Every string constant in the module (docstrings excluded, since they
        quote the Act) is checked against the identity the live instrument
        actually names. A literal match would mean the module could authorize
        an admission with the instrument deleted.
        """
        reviewer = admission.founder_authorization().human_authority
        tree = ast.parse(
            (REPO_ROOT / "tools" / "p12_knowledge_admission.py").read_text(
                encoding="utf-8"))
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                first = node.body[0] if node.body else None
                if (isinstance(first, ast.Expr)
                        and isinstance(first.value, ast.Constant)
                        and isinstance(first.value.value, str)):
                    docstrings.add(id(first.value))
        literals = [n.value for n in ast.walk(tree)
                    if isinstance(n, ast.Constant)
                    and isinstance(n.value, str) and id(n) not in docstrings]
        self.assertNotIn(reviewer, literals)


class Case9HealthyIsNotCreatedByWording(unittest.TestCase):
    """`§21` — the corpus's own zeroes do not make a verdict."""

    ZEROES = {"stale_governance_sources": 0, "citation_errors": 0,
              "live_stale_assertions": 0}

    def test_zero_zero_zero_without_criteria_is_withheld_not_healthy(self):
        verdict = work.judge(dict(self.ZEROES), None)
        self.assertEqual("WITHHELD", verdict["verdict"])
        self.assertNotEqual("HEALTHY", verdict["verdict"])

    def test_the_same_zeroes_with_the_admitted_criteria_are_evaluated(self):
        criteria = admission.candidate_identity().content
        verdict = work.judge(dict(self.ZEROES), dict(criteria))
        self.assertEqual("HEALTHY", verdict["verdict"])
        self.assertEqual("measured against the admitted criteria",
                         verdict["reason"])

    def test_the_criteria_decide_the_verdict_not_the_facts_alone(self):
        """Same facts, stricter admitted criteria, different verdict.

        If the zeroes alone produced `HEALTHY`, this could not happen — which
        is the whole of `§12`: `OBSERVED FACTS ≠ VERDICT`.
        """
        stricter = {"stale_governance_sources_max": -1,
                    "citation_errors_max": -1,
                    "live_stale_assertions_max": -1}
        verdict = work.judge(dict(self.ZEROES), stricter)
        self.assertEqual("DEGRADED", verdict["verdict"])


class Case10Independence(unittest.TestCase):
    """`§19` — the verifier must not simply trust the admission writer."""

    def test_the_verifier_imports_nothing_from_the_admission_module(self):
        tree = ast.parse(
            (REPO_ROOT / "tools" / "p12_knowledge_admission_verifier.py")
            .read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imported.add(module)
                imported.update(f"{module}.{a.name}" for a in node.names)
        offending = {name for name in imported
                     if "p12_knowledge_admission" in name
                     and not name.endswith("_verifier")}
        self.assertEqual(set(), offending, f"verifier imports {offending}")

    def test_the_two_modules_derive_the_candidate_independently(self):
        by_ast = admission.candidate_identity().content
        by_text = verifier.declared_criteria()
        self.assertEqual(dict(by_ast), dict(by_text))


class Case11TheLiveChain(unittest.TestCase):
    """The state the Act asks to be evidenced, on the live corpus."""

    def test_all_ten_admission_checks_are_satisfied(self):
        summary = verifier.summary()
        self.assertEqual((), summary["failing"])
        self.assertEqual(10, summary["satisfied"])

    def test_the_lifecycle_states_are_each_evidenced_separately(self):
        """`§22` — CANDIDATE → REVIEW → AUTHORIZATION → ADMISSION → ACTIVE."""
        self.assertTrue(admission.candidate_identity().content_hash)
        approvals = [d for d in verifier.recorded_decisions()
                     if d.get("scope") == verifier.ITEM_KEY]
        self.assertTrue(approvals, "no review decision is on record")
        self.assertEqual("AUTHORIZED",
                         admission.founder_authorization().admission)
        self.assertTrue(verifier.provenance_records())
        self.assertIsNotNone(verifier.active_version())

    def test_p6_is_consumed_by_real_system_work(self):
        from tools import p12_e12_acceptance as acc
        result = {p.phase: p.verdict for p in acc.phases()}
        self.assertEqual(acc.CONSUMED, result["P6"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
