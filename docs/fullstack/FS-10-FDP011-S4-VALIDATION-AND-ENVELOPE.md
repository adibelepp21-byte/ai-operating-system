# FS-10 — FDP-011: S4 Validation, Canonicalization, Implementation Envelope and S5 Status

| Field | Value |
|---|---|
| **Decision** | `FDP-011` (verbatim: `docs/governance/acts/FDP-011-FS-10-ESC03-PER-SESSION-X2-OPERATIONAL-ACCESS.md`; content sha256 `5a6e5a8b3cf449824fbc5ae55eeb59ebf4ebf22d5579a17b8f807116820f1296`; Register `§117`) |
| **Instructions** | Resume Gate MI (`MI-FS10-FDP011-FOUNDER-DECISION-COMPLETION-RESUME-GATE.md`, sha256 `b28d79aa…`); Submission & S4 Resume Instruction (`MI-FS10-FDP011-SUBMISSION-S4-RESUME-INSTRUCTION.md`, sha256 `eaf0159b…`) |
| **Package answered** | `decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md` — **unchanged** (byte-identical to `cea0d68`) |
| **S4** | **PASS** — valid, complete, no conflict; **canonical** at Register `§117` |
| **S5** | **BLOCKED (H8 credential boundary)** — no T5-compliant path exists in this execution environment for the bypass value; no implementation performed |
| **State** | **A. BLOCKED — SECURITY (credential custody under FDP-011 T5 / FDP-010 `§11.4`)** |
| **Release / LIVE** | **PRODUCTION RELEASE = NOT AUTHORIZED · LIVE = NOT ACTIVE** (Founder-reserved) |
| **Date** | 2026-10-01 |

Evidence classes: [CAN] canonical · [DV] directly verified · [PD] provider-documented · [UNK] unknown · [INF] inferred.

## 1. S4 re-discovery

| Item | Result |
|---|---|
| `FDP-009` `33fecb97…`, `FDP-010` `fa1d8b12…`, ESC-03 Act `b09e56ed…`, `AD-FS10-ESC03` `d10a16af…`, ESC-03 MI `549c39eb…` | recomputed; each found in the Register [DV] |
| Register | last entry `§116`; **`§117` free** [DV] |
| Decision package | byte-identical to `cea0d68` [DV] |
| FS-09 gate | byte-identical to `de47057` [DV] |
| X2 / Production | as at Register `§116`: SSO on, no bypass, no trusted IPs; project `updatedAt` `1790837188645`; serving `dpl_s8c6m…`; target `dpl_76CYC…` [DV] |
| Received text | both messages extracted byte-exactly from the session transcript; the persisted fences equal them [DV] |
| Variance | the submission message opens with an undesignated copy of the decision; it differs from the `§0`-designated instrument in one line (T4, *"It"* / *"The bypass"*), same meaning. The designated instrument is canonical |

## 2. Validation (Submission `§2`)

| # | Requirement | Result |
|---|---|---|
| 1 | D-1 is a package choice | **PASS** — O-A (package `§17`) |
| 2 | O-A corresponds exactly to E-A | **PASS** — *"Founder authorizes E-A per-session bypass"* = package `§11` E-A |
| 3 | T1–T9 populated | **PASS** — all nine stated |
| 4 | D-3 populated | **PASS** — P-2 with `aios.observe`, `aios.workflow.run`, `aios.audit`; no `aios.agent.register`; all in `security.SCOPES` |
| 5 | Release / LIVE Founder-reserved | **PASS** — stated, and constraints 4–6 |
| 6 | No silent expansion of CEO capability | **PASS** — T3: *"does not expand the CEO's underlying capability or authority"*; duties are those of `FDP-010` `§13` |
| 7 | No silent change to B3 | **PASS** — constraint 7 |
| 8 | No X2 change beyond the per-session mechanism | **PASS** — constraints 1–3; T4 per session |
| 9 | No conflict with higher authority | **PASS** — R2.10 admits *"a Founder-authorized, revocable mechanism"*; R2.5 Founder-held settings decided by the Founder; `FDP-009-02` `§5.5` architecture path held by the Founder (`FD-2` open); MI `§30` (no permanent bypass) respected; constraint 8 |
| 10 | No contradiction with FDP-009 / FDP-010 except by T9 | **PASS** — T9 *extends* `FDP-009-03` from verification to the stated operational duties and keeps its security and revocation requirements; `FDP-010` `§11.4` is kept and governs T5 |

**Interpretive notes (no ambiguity of operative meaning):**
- **T5 actor.** *"created … by the authorized account holder"*. `FDP-010` `§4.2` names the provider account holder; `§4.3` separates the operational principal from provider account ownership. Under either reading of who acts, T5 forbids the value in *"normal tool output"* and forbids tool-output transmission unless `§11.4` explicitly permits it, which it does not. The operative consequence is therefore unambiguous (`§4` below).
- **T4 expiry.** Provider documentation shows no automatic expiry for Protection Bypass for Automation (expiry exists only for shareable links, `ttl`) [PD]. T4's fallback applies: explicit end-of-session revocation and verification are mandatory.
- **T2.** A deployment becomes reachable under O-A only while it is the serving deployment or the designated verified rollback target (today `dpl_s8c6m…`, `dpl_76CYC…`).

**S4 result: VALID AND COMPLETE → canonicalized** (verbatim record, hash, Register `§117`, re-discovered; package unchanged and linked from the record and the Register).

## 3. Implementation envelope (Submission `§4`)

| Action | Class | Basis |
|---|---|---|
| Per-session automation bypass for the Production project, used to reach the serving deployment and the designated rollback target with the `aios-operator` bearer, for `FDP-010` `§13` duties | **AUTHORIZED WITH BOUNDARY** | FDP-011 D-1, T1–T4, T9 |
| Revocation at session end and on every T7 trigger; independent verification (302) | **AUTHORIZED (mandatory)** | T7 |
| Session evidence (T8 fields, never the value) | **AUTHORIZED (mandatory)** | T8 |
| Creating the bypass through the Vercel connector (`update_project_protection_bypass`) | **NOT AUTHORIZED** — the response carries the value (`protectionBypass` is keyed by the secret) [DV, earlier sessions; PD]; a caller-chosen value would sit in the tool input | T5; `FDP-010` `§11.4` |
| Revoking it through the connector | **NOT AUTHORIZED** — the request must carry the value (`revoke.secret` is required) [PD] | T5 |
| Receiving the value in chat | **OUTSIDE AUTHORITY** | T5; `FDP-010` `§4.2`, `§11.4` |
| Receiving the value through another secret path (e.g. a variable set by the account holder in this cloud environment's settings, read only from the environment) | **REQUIRES FOUNDER DECISION** — T5 requires *"an authorized secure execution/secret-handling path"* and names none; nothing beyond explicit authority is assumed (Submission `§4`) | T5 |
| Preview access via the mechanism | **NOT AUTHORIZED** | T1 |
| Other Production deployments | **NOT AUTHORIZED** | T2 |
| Standing / permanent bypass; public exposure | **NOT AUTHORIZED** | D-1; constraints 1–3 |
| Founder principal `P-2` in Production `AIOS_OPERATOR_TOKENS` (hash only; three scopes) | **AUTHORIZED WITH BOUNDARY** | D-3; B3; runbook `§15` |
| Custody of the Founder principal's plaintext by the CEO | **NOT AUTHORIZED** — separate identity and authority subject (constraint 9); plaintext never in chat (`§11.4`) | D-3 |
| Release, LIVE, traffic activation, B3 or scope changes | **OUTSIDE AUTHORITY** | D-1; constraints 4–8 |

## 4. S5 status — O-A

**BLOCKED before any provider action (Submission `§6`, `§14`: *"If the available execution environment cannot safely handle the credential without violating FDP-010 §11.4: STOP. Do not improvise another mechanism."*).**

| Lifecycle step | Path available to the CEO here | T5-compliant? |
|---|---|---|
| create | connector `update_project_protection_bypass` → value in tool output (or, with `generate.secret`, in tool input) | **no** |
| deliver to the execution environment | chat — forbidden; a secret path set by the account holder — not authorized by name (`§3`) | **not established** |
| use | `smoke.py` / client reads the value from a file or environment variable and never prints it | yes, once delivered |
| revoke | connector `revoke` → value in tool input | **no** |
| verify revocation | request with the revoked value from the file/environment → 302 | yes |

Nothing was created, configured or deployed. X2, B3 and Production are unchanged.

## 5. S5 status — P-2 (Founder principal)

Authorized (D-3) but **not executable now**:

1. **Plaintext custody.** The Founder's token must reach only the Founder. The CEO must not hold it (constraint 9) and it cannot pass through chat (`§11.4`). A path inside the existing B3 model that keeps the plaintext with the Founder alone: the Founder generates the token locally and supplies only its SHA-256 (a hash is not a secret; B3 stores hashes only). The subject name is an implementation detail (`security.py` documents `founder` as its example).
2. **Post-deploy verification.** A change to `AIOS_OPERATOR_TOKENS` takes effect only on deployment; runbook `§15` deploys twice (new rollback target, then serving) and verifies both (smoke, 403 on `aios.agent.register`). Verification of a Production deployment needs an X2 path, which is O-A (blocked, `§4`). Deploying without verification would leave Production unverified (MI `§1` item 21).

## 6. FDP-010 and FS-10

| Item | Status |
|---|---|
| ESC-01 | principal exists, verified (FDP-010 evidence); **usable through X2: not yet** (O-A blocked) |
| ESC-02 | target `dpl_76CYC…` verified; rollback execution via the control plane available; post-rollback API verification needs O-A |
| ESC-03 | **decided** (FDP-011, O-A); **NOT RESOLVED** — not implemented, not usable |
| FDP-010 | **NOT COMPLETE** (MI `§21` items 3, 4) |
| FS-10 | not READY (Resume Gate MI `§15`) |

## 7. Founder input required

1. **T5 secret-handling path for the O-A bypass** — the account holder's create/deliver/revoke path that keeps the value out of chat, tool output and logs (for example: the account holder creates and revokes the bypass in the Vercel dashboard and places the value in this cloud environment's settings, which a new session reads; or another path the Founder names; or an explicit permission under `§11.4`). Facts: a value set in the environment settings is picked up by a **new** session; the connector paths expose the value (`§4`).
2. **P-2 token hash** — or another custody path for the Founder principal's plaintext.

Neither is selected here.
