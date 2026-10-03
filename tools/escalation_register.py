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
from tools.w4_execution import ExecutionRefused

#: The refusal types that may become a persisted organizational escalation.
#:
#: Both carry ``required`` and ``held`` — what the blocked action needed against
#: what the actor held — which is the pair an escalation must put in front of a
#: human. `EscalationRequired` arises when a *plan* would exceed its authority;
#: `ExecutionRefused` when a *step* would exceed its delegation.
#:
#: Listed explicitly rather than accepted by duck-typing. `ACT-CC-P11-009 §13`
#: separates **refusal** from **organizational escalation**, and a register that
#: accepted anything shaped like a refusal would let an arbitrary object become
#: organizational state — which is the fabrication the type check exists to stop.
SANCTIONED_REFUSALS = (EscalationRequired, ExecutionRefused)

REPO_ROOT = Path(__file__).resolve().parent.parent

#: Where a response goes when the escalation itself is certified evidence
#: (`FD-AGENCY-001` S-1, B1; the same pattern as the S-1 A2 delegation ledger,
#: `docs/architecture/agency/W4-OPERATIONAL-LEDGER.md`). A response to an
#: escalation in a certified root is never written beside it: the certified
#: bytes stay frozen, and the answer is recorded here, bound to them by hash.
#: Escalations in uncertified roots are answered beside themselves, unchanged.
LIVE_RESPONSES = REPO_ROOT / "docs/architecture/agency/operations/escalation-responses"


class EscalationRegisterError(RuntimeError):
    """Fail closed (`PR-4`)."""


def _sha256(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def record_refusals(root: Path, refusals, *, subject: str,
                    authority: "AuthorityProvenance") -> Tuple[str, ...]:
    """Give every refusal an organizational home. Returns the ids recorded.

    **The single wiring path from a refusal to organizational state.**
    `ACT-CC-P11-009 §13` established the distinction this implements: a refusal
    satisfies only `ACTION BLOCKED` and *"does not prove an escalation state"* —
    an `ExecutionOutcome` inside a run's evidence file is transient to that run,
    with no lifecycle, no accountable party and no way to resolve.

    That fix was applied to the W4 path and **not to W1**, which was written
    afterwards and carried the older shape: `tools/w1_coordination_run.py`
    constructed no register at all, so a coordination refusal would have existed
    only as a string in one evidence file. `ACT-CC-P11-014` found it and this
    function is the repair — the **existing** mechanism, connected to both
    canonical execution paths instead of one.

    **It adds no idempotency, and that is deliberate.** `ACT-CC-P11-014`
    falsified the same-subject uniqueness hypothesis: the ratified Domain Model
    `§10` lists *Escalation / Incident* among deferred concepts — *"Not canonical
    entities in v1.0"* — and `DP-04 §7` fixes that *"Escalation is represented as
    a ratified Trace status rather than an independent organizational entity."*
    Trace's semantics are `§7` invariant 4, *"production is unconditional, never
    optional"*, and invariant 5, append-only. There is no canonical escalation
    identity to deduplicate on, and suppressing a second raised refusal would
    risk `DP-01` `NC-10`: *"Escalation must not be silently converted into
    success."*

    So each refusal that is actually raised is recorded. Two identical refusals
    are two occurrences, and the record says so.
    """
    if root is None:
        return ()
    recorded = []
    register = EscalationRegister(root)
    for refusal in refusals:
        recorded.append(register.record(refusal, subject=subject,
                                        authority=authority).escalation_id)
    return tuple(recorded)


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

    ``refusal_type`` names **which** refusal occurred. `§33` requires failure
    behaviour to distinguish `REFUSED`, and until this field existed both
    `EscalationRequired` (a *plan* exceeding its authority) and
    `ExecutionRefused` (a *step* exceeding its delegation) persisted into a
    byte-indistinguishable shape: the distinction was drawn in flight, by the
    exception type, and lost at rest. `§34` requires provenance to identify the
    `result`; a preserved result that cannot say which refusal it was is
    under-identified.

    **It does not distinguish `BLOCKED` from `ESCALATED`, and is not claimed
    to.** Every persisted refusal is *in the register*, so at rest it is
    escalated; a block that is not escalated is not persisted at all. Reading
    `EscalationRequired` as `§33`'s `BLOCKED` would be a semantic decision `§33`
    does not make about a term it does not define —
    `P12-027-SECTION-6-7-FRONTIER-DETERMINATION.md §3` records why it was
    available and not taken.

    Like ``required`` and ``held`` it is **derived from the raised exception,
    never supplied by a caller** — `record` takes ``type(error).__name__`` and
    ``__post_init__`` refuses any name outside `SANCTIONED_REFUSALS`, so a
    record cannot claim a refusal nothing can raise. It adds no state, no
    lifecycle and no flag anything can read permission out of.

    **Three prior packages declined to add this field on workstream-scope
    grounds** (`P12-W4 §13`: *"`W4 ≠ W3`"*; `P12-W2 §11`; `P12-005`), and
    `P12-W3` closed the joinable part *beside* the record instead.
    `ACT-CC-P12-027 §4` removes the partition those declines rested on. The
    record is not certified evidence: `p12_certified_evidence_guard.is_protected`
    returns `False` for this module, whose protected roots are the certified
    phase evidence and the platform-organization corpus — and the
    `NATIVE CORE = 11` freeze does not reach `tools/`.
    **Existing records are not rewritten**; they keep the shape they were
    written in, and `escalation_join()` still reports `0` of them naming a type.
    """

    escalation_id: str
    subject: str
    required: str
    held: str
    reason: str
    refusal_type: str
    authority: AuthorityProvenance
    raised_at: str

    def __post_init__(self):
        if self.refusal_type not in {t.__name__ for t in SANCTIONED_REFUSALS}:
            raise EscalationRegisterError(
                f"{self.refusal_type!r} is not a sanctioned refusal type — a "
                "record that names a refusal nothing can raise is not evidence")

    def to_payload(self) -> dict:
        return {
            "escalation_id": self.escalation_id,
            "subject": self.subject,
            "required": self.required,
            "held": self.held,
            "reason": self.reason,
            "refusal_type": self.refusal_type,
            "authority_instrument": self.authority.instrument,
            "authority_record": self.authority.record,
            "raised_at": self.raised_at,
        }


class EscalationRegister:
    """Durable, append-only escalations. Holds no authority of its own."""

    def __init__(self, root: Path, response_ledger: Optional[Path] = None):
        """``response_ledger`` is opt-in. Without it the register reads and
        writes exactly as before; with it, responses recorded outside a
        certified root are honoured (and are where such responses are written).
        """
        if not isinstance(root, Path):
            raise EscalationRegisterError("the register requires an explicit root")
        self._root = root
        self._responses = None if response_ledger is None else Path(response_ledger)
        self._root.mkdir(parents=True, exist_ok=True)

    def _external_response(self, escalation_id: str) -> Optional[Path]:
        """Where this root's response is filed: its full-path identity (R-1)."""
        if self._responses is None:
            return None
        from tools.w4_delegation import ledger_folder
        return ledger_folder(self._responses, self._root) / f"{escalation_id}.response.json"

    def _legacy_response(self, escalation_id: str) -> Optional[Path]:
        """A response filed under the pre-R-1 basename folder, if it differs."""
        if self._responses is None:
            return None
        from tools.w4_delegation import legacy_ledger_folder
        folder = legacy_ledger_folder(self._responses, self._root)
        return None if folder is None else folder / f"{escalation_id}.response.json"

    def _answered(self, escalation_id: str) -> bool:
        """A response beside the escalation, or a **valid** one in the ledger.

        An external response is honoured only if it names this escalation and
        this root, the ledger is not itself certified evidence, and the
        escalation's bytes are still the ones it answered.
        """
        if (self._root / f"{escalation_id}.response.json").is_file():
            return True
        return any(self._valid_external(path, escalation_id)
                   for path in (self._external_response(escalation_id),
                                self._legacy_response(escalation_id)))

    def _valid_external(self, external: Optional[Path], escalation_id: str) -> bool:
        """An external response is this root's only if it records this root (R-1)."""
        if external is None or not external.is_file():
            return False
        from tools.p12_certified_evidence_guard import is_protected
        if is_protected(external):
            return False
        try:
            item = json.loads(external.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return False
        source = self._root / f"{escalation_id}.escalation.json"
        return (item.get("escalation_id") == escalation_id
                and item.get("root") == _rel(self._root)
                and source.is_file()
                and item.get("escalation_record_sha256") == _sha256(source))

    def record(self, error, *, subject: str,
               authority: AuthorityProvenance) -> EscalationRecord:
        """Persist an escalation that was actually raised.

        Takes the raised exception rather than free text so the recorded
        ``required``/``held`` pair is **the one the refusal was made on**. Letting
        a caller supply those separately would allow a record that disagrees with
        the event it claims to describe.
        """
        if not isinstance(error, SANCTIONED_REFUSALS):
            raise EscalationRegisterError(
                "only a refusal that was actually raised may be recorded — "
                "a register that accepts invented entries is not evidence")
        if not isinstance(authority, AuthorityProvenance):
            raise EscalationRegisterError(
                "an escalation records the authority it was bounded by, as a "
                "validated citation")
        record = EscalationRecord(
            escalation_id=uuid.uuid4().hex[:16],
            subject=subject,
            required=str(error.required),
            held=str(error.held),
            reason=str(error),
            refusal_type=type(error).__name__,
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
                        response: str, basis: Optional[str] = None) -> Path:
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
        source = self._root / f"{escalation_id}.escalation.json"
        if not source.is_file():
            raise EscalationRegisterError(f"no such escalation: {escalation_id}")
        from tools.p12_certified_evidence_guard import guard, is_protected
        beside = self._root / f"{escalation_id}.response.json"
        if self._answered(escalation_id):
            raise EscalationRegisterError(
                f"escalation {escalation_id} already has a response; append-only")
        payload = {
            "escalation_id": escalation_id,
            "responded_by": authority.reviewer_id,
            "response": response,
            "responded_at": datetime.now(timezone.utc).isoformat(),
        }
        if not is_protected(beside):
            # Uncertified root: answered beside itself, as it always was.
            if basis is not None:
                payload["basis"] = basis
            beside.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            return beside
        # Certified root (F-S1-4): never beside the escalation. Routed to the
        # live ledger, bound to the escalation's exact bytes, guarded.
        path = self._external_response(escalation_id)
        if path is None:
            raise EscalationRegisterError(
                f"{source} is certified evidence: its response must be recorded "
                "in a response ledger outside the certified boundary")
        guard(path)                     # before any directory is created
        if path.exists():
            raise EscalationRegisterError(
                f"escalation {escalation_id} already has a response; append-only")
        path.parent.mkdir(parents=True, exist_ok=True)
        payload.update({"root": _rel(self._root),
                        "escalation_record_sha256": _sha256(source),
                        "basis": basis})
        guard(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    # ---- reading ----------------------------------------------------------
    def open_escalations(self) -> Tuple[str, ...]:
        """Ids with no recorded response. Derived from the files present."""
        return tuple(sorted(
            p.name.split(".")[0] for p in self._root.glob("*.escalation.json")
            if not self._answered(p.name.split(".")[0])))

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
        return "ANSWERED" if self._answered(escalation_id) else "OPEN"

    def load(self, escalation_id: str) -> dict:
        path = self._root / f"{escalation_id}.escalation.json"
        if not path.is_file():
            raise EscalationRegisterError(f"no such escalation: {escalation_id}")
        return json.loads(path.read_text(encoding="utf-8"))
