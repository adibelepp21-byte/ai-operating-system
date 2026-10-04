"""FR-2 (Runtime / Trace discovery) — integrity baseline (directive `§23`). READ-ONLY.

Captured after the directive was persisted and before discovery. Writes only its
JSON. Loads P12-W2 as data (the disclosed verifier pattern), so this tool never
enters the P12 consumer measurement it records.
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
import fr1_baseline as fb  # noqa: E402
import fr1_completion_baseline as cb  # noqa: E402
import s6_baseline as s6  # noqa: E402
import td_state_authority_baseline as td  # noqa: E402

OUT = Path(__file__).parent / "FR2-BASELINE-2026-10-04.json"
RUNTIME_TRACE = ("native_core/core/runtime", "native_core/core/trace", "native_core/core/agent",
                 "native_core/core/workflow", "native_core/core/memory")
RUNTIME_TRACE_TOOLS = ("tools/w4_execution.py", "tools/p12_trace_registry.py",
                       "tools/p12_runtime_observation.py", "tools/p12_execution_provenance.py",
                       "tools/p12_execution_chain_reader.py", "consumers/observation.py",
                       "consumers/engineering_intelligence_agent.py")
STORES = ("docs/architecture/p12/trace-stores", "docs/architecture/p12/execution-provenance",
          "docs/operations/runtime-observations", "docs/operations/p13/trace")
#: Pre-existing at every regression since MR-S5-1 (Register §152 … §160).
KNOWN_FAILURES = {"test_e11_measurement_currency": 4, "test_p12_governance_evidence_verification": 1}


def surfaces():
    s = td.surfaces()
    for w in RUNTIME_TRACE:
        s[f"runtime_trace_code:{w}"] = s6.digest(s6.files(w))
    s["runtime_trace_code:tools+consumers"] = s6.digest(REPO / f for f in RUNTIME_TRACE_TOOLS)
    for w in STORES:
        s[f"store:{w}"] = s6.digest(s6.files(w))
    return s


if __name__ == "__main__":
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    data = {"captured_at": datetime.now(timezone.utc).isoformat(), "head": head,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "surfaces": surfaces(), "register": s6.register_state(),
            "populations": fb.populations(), "verdicts": fb.verdicts(),
            "readings": fb.readings(), "consumer_measurement": cb.consumer_measurement(),
            "known_preexisting_failures": KNOWN_FAILURES}
    OUT.write_text(json.dumps(data, indent=1, default=str) + "\n", encoding="utf-8")
    d = json.loads(OUT.read_text())
    print(d["head"], len(d["surfaces"]), d["register"]["bytes"],
          len(d["consumer_measurement"]["consumers"]))
