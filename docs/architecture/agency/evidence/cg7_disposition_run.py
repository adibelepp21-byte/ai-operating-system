"""FD-CG7-001 execution: record the Founder's P12 dispositions outside the certified boundary.

Instrument: docs/governance/acts/FD-CG7-001-P12-OPERATIONAL-STATE-DISPOSITION-DECISION.md
(Register `§145`).

* FQ-CG7-2: the Founder's response to escalation ``9cb90fa0787a478c`` is
  **transcribed verbatim** from the instrument (its *Founder Response* block)
  into the response ledger, recorded under the Founder's identity, as B1 was.
  Then grant ``2494015de36246fd`` is dispositioned REVOKED (REVOKED / CLOSED).
* FQ-CG7-1: the nine historical proof-run grants are dispositioned REVOKED.

Nothing else. The two historical escalations get **no** response (the
instrument forbids fabricating one). No delegation record, escalation or other
certified byte is written: every write goes through the existing guarded ledger
functions, into ``docs/architecture/agency/operations/``. Refuses to run twice.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from native_core.core.governance import HumanAuthority  # noqa: E402
from tools import w4_delegation as w4  # noqa: E402
from tools.escalation_register import LIVE_RESPONSES, EscalationRegister  # noqa: E402

ROOT = REPO / "docs/architecture/p12/w4-operations"
ACT = REPO / w4.FD_CG7_RECORD
OUT = Path(__file__).with_name("CG7-DISPOSITION-RUN-2026-10-03.json")
FQ1 = ("FD-CG7-001 FQ-CG7-1", w4.FD_CG7_RECORD)
FQ2 = ("FD-CG7-001 FQ-CG7-2", w4.FD_CG7_RECORD)
ESCALATION = "9cb90fa0787a478c"
LIVE_GRANT = "2494015de36246fd"

#: What CG-7 established for each historical grant (`CG7-P12-OPERATIONAL-STATE-
#: RECONCILIATION-2026-10-03.md §B.1`), stated so the disposition does not
#: misrepresent its execution (FQ-CG7-1 constraint 4).
EXECUTION = {
    "e668a317fa494342": "bound execution performed: manifest p12-w4-integrated-execution-001, success 14/14",
    "b304c7ecb1024454": "bound execution performed: manifest p12-w4-integrated-execution-002, failure 5/14",
    "84e94ea2f001444d": "bound execution performed: manifest p12-w4-integrated-execution-003, failure 4/14",
    "08e14bd7aa584ea5": "bound execution performed: manifest p12-w4-integrated-execution-004, failure 3/14",
    "632b256f8335434f": "bound execution performed: manifest p12-w4-integrated-execution-005, failure 3/14",
    "332d42f021764ab6": "execution documented by commit and description only (P12 CLASS D); not joined by id",
    "522e84af52444890": "execution documented by description only (live-verification D.2); not joined by id",
    "aa591daf55ca4714": "plan run with its out-of-scope step refused (escalation 0991300404cf44d8, left OPEN / HISTORICAL)",
    "e6a3d622cfb54b4f": "plan run with its out-of-scope step refused (escalation 9d6bc0ad47294ef0, left OPEN / HISTORICAL)",
}


def founder_response() -> str:
    """The *Founder Response* block of FQ-CG7-2, verbatim from the instrument."""
    text = ACT.read_text(encoding="utf-8")
    block = re.search(r"Founder Response:\n(.*?)\nGrant Disposition:", text, re.S)
    if block is None:
        sys.exit("refusing: the instrument has no Founder Response block to transcribe")
    return block.group(1).strip()


def main() -> int:
    if w4._disposition_path(w4.LIVE_LEDGER, ROOT, LIVE_GRANT).exists():
        sys.exit("refusing: the FD-CG7-001 dispositions are already recorded (append-only)")
    act_sha = w4._sha256(ACT)
    register = EscalationRegister(ROOT, response_ledger=LIVE_RESPONSES)
    response = founder_response()
    response_path = register.record_response(
        ESCALATION, authority=HumanAuthority("Moriarty (Founder)"), response=response,
        basis=f"{w4.FD_CG7_RECORD} (file sha256 {act_sha}), FQ-CG7-2 = A, Register §145; "
              "recorded by Claude Code / AIOS Co-Founder as a transcription of the Founder's decision")
    written = {"response": str(response_path.relative_to(REPO)), "dispositions": {}}
    written["dispositions"][LIVE_GRANT] = str(w4.record_disposition(
        ROOT, LIVE_GRANT, disposition=w4.REVOKED, delegator=w4.AUTHORIZED_DELEGATOR,
        authority=FQ2,
        reason=("REVOKED / CLOSED — proof-run grant not continued (Founder FQ-CG7-2 = A, "
                f"{w4.FD_CG7_RECORD}, Register §145). Work scope verify-delegation-elements "
                "succeeded 14/14 (first-execution.evidence.json); plan step report-conformance "
                f"was outside scope, escalated as {ESCALATION}, and closed by the Founder without "
                "execution, new authority or scope expansion. Not represented as COMPLETED."),
    ).relative_to(REPO))
    for gid, fact in EXECUTION.items():
        written["dispositions"][gid] = str(w4.record_disposition(
            ROOT, gid, disposition=w4.REVOKED, delegator=w4.AUTHORIZED_DELEGATOR,
            authority=FQ1,
            reason=("REVOKED / CLOSED — historical P12 proof-run grant (Founder FQ-CG7-1 = B, "
                    f"{w4.FD_CG7_RECORD}, Register §145); {fact}. Its recipient was registered "
                    "in-process only and no current execution path exists. Certified evidence "
                    "unchanged; not represented as COMPLETED."),
        ).relative_to(REPO))
    result = {"recorded_at": datetime.now(timezone.utc).isoformat(),
              "instrument": w4.FD_CG7_RECORD, "instrument_file_sha256": act_sha,
              "founder_response_transcribed": response, **written,
              "not_answered": ["0991300404cf44d8", "9d6bc0ad47294ef0"]}
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
