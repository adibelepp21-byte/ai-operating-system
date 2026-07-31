# AIOS Decision Review Methodology — External Corpus Validation: OpenHands v1.0

**Program:** External Repository Validation Program — Repository #3 (N=3 milestone).
**Executes:** `AIOS_DECISION_REVIEW_METHOD_VALIDATION_PLAN_v1.0`.
**Corpus item:** `OpenHandsmain.zip` — repository #3. Predecessors: DSPy (#1, different-domain), LangChain (#2, execution-overlap).
**Status:** External-evidence review only. Additive. Creates no canonical document, modifies none, redesigns nothing, implements nothing, promotes no principle. Does not copy OpenHands design, API, folder structure, or implementation.
**Authority posture:** OpenHands is **external evidence, not authority** (Validation Plan §2). DSPy and LangChain are used **only as methodology comparators**, never as authority.
**Methodology discipline:** DR-0…DR-6 applied **unchanged**. Weaknesses recorded as candidate refinements **[O]**, never enacted, never promoted (directive).
**Confidence:** **[E]** evidenced · **[A]** assumption · **[O]** open question.
**Reviewer independence:** single reviewer — corpus-independence demonstrable; reviewer-independence **[O]**, reserved to the Architect (Plan §9).

---

## 0. Purpose and Framing

[E] Same twofold purpose: (1) **method test** on a third, independent corpus; (2) **third independent evidence** — which reaches the **N=3 milestone** and therefore triggers a *Preliminary* Cross-Repository Evidence Review (separate document `AIOS_DR_PRELIMINARY_EVIDENCE_REVIEW_v1.0`), explicitly **not** a final synthesis (directive).

[E] **Framing — the domain gradient.** DSPy was *different-domain*; LangChain *overlapped AIOS's execution layer*; **OpenHands overlaps AIOS's execution layer AND, for the first time, touches AIOS's governance-adjacent concerns** — it is an autonomous coding-agent platform with runtime autonomy-gating, human confirmation, event persistence, and provenance attribution. This is the **most commensurable and highest-leakage-risk corpus yet**. I fix it before judgment (PR-1) and do **not** treat AIOS as the baseline OpenHands is measured against.

[E] **Corpus-boundary honesty (DR-1).** The uploaded repository is `openhands-ai` **1.11.0**, which is the **control-center / application-server layer**. Its core agent runtime is delegated to **external packages not present in this zip**: `openhands-sdk==1.36.0`, `openhands-agent-server==1.36.0`, `openhands-tools==1.36.0` (`pyproject.toml`). Therefore claims about the *agent loop itself* (action/observation cycle, the `Event` type, controller) are **boundary-limited**: I extract what the app-server layer shows and what it references from the SDK, and I explicitly mark where the runtime lives outside the corpus. I do **not** invent the SDK's internals.

[A] Three repositories are three data points — the *minimum* the Plan names for structural-consistency (SC-5), and enough for a *preliminary* look, but **not** the final synthesis and **not** promotion evidence (reviewer-independence still absent).

---

## STAGE 1 — Repository Identification

| Attribute | Value | Evidence |
|---|---|---|
| Package | `openhands-ai` **v1.11.0** | `pyproject.toml` |
| Self-description | "OpenHands: Code Less, Make More" / "self-hosted developer control center for coding agents and automations" | `pyproject.toml`, `README.md` |
| Nature | **Control-center / app-server** that runs OpenHands, Claude Code, Codex, Gemini, or any ACP-compatible agent across local/remote/cloud backends | `README.md` |
| Agent runtime core | **External** — `openhands-sdk`, `openhands-agent-server`, `openhands-tools` (all v1.36.0), **not in this zip** | `pyproject.toml` |
| Language / runtime | Python `>=3.12, <3.14` | `pyproject.toml` |
| License | MIT | `pyproject.toml` |
| Scale (`openhands/`, non-enterprise) | 227 `.py` files, ~31,140 LOC | `find … | cat | grep -c` |
| Tests | 110 `test_*.py` in `tests/` | `find` |
| Also present | `frontend/`, `enterprise/`, `openhands-ui/`, `skills/`, `containers/`, `kind/` (k8s), docker — a full product | repo root |
| Key deps | `litellm==1.84.1` (pinned), `fastmcp`, `mcp`, `gitpython`, the three `openhands-*` packages | `pyproject.toml` |
| `app_server` subsystems | `app_conversation`, `event`, `event_callback`, `sandbox`, `mcp`, `secrets`, `settings`, `status`, `user_auth`, `integrations`, `file_store`, … | `openhands/app_server/` |

[E] **Domain classification (decisive):** OpenHands is an **autonomous coding-agent runtime platform**. Its concerns — agent runtime, execution lifecycle, task orchestration, tool execution, runtime state, autonomy boundaries, human intervention — **overlap AIOS's execution layer directly and reach into governance-adjacent territory** (this is the first corpus with a runtime autonomy-gate and provenance). It still does **not** implement AIOS's *unified governance model* (immutable per-action accountability ledger + human-governed Memory→Knowledge promotion + ratified authority tiers), as Stage 3 shows.

[E] **Parity governance-term scan.** Unlike DSPy and LangChain (near-zero governance vocabulary), OpenHands returns **several fragments**: `provenance` (Agent-Profile launch attribution, `app_conversation_models.py`, `settings_models.py`), `immutable` (frozen pydantic configs, `MappingProxyType` secrets, `integrations/provider.py frozen=True`, sandbox-spec immutable list, HTTP cache-control), and — in code, not the scan — a **confirmation policy** and **security analyzer**. **These are governance *fragments*, not a unified governance layer** (see §Stage-3 O9). This gradient is itself a finding.

---

## STAGE 2 — Architecture Extraction (objective; no judgment; no AIOS vocabulary)

### 2.1 Task orchestration & execution lifecycle
[E] A conversation is the unit of work. `app_conversation/` provides `AppConversationService` (base + SQL + live-status implementations), `AppConversationStartTaskService`, `app_conversation_router`. Starting a task runs setup: `run_setup_scripts`, `maybe_run_setup_script`, `clone_or_init_git_repo`, `maybe_setup_git_hooks`, skill loading. Lifecycle is modeled by explicit state enums:
- `SandboxStatus`: `STARTING / RUNNING / PAUSED / ERROR / MISSING` (`sandbox/sandbox_models.py`).
- `ConversationExecutionStatus` (from `openhands.sdk`): includes `ERROR`, `STUCK`, `DELETING` — note **stuck-detection** as a first-class runtime state.
- `AppConversationStartTaskStatus`: `WORKING`, `RUNNING_SETUP_SCRIPT` (`app_conversation_models.py`).

### 2.2 Agent runtime & planning
[E] The runtime is delegated to the external agent-server/SDK; the app-server configures and launches it. Planning is a first-class **agent mode**: `AgentType` distinguishes `PLAN` from `DEFAULT`, and `_create_condenser` builds a `planning_condenser` vs a default `condenser` accordingly (`app_conversation_service_base.py`).

### 2.3 Runtime state management & event persistence
[E] `app_server/event/`: `EventServiceBase` (ABC) with `save_event`, `get_event`, `search_events`, `count_events`, `iter_events_for_export`, `batch_get_events`, and `_store_event`/`_load_event`; backends are pluggable — `filesystem_event_service`, `google_cloud_event_service`, `aws_event_service`, plus an `event_store`. The `Event` type itself comes from `openhands.sdk`. `event_callback/` reacts to events (`set_title_callback_processor`, `webhook_router`, SQL-backed callbacks) — a **reactive trigger** layer. Events are saved, searched, and exportable; no `update_event`/`delete_event` appears in the base (functionally append-oriented), but persistence is backend-pluggable and **no contract-level immutability/append-only guarantee is stated** in what the corpus exposes.

### 2.4 Autonomy boundaries & human intervention
[E] The core mechanism (`app_conversation_service_base.py`):
- `SecurityAnalyzerBase` / `LLMSecurityAnalyzer` — a pluggable analyzer that assesses the risk of an agent action (`"llm"` → `LLMSecurityAnalyzer`; `"none"`/unknown → `None`).
- `ConfirmationPolicyBase` with three concrete policies: `NeverConfirm`, `AlwaysConfirm`, `ConfirmRisky`.
- `_select_confirmation_policy(confirmation_mode, security_analyzer)`: if confirmation off → `NeverConfirm`; if analyzer is `llm` → `ConfirmRisky` (confirm *only* risky actions); else → `AlwaysConfirm`.
This is a **runtime autonomy gate**: it decides, per policy and per assessed risk, which agent actions proceed autonomously vs. require human confirmation before execution.

### 2.5 Tool execution
[E] Tool execution is delegated to `openhands-tools` (external) and the **MCP** protocol: `app_server/mcp/` plus `fastmcp>=3.2` and `mcp>=1.25` dependencies. The app-server exposes/configures tools; execution occurs in the sandbox via the agent-server.

### 2.6 Hooks & skills (extensibility / intervention)
[E] `hook_loader.py`: hooks are loaded from `{project}/.openhands/hooks.json`, but **all hook loading is delegated to the agent-server** (`/api/hooks`); the app-server is "a thin proxy." `HookConfig` comes from `openhands.sdk.hooks`. `skill_loader.py` + `load_and_merge_all_skills` / `_merge_skills` / `_create_agent_with_skills` compose skills onto an agent. Both are extension points.

### 2.7 Provenance & immutability (data-modeling)
[E] `provenance` denotes **Agent-Profile launch attribution** — which profile/user launched a conversation (`app_conversation_models.py` `@computed_field`, `settings_models.py`, `live_status…launch_snapshot`). `immutable`/`frozen` are used as **data-modeling** techniques: frozen pydantic models (`integrations/provider.py`), `MappingProxyType` for secrets (`secrets_models.py`), an immutable sandbox-spec list. These are *local* immutability guarantees, not a system-wide ledger.

### 2.8 Dependency boundaries & modular integration
[E] LLM-vendor coupling is isolated behind `litellm` (single pinned dependency, with `openai` pinned only for litellm compatibility). The agent runtime is isolated behind the three `openhands-*` SDK packages. The app-server is layered (`app_conversation`, `event`, `sandbox`, `settings`, `secrets`, `user_auth`, `integrations`) with pluggable persistence backends (filesystem / GCP / AWS / SQL) per subsystem. `enterprise/` is a separate overlay.

### 2.9 Extensibility (as evidenced)
[E] Extension by: pluggable service backends (ABC + injector pattern, e.g. `AppConversationStartTaskServiceInjector`); pluggable event backends; pluggable `SecurityAnalyzer`/`ConfirmationPolicy`; skills; hooks; MCP tools; support for multiple external agent kinds (OpenHands/Claude Code/Codex/Gemini/ACP). Highly pluggable.

### 2.10 Documentation
[E] `README.md`, `AGENTS.md`, `CLAUDE.md`, `Development.md`, per-subsystem `README.md` files, `analytics/EVENTS.md`, plus external docs. No governance/decision-record documentation.

---

## STAGE 3 — AIOS Comparison (classification with evidence)

Classes: **Already Present · Stronger than AIOS · Weaker than AIOS · Different but Compatible · Not Applicable**. Justified against DM / PR. Cognate/leakage risks flagged.

| # | OpenHands finding (evidence) | Classification | Justification against AIOS canon |
|---|---|---|---|
| O1 | **External agent-runtime & LLM-vendor coupling isolated behind SDK packages + `litellm`** (§2.8) | **Already Present** | DM inv 12 (external dependency isolated). Third external corroboration (DSPy `clients/`, LangChain `partners/`). **[A]** packaging/dependency convention vs ratified invariant — corroboration only, not validation. |
| O2 | **Explicit execution-lifecycle state machines: Sandbox / ConversationExecution / StartTask, incl. STUCK detection** (§2.1) | **Different but Compatible** | AIOS models Agent-Instance lifecycle (DM §6) as a *governance* lifecycle; OpenHands models *operational runtime* states. Compatible; different purpose. STUCK-detection has no AIOS analog (AIOS traces actions but has no runtime stuck-state). |
| O3 | **Runtime autonomy gate: SecurityAnalyzer + ConfirmationPolicy (NeverConfirm/AlwaysConfirm/ConfirmRisky)** (§2.4) | **Different but Compatible** *(with a qualified-Stronger aspect AND a PR-3 tension)* | AIOS has **no runtime risk-confirmation gate**; it governs by *unconditional immutable Trace* (inv 4/5), *Fail-Closed* (PR-4), and *human-governed promotion* (inv 8). On the narrow axis of **pre-action runtime autonomy-gating, OpenHands does something AIOS does not** — a qualified strength. **But** its `ConfirmRisky` path relies on an **LLM deciding** risk (`LLMSecurityAnalyzer`), which is precisely the automated-judgment PR-3 (Detect, Don't Decide) restricts and §6.2-invariant-2 guards. So it is **not** "Stronger than AIOS" wholesale — it is a *different governance philosophy* (pre-gate by machine-judged risk vs. record-all + human-govern-promotion). Compatible only as contrast. **Bias flag:** do not read OpenHands' confirmation gate as the governance AIOS "should" have. |
| O4 | **Human intervention: confirmation_mode + hooks** (§2.4, §2.6) | **Different but Compatible — pattern cognate** | A human-gates-agent mechanism, like LangChain's HITL (approve/edit/reject). Operates at the **execution** layer (gate a pending action), not AIOS's **promotion** layer (inv 8). Second corpus instance of "human gates agent autonomy" (LangChain #2, OpenHands #3; absent in DSPy). |
| O5 | **Event store: per-action events saved/searched/exported; pluggable backend; event_callback triggers** (§2.3) | **Not Applicable for governance-audit — NEAREST false-cognate in the corpus; Different-but-Compatible as event-sourcing** | This is the **closest structural analog to AIOS Trace seen so far**: per-action, persisted, searchable, exportable, functionally append-oriented, and *central* (not optional like LangChain callbacks). **Yet it differs by purpose and guarantee:** it is an **operational conversation-history / event-sourcing** mechanism (replay, UI, resumption, analytics, export), with **backend-pluggable persistence and no stated contract-level immutability/append-only/unconditional guarantee**, and it is **not** tied to an authority or promotion model. AIOS Trace is a **ratified governance-accountability ledger** (inv 4/5 + Constitution §14.2: unconditional, immutable, append-only, exactly-one-per-action). Classified Not-Applicable for the *governance* comparison (to block a false "Already Present"), Different-but-Compatible for the *event-sourcing* aspect. **The subtlest cognate yet — the distinction rests on purpose+guarantee, not structure** (see §7). |
| O6 | **Provenance: Agent-Profile launch attribution** (§2.7) | **Different but Compatible** | First external repo with *any* provenance concept. But it attributes *who launched a conversation*, not *what every action did and who is accountable* (AIOS Trace). A fragment of accountability, not the accountability ledger. |
| O7 | **Immutability as data-modeling (frozen configs, MappingProxyType secrets)** (§2.7) | **Different but Compatible** | OpenHands uses immutability *locally* for safety of specific values. AIOS inv 5 makes immutability a *system-wide governance guarantee* on the Trace ledger. Same technique, incomparable scope/intent. **Bias flag:** local frozen models ≠ inv-5 immutable ledger. |
| O8 | **Context condensation (LLMSummarizingCondenser; planning vs default)** (§2.2) | **Different but Compatible** | Automatic context summarization rhymes with AIOS Memory *derivation*, but is **ungoverned** — no analog to inv 8 (Memory→Knowledge only via governed review). Compatible as a runtime feature; must not be read as governed Memory. |
| O9 | **Governance *fragments* but no unified governance layer** (§Stage-1 scan, O3/O6/O7) | **Not Applicable (with a gradient note)** | Unlike DSPy/LangChain (≈zero governance vocabulary), OpenHands has fragments — confirmation gate, provenance, local immutability. **But there is no unified model**: no unconditional per-action immutable accountability ledger, no human-governed knowledge-promotion, no ratified authority tiers. Third repo with no unified governance layer — **yet the *most* fragments**, tracking the domain gradient (§0). |
| O10 | **Highly pluggable backends (ABC + injector; filesystem/GCP/AWS/SQL; multiple agent kinds)** (§2.9) | **Different but Compatible** | Strong operational extensibility; orthogonal to AIOS governance-artifact structure. No conflict. |

[E] **Distribution (this repo):** Already Present ×1 (O1), Different-but-Compatible ×7 (O2, O3, O4, O6, O7, O8, O10), Not Applicable ×2 (O5-governance, O9). **No unqualified Stronger** (O3 carries a *qualified* strength on runtime-gating but is classified Different-but-Compatible because of the PR-3 tension). The governance-dimension findings remain Not-Applicable, consistent with DSPy and LangChain — but with the most governance *fragments* of the three, exactly as the domain gradient predicts.

---

## STAGE 4 — Adoption Decision

Classes: **Adopt · Adapt · Observe · Reject**. **Discipline:** adoption of external architecture into AIOS is an **Architect** decision under Authority/Evidence Inversion (external repos are evidence, never authority) and reserve-to-Architect (DR-6). Therefore **I record zero Adopt at every N** — reaching N=3 unlocks a *preliminary methodology* look, **not** self-authorized architecture transfer (directive: do not implement, do not change AIOS, do not promote).

| Finding | Decision | Justification (DM / PR) |
|---|---|---|
| O1 (dependency isolation) | **Observe** | Third corroboration of inv-12-style isolation. Now n=3 — recorded as a genuine recurring external pattern in the Preliminary Review, still evidence not authority; AIOS already holds inv 12. |
| O2 (lifecycle state machines) | **Observe** | Operational-state modeling (esp. STUCK-detection) is evidence for a possible future AIOS runtime-state concern — reserved, not adopted. |
| O3 (autonomy gate / confirmation policy) | **Observe (with hard PR-3 caveat) — explicitly NOT Adopt** | The most tempting finding for a governance system, hence the most disciplined to defer. Any AIOS runtime-gating must respect PR-3 (Detect, Don't Decide) and §6.2-inv-2 — an **LLM deciding** whether to confirm would breach them. Recorded as evidence of a *different governance philosophy*; adoption is the Architect's call, and would be *adapt-through-governance*, never copy. |
| O4 (human intervention) | **Observe** | Second instance of human-gates-agent (with LangChain). Record; do not conflate with inv-8 promotion governance. |
| O5 (event store) | **Reject (near AIOS Trace) / Observe (event-sourcing)** | Reject importing OpenHands' event model as an AIOS-Trace substitute — it lacks inv-4/5 + §14.2 guarantees. Separately Observe event-sourcing as a neutral operational technique. Seals the corpus's subtlest cognate. |
| O6 (provenance) | **Observe** | Fragment of attribution; evidence that accountability concerns appear near AIOS's domain. Not adopted; not the Trace ledger. |
| O7 (local immutability) | **Observe** | Data-modeling technique; unrelated to inv-5 ledger guarantee. |
| O8 (condensation) | **Observe (with governance caveat)** | Ungoverned summarization ≠ governed Memory (inv 8). Record; do not adopt as Memory. |
| O9 (no unified governance) | **Reject (n/a)** | Nothing to adopt; its absence is not evidence about AIOS governance. The *fragment gradient* is recorded in the Preliminary Review. |
| O10 (pluggable backends) | **Observe** | Operational extensibility; may inform future AIOS infrastructure. Not adopted. |

[E] **Net: zero Adopt, eight Observe (several caveated), two Reject. AIOS is changed by nothing.**

---

## 6. Did DR-0…DR-6 Work on a Third Domain? (Primary Deliverable)

[E] Applied **unchanged**. Step-by-step:

| Step | Held? | Evidence |
|---|---|---|
| **DR-0 Premise Verification** | **Held — hardest-working yet** | Rejected three temptations: OpenHands as same-domain peer; its governance *fragments* as AIOS-equivalent governance; and — new — the **corpus-boundary** illusion (the agent runtime is in an external SDK not in the zip). §0 corpus-boundary honesty is a DR-0 product. |
| **DR-1 Grounding** | **Held strongly** | Every claim read from source (`app_conversation_service_base.py`, `event_service_base.py`, `sandbox_models.py`, `app_conversation_models.py`, `hook_loader.py`, `pyproject.toml`). DR-1 caught the event-store cognate (O5) and kept SDK internals out of scope (not fabricated). |
| **DR-2 Option Enumeration** | **Held** | Stage 4 enumerates Adopt/Adapt/Observe/Reject per finding. |
| **DR-3 Canonical Evaluation** | **Held** | Each class tied to a specific invariant/PR (inv 4,5,8,12; PR-3, PR-4; §14.2, §6.2). |
| **DR-4 Classification** | **Held — and handled a *partial-cognate gradient*** | OpenHands produced findings that are neither full-match nor fully-N/A but *fragments* of AIOS concepts (O3 confirmation≈gating, O6 provenance≈attribution, O7 frozen≈immutability). The five classes absorbed these via explicit "fragment/aspect" qualifiers. The DSPy-era commensurability worry (MF-1) again did **not** bite. |
| **DR-5 Evidence-Tagged Recommendation** | **Held** | Stage 4 tagged; open items left open. |
| **DR-6 Consistency Review + Reserve-to-Architect** | **Held** | §8; every adoption reserved to the Architect; nothing enacted. |

[E] **Conclusion: DR-0…DR-6 functioned on a third, most-adjacent corpus** — its front (DR-0/DR-1) again did real work, this time also guarding a **corpus-boundary** illusion unique to a repo whose runtime lives in an external SDK.

[O] **New candidate refinement (recorded, NOT enacted, NOT promoted): MF-4 — a "partial-cognate / fragment" qualifier for DR-4.** As an external domain approaches AIOS's, findings arrive that are *fragments* of an AIOS concept (a confirmation gate that is *part of* governance; provenance that is *part of* accountability; frozen models that are *part of* immutability). The binary Already-Present/Not-Applicable strains; the review needed explicit "aspect/fragment" language. Whether DR-4 should formalize a partial-match qualifier is **[O]**, reserved. Methodology unchanged.

---

## 7. AIOS-Bias Audit (Directive-Required)

[E] Highest-adjacency corpus → highest stakes. Risks and handling:

1. **Event-store cognate (O5) — subtlest in the corpus.** Structurally the closest analog to AIOS Trace (central, per-action, persisted, append-oriented). Risk: false "Already Present." **Caught** by DR-1 (no immutability/unconditional guarantee; operational not governance purpose); classified Not-Applicable + Reject.
2. **Confirmation-gate as governance (O3).** Risk: reading OpenHands' runtime autonomy-gate as the governance AIOS lacks. **Caught** by DR-3 (PR-3 Detect-Don't-Decide tension: an LLM deciding confirmation is the automated judgment AIOS restricts). Classified Different-but-Compatible, not Stronger.
3. **Provenance/immutable vocabulary (O6/O7).** Risk: fragment vocabulary read as AIOS accountability/inv-5. **Flagged**; split into fragment vs. system-guarantee.
4. **Corpus-boundary illusion (new).** Risk: describing the external SDK's runtime as if present in the zip. **Caught** by DR-0/DR-1; scope explicitly limited.
5. **Predecessor-as-authority leakage.** Risk: DSPy/LangChain conclusions pre-judging OpenHands. **Controlled** — used only to test the method; every finding re-derived from OpenHands source.

[E] **M-6 leakage = 0:** Stage 2 has no AIOS vocabulary; comparison quarantined to Stage 3+. Naming four cognates is leakage *prevention*.

[A] **Residual reviewer-centric bias** unchanged — focus-area selection and the "execution/governance-fragment vs unified-governance" framing are AIOS-centric acts. Reviewer-independence limit (Plan §9), **[O]**, reserved.

---

## 8. Consistency Review (DR-6)

- [E] **Constitution:** no authority added, nothing automated, no ratified text touched. §6.2-inv-2 and §14.2 *used* as evaluation criteria (O3, O5), not altered. No contradiction.
- [E] **Domain Model:** unmodified. Classifications cite inv 4, 5, 8, 12; the `Tool`/`Skill`/`Agent`/`Runtime`/`Memory` words in OpenHands were kept from blurring the AIOS entities of the same names. No entity/relationship/invariant defined or redefined.
- [E] **Principles Register:** PR-1, PR-3, PR-4 used as lenses; none altered; none promoted.
- [E] **Validation Plan:** executed as specified — additive doc under §10 naming; corpus-independent; M-6 = 0; methodology unchanged; predecessors used only as comparators.
- [E] **DSPy (#1) & LangChain (#2) reviews:** unmodified, not treated as authority. N=3 cross-repo evidence is summarized in the **separate Preliminary Review**, explicitly not a final synthesis.

**No contradiction found.**

---

## 9. Handoff to the Preliminary Cross-Repository Evidence Review

[E] Per directive, the N=3 milestone triggers a *Preliminary* Cross-Repository Evidence Review — a **separate additive document** (`AIOS_DR_PRELIMINARY_EVIDENCE_REVIEW_v1.0`) that only: identifies patterns across all three; identifies single-repo-unique patterns; checks DR-0…DR-6 consistency across three domains; checks AIOS leakage; and records new candidate refinements as **[O]**. It is **not** a final synthesis and **promotes nothing** (directive). OpenHands' contribution to that review: it converts several n=2 signals to n=3 (dependency isolation; "trace/event never governance"; no-unified-governance), sharpens the human-gates-agent pattern to n=2, and introduces the partial-cognate-gradient observation (MF-4, [O]).

---

## 10. Summary and Stop

[E] **Repository #3 (OpenHands `openhands-ai` 1.11.0 — the control-center layer; agent runtime in external SDK) reviewed as external evidence, not authority.** Most governance-adjacent corpus yet: runtime autonomy-gate, human confirmation, event persistence, provenance — **overlapping AIOS's execution layer and touching governance-adjacent concerns, but with no unified governance model.** Findings: 1 Already-Present, 7 Different-but-Compatible, 2 Not-Applicable (including the corpus's **subtlest false-cognate**, the event store). Adoption: **0 Adopt, 8 Observe (caveated), 2 Reject — AIOS changed by nothing.**

[E] **Primary deliverable:** **DR-0…DR-6 functioned on a third domain**, with DR-0/DR-1 again load-bearing and additionally guarding a corpus-boundary illusion. One new candidate refinement **MF-4 (partial-cognate/fragment qualifier for DR-4)** recorded **[O]** — **not enacted, not promoted**; methodology unchanged.

[E] **AIOS-bias audit:** five risks (subtlest yet — the event-store cognate) identified and controlled. **M-6 = 0.** Residual reviewer-centric bias reserved to the Architect.

No implementation, code, schema, API, or subsystem was produced. No OpenHands design, API, or folder structure was copied. No AIOS canonical document was created or modified. No principle was promoted. No governance event, reviewer identity, or Trace/Memory record was fabricated. Trace store unchanged (540 records); no `execution/` file touched by this read-only review.

**Stopping after the log update and the Preliminary Cross-Repository Evidence Review. Awaiting Architect authorization for repository #4.** Final synthesis remains deferred beyond the preliminary look.
