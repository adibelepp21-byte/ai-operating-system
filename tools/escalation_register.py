"""`P11` escalation persistence — durable, append-only, and never an approval.

Authorized by `DP-01 §3 W1`, which lists *"escalation"* among the coordination
capabilities construction may implement. Built under `ACT-CC-P11-007 §13`, which
requires escalation persistence *if* it is *"an authorized and materially
required P11 capability."*

**It is both, and the classification was made rather than assumed.**

*Authorized* — `DP-01 §3 W1` names it. *Materially required* — `DP-01 §3 W4`'s
autonomous loop terminates in `CONTINUE / ESCALATE`, so an autonomous
organization reaching an authority boundary must leave a durable record of
having done so. `§13`: *"Escalation must not disappear merely because execution
reaches an error or boundary."* Today `EscalationRequired` is raised and lost the
moment the process ends.

**Why not Trace, which already ratifies `escalation` as an outcome.**
`native_core/core/trace/record.py` fixes
``VALID_STATUSES = {"success", "failure", "escalation"}`` per Domain Model
`§2.1`, so the obvious question is whether this duplicates a sanctioned surface.
It does not. `TraceRecord` requires `agent_definition_version`, `agent_instance`
and `runtime` — **it records what an agent instance actually did.** A planning
escalation has no instance and no runtime; it happens *before* execution, at the
authority boundary. Writing one into Trace would mean inventing an agent
instance and a runtime, which is the same fabrication
`tools/tests/test_plan_to_workflow_gate.py` forbids, and would additionally make
the organizational layer write into a frozen core boundary.

So: Trace remains the sanctioned surface for **execution** escalations, and this
register holds **organizational** ones. Neither replaces the other.

**`ESCALATION ≠ APPROVAL`** (`§14`). This is the property the whole module is
shaped around:

* an escalation is recorded as `OPEN`, and **nothing in this module can close
  one**;
* closing requires `record_response`, which demands a `HumanAuthority` — the
  frozen governance type that fails closed on an absent reviewer identity, and
  that **automation cannot synthesise** (Constitution `§6.2` invariant 2);
* a recorded response is *a record that a human answered*, **not a grant**. There
  is no method here that returns whether anything is permitted;
* records are **append-only**. A response is written as a new file beside the
  escalation, never over it, so the original claim survives its own answer.

**Direction of dependency.** This module imports Planning; Planning does not
import it. A caller — today a test, tomorrow the W4 loop — catches
`EscalationRequired` and records it. Planning therefore stays unaware that
persistence exists, which is what keeps its negative controls true.

**No default resident directory.** The root is a required argument. Choosing a
canonical on-disk home for runtime escalation records is a deployment decision
this Act does not grant (`§33`), and inventing one would put a directory in the
repository that nothing legitimately writes to yet. Durability is proven across a
real process boundary in the tests instead of implied by a folder.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

from native_core.core.governance import HumanAuthority
from tools.planning import AuthorityProvenance, EscalationRequired

REPO_ROOT = Path(__file__).resolve().parent.parent


class EscalationRegisterError(RuntimeError):
    """Fail closed (`PR-4`)."""


@dataclass(frozen=True)
class EscalationRecord:
    """One escalation, exactly as it was raised.

    Frozen, and written once. `§13` requires identity, authority provenance,
    reason/context, lifecycle and linkage to be preserved; `§16` of the previous
    Act established why immutability is how preservation is guaranteed rather
    than promised — there is no operation that edits a past record.

    ``status`` is derived, never stored as a mutable field: a record is `OPEN`
    unless a response file exists beside it. **A flag that could be set to
    "approved" is precisely what `§14` forbids**, so there is none.
    """

    escalation_id: str
    subject: str
    required: str
    held: str
    reason: str
    authority: AuthorityProvenance
    raised_at: str

    def to_payload(self) -> dict:
        return {
            "escalation_id": self.escalation_id,
            "subject": self.subject,
            "required": self.required,
            "held": self.held,
            "reason": self.reason,
            "authority_instrument": self.authority.instrument,
            "authority_record": self.authority.record,
            "raised_at": self.raised_at,
        }


class EscalationRegister:
    """Durable, append-only escalations. Holds no authority of its own."""

    def __init__(self, root: Path):
        if not isinstance(root, Path):
            raise EscalationRegisterError("the register requires an explicit root")
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

    def record(self, error: EscalationRequired, *, subject: str,
               authority: AuthorityProvenance) -> EscalationRecord:
        """Persist an escalation that was actually raised.

        Takes the raised exception rather than free text so the recorded
        ``required``/``held`` pair is **the one the refusal was made on**. Letting
        a caller supply those separately would allow a record that disagrees with
        the event it claims to describe.
        """
        if not isinstance(error, EscalationRequired):
            raise EscalationRegisterError(
                "only an escalation that was actually raised may be recorded — "
                "a register that accepts invented entries is not evidence")
        if not isinstance(authority, AuthorityProvenance):
            raise EscalationRegisterError(
                "an escalation records the authority it was bounded by, as a "
                "validated citation")
        record = EscalationRecord(
            escalation_id=uuid.uuid4().hex[:16],
            subject=subject,
            required=error.required,
            held=error.held,
            reason=str(error),
            authority=authority,
            raised_at=datetime.now(timezone.utc).isoformat(),
        )
        path = self._root / f"{record.escalation_id}.escalation.json"
        if path.exists():                                   # pragma: no cover
            raise EscalationRegisterError(f"refusing to overwrite {path.name}")
        path.write_text(json.dumps(record.to_payload(), indent=2),
                        encoding="utf-8")
        return record

    def record_response(self, escalation_id: str, *, authority: HumanAuthority,
                        response: str) -> Path:
        """Record that a **human** answered. Not a grant of anything.

        `HumanAuthority` is the frozen governance boundary: *"a governed decision
        requires an explicit human authority"*, and it fails closed on an absent
        reviewer identity. Requiring one here means **automation cannot close an
        escalation**, because it cannot construct the thing the closure needs.

        The response is a **new file beside the escalation**, never over it. The
        original claim survives its own answer, so a reader can always see what
        was escalated as well as what came back.

        What this does **not** do: authorize anything. `§14` — the valid path is
        `BLOCK → ESCALATION → LEGITIMATE AUTHORITY RESPONSE`, and a response
        recorded here is evidence that the third step happened, not the step
        itself. Whatever the human authorized is recorded by governance, in the
        instruments governance issues.
        """
        if not isinstance(authority, HumanAuthority):
            raise EscalationRegisterError(
                "closing an escalation requires a human authority — automation "
                "may request and recommend, never decide "
                "(Constitution §6.2 invariant 2)")
        if not (self._root / f"{escalation_id}.escalation.json").is_file():
            raise EscalationRegisterError(f"no such escalation: {escalation_id}")
        path = self._root / f"{escalation_id}.response.json"
        if path.exists():
            raise EscalationRegisterError(
                f"escalation {escalation_id} already has a response; append-only")
        path.write_text(json.dumps({
            "escalation_id": escalation_id,
            "responded_by": authority.reviewer_id,
            "response": response,
            "responded_at": datetime.now(timezone.utc).isoformat(),
        }, indent=2), encoding="utf-8")
        return path

    # ---- reading ----------------------------------------------------------
    def open_escalations(self) -> Tuple[str, ...]:
        """Ids with no recorded response. Derived from the files present."""
        return tuple(sorted(
            p.name.split(".")[0] for p in self._root.glob("*.escalation.json")
            if not (self._root / f"{p.name.split('.')[0]}.response.json").is_file()))

    def all_escalations(self) -> Tuple[str, ...]:
        return tuple(sorted(p.name.split(".")[0]
                            for p in self._root.glob("*.escalation.json")))

    def status(self, escalation_id: str) -> str:
        """`OPEN` or `ANSWERED`. **Never `APPROVED`** — `§14`.

        `ANSWERED` says a human responded. It does not say what they decided, and
        no caller can read permission out of it.
        """
        if not (self._root / f"{escalation_id}.escalation.json").is_file():
            raise EscalationRegisterError(f"no such escalation: {escalation_id}")
        answered = (self._root / f"{escalation_id}.response.json").is_file()
        return "ANSWERED" if answered else "OPEN"

    def load(self, escalation_id: str) -> dict:
        path = self._root / f"{escalation_id}.escalation.json"
        if not path.is_file():
            raise EscalationRegisterError(f"no such escalation: {escalation_id}")
        return json.loads(path.read_text(encoding="utf-8"))
