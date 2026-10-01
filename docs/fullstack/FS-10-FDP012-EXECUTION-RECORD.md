# FS-10 — FDP-012 Execution Record: Authority Reconciliation, ESC-03 Architecture, FDP-010 Completion Status

| Field | Value |
|---|---|
| **Decision** | `FDP-012` (verbatim: `docs/governance/acts/FDP-012-FS-10-FINAL-ARCHITECTURE-AUTHORITY-ESC03-RESOLUTION-FDP010-COMPLETION.md`; content sha256 `5ad7f321c463c7dbaf10998946a9933a2e165a82f6f5f582f8ff2c88ad64891f`; Register `§124`) |
| **Executor** | Claude Code / Co-Founder, ARCHITECT — FS-10 ESC-03 BOUNDED AUTHORITY (`FDP-012` `§3`) |
| **Architecture** | `AD-FS10-ESC03-R1-OPERATIONAL-EDGE-ACCESS-SELECTION.md` (Register `§125`) |
| **State reached** | **FDP-012 CANONICAL (`§124`) · ESC-03 ARCHITECTURE SELECTED (O-A, `AD-FS10-ESC03-R1`) · IMPLEMENTATION AUTHORIZED, NOT YET OCCURRED · ESC-03 NOT RESOLVED · STOPPED AT THE ACCOUNT-HOLDER ACTION BOUNDARY** (`FDP-010` `§4.2`): the next steps are account-holder controls the CEO cannot perform |
| **FDP-010 / FS-10** | NOT COMPLETE / NOT READY — completion needs one O-A session (`§5`) |
| **Release / LIVE** | **NOT AUTHORIZED · NOT ACTIVE** |
| **Date** | 2026-10-01 |

## 1. FDP-012 validation (before canonicalization)

| Check | Result |
|---|---|
| Founder-issued, explicit, complete | yes — *"Founder hereby DECIDES"* (`§26`), execution status *"GRANTED"* (`§27`) |
| Text persisted verbatim | byte-exact from the session transcript; hash above |
| Scope bounded | yes — FS-10 / ESC-03 / FDP-010 / FS-10 reconciliation (`§1`–`§3`, `§20`) |
| Exclusions | Constitution, Mission, Founder authority, governance and delegation models, permanent global appointment, Phase 14, Native Core #12, P12/P13, Platform Organization, certified roots, Release, LIVE, Final System Acceptance (`§3`) |
| Release / LIVE / FSA | stay Founder-reserved (`§19`, `§26` items 12–14) |
| Conflict with FDP-009 / FDP-010 / FDP-011 | none: they stay operative; FDP-012 governs only the specific workstream (`§4`, `§26` item 7) |
| Conflict with higher authority | **none unresolvable.** Engineering Constitution `§3.2` lets *"the Architect"* delegate a bounded, explicitly scoped portion of architectural-tier authority. FDP-012 states such a scope and the `§3.2` exclusions (Constitution, Domain Model semantics, cross-Department structure). The Founder's capacity to delegate rests on the same stated basis recorded in GDR-0015 for the Co-Founder delegation (`FD-2` implied, not ratified), on which every Founder delegation of Architect authority since has operated (ACT-004 `§7`, ACT-007, ACT-008). FDP-012 itself says so (`§2`) and does not ratify `FD-2`. Recorded as an **observation**; no source denies the basis |
| **Result** | **VALID → canonicalized at `§124`** (registration directed by the Founder's execution instruction, `acts/MI-FDP012-CANONICALIZATION-ESC03-FDP010-FS10-FINAL-EXECUTION.md`) |

## 2. Authority reconciliation for this workstream (`FDP-012` `§12`)

Historical records are preserved unchanged; this is the successor reconciliation.

| Item | Reconciled position for FS-10 / ESC-03 | Historical record |
|---|---|---|
| `FD-2` | **not ratified**; not relied on as the basis of this workstream | `§123` unchanged |
| Architect authority for FS-10 / ESC-03 | **Claude Code / Co-Founder, bounded, under `FDP-012` `§3`** | — |
| `APT-CD1.1-AA-001` | **in force, not revoked** (`FDP-012` `§26` item 5); not the basis for this workstream; its exclusions are unchanged. FDP-012 is the more specific grant (`§4`) | Appointment Register unchanged |
| Constitution `§3` | `§3.2` form met (explicit scope; exclusions); `§3.1` untouched | unchanged |
| GDR-0001 / 0015 / 0016 | precedent and appointments unchanged | unchanged |
| `FDP-009` `§8` (no CEO redesign of Production access architecture) | still operative outside the workstream; inside it, `FDP-012` `§3` (*"Production operational access architecture"*) is the specific grant | unchanged |
| `FDP-009-02` `§5.5` (*"appropriate architecture authority path"*) | for this workstream, that path is `FDP-012` `§3`. G-Q4 (`§123`) is resolved within the workstream: the selection is made under that path either way | unchanged |
| `FDP-010` `§4.2` (*"Provider credentials remain stored in the provider's appropriate secret mechanism"*) | **interpreted for this workstream** (`FDP-012` `§3`: authority-boundary interpretation, credential custody-path design). A per-session deployment-protection bypass is created and revoked by the account holder at Vercel. Holding it in the provider-operated credential store of the execution environment, under account-holder control, never in a conversational channel and never in the VM, is an *appropriate secret mechanism*. Not a general reinterpretation | FDP-010 unchanged |
| `FDP-011` | O-A remains the mechanism (`FDP-012` `§26` item 8). T5's *"authorized secure execution/secret-handling path"* is designated by `AD-FS10-ESC03-R1` | FDP-011 unchanged |
| `AD-FS10-ESC03` | evidence-phase ADR preserved; successor `AD-FS10-ESC03-R1` records the selection | unchanged |
| ESC-03 records relying on `FD-2` (`§123`, classes C/E) | preserved; for the current workstream the architectural basis is `FDP-012` | unchanged |

## 3. ESC-03 architecture

Selected in `AD-FS10-ESC03-R1`:
- **O-A**, a per-session bypass created and revoked by the account holder;
- delivered by **provider-side credential injection** to the three T2 hosts only;
- with the B3 bearer from the CEO's private file;
- conditional fallback: M1 in a dedicated environment.

The `FDP-012` `§6` conditions are addressed as follows:

| `FDP-012` `§6` condition | Status |
|---|---|
| provider capability actually available | **UNKNOWN until the account holder opens the dialog** (Pro/Max only). Proven at session step 3 (200 on injection) |
| provider behaviour sufficiently evidenced | documented (`§121`); verified at session step 3 (value absent from the VM) |
| credential custody acceptable | decided (`§2` FDP-010 `§4.2` row) |
| logging / telemetry understood sufficiently | undocumented provider-side handling is neutralized by revoke-before-delete: any retained copy is a revoked value (`AD-…-R1` `§4`) |
| exposure to Claude / session / process prevented | documented; verified at step 3 |
| bounded, revocable | three hosts; per window; revocation verified by 302 without the value |
| X2 / B3 enforced; environments separate; Release/LIVE unaffected; no permanent bypass | yes (`AD-…-R1` `§3`, `§6`) |

**Distinctions kept:** Founder Decision (FDP-012, issued) ≠ canonical registration (`§124`) ≠ architecture selection (`AD-FS10-ESC03-R1`, `§125`) ≠ implementation (**not yet**) ≠ verification (**not yet**) ≠ Release (Founder-reserved) ≠ LIVE (Founder-reserved).

## 4. Implementation done in this step

| Item | Change |
|---|---|
| `fullstack/deploy/smoke.py` | `--bypass-env NAME` (fallback M1): reads the bypass from a named variable, never prints it, aborts if unset; mutually exclusive with `--bypass-file`. Under M-AC no bypass option is passed: the proxy attaches it |
| Tests | `fullstack/tests/test_smoke.py` (3 new); guards for FDP-012's existence updated to admit only the registered Founder-issued record |
| Runbook `§15` | O-A session procedure (`AD-…-R1` `§5`) |
| Current authority, deployment head, Release Package `§23` | updated |

No Production, X2, B3 or variable change was made. No bypass exists (re-discovered 2026-10-01T17:17:47Z and again before commit, 2026-10-01T18:29:20Z: all three hosts 302; SSO `all_except_custom_domains`; no trusted IPs; project `updatedAt` `1790837188645`; the Production alias serves `dpl_s8c6m…`).

## 5. Completion criteria (`FDP-012` `§24`)

| Criterion | Status |
|---|---|
| FD-2 / Architect authority ambiguity reconciled for this workstream | **DONE** (`§2`) |
| AA-001 relationship reconciled | **DONE** (`§2`) |
| ESC-03 resolved | **NOT YET** — architecture **selected**; implementation and operational proof **PENDING** (one O-A session) |
| FDP-010 fully completed | **PENDING** — ESC-03 proof; rollback target re-verified through O-A |
| Production operational access actually usable | **PENDING** — account-holder steps 1–2 |
| X2 enforced | **YES** (302 on all hosts, no trusted IPs) |
| B3 enforced | **YES** (unchanged) |
| Operational credentials secure, bounded, revocable | **YES** — `aios-operator` hash-only, private file; no bypass exists |
| Rollback target valid and verified | **YES** — `dpl_76CYC…` (FDP-010 evidence); re-verification through O-A in the session |
| Positive / negative / security verification | **PENDING** (`AD-…-R1` `§6`) |
| Observability / audit evidence | existing; session evidence **PENDING** |
| Current documentation reconciled | **DONE** |
| Historical / certified records intact | **YES** (pinned by tests) |
| Final re-discovery | **DONE** for this step |
| FS-10 ready for the Founder Release Gate | **NO — PENDING** |
| Release not declared · LIVE not activated | **YES · YES** |

## 6. The boundary reached

The remaining steps need **account-holder actions** the CEO cannot perform: provider credentials and security controls stay *"external/account-holder controls"* (`FDP-010` `§4.2`). This is not a Founder decision; no decision is requested.

1. **Check:** whether the environment `MoriartyContent plan` dialog shows **API credentials** (Pro/Max). If not, use the M1 fallback in a dedicated environment (`AD-…-R1` `§5`).
2. **Create** one Protection Bypass for Automation in Vercel (Deployment Protection settings), noted `O-A <date>`.
3. **Add** the API credential: hosts per `AD-…-R1` `§2`; header `x-vercel-protection-bypass`; prefix cleared; value = the bypass. Then tell the CEO *"O-A credential installed"*, without the value. The product documentation (re-read 2026-10-01) states that a **new session** picks up environment settings, so the O-A session runs in a session started after the credential is added (`AD-…-R1` `§5` step 3).
4. **Later, on the CEO's signal:** revoke the bypass in Vercel, then delete the credential.

On step 3 the CEO runs the session (`AD-…-R1` `§5` steps 3–8):
- injection proof;
- smoke on serving and target;
- negative controls;
- FDP-010 completion evidence;
- revocation verification.

It then completes FS-10 reconciliation and stops at the Founder Release Gate.

## 7. Residuals outside FDP-012's completion criteria

`FDP-011` D-3 (**P-2**, the Founder principal) is still to be established. It needs the Founder's own `operator-token` entry (hash only, runbook `§2`). Its post-deploy verification can run in the same O-A session.
