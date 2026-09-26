"""FS-06 — security and authority: what is refused, what is recorded, what never leaks.

Authentication itself is Architect-reserved (`FS-DP-02`). What is tested here
is everything that does not depend on that decision: the production posture
(nobody is authenticated), scope authorization, least privilege, fail-closed
behaviour, audit, secret handling, and the Tool's confinement.
"""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from fullstack.backend import contract, docs_tool
from fullstack.backend.security import (
    AUDIT, OBSERVE, PUBLIC, RUN_WORKFLOW, AuditLedger, Authenticator,
    NoAuthenticator, Principal, authorize)
from fullstack.tests.support import (
    OBSERVER_TOKEN, OPERATOR_TOKEN, Harness, TokenAuthenticator)
from fullstack.tests.test_backend_api import RUN, run_body
from native_core.shared import Failure, Success


def _concrete(template):
    return template.replace("{run_id}", "run-00001")


def _each_route(harness, token):
    for route in contract.ROUTES:
        body = run_body() if route.method == "POST" else None
        yield route, harness.call(route.method, _concrete(route.template), token, body)[0]


class ProductionPosture(unittest.TestCase):
    """The shipped composition: `NoAuthenticator`."""

    def test_every_protected_route_answers_401(self):
        h = Harness(authenticator=NoAuthenticator())
        try:
            for route, status in _each_route(h, OPERATOR_TOKEN):
                with self.subTest(route=f"{route.method} {route.template}"):
                    self.assertEqual(200 if route.scope == PUBLIC else 401, status)
            self.assertEqual([], h.aios.runs())
        finally:
            h.close()

    def test_the_runtime_reports_that_no_mechanism_is_ratified(self):
        self.assertIn("FS-DP-02 not ratified", NoAuthenticator.mechanism)


class Authorization(unittest.TestCase):
    def setUp(self):
        self.h = Harness()

    def tearDown(self):
        self.h.close()

    def test_no_credential_or_a_wrong_one_is_nobody(self):
        for token in (None, "wrong", ""):
            with self.subTest(token=token):
                self.assertEqual(401, self.h.call("GET", "/api/v1/runtime", token)[0])

    def test_the_observer_can_read_but_not_act_or_audit(self):
        for route, status in _each_route(self.h, OBSERVER_TOKEN):
            with self.subTest(route=f"{route.method} {route.template}"):
                expected = {PUBLIC: 200, OBSERVE: 200, "authenticated": 200,
                            RUN_WORKFLOW: 403, AUDIT: 403}[route.scope]
                if route.template.endswith("{run_id}"):
                    expected = 404  # allowed, and no such run
                self.assertEqual(expected, status)
        self.assertEqual([], self.h.aios.runs())

    def test_least_privilege_a_run_only_principal_cannot_read(self):
        h = Harness(authenticator=TokenAuthenticator(
            {"runner": Principal("runner@test", {RUN_WORKFLOW})}))
        try:
            self.assertEqual(201, h.call("POST", RUN, "runner", run_body())[0])
            self.assertEqual(403, h.call("GET", RUN, "runner")[0])
            self.assertEqual(403, h.call("GET", "/api/v1/traces", "runner")[0])
        finally:
            h.close()

    def test_a_failing_authenticator_authenticates_nobody(self):
        class Broken(Authenticator):
            def authenticate(self, headers):
                raise RuntimeError("identity provider down")

        h = Harness(authenticator=Broken())
        try:
            self.assertEqual(401, h.call("GET", "/api/v1/runtime", OPERATOR_TOKEN)[0])
        finally:
            h.close()

    def test_the_rule_fails_closed_on_an_unknown_scope(self):
        everyone = Principal("x", {OBSERVE, RUN_WORKFLOW, AUDIT})
        self.assertEqual(403, authorize(everyone, "aios.everything").status)
        with self.assertRaises(ValueError):
            Principal("x", {"aios.everything"})


class Audit(unittest.TestCase):
    def setUp(self):
        self.h = Harness()

    def tearDown(self):
        self.h.close()

    def test_every_decision_is_recorded_allowed_or_refused(self):
        self.h.call("GET", "/api/v1/health")
        self.h.call("GET", "/api/v1/runtime")
        self.h.call("POST", RUN, OBSERVER_TOKEN, run_body())
        self.h.call("POST", RUN, OPERATOR_TOKEN, run_body())
        entries = list(AuditLedger(self.h.aios.storage).entries())
        self.assertEqual([(None, "GET", "refused", 401),
                          ("observer@test", "POST", "refused", 403),
                          ("operator@test", "POST", "allowed", 200)],
                         [(e["subject"], e["method"], e["decision"], e["status"])
                          for e in entries])
        self.assertEqual(set(AuditLedger.FIELDS) | {"position"}, set(entries[0]))

    def test_the_audit_route_needs_its_own_scope(self):
        self.assertEqual(403, self.h.call("GET", "/api/v1/audit", OBSERVER_TOKEN)[0])
        status, _, body = self.h.call("GET", "/api/v1/audit", OPERATOR_TOKEN)
        self.assertEqual(200, status)
        self.assertEqual("aios.audit", body["entries"][-1]["scope"])


class Secrets(unittest.TestCase):
    """NC-10: no credential in source-of-record, responses or storage."""

    def test_no_credential_reaches_any_record_or_response(self):
        h = Harness()
        try:
            seen = []
            for token in (OPERATOR_TOKEN, OBSERVER_TOKEN, "not-a-token-5e1"):
                for route in contract.ROUTES:
                    body = run_body() if route.method == "POST" else None
                    seen.append(str(h.call(route.method, _concrete(route.template),
                                           token, body)))
            stored = b"".join(p.read_bytes() for p in (h.data_dir / "storage").iterdir())
            for secret in (OPERATOR_TOKEN, OBSERVER_TOKEN, "not-a-token-5e1"):
                with self.subTest(secret=secret):
                    self.assertNotIn(secret.encode(), stored)
                    self.assertFalse(any(secret in response for response in seen))
        finally:
            h.close()

    def test_no_credential_is_committed_to_the_application(self):
        root = Path(__file__).resolve().parents[1]
        shipped = [p for p in root.rglob("*") if p.is_file() and "tests" not in p.parts
                   and "__pycache__" not in p.parts]
        for path in shipped:
            with self.subTest(path=path.name):
                self.assertNotIn("test-operator-token", path.read_text(encoding="utf-8"))

    def test_api_responses_carry_the_security_headers(self):
        h = Harness()
        try:
            _, headers, _ = h.call("GET", "/api/v1/health")
        finally:
            h.close()
        self.assertEqual("nosniff", headers["X-Content-Type-Options"])
        self.assertEqual("no-store", headers["Cache-Control"])
        self.assertEqual("DENY", headers["X-Frame-Options"])
        self.assertEqual("no-referrer", headers["Referrer-Policy"])
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])


class ToolConfinement(unittest.TestCase):
    """The only external access is `docs.read`, and it reads only `docs/`."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "docs").mkdir()
        (self.root / "docs" / "ok.md").write_text("INV-4\n", encoding="utf-8")
        (self.root / "secret.md").write_text("outside\n", encoding="utf-8")
        self.tool = docs_tool.DocsReadTool(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def read(self, path):
        return self.tool.invoke("read", {"path": path})

    def test_a_document_under_docs_is_read(self):
        outcome = self.read("docs/ok.md")
        self.assertIsInstance(outcome, Success)
        self.assertEqual(("INV-4",), outcome.value["lines"])

    def test_everything_else_is_refused(self):
        (self.root / "docs" / "big.md").write_bytes(b"x" * (docs_tool.MAX_BYTES + 1))
        (self.root / "docs" / "latin1.md").write_bytes(b"\xff\xfe")
        os.symlink(self.root / "secret.md", self.root / "docs" / "link.md")
        for path in ("docs/../secret.md", "secret.md", "/etc/passwd", "docs/.hidden.md",
                     "docs/ok.py", "docs\\ok.md", "docs/absent.md", "docs/big.md",
                     "docs/latin1.md", "docs/link.md", "", None, 3):
            with self.subTest(path=path):
                self.assertIsInstance(self.read(path), Failure)

    def test_it_has_one_action(self):
        self.assertIsInstance(self.tool.invoke("write", {"path": "docs/ok.md"}), Failure)
        self.assertEqual(("read",), docs_tool.CONTRACT.actions)

    def test_a_traversal_through_the_api_fails_the_run_not_the_boundary(self):
        h = Harness()
        try:
            run = h.call("POST", RUN, OPERATOR_TOKEN, run_body(document="docs/../README.md"))[2]
        finally:
            h.close()
        self.assertEqual("failed", run["state"])
        self.assertEqual("execution_failure", run["steps"][0]["disposition"])

    def test_no_route_invokes_a_tool_directly(self):
        """Tools are reached only by Workflow steps, through governance."""
        self.assertFalse([r for r in contract.ROUTES
                          if r.method != "GET" and "tool" in r.template])


if __name__ == "__main__":
    unittest.main()
