"""`ACT-CC-P12-018 §18` — falsification of the decision-preparation surface.

Five `RESOLVED` is also what a module that checked nothing would print, so every
control removes or corrupts the thing the resolution depends on and requires the
status to change. `§18` closes: *"Jangan membuat metric-gaming controls."*

`F-04` is the control this Act's own input made necessary: a document of the
**same filename** as the resident proposal package, carrying a different body,
must supply nothing. `FILENAME ≠ CANONICAL STATUS`.
"""

from __future__ import annotations

import ast
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from tools import p12_e12_criteria as criteria
from tools import p12_e12_source_discovery as discovery

REPO_ROOT = Path(__file__).resolve().parents[2]

SURFACE = (REPO_ROOT / "docs" / "architecture" / "p12" /
           "P12-018-E12-01-05-DECISION-SURFACE.md")


def _world(tmp: Path, *, requirement=True, proposal=True) -> Path:
    if requirement:
        target = tmp / discovery.REQUIREMENT_SOURCE
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / discovery.REQUIREMENT_SOURCE, target)
    if proposal:
        target = tmp / discovery.PROPOSAL_SOURCE
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / discovery.PROPOSAL_SOURCE, target)
    return tmp


class TheLiveDiscoveryResolves(unittest.TestCase):
    def test_all_five_resolve_from_actual_bodies(self):
        found = discovery.summary()
        self.assertEqual(5, found["resolved"])
        self.assertEqual((), found["source_gaps"])
        self.assertEqual((), found["contradictions"])

    def test_each_names_the_founder_authorization_not_the_blueprint(self):
        """A bare `§14` resolves to `State Model` in the Blueprint and to
        `P12-W1 System Integration Authority` in the Founder Authorization.
        `ACT-CC-P12-016` found the same split at `§19`."""
        for found in discovery.discover():
            with self.subTest(found.criterion):
                self.assertIn("P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED",
                              found.originating_artifact)
                self.assertIn("AUTHORITY", found.section)

    def test_the_blueprint_section_of_the_same_number_is_a_different_section(self):
        blueprint = (REPO_ROOT / "docs" / "architecture" / "p12" /
                     "AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md"
                     ).read_text(encoding="utf-8")
        for number, blueprint_heading in ((14, "State Model"),
                                          (15, "State Sources"),
                                          (16, "State Consumers"),
                                          (17, "State Authority"),
                                          (18, "State Lifecycle")):
            with self.subTest(number=number):
                heading, _ = discovery._section_body(blueprint, number)
                self.assertIn(blueprint_heading, heading)


class F01ProposalSourceUnavailable(unittest.TestCase):
    def test_no_proposal_package_yields_source_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), proposal=False)
            found = discovery.discover(root)
        self.assertEqual([discovery.SOURCE_GAP] * 5,
                         [d.status for d in found])
        for d in found:
            self.assertIn("no proposed interpretation", d.detail)

    def test_no_requirement_instrument_yields_source_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), requirement=False)
            found = discovery.discover(root)
        self.assertEqual([discovery.SOURCE_GAP] * 5,
                         [d.status for d in found])


class F02AcceptanceBoundaryUnavailable(unittest.TestCase):
    def test_the_consumption_reader_still_reports_unavailable(self):
        """Preparation does not create a boundary. `FD-P12-003` remains
        unfilled, and discovery resolving five proposals changes nothing."""
        with self.assertRaises(criteria.AcceptanceBoundaryUnavailable):
            criteria.boundaries()
        self.assertFalse(criteria.summary()["measurable"])

    def test_a_package_without_boundary_rows_yields_no_boundary_elements(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp))
            path = root / discovery.PROPOSAL_SOURCE
            stripped = re.sub(r"^\|\s*(Evidence source|Verification method|"
                              r"Negative control|Failure semantics)\s*\|.*$",
                              "", path.read_text(encoding="utf-8"), flags=re.M)
            path.write_text(stripped, encoding="utf-8")
            found = discovery.discover(root)
        self.assertTrue(all(d.existing_boundary == "" for d in found))


class F03WrongInterpretationIdentifier(unittest.TestCase):
    def test_a_selection_naming_something_else_is_rejected(self):
        """Delegated to the consumption reader, which owns the check. Repeated
        here so `F-03` is exercised by this Act and not merely cited."""
        section = ("\n{n}. FOUNDER DECISION — {c}\n\nFounder selects:\n\n"
                   "{c}\n→ an interpretation nobody ever proposed\n\n"
                   "Acceptance Boundary:\n\nsomething\n")
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp))
            (root / criteria.DECISION_ROOT).mkdir(parents=True, exist_ok=True)
            body = "FD\n\nDecision Domain: E12-01 THROUGH E12-05\n" + "".join(
                section.format(n=i, c=c)
                for i, c in enumerate(criteria.CRITERIA, start=4))
            (root / criteria.DECISION_ROOT / "FD.md").write_text(
                body, encoding="utf-8")
            found = criteria.decisions(root)
        self.assertEqual([criteria.REJECTED] * 5, [d.status for d in found])


class F04NonAuthoritativeSourceSubstituted(unittest.TestCase):
    """The control this Act's own input artifact made necessary."""

    def test_a_same_named_package_elsewhere_supplies_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), proposal=False)
            # A document with the identical filename, in another directory.
            elsewhere = root / "uploads"
            elsewhere.mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO_ROOT / discovery.PROPOSAL_SOURCE,
                        elsewhere / discovery.PROPOSAL_SOURCE.name)
            found = discovery.discover(root)
        self.assertEqual([discovery.SOURCE_GAP] * 5,
                         [d.status for d in found])

    def test_a_blank_template_of_the_same_name_resolves_nothing(self):
        """The uploaded artifact is a template: its criterion sections read
        `TO BE POPULATED FROM ACTUAL CANONICAL SOURCE`. Placed at the resident
        path it must yield `SOURCE-GAP`, not silently blank proposals."""
        template = ("E12-RATIFICATION-DECISION-PACKAGE\n\n"
                    "6. E12-01 — DECISION SURFACE\n\n"
                    "TO BE POPULATED FROM ACTUAL CANONICAL SOURCE\n")
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), proposal=False)
            target = root / discovery.PROPOSAL_SOURCE
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(template, encoding="utf-8")
            found = discovery.discover(root)
        self.assertEqual([discovery.SOURCE_GAP] * 5,
                         [d.status for d in found])


class F05MissingProvenance(unittest.TestCase):
    """A citation that resolves is not a citation that supports the claim."""

    def test_a_quotation_absent_from_the_cited_section_is_a_contradiction(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp))
            path = root / discovery.PROPOSAL_SOURCE
            text = path.read_text(encoding="utf-8")
            # Attribute a sentence to §14 that §14 does not contain.
            text = text.replace(
                '*"Phase dan Platform Organization harus tetap dibedakan"*',
                '*"this sentence appears nowhere in the cited instrument"*')
            path.write_text(text, encoding="utf-8")
            found = {d.criterion: d for d in discovery.discover(root)}
        self.assertEqual(discovery.CONTRADICTION, found["E12-01"].status)
        self.assertIn("do not appear in its body", found["E12-01"].detail)
        # The other four are unaffected: the check is per-criterion.
        for criterion in ("E12-02", "E12-03", "E12-04", "E12-05"):
            with self.subTest(criterion):
                self.assertEqual(discovery.RESOLVED, found[criterion].status)

    def test_a_cited_section_that_is_a_different_section_is_a_contradiction(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp))
            path = root / discovery.REQUIREMENT_SOURCE
            text = path.read_text(encoding="utf-8")
            text = text.replace("14. P12-W1 — SYSTEM INTEGRATION AUTHORITY",
                                "14. SOMETHING ENTIRELY DIFFERENT")
            path.write_text(text, encoding="utf-8")
            found = {d.criterion: d for d in discovery.discover(root)}
        self.assertEqual(discovery.CONTRADICTION, found["E12-01"].status)
        self.assertIn("resolves differently across instruments",
                      found["E12-01"].detail)


class F06BlankDecisionIsNotConsent(unittest.TestCase):
    """`§15` — every implicit-consent inference is refused."""

    def test_no_proposal_is_reported_ratified(self):
        found = discovery.summary()
        self.assertEqual((), found["ratified"])
        self.assertTrue(found["all_existing_proposals_unratified"])
        for d in discovery.discover():
            with self.subTest(d.criterion):
                self.assertEqual("EXISTING PROPOSAL — NOT RATIFIED",
                                 d.current_status)

    def test_the_sole_candidate_is_still_not_a_selection(self):
        proposals = criteria.proposed_interpretations()
        for criterion in criteria.CRITERIA:
            with self.subTest(criterion):
                self.assertTrue(proposals[criterion]["proposed"].strip())
        self.assertEqual(0, criteria.summary()["resolved"])

    def test_the_prepared_decision_surface_has_no_ticked_box(self):
        self.assertTrue(SURFACE.is_file(), "the decision surface is not persisted")
        body = SURFACE.read_text(encoding="utf-8")
        for ticked in ("[x]", "[X]", "[✓]", "[*]"):
            with self.subTest(ticked):
                self.assertNotIn(ticked, body)
        # Four options for each of five criteria, every one empty.
        self.assertEqual(20, len(re.findall(r"^\s*\[ \]", body, re.M)))

    def test_the_surface_declares_itself_not_a_decision(self):
        body = SURFACE.read_text(encoding="utf-8")
        self.assertIn("PREPARATION ≠ RATIFICATION", body)
        self.assertIn("ONE CANDIDATE ≠ A SELECTION", body)


class TheModuleSelectsNothing(unittest.TestCase):
    SOURCE = REPO_ROOT / "tools" / "p12_e12_source_discovery.py"

    def test_no_function_selects_ranks_or_ratifies(self):
        tree = ast.parse(self.SOURCE.read_text(encoding="utf-8"))
        creating = [n.name for n in ast.walk(tree)
                    if isinstance(n, ast.FunctionDef)
                    and n.name.lower().lstrip("_").startswith(
                        ("select", "choose", "pick", "rank", "ratify",
                         "recommend", "merge", "combine", "adopt", "prefer"))]
        self.assertEqual([], creating)

    def test_the_module_writes_nothing(self):
        source = self.SOURCE.read_text(encoding="utf-8")
        for forbidden in ("write_text(", "mkdir(", "unlink("):
            with self.subTest(forbidden):
                self.assertNotIn(forbidden, source)

    def test_it_carries_no_proposal_text_of_its_own(self):
        """Delete the package and the module must have nothing to offer."""
        body = self.SOURCE.read_text(encoding="utf-8").split('"""', 2)[-1]
        for criterion, proposal in criteria.proposed_interpretations().items():
            for phrase in [p for p in proposal["proposed"].split()
                           if len(p) > 11][:4]:
                with self.subTest(criterion=criterion, phrase=phrase):
                    self.assertNotIn(phrase.strip("`*.,"), body)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
