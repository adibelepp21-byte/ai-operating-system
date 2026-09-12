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
            delegations=(_delegation(),), traces=(_trace(),), evidence=())}
        self.assertEqual(results["workflow"].status, prov.ABSENT)
        self.assertEqual(results["evidence"].status, prov.ABSENT)

    def test_a_present_but_empty_key_is_not_coverage(self):
        """`skills_used: []` identifies no skill."""
        results = {r.element: r for r in prov.elements(
            delegations=(_delegation(objective=""),), traces=(_trace(),),
            evidence=())}
        self.assertEqual(results["objective"].status, prov.ABSENT)

    def test_a_populated_key_is_coverage(self):
        results = {r.element: r for r in prov.elements(
            delegations=(_delegation(),), traces=(_trace(),), evidence=())}
        self.assertEqual(results["objective"].status, prov.CARRIED)
        self.assertIn("delegation", results["objective"].carriers)

    def test_an_element_on_two_record_kinds_names_both(self):
        results = {r.element: r for r in prov.elements(
            delegations=(_delegation(),), traces=(_trace(),), evidence=())}
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
                               traces=(_trace(),), evidence=())
        self.assertEqual(result["status"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(result["joined"], 0)

    def test_a_unique_actor_match_is_still_not_a_join(self):
        """One grant today, two tomorrow, and the same execution turns ambiguous."""
        result = prov.assembly(delegations=(_delegation(),),
                               traces=(_trace(),), evidence=())
        self.assertEqual(result["joined"], 0)
        self.assertIn("set of grants", result["detail"])

    def test_an_execution_naming_its_delegation_is_assemblable(self):
        result = prov.assembly(
            delegations=(_delegation(),),
            traces=(_trace(delegation_id="d1"),), evidence=())
        self.assertEqual(result["status"], prov.ASSEMBLABLE)
        self.assertEqual(result["joined"], 1)

    def test_a_reference_to_a_delegation_that_does_not_exist_is_not_a_join(self):
        result = prov.assembly(
            delegations=(_delegation(),),
            traces=(_trace(delegation_id="does-not-exist"),), evidence=())
        self.assertEqual(result["status"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(result["joined"], 0)

    def test_no_executions_is_not_reported_as_assemblable(self):
        result = prov.assembly(delegations=(_delegation(),), traces=(),
                               evidence=())
        self.assertEqual(result["status"], prov.NO_EXECUTIONS)

    def test_partial_joining_is_not_reported_as_assemblable(self):
        result = prov.assembly(
            delegations=(_delegation(),),
            traces=(_trace(delegation_id="d1"), _trace()), evidence=())
        self.assertEqual(result["status"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(result["joined"], 1)


class TheLiveCorpusResult(unittest.TestCase):
    """Corrected after the original finding was falsified.

    The first version of these controls asserted `absent_elements ==
    ("workflow", "evidence")` and `executions_joined == 0`. **Both encoded a
    false finding.** The module measured only delegation records and Trace
    records; the resident `*.evidence.json` execution records — which carry
    `goal`, `plan`, `plan_authority`, the step-to-grant mapping, `workflow_steps`
    and `delegation_id` in one artifact — were outside the population.

    These assertions were changed because they were **wrong**, not to make an
    implementation pass. The distinction matters and is the reason this
    docstring exists: the corrected controls assert a *stronger* result on the
    element side and preserve the real gap on the assembly side.
    """

    def test_every_section_34_element_is_carried(self):
        summary = prov.summary()
        self.assertEqual(summary["carried"], 11)
        self.assertEqual(summary["absent_elements"], ())

    def test_the_real_gap_is_the_unmanifested_trace_records(self):
        """Updated after P12-W4 construction closed part of the gap.

        `trace_joined` was `0/2` before the execution provenance manifest
        existed. It is now `1/4`: the execution that ran under the new
        integration is joined, and three older Trace records are not. They are
        not retroactively joined, because writing a manifest for an execution
        that did not produce one would be manufacturing historical evidence.
        """
        summary = prov.summary()
        self.assertEqual(summary["assembly"], prov.NOT_ASSEMBLABLE)
        self.assertEqual(summary["evidence_joined"], "3/3")
        joined, total = summary["trace_joined"].split("/")
        self.assertGreaterEqual(int(joined), 1)
        self.assertLess(int(joined), int(total),
                        "older executions must not become joined by fiat")
        self.assertGreaterEqual(summary["manifests"], 1)

    def test_a_manifest_naming_an_unknown_delegation_does_not_join(self):
        trace = dict(_trace(), __store="s", __ordinal=0)
        fake = {"trace_store": "s", "trace_ordinal": 0,
                "delegation_id": "not-a-real-grant"}
        result = prov.assembly(delegations=(_delegation(),), traces=(trace,),
                               evidence=(), manifests=(fake,))
        self.assertEqual(result["trace_joined"], 0)

    def test_a_manifest_naming_a_real_delegation_joins_its_own_record_only(self):
        traces = (dict(_trace(), __store="s", __ordinal=0),
                  dict(_trace(), __store="s", __ordinal=1))
        manifest = {"trace_store": "s", "trace_ordinal": 0,
                    "delegation_id": "d1"}
        result = prov.assembly(delegations=(_delegation(),), traces=traces,
                               evidence=(), manifests=(manifest,))
        self.assertEqual(result["trace_joined"], 1,
                         "a manifest joins the record it addresses, not every "
                         "record sharing a runtime name")

    def test_evidence_records_carry_the_join_trace_records_lack(self):
        for record in prov.evidence_records():
            with self.subTest(record.get("goal")):
                self.assertTrue(record.get("delegation_id"))
        for record in prov.trace_records():
            with self.subTest(record.get("runtime")):
                self.assertIsNone(record.get("delegation_id"))

    def test_resident_delegations_are_actually_read(self):
        self.assertGreater(len(prov.delegation_records()), 0)

    def test_resident_traces_are_actually_read(self):
        self.assertGreater(len(prov.trace_records()), 0)

    def test_resident_evidence_records_are_actually_read(self):
        self.assertGreater(len(prov.evidence_records()), 0)


if __name__ == "__main__":
    unittest.main()
