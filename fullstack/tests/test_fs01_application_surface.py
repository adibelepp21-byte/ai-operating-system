"""FS-01 — each claim of the Application Surface Map, executed or checked.

`docs/fullstack/FS-01-APPLICATION-SURFACE-MAP.md` classifies what AIOS can
expose. Act `§10` forbids declaring a stage complete *"solely because files
exist"*, so every **executable** row is run here through its public contract,
and every **absent** row is checked against the code, not asserted in prose.
"""

from __future__ import annotations

import ast
import subprocess
import tempfile
import unittest
from pathlib import Path

from consumers.cognitive_intelligence_agent import CognitiveIntelligenceAgent
from consumers.engineering_intelligence_agent import (
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from consumers.reference_agent import ReferenceAgent
from consumers.tool_agent import ToolProposingAgent
from consumers.workflow_agent import StepFailed, WorkflowParticipatingAgent
from native_core.core.infrastructure import (
    ExternalTool, InvocationDisposition, LocalAppendOnlyStorage,
    LocalExecutionSubstrate, ToolContract, ToolIdentity)
from native_core.core.runtime import RuntimeState
from native_core.core.runtime.bootstrap import bootstrap_runtime
from native_core.core.runtime.execution import create_execution_layer
from native_core.shared import Success
from native_core.core.trace import TraceReader, TraceWriter
from native_core.core.workflow import (
    AgentInstanceRef, SkillRef, Workflow, WorkflowComposition, WorkflowIdentity,
    WorkflowState, WorkflowStep)

REPO_ROOT = Path(__file__).resolve().parents[2]


class _Echo(ExternalTool):
    canonical_key = "fs01.echo"

    def invoke(self, action, parameters):
        return Success(value=dict(parameters))


def _running(tmp: Path):
    storage = LocalAppendOnlyStorage(tmp / "storage")
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = bootstrap_runtime("fs01-runtime", storage, substrate)
    runtime.start()
    return runtime, storage


class ExecutableClaims(unittest.TestCase):
    """Rows the map classifies as EXECUTABLE."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.runtime, self.storage = _running(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def test_runtime_lifecycle(self):
        self.assertIs(RuntimeState.RUNNING, self.runtime.state)
        self.runtime.stop()
        self.assertIs(RuntimeState.STOPPED, self.runtime.state)

    def test_execution_is_minted_by_the_running_runtime(self):
        first = create_execution_layer(self.runtime)
        second = create_execution_layer(self.runtime)
        self.assertIs(self.runtime, first.runtime)
        self.assertLess(first.context.execution_sequence,
                        second.context.execution_sequence)

    def test_an_agent_action_writes_exactly_one_durable_trace(self):
        ReferenceAgent(trace_writer=TraceWriter(self.storage)).participate(
            create_execution_layer(self.runtime))
        reopened = LocalAppendOnlyStorage(self.tmp / "storage")
        reopened.provision()
        records = list(TraceReader(reopened).read())
        self.assertEqual(1, len(records))
        self.assertEqual(("reference-agent", "fs01-runtime", "success"),
                         (records[0].agent_instance, records[0].runtime,
                          records[0].status))

    def test_workflow_lifecycle_success_and_failure(self):
        steps = WorkflowComposition(steps=(
            WorkflowStep("a", AgentInstanceRef("x"), SkillRef("s")),
            WorkflowStep("b", AgentInstanceRef("x"), SkillRef("s"))))
        ok = WorkflowParticipatingAgent(
            workflow=Workflow(WorkflowIdentity("fs01-ok", "1")), composition=steps)
        self.assertIs(WorkflowState.SUCCEEDED,
                      ok.participate(create_execution_layer(self.runtime)).state)

        def fail(step):
            raise StepFailed("step b refused")

        bad = WorkflowParticipatingAgent(
            workflow=Workflow(WorkflowIdentity("fs01-bad", "1")), composition=steps,
            performer=fail)
        final = bad.participate(create_execution_layer(self.runtime))
        self.assertIs(WorkflowState.FAILED, final.state)
        monitor = self.runtime.workflows.monitor
        self.assertTrue(monitor.is_failure(WorkflowIdentity("fs01-bad", "1")))

    def test_tool_governance_distinguishes_four_outcomes(self):
        tools = self.runtime.tools
        tools.registry.define(ToolIdentity("fs01.echo"),
                              ToolContract(actions=("echo",),
                                           required_parameters={"echo": ("text",)}))
        tools.registry.register("fs01.echo")
        tools.boundary.register(_Echo())
        propose = lambda action, params: ToolProposingAgent(  # noqa: E731
            proposal=("fs01.echo", action, params)).participate(
                create_execution_layer(self.runtime))
        propose("echo", {"text": "x"})          # registered, not enabled
        tools.registry.enable("fs01.echo")
        propose("echo", {"text": "x"})          # success
        propose("echo", {})                     # invalid
        dispositions = [r.disposition for r in tools.ledger.records]
        self.assertEqual([InvocationDisposition.GOVERNANCE_REFUSAL,
                          InvocationDisposition.SUCCESS,
                          InvocationDisposition.INVALID_INVOCATION], dispositions)

    def test_cognitive_decomposition(self):
        agent = CognitiveIntelligenceAgent(unit_of_work="read; derive; record")
        agent.participate(create_execution_layer(self.runtime))
        self.assertEqual(3, len(agent.decomposition))

    def test_engineering_verification(self):
        agent = EngineeringIntelligenceAgent(
            artifact=Artifact("doc", ("INV-4 holds",)),
            criteria=(ConformanceCriterion("inv4", "INV-4"),
                      ConformanceCriterion("inv99", "INV-99")))
        agent.participate(create_execution_layer(self.runtime))
        self.assertEqual([True, False], [r.satisfied for r in agent.results])

    def test_knowledge_and_memory_are_hosted_while_running(self):
        self.assertIsNotNone(self.runtime.knowledge.repository)
        self.assertIsNotNone(self.runtime.memory.retrieval)


def _tracked_python():
    names = subprocess.run(["git", "ls-files", "*.py"], cwd=str(REPO_ROOT),
                           capture_output=True, text=True, check=True).stdout.split()
    return [n for n in names if "/tests/" not in n and not n.startswith("fullstack/")]


def _imports(name):
    tree = ast.parse((REPO_ROOT / name).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module.split(".")[0]


class AbsentClaims(unittest.TestCase):
    """Rows the map classifies as ABSENT at entry, outside `fullstack/`."""

    def test_no_network_interface_exists_outside_the_full_stack(self):
        network = {"http", "wsgiref", "socketserver", "socket", "asyncio"}
        users = [n for n in _tracked_python() if network & set(_imports(n))]
        self.assertEqual([], users)

    def test_no_database_driver_exists(self):
        drivers = {"sqlite3", "psycopg", "psycopg2", "sqlalchemy", "supabase"}
        users = [n for n in _tracked_python() if drivers & set(_imports(n))]
        self.assertEqual([], users)

    def test_the_agent_boundary_offers_no_governed_creation(self):
        """The Agent Factory is reserved: the boundary exports the contract only."""
        import native_core.core.agent as agent
        self.assertEqual(["Agent"], agent.__all__)

    def test_no_concrete_tool_is_registered_outside_tests(self):
        registrations = [n for n in _tracked_python()
                         if ".boundary.register(" in (REPO_ROOT / n).read_text(encoding="utf-8")]
        self.assertEqual([], registrations)


if __name__ == "__main__":
    unittest.main()
