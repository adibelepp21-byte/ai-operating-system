"""P12-W6 workflow integration conformance (`§31`).

The unit under test is the **link**. These controls hold the three statuses
apart and prove each can move, so that two evidenced joins out of five is a
measurement rather than a shape.
"""

from __future__ import annotations

import unittest
from unittest import mock

from tools import p12_workflow_verification as wf


class TheScopeIsSection31s(unittest.TestCase):
    def test_the_chain_is_section_31s_in_order(self):
        self.assertEqual(
            list(wf.WORKFLOW_CHAIN),
            ["PLAN", "HANDOFF", "WORK", "EXECUTION", "OBSERVATION",
             "VERIFICATION"])

    def test_five_joins_connect_six_elements(self):
        self.assertEqual(len(wf.WORKFLOW_JOINS), 5)
        self.assertEqual(wf.WORKFLOW_JOINS[0], ("PLAN", "HANDOFF"))
        self.assertEqual(wf.WORKFLOW_JOINS[-1], ("OBSERVATION", "VERIFICATION"))

    def test_every_join_has_a_probe(self):
        self.assertEqual(set(wf._JOINS), set(wf.WORKFLOW_JOINS))


class TheUnitIsTheLinkNotTheElement(unittest.TestCase):
    def test_a_partially_referenced_join_is_by_convention_not_evidenced(self):
        """The weakest link governs: some executions name their work, some do not."""
        result = {(r.source, r.target): r
                  for r in wf.verify()}[("WORK", "EXECUTION")]
        self.assertEqual(result.status, wf.BY_CONVENTION)
        self.assertIn("share only an actor name", result.detail)

    def test_a_join_with_no_references_at_all_names_the_actor(self):
        with mock.patch("tools.p12_provenance_verification.assembly",
                        return_value={"status": "NOT ASSEMBLABLE",
                                      "executions": 3, "joined": 0}):
            result = wf._work_to_execution()
        self.assertEqual(result.evidence, "actor name")

    def test_a_real_reference_makes_the_join_evidenced(self):
        delegation = {"delegation_id": "d1", "recipient_instance": "i-001",
                      "work_scope": ["w"], "lifecycle_boundary": "plan x"}
        trace = {"agent_instance": "i-001", "runtime": "r",
                 "outputs": {"k": 1}, "delegation_id": "d1"}
        with mock.patch.object(wf, "_delegations", return_value=(delegation,)), \
                mock.patch.object(wf, "_traces", return_value=(trace,)), \
                mock.patch("tools.p12_provenance_verification.evidence_records",
                           return_value=()), \
                mock.patch("tools.p12_provenance_verification.manifest_records",
                           return_value=()):
            self.assertEqual(wf._work_to_execution().status, wf.EVIDENCED)

    def test_no_executions_is_broken_not_evidenced(self):
        with mock.patch.object(wf, "_delegations", return_value=()), \
                mock.patch.object(wf, "_traces", return_value=()), \
                mock.patch("tools.p12_provenance_verification.evidence_records",
                           return_value=()), \
                mock.patch("tools.p12_provenance_verification.manifest_records",
                           return_value=()):
            self.assertEqual(wf._work_to_execution().status, wf.BROKEN)


class TheObservationJoinReadsTheRealField(unittest.TestCase):
    """It read `.subject`, which does not exist, and reported BROKEN."""

    def test_the_observation_dataclass_has_runtime_id_not_subject(self):
        import dataclasses
        from tools.p12_runtime_observation import Observation
        names = {f.name for f in dataclasses.fields(Observation)}
        self.assertIn("runtime_id", names)
        self.assertNotIn("subject", names)

    def test_the_join_does_not_report_an_attribute_error_as_a_finding(self):
        result = {(r.source, r.target): r
                  for r in wf.verify()}[("EXECUTION", "OBSERVATION")]
        self.assertNotIn("has no attribute", result.detail)

    def test_a_matching_runtime_name_yields_by_convention(self):
        class _Obs:
            runtime_id = "shared-runtime"
            kind = "runtime"

        with mock.patch.object(wf, "_traces",
                               return_value=({"runtime": "shared-runtime"},)), \
                mock.patch("tools.p12_runtime_observation.observations",
                           return_value=[_Obs()]):
            result = wf._execution_to_observation()
        self.assertEqual(result.status, wf.BY_CONVENTION)

    def test_a_non_matching_runtime_name_yields_broken(self):
        class _Obs:
            runtime_id = "some-other-runtime"
            kind = "runtime"

        with mock.patch.object(wf, "_traces",
                               return_value=({"runtime": "a-runtime"},)), \
                mock.patch("tools.p12_runtime_observation.observations",
                           return_value=[_Obs()]):
            self.assertEqual(wf._execution_to_observation().status, wf.BROKEN)


class TheChainIsConnectedOnlyIfEveryLinkIs(unittest.TestCase):
    def test_one_weak_link_disconnects_the_chain(self):
        self.assertFalse(wf.chain_is_connected())

    def test_by_convention_does_not_count_as_connected(self):
        results = (wf.JoinResult("A", "B", wf.BY_CONVENTION, "name", ""),)
        with mock.patch.object(wf, "verify", return_value=results):
            self.assertFalse(wf.chain_is_connected())

    def test_all_evidenced_connects_the_chain(self):
        results = tuple(
            wf.JoinResult(a, b, wf.EVIDENCED, "ref", "")
            for a, b in wf.WORKFLOW_JOINS)
        with mock.patch.object(wf, "verify", return_value=results):
            self.assertTrue(wf.chain_is_connected())

    def test_the_weakest_links_are_named(self):
        """`OBSERVATION→VERIFICATION` left this list through construction.

        It was BROKEN because no execution record can hold a verified state.
        That is still true — the ratified vocabulary was not widened. The edge
        is now carried by the P12 provenance manifest instead, which is the
        separation `§9` requires. `WORK→EXECUTION` remains weak because three
        older executions have no manifest and must not be given one.
        """
        summary = wf.summary()
        self.assertIn("WORK→EXECUTION", summary["weakest"])
        from native_core.core.trace import VALID_STATUSES
        self.assertNotIn("verified", VALID_STATUSES)

    def test_no_probe_reports_its_own_exception_as_a_finding(self):
        for result in wf.verify():
            with self.subTest(f"{result.source}->{result.target}"):
                self.assertNotIn("probe raised", result.detail)


if __name__ == "__main__":
    unittest.main()
