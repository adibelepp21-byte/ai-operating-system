"""FS-DP-06 L1 / M1 / R2 (ACT-004 DG-02; Register `§93`).

Logging (L1) is one structured line per request; metrics (M1) are derived from
those lines; readiness (R2) keeps its implicit meaning in the deployed
composition. Trace and Audit stay as they are: telemetry is a third, separate
record, and never carries a credential, a body or a raw path. Alerting is not
decided (Register `§91`, `§92`) and is not tested here as if it were.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from fullstack.backend import telemetry
from fullstack.backend.security import AuditLedger, token_sha256
from fullstack.backend.supabase_storage import SupabaseStorage
from fullstack.deploy import request_metrics as metrics, vercel
from fullstack.tests.support import OBSERVER_TOKEN, OPERATOR_TOKEN, Harness
from fullstack.tests.test_deployment import KEY, URL, FakePostgREST

DOC = "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md"
RUN = {"workflow": "document-conformance-review",
       "inputs": {"document": DOC, "criteria": ["INV-4 secret-criterion-text"]}}


class OneLinePerRequest(unittest.TestCase):

    def setUp(self):
        self.h = Harness()
        self.addCleanup(self.h.close)

    def lines(self):
        return self.h.telemetry.records()

    def test_every_request_yields_exactly_one_line(self):
        calls = [("GET", "/api/v1/health", None), ("GET", "/api/v1/runs", OPERATOR_TOKEN),
                 ("GET", "/api/v1/runs", None), ("POST", "/api/v1/runs", OBSERVER_TOKEN),
                 ("GET", "/api/v1/nowhere", OPERATOR_TOKEN), ("DELETE", "/api/v1/runs", None),
                 ("GET", "/", None)]
        for n, (method, path, token) in enumerate(calls, 1):
            self.h.call(method, path, token, body=RUN if method == "POST" else None)
            self.assertEqual(n, len(self.lines()), path)
        self.assertEqual([200, 200, 401, 403, 404, 405, 200],
                         [r["status"] for r in self.lines()])

    def test_the_line_has_exactly_the_documented_fields(self):
        self.h.call("GET", "/api/v1/health")
        record = self.lines()[0]
        self.assertEqual(set(telemetry.FIELDS), set(record))
        self.assertEqual(telemetry.FORMAT, record["format"])
        self.assertEqual(self.h.aios.runtime_id, record["runtime_id"])
        self.assertGreaterEqual(record["latency_ms"], 0)

    def test_the_route_template_is_logged_never_the_raw_path(self):
        status, _, run = self.h.call("POST", "/api/v1/runs", OPERATOR_TOKEN, body=RUN)
        self.assertEqual(201, status)
        self.h.call("GET", f"/api/v1/runs/{run['run_id']}", OPERATOR_TOKEN)
        self.h.call("GET", "/api/v1/traces?offset=0&limit=5", OPERATOR_TOKEN)
        routes = [r["route"] for r in self.lines()]
        self.assertEqual(["/api/v1/runs", "/api/v1/runs/{run_id}", "/api/v1/traces"], routes)
        self.assertNotIn(run["run_id"], "\n".join(self.h.telemetry.lines))
        self.assertNotIn("limit=5", "\n".join(self.h.telemetry.lines))

    def test_no_credential_body_or_content_reaches_a_line(self):
        self.h.call("POST", "/api/v1/runs", OPERATOR_TOKEN, body=RUN)
        self.h.call("GET", "/api/v1/runs", authorization="Bearer not-a-real-token-77")
        self.h.call("GET", "/api/v1/session", OBSERVER_TOKEN)
        text = "\n".join(self.h.telemetry.lines)
        for secret in (OPERATOR_TOKEN, OBSERVER_TOKEN, token_sha256(OPERATOR_TOKEN),
                       token_sha256(OBSERVER_TOKEN), "not-a-real-token-77", "Bearer",
                       "secret-criterion-text", DOC, "INV-4", "operator@test",
                       "observer@test"):
            self.assertNotIn(secret, text)

    def test_request_id_joins_the_response_the_line_and_the_audit(self):
        status, headers, _ = self.h.call("GET", "/api/v1/runs", OPERATOR_TOKEN)
        line = self.lines()[-1]
        audit = list(AuditLedger(self.h.aios.storage).entries())[-1]
        self.assertEqual(headers["X-Request-Id"], line["request_id"])
        self.assertEqual(headers["X-Request-Id"], audit["request_id"])

    def test_a_failing_sink_never_changes_the_response(self):
        def broken(_):
            raise RuntimeError("log pipe closed")
        h = Harness(telemetry_sink=broken)
        self.addCleanup(h.close)
        self.assertEqual(200, h.call("GET", "/api/v1/runs", OPERATOR_TOKEN)[0])


class TheFiveRecordsStaySeparate(unittest.TestCase):
    """Telemetry adds nothing to Trace or Audit, and neither feeds telemetry."""

    def exercise(self, sink):
        h = Harness(telemetry_sink=sink)
        self.addCleanup(h.close)
        h.call("POST", "/api/v1/runs", OPERATOR_TOKEN, body=RUN)
        h.call("GET", "/api/v1/runs", None)
        h.call("GET", "/api/v1/audit", OPERATOR_TOKEN)
        traces = h.aios.traces(0, 1000)["records"]
        audit = list(AuditLedger(h.aios.storage).entries())
        stored = {p: len(list(h.aios.storage.read(p))) for p in h.aios.storage.partitions()}
        return traces, audit, stored

    def test_logging_changes_neither_trace_nor_audit_nor_the_store(self):
        collector = telemetry.Collector()
        with_log = self.exercise(collector)
        without_log = self.exercise(None)
        self.assertEqual(len(with_log[0]), len(without_log[0]))
        self.assertEqual(len(with_log[1]), len(without_log[1]))
        self.assertEqual(with_log[2], without_log[2])
        self.assertEqual(3, len(collector.lines))
        self.assertNotIn("fullstack-telemetry", with_log[2])
        stored = json.dumps([t for t in with_log[0]])
        self.assertNotIn(telemetry.FORMAT, stored)


class DeployedCompositionLogsEveryRequest(unittest.TestCase):
    """The Vercel adapter: refusals before the Application are logged too."""

    def test_refused_and_served_requests_each_log_once(self):
        fake = FakePostgREST()
        log = telemetry.Collector()
        app = vercel.make_app(storage_factory=lambda: SupabaseStorage(URL, KEY, transport=fake),
                              authenticator=vercel.OperatorTokenAuthenticator.from_configuration("[]"),
                              telemetry_sink=log)
        none = vercel.make_app(storage_factory=lambda: None,
                               authenticator=vercel.NoAuthenticator(), telemetry_sink=log)
        from fullstack.tests.test_deployment import call
        self.assertEqual(200, call(app, "GET", "/api/v1/health")[0])
        self.assertEqual(401, call(app, "GET", "/api/v1/runs")[0])
        self.assertEqual(503, call(none, "GET", "/api/v1/runs")[0])
        self.assertEqual(404, call(app, "GET", "/")[0])
        records = log.records()
        self.assertEqual([200, 401, 503, 404], [r["status"] for r in records])
        self.assertEqual([True, True, False, False], [r["runtime_id"] is not None for r in records])
        self.assertEqual("/api/v1/runs", records[2]["route"])
        self.assertNotIn(KEY, "\n".join(log.lines))


class ReadinessKeepsItsImplicitMeaning(unittest.TestCase):
    """R2: in the deployed composition, `/api/v1/health` = 200 only after a
    Runtime started on the store; with the store unreachable it is 503."""

    def test_health_200_implies_the_store_answered(self):
        from fullstack.tests.test_deployment import call
        fake = FakePostgREST()
        app = vercel.make_app(storage_factory=lambda: SupabaseStorage(URL, KEY, transport=fake),
                              authenticator=vercel.NoAuthenticator(), telemetry_sink=None)
        status, _, body = call(app, "GET", "/api/v1/health")
        self.assertEqual((200, "ok", "running"), (status, body["status"], body["runtime_state"]))
        self.assertTrue(fake.calls, "the store was reached before health answered")
        fake.down = True
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(503, call(app, "GET", "/api/v1/health")[0])


class MetricsAreDerivedFromTheLines(unittest.TestCase):

    def test_totals_routes_and_latency(self):
        h = Harness()
        self.addCleanup(h.close)
        for _ in range(3):
            h.call("GET", "/api/v1/runs", OPERATOR_TOKEN)
        h.call("GET", "/api/v1/runs", None)
        h.call("POST", "/api/v1/runs", OPERATOR_TOKEN, body=RUN)
        noise = ["START RequestId: abc", "Traceback (most recent call last):", "{not json",
                 '{"format":"other/1"}']
        derived = metrics.derive(noise + h.telemetry.lines)
        self.assertEqual((9, 4), (derived["lines_read"], derived["ignored"]))
        self.assertEqual(5, derived["total"]["requests"])
        self.assertEqual({"2xx": 4, "4xx": 1}, derived["total"]["status_classes"])
        self.assertEqual(0, derived["total"]["server_errors"])
        self.assertEqual(4, derived["routes"]["GET /api/v1/runs"]["requests"])
        self.assertEqual(1, derived["routes"]["POST /api/v1/runs"]["requests"])
        latency = derived["total"]["latency_ms"]
        self.assertLessEqual(latency["p50"], latency["p95"])
        self.assertLessEqual(latency["p95"], latency["max"])

    def test_host_log_messages_carrying_a_line_are_read(self):
        line = telemetry.line(request_id="r1", method="GET", route="/api/v1/health",
                              status=503, latency_ms=4.5, runtime_id=None)
        derived = metrics.derive([f"2026-09-28T01:00:00Z INFO {line}"])
        self.assertEqual(1, derived["total"]["server_errors"])

    def test_the_operator_command(self):
        from fullstack.backend.__main__ import main
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "log.txt"
            log.write_text(telemetry.line(request_id="r", method="GET", route="/api/v1/runs",
                                          status=200, latency_ms=1, runtime_id="x") + "\n",
                           encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(0, main(["metrics", "--log", str(log)]))
        self.assertEqual(1, json.loads(out.getvalue())["total"]["requests"])


if __name__ == "__main__":
    unittest.main()
