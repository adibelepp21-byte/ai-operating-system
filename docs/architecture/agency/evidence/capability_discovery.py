"""Capability Discovery & Reconciliation Gate: evidence collection (read-only).

Directive: docs/governance/acts/DIR-AIOS-CAPABILITY-DISCOVERY-RECONCILIATION-GATE.md.

Computes, from the repository as it stands, the facts every classification in
`CAPABILITY-DISCOVERY-RECONCILIATION-2026-10-03.md` rests on. It creates no
capability, instance, grant or record anywhere in the repository. Executions run
on a temporary runtime and are discarded. It writes only its own JSON beside
this script.
"""
import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from consumers.cognitive_intelligence_agent import CognitiveIntelligenceAgent  # noqa: E402
from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from native_core.core.governance import HumanAuthority  # noqa: E402,F401
from native_core.core.infrastructure import LocalAppendOnlyStorage, LocalExecutionSubstrate  # noqa: E402
from native_core.core.runtime.composition import create_runtime  # noqa: E402
from native_core.core.runtime.execution import create_execution_layer  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.agent_instance_registry import AgentInstanceRegistry, InstanceRegistrationError  # noqa: E402
from tools.escalation_register import EscalationRegister, EscalationRegisterError  # noqa: E402
from tools.organization_catalog import read_departments  # noqa: E402
from tools.planning import AuthorityProvenance, Plan, PlanStep  # noqa: E402
from tools.w4_continuity import continuation_conditions, operational_state, reconstruct  # noqa: E402
from tools.w4_execution import W4Executor  # noqa: E402
from tools.w4_first_run import FD_RECORD, SELECTED_DEFINITION  # noqa: E402

OUT = Path(__file__).with_name("CAPABILITY-DISCOVERY-2026-10-03.json")
CATALOG = REPO / "docs/architecture/organization/execution-catalog"


def rel(p):
    return str(Path(p).relative_to(REPO))


def files_naming(token, roots, pattern="*.json"):
    found = []
    for root in roots:
        for path in (REPO / root).rglob(pattern):
            try:
                if token in path.read_text(encoding="utf-8"):
                    found.append(rel(path))
            except (OSError, UnicodeDecodeError):
                continue
    return sorted(found)


# 1. Canonical catalog (ADR-established Capabilities, owners, Agent Definitions).
departments = read_departments()
catalog = [{"department": d.key, "established_by": list(d.establishing_adrs),
            "capabilities": list(d.capabilities), "agent_definitions": list(d.agent_definitions)}
           for d in departments]
canonical = sorted(c for d in departments for c in d.capabilities)

# 2. Consumers that realize a capability (resident code naming the capability).
consumer_files = sorted(p for p in (REPO / "consumers").glob("*.py") if p.name != "__init__.py")
consumers_by_capability = {
    cap: [rel(p) for p in consumer_files if cap in p.read_text(encoding="utf-8")]
    for cap in canonical}

# 3. Live probes through the lawful public path, on a temporary runtime.
probes = {}
with tempfile.TemporaryDirectory() as tmp:
    storage = LocalAppendOnlyStorage(Path(tmp) / "store")
    storage.provision()
    substrate = LocalExecutionSubstrate()
    substrate.provision()
    runtime = create_runtime(runtime_id="capability-discovery-probe", storage=storage,
                             substrate=substrate)
    runtime.initialize()
    runtime.start()
    eng = EngineeringIntelligenceAgent(
        artifact=Artifact(name="probe", lines=("Objective: x", "Audience: y")),
        criteria=[ConformanceCriterion("objective", "Objective:"),
                  ConformanceCriterion("measure", "Measure:")])
    eng.participate(create_execution_layer(runtime))
    probes["engineering-intelligence"] = {
        "path": "EngineeringIntelligenceAgent.participate(create_execution_layer(RUNNING runtime))",
        "result": [(r.criterion_name, r.satisfied) for r in eng.results]}
    cog = CognitiveIntelligenceAgent(unit_of_work="draft the brief; review the brief; publish the brief")
    cog.participate(create_execution_layer(runtime))
    probes["cognitive-intelligence"] = {
        "path": "CognitiveIntelligenceAgent.participate(create_execution_layer(RUNNING runtime))",
        "result": [s.statement if hasattr(s, "statement") else str(s) for s in cog.decomposition]}
    probes["governance-artifact-integrity"] = {
        "path": None, "result": "no resident consumer realizes this capability"}

# 4. Integration: grants by capability, instances by definition, everywhere.
grants, instances = [], []
for path in sorted(REPO.glob("docs/**/*.delegation.json")):
    d = json.loads(path.read_text(encoding="utf-8"))
    grants.append({"root": rel(path.parent), "id": d["delegation_id"],
                   "capability": d.get("capability_scope"), "status": d.get("status"),
                   "recipient": d.get("recipient_instance")})
for path in sorted(REPO.glob("docs/**/*.instance.json")):
    d = json.loads(path.read_text(encoding="utf-8"))
    instances.append({"root": rel(path.parent), "instance": d.get("instance_key"),
                      "definition": d.get("definition_key"),
                      "capabilities": d.get("permitted_capabilities")})
integration = {cap: {
    "instances": sorted({i["instance"] for i in instances if cap in (i["capabilities"] or [])}),
    "grants_total": sum(1 for g in grants if cap in (g["capability"] or [])),
    "grants_active": sum(1 for g in grants if cap in (g["capability"] or []) and g["status"] == "ACTIVE"),
    "evidence_records_naming_capability": files_naming(cap, ["docs/architecture/p11", "docs/architecture/p12",
                                                             "docs/architecture/agency/operations"],
                                                       "*.evidence.json")}
    for cap in canonical}

# 5. Execution catalog: workflows, skills, Tool interfaces, runtime substrates.
evidence_roots = ["docs/architecture/p11", "docs/architecture/p12", "docs/architecture/p13"]
exec_catalog = {}
for kind in ("workflow", "skill", "tool", "runtime"):
    exec_catalog[kind] = {}
    for path in sorted((CATALOG / kind).glob("*.md")):
        key = path.stem
        exec_catalog[kind][key] = {
            "evidence_files": files_naming(f'"{key}"', evidence_roots) +
                              files_naming(f"workflow_key='{key}'", evidence_roots),
            "code_refs": [rel(p) for p in list((REPO / "tools").glob("*.py")) +
                          list((REPO / "consumers").glob("*.py")) +
                          list((REPO / "native_core").rglob("*.py")) + list(REPO.glob("*.py"))
                          if "/tests/" not in str(p) and key in p.read_text(encoding="utf-8")]}
resident_tools = sorted({rel(p) for p in list(REPO.rglob("*.py"))
                         if "/tests/" not in str(p) and "node_modules" not in str(p)
                         and p.resolve() != Path(__file__).resolve()
                         and "(ExternalTool)" in p.read_text(encoding="utf-8", errors="ignore")})

# 6. Live operational state across every folder holding W4 records.
roots = sorted({p.parent for p in REPO.glob("docs/**/*.delegation.json")})
state = {}
for root in roots:
    s = reconstruct(root)            # historical reading (the records as they are)
    o = operational_state(root)      # S-1 A2 / B1 reading (live ledgers honoured)
    state[rel(root)] = {"active": len(s["active_grants"]), "open_escalations": s["open_escalations"],
                        "instances": s["instances"],
                        "conditions": list(continuation_conditions(s)),
                        "operational": {"active": o["active_grants"],
                                        "open_escalations": o["open_escalations"],
                                        "dispositions": o.get("operational_dispositions", {}),
                                        "conditions": list(continuation_conditions(o))}}
for root in sorted({p.parent for p in REPO.glob("docs/**/*.escalation.json")} - set(roots)):
    state[rel(root)] = {"open_escalations": list(EscalationRegister(root).open_escalations())}

# 7. Negative controls through existing lawful interfaces (in memory; nothing written).
memory = AgentInstanceRegistry(None)
memory.register(instance_key="engineering-intelligence-instance-001", definition=SELECTED_DEFINITION,
                permitted_capabilities=("engineering-intelligence",),
                created_by=w4.AUTHORIZED_DELEGATOR,
                authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
                accountable_to=w4.AUTHORIZED_DELEGATOR)
issuer = w4.W4DelegationRegistry(memory, None)
FD9 = AuthorityProvenance("FD-P11-001 §9", FD_RECORD)
TERMS = dict(objective="o", work_scope=("s",), lifecycle_boundary="one execution of plan p",
             resource_boundary="r", output_expectation="o", verification_requirement="v",
             escalation_condition="e", accountable_party=w4.AUTHORIZED_DELEGATOR,
             termination_condition=w4.TERMINATION_ON_PLAN)


def refused(call):
    try:
        call()
        return "NOT REFUSED"
    except (w4.DelegationError, InstanceRegistrationError, EscalationRegisterError,
            TypeError, KeyError) as exc:
        return f"refused: {type(exc).__name__}"


def issue(**over):
    kw = dict(delegator=w4.AUTHORIZED_DELEGATOR, recipient_instance="engineering-intelligence-instance-001",
              authority=FD9, capability_scope=("engineering-intelligence",), **TERMS)
    kw.update(over)
    return lambda: issuer.issue(**kw)


catalog_before = sorted(canonical)
with tempfile.TemporaryDirectory() as tmp:
    esc_root = Path(tmp)
    (esc_root / "e1.escalation.json").write_text(json.dumps({"escalation_id": "e1"}))
    grant = issuer.issue(delegator=w4.AUTHORIZED_DELEGATOR,
                         recipient_instance="engineering-intelligence-instance-001",
                         authority=FD9, capability_scope=("engineering-intelligence",),
                         **{**TERMS, "work_scope": ("a",)})
    plan = Plan(key="p", goal_key="g", authority=AuthorityProvenance(
        "probe", "docs/governance/acts/DIR-AIOS-CAPABILITY-DISCOVERY-RECONCILIATION-GATE.md"),
        steps=(PlanStep("a", "in scope"), PlanStep("b", "out of scope", depends_on=("a",))))
    report = W4Executor(grant, memory).execute_plan(plan, lambda step: "ok")
    controls = {
        "1_agent_cannot_create_capability_beyond_definition": refused(lambda: memory.register(
            instance_key="engineering-intelligence-instance-002", definition=SELECTED_DEFINITION,
            permitted_capabilities=("creative-content",), created_by=w4.AUTHORIZED_DELEGATOR,
            authority=AuthorityProvenance("FD-P11-001 §7", FD_RECORD),
            accountable_to=w4.AUTHORIZED_DELEGATOR)),
        "2_capability_holder_gains_no_authority_to_delegate": refused(issue(
            delegator="engineering-intelligence-instance-001")),
        "3_candidate_name_not_canonical_or_recipient": refused(issue(recipient_instance="franky")),
        "4_capability_not_authorized_for_recipient": refused(issue(capability_scope=("cognitive-intelligence",))),
        "5_documented_only_capability_not_delegable": refused(issue(capability_scope=("strategic-planning",))),
        "6_missing_capability_not_auto_created": sorted(c for d in read_departments() for c in d.capabilities)
                                                 == catalog_before,
        "7_capability_cannot_change_governance": refused(lambda: EscalationRegister(esc_root).record_response(
            "e1", authority="engineering-intelligence-instance-001", response="approved")),
        "8_luffy_is_not_the_ceo": refused(issue(delegator="Monkey D. Luffy")),
        "9_agent_cannot_delegate_to_agent": refused(issue(delegator="engineering-intelligence-instance-001",
                                                          recipient_instance="governance-artifact-integrity-instance-001")),
        "10_capability_boundary_not_bypassed": {o.step_key: o.status for o in report.outcomes},
    }

result = {
    "collected_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "canonical_catalog": catalog,
    "consumers": [rel(p) for p in consumer_files],
    "consumers_by_capability": consumers_by_capability,
    "live_probes": probes,
    "instances": instances,
    "grants": {"total": len(grants), "active": sum(g["status"] == "ACTIVE" for g in grants),
               "by_root": {r: sum(1 for g in grants if g["root"] == r) for r in sorted({g["root"] for g in grants})}},
    "integration": integration,
    "execution_catalog": exec_catalog,
    "resident_external_tools": resident_tools,
    "operational_state": state,
    "negative_controls": controls,
}
OUT.write_text(json.dumps(result, indent=1, default=str) + "\n", encoding="utf-8")
print(json.dumps({"canonical": canonical, "consumers_by_capability": consumers_by_capability,
                  "probes": probes, "integration": {k: {kk: (vv if kk != "evidence_records_naming_capability" else len(vv)) for kk, vv in v.items()} for k, v in integration.items()},
                  "workflows": {k: len(v["evidence_files"]) for k, v in exec_catalog["workflow"].items()},
                  "tools": {k: (len(v["evidence_files"]), len(v["code_refs"])) for k, v in exec_catalog["tool"].items()},
                  "runtime_substrates": {k: (len(v["evidence_files"]), len(v["code_refs"])) for k, v in exec_catalog["runtime"].items()},
                  "resident_external_tools": resident_tools,
                  "state": {k: {kk: vv for kk, vv in v.items() if kk != "conditions"} for k, v in state.items()},
                  "controls": controls}, indent=1, default=str))
