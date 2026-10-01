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
