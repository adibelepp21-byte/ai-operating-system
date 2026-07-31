"""
Dedicated unit tests for execution/workflow.py.

Foundation Test Coverage Hardening phase. Exercises load() against real,
on-disk Workflow documents, and WorkflowExecution's observation-of-fact
recording behavior.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import workflow


class LoadTest(unittest.TestCase):
    def test_load_real_workflow_returns_expected_shape(self):
        wf = workflow.load("workflow.pre-ratification-validation")
        self.assertEqual(wf.canonical_key, "workflow.pre-ratification-validation")
        self.assertTrue(wf.path.is_file())
        self.assertIsInstance(wf.skill_paths, tuple)

    def test_skill_paths_are_real_existing_files(self):
        wf = workflow.load("workflow.pre-ratification-validation")
        self.assertGreater(len(wf.skill_paths), 0)
        for p in wf.skill_paths:
            self.assertTrue(p.is_file(), f"{p} does not exist on disk")

    def test_different_real_workflows_load_distinct_skill_sets(self):
        wf1 = workflow.load("workflow.pre-ratification-validation")
        wf2 = workflow.load("workflow.terminology-audit")
        self.assertNotEqual(wf1.skill_paths, wf2.skill_paths)

    def test_load_is_deterministic_and_ordered(self):
        wf1 = workflow.load("workflow.pre-ratification-validation")
        wf2 = workflow.load("workflow.pre-ratification-validation")
        self.assertEqual(wf1.skill_paths, wf2.skill_paths)


class WorkflowExecutionTest(unittest.TestCase):
    def test_record_skill_appends_in_order(self):
        wf_exec = workflow.WorkflowExecution(workflow_key="workflow.x")
        wf_exec.record_skill("skill.a", "success")
        wf_exec.record_skill("skill.b", "failure")
        self.assertEqual(len(wf_exec.skill_records), 2)
        self.assertEqual(wf_exec.skill_records[0].order_index, 0)
        self.assertEqual(wf_exec.skill_records[1].order_index, 1)
        self.assertEqual(wf_exec.skill_records[0].skill_key, "skill.a")
        self.assertEqual(wf_exec.skill_records[1].status, "failure")

    def test_starts_in_progress(self):
        wf_exec = workflow.WorkflowExecution(workflow_key="workflow.x")
        self.assertEqual(wf_exec.completion_state, "in_progress")
        self.assertIsNone(wf_exec.completed_at)

    def test_complete_sets_state_and_timestamp(self):
        wf_exec = workflow.WorkflowExecution(workflow_key="workflow.x")
        wf_exec.complete("completed")
        self.assertEqual(wf_exec.completion_state, "completed")
        self.assertIsNotNone(wf_exec.completed_at)

    def test_each_execution_instance_is_independent(self):
        wf_exec1 = workflow.WorkflowExecution(workflow_key="workflow.x")
        wf_exec2 = workflow.WorkflowExecution(workflow_key="workflow.x")
        wf_exec1.record_skill("skill.a", "success")
        self.assertEqual(len(wf_exec2.skill_records), 0)


if __name__ == "__main__":
    unittest.main()
