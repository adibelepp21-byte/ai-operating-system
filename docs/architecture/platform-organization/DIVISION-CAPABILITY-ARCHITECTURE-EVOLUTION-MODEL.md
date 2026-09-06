# Platform Division — Capability, Architecture & Evolution Model

> **Status: DERIVED from canonical source.** Constructed 2026-09-06, Cycle 22,
> under `ACT-CC-P10-CONSTRUCTION-EXECUTION v2.0 §13`, `§15`, `§17`.
> Authority: `FDE-P10-AUTONOMOUS-EXECUTION-01` Decision B;
> `DEL-T4.4-CF-001 §3.1 A/C`.
>
> Third companion to `DIVISION-OWNERSHIP-MODEL.md` and
> `DIVISION-LIFECYCLE-AND-AUTHORITY-MODEL.md`. **Model level, assigning
> nothing.**
>
> **Primary source:** `canonical-domain-model-v1.md §7`–`§10`, previously
> unread. Precedence 2 under `Engineering Constitution §4`.

---

# Part A — Capability

## 1. Capability creation is architect-restricted, and the restriction is deliberate

**[A] `Domain Model §10` Architectural Backlog, *Autonomous Capability
Creation*, verbatim:**

> *"Capability creation is **intentionally, not accidentally, restricted to
> architect-approved decisions** under the current governance model. **This is a
> deliberate constraint for the foreseeable future, not a gap.**"*

The same row records when it would change: *"Needed only if AIOS moves toward
higher autonomy where an Agent may need to **propose** new Capabilities rather
than operate solely within architect-defined ones."*

**This is the most direct statement in canon of the boundary this corpus has
operated under for twenty-two cycles.** The restriction is not an omission
awaiting repair, and constructing Capabilities autonomously would not be filling
a gap — it would be crossing a constraint the Domain Model declares deliberate.

**Note the verb.** Even under the future higher-autonomy condition, the Domain
Model contemplates an Agent that may ***propose*** new Capabilities. **Propose,
not create.** `Recommendation ≠ Decision` appears here in canonical text.

## 2. The fifteen invariants, and how this corpus has been citing them

**[E] Verified.** `Domain Model §7` states **fifteen** invariants as a numbered
list, `1.`–`15.` **The token `INV-` does not occur anywhere in the Canonical
Domain Model** — the `INV-n` notation is introduced by
`AIOS_ARCHITECTURE_FREEZE_v1.0.md §3`, which presents them as *"quoted verbatim
from the ratified Canonical Domain Model §7."*

**Two consequences, both material.**

**(a) The Freeze's "verbatim" is no longer literal, and correctly so.**
`Domain Model §7` invariant 10 now reads:

> *"**Cross-Platform-Division** Capability dependencies require governance
> approval through the Decision-Making Process — never silent adoption."*

`Freeze §3` quotes it as *"**Cross-Department** Capability dependencies…"*.
Invariants 1 and 2 diverge the same way (*Platform Division* vs *Department*).

**This is `ADR-0010` working as designed, not a defect.** `ADR-0010` amended the
Domain Model in exactly five locations and states *"nothing else in the
repository may change under this ADR."* The Freeze therefore retains the
historical wording, and **must**. **No correction is proposed, and a future
reader should not "fix" the Freeze** — doing so would exceed `ADR-0010` and
mutate a frozen artifact.

**(b) The `Constitution §6.1` gap is now identified by invariant, not by count.**
`Constitution §6.1` binds *"invariants 1–14"*. `Domain Model §7` carries
**fifteen**. The unbound one is **invariant 15**:

> *"An Agent Definition may specify zero or more Skills and zero or more
> Workflows. An empty Skill declaration, an empty Workflow declaration, or both
> empty declarations represent a valid architectural state. **No minimum
> cardinality is required for either relationship.**"*

**Previously escalated as a count discrepancy; now escalated as a specific
identified invariant.** Amendment authority is `Constitution §16`, Architect-
exclusive and non-delegable, so **no repair is attempted.**

## 3. Invariant 11 — the dependency graph must be observable

**[C]** `Domain Model §7` invariant 11, not previously recorded in this corpus:

> *"The full graph of Capability dependencies must remain **queryable and
> observable at all times** — no undocumented dependencies."*

**This is a positive obligation, and it bears directly on `G-05`.** The five
derived inter-PD edges are not merely unapproved (`INV-10`), in a category
outside the freeze (`Freeze §6`), and Architect-reserved (`Freeze §2`) — the
model also requires that whatever the true dependency graph is, it be
**documented and queryable**.

**The obligation is not currently violable by this corpus**, because no
Capability is assigned to any Division and therefore no Capability-to-Capability
dependency exists to document. It becomes live at the moment `G-09` resolves.

## 4. Contract is not a separate entity

**[A] `Domain Model §9` Explicit Non-Goals:** *"**Contract** as a separate
entity — **carried entirely within Capability's own definition**."*

Invariant 9 requires every Capability-to-Capability dependency to *"reference a
specific versioned contract."* **The contract it references lives inside the
Capability definition** — there is no `Contract` entity to construct, and
constructing one would create an unratified thirteenth entity (`Freeze §4`:
*"No new entity."*).

---

# Part B — Architecture

## 5. The Spine is three levels, and may not be deepened

**[C] `Domain Model §8` Architectural Boundaries:**

> *"The Spine is intentionally shallow (**three levels**) and is **not to be
> deepened or bypassed without an architectural decision**."*

```text
Organization  →  Platform Division  →  Capability
```

**This constrains a construction the Encyclopedia contemplates.** `E-56` records
that PD-03's `Part A / A6` *"does not establish: Sub Divisions; Capabilities;
Teams; Role Groups; reporting hierarchy"*, assigning them to *"later
architecture layers."*

**A Sub Division would be a fourth Spine level.** `Domain Model §8` places that
behind an architectural decision. **Recorded as a constraint on any future
Sub Division work; no Sub Division is constructed, proposed, or assumed here.**

## 6. Substrate is not private to any division — a qualification to the Ownership Model

**[C] `Domain Model §8`:**

> *"Substrate entities are cross-cutting and addressable from any point in the
> Spine or Execution layer — they are **not owned by, or private to, any single
> Platform Division**, Capability, or Agent."*

`DIVISION-OWNERSHIP-MODEL.md §1` records from `Freeze §4` that Knowledge is
owned *"collectively by the Organization, each item with a home Department"*.

**Both are true and the pairing is the point.** `Domain Model §5` says each
Knowledge item *"has a home Platform Division"*; `§8` says substrate is not
owned by or **private to** any single Division.

```text
home  ≠  ownership  ≠  privacy
```

**A home Division is a locus of accountability, not a boundary of access.** The
Ownership Model said `home ≠ ownership`; `§8` adds the third term. **Recorded as
a strengthening of that model, not a correction to it** — no statement in it
becomes wrong.

## 7. Only Runtime and Tool may name external technology

**[C] `Domain Model §8`:** *"Runtime and Tool are the **only** entities permitted
to name or imply anything about specific external technology, vendors, or
models. **No other entity's definition may reference implementation detail.**"*

**Consequence for division construction [D]:** a Platform Division definition
**may not name a vendor, model, or specific technology.**

**Inspected, and the result needs stating precisely.** A sweep of `divisions/`
for vendor, model and technology names returns **five hits, all `Claude` /
`Claude Code`**, in three forms: a section heading recording a source document
read (`PD-03 §1.1bis`), quotations of that document's own metadata (*"Target:
Claude Code"*), and quotations of governance constraints addressed to the
executing delegate (*"Claude must not resolve a divergence…"*).

**None is a definitional reference.** `§8` bars an entity's **definition** from
referencing implementation detail; provenance headings and quoted governance
constraints are neither definitions nor implementation detail. **No division
record names a vendor, model, or technology in its definitional content** —
which is the claim `§8` actually constrains.

## 8. The Domain Model does not constrain repository layout — and says so

**[A] `Domain Model §8`:**

> *"This document defines the **conceptual domain only**. It does not define,
> imply, or constrain **repository layout**, programming languages, storage
> technology, or APIs — those are separate, later artifacts that will be
> **projections of this model, not extensions to it**."*

**This is direct canonical confirmation of `IMPLEMENTATION-CORRESPONDENCE-MAP.md
§7`.** That map found four name correspondences between Platform Divisions and
`native_core/` boundaries and **declined to convert any into an ownership
binding**. The Domain Model states the reason independently: **repository layout
is a projection of the model, not part of it.**

**`Correspondence ≠ ownership` is therefore not this corpus's caution — it is
the Domain Model's own architectural boundary.** A directory named `governance/`
implies nothing about which Division owns anything.

---

# Part C — Evolution

## 9. Evolution is a governed backlog, not an open surface

**[A] `Domain Model §10`** defines the evolution surface as six **deferred
concepts**, each with a stated trigger and a stated reason for deferral:

| Deferred concept | Becomes important when | Currently sufficient because |
|---|---|---|
| **Goal / Objective** | AIOS pursues standing, multi-step objectives across Capability invocations over time | operation is *"invocation-scoped"*; intent-modelling now would *"describe behavior the system doesn't yet exercise"* |
| **Escalation / Incident** | *"this requires human attention"* must become a structural, queryable state | handled procedurally via the Decision-Making Process plus Trace's status field |
| **Steward** | hybrid human+AI accountability needs entity-level modelling | *"architect-approved decisions already cover accountability"* |
| **Cost Management System** | compute/vendor spend must be attributed to Divisions and Capabilities at scale | Trace *"already reserves a cost/resource metadata field"* |
| **Knowledge Trust Scoring** | promotion volume makes a binary canonical gate a bottleneck or quality risk | promotion is *"deliberate, low-volume, governed"* |
| **Autonomous Capability Creation** | an Agent must **propose** new Capabilities | *"a deliberate constraint for the foreseeable future, not a gap"* |

**Two of these concern this programme directly.** *Escalation / Incident* — this
corpus maintains escalations procedurally, which `§10` states is the intended
mechanism, so the practice is canonically correct rather than a workaround.
*Steward* — the open question of *"whether human accountability needs
entity-level treatment"* is recorded as *"not yet a demonstrated need."*

**The Evolution dimension is therefore answerable and is answered: it is closed
by design at v1.0**, with six named, reasoned, triggered deferrals. **Nothing in
it is constructible now**, and that is a result rather than a blockage.

## 10. `Policy` refines `E-80`

`E-80` recorded that `Policy` is a reserved concept with no ratified entity while
being a PD-03 domain concern, and concluded that no `Policy` entity may be
constructed. **`Domain Model §9` says more, and the addition matters:**

> *"**Policy** as a top-level entity — **modeled as a category of Knowledge**."*

**Policy is not merely excluded — it is placed.** It is a **category of
Knowledge**, and Knowledge under `§5` has a **home Platform Division**.

**So PD-03's `Policy` domain concern has a canonical representation after all**:
Knowledge items, homed to a Division, entered only through governed promotion
(invariant 8), durable and not casually deleted (invariant 7).

**`E-80` was correct and incomplete.** No `Policy` **entity** may be
constructed — that stands. But the corpus had recorded a dead end where canon
provides a mapping.

**Not acted on.** Assigning a Knowledge home requires knowing which Division —
`G-09`. The mechanism is recorded; the assignment is not made.

## 11. Three further non-goals bearing on this corpus

**[A] `Domain Model §9`:**

- *"**Product / Service / Platform / Ecosystem** as entities — these are
  **exposure/maturity postures of a Capability**, not new structural concepts."*
  **Bears on `PD-07 Infrastructure & Platform`**, whose record carries an open
  question (`§5`) about whether *"Platform"* denotes a second domain. `§9` says
  `Platform` is not an entity but a **posture of a Capability** — which does not
  resolve PD-07's naming question but does bar constructing a `Platform` entity
  to answer it.
- *"**Process** as a concept distinct from Workflow — one term, not two."*
- *"**ADR / RFC** as entities — process artifacts **about** changes to this
  model, not part of the model itself."*

---

## 12. What this constructs, and what it does not

**Constructs:** the **Capability**, **Architecture** and **Evolution**
dimensions of the Platform Organization construction scope, at model level, for
all ten Divisions, from `Domain Model §7`–`§10`.

**Does not construct:** no Capability created, assigned, or deprecated — canon
states this is *"intentionally… restricted to architect-approved decisions"*. No
Sub Division. No `Contract`, `Policy`, `Platform`, `Steward` or other entity. No
Knowledge home assigned. No `G-05` edge documented as a Capability dependency.
No change to the Freeze's historical `Department` wording.

**Dimension status after this artifact — 8 of 10 answered at model level:**

| Answered | Remaining |
|---|---|
| Identity · Authority · Ownership · **Capability** · **Architecture** · Lifecycle · Integration · **Evolution** | **Operation** · **Performance** |

**The two remaining are the two with no canonical model-level source yet
located.** `Domain Model §1`–`§11` is now read in full; neither Operation nor
Performance is treated there. The Encyclopedia's PD-03 Part D (*Governance
Operations*) and Part E (*Performance Architecture*) address them **per-division
and non-residently** (`ESC-C7-01`). **Whether a model-level answer exists for
these two is genuinely open, and is not asserted either way.**
