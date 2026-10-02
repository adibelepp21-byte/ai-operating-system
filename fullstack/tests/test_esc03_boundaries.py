"""ESC-03 negative controls (Act ACT-CC-POST-P13-AIOS-FS10-ESC03 §22), at the code level.

Whatever path later carries `aios-operator` through X2, the application itself
must offer that principal nothing beyond operation: no release, no LIVE, no
governance or certified-root change, no unlisted scope. The live counterparts
(Preview/Production credential separation, the 403 on registration) are in
`docs/fullstack/evidence/FS-10-FDP-010-OPERATIONAL-ACCESS-ROLLBACK-2026-10-01.json`.
"""

import json
import re
import unittest
from pathlib import Path

from fullstack.backend import contract, docs_tool, security

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT = json.loads((REPO_ROOT / "docs/fullstack/FS-10-CURRENT-AUTHORITY.json")
                     .read_text(encoding="utf-8"))
OPERATOR = frozenset(CURRENT["operational_principal"]["scopes"])
RELEASE_WORDS = re.compile(r"(?i)release|live|promot|activat|deploy|rollback|govern|founder")


def _reachable(scopes):
    return [r for r in contract.ROUTES
            if r.scope in scopes or r.scope in (security.PUBLIC, security.AUTHENTICATED)]


class TheOperatorReachesOperationOnly(unittest.TestCase):

    def test_nc01_nc02_no_route_releases_activates_or_deploys(self):
        for route in contract.ROUTES:
            self.assertNotRegex(route.template, RELEASE_WORDS, route)
            self.assertNotRegex(route.handler, RELEASE_WORDS, route)

    def test_nc06_no_scope_outside_the_canonical_model(self):
        self.assertTrue(OPERATOR <= set(security.SCOPES))
        for route in contract.ROUTES:
            self.assertIn(route.scope, (*security.SCOPES, security.PUBLIC, security.AUTHENTICATED))

    def test_nc09_registration_needs_a_scope_the_operator_lacks(self):
        register = [r for r in contract.ROUTES if r.handler == "register_agent"]
        self.assertEqual(1, len(register))
        self.assertEqual(security.AGENT_REGISTER, register[0].scope)
        self.assertNotIn(register[0], _reachable(OPERATOR))

    def test_nc04_nc05_the_operator_has_one_write_and_it_runs_a_workflow(self):
        writes = [r for r in _reachable(OPERATOR) if r.method != "GET"]
        self.assertEqual([("POST", "start_run")], [(r.method, r.handler) for r in writes])

    def test_nc04_nc05_the_only_tool_is_read_only(self):
        self.assertEqual("docs.read", docs_tool.KEY)
        source = (REPO_ROOT / "fullstack/backend/docs_tool.py").read_text(encoding="utf-8")
        self.assertNotRegex(source, r"\.(write_text|write_bytes|unlink|mkdir|rename)\(|open\([^)]*['\"][wa]")


class NoBypassLivesInTheApplication(unittest.TestCase):

    def test_nc03_no_served_or_operational_module_carries_a_bypass(self):
        carriers = []
        for root in ("api", "fullstack/backend", "fullstack/frontend", "fullstack/deploy"):
            for path in (REPO_ROOT / root).rglob("*"):
                if not path.is_file() or path.suffix not in (".py", ".js", ".html", ".json"):
                    continue
                rel = path.relative_to(REPO_ROOT).as_posix()
                text = path.read_text(encoding="utf-8", errors="replace")
                if re.search(r"(?i)x-vercel-protection-bypass|VERCEL_AUTOMATION_BYPASS|_vercel_share|"
                             r"x-vercel-trusted-oidc", text):
                    carriers.append(rel)
        # The smoke tool is the one client that may send a temporary bypass, read
        # from a file at run time for FDP-009-03 verification; it holds none.
        self.assertEqual(["fullstack/deploy/smoke.py"], carriers)

    def test_nc03_vercel_json_configures_no_protection_change(self):
        config = json.loads((REPO_ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertFalse({"public", "ssoProtection", "protectionBypass", "trustedIps"} & set(config))


class TheCredentialSeparationIsDeclared(unittest.TestCase):

    def test_nc07_nc08_the_operator_is_production_only(self):
        principal = CURRENT["operational_principal"]
        self.assertTrue(principal["environment"].startswith("production only"))
        self.assertEqual("aios-operator", principal["subject"])

    def test_nc10_release_and_live_stay_with_the_founder(self):
        for key in ("production_release", "live", "final_system_acceptance"):
            self.assertEqual("FOUNDER-RESERVED", CURRENT["authority"][key]["class"])


if __name__ == "__main__":
    unittest.main()


class TheEdgeAccessDecisionStaysUnselected(unittest.TestCase):
    """AD-FS10-ESC03 §5, §19, §20: no selection before the decision authority acts; no ranking."""

    ADR = REPO_ROOT / "docs/fullstack/FS-10-ESC03-ARCHITECTURE-DECISION.md"
    PACKAGE = REPO_ROOT / "docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE.md"

    def test_every_candidate_is_unselected(self):
        text = self.ADR.read_text(encoding="utf-8")
        matrix = text[text.index("## 8. Decision matrix"):text.index("## 9.")]
        rows = [line for line in matrix.splitlines() if line.startswith("| E-")]
        self.assertEqual(6, len(rows))
        for row in rows:
            self.assertTrue(row.rstrip().endswith("**UNSELECTED** |"), row)

    def test_no_ranking_or_recommendation_language(self):
        for path in (self.ADR, self.PACKAGE):
            text = path.read_text(encoding="utf-8").lower()
            for word in ("recommend", "preferred", "best option", "winner", "most suitable",
                         "least risky", "ranked first"):
                body = text.replace("not ranked", "").replace("nothing is selected, recommended, ranked",
                                                              "")
                self.assertNotIn(word, body, f"{path.name}: {word}")

    def test_release_and_live_are_untouched_by_every_candidate(self):
        text = self.ADR.read_text(encoding="utf-8")
        governance = text[text.index("## 7. Governance evaluation"):text.index("## 8.")]
        rows = [line for line in governance.splitlines() if line.startswith("| E-")]
        self.assertEqual(6, len(rows))
        for row in rows:
            self.assertTrue(row.rstrip().endswith("**NO** |"), row)


class TheCompleteFounderPackageStaysUnselected(unittest.TestCase):
    """Master Instruction §9, §10: all 23 elements, in order; no candidate selected; no steering word."""

    PACKAGE = REPO_ROOT / "docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md"
    RECORD = REPO_ROOT / "docs/fullstack/FS-10-ESC03-MI-S0-S1-RECORD.md"
    ELEMENTS = ("Decision ID", "Context", "Existing canonical authority", "Current verified state",
                "Evidence inventory", "Directly verified facts", "Provider-documented facts",
                "Implementation-observed facts", "Unknowns", "Authority classification",
                "Candidate mechanisms", "Security implications", "Governance implications",
                "Operational implications", "Release / LIVE boundary implications",
                "Exact Founder Decision Question", "Decision options", "Consequences of each option",
                "Required implementation scope after decision", "Explicit non-decisions",
                "Negative controls", "Evidence references", "Canonicalization requirements")

    def test_the_23_elements_appear_in_order(self):
        headings = re.findall(r"^## (\d+)\. (.+?)(?: \(|$)", self.PACKAGE.read_text(encoding="utf-8"), re.M)
        self.assertEqual([(str(i), e) for i, e in enumerate(self.ELEMENTS, 1)],
                         [(n, h.strip()) for n, h in headings])

    def test_no_steering_word(self):
        text = self.PACKAGE.read_text(encoding="utf-8")
        self.assertNotRegex(text, r"(?i)\b(recommend\w*|preferred|best|optimal|obvious|natural choice)\b")

    def test_every_candidate_is_unselected_and_the_package_is_not_a_decision(self):
        text = self.PACKAGE.read_text(encoding="utf-8")
        self.assertIn("All six: **UNSELECTED**.", text)
        self.assertIn("**not** a Founder Decision Record", text)
        self.assertNotRegex(text, r"(?i)\bselected\b(?! by)")

    def test_s1_exit_is_founder_decision_required_with_capability_answer_b(self):
        text = self.RECORD.read_text(encoding="utf-8")
        self.assertIn("**S1-B — FOUNDER DECISION REQUIRED**", text)
        self.assertIn("**B** — mechanism selection/authorization for an already-authorized capability", text)
        self.assertIn("FOUNDER DECISION REQUIRED\nEXECUTION PAUSED\nNO IMPLEMENTATION AUTHORIZED", text)


class Fdp011IsCanonicalAndItsBoundaryHolds(unittest.TestCase):
    """FDP-011 (Register §117): the record, its hash, the unchanged package, and the D-3 scopes."""

    RECORD = REPO_ROOT / "docs/governance/acts/FDP-011-FS-10-ESC03-PER-SESSION-X2-OPERATIONAL-ACCESS.md"
    PACKAGE = REPO_ROOT / "docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md"
    PACKAGE_SHA256 = "5cef394cbd421331155ea531ae304acbacbfa553544e6f31cf704f70f77707e1"

    def test_the_record_hash_is_registered_and_current(self):
        import hashlib
        text = self.RECORD.read_text(encoding="utf-8")
        digest = hashlib.sha256(
            text[text.index("````text\n") + 8:text.rindex("\n````")].encode("utf-8")).hexdigest()
        entry = CURRENT["decisions"]["FDP-011"]
        self.assertEqual("§117", entry["register"])
        self.assertEqual(digest, entry["sha256"])
        register = (REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md").read_text(encoding="utf-8")
        self.assertIn(digest, register)

    def test_the_decision_package_is_preserved_unchanged(self):
        import hashlib
        self.assertEqual(self.PACKAGE_SHA256, hashlib.sha256(self.PACKAGE.read_bytes()).hexdigest())

    def test_the_founder_principal_has_the_three_scopes_and_is_not_the_operator(self):
        founder = CURRENT["founder_principal"]
        self.assertEqual({"aios.observe", "aios.workflow.run", "aios.audit"}, set(founder["scopes"]))
        self.assertTrue(set(founder["scopes"]) <= set(security.SCOPES))
        self.assertNotIn(security.AGENT_REGISTER, founder["scopes"])
        self.assertNotEqual("aios-operator", founder.get("subject"))

    def test_no_bypass_is_declared_to_exist(self):
        self.assertIn("No bypass exists.", CURRENT["operational_principal"]["edge_access"])


class TheT5FeasibilityRecordClassifiesWithoutSelecting(unittest.TestCase):
    """T5 feasibility instruction §4, §7: one class per mechanism, none selected, final state C."""

    RECORD = REPO_ROOT / "docs/fullstack/FS-10-FDP011-T5-SECRET-CUSTODY-FEASIBILITY.md"
    CLASSES = ("EXISTING AUTHORIZED", "AUTHORIZED WITH BOUNDARY", "REQUIRES FOUNDER DECISION",
               "REQUIRES ARCHITECT DECISION", "PROVIDER DEPENDENCY", "INSUFFICIENT EVIDENCE",
               "INCOMPATIBLE WITH FDP-011 T5", "PROHIBITED")

    def test_each_mechanism_has_exactly_one_class(self):
        text = self.RECORD.read_text(encoding="utf-8")
        table = text[text.index("## 12. Classification"):text.index("## 13.")]
        rows = [line for line in table.splitlines() if re.match(r"\| M\d+ ", line)]
        self.assertEqual(11, len(rows))
        for row in rows:
            cell = row.split("|")[3]
            found = [c for c in self.CLASSES if f"**{c}" in cell]
            self.assertEqual(1, len(found), row)

    def test_final_state_and_no_selection_language(self):
        text = self.RECORD.read_text(encoding="utf-8")
        self.assertIn("C. NO EXISTING AUTHORIZED SECRET-HANDLING PATH", text)
        self.assertNotRegex(text, r"(?i)\b(recommend\w*|preferred|best|optimal|obvious|natural choice)\b")


class TheM1CustodyGateIsNotPassedByInference(unittest.TestCase):
    """FDP-012 custody MI §6, §24, §32: sixteen gates, UNKNOWN is not PASS, no FDP-012 manufactured."""

    RECORD = REPO_ROOT / "docs/fullstack/FS-10-FDP012-M1-CUSTODY-VALIDATION.md"

    def _gates(self):
        text = self.RECORD.read_text(encoding="utf-8")
        table = text[text.index("## 5. G1–G16 results"):text.index("## 6.")]
        return {m.group(1): m.group(2) for m in
                re.finditer(r"^\| \*\*G(\d+)\*\*[^|]*\| \*\*(PASS|FAIL|UNKNOWN)", table, re.M)}

    def test_all_sixteen_gates_have_a_result(self):
        self.assertEqual({str(n) for n in range(1, 17)}, set(self._gates()))

    def test_a_non_pass_gate_blocks_and_the_state_says_so(self):
        gates = self._gates()
        self.assertTrue(any(v != "PASS" for v in gates.values()))
        text = self.RECORD.read_text(encoding="utf-8")
        self.assertIn("STATE B — BLOCKED — TELEMETRY / LOGGING / SESSION ISOLATION", text)
        self.assertNotIn("STATE A — ", text.replace("MI `§31` STATE A", ""))

    def test_telemetry_unknown_is_not_converted_to_pass(self):
        self.assertEqual("UNKNOWN", self._gates()["4"])

    def test_no_fdp012_record_was_manufactured(self):
        # Until the Founder issued it (Register §124), no FDP-012 existed; the only
        # admissible FDP-012 record is that Founder-issued one, with its registered hash.
        import hashlib
        acts = REPO_ROOT / "docs/governance/acts"
        self.assertEqual(["FDP-012-FS-10-FINAL-ARCHITECTURE-AUTHORITY-ESC03-RESOLUTION-FDP010-COMPLETION.md"], sorted(p.name for p in acts.glob("FDP-012*")))
        text = (acts / "FDP-012-FS-10-FINAL-ARCHITECTURE-AUTHORITY-ESC03-RESOLUTION-FDP010-COMPLETION.md").read_text(encoding="utf-8")
        digest = hashlib.sha256(text[text.index("````text\n") + 8:text.rindex("\n````")].encode()).hexdigest()
        self.assertEqual("5ad7f321c463c7dbaf10998946a9933a2e165a82f6f5f582f8ff2c88ad64891f", digest)
        register = (REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md").read_text(encoding="utf-8")
        self.assertIn(digest, register[register.index("## 124. "):])


class TheProviderInjectionRecordSelectsNothing(unittest.TestCase):
    """Provider-injection MI §2, §17, §18: twenty matrix rows, one final class, mechanism unselected."""

    RECORD = REPO_ROOT / "docs/fullstack/FS-10-PROVIDER-CREDENTIAL-INJECTION-EVIDENCE.md"

    def test_the_decision_matrix_has_the_twenty_properties(self):
        text = self.RECORD.read_text(encoding="utf-8")
        table = text[text.index("## 18. Decision matrix"):text.index("## 19.")]
        rows = [line for line in table.splitlines()
                if line.startswith("| ") and not line.startswith(("| Property", "|---"))]
        self.assertEqual(20, len(rows))

    def test_one_final_classification_and_isolation_is_not_claimed(self):
        text = self.RECORD.read_text(encoding="utf-8")
        self.assertIn("**D. FOUNDER DECISION REQUIRED.**", text)
        self.assertIn("| **Selection** | **UNSELECTED.**", text)
        matrix = text[text.index("## 18. Decision matrix"):text.index("## 19.")]
        for prop in ("Session isolation", "Cross-session isolation", "Routine isolation"):
            row = next(line for line in matrix.splitlines() if line.startswith(f"| {prop} "))
            self.assertIn("**FAIL**", row)
        self.assertNotRegex(text, r"(?i)\b(recommend\w*|preferred|best|optimal|safest|obvious)\b")


class TheInjectionDecisionPackageDecidesNothing(unittest.TestCase):
    """Preparation gate §11: four questions, facts kept, UNKNOWN kept, Q-4 procedural ≠ technical,
    no ranking, nothing selected, no implementation authorized, Release/LIVE Founder-reserved."""

    PACKAGE = REPO_ROOT / "docs/fullstack/decision-packages/FS-10-PROVIDER-CREDENTIAL-INJECTION-FOUNDER-DECISION-PACKAGE.md"

    def setUp(self):
        self.text = self.PACKAGE.read_text(encoding="utf-8")

    def test_1_the_four_questions_exist_in_order(self):
        heads = re.findall(r"^## (Q-\d) — ", self.text, re.M)
        self.assertEqual(["Q-1", "Q-2", "Q-3", "Q-4"], heads)

    def test_2_the_known_provider_facts_are_represented(self):
        for fact in ("never reaches Claude, the commands it runs, or the session's environment variables",
                     "whoever started it, until you delete it",
                     "You can't view the value again after saving",
                     "available on Pro and Max plans",
                     "doesn't go through the agent proxy",
                     "x-vercel-protection-bypass"):
            self.assertIn(fact, self.text, fact)

    def test_3_unknowns_are_not_converted_to_pass(self):
        q2 = self.text[self.text.index("## Q-2"):self.text.index("## Q-3")]
        for element in ("logging exclusion", "telemetry exclusion", "deletion", "custody", "auditability"):
            row = next(line for line in q2.splitlines() if line.startswith(f"| {element} "))
            self.assertIn("**UNKNOWN**", row, element)
        self.assertIn("**FAIL**", next(line for line in q2.splitlines() if line.startswith("| delivery ")))
        self.assertIn("PLAN ENTITLEMENT = UNKNOWN", self.text)

    def test_4_procedural_use_is_distinguished_from_technical_isolation(self):
        self.assertIn("Procedural per-session use is not technical session isolation.", self.text)
        q4 = self.text[self.text.index("## Q-4"):]
        for label in ("Interpretation A", "Interpretation B", "Interpretation C"):
            self.assertIn(label, q4)

    def test_5_no_ranking_language(self):
        self.assertNotRegex(self.text, r"(?i)\b(recommend\w*|preferred|best|optimal|safest|obvious|natural choice)\b")

    def test_6_no_mechanism_is_selected(self):
        self.assertIn("is **UNSELECTED**", self.text)
        self.assertNotRegex(self.text, r"(?i)(?<!un)(?<!not )\bselected\b")

    def test_7_no_implementation_is_authorized(self):
        self.assertIn("| **Implementation** | **NOT AUTHORIZED.**", self.text)
        self.assertNotIn("IMPLEMENTATION AUTHORIZED", self.text.replace("NOT AUTHORIZED", ""))

    def test_8_release_and_live_stay_founder_reserved(self):
        self.assertIn("**PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED**", self.text)


class Fdp012IsCanonicalAndO_AIsNotClaimedImplemented(unittest.TestCase):
    """FDP-012 (Register §124, §125): bounded authority recorded; O-A selected but not implemented."""

    ADR = REPO_ROOT / "docs/fullstack/AD-FS10-ESC03-R1-OPERATIONAL-EDGE-ACCESS-SELECTION.md"

    def test_fdp012_is_registered_with_its_hash_and_is_bounded(self):
        import hashlib
        entry = CURRENT["decisions"]["FDP-012"]
        text = (REPO_ROOT / entry["record"]).read_text(encoding="utf-8")
        digest = hashlib.sha256(text[text.index("````text\n") + 8:text.rindex("\n````")].encode()).hexdigest()
        self.assertEqual(("§124", digest), (entry["register"], entry["sha256"]))
        authority = CURRENT["architecture_authority_fs10_esc03"]
        self.assertIn("bounded, not global", authority["scope"])
        self.assertIn("NOT RATIFIED", authority["fd2"])
        self.assertEqual({"Production Release", "LIVE", "Final System Acceptance"}, set(authority["founder_reserved"]))

    def test_o_a_is_selected_but_not_implemented_and_nothing_is_injected(self):
        edge = CURRENT["operational_principal"]["edge_access"]
        self.assertIn("Implementation authorized, NOT YET OCCURRED", edge)
        self.assertIn("ESC-03 NOT RESOLVED", edge)
        self.assertIn("the CEO has never seen its value", edge)
        self.assertIn("No environment credential is attached: no injection", edge)
        self.assertNotRegex(edge, r"(?i)ESC-03 (= )?RESOLVED|(?<!NOT yet )operationally accessible")

    def test_the_selection_is_made_under_fdp012_and_excludes_tool_output_delivery(self):
        text = self.ADR.read_text(encoding="utf-8")
        self.assertIn("under `FDP-012`", text)
        self.assertIn("Connector-created bypass (tool output)", text)
        self.assertIn("PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED**", text)
