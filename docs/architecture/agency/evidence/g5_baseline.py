"""FR-2 G5 (FD-FR2-002) — baseline, captured before any code changed. READ-ONLY.

Records the FR-2 construction baseline's surfaces and certified readers, the
P13 `operational_state` facts as they stand, and the FR-2 live chain, so the
verification can show what G5 added and that nothing certified moved. Loads
P12-W2, P13 and the root binding by name (the disclosed verifier pattern), so
this tool enters no consumer or reachability measurement. Writes only its JSON.
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
import fr1_completion_baseline as cb  # noqa: E402
import fr2_baseline as fr2  # noqa: E402
import fr2c_baseline as fr2c  # noqa: E402
import s6_baseline as s6  # noqa: E402

OUT = Path(__file__).parent / "G5-BASELINE-2026-10-04.json"


def p13_operational_state():
    state = importlib.import_module("tools.p13.state")
    paths = importlib.import_module("tools.p13.paths")
    source = next(s for s in state.SOURCES if s.name == "operational_state")
    observed = state.StateUnderstanding(paths.LIVE, sources=(source,)).observe()
    return fr2c.normal({f.key: [f.status, f.value, f.source] for f in observed.facts})


if __name__ == "__main__":
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    chain = importlib.import_module("tools.p12_execution_chain_reader")
    data = {"captured_at": datetime.now(timezone.utc).isoformat(), "head": head,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "surfaces": fr2.surfaces(), "register": s6.register_state(),
            "populations": fb.populations(), "verdicts": fb.verdicts(),
            "consumer_measurement": cb.consumer_measurement(),
            "certified_readers": fr2c.certified_readers(),
            "p13_operational_state": p13_operational_state(),
            "live_chain": fr2c.normal({v.execution_id: [v.status, v.origin,
                                                       [e.status for e in v.edges]]
                                      for v in chain.verify_live()}),
            "operational_overview_sha256": fb.digest(
                importlib.import_module("tools.w4_continuity").operational_overview()),
            "known_preexisting_failures": {**fr2.KNOWN_FAILURES,
                                           "fullstack NC-04, NC-05, NC-19": 3}}
    OUT.write_text(json.dumps(data, indent=1, default=str) + "\n", encoding="utf-8")
    d = json.loads(OUT.read_text())
    print(d["head"], len(d["surfaces"]), sorted(d["p13_operational_state"]),
          d["live_chain"], d["certified_readers"]["p12_w2"]["execution.provenance"])
