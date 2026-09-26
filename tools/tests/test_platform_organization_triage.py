"""`ACT-CC-POST-P13-PLATFORM-ORG-002`: the seven-point decision triage.

The triage record is evidence. These tests hold it to the Act's decision
readiness contract (`§16`), to its sources, and to the gate it triages: every
item carries all twelve fields, cites only resident sources, decides nothing,
and accounts for every open item the gate reports.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from tools import platform_organization_gate as po

REPO_ROOT = Path(__file__).resolve().parents[2]
TRIAGE = REPO_ROOT / "docs/governance/platform-organization/PO-DECISION-TRIAGE-v1.0.json"


class TheTriage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
        cls.items = {i["id"]: i for i in cls.triage["items"]}

    def test_seven_items_in_order(self):
        self.assertEqual([f"DP-{n:02d}" for n in range(1, 8)], [i["id"] for i in self.triage["items"]])

    def test_every_item_meets_the_readiness_contract(self):
        for item in self.triage["items"]:
            for field in self.triage["readiness_fields"]:
                with self.subTest(item=item["id"], field=field):
                    self.assertIn(field, item)
                    self.assertTrue(item[field])

    def test_nothing_is_decided(self):
        """NC-01, NC-02, NC-09, NC-10: packages prepared; no outcome chosen."""
        for item in self.triage["items"]:
            self.assertIsNone(item["decision_taken"], item["id"])
        self.assertIn("Decides nothing", self.triage["status"])

    def test_claude_holds_no_decision_right(self):
        for item in self.triage["items"]:
            claude = item["authority_owner"]["claude"].lower()
            for word in ("decide", "approve", "bind", "activate", "select"):
                self.assertNotIn(word, claude, item["id"])

    def test_every_cited_source_is_resident(self):
        paths = set()
        for item in self.triage["items"]:
            for entry in item["evidence"]:
                paths.add(entry.split(" ")[0])
        paths.update(self.triage["cross_cutting"]["sources"])
        missing = sorted(p for p in paths if not (REPO_ROOT / p).exists())
        self.assertEqual([], missing)

    def test_every_open_gate_item_is_triaged_or_classed_as_non_decision(self):
        triaged = {g for i in self.triage["items"] for g in i["gate_items"]}
        non_decision = " ".join(n["statement"] for n in self.triage["non_decisions"])
        # Items first recorded after the triage (the P7-I99 result, Register
        # `§50`) are traced to that later record instead.
        later = {po.P7_I99_RESULT}
        for item in po.open_items():
            if item["status"] == "OPEN":
                self.assertTrue(item["id"] in triaged or item["id"] in non_decision
                                or item["source"] in later, item["id"])

    def test_triage_agrees_with_the_gate_on_blocking(self):
        blocking = {i["id"]: i["blocking"] for i in po.open_items()}
        self.assertFalse(blocking["G-02"])
        for identifier in self.items["DP-04"]["gate_items"]:
            self.assertFalse(blocking[identifier], identifier)
        self.assertTrue(blocking["ESC-C7-01"])
        self.assertTrue(blocking["G-01"])

    def test_dp03_was_answered_by_a_per_volume_invocation(self):
        """DP-03 rests on the delegation. It stays dormant except where invoked:
        `FD-PO-003-01` invoked it for Volume 1 only, so the triage is historical
        for DP-03 and current for nothing else it records."""
        text = (REPO_ROOT / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md").read_text(encoding="utf-8")
        self.assertIn("### DEL-F03-015-P7I99-001 — Bounded P7-I99 Execution Delegation", text)
        self.assertIn("**ACTIVE — DORMANT UNTIL INVOKED**", text)
        register = (REPO_ROOT / po.REGISTER).read_text(encoding="utf-8")
        self.assertIn("### FD-PO-003-01 — Founder Decision", register)
        self.assertIn("*\"Invoke for Volume 1\"*", register)

    def test_the_dependency_graph_refers_only_to_known_nodes(self):
        known = set(self.items) | {"FD-2"}
        for edge in self.triage["dependencies"]:
            for end in (edge["from"], *[e.strip() for e in edge["to"].split(",")]):
                self.assertIn(end, known)

    def test_no_withdrawn_track_label_is_used(self):
        """NC-08."""
        self.assertIsNone(re.search(r"Track B", TRIAGE.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
