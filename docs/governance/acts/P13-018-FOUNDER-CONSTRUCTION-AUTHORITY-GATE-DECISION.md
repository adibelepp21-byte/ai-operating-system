# `P13-018` — Founder Construction Authority Gate Decision

**Document type:** Founder Decision — Founder Construction Authorization
**Decision:** **APPROVED WITH BOUNDED INITIAL AUTHORITY** — `D-1` approve · `D-2b` evidence-only initial action envelope · `D-3` FD-P12-002 criteria, read-only
**Founder:** Moriarty · **Dated:** not stated in the instrument; received 2026-09-24 · **Authority basis:** `FDR-2`
**Answers:** `docs/architecture/p13-preparation/P13-018-CONSTRUCTION-AUTHORITY-GATE.md` (the prepared gate, which carries the same number)

## Provenance

The decision arrived as one message with no attachment. The fenced block below
is that message exactly as issued, from its first line through `END OF
P13-018 FOUNDER CONSTRUCTION AUTHORITY GATE DECISION`. Its UTF-8 sha256,
taken over the fenced content, is `6dd19861d9ab4fb964590f2a5e6b7601c8ef819b8b353b347a002f19a63c0372`.

This header was written by Claude and is not part of the Founder's text.

## How the envelope is recorded — and why that is not authority creation

`D-2b` issues the initial envelope. The canonical Blueprint (`§5.1`) makes an
envelope executable only when it is **recorded and resolvable**. Accordingly,
this decision's envelope is recorded as `P13-ENV-01`:

* in the Delegation Register (`§14`), naming this instrument as its source;
* as a machine-readable record
  (`docs/governance/p13-envelopes/P13-ENV-01.json`), whose sha256 the
  Register entry fixes.

The record transcribes `§3`'s six permitted items and twelve prohibitions. It
adds none. Recording what the Founder issued is not issuing it
(`G-08`; `R06`).

## One identifier note

The Founder's decision and the prepared gate document share the number
`P13-018`. Citations to *the decision* point to this file under
`docs/governance/acts/`, which is the only place `tools/authority_citation.py`
accepts a decision record.

---

# § RECORD — issued by the Founder, verbatim

````text
P13-018 — FOUNDER CONSTRUCTION AUTHORITY GATE DECISION

Program: AIOS — Phase 13
Gate: Construction Authority Gate
Authority Basis: FDR-2
Decision Type: Founder Construction Authorization
Status: APPROVED WITH BOUNDED INITIAL AUTHORITY

⸻

1. FOUNDER DECISION SUMMARY

The Founder has reviewed the P13-018 Construction Authority Gate following:

FDR-2
  ↓
FDR-2 Registration
  ↓
P13 Reconciliation
  ↓
P13 Canonical Blueprint v1.0
  ↓
P13-018 Construction Authority Gate

The Founder approves the following:

D-1 = APPROVE
D-2 = APPROVE D-2b — EVIDENCE-ONLY INITIAL ACTION ENVELOPE
D-3 = YES — ADMIT FD-P12-002 CRITERIA

Construction is therefore authorized within the bounded scope and authority defined below.

This authorization does not constitute unrestricted P13 autonomy, Native Core expansion, governance modification, or authority self-expansion.

⸻

2. D-1 — CONSTRUCTION SCOPE

Founder Decision

APPROVED.

Claude Code is authorized to construct the P13 components explicitly included in the approved in-scope list of:

* P13-018 — Construction Authority Gate
* AIOS_P13_CANONICAL_BLUEPRINT_v1.0

Construction must remain within the defined scope.

Scope Rule

AUTHORIZED SCOPE
        ↓
BUILD
        ↓
VERIFY
        ↓
EVIDENCE

If construction discovers a requirement outside the authorized scope:

DISCOVER
   ↓
CLASSIFY
   ↓
CHECK AUTHORITY
   ↓
IF AUTHORIZED → PROCEED
IF NOT AUTHORIZED → ESCALATE

No scope expansion may occur silently.

Prohibited Scope Expansion

This authorization does not permit:

* creation of a twelfth Native Core boundary;
* modification of Founder Reserved Authority;
* modification of the Governance Constitution;
* creation of new governance authority;
* self-authorization;
* unrestricted self-modification;
* arbitrary modification of P1–P12;
* modification of certified P10–P12 evidence;
* resolution of Architect Reserved matters without appropriate authority;
* execution of actions outside the defined authority envelope.

⸻

3. D-2 — INITIAL ACTION ENVELOPE

Founder Decision

APPROVED — D-2b: EVIDENCE-ONLY INITIAL ACTION ENVELOPE.

The initial P13 action envelope is deliberately bounded.

P13 may initially perform:

1. authorized read-only verification;
2. authorized reading of AIOS state and evidence;
3. creation of P13-specific records and evidence in the designated live root;
4. creation of traceable P13 evidence;
5. creation of escalation records;
6. verification of its own authorized evidence operations.

Explicitly Prohibited

The initial envelope does not permit P13 to:

* modify certified P10–P12 evidence;
* modify Founder Decisions;
* modify governance authority;
* create or grant authority;
* alter Native Core boundaries;
* execute external/business actions;
* alter Founder Reserved Authority;
* alter Architect Reserved matters;
* self-expand its action envelope;
* grant authority to itself;
* grant authority to another component;
* interpret an unrecorded proposal as authorization.

Authority Rule

NO RECORDED AUTHORITY
        ↓
NO EXECUTION

An action is executable only where its authority envelope resolves to a valid recorded authority.

If the authority cannot be resolved:

UNKNOWN / REFUSE / ESCALATE

⸻

4. D-2b IS AN INITIAL ENVELOPE

The Founder explicitly establishes:

D-2b is the initial P13 action envelope. It is not the permanent or maximum P13 autonomy envelope.

Future expansion of P13 authority requires:

* valid authority;
* explicit authority source;
* bounded scope;
* verification;
* evidence;
* applicable governance approval.

P13 may not infer future authority from its own capability.

Therefore:

INITIAL AUTHORITY
        ≠
MAXIMUM AUTHORITY

and:

CAPABILITY
        ≠
AUTHORITY

⸻

5. E13-05 INTERPRETATION

The Founder explicitly rejects the interpretation that D-2b automatically proves the complete E13-05 execution criterion.

D-2b enables the initial verification path.

Therefore:

D-2b
  ↓
AUTHORIZED LIMITED EXECUTION
  ↓
VERIFY
  ↓
EVIDENCE

The result must be classified according to what is actually demonstrated.

If the full E13-05 contract cannot yet be demonstrated under the initial evidence-only envelope, the remainder must be classified rather than falsely marked complete.

No completion claim may exceed the evidence.

⸻

6. D-3 — FD-P12-002 CRITERIA

Founder Decision

APPROVED — YES.

P13 is authorized to consume the ratified machine-readable criteria contained in FD-P12-002 for evaluation purposes.

The relationship is:

FD-P12-002
   ↓
READ
   ↓
P13 EVALUATION
   ↓
EVIDENCE

Ownership

Ownership of the criteria remains with its existing authoritative source.

P13 does not acquire ownership merely by consuming the criteria.

P13 May

P13 may:

* read the admitted criteria;
* evaluate relevant state against the criteria;
* produce evaluation evidence;
* trace the evaluation to the criterion;
* report the result;
* escalate when the criterion cannot be evaluated reliably.

P13 May Not

P13 may not:

* modify the criteria;
* redefine the criteria;
* promote criteria into governance authority;
* use the criteria to create new authority;
* modify P12;
* certify itself solely because the criteria were satisfied.

⸻

7. MEMORY RELATIONSHIP

The Founder confirms the FDR-2 requirement-driven integration principle.

The existing:

Memory
   ↓
P13

relationship may be implemented as the defined read path described in the canonical Blueprint.

Memory ownership remains outside P13.

P13 may consume authorized memory-derived evidence but must not silently assume ownership of the Memory subsystem.

⸻

8. NATIVE CORE INVARIANT

The Founder confirms:

NATIVE CORE = 11

No twelfth Native Core boundary is authorized by this gate.

If construction discovers evidence that P13 genuinely requires a Native Core change:

DISCOVER
   ↓
DOCUMENT
   ↓
STOP AT BOUNDARY
   ↓
ARCHITECTURAL / FOUNDER AUTHORITY

The requirement must not be solved by silent boundary expansion.

⸻

9. GOVERNANCE INVARIANTS

The following remain binding throughout construction:

G-01 — Governance First

Governance authority precedes execution.

G-02 — Fail Closed

Missing or ambiguous authority results in refusal/escalation.

G-03 — No Self-Promotion

P13 cannot promote its own proposal into authority.

G-04 — Immutable Trace

Authorized P13 execution must produce durable evidence and trace.

G-05 — Certified Evidence Protection

Certified P10–P12 evidence remains protected.

G-06 — Founder Supremacy

Founder Reserved Authority remains unchanged.

G-07 — No Silent Scope Expansion

New requirements are discovered and classified before construction proceeds beyond the authorized boundary.

G-08 — No Self-Authorization

P13 cannot issue authority to itself.

⸻

10. CONSTRUCTION AUTHORIZATION STATE

Following this decision:

P13 SEMANTIC DEFINITION
= ESTABLISHED
P13 CANONICAL BLUEPRINT
= ESTABLISHED
P13 CONSTRUCTION
= AUTHORIZED WITH BOUNDED SCOPE
INITIAL P13 ACTION ENVELOPE
= EVIDENCE-ONLY
FULL P13 AUTONOMY
= NOT AUTHORIZED
NATIVE CORE
= 11
FD-P12-002 CRITERIA
= ADMITTED READ-ONLY
CERTIFICATION
= NOT GRANTED
P13 COMPLETION
= NOT CLAIMED

⸻

11. REQUIRED CONSTRUCTION LOOP

Claude Code shall operate the construction using:

DISCOVER
   ↓
UNDERSTAND
   ↓
CLASSIFY
   ↓
CHECK AUTHORITY
   ↓
DECIDE
   ↓
BUILD
   ↓
VERIFY
   ↓
INTEGRATE
   ↓
EVIDENCE
   ↓
RE-DISCOVER
   ↓
REPAIR / BUILD
   ↓
VERIFY
   ↓
EXHAUSTION / ESCALATION

Construction is not complete merely because all planned files have been created.

⸻

12. REQUIRED REPORTING AFTER CONSTRUCTION

The next construction report must distinguish:

1. built;
2. verified;
3. integrated;
4. evidence produced;
5. authority exercised;
6. authority refused;
7. escalations raised;
8. remaining gaps;
9. E13-01 through E13-07 status;
10. residual frontier;
11. newly discovered dependencies;
12. any scope pressure;
13. any authority conflict;
14. any Native Core pressure;
15. certification readiness.

No item may be reported as complete solely because code exists.

⸻

13. FINAL FOUNDER DECISION

The Founder approves:

D-1
APPROVE P13-018 IN-SCOPE CONSTRUCTION
D-2
APPROVE D-2b
EVIDENCE-ONLY INITIAL ACTION ENVELOPE
D-3
APPROVE
FD-P12-002 READ-ONLY CRITERIA ADMISSION

Therefore:

P13 construction may proceed within the authorized Blueprint scope and the initial evidence-only action envelope.

The Founder does not authorize:

unrestricted autonomous P13 execution.

The Founder does not authorize:

Native Core expansion.

The Founder does not authorize:

self-generated authority.

The Founder does not authorize:

certification of P13.

⸻

14. FINAL STATE

FDR-2
   ↓
CANONICAL P13 DEFINITION
   ↓
CANONICAL BLUEPRINT
   ↓
P13-018
   ↓
D-1 APPROVED
   ↓
D-2b APPROVED
   ↓
D-3 APPROVED
   ↓
BOUNDED P13 CONSTRUCTION
   ↓
EVIDENCE
   ↓
VERIFICATION
   ↓
RE-DISCOVERY
   ↓
E13 EXIT CONTRACT

Construction is authorized only within this bounded authority envelope.

The authority envelope itself may not be expanded by P13.

Any future authority expansion requires the applicable governance decision.

END OF P13-018 FOUNDER CONSTRUCTION AUTHORITY GATE DECISION
````
