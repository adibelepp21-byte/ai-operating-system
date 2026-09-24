"""`AuthorityGate` — AM I AUTHORIZED TO ACT? (E13-05; `D05`; Blueprint `§5`).

`NO RECORDED AUTHORITY → NO EXECUTION` (`P13-018 §3`). An envelope is an
authority only when **all** of these hold, and each one is re-checked on every
cycle:

1. its JSON record is under `docs/governance/p13-envelopes/` and names an id;
2. the Delegation Register has a `### <id> —` entry whose status is **ACTIVE**,
   and no line in the Register marks the id REVOKED or SUSPENDED;
3. that entry holds the sha256 of the JSON **as it is now**, so a tampered record
   is not the recorded one;
4. the instrument it cites resolves (`tools/authority_citation.refusal`): the
   act exists under `docs/governance/acts/`, and its identifier is in the
   Decision Register as a whole token;
5. the act's fenced Founder text still hashes to the sha256 the envelope records;
6. it was issued by the Founder. No other issuer is recognized yet, so a
   CEO-issued envelope is an anomaly, not an authority (`G-08`, `R06`);
7. it designates P13's live root and nothing else.

A record that fails any check is an **anomaly**. It is not an envelope. It is
reported, and it escalates. P13 never repairs it, and never reads it as
partial authority.

The gate applies Blueprint `§5.2` in order. The one addition is `§3.2`'s cycle
bound: a second EXECUTE in one cycle is REFUSED (E13-05's negative control).
ESCALATE is recorded through the existing `EscalationRegister.record` (item 5).
An identical escalation that is still OPEN is not raised again: nothing new
would reach the human.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tools import authority_citation
from tools.p13.model import (ESCALATE, EXECUTE, REFUSE, UNKNOWN, ActionProposal,
                             GateDecision, _GATE_TOKEN)
from tools.p13.paths import LIVE_ROOT, Paths

FDR2_ACT = "docs/governance/acts/FDR-2-P13-DEFINITION-BOUNDARY-AUTONOMY-AND-EXIT-CONTRACT.md"


@dataclass(frozen=True)
class Envelope:
    id: str
    issued_by: str
    identifier: str
    instrument: str
    record: str
    action_types: Tuple[str, ...]
    cycle_basis: Tuple[str, ...]
    sha256: str


def _section(register: str, envelope_id: str) -> Optional[str]:
    lines = register.splitlines()
    for i, line in enumerate(lines):
        if re.match(rf"### {re.escape(envelope_id)} —", line):
            end = next((j for j in range(i + 1, len(lines))
                        if lines[j].startswith(("### ", "## "))), len(lines))
            return "\n".join(lines[i:end])
    return None


def _act_text_sha(path: Path) -> Optional[str]:
    try:
        text = path.read_text(encoding="utf-8")
        body = text.split("````text\n", 1)[1].rsplit("\n````", 1)[0]
    except (OSError, IndexError):
        return None
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _validate(path: Path, paths: Paths, register: str) -> Tuple[Optional[Envelope], Optional[str]]:
    name = path.name
    try:
        raw = path.read_bytes()
        record = json.loads(raw)
        envelope_id = record["envelope_id"]
    except (OSError, ValueError, KeyError, TypeError) as error:
        return None, f"{name}: unreadable envelope record ({error})"
    sha = hashlib.sha256(raw).hexdigest()
    section = _section(register, envelope_id)
    if section is None:
        return None, f"{envelope_id}: not recorded in the Delegation Register"
    status = next((l for l in section.splitlines() if l.startswith("| **Status** |")), "")
    if "**ACTIVE**" not in status:
        return None, f"{envelope_id}: its Register entry is not ACTIVE"
    whole = re.compile(r"(?<![\w-])" + re.escape(envelope_id) + r"(?![-\w])")
    if any(whole.search(l) and re.search(r"\b(REVOKED|SUSPENDED)\b", l)
           for l in register.splitlines()):
        return None, f"{envelope_id}: the Register marks it revoked or suspended"
    if sha not in section:
        return None, (f"{envelope_id}: the record's sha256 {sha[:16]}… is not the "
                      "one the Register fixes (tampered or unrecorded)")
    instrument = str(record.get("instrument", ""))
    identifier = instrument.split(" ")[0] if instrument else ""
    refused = authority_citation.refusal(instrument, str(record.get("record", "")),
                                         identifier, paths.repo,
                                         paths.decision_register)
    if refused:
        return None, f"{envelope_id}: {refused}"
    if _act_text_sha(paths.repo / record["record"]) != record.get("decision_content_sha256"):
        return None, (f"{envelope_id}: the cited act's Founder text no longer "
                      "hashes to the recorded decision")
    if not str(record.get("issued_by", "")).startswith("Founder"):
        return None, (f"{envelope_id}: issued by {record.get('issued_by')!r}; only a "
                      "Founder-issued envelope is recognized")
    if record.get("designated_live_root") != LIVE_ROOT:
        return None, f"{envelope_id}: it does not designate {LIVE_ROOT}"
    return Envelope(
        id=envelope_id, issued_by=record["issued_by"], identifier=identifier,
        instrument=instrument, record=record["record"],
        action_types=tuple(sorted(record.get("action_types", {}))),
        cycle_basis=tuple(sorted(record.get("cycle_basis", {}))), sha256=sha), None


def load_envelopes(paths: Paths) -> Tuple[Tuple[Envelope, ...], Tuple[str, ...]]:
    """Every valid envelope, and every record that failed to be one."""
    try:
        register = paths.delegation_register.read_text(encoding="utf-8")
    except OSError as error:
        return (), (f"Delegation Register unreadable ({error}); no envelope "
                    "can resolve",)
    envelopes: List[Envelope] = []
    anomalies: List[str] = []
    if paths.envelopes.is_dir():
        for path in sorted(paths.envelopes.glob("*.json")):
            envelope, anomaly = _validate(path, paths, register)
            if envelope:
                envelopes.append(envelope)
            else:
                anomalies.append(anomaly)
    return tuple(envelopes), tuple(anomalies)


class AuthorityGate:
    def __init__(self, paths: Paths, catalog, envelopes: Tuple[Envelope, ...]):
        self._paths = paths
        self._catalog = catalog
        self._envelopes = envelopes
        self.executed = 0

    # -- the §5.2 table ----------------------------------------------------
    def decide(self, proposal) -> GateDecision:
        if type(proposal) is not ActionProposal:
            return self._refuse_foreign(proposal)
        action = self._catalog.get(proposal.action_type)
        if action is None:
            return self._decision(proposal, REFUSE, "unknown action type: not "
                                  "in the ActionCatalog")
        if action.reserved:
            return self._escalate(
                proposal, f"reserved action type {proposal.action_type!r}: never "
                "executable by P13; Founder/CEO authority required",
                required=f"Founder/CEO authority for {proposal.action_type}")
        if proposal.certainty == UNKNOWN:
            return self._decision(proposal, UNKNOWN, "the proposal rests on an "
                                  "UNKNOWN premise; discover before acting (D05)")
        permitting = [e for e in self._envelopes
                      if proposal.action_type in e.action_types]
        if not permitting:
            return self._escalate(
                proposal, "no recorded envelope permits this action type",
                required=f"a recorded envelope permitting {proposal.action_type}")
        if len(permitting) > 1:
            return self._escalate(
                proposal, "envelopes conflict: "
                + ", ".join(e.id for e in permitting),
                required="one governing envelope")
        if action.run is None:
            return self._decision(proposal, REFUSE, "the action type declares no "
                                  "resident executor")
        if self.executed >= 1:
            return self._decision(proposal, REFUSE, "cycle bound: at most one "
                                  "executed action per cycle (Blueprint §3.2)")
        self.executed += 1
        return self._decision(proposal, EXECUTE,
                              f"permitted by {permitting[0].id} "
                              f"({permitting[0].instrument})", permitting[0].id)

    # -- recording ---------------------------------------------------------
    def _decision(self, proposal, decision, reason, envelope=None,
                  escalation_id=None) -> GateDecision:
        return GateDecision(proposal, decision, reason, envelope, escalation_id,
                            _token=_GATE_TOKEN)

    def _refuse_foreign(self, thing) -> GateDecision:
        stand_in = ActionProposal(
            id="foreign", action_type="<not a proposal>",
            target=type(thing).__name__, derived_from=("<none>",),
            rationale="presented to the gate as something other than a proposal",
            certainty=UNKNOWN, priority=(9, "", ""))
        return self._decision(stand_in, REFUSE, "only an ActionProposal can be "
                              "decided; a recommendation presented as a decision "
                              "is refused (E13-04)")

    def _escalate(self, proposal, reason, *, required) -> GateDecision:
        escalation_id = raise_escalation(self._paths, self._envelopes,
                                         proposal.subject, reason,
                                         required=required)
        return self._decision(proposal, ESCALATE, reason,
                              escalation_id=escalation_id)


def raise_escalation(paths: Paths, envelopes, subject: str, reason: str, *,
                     required: str) -> str:
    """Record through the existing register, once while it stays OPEN."""
    from tools.escalation_register import EscalationRegister
    from tools.planning import AuthorityProvenance, EscalationRequired
    root = paths.escalations
    if root.is_dir():
        for record in sorted(root.glob("*.escalation.json")):
            escalation_id = record.name.split(".")[0]
            if (root / f"{escalation_id}.response.json").is_file():
                continue
            try:
                if json.loads(record.read_text(encoding="utf-8"))["subject"] == subject:
                    return escalation_id
            except (OSError, ValueError, KeyError):
                continue
    basis = next((e for e in envelopes if "escalate" in e.action_types), None)
    authority = (AuthorityProvenance(f"{basis.instrument} ({basis.id}) item 5",
                                     basis.record) if basis else
                 # G-02: missing authority results in escalation. With no
                 # envelope, the escalation stands on FDR-2 D05 alone.
                 AuthorityProvenance("FDR-2 D05", FDR2_ACT))
    held = (", ".join(sorted({t for e in envelopes for t in e.action_types}))
            or "no resolved envelope")
    error = EscalationRequired(reason, required=required, held=held)
    return EscalationRegister(root).record(error, subject=subject,
                                           authority=authority).escalation_id
