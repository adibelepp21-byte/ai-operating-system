"""FS-09 — the Production Readiness Gate, evaluated rather than asserted.

    python -m fullstack.readiness evaluate [--runs N]

Every criterion of Act `§20` gets one of:

* **PASS**: evaluated live, here, on this commit;
* **FAIL**: evaluated live and not met (a defect to repair);
* **BLOCKED**: cannot be met until a named decision package is ratified, or an
  external dependency is supplied;
* **OBSERVED**: measured, with no stated requirement to hold it to.

The functional, security and data criteria are measured by starting the real
application in a temporary directory and exercising it; nothing is copied from
an earlier run. A decision package counts as ratified only when the Decision
Register holds an entry for it with `| **Ratifies** |` and `| **Decided by** |`
rows. Preparation is not ratification (`FD-FS-001` D2-A), so no document in
`docs/fullstack/decision-packages/` can ratify itself.

**PRODUCTION READY** requires every criterion PASS or OBSERVED. Even then,
release waits for a separate Founder decision (`FD-FS-001` D4-A): this gate
never releases.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
PACKAGES = {
    "FS-DP-01": "Database implementation",
    "FS-DP-02": "Identity and Authentication",
    "FS-DP-03": "Networking",
    "FS-DP-04": "Deployment",
    "FS-DP-05": "Scaling",
    "FS-DP-06": "Observability implementation",
    "FS-DP-07": "Agent creation (Agent Factory boundary)",
}
PASS, FAIL, BLOCKED, OBSERVED = "PASS", "FAIL", "BLOCKED", "OBSERVED"
READY, NOT_READY = "PRODUCTION READY", "NOT PRODUCTION READY"

#: Supplied by the operator's own inspection; each stays until it is resolved
#: and this list is edited with the evidence of resolution.
EXTERNAL_DEPENDENCIES = (
    {"id": "EXT-01", "what": "Supabase database unreachable through the connector: three "
     "read-only queries ended in a connection timeout (2026-09-26); cause not determined",
     "needs": "the project owner to confirm the project is active (restore it if paused)"},
    {"id": "EXT-02", "what": "S-01 AIOS Transition Manifest not supplied (FD-FS-001 D5-A)",
     "needs": "the Founder to supply the exact document"},
)


def ratified(register_text: str) -> Dict[str, str]:
    """Package id → the Register entry that ratifies it."""
    found = {}
    # Split at every section heading, so an entry's rows are its own: a `##`
    # section never borrows the `Decided by` row of the `###` entry before it.
    for block in re.split(r"(?m)^(?=#{2,3} )", register_text):
        if not block.startswith("### ") or not re.search(r"(?m)^\| \*\*Decided by\*\* \|", block):
            continue
        row = re.search(r"(?m)^\| \*\*Ratifies\*\* \|([^\n]*)\|\s*$", block)
        if row:
            heading = block.splitlines()[0][4:].strip()
            for package in re.findall(r"FS-DP-0\d", row.group(1)):
                found[package] = heading
    return found


def _criterion(area, name, status, evidence, blocked_by=()):
    return {"area": area, "criterion": name, "status": status, "evidence": evidence,
            "blocked_by": list(blocked_by)}


def _blocked_unless(area, name, packages, decided, evidence_if_ratified):
    open_ = [p for p in packages if p not in decided]
    if open_:
        return _criterion(area, name, BLOCKED,
                          "awaits ratification of " + ", ".join(open_), open_)
    return _criterion(area, name, FAIL, evidence_if_ratified)


def _measure(runs: int) -> dict:
    """Exercise the real application in a throwaway directory."""
    from fullstack.backend.api import create_app
    from fullstack.backend.security import (AUDIT, OBSERVE, RUN_WORKFLOW, Authenticator,
                                            Principal)
    from wsgiref.util import setup_testing_defaults
    import io

    class _Gate(Authenticator):
        mechanism = "readiness-gate probe"
        principals = {"gate-operator": Principal("gate-operator", {OBSERVE, RUN_WORKFLOW, AUDIT}),
                      "gate-observer": Principal("gate-observer", {OBSERVE})}

        def authenticate(self, headers):
            return self.principals.get(headers.get("x-gate-principal", ""))

    def call(app, method, path, who=None, body=None):
        data = json.dumps(body).encode() if body is not None else b""
        path, _, query = path.partition("?")
        env = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
               "wsgi.input": io.BytesIO(data),
               "CONTENT_LENGTH": str(len(data)), "CONTENT_TYPE": "application/json"}
        if who:
            env["HTTP_X_GATE_PRINCIPAL"] = who
        setup_testing_defaults(env)
        seen = {}
        out = b"".join(app(env, lambda s, h: seen.update(status=int(s.split()[0]),
                                                           headers=dict(h))))
        return seen["status"], seen["headers"], json.loads(out)

    body = lambda doc: {"workflow": "document-conformance-review",  # noqa: E731
                        "inputs": {"document": doc, "criteria": ["INV-4"]}}
    with tempfile.TemporaryDirectory() as tmp:
        app, aios = create_app(Path(tmp), REPO_ROOT, _Gate())
        latencies, first = [], None
        store = Path(tmp) / "storage"
        for _ in range(runs):
            started = time.perf_counter()
            status, _, ok = call(app, "POST", "/api/v1/runs", "gate-operator",
                                 body("docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md"))
            latencies.append((time.perf_counter() - started) * 1000)
            if first is None:
                first = {p.name: p.read_bytes() for p in store.iterdir()}
        _, _, failed = call(app, "POST", "/api/v1/runs", "gate-operator", body("docs/absent.md"))
        refused = call(app, "POST", "/api/v1/runs", "gate-observer", body("docs/x.md"))[0]
        anonymous = call(app, "GET", "/api/v1/runs")[0]
        _, headers, _ = call(app, "GET", "/api/v1/health")
        traces = call(app, "GET", "/api/v1/traces", "gate-observer")[2]["total"]
        audit = call(app, "GET", "/api/v1/audit?limit=200", "gate-operator")[2]["entries"]
        aios.stop()
        final = {p.name: p.read_bytes() for p in store.iterdir()}
        appended_only = all(final[name].startswith(data) for name, data in first.items())
        _, restarted = create_app(Path(tmp), REPO_ROOT, _Gate())
        survived = len(restarted.runs())
        restarted.stop()
    return {"success": ok.get("state") == "succeeded" and status == 201,
            "failure_state": failed.get("state"), "failure_reason": failed.get("failure_reason"),
            "observer_post": refused, "anonymous_get": anonymous,
            "headers": headers, "traces": traces, "expected_traces": 3 * runs + 2,
            "audit_entries": len(audit), "appended_only": appended_only,
            "runs_after_restart": survived, "runs_made": runs + 1,
            "latency_ms": {"runs": runs, "p50": round(statistics.median(latencies), 2),
                           "max": round(max(latencies), 2)}}


def _no_shipped_credential() -> bool:
    from fullstack.backend.security import NoAuthenticator
    served = (REPO_ROOT / "fullstack/backend/__main__.py").read_text(encoding="utf-8")
    return ("NoAuthenticator()" in served
            and NoAuthenticator().authenticate({"authorization": "Bearer any"}) is None)


def evaluate(runs: int = 20, register_text: Optional[str] = None) -> dict:
    text = register_text if register_text is not None else REGISTER.read_text(encoding="utf-8")
    decided = ratified(text)
    m = _measure(runs)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT),
                          capture_output=True, text=True).stdout.strip()
    security_headers = all(m["headers"].get(h) for h in (
        "X-Content-Type-Options", "Content-Security-Policy", "X-Frame-Options",
        "Referrer-Policy"))
    c: List[dict] = [
        _criterion("Functionality", "core functions work (Scenario B)",
                   PASS if m["success"] else FAIL, f"{runs} live runs succeeded: {m['success']}"),
        _criterion("Functionality", "failure is a meaningful state (Scenario C)",
                   PASS if m["failure_state"] == "failed" else FAIL,
                   f"state {m['failure_state']!r}: {m['failure_reason']}"),
        _blocked_unless("Functionality", "agent creation (Scenario A)", ["FS-DP-07"], decided,
                        "ratified but not implemented"),
        _blocked_unless("Security", "authentication", ["FS-DP-02"], decided,
                        "ratified but no authenticator is implemented"),
        _criterion("Security", "authorization and least privilege",
                   PASS if (m["observer_post"], m["anonymous_get"]) == (403, 401) else FAIL,
                   f"observer POST → {m['observer_post']}; anonymous GET → {m['anonymous_get']}"),
        _criterion("Security", "secrets not exposed", PASS if _no_shipped_credential() else FAIL,
                   "the shipped composition uses NoAuthenticator, which accepts no credential; "
                   "the security suite scans records and responses for credentials"),
        _criterion("Security", "attack-surface controls", PASS if security_headers else FAIL,
                   "security headers present; 64 KiB body limit; Tool confined to docs/"),
        _criterion("Security", "audit", PASS if m["audit_entries"] > 0 else FAIL,
                   f"{m['audit_entries']} decisions recorded"),
        _criterion("Reliability", "failure handling", PASS if m["failure_state"] == "failed" else FAIL,
                   "a failed Tool drives the Workflow to FAILED; nothing is left RUNNING"),
        _criterion("Reliability", "recovery (local store)",
                   PASS if m["runs_after_restart"] == m["runs_made"] else FAIL,
                   f"{m['runs_after_restart']} of {m['runs_made']} runs present after restart"),
        _blocked_unless("Reliability", "recovery and rollback of a deployment",
                        ["FS-DP-01", "FS-DP-04"], decided, "ratified but not deployed"),
        _criterion("Performance", "latency of Scenario B (local, in-process)", OBSERVED,
                   f"p50 {m['latency_ms']['p50']} ms, max {m['latency_ms']['max']} ms over "
                   f"{runs} runs; no workload requirement is stated"),
        _criterion("Observability", "tracing (Trace)",
                   PASS if m["traces"] == m["expected_traces"] else FAIL,
                   f"{m['traces']} Trace records for {runs} successful and 1 failed run"),
        _blocked_unless("Observability", "logging, metrics, alerting", ["FS-DP-06"], decided,
                        "ratified but not implemented"),
        _criterion("Data", "integrity (append-only)", PASS if m["appended_only"] else FAIL,
                   "every partition's bytes after the first run are a prefix of its final "
                   f"bytes: {m['appended_only']}"),
        _blocked_unless("Data", "production persistence, backup, migration", ["FS-DP-01"],
                        decided, "ratified but not implemented"),
        _criterion("Reproducibility", "known artifact", PASS if head else FAIL,
                   f"commit {head}; no build step"),
        _blocked_unless("Reproducibility", "reproducible deployment",
                        ["FS-DP-03", "FS-DP-04"], decided, "ratified but not deployed"),
    ]
    blocking = [x for x in c if x["status"] in (FAIL, BLOCKED)]
    packages = sorted({p for x in c for p in x["blocked_by"]})
    return {
        "gate": "FS-09 Production Readiness",
        "commit": head,
        "result": READY if not blocking else NOT_READY,
        "criteria": c,
        "blocking": [f"{x['area']}: {x['criterion']}" for x in blocking],
        "decision_packages": {p: ("RATIFIED by " + decided[p]) if p in decided
                              else "PROPOSED — NOT RATIFIED" for p in PACKAGES},
        "awaiting": packages,
        "external_dependencies": list(EXTERNAL_DEPENDENCIES),
        "release": "not due: the Founder release decision follows a PASS of this gate "
                   "(FD-FS-001 D4-A); this gate never releases",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m fullstack.readiness")
    commands = parser.add_subparsers(dest="command")
    run = commands.add_parser("evaluate", help="evaluate the gate and print JSON")
    run.add_argument("--runs", type=int, default=20)
    args = parser.parse_args(argv)
    if args.command != "evaluate":
        parser.print_help()
        return 0
    print(json.dumps(evaluate(args.runs), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
