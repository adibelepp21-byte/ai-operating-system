"""CG-7 — P12 operational state reconciliation. READ-ONLY EVIDENCE TOOL.

Directive: docs/governance/acts/DIR-AIOS-CG7-P12-OPERATIONAL-STATE-RECONCILIATION-GATE.md.

Not an AIOS subsystem; nothing imports it. It:
* hashes every file under the certified P12 root, the P12 manifest's files, and
  every grant / escalation / response / instance / disposition record in the
  repository, **before** any reader runs and again **after**;
* traces each P12 grant and escalation to its record, producer, creating
  commit, joins, manifests, trace stores and the readers that report it;
* writes only its own JSON output, outside every certified root.

It issues, revokes, completes, answers, registers and moves nothing. If any
hashed byte differs after the readers ran, ``integrity.before_equals_after`` is
false and the result must not be reported as a clean reconciliation.
"""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

P12 = REPO / "docs/architecture/p12"
W4 = P12 / "w4-operations"
W3 = P12 / "w3-operations"
MANIFEST = REPO / "docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"
CAPABILITY_GATE = Path(__file__).with_name("CAPABILITY-DISCOVERY-2026-10-03.json")
OUT = Path(__file__).with_name("CG7-P12-STATE-RECONCILIATION-2026-10-03.json")
STATE_GLOBS = ("*.delegation.json", "*.escalation.json", "*.response.json",
               "*.instance.json", "*.disposition.json", "*.governance-join.json")


def rel(p):
    return str(Path(p).resolve().relative_to(REPO))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def snapshot():
    """Every byte this gate must not change."""
    certified = {rel(p): sha(p) for p in sorted(P12.rglob("*")) if p.is_file()}
    state = {rel(p): sha(p) for g in STATE_GLOBS for p in sorted(REPO.glob(f"docs/**/{g}"))}
    governance = {rel(p): sha(p) for p in (
        REPO / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md", MANIFEST)}
    return {"p12_tree": certified, "state_records": state, "governance": governance}


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# ── 0. BEFORE ────────────────────────────────────────────────────────────────
BEFORE = snapshot()
HEAD = git("rev-parse", "HEAD")
STATUS_BEFORE = git("status", "--porcelain", "--", "docs/architecture/p11", "docs/architecture/p12",
                    "docs/architecture/p13", "docs/architecture/platform-organization")

from tools import certified_evidence_integrity as integrity  # noqa: E402
from tools.authority_citation import refusal  # noqa: E402
from tools.delegation_catalog import operation_roots  # noqa: E402
from tools.escalation_register import LIVE_RESPONSES, EscalationRegister  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402
from tools.w4_continuity import continuation_conditions, operational_state, reconstruct  # noqa: E402
from tools.w4_delegation import (AUTHORIZED_DELEGATOR, LIVE_LEDGER,  # noqa: E402
                                 plan_completion, read_dispositions)

manifest = load(MANIFEST)
manifest_files = manifest["files"]
manifest_check = {
    "entries": len(manifest_files),
    "mismatched": [k for k, v in manifest_files.items() if BEFORE["p12_tree"].get(k) != v],
    "missing": [k for k in manifest_files if k not in BEFORE["p12_tree"]],
    "in_tree_not_in_manifest": sorted(set(BEFORE["p12_tree"]) - set(manifest_files)),
    "certified_commit": manifest["certified_commit"],
    "certifying_instrument": manifest["certifying_instrument"],
}

# ── A. Inventory ─────────────────────────────────────────────────────────────
grants = {p.name.split(".")[0]: p for p in sorted(W4.glob("*.delegation.json"))}
escalations = {p.name.split(".")[0]: p for d in (W3, W4) for p in sorted(d.glob("*.escalation.json"))}
joins = {load(p)["escalation_id"]: load(p) for d in (W3, W4) for p in d.glob("*.governance-join.json")}
manifests = {load(p)["delegation_id"]: {"file": rel(p), **{k: load(p)[k] for k in (
    "execution_id", "status", "trace_store", "trace_ordinal", "delegation_status", "outcome")}}
    for p in sorted((P12 / "execution-provenance").glob("*.manifest.json"))}
trace_stores = {p.parent.name: sum(1 for line in p.read_text(encoding="utf-8").splitlines() if line.strip())
                for p in sorted((P12 / "trace-stores").glob("*/trace"))}
instances_everywhere = {}
for p in REPO.glob("docs/**/*.instance.json"):
    instances_everywhere.setdefault(load(p).get("instance_key", p.name.split(".")[0]), []).append(rel(p))

producers = sorted(p for p in list(REPO.glob("*.py")) + list((REPO / "tools").glob("*.py"))
                   if "/tests/" not in str(p))


def producer_of(plan_key):
    return [rel(p) for p in producers if plan_key and plan_key in p.read_text(encoding="utf-8")]


def created(path):
    line = git("log", "--diff-filter=A", "--format=%h %ad %s", "--date=iso", "--", rel(path)).splitlines()
    return line[-1] if line else None


def commits_touching(path):
    return git("log", "--format=%h", "--", rel(path)).split()


def files_at(commit, pattern):
    return [f for f in git("show", "--name-only", "--format=", commit).splitlines() if re.search(pattern, f)]


capability_levels = {"engineering-intelligence": "C6", "cognitive-intelligence": "C4",
                     "governance-artifact-integrity": "C2"}
if CAPABILITY_GATE.is_file():
    probes = load(CAPABILITY_GATE).get("live_probes", {})
    capability_levels["_source"] = rel(CAPABILITY_GATE)
    capability_levels["_engineering_probe"] = probes.get("engineering-intelligence", {}).get("path")

# ── B. Grants ────────────────────────────────────────────────────────────────
grant_rows = {}
for gid, path in grants.items():
    r = load(path)
    plan = (r.get("lifecycle_boundary") or "").replace("one execution of plan ", "")
    birth = created(path)
    commit = birth.split()[0] if birth else None
    met, evidence, reasons = plan_completion(W4, r)
    joined_escalations = [e for e, j in joins.items() if j.get("delegation_id") == gid]
    grant_rows[gid] = {
        "record": rel(path), "sha256": sha(path),
        "status_in_record": r.get("status"),
        "revocation_fields": {k: r[k] for k in r if "revoc" in k},
        "delegator": r.get("delegator"),
        "delegator_is_authorized_constant": r.get("delegator") == AUTHORIZED_DELEGATOR,
        "authority": f"{r.get('authority_instrument')} ({r.get('authority_record')})",
        "authority_citation_refusal": refusal(r.get("authority_instrument"), r.get("authority_record"),
                                              "FD-P11-001"),
        "authority_chain": r.get("authority_chain"),
        "recipient": r.get("recipient_instance"),
        "recipient_instance_record_in_root": (W4 / f"{r.get('recipient_instance')}.instance.json").is_file(),
        "recipient_instance_records_elsewhere": instances_everywhere.get(r.get("recipient_instance"), []),
        "capability_scope": r.get("capability_scope"),
        "capability_level": [capability_levels.get(c, "C0") for c in r.get("capability_scope", [])],
        "work_scope": r.get("work_scope"), "objective": r.get("objective"),
        "plan": plan, "termination_condition": r.get("termination_condition"),
        "issued_at": r.get("issued_at"),
        "producer": producer_of(plan),
        "creating_commit": birth,
        "commits_touching_record": commits_touching(path),
        "co_created_in_commit": files_at(commit, r"p12/(w[34]-operations|execution-provenance|trace-stores)")
        if commit else [],
        "execution_manifest": manifests.get(gid),
        "escalations_joined": joined_escalations,
        "plan_completion_reader": {"met": met, "evidence": rel(evidence) if evidence else None,
                                   "reasons": list(reasons)},
    }

# Record shape: what the sanctioned issuer (`W4DelegationRegistry.issue`) emits
# today, in memory only (registry roots None; nothing is written).
from tools.agent_instance_registry import AgentInstanceRegistry  # noqa: E402
from tools.planning import AuthorityProvenance  # noqa: E402
from tools.w4_delegation import W4DelegationRegistry  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402
_memory = AgentInstanceRegistry(None)
_memory.register(instance_key="shape-probe", definition=SELECTED_DEFINITION,
                 permitted_capabilities=("engineering-intelligence",), created_by=AUTHORIZED_DELEGATOR,
                 authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD), accountable_to=AUTHORIZED_DELEGATOR)
_probe = W4DelegationRegistry(_memory, None).issue(
    delegator=AUTHORIZED_DELEGATOR, recipient_instance="shape-probe",
    authority=AuthorityProvenance("FD-P11-001 §9", FD_RECORD), objective="o",
    capability_scope=("engineering-intelligence",), work_scope=("s",), lifecycle_boundary="one execution of plan p",
    resource_boundary="r", output_expectation="o", verification_requirement="v", escalation_condition="e",
    accountable_party=AUTHORIZED_DELEGATOR, termination_condition="t")
ISSUER_KEYS = sorted(_probe.to_payload())
for gid, row in grant_rows.items():
    keys = sorted(load(grants[gid]))
    row["record_keys_equal_issuer_payload"] = keys == ISSUER_KEYS
    row["record_keys_diff"] = sorted(set(keys) ^ set(ISSUER_KEYS))

# ── C. Escalations ───────────────────────────────────────────────────────────
escalation_rows = {}
for eid, path in escalations.items():
    e = load(path)
    root = path.parent
    register = EscalationRegister(root)
    birth = created(path)
    join = joins.get(eid, {})
    responses_beside = sorted(p.name for p in root.glob(f"{eid}.response*"))
    live = sorted(rel(p) for p in LIVE_RESPONSES.rglob(f"{eid}*")) if LIVE_RESPONSES.is_dir() else []
    escalation_rows[eid] = {
        "record": rel(path), "sha256": sha(path), "root": rel(root),
        "subject": e.get("subject"), "required": e.get("required"), "held": e.get("held"),
        "reason": e.get("reason"), "refusal_type": e.get("refusal_type") or join.get("refusal_type"),
        "authority": f"{e.get('authority_instrument')} ({e.get('authority_record')})",
        "raised_at": e.get("raised_at"),
        "governance_join": join or None,
        "joined_grant_record": rel(grants[join["delegation_id"]]) if join.get("delegation_id") in grants else None,
        "creating_commit": birth,
        "commits_touching_record": commits_touching(path),
        "response_beside_record": responses_beside,
        "response_in_live_ledger": live,
        "register_status": register.status(eid),
    }

# ── E. Readers ───────────────────────────────────────────────────────────────
readers = {}
for root in (W4, W3):
    hist = reconstruct(root)
    oper = operational_state(root)
    dispositions, disposition_faults = read_dispositions(root)
    readers[rel(root)] = {
        "reconstruct (historical)": {"active_grants": hist["active_grants"],
                                     "open_escalations": hist["open_escalations"],
                                     "conditions": list(continuation_conditions(hist))},
        "operational_state (S-1 A2/B1)": {"active_grants": oper["active_grants"],
                                          "open_escalations": oper["open_escalations"],
                                          "operational_dispositions": oper.get("operational_dispositions"),
                                          "disposition_faults": oper.get("disposition_faults"),
                                          "conditions": list(continuation_conditions(oper))},
        "read_dispositions": {"valid": dispositions, "faults": list(disposition_faults),
                              "ledger_folder": rel(Path(LIVE_LEDGER) / root.name)},
        "EscalationRegister.open_escalations": list(EscalationRegister(root).open_escalations()),
        "in_delegation_catalog.operation_roots": root in operation_roots(),
        "is_protected (certified)": is_protected(root),
    }
readers["ledger_namespace"] = {
    "live_ledger_keying": "LIVE_LEDGER / Path(root).name",
    "p11_and_p12_share_basename": (REPO / "docs/architecture/p11/w4-operations").name == W4.name,
    "live_ledger_w4_operations": sorted(p.name for p in (Path(LIVE_LEDGER) / W4.name).glob("*")),
    "live_responses_w4_operations": sorted(p.name for p in (Path(LIVE_RESPONSES) / W4.name).glob("*")),
}
readers["operation_roots()"] = [rel(p) for p in operation_roots()]
for name, mod, fn in (("p12_execution_chain_reader.summary", "tools.p12_execution_chain_reader", "summary"),
                      ("p12_provenance_verification.summary", "tools.p12_provenance_verification", "summary"),
                      ("p12_failure_verification.escalation_join", "tools.p12_failure_verification",
                       "escalation_join")):
    try:
        readers[name] = getattr(__import__(mod, fromlist=[fn]), fn)()
    except Exception as exc:  # recorded, not hidden
        readers[name] = f"ERROR {type(exc).__name__}: {exc}"

# ── 0. AFTER ─────────────────────────────────────────────────────────────────
AFTER = snapshot()
STATUS_AFTER = git("status", "--porcelain", "--", "docs/architecture/p11", "docs/architecture/p12",
                   "docs/architecture/p13", "docs/architecture/platform-organization")
changed = {k: sorted(set(BEFORE[k].items()) ^ set(AFTER[k].items())) for k in BEFORE}
integrity_faults = [str(f) for f in integrity.verify().faults]

result = {
    "tool": "READ-ONLY EVIDENCE TOOL — CG-7",
    "collected_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": sha(__file__),
    "baseline": {
        "commit": HEAD,
        "certified_root": rel(P12), "certified_root_protected": is_protected(P12),
        "p12_tree_files": len(BEFORE["p12_tree"]),
        "p12_tree_digest": hashlib.sha256(json.dumps(BEFORE["p12_tree"], sort_keys=True).encode()).hexdigest(),
        "manifest": manifest_check,
        "operational_folders_in_p12": [rel(W3), rel(W4)],
        "active_grants_historical": readers[rel(W4)]["reconstruct (historical)"]["active_grants"],
        "open_escalations": {r: readers[r]["EscalationRegister.open_escalations"] for r in (rel(W3), rel(W4))},
        "git_status_certified_before": STATUS_BEFORE or "(clean)",
    },
    "inventory": {
        "grants": list(grants), "escalations": list(escalations),
        "governance_joins": joins, "execution_manifests": manifests, "trace_stores": trace_stores,
        "instance_records_in_p12": sorted(rel(p) for p in P12.rglob("*.instance.json")),
        "evidence_records_in_p12": sorted(rel(p) for p in P12.rglob("*.evidence.json")),
        "capability_levels": capability_levels,
    },
    "grants": grant_rows,
    "escalations": escalation_rows,
    "readers": readers,
    "integrity": {
        "before_equals_after": not any(changed.values()),
        "changed": changed,
        "files_hashed": {k: len(v) for k, v in BEFORE.items()},
        "certified_evidence_integrity_faults": integrity_faults,
        "git_status_certified_after": STATUS_AFTER or "(clean)",
    },
}
OUT.write_text(json.dumps(result, indent=1, default=str, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"commit": HEAD, "grants": len(grants), "escalations": len(escalations),
                  "manifest": {k: manifest_check[k] for k in ("entries", "mismatched", "missing")},
                  "before_equals_after": result["integrity"]["before_equals_after"],
                  "integrity_faults": integrity_faults}, indent=1))
