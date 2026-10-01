# AD-FS10-ESC03-R1 — Production Operational Edge Access: Architecture Selection

| Field | Value |
|---|---|
| **Decision ID** | `AD-FS10-ESC03-R1` (successor to the evidence-phase `AD-FS10-ESC03`, which is preserved unchanged) |
| **Decided by** | Claude Code / Co-Founder, as **ARCHITECT — FS-10 ESC-03 BOUNDED AUTHORITY** under `FDP-012` `§3`, `§5`, `§6`, `§7`, `§26` items 1–3, 8–10 (Register `§124`) |
| **Capacity basis** | `FDP-012` bounded grant. Not `FD-2` (not ratified, `§123`), and not `APT-CD1.1-AA-001` (in force; not the basis here) |
| **Date** | 2026-10-01 |
| **Register** | `§125` |
| **Release / LIVE** | **unaffected — PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED** |

## 1. Problem

`FDP-010-01` authorized the capability and `FDP-011` authorized the mechanism (O-A, a per-session automation bypass). The delivery and custody path is the blocker:
- the Vercel connector returns the bypass value on creation and needs it to revoke, which puts it in tool output (forbidden by `FDP-011` T5 and `FDP-012` `§8`);
- the cloud-environment variable (M1) failed process- and session-isolation gates (`§120`);
- provider-side credential injection (M-AC) was left unselected pending authority (`§121`–`§123`).

`FDP-012` grants the authority to select (`§3`, `§26` item 3).

## 2. Decision

**O-A is implemented as: a per-session Protection Bypass for Automation, created and revoked by the account holder in the Vercel dashboard, and delivered to this execution environment by provider-side credential injection (M-AC).**

The Claude Code cloud-environment *API credential* attaches the header `x-vercel-protection-bypass` (prefix cleared), at the agent proxy, only to the three T2 hosts:

| Host | Role (FDP-011 T2) |
|---|---|
| `aios-platform-adibelepp21-bytes-projects.vercel.app` | Production alias → serving deployment |
| `aios-platform-72l8flelz-adibelepp21-bytes-projects.vercel.app` | serving deployment `dpl_s8c6m…` |
| `aios-platform-9dhc3bfal-adibelepp21-bytes-projects.vercel.app` | designated verified rollback target `dpl_76CYC…` |

The client sends **only** the B3 bearer (`aios-operator`, from its private file). The bypass value never enters the VM, a command, an environment variable, a file, tool output, the transcript, evidence or the repository (provider-documented).

**Conditional fallback (`FDP-012` `§6` last paragraph, `§14`).** If the account holder finds the API-credentials feature unavailable (plan entitlement unknown; Pro/Max only), O-A is delivered by **M1 in a dedicated cloud environment**:
- a variable set by the account holder;
- read by `smoke.py --bypass-env` and never printed;
- the environment used only for O-A sessions, with no Routines and no concurrent sessions.

This is selected now so that the workstream does not stall.

## 3. Why this design (evidence, not preference)

| Requirement | M-AC delivery | Basis |
|---|---|---|
| Not in tool output, chat, logs, repository or evidence (T5; `FDP-012` `§8`) | met: *"never reaches Claude, the commands it runs, or the session's environment variables"* | provider documentation (`§121`) |
| Created by the account holder through the provider control plane (T5) | met: Vercel dashboard | T5 |
| Per session (D-1, T4, T6) | met procedurally: a new bypass per session; credential added and deleted per window | `§4` below |
| Revocable, independently verified (T7) | met **without the CEO seeing the value**: the account holder revokes at Vercel first; the CEO's next request (still carrying the revoked value) must answer **302**; then the credential is deleted | `§5` step 6 |
| T2 scope | met more tightly than a bare bypass: the proxy attaches it to the three T2 hosts only, not to other Production or Preview deployments | provider documentation |
| X2 unchanged | met: same Vercel bypass contract as FDP-009-03 | DV |
| B3 unchanged; no scope change | met: the bypass alone gives 401 on protected routes | DV (FDP-010 evidence) |
| No permanent bypass | met if the account holder revokes each session; the CEO verifies and reports a failure as a T7 incident | `§5` |

**Not selected, with reason:**

| Candidate | Reason |
|---|---|
| Connector-created bypass (tool output) | value in tool output and transcript (T5; `FDP-012` `§8` *"chat"*) |
| E-B standing bypass | `FDP-012` `§7`: *"NO PERMANENT BYPASS"* |
| E-C Trusted Sources OIDC | no issuer available to this environment; plan unknown (`§114`) |
| E-D Vercel identity for the CEO | interactive provider login in the session; seat and plan unknown |
| E-E runtime inside the boundary | scheduled only; a new operational surface; cron passage unknown |
| A relay outside X2 | public exposure (`FDP-012` `§7`) |
| A Vercel API token in M-AC (CEO creates bypasses) | a standing provider credential with team-wide authority; fails least privilege and *"no authority escalation through implementation"* |

## 4. Bounded acceptance of environment-wide attachment (Q-4)

M-AC attaches to **every** session and process in the environment that calls a listed host, until deleted. This is **not** technical session isolation, and it is not called that. It is accepted **with these controls**, under `FDP-012` `§3` (*bounded security architecture*):

1. **Window.** The credential exists only between the account holder's add and delete for one operating session.
2. **Hosts.** Only the three T2 hosts are listed.
3. **B3.** Required behind X2. The bypass alone reaches only public routes; protected routes answer 401. The `aios-operator` token exists only in the operating session's private file.
4. **No Routines.** Verified at window start (`list_triggers` empty).
5. **No concurrent sessions.** Verified at window start (`list_sessions`: no other running session in the environment).
6. **Revocation first, then deletion.** A credential the account holder forgets carries a **revoked** value (verified 302), not a live one.

**Residual risk recorded:**
- agent-proxy and Vercel logging of the header, and provider-internal telemetry, are undocumented;
- whether deletion is immediate, and whether running sessions keep the credential after deletion, are undocumented.

Each is neutralized by step-6 ordering: any retained copy is a revoked value.

## 5. Operating session procedure (per O-A session)

| # | Actor | Step |
|---|---|---|
| 1 | Account holder | Vercel → `aios-platform` → Settings → Deployment Protection → **Protection Bypass for Automation**: create one bypass, note `O-A <session-id> <date>` |
| 2 | Account holder | claude.ai/code → environment `MoriartyContent plan` → settings → **API credentials → Add credential**: Name `AIOS O-A`; Allowed websites: the three hosts of `§2`; Custom headers: Name `x-vercel-protection-bypass`, Prefix **cleared**, Value = the bypass; **Connect**. Then tell the CEO *"O-A credential installed"*, without the value |
| 3 | CEO | window checks: no Routines; no other running session; injection proven by `GET /api/v1/health` → **200** on each host. If 302, the running session did not receive the credential: report, and continue in a new session after rotating `aios-operator` (runbook `§15`) |
| 4 | CEO | operate and verify: smoke read-only on serving and target; Scenario B/C if needed; negative controls (`§6`); T8 evidence without any value |
| 5 | Account holder | **revoke** the bypass in the Vercel dashboard |
| 6 | CEO | verify revocation: each host → **302** (the proxy still sends the revoked value) |
| 7 | Account holder | **delete** the API credential |
| 8 | CEO | final evidence: session record, final access state |

**Fallback M1:**
- step 2 becomes *set `AIOS_OA_BYPASS` in a dedicated environment's variables and start a new session there*;
- the client uses `smoke.py --bypass-env AIOS_OA_BYPASS`;
- step 7 becomes *remove the variable*.

## 6. Verification design

| Control | Expected |
|---|---|
| With M-AC, no bearer → protected route | 401 (B3) |
| With M-AC + `aios-operator` → read routes | 200 |
| `aios-operator` → `POST /api/v1/agent-instances` | 403 |
| Invalid bearer | 401 |
| Preview host | not listed → 302 (no injection); Preview principal refused in Production (401) |
| Non-T2 Production deployment (e.g. `dpl_CHV72…` host) | not listed → 302 |
| No release / LIVE / deploy route | none exists (tests) |
| After revocation (step 6) | 302 on all three hosts |
| Value in VM | `env` names, files and transcript searched: absent |

## 7. What this decision does not do

- It does not ratify `FD-2`, revoke or rely on `APT-CD1.1-AA-001`, or change FDP-009, FDP-010 or FDP-011.
- It does not change X2 or B3 settings, scopes or code paths.
- It creates no permanent bypass and no public exposure.
- It does not declare Release or LIVE.
- It does not perform account-holder actions: steps 1, 2, 5 and 7 are account-holder controls (`FDP-010` `§4.2`).

## 8. Implementation notes (2026-10-01; Register `§126`)

- **Session runner:** `fullstack/deploy/oa_session.py` (tests: `fullstack/tests/test_oa_session.py`). It implements the CEO steps of `§5`: `preflight` for step 3, `verify [--write]` for step 4, `revoked` for step 6.
  - It has no bypass option and never reads, sends or prints the value: the proxy attaches it.
  - The client sends only the B3 bearer, from the CEO's private file.
  - The evidence holds no credential; the run aborts if a response echoes the bearer.
- **What "302" in `§5` and `§6` means.** X2 answers:
  - **302** to a browser-style request;
  - **401** *"Protected deployment"* to a JSON client, without `X-Request-Id`.

  The AIOS API sets `X-Request-Id` on every answer. So a 401 is attributed to X2 or to B3 by that header, never by the status alone. "302" in `§5` and `§6` reads as *stopped by X2* in either form.
- **Baseline before the account-holder steps** (`docs/fullstack/evidence/FS-10-OA-BASELINE-2026-10-01.json`):
  - `preflight` FAILS at injection: every T2 host is stopped by X2, so no credential is attached.
  - The unlisted Production deployment and the Preview are stopped by X2.
  - `revoked` PASSES: X2 is enforced on all three hosts, and the B3 bearer alone does not pass X2.
