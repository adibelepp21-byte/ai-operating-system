# FS-08 — Infrastructure & Cloud: Discovery and Requirements

| Field | Value |
|---|---|
| **Stage** | FS-08 Infrastructure & Cloud (Act `§19`) |
| **Authority used** | `FD-FS-001` D3-A: *"Claude Code may use available connectors for read-only discovery and configuration inspection where permitted."* |
| **Result** | **BLOCKED** at provisioning. The requirements are defined (FS-02 `§8`). Networking, Deployment, Database and Observability await ratification (FS-DP-01, 03, 04, 06); the named database is unreachable (EXT-01) |
| **Nothing was created, changed, purchased or deployed** | every connector call below is a read |

## 1. Provider rule (Act `§19`)

```text
AIOS Requirements → Infrastructure Architecture → Provider Evaluation → Provider Selection → Implementation
```

- **Requirements**: FS-02 `§8`.
- **Infrastructure architecture**: FS-DP-01 … FS-DP-06, Part A. Proposed; not
  ratified.
- **Provider selection**: made by the Founder (D3-A: Vercel, Supabase).
- **Provider evaluation**: `§3` below.
- **Implementation**: not started. It needs the architecture first.

## 2. Read-only discovery (MCP usage)

| # | Connector · operation | Result |
|---|---|---|
| 1 | Vercel · `list_teams` | one team, `adibelepp21-byte's projects` (`team_qTztRVft6qYBO4uqmLM9ENd7`) |
| 2 | Vercel · `get_team` | name, slug, id. **The plan tier is not reported** |
| 3 | Vercel · `list_projects` | one project, `desktop-tutorial`, not related to AIOS. No AIOS project exists |
| 4 | Supabase · `get_project_url` | a project exists: `https://baacpvssvvxtezspclgj.supabase.co` |
| 5 | Supabase · `list_tables` (public) | **connection timeout** |
| 6 | Supabase · `list_migrations` | **connection timeout** |
| 7 | Supabase · `list_branches` | none |
| 8 | Supabase · `list_tables`, retried | **connection timeout** |
| 9 | Vercel · documentation search ×4; Supabase · documentation search ×1 | facts in `§3` |

Not called, on purpose: anything that creates, deploys, changes settings,
reads secret values or keys, or involves billing. Publishable keys were not
read (NC-10).

## 3. Provider facts that bear on the decisions

From the providers' own documentation, retrieved 2026-09-26:

| Fact | Source | Bears on |
|---|---|---|
| Supabase pauses Free-plan projects with low activity over 7 days; a paused project can be restored within 90 days | Supabase *Project Pausing* | FS-DP-01; availability; EXT-01 |
| *"Database backups are not available for download for Free Plan projects."* | Supabase *Production Checklist* | FS-DP-01 Part B backup; FS-09 data criteria |
| Vercel's Python runtime takes WSGI entrypoints (Django and Flask guides; `[tool.vercel] entrypoint = "module:app"`; `maxDuration` per function) | Vercel framework guides | FS-DP-04 Part B. That a framework-free WSGI callable is served unchanged is **inferred, not confirmed** |
| Rolling back to a specific older deployment (`vercel rollback <url>`) is documented as a Pro or Enterprise feature | Vercel *Rollback* | FS-DP-04 Part B rollback; FS-09 reliability |
| The plan tier of the team and the Free/Hobby terms of use | **not established**: the connector did not report the plan, and the documentation search returned no terms page | FS-DP-04; D3-A |

**Consequence.** Under D3-A (no spending), the Supabase Free plan gives no
downloadable backup and pauses on inactivity. The FS-09 backup criterion can
then be met only by an operator-run logical export, and availability depends
on regular activity. FS-DP-01 now records this. The Architect may still choose
Supabase Free; the Founder may choose to spend. Neither is Claude's decision.

## 4. What FS-08 would build once ratified

| Item | Waits on |
|---|---|
| `SupabaseStorage(StorageFacility)` adapter, append-only table, RLS with no browser policy, versioned migration | FS-DP-01; EXT-01 |
| Real `Authenticator` | FS-DP-02 |
| Vercel project, the WSGI entrypoint, static assets, environment variables, preview environment | FS-DP-03, FS-DP-04 |
| Structured request logs; readiness beside liveness | FS-DP-06 |

## 5. Exit determination (`§19`)

| Criterion | Result |
|---|---|
| Infrastructure reproducibly provisioned | **BLOCKED** (FS-DP-01, 03, 04) |
| Dev / staging / production topology | **BLOCKED** (FS-DP-04) |
| Secrets controlled | Nothing is provisioned, so no secret exists. The backend holds none |
| Network / security boundaries verified | Local only (loopback); production **BLOCKED** (FS-DP-03) |
| Observability functional | Trace and audit work; the rest **BLOCKED** (FS-DP-06) |
| Backup / recovery verified | Local store: verified (`test_a_copied_store_restores_every_record`). Production **BLOCKED** (FS-DP-01; Free has no downloadable backups) |
| Deployment pipeline functional | **BLOCKED** (FS-DP-04) |
| Infrastructure tests pass | None to run |

**FS-08: BLOCKED.** All independent work is done. The stage advances once the
minimum decision set (FS-DP-01, 02, 03, 04, 06) is ratified and EXT-01 is
cleared.
