"""`ACT-CC-P12-007` — the phase authorization surface, and what must falsify it.

`§15` names six falsification cases and `§16` a seventh; each has a class here.
The point of all seven is one property: **a claim that P13 is authorized must
meet a resident contradiction only when the resident representation is actually
correct and actually provenanced.** A control that cannot be driven to
`ACCEPTED` is a constant, so `TheStrengthenedControlCanStillReportAccepted`
drives it there six ways.

Fixtures build whole instruments rather than patching parsed output, because
the thing under test is the reading of a Founder body. Where a fixture's
citation must resolve, `tools.planning.goal.REPO_ROOT` is pointed at the
temporary world for the duration of the test — the convention
`tools/tests/test_p12_w3_resident_wiring.py` states and
`tools/p12_negative_control_verification.py` follows. A citation that resolves
to nothing is self-authorization, and that rule is not suspended here; the
temporary world is simply where these instruments live.
"""

from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_phase_authorization as phases
from tools import p12_phase_authorization_verifier as verifier
from tools import p12_self_model as model
from tools import p12_system_negative_controls as controls
from tools.planning import goal

REPO_ROOT = Path(__file__).resolve().parents[2]

ISSUED_TAIL = """
35. FINAL FOUNDER DECISION

Decision Authority: AIOS Founder

Status: ISSUED

37. FINAL STATE TRANSITION

{block}

This is the intended state transition.

38. NON-NEGOTIABLE INVARIANTS

P12
≠
P13
"""


def _instrument(root: Path, block: str, *, preamble: str = "",
                name: str = "decision.md") -> Path:
    acts = root / "docs" / "governance" / "acts"
    acts.mkdir(parents=True, exist_ok=True)
    path = acts / name
    path.write_text(preamble + ISSUED_TAIL.format(block=block),
                    encoding="utf-8")
    return path


class _TemporaryWorld(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        patcher = mock.patch.object(goal, "REPO_ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)


class Case1CorrectAuthoritativeState(_TemporaryWorld):
    """`§15` case 1 — the Founder source says not authorized."""

    def test_the_reader_reports_exactly_what_the_block_states(self):
        _instrument(self.root, "P12\nAUTHORIZED = TRUE\nP13\nAUTHORIZED = FALSE")
        state = phases.state_of("P13", self.root)
        self.assertIs(False, state.authorized)
        self.assertEqual({"AUTHORIZED": False}, dict(state.dimensions))


class Case1OnTheLiveCorpus(unittest.TestCase):
    """`§15` case 1 against the real instrument — no fixture, no temporary
    world. `§13`: static inspection of a fixture is not the resident path."""

    def test_the_live_corpus_states_p13_unauthorized(self):
        state = phases.state_of("P13")
        self.assertIs(False, state.authorized)
        self.assertIn("FINAL STATE TRANSITION", state.stated_in)

    def test_the_self_model_reports_the_same_state_the_reader_read(self):
        reported = model.authority().value["phase_authorization"]
        self.assertTrue(reported["resolved"])
        self.assertIs(False, reported["states"]["P13"]["authorized"])

    def test_an_unstated_dimension_is_not_reported_as_false(self):
        """`§4`/`§9` — the Founder states one dimension for P13 and seven for
        P12. Normalizing the six absent ones to `False` would be inference
        dressed as measurement, however likely the inference."""
        state = phases.state_of("P13")
        self.assertNotIn("CONSTRUCTED", state.dimensions)
        self.assertIn("CONSTRUCTED", state.unstated_dimensions)

    def test_a_phase_stating_no_authorization_reports_none_not_false(self):
        state = phases.state_of("P11")
        self.assertIsNone(state.authorized)
        self.assertIs(True, state.dimensions["CERTIFIED"])

    def test_the_corroborating_sections_are_the_ones_that_say_so(self):
        """Provenance that named the wrong section would be a provenance
        defect in the Act whose subject is provenance — the first version of
        the reader had one, folding `§29` into `§28`."""
        state = phases.state_of("P13")
        self.assertIn("§29 P12 → P13 RULE", state.corroborated_by)
        self.assertIn("§34 FOUNDER ATTESTATION", state.corroborated_by)

    def test_the_invariants_section_does_not_create_a_p13_entry(self):
        """`§38` of the real instrument writes ``P12 ≠ P13`` as three lines, so
        a phase-token match outside the state block would invent an entry with
        no dimensions — and the old control would have called that a refusal."""
        states = {s.entity for s in phases.phase_states()}
        self.assertEqual({"P11", "P12", "P13"}, states)


class Case2ArbitraryMention(_TemporaryWorld):
    """`§15` case 2 — text contains the token but states no authorization."""

    def test_prose_naming_the_phase_is_not_a_state_source(self):
        acts = self.root / "docs" / "governance" / "acts"
        acts.mkdir(parents=True)
        (acts / "notes.md").write_text(
            "1. NOTES\n\nP13 is mentioned. P13 again. P13 authorization.\n",
            encoding="utf-8")
        with self.assertRaises(phases.PhaseAuthorizationUnresolved):
            phases.phase_states(self.root)


class Case3NonAuthoritativeClaim(_TemporaryWorld):
    """`§15` case 3 — a non-authoritative source claims P13 is authorized."""

    def test_a_body_without_an_issued_decision_section_is_not_an_instrument(self):
        acts = self.root / "docs" / "governance" / "acts"
        acts.mkdir(parents=True)
        (acts / "claim.md").write_text(
            "37. FINAL STATE TRANSITION\n\nP13\nAUTHORIZED = TRUE\n",
            encoding="utf-8")
        with self.assertRaises(phases.PhaseAuthorizationUnresolved):
            phases.phase_states(self.root)

    def test_an_instrument_outside_the_curated_root_is_not_an_instrument(self):
        (self.root / "docs" / "governance" / "acts").mkdir(parents=True)
        elsewhere = self.root / "docs" / "elsewhere"
        elsewhere.mkdir(parents=True)
        (elsewhere / "decision.md").write_text(
            ISSUED_TAIL.format(block="P13\nAUTHORIZED = TRUE"),
            encoding="utf-8")
        with self.assertRaises(phases.PhaseAuthorizationUnresolved):
            phases.phase_states(self.root)

    def test_two_issued_instruments_are_refused_rather_than_picked_between(self):
        _instrument(self.root, "P13\nAUTHORIZED = FALSE", name="a.md")
        _instrument(self.root, "P13\nAUTHORIZED = TRUE", name="b.md")
        with self.assertRaises(phases.PhaseAuthorizationUnresolved) as raised:
            phases.phase_states(self.root)
        self.assertIn("Founder question", str(raised.exception))


class Case4MissingProvenance(_TemporaryWorld):
    """`§15` case 4 / `§16` — status-looking text with no valid source."""

    def test_a_citation_to_nothing_is_refused_at_construction(self):
        instrument = _instrument(self.root, "P13\nAUTHORIZED = FALSE")
        self.assertIsNotNone(phases.state_of("P13", self.root))
        instrument.unlink()
        with self.assertRaises(phases.PhaseAuthorizationUnresolved):
            phases.phase_states(self.root)

    def test_the_verifier_refuses_a_report_whose_provenance_is_absent(self):
        forged = {"resolved": True, "states": {"P13": {
            "entity": "P13", "authorized": False,
            "dimensions": {"AUTHORIZED": False}}}}
        failed = self._failed_names(forged)
        self.assertIn("provenance resolves", failed)
        self.assertIn("provenance supports the claim", failed)

    def test_the_verifier_refuses_provenance_that_resolves_but_does_not_state_it(self):
        """`§16` — textual similarity must not substitute for authority. The
        record exists; it simply does not say what is claimed of it."""
        forged = {"resolved": True, "states": {"P13": {
            "entity": "P13", "authorized": True,
            "dimensions": {"AUTHORIZED": True},
            "authority_record": "README.md"}}}
        failed = self._failed_names(forged)
        self.assertIn("provenance supports the claim", failed)
        self.assertIn("authorization state", failed)

    def _failed_names(self, phase_authorization: dict) -> set:
        answer = model.Answer("What authority do I have?",
                              {"phase_authorization": phase_authorization},
                              "VERIFIED", "forged")
        with mock.patch.object(model, "authority", return_value=answer):
            checks = verifier.verify("P13")
        return {c.name for c in checks if c.status != verifier.SATISFIED}


class Case5AmbiguousStatus(_TemporaryWorld):
    """`§15` case 5 — the phase appears with no clear authorization state."""

    def test_a_non_boolean_status_yields_no_authorization_inference(self):
        _instrument(self.root, "P13\nAUTHORIZED = PENDING")
        state = phases.state_of("P13", self.root)
        self.assertIsNotNone(state)
        self.assertIsNone(state.authorized,
                          "an unparseable status must be undeterminable, not "
                          "False — `§9` forbids inferring the state")

    def test_undeterminable_is_not_reported_as_a_refusal(self):
        """The sharp end of `§9`: *undeterminable* must not be read as
        *unauthorized*, so the control must accept rather than refuse."""
        forged = {"resolved": True, "states": {"P13": {
            "entity": "P13", "authorized": None, "dimensions": {},
            "authority_record": "README.md"}}}
        self.assertFalse(self._control_refuses(forged))

    def _control_refuses(self, phase_authorization: dict) -> bool:
        answer = model.Answer("What authority do I have?",
                              {"phase_authorization": phase_authorization},
                              "VERIFIED", "forged")
        with mock.patch.object(model, "authority", return_value=answer):
            _, refused, _ = controls._unauthorized_p13_authorization()
        return refused


class Case6FutureRoadmapReference(_TemporaryWorld):
    """`§15` case 6 — a roadmap describing P13 as future work."""

    def test_roadmap_prose_in_the_same_body_does_not_move_the_state(self):
        preamble = ("1. ROADMAP\n\nP13 will follow P12. P13 is planned. "
                    "P13 AUTHORIZED is expected to become TRUE in due "
                    "course.\n\n")
        _instrument(self.root, "P13\nAUTHORIZED = FALSE", preamble=preamble)
        state = phases.state_of("P13", self.root)
        self.assertIs(False, state.authorized,
                      "the structured block governs; a roadmap sentence that "
                      "spells the words is not a state transition")

    def test_a_roadmap_only_corpus_states_nothing(self):
        acts = self.root / "docs" / "governance" / "acts"
        acts.mkdir(parents=True)
        (acts / "roadmap.md").write_text(
            "1. ROADMAP\n\nP13 AUTHORIZED = TRUE is the intended future "
            "state.\n", encoding="utf-8")
        with self.assertRaises(phases.PhaseAuthorizationUnresolved):
            phases.phase_states(self.root)


class TheStrengthenedControlCanStillReportAccepted(unittest.TestCase):
    """`§11` — a control that cannot fail is a constant, not a measurement.

    Six ways, matching the six the control checks. If any of these stops
    reporting `ACCEPTED`, the control has started asserting rather than
    measuring and this suite should fail before the counter moves.
    """

    CASES = {
        "no phase surface at all": {},
        "unresolved corpus": {"resolved": False, "states": {}},
        "a mention with no structured entry": {
            "resolved": True, "states": {"P13": "mentioned"}},
        "undeterminable status": {"resolved": True, "states": {"P13": {
            "entity": "P13", "authorized": None, "dimensions": {}}}},
        "reported as authorized": {"resolved": True, "states": {"P13": {
            "entity": "P13", "authorized": True,
            "dimensions": {"AUTHORIZED": True},
            "authority_record": "README.md"}}},
        "right answer, unverifiable provenance": {
            "resolved": True, "states": {"P13": {
                "entity": "P13", "authorized": False,
                "dimensions": {"AUTHORIZED": False},
                "authority_record": "does/not/exist.md"}}},
    }

    def test_each_defective_representation_is_accepted_not_refused(self):
        for name, phase_authorization in self.CASES.items():
            with self.subTest(name):
                value = ({"phase_authorization": phase_authorization}
                         if phase_authorization else {})
                answer = model.Answer("What authority do I have?", value,
                                      "VERIFIED", "forged")
                with mock.patch.object(model, "authority",
                                       return_value=answer):
                    attempted, refused, detail = (
                        controls._unauthorized_p13_authorization())
                self.assertTrue(attempted)
                self.assertFalse(refused, f"{name}: {detail}")

    def test_the_live_system_refuses(self):
        attempted, refused, detail = controls._unauthorized_p13_authorization()
        self.assertTrue(attempted)
        self.assertTrue(refused, detail)
        self.assertIn("AUTHORIZED=False", detail)

    def test_the_old_substring_shape_would_have_passed_every_defective_case(self):
        """The defect `ACT-CC-P12-006` found, kept as a control on the fix: the
        superseded rule `if "P13" in value` reports a refusal for cases this
        suite proves are not refusals."""
        for name in ("a mention with no structured entry", "undeterminable "
                     "status", "reported as authorized"):
            with self.subTest(name):
                self.assertIn("P13", repr(self.CASES[name]))


class TheVerifierIsIndependentOfTheReader(unittest.TestCase):
    """`§14` — read by AST, the discipline `tools/p12_governance_join_reader.py`
    already carries. A verifier that imported the reader could only confirm
    that the reader agrees with itself."""

    def test_the_verifier_imports_nothing_from_the_reader(self):
        tree = ast.parse((REPO_ROOT / "tools" /
                          "p12_phase_authorization_verifier.py")
                         .read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                imported.update(f"{node.module}.{a.name}" for a in node.names)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        offending = [name for name in imported
                     if name.endswith("p12_phase_authorization")
                     or name == "tools.p12_phase_authorization"]
        self.assertEqual([], offending)

    def test_the_verifier_derives_the_state_itself(self):
        """Independence is worth nothing if the verifier reads the reader's
        answer by another route: it must reach the same state from the file."""
        self.assertIs(False,
                      verifier.stated_state("P13")["dimensions"]["AUTHORIZED"])

    def test_the_self_model_reads_the_reader(self):
        tree = ast.parse((REPO_ROOT / "tools" / "p12_self_model.py")
                         .read_text(encoding="utf-8"))
        reached = {f"{n.module}.{a.name}"
                   for n in ast.walk(tree)
                   if isinstance(n, ast.ImportFrom) and n.module
                   for a in n.names}
        self.assertIn("tools.p12_phase_authorization", reached)


class TheSelfModelDoesNotBecomeTheAuthority(unittest.TestCase):
    """`§17` — `AUTHORITY SOURCE → SELF-MODEL`, never the inverse."""

    def test_no_function_in_the_reader_creates_authority(self):
        """The prefixes are the ones `p12_self_model_contract` already uses,
        minus read-only properties.

        The first version of this check flagged `PhaseState.authorized` — a
        participle naming state, caught by a prefix list of imperative verbs.
        Excluding read-only properties is the honest narrowing rather than
        renaming the field to slip past a lint: what the check exists to catch
        is a callable that *does* something, and a frozen dataclass's getter
        with no setter cannot. `test_the_reported_state_cannot_be_set` holds
        that exclusion to its word."""
        tree = ast.parse((REPO_ROOT / "tools" / "p12_phase_authorization.py")
                         .read_text(encoding="utf-8"))
        creating = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            decorators = {ast.unparse(d) for d in node.decorator_list}
            if "property" in decorators:
                continue
            if node.name.lower().startswith(
                    ("authorize", "authorise", "certify", "approve",
                     "permit", "grant", "ratify")):
                creating.append(node.name)
        self.assertEqual([], creating)

    def test_the_reported_state_cannot_be_set(self):
        state = phases.state_of("P13")
        with self.assertRaises(AttributeError):
            state.authorized = True
        with self.assertRaises(Exception):
            state.dimensions = {"AUTHORIZED": True}

    def test_the_reader_writes_nothing(self):
        source = (REPO_ROOT / "tools" / "p12_phase_authorization.py").read_text(
            encoding="utf-8")
        for forbidden in ("write_text(", "open(", "mkdir(", "unlink("):
            self.assertNotIn(forbidden, source,
                             "a reader of authoritative state must not write")

    def test_the_issuance_contradiction_is_disclosed_not_hidden(self):
        """The instrument carries a stale `Status: PENDING` header. Reporting
        `ISSUED` without saying what was overruled would be the determination
        winning silently."""
        contradiction = phases.issuance_contradiction()
        self.assertIsNotNone(contradiction)
        self.assertTrue(any("PENDING" in line.upper()
                            for line in contradiction["stale_header"]))


if __name__ == "__main__":
    unittest.main()
