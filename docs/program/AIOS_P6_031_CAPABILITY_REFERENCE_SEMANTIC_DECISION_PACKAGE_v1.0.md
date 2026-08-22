# AIOS — Capability Reference Semantic Decision & Post-Readiness Frontier Package v1.0

**Act:** `ACT-CC-P6-031` · **Program:** AIOS Genesis
**Phase:** `P6-AES-01 — Agent Execution Semantics`
**Predecessor:** `ACT-CC-P6-030` · **Predecessor decision:** `DEC-P6-030` — ACCEPT — NOT READY / CONSTRUCTION DEFERRED
**Executed by:** Co-Founder office — Construction Phase, under scoped §3.2 delegation `DEL-T4.4-CF-001`
**Constitutional authority:** NONE
**Mode:** READ-ONLY
**Construction:** NONE · **Mutation:** NONE (this package only) · **Commit:** NONE · **Synchronization:** NONE · **Persistence:** NONE
**Date:** 2026-08-23

---

## 1. Status

[E] **`DEC-P6-031` is DECIDED** — §30's Founder Authorization Block arrived
filled, signed *"Founder / Architect: Moriarty."*, `Status: DECIDED`, with
`Founder Decision: DEFERRED TO SEPARATE FOUNDER DECISION`. That is **§32
Outcome D**.

[A] **The distinction this office applied.** §20's *"Recommended minimal decision
form"* and its *"stronger recommendation"* are labelled recommendation. §30 is
the authorization block itself, unlabelled as recommendation and marked DECIDED.
**§30 is treated as the decision; §20 as advice.** This is the same test under
which this office declined, three times across `ACT-CC-P6-030`'s issuances, to
promote a block labelled *"Recommended … fill"* into a decision.

[A] Per **§4**, every finding below is established from source. Predecessor
findings — including this office's own — are verification targets. **No
predecessor statement is promoted merely because it appeared in `ACT-CC-P6-030`.**

### 1.1 Disclosure — a defect in this office's own verification tooling

[E] The first `§15` inspection script raised
`SyntaxError: f-string expression part cannot include a backslash` and produced
no result. The defect was in this office's script, not in the repository. It was
corrected and re-run. **Disclosed rather than quietly repeated.**

---

## 2. §7 / §8 — The two settled gates, re-verified

### 2.1 Capability self-execution — FORBIDDEN BY CANON

[E] Freeze §4, Capability entity: *"**Forbidden** [E]: **executing itself**;
cross-Department dependency without governance (INV-10); existing with zero
implementers as a steady state (INV-14)."* · `capability_spec §5`: *"Exposes
**no** capability to execute itself (Freeze §4)"* · `§8`: *"Must not execute
itself"* · `§9`: *"not an actor and authors no Trace."*

[E] AST: the Capability package holds **40 defs and zero execution primitives**.

[A] **Not reopened.** Per §7 it stays outside this Act's decision alternatives.

### 2.2 Agent → Capability invocation — EXCLUDED FROM PHASE

[E] `DEC-P6-029` issuance 4 and `DEC-P6-030` determination 6.

[A] Held **distinct** from the reference question throughout. `Reference ≠
Invocation`: a decision that a reference exists would not authorize invocation.

---

## 3. §14 / §15 — What the source actually carries

### 3.1 The Agent boundary — nine inspection targets

[E] AST over `native_core/core/agent/` excluding tests:

| §15 target | Finding |
|---|---|
| Capability imports | **0** — complete import set: `..runtime.execution.consumer` · `.agent` · `.definition` · `__future__` · `dataclasses` · `typing` |
| Capability constructor parameters | **0** — the only methods in the package are `AgentDefinition.__post_init__(self)` and `AgentInstance.__post_init__(self)`. **`Agent` has no methods at all** |
| Capability fields | `AgentDefinition.implemented_capabilities: Tuple[str, ...]` — **string keys, not Capability objects** |
| Resolver references | **0** |
| Graph references | **0** — zero code-line occurrences of `Graph` |
| Ownership references | `owning_department_key: str` — a plain key, not a resolution |
| Runtime Capability handles | **0** |
| Invocation methods | **0** — zero code-line occurrences of `invoke` or `execute` |
| Execution-context Capability state | **0** — `ExecutionContext` carries `runtime_id`, `execution_sequence` |

[A] Reported in §15's required form:

```
No currently realized semantic route from Agent execution to Capability.
```

[A] **Not** *"Capability reference prohibited."* §15 requires the distinction and
§10 forbids the inference.

### 3.2 `implemented_capabilities` — the distinction holds

[E] The source **continues to support** the §14 distinction. `implemented_capabilities`
is a **data-bearing declaration**: a tuple of plain strings on an immutable
dataclass, in a module importing only `__future__`, `dataclasses`, `typing`.
It is **not** binding, **not** resolution, **not** invocation, **not** execution.

---

## 4. Finding — a prior Founder decision already governs this reference, at one layer

[A] §4 requires inspecting *"existing governance decisions."* Doing so surfaced
one that bears directly on this gate and was not carried by the Act.

[E] `native_core/core/agent/definition.py`, verbatim:

> *"`implemented_capabilities` followed under `ACT-CC-F03-040`
> (`DEC-AGENT-FACTORY-INV2-CLAUSE2 = OPTION A`), carrying **INV-2 clause 2**.
> That clause *was* genuinely behind the reservation: a Definition declaring
> which Capabilities it implements is the *"validated against Capabilities"*
> surface the Agent Factory reserves. **The Founder opened exactly that, and
> nothing else** — the reservation stands over governed **creation, registration
> and lifecycle** of Definitions, which remain unbuilt and unrepresented here."*

> *"**What this contract does and does not assert.** It fixes that a Definition
> declares **at least one** Capability, which is the whole of INV-2 clause 2 as
> stated. Whether those Capabilities *exist*, and whether every Capability has an
> implementer (INV-14), are corpus-level facts invisible to a single Definition —
> they are **reconciled by a caller that can see both sides**, exactly as
> ownership is."*

[E] `docs/program/AIOS_DEC_AGENT_FACTORY_INV2_CLAUSE2_v1.0.md`: **`OPTION A —
AUTHORIZE`**, provenance *"Founder Decision supplied in the `§4` block of
`ACT-CC-F03-040`."*

### 4.1 What this settles, and what it does not [A]

```
Agent DEFINITION layer  →  Capability reference EXISTS, by Founder decision.
                           Form: identity-only declaration.
                           Reconciliation: caller-mediated, both-sides.
                           Opened "exactly that, and nothing else."

Agent EXECUTION layer   →  NOTHING is established. The decision is silent.
```

[A] **This does not close §9's question, and must not be read as closing it.**
`DEC-AGENT-FACTORY-INV2-CLAUSE2` decided a **Definition-layer** declaration
surface. `ACT-CC-P6-031` asks about **Agent execution semantics**. Treating the
first as answering the second would be exactly the layer-collapse §5 and §6
forbid.

[A] What it does supply is precision: the reference is not an open question at
every layer. It is **decided at the Definition layer and undecided at the
execution layer** — which sharpens §12's test below.

---

## 5. §17 — `P7-L-1`, verified without expansion

[E] Resolution *primitives* do exist — in the **Capability** boundary:

| Method | Signature | Holds Agent data? |
|---|---|---|
| `CapabilityGraph.implementers_of` | `(capability_key, declarations)` | **No** — declarations passed in as an argument |
| `CapabilityGraph.unknown_implemented_capabilities` | `(declarations)` | **No** |
| `OwnershipGraph.owner_of_agent_definition` | `(agent_definition_key)` | **No** — key passed in |
| `OwnershipGraph.resolve_agent_definitions` | `(declarations)` | **No** |

[E] `CapabilityGraph.__init__(self, capabilities: Iterable[Capability])` — the
graph is built from Capabilities **only**. It never holds Agent Definitions.

[A] **These are caller-mediated query functions, not a binding.** Neither graph
imports Agent; the Agent boundary cannot import either. Reconciliation is
performed by a third party holding both sides — the same pattern the
`DEC-AGENT-FACTORY-INV2-CLAUSE2` docstring describes for ownership.

[A] **`P7-L-1` is not expanded.** Its reservation is over *"governed creation,
registration and lifecycle"* of Definitions and Instances — Agent Factory,
bootstrap, binding. The Capability-side query methods are outside that
reservation, exist, and are tested. This office asserts **no** `CapabilityGraph`
binding, **no** `OwnershipGraph` binding, **no** Agent Factory, **no** bootstrap
from the existence of plain identifiers.

### 5.1 A refinement to this office's earlier `P7-L-1` observation

[A] In `ACT-CC-P6-030` this office recorded that `P7-L-1`'s evidence sentence —
*"no factory, registry, ownership, or capability identifier"* — is stale, since
both identifiers now exist. **That stands.** This Act adds the reason it does
not disturb the disposition:

[E] `definition.py` enforces INV-2 clause 2 **locally** — a Definition must name
at least one Capability (*"implemented_capabilities must name at least one
Capability"*). What it cannot do is verify those keys name **real** Capabilities
owned by **real** Departments; that is `unknown_implemented_capabilities` and
`resolve_agent_definitions`, both unreachable from the Agent boundary.

[A] So `P7-L-1`'s core claim holds exactly: **INV-2 is not verifiable at the
Agent boundary.** Per §18, this is recorded as a **DOCUMENTATION ACCURACY
FINDING** and **not silently corrected**. Finding Register hash unchanged:
`1eeb99a67f019270`; `git diff` on it empty.

---

## 6. §16 — Runtime boundary: exactly what `Execution` exposes

[E] `Execution` (ABC) declares **two** abstract properties: `runtime`,
`context`. Nothing else.

| §16 distinction | Exposed by `Execution`? |
|---|---|
| Runtime identity | **YES** — via `execution.runtime` and `context.runtime_id` |
| Execution ordinal | **YES** — `context.execution_sequence` |
| Context | **YES** — `execution.context` |
| **State** | **NO** — no execution state model exists |
| **Authorization** | **NO** — `_require_running` gates `create_context` and `knowledge` on **Runtime**; `Execution` exposes no authorization surface |
| **Capability reference** | **NO** |
| **Capability binding** | **NO** |

[A] **No semantic property was promoted solely because an object exists**, per
§16's closing rule.

---

## 7. §9 — The three classifications, tested and not selected

### 7.1 R-A — Reference Required · §11 test

[A] §11 requires evidence that Agent execution semantics **necessarily depend
on** Capability reference. **No such evidence exists.** Freeze §4's Agent
Instance *Allowed* list is enumerated — *"act… use Skills/Tools; consume
Knowledge; write scoped Memory"* — and does not include Capability. INV-2 binds
the **Definition**, which Freeze §4 forbids from acting. `participate`'s sole
parameter exposes `runtime` and `context`.

[A] Per §11, the mere existence of `implemented_capabilities` is insufficient —
and §4 above shows it was authorized for a **different layer**.

```
R-A: NOT SUPPORTED BY EVIDENCE — not recommended.
```

### 7.2 R-B — Reference Optional · §12 test

[A] §12 requires six distinctions be identified. **They are establishable at one
layer and not the other** — and §12 forbids fabricating the missing half:

| §12 distinction | Definition layer | **Execution layer** |
|---|---|---|
| What is referenced | Capability keys | **not established** |
| At what layer | Agent Definition | **not established** |
| Identity-only? | **YES** — plain strings | **not established** |
| Implies binding? | **NO** | **not established** |
| Implies resolution? | **NO** — caller-mediated | **not established** |
| Implies invocation? | **NO** | **not established** |

```
R-B: NOT ESTABLISHABLE AT THE EXECUTION LAYER — not recommended.
```

[A] This is a **sharper** negative than "cannot be established": the six
distinctions are answerable where a Founder decision already exists, and
unanswerable where none does. That asymmetry is itself the evidence.

### 7.3 R-C — Reference Prohibited · §13 test

[A] §13 requires explicit authority — constitutional prohibition, frozen rule,
prior Founder decision, or a decision issued through this Act. **None exists.**
No canonical text prohibits an execution-layer Capability reference.

[A] Per §13 and §15, **absence of implementation is not sufficient**, and this
office does not treat the missing route as a prohibition.

```
R-C: NO SUPPORTING AUTHORITY — not recommended.
```

### 7.4 §10 — no fourth inference

[A] No fourth classification was introduced. Neither forbidden inference was
made:

```
implemented_capabilities exists   →  therefore required   ✗ NOT MADE
participate() cannot reach it     →  therefore prohibited ✗ NOT MADE
```

---

## 8. §19 — Decision matrix, completed from source

| Gate | Question | Result |
|---|---|---|
| **C-01** | Runtime boundary preserved? | **YES** — `Agent → participate → Execution → runtime`; public surface unchanged |
| **C-02** | Capability self-execution forbidden? | **YES** — Freeze §4; 0 primitives |
| **C-03** | Capability invocation excluded? | **YES** — `DEC-P6-029` issuance 4; `DEC-P6-030` determination 6 |
| **C-04** | `implemented_capabilities` realized? | **YES** — `Tuple[str, ...]`, identity-only, `DEC-AGENT-FACTORY-INV2-CLAUSE2 = OPTION A` |
| **C-05** | Agent semantic route to Capability exists? | **NO — no currently realized semantic route** (§3.1). Per §19's own note, **this does not imply C-06 = PROHIBITED** |
| **C-06** | Capability reference canonically specified? | **NO at the execution layer.** YES at the Definition layer, by prior Founder decision — §4 |
| **C-07** | Capability binding specified? | **NO** — no binding mechanism anywhere |
| **C-08** | Capability resolution specified? | **NO for Agent execution.** Caller-mediated query primitives exist Capability-side and are unreachable from Agent — §5 |
| **C-09** | Capability reference decision available from canon? | **NO** — R-A, R-B and R-C each fail their evidence test |
| **C-10** | Founder decision required? | **YES** |

---

## 9. §30 — `DEC-P6-031`, recorded

[E] Received filled and signed:

```
Founder Decision:           DEFERRED TO SEPARATE FOUNDER DECISION
Capability Invocation:      EXCLUDED FROM P6-AES-01
Capability Self-Execution:  FORBIDDEN BY CANON
Construction:               NOT AUTHORIZED
Phase:                      P6-AES-01 — Agent Execution Semantics
Authority:                  Founder / Architect: Moriarty.
Date:                       2026-08-23
Status:                     DECIDED
```

[A] **§32 Outcome D.** The decision matches what the evidence supports at C-09
and C-10 — but it is **the Founder's act, separately attributable**, not an
adoption of this office's finding. Per §36 item 6, that attribution is what
completeness requires.

### 9.1 `DEC-P6-030` restatement — an expansion recorded

[E] The message restates `DEC-P6-030`. Compared with the version this office
recorded at `ACT-CC-P6-030 §15`, the Authority Boundary is **expanded from four
authorities to six**:

| Recorded previously | Restatement adds |
|---|---|
| Construction · Mutation · Commit · Synchronization — all NONE | **Capability Binding Authority: NONE** · **Agent Factory Authority: NONE** |

[E] It also carries eleven numbered Founder Determinations, of which three were
not in the earlier text: **10** — *"`ACT-CC-P6-031` may be issued only as a
separate Founder-authorized readiness/remediation instrument. Its issuance does
not constitute construction authorization."* **11** — *"Any future Construction
Candidate determination requires a new readiness verification and explicit
Founder disposition."* And **8** states the deferral in the same terms §30 now
decides.

[A] **Recorded as an expansion, not a substitution.** Nothing in it reverses the
version previously recorded; both point the same way, and the expansion tightens
two authorities this office had noted were unnamed.

---

## 10. §23 — Readiness reassessment

[A] §23's binding rule: *"No condition may become MET merely because a Founder
decision exists."* Applied strictly.

| Readiness condition | Before `DEC-P6-031` | After |
|---|---|---|
| Capability semantic status | NOT MET | **NOT MET** — see §10.1 |
| Failure semantics | NOT MET | NOT MET |
| Rejection semantics | NOT MET | NOT MET |
| Termination semantics | NOT MET | NOT MET |
| Evidence semantics | NOT MET | NOT MET |
| Execution state | NOT MET | NOT MET |
| Authorization semantics | NOT MET | NOT MET |
| Remaining readiness dependencies | NOT MET | NOT MET |

```
Matrix unchanged:  10 MET / 8 NOT MET
Readiness:         NOT READY
```

### 10.1 Why DEFERRED does not close the condition [A]

[A] **A deferral is a disposition, not a resolution.** `DEC-P6-031` establishes
*who decides and when* — it does not establish *what the reference means*. The
readiness condition asks for the latter. It therefore remains **NOT MET**, and
this office does not mark it satisfied on the strength of the decision's
existence.

[A] What changed is attribution, not readiness: the question moved from *an open
finding recorded by this office* to *a Founder-controlled deferral*.

---

## 11. §24 / §25 — Ladder position and prohibited transitions

[A] **§24 ladder — position unchanged:**

```
STATE A   Semantic question unresolved          ← CURRENT
STATE B   Semantic disposition established
STATE C   Readiness candidate
STATE D   Construction authorization candidate
```

[A] **Outcome D does not advance the ladder.** §32 states it as *"no semantic
commitment → no construction → NOT READY remains → separate Founder decision
required."* The Act remains at **STATE A**, with the deferral now formally
attributable to a Founder act rather than standing as an open finding.
`STATE A → STATE D` did not occur and cannot.

[E] **§25 prohibited transitions — none occurred:**

| Transition | Occurred |
|---|---|
| `implemented_capabilities` → Capability binding | ❌ NO |
| Capability identifier → Capability resolution | ❌ NO |
| Capability reference → Capability invocation | ❌ NO |
| Founder decision → Class H | ❌ NO — Class H stays EMPTY |
| PASS regression → construction authorization | ❌ NO |
| Phase existence → implementation permission | ❌ NO |
| Assigned successor → successor execution | ❌ NO |

---

## 12. §26 / §27 — Regression and governance preservation

[E] Verified at execution:

```
HEAD                          bb600ef = origin/claude/aios-genesis-planning-hmbvlc
Protected-tree diffs          empty  (native_core, tools, docs/architecture,
                                      docs/engineering, docs/constitution)
Finding Register diff         empty
native_core                   601 OK  (expected failures = 1)
tools                          49 OK
```

[E] Protected hashes unchanged — Constitution `b73723f8af91ef7a` · Freeze
`b8e7b8d105d93863` · Domain Model `6e273f12f79c3b2f` · Finding Register
`1eeb99a67f019270`.

[A] Per §26, **regression evidence is non-constitutive.** Passing tests
authorize no construction, resolve no semantic question, override no Founder
authority, and create no persistence authority.

[A] Per §27, one inconsistency was found and **reported rather than silently
reconciled**: the `P7-L-1` documentation-accuracy finding at §5.1.

---

## 13. §31 — Stop conditions

| # | Condition | Result |
|---|---|---|
| 1 | Canonical contradiction found | **CLEAR** — §4 is a layer distinction, §5.1 is documentation accuracy |
| 2 | Protected finding needs modification | **CLEAR** — reported, hash unchanged |
| 3 | Capability Reference determinable only by inference | **CLEAR** — not determined at all; §30 disposed of it by Founder act |
| 4 | Founder decision required but unavailable | **CLEAR** — required (C-10) and **supplied** at §30 |
| 5 | Construction authority implicitly triggered | **CLEAR** |
| 6 | Class H promoted without gate | **CLEAR** — EMPTY |
| 7 | Capability invocation entering scope | **CLEAR** — excluded and held distinct |
| 8 | Capability execution surface to be created | **CLEAR** — 0 primitives |
| 9 | Agent Factory to be introduced | **CLEAR** |
| 10 | Persistence authority to be inferred | **CLEAR** |
| 11 | Automation/hook substituting for Founder authority | **CLEAR** — §14.1 |
| 12 | Successor executed without issuance | **CLEAR** — none assigned |

**Zero of twelve triggered.**

---

## 14. §33 — Accounting

```
Source changes                    0
Canonical mutations               0
Governance mutations              0
participate() implementations     0
Capability execution primitives   0
Capability bindings created       0
Capability invocations created    0
Agent Factory created             0
Construction Acts prepared        0
Construction authorized           0
Class H promotions                0
Founder decisions inferred        0
Commits                           0
Pushes                            0
Synchronization                   0
```

[A] Files: **1 created** — this package. No deviation from §33's expected
values.

### 14.1 §29 — Automation boundary

[E] §29: *"No hook, urgency signal, test result, working-tree condition, or
external request constitutes authorization."*

[A] Automated commit requests were received during this Act and were
**declined**, on Engineering Constitution §6.2 invariant 2 and on §28/§29. This
office did not decide for the Founder, infer semantic authorization, infer
construction authority, infer Capability Reference status, mutate canonical
governance, prepare a Construction Act, commit, or synchronize.

---

## 15. §28 — Persistence firewall

[E] Actual state, represented truthfully:

```
GDR-0028                             UNCOMMITTED  (243 insertions / 0 deletions)
DEC-P6-029 / P6-AES-01 package       UNTRACKED
DEC-P6-030 / P6-030 package          UNTRACKED
DEC-P6-031 / this package            UNTRACKED
Persisted repository state           bb600ef
```

[A] **Four signed Founder decisions now exist only in this container's working
tree** — the T-12 scoped ratification (`GDR-0028`), the `P6-AES-01` boundary
(`DEC-P6-029`), the readiness disposition (`DEC-P6-030`), and this deferral
(`DEC-P6-031`). **Persistence Authority: NONE.** Per §28, persistence requires
*"a separate explicit, path-specific Founder authorization."* Recorded as fact,
not as a request.

---

## 16. §35 — Final state

```
Phase:                      P6-AES-01 — FORMALLY ESTABLISHED
Classification:             CLASS C — FORMAL PHASE ESTABLISHED /
                            CONSTRUCTION DEFERRED
Readiness:                  NOT READY            (10 MET / 8 NOT MET, unchanged)
Ladder position:            STATE A — deferral now Founder-attributable

Capability self-execution:  FORBIDDEN BY CANON (Freeze §4)
Capability invocation:      EXCLUDED FROM P6-AES-01
Capability reference —
  Definition layer:         DECIDED — identity-only declaration,
                            caller-reconciled (DEC-AGENT-FACTORY-INV2-CLAUSE2
                            = OPTION A). "Opened exactly that, and nothing else"
  Execution layer:          DEFERRED TO A SEPARATE FOUNDER DECISION (DEC-P6-031)
Capability binding:         NOT ESTABLISHED
Capability resolution:      NOT SPECIFIED for Agent execution; caller-mediated
                            primitives exist Capability-side, unreachable from Agent

Class H:                    EMPTY
Construction Target:        NONE ELIGIBLE
Construction:               NOT AUTHORIZED
Mutation / Persistence /
  Commit / Synchronization: NONE
Capability Binding /
  Agent Factory Authority:  NONE

C-01 / P7-L-1 / P7-O-1 /
  P7-O-2 / D-001…D-006:     PRESERVED
RU-5:                       OPEN — undischarged
Documentation finding:      P7-L-1 evidence sentence stale (§5.1) — reported,
                            not corrected
Successor:                  NONE ASSIGNED — §34
DEC-P6-031:                 DECIDED — Founder / Architect: Moriarty, 2026-08-23
```

[E] The two critical invariants, both held:

> *"The existence of `implemented_capabilities` does not authorize a semantic
> relationship between Agent execution and Capability."*
> *"The absence of a current semantic route does not authorize declaring that
> relationship prohibited."*

---

## 17. §34 / §36 — Successor and completion

[A] **§34 — no successor is inferred.** None was assigned by `DEC-P6-031`, and
none is inferred from readiness failure, automation, recommendation, test result
or existing reservation.

```
Successor = NONE ASSIGNED
```

[A] **§36 completion rule — ten of ten satisfied:** Capability Reference
independently re-verified (§3, §7) · invocation remains excluded (§2.2) ·
self-execution remains forbidden (§2.1) · binding and resolution distinguished
from reference (§5, §8) · no semantic status inferred (§7.4) · the Founder
decision is separately attributable (§1, §9) · readiness reassessed (§10) · no
construction transition (§11) · no canonical mutation (§12) · persistence
governed by explicit authority (§15).

**`ACT-CC-P6-031` is complete. STOP.**
