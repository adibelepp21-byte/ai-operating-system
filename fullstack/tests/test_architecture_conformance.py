"""FS-DP-03 N1 and FS-DP-07 A1, as ratified by ACT-004 DG-01 / DG-03 (Register `§93`).

N1 (revision 1's rule set as written): one origin, no cross-origin API access;
AIOS never network-addressable; the browser never reaches the database; the
backend's only egress is the database. A1: the application shows the Agent
Instances that act and creates none.
"""

from __future__ import annotations

import io
import json
import re
import unittest
from wsgiref.util import setup_testing_defaults

from fullstack.backend import contract
from fullstack.tests.support import OPERATOR_TOKEN, REPO_ROOT, Harness

SERVED = [REPO_ROOT / "api/index.py", REPO_ROOT / "fullstack/deploy/vercel.py",
          *sorted((REPO_ROOT / "fullstack/backend").glob("*.py"))]


def raw_call(app, method, path, headers):
    environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": "",
               "CONTENT_LENGTH": "0", "wsgi.input": io.BytesIO(b"")}
    for name, value in headers.items():
        environ["HTTP_" + name.upper().replace("-", "_")] = value
    setup_testing_defaults(environ)
    seen = {}
    b"".join(app(environ, lambda s, h: seen.update(status=int(s.split()[0]), headers=dict(h))))
    return seen["status"], seen["headers"]


class N1OneOriginNoCrossOriginAccess(unittest.TestCase):

    def setUp(self):
        self.h = Harness()
        self.addCleanup(self.h.close)

    def test_no_response_grants_cross_origin_access(self):
        origin = {"Origin": "https://attacker.example", "Authorization": f"Bearer {OPERATOR_TOKEN}"}
        for method, path in (("GET", "/api/v1/runs"), ("GET", "/api/v1/health"),
                             ("GET", "/"), ("GET", "/api/v1/nowhere")):
            with self.subTest(path=path):
                _, headers = raw_call(self.h.app, method, path, origin)
                self.assertFalse([k for k in headers if k.lower().startswith("access-control-")])

    def test_a_cors_preflight_is_not_honoured(self):
        status, headers = raw_call(self.h.app, "OPTIONS", "/api/v1/runs", {
            "Origin": "https://attacker.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "authorization"})
        self.assertEqual(405, status)
        self.assertFalse([k for k in headers if k.lower().startswith("access-control-")])

    def test_the_host_configuration_has_one_origin_and_no_cors(self):
        config = json.loads((REPO_ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertEqual("fullstack/frontend", config["outputDirectory"])
        self.assertEqual({"/api/index", "/:file"}, {r["destination"] for r in config["rewrites"]})
        headers = [h["key"].lower() for rule in config["headers"] for h in rule["headers"]]
        self.assertFalse([h for h in headers if h.startswith("access-control-")])

    def test_the_backend_has_no_listener_and_one_egress(self):
        """AIOS runs in-process; the served code's only outbound host is the
        Supabase REST endpoint. (`__main__` is the local server, loopback by default.)"""
        for path in SERVED:
            text = path.read_text(encoding="utf-8")
            hosts = set(re.findall(r"https://([A-Za-z0-9.-]+)", text))
            with self.subTest(path=path.name):
                self.assertTrue(all(h.endswith(".supabase.co") for h in hosts), hosts)
                if path.name != "__main__.py":
                    self.assertNotIn("make_server", text)
                    self.assertNotIn("socket.", text)

    def test_the_browser_holds_no_database_credential(self):
        for path in (REPO_ROOT / "fullstack/frontend").glob("*.js"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("supabase", text.lower())
                self.assertIsNone(re.search(r"sb_(?:secret|publishable)_|eyJhbGci", text))


class A2RegistersInstancesOnlyNeverDefinitions(unittest.TestCase):
    """FS-DP-07 A2 (ACT-008-DG-01, Register `§101`): the application registers an
    Agent **Instance** of an existing governed Definition and nothing more.
    A1 ("creates none") was ratified by ACT-004 and is superseded by that
    decision; A3 (authoring Definitions) is not built. What conforms to A2 is
    partly a presence and partly absences, so both are tested."""

    def test_the_state_changing_routes_are_exactly_a_run_and_an_instance_registration(self):
        writes = [(r.method, r.template, r.scope) for r in contract.ROUTES if r.method != "GET"]
        self.assertEqual([("POST", "/api/v1/runs", "aios.workflow.run"),
                          ("POST", "/api/v1/agent-instances", "aios.agent.register")], writes)

    def test_no_route_authors_edits_or_retires_a_definition(self):
        for route in contract.ROUTES:
            if route.method != "GET":
                self.assertNotIn("definition", route.template.lower(), route.template)
        self.assertEqual(["GET"], [r.method for r in contract.ROUTES
                                   if r.template.endswith("/agent-definitions")])

    def test_the_acting_agent_instances_are_shown(self):
        h = Harness()
        self.addCleanup(h.close)
        _, _, run = h.call("POST", "/api/v1/runs", OPERATOR_TOKEN, body={
            "workflow": "document-conformance-review",
            "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                       "criteria": ["INV-4"]}})
        self.assertEqual({"tool-proposing-agent", "engineering-intelligence-agent"},
                         {s["actor"] for s in run["steps"]})
        self.assertEqual(3, len(h.aios.run_trace(run["run_id"])))

    def test_the_p11_registry_authority_is_not_reused(self):
        """`FD-P11-001 §7` authorized registration for P11-W4 only; the application
        has its own instrument (ACT-008 `§7.2`) and imports nothing from `tools/`."""
        for path in SERVED:
            with self.subTest(file=path.name):
                self.assertIsNone(re.search(r"(?m)^\s*(from|import)\b[^\n]*agent_instance_registry",
                                            path.read_text(encoding="utf-8")),
                                  "served code must not import the P11 registry")

    def test_served_code_never_writes_a_definition_document(self):
        source = (REPO_ROOT / "fullstack/backend/agents.py").read_text(encoding="utf-8")
        self.assertNotRegex(source, r"write_text|write_bytes|open\([^)]*[\"'][wa]")
        for path in SERVED:
            if path.name != "agents.py":
                self.assertNotIn("AgentDefinition(", path.read_text(encoding="utf-8"), path.name)

    def test_the_console_offers_no_way_to_author_a_definition(self):
        control = re.compile(r"(create|author|edit|retire|delete)[-_ ]?(an? )?(agent )?definition",
                             re.IGNORECASE)
        for path in sorted((REPO_ROOT / "fullstack/frontend").glob("*.*")):
            with self.subTest(file=path.name):
                self.assertIsNone(control.search(path.read_text(encoding="utf-8")))

    def test_only_the_three_partitions_plus_registrations_are_ever_stored(self):
        h = Harness()
        self.addCleanup(h.close)
        h.call("POST", "/api/v1/runs", OPERATOR_TOKEN, body={
            "workflow": "document-conformance-review",
            "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                       "criteria": ["INV-4"]}})
        self.assertEqual({"trace", "fullstack-runs", "fullstack-audit"},
                         set(h.aios.storage.partitions()))


if __name__ == "__main__":
    unittest.main()
