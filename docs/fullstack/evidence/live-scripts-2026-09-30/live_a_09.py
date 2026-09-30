"""FS-09 Scenario A live checks (A2). Secrets from files; never printed."""
import json, sys, urllib.request, urllib.error, threading, time
S, BASE = sys.argv[1], sys.argv[2].rstrip("/"); STAMP = sys.argv[3]
TOKEN = open(f"{S}/token").read().strip(); BYPASS = open(f"{S}/bypass09").read().strip()
res, raw = [], []
def req(m, p, auth=True, body=None, bearer=None):
    h = {"x-vercel-protection-bypass": BYPASS, "Accept": "application/json"}
    if auth: h["Authorization"] = bearer or ("Bearer " + TOKEN)
    d = json.dumps(body).encode() if body is not None else None
    if d: h["Content-Type"] = "application/json"
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + p, data=d, headers=h, method=m), timeout=90) as r:
            st, t, hd = r.status, r.read().decode(), dict(r.headers)
    except urllib.error.HTTPError as e:
        st, t, hd = e.code, e.read().decode(), dict(e.headers)
    for s in (TOKEN, BYPASS):
        if s in t or any(s in str(v) for v in hd.values()): raise SystemExit("SECRET ECHOED")
    try: j = json.loads(t)
    except ValueError: j = None
    raw.append({"method": m, "path": p, "status": st, "request_id": hd.get("X-Request-Id") or hd.get("x-request-id")})
    return st, j
def check(name, ok, ev): res.append({"check": name, "result": "PASS" if ok else "FAIL", "evidence": ev})
KEY = f"live-desk-{STAMP}"
BODY = {"definition": "engineering-intelligence-agent", "instance_key": KEY, "capabilities": ["engineering-intelligence"]}
st, defs = req("GET", "/api/v1/agent-definitions")
names = [d["definition"] for d in (defs or {}).get("definitions", [])]
check("Scenario A: governed Definitions are listed", st == 200 and "engineering-intelligence-agent" in names, f"→ {st}, {len(names)} active Definitions")
st0, _ = req("POST", "/api/v1/agent-instances", auth=False, body=BODY)
stm, _ = req("POST", "/api/v1/agent-instances", bearer="Bearer not-the-operator-token-7c1", body=BODY)
check("Scenario A: unauthenticated and invalid-token registration rejected", (st0, stm) == (401, 401), f"no Authorization → {st0}; invalid token → {stm}")
st, inst = req("POST", "/api/v1/agent-instances", body=BODY)
check("Scenario A: agent instance registered and persisted", st == 201 and inst and inst.get("lifecycle") == "REGISTERED"
      and inst.get("grants_authority") is False and inst.get("created_by") == "founder"
      and inst.get("authority", {}).get("decision") == "ACT-008-DG-01",
      f"→ {st} {KEY}: lifecycle {inst and inst.get('lifecycle')}, grants_authority {inst and inst.get('grants_authority')}, runtime {inst and inst.get('runtime_id')}")
st_g, got = req("GET", f"/api/v1/agent-instances/{KEY}")
st_l, lst = req("GET", "/api/v1/agent-instances")
keys = [i["instance_key"] for i in (lst or {}).get("instances", [])]
check("Scenario A: read back by a later Runtime", st_g == 200 and got == inst and st_l == 200 and KEY in keys
      and (inst or {}).get("runtime_id") is not None,
      f"GET → {st_g} identical={got == inst}; listed {KEY in keys}; {len(keys)} instances")
st_d, _ = req("POST", "/api/v1/agent-instances", body=BODY)
st_u, _ = req("POST", "/api/v1/agent-instances", body=dict(BODY, definition="no-such-agent", instance_key=KEY + "-u"))
st_c, _ = req("POST", "/api/v1/agent-instances", body=dict(BODY, instance_key=KEY + "-c", capabilities=["not-a-capability"]))
st_k, _ = req("POST", "/api/v1/agent-instances", body=dict(BODY, instance_key="BAD KEY"))
st_f, _ = req("POST", "/api/v1/agent-instances", body=dict(BODY, instance_key=KEY + "-f", grants_authority=True))
st_n, _ = req("GET", "/api/v1/agent-instances/does-not-exist")
check("Scenario A: failure paths are meaningful", (st_d, st_u, st_c, st_k, st_f, st_n) == (409, 400, 400, 400, 400, 404),
      f"duplicate → {st_d}; unknown Definition → {st_u}; foreign capability → {st_c}; bad key → {st_k}; unknown field → {st_f}; unknown instance → {st_n}")
# concurrency: one key, many requests -> exactly one 201
N = 6; out = [None] * N; bar = threading.Barrier(N); CK = KEY + "-race"
transport_errors = []
def one(i):
    bar.wait()
    for attempt in range(3):
        try:
            out[i] = req("POST", "/api/v1/agent-instances", body=dict(BODY, instance_key=CK))[0]; return
        except urllib.error.URLError as e:     # no HTTP response at all: transport, not the application
            transport_errors.append(f"thread {i} attempt {attempt}: {type(e.reason).__name__}")
            time.sleep(1)
ts = [threading.Thread(target=one, args=(i,)) for i in range(N)]
[t.start() for t in ts]; [t.join(180) for t in ts]
st_l2, lst2 = req("GET", "/api/v1/agent-instances")
n_rec = sum(1 for i in (lst2 or {}).get("instances", []) if i["instance_key"] == CK)
check("Scenario A: concurrent registration of one key yields one registration", out.count(201) == 1 and n_rec == 1 and set(out) <= {201, 409},
      f"statuses {sorted(out, key=str)}; transport retries {len(transport_errors)}; registrations visible for the key: {n_rec}")
st_t, tr = req("GET", "/api/v1/audit?limit=200")
ent = [e for e in (tr or {}).get("entries", []) if e["path"] == "/api/v1/agent-instances" and e["method"] == "POST"]
ok_aud = any(e["decision"] == "allowed" and e["subject"] == "founder" for e in ent) and any(e["decision"] == "refused" and e["status"] == 401 for e in ent)
leak = any(s in json.dumps(ent) for s in (TOKEN, BYPASS))
check("Scenario A: audit records the registration decisions, no credential", st_t == 200 and ok_aud and not leak,
      f"{len(ent)} POST agent-instances audit entries; allowed+founder and refused 401 present: {ok_aud}; credential in audit: {leak}")
json.dump({"base": BASE, "results": res, "requests": raw, "instance_keys": [KEY, CK]}, open(f"{S}/live_a_09.json", "w"), indent=1)
for r in res: print(r["result"], r["check"], "|", r["evidence"])
