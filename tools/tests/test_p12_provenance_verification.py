"""P12-W6 execution provenance conformance (`§34`).

The claim under test is not "eleven elements exist somewhere". It is that
provenance can be **assembled** for an execution. These controls hold apart the
two measurements the module reports, and prove each can move.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_provenance_verification as prov


def _delegation(**over):
    record = {
        "delegation_id": "d1", "delegator": "Claude Code / AIOS Co-Founder",
        "recipient_instance": "i-001", "authority_record": "docs/x.md",
        "objective": "o", "work_scope": ["w"], "capability_scope": ["c"],
        "verification_requirement": "v", "status": "ACTIVE",
    }
    record.update(over)
    return record


def _trace(**over):
    record = {"agent_instance": "i-001", "runtime": "r", "outputs": {"k": 1},
              "status": "success"}
    record.update(over)
    return record


class TheScopeIsSection34s(unittest.TestCase):
    def test_the_eleven_elements_are_section_34s_in_order(self):
        self.assertEqual(
            list(prov.PROVENANCE_ELEMENTS),
            ["actor", "delegator", "authority", "objective", "work scope",
             "capability", "workflow", "runtime", "result", "evidence",
             "verification"])


class CoverageIsReadFromStoredRecords(unittest.TestCase):
    def test_an_element_with_no_declared_key_is_absent(self):
        results = {r.element: r for r in prov.elements(
            delegations=(_delegation(),), traces=(_trace(),))}
        self.assertEqual(results["workflow"].status, prov.ABSENT)
        self.assertEqual(results["evidence"].status, prov.ABSENT)

    def test_a_present_but_empty_key_is_not_coverage(self):
        """`skills_used: []` identifies no skill."""
        results = {r.element: r for r in prov.elements(
            delegations=(_delegation(objective=""),), traces=(_trace(),))}
        self.assertEqual(results["objective"].status, prov.ABSENT)

    def test_a_populated_key_is_coverage(self):
        results = {r.element: r for r in prov.elements(
            delegations=(_delegation(),), traces=(_trace(),))}
        self.assertEqual(results["objective"].status, prov.CARRIED)
        self.assertIn("delegation", results["objective"].carriers)

    def test_an_element_on_two_record_kinds_names_both(self):
        results = {r.element: r for r in prov.elements(
            delegations=(_delegation(),), traces=(_trace(),))}
        self.assertEqual(sorted(results["actor"].carriers),
                         ["delegation", "trace"])

    def test_trace_records_are_read_as_raw_json_not_through_the_reader(self):
        """The reader drops every key outside the ten required fields."""
        from native_core.core.trace.record import from_mapping, REQUIRED_FIELDS
        full = dict.fromkeys(REQUIRED_FIELDS, "x")
        full.update(outputs={"k": 1}, cost_resource_metadata={},
                    skills_used=[], tools_used=[], knowledge_consumed=[],
                    memory_consumed=[], status="success", delegation_id="d1")
        rebuilt = from_mapping(full)
        self.assertFalse(hasattr(rebuilt, "delegation_id"),
                         "if Trace ever carries a delegation link natively, "
                         "this module should read it through the reader")

    def test_stored_records_are_read_from_disk(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = root / "a-run"
            store.mkdir()
            (store / "trace").write_text(
                json.dumps(_trace()) + "\n" + json.dumps(_trace()) + "\n",
                encoding="utf-8")
            with mock.patch.object(prov, "TRACE_ROOT", root):
                self.assertEqual(len(prov.trace_records()), 2)


class AssemblyIsSeparateFromCoverage(unittest.TestCase):
    """Nine carried elements and zero assemblable executions co-exist."""

    def test_an_execution_with_no_delegation_reference_is_not_assemblable(self):
        result = prov.assembly(delegations=(_delegation(),),
                               traces=(_trace(),))
        self.assertEqual(result["status"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(result["joined"], 0)

    def test_a_unique_actor_match_is_still_not_a_join(self):
        """One grant today, two tomorrow, and the same execution turns ambiguous."""
        result = prov.assembly(delegations=(_delegation(),),
                               traces=(_trace(),))
        self.assertEqual(result["joined"], 0)
        self.assertIn("set of grants", result["detail"])

    def test_an_execution_naming_its_delegation_is_assemblable(self):
        result = prov.assembly(
            delegations=(_delegation(),),
            traces=(_trace(delegation_id="d1"),))
        self.assertEqual(result["status"], prov.ASSEMBLABLE)
        self.assertEqual(result["joined"], 1)

    def test_a_reference_to_a_delegation_that_does_not_exist_is_not_a_join(self):
        result = prov.assembly(
            delegations=(_delegation(),),
            traces=(_trace(delegation_id="does-not-exist"),))
        self.assertEqual(result["status"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(result["joined"], 0)

    def test_no_executions_is_not_reported_as_assemblable(self):
        result = prov.assembly(delegations=(_delegation(),), traces=())
        self.assertEqual(result["status"], prov.NO_EXECUTIONS)

    def test_partial_joining_is_not_reported_as_assemblable(self):
        result = prov.assembly(
            delegations=(_delegation(),),
            traces=(_trace(delegation_id="d1"), _trace()))
        self.assertEqual(result["status"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(result["joined"], 1)


class TheLiveCorpusResult(unittest.TestCase):
    def test_the_live_corpus_reports_the_finding(self):
        summary = prov.summary()
        self.assertEqual(summary["elements"], 11)
        self.assertEqual(summary["assembly"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(summary["executions_joined"], 0)

    def test_workflow_and_evidence_are_the_absent_elements(self):
        self.assertEqual(prov.summary()["absent_elements"],
                         ("workflow", "evidence"))

    def test_resident_delegations_are_actually_read(self):
        self.assertGreater(len(prov.delegation_records()), 0)

    def test_resident_traces_are_actually_read(self):
        self.assertGreater(len(prov.trace_records()), 0)


if __name__ == "__main__":
    unittest.main()
