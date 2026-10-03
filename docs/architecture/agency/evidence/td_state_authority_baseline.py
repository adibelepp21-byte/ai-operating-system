"""Targeted Discovery (state authority / P13 boundary) — integrity baseline (`§19`).

READ-ONLY: hashes, writes only its own JSON. Captured before discovery;
``td_state_authority_discovery.py`` recaptures the same surfaces afterwards.
Reuses the S-6 surfaces and adds the ones this gate names: the P13 source,
the P12 state code, the state readers under reconciliation, and the Register.
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).parent))

import tools  # noqa: E402,F401  -- installs the certified-write barrier
import s6_baseline as s6  # noqa: E402

OUT = Path(__file__).parent / "TD-STATE-AUTHORITY-BASELINE-2026-10-04.json"
TD_ACT = "docs/governance/acts/DIR-AIOS-AGENCY-TD-STATE-AUTHORITY-P13-RECONCILIATION.md"
READERS = ("tools/p12_operational_state.py", "tools/p12_self_model.py",
           "tools/p12_provenance_verification.py", "tools/p12_failure_verification.py",
           "tools/delegation_reconciliation.py", "tools/delegation_catalog.py",
           "tools/w4_continuity.py", "tools/w4_delegation.py", "tools/escalation_register.py",
           "tools/planning_continuity.py")


def surfaces():
    s = s6.surfaces()
    s.pop("governance:docs/governance (except Register and S-6 act)")
    s["governance:docs/governance (except Register and the S-6 / TD acts)"] = s6.digest(
        p for p in s6.files("docs/governance")
        if str(p.relative_to(REPO)) not in (s6.REGISTER, s6.S6_ACT, TD_ACT))
    s["p13:tools/p13"] = s6.digest(s6.files("tools/p13"))
    s["p13:envelopes"] = s6.digest(s6.files("docs/governance/p13-envelopes"))
    s["state_readers"] = s6.digest(REPO / r for r in READERS)
    s["p12_state:tools/p12_*.py"] = s6.digest(sorted((REPO / "tools").glob("p12_*.py")))
    return s


if __name__ == "__main__":
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    OUT.write_text(json.dumps({
        "captured_at": datetime.now(timezone.utc).isoformat(), "head": head,
        "script_sha256": s6.sha(__file__), "surfaces": surfaces(),
        "register": s6.register_state(),
        "td_act_sha256": s6.sha(REPO / TD_ACT)}, indent=1) + "\n", encoding="utf-8")
    d = json.loads(OUT.read_text())
    print(d["head"], len(d["surfaces"]), d["register"])
