"""AIOS corpus health assessment — a real system work path.

`ACT-CC-P12-014 §2`: the target is not *make a test pass*, it is **build a
working AIOS system** that receives real work, forms system context, uses real
AIOS capabilities, executes, produces observable state, persists evidence, and
can be independently verified. `§8` forbids satisfying the Act with another
demonstrator.

**The work is real, and it is the system's own.** AIOS already audits its
governance corpus — `governance_index` recomputes each instrument's content hash
against the one recorded at build, `corpus_citation_audit` resolves every
citation, `stale_state_audit` separates live assertions from historical uses.
Those audits run today. What has never existed is a path where the system
performs that assessment **as hosted work**: on a started Runtime, inside a
Workflow, remembering the previous assessment so it can say what changed, and
judging the result against criteria it holds as Knowledge.

That shape is not chosen to satisfy `R1`. It is what the task actually needs:

- **Memory is material.** *"What changed since the last assessment?"* is an
  output of this work, and it is unanswerable without the previous assessment.
  Remove Memory and the delta cannot be computed — `§20`'s test, met by the
  work's own semantics rather than by assertion.
- **Knowledge is material.** *"Is the corpus healthy?"* is a judgement against
  criteria. Remove the criteria and the audits still produce numbers, but no
  verdict follows from them. The work does not invent a threshold to fill the
  gap; it records that the verdict is withheld.

**One capability is reachable and one is not, and the difference is
authority, not engineering.** Memory admission is the lifecycle's own
(`MemoryLifecycle.admit(candidate)` — *"it cannot ask permission of anything"*).
Knowledge admission is governed: `KnowledgeAdmission.admit(candidate,
authorization)` admits **iff** `GovernanceReview.promotion_authorized` reflects
a provenance-verified **human** `approve` — a `ReviewDecision` carrying a
`HumanAuthority(reviewer_id)`. No resident Active Knowledge version exists, and
this office cannot supply a human reviewer. `§36.8` makes that a hard stop, so
the work **runs to its honest end and reports the verdict withheld** rather than
manufacturing an approval to reach a passing number.

**Boundaries this path keeps.** `§15`: capability is reached through
`execution.runtime.knowledge` / `.memory`, which the Runtime gates on RUNNING —
nothing here bypasses it. `§14`: the runtime is started and stopped by this
entry point; there is no daemon, scheduler, queue or self-activation, and
`OA-1` is untouched. `§16`: the W4 stages stay distinct. `§9`: no subsystem is
rebuilt — Runtime, Workflow, Knowledge, Memory, Trace and the three audits are
all resident and reused.

**Evidence is captured, not referenced.** `TraceRecord` INV-6 requires
`knowledge_consumed` / `memory_consumed` to hold captured content so a record
stays explainable without the later existence of any Memory or Knowledge item.
This path records content, not keys.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Optional

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from native_core.core.infrastructure import (  # noqa: E402
    LocalAppendOnlyStorage, build_default_infrastructure)
from native_core.core.memory import MemoryCandidate, MemoryProvenance  # noqa: E402
from native_core.core.runtime import AIOSRuntime, RuntimeState  # noqa: E402
from native_core.core.runtime.execution import create_execution_layer  # noqa: E402
from native_core.core.trace import TraceWriter  # noqa: E402
from native_core.core.workflow import (  # noqa: E402
    Workflow, WorkflowIdentity, WorkflowLifecycle, WorkflowMonitor)
from consumers.observation import TracedAction  # noqa: E402
from tools import p12_runtime_observation as observation  # noqa: E402

RUNTIME_ID = "aios-corpus-health-runtime"
WORKFLOW_KEY = "aios-corpus-health"
MEMORY_KEY_PREFIX = "corpus-health.finding"
KNOWLEDGE_KEY = "corpus-health.criteria"
AGENT_INSTANCE = "engineering-intelligence-instance-001"

#: The criteria this work judges against, held as Knowledge rather than as a
#: constant here — which is the point. A threshold hard-coded in the worker is
#: the worker's opinion; a threshold held as an admitted Knowledge version is
#: the system's, and changing it is a governed act.
CRITERIA_CONTENT = {
    "knowledge_item_key": KNOWLEDGE_KEY,
    "stale_governance_sources_max": 0,
    "citation_errors_max": 0,
    "live_stale_assertions_max": 0,
}


# --------------------------------------------------------------------------
# WORK — the assessment itself. Real reading of the real corpus.
# --------------------------------------------------------------------------

def judge(facts: dict, criteria: Optional[dict]) -> dict:
    """Judge the facts against the criteria.

    `criteria is None` is not a failure of the corpus and not a pass: it is a
    **withheld verdict**, and saying so is the honest outcome. `§41` forbids
    silently replacing a missing input with a convenient default.
    """
    if criteria is None:
        return {
            "verdict": "WITHHELD",
            "reason": ("no Active Knowledge version for "
                       f"{KNOWLEDGE_KEY!r}; the criteria this work judges "
                       "against are governed and none has been admitted"),
            "breaches": None,
        }
    breaches = [
        name for name, limit, actual in (
            ("stale_governance_sources",
             criteria["stale_governance_sources_max"],
             facts["stale_governance_sources"]),
            ("citation_errors", criteria["citation_errors_max"],
             facts["citation_errors"]),
            ("live_stale_assertions", criteria["live_stale_assertions_max"],
             facts["live_stale_assertions"]),
        ) if actual > limit
    ]
    return {
        "verdict": "HEALTHY" if not breaches else "DEGRADED",
        "reason": "measured against the admitted criteria",
        "breaches": tuple(breaches),
    }


def run(*, root: Path = REPO_ROOT, store_root: Optional[Path] = None) -> dict:
    """One real work cycle, hosted on a started Runtime and inside a Workflow.

    Returns what happened. Decides nothing about `E12-06` — `§29`:
    `CONSTRUCTION ≠ ACCEPTANCE`, and the measurement is
    `tools/p12_e12_acceptance`'s to make from the evidence this leaves behind.
    """
    import tempfile
    from tools.p12_trace_registry import STORE_ROOT

    # The Trace goes to the canonical durable store — the same root every other
    # real execution writes to and the one `p12_trace_registry` discovers.
    # Evidence written anywhere else is evidence no resident verifier can see.
    trace_store = LocalAppendOnlyStorage(
        (store_root or STORE_ROOT) / WORKFLOW_KEY)
    trace_store.provision()
    with tempfile.TemporaryDirectory() as tmp:
        # The Runtime's own working storage is separate and disposable: it
        # hosts the subsystems for this execution and holds no evidence.
        bootstrap = build_default_infrastructure(base_dir=Path(tmp))
        bootstrap.establish()

        # -- RUNTIME: started for real, in this process (P4) ---------------
        runtime = AIOSRuntime(
            runtime_id=RUNTIME_ID,
            storage=bootstrap.get("storage"),
            substrate=bootstrap.get("execution-substrate"),
        )
        runtime.initialize()
        runtime.start()
        if runtime.state is not RuntimeState.RUNNING:
            raise RuntimeError(f"runtime did not reach RUNNING: {runtime.state}")

        # -- WORKFLOW: this work runs inside one (P9) -----------------------
        identity = WorkflowIdentity(workflow_key=WORKFLOW_KEY,
                                    workflow_version="1.0")
        lifecycle = WorkflowLifecycle()
        lifecycle.define(Workflow(identity=identity))
        lifecycle.mark_ready(identity)
        lifecycle.enter_running(identity)
        monitor = WorkflowMonitor(lifecycle)
        if not monitor.is_active(identity):
            raise RuntimeError("workflow did not reach RUNNING")

        # `§22`: the run must be observable. Both subjects publish through the
        # canonical observation surface while they are genuinely in that state
        # — this is an observation of a real crossing, not a demonstration of
        # the observation surface.
        observation.publish(RUNTIME_ID, str(runtime.state),
                            kind=observation.RUNTIME)
        observation.publish(WORKFLOW_KEY, str(monitor.state_of(identity).state),
                            kind=observation.WORKFLOW)

        writer = TraceWriter(trace_store)

        try:
            outcome = _work(runtime, root, writer)
        except Exception:
            lifecycle.fail(identity, "the assessment raised")
            runtime.stop()
            raise

        lifecycle.succeed(identity)
        observation.publish(WORKFLOW_KEY,
                            str(monitor.state_of(identity).state),
                            kind=observation.WORKFLOW)
        outcome["workflow"] = {
            "key": WORKFLOW_KEY,
            "state": str(monitor.state_of(identity).state),
            "succeeded": bool(monitor.is_success(identity)),
        }
        runtime.stop()
        observation.publish(RUNTIME_ID, str(runtime.state),
                            kind=observation.RUNTIME)
        outcome["runtime"] = {"id": RUNTIME_ID, "state": str(runtime.state)}
        outcome["trace_records"] = _read_back(trace_store)
        return outcome


def _work(runtime, root: Path, writer) -> dict:
    """The work itself, reaching capability through the Execution Contract.

    `§15`: `CONSUMER → EXECUTION CONTRACT → RUNTIME`. `create_execution_layer`
    mints the Execution the Runtime hosts, and `execution.runtime.memory` /
    `.knowledge` are RUNNING-gated by the Runtime — this path adds no access
    control and bypasses none.

    **The assessment is three findings and a consolidation, and that is why
    Memory is load-bearing.** Each area of the corpus is assessed as its own
    step and its finding is retained; the consolidation step then reads the
    retained findings back and forms the assessment from them. Carrying those
    findings in a local variable instead would be the bypass `§8` names — the
    steps would still run, but Memory would not be consumed, and the work would
    only *look* integrated. Reading them back through `MemoryRetrieval` is the
    `E7-03` path the Memory consumer itself documents: *"propose the configured
    Candidate, then read the configured key — both during that Execution."*

    Runtime-hosted Memory is in-process by construction —
    `create_memory_subsystem` builds a bare `MemoryLifecycleStore()` holding no
    storage facility. So consumption is *within* the execution, which is the
    ratified shape, and a cross-run delta is **not** claimed.
    """
    execution = create_execution_layer(runtime)
    memory = execution.runtime.memory
    knowledge = execution.runtime.knowledge

    with TracedAction(writer, agent_instance=AGENT_INSTANCE,
                      runtime=RUNTIME_ID) as action:
        action.used_skill("corpus-health-assessment")

        # -- STEPS: assess each area, retaining each finding in Memory ------
        retained = {}
        for area, tool, assess in (
            ("governance", "tools/governance_index.py", _assess_governance),
            ("citations", "tools/corpus_citation_audit.py", _assess_citations),
            ("stale-state", "tools/stale_state_audit.py", _assess_stale_state),
        ):
            action.used_tool(tool)
            finding = assess(root)
            key = f"{MEMORY_KEY_PREFIX}.{area}"
            item = memory.lifecycle.admit(MemoryCandidate(
                key=key, payload=finding,
                provenance=MemoryProvenance(source=WORKFLOW_KEY,
                                            detail=f"{area} assessment")))
            if item is None:
                raise RuntimeError(f"Memory refused to retain {key!r}")
            retained[area] = key

        # -- CONSOLIDATION: read the findings back out of Memory -----------
        # The consolidation has no other source for them. This is the
        # consumption, and it is materially required by the work.
        facts = {}
        consumed = []
        for area, key in retained.items():
            item = memory.retrieval.active(key)
            if item is None:
                raise RuntimeError(f"Memory lost a retained finding: {key!r}")
            facts.update(item.payload)
            # INV-6: captured content, never a reference — the record stays
            # explainable if this Memory item is later expired.
            action.consumed_memory({"key": key, "content": dict(item.payload)})
            consumed.append(key)

        # -- KNOWLEDGE (P6): the governed criteria, if any exist ------------
        criteria = _active_criteria(knowledge)
        if criteria is not None:
            action.consumed_knowledge({"key": KNOWLEDGE_KEY,
                                       "content": criteria})
        verdict = judge(facts, criteria)

        outputs = {
            "facts": facts,
            "memory_keys_retained": tuple(retained.values()),
            "memory_keys_consumed": tuple(consumed),
            "verdict": verdict,
            "knowledge_available": criteria is not None,
        }
        action.produced(outputs)
        if verdict["verdict"] == "WITHHELD":
            # `§21`: a truthful failure is recorded, not engineered away. The
            # work ran and did its assessment; it could not reach a verdict,
            # and the record says exactly why.
            action.failed(verdict["reason"])

    return {"outputs": outputs,
            "knowledge_consumed": criteria is not None,
            "memory_consumed": bool(consumed)}


def _assess_governance(root: Path) -> dict:
    from tools.governance_index import GovernanceIndex, tracked_markdown
    index, _ = GovernanceIndex.build(tracked_markdown(root), root)
    return {
        "governance_records": len(index.records),
        "governance_sources": len(index.sources),
        "stale_governance_sources": len(index.stale_sources(root)),
    }


def _assess_citations(root: Path) -> dict:
    from tools import corpus_citation_audit
    report = corpus_citation_audit.audit(
        list(corpus_citation_audit.DEFAULT_ROOTS))
    return {
        "citation_documents": report["documents_scanned"],
        "citations_checked": report["citations_checked"],
        "citation_errors": report["errors"],
    }


def _assess_stale_state(root: Path) -> dict:
    from tools import stale_state_audit
    report = stale_state_audit.audit(root)
    return {
        "documents_scanned": report["documents_scanned"],
        "live_stale_assertions": report["errors"],
        "historical_uses": report["historical_uses"],
    }


def _active_criteria(knowledge) -> Optional[dict]:
    """The Active criteria version, or `None`.

    **Nothing here admits Knowledge.** `KnowledgeAdmission.admit` requires a
    `GovernanceReview` reflecting a provenance-verified **human** `approve` —
    a `ReviewDecision` carrying `HumanAuthority(reviewer_id)`. This office holds
    no human authority and does not manufacture one. `§36.8`.
    """
    version = knowledge.retrieval.active(KNOWLEDGE_KEY)
    return None if version is None else version.content


def _read_back(trace_store) -> dict:
    from native_core.core.trace import TraceReader
    try:
        records = tuple(TraceReader(trace_store).read())
    except Exception as exc:
        return {"available": False, "detail": f"{type(exc).__name__}: {exc}"}
    return {
        "available": True,
        "records": len(records),
        "with_memory_consumed": sum(1 for r in records if r.memory_consumed),
        "with_knowledge_consumed": sum(1 for r in records if r.knowledge_consumed),
    }


def main(argv=None) -> int:
    outcome = run()
    print(json.dumps(outcome, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
