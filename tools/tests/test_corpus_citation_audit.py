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
        """A deliberately cited absent authority is a finding, not a defect."""
        report = json.loads(run("--json").stdout)
        self.assertGreater(report["non_resident"], 0)
        for finding in report["findings"]:
            if finding["severity"] == "INFO":
                self.assertIn("NON-RESIDENT", finding["message"])

    def test_section_misses_are_warnings_not_errors(self):
        """Heading conventions vary; 'unconfirmed' must not be reported as 'wrong'."""
        report = json.loads(run("--json").stdout)
        for finding in report["findings"]:
            if "section heading not located" in finding["message"]:
                self.assertEqual(finding["severity"], "WARN")
                self.assertIn("not disproved", finding["message"])


if __name__ == "__main__":
    unittest.main()
