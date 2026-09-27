# FS-08 — Vercel & Supabase Discovery, Verification and Repair: Execution Record

| Field | Value |
|---|---|
| **Under** | the FS-08 Vercel & Supabase Act (Register `§66`), within `ACT-CC-POST-P13-AIOS-FULL-STACK-001` and `FD-FS-001` |
| **Executed** | 2026-09-27, by Claude Code |
| **Result** | **FS-08 BLOCKED.** The 404's cause is determined. The repair needs two Architect decisions and a Founder release decision. **Nothing was changed, deployed or written on either provider** |

Every row is marked **Observed** (reported by the provider or the
repository), **Inferred** (interpretation of observed facts) or **Unknown**
(not available through the interfaces I have) (Act `§6`).

## A. Vercel project

| Item | Value | Basis |
|---|---|---|
| Team | `adibelepp21-byte's projects` · `team_qTztRVft6qYBO4uqmLM9ENd7` | Observed |
| Project | `aios-platform` · `prj_exqF51HASzlwn5kiO4kAGJ9mHe0N` · created 2026-09-27 05:04:25 UTC | Observed |
| Repository binding | `adibelepp21-byte/ai-operating-system` (deployment metadata) | Observed |
| Production branch | `claude/aios-genesis-planning-hmbvlc`: the production deployment was built from it, and it is the repository's default branch (`git ls-remote --symref origin HEAD`) | Observed; that Vercel uses it *because* it is the default is Inferred |
| Framework preset | none (`framework: null`) | Observed |
| Node version | 24.x | Observed |
| Root directory, build and output commands | not reported | Unknown |
| Environment variables | none (`envs: []`, 0 hidden production) | Observed |
| Deployment protection | SSO on all deployments except custom domains; no password protection | Observed |
| Domains | `aios-platform-eight.vercel.app`, `aios-platform-adibelepp21-bytes-projects.vercel.app`, and a branch alias | Observed |

## B. Vercel deployment

| Item | Value | Basis |
|---|---|---|
| ID | `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` | Observed |
| Commit | `22c0b49`: *"Merge pull request #1 from …/claude/aios-activation-authority-discovery-enq7bk"* | Observed |
| Target, state | production · READY · type `LAMBDAS` · region `iad1` | Observed |
| Build | building 05:04:30 → ready 05:04:34 UTC (4.2 s) | Observed |
| Build log, runtime log, file tree | **403 Forbidden** (logs), **404 "File tree not found"** (files) through this connector | Unknown |
| Deployment URL | `aios-platform-lrz7nrx7n-…vercel.app` answers **302 to Vercel SSO** | Observed |

## C. The exact 404 cause

**Observed:**

1. `https://aios-platform-eight.vercel.app/`, `/index.html` and
   `/api/v1/health` all answer `404` with `content-type: text/plain`,
   `x-vercel-error: NOT_FOUND` and the body *"The page could not be found"*.
   That is Vercel's platform response. The backend's own 404 is JSON with
   `X-Request-Id` and security headers, and none is present.
2. Commit `22c0b49` contains **no `fullstack/` directory**. PR #1 merged this
   branch as it stood at `792bee7`. The 42 commits made on this branch since
   then are not in the deployed source: the post-P13 governance and Platform
   Organization work, and every Full Stack commit (`78d67e5` … `c6c589d`).
3. The deployed tree has no `index.html`, no `public/` or `api/` directory, no
   Vercel configuration, no Python dependency file, and no root-level Python
   entry file. Its only `index.py` is a historical module under
   `docs/architecture/history/`.

**Inferred** (high confidence from 1–3; the build log would confirm it, and
is Unknown):

- Vercel built the tree with no framework, found **no static output and no
  function route**, and so matches no path. Every request is answered by the
  platform. This is a **deployment-level 404**, not an application 404: no
  AIOS code was deployed.

**Independent second cause** (Observed from the repository at `c6c589d`, not
a deployment):

- Even the current branch has **no Vercel entrypoint**. The backend is a WSGI
  application built by `create_app(data_dir, …)`, served by
  `python -m fullstack.backend serve` (`wsgiref`). The console is static files
  under `fullstack/frontend`. Nothing maps either onto Vercel's model.
  Merging this branch alone would **still** return 404 (Inferred).

## D. Repository entrypoints

| Role | Actual | Vercel mapping today |
|---|---|---|
| Backend | `fullstack.backend.api.create_app` → WSGI `Application`; run by `python -m fullstack.backend serve --data-dir <dir>` | none |
| Frontend | static files in `fullstack/frontend/`, served by the backend at `/` and `/assets/*` | none |
| Readiness gate | `python -m fullstack.readiness evaluate` | not a web entrypoint |
| Deployment entrypoint | **none exists** | — |
| Configuration and dependency files | **none**: standard library only | — |

The backend needs a **writable, persistent data directory** at start
(`LocalAppendOnlyStorage`) and holds **one Runtime per process**.

## E. Required change

| Component | What it is | Class (Act `§8`) |
|---|---|---|
| A Vercel entry module exporting the WSGI app, plus routing so `/api/v1/*` reaches it and `/` and `/assets/*` serve the console | an adapter | would be CLASS-B **only once the two points below are decided** |
| **Where the store lives on Vercel**: the function filesystem is ephemeral, so a local store loses every run, Trace and audit entry between instances | persistence architecture | **CLASS-C**: FS-DP-01 |
| **How long a Runtime lives**: per request, or per warm function instance | deployment architecture | **CLASS-C**: FS-DP-04 Part A |
| **Putting the application on the production branch**: every merge to the default branch now deploys to the public production alias | production release | **Founder** (`FD-FS-001` D4-A) |

The required action as a whole is **CLASS-C — ARCHITECT-RESERVED**. The
adapter cannot be written without choosing the store and the Runtime
lifetime. An adapter that "just works" by writing to the temporary directory
would decide both silently, which Act `§2` forbids.

## F. Authority classification

**OUTSIDE AUTHORITY.** The repair depends on FS-DP-01 and FS-DP-04
(Architect), and deploying it to production is a release (Founder, D4-A).

## G. Files changed

| Path | Change | Reason | Authority |
|---|---|---|---|
| `docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-001-FS-08-VERCEL-SUPABASE-DISCOVERY.md` | new | the Act, persisted as received | Act `§23` (evidence recording) |
| `docs/fullstack/FS-08-VERCEL-SUPABASE-EXECUTION.md` | new | this record | same |
| `docs/fullstack/FS-08-INFRASTRUCTURE-AND-CLOUD.md` | status and facts updated | re-discovery | same |
| `docs/fullstack/decision-packages/FS-DP-01-DATABASE.md`, `FS-DP-04-DEPLOYMENT.md` | evidence added; questions sharpened | Act `§12`, `§22` | same |
| `fullstack/readiness.py`, `fullstack/tests/test_readiness.py` | external-dependency register updated | EXT-01 re-established; new EXT-03, EXT-04 | Act `§9` (Full Stack files) |
| Decision Register | `§66`, `§67` appended | record | governance practice |

**No deployment configuration, adapter or provider setting was created.**
`native_core/`, `consumers/` and `tools/` are unchanged.

## H. Deployment result

**No deployment was triggered.** Nothing was pushed to the production branch.
Pushes to this branch create no reachable deployment either: previews sit
behind Vercel SSO, and this connector is denied both preview access and share
links.

## I. Live smoke test

| Test | Result |
|---|---|
| Reachability of the production alias | reachable; **404 NOT_FOUND (platform)** on `/`, `/index.html`, `/api/v1/health` |
| Deployment URL | 302 to Vercel SSO |
| Frontend, backend, valid and failing requests, unauthorized and hostile input, AIOS path | **not testable**: no application is deployed |
| Secret exposure | none observed: the project holds no environment variables, and the responses carry no application data |

## J. Supabase state

| Item | Value | Basis |
|---|---|---|
| Organization | `adibelepp21-byte's Org` (`icmteawcgjikdkgdbutf`), **plan: free** | Observed |
| Project | `ai operating system` · ref **`scfymftfzkpilqbgmfwv`** · `ap-northeast-2` · created 2026-09-25 | Observed |
| Status | **ACTIVE_HEALTHY** · Postgres 17 (17.6.1.166, GA channel) | Observed |
| Connectivity | **VERIFIED** through the account connector: every read below succeeded | Observed |
| Schema | `public` has **no tables**; **no migrations**; no branches; no edge functions | Observed |
| Extensions installed | `plpgsql`, `pgcrypto`, `uuid-ossp`, `pg_stat_statements`, `supabase_vault`: the platform defaults | Observed |
| Security advisors | none | Observed |
| Backups | not exposed by the connector. Documentation: none downloadable on Free | Unknown (account); documented |
| Authentication and storage state | not exposed by the connector | Unknown |

**What yesterday's timeouts were.** On 2026-09-26 a project-scoped connector
was bound to `baacpvssvvxtezspclgj`, and three queries timed out. That ref is
**not among this account's projects today**, and today's project-scoped
connector answers *"You do not have permission"*. The timeouts were not the
AIOS project being down (NC-17). What that other ref is remains **Unknown**.

**Compared with the AIOS data model (FS-04):** the project is empty.
Nothing conflicts with FS-DP-01 and nothing is in place for it. The
append-only table, its revoked privileges and its RLS stance are FS-DP-01
Part B, unratified. **No schema was created.**

## K. Supabase MCP evidence

| # | Connector · operation | Class | Result |
|---|---|---|---|
| 1 | account · `list_projects` | read | one project, ACTIVE_HEALTHY |
| 2 | account · `list_organizations` | read | one organization |
| 3 | project-scoped · `get_project_url` | read | **permission denied** |
| 4 | account · `get_project` | read | as J |
| 5 | account · `get_organization` | read | plan free |
| 6 | project-scoped · `list_tables` | read | **permission denied** |
| 7 | account · `list_tables` (public) | read | `[]` |
| 8 | account · `list_migrations` | read | `[]` |
| 9 | account · `list_extensions` | read | as J |
| 10 | account · `list_branches` | read | `[]` |
| 11 | account · `list_edge_functions` | read | `[]` |
| 12 | account · `get_advisors` (security) | read | no lints |
| 13 | account · `get_project_url` | read | `https://scfymftfzkpilqbgmfwv.supabase.co` |

All on 2026-09-27. No write operation, SQL statement, key read or restore
was made.

**Vercel operations, same day:** `list_projects` and `list_deployments`
scoped to the team (403 forbidden, then re-scoped), `list_teams` (empty),
`list_projects`, `list_deployments`, `get_project`, `get_deployment`,
`list_deployment_events` (403), `web_fetch_vercel_url` ×2 (denied),
`get_access_to_vercel_url` (denied), `list_deployment_files` (404),
`filter_project_envs` (no values requested; empty), `get_runtime_logs` (403).
All reads.

## L. External dependencies

| ID | Provider | Dependency | Needs |
|---|---|---|---|
| EXT-01 | Supabase | **re-established**: the AIOS project is reachable and healthy through the account connector | nothing now; see EXT-04 |
| EXT-03 | Vercel | the connector cannot read build or runtime logs, open previews, or make share links for team `adibelepp21-bytes-projects` | re-authorize the Vercel connection with that team's scope. This blocks **live verification of any preview** |
| EXT-04 | Supabase | the project-scoped connector is denied permission, and yesterday was bound to another ref | re-bind it to `scfymftfzkpilqbgmfwv`, or rely on the account connector |
| EXT-02 | Founder | S-01 *AIOS Transition Manifest* | unchanged |
| — | Vercel / Supabase | plan and spending: both free; nothing requested | unchanged (D3-A) |

## M. Architect and Founder decisions

| Decision | Holder | Exact question now |
|---|---|---|
| **FS-DP-04 Part A** | Architect | On Vercel, does a Runtime live per request, or per warm function instance? Is the application deployed as one Python function serving both the API and the console, or as static console plus function API? |
| **FS-DP-01** | Architect | Where does the deployed store live? Supabase (`scfymftfzkpilqbgmfwv`, empty, free) as the backend beneath `StorageFacility`, or nothing persistent until decided? |
| FS-DP-02, 03, 06 | Architect | unchanged |
| **Release control** | **Founder** (D4-A) | Every merge to the default branch now deploys to the public production alias. Should Vercel's production branch be moved to a dedicated release branch, so merging is not releasing? Until then, **merging the Full Stack work into the default branch is itself a production release.** |

**Work that continues independently:** none remains on FS-08 without these.
FS-00 … FS-07 stand, and the local system and its tests are unaffected.

## N. FS-08 status

**FS-08 BLOCKED**: on FS-DP-01 and FS-DP-04 (Architect), the release control
question (Founder), and EXT-03 for any live verification. The 404 is
explained, not repaired. No claim of Production Ready, Production Released or
Operational AIOS is made.
