"""
Dedicated unit tests for execution/orchestrator.py.

Foundation Test Coverage Hardening phase. Runs the real orchestrator
end-to-end against the real Agent Definition, real Runtime catalog, and
real Workflow/Skill/Tool documents -- the only isolation is TRACE_DIR,
redirected to a temporary directory so the real execution/traces/ corpus
is never touched (same pattern already established by
execution/tests/test_review_decision.py).

Two boundary cases (workflow not permitted, skill not permitted) have no
real negative-case data in the current Agent Definition (every real
workflow and implemented skill it declares is currently permitted) --
these two tests use a controlled substitution of agent_definition.load()
to exercise the authorization-refusal path, which is otherwise
unreachable with real data today. This is disclosed, not hidden.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import agent_definition, orchestrator, trace


class RealEndToEndRunTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.patcher = mock.patch.object(trace, "TRACE_DIR", Path(self.tmpdir.name))
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.tmpdir.cleanup()

    def test_real_run_produces_a_result_with_expected_shape(self):
        result = orchestrator.run(workflow_key="workflow.pre-ratification-validation")
        self.assertIn("agent_instance_id", result)
        self.assertIn("trace_file", result)
        self.assertEqual(result["workflow"], "workflow.pre-ratification-validation")
        self.assertIn(result["workflow_completion_state"], ("completed", "failed", "escalated"))

    def test_real_run_writes_spawn_and_terminate_records(self):
        result = orchestrator.run(workflow_key="workflow.pre-ratification-validation")
        trace_file = Path(result["trace_file"])
        lines = trace_file.read_text(encoding="utf-8").splitlines()
        self.assertGreaterEqual(len(lines), 2)  # at minimum spawn + terminate

        import json
        records = [json.loads(l) for l in lines]
        events = [r["outputs"].get("event") for r in records if "event" in (r.get("outputs") or {})]
        self.assertIn("spawned", events)
        self.assertIn("terminated", events)

    def test_real_run_is_append_only_across_multiple_writers(self):
        result = orchestrator.run(workflow_key="workflow.pre-ratification-validation")
        trace_file = Path(result["trace_file"])
        count_after_one_run = len(trace_file.read_text(encoding="utf-8").splitlines())
        # a second real run uses a fresh TraceWriter (fresh file) -- confirm no cross-contamination
        result2 = orchestrator.run(workflow_key="workflow.pre-ratification-validation")
        self.assertNotEqual(result["trace_file"], result2["trace_file"])
        self.assertEqual(len(Path(result["trace_file"]).read_text(encoding="utf-8").splitlines()), count_after_one_run)

    def test_not_implemented_skill_produces_failure_status_not_a_crash(self):
        """workflow.post-amendment-consistency-sweep includes
        skill.governance-cross-reference-scan, which has no registered
        handler in skill.py -- a real, already-observed not_implemented
        path (also present in the real Trace corpus)."""
        result = orchestrator.run(workflow_key="workflow.post-amendment-consistency-sweep")
        statuses = {r["skill"]: r["status"] for r in result["skill_reports"]}
        self.assertIn("skill.governance-cross-reference-scan", statuses)
        self.assertEqual(statuses["skill.governance-cross-reference-scan"], "not_implemented")

    def test_result_reports_real_trace_ids_that_exist_on_disk(self):
        result = orchestrator.run(workflow_key="workflow.pre-ratification-validation")
        trace_file = Path(result["trace_file"])
        self.assertTrue(trace_file.is_file())


class AuthorizationBoundaryTest(unittest.TestCase):
    """Controlled substitution -- see module docstring. No real negative
    case exists in the current Agent Definition for either boundary."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.patcher = mock.patch.object(trace, "TRACE_DIR", Path(self.tmpdir.name))
        self.patcher.start()
        self.real_ad = agent_definition.load()

    def tearDown(self):
        self.patcher.stop()
        self.tmpdir.cleanup()

    def test_workflow_not_in_permitted_workflows_is_refused_and_recorded(self):
        restricted_ad = replace(self.real_ad, permitted_workflows=())
        with mock.patch.object(agent_definition, "load", return_value=restricted_ad):
            with self.assertRaises(orchestrator.AuthorizationError):
                orchestrator.run(workflow_key="workflow.pre-ratification-validation")

        # the escalation must still be recorded to Trace before raising
        trace_files = list(Path(self.tmpdir.name).glob("*.jsonl"))
        self.assertEqual(len(trace_files), 1)
        import json
        records = [json.loads(l) for l in trace_files[0].read_text(encoding="utf-8").splitlines()]
        statuses = [r["status"] for r in records]
        self.assertIn("escalation", statuses)

    def test_skill_not_in_permitted_skills_is_refused_but_run_continues(self):
        restricted_ad = replace(self.real_ad, permitted_skills=())
        with mock.patch.object(agent_definition, "load", return_value=restricted_ad):
            result = orchestrator.run(workflow_key="workflow.pre-ratification-validation")
        statuses = {r["status"] for r in result["skill_reports"]}
        self.assertIn("escalation", statuses)
        self.assertEqual(result["workflow_completion_state"], "escalated")

    def test_authorization_error_is_raised_only_for_workflow_not_skill(self):
        restricted_ad = replace(self.real_ad, permitted_skills=())
        with mock.patch.object(agent_definition, "load", return_value=restricted_ad):
            # skill-level escalation must NOT raise -- only workflow-level does
            try:
                orchestrator.run(workflow_key="workflow.pre-ratification-validation")
            except orchestrator.AuthorizationError:
                self.fail("skill-level escalation incorrectly raised AuthorizationError")


if __name__ == "__main__":
    unittest.main()
