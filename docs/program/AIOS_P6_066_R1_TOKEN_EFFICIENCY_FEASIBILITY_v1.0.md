# `ACT-CC-P6-066-R1` — Repository Graph / Token Efficiency Feasibility

**Act:** `ACT-CC-P6-066-R1` · **Mutation:** this record only · **Construction: NONE**
**Result:** **MODERATE POTENTIAL — LOW for code, HIGH for the governance corpus**
**Executor:** AIOS Co-Founder

> **CONSTRUCTION: NONE · DEPENDENCY: NONE · GRAPHIFY: NOT ADOPTED · AIOS
> KNOWLEDGE: UNMODIFIED · T-12: UNMODIFIED · T12-D-004: UNMODIFIED · PROTECTED
> STATE: UNTOUCHED**

---

## 1. Executive result (§35.1)

**MODERATE POTENTIAL**, and the potential is **not where the Act assumed it
would be.**

```
Repository CODE graph        LOW POTENTIAL      — measured, §5
GOVERNANCE RECORD index      HIGH POTENTIAL     — measured, §6
```

[A] The Act framed the question as *repository* indexing. The measurements say
AIOS's token cost is **not** in its code. It is in its governance corpus — and
that is precisely where this program's two real retrieval failures occurred.

## 2. Governance register first (§4) [E]

Searched: `graphify` · `repository graph` · `repository indexing` · `code graph`
· `token efficiency` · `context optimization` · `developer tooling` — **all
return 0.** No instrument authorizes such tooling, and **none restricts it**.
Neutral ground, not prohibited ground (§4's own caution).

[E] `ACT-CC-P6-065`'s finding re-verified: the sole canonical Graphify mention
disclaims dependency and frames it as an out-of-scope **observation mechanism** —
which is exactly the category this Act explores.

## 3. What Graphify actually does (§7, §35.2) — source-level

[E] Measured across `s5` (337 Python files), by grep over source, not README:

| Mechanism | Files | Evidence |
|---|---|---|
| **tree-sitter** parsing | **42** | OBSERVED IN SOURCE |
| **networkx** graph | **69** | OBSERVED IN SOURCE |
| LLM layer | 47 | OBSERVED IN SOURCE |
| regex | 39 | OBSERVED IN SOURCE |
| Python `ast` | 4 | OBSERVED IN SOURCE |
| embeddings | 5 | OBSERVED IN SOURCE |
| SQL / sqlite | **0** | — |

[E] **A correction to my own first inference.** Seeing 47 LLM files, I inferred
extraction was LLM-driven. Reading `extract.py` directly disproved it:

> *"**Deterministic structural extraction** from source code using tree-sitter.
> Outputs nodes+edges dicts."*

[A] **The deterministic structural core is separable from the LLM layer.** That
distinction is the single most reusable finding here — an index can be built for
**zero** LLM tokens. Had I trusted the file count, I would have reported the
opposite.

[E] Persistence: **graphml / json**, no database. Incremental update: real —
`watch.py` carries 73 hash/mtime/changed hits. `llm.py` targets
Anthropic/OpenAI/Ollama/Gemini/Kimi at `max_tokens 16384`.

## 4. AIOS baseline — measured (§10, §11)

```
python  139 files      855,841 bytes    ~213,960 tokens  (est, bytes/4)
markdown 403 files   5,540,612 bytes  ~1,385,153 tokens  (est, bytes/4)
WHOLE REPO                            ~1,599,113 tokens  (est)
```

[A] **Markdown is 6.5× the code.** Any token-efficiency effort aimed at code is
optimising the small half.

[E] **Critically, the baseline is not "read everything."** Claude Code's actual
workflow here is targeted `grep` and one-off AST sweeps — the dependency-cycle
check run in every Act is already an ad-hoc graph query. Comparing a graph
against a *naive read-everything* baseline would have inflated the benefit; the
honest comparison is against grep.

## 5. Code graph — LOW POTENTIAL [E] measured

| | Tokens (est) |
|---|---|
| Naive index (paths repeated per node) | **70,487** — 33% of the code corpus |
| **Compact index** (interned file ids) | **20,768** — **9%** of the code corpus |
| One real symbol query by `grep` | **591** |
| Reading the 2 files the symbol lives in | 2,658 |

*(1,744 nodes · 635 edges, built and measured during this Act, then discarded.)*

[A] **The index costs ~35× a single grep query.** Break-even needs ~35 repeats of
the *same class* of query — and grep already returns the precise answer at 591
tokens, so the graph replaces nothing for symbol, import, or reference lookup.
Multi-hop queries (impact, transitive dependency) are the genuine case, and at
139 Python files a one-off AST script answers those for a few hundred tokens.

**§35.5 — measured, not estimated:**

| Query class | Baseline (measured) | Graph-assisted | Saving | Confidence |
|---|---|---|---|---|
| Symbol lookup | 591 | ~index amortised | **negative until ~35 queries** | HIGH |
| Import / dependency | ~600 | similar | negligible | HIGH |
| Impact / multi-hop | ~200 (AST script) | lower per query | small, real | MEDIUM |
| Cross-file trace | varies | lower | small, real | LOW |

## 6. Governance index — HIGH POTENTIAL [E] measured

```
GOVERNANCE RECORD INDEX   176 records   28,566 bytes   ~7,141 tokens (est)
  vs markdown corpus ~1,385,153 tokens   ->  0.5%  (≈194:1 compression)
```

[E] Built during this Act (identifiers, dates, cross-references per record), then
discarded. [E] For scale: the Governance Decision Register **alone is ~55,047
tokens** and has been re-grepped in most recent Acts.

[A] **This is the finding that matters, and it is self-implicating.** Both
retrieval failures in this program — missing `DEC-PHASE5-SEMANTICS` in
`ACT-CC-P6-060`, missing `GDR-0028` in `ACT-CC-P6-061` — were **markdown
supersession failures**, not code failures. A 7K-token index carrying
*identifier → record → date* would have surfaced both: each superseding record
was **one day newer** than the one I relied on.

[A] The break-even here is not 35 queries. **It is one avoided Act.**

## 7. Costs, break-even, accuracy (§17, §18, §19, §35.6–§35.8)

```
INITIAL INDEX COST:      code ~20.8K tokens · governance ~7.1K tokens (both measured)
ONGOING MAINTENANCE:     hash/mtime incremental — feasible (Graphify demonstrates it)
STORAGE:                 json/graphml, no database
QUERY COST:              lower than grep only for multi-hop
STALE-GRAPH RISK:        HIGH for code (changes every commit) · LOW for governance
                         (append-only records; supersession is additive)
IMPLEMENTATION COMPLEXITY: LOW for governance index · MEDIUM for code graph
BREAK-EVEN — code:       ESTIMATED ~35 same-class queries; likely never reached
BREAK-EVEN — governance: ESTIMATED one avoided mis-conclusion
```

[E] **§16 honoured — no benchmark is claimed.** Graphify was **not executed**
against AIOS. Index sizes and query costs above are **MEASURED** on this
repository by scripts written here; token figures are **ESTIMATES** (bytes ÷ 4)
and labelled as such throughout.

[A] **Accuracy risks (§19):** a code graph goes stale every commit and misses
dynamic imports, reflection and runtime registration — though AIOS forbids those
in `native_core`, which *reduces* the risk and simultaneously reduces the need.
The governance index carries the opposite profile: records are append-only, so
staleness is additive and detectable.

[A] **§21/§22 boundary, non-negotiable:** such an index records that
*"`ADR-0016` cites `DEC-P6-038`"*. It **never** establishes that `DEC-P6-038`
authorized anything. It is **evidence of relationship, not authority** — the
exact inversion `ACT-CC-P6-056` measured and refused.

## 8. Options (§26, §27, §35.9)

| Option | Token benefit | Accuracy | Complexity | Maintenance | Governance risk | Recommendation |
|---|---|---|---|---|---|---|
| **A** No graph | baseline | high | none | none | none | viable — status quo works |
| **B** Lightweight index *(governance-scoped)* | **HIGH** | high | low | low | low | **RECOMMENDED** |
| **C** Full repository graph | low | medium | high | high | medium | not justified at 139 files |
| **D** Hybrid | low-medium | medium | high | high | medium | premature |
| **E** External Graphify tool | unknown | unknown | low | external | **licence + supply chain** | research only |

## 9. Recommendation (§35.10, §35.11)

```
RECOMMENDATION:        LIGHTWEIGHT INDEX — scoped to governance records, not code
DIRECT ADOPTION:       NONE
PATTERNS WORTH ADAPTING: deterministic tree-sitter-style extraction separated from
                         any LLM layer · json/graphml export · hash-based incremental
CODE REUSE:            NONE
DEPENDENCY:            NONE
```

[A] Scoped to `docs/` records; owned as **tooling**, alongside
`tools/runtime_catalog.py` and the validators — the role canon already assigns to
observation mechanisms (`ACT-CC-P6-065` §3). **Never** inside `native_core`.

[A] `ACT-CC-P6-065` §5 flagged licence divergence across the five sources (MIT vs
Apache-2.0 under one claimed identity; one declaring MIT with no `LICENSE`
shipped). **Adapting a pattern raises none of that; copying code would.**

## 10. Boundaries (§35.12, §35.14)

```
AIOS Knowledge modified: NO    T-12 modified: NO    T12-D-004 modified: NO
Phase 6 construction:    NO    Protected packages modified: NO
Created: this record only      Modified files: 0     Dependencies added: 0
```

[E] The five archives were extracted to the session scratchpad **outside the
repository**. The two indices were built in memory, measured, and **discarded** —
neither was written to the tree.

## 11. Future decision (§35.13)

```
FUTURE DECISION REQUIRED: YES
QUESTION:  Should AIOS authorize a governance-record index as repository tooling?
PROPOSED SCOPE: read-only index over docs/ — identifier, path, date,
                cross-reference, supersession edges; json output; hash-based
                incremental; resident in tools/; evidence only, never authority
NOT AUTHORIZED BY THIS ACT: implementation
```

[R] I recommend it, and I am the interested party: it would have caught two of my
own errors. That is a reason to weigh it carefully, not a reason to adopt it.

**DEVIATIONS: NONE.**
