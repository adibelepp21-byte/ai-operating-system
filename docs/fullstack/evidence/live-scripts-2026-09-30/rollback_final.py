"""FS-09 rollback drill phase. Reads secrets from files; never prints them."""
import json, sys, urllib.request, urllib.error
S, BASE, PHASE, READ_ID = sys.argv[1], sys.argv[2].rstrip("/"), sys.argv[3], sys.argv[4]
TOKEN = open(f"{S}/token").read().strip(); BYPASS = open(f"{S}/bypass09").read().strip()
def req(m, p, auth=True, body=None):
    h = {"x-vercel-protection-bypass": BYPASS}
    if auth: h["Authorization"] = "Bearer " + TOKEN
    d = json.dumps(body).encode() if body is not None else None
    if d: h["Content-Type"] = "application/json"
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + p, data=d, headers=h, method=m), timeout=90) as r:
            st, t, hd = r.status, r.read().decode(), dict(r.headers)
    except urllib.error.HTTPError as e:
        st, t, hd = e.code, e.read().decode(), dict(e.headers)
    for s in (TOKEN, BYPASS):
        if s in t: raise SystemExit("SECRET ECHOED")
    try: j = json.loads(t)
    except ValueError: j = None
    return st, j, hd.get("X-Request-Id") or hd.get("x-request-id")
RUN = {"workflow": "document-conformance-review", "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md", "criteria": ["INV-4"]}}
out = {"phase": PHASE, "base": BASE}
out["health"] = req("GET", "/api/v1/health", auth=False)[:2]
out["agent_definitions_route"] = req("GET", "/api/v1/agent-definitions")[0]
st, il, _ = req("GET", "/api/v1/agent-instances"); out["agent_instances"] = (st, len((il or {}).get("instances", [])) if st == 200 else None)
out["anonymous_runs"] = req("GET", "/api/v1/runs", auth=False)[0]
st, rt, _ = req("GET", "/api/v1/runtime"); out["runtime"] = (st, rt and rt.get("runtime_id"))
st, r, _ = req("GET", f"/api/v1/runs/{READ_ID}"); out["reads_other_version_run"] = (st, r and r.get("run_id") == READ_ID, r and r.get("format"))
st, rt2, _ = req("GET", f"/api/v1/runs/{READ_ID}")
st, b, rid = req("POST", "/api/v1/runs", body=RUN); out["scenario_b"] = (st, b and b.get("state"), b and b.get("run_id"), rid)
st, c, _ = req("POST", "/api/v1/runs", body={**RUN, "inputs": {**RUN["inputs"], "document": "docs/absent.md"}}); out["scenario_c"] = (st, c and c.get("state"))
st, runs, _ = req("GET", "/api/v1/runs"); ids = [x["run_id"] for x in (runs or {}).get("runs", [])]
out["runs_listed"] = len(ids); out["runs_distinct"] = len(set(ids))
st, tr, _ = req("GET", f"/api/v1/traces?limit=1"); out["traces_total"] = tr and tr.get("total")
json.dump(out, open(f"{S}/rollback_{PHASE}.json", "w"), indent=1); print(json.dumps(out))
