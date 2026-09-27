# `ACT-CC-POST-P13-AIOS-FULL-STACK-003` — Execution Record (Authorized Act)

| Field | Value |
|---|---|
| **Act** | `docs/governance/acts/ACT-CC-POST-P13-AIOS-FULL-STACK-003-FINAL-FOUNDER-AUTHORIZATION.md`; *"FINAL — ISSUED"*, **AUTHORIZED** by the Founder (`§3`, `§35`) |
| **Register** | `§78` |
| **Date** | 2026-09-27 |
| **Terminal state this round** | **EXECUTION BLOCKED — AUTHORITY / DEPENDENCY BOUNDARY** (`§30`) |

## A. Authority (`§3`, `§5`, `§24`)

| Holds | Does not hold |
|---|---|
| Founder authorization of the Act: re-discovery, routing, implementation **of Architect-decided packages**, verification, EXT-03/EXT-05 resolution within `§12`–`§14`, the FS-08 gate, then FS-09 and FS-10 on PASS | Architect decision on FS-DP-05 or FS-DP-02 · Production Release Authorization · Final System Acceptance · LIVE |

The Act's own closing block states both packages are *"AWAITING ARCHITECT
DECISION"*. It names the Architect as *"Moriarty / designated Architect
authority"*. That identifies who may decide. It is not itself a decision
(`§6.2`: no option may be inferred *"from … this Act"*).

## B. Re-discovery (`§33` step 2)

| Item | Observed now | Change since Register `§77` |
|---|---|---|
| Vercel connector scope | `list_teams` returns `adibelepp21-bytes-projects` (`team_qTztRVft6qYBO4uqmLM9ENd7`); project and deployment reads work | **restored** |
| Preview deployments | latest `dpl_93UhCzUyFDCixELDcoaF16i2nhUR`, READY, target preview, commit `5ed6eb2`; every push to this branch deploys a Preview | readable again |
| Preview surface via the connector (`web_fetch_vercel_url`), `/` and `/api/v1/health` | **302 to Vercel SSO**; the app is not reached | still not accessible |
| Project environment variables | **none** (`envs: []`) | EXT-05 no longer UNKNOWN: `SUPABASE_SECRET_KEY` is **absent** |
| Supabase `aios_records` (`scfymftfzkpilqbgmfwv`) | 0 rows; RLS on; 2 triggers | unchanged |
| Production alias | 404; older deployment, untouched | unchanged |
| FS-DP-05 / FS-DP-02 `§R2.13` | empty | unchanged |

No share link was created, no protection setting was changed, and no SSO flow
was followed (`§12`, `§14`). The connector's fetch stopped at the SSO
redirect. The redirect's one-time parameters are not reproduced here.

## C. Architect decision routing (`§6`–`§8`)

Routed together, decided independently, **FS-DP-05 first**. Claude Code
does not fill any field below (`§6.3`). The Architect may answer in these
fields, in the packages' `§R2.13` blocks, or in a separate instrument.

### C.1 FS-DP-05 — Concurrency / Run Identity

**Problem.** A run's number is a count read at Runtime start. Under the
ratified per-request runtime (FS-DP-04 A1), two concurrent requests both mint
`run-00001`, and the first becomes unaddressable. This is reproduced
deterministically (`TheConcurrencyFinding`). The correct property is recorded
as an expected failure. There is no live exposure yet, because no request can
authenticate.

**Proposal C1 (not a decision).** A run takes its identity from its own
Runtime's identity, never from a store count. Order is the store's append
order. Trace for a run is selected by `runtime`, not by position. With it:
I1 (no idempotency key) and partial runs accepted as described.
Implementation boundary if ratified: `fullstack/backend/aios.py`, the
console's run-id display, the FS-02 blueprint's run-id text, and tests. Not
`native_core/`, `consumers/`, `tools/`, the migration, `vercel.json`, or any
certified root.

```text
FS-DP-05 — ARCHITECT DECISION
DECISION:                 [ RATIFY / REVISE / REDIRECT / DEFER / REJECT ]
OPTION:                   [ C1 / C5 / other ]   IDEMPOTENCY: [ I1 / I2 ]
PARTIAL RUNS:             [ accepted as described / other ]
RATIONALE:                [Architect-provided]
BOUNDARY:                 [constraints]
IMPLEMENTATION AUTHORITY: [derived only from the decision]
VERIFICATION REQUIREMENT: [as package §R2.8, or amended]
DATE:                     [date]
ARCHITECT:                [identity]
```

### C.2 FS-DP-02 — Authentication

**Problem.** Every protected route fails closed today: there is no
authenticator, so there is no run creation, no audit subject and no live
flow. The console already sends a bearer credential. The request model is
stateless.

**Proposal B3 (not a decision).** Operator bearer tokens. The Founder
generates each token offline. The host stores only SHA-256 hashes, with a
subject and scopes, in `AIOS_OPERATOR_TOKENS`. The backend compares hashes in
constant time. Claude never sees a token. Alternatives in the package:
B1a/B1b (Supabase Auth), B2 (WorkOS, which needs a Founder naming), and B4
(rejected). Open sub-decisions: initial principals and grants, token lifetime
and rotation, and whether Preview and Production share principals.
Implementation boundary if ratified: one `Authenticator` in
`fullstack/backend/security.py` and its composition. Scopes, `authorize`,
audit format, console, CSP, `native_core/`, `consumers/` and `tools/` are
unchanged.

```text
FS-DP-02 — ARCHITECT DECISION
DECISION:                 [ RATIFY / REVISE / REDIRECT / DEFER / REJECT ]
PART A:                   [ A1 / A2 ]   PART B: [ B3 / B1a / B1b / B2 / other ]
INITIAL PRINCIPALS/GRANTS:[ ]
TOKEN LIFETIME/ROTATION:  [ ]
PREVIEW vs PRODUCTION:    [ shared / separate ]
RATIONALE:                [Architect-provided]
BOUNDARY:                 [constraints]
IMPLEMENTATION AUTHORITY: [derived only from the decision]
VERIFICATION REQUIREMENT: [as package §R2.12, or amended]
DATE:                     [date]
ARCHITECT:                [identity]
```

**A consequence to know before deciding.** If B3 is ratified, live
verification also needs `AIOS_OPERATOR_TOKENS` set by the Founder in Vercel
Preview: hashes only, Sensitive, never through chat. It is an external
dependency of the same kind as EXT-05.

## D. Status model (`§25`)

| Item | Status |
|---|---|
| ACT-003 | AUTHORIZED |
| FS-DP-05 | PROPOSED · routed · **awaiting Architect** |
| FS-DP-02 | PROPOSED · routed · **awaiting Architect** |
| FS-DP-05 / FS-DP-02 implementation | NOT_STARTED (`§9`) |
| EXT-03 | **partly resolved**: read scope restored; Preview surface still behind SSO |
| EXT-05 | **BLOCKED**: secret absent from Vercel |
| Live Preview verification | NOT_STARTED |
| FS-08 | **BLOCKED** |
| FS-09 · FS-10 | NOT_STARTED |
| Founder Release | NOT AUTHORIZED |
| Operational AIOS | NOT YET OPERATIONAL |

**Frozen (`§27`):** implementation (needs the decisions), live verification
(needs EXT-03 Preview access, EXT-05, and the auth configuration), the FS-08
gate, FS-09 and FS-10. No independent authorized work is left that does not
depend on one of these.

## E. Required next inputs

| # | Holder | Input |
|---|---|---|
| 1 | Architect | FS-DP-05 decision (`§C.1`) |
| 2 | Architect | FS-DP-02 decision (`§C.2`) |
| 3 | Founder | `SUPABASE_SECRET_KEY`: Vercel `aios-platform` → Settings → Environment Variables, **Sensitive**, target **Preview**. Value from Supabase `scfymftfzkpilqbgmfwv` → API Keys → secret key |
| 4 | Founder | An authorized route to the SSO-protected Preview (`§14`). For example, a Protection Bypass for Automation secret you create yourself and store as a Sensitive value outside chat, or deployment protection disabled for Preview. Your choice; I will not create one |
| 5 | Founder | If B3 is ratified: the token hashes in `AIOS_OPERATOR_TOKENS` (Preview) |

## F. Unchanged

No code, test, `tools/`, manifest, reader, certified root, Vercel setting or
Supabase state changed. P12 and P13 are protected; the certified Successor V2
is byte-identical. Added: the Act (verbatim), this record, Register `§78`.
