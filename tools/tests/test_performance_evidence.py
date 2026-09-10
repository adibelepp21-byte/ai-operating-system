"""`W6 → W2` evidence path — real transition, no authority path.

`ACT-CC-P11-006 §16`: each transition must be **real**, and *"Existence is not
connection."* `§14`: Performance may observe, measure, detect, publish and
surface; it may not authorize, approve, promote or decide.
"""

import ast
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.optimization import OptimizationObservation  # noqa: E402
from tools.performance_evidence import (  # noqa: E402
    UnobservableSource,
    as_planning_evidence,
    collect,
)
from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    EscalationRequired,
    Goal,
    Plan,
    PlanStep,
    PlanningEvidence,
    PlanningSurface,
)

ADAPTER = REPO_ROOT / "tools" / "performance_evidence.py"
PLANNING = REPO_ROOT / "tools" / "planning"
AUTHORITY = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"


def _imports(path: Path):
    names = set()
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


class TheTransitionIsReal(unittest.TestCase):
    """Before this module, both endpoints existed and nothing joined them."""

    def test_an_observation_becomes_planning_evidence(self):
        evidence = as_planning_evidence(
            OptimizationObservation(source="trace", subject="step-b",
                                    observed="failed twice"))
        self.assertIsInstance(evidence, PlanningEvidence)
        self.assertEqual(evidence.source, "optimization/trace")
        self.assertIn("failed twice", evidence.observation)

    def test_the_evidence_reaches_a_real_plan_adaptation(self):
        """End to end: Optimization observes, Planning adapts. The whole point."""
        authority = AuthorityProvenance("DP-01 §3 W2", AUTHORITY)
        surface = PlanningSurface()
        surface.declare(Goal("g", "Intent.", authority))
        plan = surface.adopt(Plan(key="p", goal_key="g", authority=authority,
                                  steps=(PlanStep("b", "B."),)))
        evidence = collect([OptimizationObservation(
            source="trace", subject="step-b", observed="failed twice")])
        adapted = surface.adapt(
            plan, steps=plan.steps + (PlanStep("retry", "Retry differently.",
                                               depends_on=("b",)),),
            reason="Observation showed the step failing.", evidence=evidence)
        self.assertEqual(len(adapted.steps), 2)
        self.assertEqual(adapted.evidence,
                         ("optimization/trace: step-b: failed twice",))

    def test_a_batch_preserves_order_and_ranks_nothing(self):
        observations = [
            OptimizationObservation(source="trace", subject=f"s{i}",
                                    observed="x" * (10 - i)) for i in range(3)]
        self.assertEqual([e.observation.split(":")[0]
                          for e in collect(observations)], ["s0", "s1", "s2"])


class TheAdapterFailsClosed(unittest.TestCase):
    def test_an_unobservable_source_is_refused(self):
        """Defence in depth against a route that genuinely exists.

        The frozen boundary already refuses an unobservable source at
        construction, so this guard is unreachable through the constructor —
        which made it look like a check that cannot fail. It is not.
        `OptimizationObservation` is a frozen dataclass, and
        ``object.__setattr__`` bypasses frozen validation, so an observation
        carrying an arbitrary source **can** reach this adapter. Verified by
        constructing exactly that case rather than assuming either way.
        """
        smuggled = OptimizationObservation(source="trace", subject="x",
                                           observed="approved")
        object.__setattr__(smuggled, "source", "founder")
        self.assertEqual(smuggled.source, "founder")
        with self.assertRaises(UnobservableSource):
            as_planning_evidence(smuggled)

    def test_the_frozen_boundary_refuses_it_first_by_the_normal_route(self):
        """The layer this guard sits behind, asserted so the order is visible."""
        from native_core.core.optimization import InvalidObservation
        with self.assertRaises(InvalidObservation):
            OptimizationObservation(source="founder", subject="x",
                                    observed="approved")

    def test_arbitrary_objects_cannot_enter_planning_as_evidence(self):
        for bad in ("just a string", 42, None, {"source": "trace"}):
            with self.subTest(value=bad):
                with self.assertRaises(TypeError):
                    as_planning_evidence(bad)


class TheAdapterCreatesNoAuthorityPath(unittest.TestCase):
    """`DP-01 §3 W6`: ``PERFORMANCE EVIDENCE ≠ PLANNING AUTHORITY``."""

    def test_the_adapter_does_not_reach_governance(self):
        self.assertEqual([m for m in _imports(ADAPTER) if "governance" in m], [])

    def test_the_adapter_neither_decides_nor_adapts(self):
        """It holds no plan and no surface, so it cannot act on what it finds."""
        source = ADAPTER.read_text(encoding="utf-8")
        tree = ast.parse(source)
        called = {node.func.attr for node in ast.walk(tree)
                  if isinstance(node, ast.Call)
                  and isinstance(node.func, ast.Attribute)}
        for forbidden in ("adapt", "revise", "adopt", "declare"):
            self.assertNotIn(forbidden, called)
        self.assertEqual([m for m in _imports(ADAPTER)
                          if m.endswith("surface")], [])

    def test_observation_through_the_real_path_still_cannot_authorize(self):
        """The end-to-end case that matters: genuine Optimization evidence,
        offered to a change that needs authority the plan does not hold."""
        authority = AuthorityProvenance("DP-01 §3 W2", AUTHORITY)
        surface = PlanningSurface()
        surface.declare(Goal("g", "Intent.", authority))
        plan = surface.adopt(Plan(key="p", goal_key="g", authority=authority,
                                  steps=(PlanStep("b", "B."),)))
        evidence = collect([OptimizationObservation(
            source="memory", subject="x", observed="strongly indicated")
            for _ in range(10)])
        with self.assertRaises(EscalationRequired):
            surface.adapt(plan, steps=plan.steps, reason="Observed.",
                          evidence=evidence, required_authority="DP-02")


class TheDependencyDirectionStaysInverted(unittest.TestCase):
    """The reason this module is not inside either endpoint.

    Optimization's boundary states *"no subsystem imports Optimization — no
    inversion, no cycle"*. Putting the adapter inside Planning would make
    Planning depend on Optimization; putting it inside Optimization would make
    the detect-only boundary aware of a consumer. It sits outside both.
    """

    def test_planning_still_does_not_import_optimization(self):
        for path in sorted(PLANNING.glob("*.py")):
            with self.subTest(module=path.name):
                self.assertEqual(
                    [m for m in _imports(path) if "optimization" in m], [])

    def test_planning_still_does_not_import_this_adapter(self):
        for path in sorted(PLANNING.glob("*.py")):
            with self.subTest(module=path.name):
                self.assertEqual(
                    [m for m in _imports(path) if "performance_evidence" in m], [])

    def test_the_adapter_depends_on_both_endpoints(self):
        imports = _imports(ADAPTER)
        self.assertTrue(any("optimization" in m for m in imports))
        self.assertTrue(any("planning" in m for m in imports))


if __name__ == "__main__":
    unittest.main()
