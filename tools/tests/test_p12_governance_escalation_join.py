"""`P12-W3` — the escalation→grant join, and its independent reader.

`W4-GAP-008` / `W2-GAP-007`: a refusal reaches the grant it was refused under
only through a regex over prose. This suite proves the structural
alternative holds under falsification: a join that does not exist is
`DANGLING`, not silently absent; a join naming a delegation, escalation, or
refusal type that does not resolve is `DANGLING`; the reader resolves nothing
by importing the writer's internal state (`§24`); and at least one real,
persisted instance — produced by `p12_w3_governance_escalation.py`, not a
fixture — resolves `JOINED`.
"""

from __future__ import annotations

import ast
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.escalation_register import EscalationRegister
from tools.planning import AuthorityProvenance
from tools.w4_execution import ExecutionRefused
from tools import p12_governance_escalation_join as writer
from tools import p12_governance_join_reader as reader

REPO_ROOT = Path(__file__).resolve().parents[2]
FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
SUBJECT = "P12-W3 conformance fixture — no delegation id embedded here"


def authority():
    return AuthorityProvenance("FD-P11-001 §9", FD_RECORD)


def refusal(step="report-conformance", held=("verify-delegation-elements",)):
    return ExecutionRefused(f"step {step!r} is outside the delegated work scope",
                            required=step, held=held)


class TempEscalation(unittest.TestCase):
    """One real, recorded escalation, in an isolated register — not a real
    delegation, so tests here that need `JOINED` mock `delegation_records`
    rather than depending on the live resident population."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.register = EscalationRegister(self.root)
        self.recorded = self.register.record(
            refusal(), subject=SUBJECT, authority=authority())
        self.addCleanup(self._tmp.cleanup)


class WriterRefusesWhatItCannotSupport(TempEscalation):
    """The join must fail closed on every input it cannot prove."""

    def test_an_empty_delegation_id_is_refused(self):
        for bad in ("", "   ", None):
            with self.subTest(bad=bad):
                with self.assertRaises(writer.GovernanceJoinError):
                    writer.join_escalation_to_grant(
                        self.root, self.register, self.recorded.escalation_id,
                        delegation_id=bad, refusal_type="ExecutionRefused")

    def test_an_unsanctioned_refusal_type_is_refused(self):
        for bad in ("SomeOtherError", "", None, "executionrefused"):
            with self.subTest(bad=bad):
                with self.assertRaises(writer.GovernanceJoinError):
                    writer.join_escalation_to_grant(
                        self.root, self.register, self.recorded.escalation_id,
                        delegation_id="a" * 16, refusal_type=bad)

    def test_joining_an_escalation_that_does_not_exist_is_refused(self):
        with self.assertRaises(Exception):
            writer.join_escalation_to_grant(
                self.root, self.register, "0" * 16,
                delegation_id="a" * 16, refusal_type="ExecutionRefused")

    def test_a_join_may_not_be_written_twice(self):
        writer.join_escalation_to_grant(
            self.root, self.register, self.recorded.escalation_id,
            delegation_id="a" * 16, refusal_type="ExecutionRefused")
        with self.assertRaises(writer.GovernanceJoinError):
            writer.join_escalation_to_grant(
                self.root, self.register, self.recorded.escalation_id,
                delegation_id="b" * 16, refusal_type="ExecutionRefused")
        # the original must survive the refused second attempt unchanged
        path = self.root / f"{self.recorded.escalation_id}.governance-join.json"
        self.assertEqual("a" * 16, json.loads(path.read_text())["delegation_id"])


class WriterPersistsWhatItValidates(TempEscalation):
    def test_a_valid_join_is_persisted_with_the_right_shape(self):
        join = writer.join_escalation_to_grant(
            self.root, self.register, self.recorded.escalation_id,
            delegation_id="a" * 16, refusal_type="ExecutionRefused")
        path = self.root / f"{self.recorded.escalation_id}.governance-join.json"
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text())
        self.assertEqual(payload["escalation_id"], self.recorded.escalation_id)
        self.assertEqual(payload["delegation_id"], "a" * 16)
        self.assertEqual(payload["refusal_type"], "ExecutionRefused")
        self.assertIn("joined_at", payload)
        self.assertEqual(join.escalation_id, self.recorded.escalation_id)

    def test_the_underlying_escalation_record_is_never_modified(self):
        before = (self.root
                  / f"{self.recorded.escalation_id}.escalation.json").read_text()
        writer.join_escalation_to_grant(
            self.root, self.register, self.recorded.escalation_id,
            delegation_id="a" * 16, refusal_type="ExecutionRefused")
        after = (self.root
                 / f"{self.recorded.escalation_id}.escalation.json").read_text()
        self.assertEqual(before, after)


class TheTwoSurfacesMustAgreeAboutOneFact(TempEscalation):
    """`ACT-CC-P12-027` put `refusal_type` on the escalation record itself.

    The join already carried one. Two surfaces now state the same fact, and
    two surfaces disagreeing about one fact is worse than one surface alone,
    so the writer refuses the contradiction.
    """

    def test_a_join_contradicting_the_record_is_refused(self):
        with self.assertRaises(writer.GovernanceJoinError) as caught:
            writer.join_escalation_to_grant(
                self.root, self.register, self.recorded.escalation_id,
                delegation_id="a" * 16, refusal_type="EscalationRequired")
        self.assertIn("may not contradict the record", str(caught.exception))
        self.assertFalse(
            (self.root
             / f"{self.recorded.escalation_id}.governance-join.json").exists(),
            "a refused join must leave nothing behind")

    def test_a_join_agreeing_with_the_record_is_written(self):
        """The control must not refuse everything."""
        join = writer.join_escalation_to_grant(
            self.root, self.register, self.recorded.escalation_id,
            delegation_id="a" * 16, refusal_type="ExecutionRefused")
        self.assertEqual(join.refusal_type, self.recorded.refusal_type)

    def test_a_record_that_names_no_type_is_not_treated_as_contradicting(self):
        """Silence is not a contradiction.

        The three resident escalations predate the field. *Cannot check* and
        *checked and found wrong* are different answers, and only the second
        may refuse — otherwise adding the field would retroactively make every
        historical record unjoinable."""
        path = (self.root
                / f"{self.recorded.escalation_id}.escalation.json")
        payload = json.loads(path.read_text())
        payload.pop("refusal_type")
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        join = writer.join_escalation_to_grant(
            self.root, self.register, self.recorded.escalation_id,
            delegation_id="a" * 16, refusal_type="EscalationRequired")
        self.assertEqual(join.refusal_type, "EscalationRequired")

    def test_the_one_wiring_path_cannot_produce_a_disagreement(self):
        """Both values come from the same object in the same loop."""
        import tempfile as _tempfile
        from tools.planning import EscalationRequired
        with _tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            refusals = [refusal(),
                        EscalationRequired("plan exceeds authority",
                                           required="r", held=("h",))]
            ids = writer.join_refusals_to_grants(
                root, refusals, subject=SUBJECT, authority=authority(),
                delegation_for=lambda _r: "b" * 16)
            self.assertEqual(len(ids), 2)
            for escalation_id in ids:
                record = json.loads(
                    (root / f"{escalation_id}.escalation.json").read_text())
                join = json.loads(
                    (root / f"{escalation_id}.governance-join.json").read_text())
                self.assertEqual(record["refusal_type"], join["refusal_type"])
            self.assertEqual(
                {json.loads((root / f"{i}.escalation.json").read_text())
                 ["refusal_type"] for i in ids},
                {"ExecutionRefused", "EscalationRequired"},
                "the fixture must exercise both sanctioned types")


class ReaderImportsNothingFromTheWriter(unittest.TestCase):
    """`§24` — a join only the writer believes in is not a join."""

    def test_the_reader_does_not_import_the_writer_module(self):
        source = (REPO_ROOT / "tools" / "p12_governance_join_reader.py"
                  ).read_text(encoding="utf-8")
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        self.assertNotIn("tools.p12_governance_escalation_join", imported)
        self.assertFalse([m for m in imported if "escalation_join" in m])


class ReaderResolvesByReferenceNotByTrust(TempEscalation):
    """Every DANGLING case a real join file could present."""

    def test_no_join_file_is_dangling(self):
        result = reader.resolve(self.root, self.root, self.recorded.escalation_id)
        self.assertEqual(reader.DANGLING, result["status"])

    def test_a_join_naming_a_different_escalation_than_its_filename_is_dangling(self):
        mismatched = dict(escalation_id="f" * 16, delegation_id="a" * 16,
                          refusal_type="ExecutionRefused", joined_at="x")
        (self.root / f"{self.recorded.escalation_id}.governance-join.json"
         ).write_text(json.dumps(mismatched), encoding="utf-8")
        result = reader.resolve(self.root, self.root, self.recorded.escalation_id)
        self.assertEqual(reader.DANGLING, result["status"])

    def test_a_join_whose_escalation_was_deleted_is_dangling(self):
        with mock.patch.object(
                reader, "delegation_records",
                return_value=({"delegation_id": "a" * 16},)):
            writer.join_escalation_to_grant(
                self.root, self.register, self.recorded.escalation_id,
                delegation_id="a" * 16, refusal_type="ExecutionRefused")
        (self.root / f"{self.recorded.escalation_id}.escalation.json").unlink()
        result = reader.resolve(self.root, self.root, self.recorded.escalation_id)
        self.assertEqual(reader.DANGLING, result["status"])

    def test_a_join_naming_an_unresolvable_delegation_is_dangling(self):
        writer.join_escalation_to_grant(
            self.root, self.register, self.recorded.escalation_id,
            delegation_id="0" * 16, refusal_type="ExecutionRefused")
        with mock.patch.object(reader, "delegation_records", return_value=()):
            result = reader.resolve(self.root, self.root,
                                    self.recorded.escalation_id)
        self.assertEqual(reader.DANGLING, result["status"])
        self.assertIn("does not resolve", result["reason"])

    def test_a_join_naming_an_unsanctioned_refusal_type_is_dangling(self):
        forged = dict(escalation_id=self.recorded.escalation_id,
                     delegation_id="a" * 16, refusal_type="NotARealRefusal",
                     joined_at="x")
        (self.root / f"{self.recorded.escalation_id}.governance-join.json"
         ).write_text(json.dumps(forged), encoding="utf-8")
        with mock.patch.object(
                reader, "delegation_records",
                return_value=({"delegation_id": "a" * 16},)):
            result = reader.resolve(self.root, self.root,
                                    self.recorded.escalation_id)
        self.assertEqual(reader.DANGLING, result["status"])

    def test_a_join_that_resolves_on_every_reference_is_joined(self):
        with mock.patch.object(
                reader, "delegation_records",
                return_value=({"delegation_id": "a" * 16},)):
            writer.join_escalation_to_grant(
                self.root, self.register, self.recorded.escalation_id,
                delegation_id="a" * 16, refusal_type="ExecutionRefused")
            result = reader.resolve(self.root, self.root,
                                    self.recorded.escalation_id)
        self.assertEqual(reader.JOINED, result["status"])
        self.assertEqual("a" * 16, result["delegation_id"])
        self.assertEqual("ExecutionRefused", result["refusal_type"])

    def test_resolve_all_covers_exactly_the_join_files_present(self):
        second = self.register.record(refusal("other-step"), subject=SUBJECT,
                                      authority=authority())
        with mock.patch.object(
                reader, "delegation_records",
                return_value=({"delegation_id": "a" * 16},)):
            writer.join_escalation_to_grant(
                self.root, self.register, self.recorded.escalation_id,
                delegation_id="a" * 16, refusal_type="ExecutionRefused")
            results = reader.resolve_all(self.root, self.root)
        ids = {r["escalation_id"] for r in results}
        self.assertEqual({self.recorded.escalation_id}, ids)
        self.assertNotIn(second.escalation_id, ids)


class RealSystemWorkNotADemonstrator(unittest.TestCase):
    """`ACT-CC-P12-W3-001 §16`-equivalent: the corpus must already carry one
    real, resolvable instance — produced by `p12_w3_governance_escalation.py`
    running for real, not constructed inside this test."""

    ROOT = REPO_ROOT / "docs/architecture/p12/w3-operations"

    def test_at_least_one_real_join_is_resident_and_resolves(self):
        joins = sorted(self.ROOT.glob("*.governance-join.json"))
        self.assertTrue(joins, "expected p12_w3_governance_escalation.py to "
                               "have been run for real at least once")
        results = reader.resolve_all(self.ROOT, self.ROOT)
        self.assertTrue(any(r["status"] == reader.JOINED for r in results),
                        results)

    def test_the_real_join_names_a_delegation_that_still_resolves(self):
        results = [r for r in reader.resolve_all(self.ROOT, self.ROOT)
                  if r["status"] == reader.JOINED]
        self.assertTrue(results)
        from tools.p12_provenance_verification import delegation_records
        known = {d["delegation_id"] for d in delegation_records()}
        for r in results:
            self.assertIn(r["delegation_id"], known)


if __name__ == "__main__":
    unittest.main()
