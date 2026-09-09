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
