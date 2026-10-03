# FD-TD-001 — P12-W2 ↔ Live Operational Ledger Integration Classification (as received)

**Received:** from the Founder (Moriarty), 2026-10-03, in the message body; extracted byte-exactly from the session transcript. Answers FQ-TD-1 of the Targeted Discovery (Register `§156`). Registered at Register `§157`; FR-1 construction result at `§158`.

````text
AIOS FOUNDER DECISION RECORD

FD-TD-001 — P12-W2 ↔ Live Operational Ledger Integration Classification

Document Type: Founder Decision Record
Decision Domain: Agency / P12-W2 / System State Integration
Predecessor: TARGETED-DISCOVERY-STATE-AUTHORITY-P13-RECONCILIATION-2026-10-04
Question: FQ-TD-1
Founder: Moriarty
Status: APPROVED
Founder Authorization: YES

⸻

1. Decision

The Founder selects:

OPTION A — Classify the P12-W2 ↔ Live Operational Ledger integration as FDR-G1 implementation maintenance.

P12-W2 remains the system-wide integration layer and does not become the owner of domain-specific operational state.

The live operational ledger remains the authoritative owner for the current lifecycle/disposition of delegations within its authorized domain.

P12-W2 may consume and project that operational state so that system-wide consumers can distinguish:

* CURRENT operational state
* HISTORICAL state
* BLOCKING state
* NON-BLOCKING historical state

without creating a competing state authority.

⸻

2. Authority Basis

This decision is grounded in:

* P12 Authorization D7 — P12-W2 as system-wide integration layer
* P12 certified STATE → AUTHORITATIVE SOURCE → PROJECTION → CONSUMER model
* A2 live operational ledger disposition
* B1 operational closure/disposition
* FD-CG7-001
* FDR-G1 §§8–9 concerning maintenance versus material certified change
* P13 certified Blueprint integration model
* Targeted Discovery result K-7-B
* Targeted Discovery result K-8-B

No authority is created or expanded by this decision.

⸻

3. Required Integration Boundary

The implementation MAY:

1. connect P12-W2 to the already-authorized live operational ledger;
2. derive CURRENT versus HISTORICAL state from that ledger;
3. expose the resulting projection to existing P12/P13 consumers;
4. preserve existing domain ownership;
5. preserve historical certified records;
6. allow fresh-process reconstruction of the same state.

The implementation MUST NOT:

1. create a second system-wide current-state authority;
2. transfer delegation-state ownership from the live ledger to P12-W2;
3. modify certified P12 verifier population;
4. modify F-17;
5. alter Founder, CEO, Agent, or delegation authority;
6. create a new capability, Agent, subsystem, or state store;
7. directly make P13 consume Agency state outside the certified P12-W2 integration path;
8. alter certified P12 semantics.

⸻

4. Certified-Change Escalation Boundary

If implementation discovery determines that the work requires changing any certified:

* contract,
* interface,
* dependency,
* semantic definition,
* certified verifier population,
* certified P12 architecture boundary,

the CEO MUST STOP the construction at that boundary and return a Founder Decision Required state.

The CEO MUST NOT independently classify such a change as maintenance.

⸻

5. P13 Boundary

P13 remains governed by its existing certified Blueprint.

The approved route is:

Live Operational Ledger
        ↓
     P12-W2
        ↓
       P13

A direct:

Agency → P13

state integration is NOT authorized by this decision.

⸻

6. FR-1 Authorization

FR-1 Minimal Integration Construction is authorized within the above boundary.

The objective is to restore the intended relationship between:

operational state → P12-W2 → P13/system-wide consumers

while preserving domain ownership and certified historical evidence.

Construction should use existing mechanisms wherever possible.

No new subsystem is authorized.

⸻

7. Verification Requirements

Before FR-1 may be declared complete, the CEO must verify at minimum:

* the 14 stale ACTIVE projections are no longer presented as current;
* the 2 genuinely live grants are correctly represented;
* historical completed/revoked grants remain historical;
* blocking versus historical/non-blocking escalation semantics remain correct;
* P12 certified evidence remains byte-identical unless an explicitly authorized certified change occurs;
* P13 receives state through P12-W2;
* fresh-process reconstruction produces the same state;
* existing P11/S-1/S-2/S-3/S-4/MR-S5-1 behavior remains intact;
* no second current-state authority has been introduced;
* authority and delegation boundaries remain unchanged.

⸻

8. Stop Conditions

Construction MUST stop and return a Founder Decision Required state if:

* certified P12 semantics must change;
* P12-W2 ownership must change;
* F-17 must be resolved;
* P13 certified architecture must change;
* a new state authority is required;
* a new capability/subsystem is required;
* authority must be expanded;
* existing mechanisms cannot satisfy the objective without architectural change.

⸻

9. Founder Decision

FQ-TD-1: OPTION A

Founder Authorization: YES

Decision State: APPROVED

FR-1 Minimal Integration Construction is authorized within the boundaries above.
````
