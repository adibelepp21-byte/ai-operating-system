"""`Frontier` — RE-DISCOVER, and say whether the work is exhausted (E13-07; `D08`).

The cycle ends in exactly one of three states:

| State | When |
|---|---|
| `NOT_EXHAUSTED` | work P13 may do is still waiting (deferred by the cycle bound), or a P13 CORE question is neither answered nor classified. Re-verifying evidence already held in Memory does not count: it is always possible, so it is classified as *refreshable* |
| `EXHAUSTED` | nothing remains |
| `EXHAUSTED_WITH_CLASSIFIED_REMAINDER` | what remains is classified: escalated to a human, UNKNOWN, a classified gap, or residual frontier |

The residual frontier is read from the record that classifies it, never
asserted here. That means the `P13-015` rows marked P13 FRONTIER or UNKNOWN,
and `GAP-0017`/`GAP-0018` as `P13-017 §2` classifies them.
"""

from __future__ import annotations

import json
from typing import List, Optional

from tools.p13.model import ESCALATE, LIMITATION, REFUSE, UNKNOWN, Outcome
from tools.p13.paths import Paths

NOT_EXHAUSTED = "NOT_EXHAUSTED"
EXHAUSTED = "EXHAUSTED"
EXHAUSTED_WITH_REMAINDER = "EXHAUSTED_WITH_CLASSIFIED_REMAINDER"

STALE_RANK = 3        # next_action.RANK["evidence-stale"]
P13_017 = "docs/architecture/p13-preparation/P13-017-POST-FDR-2-GAP-RECONCILIATION.md"
RECORDED_FRONTIER = (("GAP-0017", "`0017` | replanning"),
                     ("GAP-0018", "`0018` | recovery beyond escalation"))


class Frontier:
    def __init__(self, paths: Paths):
        self._paths = paths

    def assess(self, decisions, outcome: Optional[Outcome], gaps) -> dict:
        remainder: List[dict] = []
        deferred = []
        for d in decisions:
            if d.decision == ESCALATE:
                remainder.append({"class": "escalated", "item": d.proposal.subject,
                                  "escalation_id": d.escalation_id})
            elif d.decision == UNKNOWN:
                remainder.append({"class": "unknown", "item": d.proposal.subject})
            elif d.decision == REFUSE and d.reason.startswith("cycle bound"):
                if d.proposal.priority[0] >= STALE_RANK:
                    # Re-verifying remembered evidence is always possible, so
                    # it never blocks exhaustion. It is classified instead.
                    remainder.append({"class": "refreshable",
                                      "item": d.proposal.subject})
                else:
                    deferred.append(d.proposal.subject)
            elif d.decision == REFUSE:
                remainder.append({"class": "refused", "item": d.proposal.subject,
                                  "reason": d.reason})
        for g in gaps:
            if g.gap_class == LIMITATION:
                remainder.append({"class": "limitation", "item": g.statement})
        rows, unclassified = self._matrix()
        remainder += [{"class": "frontier", "item": f"P13-015 {r['id']} "
                       f"({r['category']}): {r.get('gloss', '')}"} for r in rows]
        remainder += self._recorded_frontier()
        if outcome is not None and outcome.status != "success":
            deferred.append(f"{outcome.action_type} failed: {outcome.detail}")
        if deferred or unclassified:
            state = NOT_EXHAUSTED
        else:
            state = EXHAUSTED_WITH_REMAINDER if remainder else EXHAUSTED
        return {"state": state, "deferred": deferred,
                "unclassified_core": unclassified, "remainder": remainder}

    def _matrix(self):
        try:
            rows = json.loads(self._paths.matrix.read_text(encoding="utf-8"))["questions"]
        except (OSError, ValueError, KeyError) as error:
            return [], [f"P13-015 unreadable: {error}"]
        frontier = [r for r in rows if r.get("category") in ("P13 FRONTIER", "UNKNOWN")]
        unclassified = [r["id"] for r in rows
                        if r.get("category") == "P13 CORE" and not r.get("evidence")]
        return frontier, unclassified

    def _recorded_frontier(self):
        try:
            text = (self._paths.repo / P13_017).read_text(encoding="utf-8")
        except OSError:
            return [{"class": "frontier", "item": f"{P13_017} unreadable"}]
        return [{"class": "frontier", "item": f"{gap} (P13-017 §2)"}
                for gap, marker in RECORDED_FRONTIER if marker in text]
