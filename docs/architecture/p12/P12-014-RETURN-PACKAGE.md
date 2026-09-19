# `ACT-CC-P12-014` — R1 Real System Work Construction & Live Operating Integration

```text
E12-06   NOT SATISFIED — 7 of 8 phases consumed by real system work
P6       NOT CONSUMED — blocked on a human governance approval, not on engineering
P4 P7 P9 CONSUMED BY REAL SYSTEM WORK  (were: demonstrator-only, not consumed, demonstrator-only)
§74 J    NOT SATISFIED
P12      NOT COMPLETE · NOT EXHAUSTED · certification NOT READY
```

**AIOS now runs a real work path.** A Runtime is started, a Workflow hosts the
work, the corpus is actually assessed, Memory is genuinely consumed, and every
crossing is observable and independently verifiable. Four phases moved. The
fifth did not, and the reason is a hard authority boundary that `§36.8` says to
stop at: **admitting Knowledge requires a provenance-verified human approval**,
and this office does not manufacture one.

**`§46` applies and is not evaded.** *"Failure is a valid engineering result. It
must not be converted into PASS by changing the acceptance interpretation."*
`R1` is untouched.

---

## A. Authority

| | |
|---|---|
| **`FD-P12-001`** actual body | read: `§4` `E12 = RATIFIED` · `§5` `FOUNDER SELECTION: R1 — CONSUMPTION BY REAL SYSTEM WORK` · `§6` `R2`/`R3` `NOT SELECTED` · `§23` `Decision Status: FINAL / ISSUED` |
| E12 ratification | **RATIFIED** |
| `§C` selection | **`R1`** — and `§5`'s exclusion clause is the load-bearing half: *"The existence of a component, provisioned capability, **demonstrator**, test fixture, or merely callable surface is not by itself sufficient evidence of consumption by real system work."* |
| Delegated construction authority | `ACT-CC-P12-014 §5`, bounded by `§9` (minimum real system), `§14` (no autonomous runtime), `§36` (hard stops) |

---

## B. Starting State

Verified fresh at `a0e96e2` before construction:

```text
E12-06 = NOT SATISFIED   4/8 consumed
P4 = demonstrator only · P6 = no execution ever recorded
P7 = no execution ever recorded · P9 = demonstrator only
P12 NOT COMPLETE · NOT EXHAUSTED
```

---

## C. Architecture

**The work is the system's own, not written for the measurement.** AIOS already
audits its governance corpus — `governance_index` recomputes each instrument's
content hash, `corpus_citation_audit` resolves every citation,
`stale_state_audit` separates live assertions from historical uses. What never
existed is a path performing that assessment **as hosted work**.

```text
REAL WORK REQUEST   assess the governance corpus
      ↓
RUNTIME             AIOSRuntime.initialize() → start() → RUNNING          (P4)
      ↓
WORKFLOW            declared, ready, RUNNING, SUCCEEDED                   (P9)
      ↓
EXECUTION CONTRACT  create_execution_layer(runtime) → execution.runtime.* (§15)
      ↓
STEPS               three areas assessed; each finding retained in Memory
      ↓
CONSOLIDATION       findings read back out of Memory                      (P7)
      ↓
JUDGEMENT           against criteria held as Knowledge                    (P6)
      ↓
OBSERVATION         runtime + workflow published while in state          (§22)
      ↓
EVIDENCE            Trace records with captured content (INV-6)
```

**Why Memory is load-bearing (`§20`).** The consolidation step has no other
source for the three findings. Carrying them in a local variable would be the
bypass `§8` names — the steps would still run and Memory would not be consumed.
Reading them back through `MemoryRetrieval` is the `E7-03` path the Memory
consumer itself documents: *"propose the configured Candidate, then read the
configured key — both during that Execution."*

**Why Knowledge is load-bearing.** *"Is the corpus healthy?"* is a judgement
against criteria. A threshold hard-coded in the worker is the worker's opinion;
a threshold held as an admitted Knowledge version is the system's, and changing
it is a governed act. Remove it and the audits still produce numbers — no
verdict follows. The work does not invent a default; it records the verdict
**withheld**.

**Components reused, not rebuilt (`§9`):** `AIOSRuntime`, `WorkflowLifecycle`,
`WorkflowMonitor`, `MemoryLifecycle`/`MemoryRetrieval`, `KnowledgeRetrieval`,
`TraceWriter`/`TraceReader`, `LocalAppendOnlyStorage`, `TracedAction`,
`p12_runtime_observation`, and the three audits. **No new subsystem, no second
Execution Contract, no competing Knowledge or Memory layer, no new Native Core
entity.**

**Architectural finding, recorded not worked around:** Runtime-hosted Memory is
in-process by construction — `create_memory_subsystem` builds a bare
`MemoryLifecycleStore()` holding no storage facility. A cross-run delta is
therefore **not** claimed; consumption is within the execution, which is the
ratified shape.

---

## D. Construction

| File | Change |
|---|---|
| `aios_corpus_health_run.py` | **new** — the real work path |
| `tools/p12_cross_phase_verification.py` | `_captured()` added; demonstrator attribution made structural — **two pre-existing defects**, see `N` |
| `tools/tests/test_p12_cross_phase_verification.py` | 4 controls realigned, 3 added |
| `tools/tests/test_p12_e12_acceptance.py` | 4 controls realigned, 2 added |
| `tools/tests/test_p12_integration_graph.py` | 1 control realigned |
| `docs/architecture/p12/P6-KNOWLEDGE-ADMISSION-DECISION-SURFACE.md` | **new** — the `§36.8` decision surface |
| `docs/architecture/p12/P12-014-RETURN-PACKAGE.md` | this document |
| `docs/architecture/p12/trace-stores/aios-corpus-health/` | **new evidence** — Trace records from real runs |
| `docs/architecture/p12/runtime-observations/` | **new evidence** — runtime and workflow observations |

**Boundaries preserved:** `§14` no daemon, scheduler, queue or self-activation —
the runtime is started and stopped by the entry point, `OA-1` untouched. `§15`
capability reached only through the Execution Contract. `§16` W4 stages
distinct. `§17` W3 join unchanged. `§27`/`§28` no historical evidence rewritten;
the demonstrator stores remain exactly as they were.

---

## E. Running System

Real run, real corpus:

```text
governance_records 469 · governance_sources 415 · stale_governance_sources 0
citation_documents 277 · citations_checked 1655 · citation_errors 0
documents_scanned 548 · live_stale_assertions 0 · historical_uses 55

runtime   aios-corpus-health-runtime   RUNNING → STOPPED
workflow  aios-corpus-health           RUNNING → SUCCEEDED
memory    3 findings retained, 3 read back
verdict   WITHHELD — no Active Knowledge version for 'corpus-health.criteria'
```

**`§21` honoured.** The work ran to its honest end and recorded the verdict
withheld rather than being altered until it passed. `TracedAction.failed()` was
called with the reason, so the Trace record carries `status: failure` — a
truthful outcome, not an engineered one.

---

## F. P7 Memory — CONSUMED

| | |
|---|---|
| Evidence | `memory_consumed ['corpus-health.finding.citations', 'corpus-health.finding.governance', 'corpus-health.finding.stale-state']` |
| Shape | **captured content, not references** — `{"key": …, "content": {…}}` per INV-6, so the record stays explainable if the Memory item is later expired |
| Materiality | the consolidation step fails loudly (`Memory lost a retained finding`) if retrieval returns nothing |
| Independent verification | `p12_cross_phase_verification` reads the durable store from disk; the fresh-process run reproduces it |

## G. P6 Knowledge — NOT CONSUMED · hard authority boundary

The work reaches `execution.runtime.knowledge.retrieval.active(...)` on a
RUNNING Runtime and finds nothing Active. Traced to the bodies:

```text
consume Knowledge  → needs an Active KnowledgeVersion
Active version     → only via KnowledgeAdmission.admit(candidate, authorization)
admit              → iff GovernanceReview.promotion_authorized(candidate)
authorized         → "True iff a human `approve` produced by this Governance is
                      on record … Default is deny — absence of an authorising,
                      provenance-verified human decision means no promotion"
human approve      → ReviewDecision(..., HumanAuthority(reviewer_id), rationale)
                      "a human authority requires a non-empty reviewer identity"
```

**No resident Active Knowledge version exists**, and this office holds no human
authority. `§36.8` makes that a hard stop. Decision surface prepared, blank, at
[`P6-KNOWLEDGE-ADMISSION-DECISION-SURFACE.md`](P6-KNOWLEDGE-ADMISSION-DECISION-SURFACE.md).

**`§10` was honoured**: no artificial P6 consumption was created to change the
status.

## H. P4 Runtime — CONSUMED (was demonstrator-only)

`aios-corpus-health-runtime` appears in the Trace records beside the existing
runtimes, and the observation is published while the Runtime is genuinely
`RUNNING`. The demonstrator evidence is untouched and still present — `§12`:
existing demonstrator evidence remains historical evidence.

## I. P9 Workflow — CONSUMED (was demonstrator-only)

`workflow observation published for ['aios-corpus-health', 'p12-f11-workflow-observation']`.
The real workflow hosted the assessment and reached `SUCCEEDED`; the
demonstrator's observation remains alongside it, unrewritten.

---

## J. F-13 — freshly re-derived

| | |
|---|---|
| Pre-construction (`P12-013 C`) | `PARTIALLY CLOSED + SOURCE-GAP` |
| What changed | the demonstrator attribution is now **structural**: a phase is demonstrator-only when the evidence names at least one demonstrator and **no** crossing that is not one. The superseded rule asked whether the evidence mentioned a demonstrator and mentioned neither `p11-` nor `engineering-intelligence` — an allow-list of the only two non-demonstrator crossings that existed when it was written |
| Source gap closed? | **Partly, and only where it was load-bearing.** The attribution no longer needs a marker allow-list, so adding a real-work crossing no longer misattributes it. `DEMONSTRATOR_EXECUTIONS` is still an explicit list of three named artifacts |
| Remaining | **SOURCE-GAP**, narrowed. No canonical rule says how to classify an arbitrary subject as demonstrator or work; `§26` forbids inventing a general taxonomy, and none was invented |
| Classification | **PARTIALLY CLOSED + SOURCE-GAP (narrowed)** |

---

## K. E12 — fresh R1 measurement

| Phase | Verdict | Change |
|---|---|---|
| `P4` Runtime | **CONSUMED BY REAL SYSTEM WORK** | ← demonstrator only |
| `P5` Intelligence | CONSUMED BY REAL SYSTEM WORK | — |
| **`P6` Knowledge** | **NOT CONSUMED — no execution ever recorded** | unchanged; authority-blocked |
| `P7` Memory | **CONSUMED BY REAL SYSTEM WORK** | ← no execution ever recorded |
| `P8` Tools | CONSUMED BY REAL SYSTEM WORK | — |
| `P9` Workflow | **CONSUMED BY REAL SYSTEM WORK** | ← demonstrator only |
| `P10` Department | CONSUMED BY REAL SYSTEM WORK | — |
| `P11` Organization | CONSUMED BY REAL SYSTEM WORK | — |

```text
E12-06 = NOT SATISFIED   consumed 7 / 8   demonstrator-only 0
```

---

## L. `§74` Part J — fresh reconciliation

`§31`: the previous failure is not copied, and not replaced by PASS without new
evidence.

| `§56` condition | Before | Now |
|---|---|---|
| REQUIREMENTS · AUTHORIZED CONSTRUCTION · OPERATIONAL EVIDENCE · INTEGRATION · SYSTEM INTEGRITY · FRONTIER CLASSIFICATION | evidenced | **evidenced** — and operational evidence is materially stronger: a hosted, observed, independently verifiable work path now exists |
| **VERIFICATION** | NOT SATISFIED (4/8) | **NOT SATISFIED (7/8)** — `P6` alone |
| **EXHAUSTION** | NOT SATISFIED | **NOT SATISFIED** — see `M` |

**Part J: NOT SATISFIED.** Two of eight conditions fail, both traceable to `P6`.
The pre-construction `§74` package is unmodified.

---

## M. P12 — completion, certification, exhaustion

```text
P12 COMPLETE       = NOT COMPLETE
P12 CERTIFICATION  = NOT READY — and Founder-reserved regardless (§57, FD §28)
P12 EXHAUSTION     = NOT EXHAUSTED
```

**Fresh frontier discovery (`§33`), not inherited:**

| Frontier | Classification |
|---|---|
| **P6 Knowledge admission** | **HARD AUTHORITY BOUNDARY — human governance decision required.** Decision surface prepared. `§34`: stop, do not self-authorize |
| `E12-06` remaining 1/8 | blocked on the above |
| `§74 J`, `P12 COMPLETE` | blocked on the above |
| `F-13` general taxonomy | **SOURCE-GAP**, narrowed |
| `F-17`, `F-18`, `F-8`, `F-9`, `FDP-P10-001/-002/-003`, `ADP-P10-001`, issuance authenticity, execution-vocabulary extension, instrument amendment, P12 certification | **RESERVED**, untouched (`§19`, `§20`) |
| P13 | **FUTURE PHASE** — `AUTHORIZED = FALSE` (`§18`) |
| New requirement / integration gap / evidence gap / contradiction / completion dependency | **none found** |

**No executable frontier remains that this Act is authorized to take.** The one
remaining item is a decision, not engineering.

---

## N. Verification

### Two pre-existing defects, found by the first real execution

| # | Defect | How found | Fix |
|---|---|---|---|
| 1 | `_knowledge_exercised`/`_memory_exercised` built a `set` straight from the record entries, so they could **only read records that violated INV-6** by storing bare hashable strings. The first record to capture content as the invariant requires made the phase report `UNKNOWN: unhashable type: 'mappingproxy'` | the real run's own measurement | `_captured()` identifies each entry whatever shape it carries. **Fixed at the verifier, not by flattening the record to strings** — the record's invariant is canonical, and a measurement that can only read records breaking it is the defect |
| 2 | Demonstrator attribution used a marker allow-list (`p11-`, `engineering-intelligence`). A **new** real-work crossing carries neither, so a genuinely crossed phase still reported demonstrator-only | `P4`/`P9` stayed flagged after real crossings appeared | attribution made structural. A control keeps the superseded rule and proves it would have misattributed the new work |

**No self-introduced defect was found.** Both defects predate this Act; the
construction surfaced them.

### Controls realigned — stricter, not relaxed

Ten controls pinned the pre-construction state and failed. Each was narrowed to
the new exact truth and paired with a control proving the new result is measured
rather than constant:

- `exercised_only_by_a_demonstrator` is now pinned `()` — **and**
  `_is_demonstrator_only` is driven on synthetic demonstrator-only evidence, so
  an empty list is a measurement.
- `not_consumed` is pinned `["P6"]` exactly — a fourth phase failing, or `P6`
  passing without an admitted Knowledge version, still fails.
- `P4`/`P9` demonstrator-only assertions became a **rule** test on synthetic
  evidence rather than a corpus observation.
- `memory ↔ state` moved `UNVERIFIED → VERIFIED`; the control that drives the
  derivation to raise still proves the edge can leave `VERIFIED`.

### `§24`/`§25` falsification

| Control | Result |
|---|---|
| demonstrator-only → NOT CONSUMED | **HELD** — driven synthetically |
| provisioned-only → NOT CONSUMED | **HELD** — `P6` is provisioned by every runtime and fails |
| fake execution / missing provenance / stale evidence | **HELD** — `§49` 12 of 13 refused |
| synthetic all-real fixture → SATISFIED | **HELD** — the verdict reaches `SATISFIED` only on evidence representing the defined condition |
| R1 result is not a constant | **HELD** — it moved `4/8 → 7/8` on real evidence, and reaches `SATISFIED` synthetically |
| Instrument falsifiability | **29 / 29 DEMONSTRATED** |

### Independent verification

The measurement reads the durable Trace store **from disk**, not from the
constructor's return value; `p12_e12_acceptance` reads the ratified boundary
from the persisted instrument by body content; every figure reproduces in a
**fresh OS process**.

---

## O. Integrity

| | |
|---|---|
| **Native Core** | **11** |
| **Protected artifacts** | `docs/program/AIOS_*` → `sha256 abfc6b09d2a14acb…`, **identical** |
| Certified P10 / P11 evidence | 0 changes |
| Pre-ratification E12 package · `§74` package | **byte-identical** |
| Demonstrator evidence | untouched |
| W3 join | `{3, 0, 2, 0, 2}` — unchanged, `W4-GAP-008`/`W2-GAP-007` not regressed |
| W4 | 4 manifests, 4 joined, 0 dangling — unchanged |
| W5 | 12/12 BOUND, 0 authority-creating functions — unchanged |
| W6 STATE | **4/4 chain complete** — not regressed |
| **W1** | 8 edges, **5 VERIFIED** (was 4), 2 UNVERIFIED, 1 RESERVED — `memory ↔ state` moved because real work populated it |
| `§49` · `§50` · `§51` | 12/1 · 8/2 · **10 HELD**, 1 `NOT APPLICABLE` |
| `§52` fresh process | **8 / 8 REPRODUCED** |
| Citations | **279 documents, 1664 citations, 0 errors** |
| **Regression** | `native_core` **801 OK** — 800 PASS + **1 EXPECTED FAILURE** (pre-existing) · `consumers` **276 OK** · `tools` **1186 OK** — 1185 PASS + **1 SKIP** (pre-existing). **0 UNRELATED · 0 NEW FAILURES.** The run before the ten controls were realigned reported **10 failures**, all of them controls pinning the pre-construction state; that red run is reported, not erased (`§40`) |
| `P13` | `AUTHORIZED = FALSE` |
| Repository | `HEAD` `a0e96e2` → this commit; 0 files deleted |

---

## Governance invariants (`§47`)

| Invariant | Held by |
|---|---|
| `RATIFICATION ≠ CONSTRUCTION` | `R1` was applied, never re-read to suit the result |
| `CONSTRUCTION ≠ RUNNING SYSTEM` | the system was run, not merely built |
| `RUNNING SYSTEM ≠ R1 SATISFACTION` | it runs, and `E12-06` is still `NOT SATISFIED` |
| `R1 SATISFACTION ≠ P12 COMPLETION` | neither is claimed |
| `DEMONSTRATOR ≠ REAL SYSTEM WORK` | attribution made structural; demonstrator evidence kept and still identified |
| `PROVISIONED ≠ CONSUMED` | `P6` is provisioned and not consumed |
| `EXECUTED ≠ PROVEN` | the run's own return value proves nothing; the measurement reads the store from disk |
| `OLD EVIDENCE ≠ NEW EVIDENCE` | demonstrator stores untouched; new evidence in a new store |
| `RUNNING SYSTEM ≠ AUTONOMOUS SELF-ACTIVATION` | no daemon, scheduler, queue or self-activation; `OA-1` intact |
| `NO FRONTIER ≠ FRONTIER EXHAUSTED` | one frontier remains, and it is a decision |
