"""Tests for the corpus citation auditor.

The auditor exists because this corpus repeatedly produced citations that
pointed at nothing, or at the wrong section. These tests hold it to the one
promise it makes — that a resolved citation means the *pointer* is real — and
to the discipline that it must not overstate that.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOL = REPO_ROOT / "tools" / "corpus_citation_audit.py"


def run(*args):
    proc = subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    return proc


class CorpusCitationAuditTests(unittest.TestCase):
    def test_tool_runs_and_reports_json(self):
        proc = run("--json")
        report = json.loads(proc.stdout)
        for key in ("documents_scanned", "citations_checked", "findings",
                    "errors", "warnings", "non_resident"):
            self.assertIn(key, report)

    def test_corpus_has_no_unresolved_citations(self):
        """Every citation in the corpus resolves, or is a recorded non-residency.

        This is the regression the auditor was built to hold. A failure here
        means a citation was introduced pointing at a file that does not exist.
        """
        report = json.loads(run("--json").stdout)
        unresolved = [f for f in report["findings"] if f["severity"] == "ERROR"]
        self.assertEqual(
            unresolved, [],
            "unresolved citations introduced:\n"
            + "\n".join(f"  {f['source']}  `{f['citation']}`  {f['message']}"
                        for f in unresolved),
        )

    def test_it_actually_scans_something(self):
        """Guards against a silent pass caused by scanning an empty tree."""
        report = json.loads(run("--json").stdout)
        self.assertGreater(report["documents_scanned"], 0)
        self.assertGreater(report["citations_checked"], 50)

    def test_missing_root_is_an_error_not_a_silent_pass(self):
        proc = run("--json", "docs/no-such-directory-exists")
        report = json.loads(proc.stdout)
        self.assertEqual(report["errors"], 1)
        self.assertNotEqual(proc.returncode, 0)

    def test_non_resident_citations_are_not_counted_as_errors(self):
        """A deliberately cited absent authority is a finding, not a defect.

        Narrowed 2026-09-09: this previously asserted that *every* INFO finding
        was a non-residency, which was true only while INFO had one meaning. The
        §27 quotation check now also reports INFO. The assertion that matters —
        that a recorded non-residency is never an ERROR — is unchanged.
        """
        report = json.loads(run("--json").stdout)
        self.assertGreater(report["non_resident"], 0)
        for finding in report["findings"]:
            if "NON-RESIDENT" in finding["message"]:
                self.assertEqual(finding["severity"], "INFO")

    def test_section_misses_are_warnings_not_errors(self):
        """Heading conventions vary; 'unconfirmed' must not be reported as 'wrong'."""
        report = json.loads(run("--json").stdout)
        for finding in report["findings"]:
            if "section heading not located" in finding["message"]:
                self.assertEqual(finding["severity"], "WARN")
                self.assertIn("not disproved", finding["message"])



class TheAuditedModulePopulationIsComplete(unittest.TestCase):
    """`ACT-CC-P11-017` — a module outside the roots has unchecked citations.

    `DEFAULT_ROOTS` enumerated `tools/` modules one entry per Act, and by the
    time this was written **five P11 modules had been created since the last
    entry and none of their citations had ever been checked.** They were clean;
    nothing would have said so if they were not.
    """

    EXCLUDED = {"tools/corpus_citation_audit.py"}

    def test_every_top_level_tools_module_is_audited(self):
        from tools.corpus_citation_audit import DEFAULT_ROOTS
        audited = set(DEFAULT_ROOTS)
        present = {str(p.relative_to(REPO_ROOT))
                   for p in (REPO_ROOT / "tools").glob("*.py")}
        self.assertTrue(present, "precondition: no modules found")
        missing = sorted(present - audited - self.EXCLUDED)
        self.assertEqual(missing, [], f"unaudited tools modules: {missing}")

    def test_the_exclusion_is_the_auditor_and_nothing_else(self):
        """An exclusion list is where a stale population hides next."""
        self.assertEqual({"tools/corpus_citation_audit.py"}, self.EXCLUDED)
        from tools.corpus_citation_audit import DEFAULT_ROOTS
        for name in self.EXCLUDED:
            self.assertNotIn(name, DEFAULT_ROOTS)


if __name__ == "__main__":
    unittest.main()


class LineCountingTests(unittest.TestCase):
    """Regression for a bug that made the auditor manufacture defects.

    ``str.splitlines()`` splits on U+2028, U+0085 and other Unicode separators
    that ``sed``, editors, and the line numbers this corpus cites do not treat
    as line breaks. Several canonical bodies contain them, so a file counted
    with ``splitlines()`` disagreed with its own citations — and the auditor
    reported TEXT MISMATCH against three citations that were correct.
    """

    def test_lines_helper_ignores_unicode_separators(self):
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        import corpus_citation_audit as audit_mod

        import tempfile
        text = "alpha\nbeta still-beta\ngamma\n"
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                         encoding="utf-8") as handle:
            handle.write(text)
            path = Path(handle.name)
        try:
            self.assertEqual(len(text.splitlines()), 4, "precondition: splitlines over-counts")
            lines = audit_mod._lines(path)
            self.assertEqual(lines[1], "beta still-beta")
            self.assertEqual(len([l for l in lines if l]), 3)
        finally:
            path.unlink()


class QuotationTruthTests(unittest.TestCase):
    """The §27 check: a quotation must occur at the line its citation names."""

    def test_no_text_mismatches_in_the_corpus(self):
        report = json.loads(run("--json").stdout)
        mismatches = [f for f in report["findings"] if "TEXT MISMATCH" in f["message"]]
        self.assertEqual(
            mismatches, [],
            "quotations attributed to lines that do not carry them:\n"
            + "\n".join(f"  {f['source']}  {f['message']}" for f in mismatches),
        )

    def test_quotations_are_actually_being_verified(self):
        """Guards against a silent pass from the check never firing."""
        report = json.loads(run("--json").stdout)
        self.assertGreater(
            report["text_verified"], 0,
            "no quotation was verified — the §27 check may have stopped running",
        )


class LedgerTableTests(unittest.TestCase):
    """The cross-column check: quotation and line citation in different cells.

    E-11 was wrong for twenty-six cycles in exactly this shape — a quotation in
    the claim column attributed to a file and line in two other columns, which
    the adjacency check could not pair.
    """

    def test_ledger_quotations_are_checked(self):
        report = json.loads(run("--json").stdout)
        self.assertGreater(
            report["ledger_quotes_checked"], 0,
            "no ledger quotation was paired — the cross-column check may have stopped running",
        )

    def test_no_ledger_text_mismatches(self):
        report = json.loads(run("--json").stdout)
        bad = [f for f in report["findings"] if "LEDGER TEXT MISMATCH" in f["message"]]
        self.assertEqual(
            bad, [],
            "ledger rows whose quotation is absent from the cited range:\n"
            + "\n".join(f"  {f['source']}  {f['citation']}  {f['message']}" for f in bad),
        )

    def test_every_paired_ledger_quotation_verified(self):
        report = json.loads(run("--json").stdout)
        self.assertEqual(report["ledger_quotes_checked"], report["ledger_verified"])

    def test_carry_forward_source_is_resolved(self):
        """`same` in the source column means the previous row's source.

        A parser treating it as a filename would check nothing while reporting
        success — the failure mode this test exists to prevent.
        """
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        import corpus_citation_audit as audit_mod
        ledger = REPO_ROOT / "docs/architecture/platform-organization/EVIDENCE-LEDGER.md"
        rows = list(audit_mod._ledger_rows(ledger))
        self.assertGreater(len(rows), 20)
        for _, ident, _, source, _ in rows:
            if source:
                self.assertNotEqual(
                    source.strip("`* ").lower(), "same",
                    f"{ident}: carry-forward source was not resolved",
                )


class EmphasisNormalizationTests(unittest.TestCase):
    """Quotations are compared as text, not as typography.

    E-44 quotes the Register's "not the semantic authority" as "**not** the
    semantic authority" — emphasis added by the citing document. The substance
    is verbatim. Comparing raw strings reported a true citation as a defect.
    """

    def test_plain_strips_emphasis_markers(self):
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        import corpus_citation_audit as audit_mod
        self.assertEqual(
            audit_mod._plain("**not** the `semantic` _authority_"),
            "not the semantic authority",
        )

    def test_emphasised_quotation_still_verifies(self):
        """The E-44/E-45 case: both must verify, not merely avoid erroring."""
        report = json.loads(run("--json").stdout)
        verified = {f["citation"].split()[0] for f in report["findings"]
                    if "LEDGER TEXT VERIFIED" in f["message"]}
        for ident in ("E-44", "E-45"):
            self.assertIn(ident, verified, f"{ident} quotation is no longer verified")


class UnmarkedHeadingConventionTests(unittest.TestCase):
    """Some frozen bodies write section headings with no ``#`` at all.

    Two citations of ``volume-1/pd-01-executive-office/B3.md §4`` stood as
    WARN — *"section heading not located"* — while the section is plainly
    there: line 96 reads ``4. Capability Ownership Matrix``. The corpus was
    right and the detector was short, which is the direction the Master
    Roadmap `§28` names: **evidence controls the detector, not the reverse.**

    The risk in accepting bare numbered lines is confirming a *list item* as a
    section. That is what these tests exist to prevent, and why the negative
    cases outnumber the positive one.
    """

    def setUp(self):
        sys.path.insert(0, str(REPO_ROOT / "tools"))
        import corpus_citation_audit as audit_mod

        self.mod = audit_mod

    def test_the_real_body_that_produced_the_warning_is_now_located(self):
        body = REPO_ROOT / "docs/architecture/volume-1/pd-01-executive-office/B3.md"
        self.assertTrue(body.is_file(), body)
        self.assertTrue(self.mod._has_section(body, "4"))
        self.assertTrue(self.mod._has_section(body, "11"))

    def test_a_section_the_body_does_not_have_is_still_not_located(self):
        body = REPO_ROOT / "docs/architecture/volume-1/pd-01-executive-office/B3.md"
        self.assertFalse(self.mod._has_section(body, "12"))

    def test_a_list_item_is_not_a_section(self):
        lines = [
            "PD-01 menjalankan:",
            "",
            "1. enterprise leadership",
            "2. Strategic Direction",
            "3. Governance",
            "",
        ]
        # Item 2 looks like a heading in isolation; its neighbours say otherwise.
        self.assertFalse(self.mod._has_bare_heading(lines, "2"))

    def test_a_sentence_is_not_a_section(self):
        lines = ["", "4. Capability ownership is defined here.", ""]
        self.assertFalse(self.mod._has_bare_heading(lines, "4"))

    def test_a_lowercase_continuation_is_not_a_section(self):
        lines = ["", "4. capability ownership matrix", ""]
        self.assertFalse(self.mod._has_bare_heading(lines, "4"))

    def test_the_accepted_form_is_the_one_the_corpus_actually_uses(self):
        lines = ["", "4. Capability Ownership Matrix", ""]
        self.assertTrue(self.mod._has_bare_heading(lines, "4"))
        self.assertFalse(self.mod._has_bare_heading(lines, "5"))

    def test_the_derived_corpus_reports_no_warnings(self):
        """The two standing WARNs were the only ones in the derived corpus.

        **Narrowed 2026-09-09** (`ACT §5.1`). This asserted zero warnings over
        *all* default roots until `docs/governance` was added, which brought 45
        ambiguous-basename WARNs with it. Those are **correct** findings — `§5.3`
        of that Act states a basename match alone is insufficient evidence, and
        WARN means *could not confirm*, not *is wrong*. Widening a root must not
        be paid for by weakening what the original roots promise, so the
        assertion is kept and scoped to the roots it was written about.
        """
        proc = run("docs/architecture/platform-organization",
                   "docs/architecture/candidates", "--json")
        report = json.loads(proc.stdout)
        self.assertEqual(report["warnings"], 0, report["findings"])
        self.assertEqual(report["errors"], 0, report["findings"])

    def test_the_governance_root_is_scanned_and_has_no_errors(self):
        """Regression for the root that was missing (`ACT §5.1`)."""
        self.assertIn("docs/governance", self.mod.DEFAULT_ROOTS)
        proc = run("docs/governance", "--json")
        report = json.loads(proc.stdout)
        self.assertGreater(report["documents_scanned"], 10, report)
        self.assertEqual(report["errors"], 0, report["findings"])

    def test_a_registry_entry_cannot_silence_a_path_that_resolves(self):
        """`ACT §5.4` in code: the registry speaks only after resolution fails.

        `setup.py` and `requirements.txt` are registered as external-corpus
        names. If either ever exists here, it must be checked normally rather
        than waved through — so the registry is consulted **only** on the
        not-found branch.
        """
        import inspect

        source = inspect.getsource(self.mod.audit)
        not_found = source.index("if not targets:")
        self.assertGreater(
            source.index("cited in NON_RESIDENT"), not_found,
            "the registry is consulted before resolution; it could mask a real path",
        )
        self.assertGreater(
            source.index("(rel, cited) in ILLUSTRATIVE"), not_found,
            "ILLUSTRATIVE is consulted before resolution; it could mask a real path",
        )

    def test_the_organization_root_is_audited(self):
        """It was outside the roots until the first P11 construction step.

        `docs/architecture/organization/` holds the P10 Department, Capability
        and Agent Definition records — the evidence the ownership graph is built
        from — and no version of this auditor had ever read them. The blind spot
        was older than the change that exposed it.
        """
        self.assertIn("docs/architecture/organization", self.mod.DEFAULT_ROOTS)

    def test_python_sources_are_scanned_not_only_markdown(self):
        """W2's architectural citations live in docstrings, not documents.

        `DP-01 §3 W2`, `DP-03 §8.4` and `DP-04 §8.2` are cited in
        `tools/planning/` module docstrings and nowhere else in that surface.
        While this auditor read only `*.md`, every one of them was unverifiable —
        a blind spot of exactly the shape it exists to prevent.
        """
        proc = run("tools/planning", "--json")
        report = json.loads(proc.stdout)
        self.assertGreaterEqual(report["documents_scanned"], 5, report)
        self.assertEqual(report["errors"], 0, report["findings"])

    def test_the_w2_planning_surface_is_a_default_root(self):
        self.assertIn("tools/planning", self.mod.DEFAULT_ROOTS)

    def test_a_root_may_name_a_single_file(self):
        """`tools/performance_evidence.py` has no directory of its own.

        Without file roots the choice would be between leaving a materially
        participating module unaudited and adopting all of `tools/`, whose only
        findings are the auditor reading its own documentation.
        """
        self.assertIn("tools/performance_evidence.py", self.mod.DEFAULT_ROOTS)
        proc = run("tools/performance_evidence.py", "--json")
        report = json.loads(proc.stdout)
        self.assertEqual(report["documents_scanned"], 1, report)
        self.assertEqual(report["errors"], 0, report["findings"])

    def test_every_default_root_exists(self):
        """An exclusion naming nothing suppresses silently; so does a root.

        The `NON_DEPARTMENT_DIRS` lesson, applied to roots: a root that resolves
        to nothing scans nothing and reports success, so the surface it was added
        to protect stays unwatched while the metric says it is covered.
        """
        missing = [r for r in self.mod.DEFAULT_ROOTS
                   if not (REPO_ROOT / r).exists()]
        self.assertEqual(missing, [], f"roots naming nothing: {missing}")

    def test_every_illustrative_entry_still_fails_to_resolve(self):
        """A stale exemption is a live citation waved through.

        The lesson is `NON_DEPARTMENT_DIRS`, which carried an entry naming a
        directory that never existed: harmless until something took the name,
        then silently suppressing it. An `ILLUSTRATIVE` entry whose route
        becomes a real file would exempt that file from checking forever, and
        the passing audit would look identical either way.
        """
        for (source_path, cited), reason in self.mod.ILLUSTRATIVE.items():
            with self.subTest(citation=cited):
                self.assertTrue(
                    (REPO_ROOT / source_path).is_file(),
                    f"exemption names a source that does not exist: {source_path}")
                resolved = REPO_ROOT / (REPO_ROOT / source_path).parent.relative_to(
                    REPO_ROOT) / cited
                self.assertFalse(
                    resolved.is_file(),
                    f"{cited} now resolves — it must be checked, not exempted")
                self.assertTrue(reason.strip(), "an exemption must state its reason")


class ScopeGuardTests(unittest.TestCase):
    """Regression for VF-10: the auditor read thirteen protected packages.

    ``docs/program/`` holds untracked protected packages that governance forbids
    this programme to touch. An earlier version of this tool had no scope guard
    and read all thirteen during a directory-wide scan. Nothing was quoted or
    persisted, but a verifier that *can* reach protected paths is a hazard
    regardless of the intent of any particular run.

    The guard is tracked-only scanning, which is also the principled scope: the
    corpus of record is what the repository has committed.
    """

    def _untracked_program_files(self):
        out = subprocess.run(
            ["git", "status", "--porcelain=v1"],
            cwd=str(REPO_ROOT), capture_output=True, text=True,
        ).stdout
        return {
            line[3:] for line in out.splitlines()
            if line.startswith("?? docs/program/")
        }

    def test_protected_untracked_files_are_never_scanned(self):
        protected = self._untracked_program_files()
        if not protected:
            self.skipTest("no untracked docs/program/ files present in this tree")
        report = json.loads(run("--json", "docs/program").stdout)
        touched = {f["source"].split(":")[0] for f in report["findings"]} & protected
        self.assertEqual(
            touched, set(),
            "auditor read protected untracked files:\n"
            + "\n".join(f"  {p}" for p in sorted(touched)),
        )

    def test_no_finding_comes_from_a_protected_untracked_path(self):
        """Narrowed 2026-09-09 (VF-11).

        This previously asserted that every finding came from a *tracked* path.
        That was true only while containment was keyed on tracked status — a
        proxy that failed open on new work, since everything this programme
        writes is untracked until staged. Containment is now keyed on path
        policy, so untracked files outside protected prefixes are legitimately
        scanned. The assertion that matters — nothing is ever read from a
        protected untracked path — is unchanged and still runs.
        """
        tracked = set(subprocess.run(
            ["git", "ls-files", "-z"], cwd=str(REPO_ROOT),
            capture_output=True, text=True,
        ).stdout.split("\0")) - {""}
        report = json.loads(run("--json", "docs/program").stdout)
        for finding in report["findings"]:
            source = finding["source"].split(":")[0]
            if source in tracked:
                continue
            self.assertFalse(
                source.startswith("docs/program/"),
                f"audit read a protected untracked path: {source}",
            )

    def test_untracked_new_work_is_still_scanned(self):
        """Regression for VF-11: the guard must not fail open on new work.

        A verifier that silently ignores newly authored files reports the safety
        of the previous state as though it were the safety of the current one.
        """
        probe = REPO_ROOT / "docs" / "architecture" / "platform-organization" / "ZZ-VF11-PROBE.md"
        probe.write_text(
            "# probe\nBroken: `docs/architecture/NO_SUCH_FILE_vf11.md`\n",
            encoding="utf-8",
        )
        try:
            report = json.loads(run("--json").stdout)
            sources = {f["source"].split(":")[0] for f in report["findings"]}
            self.assertIn(
                "docs/architecture/platform-organization/ZZ-VF11-PROBE.md", sources,
                "an untracked, non-protected new file was not scanned",
            )
        finally:
            probe.unlink(missing_ok=True)
