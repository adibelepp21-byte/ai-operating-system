"""FS-DP-07 A2 — Scenario A: *User → Create Agent → Backend → AIOS Agent
Capability → Persist → Result* (ACT-008-DG-01, Register `§101`).

Setup, action, expected and actual result, state, database and security for the
mandatory scenario, plus every way the registration refuses. The live run on the
deployed Preview is recorded separately (`docs/fullstack/evidence/`).
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from unittest import mock

from fullstack.backend import agents, telemetry
from fullstack.backend.security import AuditLedger, token_sha256
from fullstack.deploy import vercel
from fullstack.backend.supabase_storage import SupabaseStorage
from fullstack.tests.support import OBSERVER_TOKEN, OPERATOR_TOKEN, REPO_ROOT, Harness
from fullstack.tests.test_deployment import KEY, FakePostgREST, call

DEFINITION = "engineering-intelligence-agent"
REGISTER = "/api/v1/agent-instances"


def body(**changes):
    base = {"definition": DEFINITION, "instance_key": "reviewer-01",
            "capabilities": ["engineering-intelligence"]}
    base.update(changes)
    return {k: v for k, v in base.items() if v is not None}


class ScenarioAEndToEnd(unittest.TestCase):
    """The mandatory scenario, step by step."""

    def setUp(self):
        self.h = Harness()
        self.addCleanup(self.h.close)

    def test_a_user_creates_an_agent_and_the_result_is_persisted_and_visible(self):
        # SETUP: the governed Definitions the user may choose from.
        status, _, listed = self.h.call("GET", "/api/v1/agent-definitions", OPERATOR_TOKEN)
        self.assertEqual(200, status)
        self.assertEqual({"cognitive-intelligence-agent", DEFINITION,
                          "governance-artifact-integrity-agent"},
                         {d["definition"] for d in listed["definitions"]})
        # ACTION: Create Agent.
        status, headers, created = self.h.call("POST", REGISTER, OPERATOR_TOKEN, body=body())
        # EXPECTED / ACTUAL: a registration of exactly one Definition, by the caller.
        self.assertEqual(201, status)
        self.assertEqual("fullstack.agent-instance/1", created["format"])
        self.assertEqual(("reviewer-01", "REGISTERED", "operator@test"),
                         (created["instance_key"], created["lifecycle"], created["created_by"]))
        self.assertEqual({"key": DEFINITION, "version": "1.1", "owning_department": "engineering"},
                         created["definition"])
        self.assertEqual(["engineering-intelligence"], created["permitted_capabilities"])
        self.assertEqual(agents.AUTHORITY, created["authority"])
        self.assertIs(False, created["grants_authority"])
        # STATE / DATABASE: persisted in the shared store, in its own partition.
        stored = [json.loads(r) for r in self.h.aios.storage.read(agents.AGENTS_PARTITION)]
        self.assertEqual([created], stored)
        # RESULT: visible through the API (what the console renders).
        self.assertEqual([created], self.h.call("GET", REGISTER, OPERATOR_TOKEN)[2]["instances"])
        self.assertEqual(created, self.h.call("GET", f"{REGISTER}/reviewer-01", OPERATOR_TOKEN)[2])
        # SECURITY: the decision is audited, and no credential or body is.
        audit = [e for e in AuditLedger(self.h.aios.storage).entries() if e["path"] == REGISTER]
        self.assertEqual([("POST", "aios.agent.register", "allowed", "operator@test"),
                          ("GET", "aios.observe", "allowed", "operator@test")],
                         [(e["method"], e["scope"], e["decision"], e["subject"]) for e in audit])
        text = json.dumps(stored) + json.dumps(audit)
        for secret in (OPERATOR_TOKEN, token_sha256(OPERATOR_TOKEN), "Bearer"):
            self.assertNotIn(secret, text)
        # TRACE: a registration is an operator action, not an Agent acting, so it
        # writes no Trace (INV-4 is about acting Agents; AGENT INSTANCE ≠ AUTHORITY).
        self.assertEqual(0, self.h.aios.traces(0, 10)["total"])

    def test_the_registered_instance_is_not_an_actor(self):
        """Registering grants nothing: it does not appear among a run's actors and
        a run still uses the application's own instances."""
        self.h.call("POST", REGISTER, OPERATOR_TOKEN, body=body())
        _, _, run = self.h.call("POST", "/api/v1/runs", OPERATOR_TOKEN, body={
            "workflow": "document-conformance-review",
            "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                       "criteria": ["INV-4"]}})
        self.assertNotIn("reviewer-01", {s["actor"] for s in run["steps"]})

    def test_the_registration_survives_a_new_runtime(self):
        first = self.h.call("POST", REGISTER, OPERATOR_TOKEN, body=body())[2]
        again = Harness(data_dir=self.h.data_dir)
        try:
            self.assertNotEqual(self.h.aios.runtime_id, again.aios.runtime_id)
            self.assertEqual([first], again.call("GET", REGISTER, OPERATOR_TOKEN)[2]["instances"])
        finally:
            again.close()

    def test_several_instances_of_one_definition_and_of_different_ones(self):
        for key, definition, cap in (("reviewer-01", DEFINITION, "engineering-intelligence"),
                                     ("reviewer-02", DEFINITION, "engineering-intelligence"),
                                     ("cognition-01", "cognitive-intelligence-agent",
                                      "cognitive-intelligence")):
            self.assertEqual(201, self.h.call("POST", REGISTER, OPERATOR_TOKEN, body=body(
                instance_key=key, definition=definition, capabilities=[cap]))[0])
        self.assertEqual(["reviewer-01", "reviewer-02", "cognition-01"],
                         [i["instance_key"] for i in
                          self.h.call("GET", REGISTER, OPERATOR_TOKEN)[2]["instances"]])


class TheRegistrationRefuses(unittest.TestCase):

    def setUp(self):
        self.h = Harness()
        self.addCleanup(self.h.close)

    def post(self, token=OPERATOR_TOKEN, **changes):
        return self.h.call("POST", REGISTER, token, body=body(**changes))

    def nothing_was_stored(self):
        self.assertEqual([], list(self.h.aios.storage.read(agents.AGENTS_PARTITION)))

    def test_without_a_credential_or_with_a_bad_one_it_is_401(self):
        for token in (None, "", "wrong-token"):
            with self.subTest(token=token):
                self.assertEqual(401, self.post(token=token)[0])
        self.nothing_was_stored()

    def test_without_the_scope_it_is_403_and_audited(self):
        status, _, payload = self.post(token=OBSERVER_TOKEN)
        self.assertEqual((403, "forbidden"), (status, payload["error"]))
        refused = [e for e in AuditLedger(self.h.aios.storage).entries()
                   if e["path"] == REGISTER and e["decision"] == "refused"]
        self.assertEqual([("observer@test", 403)], [(e["subject"], e["status"]) for e in refused])
        self.nothing_was_stored()

    def test_the_request_cannot_name_its_own_authority_or_lifecycle(self):
        for extra in ({"authority": {"instrument": "self"}}, {"created_by": "someone-else"},
                      {"lifecycle": "ACTIVE"}, {"grants_authority": True},
                      {"accountable_to": "founder"}):
            with self.subTest(extra=extra):
                status, _, payload = self.h.call("POST", REGISTER, OPERATOR_TOKEN,
                                                 body={**body(), **extra})
                self.assertEqual((400, "invalid_request"), (status, payload["error"]))
        self.nothing_was_stored()

    def test_an_unknown_or_missing_definition_is_400_and_creates_none(self):
        for definition in ("no-such-agent", "", None, 7, ["x"]):
            with self.subTest(definition=definition):
                status, _, payload = self.post(definition=definition)
                self.assertEqual((400, "invalid_request"), (status, payload["error"]))
        self.nothing_was_stored()
        self.assertEqual(3, len(self.h.call("GET", "/api/v1/agent-definitions",
                                            OPERATOR_TOKEN)[2]["definitions"]))

    def test_a_malformed_identity_is_400(self):
        for key in (None, "", "ab", "Reviewer-01", "-reviewer", "a b c", "x" * 65, "a/b/c",
                    "../etc", 12, "reviewer_01"):
            with self.subTest(key=key):
                self.assertEqual(400, self.post(instance_key=key)[0])
        self.nothing_was_stored()

    def test_capabilities_are_explicit_bounded_by_the_definition_and_unique(self):
        for capabilities in (None, [], "engineering-intelligence", [1], [""],
                             ["engineering-intelligence", "engineering-intelligence"],
                             ["cognitive-intelligence"], ["engineering-intelligence", "admin"]):
            with self.subTest(capabilities=capabilities):
                self.assertEqual(400, self.post(capabilities=capabilities)[0])
        self.nothing_was_stored()

    def test_a_duplicate_identity_is_409_and_the_first_registration_stands(self):
        first = self.post()[2]
        status, _, payload = self.post(definition="cognitive-intelligence-agent",
                                       capabilities=["cognitive-intelligence"])
        self.assertEqual((409, "conflict"), (status, payload["error"]))
        self.assertEqual([first], self.h.call("GET", REGISTER, OPERATOR_TOKEN)[2]["instances"])

    def test_a_concurrent_duplicate_loses_after_the_fact_and_stays_inert(self):
        """Two requests pass the uniqueness check together. The first record in append
        order is the registration; the other is refused, and its record (nothing is
        deleted) is ignored by every read."""
        first = self.post()[2]
        real = agents.AgentRegistry.instance
        with mock.patch.object(agents.AgentRegistry, "instance", lambda self, key: None):
            status, _, payload = self.post(definition="cognitive-intelligence-agent",
                                           capabilities=["cognitive-intelligence"])
        self.assertEqual((409, "conflict"), (status, payload["error"]))
        self.assertEqual(2, len(list(self.h.aios.storage.read(agents.AGENTS_PARTITION))))
        self.assertEqual([first], self.h.call("GET", REGISTER, OPERATOR_TOKEN)[2]["instances"])
        self.assertEqual(first, self.h.call("GET", f"{REGISTER}/reviewer-01", OPERATOR_TOKEN)[2])
        self.assertIsNotNone(real)

    def test_a_bad_body_is_400(self):
        for raw, kind in ((b"{not json", "application/json"), (b"[]", "application/json"),
                          (b"null", "application/json"), (b'{"definition":', "application/json"),
                          (json.dumps(body()).encode(), "text/plain")):
            with self.subTest(raw=raw[:20], kind=kind):
                status, _, payload = self.h.call("POST", REGISTER, OPERATOR_TOKEN, raw=raw,
                                                 content_type=kind)
                self.assertEqual((400, "invalid_request"), (status, payload["error"]))
        self.nothing_was_stored()

    def test_an_oversized_body_is_413(self):
        raw = json.dumps(body(instance_key="a" * 70_000)).encode()
        self.assertEqual(413, self.h.call("POST", REGISTER, OPERATOR_TOKEN, raw=raw)[0])
        self.nothing_was_stored()

    def test_an_unknown_instance_is_404(self):
        self.assertEqual(404, self.h.call("GET", f"{REGISTER}/nobody-here", OPERATOR_TOKEN)[0])

    def test_the_wrong_method_is_405(self):
        for method in ("PUT", "PATCH", "DELETE"):
            with self.subTest(method=method):
                self.assertEqual(405, self.h.call(method, REGISTER, OPERATOR_TOKEN)[0])
                self.assertEqual(405, self.h.call(method, f"{REGISTER}/reviewer-01",
                                                  OPERATOR_TOKEN)[0])


class DefinitionsAreOnlyEverRead(unittest.TestCase):

    def digest(self):
        h = hashlib.sha256()
        for path in sorted((REPO_ROOT / "docs/architecture/organization").rglob("*.md")):
            h.update(path.read_bytes())
        return h.hexdigest()

    def test_registering_changes_no_governed_document(self):
        before = self.digest()
        h = Harness()
        try:
            h.call("POST", REGISTER, OPERATOR_TOKEN, body=body())
            h.call("POST", REGISTER, OPERATOR_TOKEN, body=body(definition="no-such-agent"))
        finally:
            h.close()
        self.assertEqual(before, self.digest())

    def test_an_incomplete_document_is_not_registrable(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "docs/architecture/organization/engineering/agent-definitions"
            folder.mkdir(parents=True)
            (folder / "half-written-agent.md").write_text("# Half\n\n## Metadata\n\n- **Version:** 1\n",
                                                          encoding="utf-8")
            (folder / "retired-agent.md").write_text(
                "## Metadata\n\n- **Version:** 1\n- **Status:** Retired\n\n## Implemented Capability\n\n"
                "[X](../capabilities/x-cap.md)\n", encoding="utf-8")
            (folder / "good-agent.md").write_text(
                "## Metadata\n\n- **Version:** 2.0\n- **Status:** Active\n\n## Implemented Capability\n\n"
                "[X](../capabilities/x-cap.md)\n", encoding="utf-8")
            found = agents.GovernedDefinitions(Path(tmp)).active()
        self.assertEqual(["good-agent"], sorted(found))
        self.assertEqual(("2.0", "engineering", ("x-cap",)),
                         (found["good-agent"].agent_definition_version,
                          found["good-agent"].owning_department_key,
                          found["good-agent"].implemented_capabilities))


class OnTheDeployedComposition(unittest.TestCase):
    """The Vercel function: a Runtime per request, state only in the database."""

    def test_a_registration_crosses_request_boundaries_only_through_the_database(self):
        fake = FakePostgREST()
        app = vercel.make_app(storage_factory=lambda: SupabaseStorage(
            "https://scfymftfzkpilqbgmfwv.supabase.co", KEY, transport=fake),
            authenticator=__import__("fullstack.tests.support", fromlist=["x"]).default_authenticator())
        status, _, created = call(app, "POST", REGISTER, OPERATOR_TOKEN, body())
        self.assertEqual(201, status)
        status, _, listed = call(app, "GET", REGISTER, OPERATOR_TOKEN)
        self.assertEqual([created], listed["instances"])
        self.assertIn(agents.AGENTS_PARTITION, {r["partition"] for r in fake.rows})
        self.assertEqual(201, call(app, "POST", REGISTER, OPERATOR_TOKEN,
                                   body(instance_key="reviewer-02"))[0])
        self.assertEqual(409, call(app, "POST", REGISTER, OPERATOR_TOKEN, body())[0])


class TelemetryStaysTemplated(unittest.TestCase):

    def test_the_instance_key_never_reaches_a_log_line(self):
        h = Harness()
        self.addCleanup(h.close)
        h.call("POST", REGISTER, OPERATOR_TOKEN, body=body(instance_key="secret-looking-key"))
        h.call("GET", f"{REGISTER}/secret-looking-key", OPERATOR_TOKEN)
        routes = [r["route"] for r in h.telemetry.records()]
        self.assertEqual([REGISTER, f"{REGISTER}/{{instance_key}}"], routes)
        self.assertNotIn("secret-looking-key", "\n".join(h.telemetry.lines))


if __name__ == "__main__":
    unittest.main()
