"""O-A session checks (`AD-FS10-ESC03-R1` `§5`, `§6`): what each phase proves, and what makes it fail."""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import tempfile
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from fullstack.backend.security import AGENT_REGISTER, AUDIT, OBSERVE, RUN_WORKFLOW
from fullstack.deploy import oa_session
from fullstack.tests.support import (OPERATOR_TOKEN, Harness, LiveServer,
                                     operator_authenticator)

REPO_ROOT = Path(__file__).resolve().parents[2]
TOKEN = "test-aios-operator-token-7d1e"
LEAST = {OBSERVE, RUN_WORKFLOW, AUDIT}


class Edge:
    """X2 in front of the application: a host the proxy injects for reaches the
    application; every other host gets the protection redirect."""

    def __init__(self, server: LiveServer, injected=oa_session.T2_HOSTS):
        self.server, self.injected, self.seen = server, set(injected), []

    def __call__(self, request, timeout):
        url = urllib.parse.urlsplit(request.full_url)
        self.seen.append((url.hostname, dict(request.header_items())))
        if url.hostname not in self.injected:
            if "json" in (request.get_header("Accept") or ""):
                raise urllib.error.HTTPError(
                    request.full_url, 401, "Unauthorized", {"Content-Type": "application/json"},
                    io.BytesIO(b'{"message":"Protected by Vercel Authentication"}'))
            raise urllib.error.HTTPError(request.full_url, 302, "Found",
                                         {"Location": "https://vercel.com/sso"}, io.BytesIO(b""))
        target = urllib.request.Request(
            self.server.url + url.path + (("?" + url.query) if url.query else ""),
            data=request.data, headers=dict(request.header_items()), method=request.get_method())
        return urllib.request.urlopen(target, timeout=timeout)


class Base(unittest.TestCase):
    scopes = LEAST

    def setUp(self):
        self.harness = Harness(operator_authenticator({TOKEN: ("aios-operator", self.scopes)}))
        self.server = LiveServer(self.harness)
        self.addCleanup(self.harness.close)
        self.addCleanup(self.server.close)

    def run_phase(self, phase, injected=oa_session.T2_HOSTS, environ=None, **kw):
        self.edge = Edge(self.server, injected)
        return oa_session.run(phase, TOKEN, opener=self.edge, environ=environ or {}, **kw)

    @staticmethod
    def results(record):
        return {r["check"]: r["result"] for r in record["results"]}


class ThePreflight(Base):

    def test_injection_on_the_three_hosts_and_x2_elsewhere_pass(self):
        record = self.run_phase("preflight")
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))

    def test_without_injection_the_session_cannot_start(self):
        record = self.run_phase("preflight", injected=())
        self.assertEqual("FAIL", self.results(record)[
            "injection proven on every T2 host (health 200 through X2)"])
        self.assertFalse(record["ok"])

    def test_a_credential_attached_to_an_unlisted_host_fails(self):
        leaked = oa_session.T2_HOSTS + (oa_session.CONTROL_HOSTS["Preview deployment (dpl_HvyYh…)"],)
        record = self.run_phase("preflight", injected=leaked)
        self.assertEqual("FAIL", self.results(record)["hosts not listed stay behind X2"])

    def test_a_bypass_in_the_process_environment_fails(self):
        record = self.run_phase("preflight", environ={"AIOS_OA_BYPASS": "x"})
        self.assertEqual("FAIL", self.results(record)["no bypass in the process environment"])

    def test_the_client_never_sends_a_bypass_header(self):
        self.run_phase("verify", write=True)
        self.assertTrue(self.edge.seen)
        for _, headers in self.edge.seen:
            self.assertNotIn("x-vercel-protection-bypass", {k.lower() for k in headers})


class TheVerification(Base):

    def test_read_only_verification_passes_and_writes_nothing(self):
        before = len(self.harness.aios.runs())
        record = self.run_phase("verify")
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))
        self.assertEqual(before, len(self.harness.aios.runs()))
        self.assertEqual({oa_session.ALIAS, oa_session.TARGET}, set(record["smoke"]))
        results = self.results(record)
        for host in (oa_session.ALIAS, oa_session.TARGET):
            self.assertEqual("PASS", results[f"{host}: aios.agent.register refused (403)"])
            self.assertEqual("PASS", results[
                f"{host}: audit records the register attempt as refused for aios-operator"])

    def test_the_write_profile_proves_run_trace_and_audit(self):
        before = len(self.harness.aios.runs())
        record = self.run_phase("verify", write=True)
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))
        self.assertEqual(before + 2, len(self.harness.aios.runs()))
        results = self.results(record)
        for check in ("Scenario B: a run succeeds, requested by the principal",
                      "the run is persisted and read back", "the run's own Trace records exist",
                      "audit attributes the run request to the principal (allowed)",
                      "Scenario C: a failure is a meaningful state"):
            self.assertEqual("PASS", results[check], check)

    def test_verification_does_not_run_without_injection(self):
        record = self.run_phase("verify", injected=())
        self.assertFalse(record["ok"])
        self.assertEqual({}, record["smoke"])

    def test_the_evidence_holds_no_credential(self):
        record = self.run_phase("verify", write=True)
        self.assertNotIn(TOKEN, json.dumps(record))


class AWiderPrincipalIsCaught(Base):
    """Least privilege: a principal that may register agents fails verification."""

    scopes = LEAST | {AGENT_REGISTER}

    def test_extra_scope_fails_the_scope_and_refusal_checks(self):
        record = self.run_phase("verify")
        failed = {r["check"] for r in record["results"] if r["result"] == "FAIL"}
        self.assertIn(f"{oa_session.ALIAS}: aios.agent.register refused (403)", failed)
        self.assertIn(f"{oa_session.ALIAS}: principal is aios-operator with exactly its three scopes",
                      failed)
        self.assertFalse(record["ok"])


class TheRevocationCheck(Base):

    def test_x2_back_on_every_host_passes(self):
        record = self.run_phase("revoked", injected=())
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))

    def test_one_host_still_reachable_fails(self):
        record = self.run_phase("revoked", injected=(oa_session.TARGET,))
        self.assertEqual("FAIL", self.results(record)[
            f"{oa_session.TARGET}: X2 back after revocation (anonymous and B3-only stopped by X2)"])
        self.assertFalse(record["ok"])


class WhoAnswered(Base):
    """A 401 is X2's only without the application's X-Request-Id (B3 sets it)."""

    def test_x2_401_and_302_are_the_edge_and_the_apps_401_is_not(self):
        edge = Edge(self.server, injected=(oa_session.ALIAS,))
        through = oa_session._client(oa_session.ALIAS, TOKEN, edge)
        self.assertEqual("app 401", oa_session._reach(through, "/api/v1/session"))
        self.assertFalse(oa_session._x2("app 401"))
        blocked = oa_session._client(oa_session.TARGET, TOKEN, edge)
        self.assertEqual("x2 401", oa_session._reach(blocked))
        self.assertTrue(oa_session._x2("x2 302"))


class TheCommandLine(Base):

    def test_the_cli_reads_the_token_from_a_file_and_prints_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            token_file = Path(tmp, "token")
            token_file.write_text(TOKEN + "\n", encoding="utf-8")
            out = io.StringIO()
            original = oa_session._open
            oa_session._open = Edge(self.server, ())
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                    code = oa_session.main(["revoked", "--token-file", str(token_file),
                                            "--out", str(Path(tmp, "e.json"))])
            finally:
                oa_session._open = original
            self.assertEqual(0, code)
            self.assertNotIn(TOKEN, out.getvalue())
            self.assertNotIn(TOKEN, Path(tmp, "e.json").read_text(encoding="utf-8"))

    def test_write_is_refused_outside_verify(self):
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            oa_session.main(["preflight", "--token-file", "x", "--write"])


class TheHostsAreTheDecidedOnes(unittest.TestCase):

    def test_the_t2_hosts_match_the_decision_and_the_current_authority(self):
        adr = (REPO_ROOT / "docs/fullstack/AD-FS10-ESC03-R1-OPERATIONAL-EDGE-ACCESS-SELECTION.md"
               ).read_text(encoding="utf-8")
        current = json.loads((REPO_ROOT / "docs/fullstack/FS-10-CURRENT-AUTHORITY.json"
                              ).read_text(encoding="utf-8"))["rollback_target"]
        self.assertEqual(current["serving"]["url"], oa_session.SERVING)
        self.assertEqual(current["designated"]["url"], oa_session.TARGET)
        for host in (oa_session.ALIAS, "aios-platform-72l8flelz", "aios-platform-9dhc3bfal"):
            self.assertIn(host, adr)
        self.assertFalse(set(oa_session.CONTROL_HOSTS.values()) & set(oa_session.T2_HOSTS))

    def test_the_only_bypass_input_is_a_named_variable_and_there_is_no_deploy_path(self):
        source = (REPO_ROOT / "fullstack/deploy/oa_session.py").read_text(encoding="utf-8")
        self.assertEqual(["--bypass-env"], sorted(set(re.findall(r"--bypass[\w-]*", source))))
        self.assertNotIn("--bypass-file", source)
        self.assertNotRegex(source, r"(?i)request_rollback|promote|/v\d+/deployments|release\(")


SECRET = "m1-test-bypass-value-5c2e9a"


class M1Edge:
    """X2 as Vercel applies it: a request carrying the valid bypass reaches the
    application on any deployment; anything else gets the protection 401 (JSON)."""

    def __init__(self, server: LiveServer, valid=SECRET, injected=()):
        self.server, self.valid, self.injected, self.seen = server, valid, set(injected), []

    def __call__(self, request, timeout):
        url = urllib.parse.urlsplit(request.full_url)
        headers = {k.lower(): v for k, v in request.header_items()}
        if url.hostname in self.injected:          # a proxy credential as well (must not be)
            headers["x-vercel-protection-bypass"] = self.valid
        self.seen.append((url.hostname, headers))
        if self.valid is None or headers.get("x-vercel-protection-bypass") != self.valid:
            raise urllib.error.HTTPError(
                request.full_url, 401, "Unauthorized", {"Content-Type": "application/json"},
                io.BytesIO(b'{"message":"Protected by Vercel Authentication"}'))
        target = urllib.request.Request(
            self.server.url + url.path + (("?" + url.query) if url.query else ""),
            data=request.data, headers={k: v for k, v in request.header_items()},
            method=request.get_method())
        return urllib.request.urlopen(target, timeout=timeout)


class TheM1Path(Base):

    def run_m1(self, phase, edge=None, environ=None, **kw):
        self.edge = edge or M1Edge(self.server)
        return oa_session.run(phase, TOKEN, opener=self.edge, bypass=SECRET,
                              m1_variable="AIOS_OA_BYPASS",
                              environ={"AIOS_OA_BYPASS": SECRET} if environ is None else environ,
                              **kw)

    def test_preflight_proves_both_layers_independently(self):
        record = self.run_m1("preflight")
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))
        names = {r["check"] for r in record["results"]}
        for host in (oa_session.ALIAS, oa_session.TARGET):
            self.assertIn(f"{host}: T3 M1 without a B3 bearer is refused by the application (401)", names)
            self.assertIn(f"{host}: T5 M1 with an invalid B3 bearer is refused by the application (401)", names)
        self.assertEqual("M1", record["mechanism"])

    def test_the_bypass_is_never_sent_outside_the_t2_hosts(self):
        self.run_m1("verify", write=True)
        for host, headers in self.edge.seen:
            if host not in oa_session.T2_HOSTS:
                self.assertNotIn("x-vercel-protection-bypass", headers)
        self.assertTrue(any(h not in oa_session.T2_HOSTS for h, _ in self.edge.seen))

    def test_verify_with_write_passes_and_holds_no_credential(self):
        before = len(self.harness.aios.runs())
        record = self.run_m1("verify", write=True)
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))
        self.assertEqual(before + 2, len(self.harness.aios.runs()))
        blob = json.dumps(record)
        self.assertNotIn(SECRET, blob)
        self.assertNotIn(TOKEN, blob)

    def test_a_second_mechanism_attaching_the_bypass_is_caught(self):
        record = self.run_m1("preflight", edge=M1Edge(self.server, injected=oa_session.T2_HOSTS))
        failed = {r["check"] for r in record["results"] if r["result"] == "FAIL"}
        self.assertTrue(any(c.startswith("T4 ") for c in failed))

    def test_a_wrong_bypass_does_not_reach_the_application(self):
        record = self.run_m1("preflight", edge=M1Edge(self.server, valid="another-value"))
        self.assertFalse(record["ok"])
        self.assertEqual({}, record["smoke"])

    def test_other_bypass_variables_fail_the_custody_check(self):
        record = self.run_m1("preflight", environ={"AIOS_OA_BYPASS": SECRET, "OTHER_BYPASS": "x"})
        self.assertEqual("FAIL", self.results(record)[
            "M1: only the designated variable holds a bypass (names only)"])

    def test_after_revocation_x2_stops_the_revoked_bypass(self):
        record = self.run_m1("revoked", edge=M1Edge(self.server, valid=None))
        self.assertTrue(record["ok"], json.dumps(record["results"], indent=1))

    def test_the_cli_reads_the_bypass_from_the_named_variable_and_prints_neither(self):
        with tempfile.TemporaryDirectory() as tmp:
            token_file = Path(tmp, "token")
            token_file.write_text(TOKEN + "\n", encoding="utf-8")
            original, out = oa_session._open, io.StringIO()
            oa_session._open = M1Edge(self.server, valid=None)
            os.environ["AIOS_OA_BYPASS_TEST"] = SECRET
            try:
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                    code = oa_session.main(["revoked", "--token-file", str(token_file),
                                            "--bypass-env", "AIOS_OA_BYPASS_TEST",
                                            "--out", str(Path(tmp, "e.json"))])
            finally:
                oa_session._open = original
                del os.environ["AIOS_OA_BYPASS_TEST"]
            self.assertEqual(0, code)
            for text in (out.getvalue(), Path(tmp, "e.json").read_text(encoding="utf-8")):
                self.assertNotIn(SECRET, text)
                self.assertNotIn(TOKEN, text)

    def test_an_unset_variable_aborts(self):
        os.environ.pop("AIOS_OA_BYPASS_UNSET", None)
        with tempfile.TemporaryDirectory() as tmp:
            token_file = Path(tmp, "token")
            token_file.write_text(TOKEN, encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(2, oa_session.main(["preflight", "--token-file", str(token_file),
                                                     "--bypass-env", "AIOS_OA_BYPASS_UNSET"]))
