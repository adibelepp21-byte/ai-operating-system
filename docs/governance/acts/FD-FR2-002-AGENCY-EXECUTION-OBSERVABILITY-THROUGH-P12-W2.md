# FD-FR2-002 — Agency Execution Observability Through P12-W2 (as received)

**Received:** from the Founder (Moriarty), 2026-10-04, in the message body; extracted byte-exactly from the session transcript. Answers FQ-FR2-G5 (Register `§164`). Registered at Register `§165`.

````text
AIOS FOUNDER DECISION RECORD

FD-FR2-002 — Agency Execution Observability Through P12-W2

Document Type: Founder Decision Record
Question: FQ-FR2-G5
Predecessor: FR-2 — Agency Runtime & Trace Integration
Related: FD-FR2-001, FD-FR1-001
Founder: Moriarty
Status: APPROVED
Founder Authorization: YES

⸻

1. Decision

The Founder selects:

OPTION A — Extend the existing P12-W2 integration layer to expose Agency execution observations to P13 through the established P12-W2 → P13 integration path.

P13 MUST NOT obtain Agency execution state by directly reading Agency live Trace or Runtime stores when the same information can be provided through P12-W2.

The objective is to preserve a single system-wide integration layer.

⸻

2. Architectural Principle

The Agency observability path shall remain:

Agency Runtime / Trace
        ↓
P12-W2 Execution Projection
        ↓
P13

and NOT:

Agency Runtime / Trace
        ↓
P13 Direct Access

P12-W2 remains the system-wide integration layer.

P12-W2 does not become the owner of Runtime or Trace.

P13 does not become an execution-state authority.

⸻

3. Scope

The CEO MAY:

1. extend the existing P12-W2 execution projection to observe authorized live Agency execution data;
2. preserve separation between live and certified data;
3. expose the resulting execution observation through the existing P12-W2 → P13 interface;
4. extend existing P13 observation only through the already-established P12-W2 path;
5. add verification and negative controls for the new observation path;
6. preserve existing Runtime, Trace, Manifest and Execution Contract semantics.

No new subsystem is authorized.

⸻

4. Required Observation Model

P13 should be able to determine, through P12-W2:

* whether Agency execution is currently active;
* whether an Agency execution completed;
* the associated execution identity;
* associated Agent Instance;
* associated Delegation;
* Runtime participation;
* Trace/Manifest existence;
* Result availability;
* execution outcome;
* historical versus current execution.

The projection MUST NOT become an independent authority.

⸻

5. Live / Certified Boundary

Execution observations may originate from live operational roots.

Certified historical evidence remains immutable.

The projection MUST explicitly distinguish:

CERTIFIED
LIVE
CURRENT
HISTORICAL

No live execution observation may silently become certified evidence.

Existing certified P12 populations and verdict semantics must remain unchanged unless a further Founder Decision authorizes otherwise.

⸻

6. P13 Boundary

P13 may consume Agency execution observations through the existing P12-W2 interface.

P13 MUST NOT:

* directly read Agency Trace stores;
* directly read Agency Runtime stores;
* create a second execution-state source;
* become owner of execution state;
* bypass P12-W2;
* introduce a parallel current-state model.

⸻

7. Existing Runtime / Trace Semantics

This decision does NOT authorize changes to:

* Runtime state persistence;
* Execution Contract schema;
* Trace Domain Model fields;
* Trace status semantics;
* escalation status semantics;
* ExecutionManifest schema;
* Runtime ownership.

The existing FR-2 residual gaps remain open:

* G3 — Runtime state persistence;
* G6 — Trace status semantics;
* G7 — Trace escalation production.

They must not be silently resolved as part of G5.

⸻

8. Verification Requirements

Before G5 may be declared complete, fresh-process verification MUST demonstrate:

1. Agency Runtime execution remains intact.
2. Agency Trace remains intact.
3. Agency Manifest remains intact.
4. P12-W2 observes the Agency execution through its authorized projection.
5. P13 receives the execution observation through P12-W2.
6. P13 does not directly read Agency Runtime/Trace stores.
7. Live and certified execution observations remain distinguishable.
8. Historical execution is not presented as current.
9. Existing P12 certified populations remain intact unless explicitly authorized.
10. Existing FR-1 state observation remains unchanged.
11. Existing 7-link Agency provenance remains 7/7 JOINED.
12. Fresh-process reconstruction succeeds.
13. Independent consumer measurement recognizes the legitimate P12-W2 → P13 relationship.
14. No second execution-state authority exists.

⸻

9. Negative Controls

At minimum:

N1

P13 direct access to Agency Trace is rejected.

N2

P13 direct access to Agency Runtime store is rejected.

N3

P12-W2 cannot fabricate execution observations without corresponding live evidence.

N4

Historical execution cannot be presented as current.

N5

A Result without Runtime/Trace evidence cannot be presented as Runtime execution.

N6

A Runtime observation without Agent Instance provenance cannot be presented as valid Agency execution.

N7

Certified historical execution evidence cannot be mutated.

N8

Live execution evidence cannot silently enter the certified population.

N9

A second current execution-state authority cannot be introduced.

N10

Existing FR-1 operational state remains unchanged.

⸻

10. Stop Conditions

The CEO MUST STOP and return Founder Decision Required if:

* P12-W2 certified semantics must change;
* P12-W2 ownership must change;
* P13 certified source architecture must change;
* a new execution projection subsystem is required;
* direct P13 access to live Trace becomes necessary;
* Trace schema must change;
* Execution Contract must change;
* Runtime persistence must be redesigned;
* new authority is required;
* certified evidence semantics must change.

⸻

11. Residual Frontier Preservation

The following remain explicitly OPEN after G5:

G3 — Runtime State Persistence

G6 — Trace Status Semantics

G7 — Trace Escalation Semantics

Their existence must not be interpreted as FR-2 failure.

FR-2 Runtime/Trace integration remains valid independently of these unresolved frontiers.

⸻

12. Founder Decision

FQ-FR2-G5: OPTION A

Founder Authorization: YES

Decision State: APPROVED

Agency execution observability may be exposed to P13 through P12-W2 using the existing integration architecture and live/certified separation.

No direct Agency Runtime/Trace → P13 integration is authorized.
````
