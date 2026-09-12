"""Entry point — P12-W4 durable Trace evidence.

Here rather than in `tools/` for the reason the other root proofs record: wiring
a real performer needs `consumers/`, and `tools/` may not import that region.
Both assertions are AST-based, so a guarded import would violate them exactly as
a top-level one does.

**What this proves, and what it deliberately does not.**

The canonical `P12-W4` chain terminates in `EVIDENCE`. Before this proof, the
Trace boundary was fully built and conformance-tested, and **no execution had
ever fed it**: `TraceWriter` is an optional argument defaulted to `None` in every
resident path, `LocalAppendOnlyStorage` was constructed nowhere outside its own
definition, and zero durable trace partitions existed on disk.

This runs the **same real verification** the cross-Department proof runs —
`EngineeringIntelligenceAgent.verify` over `tools/w4_delegation.py` against the
`FD-P11-001 §13` conformance criteria — and supplies a `TraceWriter` backed by
`LocalAppendOnlyStorage`. The work is not written for this proof, and the record
is produced **by** the execution rather than **about** it.

It does not claim that runtime state is now observable. *"What is running"*
remains `UNKNOWN`: a Trace record says what **ran**, in the past tense, and
reading one back is not observation of a live process. Conflating the two would
answer `F-4` with `F-3`'s evidence.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from native_core.core.infrastructure import LocalAppendOnlyStorage  # noqa: E402
from native_core.core.trace import TraceWriter  # noqa: E402
from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from consumers.observation import TracedAction  # noqa: E402
from tools.p12_trace_registry import STORE_ROOT, discover, what_has_failed  # noqa: E402
from tools.w4_delegation import REQUIRED_ELEMENTS  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent
SUBJECT = REPO_ROOT / "tools" / "w4_delegation.py"
STORE_NAME = "w4-conformance-verification"
INSTANCE = "engineering-intelligence-instance-001"
RUNTIME = "p12-w4-durability-proof"


def _store() -> LocalAppendOnlyStorage:
    path = STORE_ROOT / STORE_NAME
    storage = LocalAppendOnlyStorage(path)
    storage.provision()
    return storage


def run() -> dict:
    """Execute real work through a real writer over durable storage."""
    storage = _store()
    writer = TraceWriter(storage)
    agent = EngineeringIntelligenceAgent(trace_writer=writer)

    lines = tuple(SUBJECT.read_text(encoding="utf-8").split("\n"))
    criteria = tuple(
        ConformanceCriterion(name=name, required_text=name)
        for name in REQUIRED_ELEMENTS
    )

    with TracedAction(
        writer,
        agent_instance=INSTANCE,
        runtime=RUNTIME,
        agent_definition_version="1.1",
    ) as action:
        results = agent.verify(Artifact(name=SUBJECT.name, lines=lines), criteria)
        satisfied = tuple(r.criterion_name for r in results if r.satisfied)
        unsatisfied = tuple(r.criterion_name for r in results if not r.satisfied)
        action.used_skill("artifact-conformance-verification")
        action.used_tool("tools/w4_delegation.py")
        action.produced({
            "criteria": len(criteria),
            "satisfied": len(satisfied),
            "unsatisfied": list(unsatisfied),
        })
        if unsatisfied:
            # The Agent classifies its own outcome; `§12` makes an unsatisfied
            # conformance run an observable failure rather than a silent pass.
            action.failed(f"{len(unsatisfied)} criteria unsatisfied")

    return {
        "criteria": len(criteria),
        "satisfied": len(satisfied),
        "unsatisfied": unsatisfied,
    }


def main() -> int:
    outcome = run()
    print(f"verified {outcome['satisfied']}/{outcome['criteria']} criteria")
    stores = discover()
    print(f"durable stores discovered: {len(stores)}")
    for store in stores:
        print(f"  {store.name}: {len(store.records())} record(s)")
    print(f"failures: {len(what_has_failed())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
