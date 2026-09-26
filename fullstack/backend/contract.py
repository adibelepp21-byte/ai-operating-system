"""API contract v1, as data (FS-02 `§4`).

The router serves exactly these routes, and
`fullstack/tests/test_api_contract.py` holds the FS-02 blueprint's table to
the same list, so the published contract and the running code cannot drift
apart unnoticed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Tuple

from .security import AUDIT, AUTHENTICATED, OBSERVE, PUBLIC, RUN_WORKFLOW

API_VERSION = "v1"
BASE = f"/api/{API_VERSION}"
MAX_BODY_BYTES = 64 * 1024
MAX_PAGE = 200
ERRORS = {400: "invalid_request", 401: "unauthenticated", 403: "forbidden",
          404: "not_found", 405: "method_not_allowed", 413: "payload_too_large",
          500: "internal_error", 503: "unavailable"}


@dataclass(frozen=True)
class Route:
    method: str
    template: str
    scope: str
    handler: str

    @property
    def pattern(self) -> "re.Pattern":
        return re.compile("^" + re.sub(r"\{(\w+)\}", r"(?P<\1>[A-Za-z0-9-]{1,64})",
                                       self.template) + "$")


ROUTES: Tuple[Route, ...] = (
    Route("GET", f"{BASE}/health", PUBLIC, "health"),
    Route("GET", f"{BASE}/session", AUTHENTICATED, "session"),
    Route("GET", f"{BASE}/runtime", OBSERVE, "runtime"),
    Route("GET", f"{BASE}/tools", OBSERVE, "tools"),
    Route("GET", f"{BASE}/tools/invocations", OBSERVE, "invocations"),
    Route("GET", f"{BASE}/workflows", OBSERVE, "workflows"),
    Route("GET", f"{BASE}/runs", OBSERVE, "runs"),
    Route("GET", f"{BASE}/runs/{{run_id}}", OBSERVE, "run"),
    Route("POST", f"{BASE}/runs", RUN_WORKFLOW, "start_run"),
    Route("GET", f"{BASE}/traces", OBSERVE, "traces"),
    Route("GET", f"{BASE}/audit", AUDIT, "audit"),
)


def match(method: str, path: str) -> Tuple[Optional[Route], dict, Tuple[str, ...]]:
    """The route for (method, path), its path parameters, and the methods the
    path allows. `(None, {}, ())` means no such path."""
    allowed, found, params = [], None, {}
    for route in ROUTES:
        m = route.pattern.match(path)
        if m:
            allowed.append(route.method)
            if route.method == method:
                found, params = route, m.groupdict()
    return found, params, tuple(allowed)
