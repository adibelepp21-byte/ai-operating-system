"""FR-1 completion (FD-FR1-001) — baseline before P13 is wired. READ-ONLY.

Extends the FR-1 baseline with the certified P12 consumer measurement, which
FD-FR1-001 authorizes to change in one way only: P13 appearing as an observed
consumer of P12-W2. Writes only its JSON.
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
import fr1_baseline as fb  # noqa: E402
import td_state_authority_baseline as td  # noqa: E402

OUT = Path(__file__).parent / "FR1-COMPLETION-BASELINE-2026-10-03.json"
SURFACE = "tools.p12_operational_state"


def consumer_measurement():
    """The certified measurement (AST) and its independent dynamic verifier."""
    from tools import p12_consumer_evidence_verifier as cv
    from tools import p12_state_verification as sv
    consumers, importers = sv.consumers_of(SURFACE), sv.importers_of(SURFACE)
    link = {r.link: [r.status, r.detail] for r in sv.verify()}
    return {"consumers": consumers, "importers": importers,
            "candidates": [list(c) for c in cv.CANDIDATES],
            "independent_verifier": cv.summary(consumers, importers),
            "state_chain_links": link}


if __name__ == "__main__":
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    data = {"captured_at": datetime.now(timezone.utc).isoformat(), "head": head,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "surfaces": td.surfaces(), "populations": fb.populations(),
            "verdicts": fb.verdicts(), "readings": fb.readings(),
            "consumer_measurement": consumer_measurement()}
    OUT.write_text(json.dumps(data, indent=1, default=str) + "\n", encoding="utf-8")
    d = json.loads(OUT.read_text())
    cm = d["consumer_measurement"]
    print(d["head"], len(cm["consumers"]), len(cm["importers"]), cm["independent_verifier"]["disagrees"],
          cm["state_chain_links"]["CONSUMER"])
