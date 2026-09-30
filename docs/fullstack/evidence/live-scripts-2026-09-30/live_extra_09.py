"""FS-09 additional live checks. Reads secrets from files; never prints them."""
import json, sys, time, urllib.request, urllib.error
S = sys.argv[1]; BASE = sys.argv[2].rstrip("/")
TOKEN = open(f"{S}/token").read().strip(); BYPASS = open(f"{S}/bypass09").read().strip()
res, raw = [], []
def req(method, path, auth=True, body=None, extra=None):
    h = {"x-vercel-protection-bypass": BYPASS, "Accept": "application/json"}
    if auth: h["Authorization"] = "Bearer " + TOKEN
    if extra: h.update(extra)
    data = json.dumps(body).encode() if body is not None else None
    if data: h["Content-Type"] = "application/json"
    t = time.perf_counter()
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + path, data=data, headers=h, method=method), timeout=90) as r:
            st, txt, hd = r.status, r.read().decode(), dict(r.headers)
    except urllib.error.HTTPError as e:
        st, txt, hd = e.code, e.read().decode(), dict(e.headers)
    ms = (time.perf_counter() - t) * 1000
    for s in (TOKEN, BYPASS):
        if s in txt or any(s in str(v) for v in hd.values()): raise SystemExit("SECRET ECHOED")
    rid = hd.get("X-Request-Id") or hd.get("x-request-id")
    raw.append({"method": method, "path": path, "status": st, "request_id": rid, "ms": round(ms, 1)})
    try: body = json.loads(txt)
    except ValueError: body = None
    return st, hd, body, ms
def check(name, ok, ev): res.append({"check": name, "result": "PASS" if ok else "FAIL", "evidence": ev})
lower = lambda hd: {k.lower(): v for k, v in hd.items()}
RUN = {"workflow": "document-conformance-review", "inputs": {"document": "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md", "criteria": ["INV-4"]}}
# N1: transport and origin
st, hd, _, _ = req("GET", "/api/v1/health", auth=False, extra={"Origin": "https://attacker.example"})
h = lower(hd)
check("HSTS on HTTPS responses", "strict-transport-security" in h, f"strict-transport-security: {h.get('strict-transport-security')}")
check("no cross-origin grant on the API", not [k for k in h if k.startswith("access-control-")], f"access-control headers: {[k for k in h if k.startswith('access-control-')]}")
st, hd, _, _ = req("OPTIONS", "/api/v1/runs", auth=False, extra={"Origin": "https://attacker.example", "Access-Control-Request-Method": "POST"})
check("CORS preflight not honoured", st != 204 and not [k for k in lower(hd) if k.startswith("access-control-allow")], f"OPTIONS → {st}")
st, hd, _, _ = req("GET", "/", auth=False)
h = lower(hd)
check("console served same-origin with its CSP", st == 200 and "connect-src 'self'" in h.get("content-security-policy", ""), f"/ → {st}; connect-src self: {'connect-src' in h.get('content-security-policy','')}")
# reliability: repeated execution
ids, lat = [], []
for i in range(5):
    st, _, body, ms = req("POST", "/api/v1/runs", body=RUN)
    lat.append(ms); ids.append(body.get("run_id") if body else None)
check("repeated execution: 5 sequential runs succeed with distinct ids", len(set(ids)) == 5 and None not in ids, f"{len(set(ids))} distinct ids")
# performance observation (no requirement exists)
hl = [req("GET", "/api/v1/health", auth=False)[3] for _ in range(5)]
json.dump({"base": BASE, "results": res, "requests": raw, "run_ids": ids,
           "observed_latency_ms": {"post_run": [round(x) for x in lat], "health": [round(x) for x in hl]}},
          open(f"{S}/live_extra_09.json", "w"), indent=1)
for r in res: print(r["result"], r["check"], "|", r["evidence"])
print("latency post_run ms", [round(x) for x in lat], "health ms", [round(x) for x in hl])
