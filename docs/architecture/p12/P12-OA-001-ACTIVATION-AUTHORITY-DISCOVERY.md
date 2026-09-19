# P12-OA-001 — Operational Activation Authority Discovery & Decision Gate

**Act:** `ACT-CC-P12-OA-001`.
**Mode:** Discovery → Classification → Authority Reconciliation. **No autonomous
runtime, scheduler, daemon, listener, or activation mechanism was built here.**
**Status:** `W4-GAP-007` reclassified. **`OA-1 — NOT-A-GAP`**, with the
authority question it raised answered and preserved for any future proposal.
**Instruments:** none written — this Act is discovery and reconciliation only.
**Predecessor:** `docs/architecture/p12/P12-W4-EXECUTION-INTEGRATION.md §7`,
which raised `W4-GAP-007` and stopped at `STOP-D`.

---

## 1. What this Act found, in one line

**Nothing in the corpus — not the Founder's P12 authorization, not the
Blueprint, not the Canonical Domain Model, not the Runtime Framework — requires
AIOS to be reachable by anything other than a person.** `W4-GAP-007`'s premise
("resident entry, reachability" is a canonical requirement) does not trace to
any Founder- or Architect-authorized text. It traces to an interpretive
extension this programme introduced during its own construction and disclosed
as an extension at the time. That disclosure was correct; the gap-register entry
built on top of it went further than the disclosure supports.

This is not a finding that self-activation is forbidden forever. It is a
finding that **it is not required now**, that **no authority for it exists**,
and that **the corpus already contains explicit language a future proposal
would have to clear** — recorded below so the next person who raises this
question does not have to re-derive it.

---

## 2. Hard Question 01 — What is `W4-GAP-007`, actually?

[E] Full text, `P12-W4-EXECUTION-INTEGRATION.md §7`:

> **W4-GAP-007 — runtime reachability**
> Canonical requirement: `§17`, `§29` of the Act — resident entry,
> reachability, execution, observation, evidence.
> Actual state: unchanged. Eight root entry points, `HAND-INVOKED ONLY`.
> Classification: BLOCKED — DEPENDENCY... `STOP-D`.

**"The Act" cited is `ACT-CC-P12-W4-001`.** It is cited by ID throughout that
document and its ledger summary (`AIOS_P10_AUTONOMOUS_EXECUTION_VERIFICATION_v1.0.md
§131`), but **no standalone persisted copy of `ACT-CC-P12-W4-001` exists in this
repository.** It is not at `docs/governance/acts/`, not under
`docs/architecture/p12/`, and no grep for its identifier turns up a body with a
§17 or a §29 of its own. Unlike the Founder Decision instruments in this corpus
— which are persisted verbatim, with a `sha256` and a provenance block, precisely
so a citation to them can be checked — this constructing Act exists only as a
citation to itself.

[D] Under this Act's own §7 rule (*"Claude dilarang menerima definisi
W4-GAP-007 hanya karena terdapat pada... previous Claude report... commit
message"*): an identifier that cites a body the repository does not hold is not
a canonical requirement. **`§17, §29 of the Act` is a citation without a
verifiable decision body — `IDENTIFIER ≠ DECISION BODY`.**

[E] More importantly, the two documents that **are** resident and **are**
authoritative do not support the requirement either:

- The Founder's own `§17` (`P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §17`,
  quoted in full below) states the canonical execution chain and says P12-W4
  must prove relationships between surfaces — nothing about who or what may
  invoke them.
- `P12-W6-RUNTIME-AND-WORKFLOW-VERIFICATION.md §A.1` says, of the canonical
  scope item RUNTIME (`§30`): *"Reachability asks what `§30` implies **without
  spelling out**: whether the runtime is entered by the system or only by
  hand."* **This programme's own prior record already discloses that
  reachability is an inference, not literal canonical text**, at the exact
  point the requirement was first measured.

[D] **`W4-GAP-007`'s canonical-requirement citation does not survive
falsification.** It is not that the requirement is false — it is that no
resident authoritative source asserts it. That is a `CANONICAL DEFINITION GAP`
in the gap register entry itself, not evidence that AIOS lacks something it is
required to have.

---

## 3. Hard Question 02 — Why was resident non-manual entry treated as an authority question?

[A] `P12-W4-EXECUTION-INTEGRATION.md §7`, verbatim reasoning: *"A resident
non-manual entry means a scheduler, service or dispatcher deciding **when**
AIOS acts. That is an operational-authority question, not an
execution-integration one."*

[D] **That reasoning is sound and this Act confirms it independently, even
though the premise that triggered it (§2 above) was not canonical.** A
mechanism that decides *when* AIOS acts is not merely a technical component:

```
WHO/WHAT INITIATES?   → the mechanism (clock, event, queue), not a person
WHO/WHAT PERMITS?     → nobody, unless the mechanism itself checks permission
WHO/WHAT DECIDES?     → whatever authored the mechanism's trigger conditions
WHO/WHAT EXECUTES?    → AIOS, under whatever grant the mechanism supplies
WHO/WHAT REMAINS
  ACCOUNTABLE?         → unresolved unless a durable, checkable record ties
                          the execution back to a human decision
```

[E] Constitution §6.2 invariant 2 (`docs/constitution/engineering-constitution-v1.md:116`,
Category B, Constitutional Tier, amendable only by Constitutional Amendment):

> *"No governance action proceeds solely because of urgency, automation,
> tooling signals, inferred permission, or external pressure. Required
> approval must exist before execution. Automation may request. Automation may
> recommend. Automation may not override governance authority."*

[E] `AIOS_DELEGATION_REGISTER_v1.0.md §3.2`, exclusion 19, binding on the
executing delegate: *"Activate itself without a durable activation record."*
`AIOS_APPOINTMENT_REGISTER_v1.0.md §3.2`, exclusion 19: *"Authority to
authorize itself."*

[D] These three sources, read together, settle Hard Question 02 without
needing `W4-GAP-007` at all: **technical reachability is never, by itself,
authority.** A resident entry point is a mechanism; the authority question —
who decided this mechanism may run, under what scope, revocable by whom — is
separate and Constitutional-Tier-adjacent. This Act treats that as confirmed
governing principle, independent of whether `W4-GAP-007` itself was well
founded.

---

## 4. Hard Question 03/04 — Does canonical architecture or P12 exit require self-activation?

[A] P12 exit, canonical (`P12-FRONTIER-AND-AUTHORITY.md §5`, reading
`AIOS_PHASE_10_13_PLATFORM_ORGANIZATION_BLUEPRINT_v1.0.md §9` directly):
*"P12 complete jika AIOS terbukti sebagai coherent operating system, bukan
kumpulan subsystem independen."*

[A] The Founder's own P12-W4 authority text, `P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §17`,
in full:

> *"Canonical execution chain: INTENT → DECISION → WORK → EXECUTION →
> OBSERVATION → VERIFICATION → EVIDENCE. WORK adalah bagian canonical dan
> tidak boleh dihilangkan. P12 execution integration harus membuktikan
> hubungan antar-surface, bukan hanya keberadaan masing-masing subsystem."*

[D] "Harus membuktikan hubungan antar-surface" (must prove the relationship
between surfaces) is a claim about **provenance and joinability** — that an
EXECUTION record can be traced to the DECISION and WORK that authorized it, and
forward to the OBSERVATION, VERIFICATION and EVIDENCE it produced. It says
nothing about the invocation mechanism. `P12-W4-EXECUTION-INTEGRATION.md §4–§6`
already proved exactly this chain, twice (one success, one failure), **entirely
through hand-invoked execution** — `7 of 7 edges JOINED`, independently
verified by a reader that imports nothing from the writer. The canonical
requirement `§17` states is met by evidence that has nothing to do with who
started the process.

[A] `AIOS_DOMAIN_MODEL` / Runtime Framework (`docs/architecture/organization/runtime-framework.md §1, §3`):
Runtime is defined exclusively by the Canonical Domain Model, and this
framework's own scope is *"how Runtime instances are documented"* — structure,
fields, versioning. **No canonical source anywhere in the Domain Model tier,
the Constitution tier, or the P12 authorization instrument defines "Runtime" as
requiring continuous or self-triggered operation.** "Operating system" is a
Blueprint phase name, not a canonical operational specification, and this Act's
own §10 warns explicitly against the leap `COHERENT OPERATING SYSTEM =
AUTONOMOUSLY SELF-STARTING SYSTEM` — a leap this corpus, read directly, does
not make either.

[D] **SELF-ACTIVATION: NOT REQUIRED.** Not `UNKNOWN` — the canonical sources
that define P12 exit and P12-W4's authority are resident, were read directly,
and state a requirement that is satisfiable (and was satisfied) without it.
`OPERATIONAL REACHABILITY` as `§19`/`§30` literally ask for it — evidence that
runtime behavior occurred — is likewise `NOT REQUIRED` to mean non-manual; it
is already `DISCOVERED`/`CONSTRUCTED` per `P12-W6-RUNTIME-AND-WORKFLOW-VERIFICATION.md`
and `P12-W4-EXECUTION-INTEGRATION.md`.

---

## 5. Hard Question 05 — Invocation model taxonomy

Recorded for future use, since the corpus had not previously distinguished
these explicitly:

| Model | What decides *when* | Authority carried by the mechanism itself |
|---|---|---|
| **Human invocation** | a person, at the moment of invocation | none needed beyond the person's own — this is what every resident entry point in AIOS does today |
| **Scheduler** | a clock | none — a scheduler is an invocation mechanism; whatever it invokes still needs its own grant, checked at invocation, not assumed from the schedule existing |
| **Event listener** | an external occurrence | none — same principle; the event is provenance for *when*, not authority for *what* |
| **Queue consumer** | order of arrival in a queue | none, and additionally needs a boundary on accepted work, provenance of the item, and failure/retry/escalation handling before it can be trusted with arbitrary work |
| **Trigger** | a condition becoming true | a trigger is a candidate for invocation, not a decision; `CONDITION → TRIGGER → AUTHORIZATION CHECK → EXECUTION` |
| **Orchestrator** | dependency/sequencing logic among already-authorized steps | none new — it may only exercise authority already granted to what it orchestrates |
| **Autonomous loop** (`OBSERVE → DECIDE → ACT → OBSERVE → ADAPT → CONTINUE`) | the system's own prior observation | this is qualitatively different from the other six: it removes the checkpoint between one action and the next, so a single authorization would have to cover an open-ended sequence of future decisions rather than one bounded execution |

[D] **AIOS today has none of these.** Independently re-confirmed in this Act
(import-graph search, not filename inference, matching `P12-W6-RUNTIME-AND-WORKFLOW-VERIFICATION.md`'s
method): `native_core/core/runtime/bootstrap.py` and `runtime.py` carry
docstrings that **name and exclude** exactly this list — *"Prohibited here and
absent: singleton, registry, service locator, reflection, dynamic import, lazy
wiring, module state, cache, timestamp, UUID, randomness, thread, async,
scheduler, executor, Agent, Workflow, planner, Skill, model adapter,
automation"* (`bootstrap.py:22-25`) and *"there is no Agent, Workflow, Skill,
planner, executor, model adapter, scheduler, task queue, concurrency engine, or
automation logic here"* (`runtime.py:9-10`). **The absence is an architectural
guard, stated in the code that would host any of these, not an oversight.**
This corroborates `F-4`'s independent finding for `P12-W2` state
(*"the guard held; the probe did not"*) at the runtime layer specifically.

---

## 6. Hard Question 06/07/08 — Does authority already exist? Founder? Architect?

[E] Three passes were made over the corpus for anything resembling a grant:

1. **`FDE-P10-AUTONOMOUS-EXECUTION-01`** (`AIOS_P10_AUTONOMOUS_EXECUTION_FOUNDER_EVENT_PROPOSAL_v1.0.md`,
   ISSUED, OPERATIVE, Founder Moriarty, 2026-09-05) — read in full. Its subject
   is **Claude's own execution autonomy** during construction: resolve-on-
   discovery, standing construction authority, follow-on Act generation,
   conformance repair. Its own Level 4 table reserves *"Founder authority ·
   Founder-reserved decisions... non-delegable boundaries"* explicitly, and its
   §6 invariant states plainly: *"EXECUTION ACT → NEW AUTHORITY: prohibited."*
   **This grants nothing about AIOS deciding, on its own, when to act.** It is
   the *Claude autonomy* half of this Act's §2 core distinction, not the *AIOS
   operational authority* half.
2. **`P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md`** (the operative P12
   authorization, read in full above and at §4) — its `§20 AUTONOMOUS
   EXECUTION RULE` is the same distinction again: Claude must not stop merely
   because it found one blocker, and must continue independent authorized
   work. It does not touch invocation of AIOS by anything other than the
   person running Claude Code.
3. **Broad search** of `docs/architecture/adr/decisions/`, the Governance
   Decision Register, the Delegation Register, the Appointment Register, and
   every governance/architecture file for `scheduler|daemon|orchestrator|queue
   consumer|event listener|autonomous loop|self-activat|resident non-manual|
   operational activation` — **zero matches outside the documents already
   discussed above.**

[D] **EXISTING AUTHORITY: NO.** Not `IMPLIED BUT NOT SUFFICIENT` — genuinely
absent. No Founder Decision, ADR, delegation clause, or appointment clause
authorizes AIOS to be invoked by anything other than a person. Two clauses
affirmatively point the other way without deciding the matter pre-emptively:
`DEL §3.2` exclusion 19 (*"activate itself without a durable activation
record"*) and `APT §3.2` exclusion 19 (*"authority to authorize itself"*) —
both aimed at the delegate's own authority, not at an AIOS runtime, but
carrying the same principle this Act must apply: **activation requires a
durable record of a human decision, not a mechanism's own operation.**

[D] **Since self-activation is NOT REQUIRED (§4), Hard Questions 07/08 do not
arise now** — there is no work item that depends on Founder or Architect
authority for this, so there is nothing to escalate. This is recorded for the
future: **if** a resident non-manual entry is ever proposed for a genuine,
proven need, it would engage:

- **Founder authority** — `FDP-P10-001` (Security) and `FDP-P10-003`
  (Governance Authority) are both, today, `FOUNDER RESERVED + NO BINDING
  DECISION BODY FOUND` (`P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md §7-8`,
  `D2`/`D3 = CONDITIONAL-BLOCKING`). A mechanism that decides when AIOS acts
  is a security-relevant and governance-relevant operational policy by
  definition (§3 above) — a direct dependency on both, unresolved.
- **Architect authority** — only if the mechanism would create a new runtime
  role, a new control plane, or a structural change to the Native Core's
  eleven frozen boundaries (`D6`); a bounded, revocable, human-scoped trigger
  might not cross this boundary, but that determination cannot be made in the
  abstract and is not made here.
- **Constitution §6.2 invariant 2** — required approval must exist *before*
  execution, for the mechanism itself, not merely for the work it would run.

---

## 7. Minimum activation mechanism

[D] Per §4, the minimum sufficient mechanism for everything P12 currently
requires is **the one already in place: human-initiated activation.** Every
canonical requirement this Act traced back to source — the `§17` execution
chain, the `§19`/`§30` runtime evidence, the `§9` P12 exit criterion — is
satisfied today by hand-invoked, independently verified execution. No stronger
mechanism (scheduled, event-driven, queue-driven, bounded orchestrator,
autonomous loop) is authorized, needed, or built by this Act.

---

## 8. Two-path construction gate — disposition

Neither Path A nor Path B applies in the form the governing Act anticipates,
because the antecedent both paths share — **REQUIRED** — is false:

```
REQUIRED?  →  NO (§4)
   │
   ▼
W4-GAP-007 IS NOT A GAP AGAINST ANY CANONICAL REQUIREMENT
   │
   ▼
NO CONSTRUCTION · NO DECISION PACKAGE NEEDED · RECLASSIFY AND STOP
```

This is `§24` of the governing Act, applied: *"Jika evidence membuktikan NOT
REQUIRED, maka W4-GAP-007 → NOT-A-GAP / MISCLASSIFIED GAP... Tidak perlu
membangun activation mechanism."* No Founder or Architect decision package is
prepared, because none is owed — there is no proven dependency for either
office to rule on. §6 above is retained as a decision-ready reference for
whoever raises the question again, not as a package awaiting signature.

---

## 9. Negative controls

Per the governing Act §33, exercised against the current, unmodified system:

| Test | Expected | Result |
|---|---|---|
| unauthorized autonomous loop | blocked | **blocked** — none exists; `bootstrap.py`/`runtime.py` docstrings exclude it structurally |
| unauthorized scheduler | blocked | **blocked** — same; `native_core`, `consumers`, `tools` import-graph search (this Act, reproducing `P12-W6`'s method) finds no scheduler/dispatcher anywhere in the composed system |
| unauthorized event-driven activation | blocked | **blocked** — no event listener resident |
| unauthorized queue execution | blocked | **blocked** — no queue consumer resident |
| Founder-reserved action encountered | escalated/refused | **not exercised** — no work item reached this boundary, because none was required to |
| Architect-reserved action encountered | escalated/refused | **not exercised** — same |
| authority substitution (technical reachability treated as authority) | blocked | **blocked** — this Act's own §2/§6 finding is exactly that this substitution must not happen, and no artifact in this Act performs it |
| invalid/expired/revoked authority, invalid trigger/scope | refused | **not applicable** — no trigger or activation authority exists to test |

[D] `NOT EXERCISED` is reported honestly where nothing was reached, per the
governing Act's own prohibition on converting `NOT EXERCISED → PASS`.

---

## 10. `W3` position

[E] `docs/architecture/p12/` has no `P12-W3-*.md` of any kind — no
construction, no discovery record, no partial file. `P12-W6-SCOPE-DISCOVERY-AND-CLASSIFICATION.md`'s
`§19` item table lists `GOVERNANCE` (the `§19` scope item nearest W3's subject)
as `ACTIONABLE — P12`, separate from `STATE` (`BLOCKED — DEPENDENCY (P12-W2)`).

[D] **`W3` remains `UNBUILT + CANONICALLY REQUIRED (per the Blueprint's six
work packages) + not required by this Act's finding.** This Act does not
authorize, schedule, or recommend W3 construction. It confirms the governing
Act's own non-absorption rule (`§28`/`§30`): the escalation-join gap
(`W4-GAP-008`) and the activation-authority question this Act closes are both
things W3 must **not** be used to backfill silently — and this Act has not
used W3 for anything. `W3 ≠ automatically next construction` (§27 of the
governing Act) is honored: nothing here creates pressure toward W3 beyond what
already existed.

---

## 11. Governance summary

- `F-16` (Founder-reserved, E12 Evidence Matrix) — **not approached.**
- `F-17` (Architect/Founder, Phase↔PD implementation assignment) — **not
  approached.**
- `F-18` (Architect-reserved + source-blocked, cross-PD interface definition)
  — **not approached.**
- `FDP-P10-001` (Security), `FDP-P10-003` (Governance Authority) — **remain
  open**, `CONDITIONAL-BLOCKING`; this Act found no P12 work item with a proven
  direct dependency on either, so neither blocks anything here.
- Native Core — **unchanged, 11.** No twelfth subsystem, no new runtime role,
  no new control plane was proposed or built.
- Protected `docs/program/AIOS_*` packages — **not modified.** The one read
  (`AIOS_PHASE_10_13_PLATFORM_ORGANIZATION_BLUEPRINT_v1.0.md §9`) was for
  citation-verification only, consistent with the prior Act's own resolution
  that the protection binds modification and authority-use, not read access to
  a tracked, previously-cited canonical source.

---

## 12. Verification

[E] **Fresh-process reproducibility.** Every claim in this document rests on a
byte-for-byte grep or read of a resident file, re-run at the time of writing:
`P12-AUTHORIZATION-FOUNDER-DECISION-ISSUED.md` (full text, §§1-38),
`AIOS_P10_AUTONOMOUS_EXECUTION_FOUNDER_EVENT_PROPOSAL_v1.0.md` (full text,
§§1-40), `AIOS_DELEGATION_REGISTER_v1.0.md §3`, `AIOS_APPOINTMENT_REGISTER_v1.0.md §3`,
`engineering-constitution-v1.md §6`, `runtime-framework.md §§1-7`,
`P12-W4-EXECUTION-INTEGRATION.md` (full text), `P12-W6-RUNTIME-AND-WORKFLOW-VERIFICATION.md`
(full text), `P12-FRONTIER-AND-AUTHORITY.md` (full text), and a direct
`native_core`/`consumers`/`tools` search for scheduler/daemon/cron/event-loop
patterns. No claim here rests on a prior Claude report's summary of any of
these.

[E] **Independent verification.** No new instrument, no new module, no new
class was written to produce this finding — it is a re-derivation from source,
which is itself the strongest available independent check against the
gap-register entry it corrects.

[E] **Regression.** No file under `native_core/`, `consumers/`, or `tools/`
was modified by this Act. No certified P10/P11 evidence, no `TraceRecord`, no
delegation record was touched. The only repository changes are this document
and the correction note added to `P12-W4-EXECUTION-INTEGRATION.md §7` (below).

---

## 13. Final state

**Executive result**

```
W4-GAP-007:              CANONICAL DEFINITION GAP in its own requirement citation;
                          the underlying capability is NOT REQUIRED
FINAL CLASSIFICATION:    OA-1 — NOT-A-GAP
SELF-ACTIVATION:         NOT REQUIRED
OPERATIONAL REACHABILITY: NOT REQUIRED (non-manual sense); ALREADY SATISFIED
                          (evidence sense — §19/§30, via hand-invoked execution)
EXISTING AUTHORITY:      NO (none needed; none found either way)
FOUNDER AUTHORITY:       NOT REQUIRED NOW · WOULD BE REQUIRED if ever proposed
                          (FDP-P10-001, FDP-P10-003 both open and directly relevant)
ARCHITECT AUTHORITY:     NOT REQUIRED NOW · WOULD BE REQUIRED if the mechanism
                          crossed a Native Core or control-plane boundary
MINIMUM MECHANISM:       human-initiated activation (already in place; sufficient)
FINAL PATH:              NOT-A-GAP
```

**What closed:** `W4-GAP-007` as previously classified (`BLOCKED —
DEPENDENCY`, `STOP-D`). **What remains open:** `W4-GAP-008` (unchanged,
`DEPENDENCY (P12-W3)`), `F-16`, `F-17`, `F-18` (unchanged, unapproached). **What
is blocked:** nothing new. **What is reserved:** Founder/Architect authority
over any future resident-activation proposal, per §6 above — reserved, not
opened. **What is not-a-gap:** `W4-GAP-007`. **Next legitimate frontier:**
whatever `P12-W6`'s own remaining actionable scope items (`RUNTIME`,
`WORKFLOW`, `GOVERNANCE`, `PROVENANCE`, `FAILURE`, `NEGATIVE CONTROLS`) still
carry forward — unaffected by, and independent of, this Act's finding.

**Governing invariant, restated as this Act leaves it:** Claude Code remains
autonomous in *how* to execute authorized work, including this discovery. It
did not, and does not, decide that AIOS itself may act without a person
invoking it — because no evidence surfaced that requires that decision to be
made at all.
