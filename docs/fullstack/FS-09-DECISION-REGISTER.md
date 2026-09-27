# FS-09 — Decisions Blocking Production Readiness

| Field | Value |
|---|---|
| **Authority** | the Founder's FS-09 continuation, Workstream E: *"record … Do not choose an option on behalf of Architect or Founder"* |
| **Register** | `§88` (recorded); `§89` (Architect packages prepared, `§4`–`§5`) |
| **Nature** | a register of open questions. **No option is chosen, recommended as decided, or implemented here.** Where an earlier package carries a recommendation, it is quoted as the package's, not adopted |
| **Executable form** | `fullstack/readiness.py`: `PACKAGES` (FS-DP-03, -06, -07, and since `§89` FS-09-ENV and FS-09-RUNTIME) and `OTHER_DECISIONS` (Founder decisions with no package). Each appears in the gate's `awaiting` list until the Register records it taken |

## 1. Architect decisions

### 1.1 FS-DP-03 — Networking

| Field | Value |
|---|---|
| **Exact question** | What may reach what: ingress, AIOS addressability, database reachability, egress; TLS/HSTS; default or custom domain |
| **Source requiring it** | `FD-FS-001` D2-A (six Architect-reserved areas); Freeze `§10`; ACT-001 `§20` *Reproducibility: reproducible deployment*; ACT-003 `§19`, `§32` (*"no unverified … routes"*) |
| **Decision authority** | Architect (or the Founder acting as Architect) |
| **Available options** | Part A: the package's rule set *as written* (one origin; AIOS never addressable; the browser never reaches the database; egress only to the database) · *amended* · the package's alternative, a separate API origin with CORS. Part B: *as written* (host TLS, HSTS at the edge, default domain first) · *amended*; custom domain yes / no |
| **Implementation impact** | *As written*: almost none; it describes what is deployed (one origin via `vercel.json` rewrites, no CORS, the key only on the server). Verification on the Preview would follow, including an HSTS header check. *Separate origin*: CORS configuration, a second origin to protect, frontend changes. *Custom domain*: DNS ownership (external) and possibly a paid plan (**Founder**, D3-A) |
| **Blocker status** | **OPEN, blocking.** Gate row *Reproducibility: reproducible deployment* is BLOCKED on it. Note: the package's *"Until decided: local loopback only"* was overtaken by the ratified `FS-DP-04` deployment; the deployed Preview already follows Part A |
| **Package** | `docs/fullstack/decision-packages/FS-DP-03-NETWORKING.md`: **revision 2** prepared for Architect review (`§89`). PROPOSED — NOT RATIFIED |

### 1.2 FS-DP-06 — Observability implementation

| Field | Value |
|---|---|
| **Exact question** | How operational telemetry (request logs, metrics, a readiness signal, alerting) is produced and kept apart from Trace and audit |
| **Source requiring it** | `FD-FS-001` D2-A; Freeze `§10` and AD-8 (*observability is not accountability*); ACT-001 `§20` *Observability: logging, metrics, alerting*; ACT-003 `§19` (monitoring, alerting) |
| **Decision authority** | Architect (or the Founder acting as Architect). Any paid alerting: **Founder** (D3-A) |
| **Available options** | Part A: telemetry separate from Trace and audit, with no credentials, bodies or document contents *as written* · *amended*. Part B: one JSON line per request to stdout; a readiness signal (Runtime state and store reachability); alerting through the host's facilities or an external uptime check on `/api/v1/health`; OpenTelemetry-compatible names. Each is *as written* · *amended* · *omitted* |
| **Implementation impact** | A request-log middleware in the API, a readiness field in `/health`, tests that no credential or body enters a log line; alerting configuration on the host or an external service (an external dependency) |
| **Blocker status** | **OPEN, blocking.** Gate row *Observability: logging, metrics, alerting* is BLOCKED. The runbook's `§12` is a placeholder until it is decided |
| **Package** | `docs/fullstack/decision-packages/FS-DP-06-OBSERVABILITY.md`: **revision 2** prepared for Architect review (`§89`). PROPOSED — NOT RATIFIED |

### 1.3 FS-DP-07 — Agent creation (Scenario A)

| Field | Value |
|---|---|
| **Exact question** | May the application create Agents and, if so, what: nothing, Instances of existing governed Definitions, or Definitions themselves |
| **Source requiring it** | ACT-001 `§18` (Scenario A *User → Create Agent → … → Result* is a **mandatory** class); Freeze `§13`; Blueprint `§3`; `agent_spec §12–§13`; Domain Model `§6` (Definitions belong to the owning Platform Division) |
| **Decision authority** | Architect. Definitions' authority sits with the owning Platform Division. If A1: the **Founder** decides whether a mandatory scenario may stand as a classified residual (`§2.1`) |
| **Available options** | **A1** keep reserved (no route creates an Agent) · **A2** instance registration only (new scope `aios.agent.register`; needs an authority instrument extending `FD-P11-001 §7`-style registration) · **A3** full Agent Factory (Definitions authored through the application) |
| **Implementation impact** | A1: none; Scenario A stays impossible. A2: an authority instrument first, then one route (`POST /api/v1/agent-instances`) over the canonical `AgentInstance` contract, an append-only record, audit. A3: crosses Platform Division authority; the largest change |
| **Blocker status** | **OPEN, blocking.** Gate row *Functionality: agent creation (Scenario A)* is BLOCKED. **No Agent Factory is built** (Founder instruction) |
| **Package** | `docs/fullstack/decision-packages/FS-DP-07-AGENT-CREATION.md`: **revision 2** prepared for Architect review (`§89`). PROPOSED — NOT RATIFIED |

### 1.4 Environment separation: package `FS-09-ENV` (recorded at `§88` as ENVIRONMENT-SEPARATION)

| Field | Value |
|---|---|
| **Exact question** | How Production data is kept apart from Preview (test) data, given that the ratified arrangement names one Supabase project |
| **Source requiring it** | ACT-003 `§19` (environment separation) and `§32`; `FS-DP-01` as ratified by `FS-ARCH-RAT-001` (*"the existing AIOS Supabase project provides persistence"*; `§11.1` fixes the project URL in code) |
| **Decision authority** | Architect: every option changes or confirms the ratified persistence arrangement. An option that costs money is also a **Founder** decision (D3-A) |
| **Available options** (as found; none assessed as chosen) | **E1** a second Supabase project for Production (the organization holds one project today, `scfymftfzkpilqbgmfwv`; whether a second is free on the current plan is to be confirmed, and is **Founder** spending if not; the project URL would become configuration or a second constant) · **E2** the same project, a separate table per environment (a second migration; the adapter learns which table) · **E3** the same table, environment carried in the partition name or a column · **E4** Supabase branching (a paid-plan feature: spending) · **E5** Preview on a non-Supabase store, Production alone on Supabase (Preview would stop producing live persistence evidence) · **E6** keep one shared store and accept Preview data in Production as a classified residual |
| **Implementation impact** | Every option except E6 needs code or configuration. E1/E2: the migration replayed on the new target, then a restore drill there. Common to all: the store is append-only, so the **FS-08 test records already in `aios_records` (81 since `seq` 86) can never be removed**. *Corrected at `§89`:* the sentence first recorded here (*"Under E2, E3 or E6 they stay in the Production table, and only E1 or E5 leave them outside Production"*) was wrong for E2 and E5. They stay outside Production's data under E1 or E2 **only if the new resource serves Production**, and under E3 logically (same physical table). Under E4, E5 and E6 they are in Production's data (`FS-09-ENV` `§6.1`) |
| **Blocker status** | **OPEN, blocking.** Gate row *Data: environment separation* is BLOCKED. No new project, database or table has been created (Founder instruction) |
| **Package** | `docs/fullstack/decision-packages/FS-09-ENV-ENVIRONMENT-SEPARATION.md` (`§89`). PROPOSED — NOT RATIFIED |

### 1.5 Python runtime: package `FS-09-RUNTIME` (recorded at `§88` as PYTHON-RUNTIME-VERSION; Workstream D stopped here)

| Field | Value |
|---|---|
| **Exact question** | Which Python version the host must run, pinned in the repository |
| **Source requiring it** | ACT-001 `§20` *Reproducibility*; ACT-003 `§12` (configuration). The Founder's Workstream D: *"If the exact version cannot be established from canonical evidence, STOP and report the ambiguity instead of inventing one"* |
| **The ambiguity** | (1) `FS-02` (the program's blueprint, constructed under ACT-001 `§13`, not Architect-ratified) names **"Python 3.11 standard library"**; `FS-00` measured 3.11; every local and certified run uses 3.11 (3.11.15 here). (2) `FS-ARCH-RAT-001` (ratified) names a *"Python backend"* and a *"Vercel Python Function"*, **no version**. (3) The FS-08 Preview whose live evidence the gate uses was built with **3.12**: build log `bld_8ubuwdj02` of `dpl_Gi3MbQkzo14aW4TriGwQ9TYMudgL` reads *"No Python version specified in .python-version, pyproject.toml, or Pipfile.lock. Using python version: 3.12"*. (4) The Vercel documentation retrieved shows `.python-version` and `requires-python` as the mechanisms and 3.12/3.13 in its examples; **whether 3.11 is available on the host is not established** |
| **Decision authority** | Architect: the version belongs to the deployment arrangement (`FS-DP-04`) and settles a conflict between the blueprint and the verified deployment |
| **Available options** | **P1** pin 3.11 (the blueprint and all local evidence; host availability to be verified; the FS-08 live evidence was produced on 3.12, so the Preview would need re-verification) · **P2** pin 3.12 (the version the live evidence ran on; FS-02 amended; local and certified suites would need a 3.12 run to keep the classes aligned) · **P3** leave unpinned (the host's default decides, and may change without a commit) |
| **Implementation impact** | P1/P2: one file (`.python-version`) or `requires-python` in a `pyproject.toml`, then a Preview build whose log shows the pinned version, then live re-verification (needs Preview access: **Founder**). P3: none, and the reproducibility gap stays |
| **Blocker status** | **OPEN, blocking.** Gate row *Reproducibility: runtime version pinned* is BLOCKED. **Nothing was pinned** |
| **Package** | `docs/fullstack/decision-packages/FS-09-RUNTIME-PYTHON-RUNTIME-REPRODUCIBILITY.md` (`§89`). PROPOSED — NOT RATIFIED |

## 2. Founder decisions

| # | Exact question | Source | Options (none chosen) | Blocks |
|---|---|---|---|---|
| 2.1 | If FS-DP-07 = A1: may the mandatory Scenario A stand as a **classified non-blocking residual**? | ACT-001 `§18`, `§20` exit (*"residual non-blocking findings classified"*) | yes, as a classified residual · no (then A2 or A3 is required) | FS-09 PASS while Scenario A is impossible |
| 2.2 | **Performance requirement**: is there a workload or latency the system must meet? | ACT-001 `§20` *Performance: required workload behaviour*; no canonical source states one | state a requirement (then it is measured on the Preview) · accept OBSERVED as non-blocking | the Performance row stays OBSERVED; nothing is invented |
| 2.3 | **Operational ownership** (`OPERATIONAL-OWNERSHIP`): who operates AIOS, holds the production operator token and the database key, runs backups (and how often; retention), and answers incidents | ACT-003 `§19` (operational ownership); runbook `§13` | a named owner (Founder, a delegate) and a backup cadence | gate row *Operations: operational ownership* (BLOCKED); backup residual |
| 2.4 | **Live access for FS-09 checks**: a new, temporary Preview access (the FS-08 bypass was scoped to that suite and revoked) | NC-04; ACT-003 (no bypass without authorization); `EXT-03` | authorize a scoped, revocable mechanism for named checks · decline | a live 403, live latency, a Preview rollback drill, re-verification after any runtime pin |
| 2.5 | **Operator identities**: a second, narrower Preview principal for a live 403; custody and delivery of the production operator token (never through chat) | FS-08 residual; ACT-003 access control | configure one (the hash only, by the operator) · keep the local 403 evidence as the residual | the authorization residual |
| 2.6 | **Spending** (D3-A): paid alerting; a paid Supabase plan (downloadable backups, no pause, branching) | `FD-FS-001` D3-A; `FS-DP-01` point 6 | spend · do not spend | only the options that cost money (FS-DP-06 alerting; E4) |
| 2.7 | **Deployment protection observed disabled** (`EXT-06`): was the change of Vercel `ssoProtection` (enabled at FS-08, `enabled: false` at 2026-09-27 19:57Z; not made by Claude Code) intended? | ACT-003 NC-04; `FS-DP-03` revision 2 `R2.4` | confirm as intended · restore it (a Founder-held setting). The required edge access is decided by the Architect in `FS-DP-03` (X1–X3) | the Preview's exposure until `FS-DP-03` is decided |
| 2.8 | **Release** (`FD-FS-001` D4-A): after a FS-09 PASS, whether and what to release | `FD-FS-001` D4-A; ACT-003 | — | not due: FS-09 has not passed; FS-10 is NOT STARTED |

## 3. What is not a decision but a gap (authorized, not yet done)

| Gap | Why it is open | Needs |
|---|---|---|
| **Rollback of a deployment NOT VERIFIED** | no rollback has been exercised on any deployment; data compatibility alone is verified | a Preview rollback drill (runbook `§9`), which needs Preview access (`§2.4`) |

## 4. Blocked items at `§89`

| Gate row | Status | Waits on | Package / record |
|---|---|---|---|
| Functionality: agent creation (Scenario A) | BLOCKED | Architect `FS-DP-07`; if A1, Founder `§2.1` | `FS-DP-07` rev. 2 |
| Observability: logging, metrics, alerting | BLOCKED | Architect `FS-DP-06` | `FS-DP-06` rev. 2 |
| Data: environment separation | BLOCKED | Architect `FS-09-ENV` | `FS-09-ENV` |
| Reproducibility: runtime version pinned | BLOCKED | Architect `FS-09-RUNTIME` | `FS-09-RUNTIME` |
| Reproducibility: reproducible deployment | BLOCKED | Architect `FS-DP-03` | `FS-DP-03` rev. 2 |
| Operations: operational ownership | BLOCKED | Founder `§2.3` | this register |
| Reliability: rollback of a deployment | FAIL (not verified) | a Preview drill; Founder access `§2.4` | runbook `§9` |
| Performance | OBSERVED | Founder `§2.2` | this register |

## 5. Architect decisions awaiting ratification (`§89`)

| Package | Question | Options | Analytical recommendation (**UNRATIFIED**) |
|---|---|---|---|
| `FS-DP-03` rev. 2 | what may reach what, including edge access | N1 · N2 · N3; X1 · X2 · X3; Part B | N1, X2 (at least X1), Part B as written |
| `FS-DP-06` rev. 2 | logging, metrics, alerting, kept apart from Trace and Audit | L1–L3; M1–M3; H1–H3; R1 · R2 | L1, M1, R2; alerting with `FS-DP-03` and ownership |
| `FS-DP-07` rev. 2 | may the application create Agents | A1 · A2 · A3 | A1 now; A2 when a use needs it |
| `FS-09-ENV` | Production data apart from Preview data | E1–E6 | E1 with the new project for Production, else E2 with the new table for Production |
| `FS-09-RUNTIME` | the Python version, pinned | P1 · P2 · P3 | P2 (3.12, FS-02 amended); its condition, a full `tools` pass on 3.12, is met locally (all five suites OK on 3.12.3); P1 remains valid |

A recommendation is analysis only. None is adopted, implemented or treated as
decided until the Architect's decision is recorded in the Decision Register.

