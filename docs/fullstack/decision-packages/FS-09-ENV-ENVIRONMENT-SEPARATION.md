# FS-09-ENV — Environment Separation

| Field | Value |
|---|---|
| **Identifier** | `FS-09-ENV` (provisional) |
| **Area** | Separation of Production data from Preview data in the ratified persistence arrangement; Architect-reserved (it amends or confirms `FS-DP-01` as ratified by `FS-ARCH-RAT-001`) |
| **Status** | **RATIFIED — E1** (bounded fallback E2), by the Founder as Architect in `ACT-CC-POST-P13-AIOS-FULL-STACK-004` `§14` (Register `§93`, `ACT-004-DG-04`). E1 implemented with the new project `hmljfyqycxcueulhsjae` serving Production (store created and migrated); the adapter's per-environment selection is **implemented** under ACT-007 (`fullstack/deploy/vercel.py`, `VERCEL_ENV`; Register `§98`, ACT-007 record); it was execution-permission blocked under ACT-005. The analysis below is the package as reviewed (`§89`) |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A). Options that cost money are also a Founder decision (D3-A) |
| **Founder constraints** | Vercel; Supabase; no spending (D3-A); no new Supabase Production project created before a decision (FS-09 instructions) |
| **Prepared by** | Claude Code, 2026-09-27, on the Founder's *"FS-09 — DECISION PACKAGE PREPARATION"*. Options E1–E6 as recorded in `FS-09-DECISION-REGISTER.md` `§1.4`; no other option is introduced |

## 1. Decision ID

`FS-09-ENV` (provisional). Register `§89`. Named `ENVIRONMENT-SEPARATION` in
the `§88` records and in the readiness gate before this package.

## 2. Exact architectural question

How is Production data kept apart from Preview (test) data, given that:

* the ratified arrangement names **one** Supabase project and one table, and
* the store is **append-only**, so data already written cannot be removed.

## 3. Canonical sources

| Source | What it says |
|---|---|
| ACT-003 `§19` | environment separation is a readiness requirement |
| ACT-003 `§32` | no unverified persistence or configuration before release |
| `FS-DP-01` as ratified (`FS-ARCH-RAT-001`) | *"the existing AIOS Supabase project provides persistence"*; append-only table; RLS; server-side key |
| `FS-ARCH-RAT-001` `§11.1` | the project URL is fixed in code (`SUPABASE_PROJECT_URL`, *"Not configurable"*) |
| `FS-DP-04` A1 (ratified) | one Runtime per request; **all state in the shared store** |
| Migration `20260927062422_aios_records` | table, RLS, triggers refusing UPDATE, DELETE and TRUNCATE |

## 4. Current implementation state

| Item | State |
|---|---|
| Supabase | one project in the organization: `scfymftfzkpilqbgmfwv` (`ap-northeast-2`, ACTIVE_HEALTHY) |
| Table | `aios_records`, the only AIOS table; one migration applied (equal to the repository) |
| Contents | **81 records**: the 80 written by the FS-08 Preview suite (10 runs, 29 Trace, 41 audit; exported and digest-verified at `§88`) plus **1** anonymous refused audit entry (`seq` 86, 2026-09-27 19:57Z), appended by the read-only observation in `FS-DP-03` revision 2 `R2.4` |
| Vercel variables | `SUPABASE_SECRET_KEY` and `AIOS_OPERATOR_TOKENS` in **Preview scope only**; no Production variables exist |
| Code | project URL: a constant (`fullstack/deploy/vercel.py`). Table: a constant (`TABLE = "aios_records"`, `supabase_storage.py`). Partitions: constants (`fullstack-runs`, `fullstack-audit`, and `trace` from `native_core` `TRACE_PARTITION`) |
| Production | serves no AIOS application (`22c0b49`); no Production store is configured |

### 4.1 The binding constraint (preserved)

**The existing Preview test records are append-only and must not be deleted.**
Triggers refuse UPDATE, DELETE and TRUNCATE, the `StorageFacility` contract
offers no delete, and no option below removes, rewrites or moves them. Every
option therefore answers one question the same way: **the records stay where
they are, in `scfymftfzkpilqbgmfwv` / `aios_records`**. What differs is whether
Production reads and writes that same data.

## 5. Authority required

**Architect**: every option confirms or amends the ratified persistence
arrangement (E1 also amends `FS-ARCH-RAT-001` `§11.1`). **Founder**: any option
that costs money (E4 always; E1 if a second project is not free on the current
plan) and the acceptance of a residual under E6.

## 6. Available options (E1–E6, exactly as registered)

| ID | Option (as registered at `§88`) |
|---|---|
| **E1** | a second Supabase project for Production |
| **E2** | the same project, a separate table per environment |
| **E3** | the same table, environment carried in the partition name or a column |
| **E4** | Supabase branching (a paid-plan feature) |
| **E5** | Preview on a non-Supabase store, Production alone on Supabase |
| **E6** | keep one shared store and accept Preview data in Production as a classified residual |

### 6.1 Where the existing records end up, per option

| Option | Are the existing 81 records in Production's data? |
|---|---|
| E1 | **No**, if the **new** project serves Production (they stay with Preview). **Yes**, if the new project serves Preview instead. Which one moves is part of the E1 decision |
| E2 | **No**, if the **new** table serves Production. **Yes**, if Production keeps `aios_records` |
| E3 | **No** for Production's reads, if Production uses new partition names or a new column value. The rows stay in the **same physical table** |
| E4 | **Yes**: the main branch is the existing database, which holds them; Preview branches are separate databases |
| E5 | **Yes**: Production keeps the existing project and table, which hold them |
| E6 | **Yes**, by definition, and every future Preview test adds more |

This corrects `FS-09-DECISION-REGISTER.md` `§1.4` as first written at `§88`.
It said E5 kept the records outside Production and E2 did not; this table
states the dependence on which environment gets the new resource.

## 7. Architectural consequences

| Option | Consequence |
|---|---|
| E1 | the strongest isolation: separate database, keys, quotas and backups. The project URL becomes per-environment configuration, **amending `FS-ARCH-RAT-001` `§11.1`** (URL fixed in code). The migration is replayed on the new project |
| E2 | the adapter learns its table name from configuration; a second migration creates the second table with the same RLS and triggers. One project, one key for both |
| E3 | partition prefixes can be added by a storage wrapper in the application without touching `native_core`; a column is DDL on the append-only table, with existing rows given a default. Separation is logical only |
| E4 | branch databases per Preview through the Supabase GitHub integration; the migration applied per branch |
| E5 | **conflicts with `FS-DP-04` A1 on Preview**: a per-request function has no durable local store, so Preview state would not outlive a request, and FS-08's persistence evidence could not be reproduced on Preview |
| E6 | no change; the arrangement stays as ratified |

## 8. Data and state consequences

| Option | Consequence |
|---|---|
| E1 | a new, empty Production store. Preview data (including the 81 records) stays in the old project. Backups per project |
| E2 | a new, empty table for one environment; both in one database; one backup covers both, and a restore must restore them apart |
| E3 | both environments in one table. A defect in the prefix or column logic mixes them **permanently** (append-only) |
| E4 | branch data is discarded with the branch; Production (main) holds the 81 records |
| E5 | Preview data becomes ephemeral; Production holds the 81 records |
| E6 | test data and production data are distinguishable only by time and subject, forever |

In every option the 81 records remain; none is deleted, moved or rewritten.

## 9. Security consequences

| Option | Consequence |
|---|---|
| E1 | separate keys: a Preview key compromise cannot touch Production. Vercel scopes each key to its environment |
| E2, E3 | one service key reaches both environments: a Preview compromise reaches Production data |
| E4 | per-branch credentials handled by the integration; a new third-party link (GitHub to Supabase) |
| E5 | Production key only; Preview has no database credential |
| E6 | Preview code and Preview traffic write directly into Production data. Since Preview deployment protection is currently **off** (`FS-DP-03` revision 2), anonymous requests append audit records there too |

## 10. Operational consequences

| Option | Consequence |
|---|---|
| E1 | two projects to keep active (the free plan pauses a project after 7 days of low activity), two backups (runbook `§7`), two keys to rotate |
| E2, E3 | one project; backup and restore must respect the split |
| E4 | branching lifecycle per Preview; a paid plan |
| E5 | Preview checks can no longer exercise persistence |
| E6 | the runbook must tell operators how to separate test from production records in every investigation |

## 11. Verification requirements

1. For E1 and E2: the migration applied on the new target equals the repository's; its RLS and triggers verified (an UPDATE refused).
2. A Preview write does **not** appear in Production's store, and the reverse (counts before and after, both ways).
3. Each environment's key is scoped to that environment in Vercel, and no Production variable reaches a Preview build.
4. A backup and restore drill on the new target (runbook `§7`–`§8`).
5. The 81 existing records unchanged: joined digests per partition equal to the `§88` manifest (80), plus `seq` 86.
6. The readiness gate's *Data: environment separation* row changes from BLOCKED only after 1–5 are recorded.

## 12. Rollback implications

* Switching an environment back to the old store is configuration, but **records written in the meantime stay in the store they were written to**. The append-only rule forbids merging them back. They can only be restored into a fresh store (runbook `§8`).
* E1 and E2 can be rolled back by configuration, leaving the new store holding its records.
* E3's mixed table cannot be un-mixed.
* E4 branches are disposable; main is not.

## 13. Explicit non-scope

No Supabase project, database, branch or table is created. No record is
deleted, moved or rewritten. No configuration or code is changed. No Production
variable is set.

## 14. Dependencies

| On | Why |
|---|---|
| `FS-DP-01`/`FS-ARCH-RAT-001` | the arrangement this amends or confirms (E1 amends `§11.1`) |
| `FS-DP-04` A1 | E5 conflicts with it on Preview |
| `FS-DP-03` | Production's domain and edge; Preview edge protection (E6's exposure) |
| Founder | spending (E4; E1 if not free); residual acceptance (E6); Production configuration |
| `OPERATIONAL-OWNERSHIP` | who keeps each project active and backed up |

## 15. Whether it blocks FS-09

**Yes.** ACT-003 `§19` names environment separation. Gate row *Data:
environment separation* is BLOCKED on this package.

## 16. Analytical recommendation (**UNRATIFIED**)

> *Not a decision. Stands only as analysis until the Architect decides.*
> **E1 with the new project serving Production**, if a second project is
> available on the current plan at no cost (to be confirmed by the Founder).
> It is the only option that isolates keys and leaves all existing test
> records outside Production. If a second project is not available, **E2 with
> the new table serving Production**, with the shared-key residual stated.

## 17. Exact decision required

- [ ] E1 (new project for: Production · Preview) · E2 (new table for: Production · Preview) · E3 (partition · column) · E4 · E5 · E6
- [ ] If E1: amendment of `FS-ARCH-RAT-001` `§11.1` (project URL per environment)
- [ ] Founder: spending, if any; residual acceptance, if E6
- [ ] Decided as: Architect · Founder as Architect
