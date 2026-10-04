# FD-FR2-001 — Agency Runtime & Trace Integration Authorization (as received)

**Received:** from the Founder (Moriarty), 2026-10-04, in the message body; extracted byte-exactly from the session transcript. Answers FQ-FR2-1 (Register `§162`). Registered at Register `§163`.

````text
AIOS FOUNDER DECISION RECORD

FD-FR2-001 — Agency Runtime & Trace Integration Authorization

Document Type: Founder Decision Record
Question: FQ-FR2-1
Predecessor: FR-2 — Governed Execution → Runtime / Trace Discovery
Related: FD-FR1-001, FD-TD-001
Founder: Moriarty
Status: APPROVED
Founder Authorization: YES

⸻

1. Decision

The Founder selects:

OPTION A — Authorize the existing Runtime / Trace mechanisms to be integrated with Agency execution as bounded implementation maintenance under FDR-G1, following the live/certified separation precedent established by GOAL-V2-002.

The purpose is to connect existing Agency execution to the existing AIOS Runtime, Trace, ExecutionManifest, and Runtime observation mechanisms.

No new Runtime, Trace, Execution, provenance, or observability subsystem is authorized.

⸻

2. Provenance Objective

The authorized construction must establish the existing mechanism as an actual Agency execution path:

Agent Instance
      ↓
Delegation
      ↓
Execution
      ↓
Execution Layer
      ↓
Runtime
      ↓
Trace / Manifest
      ↓
Result
      ↓
Verification
      ↓
CEO Decision
      ↓
Plan Outcome

The existing provenance model must be used rather than replaced.

The objective is not to redesign the Trace model.

⸻

3. Runtime Integration Boundary

Agency execution MAY be routed through the existing:

* Execution Contract;
* Execution Layer;
* Runtime;
* Runtime observation mechanism;
* Trace writer;
* ExecutionManifest;
* existing chain/provenance readers.

The implementation MUST preserve the existing Runtime boundary:

Agent / Workflow / Skill / Planner / Scheduler
                    ↓
             Execution Contract
                    ↓
              Execution Layer
                    ↓
                 Runtime

Agency MUST NOT be coupled directly to Runtime internals when the existing Execution Contract provides the appropriate boundary.

⸻

4. Live / Certified State Separation

Following GOAL-V2-002 precedent, operational Agency Runtime/Trace data MAY be stored under live operational roots.

Certified historical evidence MUST remain immutable.

Readers MAY be extended to distinguish:

CERTIFIED
LIVE
HISTORICAL
CURRENT

without treating live operational data as certified historical evidence.

A live operational record MUST NOT silently become certified evidence.

⸻

5. Reader Extension

Existing readers MAY be extended to discover authorized live Agency execution data where necessary to verify the Agency provenance chain.

The following principles are mandatory:

1. Existing certified semantics remain unchanged.
2. Certified historical populations remain identifiable.
3. Live operational populations are explicitly identified.
4. Readers do not silently merge live and certified authority.
5. Domain ownership remains unchanged.
6. Derived projections do not become authoritative state.
7. Existing independent verification remains independent.

If a reader cannot represent live and certified sources without changing its certified semantics, construction MUST STOP and return Founder Decision Required.

⸻

6. Agent Instance Identity

Agency Runtime/Trace integration MUST preserve:

Agent Definition
      ≠
Agent Instance
      ≠
Delegation
      ≠
Execution

The Runtime/Trace path MUST identify the actual authorized Agent Instance.

A capability name or Agent Definition name MUST NOT be accepted as a substitute for the executing Agent Instance where the existing provenance contract requires instance identity.

The known G4 condition—Trace recording the definition name instead of the instance—must therefore be resolved within the authorized integration boundary if the existing mechanism permits it.

If resolving G4 requires a governed Domain-Model change to the Trace record, STOP and return Founder Decision Required.

⸻

7. ExecutionManifest

Each authorized Agency execution MAY use the existing ExecutionManifest mechanism.

The manifest must preserve existing relationships between:

* Goal;
* Plan;
* Delegation;
* Agent Instance;
* Execution;
* Trace;
* Result;

using the existing manifest structure.

No new manifest schema is authorized.

⸻

8. Runtime State / Persistence Boundary

The known FR-2 finding that Runtime state and execution sequence are process-local is acknowledged.

This decision does NOT authorize redesign of Runtime persistence.

The CEO may verify and document the current persistence behavior.

If persistent Runtime execution identity is required to complete the minimum Agency provenance chain and cannot be achieved through existing mechanisms, STOP and return Founder Decision Required rather than creating a new persistence subsystem.

⸻

9. Trace Semantics Boundary

This decision does NOT authorize redesign of Trace status semantics.

Specifically:

* G6 — Trace success versus verification failure;
* G7 — Trace escalation status;

must not be silently redesigned merely to make FR-2 appear complete.

They may be documented as residual gaps or future discovery frontiers.

Only the minimum existing semantics required to establish the Agency Runtime/Trace chain may be integrated.

⸻

10. P13 Boundary

P13 MAY consume Runtime/Trace information only through an already-authorized existing source/interface.

A new direct:

Agency → P13

Trace integration is NOT authorized.

If P13’s certified Blueprint or certified source model must change, STOP and return Founder Decision Required.

The existing FR-1 boundary remains:

Live Operational State
        ↓
     P12-W2
        ↓
       P13

FR-2 must not create a competing state authority.

⸻

11. Construction Scope

Authorized construction is limited to:

1. routing Agency execution through the existing Runtime path;
2. using existing Trace/manifest writers;
3. creating the necessary live operational roots;
4. extending existing readers to observe authorized live Agency execution data;
5. preserving Agent Instance identity;
6. connecting existing provenance relationships;
7. verifying fresh-process reconstruction;
8. preserving certified historical evidence.

No new subsystem is authorized.

No new capability is authorized.

No new Agent is authorized.

No new delegation authority is authorized.

Deployment remains paused.

⸻

12. Verification Requirements

Before FR-2 may be declared complete, fresh-process verification MUST establish:

Runtime

* Agency work actually enters Runtime;
* Runtime participation is evidenced;
* direct function-call bypass is prevented for the authorized path.

Trace

* Agency execution produces Trace through the existing mechanism;
* Trace identifies the actual Agent Instance;
* Trace is associated with the relevant execution;
* Trace is associated with the relevant Runtime observation.

Manifest

* ExecutionManifest is produced using the existing mechanism;
* Goal, Plan, Delegation, Agent Instance, Execution and Trace relationships are reconstructable.

Provenance

The chain must be reconstructable:

Founder Goal
→ Plan
→ Plan Step
→ Delegation
→ Agent Instance
→ Execution
→ Runtime
→ Trace
→ Result
→ Verification
→ CEO Decision
→ Plan Outcome

Observability

* existing readers can observe live Agency execution;
* certified historical evidence remains distinguishable;
* P13 does not acquire a second state authority.

Negative controls

At minimum:

* direct function execution cannot masquerade as Runtime execution;
* fabricated Agent Instance cannot pass provenance verification;
* Agent Definition cannot substitute for Agent Instance;
* hidden P13/reader dependencies cannot bypass consumer measurement;
* certified historical evidence cannot be mutated;
* live data cannot silently become certified data.

⸻

13. Stop Conditions

The CEO MUST STOP and return Founder Decision Required if:

* a new Runtime subsystem is required;
* a new Trace subsystem is required;
* Execution Contract semantics must change;
* Trace Domain Model fields must change;
* certified verifier semantics must change;
* certified architecture must change;
* P13 certified architecture must change;
* Runtime ownership must change;
* new authority is required;
* persistent execution identity requires a new architectural mechanism;
* the live/certified separation cannot be implemented without changing certified semantics.

⸻

14. Residual Gaps

The following findings from FR-2 remain acknowledged and MUST NOT be silently closed:

* G3 — Runtime state / execution sequence persistence;
* G6 — Trace success versus verification semantics;
* G7 — Trace escalation production semantics.

They remain candidates for later discovery unless the authorized construction demonstrates that an existing mechanism already resolves them.

⸻

15. Evidence Integrity

All certified historical evidence MUST remain immutable.

Any correction to prior evidence must:

1. preserve the original;
2. create a correction record;
3. identify the changed evidence tooling;
4. verify whether substantive findings changed;
5. clearly distinguish original and corrected outputs.

No historical evidence may be silently rewritten.

⸻

16. Founder Decision

FQ-FR2-1: OPTION A

Founder Authorization: YES

Decision State: APPROVED

FR-2 Runtime / Trace integration construction is authorized within the exact boundaries defined by this record.

This authorization does not authorize Runtime redesign, Trace redesign, Domain Model expansion, new subsystems, new authority, or changes to certified architecture.
````
