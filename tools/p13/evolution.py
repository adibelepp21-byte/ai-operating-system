"""`Evolution` — WHAT SHOULD CHANGE? (E13-06; `D03` q6; `GAP-0014`/`0020`–`0022`).

Collects this cycle's gaps from its conclusions, plus any `P13-015` P13 CORE
row that cites no evidence, and proposes how each one would close. **Every
evolution proposal targets code, governance or Knowledge**, which are all
reserved. So every one reaches a human through the gate as an escalation, and
none executes. *Learning* here means a proposal into governed admission
(`GAP-0022`). P13 never admits, promotes or changes anything by itself
(Constitution `§3.5` principles 4, 5).
"""

from __future__ import annotations

import json
from typing import List, Tuple

from tools.p13.model import (ARCHITECTURE_GAP, CAPABILITY_GAP, ERROR,
                             KNOWLEDGE_GAP, LIMITATION, VERIFIED, ActionProposal,
                             Conclusion, Gap, StateSnapshot)
from tools.p13.paths import Paths

DISPOSITION = {
    ERROR: ("a remedy is proposed; the gate decides it: a reserved remedy "
            "escalates, and one a recorded envelope permits may execute"),
    ARCHITECTURE_GAP: "stop at the boundary; Architect / Founder authority (P13-018 §8)",
    KNOWLEDGE_GAP: "admission is governed: admit.knowledge escalates",
    CAPABILITY_GAP: "a code change is proposed and escalated; P13 never builds itself",
    LIMITATION: "classified: the source was unreadable this cycle; re-observe",
}


class Evolution:
    def __init__(self, paths: Paths):
        self._paths = paths

    def derive(self, conclusions: Tuple[Conclusion, ...],
               snapshot: StateSnapshot) -> Tuple[Tuple[Gap, ...], Tuple[ActionProposal, ...]]:
        gaps: List[Gap] = []
        for c in conclusions:
            if c.kind in ("defect", "gap") and c.gap_class:
                gaps.append(Gap(f"g:{c.id[2:]}", c.gap_class, c.statement, (c.id,),
                                DISPOSITION[c.gap_class]))
        for row in self._core_rows_without_evidence():
            gaps.append(Gap(f"g:matrix:{row['id']}", CAPABILITY_GAP,
                            f"P13-015 {row['id']} ({row.get('gloss', '')}) is P13 CORE "
                            "and cites no evidence of an answer",
                            ("matrix",), DISPOSITION[CAPABILITY_GAP]))
        proposals = tuple(
            ActionProposal(id=f"e:{g.id[2:]}", action_type="change.code",
                           target=g.id, derived_from=g.derived_from,
                           rationale=g.statement, certainty=VERIFIED,
                           priority=(5, "", g.id), origin="evolution")
            for g in gaps if g.gap_class == CAPABILITY_GAP)
        return tuple(gaps), proposals

    def _core_rows_without_evidence(self):
        try:
            rows = json.loads(self._paths.matrix.read_text(encoding="utf-8"))["questions"]
        except (OSError, ValueError, KeyError):
            return []
        return [r for r in rows if r.get("category") == "P13 CORE" and not r.get("evidence")]
