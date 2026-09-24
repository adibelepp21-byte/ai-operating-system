"""One bounded P13 cycle, and the entry point a human or the CEO runs.

```text
OBSERVE → UNDERSTAND → EVALUATE → REASON → PROPOSE → AUTHORITY CHECK
  → EXECUTE IF AUTHORIZED → VERIFY → LEARN/EVOLVE → RE-DISCOVER → RECORD
```

That is contract C-01. No link is skipped, and each one is a component.

**P13 runs when it is run** (Blueprint `§3.3`). There is no daemon,
scheduler, queue, thread or self-activation. `--cycles N` is a bounded run
chosen by the invoker, capped at `MAX_CYCLES`. It stops early when a cycle
executes nothing, when the work is exhausted, or when the state digest repeats
(no progress).

A cycle does nothing unless a recorded envelope resolves and grants its basis:
item 2 to observe, items 3 and 4 to record. Without one, P13 raises one
escalation (`G-02`) and stops.

    python -m tools.p13.cycle --invoker "<who>" --intent "<why>" [--cycles N]
"""

from __future__ import annotations

import argparse
import json
from typing import List, Optional

from tools.p13.authority import AuthorityGate, load_envelopes, raise_escalation
from tools.p13.catalog import CATALOG
from tools.p13.evaluation import CRITERIA, Evaluation
from tools.p13.evidence import EvidenceStore
from tools.p13.evolution import Evolution
from tools.p13.execution import BoundedExecution
from tools.p13.frontier import Frontier
from tools.p13.model import (ESCALATE, EXECUTE, P13Error, UNKNOWN, VERIFIED,
                             digest, recorded)
from tools.p13.next_action import NextAction
from tools.p13.paths import LIVE, Paths
from tools.p13.reasoning import Reasoning
from tools.p13.state import SOURCES, StateUnderstanding, now

MAX_CYCLES = 5

SECTION_29 = {
    "intent": "intent", "decision": "decisions", "work": "executed",
    "actor": "invoker", "authority": "authority", "scope": "executed.action_type",
    "execution": "executed", "observation": "observation",
    "verification": "verification", "evidence": "observation.before.facts",
    "provenance": "conclusions[].premises · proposals[].derived_from",
    "lifecycle": "lifecycle",
}


def run_cycle(paths: Paths = LIVE, *, intent: str, invoker: str,
              sources=SOURCES, criteria=CRITERIA, catalog=CATALOG,
              clock=now) -> dict:
    if not (intent or "").strip() or not (invoker or "").strip():
        raise P13Error("a cycle is invoked by someone, for a reason: both are "
                       "recorded (§29 intent, actor)")
    envelopes, anomalies = load_envelopes(paths)
    if not any({"observe", "record"} <= set(e.cycle_basis) for e in envelopes):
        escalation = raise_escalation(
            paths, envelopes, "P13 cycle",
            "no recorded envelope permits a P13 cycle (observe + record); "
            "NO RECORDED AUTHORITY → NO EXECUTION"
            + (f"; anomalies: {'; '.join(anomalies)}" if anomalies else ""),
            required="a recorded envelope granting observe and record")
        return {"status": "REFUSED", "escalation_id": escalation,
                "anomalies": list(anomalies)}

    understanding = StateUnderstanding(paths, sources, clock)
    before = understanding.observe()
    evaluation = Evaluation(paths, criteria)
    evaluated_before = evaluation.evaluate(before)
    conclusions = Reasoning(catalog).reason(before, evaluated_before)
    proposals = NextAction(evaluation.admitted).propose(conclusions, before)
    gaps, evolutions = Evolution(paths).derive(conclusions, before)

    gate = AuthorityGate(paths, catalog, envelopes)
    execution = BoundedExecution(paths, catalog)
    decisions = []
    for proposal in proposals + evolutions:
        decision = gate.decide(proposal)
        decisions.append(decision)
        if decision.decision == EXECUTE:
            execution.execute(decision, clock())
    outcome = execution.outcome

    after, evaluated_after = before, evaluated_before
    if outcome is not None and outcome.produced:
        after = before.with_facts(outcome.produced, clock())
        evaluated_after = evaluation.evaluate(after)
    frontier = Frontier(paths).assess(decisions, outcome, gaps)

    cycle_id = before.taken_at.replace(":", "").replace("-", "")[:15] + "-" + before.digest[:8]
    previous = (before.get("memory.p13.previous").value
                if before.get("memory.p13.previous")
                and before.get("memory.p13.previous").status == VERIFIED else None) or {}
    verified = dict(previous.get("verified") or {})
    last_executed = dict(previous.get("last_executed") or {})
    if outcome is not None and outcome.status == "success":
        last_executed[outcome.action_type] = after.taken_at
        for fact in outcome.produced:
            if fact.key.startswith("verification."):
                verified[fact.key] = {"value": fact.value, "cycle_id": cycle_id,
                                      "at": after.taken_at}
    changes = [{"criterion": b.criterion, "before": b.result, "after": a.result,
                "certainty_before": b.certainty, "certainty_after": a.certainty}
               for b, a in zip(evaluated_before, evaluated_after)
               if (b.result, b.certainty) != (a.result, a.certainty)]
    escalations = [d.escalation_id for d in decisions if d.decision == ESCALATE]

    record = {
        "cycle_id": cycle_id,
        "p13": "tools/p13 · Blueprint v1.0 · P13-018",
        "intent": intent, "invoker": invoker,
        "authority": {"envelopes": [e.id for e in envelopes],
                      "anomalies": list(anomalies),
                      "refused_criteria": evaluation.refused},
        "observation": {"before": recorded(before), "after": recorded(after),
                        "digest_before": before.digest, "digest_after": after.digest},
        "evaluations_before": recorded(evaluated_before),
        "evaluations_after": recorded(evaluated_after),
        "conclusions": recorded(conclusions),
        "proposals": recorded(proposals + evolutions),
        "decisions": [d.recorded() for d in decisions],
        "executed": recorded(outcome) if outcome else None,
        "verification": {"re_evaluated": outcome is not None and bool(outcome.produced),
                         "changes": changes},
        "gaps": recorded(gaps),
        "frontier": frontier,
        "briefing": _briefing(decisions, evaluated_after, frontier),
        "lifecycle": "RECORDED — append-only; never rewritten",
        "section_29": SECTION_29,
    }
    store = EvidenceStore(paths)
    path, record_digest = store.write_cycle(record)
    readback = store.readback(path, record_digest)
    criteria_fact = before.get("knowledge.corpus_health_criteria")
    memory_fact = before.get("memory.p13.previous")
    store.write_trace(
        outputs={"cycle_id": cycle_id, "record_digest": record_digest,
                 "readback_holds": readback,
                 "digest_before": before.digest, "digest_after": after.digest,
                 "facts": {f.key: digest(f.value) for f in after.facts},
                 "results": {e.criterion: e.result for e in evaluated_after},
                 "executed": outcome.action_type if outcome else None,
                 "verified": verified, "last_executed": last_executed,
                 "exhaustion": frontier["state"]},
        status=("failure" if (outcome and outcome.status != "success") or not readback
                else "escalation" if escalations else "success"),
        tools_used=[outcome.executor] if outcome else [],
        knowledge_consumed=([{"key": "corpus-health.criteria",
                              "content": criteria_fact.value}]
                            if criteria_fact and criteria_fact.status == VERIFIED else []),
        memory_consumed=([{"key": "memory.p13.previous", "content": memory_fact.value}]
                         if memory_fact and memory_fact.value else []))
    return {"status": "RECORDED", "cycle_id": cycle_id,
            "record": _shown(path, paths), "readback_holds": readback,
            "executed": outcome.action_type if outcome else None,
            "decisions": {d.proposal.subject: d.decision for d in decisions},
            "escalations": escalations,
            "results": {e.criterion: f"{e.result}/{e.certainty}" for e in evaluated_after},
            "changes": changes, "exhaustion": frontier["state"],
            "digest_after": after.digest, "briefing": record["briefing"]}


def _shown(path, paths: Paths) -> str:
    try:
        return path.relative_to(paths.repo).as_posix()
    except ValueError:
        return str(path)


def _briefing(decisions, evaluations, frontier) -> List[str]:
    """What the Founder needs from this cycle, most pressing first (Q61, Q62)."""
    lines = [f"ESCALATED {d.proposal.subject}: {d.reason} [{d.escalation_id}]"
             for d in decisions if d.decision == ESCALATE]
    lines += [f"{e.criterion}: {e.result} ({e.reason})"
              for e in evaluations if e.result != "PASS"]
    lines.append(f"exhaustion: {frontier['state']}; deferred {len(frontier['deferred'])}, "
                 f"classified remainder {len(frontier['remainder'])}")
    return lines


def run(paths: Paths = LIVE, *, cycles: int = 1, **kwargs) -> List[dict]:
    if not 1 <= cycles <= MAX_CYCLES:
        raise P13Error(f"cycles must be 1…{MAX_CYCLES}; a run is bounded")
    results: List[dict] = []
    for _ in range(cycles):
        result = run_cycle(paths, **kwargs)
        results.append(result)
        if (result["status"] != "RECORDED" or result["executed"] is None
                or result["exhaustion"] != "NOT_EXHAUSTED"):
            break
        if len(results) > 1 and results[-2].get("digest_after") == result["digest_after"]:
            break                                   # no progress
    return results


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--invoker", required=True)
    parser.add_argument("--intent", required=True)
    parser.add_argument("--cycles", type=int, default=1)
    args = parser.parse_args(argv)
    results = run(cycles=args.cycles, intent=args.intent, invoker=args.invoker)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if all(r["status"] == "RECORDED" and r.get("readback_holds")
                    for r in results) else 1


if __name__ == "__main__":
    # Run as `python -m tools.p13.cycle`. The module-level `tools` imports
    # install the certified-write barrier before anything runs (GOAL-V2-004).
    raise SystemExit(main())
