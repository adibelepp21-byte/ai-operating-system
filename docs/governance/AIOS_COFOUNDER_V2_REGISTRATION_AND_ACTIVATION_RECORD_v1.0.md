# AIOS Co-Founder V2 — Canonical Registration & Activation Record v1.0

| Field | Value |
|---|---|
| **Record ID** | `REG-CFV2-001` |
| **Activation ID** | `ACT-CFV2-CEO-001-A` (Part D §D.4) |
| **Delegation registered** | `DEL-CFV2-CEO-001` — `AIOS_DELEGATION_REGISTER_v1.0.md` §12 |
| **Decisions registered** | `GDR-0038` · `FD-V2-001` … `FD-V2-013` — `AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md` §14 |
| **Date** | 2026-09-23 |
| **Founder** | Moriarty |
| **Authority for this record** | Founder directive, 2026-09-23 (`acts/FOUNDER-DIRECTIVE-COFOUNDER-V2-TRANSITION.md`): *"REGISTRATION: AUTHORIZED / ACTIVATION: AUTHORIZED"*; its `§17` and `§18` |
| **Recorded by** | Claude Code, recording under explicit Founder direction |
| **Status** | **V2 GOVERNANCE RECONCILED · REGISTERED · VERIFIED · ACTIVE** (Part D) |

**Authority disclaimer.** This record **records** a registration and an
activation that the Founder directed. It does not approve anything. The
approval is the Founder's, and it is evidenced in Part A §A.3. The record adds
no authority beyond the Founder-approved files. Where it appears to conflict
with the Engineering Constitution, the Canonical Domain Model, or a Founder
decision, those govern.

**The ID codes in this record are recording conventions** (`REG-`, `DEL-`,
`ACT-…-A`, `RD-`, `C-`, `SD-`). They follow the existing register conventions,
and they grant nothing.

---

## Part A — Canonical Registration

### A.1 What is registered

| # | Artifact | Document ID | Role in V2 | Repository path |
|---|---|---|---|---|
| F01 | Authority Reconciliation & Governance Impact Matrix | none stated | Reconciliation input behind F02; self-described design material | `cofounder-v2/F01_…_GOVERNANCE_IMPACT_MATRIX.txt` |
| F02 | Founder Decision & Authority Transition Record | none stated | **Founder Decisions** `FD-V2-001` … `FD-V2-013` | `cofounder-v2/F02_…_TRANSITION_RECORD.txt` |
| F03 | Governance Baseline — Co-Founder V2 Authority Reconciliation / Amendment | `AIOS-GOV-BASELINE-AMENDMENT-V2-001` v2.0 | **Governance Baseline amendment** | `cofounder-v2/F03_…_AMENDMENT.md` |
| F04 | Co-Founder Delegation Charter V2.0 | `AIOS-COFOUNDER-CHARTER-V2-001` v2.0 | **Delegation instrument** — what authority is delegated | `cofounder-v2/F04_…_CHARTER_V2.0.md` |
| F05 | CEO Operating Mandate & Execution Protocol | `AIOS-CEO-OPERATING-MANDATE-V2-001` v2.0 | **Operating protocol** — how that authority is exercised. Parent: F04 | `cofounder-v2/F05_…_PROTOCOL_V2.0.md` |
| — | Founder transition directive | none issued | Registration and activation instruction | `acts/FOUNDER-DIRECTIVE-COFOUNDER-V2-TRANSITION.md` |
| — | This record | `REG-CFV2-001` | Registration Record, Authority Matrix freeze, Activation Record | this file |

This record, the Delegation Register entry and the Decision Register entries
together satisfy F03 `§26` items 1–5 (Charter · Mandate · Authority Matrix ·
Canonical Registration Record · V2 Activation Record). They also satisfy F04
`§40` items 1–9 and F05 `§48`. The mapping is in §A.5.

### A.2 Byte-exact persistence

Each file was copied unchanged from the Founder's upload. The sha256 was taken
before and after the copy, and both matched.

| # | sha256 |
|---|---|
| F01 | `7d841bef9c1fa220c2b16b9aae3f69f6d1b2c3be435f608f607114b095cca8b6` |
| F02 | `adae30d9c48cca2b30a1e0fb80ce44c4be96036004584fb76848611a3b759ea3` |
| F03 | `eb79eeea6677a67a260351e4de4b6c6bc802c452e1ebcedb798b820e9db3edde` |
| F04 | `81972314010b171f8a7eb1657de259e16ebacae37581be8356f9bc9c52286b60` |
| F05 | `1a4682a5fab423c7c4e696ec4ef0c9ed67668d3a936dbae891958d20f60a6285` |
| Directive text (fenced body) | `409ec073edcc6f85d91acf68c84600c24d869f403cdab6d7408d2902a3ba5952` |

### A.3 Founder approval — evidence

| Source | Verbatim evidence |
|---|---|
| Directive `§1` | *"I have reviewed and approved the authority represented by these five files."* |
| Directive `§4` | *"The Founder has approved the V2 authority transition represented by the five files."* |
| Directive signature block (five lines; line breaks shown as ` / ` here and wherever this record quotes it) | *"FOUNDER: Moriarty / DECISION: APPROVED / TARGET: AIOS CO-FOUNDER V2 / REGISTRATION: AUTHORIZED / ACTIVATION: AUTHORIZED"* |
| F02 `§44` | *"Founder: Moriarty Decision: APPROVE Scope: FD-V2-001 through FD-V2-013 Approved Role: AIOS Co-Founder + Delegated CEO"* |
| F03 `§32` | *"Founder: Moriarty … Founder Decision: APPROVE … Approved Role: AIOS Co-Founder + Delegated CEO"* |
| F04 `§41` | *"Founder: Moriarty … Founder Decision: APPROVE … Approved Role: AIOS Co-Founder + Delegated CEO"* |
| F05 `§49` | *"Founder: Moriarty … Founder Decision: APPROVE … Approved CEO: Claude Code"* |

**The F02 `§35` sequence is satisfied.** The sequence runs Founder approval →
decision record → baseline reconciliation → CEO authority freeze → Charter →
Mandate → Authority / Escalation Matrix → *"FOUNDER REVIEW OF FINAL V2 PACKAGE"*
→ registration → activation. The Founder's review of the final package is the
directive `§1` statement quoted above. The authority freeze and the Authority /
Escalation Matrix are Part C of this record.

### A.4 Source precedence — established before any canonical change

The directive `§7`, F03 `§1`, F04 `§3` and F05 `§3` all place the Constitution
first and the V2 instruments below Founder Decisions, the Governance Baseline,
canonical architecture, the Master Program and Platform Organization. The
repository's own precedence is Engineering Constitution `§4` and Delegation
Register `§8`. The two orderings do not contradict each other. Applied together:

```text
ENGINEERING CONSTITUTION v1.0  (+ Canonical Domain Model — the constitutional pair, GDR-0001)
        ↓
FOUNDER AUTHORITY / FOUNDER DECISIONS   (incl. FD-V2-001 … FD-V2-013 and prior standing decisions)
        ↓
GOVERNANCE BASELINE  (as amended by F03)
        ↓
CANONICAL ARCHITECTURE · ADRs · Architecture Freeze
        ↓
MASTER PROGRAM / PHASE AUTHORITY
        ↓
PLATFORM ORGANIZATION / CANONICAL VOLUMES
        ↓
CO-FOUNDER DELEGATION CHARTER V2 (F04) → CEO OPERATING MANDATE (F05)
        ↓
OPERATIONAL ACTS / WORK ORDERS
        ↓
IMPLEMENTATION
```

**What "AIOS Constitution" means here.** The V2 files use the phrase without
naming a document. For repository governance, `GDR-0001` (G1′) makes the
Engineering Constitution, together with the Canonical Domain Model,
authoritative. V2 is therefore read as subordinate to both. This reading adds
constraints and removes none.

### A.5 Where V2 is registered — one system, not two

The existing governance structure already has one place for each kind of
record. V2 goes into those places, and no parallel register was created:

| Kind of record | Existing canonical home | V2 entry |
|---|---|---|
| Founder decisions | Governance Decision Register | `GDR-0038` + `FD-V2-001` … `FD-V2-013` (§14) |
| Delegations and their activation | Delegation Register | `DEL-CFV2-CEO-001` + `ACT-CFV2-CEO-001-A` (§12). `DEL-T4.4-CF-001` is marked **SUPERSEDED** in place |
| Appointments | Appointment Register | Continuity note only (§10). `APT-CD1.1-AA-001` is unchanged |
| Founder instruments | `docs/governance/acts/` | The directive |
| Instrument bodies | new `docs/governance/cofounder-v2/` | F01–F05, byte-exact, with a status README |

| Requirement | Satisfied by |
|---|---|
| F04 `§40`.1 Charter established as Delegation Charter V2.0 | §A.1; `DEL-CFV2-CEO-001` *Instrument* field |
| `§40`.2 Founder approval provenance | §A.3 |
| `§40`.3 Supersession of Charter V1.0 | `RD-06` |
| `§40`.4 Linkage to `FD-V2-001` … `FD-V2-013` | `GDR-0038`; `DEL-CFV2-CEO-001` *Governing Decisions* |
| `§40`.5 Linkage to the Baseline V2 amendment | `RD-05`; `GDR-0038` |
| `§40`.6 Activation status | §D.4 |
| `§40`.7 Effective authority envelope | Part C |
| `§40`.8 Authority matrix | §C.3 |
| `§40`.9 Supporting CEO Operating Mandate | §A.1 F05; `DEL-CFV2-CEO-001` |
| F05 `§48` Document ID · version · approval · basis · parent Charter · Baseline relationship · activation state · supersession of prior protocols | §A.1, §A.3, §D.4, `RD-07` |
| F03 `§25.2` items 1–6 | §A.1, `RD-05`, §A.3, §C.3, §D.4, §A.1 F04 |

### A.6 What registration does not do

It does not amend the Engineering Constitution (`§16`: *"No delegation of
amendment authority is permitted under any circumstance"*). It does not add the
Co-Founder or the CEO to Constitution Appendix A. It does not change the
Canonical Domain Model or any ADR. It does not change the Master Program, and
`docs/program/AIOS_*` is untouched. It certifies no phase, declares no phase
complete and grants no final acceptance. It lifts no pause (see `RD-14`), and
it rewrites no historical record.

---

## Part B — V1 as discovered, classified and reconciled

### B.1 What V1 actually is in this repository

The V2 files describe the prior model as a Governance Baseline in which
*"Claude = AI Engineering Lead"* and *"Architecture Change → Founder"* (F02 `§17`,
`§25`; F03 `§3.1`, `§19.1`). **That baseline is not resident.** `ACT-CC-T4.1:29`
records that *"Engineering Lead"* has *"zero repository occurrences."* `ACT-CC-T4.2`
classifies the description as *"VERIFIED-AS-EXTERNAL, not repository-canonical."*
A fresh search on 2026-09-23 found no occurrence outside those two Acts and the
V2 files.

The V1 that is resident and operative in the repository is the following:

| V1 component | Source | State before V2 |
|---|---|---|
| Constitutional designations: AI Systems Engineer (`§3.3`), Meta-level AI Contributor (`§14.1`) | Engineering Constitution v1.0 | Constitutional; the floor |
| Co-Founder office, Construction Phase — Model D, below the Constitutional Tier | `GDR-0015` | Ratified 2026-08-15 |
| Co-Founder construction delegation, `§3.1` scope A–E, `§3.2` 20 exclusions | `DEL-T4.4-CF-001` | **ACTIVE** — the operative V1 delegation |
| Its activation | `ACT-T4.4-CF-001-A` | **ACTIVE** (STATE 6) |
| Architecture Authority appointment | `APT-CD1.1-AA-001` / `ACT-CD1.1-AA-001-A` | **ACTIVE** |
| P7-I99 execution delegation | `DEL-F03-015-P7I99-001` | **ACTIVE — DORMANT UNTIL INVOKED** |
| Maximum Bounded Autonomous Execution | `FDE-P10-AUTONOMOUS-EXECUTION-01` / `GDR-0037` | **OPERATIVE** |
| AIOS Co-Founder Delegation Charter v1.0 | not resident; `AIOS_P10_AUTONOMOUS_EXECUTION_VERIFICATION_v1.0.md` `§21.2`, `§34.1` | Founder-approved but never registered, so **never effective** under its own header |
| Construction pause | `ACT-CC-GOV-PAUSE-001` | **IN FORCE** |
| Open premise FD-2 (Founder ≡ Architect) | `GDR-0015`; Delegation Register `§10` | **IMPLIED — open** |

### B.2 Classification

| # | V1 component | Class | Result |
|---|---|---|---|
| 1 | Constitution `§3.3` / `§14.1` designations | **RETAIN** | Unchanged. V2 operates above this floor and never replaces it (`RD-15`) |
| 2 | `GDR-0015` — Co-Founder office | **RETAIN + EXPAND** | Stays as the founding record. The office continues, expanded by `FD-V2-001` into Co-Founder + Delegated CEO. Model D is kept (`RD-09`) |
| 3 | `DEL-T4.4-CF-001` | **SUPERSEDE** | Replaced as the operative delegation by `DEL-CFV2-CEO-001`. Its text is unaltered and the mark is appended. Compatible content is carried forward (`RD-07`) |
| 4 | `ACT-T4.4-CF-001-A` | **SUPERSEDE** | Replaced by `ACT-CFV2-CEO-001-A`. This is succession, not revocation (`RD-08`) |
| 5 | `APT-CD1.1-AA-001` | **RETAIN** | ACTIVE and unchanged. Its exclusions are non-conferral clauses and do not conflict with A05 (`RD-10`) |
| 6 | `DEL-F03-015-P7I99-001` | **RETAIN** | ACTIVE and dormant. Its Founder-invocation gate stands (`RD-11`) |
| 7 | `FDE-P10-AUTONOMOUS-EXECUTION-01` | **RETAIN / RECONCILE** | Operative. Its grants are subsumed by V2, and its hard boundaries stand (`RD-12`) |
| 8 | Charter v1.0 (non-resident) | **SUPERSEDE** | Superseded before it ever became effective. It is not reconstructed (`RD-06`) |
| 9 | External "AI Engineering Lead" baseline definition | **SUPERSEDE** (as the Founder directed) · recorded as non-resident | `RD-05` |
| 10 | Constitution `§3.2` non-delegables vs A05 | **RECONCILE** | Made explicit as boundary `C-2`/`C-3` (`RD-02`) |
| 11 | Contributor delegation vs `§3.2` delegating power | **RECONCILE** | A10 assigns work and does not re-delegate approval authority (`RD-03`) |
| 12 | FD-2 delegating-capacity premise | **RECONCILE — carried open** | Same basis as V1. Listed as a Founder review item (`RD-04`) |
| 13 | `ACT-CC-GOV-PAUSE-001` | **RECONCILE** | Its V2 non-activation clauses are superseded by the later directive. The construction pause itself stays (`RD-14`) |
| 14 | "Proposer is not approver" practice | **RECONCILE** | Kept for acceptance. Where the CEO approves its own ADR, it is recorded under Constitution `§14.1` (`RD-15`) |
| 15 | Wording variance between the F03 `§20` and F04 `§33` matrices | **RECONCILE** | F04 governs (`RD-13`) |
| 16 | Stale V1 status lines in live register headers | **UPDATE** by appended mark | `RD-16` |
| — | V2 surfaces absent from V1: CEO role, Goal/Target interface, A01–A23, re-discovery, exhaustion, cross-phase repair | **ADD** | Registered through F02–F05 and Part C |
| — | Nothing in V1 was found to be operative and incompatible without being superseded | **DEPRECATE** — none needed | — |
| — | No component required a Founder decision in order to activate | **ESCALATE** — none blocking | Items for Founder review are in Part E |

### B.3 Reconciliation determinations

**`RD-01` — Precedence.** Established at §A.4. Every V2 file subordinates
itself to the Constitution and to Founder authority, so no V2 clause is read
as overriding either.

**`RD-02` — Constitution `§3.2` non-delegables bound A05.** A05 includes *"create
and approve ADRs within delegated scope"* (F04 `§10`; F02 `FD-V2-005`). F04
`§10.1` lists what architecture authority may not touch. That list does not
name the two exclusions the Constitution itself imposes on every delegation:
*"Domain Model semantic changes"* and *"cross-Department structural changes"*
(`§3.2`). **This is not a conflict,** because F04 `§3`, `§10.1` and `§19.1`
subordinate the Charter to the Constitution. It is, however, an ambiguity that
could later be read as a grant, so Part C states the two exclusions as `C-2`
and `C-3`. `ADR-0010` renamed Department to Platform Division, so `C-3` covers
cross-Platform-Division structural change. This matches A08, *"No ownership
override"*.

**`RD-03` — A10 assigns work and does not re-delegate approval.** Constitution
`§3.2` vests the power to delegate architectural-tier approval authority in *"the
Architect"*. F02 `§19` reserves *"delegation authority"* and *"authority envelope
definition"* to the Founder. F04 `§16` says: *"Delegation is a mechanism for
execution, not a mechanism for multiplying authority."* A10 therefore covers
assigning bounded work to contributors and agents. The CEO stays accountable,
and results are integrated only after verification (F05 `§36`).
Architectural-tier approval authority is not sub-delegated.

**`RD-04` — Delegating capacity and FD-2.** Constitution `§3.2` says *"The
Architect may delegate"* V2 is issued by the Founder. The V2 files never use
the word "Architect", so they neither ratify nor disturb the equivalence. V2
rests on the same basis `DEL-T4.4-CF-001` has rested on since 2026-08-15: the
Founder acting in the Architect capacity, on the `GDR-0001` precedent. That
equivalence is **IMPLIED, not separately ratified** (`GDR-0015`). **V2 creates
no new conflict here, and it resolves nothing.** Deciding FD-2 is Founder-only
(`APT-CD1.1-AA-001 §3.2` exclusion 26). It is carried open and listed in
Part E.

**`RD-05` — The "AI Engineering Lead" baseline, and what is actually
superseded.** The Founder decided (F02 `FD-V2-012`; F03 `§19.1`) that *"Claude =
AI Engineering Lead"* is superseded by *"Claude Code = AIOS Co-Founder + Delegated
CEO"* That definition lives in an external, non-resident corpus (§B.1). **The
supersession is recorded as the Founder's decision about that external
definition, wherever it is held. No body is reconstructed or quoted beyond what
the V2 files themselves say about it.** Inside the repository, the
superseded operative definition is `DEL-T4.4-CF-001` (`RD-07`). *"Architecture
Change → Founder"* corresponds to Constitution `§3.2`: *"Absent an explicit,
scoped delegation, architectural-tier authority remains with the Architect
alone."* That clause is **not** superseded. It is satisfied, because V2 is an
explicit, scoped delegation. F03 is registered as the Governance Baseline
amendment. The base Governance Baseline it amends remains non-resident (Part E,
gap `G-1`).

**`RD-06` — Charter v1.0.** F04's header says *"Supersedes: AIOS Co-Founder
Delegation Charter v1.0 upon canonical registration and activation"* The
repository record of Charter v1.0 is in the P10 verification `§21.2` and `§34.1`.
It was recovered, it was Founder-approved, and it was never registered. Its own
header makes it effective only *"Upon Founder approval and registration"*, so
it never took effect. In `§34.1` Claude declined to register it, because
registering an instrument that expands one's own authority without an
instruction to register would be self-activation (`DEL-T4.4-CF-001 §3.2`
exclusion 19). **This registration differs in the one respect that matters:
the Founder expressly directs it** (*"REGISTRATION: AUTHORIZED / ACTIVATION:
AUTHORIZED"*). Charter v1.0 is recorded as **SUPERSEDED, never effective**. Its
body stays non-resident and is not reconstructed. The historical citations
tracked under `ESC-C5-01` are left unaltered.

**`RD-07` — `DEL-T4.4-CF-001` is superseded, and its compatible content is
carried forward.** `DEL-CFV2-CEO-001` becomes the single operative Co-Founder
delegation from activation onward. The V1 text is unaltered, and a supersession
mark is appended at Delegation Register §12, following Register `§2`. These V1
elements carry forward because each has a V2 counterpart:

| V1 element | V2 counterpart |
|---|---|
| `§3.2` exclusions 1–8 (Constitution, Founder) | F03 R01–R03, R05; F04 `§26` 1–8 |
| `§3.2` exclusions 9–10 (Domain Model, cross-Department) | `C-2`, `C-3` |
| `§3.2` exclusions 11–15, 20 (authority by implication or title, self-superiority, self-expansion) | A22; F02 `§20`; F04 `§18` Rule 4, `§27` |
| `§3.2` exclusions 16–18 (historical evidence) | F04 `§27` *"fabricate historical decisions"*; `§28` |
| `§3.2` exclusion 19 (no activation without a durable record) | this record, §D.4 |
| `§3.3` never infer authority from *"role · capability · urgency · confidence · precedent · silence"* | F03 `§17.6`; F05 `§3`; F04 `§18` Rule 4 |
| `§3.4` legal and ownership boundary | F02 `§21`; F04 `§31`. The legal clauses (equity, personhood, fiduciary status) carry forward unchanged, because no V2 file addresses them |
| `§5` historical integrity, `§6` revocation | §C.8 |

The V1 clause *"commit and push where separately permitted by the applicable
engineering workflow"* (`§3.1 C`) corresponds to F04 `§28` persistence
authority, *"consistent with repository rules"*. Repository and session push
rules still apply.

**`RD-08` — `ACT-T4.4-CF-001-A` is superseded, not revoked.** V1's reversion
target, STATE 0, applied to revocation of V1. The transition is a succession,
and actions taken under V1 remain valid (V1 `§6`).

**`RD-09` — `GDR-0015` is retained and the office continues.** `GDR-0015`
established an office that is *"implementation-independent, vendor-independent,
authority-scoped, revocable, and subordinate to the Constitution"*, with Claude
Code as its occupant and *"not identical to its occupant"*. F04 `§32` keeps the
same principle: *"The organizational capability itself belongs to AIOS."* The
office continues under the V2 title Co-Founder + Delegated CEO. Its
"Construction Phase" qualifier is widened by F04 `§42` to *"autonomous AIOS
construction and operational execution"*. **Model D is retained.** The office
remains below the Constitutional Tier, and Appendix A is unchanged. Naming the
occupant follows `GDR-0015` precedent and is not a technology decision under
`§6.2` invariant 1.

**`RD-10` — `APT-CD1.1-AA-001` is retained.** Its `§3.2` list begins *"The
appointment grants none of the following"*. `ACT-CC-F03-015 §2` determined that
this is a non-conferral clause, not a prohibition. It therefore does not narrow
A05, and A05 does not amend it. The appointment remains the named Architecture
Authority designation used by the Volume 1 tables. A05 is the CEO's operative
architecture envelope.

**`RD-11` — `DEL-F03-015-P7I99-001` is retained, with its gate.** P7-I99 runs for
a Volume *"only when a separate Founder-authorized Act explicitly invokes"* it
(`FD-015-01`), and the delegation cannot be invoked *"on its own initiative"*
(exclusion 8). No V2 file supersedes `FD-015-01`, and F04 `§19.2` forbids
silently overriding a valid Founder decision, so the gate stands. The
delegate named there, "Co-Founder — Construction Phase", is the office that now
continues under V2.

**`RD-12` — `FDE-P10-AUTONOMOUS-EXECUTION-01` is retained and reconciled.** Its
grants (resolve-on-discovery, standing construction, follow-on Act generation,
conformance repair) are covered by A02, A06, A09 and F04 `§17`. Its hard
boundaries, recorded at `GDR-0037 §6`, are not removed by any V2 file: Platform
identity, CPID creation and mutation, ownership assignment and transfer,
authority-role creation and binding, canonicalization, freeze, `DERIVED ≠
ADOPTED ≠ CANONICAL ≠ FROZEN`, and protected lifecycle transitions. They stand
as `SD-2` in Part C. None of them contradicts V2. Each is either Founder-reserved
under V2 already or outside what V2 grants.

**`RD-13` — The two matrices.** F03 `§20` and F04 `§33` agree on all 23 rows
and all 23 statuses. Five Boundary or Authority cells differ in wording only:
A05, A10, A15, A16 and A17. F04 is the delegation instrument, and F05 `§44` says
*"The Charter answers: What authority does the CEO have?"*, so **F04's text is
operative**. The only difference with substance is A10. F03 calls it
"Delegation" and F04 calls it "Contributor Delegation". F04's narrower name
matches `FD-V2-007` (*"Contributor / Agent Delegation"*) and is applied.

**`RD-14` — `ACT-CC-GOV-PAUSE-001`.** The pause Act says *"This Act does NOT
activate Co-Founder V2"* (`§5`) and lists *"V2 activation authority"* as not
delegated (`§22`). The later Founder directive supersedes both clauses **as to
V2 registration and activation**, because the Founder authorizes both
expressly. The directive does **not** release the construction pause. `§21`
requires an explicit release that states *"Whether the pause is lifted"*, among
seven elements, and `§12` forbids reading *"completion of V2 analysis"* as a
release. The directive states none of the seven elements. **Result:** V2 is
ACTIVE, and the construction pause stays in force for all construction outside
the V2 transition. The pause anticipated this order of events: *"If V2 is
activated before the release, the release must identify the canonical V2
authority instrument."* That instrument is now `DEL-CFV2-CEO-001`. The release
is Founder review item `FR-1`.

**`RD-15` — Constitution `§14.1` and "proposer is not approver".** `§14.1`
requires Meta-level AI Contributors to *"Proceed only upon explicit approval
from the authority defined for that tier under Section 3."* Within the delegated architectural
scope, `§3.4` makes the delegate that authority: *"Approval rests with the
Architect, or with a delegate acting within an explicitly scoped delegation
under Section 3.2."*
`AIOS_BASELINE_LIFECYCLE_v1.0.md §5` (*"Proposer is not approver. The party that
implements a baseline does not accept it"*) governs **acceptance**. V2 keeps
acceptance with the Founder (A15, A19). **So when the CEO approves an ADR it
proposed under A05, `§14.1`'s durable-evidence duty applies:** the ADR records
that proposer and approver are the same delegate acting under
`DEL-CFV2-CEO-001`, and it remains subject to Founder Revise / Redirect
(`FD-V2-011`). This applies an existing obligation and creates no new
restriction.

**`RD-16` — Stale "current state" lines in live registers.** The Delegation
Register header and `§11` state that it records `DEL-T4.4-CF-001` *"and nothing
else"*. `§4` and `§9` show V1 as ACTIVE. The Appointment Register shows
`DEL-T4.4-CF-001` as ACTIVE in `APT §3.4`. All of these lines are historical
text and are **not rewritten**. The appended V2 sections mark them as
superseded, following the `DEL-F03-015-P7I99-001` precedent for `§11`.

---

## Part C — Effective Authority Envelope (CEO Authority Freeze)

This is the F02 `§35` *"CEO AUTHORITY FREEZE"* and *"CEO AUTHORITY /
ESCALATION MATRIX"*. It is frozen as of activation and can be changed only by
the Founder (F03 R05, F04 `§26`.7). **It restates and assembles. It adds no
authority.** Where this summary and F04 differ, F04 governs, subject to the
Constitution.

### C.1 Role

**AIOS Co-Founder + Delegated CEO.** Current occupant: Claude Code. The office
belongs to AIOS, and the occupant is its current implementation (F04 `§32`,
`§42`). **Authority = Founder Decision + Canonical Delegation + Defined Authority
Envelope, not title** (F03 `§5`).

### C.2 Operating model

```text
FOUNDER — Goal · Target · optional Strategic Constraint
   ↓
CO-FOUNDER + DELEGATED CEO — Discover → Understand → Classify → Authority Sufficiency
   → Decide / Escalate → Build / Repair / Coordinate → Verify → Evidence → Re-discover
   → Continue / Block / Escalate / Exhaust
   ↓
RESULT + EVIDENCE + CURRENT STATE
   ↓
FOUNDER REVIEW — APPROVE  |  REVISE / REDIRECT
```

(F03 `§6`, `§27`; F04 `§6`; F05 `§7`)

### C.3 Authority matrix — operative text F04 `§33`

| ID | Authority | Status | Boundary |
|---|---|---|---|
| A01 | Executive Command | AUTHORIZED | Within Founder Goal / Target |
| A02 | Autonomous Construction | AUTHORIZED | Within delegated envelope |
| A03 | System Discovery | AUTHORIZED | Evidence-based |
| A04 | Work Classification | AUTHORIZED | Preserve authority distinctions |
| A05 | Architecture | AUTHORIZED WITH BOUNDARY | Bounded Architecture Authority — **and `C-1`…`C-4`** |
| A06 | Engineering | AUTHORIZED | Within system scope |
| A07 | Cross-Phase Coordination | AUTHORIZED | No roadmap redefinition |
| A08 | Cross-Platform Coordination | AUTHORIZED | No ownership override |
| A09 | Operational Decisions | AUTHORIZED | Ordinary operational decisions |
| A10 | Contributor Delegation | AUTHORIZED WITH BOUNDARY | Delegate cannot exceed delegator — **work, not approval authority (`RD-03`)** |
| A11 | Verification | AUTHORIZED | Evidence required |
| A12 | Evidence | AUTHORIZED | Traceable |
| A13 | Re-Discovery | AUTHORIZED | Required after material construction |
| A14 | Dependency Closure | AUTHORIZED | Within target scope |
| A15 | Integration Closure | AUTHORIZED | Not final acceptance |
| A16 | Escalation Determination | AUTHORIZED | Reserved matters escalate |
| A17 | Authorized Construction Exhaustion | AUTHORIZED | Narrow semantics |
| A18 | Founder Review Interface | AUTHORIZED | Founder decides |
| A19 | Final System Acceptance | RESERVED | Founder |
| A20 | Mission / Identity | RESERVED | Founder |
| A21 | Governance Model | RESERVED | Founder |
| A22 | Authority Self-Expansion | PROHIBITED | Founder approval required |
| A23 | Canonical Override | PROHIBITED | Authorized correction only |

The bold text in A05 and A10 marks where the Constitution already bounds these
rows (`RD-02`, `RD-03`). It narrows nothing the Founder granted. The authority
states are those of F04 `§34`. **UNKNOWN AUTHORITY is not AUTHORIZED.**

### C.4 Constitutional boundary — binding on every row

| # | Boundary | Source |
|---|---|---|
| `C-1` | No Constitution amendment. Amendment authority is non-delegable | `§3.1`, `§16` |
| `C-2` | No Domain Model semantic change. No other document may introduce or redefine a Domain Model entity, relationship or invariant | `§3.2`, `§6.2` inv. 3 |
| `C-3` | No cross-Department (Platform Division) structural change | `§3.2`; `ADR-0010` |
| `C-4` | An ADR may not amend the Constitution, introduce a technology, language, framework or infrastructure decision, or grant authority beyond what is delegable. No governance document embeds a technology decision | `§3.4`; `§6.2` inv. 1 |
| `C-5` | No governance action proceeds *"solely because of urgency, automation, tooling signals, inferred permission, or external pressure"* | `§6.2` inv. 2 |
| `C-6` | Authority granted at one tier is not exercised as though granted at a higher tier | `§6.2` inv. 4 |
| `C-7` | Durable review evidence: approval required and sought is recorded in the artifact | `§14.1` |

### C.5 Founder-reserved

F03 `§4.1` R01–R09. F04 `§26` items 1–10. F02 `§19` items 1–10. The union
covers: Constitution · Mission / identity · Founder authority · Founder Reserved
Authority · Governance model · Delegation authority and the authority envelope ·
Authority expansion · Higher-order canonical override · Final system and human
acceptance · Fundamental strategic direction · Founder-only decisions. Founder
succession and AIOS termination authority remain **UNKNOWN** and are not decided
here (Delegation Register `§7`).

### C.6 Standing Founder decisions that V2 does not supersede

Each of these stands under F04 `§19.2` because no V2 file supersedes it:

| # | Standing decision | Source |
|---|---|---|
| `SD-1` | P7-I99 runs only when a Founder Act invokes it for a named Volume | `DEL-F03-015-P7I99-001`; `FD-015-01` |
| `SD-2` | Hard boundaries of the P10 autonomous-execution event | `GDR-0037 §6` |
| `SD-3` | Construction pause, until the Founder releases it | `ACT-CC-GOV-PAUSE-001 §21` |
| `SD-4` | The 13 Founder-protected `docs/program/AIOS_*` packages | `FD-P11-002 §6` |
| `SD-5` | Certified phase evidence is not overwritten | `FD-P10-005`; `FD-P11-002`; `tools/p12_certified_evidence_guard.py` |
| `SD-6` | The Native Core stays at eleven frozen subsystem boundaries | `FD-P11-002 §10` |
| `SD-7` | Spent Acts stay spent and are never reused as authority | `ACT-CC-GOV-PAUSE-001 §10` |
| `SD-8` | The P13 Blueprint v0.1–v0.4 hashes recorded by the Founder are unaltered | `FD-P13-003` … `FD-P13-005`; `ACT-CC-P13-005` … `-008` |

### C.7 Escalation matrix

The CEO **must** stop the affected action, record it and escalate when any of
the following holds (F04 `§24`):

| Trigger | Route |
|---|---|
| 1 Constitution must change · 3 Mission or identity must change · Founder Reserved Authority must be exercised (2) | Founder decision |
| 4 Delegation boundary must change · the action needs authority beyond A01–A18 | Founder decision (R05, A22) |
| 5 A protected architectural invariant cannot be kept within A05 · the action crosses `C-1`…`C-7` | Founder decision |
| 6 Two higher-order sources conflict and precedence cannot resolve it | Founder decision |
| 7 An irreversible strategic decision is not delegated · 8 An Act marks a matter Founder-only | Founder decision |
| 9 Authority is still UNKNOWN after sufficient discovery | Obtain evidence, or escalate |
| A standing decision `SD-1`…`SD-8` would be crossed | Founder decision |

**Form:** the F05 `§24` escalation package, with its 10 fields. **Independent
work that does not conflict may continue** (F04 `§24`, `§19.1`). A trade-off on
its own does not require escalation (F04 `§18` Rule 6).

### C.8 Amendment, suspension, revocation

Amendment, suspension and termination are Founder-reserved (F04 `§4`, `§26`).
**No V2 file states a reversion state on revocation.** V1's STATE 0 applied to
V1. This record does not infer one, so the revoking instrument determines it.
Actions taken validly before any revocation remain valid, and the historical
records stay immutable (V1 `§6`, retained). No emergency authority is created,
and urgency does not expand authority (`C-5`).

---

## Part D — Verification, Re-Discovery, Activation

### D.1 Verification evidence

| # | Check | Method | Result |
|---|---|---|---|
| V-01 | Byte-exact persistence | sha256 of the upload vs the repository copy | **5/5 identical**. The directive's fenced body hash matches §A.2 |
| V-02 | Quotation fidelity | Every `*"…"*` quotation in this record, Delegation Register §12, Appointment Register §10, Decision Register §14, the `cofounder-v2` README and the directive header, checked by script against F01–F05, the directive, the Constitution, the Baseline Lifecycle, the P10 verification, the Volume Activation Model and the resident registers and Acts (registers read at `HEAD`) | **98/98 verified.** Earlier runs flagged 15 genuine defects in my drafts (Part F `F-1`, `F-2`). They also flagged 3 non-defects: two sources missing from the checker's corpus, and one tool-output fragment wrongly formatted as a quote, now a code span |
| V-03 | Append-only registers | The first *n* bytes of each edited register, compared with the `HEAD` file of length *n* | **3/3 prefix-identical.** Appointment `4cfd544f…`, Delegation `cb72dc19…`, Decision `22843233…`. Earlier text unaltered |
| V-04 | Protected surfaces | `git status` on `docs/program/`, `docs/architecture/`, `tools/`, `native_core/`, `consumers/` | **0 changes.** P13 v0.1–v0.4, `ACT-CC-GOV-PAUSE-001` and certified evidence untouched |
| V-05 | Role consistency | Occurrences of *"Co-Founder + Delegated CEO"* | F01 4 · F02 8 · F03 7 · F04 5 · F05 3 · directive 3. **No variant role name** |
| V-06 | Authority-matrix consistency | Parse F03 `§20` and F04 `§33` row by row | **23/23 IDs and statuses identical.** 5 wording variances, resolved at `RD-13` |
| V-07 | Founder-boundary consistency | Compare F02 `§19`, F03 `§4.1`, F04 `§26`, F05 `§49` | No reserved item in one file is delegated in another. Union at §C.5 |
| V-08 | Precedence consistency | Directive `§7`, F03 `§1`, F04 `§3`, F05 `§3` vs Constitution `§4` and Delegation Register `§8` | Compatible (§A.4) |
| V-09 | Citation integrity | `tools/corpus_citation_audit.py` | **0 errors · 89 warnings** — identical to the pre-change baseline (0 · 89). Scanned 329 → 335 documents |
| V-10 | Stale-state audit | `python -m tools.stale_state_audit` | **0 stale assertions** · 55 historical uses |
| V-11 | Self-knowledge and discoverability | `tools.governance_index`, `tools.derived_views` | `GDR-0038` reads ACTIVE; `FD-V2-001`…`013` read OPERATIVE; `ACT-T4.4-CF-001-A` is superseded by `GDR-0038`; 13 FD-V2 in `self_knowledge()`; **0 unbridged FD-V2 gates** |
| V-12 | Certification-guard safety | Guard regex (`tools/p12_certified_evidence_guard.py`) over all new text | **0 hits.** No text can be read as a certification claim |
| V-13 | Test suite | `python -m unittest discover -s tools/tests -t .` | **1367 run · OK · 1 skipped** — identical to the pre-change baseline (1367 · OK · 1 skipped). Run on the final tree. The only later edits were this cell, the V-02 count, and one Part F wording change turning a quote into a code span. None of these is read by any test |

### D.2 Re-discovery

Searched after construction for each item in directive `§16`:

| Search | Finding | Action |
|---|---|---|
| Stale V1 role definitions | `DEL-T4.4-CF-001` and *"Co-Founder (Construction Phase)"* appear in 20 Acts and 39 other tracked documents, the three registers among them. **Each one is a dated record naming the authority it was produced under.** V1 actions remain valid and authority is not retroactive (V1 `§5`, `§6`) | **None — correct history.** Rewriting them would violate `DEL-T4.4-CF-001 §3.2` exclusions 16–18 |
| Live "current state" lines stating V1 is operative | Delegation Register `§3`, `§4`, `§9`, `§11`; Appointment Register `§3.4` | Marked superseded by appended sections (`RD-16`), not rewritten |
| V1 exclusions cited as live constraints | `DIVISION-LIFECYCLE-AND-AUTHORITY-MODEL.md:47` and `DIVISION-OPERATION-AND-PERFORMANCE-MODEL.md:197` cite `DEL-T4.4-CF-001 §3.2` exclusion 9 | **Substance still true.** The rule is Constitution `§3.2` and continues as `C-2`. No change |
| `AIOS_VOLUME_ACTIVATION_MODEL_v1.0.md` AG-05 cites `DEL-T4.4-CF-001` | The AG set was relabelled *"non-canonical implementation scaffolding"* at v1.3, and the table is *"preserved unaltered as the historical scaffold."* The model has unrelated older staleness too, e.g. *"P10 … NOT STARTED"* | Not modified. Gap `G-6` |
| *"Engineering Lead"* | 7 tracked files: `ACT-CC-T4.1`, `ACT-CC-T4.2` (history), F01–F03 (verbatim V2), this record and Decision Register §14, which quote it as superseded | **0 live claims** |
| Duplicate authority definitions | The matrix appears in F03, F04 and §C.3 | §C.3 is declared a restatement, and F04 governs (`RD-13`) |
| Authority leakage | New text reviewed for grants beyond F04 | None. Constitutional, amendment and Founder-override authority are recorded as NONE in §D.4 and in `DEL-CFV2-CEO-001` |
| Broken references | Citation audit | 0 errors (V-09) |
| Discoverability | The first draft of the FD-V2 entries did not parse (status ABSENT or garbled) | **Repaired** before commit (Part F `F-3`) |
| Index class coverage | `tools/governance_index.py` does not index `DEL-` or `APT-` identifiers, so `DEL-T4.4-CF-001` was never discoverable either | Predates V2. Gap `G-7`. The V2 decisions are discoverable through `GDR-0038` and `FD-V2-*` |
| Missing V2 dependencies | F03 `§26` items 1–5 present. Items 6–12 are covered by F05 | Gap `G-2`, non-blocking |
| Inconsistent Founder boundaries | None (V-07) | — |
| Unregistered Founder instruments | P12 and P13 instruments are resident but not in the Decision Register | Predates V2, outside this target. Gap `G-4` |

**No actionable V2-transition finding remains open.**

### D.3 Activation safety checklist — directive `§19`

| # | Directive `§19` check | Evidence | Result |
|---|---|---|---|
| 1 | Founder approval is evidenced | §A.3: directive `§1`, `§4` and signature; F02 `§44`; F03 `§32`; F04 `§41`; F05 `§49` | **PASS** |
| 2 | V2 authority is traceable | F01–F05 byte-exact with hashes (§A.2); `FD-V2-001`…`013` → `GDR-0038` → `DEL-CFV2-CEO-001` | **PASS** |
| 3 | Existing V1 has been reconciled | Part B: 16 components classified; `RD-01`…`RD-16` | **PASS** |
| 4 | Valid V1 foundation is preserved | Constitution designations, `GDR-0015` Model D, `APT-CD1.1-AA-001`, `DEL-F03-015-P7I99-001` and `FDE-P10` boundaries retained; V1 exclusions carried forward (`RD-07`) | **PASS** |
| 5 | Superseded V1 authority is no longer operative | `DEL-T4.4-CF-001` and `ACT-T4.4-CF-001-A` marked SUPERSEDED; Charter v1.0 superseded (never effective); the index confirms supersession (V-11) | **PASS** |
| 6 | Founder Reserved Authority remains intact | §C.5; A19–A21 RESERVED; V-07 | **PASS** |
| 7 | Authority self-expansion remains prohibited | A22 PROHIBITED; F02 `§20`; activation was directed by the Founder, not self-initiated (`RD-06`) | **PASS** |
| 8 | Higher-order canonical authority remains controlling | §A.4; `C-1`…`C-7`; Constitution unchanged; standing decisions `SD-1`…`SD-8` preserved | **PASS**. FD-2 is disclosed as an open premise, the same basis V1 has operated on (`RD-04`) |
| 9 | Governance documents are mutually consistent | V-05 … V-08; `RD-13` | **PASS** |
| 10 | Canonical registration is complete | §A.5: F04 `§40` 1–9, F05 `§48`, F03 `§25.2` 1–6 and `§26` 1–5 all mapped | **PASS** |
| 11 | Verification is complete | §D.1 V-01…V-13 | **PASS** |
| 12 | Re-discovery is complete | §D.2 | **PASS** |
| 13 | Activation evidence is recorded | §D.4; Delegation Register §12 | **PASS** |

**Gate result: 13/13 PASS. Activation is authorized by the Founder and executed.**

### D.4 Activation Record — `ACT-CFV2-CEO-001-A`

| Field | Value |
|---|---|
| **Activation ID** | `ACT-CFV2-CEO-001-A` |
| **Delegation** | `DEL-CFV2-CEO-001` |
| **Office** | AIOS Co-Founder + Delegated CEO |
| **Occupant** | Claude Code |
| **Activated by** | Founder — Moriarty (directive: *"ACTIVATION: AUTHORIZED"*; `§18`) |
| **Recorded by** | Claude Code, under explicit Founder direction. The recording is not an approval act |
| **Activation date** | 2026-09-23 |
| **Gate** | Directive `§19` — all 13 checks pass (§D.3) |
| **Prior state** | V1: `DEL-T4.4-CF-001` / `ACT-T4.4-CF-001-A` ACTIVE (STATE 6) |
| **Activated state** | **AIOS CO-FOUNDER V2 — ACTIVE**, within Part C |
| **Superseded** | `DEL-T4.4-CF-001`, `ACT-T4.4-CF-001-A` (succession); Charter v1.0 (never effective); the external "AI Engineering Lead" definition |
| **Constitutional authority conferred** | **NONE** |
| **Amendment authority conferred** | **NONE** |
| **Founder-override authority conferred** | **NONE** |
| **Self-authorization** | **PROHIBITED** (A22) |
| **Construction pause** | **Still in force** (`RD-14`, `SD-3`) |
| **Status** | **ACTIVE** |

**Approval separation.** The Founder approved and authorized activation. Claude
Code recorded it. The occupant did not approve, expand or activate its own
authority. It carried out a registration the Founder expressly directed, which
is the pattern `ACT-T4.4-CF-001-A` and `GDR-0037` already follow.

### D.5 Operative state

```text
AIOS CO-FOUNDER V2 — ACTIVE
Claude Code = AIOS Co-Founder + Delegated CEO
Operating model: Founder Goal / Target → Autonomous CEO Execution → Result + Evidence → Founder Approve / Revise
Construction pause (ACT-CC-GOV-PAUSE-001): IN FORCE — awaits Founder release (FR-1)
Active Founder Goal / Target beyond this transition: NONE
AIOS PROJECT COMPLETE: NO
```

**ACTIVE means the governance model is operative.** It does not mean AIOS is
complete, a phase is complete, the system has been verified, or the Founder
has accepted anything (directive `§23`; F03 `§21`).

---

## Part E — Founder review items and remaining gaps

### E.1 Founder review items — only what genuinely requires the Founder

| # | Item | Why it is the Founder's | Minimum decision |
|---|---|---|---|
| `FR-1` | **Release, or keep, the construction pause** | `ACT-CC-GOV-PAUSE-001 §21`: *"Construction may resume only after an explicit Founder release."* `§12` forbids inferring one | A release naming the seven `§21` elements. The canonical V2 instrument it must identify is `DEL-CFV2-CEO-001`. The first Goal / Target can be issued together with it |
| `FR-2` | **FD-2 — ratify Founder ≡ Architect** | Constitution `§3.2` names the Architect as delegator. The premise is load-bearing for V1 and V2 alike. `APT-CD1.1-AA-001 §3.2` exclusion 26 bars Claude from deciding it | Ratify, or state another basis |
| `FR-3` | **Review of this transition** | Directive: *"Founder Review After Execution: REQUIRED"*; A18/A19 | APPROVE, or REVISE / REDIRECT |

### E.2 Remaining gaps — recorded, not blocking, and not Founder decisions

| # | Gap | Disposition |
|---|---|---|
| `G-1` | The base Governance Baseline, Charter v1.0 and the "AIOS Claude Engineering Charter" (`EVIDENCE-LEDGER.md` `E-55`) are not resident | Supersession is recorded without the bodies. They become resident only if the Founder supplies them |
| `G-2` | F03 `§26` recommended artifacts 6–12 | Covered by F05: intake `§5` · report `§6`, `§25` · escalation `§24` · exhaustion `§29` · evidence `§19` · re-discovery `§20`. The ADR convention is the resident ADR framework. No separate artifact is required for activation |
| `G-3` | `GOVERNANCE_INDEX.md` lists the Decision Register as holding only `GDR-0001`–`0002` and does not list the Delegation Register | Carried from the V1 deferral (Delegation Register `§10`). The Index carries no authority, and its `§8` bars naming a model or vendor |
| `G-4` | The P12 and P13 Founder instruments are resident in `acts/` but not entered in the Decision Register | This recording gap predates V2 and is outside this target. It is identified work for the first authorized Goal / Target |
| `G-5` | The reversion state on V2 revocation is unspecified | §C.8 — determined by the revoking instrument |
| `G-6` | `AIOS_VOLUME_ACTIVATION_MODEL_v1.0.md` still shows `DEL-T4.4-CF-001` in its AG-05 scaffold, and its §10 status predates P10 | The AG set is non-canonical scaffolding preserved as history. A synchronization of the model is identified work for an authorized Goal / Target |
| `G-7` | `tools/governance_index.py` does not index `DEL-` or `APT-` identifier classes | Predates V2. The V2 decisions are discoverable through `GDR-0038` and `FD-V2-*`. Adding the classes is identified engineering work |

---

## Part F — Self-disclosed defects during this execution

Each defect below was introduced by me during this execution. Each was found by
my own mechanical checks **before commit**, and each is corrected in the
committed text. None of them reached the remote.

| # | Defect | How it was found | Correction |
|---|---|---|---|
| `F-1` | In Decision Register §14, `FD-V2-003` and `FD-V2-010` quoted F02 with an ASCII apostrophe (`CEO's`) where F02 has `CEO’s`. My append-integrity note then claimed the typographic form had been kept, so the note was false | Quotation script (V-02) | Apostrophes restored. The note was rewritten to describe the check that was actually run |
| `F-2` | Thirteen more flags across this record and the registers. **Seven** quoted the directive's five-line signature block joined with ` / ` without disclosing that rendering. **Six** were fidelity slips: a period added inside three quotes, two quotes truncated without an ellipsis (one of which also lower-cased *"Proceed"*), and one quote whose inner quotation marks I changed | Quotation script (V-02) | Each quote was corrected to its source. The signature rendering is now disclosed wherever it is quoted |
| `F-3` | The first draft of the thirteen FD-V2 entries used prose metadata that `tools/governance_index.py` could not parse. Status read ABSENT, or as the fragment `OPERATIVE** from` | Re-discovery (V-11) | Converted to the register's `§13` metadata-table form |
| `F-4` | The standing-decision labels `S-1`…`S-8` reused the prefix of the Register's `S-` rows, which `tools/stale_state_audit.py` reads as its superseded-claims ledger | Re-discovery. There was no functional impact, because the labels sat outside the Register | Renamed to `SD-1`…`SD-8` |
| `F-5` | §C.5 attributed the UNKNOWN status of Founder succession and termination to the Engineering Constitution | Self-review | Re-attributed to Delegation Register `§7` |
| `F-6` | One rewrite script failed partway through | Exception raised | It raised before writing, so no file changed. The replacement was then done from explicit data |

The test suite rewrites two P12 runtime-observation files as a known recurring
side effect. After the baseline run they were restored with `git checkout`, and
they are not part of this change.
