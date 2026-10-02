"""O-A operating session checks (`AD-FS10-ESC03-R1` `§5`, `§6`; `FDP-012`).

```text
python -m fullstack.deploy.oa_session preflight --token-file <file> [--bypass-env NAME] [--out <evidence.json>]
python -m fullstack.deploy.oa_session verify    --token-file <file> [--bypass-env NAME] [--write] [--out <evidence.json>]
python -m fullstack.deploy.oa_session revoked   --token-file <file> [--bypass-env NAME] [--out <evidence.json>]
```

**Delivery.** Under O-A the Protection Bypass is attached by the session's
agent proxy (cloud-environment API credential) to the three T2 hosts only; the
tool is run without ``--bypass-env`` and never receives, reads, sends or prints
it. The client sends only the B3 bearer, read from a private file and never printed.

**M1** (``--bypass-env NAME``; the `AD-FS10-ESC03-R1` fallback, authorized by the
Founder on 2026-10-02 for a dedicated environment). The client itself sends
``x-vercel-protection-bypass``, read privately from the named variable of the
dedicated cloud environment, together with the B3 bearer. The value is attached
to requests for the three T2 hosts **only**, never printed, never written, and
the evidence is checked for it before it is written. Under M1 no environment API
credential may attach the bypass as well: the check "B3 without the bypass is
stopped by X2" fails if one does.

**Phases.**

* ``preflight`` (session step 3): no bypass-named variable in the process
  environment; ``GET /api/v1/health`` → 200 on each T2 host (injection proven);
  control hosts that are not listed are stopped by X2 (nothing is injected
  there: an unlisted Production deployment and a Preview deployment).
* ``verify`` (step 4): the preflight checks again, then on the Production alias
  and on the designated rollback target the read-only smoke profile, the exact
  scopes of the principal, the ``aios.agent.register`` refusal (403), and the
  audit attribution of those requests, found by their ``X-Request-Id``. With
  ``--write`` (alias only): one Scenario B run and one Scenario C run, the run's
  own Trace records, and the audit entry of the run request.
* ``revoked`` (step 6, after the account holder revoked the bypass): on every
  T2 host X2 stops both an anonymous request and one with the B3 bearer alone.

**Who answered.** X2 answers 302 (browser) or 401 *"Protected deployment"*
(JSON client); the AIOS API always sets ``X-Request-Id``. A 401 is therefore
attributed to X2 or to B3 by that header, never by the status alone.

The evidence names hosts, statuses, request ids, subjects and scopes. It never
contains a credential; the run aborts if a response echoes the bearer, and the
evidence is checked for the bearer before it is written.

This tool deploys nothing and changes no setting: no Release, no LIVE.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fullstack.deploy import smoke

FORMAT = "fullstack.oa-session/1"
ALIAS = "aios-platform-adibelepp21-bytes-projects.vercel.app"
SERVING = "aios-platform-72l8flelz-adibelepp21-bytes-projects.vercel.app"
TARGET = "aios-platform-9dhc3bfal-adibelepp21-bytes-projects.vercel.app"
T2_HOSTS = (ALIAS, SERVING, TARGET)
CONTROL_HOSTS = {
    "unlisted Production deployment (dpl_CHV72…)":
        "aios-platform-p5o0g6or9-adibelepp21-bytes-projects.vercel.app",
    "Preview deployment (dpl_HvyYh…)":
        "aios-platform-9ohavmco2-adibelepp21-bytes-projects.vercel.app",
}
SUBJECT = "aios-operator"
SCOPES = ("aios.audit", "aios.observe", "aios.workflow.run")
#: X2 answers a browser with 302 to Vercel login and a JSON client with 401
#: "Protected deployment"; neither carries the application's X-Request-Id.
EDGE_STATUSES = (302, 401)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # an X2 302 is the observation
        return None


_OPENER = urllib.request.build_opener(_NoRedirect())


def _open(request, timeout):
    return _OPENER.open(request, timeout=timeout)


def _client(host: str, token: str, opener: Callable,
            bypass: Optional[str] = None) -> smoke.Client:
    """The bypass (M1) is attached for the T2 hosts only, whatever the caller passes."""
    return smoke.Client("https://" + host, token,
                        bypass=bypass if host in T2_HOSTS else None, opener=opener)


def _reach(client: smoke.Client, path: str = "/api/v1/health", bearer: bool = False) -> str:
    """Who answered: ``app <status>`` (the AIOS API, which always sets
    X-Request-Id), ``x2 <status>`` (Deployment Protection), or ``error``."""
    try:
        status, headers, _, _ = client.request("GET", path, bearer=bearer)
    except (urllib.error.URLError, OSError) as error:
        return f"error {type(error).__name__}"
    if "x-request-id" in headers:
        return f"app {status}"
    return f"x2 {status}" if status in EDGE_STATUSES else f"other {status}"


def _x2(answer: str) -> bool:
    return answer.startswith("x2 ")


def _check(results: List[dict], name: str, ok: bool, evidence: str, mutates: bool = False) -> None:
    results.append({"check": name, "result": "PASS" if ok else "FAIL", "evidence": evidence,
                    "mutates": mutates})


def _environment_clean(results: List[dict], environ: Dict[str, str],
                       m1_variable: Optional[str] = None) -> None:
    named = sorted(k for k in environ if "BYPASS" in k.upper())
    carried = sorted(k for k, v in environ.items() if smoke.BYPASS_HEADER in str(v).lower())
    if m1_variable is None:
        _check(results, "no bypass in the process environment",
               not named and not carried,
               f"bypass-named variables {named}; header-carrying {carried}")
    else:
        _check(results, "M1: only the designated variable holds a bypass (names only)",
               named == [m1_variable] and not carried,
               f"bypass-named variables {named}; header-carrying {carried}")


def _edge_m1(results: List[dict], token: str, opener: Callable, bypass: str) -> bool:
    reached = {h: _reach(_client(h, token, opener, bypass)) for h in T2_HOSTS}
    passed = set(reached.values()) == {"app 200"}
    _check(results, "T1 M1: the client bypass reaches the application on every T2 host",
           passed, f"{reached}")
    without = {h: _reach(_client(h, token, opener), "/api/v1/session", bearer=True)
               for h in T2_HOSTS}
    _check(results, "T4 B3 without M1 is stopped by X2 on every T2 host "
                    "(no other mechanism attaches the bypass)",
           all(_x2(a) for a in without.values()), f"{without}")
    controls = {label: _reach(_client(h, token, opener, bypass))
                for label, h in CONTROL_HOSTS.items()}
    _check(results, "M1 is never sent to hosts outside T2; they stay behind X2",
           all(_x2(a) for a in controls.values()), f"{controls}")
    return passed


def _b3_independent(results: List[dict], host: str, token: str, opener: Callable,
                    bypass: str) -> None:
    client = _client(host, token, opener, bypass)
    missing = _reach(client, "/api/v1/session")
    _check(results, f"{host}: T3 M1 without a B3 bearer is refused by the application (401)",
           missing == "app 401", missing)
    invalid = _client(host, "invalid-" + "0" * 24, opener, bypass)
    answer = _reach(invalid, "/api/v1/session", bearer=True)
    _check(results, f"{host}: T5 M1 with an invalid B3 bearer is refused by the application (401)",
           answer == "app 401", answer)


def _edge(results: List[dict], token: str, opener: Callable) -> bool:
    injected = {h: _reach(_client(h, token, opener)) for h in T2_HOSTS}
    passed = set(injected.values()) == {"app 200"}
    _check(results, "injection proven on every T2 host (health 200 through X2)",
           passed, f"{injected}")
    controls = {label: _reach(_client(h, token, opener)) for label, h in CONTROL_HOSTS.items()}
    _check(results, "hosts not listed stay behind X2",
           all(_x2(a) for a in controls.values()), f"{controls}")
    return passed


def _audit_entries(client: smoke.Client, request_ids: Sequence[str]) -> Dict[str, dict]:
    wanted, found, offset = set(request_ids), {}, 0
    while wanted - set(found):
        status, _, page, _ = client.request("GET", f"/api/v1/audit?offset={offset}&limit=200")
        if status != 200 or not isinstance(page, dict):
            break
        entries = page.get("entries") or []
        for entry in entries:
            if entry.get("request_id") in wanted:
                found[entry["request_id"]] = entry
        if len(entries) < 200:
            break
        offset += 200
    return found


def _attributed(entry: Optional[dict], decision: str, scope: str) -> bool:
    return (isinstance(entry, dict) and entry.get("subject") == SUBJECT
            and entry.get("decision") == decision and entry.get("scope") == scope)


def _principal_checks(results: List[dict], host: str, client: smoke.Client) -> None:
    status, headers, session, _ = client.request("GET", "/api/v1/session")
    session_rid = headers.get("x-request-id")
    _check(results, f"{host}: principal is {SUBJECT} with exactly its three scopes",
           status == 200 and isinstance(session, dict) and session.get("subject") == SUBJECT
           and tuple(session.get("scopes") or ()) == SCOPES,
           f"→ {status}, {session if isinstance(session, dict) else None}")
    status, headers, _, _ = client.request("POST", "/api/v1/agent-instances", body={})
    register_rid = headers.get("x-request-id")
    _check(results, f"{host}: aios.agent.register refused (403)", status == 403, f"→ {status}")
    audit = _audit_entries(client, [r for r in (session_rid, register_rid) if r])
    _check(results, f"{host}: audit attributes the session read to {SUBJECT} (allowed)",
           _attributed(audit.get(session_rid), "allowed", "authenticated"),
           f"{audit.get(session_rid)}")
    _check(results, f"{host}: audit records the register attempt as refused for {SUBJECT}",
           _attributed(audit.get(register_rid), "refused", "aios.agent.register"),
           f"{audit.get(register_rid)}")


def _write_checks(results: List[dict], client: smoke.Client) -> None:
    status, headers, run, _ = client.request("POST", "/api/v1/runs", body=smoke.RUN)
    rid = headers.get("x-request-id")
    ok = status == 201 and isinstance(run, dict) and run.get("state") == "succeeded"
    _check(results, "Scenario B: a run succeeds, requested by the principal",
           ok and run.get("requested_by") == SUBJECT,
           f"→ {status} {run.get('run_id') if isinstance(run, dict) else None}", True)
    if not ok:
        return
    status, _, again, _ = client.request("GET", f"/api/v1/runs/{run['run_id']}")
    _check(results, "the run is persisted and read back", status == 200 and again == run,
           f"GET run → {status}")
    span = run.get("trace") or {}
    status, _, first, _ = client.request("GET", "/api/v1/traces?offset=0&limit=1")
    total = first.get("total", 0) if isinstance(first, dict) else 0
    status, _, tail, _ = client.request(
        "GET", f"/api/v1/traces?offset={max(0, total - 200)}&limit=200")
    own = [r for r in (tail.get("records", []) if isinstance(tail, dict) else [])
           if r.get("runtime") == span.get("runtime")]
    _check(results, "the run's own Trace records exist",
           span.get("count", 0) > 0 and len(own) >= span.get("count", 0),
           f"span count {span.get('count')}, found {len(own)} for its Runtime")
    entry = _audit_entries(client, [rid] if rid else []).get(rid)
    _check(results, "audit attributes the run request to the principal (allowed)",
           _attributed(entry, "allowed", "aios.workflow.run"), f"{entry}")
    failing = {**smoke.RUN, "inputs": {**smoke.RUN["inputs"], "document": "docs/absent.md"}}
    status, _, failed, _ = client.request("POST", "/api/v1/runs", body=failing)
    _check(results, "Scenario C: a failure is a meaningful state",
           status == 201 and isinstance(failed, dict) and failed.get("state") == "failed"
           and bool(failed.get("failure_reason")),
           f"→ {status} state {failed.get('state') if isinstance(failed, dict) else None}", True)


def run(phase: str, token: str, *, write: bool = False, opener: Optional[Callable] = None,
        environ: Optional[Dict[str, str]] = None, bypass: Optional[str] = None,
        m1_variable: Optional[str] = None) -> dict:
    """Run one phase. Returns the evidence record (no credential in it).

    ``bypass`` set means M1: the client sends it, to the T2 hosts only."""
    opener = opener or _open
    results: List[dict] = []
    smoke_records: Dict[str, dict] = {}
    if phase in ("preflight", "verify"):
        _environment_clean(results, dict(os.environ if environ is None else environ),
                           m1_variable if bypass else None)
        if bypass:
            injected = _edge_m1(results, token, opener, bypass)
            if injected:
                for host in (ALIAS, TARGET):
                    _b3_independent(results, host, token, opener, bypass)
        else:
            injected = _edge(results, token, opener)
        if phase == "verify" and injected:
            for host in (ALIAS, TARGET):
                client = _client(host, token, opener, bypass)
                record = smoke.run(client, write=False)
                smoke_records[host] = record
                _check(results, f"{host}: read-only smoke profile", record["ok"],
                       f"{sum(r['result'] == 'PASS' for r in record['results'])}"
                       f"/{len(record['results'])} PASS")
                _principal_checks(results, host, client)
            if write:
                _write_checks(results, _client(ALIAS, token, opener, bypass))
    elif phase == "revoked":
        for host in T2_HOSTS:
            client = _client(host, token, opener, bypass)
            anonymous, bearer = _reach(client), _reach(client, "/api/v1/session", bearer=True)
            _check(results, f"{host}: X2 back after revocation (anonymous and B3-only stopped by X2)",
                   _x2(anonymous) and _x2(bearer), f"anonymous {anonymous}, B3-only {bearer}")
    else:
        raise ValueError(f"unknown phase {phase!r}")
    record = {"format": FORMAT, "phase": phase, "mechanism": "M1" if bypass else "O-A",
              "t2_hosts": list(T2_HOSTS),
              "control_hosts": CONTROL_HOSTS, "results": results, "smoke": smoke_records,
              "ok": bool(results) and all(r["result"] == "PASS" for r in results),
              "writes_made": phase == "verify" and write}
    blob = json.dumps(record)
    if (token and token in blob) or (bypass and bypass in blob):
        raise smoke.SecretEchoed("the evidence would carry a credential")
    return record


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m fullstack.deploy.oa_session",
                                     description=__doc__.split("\n")[0])
    parser.add_argument("phase", choices=("preflight", "verify", "revoked"))
    parser.add_argument("--token-file", required=True, type=Path)
    parser.add_argument("--write", action="store_true",
                        help="verify: also run Scenarios B and C on the alias (appends records)")
    parser.add_argument("--bypass-env", metavar="NAME",
                        help="M1: read the bypass from this variable of the dedicated "
                             "environment; sent to the T2 hosts only, never printed")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    if args.write and args.phase != "verify":
        parser.error("--write applies to verify only")
    token = args.token_file.read_text(encoding="utf-8").strip()
    bypass = None
    if args.bypass_env:
        bypass = os.environ.get(args.bypass_env, "").strip()
        if not bypass:
            print(f"aborted: {args.bypass_env} is not set", file=sys.stderr)
            return 2
    if args.write:
        print(f"WRITE: Scenario B and C runs will be appended on {ALIAS}", file=sys.stderr)
    try:
        record = run(args.phase, token, write=args.write, bypass=bypass,
                     m1_variable=args.bypass_env)
    except smoke.SecretEchoed as error:
        print(f"aborted: {error}", file=sys.stderr)
        return 3
    text = json.dumps(record, indent=1)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import tools  # noqa: E402,F401  (GOAL-V2-004 certified-write barrier)
    sys.exit(main())
