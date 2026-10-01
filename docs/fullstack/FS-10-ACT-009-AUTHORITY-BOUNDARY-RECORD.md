# FS-10 — Authority Boundary Record (ACT-009)

| Field | Value |
|---|---|
| **Act** | `ACT-CC-POST-P13-AIOS-FULL-STACK-009`, *FS-10 Founder-Reserved Boundary Reconciliation Act* (verbatim: `docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-009-…`) |
| **Register** | `§105` receipt · `§106` result |
| **Date** | 2026-10-01 |
| **Nature** | an authority map and a Founder Decision Package. **Classification is not a decision** (Act `§25`); nothing here authorizes a Production action (Act `§4`, `§24`) |
| **Production** | unchanged: observed before and after (`§10`); evidence `evidence/FS-10-ACT-009-PRODUCTION-STATE-2026-10-01.json` |

**Result: terminal state D — CONFLICT** on the next Production action (a Production deployment), with Founder-reserved items identified and their Founder Decision Package **READY**. Production is **UNCHANGED**. The full matrix is in `§7`.

Observed facts are marked **[OBS]**. Inference from sources is marked **[INF]**. Nothing here is marked as a decision, because none was taken.

## 1. Sources and their status (Act `§5`)

The authority precedence is F06 `§3`: Constitution → Founder Authority / Founder Decisions → Governance Baseline → Canonical Architecture → Master Program / Phase Authority → … → Charter → Mandate → Matrix → Execution.

| # | Source | Path | Status | Used for |
|---|---|---|---|---|
| 1 | FS-10 deployment document | `docs/fullstack/FS-10-DEPLOYMENT.md` (sha256 `b9710fca…`, commit `b586a9b`) | **CURRENT; execution / preparation document, not an authority** (written by Claude under ACT-008) | reviewed in `§2` |
| 2 | FS-10 / FS-09 execution records | `FS-09-ACT-008-EXECUTION-RECORD.md`; `FS-09-OPERATIONAL-RUNBOOK.md` `§14`; `FS-09-OPERATIONAL-OWNERSHIP.md` | **CURRENT records; not authority.** The ownership model states *"No new Founder authority is created by this operational model"* (ACT-004 `§37`) | evidence of historical reasoning only |
| 3 | Governance Baseline | `cofounder-v2/F03_…AMENDMENT.md` (`AIOS-GOV-BASELINE-AMENDMENT-V2-001`) · `AIOS_POST_V2_OPERATIONAL_BASELINE_v1.0.md` | **CANONICAL, CURRENT** (V2 registered and active 2026-09-23; the body's *"PENDING"* wording is historical text, `cofounder-v2/README.md`) | reserved matters R01–R09 (`§4.1`) |
| 4 | Co-Founder Delegation Charter V2 | `cofounder-v2/F04_…CHARTER_V2.0.md` | **CANONICAL, CURRENT** | `§26` reserved authority; `§24` escalation triggers |
| 5 | CEO Operating Mandate V2 | `cofounder-v2/F05_…MANDATE…V2.0.md` | **CANONICAL, CURRENT** | `§42` irreversible actions; `§43` security boundary |
| 6 | CEO Authority / Escalation Matrix V2 | `cofounder-v2/F06_…MATRIX_V2.0.txt` | **CANONICAL, CURRENT** (registered and active 2026-09-24, Delegation Register `§13`) | A01–A23; `§30` reserved matrix; `§36` unknown authority |
| 7 | Founder Decision & Authority Transition Record | `cofounder-v2/F02_…TRANSITION_RECORD.txt` | **CANONICAL, CURRENT** (`FD-V2-001`…`013`) | `§19` Founder reserved authority |
| — | Registration and Activation Record | `AIOS_COFOUNDER_V2_REGISTRATION_AND_ACTIVATION_RECORD_v1.0.md` | **CANONICAL, CURRENT** | `§C.5` reserved union; `§C.6` standing decisions (`SD-7` spent Acts are not reused); `§C.7` escalation triggers |
| 8a | `FD-FS-001` (D1-A · D2-A · D3-A · D4-A · D5-A) | Register `§62`; record `acts/ACT-CC-POST-P13-AIOS-FULL-STACK-001-D1-D5-EXECUTION.md` | **CANONICAL Founder Decision, CURRENT, standing** (not superseded by any later instrument) | release (D4-A), spending (D3-A), Architect-reserved areas (D2-A) |
| 8b | `ACT-CC-POST-P13-AIOS-FULL-STACK-001` (Full Stack Act) | `acts/…-001-FULL-STACK-DEVELOPMENT-AND-OPERATIONALIZATION.md` | **CANONICAL, CURRENT** (operative since `§62`) | `§6.3` Founder-reserved matters; `§7.1` credential boundary; `§30` when Founder intervention is requested |
| 8c | `ACT-CC-POST-P13-AIOS-FULL-STACK-003`, issued | `acts/…-003-FINAL-FOUNDER-AUTHORIZATION.md` (Register `§78`) | **CANONICAL, CURRENT** parent Act; its terminal state (`§30`) is not reached | `§4.8`, `§12`–`§14`, `§20`–`§24`, `§28`, `§33`, `§34` |
| 8d | `ACT-003`, proposed text | `acts/…-003-FULL-STACK-COMPLETION-TO-OPERATIONAL-AIOS.md` (Register `§77`) | **SUPERSEDED** by 8c | not used as authority |
| 8e | Founder decisions recorded under ACT-004 (`ACT-004-DG-01`…`05`) | Register `§93` | **CANONICAL Founder Decisions, CURRENT** | N1 networking with form X2; L1/M1/R2; E1; P2 |
| 8f | ACT-004 … ACT-008 as Acts | `acts/…-004` … `-008` | **SPENT** (their terminal states were reached; `SD-7`). Their recorded decisions stand; their grants (e.g. ACT-004 `§56`, ACT-008 `§10.2`, ACT-008 `§28`) are not reused as authority (Act `§16`) | decisions only |
| 8g | `FS-ARCH-RAT-001` (FS-DP-01, FS-DP-04) | Register `§68` | **CANONICAL Architect ratification, CURRENT** | `§11.2`: A1 + B1, conditions 8–10 |
| 8h | FS-DP-02 B3, FS-DP-05 C1 | Register `§79`, `§81` | **CANONICAL Architect decisions, CURRENT** | authentication mechanism |
| 8i | Decision packages `FS-DP-01`…`07`, `FS-09-ENV`, `FS-09-RUNTIME` | `docs/fullstack/decision-packages/` | **analysis; only the recorded selection carries authority** | context |
| 9 | FS-08 / FS-09 records | `FS-08-*`, `FS-09-*` | **HISTORICAL / CURRENT records** | Register `§67`: *"every merge to the default branch deploys to public production"* |
| 10 | Production / infrastructure state | read now through the Vercel and Supabase connectors | **[OBS] CURRENT** | `§10` |

**Not found:** no canonical source names the persons who may hold Production access, and none assigns Production rollback after a release (`§3`, rows C and P).

## 2. FS-10-DEPLOYMENT.md, as resident (Act `§6`)

It was read and **not modified** (sha256 before and after, `§10`). Its statements, tested against the sources above:

| Statement in FS-10 | What it says | Authority level | Status | Actually Founder-reserved? | Evidence |
|---|---|---|---|---|---|
| Objective / status | FS-10 ACTIVE, Deployment Preparation, entered on FS-09 PASS/CLOSED | record of ACT-008 `§27` (spent) | CURRENT | n/a | Register `§104` |
| Sequence | Deployment Preparation → Production Deployment → Smoke → Health → Integration → Production Verification → Operational Verification → FRA → LIVE | copies ACT-003 `§20` | CURRENT | — | ACT-003 `§20` |
| Production deployment is a Founder-reserved operator action | in `§1` and the sequence | execution note | **contradicted in part** | **Not established as such.** Two Founder instruments disagree about whether it needs a Founder decision first: **CONFLICT** (`§3` row E) | FD-FS-001 record `§5`, `§9` item 9 vs ACT-003 `§4.8`, `§20`, `§33` |
| Production credentials are Founder-reserved (P1, P2) | operator sets them on a Founder decision | execution note | **corrected** | **No.** ACT-001 `§7.1` classes Founder-owned credentials as a *"GENUINE EXTERNAL DEPENDENCY"*: **EXTERNAL-CONTROL**, timed by row E | `§3` rows A, B, I |
| Deployment Protection is a Founder decision (P5) | a decision for the Founder | execution note | **corrected** | **No.** Already decided: N1 with form X2, protection on every deployment, Production included (`ACT-004-DG-01`, `§8` delegation). Changing it is **ARCHITECT-RESERVED** | `§3` row G |
| Release candidate is the Founder's to name (P6) | Founder names it | execution note | **corrected** | **No** for identification (ACT-001 `§20`: FS-09 exit has the release artifact identified; D4-A's option text has Claude submit the release package). **Yes** for its approval, which is the release decision | `§3` row F |
| Smoke write policy is a Founder decision (P7) | Founder decides | execution note | **corrected** | **No.** ACT-003 `§20` places integration testing and Production verification before the release authorization, inside the executed FS-10 sequence; no source reserves test writes | `§3` row K |
| Alerting cadence (P8) | Founder / operator | execution note | **corrected** | **No** for the cadence of H3 checks (an ordinary operational decision, F06 A09). A move to H1/H2 is **ARCHITECT-RESERVED** (D2-A observability), with D3-A if paid | `§3` row O |
| Rollback is the Founder's (P9) | Founder | execution note | **not established** | **UNKNOWN** after a release; before a release it is a Production deployment (row E) | `§3` row P |
| FRA and LIVE are the Founder's | `§1` | ACT-003 `§21`; D4-A | CURRENT | **Yes** | `§3` row T |
| Stop condition | no Production step until the Founder decisions exist | execution note | **corrected** | the real stop is the conflict in row E and the Founder-reserved items in `§6` | `§3`, `§6` |

FS-10-DEPLOYMENT.md therefore over-escalates P5, P6, P7 and P8 and labels P1 and P2 wrongly. Under Act `§6` it stays unaltered here; its correction is a later, recorded edit (`§9`).

## 3. Inventory and classification (Act `§7`–`§13`, `§20`)

One primary state per action. *Decision owner* is who decides; *execution owner* is who acts. **[OBS]** marks a fact read now, and everything else is reasoning from the cited source.

### A. Production credentials (the Production database secret, custody)
* **Source:** ACT-001 `§7.1` (*"Founder-owned credentials … unavailable secret"* → *"GENUINE EXTERNAL DEPENDENCY"*, *"not treated as an architecture Micro-Act"*); ACT-003 `§13` (the Founder configures the secret; Preview only), `§28` (secrets stay outside chat, Act bodies, Git, logs and evidence).
* **[OBS]** no Production variable exists (`hiddenProductionEnvCount: 0`); the session holds no Production key.
* **Reasoning:** custody belongs to the account holder; no source makes *having* the credential a Founder decision. When it may be put to use depends on row E.
* **Counter-evidence:** runbook `§14` lists credentials under *Founder*; it is an execution artifact, not an authority.
* **Final: EXTERNAL-CONTROL.**

### B. Production secrets — insertion into the Vercel Production scope
* **Source:** ACT-003 `§13` (*"The Founder may configure: SUPABASE_SECRET_KEY"*, target *"Preview only"*, type *"Sensitive"*; nothing in the issued Act covers a Production secret); `§28`; ACT-001 `§7.1`.
* **Reasoning:** the value may not pass through the session (`§28`), so the account holder inserts it. Timing follows row E.
* **Final: EXTERNAL-CONTROL.**

### C. Production operator identity / token
* **Source:** FS-DP-02 **B3** (Architect decision, Register `§81`): operator bearer tokens, hashes in `AIOS_OPERATOR_TOKENS`, the plaintext kept by the holder; ACT-003 `§28`.
* **Reasoning:** the *mechanism* is ratified. **Which persons may hold Production access, with which scopes,** is named by no canonical source; it is neither an ordinary operational choice nor a listed reserved matter.
* **Counter-evidence:** the ownership model says the operator issues tokens; it creates no authority.
* **Final: UNKNOWN** (escalation `ESC-01`, `§6`).

### D. Production database selection / wiring
* **Source:** `ACT-004-DG-04` (E1, Register `§93`); implemented and verified under ACT-004/ACT-008.
* **[OBS]** Production project `hmljfyqycxcueulhsjae`: migration `20260928051800_aios_records` applied, **0 rows**; the resolver maps `VERCEL_ENV=production` to it.
* **Final: CEO-AUTHORIZED** (done; no action pending).

### E. Production deployment (including a merge to the default branch, a promotion, or a Production-target deployment)
* **[OBS]** the default branch is `claude/aios-genesis-planning-hmbvlc` at `22c0b49`; the only Production deployment `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` was built from it. **[INF]** a merge into it builds a Production deployment (Register `§67`; FS-DP-04 package point 4).
* **Source 1 — FD-FS-001** (Founder Decision, 2026-09-26): D4-A *"Production release requires a separate Founder decision at the FS-09 release gate."* Its record `§5`: *"FS-09 Production Readiness PASS → Founder Release Decision → FS-10 Deployment / Operationalization"*; `§9` item 9: *"At FS-10, execute only after the required release decision exists."* FS-DP-04's ratified conditions (`FS-ARCH-RAT-001` `§11.2` cond. 10): *"Production release remains subject to FS-09 and separate Founder authorization."*
* **Source 2 — ACT-003, issued** (Founder Act, 2026-09-27): `§4.8` *"Upon successful FS-09 closure, continue into FS-10 Deployment"* as authorized scope; `§20` *"FS-10 may begin only after: FS-09 = PASS"* with *DEPLOY → SMOKE → HEALTH → INTEGRATION → PRODUCTION VERIFICATION → OPERATIONAL VERIFICATION → FOUNDER RELEASE AUTHORIZATION → LIVE*; `§33` (its execution diagram runs FS-10 DEPLOYMENT, then PRODUCTION VERIFICATION, then *"STOP AT FOUNDER RELEASE AUTHORIZATION"*); `§23` lists *"Production deployment without authorization"* as a negative control without naming which authorization.
* **Reasoning:** both are Founder-level instruments. Under Source 1 a Production deployment waits for a Founder decision. Under Source 2 it is authorized after FS-09 PASS, and the Founder's decision comes after Production verification. F04 `§19.2` governs a conflict with *"a currently valid Founder Decision"*: *"do not silently override the decision"*; *"determine whether a later Founder Decision supersedes it"*; *"if not, escalate where required."* **[OBS]** the issued ACT-003 names neither FD-FS-001 nor D4-A, and states no supersession (its only supersession is of its own proposed text); nor do ACT-004 or ACT-008. **[INF]** supersession cannot be established, so the route is escalation, not a choice by the CEO. ACT-008 `§27`–`§28` repeats Source 2's order but defers to *"actions already authorized by the parent Full Stack program"* and is spent. Precedence (F06 `§3`) does not separate two Founder instruments.
* **Route:** *"Two higher-order sources conflict and precedence cannot resolve it"*, routed to *"Founder decision"* (Registration Record `§C.7` trigger 6; F04 `§24`).
* **Final: CONFLICT** → `FDP-009-01`.

### F. Deployment candidate / release commit
* **Source:** ACT-001 `§20` FS-09 exit *"release artifact identified"*; FD-FS-001 D4-A option effect *"At FS-09 exit Claude submits a release package"*; ACT-003 `§21`, `§24` (no self-release).
* **[OBS]** the verified served commit is `d05261c` (FS-09 record).
* **Reasoning:** identifying and submitting the candidate is execution; approving it for release is the Founder's release decision (row T).
* **Counter-evidence:** FS-10 P6 says the Founder names it (an execution note).
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY** (identify and submit; identification ≠ approval).

### G. Deployment Protection stance
* **Source:** `ACT-004-DG-01` (Founder decision: N1) and ACT-004 `§8` (*"Claude is authorized to select the implementation form that satisfies N1"*), under which **X2** was selected: protection on every deployment, Production included; no custom domain (Register `§93`). D2-A: networking stays Architect-reserved.
* **[OBS]** `ssoProtection` enabled, `all_except_custom_domains`; no custom domain; the Production URL answers 401/302 without Vercel access.
* **Architectural question:** whether Production's edge is private (X2) or public (X1/X3). **Owner:** the holder of Architect authority (the Founder acted as Architect in ACT-004; `FD-2` is open). **Frozen invariant changed?** No. **Founder escalation?** Only through the Architect role, or if a change requires spending (D3-A).
* **Final: ARCHITECT-RESERVED** (decided; compliant now). Applying a setting is external control (row W).

### H. Domain / Production alias
* **Source:** FS-DP-03 Part B (default domain; a custom domain needs DNS ownership); X2 *"no custom domain"*; D2-A networking; D3-A (no spending).
* **Reasoning:** the default Production alias moves with a Production deployment (row E); a custom domain is a networking decision and an external DNS action.
* **Final: ARCHITECT-RESERVED** (custom domain; none planned).

### I. Environment-variable activation (Production scope)
* **Source:** as A and B; E1 (`ACT-004-DG-04`) fixes which store Production uses.
* **[OBS]** none exist in Production scope.
* **Final: EXTERNAL-CONTROL** (account holder; timing follows row E).

### J. Production smoke policy (read-only checks)
* **Source:** ACT-003 `§20` (SMOKE TEST in the FS-10 sequence); F06 A11 (verification), A12 (evidence).
* **Boundary:** only against an authorized Production deployment (row E); under X2 the API checks need an access path, which is Founder-reserved (row X1); the connector's GET-only fetch reaches health only.
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY.**

### K. Production smoke write behavior (test runs written to the Production store)
* **Source:** ACT-003 `§20` (INTEGRATION TEST, PRODUCTION VERIFICATION, before the release authorization), `§24` (verification ≠ authorization).
* **Reasoning:** no source reserves test writes. The append-only store makes them permanent (F05 `§42`: for irreversible actions *"verify … whether Founder authority is required"*); F04 `§24` reserves an *irreversible **strategic*** decision, and labelled verification records are not strategic.
* **Counter-evidence:** FS-10 P7 called it a Founder decision; that is an execution note.
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY** (only after an authorized deployment; minimum writes, each labelled; never to gain evidence for its own sake).

### L. Production health verification
* **Source:** ACT-003 `§20`; F06 A11.
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY** (after row E; through an authorized path).

### M. Production integration verification
* **Source:** ACT-003 `§20`, `§22`; F06 A11.
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY** (as K).

### N. Production monitoring (L1, M1, R2)
* **Source:** `ACT-004-DG-02` (L1/M1/R2 ratified; *"Claude may implement the complete L1/M1/R2 observability architecture without further Architect approval"*); F06 A03, A11.
* **Final: CEO-AUTHORIZED** (reading logs and metrics through authorized connectors; adds no monitor).

### O1. Alerting cadence (H3 manual checks once Production serves)
* **Source:** alerting H3 in force (`ACT-008-DG-02`, Register `§101`); F06 A09 (*"operational prioritization"*, sequencing); ACT-004 `§37` (monitoring in the ownership model).
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY** (cadence and executor of the checks; no automatic alert is created).

### O2. Alerting mechanism or recipients (H1/H2; who is paged)
* **Source:** D2-A (observability architecture is Architect-reserved); D3-A (no spending); ACT-001 `§7.1` (third-party account = external dependency).
* **Final: ARCHITECT-RESERVED** (not required while H3 stands).

### P. Rollback authority (Production)
* **Source:** ACT-003 `§12` forbids rolling back Production *"merely to gain evidence"*; no issued source assigns rollback authority. The *"execute authorized rollback if the rollback path is already approved"* text is in the **superseded** proposed ACT-003 and is not used.
* **Reasoning:** before a release, a rollback is a Production deployment (row E); after a release, no owner is established.
* **Final: UNKNOWN** (escalation `ESC-02`).

### Q. Roll-forward authority
* **Reasoning:** a roll-forward is a Production deployment.
* **Final: CONFLICT** (as row E).

### R. Production incident authority
* **Source:** F06 A03, A11, A12, A16; ACT-003 `§27` (identify, freeze dependent action, record, escalate); F05 `§43`.
* **Boundary:** investigate, contain within existing authority, record, escalate; containment that changes Production follows rows E, P, B.
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY.**

### S. Production traffic activation (making Production reachable by its users)
* **Source:** ACT-003 `§21` (*"Production Release remains Founder-reserved"*); D4-A. Under X2 the Production edge is private, so public reachability also needs an Architect change (row G).
* **Final: FOUNDER-RESERVED** (part of the release) → `FDP-009-02`.

### T. Production release / Founder Release Authorization
* **Source:** FD-FS-001 D4-A; ACT-003 `§21`, `§24`, `§34`, `§35` (*"This authorization does not constitute Production Release Authorization"*); ACT-001 `§6.3`, NC-25; ACT-004 `§67`; F04 `§26` item 10 (*"decisions explicitly designated Founder-only by … Founder Decision"*).
* **Test met:** 9.1 (explicit reservation) and 9.3 (release boundary).
* **Final: FOUNDER-RESERVED** → `FDP-009-02`.

### U. Operational AIOS activation (recording the operational state)
* **Source:** ACT-003 `§22` (*"Only then may the operational state be recorded"*, after FS-10 verified, Production verified and the Founder Release Authorization); ACT-001 `§31`.
* **Final: CEO-AUTHORIZED-WITH-BOUNDARY** (recording, only once every condition holds; the conditions include a Founder decision). Final System Acceptance is separate (row X4).

### V. Billing / paid infrastructure
* **Source:** FD-FS-001 D3-A (*"no spending authorization is granted"*; *"Any action that creates a monetary commitment must stop and escalate"*); `FS-ARCH-RAT-001` `§11.2` conditions 8–9; ACT-004 `§57`.
* **Test met:** 9.1. **Already decided** (no spending); no paid action is planned.
* **Final: FOUNDER-RESERVED** → `FDP-009-04` (standing; no new decision pending).

### W. External-provider control actions (project and team settings, production branch setting, plan, connector permissions, account membership)
* **Source:** ACT-001 `§7.1`, `§7.2` (*"Access to an MCP does not itself authorize an action that governance does not authorize"*); ACT-003 `§12` (Founder-side actions on the Vercel connector).
* **[OBS]** every deployment and variable was created by the account `adibelepp21-byte`.
* **Final: EXTERNAL-CONTROL.**

### Additional actions found

| ID | Action | Source | Final |
|---|---|---|---|
| X1 | Temporary access to Production past Vercel SSO (bypass or shareable link) for verification | ACT-003 `§12` (*"Claude shall not:"* … *"bypass Vercel access controls"*; *"circumvent SSO"*), `§14` (*"No protection bypass may be invented or executed without authorization"*; access through the connector or a *"Founder-created authorized protection/access configuration"*). Every earlier bypass was granted by a named Founder Act (ACT-004 `§56`, ACT-008 `§10.2`, Preview only), both spent | **FOUNDER-RESERVED** → `FDP-009-03` |
| X2 | Changing Vercel's production branch (release control: today every merge to the default branch deploys Production) | D2-A (deployment architecture); FS-DP-04 decision note recorded the question as open; `FD-2` open | **ARCHITECT-RESERVED** (only needed if `FDP-009-01` is answered so that merges must not deploy) |
| X3 | Production store backup before a release (read-only export) | FS-DP-01 point 6, ratified (`FS-ARCH-RAT-001`); runbook `§7` | **CEO-AUTHORIZED-WITH-BOUNDARY** (read-only; never restored into Production) |
| X4 | Final System Acceptance (A19) | F06 A19, `§30`; F04 `§26` item 9; F03 R08 | **FOUNDER-RESERVED** → `FDP-009-05` (not due) |
| X5 | Production schema change / migration | D2-A (database); FS-DP-01 ratified; **[OBS]** schema equal to Preview, one migration, none pending | **ARCHITECT-RESERVED** (none required) |

## 4. The five previously identified items (Act `§13`)

| # | Item | Proposed earlier (FS-10 `§3`) | Canonical basis | Actual owner | Why | Counter-evidence | Final |
|---|---|---|---|---|---|---|---|
| 1 | Production credentials | Founder decision (P1, P2) | ACT-001 `§7.1`; ACT-003 `§13`, `§28` | account holder (custody and insertion); timing per row E | credentials are an external dependency by the Act's own words, not a decision | runbook `§14` (execution artifact) | **EXTERNAL-CONTROL** |
| 2 | Deployment Protection stance | Founder decision (P5) | `ACT-004-DG-01` + `§8` delegation → X2 | Architect (to change); account holder (to apply) | already decided; protection stays on Production | ownership model *"protection settings are the operator's"* (custody, not decision) | **ARCHITECT-RESERVED** (decided) |
| 3 | Release candidate commit | Founder names it (P6) | ACT-001 `§20`; D4-A option effect | CEO identifies and submits; the Founder approves in the release decision | identification is execution | none canonical | **CEO-AUTHORIZED-WITH-BOUNDARY** |
| 4 | Smoke write policy | Founder decision (P7) | ACT-003 `§20` | CEO, after an authorized deployment | integration testing is inside the authorized sequence; not strategic | permanence (F05 `§42`) weighed and found not strategic | **CEO-AUTHORIZED-WITH-BOUNDARY** |
| 5 | Alerting cadence | Founder / operator (P8) | F06 A09; H3 in force | CEO (cadence); Architect (mechanism) | an ordinary operational schedule | H1/H2 recipients would be Architect-reserved, plus D3-A | **CEO-AUTHORIZED-WITH-BOUNDARY** (O1) |

## 5. Preparation ≠ Deployment ≠ Verification ≠ Release ≠ Authorization ≠ Operational (Act `§14`)

| Transition | Who decides | Who executes | Who verifies | Evidence required |
|---|---|---|---|---|
| **Preparation** (tooling, pre-flight, candidate, Preview work) | CEO (F06 A01, A02, A09; ACT-003 `§4.8` preparation) | CEO | CEO | tests, records |
| **Production Deployment** | **CONFLICT**: Founder first (FD-FS-001 D4-A record) **or** authorized after FS-09 PASS (ACT-003 `§4.8`, `§20`) → `FDP-009-01` | CEO for repository and deployment steps; the account holder for credentials and variables (rows A, B, I) | CEO | the candidate commit and its build; Production variables present (names only); `VERCEL_ENV` resolution |
| **Production Verification** (smoke, health, integration) | CEO (ACT-003 `§20`; F06 A11) | CEO, through the connector (GET) and an access path for authenticated checks (`FDP-009-03`) | CEO | the smoke record; L1 lines; Production store rows written by verification, labelled |
| **Production Release** (traffic, LIVE) | **Founder** (row T, S) | as the Founder directs; edge changes need the Architect (row G) | CEO | release package; verification evidence |
| **Founder Release Authorization** | **Founder** | Founder | — | the Founder's instrument |
| **Operational AIOS** | conditions in ACT-003 `§22`; recording by the CEO once they hold; **Final System Acceptance stays the Founder's** (A19) | CEO records | CEO; Founder accepts | the full chain of evidence |

## 6. Founder Decision Package (Act `§15`)

No option below is recommended. F06 `§5` (E3) and `§38` would permit a CEO recommendation, but none is given, so that no decision is embedded in its presentation.

### FDP-009-01 — Order of Production deployment and the Founder release decision

| Field | Content |
|---|---|
| **Decision ID** | `FDP-009-01` |
| **Decision Subject** | whether a Production deployment (before any release) needs a Founder decision first |
| **Exact Decision Required** | the Founder states which governs FS-10: **(i)** FD-FS-001 D4-A as recorded: the Founder Release Decision comes **before** any Production deployment (record `§5`, `§9` item 9); **or (ii)** ACT-003 `§4.8`/`§20`/`§33`: Production deployment, smoke, health, integration and Production verification are authorized after FS-09 PASS, and the Founder Release Authorization comes **after** Production verification, before LIVE. Or another arrangement the Founder states |
| **Why This Is Founder-Reserved** | two Founder instruments conflict, precedence does not resolve them, and no later Founder decision states that it supersedes D4-A (F04 `§19.2`: *"if not, escalate where required."*; Registration Record `§C.7` trigger 6; F04 `§24`); resolving a conflict between Founder decisions is Founder authority (F02 `§19` item 9; F03 R07) |
| **Canonical Authority** | FD-FS-001 (Register `§62`); ACT-003 issued (Register `§78`); F04 `§24`; Registration Record `§C.6`, `§C.7` |
| **Relevant Existing Decisions** | D4-A; ACT-003 `§35` (*"does not constitute Production Release Authorization"*); `FS-ARCH-RAT-001` `§11.2` cond. 10; `ACT-004-DG-01` (X2: Production's edge stays private) |
| **If (i)** | Production deployment waits for the Founder Release Decision; after it, the CEO deploys and verifies; the release package (row F) is what the Founder decides on |
| **If (ii)** | the CEO may deploy to Production and verify it after FS-09 PASS (already met), once the account holder has set the Production variables (rows A, B, I) and an access path exists (`FDP-009-03`); the release to LIVE stays with the Founder (`FDP-009-02`). Under X2 the deployment stays private |
| **If neither is stated** | row E stays **CONFLICT**; no Production deployment, roll-forward or merge to the default branch |
| **What Remains CEO-Autonomous** | preparation; Preview work; identifying and packaging the release candidate (row F); correcting FS-10-DEPLOYMENT.md; read-only Production observation |
| **What Evidence Already Exists** | FS-09 PASS / CLOSED with its record; the served commit `d05261c` verified live on Preview; the smoke tool (8 tests); Production store migrated and empty |
| **What Evidence Is Still Needed** | none for the decision itself. For a deployment: the Production variables, the candidate's Preview build of the same commit, the release package |

### FDP-009-02 — Production Release (Founder Release Authorization, traffic activation)

| Field | Content |
|---|---|
| **Decision ID** | `FDP-009-02` |
| **Decision Subject** | releasing AIOS to Production use (LIVE) |
| **Exact Decision Required** | AUTHORIZE / DO NOT AUTHORIZE the release of a named, verified candidate, and state what *LIVE* means for reachability: under the ratified X2 Production is reachable only by people with Vercel access; a public Production needs an Architect change of FS-DP-03 (row G) |
| **Why This Is Founder-Reserved** | explicit reservation and release boundary (tests 9.1, 9.3): D4-A; ACT-003 `§21`, `§24`, `§34`, `§35`; ACT-001 `§6.3`, NC-25 |
| **Canonical Authority** | as above |
| **Relevant Existing Decisions** | D4-A; ACT-003 `§35`; `ACT-004-DG-01` (X2); FS-09 PASS (`§103`), which is not a release |
| **What Happens If Approved** | the CEO executes the release as directed, verifies post-release (ACT-003 `§22`), and records the operational state only when every `§22` condition holds |
| **What Happens If Rejected** | Production stays as it is; FS-10 stays at the release boundary (ACT-003 `§29`: *"the program remains at the release boundary"*) |
| **What Remains CEO-Autonomous** | everything before the release under the answer to `FDP-009-01` |
| **What Evidence Already Exists** | FS-09 evidence; nothing yet from Production |
| **What Evidence Is Still Needed** | Production deployment and Production verification evidence (rows E, J–M); the release package (row F) |
| **Timing** | **not decidable yet**: it needs Production verification evidence, which needs `FDP-009-01` |

### FDP-009-03 — Temporary access to Production for verification

| Field | Content |
|---|---|
| **Decision ID** | `FDP-009-03` |
| **Decision Subject** | an authorized path for the CEO to run authenticated checks against a protected Production deployment |
| **Exact Decision Required** | whether a temporary, Production-scoped access instrument (an automation bypass revoked after use, or a Founder-created access configuration) may be used for FS-10 verification, and on what conditions; or that Production verification is limited to what the connector can reach (GET only: health) |
| **Why This Is Founder-Reserved** | ACT-003 `§12` and `§14` forbid bypassing Vercel access controls without authorization and name the Founder-created configuration as the authorized form; each earlier instrument was granted by a Founder Act (ACT-004 `§56`; ACT-008 `§10.2`, Preview only, spent) |
| **Canonical Authority** | ACT-003 `§12`, `§14`, `§23`; F05 `§43` |
| **Relevant Existing Decisions** | `ACT-004-DG-01` (X2: Production is protected) |
| **What Happens If Approved** | the CEO runs `python -m fullstack.deploy.smoke` against Production within the stated conditions, revokes the instrument and verifies it absent, as at FS-09 |
| **What Happens If Rejected** | Production verification covers health only (GET through the connector); authenticated smoke and integration checks are not run on Production, and the evidence says so |
| **What Remains CEO-Autonomous** | read-only checks through the authorized connector |
| **What Evidence Already Exists** | the FS-09 bypass lifecycle (created, used, revoked, verified absent) as precedent |
| **What Evidence Is Still Needed** | an authorized Production deployment (`FDP-009-01`) |

### FDP-009-04 — Spending (standing)

| Field | Content |
|---|---|
| **Decision ID** | `FDP-009-04` |
| **Decision Subject** | paid plans, paid alerting, paid domains, any monetary commitment |
| **Exact Decision Required** | **none now.** D3-A stands: no spending. A decision is needed only if a paid action is proposed; none is |
| **Why This Is Founder-Reserved** | D3-A (explicit), `FS-ARCH-RAT-001` `§11.2` cond. 8–9, ACT-004 `§57` |
| **What Happens If Approved / Rejected** | n/a while nothing paid is proposed |
| **What Remains CEO-Autonomous** | free-tier and already-paid capacity |
| **Evidence** | **[OBS]** no purchase, plan or billing call was made in this Act; the plans in force were not changed |

### FDP-009-05 — Final System Acceptance (A19)

| Field | Content |
|---|---|
| **Decision ID** | `FDP-009-05` |
| **Decision Subject** | Founder acceptance of the system |
| **Exact Decision Required** | **none now**; due only after LIVE and operational verification |
| **Why This Is Founder-Reserved** | F06 A19, `§30`; F04 `§26` item 9; F03 R08 |
| **Evidence Still Needed** | the full FS-10 chain |

### Escalations: UNKNOWN authority (not Founder decisions by classification)

| ID | Question | Why UNKNOWN | Affected |
|---|---|---|---|
| `ESC-01` | Who may hold Production access, with which scopes? (row C) | B3 fixes the mechanism; no canonical source names the principals | Production variables (row I); authenticated Production checks |
| `ESC-02` | Who may roll Production back after a release? (row P) | no issued source assigns it; the only text is in the superseded proposal | incident handling after LIVE |

They are escalated under F06 `§36` step 5; the Founder may answer them or assign the answer.

### Architect-reserved items (route to the holder of Architect authority)

| Item | State | Needed now? |
|---|---|---|
| G Deployment Protection (X2) | decided | no |
| H custom domain | not planned | no |
| O2 alerting mechanism or recipients | H3 in force | no |
| X2 production branch (release control) | open question | only if `FDP-009-01` makes merges non-deploying |
| X5 schema change | none pending | no |

## 7. Founder boundary matrix (Act `§17`)

| Action | Authority State | Decision Owner | Execution Owner | Canonical Source | Boundary | Evidence | Status |
|---|---|---|---|---|---|---|---|
| A Production credentials | EXTERNAL-CONTROL | — (custody) | account holder | ACT-001 `§7.1`; ACT-003 `§13`, `§28` | never in the session or repository | [OBS] none set | waiting on E |
| B Production secret insertion | EXTERNAL-CONTROL | — | account holder | ACT-003 `§13`, `§28` | Production scope only | [OBS] none | waiting on E |
| C Production principals / tokens | UNKNOWN | unassigned (`ESC-01`) | holder generates own token | FS-DP-02 B3; ACT-003 `§28` | plaintext stays with its holder | none | escalated |
| D Production store wiring | CEO-AUTHORIZED | done (`ACT-004-DG-04`) | CEO | E1 | no store change | [OBS] migrated, 0 rows | complete |
| E Production deployment / merge to default | CONFLICT | Founder (`FDP-009-01`) | CEO + account holder | D4-A vs ACT-003 `§4.8`, `§20`, `§33` | nothing until resolved | [OBS] default branch = Production | STOP |
| F Release candidate | CEO-AUTHORIZED-WITH-BOUNDARY | CEO identifies; Founder approves (T) | CEO | ACT-001 `§20`; D4-A | identification ≠ approval | `d05261c` verified on Preview | ready to prepare |
| G Deployment Protection | ARCHITECT-RESERVED | Architect | account holder | `ACT-004-DG-01`, `§8` (X2); D2-A | stays X2 | [OBS] SSO on | decided |
| H Custom domain | ARCHITECT-RESERVED | Architect | account holder / registrar | FS-DP-03 Part B; D2-A; D3-A | none planned | [OBS] none | not needed |
| I Production variables | EXTERNAL-CONTROL | — | account holder | ACT-001 `§7.1`; ACT-003 `§13` | after E | [OBS] none | waiting on E |
| J Smoke (read-only) | CEO-AUTHORIZED-WITH-BOUNDARY | CEO | CEO | ACT-003 `§20`; F06 A11 | after E; path per X1 | tool tested | waiting on E |
| K Smoke writes | CEO-AUTHORIZED-WITH-BOUNDARY | CEO | CEO | ACT-003 `§20` | after E; labelled, minimal | tool tested | waiting on E |
| L Health verification | CEO-AUTHORIZED-WITH-BOUNDARY | CEO | CEO | ACT-003 `§20` | after E | — | waiting on E |
| M Integration verification | CEO-AUTHORIZED-WITH-BOUNDARY | CEO | CEO | ACT-003 `§20`, `§22` | after E | — | waiting on E |
| N Monitoring (L1/M1/R2) | CEO-AUTHORIZED | CEO | CEO | `ACT-004-DG-02` | no new monitor | implemented | ready |
| O1 Alerting cadence (H3) | CEO-AUTHORIZED-WITH-BOUNDARY | CEO | CEO | F06 A09; `ACT-008-DG-02` | no automatic alert | runbook `§12.1` | ready |
| O2 Alerting mechanism / recipients | ARCHITECT-RESERVED | Architect (+ D3-A) | — | D2-A; D3-A | H3 stands | — | not needed |
| P Production rollback | UNKNOWN | unassigned (`ESC-02`) | — | ACT-003 `§12` (limit only) | before release = E | — | escalated |
| Q Roll-forward | CONFLICT | Founder (`FDP-009-01`) | CEO | as E | as E | — | STOP |
| R Incident handling | CEO-AUTHORIZED-WITH-BOUNDARY | CEO | CEO | F06 A03, A11, A16; ACT-003 `§27` | Production changes follow E, P, B | runbook `§11` | ready |
| S Traffic activation | FOUNDER-RESERVED | Founder (`FDP-009-02`) | as directed | ACT-003 `§21`; D4-A | plus an Architect change under X2 | — | HOLD |
| T Production release / FRA | FOUNDER-RESERVED | Founder (`FDP-009-02`) | as directed | D4-A; ACT-003 `§21`, `§34`, `§35`; ACT-001 `§6.3` | after verification | — | HOLD |
| U Operational AIOS record | CEO-AUTHORIZED-WITH-BOUNDARY | conditions (ACT-003 `§22`) | CEO | ACT-003 `§22` | only when all hold | — | not due |
| V Billing / paid | FOUNDER-RESERVED | Founder (`FDP-009-04`) | — | D3-A; `FS-ARCH-RAT-001` `§11.2` | none proposed | [OBS] no purchase | standing: none |
| W Provider controls | EXTERNAL-CONTROL | — | account holder | ACT-001 `§7.1`, `§7.2`; ACT-003 `§12` | MCP access ≠ authority | [OBS] account `adibelepp21-byte` | as needed |
| X1 Production access past SSO | FOUNDER-RESERVED | Founder (`FDP-009-03`) | CEO, then revoke | ACT-003 `§12`, `§14` | temporary, revoked, verified absent | FS-09 precedent | HOLD |
| X2 Production branch setting | ARCHITECT-RESERVED | Architect | account holder | D2-A | only if `FDP-009-01` needs it | [OBS] default branch | open |
| X3 Production backup (read-only) | CEO-AUTHORIZED-WITH-BOUNDARY | CEO | CEO | FS-DP-01 pt. 6 (ratified) | read-only; never restored into Production | Preview drills | ready |
| X4 Final System Acceptance | FOUNDER-RESERVED | Founder (`FDP-009-05`) | Founder | F06 A19 | after LIVE | — | not due |
| X5 Production schema change | ARCHITECT-RESERVED | Architect | CEO | D2-A; FS-DP-01 | none pending | [OBS] one migration | not needed |

Count: CEO-AUTHORIZED 2 · CEO-AUTHORIZED-WITH-BOUNDARY 9 · ARCHITECT-RESERVED 5 · FOUNDER-RESERVED 5 · EXTERNAL-CONTROL 4 · CONFLICT 2 · UNKNOWN 2 = **29 actions, all classified** (counted from the table).

## 8. Authority graph (Act `§18`)

```text
FOUNDER (Moriarty)
  │
  ├── Founder-reserved: release / LIVE (T, S) · Production access past SSO (X1) · spending (V, standing: none)
  │                     · Final System Acceptance (X4, not due)
  ├── To resolve: the conflict on Production deployment (E, Q) → FDP-009-01
  ├── To answer or assign: Production principals (C, ESC-01) · post-release rollback (P, ESC-02)
  │
  ├── as ARCHITECT (FD-2 open; acted as Architect in ACT-004)
  │     └── protection X2 (G, decided) · custom domain (H) · alerting mechanism (O2) · production branch (X2) · schema (X5)
  ▼
CEO / CO-FOUNDER (Claude Code, DEL-CFV2-CEO-001)
  │
  ├── CEO-autonomous: store wiring (D, done) · monitoring (N) · release candidate (F) · H3 cadence (O1)
  │                   · incident handling (R) · read-only backup (X3) · operational-state record (U, when due)
  ├── Verification, once a deployment is authorized: smoke (J) · test writes (K) · health (L) · integration (M)
  └── Execution of repository and deployment steps, once E is resolved
  ▼
EXTERNAL CONTROLS (account `adibelepp21-byte`)
  │
  ├── Cloud / provider: Vercel project and team settings, production branch, plan (W)
  ├── Database provider: Supabase organization, Production key (A)
  ├── Credentials: Production variables (B, I)
  └── Domain: DNS for any custom domain (H; none planned)
```

## 9. Next legal execution boundary

* **May proceed now, under existing authority** (none of it is Production): correct FS-10-DEPLOYMENT.md to this map, as a recorded edit; prepare the release package for the candidate (row F); Preview work; read-only Production observation.
* **Stops here:** any Production deployment, merge to the default branch, promotion or roll-forward (`FDP-009-01`); Production variables (account holder, after `FDP-009-01`); authenticated Production checks (`FDP-009-03`); release and LIVE (`FDP-009-02`).
* **Under this Act:** nothing further. It authorizes no Production action (`§24`).

## 10. Negative controls and re-discovery (Act `§19`, `§21`)

| Control | Check | Result |
|---|---|---|
| NC-01 No Production deployment | `list_deployments target=production` before and after | one deployment, `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` (`22c0b49`), both times · HELD |
| NC-02 No Production write | Production store `count(*)`, `max(seq)`; migrations | 0 rows, `max_seq` 0, one migration, both times · HELD |
| NC-03 No traffic activation | project protection; Production deployment unchanged | SSO on; unchanged · HELD |
| NC-04 No secret insertion | Production-scope variables | none (`hiddenProductionEnvCount` 0) both times · HELD |
| NC-05 No token creation | no token generated; repository scan | none · HELD |
| NC-06 No protection change | `ssoProtection` and project `updatedAt` | unchanged (`updatedAt` `1790794799156`) · HELD |
| NC-07 No billing commitment | no purchase or plan call made | none · HELD |
| NC-08 No release authorization | no instrument created; Register `§106` records none | HELD |
| NC-09 No Operational AIOS activation | no such record | HELD |
| NC-10 No governance modification | `cofounder-v2/`, Delegation and Appointment Registers unchanged; the Decision Register only appended (`§105`, `§106`) | HELD |
| NC-11 No Founder Reserved Authority change | nothing reserved is altered or narrowed; classifications cite existing reservations | HELD |
| NC-12 No certified-root modification | `tools/`, `native_core/`, `consumers/`, P12/P13 roots unchanged | HELD |
| NC-13 No P12/P13 reopening | no closure, gate or manifest touched | HELD |
| NC-14 No authority self-expansion | every CEO row cites an existing grant; none relies on ACT-004…ACT-008 grants | HELD |
| NC-15 No decision masquerading as evidence | the package states choices without selecting; no Register entry reads as a decision | HELD |

Re-discovery (Act `§21`): the repository holds only this record, the Act, its evidence, a test window update and Register `§105`–`§106` as changes; Production unchanged; FS-10-DEPLOYMENT.md byte-identical; no new authority; 29 actions classified; every Founder-reserved row has a package (`§6`); UNKNOWN stays UNKNOWN (C, P); the next boundary is `§9`.

## 11. Closure (Act `§22`, `§23`)

```text
[PASS] FS-10 boundary inspected                 [PASS] external-control dependencies identified
[PASS] canonical authority inspected            [PASS] Founder Decision Package prepared
[PASS] material Production actions enumerated   [PASS] no Production state change occurred
[PASS] authority classification complete        [PASS] negative controls held
[PASS] Founder-reserved matters evidenced       [PASS] final re-discovery completed
[PASS] Architect-reserved matters evidenced
[PASS] CEO-authorized actions evidenced

BOUNDARY REVIEW COMPLETE

Terminal state  : D — CONFLICT (Production deployment: FD-FS-001 D4-A vs ACT-003 §4.8/§20/§33)
                  also A: Founder-reserved decisions exist; Founder Decision Package = READY
Production      : UNCHANGED
FS-10           : ACTIVE — Deployment Preparation; Production execution STOPPED at FDP-009-01
```
