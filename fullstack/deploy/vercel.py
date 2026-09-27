"""The Vercel Python function: one AIOS Runtime per request (FS-DP-04 A1, B1;
ratified `FS-ARCH-RAT-001`, Register `§68`).

```text
HTTP request → this adapter → Application (API v1) → AIOSApplication
            → AIOS public contracts → StorageFacility → SupabaseStorage → aios_records
```

For every request the adapter:

1. builds the ratified store, `SupabaseStorage` on project
   `scfymftfzkpilqbgmfwv`, with the server-side key from the environment;
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

Authentication is `NoAuthenticator` until FS-DP-02 is ratified, so every
protected route answers 401, as locally.
"""

from __future__ import annotations

import json
import os
import secrets
import sys
import traceback
from pathlib import Path
from typing import Callable, Iterable, Mapping, Optional

from fullstack.backend.aios import AIOSApplication
from fullstack.backend.api import API_CSP, BASE_HEADERS, Application, _reason
from fullstack.backend.security import AuditLedger, Authenticator, NoAuthenticator
from fullstack.backend.supabase_storage import SupabaseStorage, StorageUnavailable

REPO_ROOT = Path(__file__).resolve().parents[2]
#: The ratified project (FS-ARCH-RAT-001 `§11.1`). Not configurable, so the
#: deployment cannot be pointed at another database by an environment variable.
SUPABASE_PROJECT_URL = "https://scfymftfzkpilqbgmfwv.supabase.co"
#: Where the operator puts the server-side key, first match wins. The value is
#: read here and handed to the store; it is never logged or returned.
KEY_VARIABLES = ("SUPABASE_SECRET_KEY", "SUPABASE_SERVICE_ROLE_KEY")


def storage_from_environment(environment: Mapping[str, str] = os.environ,
                             **options) -> Optional[SupabaseStorage]:
    key = next((environment[v] for v in KEY_VARIABLES if environment.get(v, "").strip()),
               None)
    return SupabaseStorage(SUPABASE_PROJECT_URL, key.strip(), **options) if key else None


def _refusal(start_response, status: int, error: str, detail: str):
    body = json.dumps({"error": error, "detail": detail},
                      separators=(",", ":")).encode("utf-8")
    start_response(f"{status} {_reason(status)}", [
        ("Content-Type", "application/json; charset=utf-8"), ("Cache-Control", "no-store"),
        ("Content-Security-Policy", API_CSP), *BASE_HEADERS,
        ("X-Request-Id", secrets.token_hex(8)), ("Content-Length", str(len(body)))])
    return [body]


def make_app(storage_factory: Callable[[], Optional[object]] = storage_from_environment,
             authenticator: Optional[Authenticator] = None,
             repo_root: Path = REPO_ROOT, **aios_options):
    """The WSGI callable Vercel invokes. Each call is one request, one Runtime."""
    authenticator = authenticator or NoAuthenticator()

    def app(environ, start_response) -> Iterable[bytes]:
        if not (environ.get("PATH_INFO") or "").startswith("/api/"):
            return _refusal(start_response, 404, "not_found",
                            "this function serves /api/ only; the console is static")
        storage = storage_factory()
        if storage is None:
            return _refusal(start_response, 503, "unavailable",
                            "persistence is not configured: the operator has not set "
                            "the server-side database key")
        aios = AIOSApplication(None, repo_root, storage=storage, **aios_options)
        try:
            aios.start()
        except Exception as error:
            print(f"runtime start failed: {type(error).__name__}: "
                  f"{error if isinstance(error, StorageUnavailable) else ''}", file=sys.stderr)
            return _refusal(start_response, 503, "unavailable",
                            "the AIOS Runtime could not start on its store")
        try:
            api = Application(aios, authenticator, AuditLedger(aios.storage))
            # Materialize the body while the Runtime is running.
            return [b"".join(api(environ, start_response))]
        except Exception:
            print("request failed after start\n" + traceback.format_exc(), file=sys.stderr)
            return _refusal(start_response, 503, "unavailable", "the request could not complete")
        finally:
            aios.stop()

    return app


app = make_app()
