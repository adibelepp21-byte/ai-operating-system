"""CG-7 remediation evidence (FD-CG7-001 `§13`, `§14`). READ-ONLY EVIDENCE TOOL.

``python3 cg7_remediation_evidence.py baseline`` captures the pre-remediation
state and writes ``CG7-REMEDIATION-BASELINE-2026-10-03.json``.
``python3 cg7_remediation_evidence.py verify`` captures it again, compares it
with the baseline and writes ``CG7-REMEDIATION-VERIFICATION-2026-10-03.json``.

It reads only. Every reader it calls is a resident one; it writes nothing but
its own JSON output, outside every certified root.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

HERE = Path(__file__).parent
BASELINE = HERE / "CG7-REMEDIATION-BASELINE-2026-10-03.json"
VERIFICATION = HERE / "CG7-REMEDIATION-VERIFICATION-2026-10-03.json"
P11_ROOTS = ("docs/architecture/p11/w1-operations", "docs/architecture/p11/w4-operations",
             "docs/architecture/p11/x-department-operations")
P12_ROOTS = ("docs/architecture/p12/w4-operations", "docs/architecture/p12/w3-operations")
AGENCY_ROOTS = ("docs/architecture/agency/operations/w4-s2-plan-delegation",
                "docs/architecture/agency/operations/w4-s3-founder-goal")
CODE = ("tools/w4_delegation.py", "tools/w4_continuity.py", "tools/escalation_register.py",
        "tools/delegation_catalog.py", "tools/p12_execution_provenance.py",
        "tools/tests/test_w4_operational_ledger.py")
NINE = ("08e14bd7aa584ea5", "332d42f021764ab6", "522e84af52444890", "632b256f8335434f",
        "84e94ea2f001444d", "aa591daf55ca4714", "b304c7ecb1024454", "e668a317fa494342",
        "e6a3d622cfb54b4f")
LIVE_PAIR = {"grant": "2494015de36246fd", "escalation": "9cb90fa0787a478c"}
HISTORICAL_ESCALATIONS = ("0991300404cf44d8", "9d6bc0ad47294ef0")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, default=str, ensure_ascii=False)


def capture():
    from tools import certified_evidence_integrity as integrity
    from tools.escalation_register import LIVE_RESPONSES, EscalationRegister
    from tools.w4_continuity import operational_state, reconstruct
    from tools.w4_delegation import plan_completion

    p12_tree = {str(p.relative_to(REPO)): sha(p)
                for p in sorted((REPO / "docs/architecture/p12").rglob("*")) if p.is_file()}
    manifest = json.loads((REPO / "docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json")
                          .read_text(encoding="utf-8"))["files"]
    records = {str(p.relative_to(REPO)): sha(p)
               for g in ("*.delegation.json", "*.escalation.json", "*.instance.json",
                         "*.governance-join.json", "*.evidence.json")
               for root in P11_ROOTS + P12_ROOTS + AGENCY_ROOTS
               for p in sorted((REPO / root).glob(g))}

    readers = {}
    for root in P11_ROOTS + P12_ROOTS + AGENCY_ROOTS:
        path = REPO / root
        hist = reconstruct(path)
        oper = operational_state(path)
        completion = {}
        for rec in sorted(path.glob("*.delegation.json")):
            met, evidence, reasons = plan_completion(path, json.loads(rec.read_text(encoding="utf-8")))
            completion[rec.name.split(".")[0]] = {
                "met": met, "evidence": str(evidence.relative_to(REPO)) if evidence else None,
                "reasons": list(reasons)}
        readers[root] = {
            "historical": json.loads(canonical(hist)),
            "operational": json.loads(canonical(oper)),
            "escalation_status": {e: EscalationRegister(path).status(e)
                                  for e in EscalationRegister(path).all_escalations()},
            "escalation_status_operational": {
                e: EscalationRegister(path, response_ledger=LIVE_RESPONSES).status(e)
                for e in EscalationRegister(path).all_escalations()},
            "plan_completion": completion,
        }
    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "head": git("rev-parse", "HEAD"),
        "code_sha256": {f: sha(REPO / f) for f in CODE},
        "p12_tree": p12_tree,
        "p12_tree_digest": hashlib.sha256(canonical(p12_tree).encode()).hexdigest(),
        "p12_manifest_mismatches": [k for k, v in manifest.items() if p12_tree.get(k) != v],
        "state_record_sha256": records,
        "integrity_faults": [str(f) for f in integrity.verify().faults],
        "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p11",
                                    "docs/architecture/p12", "docs/architecture/p13",
                                    "docs/architecture/platform-organization") or "(clean)",
        "readers": readers,
        "counts": {root: {"historical_active": len(readers[root]["historical"]["active_grants"]),
                          "operational_active": len(readers[root]["operational"]["active_grants"]),
                          "historical_open": len(readers[root]["historical"]["open_escalations"]),
                          "operational_open": len(readers[root]["operational"]["open_escalations"])}
                   for root in readers},
        "subjects": {"nine_historical_grants": list(NINE), "live_pair": LIVE_PAIR,
                     "historical_escalations": list(HISTORICAL_ESCALATIONS)},
    }


def main(mode):
    now = capture()
    if mode == "baseline":
        BASELINE.write_text(json.dumps(now, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"head": now["head"], "counts": now["counts"],
                          "p12_tree_digest": now["p12_tree_digest"],
                          "manifest_mismatches": now["p12_manifest_mismatches"],
                          "integrity_faults": now["integrity_faults"]}, indent=1))
        return 0
    return verify(now)


def verify(now):
    """`§14` A–G, computed from the baseline and the current capture."""
    from tools import w4_delegation as w4
    from tools.w4_continuity import operational_overview
    before = json.loads(BASELINE.read_text(encoding="utf-8"))
    p11 = {r: {k: before["readers"][r][k] == now["readers"][r][k]
               for k in ("historical", "operational", "escalation_status",
                         "escalation_status_operational", "plan_completion")}
           for r in P11_ROOTS}
    agency = {r: {k: before["readers"][r][k] == now["readers"][r][k]
                  for k in ("historical", "operational")} for r in AGENCY_ROOTS}
    historical_p12 = {r: before["readers"][r]["historical"] == now["readers"][r]["historical"]
                      for r in P12_ROOTS}
    w4root = now["readers"][P12_ROOTS[0]]
    w3root = now["readers"][P12_ROOTS[1]]
    view = operational_overview()
    escalation = {e["escalation_id"]: e["classification"] for e in view["escalations"].values()}
    expected_operational = {
        "nine_historical_REVOKED": all(w4root["operational"]["operational_dispositions"].get(g)
                                       == "REVOKED" for g in NINE),
        "2494015d_REVOKED": w4root["operational"]["operational_dispositions"].get(
            LIVE_PAIR["grant"]) == "REVOKED",
        "p12_w4_operational_active": w4root["operational"]["active_grants"],
        "9cb90fa0_ANSWERED": w4root["escalation_status_operational"].get(LIVE_PAIR["escalation"])
        == "ANSWERED",
        "historical_escalations_OPEN_HISTORICAL": {
            e: (w3root["escalation_status_operational"].get(e), escalation.get(e))
            for e in HISTORICAL_ESCALATIONS},
        "disposition_faults": {r: now["readers"][r]["operational"].get("disposition_faults")
                               for r in P11_ROOTS + P12_ROOTS},
    }
    identity = {"p11_w4": w4.ledger_identity(REPO / P11_ROOTS[1]),
                "p12_w4": w4.ledger_identity(REPO / P12_ROOTS[0])}
    result = {
        "verified_at": now["captured_at"], "head": now["head"],
        "baseline_head": before["head"],
        "A_certified_bytes": {
            "p12_tree_digest_before": before["p12_tree_digest"],
            "p12_tree_digest_after": now["p12_tree_digest"],
            "equal": before["p12_tree"] == now["p12_tree"],
            "manifest_mismatches": now["p12_manifest_mismatches"],
            "state_records_equal": before["state_record_sha256"] == now["state_record_sha256"],
            "integrity_faults": now["integrity_faults"],
            "git_status_certified": now["git_status_certified"]},
        "B_historical_reconstructable": {"p12_historical_reading_unchanged": historical_p12,
                                         "p12_w4_historical_active": len(
                                             w4root["historical"]["active_grants"]),
                                         "p12_historical_open": {
                                             r: now["readers"][r]["historical"]["open_escalations"]
                                             for r in P12_ROOTS}},
        "C_operational": expected_operational,
        "D_identity": dict(identity, distinct=identity["p11_w4"] != identity["p12_w4"]),
        "E_reader": {"current_grants": view["current_grants"],
                     "blocking_escalations": view["blocking_escalations"],
                     "escalations": escalation},
        "F_p11_and_agency_readers_unchanged": {"p11": p11, "agency": agency},
        "code_changed": {f: before["code_sha256"][f] != now["code_sha256"][f] for f in CODE},
        "counts_before": before["counts"], "counts_after": now["counts"],
    }
    result["all_ok"] = (
        result["A_certified_bytes"]["equal"] and result["A_certified_bytes"]["state_records_equal"]
        and not now["p12_manifest_mismatches"] and not now["integrity_faults"]
        and now["git_status_certified"] == "(clean)"
        and all(historical_p12.values())
        and expected_operational["nine_historical_REVOKED"]
        and expected_operational["2494015d_REVOKED"]
        and expected_operational["p12_w4_operational_active"] == []
        and expected_operational["9cb90fa0_ANSWERED"]
        and all(v == ("OPEN", "OPEN — HISTORICAL (its grant is not current)")
                for v in expected_operational["historical_escalations_OPEN_HISTORICAL"].values())
        and not any(expected_operational["disposition_faults"].values())
        and result["D_identity"]["distinct"]
        and all(all(v.values()) for v in p11.values())
        and all(all(v.values()) for v in agency.values())
        and view["blocking_escalations"] == [])
    VERIFICATION.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("A_certified_bytes", "C_operational", "D_identity",
                                              "F_p11_and_agency_readers_unchanged", "all_ok")},
                     indent=1, ensure_ascii=False))
    return 0 if result["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "baseline"))
