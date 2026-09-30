"""FS-DP-06 L1: one structured JSON line per request (ACT-004 DG-02; Register `§93`).

Operational telemetry, kept apart from the two accountability records AIOS
already has: Trace (what an Agent Instance did, authored by AIOS) and Audit
(who was allowed or refused what). Telemetry says how the service behaved:

    {"at": ..., "format": "fullstack.request/1", "latency_ms": 3.2,
     "method": "GET", "request_id": "…", "route": "/api/v1/runs/{run_id}",
     "runtime_id": "aios-fullstack/…", "status": 200}

A line never carries the Authorization header, a token or its hash, a request
body, a document's contents or a database key. It names the route **template**,
never the raw path, so no identifier or input reaches the log. The host's
function log collects stdout; metrics are derived from these lines (M1,
`fullstack/deploy/request_metrics.py`). `request_id` equals the response's
`X-Request-Id` and the audit entry's `request_id`: the only join between them.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from typing import Callable, List, Optional

FORMAT = "fullstack.request/1"
FIELDS = ("at", "format", "latency_ms", "method", "request_id", "route",
          "runtime_id", "status")

Sink = Callable[[str], None]


def line(*, request_id: str, method: str, route: str, status: int,
         latency_ms: float, runtime_id: Optional[str],
         at: Optional[str] = None) -> str:
    """One request, as one line of sorted-key JSON."""
    return json.dumps({
        "at": at or datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "format": FORMAT, "latency_ms": round(float(latency_ms), 2),
        "method": str(method)[:16], "request_id": request_id, "route": route,
        "runtime_id": runtime_id, "status": int(status)}, sort_keys=True,
        separators=(",", ":"))


def stdout_sink(text: str) -> None:
    """The deployed default: stdout, which the host's function log collects."""
    print(text, file=sys.stdout, flush=True)


class Collector:
    """A sink that keeps the lines, for tests and in-process tools."""

    def __init__(self) -> None:
        self.lines: List[str] = []

    def __call__(self, text: str) -> None:
        self.lines.append(text)

    def records(self) -> List[dict]:
        return [json.loads(text) for text in self.lines]
