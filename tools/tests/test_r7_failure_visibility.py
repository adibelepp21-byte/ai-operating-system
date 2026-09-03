"""
`ACT-CC-R7 §10`–`§11` — a `failure` record must actually reach the derived view.

This is the downstream half of the R7 evidence. The producer half — that a Tool
invocation's *disposition*, not its `execution_attempted` flag, decides the
status written — is locked in
`consumers/tests/test_r7_trace_outcome_integrity.py`. What that suite cannot
establish is why the R6 defect was *systemic*: `self_knowledge()` selects
failures by `status == "failure"`, so a genuine execution failure filed as
`success` was invisible to the system's own account of itself.

**Why the chain is verified across two suites rather than one.** `consumers/`
and `tools/` are mutually isolated by resident conformance guards —
`TestResidency.test_the_region_depends_on_nothing_in_tools` and
`TestTheCoreRemainsUnaware.test_tools_imports_nothing_from_consumers` — and both
scan test files. So no test may import across the seam, in either direction. The
seam itself is the contract: a `TraceRecord` carrying `status="failure"`. The
producer suite proves a failed invocation writes exactly that; this suite proves
exactly that is what the projection surfaces. Verifying each region against the
shared record — rather than against the other region — is the discipline those
guards exist to enforce, and R7 was not authorized to relax either of them.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.trace import TraceReader, TraceWriter, new_record
from tools.derived_views import UNKNOWN, VERIFIED, self_knowledge


def _reader_over(*statuses):
    """A Trace store holding one record per status, written through the real
    writer and read back through the real reader — the same production pair the
    consumer region writes with."""
    storage = LocalAppendOnlyStorage(Path(tempfile.mkdtemp()))
    storage.provision()
    writer = TraceWriter(storage)
    for status in statuses:
        writer.write(
            new_record(
                agent_definition_version="unversioned",
                agent_instance="tool-proposing-agent",
                runtime="r7-view",
                tools_used=("r7.tool",),
                outputs=(
                    {"reason": "EXECUTION_FAILURE for r7.tool.run"}
                    if status == "failure"
                    else {"disposition": "SUCCESS"}
                ),
                status=status,
            )
        )
    return TraceReader(storage)


class AFailureRecordIsVisibleDownstream(unittest.TestCase):

    def test_t05_a_failure_record_reaches_the_derived_view(self):
        """The record the corrected producer now writes for a genuine
        `EXECUTION_FAILURE`, put through the production projection. Before R7
        this same invocation produced `status="success"` and the projection
        reported zero failures while a real one had occurred."""
        failures = self_knowledge(trace_reader=_reader_over("failure")).answer(
            "what has failed"
        )

        self.assertEqual(VERIFIED, failures.status)
        self.assertEqual(1, len(failures.value))
        self.assertEqual("tool-proposing-agent", failures.value[0].agent_instance)
        self.assertEqual(("r7.tool",), failures.value[0].tools_used)

    def test_a_success_does_not_appear_as_a_failure(self):
        """The anti-overcorrection control: the projection must not begin
        reporting failures that did not happen."""
        projection = self_knowledge(trace_reader=_reader_over("success"))

        self.assertEqual(0, len(projection.answer("what has failed").value))

    def test_the_defective_record_shape_is_exactly_what_stayed_invisible(self):
        """The R6 defect, reproduced as a fixture and shown to be invisible.
        This is why the producer had to change: no amount of reading fixes a
        record that says `success`, and Trace is append-only, so the record
        cannot be corrected after the fact."""
        defective = self_knowledge(trace_reader=_reader_over("success")).answer(
            "what has failed"
        )

        self.assertEqual(0, len(defective.value), "the failure was unobservable")

    def test_run_count_and_failure_count_stay_independent(self):
        """`what has run` counts actions; `what has failed` selects among them.
        A failed invocation is still an action that ran — collapsing the two
        would trade one misreport for another."""
        projection = self_knowledge(trace_reader=_reader_over("success", "failure"))

        self.assertEqual(2, projection.answer("what has run").value)
        self.assertEqual(1, len(projection.answer("what has failed").value))

    def test_without_a_reader_the_projection_still_declines_to_guess(self):
        """`§11` forbids inventing a self-knowledge feature here. Absent
        evidence must still read `UNKNOWN`, never `no failures`."""
        projection = self_knowledge()

        self.assertEqual(UNKNOWN, projection.answer("what has failed").status)
        self.assertIsNone(projection.answer("what has failed").value)


if __name__ == "__main__":
    unittest.main()
