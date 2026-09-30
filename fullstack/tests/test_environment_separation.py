"""FS-09-ENV E1 (ACT-004 DG-04; ACT-007 `§7`): the application selects the
Supabase project of its own deployment environment, and nothing else.

```text
VERCEL_ENV=preview     → Preview project     (scfymftfzkpilqbgmfwv)
VERCEL_ENV=production  → Production project  (hmljfyqycxcueulhsjae)
anything else          → no project; every API route answers 503
```

The databases are replaced by recording fakes, so the tests show which host a
deployment of each environment talks to, and that it never talks to the other.
Nothing here releases, deploys or touches a real Production store.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from fullstack.backend.supabase_storage import SupabaseStorage
from fullstack.deploy import vercel
from fullstack.tests.support import OPERATOR_TOKEN, default_authenticator
from fullstack.tests.test_deployment import KEY, FakePostgREST, call

PREVIEW = "https://scfymftfzkpilqbgmfwv.supabase.co"
PRODUCTION = "https://hmljfyqycxcueulhsjae.supabase.co"
REPO_ROOT = Path(__file__).resolve().parents[2]


class Recorder:
    """A database per project: which host was called, and with what key."""

    def __init__(self):
        self.databases = {PREVIEW: FakePostgREST(), PRODUCTION: FakePostgREST()}
        self.hosts = []

    def __call__(self, method, url, headers, body):
        host = next((h for h in self.databases if url.startswith(h + "/")), None)
        self.hosts.append(host if host else url)
        if host is None:
            raise AssertionError(f"a call to an unknown host: {url}")
        return self.databases[host](method, url, headers, body)


def deployment(environment):
    """A deployed function for `environment`, over recording databases."""
    recorder = Recorder()
    app = vercel.make_app(
        storage_factory=lambda: vercel.storage_from_environment(
            environment, transport=recorder),
        authenticator=default_authenticator())
    return app, recorder


class TheEnvironmentNamesTheProject(unittest.TestCase):

    def test_each_environment_selects_exactly_its_own_project(self):
        self.assertEqual({"preview": PREVIEW, "production": PRODUCTION},
                         vercel.SUPABASE_PROJECTS)
        self.assertNotEqual(PREVIEW, PRODUCTION)
        for name, project in (("preview", PREVIEW), ("production", PRODUCTION)):
            with self.subTest(environment=name):
                store = vercel.storage_from_environment(
                    {"VERCEL_ENV": name, "SUPABASE_SECRET_KEY": KEY})
                self.assertEqual(f"SupabaseStorage('{project}/rest/v1')", repr(store))
        self.assertEqual(PREVIEW, vercel.SUPABASE_PROJECT_URL)

    def test_a_preview_deployment_never_reaches_the_production_database(self):
        app, recorder = deployment({"VERCEL_ENV": "preview", "SUPABASE_SECRET_KEY": KEY})
        self.assertEqual(200, call(app, "GET", "/api/v1/health")[0])
        self.assertEqual(201, call(app, "POST", "/api/v1/runs", OPERATOR_TOKEN, RUN)[0])
        self.assertTrue(recorder.databases[PREVIEW].calls)
        self.assertTrue(recorder.databases[PREVIEW].rows)
        self.assertEqual([], recorder.databases[PRODUCTION].calls)
        self.assertEqual({PREVIEW}, set(recorder.hosts))

    def test_a_production_deployment_never_reaches_the_preview_database(self):
        app, recorder = deployment({"VERCEL_ENV": "production", "SUPABASE_SECRET_KEY": KEY})
        self.assertEqual(200, call(app, "GET", "/api/v1/health")[0])
        self.assertEqual(201, call(app, "POST", "/api/v1/runs", OPERATOR_TOKEN, RUN)[0])
        self.assertTrue(recorder.databases[PRODUCTION].rows)
        self.assertEqual([], recorder.databases[PREVIEW].calls)
        self.assertEqual({PRODUCTION}, set(recorder.hosts))

    def test_two_environments_keep_two_states(self):
        preview, pr = deployment({"VERCEL_ENV": "preview", "SUPABASE_SECRET_KEY": KEY})
        production, po = deployment({"VERCEL_ENV": "production", "SUPABASE_SECRET_KEY": KEY})
        call(preview, "POST", "/api/v1/runs", OPERATOR_TOKEN, RUN)
        self.assertEqual(1, len(call(preview, "GET", "/api/v1/runs", OPERATOR_TOKEN)[2]["runs"]))
        self.assertEqual([], call(production, "GET", "/api/v1/runs", OPERATOR_TOKEN)[2]["runs"])
        self.assertEqual([], pr.databases[PRODUCTION].calls)
        self.assertEqual([], po.databases[PREVIEW].calls)
        # Production holds only its own audit entry for the read it served: none of
        # the Preview deployment's run, Trace or audit records.
        self.assertEqual({"fullstack-audit"},
                         {r["partition"] for r in po.databases[PRODUCTION].rows})
        self.assertEqual({"fullstack-runs", "trace", "fullstack-audit"},
                         {r["partition"] for r in pr.databases[PREVIEW].rows})
        self.assertEqual(1, len(po.databases[PRODUCTION].rows))


class AnUnresolvedEnvironmentFailsClosed(unittest.TestCase):

    UNRESOLVED = ({}, {"VERCEL_ENV": ""}, {"VERCEL_ENV": "development"},
                  {"VERCEL_ENV": "Production"}, {"VERCEL_ENV": "PREVIEW"},
                  {"VERCEL_ENV": " preview"}, {"VERCEL_ENV": "production\n"},
                  {"VERCEL_ENV": "staging"}, {"VERCEL_ENV": "prod"})

    def test_no_database_is_called_and_every_route_is_503(self):
        for extra in self.UNRESOLVED:
            with self.subTest(environment=extra):
                app, recorder = deployment({**extra, "SUPABASE_SECRET_KEY": KEY})
                for path in ("/api/v1/health", "/api/v1/runs"):
                    status, headers, body = call(app, "GET", path, OPERATOR_TOKEN)
                    self.assertEqual((503, "unavailable"), (status, body["error"]))
                    self.assertEqual("nosniff", headers["X-Content-Type-Options"])
                self.assertEqual([], recorder.hosts)

    def test_the_refusal_quotes_neither_the_environment_nor_the_key(self):
        app, _ = deployment({"VERCEL_ENV": "secret-looking-value", "SUPABASE_SECRET_KEY": KEY})
        text = json.dumps(call(app, "GET", "/api/v1/health")[2])
        self.assertNotIn("secret-looking-value", text)
        self.assertNotIn(KEY, text)

    def test_the_environment_is_read_before_the_key(self):
        """No key and no environment: the refusal is about the environment, and
        neither path reaches a database."""
        with self.assertRaises(vercel.UnknownEnvironment):
            vercel.storage_from_environment({})

    def test_a_refusal_is_logged_like_any_other_503(self):
        from fullstack.backend import telemetry
        log = telemetry.Collector()
        app = vercel.make_app(
            storage_factory=lambda: vercel.storage_from_environment({"SUPABASE_SECRET_KEY": KEY}),
            authenticator=default_authenticator(), telemetry_sink=log)
        self.assertEqual(503, call(app, "GET", "/api/v1/health")[0])
        self.assertEqual([503], [r["status"] for r in log.records()])
        self.assertIsNone(log.records()[0]["runtime_id"])


class NothingElseChoosesTheProject(unittest.TestCase):

    def test_no_variable_overrides_the_project(self):
        for name in ("SUPABASE_URL", "SUPABASE_PROJECT_URL", "NEXT_PUBLIC_SUPABASE_URL"):
            with self.subTest(variable=name):
                for env, project in (("preview", PREVIEW), ("production", PRODUCTION)):
                    store = vercel.storage_from_environment(
                        {"VERCEL_ENV": env, "SUPABASE_SECRET_KEY": KEY,
                         name: "https://other.supabase.co"})
                    self.assertEqual(f"SupabaseStorage('{project}/rest/v1')", repr(store))

    def test_the_source_names_exactly_the_two_recorded_projects(self):
        source = (REPO_ROOT / "fullstack/deploy/vercel.py").read_text(encoding="utf-8")
        import re
        self.assertEqual({PREVIEW, PRODUCTION},
                         set(re.findall(r"https://[a-z0-9]+\.supabase\.co", source)))
        self.assertNotIn("os.environ[\"SUPABASE_URL\"]", source)

    def test_the_selection_uses_no_request_data(self):
        """Authority is never taken from the browser (ACT-007 `§7.3`): the
        environment comes from the process, not from any header or path."""
        app, recorder = deployment({"VERCEL_ENV": "preview", "SUPABASE_SECRET_KEY": KEY})
        import io
        from wsgiref.util import setup_testing_defaults
        environ = {"REQUEST_METHOD": "GET", "PATH_INFO": "/api/v1/health", "QUERY_STRING": "",
                   "wsgi.input": io.BytesIO(b""), "CONTENT_LENGTH": "0",
                   "HTTP_X_VERCEL_ENV": "production", "HTTP_HOST": "production.example",
                   "HTTP_X_FORWARDED_HOST": "production.example"}
        setup_testing_defaults(environ)
        seen = {}
        b"".join(app(environ, lambda status, headers: seen.update(status=status)))
        self.assertTrue(seen["status"].startswith("200"))
        self.assertEqual({PREVIEW}, set(recorder.hosts))


RUN = {"workflow": "document-conformance-review",
       "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                  "criteria": ["INV-4"]}}


if __name__ == "__main__":
    unittest.main()
