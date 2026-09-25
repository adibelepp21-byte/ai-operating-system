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
7. it designates P13's live root and nothing else;
8. if it states an `expires` date, that date has not passed (EXPIRED);
9. its id is recorded once, in one JSON record and one Register entry
   (AMBIGUOUS otherwise).

A record that fails any check is an **anomaly**. It is not an envelope. It is
reported, and it escalates. P13 never repairs it, and never reads it as
partial authority.

One failure is not an anomaly: an envelope **retired** by a Founder decision.
Its REVOKED line in the Register names that decision, and the decision
resolves (`authority_citation.refusal` against its own act). An example is
`P13-ENV-02`, spent under `FDR-4` `FD-B`. A retired envelope is no authority,
exactly like an anomaly. It is reported as retired rather than as a defect,
because nothing about it needs a human's repair. A REVOKED line that names no
resolving decision is still an anomaly.

The gate applies Blueprint `§5.2` in order, then refuses what `§5.2` leaves
open. Every added check can only refuse, never permit (the post-construction
instruction, `§8.3`, Case C):

* a target outside the scope the envelope declares for that action type (a
  state-changing type with no declared targets has no scope at all);
* an action with no verification path (`§8.5`);
* a failing precondition;
* `§3.2`'s cycle bound, so a second EXECUTE in one cycle is REFUSED.

An ESCALATE, REFUSE or UNKNOWN never executes. ESCALATE is a refusal that is
also escalated.
ESCALATE is recorded through the existing `EscalationRegister.record` (item 5).
An identical escalation that is still OPEN is not raised again: nothing new
would reach the human.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tools import authority_citation
from tools.p13.catalog import READ_ONLY
from tools.p13.model import (ESCALATE, EXECUTE, REFUSE, UNKNOWN, ActionProposal,
                             GateDecision, _GATE_TOKEN)
from tools.p13.paths import LIVE_ROOT, Paths

AMBIGUOUS = "AMBIGUOUS"


def today() -> date:
    return datetime.now(timezone.utc).date()


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
    #: action type → the targets it may touch. A type absent here declares
    #: no target scope.
    targets: Tuple[Tuple[str, Tuple[str, ...]], ...] = ()

    def targets_for(self, action_type: str) -> Optional[Tuple[str, ...]]:
        return dict(self.targets).get(action_type)


def _section(register: str, envelope_id: str) -> Optional[str]:
    """The envelope's Register entry. Two entries for one id is AMBIGUOUS."""
    lines = register.splitlines()
    found = [i for i, line in enumerate(lines)
             if re.match(rf"### {re.escape(envelope_id)} —", line)]
    if len(found) != 1:
        return None if not found else AMBIGUOUS
    i = found[0]
    end = next((j for j in range(i + 1, len(lines))
                if lines[j].startswith(("### ", "## "))), len(lines))
    return "\n".join(lines[i:end])


def _act_text_sha(path: Path) -> Optional[str]:
    try:
        text = path.read_text(encoding="utf-8")
        body = text.split("````text\n", 1)[1].rsplit("\n````", 1)[0]
    except (OSError, IndexError):
        return None
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _retired_by(marked, paths: Paths) -> Optional[str]:
    """The Founder decision a REVOKED line names, if that decision resolves.

    Only REVOKED counts, never SUSPENDED. The decision must be an act under
    `docs/governance/acts/` that `authority_citation.refusal` resolves against
    the Decision Register. Anything less leaves the envelope an anomaly.
    """
    from tools.governance_index import IDENTIFIER_RE
    acts = paths.repo / "docs/governance/acts"
    for line in marked:
        if not re.search(r"\bREVOKED\b", line):
            continue
        for identifier in IDENTIFIER_RE.findall(line):
            record = next((p for p in sorted(acts.glob(f"{identifier}-*.md"))), None)
            if record is None:
                continue
            relative = record.relative_to(paths.repo).as_posix()
            if authority_citation.refusal(identifier, relative, identifier, paths.repo,
                                          paths.decision_register) is None:
                return identifier
    return None


def retired_envelopes(paths: Paths) -> Tuple[dict, ...]:
    """Envelopes a resolving Founder decision retired. None of them is authority."""
    try:
        register = paths.delegation_register.read_text(encoding="utf-8")
    except OSError:
        return ()
    out = []
    if paths.envelopes.is_dir():
        for path in sorted(paths.envelopes.glob("*.json")):
            try:
                envelope_id = json.loads(path.read_bytes())["envelope_id"]
            except (OSError, ValueError, KeyError, TypeError):
                continue
            whole = re.compile(r"(?<![\w-])" + re.escape(envelope_id) + r"(?![-\w])")
            marked = [l for l in register.splitlines()
                      if whole.search(l) and re.search(r"\b(REVOKED|SUSPENDED)\b", l)]
            by = _retired_by(marked, paths) if marked else None
            if by:
                out.append({"envelope": envelope_id, "retired_by": by})
    return tuple(out)


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
    if section is AMBIGUOUS:
        return None, f"{envelope_id}: recorded more than once in the Register (AMBIGUOUS)"
    status = next((l for l in section.splitlines() if l.startswith("| **Status** |")), "")
    if "**ACTIVE**" not in status:
        return None, f"{envelope_id}: its Register entry is not ACTIVE"
    whole = re.compile(r"(?<![\w-])" + re.escape(envelope_id) + r"(?![-\w])")
    marked = [l for l in register.splitlines()
              if whole.search(l) and re.search(r"\b(REVOKED|SUSPENDED)\b", l)]
    if marked:
        if _retired_by(marked, paths):
            return None, None            # retired: no authority, and no defect
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
    expires = record.get("expires")
    if expires is not None:
        try:
            expired = date.fromisoformat(str(expires)) < today()
        except ValueError:
            return None, f"{envelope_id}: its expiry {expires!r} is not a date (AMBIGUOUS)"
        if expired:
            return None, f"{envelope_id}: EXPIRED on {expires}"
    targets = []
    for action_type, grant in (record.get("action_types") or {}).items():
        if isinstance(grant, dict) and "targets" in grant:
            targets.append((action_type, tuple(grant["targets"])))
    return Envelope(
        id=envelope_id, issued_by=record["issued_by"], identifier=identifier,
        instrument=instrument, record=record["record"],
        action_types=tuple(sorted(record.get("action_types", {}))),
        cycle_basis=tuple(sorted(record.get("cycle_basis", {}))), sha256=sha,
        targets=tuple(sorted(targets))), None


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
            elif anomaly:                    # None: retired, which is no defect
                anomalies.append(anomaly)
    ids = [e.id for e in envelopes]
    for twice in sorted({i for i in ids if ids.count(i) > 1}):
        anomalies.append(f"{twice}: more than one record claims this id (AMBIGUOUS)")
        envelopes = [e for e in envelopes if e.id != twice]
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
        envelope = permitting[0]
        scope = envelope.targets_for(proposal.action_type)
        if scope is None and action.effect != READ_ONLY:
            return self._decision(proposal, REFUSE, f"{envelope.id} declares no target "
                                  f"scope for {proposal.action_type}")
        if scope is not None and not any(
                proposal.target == t or proposal.target.startswith(t.rstrip("/") + "/")
                for t in scope):
            return self._decision(proposal, REFUSE, f"wrong target: {proposal.target!r} "
                                  f"is outside {envelope.id}'s scope {list(scope)}")
        if action.run is None:
            return self._decision(proposal, REFUSE, "the action type declares no "
                                  "resident executor")
        if not action.verifiable:
            return self._decision(proposal, REFUSE, "no verification path: no "
                                  "execution (post-construction instruction §8.5)")
        if action.effect != READ_ONLY and not proposal.expected:
            return self._decision(proposal, REFUSE, "no expected consequence: a "
                                  "state change must say beforehand what it should "
                                  "bring about")
        for precondition in action.preconditions:
            unmet = precondition(self._paths, proposal.target)
            if unmet:
                return self._decision(proposal, REFUSE, f"missing precondition: {unmet}")
        if self.executed >= 1:
            return self._decision(proposal, REFUSE, "cycle bound: at most one "
                                  "executed action per cycle (Blueprint §3.2)")
        self.executed += 1
        return self._decision(proposal, EXECUTE,
                              f"permitted by {envelope.id} ({envelope.instrument})",
                              envelope.id, scope=scope or ())

    # -- recording ---------------------------------------------------------
    def _decision(self, proposal, decision, reason, envelope=None,
                  escalation_id=None, scope=()) -> GateDecision:
        return GateDecision(proposal, decision, reason, envelope, escalation_id,
                            _token=_GATE_TOKEN, scope=tuple(scope))

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


# ---------------------------------------------------------------------------
# FE-2: the authority dimensions, kept apart (post-construction instruction §5)
# ---------------------------------------------------------------------------

P13_018_ACT = "docs/governance/acts/P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md"


def _executable(action):
    """True, or why the gate could not execute this type at all."""
    if action is None:
        return "not in the ActionCatalog"
    if action.reserved or action.run is None:
        return "no executor"
    if not action.verifiable:
        return "no verification path"
    return True


def authority_dimensions(paths: Paths, catalog=None) -> Dict[str, dict]:
    """Five authority dimensions for P13, each read from its own source.

    Nothing here writes, and no dimension is derived from another. Above all,
    **construction authority is not phase authorization.** The phase value is
    the current state from `p12_phase_authorization`: the P12 decision `§37`
    snapshot, superseded only by a Register-resolving Founder authorization
    (`FDR-6` `FDQ-1`). P13-018 is never read as changing it, and phase
    authorization is never read as certification.
    """
    from tools import p12_certified_evidence_guard as guard
    from tools import p12_phase_authorization as phases
    from tools.p13.catalog import CATALOG, READ_ONLY as RO, RECORD
    catalog = catalog or CATALOG
    out: Dict[str, dict] = {}

    try:
        p13 = {s["entity"]: s for s in phases.current_states(paths.repo)}["P13"]
        out["phase_authorization"] = {
            "state": "AUTHORIZED" if p13["authorized"] else "NOT AUTHORIZED",
            "source": f"{p13['authority']}",
            "meaning": ("Master Program phase authorization. In P12's decision it is "
                        "the only state authorization produces (§25), and P13 stays "
                        "NOT AUTHORIZED until a separate valid Founder authorization "
                        "(§29). FDR-6 FDQ-1 is that authorization. It is not "
                        "certification, closure or Phase 14 authorization"),
            "verified": "VERIFIED"}
    except Exception as error:
        out["phase_authorization"] = {"state": "UNKNOWN", "source": str(error),
                                      "meaning": "", "verified": "UNKNOWN"}

    try:
        register = paths.decision_register.read_text(encoding="utf-8")
        sha = _act_text_sha(paths.repo / P13_018_ACT)
        registered = ("### P13-018 — Founder Decision" in register
                      and sha is not None and sha in register)
    except OSError:
        registered = False
    out["construction_authorization"] = {
        "state": "AUTHORIZED — bounded to Blueprint §10 IN" if registered else "UNKNOWN",
        "source": "Decision Register §22 · P13-018 D-1 (act hash matches the Register)",
        "meaning": ("permission to build the named scope. Distinct from phase "
                    "authorization (FDR-2 D10) and conferring no operational authority"),
        "verified": "VERIFIED" if registered else "UNKNOWN"}

    envelopes, anomalies = load_envelopes(paths)
    effects = {t: catalog[t].effect if t in catalog else "unknown"
               for e in envelopes for t in e.action_types}
    # A state-changing grant is projected with its envelope, instrument and
    # target scope, so the projection names exactly what may change and on
    # what authority (FDR-3 §5: "an unambiguous authority projection").
    grants = [{"action_type": t, "effect": effects[t], "envelope": e.id,
               "instrument": e.instrument, "targets": list(e.targets_for(t) or ()),
               "executable": _executable(catalog.get(t))}
              for e in envelopes for t in e.action_types
              if effects[t] not in (RO, RECORD)]
    bounded = bool(grants) and all(g["targets"] for g in grants)
    out["operational_envelope"] = {
        "state": ("NONE" if not envelopes else "EVIDENCE-ONLY" if not grants
                  else "EVIDENCE-ONLY + BOUNDED STATE-CHANGING" if bounded
                  else "MIXED"),
        "source": ", ".join(f"{e.id} ({e.instrument})" for e in envelopes)
                  or "no resolved envelope",
        "meaning": "what P13 may execute, from recorded envelopes only",
        "verified": "VERIFIED", "action_types": effects,
        "anomalies": list(anomalies),
        "retired": list(retired_envelopes(paths))}

    def shown(g):
        scope = ", ".join(g["targets"]) or "no target scope, so the gate refuses it"
        ready = "" if g["executable"] is True else f" [not executable: {g['executable']}]"
        return (f"{g['action_type']} → {scope} "
                f"({g['envelope']} · {g['instrument']}){ready}")
    out["state_changing_authority"] = {
        "state": ("NONE" if not grants else
                  ("BOUNDED: " if bounded else "GRANTED: ")
                  + "; ".join(shown(g) for g in sorted(grants, key=lambda g:
                                                       g["action_type"]))),
        "source": ("every action type a resolved envelope permits whose effect "
                   "class is not read-only or record, with that envelope's "
                   "declared targets"),
        "meaning": ("authority to change state beyond P13's own records. Required "
                    "for E13-05's full contract; only a governance decision grants it"),
        "verified": "VERIFIED", "grants": grants,
        "retired": list(retired_envelopes(paths))}

    try:
        certified = 13 in guard.certified_phases()
        out["certification_authority"] = {
            "state": "CERTIFIED" if certified else "NOT GRANTED",
            "source": "p12_certified_evidence_guard.certified_phases()",
            "meaning": "a Founder certification decision for P13 (Blueprint §11)",
            "verified": "VERIFIED"}
    except Exception as error:
        out["certification_authority"] = {"state": "UNKNOWN", "source": str(error),
                                          "meaning": "", "verified": "UNKNOWN"}
    return out

