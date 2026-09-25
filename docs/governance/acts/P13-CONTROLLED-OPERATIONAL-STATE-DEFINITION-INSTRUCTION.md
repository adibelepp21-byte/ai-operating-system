# P13 Controlled Operational State Definition (Residual Frontier Register) — Instruction

**Instruction type (as issued):** Semantic Definition / Pre-FDR-3 Gate · No identifier is stated in the instrument · **Dated:** not stated; received 2026-09-24
**Received from:** the Founder's session (Moriarty) · **Authorizes:** read-only inspection and documentation within existing authority (instrument `§26`). It authorizes no construction, no state change, no authority selection and no Founder decision
**Definition document:** `docs/architecture/p13-preparation/P13-CONTROLLED-OPERATIONAL-STATE-DEFINITION-RESIDUAL-FRONTIER-REGISTER.md`

## Provenance

The instruction arrived as one message with no attachment. The fenced block
below is that message as received, from its first line through `END OF
INSTRUCTION`. Its UTF-8 sha256, taken over the fenced content, is `f4c828ec88d63798fe625853257d787f49f2f69c3979dd8f7779081b98aaf864`.
The instrument states no identifier, so none is given to it here. It is cited
by this file's path.

This header was written by Claude and is not part of the Founder's text.

# § RECORD — as issued, verbatim

````text
AIOS — P13 CONTROLLED OPERATIONAL STATE DEFINITION

Residual Frontier Register

Instruction Type: Semantic Definition / Pre-FDR-3 Gate
Target: Claude Code / Co-Founder / CEO
Scope: P13 E13-05
Primary Surface: Residual Frontier Register
Status: EXECUTE DEFINITION — NO FDR-3 YET
Authority: Existing delegated discovery / analysis / architecture-preparation authority only
Construction: NOT AUTHORIZED BY THIS INSTRUCTION
State-Changing Authority: NOT GRANTED
Authority Selection: NOT AUTHORIZED
Founder Decision: NOT MADE BY THIS INSTRUCTION
Certification: NOT REQUESTED

⸻

1. PURPOSE

This instruction follows the completed:

P13-E13-05-SEMANTIC-PROOF-SURFACE-DISCOVERY.md

The discovery identified the Residual Frontier Register as the only conditional candidate currently found that has a legitimate reason to exist independently of E13-05 testing within the P13 operational boundary.

This instruction does NOT authorize implementation.

Its purpose is to define the semantic meaning of that operational surface sufficiently precisely that a later Founder decision can determine whether bounded state-changing authority should exist.

The immediate question is:

What exactly is the Residual Frontier Register as an operational state, what does an entry mean, what constitutes a valid state transition, and how does that state participate in P13’s observation → reasoning → action → consequence → re-observation → rediscovery loop?

The technical representation must emerge from the semantic definition.

Do NOT begin by designing:

* JSON schema
* Python classes
* database schema
* executor
* file layout
* authority envelope
* mutation API
* test harness

unless a technical representation is strictly necessary to explain an already-established semantic requirement.

⸻

2. CURRENTLY ESTABLISHED DISCOVERY

The previous discovery established the following findings.

2.1 Existing architectural basis

The Residual Frontier Register is not an object invented solely for E13-05.

The current evidence indicates:

* FDR-2 D08 requires completion with a classified residual frontier.
* E13-07 requires that unresolved frontier be explicitly recorded.
* The P13 Blueprint §3.2 assigns the Frontier component ownership of the residual frontier register.
* Current implementation recomputes the frontier each cycle.
* Current P13 Memory does not provide persistent frontier content sufficient to distinguish newly discovered frontier items from previously observed ones.
* Five live cycles observed the same six frontier items without demonstrating persistent frontier-state progression.
* The P13 workspace directory did not yet exist during the discovery.
* No state-changing authority has been granted.

These findings are discovery evidence and must remain properly classified.

Do not silently upgrade them into canonical claims beyond what the sources establish.

⸻

3. CORE SEMANTIC DISTINCTION

The Residual Frontier Register MUST NOT become a second source of truth for AIOS reality.

The architecture must preserve:

CANONICAL AIOS SOURCES
        ↓
actual system / frontier state
        ↓
P13 observes
        ↓
P13 interprets
        ↓
P13 records its operational knowledge
        ↓
Residual Frontier Register

NOT:

Residual Frontier Register
        ↓
defines canonical AIOS reality

The register is therefore an operational knowledge/state record, not a canonical authority over the underlying frontier.

The following distinction is mandatory:

The canonical sources determine what the AIOS frontier actually is. The Residual Frontier Register records what P13 has discovered, understood, and retained about that frontier.

⸻

4. CENTRAL SEMANTIC QUESTION

Define precisely:

What does it mean for a residual frontier item to be “known” by P13?

Do not assume that:

known = present in a file

Instead determine whether “known” requires some combination of:

* observation
* identification
* classification
* evidence/provenance
* discovery cycle
* source reference
* status
* last observation
* verification state

Only include elements supported by the existing architecture and evidence.

If the existing system does not define a required element, mark it as:

PROPOSED

rather than silently treating it as canonical.

⸻

5. DEFINE THE SEMANTIC OBJECT

Define the semantic meaning of:

Residual Frontier

What does “frontier” mean in the existing P13 completion / exhaustion model?

Frontier Item

What is the smallest meaningful unit of residual frontier?

Determine whether an item represents:

* an unresolved question
* a gap
* a dependency
* an unknown
* an authority blocker
* an evidence deficiency
* another category

Do not invent categories.

Use existing canonical taxonomy where available.

Frontier Observation

What exactly has P13 observed?

Frontier Record

What exactly does the register preserve?

Frontier Divergence

What does it mean when:

Canonical frontier contains F

but:

Register does not contain F

?

Frontier Change

What does it mean when:

Register contains F

but the newly observed canonical state differs from the recorded observation?

Frontier Persistence

What does it mean when:

F exists across multiple observations

?

Frontier Resolution

What does it mean if canonical sources indicate that F is no longer unresolved?

Critically:

Does the register merely record the observation of resolution, or is it itself permitted to close/remove the frontier item?

Do not grant authority through semantic definition.

⸻

6. DEFINE “ADMISSION”

This is the central semantic operation.

Determine exactly what:

ADMIT frontier item

means.

The working hypothesis is:

Canonical frontier contains F
+
P13 observes F
+
Register does not contain F
        ↓
P13 determines that F should be recorded
        ↓
ADMIT F
        ↓
Register now contains an operational record of F

But this is only a hypothesis.

Validate it against canonical architecture.

Answer:

1. What condition permits admission?
2. What evidence must exist?
3. Who/what determines that the item is eligible for admission?
4. Is admission a classification decision or merely a recording decision?
5. Can admission alter the canonical frontier?
6. Can admission change the item’s canonical classification?
7. Can admission declare a gap closed?
8. Can admission declare P13 complete?

The expected answer to questions 5–8 must be determined from sources, not assumed.

⸻

7. DISTINGUISH RECORDING FROM DECISION

This distinction is critical.

Determine whether:

P13 records:
"I observed frontier item F."

is different from:

P13 decides:
"F is no longer a frontier item."

The register should not become a mechanism through which P13 silently exercises authority over canonical state.

Explicitly establish:

RECORDING AUTHORITY
        ≠
CANONICAL DECISION AUTHORITY

If this distinction is already established by canonical sources, cite those sources.

If it is an architectural proposal emerging from this analysis, label it PROPOSED.

⸻

8. DEFINE THE REGISTER STATE MODEL

Do NOT create an artificial lifecycle merely to support testing.

Instead derive the smallest state model required by the actual semantics.

Investigate whether the following distinctions are genuinely necessary:

NOT RECORDED
      ↓
OBSERVED / ADMITTED
      ↓
KNOWN
      ↓
RE-OBSERVED

And whether the system legitimately needs to distinguish:

NEW
PERSISTENT
CHANGED
STALE
RESOLVED

Do not assume all of these states are required.

For each proposed state or condition, provide:

Name
Meaning
Source basis
Why it is needed
Whether it is canonical / measured / implementation / proposed

Avoid creating a state machine merely because it is convenient for the test.

⸻

9. DEFINE THE MINIMUM SEMANTIC RECORD

Determine the minimum information required for a frontier record to have operational meaning.

Do NOT design a file schema.

Instead answer conceptually:

What facts must be retained for P13 to recognize the difference between “I have never seen this frontier” and “I have already observed this frontier”?

Potential dimensions may include:

identity
source/provenance
classification
first observation
last observation
observation cycle
status
evidence reference
basis

But these are NOT automatically required.

For each dimension:

REQUIRED
OPTIONAL
NOT REQUIRED
UNKNOWN

and explain why.

⸻

10. DEFINE STATE BEFORE AND STATE AFTER

The E13-05 proof requires a meaningful transition.

Define the semantic state before admission.

Example working abstraction:

CANONICAL:
F exists as unresolved frontier item
P13 OPERATIONAL KNOWLEDGE:
F has been observed
REGISTER:
F is not yet represented

Then define the semantic state after admission:

CANONICAL:
F remains unchanged
P13 OPERATIONAL KNOWLEDGE:
F has been observed and retained
REGISTER:
F is represented with sufficient provenance/basis

Do NOT assume this abstraction is correct.

Verify it.

The critical property is:

The action changes P13’s operational knowledge of the frontier without changing the canonical frontier itself.

⸻

11. DEFINE THE EXPECTED CONSEQUENCE

Determine the expected consequence of admission.

The current working hypothesis is:

BEFORE:
F is observed but not persistently known by P13
ACTION:
ADMIT F
EXPECTED AFTER:
F is persistently known by P13

Then define what the next observation should reveal.

For example:

NEXT CYCLE
canonical frontier still contains F
register contains F
        ↓
P13 recognizes F as previously known

This is not yet canonical.

Verify whether this is actually sufficient to constitute a meaningful consequence.

⸻

12. DEFINE RE-OBSERVATION

This is mandatory for E13-05.

Determine exactly what P13 observes after admission.

The semantic loop should be capable of expressing:

OBSERVATION N
Canonical frontier:
F exists
Register:
F absent
        ↓
P13 reasons:
F is a newly observed / unrecorded frontier item
        ↓
ADMISSION
        ↓
OBSERVATION N+1
Canonical frontier:
F exists
Register:
F present
        ↓
P13 understands:
F is already known

If this does NOT produce meaningful new information, explain why and identify the missing semantic component.

⸻

13. DEFINE REDISCOVERY

Determine what “rediscovery” means in this context.

It must NOT simply mean:

run the same code again.

Determine whether rediscovery means P13 can discover:

* a new frontier item
* persistence of an existing frontier item
* change in an existing frontier item’s basis
* change in status
* resolution
* disappearance
* stale information
* another meaningful state transition

Only include distinctions supported by existing architecture.

⸻

14. DEFINE CONSEQUENCE MISMATCH

E13-05 requires the possibility that:

Expected consequence ≠ Actual consequence

Define this specifically for the frontier register.

Example working case:

Expected:
F becomes known after admission
Actual:
register does not contain F

or:

Expected:
F remains represented
Actual:
canonical observation changed before verification

Determine the correct interpretation.

A mismatch MUST NOT be silently converted into success.

The semantic response must be something like:

MISMATCH
   ↓
RE-OBSERVE
   ↓
RE-EVALUATE
   ↓
REDISCOVER

but verify the exact behavior from the existing P13 model.

⸻

15. DEFINE OWNERSHIP

Determine the semantic ownership of:

Canonical frontier

Who owns the authoritative state?

P13 Frontier component

What does “owns the residual frontier register” mean?

Register contents

Are they:

* P13 operational knowledge?
* canonical AIOS state?
* evidence?
* memory?
* trace?
* derived state?

Do not blur these categories.

The critical distinction must remain:

OWNERSHIP OF REGISTER
        ≠
AUTHORITY OVER CANONICAL FRONTIER

⸻

16. DEFINE AUTHORITY BOUNDARY — WITHOUT GRANTING AUTHORITY

This instruction does NOT authorize any state-changing action.

Nevertheless, define the minimum conceptual authority that would be required if the Founder later chooses to authorize the proof.

Describe:

Permitted semantic action
Forbidden semantic actions
Target boundary
Maximum mutation
Reversibility
Expiry
Preconditions
Verification requirement
Trace requirement

The likely candidate action is:

ADMIT ONE FRONTIER OBSERVATION

But do not assume this is correct.

Validate it.

Explicitly distinguish:

semantic requirement

from:

authority actually granted

Current authority remains:

State-changing Authority = NONE

unless a current canonical source proves otherwise.

⸻

17. EXPLICITLY ANALYZE THE PROPOSED MINIMUM ACTION

Determine whether the smallest meaningful E13-05 action is:

Admission of exactly one real frontier divergence into the P13-owned residual frontier register.

Evaluate this against:

B1 State Before Known
B2 P13 Determines Action
B3 Real State Change
B4 Expected Consequence
B5 Resulting State Observable

Then evaluate:

P1 Decision
P2 Authority
P3 Execution
P4 Consequence Verification
P5 Evidence
P6 Re-observation

Do NOT score or rank.

Use factual classifications such as:

SUPPORTED
PARTIALLY SUPPORTED
INSUFFICIENT EVIDENCE
UNKNOWN
AUTHORITY BLOCKED
BOUNDARY CONFLICT

⸻

18. CRITICAL TEST: IS ADMISSION REALLY A STATE CHANGE?

Do not assume:

register absent
→ register entry exists

is sufficient.

Determine whether the meaningful transition is actually:

P13 operational knowledge:
UNRECORDED
        ↓
PERSISTENTLY KNOWN

and whether that changed state materially affects future P13 observation.

If the only change is file existence, reject it as insufficient.

If the semantic change is persistent operational knowledge, establish evidence for that interpretation.

⸻

19. CRITICAL TEST: DOES THE REGISTER CREATE A SECOND SOURCE OF TRUTH?

Explicitly test:

Canonical frontier = authoritative
Register = P13 operational knowledge

The register MUST NOT be able to:

* redefine canonical frontier
* delete canonical frontier items
* reclassify canonical frontier items
* declare gaps resolved
* declare completion
* alter E13 exit criteria
* alter governance
* create authority
* override Founder decisions

If any proposed register semantics would create such a capability, stop and classify the boundary conflict.

⸻

20. CRITICAL TEST: E13-05 VS E13-06

Determine whether:

ADMIT FRONTIER ITEM

is merely operational state management or whether it constitutes system evolution.

The current working boundary is:

E13-05
bounded operational state change

versus:

E13-06
evolution / capability change / self-modification

The register action must not:

* modify P13 source code
* modify architecture
* create new capabilities
* expand authority
* modify governance
* alter canonical definitions

If admission remains a record of operational knowledge, explain why it remains E13-05 rather than E13-06.

⸻

21. LIVE-PROOF DEPENDENCY

The discovery established that the current six-item frontier has not moved across five live cycles.

Therefore explicitly analyze:

What constitutes a legitimate live divergence that could later trigger the admission action?

Examples may include:

new frontier item
newly discovered gap
new dependency
changed evidence basis
new unresolved condition

Do NOT manufacture a frontier item merely to make the test pass.

Do NOT modify canonical sources to create one.

If no naturally occurring divergence exists at present, record:

LIVE E13-05 TRIGGER = NOT CURRENTLY OBSERVED

This does NOT invalidate the semantic surface.

It means live proof remains contingent on an authentic operational divergence.

⸻

22. TEST-HARNESS BOUNDARY

Define exactly what a future test harness may and may not do.

The harness MAY:

* provide an actual world/system state
* initiate a legitimate observation cycle
* provide environmental timing or deterministic test conditions
* verify post-action state independently

The harness MUST NOT:

* name the frontier item P13 should select
* prescribe the action
* prescribe the expected consequence in a way that bypasses P13 reasoning
* directly mutate the register before P13 acts
* silently grant authority
* manufacture canonical evidence
* declare the action successful

The semantic definition must preserve:

P13 discovers
P13 reasons
P13 decides

rather than:

test harness decides
P13 executes

⸻

23. REVERSIBILITY

Define what reversibility means semantically.

Do not assume “delete the file” is sufficient.

If P13 admits:

F

what does rollback mean?

Possibilities must be analyzed carefully:

remove operational record

versus:

append a compensating observation

versus:

mark record superseded

Do not select an implementation.

Determine the semantic requirement first.

Importantly:

Rollback must not alter the canonical frontier merely to undo P13’s operational record.

⸻

24. FOUNDER-RESERVED QUESTIONS

At the end, identify which questions remain Founder-reserved.

Potential questions include:

Q1 — Does the P13-owned residual frontier register qualify as the
     intended operational reality for E13-05?
Q2 — Is admission-only semantics the correct bounded transition?
Q3 — Is construction of the register covered by P13-018 D-1?
Q4 — Is append-only admission covered by the existing operational envelope,
     or does it require new state-changing authority?
Q5 — What exact authority envelope is required, if any?
Q6 — Is live proof required before E13-05 can be considered demonstrated?

Do NOT answer Founder-reserved questions as Founder.

Classify them as:

OPEN
FOUNDER RESERVED
ANSWERABLE FROM CANONICAL SOURCE
UNKNOWN

Only use the categories supported by the actual evidence.

⸻

25. NO FDR-3

This instruction MUST NOT produce:

* FDR-3
* Founder Decision Record
* Founder recommendation
* Founder selection
* authority grant
* authority envelope
* construction authorization
* state-changing authorization

The output may prepare a future decision surface, but it must not make the decision.

⸻

26. NO IMPLEMENTATION

Do NOT:

* create the register
* create workspace state
* modify P13 source code
* modify canonical artifacts
* modify P1–P12 artifacts
* create an executor
* create a mutation API
* alter AuthorityGate
* alter P13-ENV-01
* create production tests requiring the new authority
* create artificial frontier items
* modify the six existing frontier items
* create a fake divergence

Read-only inspection and documentation are permitted within existing authority.

⸻

27. SOURCE FIDELITY

Before defining semantics, re-discover current state.

Read and reconcile, at minimum:

1. Current P13 Canonical Blueprint.
2. FDR-2.
3. P13-019.
4. P13 semantic proof surface discovery report.
5. Current P13 Frontier implementation.
6. Current P13 Memory implementation relevant to frontier state.
7. Current Trace/evidence implementation.
8. Current P13 E13-07 exit implementation.
9. Current authority / governance sources.
10. Current live Trace evidence.
11. Current residual frontier evidence.

Preserve distinctions between:

CANONICAL
VERIFIED REALITY
MEASURED
IMPLEMENTATION
DISCOVERY RESULT
PROPOSED
UNKNOWN
INSUFFICIENT EVIDENCE

Do not reconstruct missing Founder intent.

⸻

28. REQUIRED OUTPUT

Create:

docs/architecture/p13-preparation/
P13-CONTROLLED-OPERATIONAL-STATE-DEFINITION-RESIDUAL-FRONTIER-REGISTER.md

Do not overwrite the previous discovery report.

The document must contain:

1. Document Control
2. Purpose and Scope
3. Source Basis
4. Current Discovery Finding
5. Semantic Definition of Residual Frontier
6. Semantic Definition of Frontier Item
7. Semantic Definition of Frontier Observation
8. Semantic Definition of Frontier Register
9. Semantic Definition of Admission
10. Canonical State vs P13 Operational Knowledge
11. Ownership and Authority Boundary
12. State-Before / State-After Model
13. Minimum Meaningful State Transition
14. Expected Consequence
15. Re-Observation Model
16. Rediscovery Model
17. Consequence-Mismatch Model
18. Minimum Semantic Record
19. Valid and Invalid Transitions
20. E13-05 Proof Mapping
    P1–P6
    B1–B5
21. Negative Behavioral Cases
22. E13-05 / E13-06 Boundary
23. Reversibility Boundary
24. Live-Proof Dependency
25. Test-Harness Boundary
26. Authority Requirement
    [DESCRIBED, NOT GRANTED]
27. Founder-Reserved Questions
28. Remaining Unknowns
29. Semantic Decision Readiness
30. Conclusion

⸻

29. REQUIRED SEMANTIC DIAGRAM

The document MUST include a conceptual diagram equivalent to:

                 CANONICAL AIOS SOURCES
                          │
                          ▼
                  RESIDUAL FRONTIER
                          │
                          ▼
                     P13 OBSERVE
                          │
                          ▼
                   P13 UNDERSTAND
                          │
                          ▼
                    P13 EVALUATE
                          │
                          ▼
                     P13 REASON
                          │
                          ▼
                DETERMINE NEXT ACTION
                          │
                          ▼
                  AUTHORITY CHECK
                     /          \
               INVALID          VALID
                 │                │
              REFUSE          EXECUTE
                                  │
                                  ▼
                           REGISTER STATE
                              CHANGES
                                  │
                                  ▼
                             VERIFY
                                  │
                                  ▼
                          TRACE / EVIDENCE
                                  │
                                  ▼
                           RE-OBSERVE
                                  │
                                  ▼
                            REDISCOVER
                                  │
                                  ▼
                     UPDATED P13 KNOWLEDGE

Clearly label:

CANONICAL SOURCE OF TRUTH

and:

P13 OPERATIONAL KNOWLEDGE

so they cannot be confused.

⸻

30. REQUIRED TRANSITION EXAMPLE

Provide at least one fully semantic example without implementing it.

Example structure:

BEFORE
Canonical frontier:
F exists
P13 operational knowledge:
F observed
F not persistently represented
        ↓
P13 observes divergence
        ↓
P13 evaluates
        ↓
P13 determines:
ADMIT F
        ↓
Authority check
        ↓
[Future authorized execution only]
        ↓
AFTER
Canonical frontier:
F unchanged
P13 operational knowledge:
F persistently recorded
        ↓
NEXT OBSERVATION
Canonical frontier:
F exists
Register:
F exists
        ↓
P13 recognizes:
F is known / previously observed
        ↓
REDISCOVERY

Clearly mark all parts that are:

CANONICAL
MEASURED
IMPLEMENTATION
PROPOSED
UNKNOWN

Do not present the example as already-authorized behavior.

⸻

31. SEMANTIC ADEQUACY GATE

At the end, answer this exact question:

Does the Residual Frontier Register provide a genuine semantic state transition that can satisfy E13-05 without becoming a second source of truth, without crossing ownership boundaries, and without requiring E13-06 capabilities?

Return one of:

SEMANTICALLY ADEQUATE
SEMANTICALLY ADEQUATE WITH OPEN AUTHORITY QUESTIONS
SEMANTICALLY INSUFFICIENT
INSUFFICIENT EVIDENCE

The classification must be evidence-based.

Do not choose a favorable classification merely because it enables construction.

⸻

32. FINAL CONSTRAINT

The governing sequence is:

DISCOVER
   ↓
DEFINE SEMANTICS
   ↓
VALIDATE AGAINST CANONICAL SOURCES
   ↓
DEFINE STATE TRANSITION
   ↓
DEFINE CONSEQUENCE
   ↓
DEFINE RE-OBSERVATION
   ↓
DEFINE REDISCOVERY
   ↓
DEFINE MINIMUM AUTHORITY REQUIREMENT
   ↓
IDENTIFY FOUNDER DECISION SURFACE
   ↓
STOP

Do NOT continue automatically into:

FDR-3

or:

construction

or:

authority grant

The purpose of this gate is to make the next Founder decision precise enough that the Founder is deciding a real architectural/governance boundary rather than a technical implementation detail.

⸻

END OF INSTRUCTION
````
