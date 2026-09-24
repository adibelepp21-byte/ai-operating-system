"""`NextAction` — WHAT SHOULD I DO NEXT? (E13-04; `D03` q3).

Turns conclusions into **proposals**. A proposal is not a decision (see
`model.ActionProposal`). The gate decides.

| Conclusion | Proposal |
|---|---|
| defect | the criterion's remedy (always a reserved type → the gate escalates) |
| evidence-obtainable | the verifier that produces the missing evidence |
| knowledge gap | `admit.knowledge` (reserved; admission is governed, `§3.5` p5) |
| evidence-stale | the verifier that makes remembered evidence current |

**Priority** (Q41, Q63, Q69, Q73) is a fixed rule, not a judgement:

1. defects first, because a governed criterion is violated;
2. then evidence the cycle lacks;
3. then knowledge gaps;
4. then stale evidence.

Within a rank, the verification done least recently according to Memory goes
first, so repeated cycles rotate through what is unverified instead of
re-running one check. Ties break on id. Every criterion cites a Founder-issued
instrument, so *what matters most to the Founder* (Q63) is answered only as far
as the Founder's decisions state it. A wider answer is frontier (Q63 in
`P13-015`).
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from tools.p13.model import (INFERRED, KNOWLEDGE_GAP, UNKNOWN, VERIFIED,
                             ActionProposal, Conclusion, StateSnapshot)

RANK = {"defect": 0, "evidence-obtainable": 1, "gap": 2, "evidence-stale": 3}
_WORST = {VERIFIED: 0, INFERRED: 1, UNKNOWN: 2}


class NextAction:
    def __init__(self, criteria):
        self._remedy = {c.id: c.remedy for c in criteria}

    def propose(self, conclusions: Tuple[Conclusion, ...],
                snapshot: StateSnapshot) -> Tuple[ActionProposal, ...]:
        memory = snapshot.get("memory.p13.previous")
        last = ((memory.value or {}).get("last_executed", {})
                if memory and memory.status != UNKNOWN else {})
        grouped: Dict[Tuple[str, str], List[Conclusion]] = {}
        for c in conclusions:
            key = self._action(c)
            if key:
                grouped.setdefault(key, []).append(c)
        proposals = []
        for (action, target), group in grouped.items():
            rank = min(RANK[c.kind] for c in group)
            certainty = max((c.certainty for c in group), key=_WORST.get)
            proposals.append(ActionProposal(
                id=f"p:{action}:{target}", action_type=action, target=target,
                derived_from=tuple(c.id for c in group),
                rationale="; ".join(c.statement for c in group),
                certainty=certainty,
                priority=(rank, last.get(action, ""), f"{action}:{target}")))
        return tuple(sorted(proposals, key=lambda p: p.priority))

    def _action(self, c: Conclusion):
        if c.kind == "defect":
            if c.subject == "authority":
                return ("change.governance", "p13-envelopes")
            return (self._remedy.get(c.subject, "change.governance"), c.subject)
        if c.kind in ("evidence-obtainable", "evidence-stale"):
            return (c.subject, "state")
        if c.kind == "gap" and c.gap_class == KNOWLEDGE_GAP:
            return ("admit.knowledge", c.subject)
        return None
