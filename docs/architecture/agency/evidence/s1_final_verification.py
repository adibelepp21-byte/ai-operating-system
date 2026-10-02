"""S-1 final verification (Founder decisions Q-S1-A = A2, Q-S1-B = B1).

Read-only over every ledger: certified P11 roots, the live delegation ledger,
the live escalation-response ledger. Rebuilds state in this process from files
alone. Writes only its own JSON output beside this script.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from tools import certified_evidence_integrity as integrity  # noqa: E402
from tools.escalation_register import LIVE_RESPONSES, EscalationRegister  # noqa: E402
from tools.p12_certified_evidence_guard import is_protected  # noqa: E402
from tools.w4_continuity import continuation_conditions, operational_state, reconstruct  # noqa: E402
from tools.w4_delegation import LIVE_LEDGER  # noqa: E402

P11 = REPO / "docs/architecture/p11"
MANIFEST = REPO / "docs/governance/AIOS_P11_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"
OUT = Path(__file__).with_name("S1-FINAL-VERIFICATION-2026-10-02.json")
ROOTS = ("w1-operations", "w4-operations", "x-department-operations")
EXPECTED = {"4daebea9012d4cc7": "COMPLETED", "0f7ac0785bd8442b": "COMPLETED",
            "a437cdbbd29940af": "COMPLETED", "4313bd2246124a94": "REVOKED"}
ESC = "23f315ba9f504272"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


certified = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
p11_files = {k: v for k, v in certified.items() if k.startswith("docs/architecture/p11/")}
mismatch = [k for k, v in p11_files.items() if sha(REPO / k) != v]
git_p11 = subprocess.run(["git", "status", "--porcelain", "--", "docs/architecture/p11"],
                         cwd=REPO, capture_output=True, text=True).stdout.strip()

historical = {r: reconstruct(P11 / r) for r in ROOTS}
operational = {r: operational_state(P11 / r) for r in ROOTS}
response_path = LIVE_RESPONSES / "w4-operations" / f"{ESC}.response.json"
response = json.loads(response_path.read_text(encoding="utf-8"))

checks = {
    "1_certified_p11_bytes_unchanged": {
        "files_checked": len(p11_files), "mismatches": mismatch,
        "integrity_faults": [str(f) for f in integrity.verify().faults],
        "git_status_p11": git_p11 or "(clean)",
        "ok": not mismatch and not git_p11,
    },
    "2_response_outside_certified_boundary": {
        "path": str(response_path.relative_to(REPO)),
        "protected": is_protected(response_path),
        "beside_escalation_exists": (P11 / "w4-operations" / f"{ESC}.response.json").exists(),
        "responded_by": response["responded_by"], "basis": response["basis"],
        "bound_to_escalation_sha256": response["escalation_record_sha256"]
        == sha(P11 / "w4-operations" / f"{ESC}.escalation.json"),
    },
    "3_escalation_observably_closed": {
        "operational_status": EscalationRegister(P11 / "w4-operations", LIVE_RESPONSES).status(ESC),
        "operational_open": operational["w4-operations"]["open_escalations"],
        "operational_conditions": list(continuation_conditions(operational["w4-operations"])),
    },
    "4_dispositions": {r: operational[r]["operational_dispositions"] for r in ROOTS},
    "5_historical_vs_operational": {r: {
        "historical_active": operational[r]["historical_active_grants"],
        "operational_active": operational[r]["active_grants"],
        "disposition_faults": operational[r]["disposition_faults"]} for r in ROOTS},
    "6_default_reader_unchanged": {r: {
        "active_grants": historical[r]["active_grants"],
        "open_escalations": historical[r]["open_escalations"],
        "has_operational_keys": "operational_dispositions" in historical[r]} for r in ROOTS},
}
got = {g: d for r in ROOTS for g, d in operational[r]["operational_dispositions"].items()}
checks["2_response_outside_certified_boundary"]["ok"] = (
    not checks["2_response_outside_certified_boundary"]["protected"]
    and not checks["2_response_outside_certified_boundary"]["beside_escalation_exists"]
    and checks["2_response_outside_certified_boundary"]["bound_to_escalation_sha256"])
checks["3_escalation_observably_closed"]["ok"] = (
    checks["3_escalation_observably_closed"]["operational_status"] == "ANSWERED"
    and not checks["3_escalation_observably_closed"]["operational_open"])
checks["4_dispositions"]["ok"] = got == EXPECTED
checks["5_historical_vs_operational"]["ok"] = all(
    v["historical_active"] and not v["operational_active"] and not v["disposition_faults"]
    for v in checks["5_historical_vs_operational"].values() if isinstance(v, dict))
checks["6_default_reader_unchanged"]["ok"] = (
    historical["w4-operations"]["open_escalations"] == [ESC]
    and all(historical[r]["active_grants"] for r in ROOTS)
    and not any(v["has_operational_keys"] for v in checks["6_default_reader_unchanged"].values()
                if isinstance(v, dict)))

result = {"checked_at": datetime.now(timezone.utc).isoformat(),
          "script_sha256": sha(Path(__file__)),
          "live_ledgers": {"dispositions": str(LIVE_LEDGER.relative_to(REPO)),
                           "responses": str(LIVE_RESPONSES.relative_to(REPO))},
          "checks": checks,
          "all_ok": all(c["ok"] for c in checks.values())}
OUT.write_text(json.dumps(result, indent=1, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: v["ok"] for k, v in checks.items()}, indent=1), "\nall_ok", result["all_ok"])
