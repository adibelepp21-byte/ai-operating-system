"""FS-DP-06 M1: metrics derived from the L1 request lines (ACT-004 DG-02; Register `§93`).

There is no metrics emitter. The application writes one `fullstack.request/1`
line per request (`fullstack/backend/telemetry.py`); the host's function log
keeps them; this module derives request volume, status classes and latency from
whatever lines it is given: a local capture, or log messages exported from the
host. Lines that are not request lines (the host's own messages, tracebacks)
are counted as ignored, never guessed at.

    python -m fullstack.backend metrics --log <file>

Metrics are operational visibility only. They decide nothing (ACT-004 `§11`).
"""

from __future__ import annotations

import json
import statistics
from typing import Dict, Iterable, List

from fullstack.backend.telemetry import FORMAT


def request_lines(texts: Iterable[str]) -> List[dict]:
    """The request lines among `texts`; anything else is left out."""
    found = []
    for text in texts:
        text = text.strip()
        start = text.find("{")
        if start < 0:
            continue
        try:
            record = json.loads(text[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict) and record.get("format") == FORMAT:
            found.append(record)
    return found


def _percentile(values: List[float], fraction: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round(fraction * (len(ordered) - 1))))
    return round(ordered[index], 2)


def _summary(records: List[dict]) -> dict:
    latencies = [float(r["latency_ms"]) for r in records]
    classes: Dict[str, int] = {}
    for r in records:
        key = f"{int(r['status']) // 100}xx"
        classes[key] = classes.get(key, 0) + 1
    return {"requests": len(records), "status_classes": dict(sorted(classes.items())),
            "server_errors": sum(1 for r in records if int(r["status"]) >= 500),
            "latency_ms": {"p50": round(statistics.median(latencies), 2),
                           "p95": _percentile(latencies, 0.95),
                           "max": round(max(latencies), 2)} if latencies else None}


def derive(texts: Iterable[str]) -> dict:
    """Totals and per-route figures from the request lines in `texts`."""
    texts = list(texts)
    records = request_lines(texts)
    routes: Dict[str, List[dict]] = {}
    for r in records:
        routes.setdefault(f"{r['method']} {r['route']}", []).append(r)
    return {"lines_read": len(texts), "ignored": len(texts) - len(records),
            "total": _summary(records),
            "routes": {name: _summary(rs) for name, rs in sorted(routes.items())},
            "runtimes": len({r["runtime_id"] for r in records if r.get("runtime_id")})}
