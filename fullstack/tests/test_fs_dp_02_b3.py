"""FS-DP-02 B3 — operator bearer tokens (Architect decision, Register `§81`).

Each class names the verification row (`§9` V1–V9) and security property
(`§8` S1–S10) it evidences. The tokens are the obviously fake test tokens of
`support`; the authenticator is the production one, configured with their hashes.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

from fullstack.backend import contract
from fullstack.backend.security import (
    AUDIT, OBSERVE, PUBLIC, RUN_WORKFLOW, AuditLedger, OperatorTokenAuthenticator,
    parse_operator_tokens, OperatorTokenConfigurationError, token_sha256)
from fullstack.tests.support import (
    OBSERVER_TOKEN, OPERATOR_TOKEN, REPO_ROOT, Harness, operator_configuration)
from fullstack.tests.test_backend_api import RUN, run_body

PROTECTED = [r for r in contract.ROUTES if r.scope != PUBLIC]


def _path(template):
    return template.replace("{run_id}", "run-x")


def _body(route):
    return run_body() if route.method == "POST" else None


class _Case(unittest.TestCase):
    def setUp(self):
        self.h = Harness()

    def tearDown(self):
        self.h.close()


class V1MissingCredential(_Case):
    """V1 · S1: no credential, no access, on every protected route."""

    def test_every_protected_route_rejects_a_request_without_a_credential(self):
        for route in PROTECTED:
            with self.subTest(route=f"{route.method} {route.template}"):
                self.assertEqual(401, self.h.call(route.method, _path(route.template),
                                                  None, _body(route))[0])
        self.assertEqual([], self.h.aios.runs())


class V2InvalidCredential(_Case):
    """V2 · S2: a well-formed token that is not configured is nobody."""

    def test_unknown_near_miss_and_hash_as_token_are_rejected(self):
        for token in ("unknown-token-3b7", OPERATOR_TOKEN.upper(), OPERATOR_TOKEN[:-1],
                      OPERATOR_TOKEN + "x", token_sha256(OPERATOR_TOKEN)):
            with self.subTest(token=token[:12]):
                self.assertEqual(401, self.h.call("GET", "/api/v1/runtime", token)[0])
                self.assertEqual(401, self.h.call("POST", RUN, token, run_body())[0])
        self.assertEqual([], self.h.aios.runs())


class V3MalformedCredential(_Case):
    """V3 · S3: anything but `Bearer <b64token>` is rejected, never an error."""

    MALFORMED = ("", "Bearer", "Bearer ", f"Bearer  {OPERATOR_TOKEN}",
                 f"Bearer {OPERATOR_TOKEN} ", f"Bearer {OPERATOR_TOKEN}\n",
                 f"Basic {OPERATOR_TOKEN}", OPERATOR_TOKEN, f"Token {OPERATOR_TOKEN}",
                 f"Bearer {OPERATOR_TOKEN},Bearer {OBSERVER_TOKEN}",
                 f"Bearer {OPERATOR_TOKEN} {OBSERVER_TOKEN}", "Bearer tök",
                 "Bearer " + "a" * 600, "Bearer \x00", "Bearer ===")

    def test_malformed_authorization_headers_are_rejected(self):
        for header in self.MALFORMED:
            with self.subTest(header=repr(header[:30])):
                status, _, body = self.h.call("GET", "/api/v1/runtime", authorization=header)
                self.assertEqual((401, "unauthenticated"), (status, body["error"]))

    def test_the_scheme_is_case_insensitive_as_http_defines_it(self):
        self.assertEqual(200, self.h.call("GET", "/api/v1/runtime",
                                          authorization=f"bearer {OPERATOR_TOKEN}")[0])


class V4ValidCredential(_Case):
    """V4 · S4: a configured token is its principal, with exactly its scopes."""

    def test_a_valid_operator_token_is_accepted_and_audited_by_subject(self):
        status, _, run = self.h.call("POST", RUN, OPERATOR_TOKEN, run_body())
        self.assertEqual((201, "succeeded"), (status, run["state"]))
        self.assertEqual("operator@test", run["requested_by"])
        session = self.h.call("GET", "/api/v1/session", OPERATOR_TOKEN)[2]
        self.assertEqual({"subject": "operator@test",
                          "scopes": sorted([AUDIT, OBSERVE, RUN_WORKFLOW])}, session)
        last = list(AuditLedger(self.h.aios.storage).entries())[-1]
        self.assertEqual(("operator@test", "allowed"), (last["subject"], last["decision"]))

    def test_authorization_is_unchanged_scopes_still_decide(self):
        """`§5`: B3 authenticates; the existing scope rule still authorizes."""
        self.assertEqual(403, self.h.call("POST", RUN, OBSERVER_TOKEN, run_body())[0])
        self.assertEqual(403, self.h.call("GET", "/api/v1/audit", OBSERVER_TOKEN)[0])
        self.assertEqual(200, self.h.call("GET", RUN, OBSERVER_TOKEN)[0])

    def test_an_entry_without_scopes_grants_observe_only(self):
        a = OperatorTokenAuthenticator.from_configuration(json.dumps(
            [{"subject": "reader", "sha256": token_sha256("reader-token-0c1")}]))
        self.assertEqual(frozenset({OBSERVE}),
                         a.authenticate({"authorization": "Bearer reader-token-0c1"}).scopes)


class V5ProtectedRouteEnforcement(_Case):
    """V5 · S6: only liveness is public, and it discloses nothing protected."""

    def test_the_only_public_route_is_health_and_it_says_only_liveness(self):
        self.assertEqual(["/api/v1/health"], [r.template for r in contract.ROUTES
                                              if r.scope == PUBLIC])
        self.assertEqual({"status", "runtime_state"},
                         set(self.h.call("GET", "/api/v1/health")[2]))


class V6NoPlaintextPersistence(unittest.TestCase):
    """V6 · S5: the server side holds hashes; a plaintext token cannot be configured."""

    def test_the_configuration_refuses_anything_but_a_hash(self):
        for value in (
                [{"subject": "a", "token": OPERATOR_TOKEN}],
                [{"subject": "a", "sha256": token_sha256(OPERATOR_TOKEN), "token": OPERATOR_TOKEN}],
                [{"subject": "a", "sha256": OPERATOR_TOKEN}],
                [{"subject": "a", "sha256": token_sha256("x").upper()}],
                [{"subject": "a", "sha256": token_sha256("x"), "password": "p"}]):
            with self.subTest(value=str(value)[:40]):
                with self.assertRaises(OperatorTokenConfigurationError):
                    parse_operator_tokens(json.dumps(value))

    def test_the_authenticator_keeps_hashes_and_principals_only(self):
        a = OperatorTokenAuthenticator.from_configuration(operator_configuration(
            {OPERATOR_TOKEN: ("operator@test", {OBSERVE})}))
        a.authenticate({"authorization": f"Bearer {OPERATOR_TOKEN}"})
        held = repr(vars(a))
        self.assertNotIn(OPERATOR_TOKEN, held)
        self.assertIn(token_sha256(OPERATOR_TOKEN), held)

    def test_nothing_is_written_when_issuing_a_token(self):
        with tempfile.TemporaryDirectory() as cwd:
            done = subprocess.run(
                [sys.executable, "-m", "fullstack.backend", "operator-token",
                 "--subject", "founder", "--scope", OBSERVE, "--scope", RUN_WORKFLOW],
                cwd=cwd, env=dict(os.environ, PYTHONPATH=str(REPO_ROOT)),
                capture_output=True, text=True, timeout=60)
            self.assertEqual(0, done.returncode, done.stderr)
            self.assertEqual([], os.listdir(cwd))
        lines = done.stdout.splitlines()
        token, entry = lines[1], json.loads(lines[3])
        self.assertGreaterEqual(len(token), 43)  # 32 random bytes
        self.assertEqual({"subject": "founder", "sha256": token_sha256(token),
                          "scopes": sorted([OBSERVE, RUN_WORKFLOW])}, entry)
        self.assertEqual("founder", OperatorTokenAuthenticator.from_configuration(
            json.dumps([entry])).authenticate({"authorization": f"Bearer {token}"}).subject)


class V7FailClosed(unittest.TestCase):
    """V7 · S7: an absent or refused configuration authenticates nobody, and a
    refusal never quotes the configuration."""

    BAD = ("", "   ", "not json", "{}", "[1]", '[{"subject": "a"}]',
           json.dumps([{"subject": "", "sha256": token_sha256("x")}]),
           json.dumps([{"subject": "a", "sha256": token_sha256("x"), "scopes": ["aios.all"]}]),
           json.dumps([{"subject": "a", "sha256": token_sha256("x")},
                       {"subject": "b", "sha256": token_sha256("x")}]),
           json.dumps([{"subject": "a", "sha256": token_sha256("x")},
                       {"subject": "a", "sha256": token_sha256("y")}]))

    def test_a_bad_configuration_authenticates_nobody(self):
        for text in self.BAD:
            with self.subTest(text=text[:40]):
                a = OperatorTokenAuthenticator.from_configuration(text)
                self.assertIsNotNone(a.configuration_error)
                for token in ("x", "y", OPERATOR_TOKEN):
                    self.assertIsNone(a.authenticate({"authorization": f"Bearer {token}"}))
                if len(text.strip()) > 5:
                    self.assertNotIn(text, a.configuration_error)

    def test_one_bad_entry_refuses_the_whole_configuration(self):
        good = {"subject": "a", "sha256": token_sha256(OPERATOR_TOKEN)}
        a = OperatorTokenAuthenticator.from_configuration(json.dumps([good, {"subject": "b"}]))
        self.assertIsNone(a.authenticate({"authorization": f"Bearer {OPERATOR_TOKEN}"}))

    def test_rejection_never_reaches_the_protected_handler(self):
        h = Harness(authenticator=OperatorTokenAuthenticator.from_configuration("not json"))
        try:
            self.assertEqual(401, h.call("POST", RUN, OPERATOR_TOKEN, run_body())[0])
            self.assertEqual([], h.aios.runs())
            self.assertEqual(0, sum(1 for _ in h.aios.storage.read("trace")))
        finally:
            h.close()


class V8ConsoleFlow(_Case):
    """V8 · S8: the console's own request shape. The browser end to end
    (`test_integration.ConsoleInABrowser`) runs through this same authenticator."""

    def test_the_console_request_shape_is_accepted(self):
        # fullstack/frontend/api.js sends `Authorization: Bearer <credential>`.
        api_js = (REPO_ROOT / "fullstack/frontend/api.js").read_text(encoding="utf-8")
        self.assertIn("headers.Authorization = `Bearer ${token}`", api_js)
        self.assertEqual(200, self.h.call("GET", "/api/v1/session",
                                          authorization=f"Bearer {OBSERVER_TOKEN}")[0])


class V9NoSideDoor(_Case):
    """V9 · S9: no other header, parameter, method or path grants access."""

    def test_no_alternate_credential_carrier_is_honoured(self):
        for header, value in (("HTTP_X_GATE_PRINCIPAL", "gate-operator"),
                              ("HTTP_X_FORWARDED_USER", "operator@test"),
                              ("HTTP_X_AIOS_TOKEN", OPERATOR_TOKEN),
                              ("HTTP_COOKIE", f"token={OPERATOR_TOKEN}"),
                              ("HTTP_PROXY_AUTHORIZATION", f"Bearer {OPERATOR_TOKEN}")):
            with self.subTest(header=header):
                self.assertEqual(401, self._call_with("GET", "/api/v1/runtime", "",
                                                      {header: value}))
        self.assertEqual(401, self._call_with("GET", "/api/v1/runtime",
                                              f"token={OPERATOR_TOKEN}", {}))
        self.assertEqual(401, self._call_with("GET", "/api/v1/runtime",
                                              f"access_token={OPERATOR_TOKEN}", {}))

    def test_other_methods_and_path_forms_do_not_open_a_route(self):
        for method, path in (("HEAD", "/api/v1/runs"), ("OPTIONS", "/api/v1/runs"),
                             ("PUT", "/api/v1/runs"), ("GET", "/api/v1/runs/"),
                             ("GET", "/api/v1//runs"), ("GET", "/api/v1/RUNS"),
                             ("GET", "/api/v1/health/../runs"), ("GET", "/api/v2/runs")):
            with self.subTest(method=method, path=path):
                self.assertNotEqual(200, self._call_with(method, path, "", {}))
        self.assertEqual([], self.h.aios.runs())

    def _call_with(self, method, path, query, extra):
        from wsgiref.util import setup_testing_defaults
        environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
                   "CONTENT_LENGTH": "0", "wsgi.input": io.BytesIO(b""), **extra}
        setup_testing_defaults(environ)
        seen = {}
        b"".join(self.h.app(environ, lambda s, h: seen.update(status=int(s.split()[0]))))
        return seen["status"]


class S10SecretBoundary(unittest.TestCase):
    """S10 · NC-13 · NC-14: neither a token nor its hash is stored, logged or returned."""

    def test_no_token_or_hash_reaches_storage_responses_or_logs(self):
        err, out = io.StringIO(), io.StringIO()
        h = Harness()
        try:
            seen = []
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
                for token in (OPERATOR_TOKEN, OBSERVER_TOKEN, "wrong-token-77d"):
                    for route in contract.ROUTES:
                        seen.append(str(h.call(route.method, _path(route.template),
                                               token, _body(route))))
            stored = b"".join(p.read_bytes() for p in (h.data_dir / "storage").iterdir())
            for secret in (OPERATOR_TOKEN, OBSERVER_TOKEN, "wrong-token-77d",
                           token_sha256(OPERATOR_TOKEN), token_sha256(OBSERVER_TOKEN)):
                with self.subTest(secret=secret[:12]):
                    self.assertNotIn(secret.encode(), stored)
                    self.assertFalse(any(secret in r for r in seen))
                    self.assertNotIn(secret, err.getvalue() + out.getvalue())
        finally:
            h.close()

    def test_no_real_token_hash_is_committed(self):
        """Only the fake test tokens' hashes may appear, and only computed in tests."""
        tracked = subprocess.run(["git", "ls-files", "fullstack", "api", "vercel.json"],
                                 cwd=str(REPO_ROOT), capture_output=True, text=True).stdout
        import re
        # Built, not written: this file is itself scanned.
        assignment = "AIOS_OPERATOR_TOKENS" + "="
        for name in tracked.split():
            path = REPO_ROOT / name
            if path.suffix not in (".py", ".js", ".json", ".html", ".css", ".mjs"):
                continue
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=name):
                self.assertNotIn(assignment, text)
                self.assertEqual([], re.findall(r'"sha256"\s*:\s*"[0-9a-f]{64}"', text))


if __name__ == "__main__":
    unittest.main()
