"""`BoundedExecution` — EXECUTE IF AUTHORIZED, then VERIFY (E13-05).

It runs one thing: an `EXECUTE` that the `AuthorityGate` minted. A proposal is
refused by type. So is any other decision, and so is a second execution in the
same cycle. It runs only the executor the action type declares.

**Read-only types** (all that `P13-ENV-01` permits) are verified by the cycle
re-deriving the snapshot from what they produced and re-evaluating it.

**State-changing types** follow the post-construction instruction's `§8.5`:

```text
OBSERVE BEFORE → EXECUTE → OBSERVE AFTER → COMPARE → VERIFY → (trace, state update)
```

The type observes its whole boundary, which is wider than the target, so the
comparison can show that nothing **outside** the authorized scope changed. Any
change outside the scope, or a postcondition that does not hold, is a FAILURE
outcome. It is never a success. `P13-ENV-02` (`FDR-3`) permitted
`s_ops.open` and `s_ops.close` on the one S-OPS object, and the path ran live
for the E13-05 proof. `FDR-4` `FD-B` retired that envelope afterwards. No
recorded envelope permits a state-changing type now (`EXECUTION CAPABLE ≠
EXECUTION AUTHORIZED`).
"""

from __future__ import annotations

from typing import Optional

from tools.p13.catalog import READ_ONLY
from tools.p13.model import (EXECUTE, VERIFIED, Fact, GateDecision, Outcome,
                             P13Error)
from tools.p13.paths import Paths


def _within(path: str, scope) -> bool:
    return any(path == t or path.startswith(t.rstrip("/") + "/") for t in scope)


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
        if action.reserved or action.run is None or not action.verifiable:
            raise P13Error(f"{action.name} has no executor P13 may run")
        target = decision.proposal.target
        if action.effect != READ_ONLY and not _within(target, decision.scope):
            raise P13Error(f"{target!r} is outside the authorized scope")
        try:
            if action.effect == READ_ONLY:
                produced = action.run(self._paths)
                status, detail = "success", f"{action.executor} ran"
            else:
                produced, status, detail = self._state_changing(action, decision, target)
            facts = tuple(Fact(k, v, VERIFIED,
                               f"{action.executor} (executed under {decision.envelope})",
                               observed_at) for k, v in sorted(produced.items()))
        except Exception as error:
            status, detail, facts = "failure", f"{type(error).__name__}: {error}", ()
        self.outcome = Outcome(decision.proposal.id, action.name, decision.envelope,
                               action.executor, status, detail, facts)
        return self.outcome

    def _state_changing(self, action, decision, target):
        before = action.observe(self._paths, target)
        produced = dict(action.run(self._paths, target) or {})
        after = action.observe(self._paths, target)
        changed = sorted(k for k in set(before) | set(after)
                         if before.get(k) != after.get(k))
        outside = [k for k in changed if not _within(k, decision.scope)]
        holds, why = action.verify(self._paths, target, before, after)
        produced[f"execution.{action.name}"] = {
            "target": target, "scope": list(decision.scope), "changed": changed,
            "outside_scope": outside, "postcondition_holds": bool(holds),
            "postcondition": why, "verified": bool(holds) and not outside}
        if outside:
            return produced, "failure", f"changed outside the authorized scope: {outside}"
        if not holds:
            return produced, "failure", f"postcondition does not hold: {why}"
        return produced, "success", (f"{action.executor} changed {changed}; "
                                     f"verified: {why}")
