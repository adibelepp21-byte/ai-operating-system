"""FR-2 construction (FD-FR2-001) — baseline, captured before any code changed. READ-ONLY.

Records every surface the FR-2 discovery baseline recorded, plus what the
certified readers this construction may extend answer **today**: the chain
reader's certified population and verdicts, the trace registry's certified
population, the manifests, the observations, and P12-W2's projections of them.
The verification compares against this to show that the certified populations
did not move. Loads P12-W2 as data (the disclosed verifier pattern), so this
tool never enters the P12 consumer measurement it records. Writes only its JSON.
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
import s6_baseline as s6  # noqa: E402

OUT = Path(__file__).parent / "FR2C-BASELINE-2026-10-04.json"


def normal(value):
    return json.loads(json.dumps(value, sort_keys=True, default=str))


def certified_readers():
    """What the readers FD-FR2-001 `§5` lets this construction extend answer now."""
    chain = importlib.import_module("tools.p12_execution_chain_reader")
    traces = importlib.import_module("tools.p12_trace_registry")
    provenance = importlib.import_module("tools.p12_execution_provenance")
    observation = importlib.import_module("tools.p12_runtime_observation")
    w2 = importlib.import_module("tools.p12_operational_state")
    entries = {e.state_id: e for e in w2.project()}
    return normal({
        "chain_summary": chain.summary(),
        "chain_verdicts": {v.execution_id: [v.status, [[e.source, e.target, e.status, e.detail]
                                                       for e in v.edges]]
                           for v in chain.verify_all()},
        "chain_roots": {k: str(getattr(chain, k).relative_to(REPO))
                        for k in ("MANIFESTS", "TRACE_STORES", "OBSERVATIONS")},
        "chain_delegation_dirs": [str(d.relative_to(REPO)) for d in chain.DELEGATION_DIRS],
        "trace_registry_certified": traces.what_has_run(traces.STORE_ROOT),
        "trace_registry_failures": len(traces.what_has_failed(traces.STORE_ROOT)),
        "manifests_certified": sorted(m["execution_id"] for m in provenance.manifests()),
        "observations": sorted([o.runtime_id, o.origin, o.state]
                               for o in observation.observations(observation.OBSERVATION_ROOT)),
        "p12_w2": {k: [entries[k].status, entries[k].value]
                   for k in ("execution.recorded", "execution.provenance", "runtime.observed")},
        "p12_w2_sources": [[s.state_id, s.read_path, s.owner, s.provider] for s in w2.SOURCES],
        "live_roots_present": {p: (REPO / p).exists() for p in (
            "docs/operations/trace-stores", "docs/operations/execution-provenance")},
    })


if __name__ == "__main__":
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    w4c = importlib.import_module("tools.w4_continuity")
    data = {"captured_at": datetime.now(timezone.utc).isoformat(), "head": head,
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "surfaces": fr2.surfaces(), "register": s6.register_state(),
            "populations": fb.populations(), "verdicts": fb.verdicts(),
            "readings": fb.readings(), "consumer_measurement": cb.consumer_measurement(),
            "certified_readers": certified_readers(),
            "operational_overview_sha256": fb.digest(w4c.operational_overview()),
            "known_preexisting_failures": fr2.KNOWN_FAILURES}
    OUT.write_text(json.dumps(data, indent=1, default=str) + "\n", encoding="utf-8")
    d = json.loads(OUT.read_text())
    r = d["certified_readers"]
    print(d["head"], len(d["surfaces"]), r["chain_summary"], r["trace_registry_certified"]["records"],
          len(r["observations"]), r["live_roots_present"])
