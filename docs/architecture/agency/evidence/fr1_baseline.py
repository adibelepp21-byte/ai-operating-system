"""FR-1 (FD-TD-001) — pre-construction baseline. READ-ONLY: writes only its JSON.

Captures what FR-1 must leave unchanged (certified digests, every certified
verifier population, the verifiers' verdicts) and what it is meant to change
(P12-W2's delegation / escalation readings, P13's observed facts), before any
code is touched. ``fr1_verification.py`` compares against it afterwards.
"""
import hashlib
import importlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).parent))

import tools  # noqa: E402,F401  -- installs the certified-write barrier
import td_state_authority_baseline as td  # noqa: E402

OUT = Path(__file__).parent / "FR1-BASELINE-2026-10-03.json"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()


def populations():
    """Every population a certified P11 / P12 verifier reads — FD-TD-001 §3 must-not 3."""
    from tools import delegation_catalog, delegation_reconciliation
    from tools import p12_failure_verification as fail
    from tools import p12_provenance_verification as prov
    return {
        "p12_delegation_roots": [str(r.relative_to(REPO)) for r in prov.DELEGATION_ROOTS],
        "p12_delegation_records": sorted(d["delegation_id"] for d in prov.delegation_records()),
        "p11_operation_roots": [str(r.relative_to(REPO)) for r in delegation_catalog.operation_roots()],
        "w3_projections": sorted((p.grant_id or "", p.role or "") for p in
                                 delegation_reconciliation.reconcile()["projections"]),
        "p12_escalation_join": fail.escalation_join(),
    }


def verdicts():
    w2 = importlib.import_module("tools.p12_operational_state")   # as data: see readings()
    from tools import p12_operational_state_verifier as w2v
    from tools import p12_state_verification as chain
    return {"w2_verifier": [(c.name, c.status) for c in w2v.verify()],
            "w2_summary": {k: v for k, v in w2.summary().items() if k != "observed_at"},
            "state_chain": {k: v for k, v in chain.summary().items()
                            if not str(k).endswith("_at")}}


def readings():
    # Read as data, by name (the disclosed pattern of `tools/p12_operational_state_verifier.py`):
    # an evidence tool measures the surface and is not one of its consumers, so it must
    # not enter the P12 consumer measurement (`p12_state_verification.consumers_of`).
    w2 = importlib.import_module("tools.p12_operational_state")
    from tools import w4_continuity
    from tools.p13.paths import LIVE
    from tools.p13.state import StateUnderstanding
    facts = StateUnderstanding(LIVE).observe().facts
    return {
        "w2": {e.state_id: {"status": e.status, "value": e.value} for e in w2.project()},
        "p13_fact_keys": sorted(f.key for f in facts),
        "p13_escalations_open": next(f.value for f in facts if f.key == "escalations.open"),
        "operational_overview_sha256": digest(w4_continuity.operational_overview()),
    }


if __name__ == "__main__":
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    pops = populations()
    OUT.write_text(json.dumps({
        "captured_at": datetime.now(timezone.utc).isoformat(), "head": head,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "surfaces": td.surfaces(), "populations": pops, "populations_sha256": digest(pops),
        "verdicts": verdicts(), "readings": readings()}, indent=1, default=str) + "\n",
        encoding="utf-8")
    d = json.loads(OUT.read_text())
    print(d["head"], d["populations_sha256"][:16], d["verdicts"]["w2_verifier"],
          d["readings"]["w2"]["delegation.granted"], len(d["readings"]["p13_fact_keys"]))
