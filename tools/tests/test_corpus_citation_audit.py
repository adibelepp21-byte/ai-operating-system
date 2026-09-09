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
