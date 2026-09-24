"""`Reasoning` — reason over evidence (E13-03; `D01`).

Deterministic rules over typed evidence (Blueprint `§3.4`: no model, no
vendor). Every conclusion names its rule and its premises. Every premise must
be a fact or an evaluation **of the same cycle**; one that names anything else
is rejected (E13-03's negative controls).

| Rule | From | Concludes | Answers |
|---|---|---|---|
| `R-DEFECT` | a FAIL | a defect, classed by its criterion (error / architecture gap) | Q40 |
| `R-OBTAINABLE` | an UNKNOWN whose missing facts a resident verifier produces | the evidence can be obtained, and by what | Q17 |
| `R-STALE` | a result that rests on Memory (INFERRED) | re-verification would make it current | Q17 |
| `R-GAP` | an UNKNOWN that nothing resident can resolve | a knowledge gap, a limitation, or a capability gap | Q19, Q27, Q40, Q89 |
| `R-SYSTEMIC` | two or more FAILs that share a source, or UNKNOWNs whose shared source is down | one common cause, not several problems | Q57, Q59 |
| `R-CHANGED` | this cycle's facts vs the last cycle's, from Memory | what changed | E13-06 |
| `R-AUTHORITY` | an envelope anomaly | a governance defect | `G-02` |
| `R-AWAITING` | OPEN escalations | a human response is pending; P13 cannot give one | `§5.3` |

An unknown **matters** (Q19, Q89) exactly when an authority-bearing criterion
needs it. Facts no criterion requires raise no gap.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

from tools.p13.catalog import CATALOG, producer
from tools.p13.model import (CAPABILITY_GAP, ERROR, FAIL, INFERRED,
                             KNOWLEDGE_GAP, LIMITATION, PASS, UNKNOWN, VERIFIED,
                             Conclusion, EvaluationResult, P13Error,
                             StateSnapshot, digest)

SKIP_IN_CHANGE = ("memory.", "self_model.what_changed", "authority.")


def _source_of(text: str) -> str:
    return text.split(":")[0].split(" (")[0].strip()


class Reasoning:
    def __init__(self, catalog=CATALOG):
        self._catalog = catalog

    def reason(self, snapshot: StateSnapshot,
               evaluations: Tuple[EvaluationResult, ...]) -> Tuple[Conclusion, ...]:
        out: List[Conclusion] = []
        for e in evaluations:
            keys = tuple(e.evidence) or ()
            needed = e.requires or keys
            if e.result == FAIL:
                out.append(Conclusion(
                    f"c:defect:{e.criterion}", "R-DEFECT", "defect",
                    f"{e.criterion} violated: {e.reason}", (e.id,) + keys,
                    e.certainty, e.criterion, e.gap_class))
            elif e.result == UNKNOWN:
                missing = tuple(k for k in needed
                                if (snapshot.get(k) is None
                                    or snapshot.get(k).status == UNKNOWN))
                producers = {k: producer(k, self._catalog) for k in missing}
                if missing and all(producers.values()):
                    for action in sorted(set(producers.values())):
                        out.append(Conclusion(
                            f"c:obtainable:{e.criterion}:{action}", "R-OBTAINABLE",
                            "evidence-obtainable",
                            f"{e.criterion} is UNKNOWN; {action} produces "
                            + ", ".join(k for k, a in producers.items() if a == action),
                            (e.id,) + tuple(k for k in missing if snapshot.get(k)),
                            VERIFIED, action))
                else:
                    unresolvable = [k for k, a in producers.items() if not a] or list(needed)
                    out.append(Conclusion(
                        f"c:gap:{e.criterion}", "R-GAP", "gap",
                        f"{e.criterion} cannot be evaluated: "
                        + ", ".join(unresolvable) + " — nothing resident resolves it",
                        (e.id,) + tuple(k for k in unresolvable if snapshot.get(k)),
                        VERIFIED, e.criterion,
                        _classify(unresolvable, snapshot)))
            elif e.certainty == INFERRED:
                stale = [k for k in needed if snapshot.get(k)
                         and snapshot.get(k).status == INFERRED]
                action = producer(stale[0], self._catalog) if stale else None
                if action:
                    out.append(Conclusion(
                        f"c:stale:{e.criterion}:{action}", "R-STALE", "evidence-stale",
                        f"{e.criterion} is {e.result} on remembered evidence only; "
                        f"{action} would make it current",
                        (e.id,) + tuple(stale), INFERRED, action))
        out.extend(self._systemic(evaluations))
        out.extend(self._changed(snapshot))
        out.extend(self._authority(snapshot))
        out.extend(self._awaiting(snapshot))
        for c in out:
            self.check(c, snapshot, evaluations)
        return tuple(out)

    @staticmethod
    def check(conclusion: Conclusion, snapshot: StateSnapshot,
              evaluations: Tuple[EvaluationResult, ...]) -> None:
        """Every premise resolves in this cycle, or the conclusion is rejected."""
        known = set(snapshot.keys()) | {e.id for e in evaluations}
        dangling = [p for p in conclusion.premises if p not in known]
        if dangling:
            raise P13Error(f"{conclusion.id}: premise(s) {dangling} name nothing "
                           "in this cycle (E13-03)")

    @staticmethod
    def _systemic(evaluations) -> List[Conclusion]:
        # A FAIL counts against every source it read. An UNKNOWN counts only
        # against a source that was *down*: evidence that was simply never
        # verified yet is obtainable one verifier at a time, not a common cause.
        # (The first live cycles concluded "systemic" from three never-verified
        # facts; recorded in the P13 construction record.)
        by_source: Dict[str, List[EvaluationResult]] = defaultdict(list)
        for e in evaluations:
            if e.result == FAIL:
                sources = e.sources
            elif e.result == UNKNOWN:
                sources = [s for s in e.sources if "unavailable" in s]
            else:
                continue
            for s in {_source_of(s) for s in sources}:
                by_source[s].append(e)
        out = []
        for source, group in sorted(by_source.items()):
            if len(group) >= 2:
                certainty = (VERIFIED if all(e.certainty == VERIFIED for e in group)
                             else INFERRED)
                out.append(Conclusion(
                    f"c:systemic:{digest(source)[:12]}", "R-SYSTEMIC", "systemic",
                    f"{len(group)} criteria fail or are unknown on one source "
                    f"({source}): one cause, not {len(group)} problems",
                    tuple(e.id for e in group), certainty, source))
        return out

    @staticmethod
    def _changed(snapshot: StateSnapshot) -> List[Conclusion]:
        memory = snapshot.get("memory.p13.previous")
        if memory is None or memory.status == UNKNOWN or not memory.value:
            return []
        before = memory.value.get("facts") or {}
        changed = sorted(
            f.key for f in snapshot.facts
            if f.key in before and f.status != UNKNOWN
            and not f.key.startswith(SKIP_IN_CHANGE)
            and digest(f.value) != before[f.key])
        return [Conclusion(
            "c:changed", "R-CHANGED", "changed" if changed else "unchanged",
            (f"changed since cycle {memory.value.get('cycle_id')}: "
             + ", ".join(changed)) if changed else
            f"no observed fact changed since cycle {memory.value.get('cycle_id')}",
            ("memory.p13.previous",) + tuple(changed), VERIFIED, "state")]

    @staticmethod
    def _authority(snapshot: StateSnapshot) -> List[Conclusion]:
        anomalies = snapshot.get("authority.anomalies")
        if anomalies is None or anomalies.status == UNKNOWN or not anomalies.value:
            return []
        return [Conclusion(
            "c:defect:authority", "R-AUTHORITY", "defect",
            "envelope record(s) failed to resolve: " + "; ".join(anomalies.value),
            ("authority.anomalies",), VERIFIED, "authority", ERROR)]

    @staticmethod
    def _awaiting(snapshot: StateSnapshot) -> List[Conclusion]:
        opened = snapshot.get("escalations.open")
        if opened is None or opened.status == UNKNOWN or not opened.value:
            return []
        return [Conclusion(
            "c:awaiting", "R-AWAITING", "awaiting-human",
            f"{len(opened.value)} escalation(s) OPEN; only a human response "
            "closes one (record_response requires HumanAuthority)",
            ("escalations.open",), VERIFIED, "escalations")]


def _classify(keys, snapshot: StateSnapshot) -> str:
    if any(k.startswith("knowledge.") for k in keys):
        return KNOWLEDGE_GAP
    if any(snapshot.get(k) and "unavailable" in snapshot.get(k).source for k in keys):
        return LIMITATION
    return CAPABILITY_GAP
