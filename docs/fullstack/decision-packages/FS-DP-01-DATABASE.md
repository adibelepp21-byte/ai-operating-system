# FS-DP-01 — Database Implementation

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-01` (provisional; no ADR number is taken) |
| **Area** | Database implementation — Freeze `§10`, Architect-reserved |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A; `FD-2` open) |
| **Founder constraints** | Supabase is the named database provider; no spending (D3-A). *"Provider selection is not permission to redesign AIOS architecture around a provider-specific feature."* |
| **Prepared by** | Claude Code, 2026-09-26 |

## Context

- Trace is append-only and immutable (Freeze INV-5). Its ordering discipline
  is the storage facility's append order; no timestamp field is added
  (`trace/record.py`).
- Infrastructure owns persistence *beneath* the entities; the backend is
  replaceable (Infrastructure spec `§12`). `StorageFacility` offers append and
  read, and **no edit or delete**.
- Workflow lifecycle state is in-process by decision (`FD-P9-001 §12.4`).
  Memory lifecycle is in-process today.
- FS-04 classified the durable state: Trace, Knowledge, the application's run
  records and audit (`docs/fullstack/FS-04-DATA-AND-STATE.md`).
- Today all of it lives in `LocalAppendOnlyStorage` files under one data
  directory. That cannot survive a serverless host, whose filesystem is
  ephemeral (FS-DP-04).

## Part A — Architectural decision (ADR-eligible)

**Question.** Where does a database sit in AIOS, and what may it do?

| Option | Statement | Assessment |
|---|---|---|
| **A1** | The database is a **backend beneath `StorageFacility`**. It stores partitions of append-only records and nothing else; entities keep their own meaning. Append-only is enforced by the store too, not only by the facility | Keeps every boundary; no Domain Model change; satisfies INV-5 twice over |
| A2 | The application defines its own schema per entity (agents, runs, messages …) and reads and writes it directly | Rejected: generic schemas without ownership evidence (Act NC-14); bypasses Infrastructure; makes the database a second source of truth beside Trace |
| A3 | No database; files only | Blocks every host without a persistent disk, which includes the named one |

**Recommendation: A1.**

## Part B — Implementation decision (Freeze `§10`; not ADR-eligible, Constitution `§3.4`)

**Question.** How is A1 realized on Supabase?

Recommended realization:

1. One table, `aios_records(partition text, seq bigint generated always as
   identity, record jsonb, appended_at timestamptz default now())`,
   primary key `seq`. `seq` is the append order.
2. **Append-only in the database**: `UPDATE`, `DELETE` and `TRUNCATE`
   revoked from every role the backend uses; a trigger that raises on update
   or delete as a second barrier.
3. **Row Level Security enabled with no policy for `anon` or
   `authenticated`**: the browser can reach nothing. Only the backend, with a
   server-side key, reads and appends.
4. A `SupabaseStorage(StorageFacility)` adapter in the application layer,
   selected by configuration. `native_core` is not modified.
5. Migrations versioned in the repository; applied first to a Supabase
   branch or a separate free project, then to production (D4-A).
6. Backup and recovery: **must be confirmed on the account** during FS-08
   read-only discovery. If the plan has no downloadable backups, a
   logical export run by the operator is the fallback. Either way, a restore
   drill is an FS-09 criterion.

**Facts to confirm before ratifying, not asserted here:** the free plan's
database size, pause-on-inactivity behaviour, backup availability, and
connection limits. Each could make the free plan unsuitable. Upgrading is a
spending decision, not the Architect's (D3-A).

## Facts found in FS-08 discovery (2026-09-26)

- A Supabase project exists (`baacpvssvvxtezspclgj`). Three read-only queries
  through the connector **timed out**; the cause is not determined (EXT-01).
- Supabase's documentation: Free-plan projects **pause after 7 days of low
  activity** (restorable within 90 days), and *"database backups are not
  available for download for Free Plan projects."*
- So on the Free plan (D3-A), point 6 above can only be met by an
  operator-run logical export, and availability depends on regular activity.
  Choosing a paid plan instead is a spending decision for the Founder.

## Until decided

The backend persists through `LocalAppendOnlyStorage` under an explicit data
directory. It runs locally and in tests. **It is not deployable to a
serverless host** until this package is decided.

## Exact decision required

- [ ] Part A: A1 · A2 · A3 · other
- [ ] Part B: the realization above · amended as stated · other
- [ ] Decided as: Architect · Founder as Architect
