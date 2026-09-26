"""The HTTP layer: a WSGI application serving API contract v1 and the console.

Every API request passes the same sequence, and none skips a step:

```text
match route → authenticate (port) → authorize (scope) → audit → handle → respond
```

The frontend is served from the same origin, so no CORS is configured
(`FS-DP-03`). Responses carry the security headers of FS-02 `§6`; an error
carries `{"error", "detail"}` and never a traceback.
"""

from __future__ import annotations

import json
import mimetypes
import secrets
import sys
import traceback
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Tuple
from urllib.parse import parse_qs

from . import contract
from .aios import AIOSApplication, InvalidRunRequest, NotRunning, UnknownWorkflow
from .security import PUBLIC, AuditLedger, Authenticator, authorize

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
STATIC_TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
                ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml"}

BASE_HEADERS = (
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "no-referrer"),
    ("X-Frame-Options", "DENY"),
    ("Cross-Origin-Opener-Policy", "same-origin"),
)
API_CSP = "default-src 'none'; frame-ancestors 'none'"
PAGE_CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
            "connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")


class _Refusal(Exception):
    def __init__(self, status: int, detail: str, headers: Tuple = ()):
        super().__init__(detail)
        self.status, self.detail, self.headers = status, detail, headers


class Application:
    """The WSGI callable. Holds no AIOS state of its own."""

    def __init__(self, aios: AIOSApplication, authenticator: Authenticator,
                 audit: AuditLedger, frontend_dir: Path = FRONTEND_DIR,
                 request_id: Callable[[], str] = lambda: secrets.token_hex(8)):
        self._aios = aios
        self._authenticator = authenticator
        self._audit = audit
        self._frontend = Path(frontend_dir).resolve()
        self._request_id = request_id

    def __call__(self, environ, start_response) -> Iterable[bytes]:
        request_id = self._request_id()
        path = environ.get("PATH_INFO") or "/"
        if path.startswith("/api/"):
            status, headers, body = self._api(environ, path, request_id)
        else:
            status, headers, body = self._static(environ, path)
        headers = list(headers) + list(BASE_HEADERS) + [("X-Request-Id", request_id),
                                                        ("Content-Length", str(len(body)))]
        start_response(f"{status} {_reason(status)}", headers)
        return [body] if environ.get("REQUEST_METHOD") != "HEAD" else [b""]

    # -- API ------------------------------------------------------------------

    def _api(self, environ, path, request_id):
        method = environ.get("REQUEST_METHOD", "GET")
        route, params, allowed = contract.match(method, path)
        try:
            if route is None:
                if allowed:
                    raise _Refusal(405, f"{method} is not allowed on {path}",
                                   (("Allow", ", ".join(allowed)),))
                raise _Refusal(404, f"no route {path}")
            principal = self._authenticate(environ)
            decision = authorize(principal, route.scope)
            if route.scope != PUBLIC:
                self._audit.record(request_id=request_id, subject=decision.subject,
                                   method=method, path=path, scope=route.scope,
                                   decision="allowed" if decision.allowed else "refused",
                                   status=decision.status)
            if not decision.allowed:
                raise _Refusal(decision.status,
                               "no authenticated principal" if decision.status == 401
                               else f"scope {route.scope} is required")
            status, payload = getattr(self, "_h_" + route.handler)(environ, params, principal)
            return self._json(status, payload)
        except _Refusal as refusal:
            return self._json(refusal.status, {"error": contract.ERRORS[refusal.status],
                                               "detail": refusal.detail}, refusal.headers)
        except InvalidRunRequest as error:
            return self._json(400, {"error": "invalid_request", "detail": str(error)})
        except UnknownWorkflow as error:
            return self._json(400, {"error": "invalid_request", "detail": str(error)})
        except NotRunning as error:
            return self._json(503, {"error": "unavailable", "detail": str(error)})
        except Exception:
            # Logged for the operator, never returned to the caller.
            print(f"[{request_id}] internal error on {method} {path}\n"
                  + traceback.format_exc(), file=sys.stderr)
            return self._json(500, {"error": "internal_error",
                                    "detail": f"request {request_id} failed"})

    def _authenticate(self, environ):
        headers = {k[5:].lower().replace("_", "-"): v
                   for k, v in environ.items() if k.startswith("HTTP_")}
        try:
            return self._authenticator.authenticate(headers)
        except Exception:
            return None  # fail closed: a broken authenticator authenticates nobody

    @staticmethod
    def _json(status, payload, extra=()):
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return status, [("Content-Type", "application/json; charset=utf-8"),
                        ("Cache-Control", "no-store"),
                        ("Content-Security-Policy", API_CSP), *extra], body

    @staticmethod
    def _page(environ) -> Tuple[int, int]:
        query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)
        try:
            offset = int(query.get("offset", ["0"])[0])
            limit = int(query.get("limit", ["50"])[0])
        except ValueError:
            raise _Refusal(400, "offset and limit must be integers") from None
        if offset < 0 or not 1 <= limit <= contract.MAX_PAGE:
            raise _Refusal(400, f"offset ≥ 0 and 1 ≤ limit ≤ {contract.MAX_PAGE}")
        return offset, limit

    @staticmethod
    def _body(environ) -> dict:
        try:
            length = int(environ.get("CONTENT_LENGTH") or 0)
        except ValueError:
            raise _Refusal(400, "invalid Content-Length") from None
        if length > contract.MAX_BODY_BYTES:
            raise _Refusal(413, f"the body limit is {contract.MAX_BODY_BYTES} bytes")
        if not (environ.get("CONTENT_TYPE") or "").startswith("application/json"):
            raise _Refusal(400, "the body must be application/json")
        raw = environ["wsgi.input"].read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8") or "null")
        except (UnicodeDecodeError, ValueError):
            raise _Refusal(400, "the body is not valid JSON") from None
        if not isinstance(body, dict):
            raise _Refusal(400, "the body must be a JSON object")
        return body

    # -- handlers -------------------------------------------------------------

    def _h_health(self, environ, params, principal):
        return 200, self._aios.health()

    def _h_session(self, environ, params, principal):
        return 200, {"subject": principal.subject, "scopes": sorted(principal.scopes)}

    def _h_runtime(self, environ, params, principal):
        return 200, dict(self._aios.runtime_status(),
                         authentication=self._authenticator.mechanism)

    def _h_tools(self, environ, params, principal):
        return 200, {"tools": self._aios.tools()}

    def _h_invocations(self, environ, params, principal):
        return 200, {"invocations": self._aios.invocations()}

    def _h_workflows(self, environ, params, principal):
        return 200, {"workflows": self._aios.catalog()}

    def _h_runs(self, environ, params, principal):
        return 200, {"runs": self._aios.runs()}

    def _h_run(self, environ, params, principal):
        run = self._aios.run(params["run_id"])
        if run is None:
            raise _Refusal(404, f"no run {params['run_id']}")
        return 200, run

    def _h_start_run(self, environ, params, principal):
        body = self._body(environ)
        unknown = set(body) - {"workflow", "inputs"}
        if unknown:
            raise _Refusal(400, f"unknown field(s): {sorted(unknown)}")
        if not isinstance(body.get("workflow"), str):
            raise _Refusal(400, "workflow must name a catalog entry")
        return 201, self._aios.start_run(body["workflow"], body.get("inputs"),
                                         requested_by=principal.subject)

    def _h_traces(self, environ, params, principal):
        offset, limit = self._page(environ)
        return 200, self._aios.traces(offset, limit)

    def _h_audit(self, environ, params, principal):
        offset, limit = self._page(environ)
        return 200, {"offset": offset, "limit": limit,
                     "entries": self._audit.page(offset, limit)}

    # -- static frontend ------------------------------------------------------

    def _static(self, environ, path):
        method = environ.get("REQUEST_METHOD", "GET")
        if method not in ("GET", "HEAD"):
            return self._json(405, {"error": "method_not_allowed",
                                    "detail": "the console is read-only"},
                              (("Allow", "GET, HEAD"),))
        name = "index.html" if path in ("/", "/index.html") else (
            path[len("/assets/"):] if path.startswith("/assets/") else None)
        target = self._resolve(name)
        if target is None:
            return self._json(404, {"error": "not_found", "detail": f"no page {path}"})
        headers = [("Content-Type", STATIC_TYPES[target.suffix]),
                   ("Cache-Control", "no-cache"),
                   ("Content-Security-Policy", PAGE_CSP)]
        return 200, headers, target.read_bytes()

    def _resolve(self, name: Optional[str]) -> Optional[Path]:
        if not name or "/" in name or "\\" in name or name.startswith("."):
            return None
        target = (self._frontend / name).resolve()
        if target.parent != self._frontend or target.suffix not in STATIC_TYPES:
            return None
        return target if target.is_file() else None


def _reason(status: int) -> str:
    return {200: "OK", 201: "Created", 400: "Bad Request", 401: "Unauthorized",
            403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed",
            413: "Payload Too Large", 500: "Internal Server Error",
            503: "Service Unavailable"}.get(status, "Unknown")


def create_app(data_dir: Path, repo_root: Path, authenticator: Authenticator,
               **aios_options) -> Tuple[Application, AIOSApplication]:
    """Build and start the application: one AIOS Runtime, the API over it."""
    aios = AIOSApplication(data_dir=data_dir, repo_root=repo_root, **aios_options)
    aios.start()
    return Application(aios, authenticator, AuditLedger(aios.storage)), aios
