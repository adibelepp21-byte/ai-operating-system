"""FS-03 — the backend: every route of API contract v1, run end to end in-process.

Each run here is a real AIOS execution: a RUNNING Runtime, an Execution it
minted, a Workflow driven through its lifecycle by the Workflow-participating
Agent, a Tool reached only through governance, and one durable Trace per
Agent-Instance action.
"""

from __future__ import annotations

import unittest
from unittest import mock

from fullstack.backend import contract
from fullstack.tests.support import OBSERVER_TOKEN, OPERATOR_TOKEN, Harness

DOC = "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md"
RUN = "/api/v1/runs"


def run_body(document=DOC, criteria=("INV-4", "Architect Reserved")):
    return {"workflow": "document-conformance-review",
            "inputs": {"document": document, "criteria": list(criteria)}}


class _Case(unittest.TestCase):
    def setUp(self):
        self.h = Harness()

    def tearDown(self):
        self.h.close()

    def call(self, *args, **kwargs):
        return self.h.call(*args, **kwargs)


class Health(_Case):
    def test_health_is_public_and_says_nothing_else(self):
        status, _, body = self.call("GET", "/api/v1/health")
        self.assertEqual((200, {"status": "ok", "runtime_state": "running"}), (status, body))

    def test_health_reports_a_stopped_runtime(self):
        self.h.aios.stop()
        self.assertEqual("unavailable", self.call("GET", "/api/v1/health")[2]["status"])


class Reads(_Case):
    def test_runtime_status(self):
        status, _, body = self.call("GET", "/api/v1/runtime", OBSERVER_TOKEN)
        self.assertEqual(200, status)
        self.assertEqual("running", body["state"])
        self.assertTrue(body["runtime_id"].startswith("aios-fullstack/"))
        self.assertEqual({"knowledge": True, "memory": True, "tools": True,
                          "workflows": True}, body["hosted"])

    def test_the_one_tool_is_registered_and_enabled(self):
        tools = self.call("GET", "/api/v1/tools", OBSERVER_TOKEN)[2]["tools"]
        self.assertEqual([("docs.read", "1", "enabled", True, ["read"])],
                         [(t["key"], t["version"], t["state"], t["invocable"], t["actions"])
                          for t in tools])

    def test_the_catalog(self):
        workflows = self.call("GET", "/api/v1/workflows", OBSERVER_TOKEN)[2]["workflows"]
        self.assertEqual(["document-conformance-review"], [w["key"] for w in workflows])
        self.assertEqual(["read-document", "verify-criteria"],
                         [s["step_key"] for s in workflows[0]["steps"]])

    def test_session_names_the_principal(self):
        body = self.call("GET", "/api/v1/session", OBSERVER_TOKEN)[2]
        self.assertEqual({"subject": "observer@test", "scopes": ["aios.observe"]}, body)


class Runs(_Case):
    def test_a_conformant_run(self):
        status, _, run = self.call("POST", RUN, OPERATOR_TOKEN, run_body())
        self.assertEqual(201, status)
        self.assertEqual(("run-00001", "succeeded", True),
                         (run["run_id"], run["state"], run["succeeded"]))
        self.assertEqual(["defined", "ready", "running", "succeeded"], run["states"])
        self.assertEqual(["completed", "completed"], [s["status"] for s in run["steps"]])
        self.assertEqual({"conformant": True, "satisfied": 2, "total": 2}, run["outcome"])
        self.assertEqual("operator@test", run["requested_by"])

    def test_every_acting_agent_wrote_exactly_one_trace(self):
        run = self.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        self.assertEqual(3, run["trace"]["count"])
        page = self.call("GET", f"/api/v1/traces?offset={run['trace']['from']}&limit=3",
                         OBSERVER_TOKEN)[2]
        self.assertEqual(["tool-proposing-agent", "engineering-intelligence-agent",
                          "workflow-participating-agent"],
                         [r["agent_instance"] for r in page["records"]])
        self.assertEqual({run["runtime_id"]}, {r["runtime"] for r in page["records"]})
        self.assertEqual(["docs.read"], page["records"][0]["tools_used"])

    def test_the_step_actors_are_the_trace_authors(self):
        """The Workflow names who acts; Trace shows the same Agent Instances."""
        run = self.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        page = self.call("GET", f"/api/v1/traces?offset={run['trace']['from']}&limit=2",
                         OBSERVER_TOKEN)[2]
        self.assertEqual([s["actor"] for s in run["steps"]],
                         [r["agent_instance"] for r in page["records"]])

    def test_a_document_that_misses_a_criterion_is_a_successful_run(self):
        run = self.call("POST", RUN, OPERATOR_TOKEN,
                        run_body(criteria=("INV-4", "no such text zq9")))[2]
        self.assertEqual("succeeded", run["state"])
        self.assertEqual({"conformant": False, "satisfied": 1, "total": 2}, run["outcome"])

    def test_scenario_c_a_tool_failure_fails_the_workflow(self):
        """Execution failure → Runtime → Trace → Backend: a meaningful state."""
        run = self.call("POST", RUN, OPERATOR_TOKEN, run_body(document="docs/absent.md"))[2]
        self.assertEqual("failed", run["state"])
        self.assertEqual(["defined", "ready", "running", "failed"], run["states"])
        self.assertIn("docs.read execution_failure", run["failure_reason"])
        self.assertEqual(["failed", "not_run"], [s["status"] for s in run["steps"]])
        self.assertIsNone(run["outcome"])
        page = self.call("GET", f"/api/v1/traces?offset={run['trace']['from']}&limit=5",
                         OBSERVER_TOKEN)[2]
        self.assertEqual([("tool-proposing-agent", "failure"),
                          ("workflow-participating-agent", "failure")],
                         [(r["agent_instance"], r["status"]) for r in page["records"]])

    def test_the_ledger_shows_admission_and_execution(self):
        self.call("POST", RUN, OPERATOR_TOKEN, run_body())
        self.call("POST", RUN, OPERATOR_TOKEN, run_body(document="docs/absent.md"))
        ledger = self.call("GET", "/api/v1/tools/invocations", OBSERVER_TOKEN)[2]["invocations"]
        self.assertEqual([("success", True, True), ("execution_failure", True, True)],
                         [(r["disposition"], r["governance_admitted"], r["execution_attempted"])
                          for r in ledger])

    def test_an_unexpected_step_error_still_ends_the_workflow(self):
        with mock.patch.object(type(self.h.aios), "_verify", side_effect=ValueError("boom")):
            run = self.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        self.assertEqual("failed", run["state"])
        self.assertEqual("verify-criteria: internal error (ValueError)", run["failure_reason"])
        self.assertNotIn("boom", str(run))

    def test_runs_are_listed_newest_first_and_fetchable(self):
        first = self.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        second = self.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        listed = self.call("GET", RUN, OBSERVER_TOKEN)[2]["runs"]
        self.assertEqual([second["run_id"], first["run_id"]], [r["run_id"] for r in listed])
        self.assertEqual(first, self.call("GET", f"{RUN}/{first['run_id']}", OBSERVER_TOKEN)[2])
        self.assertEqual(404, self.call("GET", f"{RUN}/run-99999", OBSERVER_TOKEN)[0])

    def test_each_run_is_its_own_workflow_identity(self):
        a = self.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        b = self.call("POST", RUN, OPERATOR_TOKEN, run_body())[2]
        self.assertNotEqual(a["workflow_identity"], b["workflow_identity"])
        self.assertLess(a["execution_sequence"], b["execution_sequence"])


class InputContract(_Case):
    def post(self, body=None, **kwargs):
        return self.call("POST", RUN, OPERATOR_TOKEN, body, **kwargs)

    def test_invalid_inputs_are_refused_with_400(self):
        cases = [
            {"workflow": "no-such-workflow", "inputs": {"document": DOC, "criteria": ["x"]}},
            {"workflow": "document-conformance-review", "inputs": {"document": DOC}},
            {"workflow": "document-conformance-review", "inputs": {"document": DOC, "criteria": []}},
            {"workflow": "document-conformance-review",
             "inputs": {"document": DOC, "criteria": ["x"] * 21}},
            {"workflow": "document-conformance-review",
             "inputs": {"document": DOC, "criteria": ["x" * 201]}},
            {"workflow": "document-conformance-review",
             "inputs": {"document": DOC, "criteria": ["x"], "extra": 1}},
            {"workflow": "document-conformance-review", "inputs": [], "surplus": True},
            {"inputs": {}},
        ]
        for body in cases:
            with self.subTest(body=str(body)[:80]):
                status, _, error = self.post(body)
                self.assertEqual((400, "invalid_request"), (status, error["error"]))
        self.assertEqual([], self.call("GET", RUN, OBSERVER_TOKEN)[2]["runs"])

    def test_the_body_must_be_a_json_object(self):
        self.assertEqual(400, self.post(raw=b"{not json")[0])
        self.assertEqual(400, self.post(raw=b"[1,2]")[0])
        self.assertEqual(400, self.post(raw=b'{"workflow":"x"}', content_type="text/plain")[0])

    def test_an_oversized_body_is_refused(self):
        status, _, error = self.post(raw=b"{" + b" " * (contract.MAX_BODY_BYTES + 1) + b"}")
        self.assertEqual((413, "payload_too_large"), (status, error["error"]))

    def test_paging_is_bounded(self):
        for query in ("offset=-1", "limit=0", "limit=201", "offset=x"):
            with self.subTest(query=query):
                self.assertEqual(400, self.call("GET", f"/api/v1/traces?{query}",
                                                OBSERVER_TOKEN)[0])


class Routing(_Case):
    def test_unknown_route_is_404(self):
        self.assertEqual((404, "not_found"),
                         (lambda s, h, b: (s, b["error"]))(*self.call("GET", "/api/v1/nope")))

    def test_wrong_method_is_405_with_allow(self):
        status, headers, body = self.call("DELETE", RUN, OPERATOR_TOKEN)
        self.assertEqual((405, "GET, POST"), (status, headers["Allow"]))

    def test_an_internal_error_hides_its_internals(self):
        with mock.patch.object(type(self.h.aios), "catalog", side_effect=RuntimeError("secret-x")):
            with mock.patch("sys.stderr"):
                status, _, body = self.call("GET", "/api/v1/workflows", OBSERVER_TOKEN)
        self.assertEqual((500, "internal_error"), (status, body["error"]))
        self.assertNotIn("secret-x", str(body))
        self.assertNotIn("Traceback", str(body))

    def test_a_stopped_runtime_is_503(self):
        self.h.aios.stop()
        status, _, body = self.call("GET", "/api/v1/runtime", OBSERVER_TOKEN)
        self.assertEqual((503, "unavailable"), (status, body["error"]))
        self.assertEqual(503, self.call("POST", RUN, OPERATOR_TOKEN, run_body())[0])


class StaticConsole(_Case):
    def test_the_console_is_served(self):
        status, headers, page = self.call("GET", "/")
        self.assertEqual(200, status)
        self.assertIn(b"AIOS Console", page)
        self.assertIn("script-src 'self'", headers["Content-Security-Policy"])
        for asset in ("app.js", "api.js", "model.js", "styles.css"):
            with self.subTest(asset=asset):
                self.assertEqual(200, self.call("GET", f"/assets/{asset}")[0])

    def test_nothing_outside_the_frontend_is_served(self):
        for path in ("/assets/../backend/api.py", "/assets/..%2Fbackend%2Fapi.py",
                     "/assets/.hidden", "/assets/README.md", "/backend/api.py",
                     "/assets/", "/assets/nope.js"):
            with self.subTest(path=path):
                self.assertEqual(404, self.call("GET", path)[0])

    def test_the_console_is_read_only(self):
        self.assertEqual(405, self.call("POST", "/")[0])


if __name__ == "__main__":
    unittest.main()
