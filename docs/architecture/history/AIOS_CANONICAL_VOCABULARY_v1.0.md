# AIOS Canonical Vocabulary v1.0

**Status:** Canonical glossary — one authoritative definition per architectural term, to eliminate terminology drift.
**Version:** v1.0
**Authority:** Subordinate to the ratified Canonical Domain Model (whose entity definitions are restated here by citation, never altered) and Knowledge Architecture Blueprint v3 (whose settled vocabulary this glossary canonicalizes). Where the Domain Model already defines a term, that definition governs and is referenced, not competed with.

Format per term: definition · is / is-not · relationships · example · common mistake · reference.

---

### Identity
A stable logical correlation key shared by all records belonging to one logical entity. **Is:** a value carried by records. **Is not:** a stored parent record or entity of its own. **Relationships:** correlates Versions; derived facts about an identity come from aggregating its records. **Example:** an Agent Instance's `instance_id` across its Trace records; a Knowledge identity across its versions. **Common mistake:** modeling identity as a mutable master row — or assuming a key is stable when it is not (`memory_id` regenerates per extraction; Memory deliberately has no stable identity). **Ref:** Blueprint v3 Decision 1; Pattern P5.

### Version
One immutable, separately addressable record of an identity's content at a point in its history. **Is:** the only stored form of a versioned entity. **Is not:** an internal attribute, a diff, or an editable draft. **Relationships:** belongs to exactly one Identity; holds one lifecycle State and a Validity condition history. **Example:** a Knowledge version created by admission or revision. **Common mistake:** "updating" a version — change always means a new version. **Ref:** Blueprint v3 §2.1.

### Revision
The governed act of creating a new Version of an existing Identity, superseding the prior one. **Is:** an explicit, human-reviewed event producing a new record. **Is not:** an in-place edit, and not the same as Retraction (which has no successor). **Relationships:** produces a Version; transitions the prior Version to Superseded. **Example:** the Human Review `edit` decision's shape (original preserved, correction separate) applied at entity scale. **Common mistake:** conflating the *signal* that revision may be needed (a condition) with the *executed* revision (an event) — an explicitly open boundary (#5). **Ref:** Blueprint v3 §2.2.

### Promotion
Movement of content from a more volatile trust layer toward a more durable one, always through governed review. **Is:** a pipeline (candidate selection → human decision). **Is not:** automatic — invariant 8 forbids it. **Relationships:** consumes Memory; produces Candidates; feeds Admission. **Example:** `promotion.select_candidates()` → Human Review. **Common mistake:** letting ranking signals gate promotion (they may only prioritize — Pattern P13). **Ref:** Domain Model invariant 8; `promotion.py`.

### Admission
The specific governed decision that creates a Knowledge identity's first Version. **Is:** a separate decision layered on Human Review infrastructure (settled: Option B). **Is not:** the same act as candidate approval — a candidate `approve` retains its own meaning. **Relationships:** follows candidate Review; produces an Active, Confirmed Version. **Example:** none yet — no real admission has occurred. **Common mistake:** retroactively reinterpreting existing `approve` events as admissions. **Ref:** Blueprint v3 §2.9, Decision 10.

### Knowledge
Curated, canonical, reviewed, versioned, durable understanding (Domain Model §2 — that definition governs). **Is:** a cross-cutting Substrate entity, the output of governed review. **Is not:** a raw observation, a retrieval result, a cached fact, or Memory. **Relationships:** admitted from Candidates; versioned under an Identity; owned collectively with a Home Department accountable. **Example:** none yet exists in this repository. **Common mistake:** treating anything not yet through admission as Knowledge. **Ref:** Domain Model §2, §5, §6; Blueprint v3.

### Memory
A dynamic, provisional, retention-bounded record of what an Agent Instance encountered (Domain Model §2 governs). **Is:** derived, recomputed, deliberately without stable identity. **Is not:** durable, authoritative, or a source that may override Knowledge. **Relationships:** derived from Trace evidence; upstream of Promotion. **Example:** the 370 real `MemoryRecord`s recomputed from the Trace corpus. **Common mistake:** persisting or comparing `memory_id` across extractions. **Ref:** Domain Model §2, §6; `memory/extractor.py`.

### Trace
The immutable, append-only, unconditional audit record of one Agent Instance action (Domain Model §2/§2.1 governs). **Is:** the sole permanent source of truth for what happened. **Is not:** governed content itself, and never mutable. **Relationships:** everything derived (Memory, review state) recomputes from it. **Example:** the 540-record real corpus. **Common mistake:** any design requiring a Trace record to change. **Ref:** Domain Model invariants 4–6; `trace.py`.

### Condition
An evaluation attached to a record — what the system currently holds about it — orthogonal to lifecycle position. **Is:** the evaluation axis (Validity conditions; conflict). **Is not:** a lifecycle State. **Relationships:** set by governed review; proposable by detection. **Example:** Questioned; a conflict flag. **Common mistake:** encoding a condition as a state ("Retracted" as a lifecycle state — rejected). **Ref:** State/Condition Separation Principle, Blueprint v3 §3.

### State
A record's lifecycle position in its identity's history. **Is:** Active or Superseded (for Knowledge v1). **Is not:** an evaluation or trust judgment. **Relationships:** transitions only via governed events (Revision). **Example:** a version becoming Superseded when revised. **Common mistake:** adding states to express evaluation (Archived, Retracted — both rejected for v1). **Ref:** Blueprint v3 §2.2.

### Lifecycle
The ordered set of States and governed transitions an entity's records move through. **Is:** the position dimension over time. **Is not:** the validity dimension. **Relationships:** every transition produces a Trace record. **Example:** Candidate → Admitted/Active → Superseded. **Common mistake:** designing rich lifecycles ahead of evidence (8 explored states collapsed to 2). **Ref:** Blueprint v3 §2.2; Domain Model §6.

### Validity
The epistemic condition of a specific Version: Confirmed, Questioned, or Invalidated. **Is:** an orthogonal evaluation axis. **Is not:** a lifecycle state; not automatic. **Relationships:** transitions are governed human decisions; detection may propose Questioned. **Example:** a version Invalidated while still lifecycle-Active (retraction). **Common mistake:** binary valid/invalid thinking — the Questioned interval is where governance actually operates. **Ref:** Blueprint v3 §2.3.

### Conflict
The preserved condition of different Knowledge identities holding contradicting claims without sufficient evidence to resolve. **Is:** inter-identity; a condition, never a state; always surfaced. **Is not:** supersession (intra-identity) and not Invalidity (a settled judgment about one version). **Relationships:** may eventually lead to a governed invalidation. **Example:** none real yet — zero organic conflicts across four corpus scans. **Common mistake:** merging conflict-resolution with supersession mechanics. **Ref:** Blueprint v3 §2.7.

### Repository
The append-only, versioned store of Knowledge Versions. **Is:** a storage discipline (immutable records, no in-place change). **Is not:** yet implemented; not a mutable database of current-state rows. **Relationships:** holds Versions; consulted by Retrieval. **Example:** none yet. **Common mistake:** designing it before version-addressing was settled (now settled — Decision 1). **Ref:** Blueprint v3 Decision 4.

### Retrieval
The act of finding and returning Knowledge (or documents) relevant to a query. **Is:** a consumer evaluating two independent dimensions (State, Validity). **Is not:** itself Knowledge, and never an authority on truth. **Relationships:** reads Repository; visibility policy explicitly open (#6). **Example:** the dormant `execution/knowledge/retrieval.py` prototype (documents only, zero real consumers). **Common mistake:** letting retrieval ranking imply epistemic endorsement. **Ref:** Blueprint v3 §2.8.

### Evidence
A single recorded finding produced by a real execution — the smallest unit in the derivation chain. **Is:** structured fact inside a Trace record's outputs. **Is not:** reviewed, and not itself Memory or Knowledge. **Relationships:** aggregated into Memory; cited by Provenance. **Example:** `{"source": "tool", "kind": "cross_reference_check", "resolved": false, ...}`. **Common mistake:** treating heuristic evidence as equivalent to tool evidence without the source distinction. **Ref:** `skill.py` Evidence dataclass; P8.

### Observation
What an execution encountered, as captured in Evidence — the pre-Memory raw fact. **Is:** the content of an evidence entry (kind + detail). **Is not:** a governance judgment. **Relationships:** deduplicated Observations become Memory. **Example:** "§9 not found anywhere in cited.md". **Common mistake:** using "observation" and "memory" interchangeably — Memory is the aggregated, deduplicated derivative. **Ref:** `memory/extractor.py`.

### Provenance
The verifiable chain from any derived artifact back to its real sources. **Is:** recorded identifiers plus captured snapshots at each derivation step. **Is not:** optional metadata; and a live reference is not provenance (capture, don't reference). **Relationships:** spans Trace → Memory → Candidate → Decision → (future) Knowledge. **Example:** `Provenance(memory_id, trace_ids, agent_definition_name, department_status)`. **Common mistake:** treating generational absence of a field as a conflict (the fingerprint lesson). **Ref:** P7, P8.

### Ownership
Accountability for an artifact, per the Domain Model's ownership rules (§5 governs). **Is:** answerability and curation duty. **Is not:** exclusive access or restriction rights — Knowledge remains cross-cutting (§8). **Relationships:** Home Department owns accountability; Organization owns collectively. **Example:** Home Department as first responder for a Knowledge item. **Common mistake:** reading "owner" as "gatekeeper." **Ref:** Domain Model §5, §8; Blueprint v3 §2.6.

### Authority
The right to make a specific governed decision. **Is:** scoped, explicit, and human-held for all governance decisions. **Is not:** derived from automation, and not implied by ownership alone (Reviewer ≠ owner). **Relationships:** exercised through Review; recorded in Trace. **Example:** invalidation authority = Human Reviewer acting under Home Department authority. **Common mistake:** treating a hook, score, or automated signal as authorization (Constitution §6.2 invariant 2 forbids it). **Ref:** Blueprint v3 §2.6.

### Review
The governed human evaluation of a candidate or version, producing a recorded decision. **Is:** the exclusive path for all promotion/admission/invalidation. **Is not:** computable — the contract structurally cannot produce a verdict. **Relationships:** consumes a snapshot; produces a Trace-recorded decision. **Example:** the 6 real `human_review_decision_recorded` events. **Common mistake:** letting any code path recommend an outcome to the reviewer. **Ref:** `review_decision.py`; P3, P9.

### Approval
The candidate-review decision (`approve`) that an evidence package is fit to retain as a governance record. **Is:** one of three candidate decisions (approve/reject/edit). **Is not:** Knowledge Admission (settled: separate decisions) and not a claim the content is externally verified — real reviewer rationale consistently drew this line. **Relationships:** prerequisite to Admission under the settled model. **Example:** 4 real approve events. **Common mistake:** collapsing approval into admission (rejected Option A). **Ref:** Blueprint v3 Decision 10.

### Retraction
The governed event of determining an admitted Version untrustworthy with no replacement. **Is:** a validity event — the version becomes Invalidated while remaining lifecycle-Active. **Is not:** a lifecycle state, a deletion, or a Revision. **Relationships:** produces an invalidation decision record; preserves all history. **Example:** none yet. **Common mistake:** modeling it as a "Retracted" state (rejected). **Ref:** Blueprint v3 §2.4, Decision 3.

### Superseded
The lifecycle State of a Version replaced by a newer Version of the same Identity. **Is:** a position fact ("no longer current"). **Is not:** a judgment the version was wrong — a Superseded version may have been perfectly valid when current. **Relationships:** entered only via Revision. **Example:** the prior version after any revision. **Common mistake:** using Superseded to express invalidity (that is the validity axis) or conflict resolution (inter-identity). **Ref:** Blueprint v3 §2.2.

### Questioned
The Validity condition of a Version facing real challenging evidence with no governed determination yet made. **Is:** the honest intermediate condition; proposable by detection, settable only by humans (pending open question #8's mechanics). **Is not:** Invalidated, and not a lifecycle state. **Relationships:** transitions to Confirmed or Invalidated via review. **Example:** none yet. **Common mistake:** letting it become a permanent parking state (a tracked risk). **Ref:** Blueprint v3 §2.3.

### Confirmed
The default Validity condition of an admitted Version: governed review found its evidence sufficient at decision time. **Is:** an evaluation on record. **Is not:** a claim of external/absolute truth — the same line real reviewers drew for approval. **Relationships:** may transition to Questioned upon new evidence. **Example:** the default condition of any future first admission. **Common mistake:** reading Confirmed as immune to challenge. **Ref:** Blueprint v3 §2.3.

### Invalidated
The Validity condition of a Version determined, by evidence-backed governed review, to be no longer trustworthy. **Is:** a settled epistemic judgment about one specific version. **Is not:** a deletion, a lifecycle state, or a Conflict (which is unresolved and inter-identity). **Relationships:** set by a Human Reviewer under Home Department authority; permanent record. **Example:** none yet. **Common mistake:** conflating with Superseded. **Ref:** Blueprint v3 §2.3–§2.4.

### Capability
A stable, named, outcome-oriented contract owned by exactly one Department (Domain Model §2 governs). **Is:** the unit persisting across model/vendor/Agent change. **Is not:** implemented anywhere in the Execution Layer yet. **Relationships:** implemented by Agent Definitions; dependency-governed by invariants 9–11. **Example:** none in code. **Common mistake:** extending Capability-scoped invariants (e.g. invariant 10) to other entities by analogy — explicitly rejected for Knowledge conflicts. **Ref:** Domain Model §2, §5.

### Workflow
An explicit, inspectable composition of Skills accomplishing a multi-step outcome (Domain Model §2 governs). **Is:** loaded from its governance document; document order = execution order (disclosed implementation choice). **Is not:** a scheduler or retry engine. **Relationships:** contains Skills; authorized per Agent Definition. **Example:** `workflow.pre-ratification-validation`. **Ref:** Domain Model §2; `workflow.py`.

### Skill
A discrete, reusable, bounded unit of executable ability (Domain Model §2 governs). **Is:** invoked by an Agent Instance through a Workflow; the only path to Tool invocation. **Is not:** a Tool (no external dependency) and not an Agent. **Relationships:** permitted per Agent Definition; produces Evidence. **Example:** `skill.citation-discipline-verification`. **Ref:** Domain Model §2; `skill.py`.

### Runtime
The execution substrate hosting Agent Instances (Domain Model §2 governs). **Is:** the model/infrastructure substitution seam; binding is checked, never guessed. **Is not:** an Agent or a Workflow engine. **Relationships:** hosts Agent Instances; recorded in every Trace record. **Example:** `runtime.batch-governance-review-substrate`. **Ref:** Domain Model §2; `runtime.py`.
