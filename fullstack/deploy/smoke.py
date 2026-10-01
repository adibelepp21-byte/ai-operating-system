"""Smoke checks for a deployed AIOS Full Stack (FS-10).

```text
python -m fullstack.deploy.smoke --base https://<host> --token-file <file> \
    [--bypass-file <file> | --bypass-env <NAME>] [--write] [--out <evidence.json>]
```

**Two profiles.**

* **Read-only** (default): no run, trace or agent record is written. The
  application still appends one access-audit record (`fullstack-audit`) for
  each request to a protected route, allowed or refused, by design; the
  profile makes 18 such requests (observed on Production, FS-10). It checks
  health and readiness, that every protected route refuses a missing, an
  invalid and a malformed `Authorization`, that a valid bearer authenticates,
  that the Runtime is running, that the read routes answer, and that the
  console is served with its security headers.
* **Write** (`--write`): adds one Scenario B run and one Scenario C run. The
  store is append-only, so these records stay for good. On a Production target
  that is a Founder decision (`FS-10-DEPLOYMENT.md`); the tool never turns the
  profile on by itself and prints the target before it writes.

**Secrets.** The operator token and, where Deployment Protection is on, the
bypass secret are read from files (or, for the bypass, from a named
environment variable), sent as headers, never printed, and never written to the
evidence. A response that echoes either aborts the run. Where the session's
agent proxy attaches the bypass itself (FDP-012 O-A delivery), pass neither
bypass option: the value never reaches this process.

**No environment inference.** The tool is told the base URL; it does not decide
that a host is Preview or Production. It records the URL it was given.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

FORMAT = "fullstack.smoke/1"
PROTECTED_GET = ("/api/v1/runs", "/api/v1/runtime", "/api/v1/traces", "/api/v1/audit",
                 "/api/v1/session", "/api/v1/agent-instances")
RUN = {"workflow": "document-conformance-review",
       "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
                  "criteria": ["INV-4"]}}
SECURITY_HEADERS = ("content-security-policy", "x-content-type-options", "x-frame-options",
                    "referrer-policy")
BYPASS_HEADER = "x-vercel-protection-bypass"
RUN_ID = re.compile(r"^run-\d{8}T\d{6}Z-[0-9a-f]{16}-0$")


class SecretEchoed(RuntimeError):
    """A response carried a credential back. The run stops."""


Response = Tuple[int, Dict[str, str], Optional[object], str]


class Client:
    def __init__(self, base: str, token: str, bypass: Optional[str] = None,
                 opener: Optional[Callable] = None, timeout: float = 60.0):
        self.base, self._token, self._bypass = base.rstrip("/"), token, bypass
        self._open, self._timeout = opener or urllib.request.urlopen, timeout

    def request(self, method: str, path: str, *, authorization: Optional[str] = None,
                body: Optional[dict] = None, bearer: bool = True) -> Response:
        headers = {"Accept": "application/json"}
        if self._bypass:
            headers[BYPASS_HEADER] = self._bypass
        if authorization is not None:
            headers["Authorization"] = authorization
        elif bearer:
            headers["Authorization"] = "Bearer " + self._token
        data = json.dumps(body).encode("utf-8") if body is not None else None
        if data is not None:
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(self.base + path, data=data, headers=headers, method=method)
        try:
            with self._open(req, timeout=self._timeout) as resp:
                status, raw, hdrs = resp.status, resp.read().decode("utf-8", "replace"), dict(resp.headers)
        except urllib.error.HTTPError as error:
            status, raw, hdrs = error.code, error.read().decode("utf-8", "replace"), dict(error.headers)
        for secret in filter(None, (self._token, self._bypass)):
            if secret in raw or any(secret in str(v) for v in hdrs.values()):
                raise SecretEchoed(f"{method} {path} echoed a credential")
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = None
        return status, {k.lower(): v for k, v in hdrs.items()}, payload, raw


def _check(results: List[dict], name: str, ok: bool, evidence: str, mutates: bool = False) -> None:
    results.append({"check": name, "result": "PASS" if ok else "FAIL", "evidence": evidence,
                    "mutates": mutates})


def run(client: Client, write: bool = False) -> dict:
    """Run the profile. Returns the evidence record (no credential in it)."""
    results: List[dict] = []
    status, _, health, _ = client.request("GET", "/api/v1/health", bearer=False)
    _check(results, "health and readiness (R2)",
           status == 200 and isinstance(health, dict) and health.get("status") == "ok"
           and health.get("runtime_state") == "running", f"GET /health → {status} {health}")

    anon = {p: client.request("GET", p, bearer=False)[0] for p in PROTECTED_GET}
    _check(results, "anonymous protected routes refused",
           set(anon.values()) == {401}, f"{anon}")
    bad = {"unknown token": "Bearer not-a-valid-token-0", "hash-shaped": "Bearer " + "0" * 64,
           "wrong scheme": "Basic abc", "empty bearer": "Bearer "}
    bad_status = {k: client.request("GET", "/api/v1/runtime", authorization=v)[0]
                  for k, v in bad.items()}
    _check(results, "invalid and malformed Authorization refused",
           set(bad_status.values()) == {401}, f"{bad_status}")
    status, _, session, _ = client.request("GET", "/api/v1/session")
    _check(results, "valid bearer authenticates",
           status == 200 and isinstance(session, dict) and bool(session.get("subject"))
           and bool(session.get("scopes")),
           f"→ {status}, subject {session.get('subject') if isinstance(session, dict) else None}, "
           f"scopes {session.get('scopes') if isinstance(session, dict) else None}")
    status, _, runtime, _ = client.request("GET", "/api/v1/runtime")
    _check(results, "Runtime running on the store",
           status == 200 and isinstance(runtime, dict) and runtime.get("state") == "running",
           f"→ {status}, state {runtime.get('state') if isinstance(runtime, dict) else None}")
    reads = {p: client.request("GET", p)[0] for p in
             ("/api/v1/runs", "/api/v1/traces", "/api/v1/workflows", "/api/v1/tools",
              "/api/v1/agent-definitions", "/api/v1/agent-instances")}
    _check(results, "read routes answer", set(reads.values()) == {200}, f"{reads}")
    status, headers, _, raw = client.request("GET", "/", bearer=False)
    missing = [h for h in SECURITY_HEADERS if h not in headers]
    _check(results, "console served with its security headers",
           status == 200 and not missing and "AIOS" in raw, f"→ {status}, missing {missing}")

    if write:
        status, _, created, _ = client.request("POST", "/api/v1/runs", body=RUN)
        ok_b = (status == 201 and isinstance(created, dict) and created.get("state") == "succeeded"
                and bool(RUN_ID.match(str(created.get("run_id", "")))))
        _check(results, "Scenario B: a run succeeds", ok_b,
               f"→ {status} {created.get('run_id') if isinstance(created, dict) else None}", True)
        if ok_b:
            status, _, again, _ = client.request("GET", f"/api/v1/runs/{created['run_id']}")
            _check(results, "the run is read back", status == 200 and again == created,
                   f"GET run → {status}")
        failing = {**RUN, "inputs": {**RUN["inputs"], "document": "docs/absent.md"}}
        status, _, failed, _ = client.request("POST", "/api/v1/runs", body=failing)
        _check(results, "Scenario C: a failure is a meaningful state",
               status == 201 and isinstance(failed, dict) and failed.get("state") == "failed"
               and bool(failed.get("failure_reason")),
               f"→ {status} state {failed.get('state') if isinstance(failed, dict) else None}", True)
    return {"format": FORMAT, "base": client.base, "profile": "write" if write else "read-only",
            "results": results, "ok": all(r["result"] == "PASS" for r in results),
            "writes_made": write}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m fullstack.deploy.smoke", description=__doc__.split("\n")[0])
    parser.add_argument("--base", required=True)
    parser.add_argument("--token-file", required=True, type=Path)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--bypass-file", type=Path)
    source.add_argument("--bypass-env", metavar="NAME",
                        help="read the bypass from this environment variable; never printed")
    parser.add_argument("--write", action="store_true",
                        help="also run Scenarios B and C; appends records to the target's store")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    token = args.token_file.read_text(encoding="utf-8").strip()
    bypass = args.bypass_file.read_text(encoding="utf-8").strip() if args.bypass_file else None
    if args.bypass_env:
        bypass = os.environ.get(args.bypass_env, "").strip()
        if not bypass:
            print(f"aborted: {args.bypass_env} is not set", file=sys.stderr)
            return 2
    if args.write:
        print(f"WRITE profile against {args.base}: records will be appended to its store", file=sys.stderr)
    try:
        record = run(Client(args.base, token, bypass), write=args.write)
    except SecretEchoed as error:
        print(f"aborted: {error}", file=sys.stderr)
        return 3
    text = json.dumps(record, indent=1)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`
    # (`--out` writes a file).
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import tools  # noqa: E402,F401
    sys.exit(main())
