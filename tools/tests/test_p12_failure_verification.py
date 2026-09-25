"""P12-W6 failure-behaviour conformance (`§33`).

Three of seven states distinguished is a claim that must be falsifiable in both
directions: the module must be able to promote a state to `DISTINGUISHED` when
the system earns it, and must not count a state it cannot reach.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_failure_verification as fail


class TheScopeIsSection33s(unittest.TestCase):
    def test_the_seven_states_are_section_33s_in_order(self):
        self.assertEqual(
            list(fail.FAILURE_STATES),
            ["RETRYABLE", "BLOCKED", "REFUSED", "FAILED", "ESCALATED",
             "SUCCEEDED", "VERIFIED"])

    def test_the_five_retry_prohibitions_are_section_33s_in_order(self):
        self.assertEqual(
            list(fail.RETRY_PROHIBITIONS),
            ["duplicate authority", "duplicate delegation",
             "duplicate execution", "orphan state", "false success"])

    def test_every_state_has_a_probe(self):
        self.assertEqual(set(fail._STATES), set(fail.FAILURE_STATES))


class TheVerifierIsNotPartOfTheSystemItMeasures(unittest.TestCase):
    """It counted its own function names as retry mechanisms. Held closed."""

    def test_this_module_is_excluded_from_the_live_population(self):
        module = (fail.REPO_ROOT / "tools" / "p12_failure_verification.py")
        self.assertNotIn(module.resolve(),
                         {p.resolve() for p in fail.live_modules()})

    def test_its_own_retry_named_functions_are_not_counted(self):
        found = fail.retry_mechanisms()
        self.assertFalse(
            [m for m in found if "p12_failure_verification" in m],
            "the verifier is matching itself again")

    def test_historical_code_is_excluded(self):
        legacy = (fail.REPO_ROOT
                  / "docs/architecture/history/legacy-execution/tool_executor.py")
        if legacy.is_file():
            self.assertNotIn(legacy.resolve(),
                             {p.resolve() for p in fail.live_modules()})

    def test_the_search_is_content_anchored_not_textual(self):
        """A comment mentioning retry is not a retry mechanism."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "m.py").write_text(
                "# retry is discussed here\n"
                "RETRY_DOC = 'we do not retry'\n"
                "def unrelated():\n    return 1\n", encoding="utf-8")
            with mock.patch.object(fail, "REPO_ROOT", root), \
                    mock.patch.object(fail, "HISTORICAL", root / "nowhere"):
                self.assertEqual(fail.retry_mechanisms(), ())

    def test_a_real_retry_definition_is_found(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "m.py").write_text(
                "def retry_policy(n):\n    return n\n", encoding="utf-8")
            with mock.patch.object(fail, "REPO_ROOT", root), \
                    mock.patch.object(fail, "HISTORICAL", root / "nowhere"):
                self.assertEqual(len(fail.retry_mechanisms()), 1)


class DistinguishedMeansReachableAndTellableApart(unittest.TestCase):
    def test_failed_succeeded_and_escalated_are_distinguished(self):
        results = {r.state: r for r in fail.verify()}
        for state in ("FAILED", "SUCCEEDED", "ESCALATED"):
            with self.subTest(state):
                self.assertEqual(results[state].status, fail.DISTINGUISHED)
                self.assertTrue(results[state].persisted_as)

    def test_refused_is_now_persisted_distinguishably(self):
        """Closed by `ACT-CC-P12-027`, on the criterion the previous control
        pre-declared: the record gained `refusal_type`, and `_refused()` —
        which was **not** modified — reads it."""
        result = {r.state: r for r in fail.verify()}["REFUSED"]
        self.assertEqual(result.status, fail.DISTINGUISHED)
        self.assertEqual(result.persisted_as, "escalation record .refusal_type")

    def test_the_field_is_derived_from_the_raised_refusal_not_supplied(self):
        """The distinction is worth nothing if a caller can assert it.

        A record is built from the exception, so the persisted name is the one
        the refusal was actually made under — the same discipline `required`
        and `held` already carry — and a name outside `SANCTIONED_REFUSALS`
        cannot be constructed at all."""
        import tempfile
        from tools.escalation_register import (
            EscalationRecord, EscalationRegister, EscalationRegisterError)
        from tools.planning import AuthorityProvenance, EscalationRequired
        from tools.w4_execution import ExecutionRefused

        provenance = AuthorityProvenance(
            "FD-P11-001 §9",
            "docs/governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-"
            "INSTANCE-AUTHORIZATION.md")
        with tempfile.TemporaryDirectory() as tmp:
            register = EscalationRegister(Path(tmp))
            blocked = register.record(
                EscalationRequired("plan exceeds authority", required="r",
                                   held="h"),
                subject="a plan", authority=provenance)
            refused = register.record(
                ExecutionRefused("step exceeds delegation", required="r",
                                 held="h"),
                subject="a step", authority=provenance)
            self.assertEqual(blocked.refusal_type, "EscalationRequired")
            self.assertEqual(refused.refusal_type, "ExecutionRefused")
            self.assertNotEqual(register.load(blocked.escalation_id)
                                ["refusal_type"],
                                register.load(refused.escalation_id)
                                ["refusal_type"])

        with self.assertRaises(EscalationRegisterError):
            EscalationRecord(
                escalation_id="0" * 16, subject="s", required="r", held="h",
                reason="why", refusal_type="TotallyLegitimateRefusal",
                authority=provenance, raised_at="2026-09-18T00:00:00+00:00")

    def test_the_escalation_record_still_carries_no_structured_join(self):
        """Two different findings shared one control, and only one closed.

        `§33`'s *which refusal occurred* is now on the record. `§34`'s
        *which delegation it was refused under* is **not**: no delegation
        field was added, and the resident records still join their grant by a
        spelling. `P12-W3`'s beside-the-record surface remains the structural
        answer to that one."""
        join = fail.escalation_join()
        self.assertGreater(join["records"], 0)
        self.assertEqual(join["joined_by_structured_field"], 0,
                         "if escalation records have gained a delegation "
                         "field, this finding is closed and the evidence "
                         "record must say so")
        self.assertGreater(join["joined_by_parsed_prose"], 0)

    #: The escalations that predate `refusal_type`. Named, because "the count
    #: is 0" stopped being the right control the moment a live run under
    #: `FD-P12-006 §16` wrote a real escalation that does carry one.
    PREDATING = ("23f315ba9f504272", "0991300404cf44d8", "9cb90fa0787a478c")

    def test_the_records_predating_the_field_were_not_backfilled(self):
        """`refusal_type` is for records written from the field onward.

        Backfilling a value nobody observed onto a historical record would be
        manufacturing evidence. These three keep the shape they were written
        in, and the control names them rather than asserting a total — a total
        of `0` would now be false for an honest reason, and a control that has
        to be relaxed to stay true is not measuring what it claims."""
        import json
        records = {
            json.loads(path.read_text(encoding="utf-8"))["escalation_id"]:
                json.loads(path.read_text(encoding="utf-8"))
            for path in (fail.REPO_ROOT / "docs/architecture")
            .rglob("*.escalation.json")}
        for escalation_id in self.PREDATING:
            with self.subTest(escalation_id):
                self.assertIn(escalation_id, records)
                self.assertNotIn("refusal_type", records[escalation_id])

    def test_a_record_written_since_the_field_carries_it(self):
        """The other half: the field must actually reach resident records, or
        it is a schema change nothing exercises."""
        naming = fail.escalation_join()["naming_the_refusal_type"]
        self.assertGreater(naming, 0,
                           "no resident escalation names its refusal type; "
                           "the field is not reaching real records")

    def test_refused_falls_back_if_the_record_ever_loses_the_field(self):
        """The falsification: the state must not stay `DISTINGUISHED` on
        habit. Strip the field and the finding must re-open."""
        with mock.patch.object(fail, "_escalation_record_fields",
                               return_value=("escalation_id", "subject")):
            result = fail._refused()
            self.assertEqual(result.status, fail.RAISED_ONLY)
            self.assertIn("no field names which one", result.detail)


class GovernanceJoinSurfaceIsMeasuredSeparately(unittest.TestCase):
    """`P12-W3`/`P12-005`: a refusal now also joins its grant through an
    independently resolvable, beside-the-record reference — real, persisted
    instances, not mocks. `docs/architecture/p12/w3-operations/` carries the
    run `p12_w3_governance_escalation.py` produced (`ACT-CC-P12-003`);
    `docs/architecture/p12/w4-operations/` now also carries one produced by
    the wired resident call site `tools/w4_first_run.py`
    (`p12_w3_resident_wiring_proof.py`, `ACT-CC-P12-005`) — proof the join
    resolves per-escalation, beside whichever directory each one actually
    lives in, not against one hardcoded root (the defect this Act found and
    fixed in `escalation_join()` itself)."""

    def test_at_least_two_real_runs_join_by_the_new_surface(self):
        join = fail.escalation_join()
        self.assertGreaterEqual(join["joined_by_governance_surface"], 2,
                                "expected both the P12-W3 cycle's run and "
                                "this cycle's resident-wiring run to have "
                                "left an independently-resolvable join on "
                                "disk, in their own directories")

    def test_the_w3_cycle_record_does_not_depend_on_prose_matching(self):
        """`ACT-CC-P12-003`'s record's subject was deliberately worded so
        the old regex does not match it — proof that record specifically is
        resolved by the governance surface, not the prose fallback. A
        second, later real record (`ACT-CC-P12-005`, `w4-operations`) was
        *not* given adversarial wording — its subject follows
        `tools/w4_first_run.py`'s own unchanged format, which happens to
        satisfy the old regex too — so the aggregate count below is not, by
        itself, proof of independence; this test checks the one record that
        is."""
        from tools.p12_governance_join_reader import resolve, JOINED
        root = fail.REPO_ROOT / "docs/architecture/p12/w3-operations"
        escalation_id = next(
            p.name.split(".")[0]
            for p in root.glob("*.escalation.json"))
        payload = json.loads(
            (root / f"{escalation_id}.escalation.json").read_text())
        self.assertNotRegex(payload["subject"], r"delegation [0-9a-f]{16}")
        self.assertEqual(
            resolve(root, root, escalation_id)["status"], JOINED)

    def test_verified_is_unreachable_in_the_ratified_vocabulary(self):
        result = {r.state: r for r in fail.verify()}["VERIFIED"]
        self.assertEqual(result.status, fail.UNREACHABLE)

    def test_verified_would_be_distinguished_if_the_vocabulary_held_it(self):
        with mock.patch.object(fail, "_trace_statuses",
                               return_value=frozenset({"success", "verified"})):
            self.assertEqual(fail._verified().status, fail.DISTINGUISHED)

    def test_an_unreachable_state_is_never_counted_as_distinguished(self):
        summary = fail.summary()
        self.assertEqual(
            summary["distinguished"] + summary["raised_only"]
            + summary["unreachable"], summary["states"])
        self.assertIn("VERIFIED", summary["not_distinguished"])
        self.assertIn("RETRYABLE", summary["not_distinguished"])


class TheRetryRulesAreNotReportedSatisfied(unittest.TestCase):
    """Five rules trivially true in a system with no retry is not compliance."""

    def test_no_retry_yields_not_applicable_not_pass(self):
        rules = fail.retry_prohibitions()
        self.assertEqual(rules["status"], "NOT APPLICABLE")
        self.assertNotIn("PASS", rules["status"])
        self.assertIn("none is controlled against", rules["detail"])

    def test_a_retry_mechanism_makes_the_rules_unverified_not_satisfied(self):
        with mock.patch.object(fail, "retry_mechanisms",
                               return_value=("some/module.py retry_policy",)):
            self.assertEqual(fail.retry_prohibitions()["status"], "UNVERIFIED")

    def test_all_five_prohibitions_are_counted(self):
        self.assertEqual(fail.retry_prohibitions()["prohibitions"], 5)


class WhatThisSuiteDoesNotEstablish(unittest.TestCase):
    def test_distinguished_is_not_a_correctness_claim(self):
        """That a state can be told apart says nothing about when it is used."""
        for result in fail.verify():
            if result.status == fail.DISTINGUISHED:
                with self.subTest(result.state):
                    self.assertTrue(result.persisted_as)


if __name__ == "__main__":
    unittest.main()
