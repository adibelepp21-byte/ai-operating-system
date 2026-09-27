# `ACT-CC-POST-P13-AIOS-FULL-STACK-001` — FS-08 Vercel & Supabase Infrastructure Discovery, Verification & Repair Act (as received)

**Received:** from the Founder, 2026-09-27, in the message body.
**Stated status:** *"AUTHORIZED FOR EXECUTION UNDER EXISTING FULL STACK ACT"*.

Reproduced below as received. Its list items were rendered as bullets in the
message; they are kept as `*` bullets here.

````text
ACT-CC-POST-P13-AIOS-FULL-STACK-001

FS-08 VERCEL & SUPABASE INFRASTRUCTURE DISCOVERY, VERIFICATION & REPAIR ACT

Program: AIOS Full Stack Development & Operationalization
Parent Act: ACT-CC-POST-P13-AIOS-FULL-STACK-001
Founder Decision: FD-FS-001
Stage: FS-08 — Infrastructure & Cloud
Act Type: Continuous Stage Execution / Discovery / Verification / Authorized Repair
Status: AUTHORIZED FOR EXECUTION UNDER EXISTING FULL STACK ACT

⸻

1. PURPOSE

This Act authorizes Claude Code to continue the existing AIOS Full Stack program from the current FS-08 state.

A Vercel project has been created and a deployment has been performed.

The current deployment returns:

404 NOT_FOUND

This Act therefore establishes a controlled FS-08 investigation covering:

1. Vercel project and deployment;
2. Vercel build/runtime configuration;
3. AIOS repository structure and Full Stack entrypoints;
4. deployment adapter/configuration requirements;
5. Supabase project/database connectivity;
6. Supabase configuration relevant to the Full Stack;
7. external infrastructure dependencies;
8. authorized repair and redeployment;
9. live verification;
10. evidence and FS-08 status update.

This Act is not permission to redesign AIOS infrastructure.

⸻

2. GOVERNING PRINCIPLE

Claude Code MUST NOT guess the deployment architecture.

The execution sequence is:

DISCOVER
    ↓
OBSERVE
    ↓
CLASSIFY
    ↓
CHECK AUTHORITY
    ↓
REPAIR IF AUTHORIZED
    ↓
VERIFY
    ↓
REDEPLOY IF AUTHORIZED
    ↓
LIVE SMOKE TEST
    ↓
RECORD EVIDENCE
    ↓
RE-DISCOVER
    ↓
UPDATE FS-08

No implementation may be justified merely because it makes the deployment appear to work.

⸻

3. AUTHORITY BASIS

This Act operates under:

* ACT-CC-POST-P13-AIOS-FULL-STACK-001
* FD-FS-001
* existing AIOS Governance Baseline;
* existing authority matrix;
* existing Freeze §10;
* existing Full Stack FS-08 evidence model;
* existing decision-package structure.

The following remain Architect-reserved unless already explicitly ratified:

* Deployment architecture;
* Networking architecture;
* Database architecture;
* Identity and Authentication architecture;
* Scaling architecture;
* Observability architecture;
* Agent creation architecture where already identified as reserved.

MCP access does not expand these authorities.

⸻

4. PROVIDER SCOPE

Founder decision D3-A established:

Hosting

Vercel

Database

Supabase

Spending

NONE AUTHORIZED

Therefore:

Vercel
    = authorized named hosting provider
    ≠ unlimited deployment authority
Supabase
    = authorized named database provider
    ≠ unlimited database authority
MCP
    = execution/discovery interface
    ≠ authority expansion

⸻

5. VERCEL DISCOVERY

Claude Code SHALL discover the actual Vercel state.

5.1 Project Discovery

Using the available Vercel integration/MCP or other authorized interface:

* identify the Vercel team;
* identify the AIOS project;
* identify project ID;
* identify project name;
* identify repository binding;
* identify production branch;
* identify deployment history;
* identify latest deployment;
* identify deployment URL;
* identify current deployment status;
* identify framework preset;
* identify root directory;
* identify build configuration;
* identify output configuration;
* identify environment-variable configuration metadata without exposing secrets.

Do not disclose secret values in evidence.

⸻

5.2 Deployment Discovery

Inspect the latest deployment.

Record:

* deployment ID;
* commit SHA;
* branch;
* deployment state;
* build state;
* runtime state;
* deployment timestamp;
* deployment URL;
* relevant build/runtime errors;
* relevant routing errors.

Determine whether:

404 NOT_FOUND

originates from:

* incorrect root directory;
* missing output;
* missing route;
* missing function;
* unsupported runtime;
* incorrect framework detection;
* absent deployment adapter;
* incorrect Vercel configuration;
* application-level 404;
* deployment-level 404;
* another verified cause.

Do not classify the cause until evidence is obtained.

⸻

6. VERCEL LOG EVIDENCE

Claude Code MUST inspect available build/deployment/runtime logs.

The return package MUST distinguish:

Observed

Facts directly reported by Vercel.

Inferred

Technical interpretation supported by observed evidence.

Unknown

Information unavailable through the available interfaces.

No inferred cause may be reported as an observed fact.

⸻

7. AIOS REPOSITORY ENTRYPOINT DISCOVERY

Inspect the actual repository state.

Identify:

* Full Stack directory;
* backend entrypoint;
* frontend entrypoint;
* readiness gate;
* static assets;
* configuration files;
* dependency files;
* deployment configuration;
* existing runtime adapters;
* existing Vercel configuration, if any;
* existing cloud configuration, if any.

Specifically verify the implementation currently exercised locally.

The investigation MUST NOT assume that a locally executable Python server automatically maps to Vercel’s deployment model.

⸻

8. VERCEL COMPATIBILITY ANALYSIS

Compare:

AIOS actual entrypoint
        ↓
AIOS runtime assumptions
        ↓
Vercel supported deployment model
        ↓
Current Vercel configuration
        ↓
Observed deployment behavior

Classify the required action as exactly one of:

CLASS-A — CONFIGURATION-ONLY

Example:

* root directory;
* route configuration;
* build configuration;
* output configuration;
* deployment metadata.

May be repaired within existing authority if no Architect-reserved architecture is changed.

CLASS-B — AUTHORIZED IMPLEMENTATION

A deployment adapter or integration component is required and can be implemented without changing a reserved architectural decision.

May be implemented within current authority.

CLASS-C — ARCHITECT-RESERVED

The deployment requires a substantive architecture decision reserved to the Architect.

Claude Code MUST NOT self-ratify.

CLASS-D — EXTERNAL DEPENDENCY

The issue cannot be resolved from repository/configuration authority and requires an external account/provider action.

Record exact dependency.

CLASS-E — UNKNOWN

Evidence is insufficient.

Do not invent a resolution.

⸻

9. AUTHORIZED VERCEL REPAIR

If the issue is CLASS-A or authorized CLASS-B, Claude Code MAY:

* create or modify deployment configuration;
* create a deployment adapter;
* modify Full Stack deployment-specific files;
* add only necessary dependencies;
* update routing;
* update build configuration;
* commit;
* push;
* trigger a new deployment;
* perform live verification.

All modifications MUST:

* preserve AIOS architecture;
* preserve public AIOS contracts;
* avoid unnecessary dependencies;
* avoid certified-root modification;
* avoid modification of native_core/, consumers/, or tools/ unless strictly necessary and independently authorized;
* pass repository verification;
* preserve the certified-write barrier.

⸻

10. SUPABASE MCP DISCOVERY

The available Supabase MCP SHALL be used as an authorized discovery interface.

The purpose is to establish the actual Supabase state rather than infer it from documentation or prior assumptions.

Claude Code SHALL inspect, where available and authorized:

* connected Supabase project;
* project identity;
* project reference;
* project status;
* database connectivity;
* database availability;
* branches;
* database schema;
* tables;
* migrations;
* functions;
* extensions;
* relevant storage state;
* relevant authentication state metadata;
* relevant project configuration metadata;
* available logs/diagnostics;
* backup/recovery capabilities;
* plan information where exposed without billing changes.

Secret values MUST NOT be copied into repository evidence.

⸻

11. SUPABASE READ-ONLY FIRST RULE

The first Supabase pass MUST be read-only.

Claude Code MUST NOT initially:

* create tables;
* alter schema;
* run destructive SQL;
* create users;
* change authentication configuration;
* change RLS policies;
* create storage buckets;
* modify production data;
* create paid resources;
* upgrade plans;
* enable billable features.

The objective is:

DISCOVER SUPABASE
       ↓
VERIFY CONNECTIVITY
       ↓
VERIFY CURRENT STATE
       ↓
COMPARE WITH AIOS DATA/STATE MODEL

⸻

12. SUPABASE DATABASE ARCHITECTURE BOUNDARY

Database architecture remains Architect-reserved under the existing Full Stack authority model.

Therefore Claude Code may:

* inspect;
* document;
* classify;
* compare;
* identify missing state;
* prepare migration proposals;
* prepare database ADR material;
* test existing read-only interfaces.

Claude Code MUST NOT independently ratify:

* canonical schema;
* state ownership model;
* production migration architecture;
* database topology;
* persistence architecture;
* backup architecture;
* security policy architecture.

If implementation requires one of these decisions, update FS-DP-01 with evidence.

⸻

13. SUPABASE CONNECTIVITY FAILURE

If Supabase MCP cannot connect:

Do NOT conclude:

“Supabase is down.”

Instead record:

SUPABASE CONNECTIVITY STATUS:
UNVERIFIED / UNREACHABLE THROUGH AVAILABLE INTERFACE

Record:

* number of attempts;
* operations attempted;
* timestamps;
* error type;
* whether failure is network, authentication, project state, timeout, permission, or unknown.

Retry only where technically reasonable.

Do not create a loop of repeated retries.

⸻

14. SUPABASE REPAIR

If a Supabase issue is discovered, classify it before acting.

Allowed without new Architect decision

Only changes clearly within existing authority and explicitly non-architectural.

Architect-reserved

Any change affecting:

* database architecture;
* authentication architecture;
* authorization architecture;
* persistent state ownership;
* schema architecture;
* production migration strategy;
* backup/recovery architecture.

Spending-reserved

Any action requiring:

* plan upgrade;
* paid resource;
* billing commitment;
* commercial subscription;
* increased quota through paid tier.

Such actions MUST NOT be executed.

⸻

15. VERCEL + SUPABASE INTEGRATION ANALYSIS

After individual provider discovery, compare the two systems.

Determine whether the current AIOS Full Stack requires:

Vercel
  ↓
Backend / API
  ↓
Supabase

or another architecture supported by existing evidence.

Do not choose the topology merely because it is convenient.

If topology is Architect-reserved, update the relevant decision package instead of implementing the topology.

⸻

16. ENVIRONMENT VARIABLES

Inspect environment-variable requirements.

Classify every required variable as:

* public configuration;
* private secret;
* provider credential;
* database credential;
* AI provider credential;
* authentication secret;
* deployment configuration;
* unknown.

Never expose secret values in:

* commit messages;
* source code;
* logs;
* screenshots;
* evidence records;
* return package.

Do not create missing secrets merely to make deployment pass.

⸻

17. SPENDING CONTROL

The following actions are explicitly prohibited under D3-A unless a later Founder decision authorizes them:

* Vercel plan upgrade;
* Supabase plan upgrade;
* paid database resources;
* paid compute;
* paid storage;
* paid observability;
* paid authentication;
* paid third-party services;
* commercial domain purchase;
* billing commitment.

If a free-tier limitation blocks progress:

1. record the limitation;
2. identify its impact;
3. continue independent work;
4. route the spending decision to the appropriate authority.

⸻

18. CERTIFIED ROOT PROTECTION

Claude Code MUST preserve existing certified-root protection.

Before any new entrypoint or deployment tooling writes data, it MUST respect the repository’s certified-write barrier.

No deployment diagnostic may write into:

* certified evidence roots;
* protected architecture roots;
* immutable historical baselines.

Use temporary/external working directories for generated diagnostic state.

⸻

19. REPAIR AND REDEPLOYMENT

After an authorized repair:

CHANGE
 ↓
LOCAL TEST
 ↓
REPOSITORY TEST
 ↓
COMMIT
 ↓
PUSH
 ↓
VERCEL DEPLOY
 ↓
DEPLOYMENT VERIFICATION
 ↓
LIVE SMOKE TEST

Do not claim success merely because the deployment becomes READY.

⸻

20. LIVE SMOKE TEST

At minimum test:

Health

* root/health endpoint as applicable;
* deployment reachability.

Application

* actual frontend surface;
* actual backend endpoint;
* one valid request;
* one failure request.

Security

* unauthorized request behavior;
* hostile input behavior;
* no secret exposure.

Integration

Where available:

Frontend
 → Backend
 → AIOS public interface
 → Runtime/Execution
 → Result

If Supabase is part of the deployed path, test only the already-authorized integration surface.

⸻

21. NO PRODUCTION CLAIM

This Act MUST NOT by itself declare:

* Production Ready;
* Production Released;
* Operational AIOS.

A successful Vercel deployment means only that the deployment surface passed the relevant deployment tests.

FS-09 remains the production-readiness gate.

D4 remains the separate Founder Release Decision.

⸻

22. ARCHITECT ESCALATION

If a required change is Architect-reserved:

Claude Code SHALL produce:

1. exact technical question;
2. evidence;
3. affected components;
4. alternatives supported by evidence;
5. consequences;
6. current recommendation only if the existing governance format permits recommendations;
7. exact decision required;
8. affected decision package;
9. statement of what work can continue independently.

Claude Code MUST NOT write:

RATIFIED

until the appropriate authority has actually ratified the decision.

⸻

23. CONTINUOUS EXECUTION

Do not create a Micro-Act for:

* Vercel 404 diagnosis;
* Vercel configuration repair;
* Supabase connectivity investigation;
* ordinary deployment configuration;
* deployment verification;
* evidence recording.

These are part of FS-08 execution under the existing Full Stack Act.

Only genuinely authority-reserved decisions become escalation points.

⸻

24. REQUIRED RETURN PACKAGE

After execution, return:

A. Vercel Project

* project identity;
* team;
* project ID;
* repository binding;
* relevant configuration.

B. Vercel Deployment

* deployment ID;
* commit;
* URL;
* status;
* build status.

C. Exact 404 Cause

* observed evidence;
* interpretation;
* confidence/classification.

D. Repository Entrypoint

* actual backend entrypoint;
* frontend entrypoint;
* deployment entrypoint;
* configuration files.

E. Required Change

* configuration;
* adapter;
* code;
* Architect decision;
* external dependency;
* or unknown.

F. Authority Classification

Exactly one:

* AUTHORIZED;
* AUTHORIZED WITH BOUNDARY;
* REQUIRES FOUNDER DECISION;
* CONFLICT WITH CANONICAL SOURCE;
* OUTSIDE AUTHORITY;
* UNKNOWN AUTHORITY.

G. Files Changed

Include:

* path;
* change;
* reason;
* authority basis.

H. Deployment Result

* commit;
* deployment ID;
* status;
* URL;
* build result.

I. Live Smoke Test

* tests;
* results;
* failures;
* evidence.

J. Supabase State

* project;
* connectivity;
* database status;
* schema state;
* relevant configuration;
* limitations;
* unresolved issues.

K. Supabase MCP Evidence

Record:

* MCP operation;
* read/write classification;
* result;
* errors;
* timestamps where available.

L. External Dependencies

List unresolved:

* provider;
* account;
* credential;
* connectivity;
* plan;
* spending;
* domain;
* networking;
* other.

M. Architect Decisions

List each unresolved decision package.

N. FS-08 Status

Use only an evidence-supported state such as:

* FS-08 COMPLETE
* FS-08 COMPLETE WITH CLASSIFIED RESIDUAL
* FS-08 BLOCKED
* FS-08 PARTIALLY COMPLETE

Do not claim completion merely because Vercel accepts a deployment.

⸻

25. NEGATIVE CONTROLS

Claude Code MUST NOT:

1. guess the cause of the 404;
2. guess the Vercel runtime;
3. invent deployment architecture;
4. invent networking architecture;
5. invent database architecture;
6. self-ratify Architect decisions;
7. upgrade Vercel;
8. upgrade Supabase;
9. spend money;
10. create billing commitments;
11. expose credentials;
12. modify certified roots;
13. weaken the certified-write barrier;
14. bypass AIOS public interfaces;
15. directly modify native core merely to solve deployment convenience;
16. claim Vercel READY equals application success;
17. claim Supabase timeout equals provider outage;
18. claim production readiness;
19. claim Operational AIOS;
20. create a Micro-Act for ordinary FS-08 repair.

⸻

26. FINAL DIRECTIVE

Continue the existing AIOS Full Stack program from FS-08.

Investigate the actual Vercel deployment.

Determine the exact cause of the 404 NOT_FOUND.

Inspect and verify the real AIOS Full Stack entrypoints.

Use the available Vercel and Supabase MCP integrations for evidence-based infrastructure discovery.

Repair only what is within existing authority.

Prepare Architect decision packages where required.

Do not self-ratify Architect-reserved decisions.

Do not spend money.

Do not upgrade providers.

Do not redesign AIOS merely to satisfy a hosting provider.

After every authorized repair, verify locally, commit, push, redeploy where authorized, and perform a live smoke test.

Record all evidence.

Re-discover after material changes.

Continue independently wherever possible.

Stop only at the actual authority boundary or genuine external dependency.

This Act is an FS-08 execution continuation, not a new Micro-Act and not a new Phase.
````
