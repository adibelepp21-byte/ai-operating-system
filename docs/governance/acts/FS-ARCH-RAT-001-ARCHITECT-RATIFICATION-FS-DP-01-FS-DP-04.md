# `FS-ARCH-RAT-001` — Architect Ratification Decision Package: FS-DP-01 Database + FS-DP-04 Deployment (as received)

**Received:** from the Founder, 2026-09-27, in the message body. It was the
third form of the package that day. The first two were interrupted before any
action, and the second carried a partly filled ratification block.
**Stated status (header):** *"PROPOSED FOR ARCHITECT RATIFICATION"*.
**Ratification records in the body** (`§3.4`, `§4.5`, `§11.1`, `§11.2`, `§17`):
*"Status: RATIFIED"*, *"Architect: Moriarty"*, *"Date: 27 September 2026"*,
*"Authority: ARCHITECT"*.

The header keeps its proposal wording, while every ratification record in the
body is completed and signed. Register `§68` records the decision on the body's
records and notes the header.

Reproduced below as received. List items are kept as `*` bullets and check
boxes as `[ ]`.

````text
FS-ARCH-RAT-001

AIOS FULL STACK — ARCHITECT RATIFICATION DECISION PACKAGE

FS-DP-01 DATABASE + FS-DP-04 DEPLOYMENT

Program: AIOS Full Stack Development & Operationalization
Parent Act: ACT-CC-POST-P13-AIOS-FULL-STACK-001
Founder Decision: FD-FS-001
Current Stage: FS-08 — Infrastructure & Cloud
Package Type: Architect Ratification / Architecture Decision Package
Status: PROPOSED FOR ARCHITECT RATIFICATION

⸻

1. PURPOSE AND AUTHORITY

This package consolidates the two architecture decisions required to continue the AIOS Full Stack deployment adapter:

1. FS-DP-01 — Database / Persistent State Architecture
2. FS-DP-04 — Deployment / Runtime Architecture

It operates under:

* ACT-CC-POST-P13-AIOS-FULL-STACK-001;
* FD-FS-001;
* the existing AIOS Governance Baseline and authority matrix;
* Freeze §10;
* the FS-08 evidence model;
* the existing FS decision-package structure.

Database, deployment, networking, identity/authentication, scaling, observability, and separately reserved Agent creation architecture remain Architect-reserved.

Claude Code may discover, analyze, prepare, implement, and verify work within delegated authority, but MUST NOT treat this package as ratified merely because it exists.

⸻

2. CURRENT EVIDENCE

2.1 Full Stack Local Surface

The current implementation provides:

* Python backend;
* dependency-light frontend console;
* AIOS public-interface integration;
* Workflow execution;
* governed docs.read Tool execution;
* Trace generation;
* success/failure scenarios;
* security refusal and hostile-input handling;
* browser integration;
* audit/session surfaces;
* certified-write protection.

Verification on the recorded commit:

tools              1,920
native_core          801
consumers            276
bounded_exception     29
fullstack             79

Certified-write probe:

0 certified-root writes

Local Full Stack execution is therefore verified.

⸻

2.2 Vercel

Project: aios-platform
Production deployment: dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj
Status: READY
Deployment commit: 22c0b49
Production behavior: 404 NOT_FOUND

The deployed commit lacks:

* fullstack/;
* the current Full Stack implementation;
* index.html;
* public/;
* api/;
* Vercel configuration;
* a Python deployment entrypoint.

The current branch also lacks a Vercel-specific entrypoint.

The 404 is therefore explained by the absence of a deployable application surface in the deployed source/configuration.

AIOS Full Stack
      │
      ├── Local execution       VERIFIED
      ├── Backend               VERIFIED
      ├── Frontend              VERIFIED
      ├── AIOS integration      VERIFIED
      ├── Browser integration   VERIFIED
      │
      └── Cloud deployment
              ├── Vercel project EXISTS
              ├── Deployment      READY
              └── Application     NOT REACHABLE
                                  ↓
                              404 NOT_FOUND

⸻

2.3 Supabase

Project: ai operating system
Project Ref: scfymftfzkpilqbgmfwv
Status: ACTIVE_HEALTHY

Current state:

* project reachable;
* database available;
* no application schema;
* no migrations;
* no branches;
* no functions;
* no schema changes performed by this program;
* Free plan;
* no spending authorized.

The previous timeout concerned a different project reference and is not evidence that the AIOS Supabase project is unavailable.

⸻

3. FS-DP-01 — DATABASE / PERSISTENT STATE

3.1 Architectural Question

The local backend uses filesystem-backed state, but hosted function filesystems cannot be assumed to provide durable persistence.

Deployed AIOS state therefore requires an explicit persistence boundary.

⸻

3.2 Proposed Decision: OPTION A — SUPABASE

Use the existing AIOS Supabase project:

scfymftfzkpilqbgmfwv

as the persistent database implementation behind the existing AIOS state/storage interface.

AIOS State Contract
        ↓
Existing State / Storage Interface
        ↓
Supabase Persistence Adapter
        ↓
AIOS Supabase Project

Supabase remains an infrastructure/service implementation and MUST NOT become the source of AIOS state architecture.

Rationale

Option A is proposed because:

1. the project already exists and is ACTIVE_HEALTHY;
2. Supabase is the named database provider under Founder Decision D3-A;
3. no schema has yet imposed a premature state model;
4. it provides durable persistence without relying on Vercel function storage;
5. it preserves the existing AIOS state/storage boundary;
6. it allows the database implementation to evolve without making Supabase schema canonical AIOS architecture.

The schema MUST be derived from established AIOS state/storage requirements.

Claude Code MUST NOT invent generic tables such as:

users
agents
messages
documents

unless required by an existing AIOS contract.

⸻

3.3 Implementation Boundary

After ratification, Claude Code may:

* implement the Supabase persistence adapter;
* create required schema and migrations;
* test persistence and restart persistence;
* test append-only Trace/audit requirements where applicable;
* test failure behavior;
* test available backup/restore mechanisms;
* record schema evidence;
* integrate the adapter behind the existing state/storage interface.

Claude Code MUST NOT:

* redefine AIOS state ownership;
* redesign AIOS Memory, Trace, or Runtime architecture;
* make Supabase-specific features canonical AIOS architecture;
* upgrade Supabase;
* purchase a paid plan;
* create billing commitments.

⸻

3.4 Ratification Record

Decision: RATIFY OPTION A — SUPABASE
Authority: ARCHITECT
Architect: Moriarty
Date: 27 September 2026
Status: RATIFIED

Selected Architecture:

Existing AIOS Supabase project:

scfymftfzkpilqbgmfwv

provides persistence behind the existing AIOS state/storage interface.

Conditions:

* Supabase does not define AIOS state architecture.
* Persistent state MUST NOT depend on Vercel function filesystem durability.
* No Vercel or Supabase paid-plan upgrade or billing commitment is authorized.

⸻

4. FS-DP-04 — DEPLOYMENT / RUNTIME ARCHITECTURE

4.1 Architectural Question

The local implementation runs as:

python -m fullstack.backend serve

A local persistent process cannot be assumed to map directly to Vercel’s function model.

The deployment therefore requires an explicit execution boundary.

⸻

4.2 Runtime Decision: A1 — PER REQUEST

The deployed API shall use per-request execution:

HTTP Request
     ↓
Vercel Python Function
     ↓
AIOS Full Stack Adapter
     ↓
AIOS Public Contract
     ↓
Runtime / Execution
     ↓
Persistent State
     ↓
Response

The architecture MUST NOT depend on a warm function instance as durable state.

Per-request execution is selected because it:

* avoids warm-instance persistence assumptions;
* separates ephemeral execution from persistent state;
* aligns with function-oriented hosting;
* forces persistence through the explicit database boundary;
* preserves AIOS Runtime contracts as the source of execution semantics.

The deployment adapter is an adapter around AIOS, not a replacement Runtime.

⸻

4.3 Deployment Shape: B1 — STATIC FRONTEND + PYTHON API FUNCTION

                    VERCEL
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    Static Console           Python API
                                    │
                                    ▼
                             Full Stack Adapter
                                    │
                                    ▼
                             AIOS Public APIs
                                    │
                                    ▼
                             Runtime / Execution
                                    │
                                    ▼
                             State / Storage API
                                    │
                                    ▼
                                Supabase

The frontend remains a presentation/control surface.

The backend remains an application interface to AIOS.

AIOS remains the authority for Runtime and Execution semantics.

Frontend Requirements

The existing dependency-light console SHALL be served as static assets where technically supported and MUST preserve:

* existing behavior;
* security-safe rendering;
* current frontend tests;
* existing backend API contracts;
* the current AIOS integration boundary.

The frontend MUST NOT become the authority for:

* permissions;
* capabilities;
* governance;
* Runtime decisions;
* execution authority.

Python API Requirements

The Vercel-compatible Python function/entrypoint SHALL:

* accept HTTP requests;
* map them to the existing Full Stack backend/application contract;
* invoke AIOS through existing public interfaces;
* preserve API response semantics;
* preserve failure behavior;
* preserve security behavior;
* preserve Trace/audit behavior.

It MUST NOT bypass AIOS public contracts to reach internal Runtime implementation.

⸻

4.4 Runtime Lifecycle

Function-local process memory is:

EPHEMERAL

not:

DURABLE

State required across requests MUST use the ratified persistence mechanism.

Ephemeral Execution Context
        ≠
Persistent AIOS State

⸻

4.5 Ratification Record

Runtime Lifecycle: RATIFY A1 — PER REQUEST
Deployment Shape: RATIFY B1 — STATIC FRONTEND + PYTHON API FUNCTION
Authority: ARCHITECT
Architect: Moriarty
Date: 27 September 2026
Status: RATIFIED

Conditions:

* The deployment adapter shall expose existing AIOS contracts without redefining AIOS Runtime architecture.
* Function-local memory is ephemeral and cannot be treated as durable state.
* Persistent state uses the ratified FS-DP-01 architecture.
* No spending or provider-plan upgrade is authorized.

Rationale:

Per-request execution provides a clear deployment boundary without warm-instance persistence assumptions.

Static frontend plus Python API preserves Full Stack separation while AIOS Runtime and Execution remain authoritative.

⸻

5. COMBINED RATIFIED ARCHITECTURE

With both decisions ratified:

                         USER
                           │
                           ▼
                    VERCEL PLATFORM
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       STATIC FRONTEND             PYTHON API
                                          │
                                          ▼
                                  FULL STACK ADAPTER
                                          │
                                          ▼
                                  AIOS PUBLIC CONTRACTS
                                          │
                                          ▼
                                  RUNTIME / EXECUTION
                                          │
                                          ▼
                                  STATE / STORAGE API
                                          │
                                          ▼
                                      SUPABASE

Authoritative boundaries:

Vercel
  ↓
Deployment Adapter
  ↓
AIOS Public Contract
  ↓
AIOS Runtime / Execution
AIOS State Contract
  ↓
State / Storage Interface
  ↓
Supabase

The infrastructure providers implement the required deployment and persistence boundaries.

They do not become the architectural source of truth for AIOS.

⸻

6. NON-AUTHORIZED SCOPE

This package does NOT authorize:

* production release;
* Founder Final System Acceptance;
* Vercel or Supabase plan upgrades;
* spending or billing commitments;
* authentication or identity architecture;
* networking beyond what the ratified deployment requires;
* scaling architecture;
* observability architecture;
* Agent Factory architecture;
* redesign of AIOS Runtime;
* modification of certified P13 roots;
* reopening Platform Organization closure;
* Phase 14;
* any new Phase.

⸻

7. REQUIRED IMPLEMENTATION AFTER RATIFICATION

Following ratification and Governance Decision Register persistence, Claude Code shall continue automatically under the existing Full Stack Act:

1. Persistence

Implement the Supabase adapter behind the existing AIOS state/storage interface.

Create only schema required by established AIOS contracts.

2. Deployment Adapter

Implement:

Vercel
   ↓
Python Function
   ↓
Full Stack Backend
   ↓
AIOS Public Contracts

3. Frontend

Expose the existing console as static assets.

4. Local Verification

Run:

* Full Stack tests;
* database persistence tests;
* restart persistence tests;
* failure tests;
* security tests;
* certified-write protection tests;
* integration tests.

5. Commit

Commit only verified changes.

6. Vercel Preview

Deploy a preview.

Preview success is not production release.

7. Supabase Verification

Verify:

* connection;
* schema;
* persistence;
* restart behavior;
* applicable Trace/audit persistence;
* failure handling.

8. Live Smoke Test

Verify:

* frontend;
* API;
* health;
* successful workflow;
* failed workflow;
* authorization refusal;
* Trace;
* persistence.

9. FS-08 Re-Discovery

Re-discover:

* Vercel;
* Supabase;
* deployment;
* runtime;
* state;
* observability;
* unresolved external dependencies.

10. FS-09

Proceed to Production Readiness only if the FS-08 exit criteria are satisfied.

⸻

8. PRODUCTION RELEASE REMAINS SEPARATE

Even if:

Vercel Preview = PASS
Supabase = PASS
FS-08 = PASS

production release is not authorized by this package.

The governed sequence remains:

FS-08 PASS
    ↓
FS-09 Production Readiness
    ↓
FS-09 PASS
    ↓
FOUNDER RELEASE DECISION
    ↓
FS-10 Deployment

This preserves D4-A from FD-FS-001.

⸻

9. NEGATIVE CONTROLS

Claude Code MUST NOT:

1. treat this package as authorization for any decision outside its scope;
2. modify the ratified architecture without the applicable authority;
3. create generic database schema without evidence;
4. make Supabase the source of AIOS architecture;
5. make Vercel the source of AIOS Runtime architecture;
6. use warm-instance state as durable state;
7. bypass AIOS public contracts;
8. redesign Runtime solely for Vercel convenience;
9. upgrade Vercel or Supabase;
10. spend money or add billing commitments;
11. introduce authentication, identity, networking, scaling, or observability architecture beyond existing authority;
12. claim Production Ready;
13. claim Operational AIOS;
14. treat preview deployment as production release;
15. create another Micro-Act merely to implement these ratified decisions;
16. modify certified P13 roots;
17. reopen the closed Platform Organization;
18. create or imply Phase 14;
19. silently expand Architect or Founder authority;
20. treat provider limitations as permission to alter AIOS architecture.

⸻

10. GOVERNANCE REGISTER ENTRY

Claude Code SHALL create one Governance Decision Register record containing:

Decision Package:
FS-ARCH-RAT-001
Ratified Components:
FS-DP-01
FS-DP-04
FS-DP-01:
OPTION A — SUPABASE
FS-DP-04 Runtime:
A1 — PER REQUEST
FS-DP-04 Deployment Shape:
B1 — STATIC FRONTEND + PYTHON API FUNCTION
Architect:
Moriarty
Date:
27 September 2026
Authority:
ARCHITECT

The record MUST include:

* exact decision;
* rationale;
* conditions;
* authority;
* date;
* affected implementation;
* implementation boundary;
* explicit non-authorized scope.

The Register entry is the authoritative governance record of the ratification.

⸻

11. ARCHITECT RATIFICATION RECORD

11.1 FS-DP-01 — DATABASE / PERSISTENT STATE

Decision: RATIFY OPTION A — SUPABASE

Architect: Moriarty

Date: 27 September 2026

Authority: ARCHITECT

Status: RATIFIED

Selected Architecture:

AIOS State Contract
        ↓
Existing State / Storage Interface
        ↓
Supabase Persistence Adapter
        ↓
AIOS Supabase Project

Supabase Project:

Project:
ai operating system
Project Ref:
scfymftfzkpilqbgmfwv

Conditions:

1. Supabase is an infrastructure implementation only.
2. Supabase does not define AIOS state architecture.
3. Existing AIOS state/storage contracts remain authoritative.
4. Persistent state must not depend on Vercel function filesystem durability.
5. Database schema must be derived from established AIOS requirements.
6. No generic schema may be invented without evidence.
7. No spending is authorized.
8. No paid-plan upgrade is authorized.
9. No billing commitment is authorized.

Rationale:

The existing AIOS Supabase project is healthy and was already selected as the database provider under Founder Decision D3-A.

It provides the persistence boundary required for hosted deployment while preserving the separation between AIOS architecture and infrastructure implementation.

⸻

11.2 FS-DP-04 — DEPLOYMENT / RUNTIME

Runtime Lifecycle: RATIFY A1 — PER REQUEST

Deployment Shape: RATIFY B1 — STATIC FRONTEND + PYTHON API FUNCTION

Architect: Moriarty

Date: 27 September 2026

Authority: ARCHITECT

Status: RATIFIED

Selected Runtime:

HTTP Request
     ↓
Vercel Python Function
     ↓
AIOS Full Stack Adapter
     ↓
AIOS Public Contract
     ↓
Runtime / Execution
     ↓
Persistent State
     ↓
Response

Selected Deployment Shape:

Static Frontend
        +
Python API Function

Conditions:

1. The deployment adapter exposes existing AIOS contracts.
2. The adapter does not redefine AIOS Runtime architecture.
3. Function-local memory is ephemeral.
4. Function-local memory cannot be treated as durable AIOS state.
5. Persistent state uses the ratified FS-DP-01 architecture.
6. AIOS Runtime and Execution remain authoritative.
7. Vercel does not become the source of AIOS architecture.
8. No spending is authorized.
9. No provider-plan upgrade is authorized.
10. Production release remains subject to FS-09 and separate Founder authorization.

Rationale:

Per-request execution establishes a clear boundary between ephemeral deployment execution and durable AIOS state.

Static frontend plus Python API preserves the Full Stack application boundary while AIOS Runtime and Execution remain authoritative.

⸻

12. ARCHITECTURAL BOUNDARY STATEMENT

The ratification establishes the following boundary:

                    AIOS
                     │
       ┌─────────────┴─────────────┐
       │                           │
       ▼                           ▼
 Runtime / Execution          State Contract
       │                           │
       ▼                           ▼
Full Stack Adapter          Storage Interface
       │                           │
       ▼                           ▼
     Vercel                    Supabase

Therefore:

Vercel ≠ AIOS Runtime
Supabase ≠ AIOS State Architecture

They are infrastructure implementations behind governed AIOS interfaces.

⸻

13. IMPLEMENTATION AUTHORITY

Following formal registration of this ratification, Claude Code is authorized to implement the selected architecture within the boundaries of:

ACT-CC-POST-P13-AIOS-FULL-STACK-001
        +
FD-FS-001
        +
FS-ARCH-RAT-001

Claude Code may perform ordinary implementation, testing, repair, integration, verification, and redeployment necessary to satisfy the ratified architecture.

No additional Micro-Act is required merely to:

* implement the Supabase adapter;
* implement the Vercel deployment adapter;
* expose the frontend;
* create evidence-backed schema;
* deploy a preview;
* execute verification;
* repair ordinary implementation defects within authority;
* re-run FS-08 verification.

Any genuinely Architect-reserved or Founder-reserved matter remains subject to its existing authority boundary.

⸻

14. AUTO-ADVANCE AFTER RATIFICATION

After ratification, Claude Code SHALL NOT stop merely to request permission for the next ordinary technical step.

The execution sequence is:

FS-DP-01 RATIFIED
        +
FS-DP-04 RATIFIED
        ↓
IMPLEMENT
        ↓
VERIFY
        ↓
COMMIT
        ↓
VERCEL PREVIEW
        ↓
SUPABASE VERIFICATION
        ↓
LIVE SMOKE TEST
        ↓
FS-08 RE-DISCOVERY
        ↓
FS-08 EXIT GATE
        │
        ├── PASS
        │    ↓
        │  FS-09
        │
        └── FAIL
             ↓
          SELF-REPAIR
             ↓
          RE-VERIFY

This follows the autonomous execution model established by the parent Full Stack Act.

⸻

15. FS-08 EXIT CONDITION

FS-08 may be considered complete only when evidence demonstrates that the ratified infrastructure architecture is actually operational.

Required evidence includes, at minimum:

[ ] Vercel deployment surface exists
[ ] Static frontend reachable
[ ] Python API function reachable
[ ] API invokes existing Full Stack contracts
[ ] AIOS public contracts remain the integration boundary
[ ] Supabase persistence adapter operational
[ ] Evidence-backed schema exists
[ ] Persistent state survives restart/request boundaries
[ ] Function-local memory is not used as durable state
[ ] Security behavior preserved
[ ] Trace/audit behavior preserved where applicable
[ ] Failure handling verified
[ ] Certified-write protection preserved
[ ] Preview/live verification completed as applicable
[ ] No unauthorized certified-root modifications
[ ] Full regression suites pass
[ ] FS-08 re-discovery completed
[ ] No unresolved blocker within FS-08 scope

No evidence means no FS-08 closure.

No verification means no claim of successful infrastructure integration.

⸻

16. PRODUCTION BOUNDARY

This package intentionally stops before production release.

The intended lifecycle remains:

FS-08
Infrastructure & Cloud
        ↓
FS-09
Production Readiness
        ↓
Founder Release Decision
        ↓
FS-10
Deployment & Operationalization
        ↓
Operational AIOS

The Architect ratification in this package does not substitute for the Founder Release Decision.

⸻

17. FINAL STATUS

As of:

27 September 2026

the ratification status of this package is:

FS-DP-01
DATABASE / PERSISTENT STATE
        ↓
RATIFIED
OPTION A — SUPABASE
        ↓
Architect: Moriarty
FS-DP-04
DEPLOYMENT / RUNTIME
        ↓
RATIFIED
A1 — PER REQUEST
B1 — STATIC FRONTEND + PYTHON API FUNCTION
        ↓
Architect: Moriarty

Therefore:

FS-DP-01 = RATIFIED
FS-DP-04 = RATIFIED
Implementation = AUTHORIZED
FS-08 = CONTINUE EXECUTION

Production release remains:

NOT AUTHORIZED BY THIS PACKAGE

and remains subject to:

FS-09 PASS
        ↓
FOUNDER RELEASE DECISION
        ↓
FS-10

⸻

18. FINAL DIRECTIVE TO CLAUDE CODE

Treat FS-ARCH-RAT-001 as the consolidated Architect Ratification Package for:

FS-DP-01 — Database / Persistent State
FS-DP-04 — Deployment / Runtime

The selected architecture is:

DATABASE
AIOS State Contract
        ↓
Existing State / Storage Interface
        ↓
Supabase Persistence Adapter
        ↓
AIOS Supabase Project
DEPLOYMENT
HTTP Request
        ↓
Vercel Python Function
        ↓
AIOS Full Stack Adapter
        ↓
AIOS Public Contracts
        ↓
Runtime / Execution
        ↓
Persistent State
        ↓
Response

The deployment shape is:

STATIC FRONTEND
        +
PYTHON API FUNCTION

The runtime lifecycle is:

PER REQUEST

Architect:

Moriarty

Date:

27 September 2026

Proceed with implementation, verification, preview deployment, Supabase verification, live smoke testing, and FS-08 re-discovery under the existing Full Stack Act.

Do not create a Micro-Act for ordinary implementation work.

Do not spend money.

Do not upgrade provider plans.

Do not redefine AIOS Runtime or State architecture.

Do not bypass AIOS public contracts.

Do not modify certified P13 roots.

Do not reopen the closed Platform Organization.

Do not create Phase 14.

Do not claim Production Ready before FS-09.

Do not claim Operational AIOS before the complete governed deployment lifecycle is satisfied.

Continue automatically to FS-09 only when FS-08 evidence supports the transition.

NO EVIDENCE → NO CLOSURE.

NO VERIFICATION → NO CLAIM OF SUCCESS.

RATIFICATION → IMPLEMENTATION → VERIFICATION → RE-DISCOVERY → GATE → AUTO-ADVANCE.
````
