# AIOS Decision Review Methodology — External Corpus Validation: Letta (formerly MemGPT) v1.0

**Program:** External Repository Validation Program — Repository #4.
**Executes:** `AIOS_DECISION_REVIEW_METHOD_VALIDATION_PLAN_v1.0`.
**Corpus item:** `lettamain.zip`. Predecessors: DSPy (#1, different-domain), LangChain (#2, execution-overlap), OpenHands (#3, governance-adjacent).
**Status:** External-evidence review only. Additive. Creates no canonical document, modifies none, redesigns nothing, implements nothing, promotes no principle, makes **no adoption decision** (directive). Does not copy Letta design, API, folder structure, or implementation.
**Authority posture:** Letta is **external evidence, not authority** (Validation Plan §2). Predecessors used **only as methodology comparators**, never as authority.
**Methodology discipline:** DR-0…DR-6 applied **unchanged**. Weaknesses recorded as candidate refinements **[O]**, never enacted, never promoted.
**Directive structure:** Stage 1 Identification · Stage 2 Extraction · Stage 3 Comparison (Already Present / Different but Compatible / Observe / Reject / Not Applicable) · Stage 4 Method Evaluation. **No synthesis** (directive).
**Confidence:** **[E]** evidenced · **[A]** assumption · **[O]** open question. Single reviewer → reviewer-independence **[O]**, reserved to Architect (Plan §9).

---

## 0. Framing — The Apex of the Domain Gradient

[E] The corpus was walked along a deliberate adjacency gradient: DSPy (different domain) → LangChain (execution-overlap) → OpenHands (governance-adjacent) → **Letta, which occupies AIOS's *home domain* directly: long-term memory, knowledge representation, agent identity/persistence, and context management.** Letta's stated purpose — "advanced memory that can **learn and self-improve over time**" — is the exact subject matter of AIOS's Memory and Knowledge entities and the inv-8 promotion boundary.

[E] **This makes Letta the maximum-leakage, maximum-false-cognate corpus, and the sharpest test of the method.** Letta reuses nearly every AIOS entity *name*: `Memory`, `Block` (≈ a knowledge unit), `Identity`, `Organization`, `Source`, `Trace`, `Agent`, `Step`. Each is a live collision. I fix this before judgment (PR-1) and do **not** treat AIOS as the baseline Letta is scored against — Letta is evidence.

[E] **The single most important framing fact:** Letta and AIOS take **opposite stances on the same axis.** Letta's memory is **agent-self-edited and autonomously self-improving**; AIOS's core invariant (inv 8) is that **Memory→Knowledge promotion is *never* automatic** and requires human-governed review. Letta is not "weaker" — it optimizes for **autonomous adaptivity**; AIOS optimizes for **governed accountability**. Same domain, inverted philosophy. This inversion, not any single mechanism, is the review's central evidence.

---

## STAGE 1 — Identification

| Attribute | Value | Evidence |
|---|---|---|
| Package | `letta` **v0.16.8** (formerly MemGPT) | `pyproject.toml`, `README.md` |
| Self-description | "Create LLM agents with long-term memory and custom tools"; "advanced memory that can learn and self-improve over time" | `pyproject.toml`, `README.md` |
| Scope of *this* repo | **Legacy Letta server** (the API server behind the Letta V1 API/SDKs). README states active development **moved** to the separate `letta-code` repo; self-hosting now via a separate App Server. | `README.md` |
| Language / runtime | Python `>=3.11, <3.14` | `pyproject.toml` |
| License | Apache | `pyproject.toml` |
| Scale | 536 `.py` files, ~116,986 LOC — **largest corpus repo** | `find … | cat | grep -c` |
| Tests | 93 `test_*.py` | `find` |
| Persistence | SQLAlchemy 2 (async) + Alembic; **pgvector** (postgres) or **sqlite-vec** (sqlite) for archival-memory embeddings | `pyproject.toml` |
| LLM boundary | `letta/llm_api/*_client.py` + `letta/schemas/providers/*` per vendor (anthropic, azure, bedrock, deepseek, fireworks, gemini, …) | `letta/llm_api/`, `schemas/providers/` |
| Key data entities | `Block`, `Memory`, `Passage`, `Archive`, `Message`, `Conversation`, `Identity`, `Organization`, `Agent`, `Source`, `Step`, `Run`, `Job`, `ProviderTrace` | `letta/schemas/`, `letta/orm/` |

[E] **What exists in the repo:** the full legacy memory server — schemas, ORM (SQLAlchemy), per-entity service managers (`block_manager`, `archive_manager`, `passage_manager`, `identity_manager`, `agent_manager`, `source_manager`, `memory_repo`), memory-editing tool functions, LLM API clients, and a FastAPI server.
[E] **What does NOT exist here (boundary honesty, DR-1):** the *current* Letta agent (moved to `letta-code`) and the new App Server are **not in this zip**; findings describe the **legacy V1 server** only, and I do not extrapolate to Letta's current architecture.

[E] **Parity governance-term scan.** No `governance`/`promotion`/`ratif*` layer. The only governance-adjacent constructs are: `RequiresApprovalToolRule` (HITL tool approval), `block_history` (memory-edit versioning), and "Audit fields" (created_by/updated_by ORM metadata). **Fragments, not a unified governance model** — and, uniquely, they sit *inside AIOS's home domain*, which is what makes them cognates rather than unrelated.

---

## STAGE 2 — Extraction (objective; no judgment; Letta-native vocabulary)

### 2.1 Memory architecture — tiered, OS-analogy (the MemGPT core)
[E] Memory is tiered by *proximity to the context window*:
- **Core memory** — in-context, always present. `Memory` (`schemas/memory.py`) = a list of `Block` objects labeled by section (e.g. `human`, `persona`), plus tools to edit them. This is the agent's editable working memory.
- **Archival memory** — out-of-context, long-term. `Passage` (`schemas/passage.py`) = `text` + `embedding` (vector), stored via pgvector/sqlite-vec, searched by similarity.
- **Recall memory** — conversation history (`Message`/`Conversation`), searchable.
`ContextWindowOverview` tracks `num_tokens_core_memory`, `num_archival_memory`, `num_recall_memory`, and an external-memory summary — i.e., explicit **context-window accounting**.

### 2.2 The Block (knowledge-representation unit)
[E] `Block` (`schemas/block.py`): `value: str`, `limit: int` (char limit), `label` (section), `read_only: bool`, `is_template`/`template_id`/`base_template_id` (templating), `description`, `metadata`, `hidden`. Blocks are the atomic, labeled, size-bounded memory/knowledge units. Blocks can be shared across agents (`blocks_agents`, `identities_blocks` ORM join tables).

### 2.3 Self-editing memory (the defining mechanism)
[E] The agent edits its **own** memory through tool functions (`functions/function_sets/base.py`): `core_memory_append`, `core_memory_replace`, `memory_insert`, `memory_replace`, `memory_rethink`, `memory_apply_patch`, `memory_finish_edits`, `archival_memory_insert`, `archival_memory_search`, `conversation_search`. Memory mutation is **agent-driven and autonomous** — the model calls these tools to rewrite its working and long-term memory during operation.

### 2.4 Memory versioning
[E] `orm/block_history.py`: `BlockHistory` keeps a `sequence_number` (monotonically increasing per `block_id`, starting at 1, unique index on `(block_id, sequence_number)`) — an **edit-history / version chain of each block's self-edits**. `services/block_manager_git.py` exists (git-backed block management), reinforcing versioned block state.

### 2.5 Agent identity & persistence
[E] `Agent` is ORM-persisted; `Identity` (`schemas/identity.py`) = an external, user-generated `identifier_key` + `name` + `identity_type`, associated with agents and blocks — a **multi-tenant ownership identity** (a user/org that owns agents and memory). `Organization` is the tenancy boundary. Agent state (blocks, messages, passages, tools, config) is serialized (`agent_serialization_manager`, `agent_file.py`) for persistence/migration.

### 2.6 Lifecycle handling
[E] `Step` (+ `step_metrics`), `Run` (+ `run_metrics`), `Job` (+ `job_messages`) model execution units; `llm_batch_job`/`llm_batch_items` model batched inference. Agent steps are persisted with metrics.

### 2.7 Provenance / auditability
[E] `ProviderTrace` (`schemas/provider_trace.py`) = `request_json` + `response_json` + `user_id` + `billing_context` — **LLM request/response + cost logging**; `llm_trace.py` is explicitly "LLM request/response traces stored in ClickHouse for **analytics**." `block_history` provides memory-edit lineage; ORM "Audit fields" record created_by/updated_by; `source_metadata` tracks ingested-document origin. These are **observability/analytics/edit-lineage**, not a unified immutable accountability ledger.

### 2.8 Human governance boundaries
[E] `helpers/tool_rule_solver.py`: `RequiresApprovalToolRule` — "Tool rules that trigger an approval request for **human-in-the-loop**." Designated tools require human approval before execution. **Notably, memory-editing tools are not gated by default** — the agent self-edits memory autonomously; approval is per-configured-tool.

### 2.9 Dependency boundaries & extensibility
[E] LLM-vendor coupling isolated in `llm_api/*_client.py` + `schemas/providers/*` (one module per vendor). Tools are extensible (function sets, MCP client, Composio). Persistence backend is swappable (postgres/sqlite). Per-entity "manager" services encapsulate business logic.

---

## STAGE 3 — Comparison (evidence analysis only; do not force adoption)

Labels: **Already Present · Different but Compatible · Observe · Reject · Not Applicable**. Each justified against DM/PR. Cognate/leakage flagged. "Reject"/"Observe" are **evidence dispositions**, not adoption acts, and never criticisms of Letta on its own terms.

| # | Letta finding (evidence) | Disposition | Justification against AIOS canon |
|---|---|---|---|
| LT1 | **LLM-vendor coupling isolated to per-vendor client/provider modules** (§2.9) | **Already Present** | DM inv 12. Fourth external corroboration (DSPy/LangChain/OpenHands). Corroboration only, not authority. |
| LT2 | **Tiered memory + explicit context-window accounting (core/archival/recall)** (§2.1) | **Different but Compatible** | AIOS models Memory as *derived, non-authoritative* (inv 8) but does **not** manage the LLM context window as a domain concern. Letta's context-window paging is a genuine capability in a layer AIOS does not model. No conflict; different purpose. |
| LT3 | **Autonomous agent self-editing of memory** (`core_memory_append/replace`, `memory_rethink`) (§2.3) | **Reject** *(as an AIOS model — evidence disposition, not a judgment of Letta)* | **Direct inversion of DM inv 8**: AIOS holds that memory must **never** be promoted to authoritative knowledge automatically; here the agent autonomously rewrites its own authoritative memory. Adopting this into AIOS would violate inv 8 and PR-3 (Detect, Don't Decide). Recorded Reject *for AIOS*; for Letta it is the correct design for *its* goal (autonomy). **The corpus's clearest philosophy inversion.** |
| LT4 | **Memory versioning via `block_history` (monotonic sequence per block)** (§2.4) | **Different but Compatible** *(with the corpus's sharpest false-cognate)* | Structurally this resembles the AIOS Knowledge **versioned-identity** design (Blueprint v3: immutable versions + stable correlation key). **But the governance is opposite:** Letta versions *autonomous self-edits*; AIOS versions *human-governed promotions*. Same versioning *structure*, inverted *authority*. Compatible as a technique; **must not** be read as AIOS's governed versioning already existing. **Bias flag:** the strongest "same-structure, opposite-governance" cognate in the program. |
| LT5 | **No Memory/Knowledge boundary — memory *is* the agent's knowledge** (§2.1–2.3) | **Not Applicable / Reject** | AIOS's defining distinction — derived **Memory** vs governed **Knowledge**, separated by the inv-8 promotion gate — **is absent**: Letta's self-edited memory is directly authoritative to the agent. There is no promotion boundary to compare (Not Applicable), and importing the boundary-less model would erase inv 8 (Reject). **This is the deepest structural difference in the corpus.** |
| LT6 | **`Identity` = multi-tenant owner (identifier_key, agents, blocks)** (§2.5) | **Not Applicable** *(false cognate)* | AIOS "Identity" (Blueprint v3) is a **stable correlation key for Knowledge versions**. Letta "Identity" is a **tenancy/ownership principal**. Same word, unrelated concept. **Bias flag.** |
| LT7 | **`Organization` = tenancy boundary** (§2.5) | **Not Applicable** *(false cognate)* | AIOS `Organization` is the **top of the governed domain hierarchy** (Department ownership, §5). Letta `Organization` is a **multi-tenant account**. Same word, different ontology. **Bias flag.** |
| LT8 | **`ProviderTrace`/`llm_trace` = request/response + billing, ClickHouse analytics** (§2.7) | **Not Applicable** *(false cognate)* | AIOS Trace = unconditional, immutable, append-only, per-action **accountability** (inv 4/5, §14.2). Letta "trace" = observability/billing/analytics. Fourth corpus instance of the "trace is never governance-audit" cognate. |
| LT9 | **`RequiresApprovalToolRule` — HITL approval for designated tools** (§2.8) | **Different but Compatible** *(pattern cognate)* | A human-gates-agent mechanism (like LangChain HITL, OpenHands confirmation). Operates at **tool execution**, not the **knowledge-promotion** layer inv 8 governs — and pointedly **does not gate memory self-editing**. Third corpus instance of R-5 (human gates agent). |
| LT10 | **Agent identity & persistence via ORM + serialization** (§2.5) | **Different but Compatible** | Operational persistence of agent state; AIOS persists Agent Definition/Instance through governed lifecycle (DM §6). Compatible; Letta's is operational, AIOS's is governed. |
| LT11 | **Auditability fragments (block_history lineage, created/updated_by, source_metadata) but no unified immutable ledger** (§2.7) | **Not Applicable** *(gradient note)* | Letta has the **most memory-history/edit-lineage** of any corpus repo — fitting, since memory is its subject — yet still **no unified immutable per-action accountability ledger** and no promotion governance. The fragment gradient (DSPy≈0 → OpenHands → **Letta most**) peaks here, still short of AIOS's unified model. |

[E] **Distribution:** Already Present ×1, Different-but-Compatible ×4, Not-Applicable ×4 (three of them false cognates), **Reject ×1 (LT3) + Reject/N-A ×1 (LT5)**. **No "Stronger than AIOS."** The two Rejects are the headline: they mark where Letta, in AIOS's own domain, does the **opposite** of a ratified AIOS invariant — the strongest possible evidence that governance (not memory mechanics) is AIOS's distinguishing commitment.

---

## STAGE 4 — Method Evaluation (directive-specified)

### 4.1 DR-0…DR-6 effectiveness
[E] Applied **unchanged**; each step held:
- **DR-0 Premise Verification** — rejected the strongest premise yet: *"Letta is in AIOS's domain, therefore its Memory/Block/Identity are AIOS's concepts."* They collide by *name* and often by *structure*, but not by *governance*. Also caught the corpus-scope premise (legacy server, not current Letta). **Most premise-work of any review.**
- **DR-1 Grounding** — every claim read from source (`schemas/memory.py`, `block.py`, `orm/block_history.py`, `functions/function_sets/base.py`, `schemas/identity.py`, `provider_trace.py`, `tool_rule_solver.py`). DR-1 is what distinguished LT4 (same-structure versioning) from AIOS governed versioning — only reading the *authority* behind the structure revealed the inversion.
- **DR-2 / DR-3** — options enumerated; each disposition tied to a specific invariant (inv 4,5,8,12; PR-3) — inv 8 did the decisive work (LT3, LT5).
- **DR-4 Classification** — handled the hardest cases in the program: *same word + same structure + opposite governance* (LT4), and *inverted philosophy* (LT3, LT5). The five labels held, but the **partial-cognate/fragment qualifier (MF-4)** and a new *inversion* qualifier were needed (see 4.3).
- **DR-5 / DR-6** — evidence-tagged; every disposition reserved to the Architect; **no adoption made** (directive); nothing enacted.

[E] **Verdict: DR-0…DR-6 functioned in AIOS's home domain against maximal collision** — arguably its hardest test, and its front (DR-0/DR-1) carried the most load by reading *authority/governance behind structure*, not structure alone.

### 4.2 AIOS leakage risks
[E] **Leakage risk was the highest in the program** — Letta uses AIOS's own entity names (Memory, Block≈Knowledge-unit, Identity, Organization, Source, Trace, Agent, Step). **Yet M-6 = 0:** Stage 2 was written in Letta-native terms with no AIOS vocabulary, and every collision was quarantined to Stage 3 and there **named as a cognate** (LT4, LT6, LT7, LT8) — naming cognates is the mechanism that *prevents* leakage. **F-1 not triggered.** The clean result under maximal pressure is the strongest corpus-independence evidence so far — but still says nothing about reviewer-independence.

### 4.3 New methodology observations (all [O]; none enacted, none promoted)
- **[O] MF-4 (reinforced):** partial-cognate/fragment qualifier for DR-4 — needed again (LT11 fragments).
- **[O] MF-6 (new):** a distinct cognate class appeared — **same-word + same-structure + *opposite-governance*** (LT4 versioning; LT3/LT5 self-editing memory). Unlike a name-only cognate (DSPy `trace`) or a fragment (OpenHands provenance), this is a *structural twin with inverted authority*. Candidate: DR-4 could name an explicit "inversion cognate" so a reviewer checks *governance/authority behind* a matching structure, not just the structure. **[O]** — recorded, **not enacted**.
- **[O] MF-1 (further confirmed):** the Stronger/Weaker axis stayed usable in a same-domain corpus (no forced Stronger/Weaker; the honest result was two Rejects, not a "Weaker"). Consistent with the domain-dependence finding.

### 4.4 Evidence limitations
- **[A]** This is the **legacy** Letta V1 server; the current Letta agent (`letta-code`) and new App Server are **out of corpus** — conclusions are scoped to the legacy server and not extrapolated.
- **[A]** Single reviewer → reviewer-independence absent (Plan §9); nothing here is promotion evidence.
- **[A]** Depth was prioritized on the seven focus areas; peripheral subsystems (streaming, batch inference, sandbox) were identified but not deeply extracted.

---

## 5. Consistency Review (DR-6)

- [E] **Constitution:** no authority added, nothing automated, no ratified text touched. §6.2-inv-2, §14.2 used as criteria, not altered. No contradiction.
- [E] **Domain Model:** unmodified. inv 4,5,8,12 cited; the `Memory`/`Block`/`Identity`/`Organization`/`Source`/`Trace`/`Agent` word-collisions were explicitly kept from blurring the AIOS entities of those names (LT4, LT6, LT7, LT8). No entity/relationship/invariant defined or redefined.
- [E] **Principles Register:** PR-1, PR-3 used as lenses; none altered; none promoted.
- [E] **Knowledge Blueprint v3:** cited for the versioned-identity comparison (LT4); **unmodified**; the comparison is evidence analysis, not a change.
- [E] **Validation Plan / prior reviews:** executed as specified; predecessors used only as comparators; **no synthesis** (directive); log updated separately.

**No contradiction found. No canonical change. No adoption. No synthesis.**

---

## 6. Summary and Stop

[E] **Repository #4 (Letta / formerly MemGPT, `letta` v0.16.8 — legacy V1 server) reviewed as external evidence, not authority.** Letta occupies **AIOS's home domain** (memory, knowledge representation, agent identity/persistence, context management) but takes the **opposite governance stance**: memory is **autonomously self-edited and self-improving**, whereas AIOS holds Memory→Knowledge promotion must **never** be automatic (inv 8). Dispositions: 1 Already-Present, 4 Different-but-Compatible, 4 Not-Applicable (3 false cognates), **2 Reject** — the Rejects (autonomous self-editing memory; absence of a Memory/Knowledge boundary) mark direct inversions of a ratified AIOS invariant. **No adoption was made (directive); AIOS is changed by nothing.**

[E] **Method evaluation:** **DR-0…DR-6 functioned under the program's maximum vocabulary/structure collision**, its front reading *governance-behind-structure* to separate true concepts from cognates. **AIOS leakage M-6 = 0** under the highest risk yet. One new observation **MF-6 (an "inversion cognate" class: same word + same structure + opposite governance)** recorded **[O]** — **not enacted, not promoted**; methodology unchanged. Evidence limited to the legacy server; reviewer-independence still absent.

No implementation, code, schema, API, or subsystem was produced. No Letta design, API, or folder structure was copied. No AIOS canonical document was created or modified. No principle was promoted. No adoption decision was made. No governance event, reviewer identity, or Trace/Memory record was fabricated. Trace store unchanged (540 records); no `execution/` file touched by this read-only review.

**Stopping after the validation log update, per directive. Awaiting Architect review before any repository #5.** No synthesis performed.
