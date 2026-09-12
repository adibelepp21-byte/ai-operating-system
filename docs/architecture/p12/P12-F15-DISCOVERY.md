# P12 `F-15` — P6/P7 execution evidence · discovery & classification

> **Classification: `F15-C1` — FALSE POSITIVE.** The canonical requirement does
> not require the missing exercise in the present context.
>
> **No construction. No execution manufactured.** `historical rewrite = 0` ·
> `native_core changes = 0` · `P12 CONSTRUCTED = FALSE`.

---

## 1. Gate A — the canonical requirement, from the bodies

| Clause | What it actually says |
|---|---|
| `§46` | *"For every **phase**"* — a matrix with `EVIDENCE` and `VERIFICATION` columns; certification *"does not substitute for P12 integration verification"* |
| `§48` | *"A relationship is not considered verified merely because both surfaces exist"* |
| `§19` | thirteen minimum scope items, `CROSS-PHASE CONTRACTS` among them |
| **`§53`** | each E12 criterion *"must have canonical definition; measurable interpretation; evidence source; verification method"* — and **"No E12 criterion may be silently invented or treated as ratified before canonical reconciliation."** |

**`E12` is not ratified.** `E12-06` System-wide Verification therefore has **no
measurable interpretation**, and nothing in the canonical body establishes that
every phase must carry execution evidence *now*.

The inference the Act prohibits at `§12` —

```text
P6 exists + P7 exists + W6 covers P4–P11  ⟹  P6/P7 must be exercised
```

— is exactly the inference `F-15` needed, and the canonical body does not support
it. It **defers** the question to a ratification that has not occurred.

---

## 2. Gate B — P6 and P7, measured separately

| | `P6` Knowledge | `P7` Memory |
|---|---|---|
| Native Core boundary | present (`admission.py`, …) | present (`admission.py`, `candidate.py`, …) |
| Consumer agent | `consumers/knowledge_agent.py` — complete | `consumers/memory_agent.py` — complete |
| Runtime access path | `execution.runtime.knowledge`, RUNNING-gated | `execution.runtime.memory`, RUNNING-gated |
| **Resident non-test callers** | **zero** | **zero** |
| Trace consumption evidence | `knowledge_consumed` empty in every record | `memory_consumed` empty in every record |
| Provisioned by a real run | **yes** | **yes** |

Measured independently, not collapsed because both read `NOT EXERCISED`.

---

## 3. Gate D — falsification results

| | Hypothesis | Result |
|---|---|---|
| `H1` | P6 exercised but the verifier cannot see it | **PARTIALLY CONFIRMED** — see `§4` |
| `H2` | P7 exercised but invisible | **PARTIALLY CONFIRMED** — same shape |
| `H3` | evidence exists under another vocabulary | **FALSIFIED** — `knowledge_consumed`/`memory_consumed` are the only Trace fields for it, and `INV-6` requires *captured content*, not references |
| `H4` | demonstrator paths wrongly excluded | **FALSIFIED** — no demonstrator consumes knowledge or memory either |
| `H5` | canon does not require P6/P7 execution now | **CONFIRMED** — `§53`, E12 unratified |
| `H6` | real work crossed P6/P7 but failed to persist evidence | **FALSIFIED** — no work path constructs either agent, so no crossing occurred to go unrecorded |
| `H7` | dormant because no work has required them | **CONFIRMED** — the two resident work paths are a governance corpus health check and an artifact conformance verification; neither semantically requires knowledge admission or memory retention |

---

## 4. `H1`/`H2` — and an overclaim of mine, corrected

A real `AIOSRuntime` **provisions** `KnowledgeSubsystem` and `MemorySubsystem`
on every run, including the resident W1 work path. So the boundaries *are*
reached by real execution.

**My `W6` evidence document said P6/P7 had "never been crossed by any execution."
That overstates what was measured**, and it is corrected in place rather than
left standing:

```text
PROVISIONED  ≠  CONSUMED
```

The verifier measures **consumption**, because consumption is what the Trace
vocabulary records — and it reports exactly that in its evidence string
(*"`knowledge_consumed` is empty in every Trace record"*). The label was accurate;
my prose around it was not.

**The verifier was not changed.** Reporting `PROVISIONED` would require evidence
that provisioning occurred, and no execution-produced record carries it —
inferring it from the runtime's construction is precisely the inference this
programme refuses. Manufacturing such a record would be construction the
classification does not justify.

---

## 5. Gate H — demonstrator contamination

Not applicable in the direction expected: **no** crossing of P6/P7 exists to
classify, demonstrator or otherwise. `H4` was tested and falsified — even the
proofs consume neither.

---

## 6. Programme hypothesis — confirmed on two more surfaces

```text
CAPABILITY EXISTS → CONFORMANCE EXISTS → OPERATIONAL REACHABILITY ABSENT
```

`KnowledgeAgent` and `MemoryAgent` are complete, documented, conformance-tested,
and resolve their subsystems through the authorized RUNNING-gated path — with
**zero resident non-test callers**. That is the same shape as the Trace boundary,
the Trace store, and `WorkflowMonitor`.

**Five surfaces now.** The hypothesis was falsified as a universal claim by
`F-10′` (one work path does reach observation) and is confirmed again here for
the majority. It is retained as a systemic finding, still not promoted to a rule.

---

## 7. Why `C1` and not the alternatives

- **not `C2`** — nothing was misclassified; consumption genuinely never occurred.
- **not `C3`** — no work crossed P6/P7, so there is no missing evidence for a
  crossing that happened.
- **not `C4`** — a required integration is not established, so remediation is not
  authorized by necessity. `NECESSITY ≠ AUTHORITY`.
- **not `C7`** — this would license manufacturing work to produce evidence, which
  `§14` prohibits and which the canon does not require.
- **not `C5`/`C6`** — the immediate question is answerable from resident bodies.
  The *future* answer depends on E12 ratification, which is Founder-reserved;
  that is a known standing boundary, not a new block.

`NOT EXERCISED ≠ FAILED`, and `ABSENCE OF EXECUTION EVIDENCE ≠ EVIDENCE THAT
EXECUTION SHOULD HAVE OCCURRED`.

---

## 8. `F-13` — kept separate

Not merged. `F-13` concerns whether W5's observed population represents real
system work. `F-15` concerns whether two phases must be exercised at all. They
share the demonstrator/work distinction as *evidence*, and that is not identity.
`F-15`'s result does contribute one datum to `F-13`: even demonstrators do not
reach P6/P7, so the observed population's composition is not what keeps those
phases dormant.

---

## 9. Fresh rediscovery

| ID | Frontier | Status |
|---|---|---|
| `F-15` | P6/P7 execution evidence | **CLOSED — `C1` FALSE POSITIVE** |
| `F-16` | `E12` has no ratified measurable interpretation, so no phase-level completion criterion can be evaluated | **OPEN — FOUNDER-RESERVED.** `§53` reserves it; this office may prepare, not ratify |
| `F-14` | two work paths publish no observation | OPEN — non-blocking |
| `F-13` | work vs demonstration subjects in W5 | OPEN — narrowed |

**`F-16` is the real boundary this gate found.** Every remaining W6 question —
what counts as sufficient cross-phase evidence, whether provisioning counts,
whether dormant phases must be exercised — resolves to a measurable
interpretation of `E12-06` that only a Founder ratification can supply.

---

## 10. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 811 OK = 1888
citation 215 documents / 1155 citations / 0 errors · stale-state 510 / 0
changes: 2 documents corrected (my overclaim) · 0 code · 0 tests
historical rewrite 0 · p11 changes 0 · native_core changes 0
protected read 0 / staged 0 / committed 0 · Native Core 11
```
