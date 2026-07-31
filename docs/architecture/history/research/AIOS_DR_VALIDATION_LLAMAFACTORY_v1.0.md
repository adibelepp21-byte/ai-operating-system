# AIOS Decision Review Methodology — External Corpus Validation: LlamaFactory v1.0

**Program:** External Repository Validation Program — Repository #10.
**Executes:** `AIOS_DECISION_REVIEW_METHOD_VALIDATION_PLAN_v1.0`.
**Corpus item:** `hiyouga/LLaMA-Factory` (package `llamafactory` **0.9.6.dev0**), supplied as `LlamaFactorymain.zip` (official public repository snapshot). Predecessors: DSPy (#1), LangChain (#2), OpenHands (#3), Letta (#4), Haystack (#5), CrewAI (#6), LlamaIndex (#7), LangGraph (#8), Supabase (#9).
**Status:** External-evidence review only. Additive. Creates no canonical document, modifies none, redesigns nothing, implements nothing, promotes no principle. **No Adopt, No Reject.** Does not copy LlamaFactory design, API, folder structure, or implementation.
**Authority posture:** LlamaFactory is **external evidence, not authority** (Validation Plan §2). Predecessors used **only as methodology comparators**, never as authority.
**Methodology discipline:** DR-0…DR-6 **frozen**; applied unchanged. Weaknesses recorded as candidate refinements **[O]**, never enacted, never promoted. **No synthesis, no cross-repository comparison** (directive).
**Principles applied:** PR-1 Evidence First · PR-3 Detect Don't Decide · PR-4 Fail Closed · PR-5 Capture Don't Reference.
**Corpus provenance (DR-1 honesty):** extracted read-only to scratch (`/tmp`); nothing written to AIOS.
**Confidence:** **[E]** direct observation · **[A]** reasoned inference · **[O]** open question. Single reviewer → reviewer-independence **[O]**, reserved to the Architect (Plan §9).

---

## 0. DR-0 — Premise & Boundary

[E] **Domain:** LlamaFactory is an **LLM fine-tuning / training framework** — a config-driven **unified wrapper over the HuggingFace training stack** (`transformers`, `peft`, `trl`, `datasets`, `accelerate`). This is an **ML model-training** domain — related to DSPy (#1, ML) but *training/adaptation*, not prompt-optimization. The premise to reject: *"LlamaFactory's Adapter/Checkpoint/Merge/Template/Provenance are AIOS concepts"* — they are ML-training terms whose meaning is domain-specific (and, as §17 shows, collide with *different* meanings already seen in the corpus).
[E] **Corpus-boundary honesty (DR-1):** the mature package is `src/llamafactory`; a parallel **`v1/`** restructure (`core`, `trainers`, `plugins`, `config`, `accelerator`, `samplers`) and `tests_v1/` are present as an **emerging rewrite**. Primary review targets the mature `src/llamafactory`; `v1/` is noted as in-progress and not extrapolated. The actual training compute (autograd, kernels) lives in `transformers`/`peft`/`torch` — **out of corpus**, wrapped here.

---

## 1. Training Architecture

[E] `train/tuner.py::run_exp` dispatches by `finetuning_args.stage` to stage-specific workflows: **pt** (pretraining), **sft** (supervised fine-tuning), **rm** (reward modeling), **ppo**, **dpo**, **kto**, **mca** — each a `train/<stage>/workflow.py` built on HuggingFace `Trainer`/TRL. Plus `hyper_parallel`, `fp8_utils`, `callbacks.py`. Training = **config → stage-trainer → HF Trainer loop**.

## 2. Dataset Lifecycle

[E] `data/`: `loader.py` (`_load_single_dataset` → `get_dataset`) loads from HF Hub / ModelScope / OpenMind / local via `datasets`; `converter.py`/`aligner` normalize to a standard schema; `formatter.py` + `template.py` apply chat templates; `processor/` tokenizes; `collator.py` batches; `mm_plugin.py` handles multimodal. Lifecycle: **load → align/convert → template-format → tokenize → collate → merge**.

## 3. Model Lifecycle

[E] `model/loader.py` loads model+tokenizer from `model_name_or_path` (+ `model_revision`); `patcher.py` patches for training (attention, rope, etc.); `adapter.py` attaches the tuning method; after training, `export_model` merges/quantizes/exports. Lifecycle: **load → patch → adapt → train → merge → quantize → export**.

## 4. Checkpoint Management

[E] Via HuggingFace `Trainer` (`output_dir`, `save_steps`, `resume_from_checkpoint`). A **checkpoint = a saved snapshot of model weights (+ optimizer/scheduler state) for resume/selection.** (This is a *third* distinct sense of "checkpoint" in the corpus — see §17.)

## 5. Adapter Architecture (LoRA / QLoRA)

[E] `model/adapter.py` (via PEFT: `LoraConfig`, `LoraModel`, `PeftModel`, `get_peft_model`, `OFTConfig`) supports four modes: **full** (`_setup_full_tuning`), **freeze** (`_setup_freeze_tuning` — last-N / strided layers), **LoRA**, and **QLoRA** (LoRA over a quantized base). An **Adapter = a trainable low-rank weight-delta module** injected into the frozen base. (A *different* meaning of "Adapter" than #2/#5 — see §17.)

## 6. Quantization

[E] `model/model_utils/quantization.py` supports **bitsandbytes, GPTQ, AWQ, AQLM, HQQ, EETQ** (+ FP8). Used for QLoRA (quantized base) and export-time quantization. Precision reduction for memory/speed.

## 7. Merge Pipeline

[E] `train/tuner.py::export_model`: **merges LoRA adapter weights into the base model** (guards: "merge adapters before quantizing"; "cannot merge adapters to a quantized model"), then optionally re-quantizes and exports (optionally pushes to a hub). **Merge = weight arithmetic (fold ΔW into W)** — not a version-control or conflict merge (see §17).

## 8. Evaluation Pipeline

[E] `eval/` runs benchmark evaluation (MMLU/CMMLU/C-Eval style) via `evaluation_args`; training-time metrics via `metrics.txt` extras. Evaluation = **benchmark scoring of a model**.

## 9. Experiment Tracking

[E] HF Trainer `report_to` + integrations: **wandb, tensorboard, mlflow, swanlab** (`finetuning_args`, `callbacks.py`). Tracks runs, hyperparameters, metrics, artifacts for reproducibility.

## 10. Configuration Architecture

[E] `hparams/`: dataclasses — `model_args`, `data_args`, `training_args`, `finetuning_args`, `generating_args`, `evaluation_args` — parsed by `parser.py` from **YAML/CLI/JSON**. The entire run is declared by config (see `examples/`). Config-first design.

## 11. Extension Mechanism

[E] Register custom **datasets** (`data/dataset_info.json`), **chat templates** (`template.py`), **models** (loader/patcher), **quantization/optimizer** backends (per-feature requirements), and `third_party/` integrations; `webui/` for no-code use. Extensible by registration + optional dependencies.

## 12. Dependency Isolation

[E] `requirements/` holds **per-feature requirement files** — `bitsandbytes`, `gptq`, `awq`/`aqlm`, `hqq`, `eetq`, `deepspeed`, `galore`, `badam`, `apollo`, `adam-mini`, `liger-kernel`, `vllm`, `sglang`, `swanlab`, `npu`, `fp8`, … Each capability is an **isolated optional extra**; core = transformers/peft/trl/accelerate/datasets. Strong optional-dependency isolation.

## 13. Vendor Abstraction

[E] LlamaFactory is fundamentally a **unified abstraction over the HuggingFace ecosystem** (transformers/peft/trl/datasets/accelerate) plus multiple **model hubs** (HuggingFace, ModelScope, OpenMind) and inference backends (vLLM, SGLang). Its value *is* the vendor/stack abstraction.

## 14. Provenance

[E] **Operational (reproducibility) provenance, Observed:** an adapter records its base via `adapter_name_or_path`/PEFT `adapter_config.json` (`base_model_name_or_path`); models pinned by `model_revision`; datasets sourced with hub tokens (`hf_hub_token`/`ms_hub_token`/`om_hub_token`) and identifiers; experiment trackers log run lineage. **Governance provenance: Not Observed** — this is artifact/reproducibility lineage, not accountable per-action governance provenance.

## 15. Versioning

[E] Package `VERSION = 0.9.6.dev0`; **model versioning** via `model_revision` (hub commit/tag pin); dataset versioning via source + hashing. Versioning of *artifacts* (models/datasets), **not** AIOS Knowledge versioned-identity (Blueprint v3).

## 16. Governance Concepts (Observed / Not Observed)

[E] Governance/provenance/audit/immutable/authority/promotion scan of `src/llamafactory`: **empty.**

| Property | Verdict |
|---|---|
| Governance · Authority · Ownership · Promotion · Review · Approval · Accountability · Immutable audit · Policy · Conflict handling | **Not Observed** |
| Provenance (reproducibility/artifact lineage) | **Observed (ML plane) / Not Observed (governance)** |
| Versioning (model/dataset revisions) | **Observed (artifact plane) / Not Observed (Knowledge-versioning sense)** |

[A] LlamaFactory is **governance-orthogonal**, like the retrieval/engine repos (#5/#7/#8) — a pure ML-training tool. Its "provenance/versioning" are reproducibility mechanisms (which model+data+config produced this artifact), a *different plane* from AIOS governance accountability.

## 17. Dangerous False Cognates

[E] | Term | LlamaFactory meaning | Collides with | Verdict |
|---|---|---|---|
| **Adapter** | Trainable LoRA low-rank **weight-delta** module (PEFT) | LangChain/Haystack `Adapter` = LM **I/O-format** boundary | **False cognate (dangerous — 2 prior senses)** |
| **Checkpoint** | Saved **model-weight** snapshot for resume | LangGraph `Checkpoint` = **graph-state** snapshot; AIOS Trace = accountability | **False cognate (dangerous — 3rd distinct sense in corpus)** |
| **Merge** | **Weight arithmetic** (fold ΔW into base) | VCS merge / AIOS conflict resolution | **False cognate (dangerous)** |
| **Template** | **Chat/conversation** format template | Prompt template | **Partially similar** |
| **Stage** | Training stage (pt/sft/rm/ppo/dpo) | AIOS Step/stage | **Vocabulary overlap only** |
| **Evaluation** | **Benchmark scoring** of a model | AIOS evaluation/verification | **Partially similar** |
| **Provenance** | Model/adapter/dataset **reproducibility lineage** | AIOS governance provenance | **Different-plane cognate** |
| **Reward / Preference** | RLHF reward model / preference pairs | *(no AIOS cognate)* | **Not observed (in AIOS)** |

[A] **Signature risk:** `Adapter`, `Checkpoint`, and `Merge` are *thrice-overloaded* across the corpus and AIOS. The lesson DR-1 already enforces: a term's meaning is **corpus-domain-dependent** and must be re-derived per repo, never carried across (see Methodology §).

## 18. AIOS Leakage Check

[E] **M-6 = 0.** Extraction (§§1–15) written in LlamaFactory-native ML-training terms; all overloaded terms quarantined to §17 and re-derived from source. **F-1 not triggered.**

## 19. Architecture Boundaries

[E] Boundaries: **config (hparams) ⟂ data pipeline ⟂ model/adapter ⟂ trainer(stage) ⟂ export/merge ⟂ eval ⟂ serving(api/chat/webui)**; the HF training internals and torch autograd are **outside** the wrapper; optional backends are **isolated per-requirement**; a **`v1/` restructure** is an emerging parallel boundary. Clean layering around a config-driven core.

## 20. Domain-Specific Terminology

[E] Native vocabulary (no AIOS mapping): SFT/DPO/KTO/PPO/RM/PT (training stages), LoRA/QLoRA/DoRA/PiSSA/OFT (adapter methods), quantization (bnb/GPTQ/AWQ/AQLM/HQQ/EETQ), DeepSpeed/FSDP (parallelism), GaLore/BAdam/APOLLO/Adam-mini (optimizers), Liger-Kernel/FlashAttention (kernels), packing/neat-packing, RoPE scaling, template, collator, reward model, preference dataset.

---

## Architecture Review (dispositions; No Adopt, No Reject)

| # | Finding (evidence) | Disposition | Justification (DM/PR) |
|---|---|---|---|
| LF1 | Per-feature optional-dependency isolation (`requirements/*.txt`) | **Already Present** | inv 12 (external dependency isolated) at fine granularity. Tenth corroboration; corroboration only, not authority. |
| LF2 | Config-driven unified training pipeline (dataclass args → stage dispatch over the HF stack) | **Scope-qualified Stronger** *(dimension: config-driven ML-training orchestration only)* | As a *declarative orchestration of a complex ML-training lifecycle*, it is more developed than anything AIOS models (AIOS does not train models). **Scope:** ML-training orchestration only; silent on governance. No global claim; No Adopt. |
| LF3 | Adapter (LoRA/QLoRA/full/freeze) architecture | **Different but Compatible** *(dangerous cognate)* | A weight-delta training mechanism; unrelated to AIOS. Must not be conflated with format-`Adapter` (#2/#5). |
| LF4 | Training checkpoints | **Different but Compatible** *(false cognate)* | Weight snapshots for resume; not AIOS Trace, not LangGraph state. |
| LF5 | Merge pipeline | **Different but Compatible** *(dangerous cognate)* | Weight arithmetic; not conflict/governance merge. |
| LF6 | Quantization | **Not Applicable** | No AIOS counterpart (precision engineering). |
| LF7 | Provenance (model/adapter/dataset lineage + revision pinning) | **Different but Compatible** *(different-plane)* | Reproducibility lineage (Observed), not governance provenance (Not Observed). A milder echo of Supabase's plane distinction. |
| LF8 | Experiment tracking (wandb/mlflow/swanlab) | **Different but Compatible** | ML run tracking for reproducibility, not governance audit. |
| LF9 | Evaluation pipeline | **Different but Compatible** | Benchmark scoring; not AIOS verification/governance review. |
| LF10 | Dataset lifecycle (load→align→template→tokenize→collate) | **Different but Compatible** | Data-prep pipeline; orthogonal to AIOS. |
| LF11 | AIOS-sense governance | **Not Observed** | Pure ML-training tool. |

[E] **Distribution:** Already-Present ×1, Different-but-Compatible ×7, **Scope-Stronger ×1 (LF2)**, Not-Applicable ×1, Not-Observed ×1. The one scope-verdict names a single dimension; no global claim; No Adopt, No Reject.

---

## Methodology Validation (DR-0 … DR-6)

- **DR-0** [E]: rejected "Adapter/Checkpoint/Merge/Provenance are AIOS concepts"; fixed the boundary (mature `src/llamafactory` vs emerging `v1/`; training internals in `transformers`/`torch` out of corpus).
- **DR-1** [E]: every claim reads from source; the empty governance scan grounds the "Not Observed" verdicts.
- **DR-2 / DR-3** [E]: dispositions tied to inv 12, inv 5/8 (versioning/provenance planes); ML terms re-derived, not assumed.
- **DR-4** [E]: domain-aware — ML-training domain, governance-orthogonal; scope-qualified Stronger (LF2) names one dimension.
- **DR-5** [E]: No Adopt, No Reject, no recommendation.
- **DR-6** [E]: nothing enacted; AIOS unchanged; reserved to Architect.
- [O] **New observation (not enacted, not promoted): cross-corpus polysemy.** `Adapter` (format vs weight-delta) and `Checkpoint` (graph-state vs model-weights) now carry **≥3 distinct corpus meanings**; the term's sense is **corpus-domain-dependent**. This confirms — as evidence, not a change — the standing DR-1 rule that meaning must be re-derived per repository and never carried across. **[O].**
- [A] **Limitations:** mature package only (`v1/` emerging, out of depth); training internals wrapped/out-of-corpus; single reviewer → reviewer-independence absent (Plan §9).

## Consistency Review (DR-6)

- [E] **Constitution / Domain Model / Principles Register:** unmodified; used only as references (inv 5, 8, 12 cited; provenance/versioning planes). No entity/relationship/invariant defined or redefined; the Adapter/Checkpoint/Merge/Template/Provenance collisions kept from blurring AIOS concepts.
- [E] **Validation Plan / prior reviews:** executed as specified; predecessors only comparators; **no synthesis, no cross-all-repo comparison**; log appended separately (prior entries untouched).

**No contradiction found. No canonical change. No adoption. No synthesis.**

---

## Summary and Stop

[E] **Repository #10 (LlamaFactory `llamafactory` 0.9.6.dev0, Apache-2.0) reviewed as external evidence, not authority**, via read-only extraction. LlamaFactory is an **LLM fine-tuning/training framework** — a config-driven unified wrapper over the HuggingFace stack covering the full adaptation lifecycle (dataset prep → pt/sft/rm/ppo/dpo/kto training → LoRA/QLoRA adapters → merge → quantize → export → eval), with per-feature optional-dependency isolation, artifact provenance/versioning, and experiment tracking. **Governance Review: all AIOS-sense governance is "Not Observed"** (provenance/versioning are Observed only on the ML reproducibility plane) — governance-orthogonal, like the retrieval/engine repos. Dispositions: 1 Already-Present, 7 Different-but-Compatible, **1 scope-Stronger (LF2 — config-driven ML-training orchestration)**, 1 Not-Applicable, 1 Not-Observed. **No Adopt, No Reject; AIOS changed by nothing.**

[E] **Method validation:** DR-0…DR-6 held on the ML-training domain; DR-1 re-derived the thrice-overloaded `Adapter`/`Checkpoint`/`Merge` terms from source (**M-6 = 0**). New observation (**cross-corpus polysemy** — meaning is corpus-domain-dependent) recorded **[O]** — not enacted, not promoted; methodology unchanged.

No implementation, code, schema, API, or subsystem was produced. No LlamaFactory design, API, or folder structure was copied. No AIOS canonical document was created or modified. No principle was promoted. No adoption/rejection decision was made. No governance event, reviewer identity, or Trace/Memory record was fabricated. Trace store unchanged (540 records); no `execution/` file touched by this read-only review.

**Stopping after the validation log update, per directive. Awaiting Architect authorization for Repository #11.** No synthesis, no cross-repository comparison performed.
