"""Escalation persistence — durable across a process boundary, never an approval.

`ACT-CC-P11-007 §13` requires persistence that preserves identity, authority
provenance, reason, lifecycle and linkage, and that **survives the relevant
process boundary**. `§14` requires that a persisted escalation never read as
authorization, approval, success or completion.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.governance import HumanAuthority  # noqa: E402
from tools.escalation_register import (  # noqa: E402
    EscalationRegister,
    EscalationRegisterError,
)
from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    EscalationRequired,
    Goal,
    Plan,
    PlanStep,
    PlanningSurface,
)

AUTHORITY = "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"


def _provenance():
    return AuthorityProvenance("DP-01 §3 W2", AUTHORITY)


def _raise_a_real_escalation():
    """Produce a genuine escalation rather than constructing one by hand.

    The register refuses invented entries, so the tests must obtain a real
    refusal — which also proves the two surfaces actually fit together.
    """
    surface = PlanningSurface()
    surface.declare(Goal("g", "Intent.", _provenance()))
    plan = surface.adopt(Plan(key="p", goal_key="g", authority=_provenance(),
                              steps=(PlanStep("a", "A."),)))
    try:
        surface.adapt(plan, steps=plan.steps, reason="Needs wider authority.",
                      required_authority="DP-02")
    except EscalationRequired as error:
        return error
    raise AssertionError("the surface failed to escalate")


class AnEscalationIsRecordedAsItWasRaised(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.register = EscalationRegister(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def test_the_recorded_pair_is_the_one_the_refusal_was_made_on(self):
        record = self.register.record(_raise_a_real_escalation(),
                                      subject="plan p", authority=_provenance())
        self.assertEqual(record.required, "DP-02")
        self.assertEqual(record.held, "DP-01 §3 W2")

    def test_every_required_element_is_preserved(self):
        record = self.register.record(_raise_a_real_escalation(),
                                      subject="plan p", authority=_provenance())
        payload = self.register.load(record.escalation_id)
        for field in ("escalation_id", "subject", "required", "held", "reason",
                      "authority_instrument", "authority_record", "raised_at"):
            self.assertIn(field, payload)
            self.assertTrue(payload[field], field)

    def test_an_invented_escalation_cannot_be_recorded(self):
        """A register that accepts entries nobody raised is not evidence."""
        for bogus in ("Founder Reserved Authority", None, 42,
                      RuntimeError("denied")):
            with self.subTest(value=bogus):
                with self.assertRaises(EscalationRegisterError):
                    self.register.record(bogus, subject="s",
                                         authority=_provenance())

    def test_provenance_must_be_a_validated_citation(self):
        with self.assertRaises(EscalationRegisterError):
            self.register.record(_raise_a_real_escalation(), subject="s",
                                 authority="Governance Authority")


class EscalationIsNotApproval(unittest.TestCase):
    """`§14`. The property the module is shaped around."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.register = EscalationRegister(Path(self._tmp.name))
        self.record = self.register.record(_raise_a_real_escalation(),
                                           subject="plan p",
                                           authority=_provenance())

    def tearDown(self):
        self._tmp.cleanup()

    def test_a_new_escalation_is_open_and_nothing_can_close_it_alone(self):
        self.assertEqual(self.register.status(self.record.escalation_id), "OPEN")
        closers = [n for n in dir(self.register)
                   if any(v in n.lower() for v in
                          ("close", "approve", "grant", "authorize", "resolve",
                           "accept"))]
        self.assertEqual(closers, [])

    def test_automation_cannot_answer_an_escalation(self):
        """`HumanAuthority` is the boundary automation cannot cross."""
        for not_a_human in ("automation", None, {"reviewer_id": "bot"}, 1):
            with self.subTest(value=not_a_human):
                with self.assertRaises(EscalationRegisterError):
                    self.register.record_response(
                        self.record.escalation_id, authority=not_a_human,
                        response="approved")

    def test_a_human_response_marks_answered_and_never_approved(self):
        self.register.record_response(
            self.record.escalation_id,
            authority=HumanAuthority("a-real-human"), response="Denied.")
        self.assertEqual(self.register.status(self.record.escalation_id),
                         "ANSWERED")
        self.assertNotEqual(self.register.status(self.record.escalation_id),
                            "APPROVED")

    def test_the_response_does_not_overwrite_the_escalation(self):
        """The original claim survives its own answer."""
        before = self.register.load(self.record.escalation_id)
        self.register.record_response(
            self.record.escalation_id,
            authority=HumanAuthority("a-real-human"), response="Denied.")
        self.assertEqual(self.register.load(self.record.escalation_id), before)

    def test_a_second_response_is_refused_append_only(self):
        self.register.record_response(
            self.record.escalation_id,
            authority=HumanAuthority("h"), response="Denied.")
        with self.assertRaises(EscalationRegisterError):
            self.register.record_response(
                self.record.escalation_id,
                authority=HumanAuthority("h"), response="Actually, approved.")

    def test_answering_grants_no_permission_anywhere(self):
        """An answered escalation does not widen what the plan may do."""
        self.register.record_response(
            self.record.escalation_id,
            authority=HumanAuthority("h"), response="Acknowledged.")
        surface = PlanningSurface()
        surface.declare(Goal("g", "Intent.", _provenance()))
        plan = surface.adopt(Plan(key="p", goal_key="g", authority=_provenance(),
                                  steps=(PlanStep("a", "A."),)))
        with self.assertRaises(EscalationRequired):
            surface.adapt(plan, steps=plan.steps, reason="Now allowed?",
                          required_authority="DP-02")


class PersistenceSurvivesTheProcessBoundary(unittest.TestCase):
    """`§13` item 7, tested literally — a **separate interpreter** reads it back.

    An in-process assertion would prove only that a dict survived a function
    call. The requirement is that an escalation outlive the run that raised it,
    so the read happens in a subprocess that shares nothing but the filesystem.
    """

    def test_a_recorded_escalation_is_readable_from_a_fresh_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            register = EscalationRegister(Path(tmp))
            record = register.record(_raise_a_real_escalation(),
                                     subject="plan p", authority=_provenance())
            proc = subprocess.run(
                [sys.executable, "-c",
                 "import sys; sys.path.insert(0, sys.argv[1]);"
                 "from pathlib import Path;"
                 "from tools.escalation_register import EscalationRegister;"
                 "r = EscalationRegister(Path(sys.argv[2]));"
                 "import json; print(json.dumps({"
                 "'open': list(r.open_escalations()),"
                 "'status': r.status(sys.argv[3]),"
                 "'held': r.load(sys.argv[3])['held']}))",
                 str(REPO_ROOT), tmp, record.escalation_id],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            seen = json.loads(proc.stdout)
            self.assertEqual(seen["open"], [record.escalation_id])
            self.assertEqual(seen["status"], "OPEN")
            self.assertEqual(seen["held"], "DP-01 §3 W2")

    def test_an_answer_from_one_process_is_visible_to_another(self):
        with tempfile.TemporaryDirectory() as tmp:
            register = EscalationRegister(Path(tmp))
            record = register.record(_raise_a_real_escalation(),
                                     subject="plan p", authority=_provenance())
            register.record_response(record.escalation_id,
                                     authority=HumanAuthority("h"),
                                     response="Denied.")
            fresh = EscalationRegister(Path(tmp))
            self.assertEqual(fresh.open_escalations(), ())
            self.assertEqual(fresh.status(record.escalation_id), "ANSWERED")


class TheRegisterDoesNotCoupleToPlanning(unittest.TestCase):
    """Planning must stay unaware that persistence exists.

    If Planning imported the register, its negative controls would be describing
    a module that had grown a dependency on durable storage — and a caller could
    no longer choose *not* to persist.
    """

    def test_planning_does_not_import_the_register(self):
        import ast
        for path in sorted((REPO_ROOT / "tools" / "planning").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotIn("escalation_register", node.module)

    def test_the_register_requires_an_explicit_root(self):
        """No default directory — choosing a canonical home is not this Act's."""
        with self.assertRaises(EscalationRegisterError):
            EscalationRegister("not-a-path")


if __name__ == "__main__":
    unittest.main()
