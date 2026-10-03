# FD-FR1-001 — P13 Consumer Registration & P12-W2 Integration Authorization (as received)

**Received:** from the Founder (Moriarty), 2026-10-03, in the message body; extracted byte-exactly from the session transcript. Answers FQ-FR1-1 (Register `§158`). Registered at Register `§159`; FR-1 completion at `§160`.

````text
AIOS FOUNDER DECISION RECORD

FD-FR1-001 — P13 Consumer Registration & P12-W2 Integration Authorization

Document Type: Founder Decision Record
Question: FQ-FR1-1
Predecessor: FR-1 — Live Ledger → P12-W2 → P13
Related Decision: FD-TD-001
Founder: Moriarty
Status: APPROVED
Founder Authorization: YES

⸻

1. Decision

The Founder selects:

OPTION A — Authorize P13 as an observed consumer of P12-W2 under the existing certified P12 consumer-evidence model.

P13 may be wired to consume:

tools.p12_operational_state.project()

through the already-defined P12-W2 integration boundary.

This authorization follows the existing precedent established by ACT-CC-P12-019 for registration of a new P12 consumer.

⸻

2. Decision Boundary

This authorization is limited to:

1. registering P13 as an observed consumer in the existing P12 consumer-evidence harness;
2. updating the corresponding pinned consumer tests;
3. updating the existing STATE consumer classification;
4. wiring P13 to the already-certified P12-W2 interface;
5. verifying that the independent consumer measurement recognizes the new consumer;
6. preserving the existing P12-W2 ownership, semantics, source model and authority boundary.

This is an authorization to reconcile an already-defined consumer relationship.

It is NOT authorization to redesign P12-W2 or P13.

⸻

3. Authority and Architecture Preservation

The following remain unchanged:

* P12-W2 remains the system-wide integration layer.
* The live operational ledger remains the authoritative owner of current delegation lifecycle state.
* P13 remains a consumer of P12-W2.
* P12-W2 does not become the owner of domain-specific operational state.
* P13 does not become a state authority.
* No second system-wide current-state view may be introduced.
* F-17 remains unresolved and untouched.
* Founder, CEO, Agent and delegation authority remain unchanged.
* No new capability is created.
* No new Agent is created.
* No new subsystem or state store is created.
* Deployment remains paused.

⸻

4. Certified Consumer Evidence

The existing P12 consumer-evidence harness MUST remain authoritative for determining whether P13 is an actual P12-W2 consumer.

The implementation MUST NOT:

* hide the P13 dependency from the consumer scanner;
* use an indirect import solely to evade measurement;
* modify the consumer scanner to conceal P13;
* weaken the independent verifier;
* create a parallel consumer measurement.

The certified measurement must honestly report P13 as a consumer after wiring.

⸻

5. Certified-Change Boundary

The CEO MAY update the existing consumer-evidence population and its directly associated tests/classification as authorized above.

The CEO MUST STOP and return Founder Decision Required if implementation requires:

* changing P12-W2 semantics;
* changing P12-W2 ownership;
* changing the certified P12 source population;
* changing certified P12 verifier semantics;
* changing P12 architecture beyond consumer registration;
* changing F-17;
* changing the certified P13 Blueprint;
* creating a new architectural interface;
* expanding authority.

The CEO MUST NOT classify such changes as maintenance without Founder authorization.

⸻

6. FR-1 Completion Objective

FR-1 may continue with the objective:

Live Operational Ledger
        ↓
     P12-W2
        ↓
       P13

The completed chain must be observable and independently measurable.

The following must hold:

1. P12-W2 reports current versus historical delegation state correctly.
2. P12-W2 reports blocking versus historical/answered escalation state correctly.
3. P13 receives state through P12-W2.
4. The certified consumer measurement recognizes P13.
5. Existing P12 certified verifiers remain valid.
6. Existing P12 source populations remain unchanged unless explicitly authorized.
7. P13 does not directly consume Agency state.
8. Fresh-process reconstruction reproduces the same relationship.
9. Existing S-1 through S-4 and MR-S5-1 behavior remains intact.
10. No new current-state authority is introduced.

⸻

7. Evidence Integrity Correction

The previously generated S-6 and Targeted Discovery evidence records contained script_sha256 values corresponding to earlier versions of their evidence scripts.

Because those scripts were subsequently modified to prevent false consumer classification, the CEO MUST reconcile this evidence-chain discrepancy.

The CEO MAY:

* generate corrected evidence outputs;
* append an explicit correction record;
* preserve the original evidence as historical;
* clearly distinguish original and corrected evidence.

The CEO MUST NOT silently overwrite or falsify historical evidence.

This correction MUST NOT alter the substantive findings of S-6 or Targeted Discovery unless fresh verification demonstrates that their findings were materially affected.

⸻

8. Verification

Before declaring FR-1 complete, perform fresh-process verification covering:

* P12-W2 current/historical state;
* P12-W2 escalation classification;
* P13 → P12-W2 dependency;
* certified consumer measurement;
* P12 verifier population;
* P12 verifier verdicts;
* P13 observation;
* direct Agency → P13 negative control;
* fresh-process reconstruction;
* certified-byte integrity;
* regression suites;
* citation and stale-reference audits.

The verification must distinguish:

data change

from

certified semantic change.

⸻

9. Stop Conditions

Stop immediately and return to Founder if:

* the certified P12 semantic contract must change;
* the certified verifier’s meaning must change;
* P12 source population must change;
* a new state authority is required;
* P13 requires direct Agency-state access;
* F-17 must be resolved;
* a new subsystem is required;
* authority must expand;
* the existing consumer-evidence architecture cannot represent P13 honestly.

⸻

10. Founder Decision

FQ-FR1-1: OPTION A

Founder Authorization: YES

Decision State: APPROVED

FR-1 may continue within the boundaries of this Founder Decision.

No additional authority is implied beyond the explicit consumer-registration and P13 integration scope stated above.
````
