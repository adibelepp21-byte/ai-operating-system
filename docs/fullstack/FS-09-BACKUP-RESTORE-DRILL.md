# FS-09 — Backup and Restore Drill

| Field | Value |
|---|---|
| **Authority** | `FS-DP-01` point 6 (free plan: an operator-run logical export; *"a restore drill is an FS-09 criterion"*), ratified by `FS-ARCH-RAT-001`; its `§3.3` authorizes testing backup and restore. The Founder's FS-09 continuation, Workstream B |
| **Register** | `§88` |
| **Date** | 2026-09-27 |
| **Source** | Supabase project `scfymftfzkpilqbgmfwv`, table `public.aios_records`, the ratified store. Only the FS-08 Preview has written to it |
| **Target** | fresh stores created for the drill: the certified local append-only backend in a temporary directory, and `SupabaseStorage` over the in-memory PostgREST used by the test suite |
| **Production** | not touched. No Production deployment, alias, variable or credential was read or changed; no project, database or table was created |
| **Result** | **the restore is byte-identical to the live store, and the application reads it**: 80 of 80 records, every partition and the whole table equal to the digests the database computed |

## 1. Why the target is a fresh local store

Restoring into a live Supabase target other than `scfymftfzkpilqbgmfwv`
would mean creating or choosing a second environment. That is the open
Architect decision `ENVIRONMENT-SEPARATION` (`FS-09-DECISION-REGISTER.md`
`§1.4`), so the drill stops at that boundary. Restoring into
`scfymftfzkpilqbgmfwv` itself is impossible by design: the table is
append-only and the restore refuses a target that already holds the partitions.

## 2. Procedure, exactly as run

| # | Step | How | Result |
|---|---|---|---|
| 1 | Record the live digests | read-only SQL through the operator's Supabase connection: per partition `count`, `sum(octet_length(record))`, `min/max(seq)`, and `encode(sha256(string_agg(record, '\x0a'::bytea order by seq)),'hex')`; the same over the whole table | the table below |
| 2 | Export | every row read in `seq` order (read-only SQL). Each record's bytes were materialized from its canonical JSON form (`sort_keys`, no spaces) and **accepted only when its SHA-256 equalled the value the database computed for that row** (`encode(sha256(record),'hex')`) | 80 of 80 rows byte-identical (10 runs, 29 Trace, 41 audit) |
| 3 | Write the export | one `fullstack.backup/1` line per row, in `seq` order, with `position` per partition (`fullstack/deploy/backup.py`) | `docs/fullstack/evidence/FS-09-BACKUP-EXPORT-2026-09-27.jsonl`, 48 882 bytes, SHA-256 `6e535b5e8da200c33656db5a369439c8547d7fb04f52e65f5df9f0042492e251` |
| 4 | Check the export against the live store | `backup.summary(backup.read_file(…))` against step 1 | every partition and the whole table equal |
| 5 | Re-check the live store is unchanged | step 1 again at 19:01 UTC | identical: 80 rows, same digests |
| 6 | Scan for credentials | the operator token, the revoked bypass secret, the Supabase secret-key prefix, a JWT prefix, `Bearer`, `apikey`, `service_role`, `authorization`, `AIOS_OPERATOR_TOKENS` | none present. Audit subjects are `founder` or `null` |
| 7 | Keep a manifest | source, method, digests, the export's own SHA-256 | `docs/fullstack/evidence/FS-09-BACKUP-MANIFEST-2026-09-27.json` |
| 8 | Restore into a fresh store | `python -m fullstack.backend backup-restore --export <export> --data-dir <new dir>` (and `backup.restore` into `SupabaseStorage` over the in-memory PostgREST) | `"identical": true`, the same three joined digests |
| 9 | Refuse a second restore | the same command again on the same directory | exit 2: *"the target already holds fullstack-audit, fullstack-runs, trace; a restore makes a fresh store and never merges"* |
| 10 | Read it through the application | `AIOSApplication` on the restored directory; the API v1 over it | see `§4` |

The export went through the operator's SQL access because the application's
server-side key lives only in the host's environment, and Claude does not read
it. With the key, the same export can be produced through the `StorageFacility`
contract (`backup.export_store`).

## 3. Digests: the live store against the export

| Partition | Records | Bytes | `seq` | Joined SHA-256 (database) | Export |
|---|---|---|---|---|---|
| `fullstack-audit` | 41 | 8 825 | 6–85 | `a21d5dac8a356aac82d8bb8e1c71d9fc23a6f4a61fc3ea0a4a9619eb351f59b8` | equal |
| `fullstack-runs` | 10 | 12 859 | 33–82 | `94635f4bf48b54a86d8acde7995a4daedeba652eb216a594849ee9636d7b3613` | equal |
| `trace` | 29 | 9 870 | 30–81 | `099fa8cee2aa8673720c0089a490bea1c7c90b26c1c8090626f287a80bbbe088` | equal |
| whole table | 80 | 31 554 | 6–85 | `46e8fa3f668b6acda740af6486b08d5a3ddf2b602f22011a0f28e7458fb7dec2` | equal |

`seq` 1–5 are absent in the source (identity gaps), which the store allows.

## 4. What the application reads from the restored store

Held by `fullstack/tests/test_backup_restore.py` (23 tests) on every regression run:

| Check | Result |
|---|---|
| runs | 10, equal to the exported records, newest first; 10 distinct ids; 9 `succeeded`, 1 `failed` |
| each run's Trace (`run_trace`, `FS-DP-05` C1) | resolved for all 10: its `count` records (3, or 2 for the failed run), all from the run's own Runtime, one naming `document-conformance-review/<run id>` |
| Trace | 29 records in the exported order |
| audit | 41 entries, equal and in order (positions 0–40): 21 refused (401), 20 allowed (200) |
| through the API | `GET /api/v1/runs` → 10; `GET /api/v1/runs/{id}` → that run; `GET /api/v1/audit` → the 41 restored entries, then the drill's own |
| append-only after restore | a new run appends; every earlier record is unchanged; the store offers no edit or delete |
| both backends | byte-identical on the local backend and on `SupabaseStorage` |
| refusals | a changed record (digest), a missing or reordered record (position), a backwards `seq`, an unknown format or field (for example `token`): each refused before anything is written |

Mutation checks on `backup.py` (fresh-target check, digest check, position
check, order of restore, `seq` order, the comparison, the field whitelist):
each broken version is caught by the tests.

## 5. What this does not establish

* **A schedule.** Backups exist only when the operator runs one. Cadence,
  retention and who runs it wait on the Founder (`OPERATIONAL-OWNERSHIP`).
* **A restore into a second live project**, which waits on `ENVIRONMENT-SEPARATION`.
* **Point-in-time recovery.** The free plan has none; the export is the recovery point.


## 6. Final drill on current data (ACT-008 `§12`, 2026-09-30)

The 2026-09-27 drill above (80 records) is now the **historical control**. The
final drill repeats the procedure on the store as it stands after the final
live suites.

| # | Step | Result |
|---|---|---|
| 1 | Live digests (read-only SQL, `seq <= 510`) | 505 records, 206 462 bytes; partitions `fullstack-agents` 5, `fullstack-audit` 245, `fullstack-runs` 66, `trace` 189; whole-table SHA-256 `b70efff9…8de4` |
| 2 | Export | every row materialized from its canonical JSON and accepted only when its SHA-256 equalled the database's for that row: **505 of 505**; `FS-09-BACKUP-EXPORT-2026-09-30.jsonl`, 317 729 bytes, SHA-256 `7fe7e26f…90e6` |
| 3 | Integrity | every partition's joined digest and the whole table equal the database's (`FS-09-BACKUP-MANIFEST-2026-09-30.json`) |
| 4 | Store unchanged | the same digests over `seq <= 510` after the export (append-only) |
| 5 | Credential scan | none: the operator token, the temporary bypass secret, the Supabase key prefix, a JWT prefix, `Bearer`, `apikey`, `service_role`, `AIOS_OPERATOR_TOKENS`. Audit subjects `founder` or `null` |
| 6 | Restore into an empty target | `backup-restore` into a fresh directory: identical; into `SupabaseStorage` over the in-memory PostgREST: identical; a second restore into the same directory is refused (*never merges*) |
| 7 | Readability | the application reads 66 runs, resolves every run's Trace, lists 245 audit entries in order, 189 Trace records, and the **Agent Instance registrations** through the registry; the API serves them; a new run appends without touching any earlier record |

Held by `fullstack/tests/test_backup_current.py` (15 tests) and by the gate row
*Data: backup and restore*, which now restores this export on every evaluation.
Not restored into the Production project: it holds 0 rows and stays apart.
Runbook check for a backup before a Production deployment: `§7` then `§8`,
exactly as above. What this does not establish is unchanged (`§5`): no
schedule, no point-in-time recovery; cadence and owner wait on the Founder.
