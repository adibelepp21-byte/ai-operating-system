"""The Final Platform Organization Closure Gate (`FD-PO-004` §12–§14).

**Read-only.** It consumes the decisions actually registered under `FD-PO-004`
(its `§10`: *"must not infer any decision not explicitly recorded"*). From
them, the Platform Organization gate and the construction verifier, it
establishes independently:

- `§12.1` construction status;
- `§12.2` evidence;
- `§12.3` epistemic integrity;
- `§12.4` authority integrity;
- `§12.5` cross-PD coherence;
- `§12.6` residual integrity;
- `§12.7` protected-root integrity;
- `§14` the P13 and P14 controls.

It returns exactly one primary state (`§13`), with the exact blockers when
not closed. It certifies, closes, freezes and activates nothing: a report
carries `certifies`, `grants_authority` and `decides` as False.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from tools import certified_evidence_integrity as integrity
from tools import platform_division_construction as pc
from tools import platform_organization_gate as po

REPO_ROOT = po.REPO_ROOT
DECISION = "FD-PO-004"
CLOSED = "PLATFORM ORGANIZATION CLOSED"
NOT_CLOSED = "PLATFORM ORGANIZATION NOT CLOSED"

#: `FD-PO-004 §2`: the classification counts the Founder certified. Canonical
#: state must retain them (`§9`).
CERTIFIED_COUNTS = {pc.SOURCE_DERIVED: 29, pc.INHERITED: 6, pc.ADAPTATION: 14,
                    pc.RECONSTRUCTION: 11, pc.UNKNOWN: 7, pc.RESERVED: 23}

BLOCKER = "BLOCKER"
ACCEPTED = "ACCEPTED RESIDUAL"
CLASSIFIED = "CLASSIFIED RESIDUAL"

#: Every open gate item and how closure treats it, with the basis. An open item
#: that is not listed fails `§12.6`: a new item cannot pass unreviewed.
#: - ACCEPTED: `FD-PO-004 §8` preserves its classification.
#: - CLASSIFIED: outside FD-PO-004, classified by its own source as not
#:   bearing on construction or canonical status.
#: - BLOCKER: stays open until the action named in its basis is completed.
CLOSURE_CLASSIFICATION: Dict[str, tuple] = {
    "ESC-C7-01": (BLOCKER, "D2", "FD-PO-004 D2 selected supply of Volumes 3 and 4 (D2-A); "
                  "until they are received and verified, D2 is not applied"),
    "FN-1": (BLOCKER, "D2", "the PD-01 / PD-03 governance-authority boundary is assessable only "
             "once Volume 3 is resident (D2)"),
    "G-10": (ACCEPTED, "ARCHITECT-RESERVED", "FD-PO-004 §8: G-10 not decided; classification preserved"),
    "G-02": (ACCEPTED, "FOUNDER / ARCHITECT-RESERVED", "FD-PO-004 §8: G-02 not decided"),
    "C6-A1": (ACCEPTED, "ARCHITECT-RESERVED", "FD-PO-004 §8: Architectural Part Structure not decided"),
    "ADP-P10-001": (ACCEPTED, "ARCHITECT-RESERVED", "FD-PO-004 §8: ADR-0029 not decided"),
    "P7-I99": (CLASSIFIED, "EVIDENCE", "RESULT B is freeze-readiness evidence for a volume already "
               "FROZEN (GDR-0017); rooted in G-10 (§8) and FN-1 (D2); a re-run needs a new invocation"),
    "RG-1": (CLASSIFIED, "FOUNDER-RESERVED · ACTIVATION", "PD-01 activation (ACT-CC-F03-014 §3); "
             "activation is outside construction and canonical status"),
    "FDP-P10-003": (CLASSIFIED, "FOUNDER-RESERVED", "non-blocking by its source (P12 policy D3 "
                    "CONDITIONAL-BLOCKING); its target PD-03 awaits D2"),
    "G-06": (CLASSIFIED, "SOURCE GAP", "non-blocking by the certified SYSTEMIC-GAP-MAP"),
    "G-07": (CLASSIFIED, "SOURCE GAP", "non-blocking by the certified SYSTEMIC-GAP-MAP"),
}

#: `§12.5`: the gate's coherence reasons that are accepted residuals, not
#: collisions, contradictions or bypasses.
_ACCEPTED_COHERENCE = (
    (r"declared edges have no defined interface", "ADP-P10-001"),
    (r"^G-02 open", "G-02"),
    (r"^ADP-P10-001 open", "ADP-P10-001"),
)
_ISOLATION = re.compile(r"divisions in no declared edge: (.+)$")


def selections(root: Path = REPO_ROOT) -> Dict[str, Optional[str]]:
    """The D1 … D4 options recorded in the registered decision, and nothing else."""
    register = po._read(root, po.REGISTER) or ""
    entry = po._entry(register, DECISION)
    out = {f"D{n}": None for n in range(1, 5)}
    if entry is None or not po._decided_by(entry, po.FOUNDER):
        return out
    row = re.search(r"^\| \*\*Decision\*\* \| (.+) \|\s*$", entry["block"], re.M)
    for match in re.finditer(r"\b(D[1-4])-([ABC])\b", row.group(1) if row else ""):
        out[match.group(1)] = f"{match.group(1)}-{match.group(2)}"
    return out


def _criterion(name: str, passes: bool, evidence: List[str], blockers: List[str]) -> dict:
    return {"criterion": name, "passes": passes, "evidence": evidence, "blockers": blockers}


def evaluate(root: Path = REPO_ROOT) -> dict:
    root = Path(root)
    chosen = selections(root)
    gate = po.evaluate(root)
    construction = pc.verify(root)
    items = {i["id"]: i for i in gate["open_items"]}
    open_ids = [i for i, v in items.items() if v["status"] == "OPEN"]
    criteria = []

    # §12.1 Construction
    blockers, evidence = [], []
    lifecycle = po.lifecycle_decisions(root)
    vi = gate["volume_integrity"]
    if not (lifecycle.get("PD-01", {}).get("frozen") and vi.get("PD-01", {}).get("holds")):
        blockers.append("PD-01 is not frozen with verifying bodies")
    if not all(lifecycle.get("PD-02", {}).get(k) for k in ("frozen", "active")) \
            or not vi.get("PD-02", {}).get("holds"):
        blockers.append("PD-02 is not frozen and active with verifying bodies")
    evidence.append("PD-01 FROZEN; PD-02 FROZEN · ACTIVE; bodies verify")
    resident = po.resident_corpora(root)
    if chosen["D2"] == "D2-A":
        missing = [c for c in ("PD-03", "PD-04") if c not in resident]
        if missing or items.get("ESC-C7-01", {}).get("status") == "OPEN":
            blockers.append(f"D2-A (supply) not yet applied: {', '.join(missing) or 'residency'} "
                            "not received and verified")
    elif chosen["D2"] == "D2-B":
        if items.get("ESC-C7-01", {}).get("status") == "OPEN":
            blockers.append("D2-B recorded but ESC-C7-01 not closed by it")
    else:
        blockers.append("D2 not recorded")
    expected = pc.CANONICAL_STATE if chosen["D1"] == "D1-A" else "CONSTRUCTED — VERIFIED"
    if chosen["D1"] not in ("D1-A", "D1-B"):
        blockers.append(f"D1 is {chosen['D1'] or 'not recorded'}: no construction status to establish")
    wrong = {c: s for c, s in construction["state"].items() if s != expected}
    if wrong:
        blockers.append(f"PD-05 … PD-10 not {expected}: {wrong}")
    evidence.append(f"PD-05 … PD-10: {sorted(set(construction['state'].values()))}")
    criteria.append(_criterion("§12.1 Construction", not blockers, evidence, blockers))

    # §12.2 Evidence
    g13 = next(g for g in gate["gate"] if g["id"] == "G13")
    ok = construction["passes"] and g13["status"] == po.PASS
    criteria.append(_criterion("§12.2 Evidence", ok,
                               ["every quotation in the construction volumes found in its source",
                                f"G13 {g13['status']}"],
                               [] if ok else construction["errors"][:5] + [f"G13 {g13['status']}"]))

    # §12.3 Epistemic integrity
    counts = {c: 0 for c in pc.CLASSES}
    for volume in construction["volumes"].values():
        for cls, n in volume.get("classes", {}).items():
            counts[cls] = counts.get(cls, 0) + n
    blockers = []
    if counts != CERTIFIED_COUNTS:
        blockers.append(f"classification counts {counts} ≠ certified {CERTIFIED_COUNTS}")
    if construction["canonical"] and chosen["D1"] != "D1-A":
        blockers.append("canonical state without D1-A")
    blockers += [e for e in construction["errors"]
                 if any(k in e for k in ("class", "not source", "certif", "canonical"))]
    criteria.append(_criterion("§12.3 Epistemic integrity", not blockers,
                               [f"classes {counts}", "no UNKNOWN → FACT, REFERENCE → SOURCE, "
                                "PROPOSAL → CANON (verifier)"], blockers))

    # §12.4 Authority integrity
    blockers = []
    bound = {"FDP-P10-001": "D3", "FDP-P10-002": "D4"}
    for item, d in bound.items():
        closed = items.get(item, {}).get("status", "").startswith("CLOSED")
        if closed != (chosen[d] == f"{d}-A"):
            blockers.append(f"{item} state does not follow {d} = {chosen[d]}")
    if any("forbidden assertion" in e or "Binding" in e for e in construction["errors"]):
        blockers.append("a binding or authority assertion fails the verifier")
    if not gate["governance"]["holds"]:
        blockers.append(f"governance invariants fail: {gate['governance']['failing']}")
    criteria.append(_criterion("§12.4 Authority integrity", not blockers,
                               ["bindings exactly those decided (D3, D4); FDP-P10-003 open and "
                                "not asserted", "governance invariants hold"], blockers))

    # §12.5 Cross-PD coherence
    blockers, evidence = [], []
    if gate["ownership"]["conflicts"]:
        blockers.append(f"ownership conflicts: {gate['ownership']['conflicts']}")
    if not construction["reconciliation"]["passes"]:
        blockers.append("construction reconciliation fails")
    for reason in gate["coherence"]["reasons"]:
        accepted = next((r for pattern, r in _ACCEPTED_COHERENCE if re.search(pattern, reason)), None)
        isolated = _ISOLATION.search(reason)
        if accepted and items.get(accepted, {}).get("status") == "OPEN" \
                and CLOSURE_CLASSIFICATION.get(accepted, (None,))[0] == ACCEPTED:
            evidence.append(f"accepted residual {accepted}: {reason}")
        elif isolated:
            for cpid in [c.strip() for c in isolated.group(1).split(",")]:
                answer = _relationships_sourced(root, cpid, construction)
                (evidence if answer else blockers).append(
                    f"{cpid} in no certified registry edge; " + (answer or "no sourced relationship"))
        else:
            blockers.append(f"coherence: {reason}")
    criteria.append(_criterion("§12.5 Cross-PD coherence", not blockers, evidence, blockers))

    # §12.6 Residual integrity
    blockers, evidence = [], []
    for identifier in open_ids:
        if identifier not in CLOSURE_CLASSIFICATION:
            blockers.append(f"{identifier} open and not classified for closure")
        elif not items[identifier]["recorded"]:
            blockers.append(f"{identifier} no longer recorded in its source")
        else:
            kind, cls, _ = CLOSURE_CLASSIFICATION.get(identifier, (BLOCKER, "UNCLASSIFIED", ""))
            evidence.append(f"{identifier}: {kind} · {cls}")
    stale = [i for i in CLOSURE_CLASSIFICATION if i not in open_ids]
    if stale:
        evidence.append(f"classified but no longer open: {stale}")
    reservations = pc.reservations(root)
    lost = [r for r, v in reservations.items() if not v["recorded"]]
    if lost:
        blockers.append(f"reservations no longer recorded: {lost}")
    criteria.append(_criterion("§12.6 Residual integrity", not blockers, evidence, blockers))

    # §12.7 Protected-root integrity
    report = integrity.verify(root)
    phases_hold = all(getattr(p, "holds", False) for p in report.phases.values())
    ok = not report.faults and phases_hold and vi.get("PD-01", {}).get("holds") \
        and vi.get("PD-02", {}).get("holds")
    criteria.append(_criterion("§12.7 Protected-root integrity", bool(ok),
                               [f"certified phases {sorted(report.phases)} hold", "PD-01, PD-02 verify"],
                               [] if ok else [f"faults {list(report.faults)[:3]}"]))

    # §14 P13 / P14
    p14 = [p.name for p in (root / pc.CONSTRUCTION_ROOT).rglob("*.md")
           if re.search(r"\bP14\b|Phase 14", p.read_text(encoding="utf-8"))]
    ok = gate["governance"]["holds"] and not p14
    criteria.append(_criterion("§14 P13 closed · no P14", ok, ["P13 closure holds"],
                               [] if ok else [f"P14 references: {p14}"]))

    blockers = [f"{c['criterion']}: {b}" for c in criteria for b in c["blockers"]]
    open_blockers = [i for i in open_ids if CLOSURE_CLASSIFICATION.get(i, (BLOCKER,))[0] == BLOCKER]
    state = CLOSED if not blockers and not open_blockers else NOT_CLOSED
    return {
        "decision": DECISION,
        "selections": chosen,
        "state": state,
        "criteria": criteria,
        "blockers": blockers,
        "open_blocking_items": open_blockers,
        "residuals": {i: CLOSURE_CLASSIFICATION[i] for i in open_ids if i in CLOSURE_CLASSIFICATION},
        "certifies": False,
        "grants_authority": False,
        "decides": False,
    }


def _relationships_sourced(root: Path, cpid: str, construction: dict) -> Optional[str]:
    """For a division the certified registry leaves without an edge: a sourced
    relationship in its canonical baseline, or its frozen corpus's own
    cross-platform section."""
    if cpid in pc.VOLUMES:
        text = pc._read(root, pc.VOLUMES[cpid]) or ""
        integration = [s for s in pc.sections(text) if s["dimension"] == "Integration"]
        if integration and integration[0]["class"] == pc.SOURCE_DERIVED:
            return f"its baseline's Integration section ({integration[0]['id']}) is SOURCE-DERIVED"
        return None
    if cpid == "PD-01" and (root / po.VOLUME_1 / "C8.md").exists():
        return "its frozen corpus defines cross-platform governance (volume-1 C8)"
    return None


def main() -> int:
    report = evaluate()
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    return 0 if report["state"] == CLOSED else 1


if __name__ == "__main__":
    raise SystemExit(main())
