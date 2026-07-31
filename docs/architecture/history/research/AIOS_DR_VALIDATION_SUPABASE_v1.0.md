# AIOS Decision Review Methodology — External Corpus Validation: Supabase v1.0

**Program:** External Repository Validation Program — Repository #9.
**Executes:** `AIOS_DECISION_REVIEW_METHOD_VALIDATION_PLAN_v1.0`.
**Corpus item:** `supabase/supabase` (Apache-2.0), cloned read-only from the official public repository at HEAD `b76d04d6` (2026-07-23). Predecessors: DSPy (#1), LangChain (#2), OpenHands (#3), Letta (#4), Haystack (#5), CrewAI (#6), LlamaIndex (#7), LangGraph (#8).
**Status:** External-evidence review only. Additive. Creates no canonical document, modifies none, redesigns nothing, implements nothing, promotes no principle. **No Adopt, No Reject** (established discipline). Does not copy Supabase design, API, folder structure, or implementation.
**Authority posture:** Supabase is **external evidence, not authority** (Validation Plan §2). Predecessors used **only as methodology comparators**, never as authority.
**Methodology discipline:** DR-0…DR-6 **frozen**; applied unchanged. Weaknesses recorded as candidate refinements **[O]**, never enacted, never promoted. **No synthesis, no cross-repository comparison** (directive).
**Principles applied:** PR-1 Evidence First · PR-3 Detect Don't Decide · PR-4 Fail Closed · PR-5 Capture Don't Reference.
**Corpus provenance (DR-1 honesty):** read-only `git clone` of the official public repo; scratch only (`/tmp`); nothing written to AIOS.
**Confidence:** **[E]** direct observation · **[A]** reasoned inference · **[O]** open question. Single reviewer → reviewer-independence **[O]**, reserved to the Architect (Plan §9).

---

## 0. DR-0 — Premise & Boundary (critical for this corpus)

[E] **The first non-LLM, non-agent corpus item:** Supabase is a **Postgres-centric backend-as-a-service platform** (database + auth + storage + realtime + edge functions). This breaks the prior domain pattern and is the first repo with *genuine* authorization/access-control as core architecture — so the false-cognate risk is **inverted**: the governance-family words here (policy, authorization, role, audit, authority) name **real mechanisms**, not empty vocabulary. The premise to reject is *"Supabase's governance-family mechanisms are AIOS governance."* They are real — but operate on a **different plane** (see §18/§19).

[E] **Corpus-boundary honesty (DR-1):** the `supabase/supabase` repo is **not** the platform's service implementations. It is primarily: **Studio** (the dashboard, `apps/studio` ~53 MB TS/React), **docs** (`apps/docs`, MDX guides), **`packages/pg-meta`** (the Postgres introspection/management abstraction), and the **self-hosting orchestration** (`docker/docker-compose.yml`) plus a local project scaffold (`supabase/` with migrations/functions/buckets). The **services** — `gotrue` (auth), `postgrest` (REST/RLS), `realtime`, `storage-api`, `supavisor` (pooler), `edge-runtime` — are **separate repositories pulled as pinned Docker images**. Therefore the platform architecture (RLS, auth, realtime, storage, edge) is **observed via configuration + documentation + the pg-meta management layer**, while service *internals* are **out of corpus** and not extrapolated.

---

## 1. System Architecture

[E] From `docker/docker-compose.yml` (pinned service images): **Postgres at the center** (`supabase/postgres:17.6.1.136`), fronted by a **Kong** API gateway (`kong:3.9.1`), with satellite services: **auth/GoTrue** (`gotrue:v2.189.0`), **REST/PostgREST** (`postgrest:v14.12`), **Realtime** (`realtime:v2.102.3`), **Storage** (`storage-api:v1.60.4` + `imgproxy`), **Edge Functions** (`edge-runtime:v1.74.0`), **postgres-meta** (`postgres-meta:v0.96.6`), **Supavisor** connection pooler (`supavisor:2.9.5`), and **Studio** (`studio:2026.07.07`). Architecture pattern: **the database is the source of truth; services project it** (REST, realtime, storage) and enforce access via Postgres roles + RLS driven by JWT.

## 2. Service Boundaries

[E] Each capability is an **independently-versioned service** behind the Kong gateway; they share the Postgres instance and a common JWT secret. Boundaries are **process/container boundaries** with the DB as the shared substrate. Studio talks to services and to `postgres-meta` for DB management.

## 3. Storage Architecture

[E] Two senses: (a) **object storage** — `storage-api` (S3-backed) with per-object access governed by RLS + `buckets`; (b) **data storage** — Postgres itself. Local project scaffold has `supabase/buckets` and `supabase/seed.sql`. Storage internals are out of corpus (separate repo).

## 4. Database Abstractions

[E] `packages/pg-meta` is the in-repo **DB abstraction**: typed modules introspecting/managing Postgres catalogs — `pg-meta-tables`, `-columns`, `-functions` (with volatility `IMMUTABLE/STABLE/VOLATILE`), `-extensions`, `-policies`, `-roles`, `-table-privileges`, `-column-privileges`, `-triggers`, `-foreign-tables`. It generates safe SQL (`pg-format`, `safeSql`) for Studio to read/modify schema.

## 5. Authentication

[E] **GoTrue** (`supabase-auth`) issues JWTs; `AUTH_JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY` (symmetric and asymmetric variants observed). Identity → signed JWT with claims. Implementation out of corpus; configuration + docs observed.

## 6. Authorization

[E] **JWT claims → Postgres role → privileges + RLS.** Three canonical roles: `anon`, `authenticated`, `service_role` (the last a `GOTRUE_JWT_ADMIN_ROLES`). Table/column privileges (`pg-meta-table-privileges`, `-column-privileges`) plus RLS policies constitute the authorization model. This is a **genuine, fine-grained, data-plane authorization system**.

## 7. Row Level Security (RLS)

[E] `pg-meta-policies.ts`: a policy has `schema`, `table`, `roles: string[]`, `command` (SELECT/INSERT/UPDATE/DELETE/ALL), `definition` (the `USING` read predicate), `check` (the `WITH CHECK` write predicate), `permissive`. RLS = **per-table, per-command, per-role SQL predicates that filter/authorize rows** — enforced in Postgres, so every projecting service inherits it. This is the platform's core access-control primitive.

## 8. Realtime Subsystem

[E] `supabase-realtime` streams Postgres changes (CDC/logical replication) to subscribed clients over websockets, **respecting RLS**. Internals out of corpus; role/config observed.

## 9. Storage Subsystem

[E] `storage-api` + `imgproxy`: object storage with bucket/object RLS and image transformation. Internals out of corpus.

## 10. Edge Functions

[E] `edge-runtime` (Deno) runs user functions at the edge; local scaffold `supabase/functions/`. A serverless compute layer beside the DB. Internals out of corpus.

## 11. API Layer

[E] **Kong gateway** routes to services; **PostgREST** auto-generates a RESTful API directly from the Postgres schema (tables/views/functions → endpoints), with RLS enforced per request via the caller's JWT role. The API is a **projection of the database schema**.

## 12. Extension Mechanism

[E] Two: (a) **Postgres extensions** (`pg-meta-extensions` manages install/enable — e.g. pgvector, pg_cron, etc.); (b) **Edge Functions** (custom compute). Extensibility is DB-native + serverless.

## 13. Multi-tenant Model

[E] In the OSS/self-host repo, tenancy is **per-Postgres-instance** with **RLS-based row isolation** (`auth.uid()`-scoped policies) and, in Studio, an **organization/project** hierarchy (`apps/studio/data/organizations`). Hosted multi-project isolation is a platform concern out of corpus.

## 14. Migration / Versioning

[E] `supabase/migrations/` — **timestamp-prefixed, ordered SQL migration files** (e.g. `20230126220613_doc_embeddings.sql`), applied forward. Versioning = ordered schema migrations (change history), not entity/knowledge versioning.

## 15. Observability

[E] Studio surfaces logs/reports; the platform ships a Logflare/analytics service (full compose) and **audit logs** (`apps/studio/data/misc/audit-login-mutation.ts` — "add login event to user's audit log"; `organizations/organization-audit-logs-query.ts` — org audit logs, microsecond timestamps). Audit-log **data** is generated by the platform API and **queried** by Studio (not implemented in this repo).

## 16. Dependency Isolation

[E] Services are **independently-versioned, separately-repo'd, pinned Docker images**; the monorepo isolates shared code into `packages/*`. Strong process-level isolation.

## 17. Vendor Boundary

[E] The DB is `supabase/postgres` (Postgres + curated extensions); external vendor coupling (S3 for storage, etc.) is behind service boundaries. No single-vendor LLM coupling (not an LLM framework).

## 18. Governance Concepts (Observed / Not Observed)

[E] **"Observed"/"Not Observed" = presence in the corpus, never a deficiency.** Supabase yields more "Observed" than any prior repo — but **all at the data-access-security plane**, which is a *different plane* from AIOS's decision/knowledge governance.

| Property | Verdict | Evidence / plane |
|---|---|---|
| Governance | **Observed (data-access plane) / Not Observed (AIOS decision-plane)** | RLS/roles/privileges govern *data access*; no decision/knowledge governance |
| Authority | **Observed (data-access plane)** | Postgres RBAC roles (`anon`/`authenticated`/`service_role`); role hierarchy — but not architecture-decision authority |
| Ownership | **Observed (data plane)** | Row ownership via RLS (`auth.uid() = user_id`), object/bucket ownership, org/project ownership — not AIOS entity ownership |
| Promotion | **Not Observed** | Migrations are *applied forward*, not human-*promoted* via governed review; no Memory→Knowledge analog |
| Review | **Not Observed (as governance)** | No architectural governance review |
| Approval | **Not Observed (as governance)** | No governance approval gate (auth is authentication, not decision approval) |
| Accountability | **Observed (activity plane)** | Audit logs (login/org activity), microsecond-stamped — but platform-managed, queried-not-implemented here |
| Immutable audit | **Not Observed (by guarantee)** | Audit *logs* exist and migrations are ordered/forward, but no contractual immutable-append-only-per-governed-action ledger in the AIOS sense |
| Provenance | **Not Observed (as governance)** | Activity lineage via audit logs; no governance provenance |
| Policy | **Observed (data-access plane)** | RLS *policies* — genuine access-control policy, not decision-governance policy |

[A] **The plane distinction is the whole finding:** Supabase has a **real, mature governance sub-system — for data access** (authentication, authorization, RLS, roles, ownership, activity audit). AIOS governance is a **different plane** — accountability for governed *actions* (immutable per-action Trace, inv 4/5), human-*promotion* of Memory→Knowledge (inv 8), and ratified *authority tiers over architecture* (Constitution §3). Same word-family, **orthogonal planes.**

## 19. Dangerous False Cognates

[E] | Term | Supabase meaning | vs AIOS | Verdict |
|---|---|---|---|
| **Policy** | RLS SQL row predicate (USING/WITH CHECK) | Decision/knowledge governance policy | **Different-plane cognate (dangerous)** — real policy, different plane |
| **Authorization** | JWT→role→RLS data access | Governance authority over decisions/architecture | **Different-plane cognate (dangerous)** |
| **Role** | Postgres RBAC principal (anon/authenticated/service_role) | Department/Agent-Definition-scoped authority | **Partially similar** — a genuine authority role, but data-plane (contrast CrewAI `Role`=persona, which was a *false* cognate) |
| **Authority** | Role/privilege hierarchy | Ratified architectural authority tiers | **Different-plane cognate** |
| **Audit (log)** | Login/org activity log (platform-managed) | Immutable per-governed-action accountability ledger (inv 4/5) | **Different-plane cognate (dangerous — nearest real "audit")** |
| **Migration/Versioning** | Ordered forward SQL schema migrations | Knowledge versioned identity (Blueprint v3) | **False cognate** — schema change history, not knowledge versioning |
| **Realtime/Storage/Edge** | Infrastructure subsystems | *(no AIOS counterpart)* | **Not observed (in AIOS)** |

[A] **The signature risk of this corpus:** because the mechanisms are *genuine governance-family systems*, the temptation is to score them "Already Present" against AIOS governance. DR-1 + the plane distinction prevent that: they are Present **as data-access security**, absent **as AIOS decision/knowledge governance**.

## 20. AIOS Leakage Check

[E] **M-6 = 0.** Extraction (§§1–17) written in Supabase-native terms (RLS/roles/JWT/audit-log/migrations). The plane distinction is quarantined to §§18–19. **The inverted risk (real mechanisms, not empty words) was handled by the "same-family, different-plane" discrimination**, not by importing AIOS meaning. **F-1 not triggered.**

---

## Architecture Review (dispositions; No Adopt, No Reject)

Dispositions: **Already Present · Different but Compatible · Scope-qualified Stronger · Scope-qualified Weaker · Not Applicable.**

| # | Finding (evidence) | Disposition | Justification (DM/PR) |
|---|---|---|---|
| SB1 | Services as independently-versioned, isolated pinned images behind a gateway | **Already Present** | Analogous to inv 12 (external dependency isolated) at the *service* granularity. Ninth corroboration; different mechanism (containers). Corroboration only, not authority. |
| SB2 | **RLS + roles = fine-grained runtime data-access authorization** | **Scope-qualified Stronger** *(dimension: runtime data-access authorization only)* | **The corpus's first genuine authorization mechanism.** On the narrow dimension of *per-row/per-command/per-role runtime data access*, Supabase does something AIOS does not model at the data layer. **Scope:** data-access authority only; **silent on** decision/knowledge governance, immutable per-action Trace (inv 4), human promotion (inv 8). No global claim; No Adopt. |
| SB3 | Activity **audit logs** (login/org) | **Scope-qualified Weaker** *(dimension: immutable governed-action accountability only)* | Nearest real "audit" in the corpus, yet a **mutable, platform-managed activity log** (queried-not-implemented here) — not an immutable append-only per-*governed-action* ledger (inv 4/5, §14.2). Weaker strictly on *governed-action immutable accountability*; says nothing about its data-security strengths. |
| SB4 | Ordered forward SQL **migrations** | **Different but Compatible** | Schema change history; not Knowledge versioned identity (Blueprint v3). No conflict. |
| SB5 | **Authentication** (GoTrue/JWT identity) | **Not Applicable** | AIOS models no authentication layer; identity is a separate concern. |
| SB6 | **Multi-tenant** (RLS row isolation + org/project) | **Different but Compatible** | Data-isolation model; orthogonal to AIOS Organization/Department governance. |
| SB7 | Postgres-centric service architecture (DB as source of truth; services project it) | **Different but Compatible** | A mature platform architecture; orthogonal to AIOS's governance model. |
| SB8 | Realtime / Storage / Edge subsystems | **Not Applicable** | Infrastructure subsystems; no AIOS counterpart. |
| SB9 | `pg-meta` DB introspection/management abstraction | **Different but Compatible** | Operational DB tooling. |
| SB10 | Extension mechanism (Postgres extensions + edge functions) | **Different but Compatible** | DB-native + serverless extensibility. |
| SB11 | AIOS-sense governance (immutable decision audit, Memory→Knowledge promotion, ratified authority tiers over architecture) | **Not Observed** | Supabase governs data access, not decisions/knowledge/architecture. |

[E] **Distribution:** Already-Present ×1, Different-but-Compatible ×5, **Scope-Stronger ×1 (SB2)**, **Scope-Weaker ×1 (SB3)**, Not-Applicable ×2, Not-Observed ×1. Both scope-verdicts name one exact dimension; no global claim; No Adopt, No Reject.

---

## Methodology Validation (DR-0 … DR-6)

- **DR-0** [E]: rejected the domain-shift premise (first non-LLM repo) and, decisively, the *"real governance-family words ⇒ AIOS governance"* premise; fixed the corpus boundary (Studio/docs/pg-meta/orchestration in-repo; services out).
- **DR-1** [E]: every claim reads from source/config/docs; the in-repo/out-of-corpus split is stated explicitly for each subsystem.
- **DR-2 / DR-3** [E]: dispositions tied to inv 4/5, 8, 12, §14.2, Constitution §3; the plane distinction is the core canonical evaluation.
- **DR-4** [E]: remained domain-aware — distinguished **data-access governance (present)** from **AIOS decision/knowledge governance (not observed)**; scope-qualified Stronger (SB2) and Weaker (SB3) each name one dimension.
- **DR-5** [E]: No Adopt, No Reject, no recommendation.
- **DR-6** [E]: nothing enacted; AIOS unchanged; reserved to Architect.
- [O] **New observation (not enacted, not promoted): the "different-plane cognate."** Unlike every prior cognate species (name-only, structural, inversion, lexical, authority-word, structural-index, rewritable-history), Supabase's policy/authorization/role/audit are **genuine governance-family mechanisms on a different plane** (data-access security vs decision/knowledge governance). DR-4 needed a *plane* distinction, not a *falseness* distinction. Extends the cognate taxonomy with its first "real-but-different-plane" case. **[O].**
- [A] **Limitations:** platform services out of corpus (biggest boundary gap in the program — much architecture is observed via config/docs, not implementation); huge monorepo (depth prioritized on the 20 targets); single reviewer → reviewer-independence absent (Plan §9).

## Consistency Review (DR-6)

- [E] **Constitution / Domain Model / Principles Register:** unmodified; used only as references (inv 4/5/8/12, §14.2, Constitution §3, PR-5 cited). No entity/relationship/invariant defined or redefined; the Policy/Authorization/Role/Authority/Audit word-collisions kept from blurring AIOS governance via the plane distinction.
- [E] **Validation Plan / prior reviews:** executed as specified; predecessors only comparators; **no synthesis, no cross-all-repo comparison**; log appended separately (prior entries untouched).

**No contradiction found. No canonical change. No adoption. No synthesis.**

---

## Summary and Stop

[E] **Repository #9 (Supabase, Apache-2.0, HEAD `b76d04d6`) reviewed as external evidence, not authority**, via read-only clone. Supabase is a **Postgres-centric backend-as-a-service platform** — the first non-LLM corpus item and the first with *genuine* authorization as core architecture (JWT auth → Postgres roles → **RLS** row-access policies, activity **audit logs**, ordered SQL **migrations**, multi-tenant RLS isolation). **DR-1 boundary:** this repo is Studio + docs + `pg-meta` + self-hosting orchestration; the services (auth/rest/realtime/storage/edge) are separate repos as pinned images, so platform architecture is observed via config/docs, internals out of corpus. **Governance Review:** governance-family properties are **Observed at the data-access-security plane** (policy, authorization, role, ownership, activity audit) but **Not Observed at AIOS's decision/knowledge plane** (immutable per-governed-action accountability, Memory→Knowledge promotion, ratified authority tiers). Dispositions: 1 Already-Present, 5 Different-but-Compatible, **1 scope-Stronger (SB2 — runtime data-access authorization via RLS)**, **1 scope-Weaker (SB3 — immutable governed-action accountability)**, 2 Not-Applicable, 1 Not-Observed. **No Adopt, No Reject; AIOS changed by nothing.**

[E] **Method validation:** DR-0…DR-6 held on a genuinely different domain with *inverted* cognate risk (real mechanisms, not empty words); DR-4 distinguished **same-governance-family, different-plane** rather than false-vs-real. **M-6 leakage = 0.** New observation (**different-plane cognate**) recorded **[O]** — not enacted, not promoted; methodology unchanged.

No implementation, code, schema, API, or subsystem was produced. No Supabase design, API, or folder structure was copied. No AIOS canonical document was created or modified. No principle was promoted. No adoption/rejection decision was made. No governance event, reviewer identity, or Trace/Memory record was fabricated. Trace store unchanged (540 records); no `execution/` file touched by this read-only review.

**Stopping after the validation log update, per directive. Awaiting Architect authorization for Repository #10.** No synthesis, no cross-repository comparison performed.
