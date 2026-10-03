"""MR-S5-1 verification, in a fresh process, from files alone. READ-ONLY.

Reconstructs every decision in every operational root **without reading reason
text**, checks the three live paths (ACCEPT, REWORK, REJECT) against the run
log, checks legacy records still read as before and were not rewritten, runs
live negative controls (refused before any write; bytes hashed before and
after), and compares integrity with the pre-construction baseline
(`MR-S5-1-BASELINE-2026-10-03.json`).
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

import tools  # noqa: E402,F401  -- installs the certified-write barrier before anything runs

HERE = Path(__file__).parent
OUT = HERE / "MR-S5-1-VERIFICATION-2026-10-03.json"
BASELINE = json.loads((HERE / "MR-S5-1-BASELINE-2026-10-03.json").read_text(encoding="utf-8"))
ROOT = REPO / "docs/architecture/agency/operations/w4-s4-plan-outcome"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tree(w):
    return {str(p.relative_to(REPO)): sha(p) for p in sorted((REPO / w).rglob("*")) if p.is_file()}


def digest(w):
    t = tree(w)
    return {"files": len(t), "digest": hashlib.sha256(json.dumps(t, sort_keys=True).encode()).hexdigest()}


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


from tools import certified_evidence_integrity as integrity  # noqa: E402
from tools import planning_continuity  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.delegation_catalog import all_operation_roots  # noqa: E402
from tools.planning import PlanStep  # noqa: E402

run = json.loads((ROOT / "mr-s5-1-run.result.json").read_text(encoding="utf-8"))
surface = planning_continuity.restore(ROOT / "planning.state.json")
expected = {e["grant"]: e for e in run["log"] if "decision" in e}

# Every decision, everywhere, read without the reason field.
records, explicit, legacy = [], 0, 0
for root in all_operation_roots():
    valid, faults = w4.read_dispositions(root)
    for gid, item in sorted(valid.items()):
        free = {k: v for k, v in item.items() if k != "reason"}
        decision, provenance = w4._decision_of(free)
        explicit += provenance == "EXPLICIT"
        legacy += provenance != "EXPLICIT"
        records.append({"root": str(root.relative_to(REPO)), "grant": gid,
                        "disposition": free["disposition"], "decision": decision,
                        "provenance": provenance, "resulting_plan": free.get("resulting_plan"),
                        "rework_target": free.get("rework_target")})
    if faults:
        records.append({"root": str(root.relative_to(REPO)), "faults": list(faults)})

live = {r["grant"]: r for r in records if r.get("grant") in expected}
paths = {gid: {"recorded": (r["decision"], r["resulting_plan"], r["rework_target"]),
               "run_log": (expected[gid]["decision"], expected[gid]["resulting_plan"],
                           expected[gid]["rework_target"])}
         for gid, r in live.items()}
outcomes = {g: w4.plan_outcome(surface, g, ROOT) for g in surface._goals}  # noqa: SLF001
rework_links = [s["reworks"] for o in outcomes.values() for v in o["versions"]
                for s in v["steps"] if s.get("reworks")]

# Legacy: pre-MR-S5-1 ledger entries unchanged since the baseline commit.
legacy_ledger = sorted(p for p in (REPO / "docs/architecture/agency/operations/w4-dispositions")
                       .rglob("*.disposition.json")
                       if not git("ls-files", "--error-unmatch", str(p.relative_to(REPO))) == "")
legacy_unchanged = git("diff", "--name-only", BASELINE["head"], "--",
                       "docs/architecture/agency/operations/w4-dispositions",
                       "docs/architecture/agency/operations/escalation-responses") == ""

# Live negative controls (refused before anything is written).
p2 = run["log"][2]["grant"]           # REWORK path: the failed grant (already decided)
watched = [ROOT, w4.LIVE_LEDGER]
before = {str(w): tree(w.relative_to(REPO)) for w in watched}


def refused(call):
    try:
        call()
        return "NOT REFUSED"
    except Exception as exc:  # recorded, not hidden
        return f"refused: {type(exc).__name__}: {str(exc)[:90]}"


steps = (PlanStep("z", "z", requires_delegation=True),)
controls = {
    "agent_cannot_decide": refused(lambda: w4.review_result(
        ROOT, p2, surface=surface, decision=w4.ACCEPT,
        reviewer="engineering-intelligence-instance-001", reason="mine")),
    "accept_on_failed_result_refused": refused(lambda: w4.review_result(
        ROOT, p2, surface=surface, decision=w4.ACCEPT, reviewer=w4.AUTHORIZED_DELEGATOR,
        reason="x")),
    "reject_with_rework_target_refused": refused(lambda: w4.review_result(
        ROOT, p2, surface=surface, decision=w4.REJECT, reviewer=w4.AUTHORIZED_DELEGATOR,
        reason="x", rework_target="z")),
    "rework_without_target_refused": refused(lambda: w4.review_result(
        ROOT, p2, surface=surface, decision=w4.REWORK, reviewer=w4.AUTHORIZED_DELEGATOR,
        reason="x", rework_steps=steps)),
    "malformed_provenance_refused": refused(lambda: w4.record_disposition(
        ROOT, p2, disposition=w4.REVOKED, delegator=w4.AUTHORIZED_DELEGATOR, reason="x",
        authority=w4.DELEGATOR_REVIEW,
        provenance={"decision": w4.REJECT, "resulting_plan": "p",
                    "rework_target": {"plan": "p", "step": "z"}})),
}
after = {str(w): tree(w.relative_to(REPO)) for w in watched}
controls["nothing_written_by_controls"] = before == after

certified = {w: digest(w) for w in ("docs/architecture/p11", "docs/architecture/p12",
                                    "docs/architecture/p13",
                                    "docs/architecture/platform-organization", "docs/operations")}
acts_now = {str(p.relative_to(REPO)): sha(p)
            for p in sorted((REPO / "docs/governance/acts").glob("*.md")) if "MR-S5-1" not in p.name}
catalog_now = {str(p.relative_to(REPO)): sha(p)
               for p in sorted((REPO / "docs/architecture/organization").rglob("*")) if p.is_file()}
instances_changed = git("diff", "--name-only", BASELINE["head"], "--", "*.instance.json")
new_instances = [p for p in git("ls-files", "--others", "--exclude-standard").splitlines()
                 if p.endswith(".instance.json")]

result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "script_sha256": sha(__file__),
    "head": git("rev-parse", "HEAD"), "baseline_head": BASELINE["head"],
    "decisions_read_without_reason": records,
    "counts": {"explicit": explicit, "legacy": legacy},
    "live_paths": paths,
    "plan_outcomes": {g: {k: o[k] for k in ("current_plan", "completed", "open_steps",
                                           "decision_faults", "founder_acceptance")}
                      for g, o in outcomes.items()},
    "rework_links": rework_links,
    "legacy_ledger_unchanged_since_baseline": legacy_unchanged,
    "negative_controls": controls,
    "integrity": {
        "certified_unchanged": {w: certified[w] == BASELINE[w] for w in certified},
        "acts_unchanged": acts_now == {k: v for k, v in BASELINE["acts"].items()},
        "capability_catalog_unchanged": catalog_now == BASELINE["capability_catalog"],
        "instance_records_changed": instances_changed or "(none)",
        "instance_records_new": new_instances,
        "integrity_faults": [str(f) for f in integrity.verify().faults],
        "git_status_certified": git("status", "--porcelain", "--", "docs/architecture/p11",
                                    "docs/architecture/p12", "docs/architecture/p13",
                                    "docs/architecture/platform-organization") or "(clean)"},
}
result["all_ok"] = (
    all(v["recorded"] == v["run_log"] for v in paths.values()) and len(paths) == 5
    and {v["recorded"][0] for v in paths.values()} == {"ACCEPT", "REWORK", "REJECT"}
    and all(o["completed"] for g, o in outcomes.items() if g.startswith("founder-mr-s5-1"))
    and all(not o["decision_faults"] for o in outcomes.values())
    and len(rework_links) == 1 and not any("faults" in r for r in records)
    and legacy_unchanged
    and all(str(v).startswith("refused") for k, v in controls.items()
            if k != "nothing_written_by_controls") and controls["nothing_written_by_controls"]
    and all(result["integrity"]["certified_unchanged"].values())
    and result["integrity"]["acts_unchanged"] and result["integrity"]["capability_catalog_unchanged"]
    and result["integrity"]["instance_records_changed"] == "(none)"
    and not new_instances and not result["integrity"]["integrity_faults"]
    and result["integrity"]["git_status_certified"] == "(clean)")
OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
print(json.dumps({k: result[k] for k in ("counts", "live_paths", "plan_outcomes", "rework_links",
                                          "legacy_ledger_unchanged_since_baseline",
                                          "negative_controls", "integrity", "all_ok")},
                 indent=1, ensure_ascii=False, default=str))
