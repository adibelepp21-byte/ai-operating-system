"""
Agent execution semantics — BOUNDED BEHAVIOURAL EVIDENCE (ACT-CC-P6-038).

WHAT THIS MODULE IS. Evidence infrastructure produced under the Co-Founder
Delegation Charter (§4.2 test strategy, §4.5 verification) to close the
producible half of the evidence gap recorded at `ACT-CC-P6-037 §4`. It
exercises the claims of `docs/engineering/agent/agent_execution_semantics_spec.md`
that can be evidenced **without constructing E-01**, and nothing else.

WHAT THIS MODULE IS NOT.
  - It is **not** an implementation of `Agent` or of `participate()`. The
    consumer below is a disposable test fixture. No production code is added to
    `native_core/`, and `E-01` remains unconstructed.
  - It is **not** canon. A passing test here is `[E] behaviour observed under a
    specified condition` — never `[E] the specification is ratified`.
  - It is **disposable evidence infrastructure** unless separately adopted,
    following the `ACT-CC-P6-015 §5` precedent.

WHAT IT DELIBERATELY DOES NOT EVIDENCE — and why.
  **Trace obligations (INV-4).** The spec states that an accepted action
  produces exactly one Trace (§7, §15, §16) but deliberately does not specify
  *how* an Agent produces it, and §17.2 bars this work from changing Trace, its
  storage, or its writer. A fixture that wrote a Trace would have to invent that
  unspecified mechanism. **No Trace is written here, and no Trace obligation is
  evidenced.** That half of the evidence remains unproducible until construction
  — the ordering finding recorded at `ACT-CC-P6-037 §4`.

BOUNDARIES OBSERVED.
  - `test_agent_conformance.py` is **not modified, appended to, or imported
    from.** This is a separate module by design.
  - **No Capability import**, consistent with the boundary the conformance suite
    asserts by equality.
  - The Capability reference is **OPTIONAL** (`DEC-P6-033`). Scope D evidences
    that an execution is valid without one. **No test asserts a reference is
    present, asserts it is absent, or derives invocation from it** (spec §18.6).
  - No halt-message text is asserted; exception **types** only (spec §10).
"""

from __future__ import annotations

import ast
import pathlib
import unittest

from native_core.core.agent import Agent
from native_core.core.infrastructure import (
    LocalAppendOnlyStorage,
    LocalExecutionSubstrate,
)
from native_core.core.runtime.exceptions import RuntimeNotRunning, RuntimeSubsystemError
from native_core.core.runtime.execution.composition import create_execution_layer
from native_core.core.runtime.execution.context import ExecutionContext
from native_core.core.runtime.execution.exceptions import (
    ExecutionError,
    InvalidExecutionConfiguration,
)
from native_core.core.runtime.execution.session import ExecutionSession
from native_core.core.runtime.runtime import AIOSRuntime

_REPO = pathlib.Path(__file__).resolve().parents[4]


def _facilities(tmp):
    storage = LocalAppendOnlyStorage(base_dir=tmp / "storage")
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    return storage, substrate


def _running_runtime(tmp, runtime_id="evidence-runtime"):
    storage, substrate = _facilities(tmp)
    runtime = AIOSRuntime(runtime_id=runtime_id, storage=storage, substrate=substrate)
    runtime.initialize()
    runtime.start()
    return runtime


class _RecordingConsumer(Agent):
    """Disposable fixture. Records what it was handed; references no Capability."""

    def __init__(self):
        self.received = None
        self.calls = 0

    def participate(self, execution) -> None:
        self.calls += 1
        self.received = execution
        return None


class _FailingConsumer(Agent):
    """Disposable fixture. Fails an accepted participation under ExecutionError."""

    def participate(self, execution) -> None:
        raise ExecutionError("accepted participation did not complete")


class ScopeARejection(unittest.TestCase):
    """spec §4, §15 T2 — refusal before acceptance."""

    def setUp(self):
        import tempfile

        self.tmp = pathlib.Path(tempfile.mkdtemp())

    def test_boundary_cannot_be_built_against_a_non_running_runtime(self):
        storage, substrate = _facilities(self.tmp)
        runtime = AIOSRuntime(runtime_id="not-started", storage=storage, substrate=substrate)
        with self.assertRaises(RuntimeNotRunning):
            create_execution_layer(runtime)

    def test_rejection_raises_rather_than_returns(self):
        storage, substrate = _facilities(self.tmp)
        runtime = AIOSRuntime(runtime_id="not-started", storage=storage, substrate=substrate)
        outcome = None
        try:
            outcome = create_execution_layer(runtime)
        except RuntimeNotRunning:
            pass
        self.assertIsNone(outcome, "a rejection must not yield a boundary object")

    def test_malformed_binding_is_refused(self):
        with self.assertRaises(InvalidExecutionConfiguration):
            ExecutionSession(_runtime=object(), _context=ExecutionContext("r", 0))

    def test_rejection_is_within_the_fail_closed_taxonomy(self):
        self.assertTrue(issubclass(RuntimeNotRunning, RuntimeSubsystemError))
        self.assertTrue(issubclass(InvalidExecutionConfiguration, RuntimeSubsystemError))


class ScopeBParticipation(unittest.TestCase):
    """spec §13 — entry, and what the consumer is handed."""

    def setUp(self):
        import tempfile

        self.runtime = _running_runtime(pathlib.Path(tempfile.mkdtemp()))

    def test_consumer_receives_the_bound_execution(self):
        execution = create_execution_layer(self.runtime)
        consumer = _RecordingConsumer()
        consumer.participate(execution)
        self.assertIs(consumer.received, execution)
        self.assertIs(consumer.received.runtime, self.runtime)
        self.assertIsInstance(consumer.received.context, ExecutionContext)

    def test_completion_signal_is_none(self):
        execution = create_execution_layer(self.runtime)
        self.assertIsNone(_RecordingConsumer().participate(execution))

    def test_execution_exposes_only_runtime_and_context(self):
        execution = create_execution_layer(self.runtime)
        public = {n for n in dir(execution) if not n.startswith("_")}
        self.assertEqual({"runtime", "context"}, public)


class ScopeCFailure(unittest.TestCase):
    """spec §5 — an accepted participation that does not complete."""

    def setUp(self):
        import tempfile

        self.runtime = _running_runtime(pathlib.Path(tempfile.mkdtemp()))

    def test_failure_propagates_under_execution_error(self):
        execution = create_execution_layer(self.runtime)
        with self.assertRaises(ExecutionError):
            _FailingConsumer().participate(execution)

    def test_execution_error_is_within_the_fail_closed_taxonomy(self):
        self.assertTrue(issubclass(ExecutionError, RuntimeSubsystemError))

    def test_failure_yields_no_result_object(self):
        execution = create_execution_layer(self.runtime)
        outcome = None
        try:
            outcome = _FailingConsumer().participate(execution)
        except ExecutionError:
            pass
        self.assertIsNone(outcome, "a failure must not yield a result")


class ScopeDCapabilityIndependence(unittest.TestCase):
    """spec §18 — OPTIONAL: an execution is valid with no Capability reference."""

    def setUp(self):
        import tempfile

        self.runtime = _running_runtime(pathlib.Path(tempfile.mkdtemp()))

    def test_execution_completes_with_a_consumer_referencing_no_capability(self):
        execution = create_execution_layer(self.runtime)
        consumer = _RecordingConsumer()
        self.assertIsNone(consumer.participate(execution))
        self.assertEqual(1, consumer.calls)

    def test_agent_boundary_imports_nothing_from_capability(self):
        reached = set()
        pkg = _REPO / "native_core" / "core" / "agent"
        for path in pkg.rglob("*.py"):
            if "tests" in path.parts:
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.ImportFrom) and (node.level or 0) >= 2:
                    reached.add((node.module or "").split(".")[0])
        self.assertEqual({"runtime"}, reached)


class ScopeENoResumption(unittest.TestCase):
    """spec §15.2 — a further participation is a different execution."""

    def test_each_execution_carries_a_distinct_runtime_issued_ordinal(self):
        import tempfile

        runtime = _running_runtime(pathlib.Path(tempfile.mkdtemp()))
        first = create_execution_layer(runtime)
        second = create_execution_layer(runtime)
        self.assertNotEqual(
            first.context.execution_sequence, second.context.execution_sequence
        )
        self.assertEqual(first.context.runtime_id, second.context.runtime_id)


class ScopeFNegativeEvidence(unittest.TestCase):
    """spec §9 — negative evidence is required, not optional."""

    def test_no_participate_implementation_exists_outside_the_declaration(self):
        found = []
        for path in (_REPO / "native_core").rglob("*.py"):
            if "tests" in path.parts or path.name == "consumer.py":
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.FunctionDef) and node.name == "participate":
                    found.append(str(path))
        self.assertEqual([], found, "E-01 must remain unconstructed")

    def test_capability_boundary_exposes_no_execution_primitive(self):
        forbidden = {"execute", "run", "invoke", "call", "perform"}
        found = []
        for path in (_REPO / "native_core" / "core" / "capability").rglob("*.py"):
            if "tests" in path.parts:
                continue
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node, ast.FunctionDef) and node.name in forbidden:
                    found.append(f"{path.name}:{node.name}")
        self.assertEqual([], found)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
