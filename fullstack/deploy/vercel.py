"""The Vercel Python function: one AIOS Runtime per request (FS-DP-04 A1, B1;
ratified `FS-ARCH-RAT-001`, Register `§68`).

```text
HTTP request → this adapter → Application (API v1) → AIOSApplication
            → AIOS public contracts → StorageFacility → SupabaseStorage → aios_records
```

For every request the adapter:

1. resolves the deployment environment (`VERCEL_ENV`) and builds the store for
   it, `SupabaseStorage` on that environment's project (FS-09-ENV E1: Preview
   `scfymftfzkpilqbgmfwv`, Production `hmljfyqycxcueulhsjae`), with the
   server-side key from the same environment. An environment that is neither
   `preview` nor `production` (absent, `development`, misspelt) resolves to no
   store: every API route answers 503 and no database is called;
2. bootstraps a fresh Runtime on it (`AIOSApplication.start`), whose identity
   is unique to this request;
3. serves the request through the unchanged API v1 `Application`: the same
   routing, authentication port, scopes, audit, errors and headers as locally;
4. stops the Runtime before returning.

**Function-local memory is not state.** Nothing is kept between requests in
this process: runs, Trace and audit are read from and appended to the database.
There is no fallback to the function's filesystem. Without a key, or with the
database unreachable, every API route answers 503 (Fail Closed).

The static console is served by Vercel from `fullstack/frontend` (`vercel.json`);
this function answers only `/api/`.

Authentication is FS-DP-02 B3 (Architect decision, Register `§81`): operator
bearer tokens verified against the hashes in `AIOS_OPERATOR_TOKENS`, read from
the environment when the function loads. Without that variable, or with one
that does not parse, nobody is authenticated and every protected route answers
401, as locally.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import sys
import time
import traceback
from pathlib import Path
from typing import Callable, Iterable, Mapping, Optional

from fullstack.backend.aios import AIOSApplication
from fullstack.backend import telemetry
from fullstack.backend.api import API_CSP, BASE_HEADERS, Application, _reason
from fullstack.backend.contract import match
from fullstack.backend.security import (
    AuditLedger, Authenticator, NoAuthenticator, OperatorTokenAuthenticator)
from fullstack.backend.supabase_storage import SupabaseStorage, StorageUnavailable

REPO_ROOT = Path(__file__).resolve().parents[2]
#: FS-09-ENV E1 (ACT-004 DG-04, Register `§93`): one Supabase project per
#: deployment environment, amending FS-ARCH-RAT-001 `§11.1` from one project to
#: one per environment. Fixed in code, keyed by Vercel's own `VERCEL_ENV`, so
#: the deployment cannot be pointed at another database by a variable an
#: operator sets. Each environment's key is a Vercel variable scoped to that
#: environment alone.
SUPABASE_PROJECTS = {
    "preview": "https://scfymftfzkpilqbgmfwv.supabase.co",
    "production": "https://hmljfyqycxcueulhsjae.supabase.co",
}
#: The Preview project (the ratified project of FS-ARCH-RAT-001 `§11.1`).
SUPABASE_PROJECT_URL = SUPABASE_PROJECTS["preview"]
#: The variable Vercel sets on every deployment: `production`, `preview` or
#: `development`. Only the first two name a project; anything else is refused.
ENVIRONMENT_VARIABLE = "VERCEL_ENV"
#: Where the operator puts the server-side key, first match wins. The value is
#: read here and handed to the store; it is never logged or returned.
KEY_VARIABLES = ("SUPABASE_SECRET_KEY", "SUPABASE_SERVICE_ROLE_KEY")


#: What a Supabase server-side key is made of (a secret API key or a JWT).
#: A value with anything else (a line break, space, quote, non-ASCII) cannot be
#: sent as a header and is refused before any database call.
_KEY_SHAPE = re.compile(r"[A-Za-z0-9._~+/=-]+")


class MalformedKey(ValueError):
    """The configured key cannot be sent. The message never quotes it."""


class UnknownEnvironment(ValueError):
    """The deployment environment names no project (FS-09-ENV E1, Fail Closed).
    The message never quotes the observed value."""


def project_url_for(environment: Mapping[str, str] = os.environ) -> str:
    """The Supabase project of this deployment's environment, or refuse.

    The value must be exactly `preview` or `production`, as Vercel sets it. It
    is never trimmed, folded or defaulted: a deployment whose environment
    cannot be read safely must not guess a database."""
    name = environment.get(ENVIRONMENT_VARIABLE)
    if name not in SUPABASE_PROJECTS:
        raise UnknownEnvironment(
            f"the deployment environment ({ENVIRONMENT_VARIABLE}) is not 'preview' or "
            "'production', so no database is selected")
    return SUPABASE_PROJECTS[name]


def storage_from_environment(environment: Mapping[str, str] = os.environ,
                             **options) -> Optional[SupabaseStorage]:
    project_url = project_url_for(environment)   # refuses before any key is read
    key = next((environment[v] for v in KEY_VARIABLES if environment.get(v, "").strip()),
               None)
    if key is None:
        return None
    key = key.strip()
    if not _KEY_SHAPE.fullmatch(key):
        raise MalformedKey("the server-side database key contains a character that cannot "
                           "be sent (a line break, space, quote or non-ASCII character); "
                           "enter it again as one line")
    return SupabaseStorage(project_url, key, **options)


def _refusal(start_response, status: int, error: str, detail: str,
             request_id: Optional[str] = None):
    body = json.dumps({"error": error, "detail": detail},
                      separators=(",", ":")).encode("utf-8")
    start_response(f"{status} {_reason(status)}", [
        ("Content-Type", "application/json; charset=utf-8"), ("Cache-Control", "no-store"),
        ("Content-Security-Policy", API_CSP), *BASE_HEADERS,
        ("X-Request-Id", request_id or secrets.token_hex(8)),
        ("Content-Length", str(len(body)))])
    return [body]


def authenticator_from_environment(
        environment: Mapping[str, str] = os.environ) -> OperatorTokenAuthenticator:
    """FS-DP-02 B3. The configuration holds hashes only; a refused one is
    reported by its reason, never by its value."""
    authenticator = OperatorTokenAuthenticator.from_environment(environment)
    if authenticator.configuration_error not in (None, "not configured"):
        print(f"AIOS_OPERATOR_TOKENS {authenticator.configuration_error}; "
              "nobody is authenticated", file=sys.stderr)
    return authenticator


def make_app(storage_factory: Callable[[], Optional[object]] = storage_from_environment,
             authenticator: Optional[Authenticator] = None,
             repo_root: Path = REPO_ROOT,
             telemetry_sink: Optional[telemetry.Sink] = telemetry.stdout_sink,
             **aios_options):
    """The WSGI callable Vercel invokes. Each call is one request, one Runtime.

    FS-DP-06 L1: every request yields one line. A request refused before the
    Application runs (the 503 fail-closed paths) gets its line here, with no
    Runtime; every other request gets it from the Application."""
    authenticator = authenticator or authenticator_from_environment()

    def app(environ, start_response) -> Iterable[bytes]:
        started = time.perf_counter()
        path = environ.get("PATH_INFO") or ""
        method = environ.get("REQUEST_METHOD", "GET")

        def refuse(status, error, detail):
            request_id = secrets.token_hex(8)
            body = _refusal(start_response, status, error, detail, request_id)
            if telemetry_sink is not None:
                route = match(method, path)[0] if path.startswith("/api/") else None
                try:
                    telemetry_sink(telemetry.line(
                        request_id=request_id, method=method,
                        route=route.template if route is not None else "(unmatched)",
                        status=status, latency_ms=(time.perf_counter() - started) * 1000,
                        runtime_id=None))
                except Exception:
                    pass  # telemetry never changes a response
            return body

        if not path.startswith("/api/"):
            return refuse(404, "not_found",
                          "this function serves /api/ only; the console is static")
        try:
            storage = storage_factory()
        except (MalformedKey, UnknownEnvironment) as error:
            print(f"storage not configured: {error}", file=sys.stderr)
            return refuse(503, "unavailable", str(error))
        if storage is None:
            return refuse(503, "unavailable",
                          "persistence is not configured: the operator has not set "
                          "the server-side database key")
        aios = AIOSApplication(None, repo_root, storage=storage, **aios_options)
        try:
            aios.start()
        except Exception as error:
            print(f"runtime start failed: {type(error).__name__}: "
                  f"{error if isinstance(error, StorageUnavailable) else ''}", file=sys.stderr)
            return refuse(503, "unavailable", "the AIOS Runtime could not start on its store")
        try:
            api = Application(aios, authenticator, AuditLedger(aios.storage),
                              telemetry_sink=telemetry_sink)
            # Materialize the body while the Runtime is running.
            return [b"".join(api(environ, start_response))]
        except Exception:
            print("request failed after start\n" + traceback.format_exc(), file=sys.stderr)
            return refuse(503, "unavailable", "the request could not complete")
        finally:
            aios.stop()

    return app


app = make_app()
