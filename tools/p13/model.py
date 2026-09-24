"""The P13 types: one record per link of the semantic chain (Blueprint `§3.2`).

Every type here is frozen, and each one refuses to exist in a shape the
Blueprint forbids:

* a `Fact` without a source (E13-01's negative control);
* a `Conclusion` without premises (E13-03);
* an `ActionProposal` that carries authority. It has no field that could hold
  one, so a proposal cannot be read as a decision (E13-04, `GSI-02`);
* a `GateDecision` built outside the `AuthorityGate`. Only the gate holds the
  token its constructor checks, so nothing else can mint an `EXECUTE`
  (E13-05, `G-08`).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple

VERIFIED, INFERRED, UNKNOWN = "VERIFIED", "INFERRED", "UNKNOWN"
FACT_STATUSES = (VERIFIED, INFERRED, UNKNOWN)

PASS, FAIL = "PASS", "FAIL"
RESULTS = (PASS, FAIL, UNKNOWN)

EXECUTE, ESCALATE, REFUSE = "EXECUTE", "ESCALATE", "REFUSE"
DECISIONS = (EXECUTE, ESCALATE, REFUSE, UNKNOWN)

# Q40: the kinds of shortfall AIOS tells apart. Each criterion names the class
# its failure belongs to; an UNKNOWN is classed by why the evidence is missing.
ERROR = "error"                      # a governed criterion is violated
LIMITATION = "limitation"            # a source exists but could not be read
KNOWLEDGE_GAP = "knowledge gap"      # a governed input is not admitted
CAPABILITY_GAP = "capability gap"    # nothing resident can produce the evidence
ARCHITECTURE_GAP = "architecture gap"  # the shortfall is at a frozen boundary
GAP_CLASSES = (ERROR, LIMITATION, KNOWLEDGE_GAP, CAPABILITY_GAP, ARCHITECTURE_GAP)


class P13Error(ValueError):
    """A P13 record that would break its own contract. Fail closed."""


def plain(value: Any) -> Any:
    """A JSON-native copy, so every record can be persisted and hashed."""
    return json.loads(json.dumps(value, default=str, sort_keys=True))


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(plain(value), sort_keys=True,
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Fact:
    """One observed fact: what, how sure, from where, and when."""

    key: str
    value: Any
    status: str
    source: str
    observed_at: str

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key.strip():
            raise P13Error("a fact needs a key")
        if self.status not in FACT_STATUSES:
            raise P13Error(f"{self.key}: {self.status!r} is not a fact status")
        if not isinstance(self.source, str) or not self.source.strip():
            raise P13Error(f"{self.key}: a fact without a source is not "
                           "evidence (E13-01)")
        object.__setattr__(self, "value", plain(self.value))


@dataclass(frozen=True)
class StateSnapshot:
    """What state AIOS is in, as far as this cycle can show (`D03` q1)."""

    facts: Tuple[Fact, ...]
    taken_at: str

    def __post_init__(self):
        keys = [f.key for f in self.facts]
        if len(keys) != len(set(keys)):
            raise P13Error("a snapshot holds each fact once")

    def get(self, key: str) -> Optional[Fact]:
        return next((f for f in self.facts if f.key == key), None)

    def keys(self) -> Tuple[str, ...]:
        return tuple(f.key for f in self.facts)

    @property
    def digest(self) -> str:
        """The state, without its timestamps. Equal digests mean no progress."""
        return digest([(f.key, f.value, f.status) for f in self.facts])

    def with_facts(self, extra: Tuple[Fact, ...], taken_at: str) -> "StateSnapshot":
        replaced = {f.key for f in extra}
        return StateSnapshot(tuple(f for f in self.facts if f.key not in replaced)
                             + tuple(extra), taken_at)


@dataclass(frozen=True)
class Citation:
    """Where a criterion's authority is recorded. Resolved, never assumed."""

    identifier: str
    instrument: str
    record: str


@dataclass(frozen=True)
class EvaluationResult:
    criterion: str
    result: str
    certainty: str          # VERIFIED, or INFERRED when any premise was
    evidence: Dict[str, Any]
    sources: Tuple[str, ...]
    authority: str
    gap_class: str
    reason: str
    requires: Tuple[str, ...] = ()

    def __post_init__(self):
        if self.result not in RESULTS:
            raise P13Error(f"{self.result!r} is not an evaluation result")

    @property
    def id(self) -> str:
        return f"eval:{self.criterion}"


@dataclass(frozen=True)
class Conclusion:
    """A conclusion names its rule and the premises it stands on (E13-03)."""

    id: str
    rule: str
    kind: str
    statement: str
    premises: Tuple[str, ...]
    certainty: str
    subject: str = ""
    gap_class: str = ""

    def __post_init__(self):
        if not self.premises:
            raise P13Error(f"{self.id}: no premise, no conclusion (E13-03)")
        if self.certainty not in FACT_STATUSES:
            raise P13Error(f"{self.id}: {self.certainty!r} is not a certainty")


@dataclass(frozen=True)
class ActionProposal:
    """What P13 thinks should happen. **Not a decision, and not authority.**

    There is no field here that could carry an authorization, and no method
    that turns a proposal into one. Only `AuthorityGate.decide` produces a
    `GateDecision`, and only from a recorded envelope.
    """

    id: str
    action_type: str
    target: str
    derived_from: Tuple[str, ...]
    rationale: str
    certainty: str
    priority: Tuple[int, str, str]
    origin: str = "next-action"      # or "evolution"

    def __post_init__(self):
        if not self.derived_from:
            raise P13Error(f"{self.id}: a proposal derives from a conclusion "
                           "(E13-04)")

    @property
    def subject(self) -> str:
        return f"P13 {self.action_type} {self.target}"


_GATE_TOKEN = object()


@dataclass(frozen=True)
class GateDecision:
    proposal: ActionProposal
    decision: str
    reason: str
    envelope: Optional[str] = None
    escalation_id: Optional[str] = None
    _token: Any = field(default=None, repr=False, compare=False)
    #: For EXECUTE: the targets the envelope authorizes for this action type.
    #: Empty means none were declared, which only a read-only type may run with.
    scope: Tuple[str, ...] = ()

    def __post_init__(self):
        if self._token is not _GATE_TOKEN:
            raise P13Error("only the AuthorityGate decides (G-08: P13 cannot "
                           "issue authority to itself)")
        if self.decision not in DECISIONS:
            raise P13Error(f"{self.decision!r} is not a gate decision")
        if self.decision == EXECUTE and not self.envelope:
            raise P13Error("EXECUTE names the envelope that permits it")

    def recorded(self) -> dict:
        return {"proposal": self.proposal.id, "action_type": self.proposal.action_type,
                "target": self.proposal.target, "decision": self.decision,
                "reason": self.reason, "envelope": self.envelope,
                "escalation_id": self.escalation_id, "scope": list(self.scope),
                "executes": self.decision == EXECUTE}


@dataclass(frozen=True)
class Outcome:
    """What an executed action did, and what the re-check showed."""

    proposal: str
    action_type: str
    envelope: str
    executor: str
    status: str             # success / failure (Domain Model §2.1)
    detail: str
    produced: Tuple[Fact, ...]


@dataclass(frozen=True)
class Gap:
    id: str
    gap_class: str
    statement: str
    derived_from: Tuple[str, ...]
    disposition: str


def recorded(value: Any) -> Any:
    """A dataclass (or tuple of them) as its persisted form."""
    if isinstance(value, tuple):
        return [recorded(v) for v in value]
    if hasattr(value, "recorded"):
        return value.recorded()
    if hasattr(value, "__dataclass_fields__"):
        return plain(asdict(value))
    return plain(value)
