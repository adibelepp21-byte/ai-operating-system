# P12 — Fresh Independent Exit Contract Determination

**Required by:** `FD-P12-004` — *"After applying the ruling, perform a fresh
independent P12 Exit Contract determination… Do not assume `§6.8 SATISFIED` +
`§6.9 SATISFIED` = `P12 COMPLETE`."*

```text
P12 COMPLETE = NO

Blocking: §6.7  system-wide verification has been completed
          §6.14 completion conditions independently satisfied (through §6.7)
```

**The instruction not to assume was the load-bearing one.** `§6.8` and `§6.9`
did both close, and had the determination been taken as their sum, P12 would
have been declared complete. Re-measuring every condition instead surfaced a
different blocker — **live W6 findings that have nothing to do with `R-A`,
`R-B`, or anything the last six Acts were chasing.** They were never hidden;
they were simply never the thing being looked at, because the blocker set had
been fixed on `§6.8`/`§6.9`/`§6.11` since `ACT-CC-P12-022`.

---

## 1. Every condition, measured fresh

Each row re-run against the repository at the head of this record, not carried
from a prior package.

| | Condition | Measurement | State |
|---|---|---|---|
| 1 | W1–W6 satisfied | `E12-01…05` **5/5**; `E12-06` ratified `R1` | **SATISFIED** |
| 2 | P4–P11 integration coherent | 8 classes · 7 VERIFIED · 1 RESERVED (`F-17`) · **0 invalid · 0 dangling** | **SATISFIED** |
| 3 | unified operational state valid | 9 checks · **9 verified** · 0 violated | **SATISFIED** |
| 4 | governance integration valid | `E12-03` | **SATISFIED** |
| 5 | execution integration traceable | `E12-04`; 4 provenance manifests, each resolving a delegation and a Trace record | **SATISFIED** |
| 6 | self-model sufficiently accurate | 12 questions · 10 verified · 2 inferred · **0 unknown** | **SATISFIED** |
| **7** | **system-wide verification has been completed** | **see §2 — five live findings** | **NOT SATISFIED** |
| 8 | negative controls hold | `§49` **13 / 13 refused** (`FD-P12-004`) | **SATISFIED** |
| 9 | mutation tests hold | `§50` **10 / 10 detected** (`D-P12-027-01`) | **SATISFIED** |
| 10 | regression integrity holds | `§51` **11 / 11 HELD** · 0 REGRESSED · 0 UNANCHORED | **SATISFIED** |
| 11 | cross-phase / cross-platform evidence | cross-phase **8/8**; cross-platform **18/18** readable, `MENTIONED 0` (`D-P12-027-03`) | **SATISFIED** |
| 12 | remaining frontiers classified | every residual classified, owned, sourced | **SATISFIED** |
| 13 | no authorized actionable construction remains | **see §3** | **NOT SATISFIED** |
| **14** | **completion conditions independently satisfied** | `§56`'s `VERIFICATION` rests on `§6.7` | **NOT SATISFIED** |

```text
11 SATISFIED · 3 NOT SATISFIED   (11 + 3 = 14)
```

---

## 2. `§6.7` — what the W6 surfaces actually report

`§6.7` is the only condition that carries the results of the W6 surfaces
`§6.8`–`§6.11` do not cover. `§6.8` carries negative controls, `§6.9`
mutations, `§6.10` regression, `§6.11` cross-phase and cross-platform evidence.
**Nothing else carries `§30` runtime, `§31` workflow, `§33` failure semantics or
`§34` provenance** — so `§6.7` does, and these are its findings.

### 2.1 `§33` — failure states · **3 of 7 distinguished**

`§33`: *"Failure behavior **must** distinguish: `RETRYABLE BLOCKED REFUSED
FAILED ESCALATED SUCCEEDED VERIFIED`."*

```text
RETRYABLE   UNREACHABLE    no live retry mechanism exists
BLOCKED     RAISED ONLY    persisted as required-vs-held; not told apart afterwards
REFUSED     RAISED ONLY    2 refusal types raised; no field names which one
FAILED      DISTINGUISHED  Trace status='failure'
ESCALATED   DISTINGUISHED  Trace status='escalation' + escalation record
SUCCEEDED   DISTINGUISHED  Trace status='success'
VERIFIED    UNREACHABLE    ratified Trace vocabulary is ['escalation','failure','success']

retry prohibitions (5): NOT APPLICABLE — no live retry mechanism exists, so
none of the five can be violated, and none is controlled against
```

*"A state is distinguished only if it can be reached AND told apart afterwards.
The record is what anyone reads later, not the traceback."*

### 2.2 `§34` — execution provenance · **NOT ASSEMBLABLE**

11 of 11 elements are carried, and the chain still does not join:

```text
7 / 15 executions name their delegation
  evidence records  3 / 3
  Trace records     4 / 12
8 could only be matched by actor name, which identifies a set of grants
rather than the one in force
```

*"An element carried on one record and another on a different record is
provenance only if the two records can be joined."*

### 2.3 `§31` — workflow chain · **NOT CONNECTED**

```text
PLAN → HANDOFF        EVIDENCED      31/31 delegations name their bound plan
HANDOFF → WORK        EVIDENCED      31/31 declare the work they author
WORK → EXECUTION      BY CONVENTION  7/15 executions name the work performed  ← weakest
EXECUTION → OBSERVATION  EVIDENCED   4/4 manifests name an observation subject
OBSERVATION → VERIFICATION EVIDENCED 4 manifests carry requirement and outcome
```

*"The unit is the link, not the element."* One link of five holds only by
convention, so the chain is not connected.

### 2.4 `§30` — runtime · **1 of 9 items absent**

`verification` is absent from the ratified Trace vocabulary — the same cause as
`VERIFIED` in `§33`.

### 2.5 `§35` — governance evidence · **2 of 9 elements absent**

Over **436** instruments: 1 element `ESTABLISHED`, 6 `PARTIAL`, 2 `ABSENT`
(`affected surfaces`, `verification`). A property of a corpus issued across the
whole programme; retrofitting labels onto historical instruments would be
rewriting historical evidence.

### 2.6 Classification of each

| Finding | Class | Closable by P12? |
|---|---|---|
| `VERIFIED` unreachable; runtime `verification` absent | **RATIFIED-CONTRACT RESERVED** — the Trace vocabulary is ratified and `NATIVE CORE = 11` is frozen | **No** — altering it is outside P12 |
| `RETRYABLE` unreachable | **CAPABILITY ABSENT** — no retry mechanism exists anywhere resident | **Unknown** — building one is construction no Act has authorized, and `§33` does not require a retry mechanism to exist, only that the state be distinguished if it occurs |
| `BLOCKED` / `REFUSED` raised-only | **P12 GAP** — the escalation record carries no field naming which refusal occurred | **Plausibly yes** — a record field, for future records |
| provenance `NOT ASSEMBLABLE` (8/15) | **HISTORICAL RECORD** — the eight unjoinable executions are already written | **Not retrospectively** — rewriting them is forbidden |
| workflow `WORK→EXECUTION` by convention | **HISTORICAL RECORD** — same eight executions | **Not retrospectively** |
| governance elements absent over 436 | **HISTORICAL CORPUS** | **No** — would rewrite history |

**This is not a claim that `§6.7` is unclosable.** Two of the six look closable
for future records. It is a statement that `§6.7` is **not satisfied now**, on
measurements taken now.

---

## 3. `§6.13` — and the correction it forces

`ACT-CC-P12-026` recorded *"no authorized actionable construction remains"* and
this determination cannot repeat it. `§2.6` identifies at least one finding —
the escalation record naming which refusal occurred — that is **plausibly
closable P12 construction** and is authorized under `ACT-CC-P12-027 §4`, which
covers implementation, verifier correction and evidence generation without a
further Act.

**`§6.13` is therefore `NOT SATISFIED`**, and that is a correction against the
Handoff Record's `P12 ACTIONABLE WORK = NONE`. Whether the work closes `§6.7` is
not yet established; that it exists and is authorized is.

**No such work is performed in this record.** `FD-P12-004`'s required action was
a determination, and a determination that started constructing would stop being
one.

---

## 4. What did **not** block, and is worth stating

`R-A` and `R-B` — the two residuals five Acts were organised around — **do not
appear in this determination at all.**

- `R-A` (instrument authenticity) was never needed: `§6.9` closed against the
  canonical decision contract, and `§6.8` closed on the Founder's ruled
  semantics. Neither required a trust anchor.
- `R-B` (corpus residency) was never a requirement: `ESC-C7-01`, `E-29`,
  Volumes 3/4, `G-01` and `F-18` appear **zero times** in the canonical Exit
  Contract (`ACT-CC-P12-026`).

Both remain real external matters owned by the Founder and Architect. Neither
is a P12 completion dependency, and neither is what P12 is waiting on.

---

## 5. Determination

```text
P12 COMPLETE = NO

EXACT CONDITIONS AND BASIS
  §6.7   NOT SATISFIED   §33 3/7 failure states distinguished ·
                         §34 provenance NOT ASSEMBLABLE (7/15) ·
                         §31 workflow chain not connected ·
                         §30 1/9 runtime items absent ·
                         §35 2/9 governance elements absent over 436
  §6.13  NOT SATISFIED   at least one authorized, plausibly closable item
                         exists — correcting ACT-CC-P12-026
  §6.14  NOT SATISFIED   §56 VERIFICATION rests on §6.7

P12 CONSTRUCTION   = NOT EXHAUSTED   ← corrected
P12 CERTIFICATION  = NOT CLAIMED     (§57 Founder-reserved)
P13                = NOT AUTHORIZED  (§58; P13 AUTHORIZED = false, stated)
```

`FD-P12-004`: *"If any condition remains NOT SATISFIED or NOT ESTABLISHED,
report the exact condition and basis."* Three do, and none of them is
`§6.8`, `§6.9` or `§6.11`.

## 6. Corrections this determination makes to the record

| Previous | Correction |
|---|---|
| `P12 CONSTRUCTION = EXHAUSTED` (Handoff Record `§2`, `ACT-CC-P12-025`) | **NOT EXHAUSTED** — `§2.6` identifies authorized, plausibly closable work |
| `P12 ACTIONABLE WORK = NONE` (Handoff `§10`; `ACT-CC-P12-026`) | **Work exists**; `§6.13` is `NOT SATISFIED` |
| `§6.7 PARTIAL` because of cross-PD interfaces | **NOT SATISFIED for different reasons** — the cross-PD half resolved under `D-P12-027-03`; the actual findings are `§30`/`§31`/`§33`/`§34`/`§35` |
| Blocking set = `R-A` + `R-B` | **Neither blocks.** The blocking findings are internal to W6 and were never examined while the blocker set was fixed |

Historical records are preserved; these corrections are additive and named.
