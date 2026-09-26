# `FD-FS-001` — Authorization of the Full Stack Act and Its Boundaries

**Document type:** Founder Decision instrument
**Status: PROPOSED FOR FOUNDER DECISION.** Every decision field below is blank.
**Prepared by:** Claude Code (Co-Founder / CEO) · **Date:** 2026-09-26
**Concerns:** `ACT-CC-POST-P13-AIOS-FULL-STACK-001` (Register `§60`)

**No blank field may be read as approval.** Claude's recommendation is given
for each decision and is not a selection.

## Why a decision is needed

The Act was received as *"PROPOSED FOR FOUNDER AUTHORIZATION"*. Its `§5.3`
makes Founder authorization an entry criterion for FS-00 and states *"No
authority may be inferred from absence."* So nothing under the Act has
started: no FS-00 discovery, no tool call to a cloud connector.

Four more matters would each stop a stage once it started. The Act asks for
Founder intervention only where it is genuinely needed (`§30`), so they are
put forward now, in one instrument, rather than one at a time mid-program.

| # | Matter | Where it binds | Why Claude cannot decide it |
|---|---|---|---|
| D1 | Authorization of the Act | `§5.3`, `§33` | Founder's by the Act's own terms |
| D2 | Freeze `§10` deferred architecture | FS-04, FS-06, FS-08 | Reserved to the Architect; `FD-2` (Founder ≡ Architect) is open |
| D3 | Cloud accounts and spending | FS-08, FS-10; `§7.1` | Account creation, billing and payment are external dependencies |
| D4 | Production release authority | FS-09 → FS-10; `§6.3`; NC-24, NC-25 | The Act defers to *"where reserved by the existing governance model"*, which does not say |
| D5 | Two missing source documents | `§3` items 4 and 6 | Only the Founder can supply them or waive them |

## D1 — Authorization of the Act

| Option | Effect |
|---|---|
| **D1-A** Authorize | The Act is in force as received. FS-00 begins. D2–D5 bound only the actions they name |
| **D1-B** Do not authorize; revise | Nothing starts. The Founder states what to revise |

**Selection:** ______

*Recommendation: D1-A.*

## D2 — Freeze `§10` deferred architecture

The Freeze reserves these areas to the Architect, *"not frozen"*, each
awaiting *"an Architect decision before it enters any freeze"*. Its `§12`
adds that implementation of a deferred area *"must first be brought through
governance; implementation may not silently define them."*

| Area (Freeze `§10`) | Stage that needs it |
|---|---|
| Database implementation | FS-04 Data & State |
| Identity, Authentication | FS-06 Security & Authority Integration |
| Networking, Deployment, Scaling, Observability implementation | FS-08 Infrastructure & Cloud; FS-10 |

The Act's `§6.2` (2) and (4) allow repair only *"consistent with canonical
architecture"* and without *"silently alter[ing] certified architectural
meaning"*. So building these areas needs an Architect decision, not only
this Act.

| Option | Effect |
|---|---|
| **D2-A** ADRs for ratification | Claude drafts one ADR per area from the existing canon, as a single package. Each area is implemented only after its ADR is ratified by the holder of Architect authority. All other work continues meanwhile |
| **D2-B** Delegate implementation-tier choices | The holder of Architect authority delegates the implementation-tier choices for these areas to Claude within this Act. Claude records each choice as an ADR. The Freeze is not amended, and no entity is ratified. **Valid only if decided by the holder of Architect authority** (`FD-2` is open) |
| **D2-C** Keep reserved | FS-04, FS-06 and FS-08 stop at the reserved action. Only in-process work proceeds, so no deployed system can result |

**Selection:** ______ · **Decided as:** Founder / Architect / both ______

*Recommendation: D2-A. It keeps the Freeze intact, costs one ratification
round, and does not stop the stages that come first.*

## D3 — Cloud accounts and spending (FS-08, FS-10)

Connectors for Vercel, Supabase, Cloudflare, WorkOS and Manufact are listed
in this session. Claude has not called any of them. Whose accounts they
reach, and on what plan, is not established.

| Option | Effect |
|---|---|
| **D3-A** Named accounts, no spending | Claude uses only the accounts named below, and only free-tier or already-paid capacity. Any purchase, plan change or billing step is an external dependency (`§7.1`) and stops that action |
| **D3-B** Named accounts, with a ceiling | As D3-A, with authority to spend up to the ceiling below |
| **D3-C** No cloud | Deployment is local or in the container only. FS-10's live proof stops at the external dependency |

**Selection:** ______
**Accounts / providers:** ______
**Spending ceiling (D3-B only):** ______

*Recommendation: D3-A, naming one hosting provider and one database
provider.*

## D4 — Production release authority

The authority matrix reserves A19 *Final System Acceptance* to the Founder.
It does not name production release. The Act does not authorize
*"uncontrolled production deployment"* (`§32`), and it forbids deploying
*"merely because infrastructure exists"* (NC-24).

| Option | Effect |
|---|---|
| **D4-A** Separate Founder release decision | At FS-09 exit Claude submits a release package. Production release waits for the Founder's decision. Non-production environments proceed without it |
| **D4-B** Release on a passed gate | Claude may release to production once the FS-09 Production Readiness Gate passes |

**Under either option, Final System Acceptance (A19) stays with the
Founder**, and Operational AIOS is claimed only on final operational proof
(`§31`).

**Selection:** ______

*Recommendation: D4-A.*

## D5 — Missing source documents

Two of the Act's seven named sources are not in the repository:
- `§3` item 4, *AIOS Transition Manifest*;
- `§3` item 6, *AIOS Full Stack Development Roadmap recorded in Memikirkan
  Deployment AIOS*.

| Option | Effect |
|---|---|
| **D5-A** Supply | The Founder uploads them. They are received, pinned and recorded like Volumes 3 and 4 |
| **D5-B** Proceed without | They are recorded as absent sources. Nothing is reconstructed from them or attributed to them. Supplying them later remains possible |

**Selection:** ______

*Recommendation: D5-A if they exist as documents; otherwise D5-B.*

## What this instrument does not decide

- **Final System Acceptance (A19).** It stays Founder-reserved under every
  option.
- **`FD-2`** (Founder ≡ Architect) stays open. D2-B records who decided it,
  and does not settle `FD-2` in general.
- **No open item is closed:**
  - `FN-1`, `P7-I99`, `RG-1`, `FDP-P10-003`;
  - `G-02`, `G-06`, `G-07`, `G-10`;
  - `C6-A1`, `ADP-P10-001`.
- **P13 and Platform Organization stay closed.** No Phase 14 is created
  (NC-21).
