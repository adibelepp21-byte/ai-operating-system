"""P13 fresh verification before a Founder Closure Decision (`FDR-G2` `§6.3`).

`FD-G2-C6` sets the minimum closure evidence:

```text
CURRENT CLOSURE GATE  +  FRESH VERIFICATION  +  FOUNDER CLOSURE DECISION
```

This module is the second term. It runs after the closure gate
(`tools/p13_closure_gate.py`) and before the Founder decides. It checks, against
the current tree, every state `§6.3` names (V01 … V17 below).

It is a **state** verification. It is not a new E13-05 live proof:
*"FRESH VERIFICATION ≠ NEW E13-05 LIVE PROOF"* (`§6.3`). It executes nothing
state-changing and writes nothing. Each check is `PASS`, `FAIL` or
`UNDETERMINABLE`, and the whole holds only when every check passes.

**Closure statements are read carefully.** `FDR-G2` `§6.4` contains the line
*"P13 CLOSURE = GRANTED"*. It is the form the Founder's Closure Decision shall
use, and it grants nothing. V16 treats that one occurrence as a stated form:
the same instrument says *"FDR-G2 does not itself close P13."* The guard learned
the same lesson from negations: a reader fooled by a stated form is worse than
none.

**After `FDR-G3`.** V16 scans closure lines by its own parse. Each one it finds
in a Register-resolving instrument must be either that stated form or a closure
`tools.p12_phase_authorization.closures()` recognises as valid under `FDR-G3`
`§27`. Every closure the reader recognises must also appear in the scan. Any
other closure line fails. V13 reads the `§27` lifecycle.

`post_closure()` is the `FDR-G3` `§30` verification. It holds all 17 checks, and
also requires P13 CLOSED and the three `FDR-G2` dispositions evidenced. The
certified-write probe is external (it runs in disposable worktrees), and its
result is recorded beside this output.

Nothing here closes, certifies or authorizes anything.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Callable, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTS = "docs/governance/acts"
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
ROADMAP = "docs/program/AIOS_MASTER_ROADMAP_CONSOLIDATED_v1.0.md"
OPERATIONS_README = "docs/operations/README.md"

PASS = "PASS"
FAIL = "FAIL"
UNDETERMINABLE = "UNDETERMINABLE"

#: The certifying instruments of the certified set, as the guard reads them.
CERTIFYING = {
    10: "FD-P10-005-CERTIFICATION-OF-PHASE-10-DEPARTMENT-ECOSYSTEM.md",
    11: "FD-P11-002-P11-CERTIFICATION.md",
    12: "FD-P12-006-P12-CERTIFICATION-AND-LIVE-VERIFICATION.md",
    13: "FDR-7-P13-FOUNDER-CERTIFICATION-AND-FINAL-SYSTEM-ACCEPTANCE.md",
}
_CLOSURE_GRANTED = re.compile(r"^\s*P13 CLOSURE\s*=\s*GRANTED\s*$", re.MULTILINE)
#: The one instrument whose closure line is a stated form, and the line it
#: must also carry for that reading to hold.
STATED_FORM = {
    "FDR-G2-P13-CLOSURE-RESIDUAL-GOVERNANCE-AND-POST-CLOSURE-OPERATING-MODEL.md":
        "FDR-G2 does not itself close P13.",
}


def _commit(root: Path) -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                             capture_output=True, text=True, timeout=30)
        return out.stdout.strip() or "UNKNOWN"
    except (OSError, subprocess.SubprocessError):
        return "UNKNOWN"


def _check(identifier: str, name: str, test: Callable[[], Tuple[bool, List[str]]]) -> dict:
    try:
        passed, evidence = test()
        status = PASS if passed else FAIL
    except Exception as error:  # a check that cannot run is not a pass
        status, evidence = UNDETERMINABLE, [f"{type(error).__name__}: {error}"]
    return {"id": identifier, "check": name, "status": status, "evidence": evidence}


def verify(root: Path = REPO_ROOT) -> Dict[str, object]:
    from tools import certification_baseline as baseline
    from tools import certified_evidence_integrity as integrity
    from tools import certified_write_barrier as barrier
    from tools import p12_certified_evidence_guard as sentinel
    from tools import p12_phase_authorization as phases
    from tools import p13_closure_gate as gate
    from tools.p13 import authority
    from tools.p13.paths import Paths

    try:
        register_text = (root / REGISTER).read_text(encoding="utf-8")
    except OSError as error:
        return {"instrument": "FDR-G2 FD-G2-C6, §6.3", "commit": _commit(root),
                "holds": False, "checks": [], "counts": {UNDETERMINABLE: 17},
                "statement": f"UNDETERMINABLE: Decision Register unreadable: {error}"}
    acts, register = root / ACTS, root / REGISTER
    paths = Paths(root)

    def registered(name: str) -> str:
        return gate._registered_text(f"{ACTS}/{name}", root, register_text) or ""

    def dims() -> Dict[str, str]:
        return {k: v.get("state") for k, v in authority.authority_dimensions(paths).items()}

    def p13_state() -> dict:
        return {s["entity"]: s for s in phases.current_states(root)}["P13"]

    def v01():
        state = p13_state()
        return (state["authorized"] is True and "FDR-6" in state["authority"],
                [f"authorized: {state['authorized']}", state["authority"]])

    def v02():
        text = registered(Path(gate.FDR5).name)
        return ("P13 Exit Contract = SATISFIED" in text,
                [f"{gate.FDR5}: P13 Exit Contract = SATISFIED"])

    def v03():
        found = {n for p, n in sentinel.certification_provenance(acts) if p == 13}
        certified = 13 in sentinel.certified_phases(acts, register)
        return (certified and found == {CERTIFYING[13]},
                [f"certified: {certified}", f"provenance: {sorted(found)}"])

    def v04():
        g1 = registered(Path(gate.FDRG1).name)
        exhausted = gate._EXHAUSTION_ROW.search(register_text) is not None
        return ("P13 CONSTRUCTION FRONTIER\nNONE" in g1 and exhausted,
                ["FDR-G1 §39: P13 CONSTRUCTION FRONTIER NONE",
                 f"A17 exhaustion registered: {exhausted}"])

    def v05():
        record = dims().get("construction_authorization", "")
        g2 = registered(Path(gate.FDRG2).name)
        accepted = "P13-018 D-1\n=\nEXHAUSTED" in g2
        exhausted = gate._EXHAUSTION_ROW.search(register_text) is not None
        return (record.startswith("AUTHORIZED") and exhausted and accepted,
                [f"record preserved: {record}", f"A17 exhaustion: {exhausted}",
                 f"FDR-G2 §7.5 accepts it: {accepted}"])

    def v06():
        state = dims().get("state_changing_authority")
        return state == "NONE", [f"state_changing_authority: {state}"]

    def v07():
        active = [e.id for e in authority.load_envelopes(paths)[0]]
        retired = {r["envelope"]: r["retired_by"] for r in authority.retired_envelopes(paths)}
        return (retired.get("P13-ENV-02") == "FDR-4" and "P13-ENV-02" not in active,
                [f"active: {active}", f"retired: {retired}"])

    def v08():
        envelopes = authority.load_envelopes(paths)[0]
        s_ops = [t for e in envelopes for t in e.action_types if t.startswith("s_ops")]
        envelope = dims().get("operational_envelope")
        return (not s_ops and envelope == "EVIDENCE-ONLY",
                [f"active S-OPS action types: {s_ops}", f"operational_envelope: {envelope}"])

    def v09():
        report = integrity.verify(root)
        chains = {p: [(v["version"], v["state"]) for v in c]
                  for p, c in report.versions.items()}
        return report.holds, [f"holds: {report.holds}", f"faults: {list(report.faults)}",
                              f"versions: {chains}"]

    def v10():
        guarded = {str(p.resolve()) for p in sentinel.protected_roots(root, acts, register)}
        determined, _, _ = barrier.determine(root)
        determined = {str(Path(r).resolve()) for r in determined}
        evidence = [f"guard roots covered by the barrier: {guarded <= determined}"]
        passed = guarded <= determined and len(guarded) == len(CERTIFYING)
        if root.resolve() == REPO_ROOT.resolve():
            refused = all(barrier.refuses(Path(r) / "fresh-verification-probe.md")
                          for r in guarded)
            evidence.append(f"barrier installed and refusing each root: {refused}")
            passed = passed and refused
        return passed, evidence

    def v11():
        from tools import foundational_question_reconciliation as frontier
        checked = frontier.verify(root / gate.MATRIX, root)
        drift = gate.residual_drift(root)
        return (checked["holds"] and not drift,
                [f"P13-015 matrix holds: {checked['holds']}",
                 f"drift from FD-G2-C5: {drift or 'none'}"])

    def v12():
        current = dims()
        expected = {"phase_authorization": "AUTHORIZED", "operational_envelope":
                    "EVIDENCE-ONLY", "state_changing_authority": "NONE",
                    "certification_authority": "CERTIFIED"}
        passed = all(current.get(k) == v for k, v in expected.items()) and \
            current.get("construction_authorization", "").startswith("AUTHORIZED")
        return passed, [f"{k}: {v}" for k, v in current.items()]

    def v13():
        states = {s["entity"]: s for s in phases.current_states(root)}
        folded = [k for k in states["P13"].get("dimensions", {}) if "CLOS" in k.upper()]
        state = phases.lifecycle("P13", root)
        return (set(states) == {"P11", "P12", "P13"} and not folded
                and state["authorized"] is True and state["exit_satisfied"]
                and state["certified"] and state["resolved"],
                [f"phase model: {sorted(states)}",
                 f"P13 dimensions: {states['P13'].get('dimensions')}",
                 f"lifecycle: authorized {state['authorized']}, exit "
                 f"{state['exit_satisfied']}, certified {state['certified']}, "
                 f"closed {state['closed']} ({state['closure_source']})"])

    def v14():
        roadmap = (root / ROADMAP).read_text(encoding="utf-8").splitlines()
        start = next(i for i, line in enumerate(roadmap) if line.startswith("| # | Name"))
        table = []
        for line in roadmap[start + 2:]:
            if not line.startswith("|"):
                break
            table.append(line)
        rows = sorted({int(m.group(1)) for line in table
                       for m in [re.match(r"^\|\s*(\d+)\s*\|", line)] if m})
        certified = sentinel.certified_phases(acts, register)
        authorized = set(phases.authorizations(root)["phases"])
        entities = {s["entity"] for s in phases.current_states(root)}
        numbers = {int(e[1:]) for e in authorized | entities} | set(certified)
        return (rows == list(range(14)) and max(numbers) <= 13,
                [f"roadmap phase rows: {rows[0]}–{rows[-1]}",
                 f"highest phase anywhere read: {max(numbers)}"])

    def v15():
        certified = sentinel.certified_phases(acts, register)
        provenance = {n for _, n in sentinel.certification_provenance(acts)}
        anomalies = sentinel.certification_anomalies(acts, register)
        base = baseline.baseline(root)
        return (set(certified) == set(CERTIFYING) and provenance == set(CERTIFYING.values())
                and not anomalies and base.get("holds") is True,
                [f"certified: {sorted(certified)}", f"anomalies: {list(anomalies)}",
                 f"baseline holds: {base.get('holds')}"])

    def v16():
        recognised = {Path(c["instrument"]).name
                      for c in (phases.closures(root).get("phases") or {}).values()}
        found, stated, valid = [], [], []
        for path in sorted(acts.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if not _CLOSURE_GRANTED.search(text):
                continue
            if sentinel._register_identity(path.stem, register_text) is None:
                continue
            if STATED_FORM.get(path.name, "\0") in text:
                stated.append(path.name)
            elif path.name in recognised:
                valid.append(path.name)
            else:
                found.append(path.name)
        report = gate.evaluate(root)
        return (not found and set(valid) == recognised and report["closes"] is False,
                [f"unrecognised closure grants in Register-resolving instruments: {found}",
                 f"valid Founder closure decisions: {valid}",
                 f"stated forms, not grants: {stated}",
                 f"closure gate closes: {report['closes']}"])

    def v17():
        from tools import p12_self_model as model
        answer = model.authority(root).value
        certified = set(answer["phase_authorization"].get("certification", {})
                        .get("phases", {}))
        tiers = answer.get("certification_baseline", {}).get("tiers")
        readme = (root / OPERATIONS_README).read_text(encoding="utf-8")
        checks = {
            "self-model reports P10–P13 certified": certified == {"P10", "P11", "P12", "P13"},
            "self-model reports the accepted baseline": tiers == baseline.baseline(root)
            .get("tiers"),
            "projection certification agrees with the guard":
                dims().get("certification_authority") == "CERTIFIED",
            "operations README states P13-ENV-02 retired": "spent and retired" in readme,
        }
        return all(checks.values()), [f"{k}: {v}" for k, v in checks.items()]

    checks = [
        ("V01", "P13 authorization state", v01),
        ("V02", "P13 exit state", v02),
        ("V03", "P13 certification state", v03),
        ("V04", "P13 construction frontier", v04),
        ("V05", "P13-018 disposition", v05),
        ("V06", "P13 state-changing authority", v06),
        ("V07", "P13-ENV-02 status", v07),
        ("V08", "S-OPS status", v08),
        ("V09", "certified-root integrity", v09),
        ("V10", "write-protection integrity", v10),
        ("V11", "residual-frontier classification", v11),
        ("V12", "current authority projection", v12),
        ("V13", "current phase state", v13),
        ("V14", "absence of Phase 14", v14),
        ("V15", "absence of unauthorized certification", v15),
        ("V16", "absence of unauthorized closure", v16),
        ("V17", "absence of contradictory current-state assertions", v17),
    ]
    results = [_check(identifier, name, test) for identifier, name, test in checks]
    return {
        "instrument": "FDR-G2 FD-G2-C6, §6.3",
        "commit": _commit(root),
        "holds": all(r["status"] == PASS for r in results),
        "checks": results,
        "counts": {s: sum(1 for r in results if r["status"] == s)
                   for s in (PASS, FAIL, UNDETERMINABLE)},
        "statement": ("State verification only. It is not an E13-05 live proof, "
                      "executes nothing state-changing, and closes nothing "
                      "(FDR-G2 §6.3, §6.4)."),
    }


def post_closure(root: Path = REPO_ROOT) -> Dict[str, object]:
    """The `FDR-G3` `§30` post-closure verification.

    All 17 checks of `verify()` must pass. On top of them, P13 must be CLOSED by
    a valid Founder decision, and the gate must still evidence `FD-G2-C5`,
    `-C6` and `-C8`. The certified-write probe is recorded beside this output.
    """
    from tools import p12_phase_authorization as phases
    from tools import p13_closure_gate as gate
    fresh = verify(root)
    by_id = {c["id"]: c["status"] for c in fresh["checks"]}
    state = phases.lifecycle("P13", root)
    criteria = {c["id"]: c["status"] for c in gate.evaluate(root)["criteria"]}

    def item(label: str, passed: bool, source: str) -> dict:
        return {"state": label, "status": PASS if passed else FAIL, "source": source}

    items = [
        item("P13 AUTHORIZATION TRUE", state["authorized"] is True, "lifecycle; V01"),
        item("P13 EXIT SATISFIED", state["exit_satisfied"], f"{state['exit_source']}; V02"),
        item("P13 CERTIFICATION TRUE", state["certified"],
             f"{state['certification_source']}; V03"),
        item("P13 CLOSURE CLOSED", state["closed"], f"{state['closure_source']}; V16"),
        item("P13 CONSTRUCTION FRONTIER NONE", by_id.get("V04") == PASS, "V04"),
        item("P13-018 D-1 EXHAUSTED", by_id.get("V05") == PASS, "V05"),
        item("P13-ENV-02 RETIRED", by_id.get("V07") == PASS, "V07"),
        item("S-OPS HISTORICAL ONLY", by_id.get("V08") == PASS, "V08"),
        item("STATE-CHANGING AUTHORITY NONE", by_id.get("V06") == PASS, "V06"),
        item("C5 RESIDUALS NON-BLOCKING", criteria.get("C5") == gate.EVIDENCED, "gate C5"),
        item("C6 EVIDENCE MODEL SATISFIED", criteria.get("C6") == gate.EVIDENCED
             and state["closed"], "gate C6; closure evidence"),
        item("C8 OPERATING MODEL GOVERNED OPERATION", criteria.get("C8") == gate.EVIDENCED,
             "gate C8"),
        item("CERTIFIED ROOT UNCHANGED", by_id.get("V09") == PASS, "V09"),
        item("PHASE 14 NOT ESTABLISHED", by_id.get("V14") == PASS, "V14"),
    ]
    return {
        "instrument": "FDR-G3 §30",
        "commit": fresh["commit"],
        "holds": fresh["holds"] and all(i["status"] == PASS for i in items),
        "items": items,
        "fresh_verification": fresh,
        "external": {"CERTIFIED WRITE PROBE 0": "recorded beside this output "
                     "(tools/certified_write_probe.py)"},
        "statement": "Verification only. It grants, closes and certifies nothing.",
    }


def main() -> int:
    import sys
    if "--post-closure" in sys.argv[1:]:
        result = post_closure()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["holds"] else 1
    result = verify()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["holds"] else 1


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
