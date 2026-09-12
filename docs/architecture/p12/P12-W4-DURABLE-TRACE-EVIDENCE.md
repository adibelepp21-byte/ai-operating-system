# P12-W4 — Execution Integration · durable Trace evidence

> **`P12 AUTHORIZED = TRUE` · `P12 CONSTRUCTED = FALSE`.** One increment, not a
> work package complete. Authorized by `§17` (Execution Integration) and `§10`.

---

## 1. The gap was not the one the code said it was

`derived_views` answered *"what has run"* and *"what has failed"* with `UNKNOWN`,
explaining that a Trace store is per-`StorageFacility` and no cross-process
registry exists. **Accurate, and incomplete.** Measured at entry:

```text
durable trace partitions on disk           0
constructions of LocalAppendOnlyStorage    0   outside its own definition
resident executions supplying a writer     0   TraceWriter is optional, None everywhere
```

**The Trace boundary was fully built, conformance-tested, and never fed.** A
registry alone would have enumerated an empty set and reported success — a guard
that passes because there is nothing to see. `ACT-CC-R1-SYSTEMIC-001` had found
the same shape once before: *"the Trace boundary complete and never called."*
R2-A supplied the call; nothing had ever supplied the **store**.

So two things had to land together: discovery, and a real execution that
produces something to discover.

---

## 2. What was built

**`tools/p12_trace_registry.py`** — discovery by filesystem shape. A store is a
directory holding a partition file. Reading is delegated entirely to the Native
Core `TraceReader`; this module parses no record itself, so it cannot become a
second Trace vocabulary. Native Core is untouched — `§11` expressly permits
integration layers outside the frozen boundaries.

**`p12_trace_durability_proof.py`** — at the repository root, because wiring a
real performer needs `consumers/` and `tools/` may not import that region. It
runs the **same real verification** the cross-Department proof runs —
`EngineeringIntelligenceAgent.verify` over `tools/w4_delegation.py` against the
`FD-P11-001 §13` criteria — with a `TraceWriter` over `LocalAppendOnlyStorage`.
The record is produced **by** the execution, not written **about** it.

---

## 3. The first thing the system could say about its own failures was mine

The store holds two records. The first is **my own crash**, from four minutes
before the second:

```text
status  : failure
outputs : {'error': "AttributeError: 'TracedAction' object has no attribute 'record'"}
skills  : ()          tools: ()
```

I had called a `record()` method that does not exist — the real API is
`used_skill` / `used_tool` / `produced`, with the single write on `__exit__`.
`TracedAction.__exit__` did exactly what its docstring promises: it wrote one
record, with status `failure`, and let the exception propagate.

**It has not been removed, and cannot be.** The facility offers no delete and no
edit by design, and `§13.8` forbids rewriting historical evidence to make current
state look clean. The second record is the successful run:

```text
status  : success
outputs : {'criteria': 14, 'satisfied': 14, 'unsatisfied': ()}
skills  : ('artifact-conformance-verification',)
tools   : ('tools/w4_delegation.py',)
```

Exactly one record per action, across two actions. A durability proof whose
first durable artifact is the author's own mistake is better evidence than a
clean one: nothing about it could have been staged.

---

## 4. Fresh-process verification (`§52`)

The store was read back by two **independent interpreters**, neither sharing
state with the writer:

```text
pid 4931 → stores 1 · records 2 · {'failure': 1, 'success': 1} · failures 1
pid 4932 → {'failure': 1, 'success': 1}
```

Durability survives the process boundary. That is the property `F-3` named and
nothing in the repository had ever demonstrated.

---

## 5. Self-model: `What failed?` is now answered from evidence

```text
BEFORE   8 VERIFIED · 2 INFERRED · 2 UNKNOWN
AFTER    9 VERIFIED · 2 INFERRED · 1 UNKNOWN
```

**`What is running?` remains `UNKNOWN`, deliberately.** A Trace record says what
*ran*, past tense; reading one back is not observation of a live process.
Answering `F-4` with `F-3`'s evidence would be exactly the substitution this
model exists to refuse, and a test now asserts the two answers differ.

**An empty registry returns to `UNKNOWN`, not to zero.** Absence of records is
not absence of failures, and reporting `0 failures` from `0 records` would be the
cleanest possible lie. `EmptyIsNotSuccess` proves it with a temporary empty root.

---

## 6. Two tests of mine were changed, and why that is not the forbidden thing

`test_runtime_questions_are_unknown_not_guessed` and the coverage threshold
asserted that *"What failed?"* is `UNKNOWN` and that at least **two** questions
are unanswered. Both were written earlier in this same session, and both failed
after `W4` landed.

**They were changed because the measured state changed, not to make an
implementation pass.** The invariant they protected is now enforced *harder*, in
`EmptyIsNotSuccess`, which proves the answer reverts to `UNKNOWN` the instant the
evidence is absent — a stronger claim than the original static assertion. The
coverage floor is `1` and is **not a target to drive to zero**: it falls only when
a question becomes answerable from real evidence.

---

## 7. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 756 OK = 1833
   tools +15 — durable-trace registry conformance
citation 206 documents / 0 errors · stale-state 504 / 0 stale assertions
region boundary: tools/ imports no consumers — proof wiring is at the root
Native Core 11 frozen · protected read 0 · staged 0 · committed 0
```

---

## 8. Frontier

`F-3` **closed** — durable Trace persistence exists, is discoverable, and
survives a fresh process. `F-1` further closed — 11 of 12 questions answered.
`F-4` **open and authorized**: runtime state is still unobserved from outside,
and that is the next `P12-W2` increment. `F-5`, `F-6` open. `F-7` external. `F-8`
reserved, no direct dependency proven. `F-9` untouched.

```text
P12 AUTHORIZED = TRUE   P12 CONSTRUCTED = FALSE   E12 NOT RATIFIED
P13 NOT AUTHORIZED      GOVERNANCE CLOSED = NO
```
