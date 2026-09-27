"""FS-08 — the ratified deployment (FS-ARCH-RAT-001): the Supabase store behind
`StorageFacility`, and the per-request Vercel function over it.

The database is replaced by `FakePostgREST`, an in-memory model of the
`aios_records` table as PostgREST serves it: the same URLs, headers, status
codes and bytea encoding. The live project is verified separately
(`docs/fullstack/FS-08-DEPLOYMENT-EVIDENCE.md`).
"""

from __future__ import annotations

import io
import json
import re
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit
from wsgiref.util import setup_testing_defaults

from fullstack.backend import api as api_module
from fullstack.backend.aios import (
    AIOSApplication, LEGACY_RUN_FORMAT, RUN_FORMAT, RUNS_PARTITION, run_id_for)
from fullstack.backend import supabase_storage
from fullstack.backend.supabase_storage import SupabaseStorage, StorageUnavailable
from fullstack.deploy import vercel
from fullstack.tests.support import (
    OBSERVER_TOKEN, OPERATOR_TOKEN, default_authenticator, operator_configuration)
from native_core.core.infrastructure import LocalAppendOnlyStorage
from native_core.core.infrastructure.facility import FacilityState

REPO_ROOT = Path(__file__).resolve().parents[2]
URL = "https://scfymftfzkpilqbgmfwv.supabase.co"
KEY = "sb_secret_test-only-not-a-real-key"
MIGRATIONS = REPO_ROOT / "fullstack/deploy/supabase/migrations"


class FakePostgREST:
    """`aios_records` as PostgREST serves it, in memory. Append-only: it has no
    route that updates or deletes, like the table's privileges."""

    def __init__(self, key=KEY):
        self.key, self.rows, self.calls, self.down = key, [], [], False

    def __call__(self, method, url, headers, body):
        self.calls.append((method, url, dict(headers)))
        if self.down:
            raise OSError("connection refused")
        if headers.get("apikey") != self.key or headers.get("Authorization") != f"Bearer {self.key}":
            return 401, b'{"message":"Invalid API key"}'
        parts = urlsplit(url)
        path = parts.path.split("/rest/v1/")[-1]
        if method == "POST" and path == "aios_records":
            row = json.loads(body)
            record = bytes.fromhex(row["record"][2:])
            p = row["partition"]
            if b"\n" in record or not p or "/" in p or "\\" in p or p in (".", ".."):
                return 400, b'{"code":"23514"}'
            self.rows.append({"seq": len(self.rows) + 1, "partition": p, "record": record})
            return 201, b""
        if method == "GET" and path == "aios_records":
            q = {k: v[0] for k, v in parse_qs(parts.query).items()}
            rows = self.rows
            if "partition" in q:
                rows = [r for r in rows if r["partition"] == unquote(q["partition"][3:])]
            if "seq" in q:
                rows = [r for r in rows if r["seq"] > int(q["seq"][3:])]
            rows = sorted(rows, key=lambda r: r["seq"])[:int(q.get("limit", 1000))]
            return 200, json.dumps([{"seq": r["seq"], "record": "\\x" + r["record"].hex()}
                                    for r in rows]).encode()
        if method == "POST" and path == "rpc/aios_partitions":
            names = sorted({r["partition"] for r in self.rows}, key=lambda s: s.encode())
            return 200, json.dumps(names).encode()
        return 404, b"{}"


def supabase(fake=None):
    fake = fake or FakePostgREST()
    store = SupabaseStorage(URL, KEY, transport=fake)
    store.provision()
    return store, fake


class TheStorageContractHoldsOnBothBackends(unittest.TestCase):
    """The same assertions against the certified local backend and the new one."""

    def backends(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        local = LocalAppendOnlyStorage(Path(tmp.name))
        local.provision()
        return {"local": local, "supabase": supabase()[0]}

    def test_append_then_read_in_append_order(self):
        for name, store in self.backends().items():
            with self.subTest(backend=name):
                for record in (b'{"a":1}', b"\x00\xff\xfe", "ü".encode(), b"3"):
                    store.append("trace", record)
                store.append("other", b"x")
                self.assertEqual([b'{"a":1}', b"\x00\xff\xfe", "ü".encode(), b"3"],
                                 list(store.read("trace")))
                self.assertEqual([], list(store.read("absent")))

    def test_partitions_are_listed_in_byte_order(self):
        for name, store in self.backends().items():
            with self.subTest(backend=name):
                for p in ("fullstack-runs", "trace", "Z", "fullstack-audit"):
                    store.append(p, b"r")
                self.assertEqual(["Z", "fullstack-audit", "fullstack-runs", "trace"],
                                 list(store.partitions()))

    def test_the_same_refusals(self):
        for name, store in self.backends().items():
            with self.subTest(backend=name):
                with self.assertRaises(ValueError):
                    store.append("trace", b"a\nb")
                for bad in ("", "..", "a/b", "a\\b"):
                    with self.assertRaises(ValueError):
                        store.append(bad, b"r")
                with self.assertRaises(TypeError):
                    store.append("trace", "text")

    def test_neither_offers_edit_or_delete(self):
        for name, store in self.backends().items():
            with self.subTest(backend=name):
                offered = {m for m in dir(store) if not m.startswith("_")}
                self.assertFalse(offered & {"update", "delete", "remove", "truncate",
                                            "edit", "overwrite", "clear"})


class SupabaseStorageFailsClosed(unittest.TestCase):
    def test_reads_page_through_every_row(self):
        store, fake = supabase()
        original = supabase_storage.PAGE_ROWS
        supabase_storage.PAGE_ROWS = 3
        self.addCleanup(setattr, supabase_storage, "PAGE_ROWS", original)
        for i in range(8):
            store.append("trace", str(i).encode())
        self.assertEqual([str(i).encode() for i in range(8)], list(store.read("trace")))
        pages = lambda: sum(1 for c in fake.calls if c[0] == "GET" and "partition=eq.trace" in c[1])
        self.assertEqual(3, pages())  # 3 + 3 + 2: a short page ends the read
        store.append("trace", b"8")
        fake.calls.clear()
        self.assertEqual(9, len(list(store.read("trace"))))
        self.assertEqual(4, pages())  # 3 + 3 + 3 + an empty page

    def test_a_wrong_key_never_provisions(self):
        store = SupabaseStorage(URL, "wrong-key", transport=FakePostgREST())
        with self.assertRaises(StorageUnavailable):
            store.provision()
        self.assertIs(FacilityState.FAILED, store.state)

    def test_an_unreachable_database_raises_without_the_key(self):
        store, fake = supabase()
        fake.down = True
        for act in (lambda: store.append("trace", b"r"), lambda: list(store.read("trace")),
                    lambda: list(store.partitions())):
            with self.assertRaises(StorageUnavailable) as caught:
                act()
            self.assertNotIn(KEY, str(caught.exception))
        self.assertNotIn(KEY, repr(store))

    def test_a_refused_append_is_an_error_not_a_silent_loss(self):
        store, fake = supabase()
        fake.key = "rotated"
        with self.assertRaises(StorageUnavailable):
            store.append("trace", b"r")
        self.assertEqual([], fake.rows)

    def test_nothing_is_used_before_provisioning(self):
        store = SupabaseStorage(URL, KEY, transport=FakePostgREST())
        with self.assertRaises(Exception):
            store.append("trace", b"r")

    def test_the_key_travels_only_in_the_two_headers(self):
        store, fake = supabase()
        store.append("trace", b"r")
        for method, url, headers in fake.calls:
            self.assertNotIn(KEY, url)
            self.assertEqual({"apikey", "Authorization"},
                             {h for h, v in headers.items() if KEY in v})


def call(app, method, path, token=None, body=None):
    data = json.dumps(body).encode() if body is not None else b""
    path, _, query = path.partition("?")
    env = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
           "wsgi.input": io.BytesIO(data), "CONTENT_LENGTH": str(len(data)),
           "CONTENT_TYPE": "application/json"}
    if token:
        env["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    setup_testing_defaults(env)
    seen = {}
    out = b"".join(app(env, lambda s, h: seen.update(status=int(s.split()[0]), headers=dict(h))))
    return seen["status"], seen["headers"], json.loads(out) if out else None


RUN = {"workflow": "document-conformance-review",
       "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                  "criteria": ["INV-4"]}}


class ThePerRequestFunction(unittest.TestCase):
    """FS-DP-04 A1: a Runtime per request; state only in the database."""

    def setUp(self):
        self.fake = FakePostgREST()
        self.app = vercel.make_app(
            storage_factory=lambda: SupabaseStorage(URL, KEY, transport=self.fake),
            authenticator=default_authenticator())

    def test_state_crosses_request_boundaries_only_through_the_database(self):
        status, _, run = call(self.app, "POST", "/api/v1/runs", OPERATOR_TOKEN, RUN)
        self.assertEqual((201, "succeeded"), (status, run["state"]))
        # A later request is a new Runtime, in the same process or another.
        _, _, runtime = call(self.app, "GET", "/api/v1/runtime", OBSERVER_TOKEN)
        self.assertNotEqual(run["runtime_id"], runtime["runtime_id"])
        _, _, runs = call(self.app, "GET", "/api/v1/runs", OBSERVER_TOKEN)
        self.assertEqual([run["run_id"]], [r["run_id"] for r in runs["runs"]])
        _, _, traces = call(self.app, "GET", "/api/v1/traces", OBSERVER_TOKEN)
        self.assertEqual(3, traces["total"])
        self.assertEqual({"trace", "fullstack-runs", "fullstack-audit"},
                         {r["partition"] for r in self.fake.rows})

    def test_sequential_requests_get_distinct_runtime_derived_ids(self):
        """FS-DP-05 V1: each request is its own Runtime, so its own run id."""
        runs = [call(self.app, "POST", "/api/v1/runs", OPERATOR_TOKEN, RUN)[2]
                for _ in range(3)]
        self.assertEqual(3, len({r["run_id"] for r in runs}))
        for run in runs:
            with self.subTest(run=run["run_id"]):
                self.assertEqual(run_id_for(run["runtime_id"].split("/", 1)[1],
                                            run["execution_sequence"]), run["run_id"])
                self.assertEqual(run, call(self.app, "GET", f"/api/v1/runs/{run['run_id']}",
                                           OBSERVER_TOKEN)[2])

    def test_a_failed_run_is_durable_too(self):
        body = dict(RUN, inputs=dict(RUN["inputs"], document="docs/absent.md"))
        status, _, run = call(self.app, "POST", "/api/v1/runs", OPERATOR_TOKEN, body)
        self.assertEqual((201, "failed"), (status, run["state"]))
        self.assertEqual("failed", call(self.app, "GET", f"/api/v1/runs/{run['run_id']}",
                                        OBSERVER_TOKEN)[2]["state"])

    def test_security_behaviour_is_unchanged(self):
        self.assertEqual(401, call(self.app, "GET", "/api/v1/runs")[0])
        self.assertEqual(403, call(self.app, "POST", "/api/v1/runs", OBSERVER_TOKEN, RUN)[0])
        status, headers, _ = call(self.app, "GET", "/api/v1/health")
        self.assertEqual(200, status)
        self.assertEqual(api_module.API_CSP, headers["Content-Security-Policy"])
        audit = call(self.app, "GET", "/api/v1/audit", OPERATOR_TOKEN)[2]["entries"]
        self.assertEqual({"refused"}, {e["decision"] for e in audit
                                       if e["path"] == "/api/v1/runs" and e["method"] == "POST"})

    def test_the_shipped_function_authenticates_nobody_until_configured(self):
        """FS-DP-02 B3: the function reads `AIOS_OPERATOR_TOKENS`; without it,
        or with a refused value, nobody is authenticated."""
        store = lambda: SupabaseStorage(URL, KEY, transport=self.fake)
        for environment in ({}, {"AIOS_OPERATOR_TOKENS": "not json"}):
            with self.subTest(environment=environment):
                shipped = vercel.make_app(
                    storage_factory=store,
                    authenticator=vercel.authenticator_from_environment(environment))
                self.assertEqual(200, call(shipped, "GET", "/api/v1/health")[0])
                self.assertEqual(401, call(shipped, "GET", "/api/v1/runs", OPERATOR_TOKEN)[0])
        configured = vercel.make_app(
            storage_factory=store, authenticator=vercel.authenticator_from_environment(
                {"AIOS_OPERATOR_TOKENS": operator_configuration(
                    {OPERATOR_TOKEN: ("operator@test", {"aios.observe"})})}))
        self.assertEqual(200, call(configured, "GET", "/api/v1/runs", OPERATOR_TOKEN)[0])
        self.assertEqual(401, call(configured, "GET", "/api/v1/runs", OBSERVER_TOKEN)[0])

    def test_a_malformed_key_is_named_as_such_and_never_quoted(self):
        """A key broken by a line break used to reach urllib and fail as a bare
        `ValueError`. It is refused first, with a reason and without the value."""
        for bad in ("sb_secret_abc\ndef", "sb_secret_abc\r\ndef", "sb_secret abc",
                    '"sb_secret_abc"', "sb_secret_abcé"):
            with self.subTest(key=repr(bad)):
                app = vercel.make_app(storage_factory=lambda b=bad: vercel.storage_from_environment(
                    {"SUPABASE_SECRET_KEY": b}, transport=self.fake))
                status, _, body = call(app, "GET", "/api/v1/health")
                self.assertEqual(503, status)
                self.assertIn("cannot be sent", body["detail"])
                self.assertNotIn("sb_secret", json.dumps(body))
        self.assertEqual([], self.fake.calls)
        good = vercel.storage_from_environment({"SUPABASE_SECRET_KEY": f"  {KEY}\n"},
                                               transport=self.fake)
        self.assertIsInstance(good, SupabaseStorage)

    def test_no_key_means_503_and_nothing_else(self):
        app = vercel.make_app(storage_factory=lambda: vercel.storage_from_environment({}))
        for path in ("/api/v1/health", "/api/v1/runs"):
            status, headers, body = call(app, "GET", path)
            self.assertEqual((503, "unavailable"), (status, body["error"]))
            self.assertEqual("nosniff", headers["X-Content-Type-Options"])

    def test_an_unreachable_database_is_503_not_a_local_fallback(self):
        self.fake.down = True
        with tempfile.TemporaryDirectory() as tmp:
            import os
            before = os.getcwd()
            os.chdir(tmp)
            try:
                status, _, body = call(self.app, "GET", "/api/v1/health")
            finally:
                os.chdir(before)
            self.assertEqual(503, status)
            self.assertNotIn(KEY, json.dumps(body))
            self.assertEqual([], list(Path(tmp).iterdir()))

    def test_the_function_serves_the_api_only(self):
        self.assertEqual(404, call(self.app, "GET", "/")[0])
        self.assertEqual([], self.fake.calls)

    def test_the_adapter_never_names_a_local_store(self):
        source = (REPO_ROOT / "fullstack/deploy/vercel.py").read_text(encoding="utf-8")
        self.assertNotIn("LocalAppendOnlyStorage", source)
        self.assertNotIn("data_dir", source)

    def test_the_store_is_the_ratified_project(self):
        store = vercel.storage_from_environment({"SUPABASE_SECRET_KEY": KEY,
                                                 "SUPABASE_URL": "https://other.supabase.co"})
        self.assertEqual("SupabaseStorage('https://scfymftfzkpilqbgmfwv.supabase.co/rest/v1')",
                         repr(store))
        self.assertIsNone(vercel.storage_from_environment({"SUPABASE_SECRET_KEY": "  "}))


class _SerializedDatabase:
    """The fake table behind a lock, as a database serializes its own INSERTs.

    Only the stand-in for Postgres is locked. The application under test is
    not: each Runtime runs in its own thread with nothing shared but the store."""

    def __init__(self):
        self.fake, self._lock = FakePostgREST(), threading.Lock()

    def __call__(self, *args):
        with self._lock:
            return self.fake(*args)


class TheConcurrencyResolution(unittest.TestCase):
    """FS-DP-05, C1 ratified (Register `§79`): run identity comes from the Runtime.

    Before C1 a run's number was a count of run records read at Runtime start,
    and two Runtimes that started together both minted `run-00001`. That
    finding is kept below as the case that now resolves."""

    def per_request_apps(self, n, transport):
        apps = [AIOSApplication(None, REPO_ROOT, storage=SupabaseStorage(URL, KEY, transport=transport))
                for _ in range(n)]
        for app in apps:
            app.start()
        return apps

    def two_concurrent_runs(self):
        first, second = self.per_request_apps(2, FakePostgREST())
        # Both Runtimes are started before either runs: the interleaving that
        # used to collide.
        runs = [app.start_run(RUN["workflow"], RUN["inputs"], who)
                for app, who in ((first, "p1"), (second, "p2"))]
        return runs, first

    def test_the_former_finding_now_resolves(self):
        runs, reader = self.two_concurrent_runs()
        self.assertNotEqual(runs[0]["runtime_id"], runs[1]["runtime_id"])
        # Each run is addressable by its own id and is the run that was made.
        self.assertEqual("p1", reader.run(runs[0]["run_id"])["requested_by"])
        self.assertEqual("p2", reader.run(runs[1]["run_id"])["requested_by"])

    def test_concurrent_requests_mint_distinct_run_ids(self):
        runs, _ = self.two_concurrent_runs()
        self.assertNotEqual(runs[0]["run_id"], runs[1]["run_id"])

    def test_n_parallel_requests_give_n_distinct_runs_with_their_own_trace(self):
        """V2, V3, V5: N Runtimes in N threads over one store."""
        n = 12
        db = _SerializedDatabase()
        apps = self.per_request_apps(n, db)
        barrier, results, errors = threading.Barrier(n), [None] * n, []

        def request(i):
            try:
                barrier.wait()
                results[i] = apps[i].start_run(RUN["workflow"], RUN["inputs"], f"p{i}")
            except Exception as error:  # reported below, never swallowed
                errors.append(error)

        threads = [threading.Thread(target=request, args=(i,)) for i in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(60)
        self.assertEqual([], errors)
        ids = [r["run_id"] for r in results]
        self.assertEqual(n, len(set(ids)), "duplicate run identity")
        reader = AIOSApplication(None, REPO_ROOT, storage=SupabaseStorage(URL, KEY, transport=db))
        reader.start()
        self.assertEqual(sorted(ids), sorted(r["run_id"] for r in reader.runs()))
        for i, run in enumerate(results):
            with self.subTest(run=run["run_id"]):
                self.assertEqual(f"p{i}", reader.run(run["run_id"])["requested_by"])
                trace = reader.run_trace(run["run_id"])
                self.assertEqual(run["trace"]["count"], len(trace))
                self.assertEqual(3, len(trace))
                self.assertEqual({run["runtime_id"]}, {t["runtime"] for t in trace})
                # The Workflow's own Trace names this run, and no other.
                self.assertEqual([[f"{RUN['workflow']}/{run['run_id']}"]],
                                 [t["skills_used"] for t in trace
                                  if t["agent_instance"] == "workflow-participating-agent"])

    def test_parallel_runs_in_one_runtime_are_distinct(self):
        """V2 for a long-lived Runtime (the local server): its ordinals never repeat."""
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        app = AIOSApplication(Path(tmp.name), REPO_ROOT)
        app.start()
        self.addCleanup(app.stop)
        results = []
        threads = [threading.Thread(target=lambda: results.append(
            app.start_run(RUN["workflow"], RUN["inputs"], "p"))) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(60)
        self.assertEqual(8, len({r["run_id"] for r in results}))
        self.assertEqual(list(range(8)), sorted(r["execution_sequence"] for r in results))
        for run in results:
            trace = app.run_trace(run["run_id"])
            self.assertEqual([[f"{RUN['workflow']}/{run['run_id']}"]],
                             [t["skills_used"] for t in trace
                              if t["agent_instance"] == "workflow-participating-agent"])

    def test_lookup_does_not_depend_on_position(self):
        """V4: a run is found by its id wherever its record sits in the store."""
        db = FakePostgREST()
        runs = [app.start_run(RUN["workflow"], RUN["inputs"], f"p{i}")
                for i, app in enumerate(self.per_request_apps(3, db))]
        # Another writer's records and a Trace record of another Runtime land
        # between and after the runs.
        store, _ = supabase(db)
        store.append("trace", db.rows[0]["record"])
        db.rows.reverse()                     # the same records, in a new order
        for i, row in enumerate(db.rows, 1):
            row["seq"] = i
        reader = AIOSApplication(None, REPO_ROOT, storage=SupabaseStorage(URL, KEY, transport=db))
        reader.start()
        for i, run in enumerate(runs):
            with self.subTest(run=run["run_id"]):
                self.assertEqual(f"p{i}", reader.run(run["run_id"])["requested_by"])

    def test_a_failed_or_partial_run_never_lends_its_identity(self):
        """V7: a failed run keeps its own id; a run whose record was never
        written leaves Trace no other run can claim."""
        db = FakePostgREST()
        failing = [AIOSApplication(None, REPO_ROOT, storage=SupabaseStorage(URL, KEY, transport=db))]
        failing[0].start()
        failed = failing[0].start_run(RUN["workflow"], dict(RUN["inputs"], document="docs/absent.md"), "p")
        self.assertEqual("failed", failed["state"])

        # A partial run: its Trace is appended, then the run record is lost.
        partial_app = AIOSApplication(None, REPO_ROOT, storage=SupabaseStorage(URL, KEY, transport=db))
        partial_app.start()
        real_append = partial_app.storage.append

        def lose_the_run_record(partition, record):
            if partition == RUNS_PARTITION:
                raise StorageUnavailable("response lost")
            real_append(partition, record)

        partial_app.storage.append = lose_the_run_record
        with self.assertRaises(StorageUnavailable):
            partial_app.start_run(RUN["workflow"], RUN["inputs"], "p")
        partial_app.storage.append = real_append
        # The same Runtime runs again: a new ordinal, and its Trace excludes the orphan.
        after = partial_app.start_run(RUN["workflow"], RUN["inputs"], "p")
        self.assertTrue(after["run_id"].endswith("-1"))
        self.assertEqual({"runtime_from": 3, "runtime_to": 6},
                         {k: after["trace"][k] for k in ("runtime_from", "runtime_to")})

        reader = AIOSApplication(None, REPO_ROOT, storage=SupabaseStorage(URL, KEY, transport=db))
        reader.start()
        ids = [r["run_id"] for r in reader.runs()]
        self.assertEqual(2, len(set(ids)))
        self.assertNotIn(run_id_for(partial_app._boot_id, 0), ids)
        for run_id in ids:
            trace = reader.run_trace(run_id)
            self.assertEqual(reader.run(run_id)["trace"]["count"], len(trace))
            self.assertEqual([[f"{RUN['workflow']}/{run_id}"]],
                             [t["skills_used"] for t in trace
                              if t["agent_instance"] == "workflow-participating-agent"])

    def test_records_written_before_c1_are_still_read(self):
        """`fullstack.run/1` records stay as appended and stay addressable."""
        db = FakePostgREST()
        store, _ = supabase(db)
        legacy = {"format": LEGACY_RUN_FORMAT, "run_id": "run-00001", "requested_by": "old",
                  "runtime_id": "aios-fullstack/legacy", "trace": {"from": 0, "to": 0, "count": 0}}
        store.append(RUNS_PARTITION, json.dumps(legacy).encode())
        app = AIOSApplication(None, REPO_ROOT, storage=SupabaseStorage(URL, KEY, transport=db))
        app.start()
        new = app.start_run(RUN["workflow"], RUN["inputs"], "p")
        self.assertEqual(RUN_FORMAT, new["format"])
        self.assertEqual("old", app.run("run-00001")["requested_by"])
        self.assertEqual([], app.run_trace("run-00001"))
        self.assertEqual([new["run_id"], "run-00001"], [r["run_id"] for r in app.runs()])

    def test_run_ids_fit_the_api_pattern_and_bad_boot_ids_are_refused(self):
        app = AIOSApplication(None, REPO_ROOT, storage=supabase()[0])
        app.start()
        run = app.start_run(RUN["workflow"], RUN["inputs"], "p")
        self.assertRegex(run["run_id"], r"^run-\d{8}T\d{6}Z-[0-9a-f]{16}-0$")
        for bad in ("has/slash", "under_score", "x" * 41):
            with self.subTest(boot_id=bad), self.assertRaises(ValueError):
                AIOSApplication(None, REPO_ROOT, storage=supabase()[0], boot_id=bad)


class TheVercelConfiguration(unittest.TestCase):
    """B1: the console as static assets, the API as one Python function."""

    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((REPO_ROOT / "vercel.json").read_text(encoding="utf-8"))

    def test_the_console_is_static_and_the_api_is_the_function(self):
        self.assertEqual("fullstack/frontend", self.config["outputDirectory"])
        self.assertTrue((REPO_ROOT / "fullstack/frontend/index.html").is_file())
        self.assertIn({"source": "/api/v1/:path*", "destination": "/api/index"},
                      self.config["rewrites"])
        self.assertIn({"source": "/assets/:file", "destination": "/:file"},
                      self.config["rewrites"])
        self.assertEqual(["api/index.py"], list(self.config["functions"]))
        self.assertEqual(["index.py"], sorted(p.name for p in (REPO_ROOT / "api").iterdir()
                                              if p.suffix == ".py"))

    def test_the_static_console_carries_the_backend_page_headers(self):
        (rule,) = self.config["headers"]
        headers = {h["key"]: h["value"] for h in rule["headers"]}
        self.assertEqual(api_module.PAGE_CSP, headers["Content-Security-Policy"])
        for name, value in api_module.BASE_HEADERS:
            self.assertEqual(value, headers[name])
        self.assertEqual("/((?!api/).*)", rule["source"])

    def test_the_entrypoint_installs_the_barrier_and_exports_the_adapter(self):
        source = (REPO_ROOT / "api/index.py").read_text(encoding="utf-8")
        self.assertLess(source.index("import tools"), source.index("from fullstack"))
        self.assertIn("from fullstack.deploy.vercel import app", source)

    def test_no_secret_is_in_the_repository_configuration(self):
        for path in [REPO_ROOT / "vercel.json", REPO_ROOT / "api/index.py",
                     REPO_ROOT / "fullstack/deploy/vercel.py", *MIGRATIONS.iterdir()]:
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"sb_secret_|sb_publishable_|eyJhbGci", text), path)


class TheMigration(unittest.TestCase):
    """Only the schema the StorageFacility contract requires (FS-ARCH-RAT-001 `§3.2`)."""

    @classmethod
    def setUpClass(cls):
        (cls.path,) = sorted(MIGRATIONS.glob("*.sql"))
        cls.sql = cls.path.read_text(encoding="utf-8")
        cls.code = "\n".join(l.split("--")[0] for l in cls.sql.splitlines()).lower()

    def test_one_table_one_listing_function_one_guard(self):
        self.assertEqual(["public.aios_records"], re.findall(r"create table ([\w.]+)", self.code))
        self.assertEqual(["public.aios_records_refuse_mutation", "public.aios_partitions"],
                         re.findall(r"create function ([\w.]+)", self.code))
        self.assertEqual(["seq", "partition", "record"],
                         re.findall(r"^\s{4}(\w+)\s+(?:bigint|text|bytea)", self.code, re.M))

    def test_no_generic_tables(self):
        for name in ("users", "agents", "messages", "documents"):
            self.assertNotRegex(self.code, rf"create table [\w.]*\b{name}\b")

    def test_append_only_and_no_browser_path(self):
        self.assertIn("before update or delete on public.aios_records", self.code)
        self.assertIn("before truncate on public.aios_records", self.code)
        self.assertIn("enable row level security", self.code)
        self.assertNotIn("create policy", self.code)
        self.assertIn("revoke all on table public.aios_records from public, anon, "
                      "authenticated, service_role", self.code)
        self.assertIn("grant select, insert on table public.aios_records to service_role",
                      self.code)
        self.assertNotRegex(self.code, r"grant [^;]*(update|delete|truncate)")

    def test_it_is_named_by_the_version_the_project_applied(self):
        self.assertEqual("20260927062422_aios_records.sql", self.path.name)


if __name__ == "__main__":
    unittest.main()
