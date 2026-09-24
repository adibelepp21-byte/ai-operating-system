"""`GOAL-V2-005 §14` — the ecosystem relationship map, and its controls.

The map is a measurement. These tests hold the measured state, so a change to
any relationship is noticed, and they show that each kind of evidence can come
back negative.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools import ecosystem_relationships as eco

REPO_ROOT = Path(__file__).resolve().parents[2]


class TheMeasuredChain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.result = {(r.left, r.right): r for r in eco.measure()}

    def test_the_chain_is_the_goals_eight_nodes_seven_relationships(self):
        self.assertEqual(len(eco.CHAIN), 8)
        self.assertEqual(len(self.result), 7)

    def test_the_measured_state(self):
        """If this changes, a relationship was built or broken. Update it with
        the evidence, never to make the suite pass."""
        self.assertEqual({k: r.status for k, r in self.result.items()}, {
            ("Knowledge", "Memory"): eco.CONNECTED_CODE,
            ("Memory", "Intelligence"): eco.NOT_CONNECTED,
            ("Intelligence", "Capability"): eco.CONNECTED_DATA,
            ("Capability", "Workflow"): eco.MEDIATED,
            ("Workflow", "Organization"): eco.CONNECTED_CODE,
            ("Organization", "Governance"): eco.CONNECTED_CODE,
            ("Governance", "FounderDecision"): eco.CONNECTED_DATA,
        })

    def test_every_absence_carries_its_recorded_reason_and_none_is_stale(self):
        for key in (("Memory", "Intelligence"), ("Capability", "Workflow")):
            with self.subTest(key):
                self.assertTrue(self.result[key].recorded_reason)
                self.assertEqual(self.result[key].stale_reason, [])

    def test_the_founder_decision_link_is_every_escalation_resolving(self):
        data = self.result[("Governance", "FounderDecision")].data
        self.assertTrue(any(d.startswith("4/4 escalation records") for d in data),
                        data)


class EachKindOfEvidenceCanComeBackNegative(unittest.TestCase):

    def test_a_reason_no_longer_in_its_file_is_reported_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "consumers/cognitive_intelligence_agent.py"
            target.parent.mkdir(parents=True)
            target.write_text('"""now it reads Memory"""\n', encoding="utf-8")
            held, stale = eco.recorded_reasons(root, "Memory", "Intelligence")
        self.assertTrue(any("cognitive" in s for s in stale))

    def test_an_escalation_citing_the_wrong_file_does_not_bind(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ops = root / "docs/operations/x"
            ops.mkdir(parents=True)
            (ops / "e.escalation.json").write_text(json.dumps({
                "authority_instrument": "FD-P11-001 §9",
                "authority_record": "README.md"}), encoding="utf-8")
            (root / "docs/architecture").mkdir(parents=True)
            data = eco.data_bindings(root, "Governance", "FounderDecision")
        self.assertEqual(data, [])

    def test_a_graph_without_the_import_has_no_code_binding(self):
        graph = {"native_core.core.knowledge.admission": {"json"},
                 "native_core.core.memory.store": {"os"}}
        self.assertEqual(eco.code_bindings(graph, "Knowledge", "Memory"), [])
        graph["native_core.core.knowledge.admission"].add("native_core.core.memory")
        self.assertTrue(eco.code_bindings(graph, "Knowledge", "Memory"))


if __name__ == "__main__":
    unittest.main()
