"""`BoundedExecution` — EXECUTE IF AUTHORIZED, then VERIFY (E13-05).

It runs one thing: an `EXECUTE` that the `AuthorityGate` minted. A proposal is
refused by type. So is any other decision, and so is a second execution in the
same cycle. It runs only the executor the action type declares, which is always
an existing resident verifier. After the run, the cycle rebuilds the snapshot
with what the executor produced and re-evaluates, and that re-evaluation is the
verification.

This is **authorized limited execution** under the evidence-only envelope
(`P13-018 §5`). It does not show that P13 can carry out actions that change
state, because the envelope permits none.
"""

from __future__ import annotations

from typing import Optional

from tools.p13.model import (EXECUTE, VERIFIED, Fact, GateDecision, Outcome,
                             P13Error)
from tools.p13.paths import Paths


class BoundedExecution:
    def __init__(self, paths: Paths, catalog):
        self._paths = paths
        self._catalog = catalog
        self.outcome: Optional[Outcome] = None

    def execute(self, decision, observed_at: str) -> Outcome:
        if not isinstance(decision, GateDecision):
            raise TypeError("only a GateDecision can be executed; a proposal "
                            "is not an authorization (E13-04)")
        if decision.decision != EXECUTE:
            raise P13Error(f"{decision.decision} is not EXECUTE")
        if self.outcome is not None:
            raise P13Error("cycle bound: one executed action per cycle")
        action = self._catalog[decision.proposal.action_type]
        if action.reserved or action.run is None:
            raise P13Error(f"{action.name} has no executor P13 may run")
        try:
            produced = action.run(self._paths)
            status, detail = "success", f"{action.executor} ran"
            facts = tuple(Fact(k, v, VERIFIED,
                               f"{action.executor} (executed under {decision.envelope})",
                               observed_at) for k, v in sorted(produced.items()))
        except Exception as error:
            status, detail, facts = "failure", f"{type(error).__name__}: {error}", ()
        self.outcome = Outcome(decision.proposal.id, action.name, decision.envelope,
                               action.executor, status, detail, facts)
        return self.outcome
