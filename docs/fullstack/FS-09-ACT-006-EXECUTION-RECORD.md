# FS-09 — ACT-006 Execution Record

| Field | Value |
|---|---|
| **Act** | `ACT-CC-POST-P13-AIOS-FULL-STACK-006` — FS-09 Temporary Access Revocation & Final Re-Discovery (Register `§95`, `§96`) |
| **Date** | 2026-09-30. Continued by ACT-007 (`docs/fullstack/FS-09-ACT-007-EXECUTION-RECORD.md`): the revocation this record could not make was made there. This record stands as written |
| **Evidence** | `docs/fullstack/evidence/FS-09-ACT-006-REDISCOVERY-2026-09-30.json` |
| **Act classification** | **C. BLOCKED** (`§13`): the revocation, the Act's primary objective, could not be made. Re-discovery itself is complete |
| **FS-09 state** | unchanged: **EXHAUSTED_WITH_CLASSIFIED_REMAINDER**; not PASS |
| **Not** | FS-09 PASS · Production LIVE · Founder Acceptance · Operational AIOS · FS-10 started |

Evidence states are kept apart (ACT-006 `§10`): **DIRECTLY VERIFIED** (measured now, first hand) ·
**OBSERVED** (my own action log or a pattern scan) · **RECORDED** (an earlier record, not re-measured) ·
**INFERRED** · **UNKNOWN** · **BLOCKED**.

## 1. Current-state discovery

| Item | State | Class |
|---|---|---|
| Repository | branch `claude/aios-activation-authority-discovery-enq7bk`; start `6ffa6f5`, after receipt `ab18082`; tree clean | DIRECTLY VERIFIED |
| Deployment Protection | `ssoProtection` enabled, `all_except_custom_domains`; password protection and trusted IPs off | DIRECTLY VERIFIED |
| Temporary bypass (note *"TEMPORARY FS-09 re-verification 297e8b8"*) | created 2026-09-30 before 15:30Z; **no revocation recorded** | RECORDED; current presence **UNKNOWN** |
| Newest Preview | `dpl_5dx5p95up7MJjRfQxsaEC2DqKXRZ` (built from a push of this branch); the branch alias is still pinned to `dpl_FjjGC9Hg54RGzGSugwidwHdRTrwM` (`297e8b8`) | DIRECTLY VERIFIED |

## 2. W1 — revocation: BLOCKED

| Field | Value |
|---|---|
| Target | the entry noted *"TEMPORARY FS-09 re-verification 297e8b8"* |
| What the control needs | the bypass secret as a parameter. The Vercel connector lists no bypass entries (it hides the secrets), so an entry cannot be identified or revoked without it |
| Permission boundary observed | loading the secret from its private file into the session was denied by the permission classifier (*Credential Materialization*), at the end of ACT-005 and again under ACT-006 `§4`, after the Act was issued. The denial covers the outcome, not one command |
| What was **not** done (`§4.4`) | no other tool, script, transcript search or host was used to obtain the secret; no bypass generated; protection not changed; no revocation claimed. The revoke call itself was never made, so there is no Vercel response to record |
| Manual action | the Founder/user revokes the entry in Vercel: project `aios-platform` → Settings → Deployment Protection → Protection Bypass for Automation; **or** allows the session to load that file (a Bash permission rule for it), after which the revoke can be made here |

## 3. W2 — post-revocation posture (no revocation happened; measured as it stands)

| Check | Result | Class |
|---|---|---|
| V2.1 protection enabled | yes | DIRECTLY VERIFIED |
| V2.2 no active temporary bypass | **not evidenced** | UNKNOWN |
| V2.3 anonymous static access | newest Preview `/` and the branch alias `/`: 302 → `vercel.com/sso-api` | DIRECTLY VERIFIED |
| V2.4 anonymous protected API | `/api/v1/runs` on both: 302 → `vercel.com/sso-api`, answered by Vercel before the function. AIOS's own 401 was verified through the bypass on `297e8b8` (recorded, not re-measured here). The Preview store did not change (max seq 350, 345 rows), so no anonymous request reached the function | DIRECTLY VERIFIED (Vercel layer); RECORDED (AIOS layer) |
| V2.5 Production isolation | deployment `dpl_A5Qs4nVK3ufkseGv3brxGSYr3ivj` (`22c0b49`, target production, READY, aliases unchanged); Production variables: none; Production store `hmljfyqycxcueulhsjae`: **0 rows**; `aios-platform-eight.vercel.app` `/` → 302 SSO | DIRECTLY VERIFIED |

## 4. W3 — final re-discovery

Sources re-opened: the ACT-004/005/006 instruments (ACT-004 and ACT-005 byte-identical since `d64b179`), the ACT-005 record, gate v3, the FS-08 and FS-09 evidence, the FS-09 decision register and runbook, the FS-DP-06 and FS-DP-07 packages, `FS-09-ENV`, `FS-09-RUNTIME`, `fullstack/deploy/vercel.py`, the live project and deployment state, and both stores.

Gate v3 (`python -m fullstack.readiness evaluate`): **NOT PRODUCTION READY**, 26 PASS, 1 OBSERVED, 0 FAIL, **4 BLOCKED**; the `297e8b8` recording is current (no served code changed since).

## 5. Residual matrix

| | Fact | Owner | Authority required | Why it cannot be closed here | Evidence |
|---|---|---|---|---|---|
| **R-A** Scenario A | no source classifies Scenario A under **A1**. A1 remains the applicable architecture; no Agent-creating route exists. Founder decision still required. Nothing was selected | Founder | classify it a non-blocking residual, or choose A2/A3 | Founder-reserved; ACT-006 `§12` | RECORDED: FS-DP-07 status, Register `§93` DG-03, decision register `§2.1` |
| **R-B** Alerting | FS-DP-06 rev 2 `R2.6` keeps **Logging** (L1–L3), **Metrics** (M1–M3), **Alerting** (H1–H3) and **Readiness** (R1/R2) as separate mechanisms. **R2 = readiness** and is not an alerting selection. **No source selects H1, H2 or H3.** The package's own recommendation (lines 199–201) is unratified analysis | Founder as Architect | select H1, H2 or H3 (H1 may cost money, D3-A) | Architect-reserved; ACT-006 `§2`, `§12` | DIRECTLY VERIFIED (source text); Register `§93` |
| **R-C** E1 wiring | Production project exists ✔ · schema verified ✔ (recorded 2026-09-28; migration list re-read 2026-09-30: `20260928051800_aios_records`) · **application wiring ✘** (`vercel.py` names only the Preview project, last changed `a4a11cf`) · Production deployment ✘ · Production LIVE ✘ | Founder/user (session permissions) | allow the `vercel.py` edit (ACT-004 DG-04 authority stands) | the edit is application construction, outside ACT-006's bounded scope (`§2`, `§8`), and the earlier permission denial stands. Not attempted, not routed around | DIRECTLY VERIFIED (code, stores) |
| **R-D** Bypass | Protection **ON**; bypass **not shown revoked**; no revocation attempt reached Vercel | Founder/user | revoke it, or allow the file load (`§2`) | session permission; `§4.4` | protection DIRECTLY VERIFIED; bypass UNKNOWN / BLOCKED |

## 6. New findings

| # | Finding | Action |
|---|---|---|
| **N-1** | **No session can observe a bypass's absence.** The connector hides entries, and the only test needs the same secret load. After a manual revocation the evidence is the Founder's dashboard observation (RECORDED); a session can only add a first-hand check (a 302 with the old secret) if it may load the file | none possible here; stated in the handoff |
| **N-2** | ACT-005 record `§5` and Register `§92` say the FS-DP-06 package is *"unchanged since `5941d72` (SHA-256 `7aad41b3…`)"*. Its Status row changed at `7df974a` (ratification annotation). The option definitions are byte-identical to `5941d72` (`7aad41b3…` reproduces from that commit; the file now hashes `f16aabd3…`) | qualified in ACT-005 record `§5`; Register `§92` is append-only history and stands as written |
| **N-3** | the gate and two status documents said the bypass *"is still active"*: that was INFERRED, not observed | reworded to *"no recorded revocation"* (`fullstack/readiness.py`, decision register `§7`, readiness program `§11`); the row stays BLOCKED |

No other work is actionable under this Act.

## 7. Documentation reconciliation (`§11`), minimal

* `fullstack/readiness.py`: three phrases (N-3). Tests: 197 fullstack OK.
* `FS-09-ACT-005-EXECUTION-RECORD.md`: `§5` qualified (N-2); header points here. Its `§15`, `§19`, `§22` and Register `§94` describe the state at 2026-09-30 ~16:10Z and are **kept as written**.
* `FS-09-DECISION-REGISTER.md` `§7` and `FS-09-READINESS-PROGRAM.md` `§11`: bypass row reworded, pointer added.
* Historical evidence files untouched: `FS-09-LIVE-PREVIEW-2026-09-30.json` still says `access_revoked: false`, which is what was true when it was recorded and remains the last recorded state.

## 8. Negative controls (`§9`)

| NC | Result | Basis |
|---|---|---|
| 01 no new bypass | HELD | OBSERVED: no bypass-control call was made in this Act (not externally verifiable) |
| 02 protection not disabled | HELD | DIRECTLY VERIFIED |
| 03 no secret persisted | HELD | OBSERVED: a pattern scan of every line added since `297e8b8~1` finds no non-hex 32-character token. The value comparison made at `03e4b0e` is RECORDED; it was not repeated because it reads the file whose load was denied |
| 04 no Production release | HELD | `22c0b49` unchanged |
| 05 no Production environment mutation | HELD | DIRECTLY VERIFIED (no variables; deployment unchanged) |
| 06 no Production data mutation | HELD | DIRECTLY VERIFIED (0 rows) |
| 07 certified roots | HELD | integrity holds; `tools/` unchanged since `edb3beb` |
| 08 Native Core | HELD | `native_core/`, `consumers/` unchanged since `edb3beb` |
| 09 no Phase 14 | HELD | no p14/phase-14 path |
| 10 no P13 reopening | HELD | — |
| 11 no Scenario A decision invented | HELD | `§5` R-A |
| 12 no H1/H2/H3 invented | HELD | `§5` R-B |
| 13 no E1 success claimed | HELD | `§5` R-C |
| 14 verification ≠ Founder Acceptance | HELD | — |
| 15 exhaustion ≠ completion | HELD | `§9` |
| 16 no permission boundary bypassed | HELD | the credential-load denial was not worked around (`§2`) |
| 17 no unsupported VERIFIED | HELD | the bypass is UNKNOWN, not REVOKED |
| 18 stale evidence qualified | HELD | `§6` N-2, N-3; `§7` |

## 9. Terminal classification

```text
ACT-006 = C. BLOCKED   (revocation not made: session cannot load the secret; absence not evidenced)
Re-discovery = COMPLETE   Residuals A/B/C/D re-checked; none changed; none resolved
FS-09 = EXHAUSTED_WITH_CLASSIFIED_REMAINDER   FS-09 ≠ PASS
FS-10 = NOT STARTED   Production = untouched; not released; not LIVE
```

The single item that cleans up after this program's own action (the active bypass) is the one that needs a person. Until it is revoked, Preview deployment protection can be passed by anyone holding that secret; the API itself still requires the operator token for everything except `/health`.
