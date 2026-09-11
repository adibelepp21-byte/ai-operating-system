"""`ACT-CC-P11-014` — escalation subject semantics and organizational wiring.

Two separate results are protected here, and they must not be confused:

**`E4`.** Same-subject uniqueness is **not** a canonical requirement. The
ratified Domain Model `§10` lists *Escalation / Incident* among deferred
concepts — *"Not canonical entities in v1.0"* — and `DP-04 §7` fixes that
*"Escalation is represented as a ratified Trace status rather than an
independent organizational entity."* Trace's semantics are invariant 4,
*"production is unconditional, never optional"*, and invariant 5, append-only.
So the controls below assert that duplication is **preserved**, not prevented:
a test suite that silently acquired deduplication would be enforcing a Domain
Model change nobody issued.

**`E2`.** The refusal → organizational-escalation wiring existed on the W4 path
and **not on W1**. These controls hold it on both.

`§22` — no control here asserts *"there is one file"*, *"the count is expected"*
or *"the directory is empty"* about the resident corpus. Every population it
measures is one it created.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.governance import HumanAuthority  # noqa: E402
from tools.escalation_register import (  # noqa: E402
    EscalationRegister,
    EscalationRegisterError,
    record_refusals,
)
from tools.planning import AuthorityProvenance, EscalationRequired  # noqa: E402
from tools.w4_execution import ExecutionRefused  # noqa: E402

FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")
SUBJECT = "plan p-0 / delegation d-0"


def authority():
    return AuthorityProvenance("FD-P11-001 §9", FD_RECORD)


def refusal(step="report-conformance", held=("verify-delegation-elements",)):
    return ExecutionRefused(f"step {step!r} is outside the delegated work scope",
                            required=step, held=held)


class TempRegister(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.register = EscalationRegister(self.root)
        self.addCleanup(self._tmp.cleanup)

    def files(self):
        return sorted(p.name for p in self.root.glob("*.escalation.json"))


class C1_SameSubjectRepeated(TempRegister):
    """`§20.1` — and the control that proves `E4` rather than assuming it."""

    def test_two_identical_refusals_produce_two_occurrences(self):
        a = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority())
        b = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority())
        self.assertNotEqual(a.escalation_id, b.escalation_id)
        self.assertEqual(2, len(self.files()))
        self.assertEqual(2, len(self.register.open_escalations()))

    def test_the_two_records_agree_on_everything_but_identity_and_time(self):
        """They are the same *subject*, and the register says so plainly —
        which is what makes the multiplicity legible rather than accidental."""
        a = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority()).to_payload()
        b = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority()).to_payload()
        volatile = ("escalation_id", "raised_at")
        self.assertEqual({k: v for k, v in a.items() if k not in volatile},
                         {k: v for k, v in b.items() if k not in volatile})

    def test_no_deduplication_is_introduced_by_the_wiring_helper(self):
        """`§17`/`§24` — `record_refusals` must not acquire suppression.

        Suppressing a raised refusal is the shape `DP-01` `NC-10` forbids:
        *"Escalation must not be silently converted into success."*
        """
        first = record_refusals(self.root, [refusal()], subject=SUBJECT,
                                authority=authority())
        second = record_refusals(self.root, [refusal()], subject=SUBJECT,
                                 authority=authority())
        self.assertEqual(1, len(first))
        self.assertEqual(1, len(second))
        self.assertNotEqual(first, second)
        self.assertEqual(2, len(self.register.all_escalations()))


class C2_DifferentSubject(TempRegister):
    """`§20.2` / `F1` — similar text must not collapse into one subject."""

    def test_subjects_differing_only_slightly_stay_distinct(self):
        self.register.record(refusal(), subject=SUBJECT, authority=authority())
        self.register.record(refusal(), subject=SUBJECT + " (rerun)",
                             authority=authority())
        subjects = {json.loads((self.root / n).read_text())["subject"]
                    for n in self.files()}
        self.assertEqual(2, len(subjects))

    def test_different_refusal_types_are_both_sanctioned_and_distinguishable(self):
        """`EscalationRequired` is a *plan* exceeding authority;
        `ExecutionRefused` is a *step* exceeding its delegation."""
        self.register.record(
            EscalationRequired("plan exceeds authority", required="r",
                               held="h"),
            subject=SUBJECT, authority=authority())
        self.register.record(refusal(), subject=SUBJECT, authority=authority())
        reasons = {json.loads((self.root / n).read_text())["reason"]
                   for n in self.files()}
        self.assertEqual(2, len(reasons))


class C3_ResolvedThenRecurs(TempRegister):
    """`§20.3` / `F3` — an answered subject does not bar a real recurrence."""

    def test_a_new_occurrence_after_a_response_is_recorded(self):
        first = self.register.record(refusal(), subject=SUBJECT,
                                     authority=authority())
        self.register.record_response(
            first.escalation_id,
            authority=HumanAuthority(reviewer_id="founder"),
            response="acknowledged")
        self.assertEqual("ANSWERED", self.register.status(first.escalation_id))
        second = self.register.record(refusal(), subject=SUBJECT,
                                      authority=authority())
        self.assertEqual("OPEN", self.register.status(second.escalation_id))
        self.assertEqual((second.escalation_id,),
                         self.register.open_escalations())

    def test_answering_one_occurrence_does_not_answer_another(self):
        a = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority())
        b = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority())
        self.register.record_response(
            a.escalation_id, authority=HumanAuthority(reviewer_id="founder"),
            response="acknowledged")
        self.assertEqual("ANSWERED", self.register.status(a.escalation_id))
        self.assertEqual("OPEN", self.register.status(b.escalation_id))


class C4_C5_StaleAndMissingReferences(TempRegister):
    """`§20.4`, `§20.5` — a reference to nothing is not an escalation."""

    def test_status_of_an_unknown_id_fails_closed(self):
        with self.assertRaises(EscalationRegisterError):
            self.register.status("0" * 16)

    def test_loading_an_unknown_id_fails_closed(self):
        with self.assertRaises(EscalationRegisterError):
            self.register.load("0" * 16)

    def test_responding_to_an_unknown_id_fails_closed(self):
        with self.assertRaises(EscalationRegisterError):
            self.register.record_response(
                "0" * 16, authority=HumanAuthority(reviewer_id="founder"),
                response="x")

    def test_an_evidence_reference_with_no_record_is_detectable(self):
        """A stale id in an evidence file must be recoverable as *absent*,
        not silently treated as a live escalation."""
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        named = {recorded.escalation_id, "f" * 16}
        present = set(self.register.all_escalations())
        self.assertEqual({"f" * 16}, named - present)


class C6_InvalidProvenance(TempRegister):
    """`§20.6` / `§12` — a record does not become an escalation by existing."""

    def test_an_unsanctioned_error_may_not_be_recorded(self):
        with self.assertRaises(EscalationRegisterError):
            self.register.record(RuntimeError("not a sanctioned refusal"),
                                 subject=SUBJECT, authority=authority())

    def test_an_unvalidated_citation_may_not_be_recorded(self):
        with self.assertRaises(EscalationRegisterError):
            self.register.record(refusal(), subject=SUBJECT,
                                 authority="FD-P11-001 §9")

    def test_the_helper_inherits_both_refusals(self):
        with self.assertRaises(EscalationRegisterError):
            record_refusals(self.root, [RuntimeError("nope")], subject=SUBJECT,
                            authority=authority())
        with self.assertRaises(EscalationRegisterError):
            record_refusals(self.root, [refusal()], subject=SUBJECT,
                            authority="not a provenance")


class C7_C10_HumanAuthority(TempRegister):
    """`§20.7`, `§20.10`, `§15` — automation may request, never decide."""

    def test_a_response_without_human_authority_is_refused(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        for impostor in (None, "founder", object(), authority()):
            with self.subTest(impostor=type(impostor).__name__):
                with self.assertRaises(EscalationRegisterError):
                    self.register.record_response(
                        recorded.escalation_id, authority=impostor,
                        response="approved")
        self.assertEqual("OPEN", self.register.status(recorded.escalation_id))

    def test_there_is_no_status_that_means_approved(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        self.assertEqual("OPEN", self.register.status(recorded.escalation_id))
        self.register.record_response(
            recorded.escalation_id,
            authority=HumanAuthority(reviewer_id="founder"),
            response="approved in full")
        self.assertEqual("ANSWERED", self.register.status(recorded.escalation_id))

    def test_no_public_method_returns_a_permission(self):
        """`§24` — the purpose is state integrity, not governance automation."""
        names = [n for n in dir(EscalationRegister) if not n.startswith("_")]
        for name in names:
            for forbidden in ("approve", "authorize", "permit", "grant",
                              "resolve", "close"):
                self.assertNotIn(forbidden, name.lower(), name)


class C8_DuplicatePersistence(TempRegister):
    """`§20.8` — append-only, at the level where canon actually requires it."""

    def test_a_response_may_not_be_written_twice(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        human = HumanAuthority(reviewer_id="founder")
        self.register.record_response(recorded.escalation_id, authority=human,
                                      response="first")
        with self.assertRaises(EscalationRegisterError):
            self.register.record_response(recorded.escalation_id,
                                          authority=human, response="second")
        payload = json.loads(
            (self.root / f"{recorded.escalation_id}.response.json").read_text())
        self.assertEqual("first", payload["response"])

    def test_the_original_claim_survives_its_own_answer(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        before = (self.root /
                  f"{recorded.escalation_id}.escalation.json").read_text()
        self.register.record_response(
            recorded.escalation_id,
            authority=HumanAuthority(reviewer_id="founder"), response="x")
        after = (self.root /
                 f"{recorded.escalation_id}.escalation.json").read_text()
        self.assertEqual(before, after)


class C9_FreshProcess(TempRegister):
    """`§20.9`, `§18` — state integrity across a real process boundary."""

    def test_a_separate_interpreter_reconstructs_the_same_state(self):
        a = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority())
        b = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority())
        self.register.record_response(
            a.escalation_id, authority=HumanAuthority(reviewer_id="founder"),
            response="acknowledged")
        script = (
            "import sys, json; sys.path.insert(0, %r);"
            "from pathlib import Path;"
            "from tools.escalation_register import EscalationRegister;"
            "r = EscalationRegister(Path(%r));"
            "print(json.dumps({'open': list(r.open_escalations()),"
            "'all': list(r.all_escalations()),"
            "'statuses': {i: r.status(i) for i in r.all_escalations()}}))"
            % (str(REPO_ROOT), str(self.root)))
        done = subprocess.run([sys.executable, "-c", script],
                              capture_output=True, text=True)
        self.assertEqual(0, done.returncode, done.stderr)
        fresh = json.loads(done.stdout)
        self.assertEqual(list(self.register.open_escalations()), fresh["open"])
        self.assertEqual([b.escalation_id], fresh["open"])
        self.assertEqual("ANSWERED", fresh["statuses"][a.escalation_id])

    def test_a_fresh_process_repeating_the_condition_still_does_not_dedupe(self):
        """`§18` asks whether idempotency survives a process boundary. There is
        none to survive, and that is the proven canonical answer — asserted so
        that acquiring one later fails loudly rather than passing quietly."""
        record_refusals(self.root, [refusal()], subject=SUBJECT,
                        authority=authority())
        script = (
            "import sys; sys.path.insert(0, %r);"
            "from pathlib import Path;"
            "from tools.escalation_register import record_refusals;"
            "from tools.w4_execution import ExecutionRefused;"
            "from tools.planning import AuthorityProvenance;"
            "print(record_refusals(Path(%r), [ExecutionRefused('x',"
            " required='report-conformance', held=('a',))],"
            " subject=%r, authority=AuthorityProvenance('FD-P11-001 §9', %r)))"
            % (str(REPO_ROOT), str(self.root), SUBJECT, FD_RECORD))
        done = subprocess.run([sys.executable, "-c", script],
                              capture_output=True, text=True)
        self.assertEqual(0, done.returncode, done.stderr)
        self.assertEqual(2, len(self.register.all_escalations()))


class E2_BothCanonicalPathsAreWired(unittest.TestCase):
    """The repair: refusals reach organizational state from **both** paths.

    Read by AST. A substring search for `record_refusals` would match the
    import, a comment, or this docstring — the false-positive class `§22` names,
    and one this programme has already produced five times.
    """

    #: Every production module that runs a `W4Executor`. Hand-maintained lists
    #: of surfaces are how W1 came to have no escalation wiring in the first
    #: place, so `test_the_list_covers_every_production_execution_path` derives
    #: the real set from source and fails if this one is narrower.
    PATHS = ("tools/w4_first_run.py", "tools/w1_coordination_run.py",
             "tools/w1_cross_department_run.py")

    def _execution_paths(self):
        """Modules that construct a `W4Executor`, discovered — not listed."""
        found = set()
        for directory in ("tools", "consumers"):
            for path in sorted((REPO_ROOT / directory).rglob("*.py")):
                if "tests" in path.parts:
                    continue
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and \
                            isinstance(node.func, ast.Name) and \
                            node.func.id == "W4Executor":
                        found.add(path.relative_to(REPO_ROOT).as_posix())
        return found

    def test_the_list_covers_every_production_execution_path(self):
        """`ACT-CC-P11-015 §19` — a control's population must be complete.

        Four times in this programme a control has covered part of its
        population and passed on the part it covered: a loader reading one of
        two operational roots, a continuity reader knowing one evidence
        filename, a line-coherence list naming two of three emitters, and this
        one — correct today only because someone maintained it by hand.
        """
        discovered = self._execution_paths()
        self.assertTrue(discovered, "precondition: no execution path found")
        self.assertLessEqual(
            discovered, set(self.PATHS),
            "these run a W4Executor and are not checked for escalation "
            "wiring: %s" % sorted(discovered - set(self.PATHS)))

    def _calls(self, module):
        tree = ast.parse((REPO_ROOT / module).read_text(encoding="utf-8"))
        return [n for n in ast.walk(tree)
                if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Name)
                and n.func.id == "record_refusals"]

    def test_each_canonical_run_path_calls_the_wiring_exactly_once(self):
        for module in self.PATHS:
            with self.subTest(module=module):
                self.assertEqual(1, len(self._calls(module)))

    def test_each_call_passes_the_executors_own_refusals(self):
        """Not a list built elsewhere — the refusals the run actually made."""
        for module in self.PATHS:
            with self.subTest(module=module):
                call = self._calls(module)[0]
                self.assertTrue(call.args, "refusals must be passed")
                source = ast.unparse(call.args[1])
                self.assertEqual("report.refusals", source)

    def test_each_call_cites_a_validated_authority_provenance(self):
        for module in self.PATHS:
            with self.subTest(module=module):
                call = self._calls(module)[0]
                keywords = {k.arg: ast.unparse(k.value) for k in call.keywords}
                self.assertIn("authority", keywords)
                self.assertIn("AuthorityProvenance", keywords["authority"])
                self.assertIn("subject", keywords)

    def test_no_run_path_constructs_its_own_register(self):
        """`§13` — one wiring, reused. Two copies is how W1 came to have none."""
        for module in self.PATHS:
            with self.subTest(module=module):
                tree = ast.parse((REPO_ROOT / module).read_text(encoding="utf-8"))
                names = {n.func.id for n in ast.walk(tree)
                         if isinstance(n, ast.Call)
                         and isinstance(n.func, ast.Name)}
                self.assertNotIn("EscalationRegister", names)

    def test_the_w1_evidence_shape_carries_escalations(self):
        """The field a reader needs in order to find them at all."""
        tree = ast.parse(
            (REPO_ROOT / "tools/w1_coordination_run.py").read_text(
                encoding="utf-8"))
        keys = {n.value for n in ast.walk(tree)
                if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        self.assertIn("escalations", keys)


class MutationControls(TempRegister):
    """`§21` — each control must fail when its invariant is broken.

    Mutation here is applied to **state and inputs**, not to the module source:
    a source-rewriting probe of mine has produced a false verdict by four
    different mechanisms in this programme. Every case below breaks the
    protected condition for real and asserts the control notices.
    """

    def test_mutating_subject_identity_is_visible(self):
        a = self.register.record(refusal(), subject=SUBJECT,
                                 authority=authority())
        b = self.register.record(refusal(), subject="a different subject",
                                 authority=authority())
        self.assertNotEqual(self.register.load(a.escalation_id)["subject"],
                            self.register.load(b.escalation_id)["subject"])

    def test_mutating_active_state_filtering_is_visible(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        self.assertIn(recorded.escalation_id, self.register.open_escalations())
        (self.root / f"{recorded.escalation_id}.response.json").write_text(
            json.dumps({"escalation_id": recorded.escalation_id}),
            encoding="utf-8")
        self.assertNotIn(recorded.escalation_id,
                         self.register.open_escalations())
        self.assertEqual("ANSWERED", self.register.status(recorded.escalation_id))

    def test_mutating_persistence_is_visible(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        (self.root / f"{recorded.escalation_id}.escalation.json").unlink()
        with self.assertRaises(EscalationRegisterError):
            self.register.status(recorded.escalation_id)
        self.assertEqual((), self.register.all_escalations())

    def test_mutating_lifecycle_state_is_visible(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())
        response = self.root / f"{recorded.escalation_id}.response.json"
        response.write_text("{}", encoding="utf-8")
        self.assertEqual("ANSWERED", self.register.status(recorded.escalation_id))
        response.unlink()
        self.assertEqual("OPEN", self.register.status(recorded.escalation_id))

    def test_mutating_provenance_is_refused_at_the_boundary(self):
        for bad in (None, "FD-P11-001 §9", 0):
            with self.subTest(bad=bad):
                with self.assertRaises(EscalationRegisterError):
                    self.register.record(refusal(), subject=SUBJECT,
                                         authority=bad)

    def test_mutating_the_human_authority_requirement_is_refused(self):
        recorded = self.register.record(refusal(), subject=SUBJECT,
                                        authority=authority())

        class LooksLikeAuthority:
            reviewer_id = "founder"

        with self.assertRaises(EscalationRegisterError):
            self.register.record_response(recorded.escalation_id,
                                          authority=LooksLikeAuthority(),
                                          response="approved")
        self.assertEqual("OPEN", self.register.status(recorded.escalation_id))

    def test_mutating_the_wiring_call_is_caught_by_the_ast_control(self):
        """The `E2` control, mutation-tested against a source it does not own:
        a copy with the call removed must fail the same check."""
        source = (REPO_ROOT / "tools/w1_coordination_run.py").read_text(
            encoding="utf-8")
        mutated = source.replace("record_refusals(", "_suppressed_wiring(")
        self.assertNotEqual(source, mutated, "anchor did not match")
        tree = ast.parse(mutated)
        calls = [n for n in ast.walk(tree)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                 and n.func.id == "record_refusals"]
        self.assertEqual([], calls)


class CanonicalGrounding(unittest.TestCase):
    """`§10` — the classification rests on resident canonical bodies, quoted.

    Read from source on every run. If a future edit changes what these
    documents say, the `E4` classification stops being supported and this fails
    — which is the difference between a classification and a memory of one.
    """

    def _text(self, relative):
        return " ".join((REPO_ROOT / relative).read_text(
            encoding="utf-8").split())

    def test_escalation_is_a_deferred_concept_in_the_ratified_domain_model(self):
        body = self._text("docs/architecture/domain-model/"
                          "canonical-domain-model-v1.md")
        self.assertIn("Deferred concepts. Not canonical entities in v1.0.", body)
        self.assertIn("no dedicated entity required yet", body)

    def test_dp04_places_escalation_on_trace_not_as_an_entity(self):
        body = self._text("docs/architecture/p11/"
                          "DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md")
        self.assertIn("Escalation is represented as a ratified Trace status "
                      "rather than an independent organizational entity.", body)

    def test_trace_production_is_unconditional_and_append_only(self):
        body = self._text("docs/architecture/domain-model/"
                          "canonical-domain-model-v1.md")
        self.assertIn("production is unconditional, never optional", body)
        self.assertIn("Trace is immutable and append-only", body)

    def test_nc10_forbids_converting_escalation_into_success(self):
        body = self._text("docs/governance/acts/"
                          "DP-01-P11-FOUNDER-AUTHORIZATION.md")
        self.assertIn("Escalation must not be silently converted into success.",
                      body)

    def test_no_canonical_body_requires_one_open_escalation_per_subject(self):
        """The absence that makes `E4` the answer, asserted rather than assumed.

        Stated as a search over the bodies that would have to carry such a rule.
        It is not proof of a universal negative — it is proof that the documents
        governing escalation do not contain one, which is what `§10` asks.
        """
        for relative in ("docs/architecture/domain-model/canonical-domain-model-v1.md",
                         "docs/architecture/p11/DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md",
                         "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md",
                         "docs/governance/acts/"
                         "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md"):
            body = self._text(relative).lower()
            for phrase in ("one open escalation", "single open escalation",
                           "duplicate escalation", "escalation idempoten",
                           "same-subject escalation", "unique escalation"):
                self.assertNotIn(phrase, body, f"{relative}: {phrase}")


if __name__ == "__main__":
    unittest.main()
