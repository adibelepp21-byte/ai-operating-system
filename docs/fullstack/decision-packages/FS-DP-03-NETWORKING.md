# FS-DP-03 — Networking

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-03` (provisional) |
| **Area** | Networking — Freeze `§10`, Architect-reserved |
| **Status** | **RATIFIED — N1**, by the Founder as Architect in `ACT-CC-POST-P13-AIOS-FULL-STACK-004` `§8` (Register `§93`, `ACT-004-DG-01`); implementation form X2 selected under its delegation. Revision 2 (below) is the package as reviewed (`§89`); its recommendation stands as analysis |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | Vercel hosting; Supabase database; no spending (D3-A) |
| **Prepared by** | Claude Code, 2026-09-26; **Revision 2** 2026-09-27 (below), on the Founder's *"FS-09 — DECISION PACKAGE PREPARATION"* |

## Context

- The Frontend talks only to the Backend; the Backend alone reaches AIOS and
  the database (FS-02 `§1`).
- Locally the backend binds `127.0.0.1` only; `--host` must be given to bind
  anything else.
- No CORS is configured: the frontend is served from the same origin.

## Part A — Architectural decision (ADR-eligible)

**Question.** What may reach what?

**Recommended rule set:**

1. **One ingress**: the application edge serving the Frontend and
   `/api/v1` on **one origin**. No cross-origin API access.
2. **AIOS is never network-addressable.** It runs inside the backend process
   and has no listener of its own.
3. **The browser never reaches the database.** Only the backend holds a
   database credential (FS-DP-01 Part B, RLS with no browser policy).
4. **Egress** from the backend only to the database and, if chosen, the
   identity provider (FS-DP-02). Tools reach nothing external today; any
   future external Tool is its own decision (INV-12).

Alternative: a separate API origin with CORS. Not recommended; it widens the
attack surface for no requirement found in FS-01.

## Part B — Implementation decision (not ADR-eligible)

- TLS terminated by the host; HTTPS only; HSTS set at the edge.
- The host's default domain first. A custom domain needs DNS ownership, which
  is an external dependency, and may need a paid plan.
- Supabase reached over its TLS endpoint; connection pooling per FS-DP-05.

## Until decided

Local loopback only. Nothing is exposed.

## Exact decision required

- [ ] Part A rule set: as written · amended
- [ ] Part B: as written · amended; custom domain yes/no
- [ ] Decided as: Architect · Founder as Architect

## Revision 2 (2026-09-27): FS-09 Architect review package

Revision 1 above is unchanged. This revision states the current network path
and boundary first, as deployed and observed, then the decision.

### R2.1 Decision ID

`FS-DP-03` (provisional), revision 2. Register `§89`.

### R2.2 Exact architectural question

What may reach what in the deployed AIOS Full Stack:

1. **ingress**: through how many origins the console and `/api/v1` are served, and whether cross-origin API access exists;
2. **edge access**: whether requests must pass the host's deployment protection before reaching AIOS, or whether AIOS's own authentication (`FS-DP-02` B3) is the only gate. Surfaced by this revision (`R2.4`);
3. **AIOS addressability**: whether the Runtime has any network listener;
4. **database reachability**: who may reach the database;
5. **egress**: where the backend may connect;
6. **transport and domain**: TLS termination, HSTS, default or custom domain.

### R2.3 Canonical sources

| Source | What it requires |
|---|---|
| `FD-FS-001` D2-A; Freeze `§10` | networking is Architect-reserved |
| ACT-001 `§20` | Security: attack surface; Reproducibility: reproducible deployment |
| ACT-003 `§19`, `§32` | access control, environment separation; *"no unverified … routes"* before release |
| FS-02 `§1` | the boundary rule: the frontend talks only to the backend; only the backend reaches AIOS and the database |
| `FS-DP-01` Part B (ratified, `FS-ARCH-RAT-001`) | RLS on, no browser policy; the key only on the server |
| `FS-DP-04` A1 (ratified) | a static console plus a per-request Python function on Vercel |
| `FS-DP-02` B3 (ratified, `§81`) | bearer tokens verified against hashes |
| NC-04 (ACT-003) | Vercel protection is never bypassed except by an authorized mechanism |

### R2.4 Current implementation state: the network path and boundary

```text
Browser ──HTTPS──▶ Vercel edge (TLS by the host; *.vercel.app; deployment protection = a project setting)
   ├─ /, /app.js, /api.js, /styles.css …  ─▶ static files, fullstack/frontend
   │                                           (vercel.json: CSP, nosniff, no-referrer, X-Frame-Options DENY, COOP)
   └─ /api/v1/*  ─rewrite─▶ api/index.py: Python function, region icn1
                               └─ per request: one AIOS Runtime, in-process (no listener)
                                    └─HTTPS─▶ https://scfymftfzkpilqbgmfwv.supabase.co/rest/v1  (ap-northeast-2)
                                              server-side key; table aios_records, RLS on, no browser policy
```

| Boundary | As deployed (Preview) | Evidence |
|---|---|---|
| Origins | one per deployment: console and API on the same host; no CORS header is emitted | `vercel.json`; `fullstack/backend/api.py` |
| Response headers | console: the `vercel.json` set. API: `nosniff`, `no-referrer`, `DENY`, COOP, CSP `default-src 'none'; frame-ancestors 'none'`, `Cache-Control: no-store` on JSON | FS-08 check (all 34 responses); code |
| **Edge access** | **At FS-08 (`§86`)** `ssoProtection` was enabled (`all_except_custom_domains`): unauthenticated requests got 302 from Vercel. **Observed 2026-09-27 19:57Z: `ssoProtection` disabled** (`enabled: false`; password protection and trusted IPs also off). Claude Code did not change it: its only Vercel changes this session were the Preview `AIOS_OPERATOR_TOKENS` variable and the FS-08 bypass, created and revoked. Anonymous requests now reach AIOS: `GET /api/v1/health` → 200 on the latest Preview and on `aios-platform-eight.vercel.app`; `GET /api/v1/runs` → **401 from AIOS** (B3 holds) | `get_project` at 19:57Z; three read-only requests |
| Side effect of open edge | each anonymous refused request **appends an audit record** to the append-only store. The observation request above appended one (`seq` 86, `refused`, subject `null`). No other outside request was recorded after `seq` 85 | SQL on `aios_records`, 2026-09-27 |
| AIOS addressability | none: the Runtime lives inside the function for one request | `fullstack/deploy/vercel.py` |
| Database | only the function holds the key (a sensitive Vercel variable, **Preview scope only**; no Production variables exist). RLS on, no `anon`/`authenticated` policy; the project URL is a code constant, not configurable | `FS-ARCH-RAT-001` `§11.1`; migration `20260927062422` |
| Egress | the function connects only to the Supabase REST endpoint. The one Tool (`docs.read`) reads files bundled with the function | code |
| TLS / HSTS | TLS terminated by Vercel. **HSTS was not among the FS-08 checks: not verified** | — |
| Domains | three `*.vercel.app` aliases; no custom domain | `get_project` |
| Local | `python -m fullstack.backend serve` binds `127.0.0.1` unless `--host` is given | `__main__.py` |
| Production | `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj`, commit `22c0b49`: that tree has no `api/`, `vercel.json` or `fullstack/`, so Production serves **no AIOS application**. Untouched | `git ls-tree 22c0b49` |
| Rate limiting / firewall | none configured by this program | — |

Revision 1's *"Until decided: local loopback only"* was overtaken when
`FS-DP-04` was ratified and the Preview deployed. The deployed Preview already
follows revision 1's Part A rules 1–4. The edge-access question (item 2 of
`R2.2`) was not in revision 1.

### R2.5 Authority required

**Architect** (or the Founder acting as Architect; `FD-2` is open) for the
rule set. The **Founder** holds the project settings that implement edge
access (deployment protection is a Founder-held configuration in this
program), any custom domain (DNS ownership), and any paid protection or
firewall (D3-A).

### R2.6 Available options

**Part A: routing rule set** (revision 1, unchanged)

| ID | Option |
|---|---|
| **N1** | revision 1's rule set **as written**: one origin; AIOS never addressable; the browser never reaches the database; egress only to the database |
| **N2** | the rule set **amended** (the Architect states the amendment) |
| **N3** | revision 1's alternative: a **separate API origin with CORS** |

**Edge access** (surfaced in revision 2)

| ID | Option |
|---|---|
| **X1** | deployment protection required on every non-Production deployment (Previews); Production reachable by the internet, gated by AIOS authentication |
| **X2** | deployment protection on every deployment, Production included (the console is for operators only; B3 issues tokens only to operators) |
| **X3** | no edge protection anywhere; AIOS authentication is the only gate |

**Part B: transport and domain** (revision 1, unchanged): TLS and HSTS at the
edge, *as written* or *amended*; the host's default domain, or a custom domain.

### R2.7 Architectural consequences

| Option | Consequence |
|---|---|
| N1 | codifies what is deployed. No change to FS-02's boundary rule |
| N2 | depends on the amendment |
| N3 | a second origin: the browser makes cross-origin calls, CORS configuration becomes part of the API contract, and the console needs the API origin as configuration |
| X1 | two exposure classes: Previews private, Production public. Production's `/health` and 401s are internet-facing |
| X2 | the whole system is private at the edge. External tools (an uptime check, `FS-DP-06`) cannot reach it without an authorized path |
| X3 | the internet reaches every deployment, including Previews that run unreleased code on the shared store |
| Custom domain | leaves `all_except_custom_domains` protection: a custom domain is **not** covered by that mode |

### R2.8 Data and state consequences

* Every request that reaches AIOS and is refused **appends an audit record**,
  and nothing may delete it. Under X3 (and for Production under X1) anonymous
  traffic grows `fullstack-audit` without bound. Under X2 it cannot reach AIOS.
* While Previews and Production share one store (`FS-09-ENV` open), an open
  Preview edge lets outside traffic write into what may become Production's audit.
* N1, N2 and N3 change no data format.

### R2.9 Security consequences

| Option | Consequence |
|---|---|
| X1 / X2 | defence in depth: the host refuses unauthenticated traffic before any AIOS code runs, which shrinks the attack surface to the host's login |
| X3 | the B3 authenticator is the only barrier, and every AIOS route (including the `/health` Runtime start) is exposed to the internet. The audit growth of `R2.8` is a cheap denial-of-service and cost vector on the free plan |
| N3 | CORS misconfiguration becomes a new class of defect |
| HSTS | without it, a first visit over plain HTTP can be downgraded. The host's behaviour is to be verified, not assumed |

### R2.10 Operational consequences

* X1/X2: each live check needs a Vercel login or a Founder-authorized,
  revocable mechanism (as at FS-08). An external uptime check (`FS-DP-06`)
  cannot pass X2 without one.
* X3: no access friction for operators, and no protection either.
* A custom domain needs DNS ownership (external) and may need a paid plan.
* A setting can change outside the repository (as observed). Whichever option
  is chosen needs a check that the live setting matches it (`R2.11`).

### R2.11 Verification requirements

1. `vercel.json` routes exactly `/api/v1/*` to the function, and static files for the rest (existing test).
2. No `Access-Control-Allow-Origin` on any API response, and a cross-origin preflight not honoured (new test; live check).
3. The anon key cannot read or write `aios_records` (live check: RLS with no policy).
4. The function's only outbound host is the Supabase endpoint (code review plus test).
5. HSTS present on HTTPS responses, if Part B requires it (live check).
6. **Edge access matches the decision**: the project's protection setting read through the connector, and an unauthenticated request answered by the host (302/401) or by AIOS as decided. Repeated before any release, because the setting lives outside the repository.
7. The readiness gate's *reproducible deployment* row changes from BLOCKED only after 1–6 are recorded.

Live checks on a protected Preview need a new, temporary Founder
authorization. No bypass is created by this package.

### R2.12 Rollback implications

* N1–N3 and Part B are configuration and code: they roll back with the commit.
* Edge protection is a project setting that is reversible at once. **Records
  appended while the edge was open cannot be removed.**
* A custom domain's DNS reverts only after propagation.

### R2.13 Explicit non-scope

This package does not change the protection setting (it only records the
observation), create a bypass, add CORS, buy a domain or firewall, change
Production, or decide observability (`FS-DP-06`) or environment separation
(`FS-09-ENV`).

### R2.14 Dependencies

| On | Why |
|---|---|
| `FS-DP-04` A1, `FS-DP-02` B3 (ratified) | the deployment shape and the authentication this rule set assumes |
| `FS-09-ENV` | which store and which domain Production uses |
| `FS-DP-06` | an external uptime check needs an edge path (X2) |
| Founder | the protection setting, a custom domain, spending |

### R2.15 Whether it blocks FS-09

**Yes.** Gate row *Reproducibility: reproducible deployment* is BLOCKED on
it, and ACT-003 `§32` requires no unverified routes before release.

### R2.16 Analytical recommendation (**UNRATIFIED**)

> *Not a decision. Stands only as analysis until the Architect decides.*
> N1 (it describes what is deployed and verified), with **X2** while the
> console serves operators only, and at least X1. Part B as written, on the
> default domain. The Founder confirms whether the observed disabling of
> deployment protection was intended, because under X1 or X2 the current
> setting does not conform.

### R2.17 Exact decision required

- [ ] Part A: N1 · N2 (amendment stated) · N3
- [ ] Edge access: X1 · X2 · X3
- [ ] Part B: as written · amended; custom domain yes / no
- [ ] Decided as: Architect · Founder as Architect

