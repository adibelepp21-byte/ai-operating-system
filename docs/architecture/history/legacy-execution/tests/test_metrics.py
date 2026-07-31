"""
Regression tests for execution/metrics.py — Tier 4.

Two tests required by the Tier 4 Execution Metrics Implementation
directive, on top of ordinary correctness coverage:

  1. Determinism — the same Observability input must produce
     byte-identical Metrics output across repeated calls.
  2. Layering — metrics.py must not import Trace, Orchestrator, Tool,
     Skill, or any other execution module besides observability.py
     (and observability.py isn't even imported today — metrics.py
     consumes event objects structurally, via duck typing, without
     importing the module that defines their classes).

Uses only the standard library (unittest), consistent with
tools/tests/test_validators.py.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import ast
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import metrics
from execution.observability import SkillTelemetryEvent, ToolCallTelemetry, WorkflowTelemetryEvent

FORBIDDEN_MODULE_PREFIXES = (
    "execution.trace",
    "execution.orchestrator",
    "execution.tool",
    "execution.skill",
    "execution.workflow",
    "execution.runtime",
    "execution.agent_definition",
    "execution.agent_instance",
    "execution.verification",
    "execution.memory",
    "execution.knowledge",
)
ALLOWED_EXECUTION_IMPORT = "execution.observability"


def _make_skill_events():
    return [
        SkillTelemetryEvent(
            trace_id="t1", agent_instance_id="i1", workflow="workflow.a",
            skill_key="skill.alpha", status="success", failure_class=None,
            duration_ms=10.0, tool_calls=(
                ToolCallTelemetry(tool_key="tool.x", resolved=True, cache_status="hit", verification_status="verified"),
            ), timestamp=1.0,
        ),
        SkillTelemetryEvent(
            trace_id="t2", agent_instance_id="i1", workflow="workflow.a",
            skill_key="skill.alpha", status="failure", failure_class="assertion_failed",
            duration_ms=30.0, tool_calls=(
                ToolCallTelemetry(tool_key="tool.x", resolved=False, cache_status="invalidated", verification_status="invalidated"),
            ), timestamp=2.0,
        ),
        SkillTelemetryEvent(
            trace_id="t3", agent_instance_id="i2", workflow="workflow.b",
            skill_key="skill.beta", status="failure", failure_class="not_implemented",
            duration_ms=None, tool_calls=(), timestamp=3.0,
        ),
        SkillTelemetryEvent(
            trace_id="t4", agent_instance_id="i2", workflow="workflow.b",
            skill_key="skill.beta", status="success", failure_class=None,
            duration_ms=20.0, tool_calls=(
                ToolCallTelemetry(tool_key=None, resolved=True, cache_status="not_applicable", verification_status="not_applicable"),
                # production-shaped call: no cache attached at all -- must NOT count
                # toward tool.x's cache_hit_rate denominator (this is the exact
                # misrepresentation the Hardening sprint fixed). tool_key=None here
                # additionally exercises the "excluded from Tool Metrics entirely" path.
                ToolCallTelemetry(tool_key="tool.x", resolved=True, cache_status="not_applicable", verification_status="not_applicable"),
                ToolCallTelemetry(tool_key="tool.x", resolved=False, cache_status="no_entry", verification_status="no_entry"),
            ), timestamp=4.0,
        ),
    ]


def _make_workflow_events():
    return [
        WorkflowTelemetryEvent(agent_instance_id="i1", workflow="workflow.a", duration_ms=100.0, skill_event_count=2, final_status="completed"),
        WorkflowTelemetryEvent(agent_instance_id="i2", workflow="workflow.b", duration_ms=50.0, skill_event_count=2, final_status="failed"),
        WorkflowTelemetryEvent(agent_instance_id="i3", workflow="workflow.a", duration_ms=200.0, skill_event_count=1, final_status="escalated"),
    ]


class SkillMetricsTest(unittest.TestCase):
    def test_groups_and_excludes_not_implemented_from_success_rate(self):
        results = metrics.compute_skill_metrics(_make_skill_events())
        by_key = {m.skill_key: m for m in results}

        alpha = by_key["skill.alpha"]
        self.assertEqual(alpha.total_invocations, 2)
        self.assertEqual(alpha.success_count, 1)
        self.assertEqual(alpha.failure_count, 1)
        self.assertEqual(alpha.success_rate, 0.5)
        self.assertEqual(alpha.median_duration_ms, 20.0)
        self.assertEqual(alpha.max_duration_ms, 30.0)

        beta = by_key["skill.beta"]
        self.assertEqual(beta.total_invocations, 2)
        self.assertEqual(beta.not_implemented_count, 1)
        self.assertEqual(beta.success_count, 1)
        self.assertEqual(beta.failure_count, 0)
        self.assertEqual(beta.success_rate, 1.0)  # not_implemented excluded from denominator


class ToolMetricsTest(unittest.TestCase):
    def test_cache_and_verification_rates_and_live_execution_rate(self):
        results = metrics.compute_tool_metrics(_make_skill_events())
        by_key = {m.tool_key: m for m in results}

        x = by_key["tool.x"]
        self.assertEqual(x.total_calls, 4)  # hit, invalidated, not_applicable, no_entry
        self.assertEqual(x.cache_hit_count, 1)
        self.assertEqual(x.cache_invalidated_count, 1)
        self.assertEqual(x.cache_no_entry_count, 1)
        self.assertEqual(x.cache_not_applicable_count, 1)
        self.assertEqual(x.cache_unknown_count, 0)
        # cache_hit_rate must be computed only over calls where a cache was actually
        # consulted (hit + invalidated + no_entry = 3), excluding not_applicable --
        # the exact fix this Hardening sprint made. A naive hits/total would give
        # 1/4=0.25 instead of the correct 1/3.
        self.assertAlmostEqual(x.cache_hit_rate, 1 / 3)
        self.assertAlmostEqual(x.live_execution_rate, 2 / 3)
        self.assertAlmostEqual(x.cache_hit_rate + x.live_execution_rate, 1.0)
        self.assertEqual(x.verified_count, 1)
        self.assertEqual(x.invalidated_count, 1)
        self.assertEqual(x.verification_rate, 0.5)

        self.assertNotIn(None, by_key)  # tc.tool_key=None call must be excluded entirely

    def test_cache_hit_rate_none_when_no_cache_ever_consulted(self):
        events = [
            SkillTelemetryEvent(
                trace_id="t1", agent_instance_id="i1", workflow="workflow.a",
                skill_key="skill.alpha", status="success", failure_class=None,
                duration_ms=1.0, tool_calls=(
                    ToolCallTelemetry(tool_key="tool.y", resolved=True, cache_status="not_applicable", verification_status="not_applicable"),
                ), timestamp=1.0,
            ),
        ]
        results = metrics.compute_tool_metrics(events)
        y = results[0]
        self.assertEqual(y.cache_not_applicable_count, 1)
        self.assertIsNone(y.cache_hit_rate)
        self.assertIsNone(y.live_execution_rate)


class WorkflowMetricsTest(unittest.TestCase):
    def test_groups_and_success_rate(self):
        results = metrics.compute_workflow_metrics(_make_workflow_events())
        by_key = {m.workflow_key: m for m in results}

        a = by_key["workflow.a"]
        self.assertEqual(a.total_runs, 2)
        self.assertEqual(a.completed_count, 1)
        self.assertEqual(a.escalated_count, 1)
        self.assertEqual(a.success_rate, 0.5)
        self.assertEqual(a.median_duration_ms, 150.0)
        self.assertEqual(a.max_duration_ms, 200.0)


class BottleneckReportTest(unittest.TestCase):
    def test_ranked_descending_by_avg_duration(self):
        report = metrics.bottleneck_report(_make_skill_events(), top_n=5)
        self.assertEqual(report[0].skill_key, "skill.alpha")  # avg (10+30)/2=20 > beta's 20/1=20? tie broken by sort stability
        durations = [e.avg_duration_ms for e in report]
        self.assertEqual(durations, sorted(durations, reverse=True))
        self.assertEqual([e.rank for e in report], list(range(1, len(report) + 1)))


class DeterminismTest(unittest.TestCase):
    """Required test 1: same Observability input -> byte-identical Metrics output."""

    def test_same_input_produces_byte_identical_output(self):
        skill_events = _make_skill_events()
        workflow_events = _make_workflow_events()

        def _snapshot():
            return json.dumps({
                "skill_metrics": [vars(m) for m in metrics.compute_skill_metrics(skill_events)],
                "tool_metrics": [vars(m) for m in metrics.compute_tool_metrics(skill_events)],
                "workflow_metrics": [vars(m) for m in metrics.compute_workflow_metrics(workflow_events)],
                "bottleneck_report": [vars(m) for m in metrics.bottleneck_report(skill_events)],
            }, sort_keys=True)

        first = _snapshot()
        for _ in range(5):
            self.assertEqual(_snapshot(), first)

    def test_real_corpus_determinism(self):
        """Same real, on-disk Observability output run twice must also match."""
        from execution.memory.extractor import load_trace_records
        from execution.observability import extract_skill_events, extract_workflow_events

        records = load_trace_records()
        skill_events = extract_skill_events(records)
        workflow_events = extract_workflow_events(records)

        def _snapshot():
            return json.dumps({
                "skill_metrics": [vars(m) for m in metrics.compute_skill_metrics(skill_events)],
                "tool_metrics": [vars(m) for m in metrics.compute_tool_metrics(skill_events)],
                "workflow_metrics": [vars(m) for m in metrics.compute_workflow_metrics(workflow_events)],
                "bottleneck_report": [vars(m) for m in metrics.bottleneck_report(skill_events)],
            }, sort_keys=True, default=str)

        first = _snapshot()
        second = _snapshot()
        self.assertEqual(first, second)

    def test_inputs_not_mutated(self):
        skill_events = _make_skill_events()
        workflow_events = _make_workflow_events()
        skill_events_copy = list(skill_events)
        workflow_events_copy = list(workflow_events)

        metrics.compute_skill_metrics(skill_events)
        metrics.compute_tool_metrics(skill_events)
        metrics.compute_workflow_metrics(workflow_events)
        metrics.bottleneck_report(skill_events)

        self.assertEqual(skill_events, skill_events_copy)
        self.assertEqual(workflow_events, workflow_events_copy)


class LayeringTest(unittest.TestCase):
    """Required test 2: metrics.py must not import Trace, Orchestrator,
    Tool, Skill, or any other execution module besides observability.py.

    Statically inspects metrics.py's own import statements via `ast`,
    rather than trusting docstring claims or runtime behavior alone —
    a module could avoid importing something at call time yet still
    declare the import at module scope."""

    def test_no_forbidden_execution_imports(self):
        source = Path(metrics.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=metrics.__file__)

        imported_modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                prefix = "." * node.level
                imported_modules.append(f"{prefix}{node.module}")

        for name in imported_modules:
            normalized = name.lstrip(".")
            for forbidden in FORBIDDEN_MODULE_PREFIXES:
                forbidden_leaf = forbidden.split(".")[-1]
                self.assertFalse(
                    normalized == forbidden or normalized.startswith(forbidden + ".") or normalized == forbidden_leaf,
                    f"metrics.py imports forbidden execution module: {name!r}",
                )

        # observability.py is the only execution-internal module metrics.py
        # is permitted to import; as currently written it imports none at
        # all (pure duck typing over the event objects), which trivially
        # satisfies the constraint. This assertion pins that fact so a
        # future change that adds a different execution import fails loudly.
        execution_imports = [
            name for name in imported_modules
            if name.lstrip(".") == "execution" or name.lstrip(".").startswith("execution.") or name.startswith(".")
        ]
        for name in execution_imports:
            normalized = name.lstrip(".")
            self.assertTrue(
                normalized == ALLOWED_EXECUTION_IMPORT or normalized == "observability" or normalized == "",
                f"metrics.py imports execution module other than observability.py: {name!r}",
            )

    def test_no_call_site_in_execution_path(self):
        """metrics.py must not be imported by orchestrator.py, skill.py,
        tool.py, tool_executor.py, or workflow.py — confirms it has no
        call site that could influence execution behavior."""
        execution_dir = Path(metrics.__file__).resolve().parent
        guarded_files = ["orchestrator.py", "skill.py", "tool.py", "tool_executor.py", "workflow.py", "trace.py"]
        for filename in guarded_files:
            path = execution_dir / filename
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                else:
                    continue
                self.assertFalse(
                    any(n.endswith("metrics") for n in names),
                    f"{filename} imports metrics.py — this would give it a call site in the execution path",
                )


if __name__ == "__main__":
    unittest.main()
