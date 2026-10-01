"""FS-10 smoke tool: what it checks, what it never does by default."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from fullstack.deploy import smoke
from fullstack.tests.support import OBSERVER_TOKEN, OPERATOR_TOKEN, Harness, LiveServer


class TheSmokeProfiles(unittest.TestCase):

    def setUp(self):
        self.harness = Harness()
        self.server = LiveServer(self.harness)
        self.addCleanup(self.harness.close)
        self.addCleanup(self.server.close)

    def runs(self):
        return len(self.harness.aios.runs())

    def test_the_read_only_profile_passes_and_writes_nothing(self):
        before = self.runs()
        record = smoke.run(smoke.Client(self.server.url, OPERATOR_TOKEN))
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))
        self.assertEqual("read-only", record["profile"])
        self.assertFalse(record["writes_made"])
        self.assertEqual(before, self.runs())
        self.assertFalse([r for r in record["results"] if r["mutates"]])

    def test_the_write_profile_adds_scenarios_b_and_c(self):
        before = self.runs()
        record = smoke.run(smoke.Client(self.server.url, OPERATOR_TOKEN), write=True)
        names = {r["check"]: r for r in record["results"]}
        self.assertEqual("PASS", names["Scenario B: a run succeeds"]["result"])
        self.assertEqual("PASS", names["Scenario C: a failure is a meaningful state"]["result"])
        self.assertTrue(names["Scenario B: a run succeeds"]["mutates"])
        self.assertEqual(before + 2, self.runs())

    def test_a_wrong_token_fails_the_authentication_checks(self):
        record = smoke.run(smoke.Client(self.server.url, "not-the-operator-token"))
        failed = {r["check"] for r in record["results"] if r["result"] == "FAIL"}
        self.assertIn("valid bearer authenticates", failed)
        self.assertFalse(record["ok"])

    def test_an_observer_token_authenticates_but_cannot_be_used_for_the_write_profile(self):
        record = smoke.run(smoke.Client(self.server.url, OBSERVER_TOKEN), write=True)
        names = {r["check"]: r["result"] for r in record["results"]}
        self.assertEqual("FAIL", names["Scenario B: a run succeeds"])

    def test_the_evidence_holds_no_credential(self):
        record = smoke.run(smoke.Client(self.server.url, OPERATOR_TOKEN, bypass="b" * 32), write=True)
        blob = json.dumps(record)
        self.assertNotIn(OPERATOR_TOKEN, blob)
        self.assertNotIn("b" * 32, blob)


class TheSafetyRules(unittest.TestCase):

    def test_a_response_that_echoes_the_token_aborts_the_run(self):
        class Echo:
            status = 200
            headers = {}
            def __init__(self, token): self.token = token
            def read(self): return json.dumps({"status": "ok", "leak": self.token}).encode()
            def __enter__(self): return self
            def __exit__(self, *a): return False
        client = smoke.Client("http://x.invalid", "secret-token-value", opener=lambda req, timeout: Echo("secret-token-value"))
        with self.assertRaises(smoke.SecretEchoed):
            smoke.run(client)

    def test_the_cli_reads_secrets_from_files_and_prints_none(self):
        harness = Harness()
        server = LiveServer(harness)
        self.addCleanup(harness.close)
        self.addCleanup(server.close)
        with tempfile.TemporaryDirectory() as tmp:
            token = Path(tmp) / "token"
            token.write_text(OPERATOR_TOKEN + "\n", encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = smoke.main(["--base", server.url, "--token-file", str(token), "--out", str(Path(tmp) / "e.json")])
            self.assertIn(code, (0, 1))
            self.assertNotIn(OPERATOR_TOKEN, out.getvalue() + err.getvalue())
            self.assertEqual("read-only", json.loads((Path(tmp) / "e.json").read_text())["profile"])

    def test_the_write_profile_announces_its_target(self):
        harness = Harness()
        server = LiveServer(harness)
        self.addCleanup(harness.close)
        self.addCleanup(server.close)
        with tempfile.TemporaryDirectory() as tmp:
            token = Path(tmp) / "token"
            token.write_text(OPERATOR_TOKEN, encoding="utf-8")
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                smoke.main(["--base", server.url, "--token-file", str(token), "--write"])
            self.assertIn(f"WRITE profile against {server.url}", err.getvalue())


if __name__ == "__main__":
    unittest.main()


class TheBypassFromTheEnvironment(unittest.TestCase):
    """FDP-012 O-A delivery fallback: the bypass may come from a named variable, never printed."""

    def setUp(self):
        self.harness = Harness()
        self.server = LiveServer(self.harness)
        self.addCleanup(self.harness.close)
        self.addCleanup(self.server.close)
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.token_file = Path(folder.name) / "token"
        self.token_file.write_text(OPERATOR_TOKEN, encoding="utf-8")

    def _main(self, *extra, env=None):
        import os
        out, err = io.StringIO(), io.StringIO()
        saved = dict(os.environ)
        os.environ.update(env or {})
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = smoke.main(["--base", self.server.url, "--token-file", str(self.token_file), *extra])
        finally:
            os.environ.clear()
            os.environ.update(saved)
        return code, out.getvalue() + err.getvalue()

    def test_a_named_variable_is_used_and_never_printed(self):
        value = "e" * 32
        code, printed = self._main("--bypass-env", "AIOS_TEST_BYPASS", env={"AIOS_TEST_BYPASS": value})
        self.assertEqual(0, code, printed)
        self.assertNotIn(value, printed)
        self.assertNotIn(OPERATOR_TOKEN, printed)

    def test_an_unset_variable_aborts_before_any_request(self):
        code, printed = self._main("--bypass-env", "AIOS_TEST_BYPASS_UNSET")
        self.assertEqual(2, code)
        self.assertIn("is not set", printed)

    def test_file_and_variable_cannot_both_be_given(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            smoke.main(["--base", self.server.url, "--token-file", str(self.token_file),
                        "--bypass-file", str(self.token_file), "--bypass-env", "X"])
