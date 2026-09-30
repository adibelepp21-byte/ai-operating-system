import json, sys, time, urllib.request, urllib.error, datetime
BASE=sys.argv[1].rstrip("/"); S="."
T=open("token").read().strip(); Y=open("bypass09").read().strip()
def req(m,p,auth=True,body=None,bearer=None):
    h={"x-vercel-protection-bypass":Y,"Accept":"application/json"}
    if auth: h["Authorization"]=bearer or "Bearer "+T
    d=json.dumps(body).encode() if body is not None else None
    if d: h["Content-Type"]="application/json"
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE+p,data=d,headers=h,method=m),timeout=90) as r: st,hd=r.status,dict(r.headers); r.read()
    except urllib.error.HTTPError as e: st,hd=e.code,dict(e.headers); e.read()
    return st,(hd.get("X-Request-Id") or hd.get("x-request-id"))
key="obs-desk-"+datetime.datetime.utcnow().strftime("%H%M%S")
B={"definition":"engineering-intelligence-agent","instance_key":key,"capabilities":["engineering-intelligence"]}
RUN={"workflow":"document-conformance-review","inputs":{"document":"docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md","criteria":["INV-4"]}}
start=datetime.datetime.utcnow().isoformat(timespec="seconds")
calls=[("GET","/api/v1/health",False,None,None),("GET","/api/v1/runs",False,None,None),("GET","/api/v1/runs",True,None,"Bearer wrong-token-x"),
 ("POST","/api/v1/runs",True,RUN,None),("POST","/api/v1/runs",True,dict(RUN,inputs=dict(RUN["inputs"],document="docs/absent.md")),None),
 ("POST","/api/v1/agent-instances",True,B,None),("POST","/api/v1/agent-instances",True,B,None),("POST","/api/v1/agent-instances",True,dict(B,definition="nope",instance_key=key+"-x"),None),
 ("GET","/api/v1/agent-instances/"+key,True,None,None),("GET","/api/v1/agent-instances/absent-one",True,None,None),("GET","/api/v1/audit?limit=5",True,None,None),("GET","/api/v1/session",True,None,None)]
out=[]
for m,p,a,b,br in calls:
    st,rid=req(m,p,auth=a,body=b,bearer=br); out.append({"method":m,"path":p.split("?")[0],"status":st,"request_id":rid}); time.sleep(0.3)
end=datetime.datetime.utcnow().isoformat(timespec="seconds")
json.dump({"start":start,"end":end,"key":key,"requests":out},open("obs_probe.json","w"),indent=1)
print(start,end,key)
for o in out: print(o)
