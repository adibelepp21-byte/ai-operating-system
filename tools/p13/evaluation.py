"""`Evaluation` — IS THAT STATE GOOD? (E13-02; `D03` q2).

A criterion is admitted only if its authority resolves: the act exists and its
identifier is in the Decision Register (`tools/authority_citation.refusal`). A
criterion whose citation does not resolve is **refused**. It is reported, and
never evaluated (E13-02's negative control). P13 authors none of these
thresholds. Each one is quoted from the instrument it cites:

| Criterion | Authority | Threshold |
|---|---|---|
| `CR-INTEGRITY` | `P13-018` `G-05` | certified P10–P12 evidence holds against its manifests |
| `CR-NATIVE-CORE` | `FDR-2` `D09` · `P13-018` `§8` | `NATIVE CORE = 11` |
| `CR-CORPUS-*` | `FD-P12-002` (admitted Knowledge; `P13-018` `D-3`) | each `<fact>_max` in the Active criteria |
| `CR-RECONCILIATION` | `FDR-1` `§12` | the P13-015 matrix verifies against the tree |
| `CR-MEMORY-INTELLIGENCE` | `FDR-2` `D06` | Memory ↔ Intelligence is not NOT CONNECTED |
| `CR-P13-EVIDENCE` | `P13-018` `G-04` | P13's own records and Trace verify |

**Missing evidence gives UNKNOWN, never PASS.** Every required fact must be
present and known. A judgement that cannot be computed is also UNKNOWN. A
result that rests on an INFERRED fact (Memory, i.e. an earlier cycle) is
marked INFERRED.

The criteria are read, never modified or promoted (`P13-018 §6`). A PASS
certifies nothing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple

from tools import authority_citation
from tools.p13.model import (ARCHITECTURE_GAP, ERROR, FAIL, INFERRED, PASS,
                             UNKNOWN, VERIFIED, Citation, EvaluationResult,
                             StateSnapshot)
from tools.p13.paths import Paths

ACTS = "docs/governance/acts/"
P13_018 = ACTS + "P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md"
FDR_2 = ACTS + "FDR-2-P13-DEFINITION-BOUNDARY-AUTONOMY-AND-EXIT-CONTRACT.md"
FDR_1 = ACTS + "FDR-1-FOUNDER-REVIEW-AND-DISPOSITION-OF-P13-BLUEPRINT-V0-4.md"
FD_P12_002 = ACTS + "FD-P12-002-P6-KNOWLEDGE-ADMISSION.md"

Judge = Callable[[Dict[str, Any]], bool]


@dataclass(frozen=True)
class Criterion:
    id: str
    description: str
    citation: Citation
    requires: Tuple[str, ...]
    judge: Judge
    gap_class: str
    remedy: str             # the action type a FAIL would need: always reserved


def _within(fact: str) -> Judge:
    def judge(values):
        limit = values["knowledge.corpus_health_criteria"]["content"][f"{fact}_max"]
        return values[f"corpus.{fact}"] <= limit
    return judge


CRITERIA: Tuple[Criterion, ...] = (
    Criterion("CR-INTEGRITY", "certified P10–P12 evidence holds",
              Citation("P13-018", "P13-018 §9 G-05", P13_018),
              ("integrity.holds",), lambda v: v["integrity.holds"] is True,
              ERROR, "change.certified_evidence"),
    Criterion("CR-NATIVE-CORE", "NATIVE CORE = 11",
              Citation("FDR-2", "FDR-2 D09", FDR_2),
              ("native_core.boundaries",), lambda v: v["native_core.boundaries"] == 11,
              ARCHITECTURE_GAP, "change.native_core"),
    *(Criterion(f"CR-CORPUS-{fact.upper().replace('_', '-')}",
                f"{fact} within the admitted corpus-health criteria",
                Citation("FD-P12-002", "FD-P12-002", FD_P12_002),
                (f"corpus.{fact}", "knowledge.corpus_health_criteria"),
                _within(fact), ERROR, "change.governance")
      for fact in ("citation_errors", "live_stale_assertions",
                   "stale_governance_sources")),
    Criterion("CR-RECONCILIATION", "the foundational-question matrix verifies",
              Citation("FDR-1", "FDR-1 §12", FDR_1),
              ("verification.foundational_question_reconciliation",),
              lambda v: v["verification.foundational_question_reconciliation"]["holds"] is True,
              ERROR, "change.governance"),
    Criterion("CR-MEMORY-INTELLIGENCE", "Memory ↔ Intelligence is connected",
              Citation("FDR-2", "FDR-2 D06", FDR_2),
              ("verification.ecosystem_relationships",),
              lambda v: v["verification.ecosystem_relationships"]["Memory↔Intelligence"]
              != "NOT CONNECTED",
              ERROR, "change.code"),
    Criterion("CR-P13-EVIDENCE", "P13's own records and Trace verify",
              Citation("P13-018", "P13-018 §9 G-04", P13_018),
              ("verification.p13_evidence",),
              lambda v: v["verification.p13_evidence"]["holds"] is True,
              ERROR, "change.code"),
)


class Evaluation:
    def __init__(self, paths: Paths, criteria: Tuple[Criterion, ...] = CRITERIA):
        self.admitted: List[Criterion] = []
        self.refused: List[dict] = []
        for criterion in criteria:
            c = criterion.citation
            why = authority_citation.refusal(c.instrument, c.record, c.identifier,
                                             paths.repo, paths.decision_register)
            if why:
                self.refused.append({"criterion": criterion.id, "reason": why})
            else:
                self.admitted.append(criterion)

    def evaluate(self, snapshot: StateSnapshot) -> Tuple[EvaluationResult, ...]:
        return tuple(self._one(c, snapshot) for c in self.admitted)

    @staticmethod
    def _one(criterion: Criterion, snapshot: StateSnapshot) -> EvaluationResult:
        facts = {k: snapshot.get(k) for k in criterion.requires}
        unknown = sorted(k for k, f in facts.items() if f is None or f.status == UNKNOWN)
        sources = tuple(f.source if f else f"{k}: absent" for k, f in facts.items())
        values = {k: f.value for k, f in facts.items() if f is not None}
        certainty = (INFERRED if any(f and f.status == INFERRED for f in facts.values())
                     else VERIFIED)

        def result(outcome, reason):
            return EvaluationResult(criterion.id, outcome, certainty, values,
                                    sources, criterion.citation.instrument,
                                    criterion.gap_class, reason, criterion.requires)

        if unknown:
            return result(UNKNOWN, "insufficient evidence: " + ", ".join(unknown))
        try:
            passed = criterion.judge(values)
        except Exception as error:      # cannot judge → cannot pass
            return result(UNKNOWN, f"not judgeable: {type(error).__name__}: {error}")
        return result(PASS if passed else FAIL,
                      criterion.description + (" — holds" if passed else " — violated"))
