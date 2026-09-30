"""FS-08 live suite against one Preview. Reads secrets from files; never prints them."""
import json, re, sys, threading, time, urllib.request, urllib.error
S = sys.argv[1]; BASE = sys.argv[2].rstrip("/")
TOKEN = open(f"{S}/token").read().strip(); BYPASS = open(f"{S}/bypass09").read().strip()
SECRETS = (TOKEN, BYPASS)
results, raw = [], []

def req(method, path, auth=None, body=None, bypass=True):
    headers = {"Accept": "application/json"}
    if bypass: headers["x-vercel-protection-bypass"] = BYPASS
    if auth is not None: headers["Authorization"] = auth
    data = None
    if body is not None:
        data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=90) as resp:
            status, text, hdrs = resp.status, resp.read().decode("utf-8", "replace"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        status, text, hdrs = e.code, e.read().decode("utf-8", "replace"), dict(e.headers)
    for s in SECRETS:
        if s in text or any(s in str(v) for v in hdrs.values()):
            raise SystemExit("SECRET ECHOED IN RESPONSE — aborting")
    try: payload = json.loads(text)
    except ValueError: payload = text[:200]
    raw.append({"method": method, "path": path, "status": status,
                "request_id": hdrs.get("X-Request-Id") or hdrs.get("x-request-id")})
    return status, payload

def check(n, name, ok, evidence):
    results.append({"n": n, "check": name, "result": "PASS" if ok else "FAIL", "evidence": evidence})

BEARER = "Bearer " + TOKEN
RUN = {"workflow": "document-conformance-review",
       "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md", "criteria": ["INV-4"]}}
ID = re.compile(r"^run-\d{8}T\d{6}Z-[0-9a-f]{16}-0$")

# 0. without the bypass, SSO still guards the Preview
st, _ = req("GET", "/api/v1/health", bypass=False)
check(0, "protection still active without the bypass", st in (302, 401, 403), f"GET health without bypass → {st}")
st, body = req("GET", "/api/v1/health")
check(0, "health through the bypass", st == 200 and body.get("runtime_state") == "running", f"→ {st} {body}")

# 1. missing authorization
sts = {p: req("GET", p)[0] for p in ("/api/v1/runs", "/api/v1/runtime", "/api/v1/traces", "/api/v1/audit", "/api/v1/session")}
st_post, _ = req("POST", "/api/v1/runs", body=RUN)
check(1, "missing Authorization rejected", set(sts.values()) == {401} and st_post == 401, f"{sts}; POST runs → {st_post}")

# 2. invalid / malformed authorization
bad = {"unknown token": "Bearer not-the-operator-token-7c1", "hash as token": "Bearer " + "0"*64,
       "truncated": BEARER[:-1], "wrong scheme": "Basic " + TOKEN, "no scheme": "x" * 10,
       "empty bearer": "Bearer "}
bad_sts = {k: req("GET", "/api/v1/runtime", auth=v)[0] for k, v in bad.items()}
check(2, "invalid and malformed Authorization rejected", set(bad_sts.values()) == {401}, str(bad_sts))

# 3. valid B3
st, session = req("GET", "/api/v1/session", auth=BEARER)
check(3, "valid B3 bearer authenticates", st == 200 and session.get("subject") == "founder"
      and session.get("scopes") == ["aios.agent.register", "aios.audit", "aios.observe", "aios.workflow.run"], f"→ {st} {session}")

# 4. protected GET
st, rt = req("GET", "/api/v1/runtime", auth=BEARER)
check(4, "protected GET", st == 200 and rt.get("state") == "running", f"runtime → {st}, state {rt.get('state')}, runtime_id {rt.get('runtime_id')}")

# 5. authenticated POST
st, run = req("POST", "/api/v1/runs", auth=BEARER, body=RUN)
check(5, "authenticated POST creates a run", st == 201 and run.get("state") == "succeeded",
      f"→ {st} run_id {run.get('run_id')} state {run.get('state')} requested_by {run.get('requested_by')} format {run.get('format')}")

# 6. persistence: read back in a later request (a new Runtime)
st, again = req("GET", f"/api/v1/runs/{run.get('run_id')}", auth=BEARER)
st2, rt2 = req("GET", "/api/v1/runtime", auth=BEARER)
check(6, "persisted in Supabase, read by a later Runtime", st == 200 and again == run and rt2.get("runtime_id") != run.get("runtime_id"),
      f"GET run → {st} identical={again == run}; later runtime {rt2.get('runtime_id')} ≠ run runtime {run.get('runtime_id')}")

# 7. trace association
st, tr = req("GET", "/api/v1/traces?limit=200", auth=BEARER)
mine = [r for r in tr.get("records", []) if r.get("runtime") == run["trace"]["runtime"]][run["trace"]["runtime_from"]:run["trace"]["runtime_to"]]
wf = [r["skills_used"] for r in mine if r.get("agent_instance") == "workflow-participating-agent"]
check(7, "Trace associated with the run", st == 200 and len(mine) == run["trace"]["count"] == 3
      and wf == [[f"document-conformance-review/{run['run_id']}"]],
      f"traces total {tr.get('total')}; this run's {len(mine)} of {run['trace']['count']}; workflow record names {wf}")

# 8. audit association
st, au = req("GET", "/api/v1/audit?limit=200", auth=BEARER)
entries = au.get("entries", [])
allowed = [e for e in entries if e["subject"] == "founder" and e["method"] == "POST" and e["path"] == "/api/v1/runs" and e["decision"] == "allowed"]
refused = [e for e in entries if e["subject"] is None and e["decision"] == "refused" and e["status"] == 401]
leaked = any(any(s in json.dumps(e) for s in SECRETS) for e in entries)
check(8, "audit records subjects and decisions, no credential", st == 200 and allowed and len(refused) >= 6 and not leaked,
      f"entries {len(entries)}; founder POST allowed {len(allowed)}; anonymous 401 refused {len(refused)}; credential in audit: {leaked}")

# 9-11. concurrency
N = 8; out = [None] * N; barrier = threading.Barrier(N)
def one(i):
    barrier.wait(); out[i] = req("POST", "/api/v1/runs", auth=BEARER, body=RUN)
ts = [threading.Thread(target=one, args=(i,)) for i in range(N)]
[t.start() for t in ts]; [t.join(180) for t in ts]
codes = [o[0] if o else None for o in out]; ids = [o[1].get("run_id") for o in out if o and o[0] == 201]
check(9, f"{N} concurrent POSTs", codes == [201] * N, f"statuses {codes}")
check(10, "distinct runtime-derived identities", len(ids) == N and all(ID.match(i) for i in ids)
      and len({o[1]['runtime_id'] for o in out}) == N, f"{len(ids)} ids, all match run-<boot>-0: {all(ID.match(i) for i in ids)}; distinct runtimes {len({o[1]['runtime_id'] for o in out})}")
st, listed = req("GET", "/api/v1/runs", auth=BEARER)
all_ids = [r["run_id"] for r in listed.get("runs", [])]
check(11, "no duplicate identity in the store", len(all_ids) == len(set(all_ids)) and set(ids) <= set(all_ids),
      f"{len(all_ids)} runs listed, {len(set(all_ids))} distinct; all concurrent ids present: {set(ids) <= set(all_ids)}")

# 12. failure paths
st_f, failed = req("POST", "/api/v1/runs", auth=BEARER, body={**RUN, "inputs": {**RUN["inputs"], "document": "docs/absent.md"}})
st_v, inval = req("POST", "/api/v1/runs", auth=BEARER, body={"workflow": "document-conformance-review", "inputs": {"document": "", "criteria": []}})
st_u, unk = req("POST", "/api/v1/runs", auth=BEARER, body={"workflow": "no-such-workflow", "inputs": RUN["inputs"]})
st_n, nf = req("GET", "/api/v1/runs/run-does-not-exist", auth=BEARER)
check(12, "failure paths are meaningful states", st_f == 201 and failed.get("state") == "failed" and st_v == 400 and st_u in (400, 404) and st_n == 404,
      f"missing doc → {st_f} state {failed.get('state')} ({failed.get('failure_reason')}); invalid input → {st_v}; unknown workflow → {st_u}; unknown run → {st_n}")

json.dump({"base": BASE, "results": results, "requests": raw, "run_ids": {"single": run.get("run_id"), "concurrent": ids, "failed": failed.get("run_id")}},
          open(f"{S}/live_results_09.json", "w"), indent=1)
for r in results:
    print(f"{r['n']:>2} {r['result']:4} {r['check']}: {r['evidence']}")
