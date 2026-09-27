# `FD-P12-007` — P12 Population Guard Lifecycle & Disposition Decision (as received)

**Received:** from the Founder, 2026-09-27, in the message body.
**Stated decision:** *"CERTIFY / AUTHORIZE FD-P12-007"*, signed *"Founder: Moriarty"*.
D1–D5 *"RATIFIED"* (`§29`). It **does not reopen P12 certification** (`§1`,
`§27`); "CERTIFY" here certifies this decision, not a phase.

Register `§73` records the decision.

Reproduced below as received, in the decision's own mixed Indonesian and
English. The message's formatting is kept as sent, including a code fence
opened in `§3` and not closed.

````text
# FD-P12-007
# P12 POPULATION GUARD LIFECYCLE & DISPOSITION DECISION

Document Type: Founder Decision Record
Decision Domain: P12 Verification / Governance Verification Machinery
Program Context: AIOS Full Stack Development & Operationalization
Related Act:
ACT-CC-POST-P13-AIOS-FULL-STACK-P12-001
— P12 Population Guard Intent Discovery Act

Related Parent Act:
ACT-CC-POST-P13-AIOS-FULL-STACK-002
— FS-08 Continuation, External Dependency Resolution & Architecture Resolution Act

Related Gate:
FS-08 Full Stack Infrastructure & Production Readiness Gate

Related Historical Gate:
P12

Decision Class:
FOUNDER DECISION

Decision Status:
CERTIFIED / AUTHORIZED FOR IMPLEMENTATION WITH BOUNDED SCOPE

Founder:
Moriarty

Decision Date:
27 September 2026

---

# 1. DECISION PURPOSE

Founder Decision ini menetapkan lifecycle dan disposition resmi untuk:

> **P12 Population Guard**

berdasarkan evidence yang dihasilkan oleh:

`ACT-CC-POST-P13-AIOS-FULL-STACK-P12-001`

Discovery tersebut berstatus:

> **INTENT DETERMINED WITH RESIDUAL**

Decision ini menyelesaikan residual mengenai:

1. status historical P12 evidence;
2. status Population Guard sebagai living check;
3. lifecycle Population Guard;
4. treatment current failing state;
5. relationship antara Population Guard dan FS-08 full-regression requirement;
6. bounded authorization apabila verification machinery di `tools/` perlu diubah.

Decision ini **tidak membuka kembali P12 certification**.

Decision ini **tidak mengubah historical P12 evidence**.

Decision ini **tidak memberikan blanket authority terhadap `tools/`**.

Decision ini memberikan authority hanya dalam boundary yang secara eksplisit ditentukan dalam dokumen ini.

---

# 2. DISCOVERY BASIS

Founder Decision ini menggunakan hasil discovery yang telah dicatat dalam:

`docs/fullstack/P12-POPULATION-GUARD-INTENT-DISCOVERY.md`

serta evidence repository dan historical git history yang digunakan oleh discovery.

Temuan utama:

- Population Guard diperkenalkan pada commit `14afe69` tanggal 12 September 2026.
- Test tidak pernah dimodifikasi sejak introduction commit.
- Later change `67b405b` menambahkan write barrier pada `__main__`, bukan mengubah measurement semantics.
- Pada creation, population classifier menghasilkan sekitar 389 governance documents dan 33 Founder acts.
- P12 historical record menggunakan dated figures yang tercatat pada evidence P12.
- P12-W6 menyatakan population sebagai time-indexed dan guard dimaksudkan untuk mencegah directional comparison mengalami silent inversion.
- P12 certified manifest mem-pin historical P12 evidence pada commit `6968c6e`.
- `tools/` test dan module tidak termasuk dalam P12 certified manifest.
- Current governance corpus terus berkembang.
- Founder-act status-label ratio meningkat dari waktu ke waktu dan property yang dahulu diukur akhirnya mengalami inversion.
- Inversion sudah terlihat sebelum current failing commit `20742f5`.
- Commit `76366be` juga memperluas governance-identifier classes sehingga corpus evolution terdiri dari corpus growth dan classifier evolution.
- Current failure bukan bukti bahwa test implementation rusak.
- Current failure menunjukkan bahwa property yang dipantau oleh living guard tidak lagi berlaku terhadap current corpus.

---

# 3. HISTORICAL P12 RECORD

## DECISION D1

Founder menetapkan:

> **P12 historical certification evidence remains immutable.**

Tidak ada current governance corpus change yang boleh digunakan untuk mengubah historical P12 evidence.

Artefak yang dilindungi meliputi:

- P12-W6 historical record;
- P12 certification evidence;
- P12 certified manifest;
- historical figures;
- historical measurements;
- historical population claims;
- historical certification chronology;
- historical Founder records yang menjadi bagian dari P12 evidence.

### D1 RESULT

```text
RATIFIED
HISTORICAL P12 EVIDENCE = IMMUTABLE
D1 Rationale
P12 certification adalah historical state.
Current governance corpus adalah state yang berkembang.
Perubahan current corpus tidak boleh ditulis balik ke historical certification state.
Decision ini konsisten dengan:
Immutable Historical Baseline
dalam FDR-G1.
 
⸻
 
4. LIVING POPULATION GUARD
DECISION D2
Founder menetapkan bahwa:
P12 Population Guard tetap diakui sebagai LIVING GOVERNANCE-CORPUS CHECK.
Population Guard tidak direclassify sebagai frozen historical snapshot.
Ia terus membaca governance population yang berlaku pada current committed repository state.
Model semantic-nya adalah:
Current Governance Corpus
        ↓
Current Population Classifier
        ↓
Founder-Act Subset
        ↓
Population Comparison
        ↓
Directional Property Check
        ↓
Current Governance Signal
D2 RESULT
RATIFIED
POPULATION GUARD = LIVING CHECK
D2 Rationale
Discovery menemukan bahwa:
1. test membaca current committed population;
2. tidak ada pinned snapshot di dalam test;
3. historical record menggunakan dated measurement;
4. purpose guard adalah mendeteksi silent inversion;
5. corpus memang dirancang berkembang setelah P12.
Karena itu living semantics merupakan intent yang didukung langsung oleh evidence.
 
⸻
 
5. POPULATION GUARD LIFECYCLE
DECISION D3
Founder memilih:
L2 — VERSIONED SUCCESSOR
Existing P12 Population Guard tidak direwrite in place.
Historical/lifecycle identity dari existing check tetap dipertahankan sebagai historical verification artifact.
Jika current governance semantics memerlukan check baru atau perubahan measurement semantics, perubahan dilakukan melalui:
Versioned Successor
sesuai model:
Existing Population Guard
        │
        │ immutable historical/reference state
        ▼
Versioned Successor
        │
        ▼
Current Governance-Corpus Semantics
D3 RESULT
RATIFIED
LIFECYCLE = VERSIONED SUCCESSOR
D3 Rationale
L2 dipilih karena:
1. Population Guard terbukti merupakan living check;
2. historical P12 evidence harus tetap immutable;
3. current property telah berubah;
4. FDR-G1 menetapkan Versioned Successor + Immutable Historical Baseline sebagai model architectural evolution;
5. in-place mutation berisiko mengaburkan perbedaan antara historical semantics dan current semantics;
6. pinned historical check tidak sesuai dengan evidence bahwa current guard memang dimaksudkan sebagai living check.
 
⸻
 
6. VERSIONED SUCCESSOR REQUIREMENTS
Successor Population Guard wajib memiliki:
1. unique successor identity;
2. explicit version;
3. explicit purpose;
4. explicit population definition;
5. explicit Founder-Act subset definition;
6. explicit semantic difference dari predecessor;
7. explicit relationship terhadap historical P12 guard;
8. explicit authority;
9. explicit verification criteria;
10. explicit regression evidence.
Successor tidak boleh menyatakan atau menyiratkan:
bahwa historical P12 guard sejak awal memiliki semantics successor.
Successor hanya merepresentasikan current/revised governance verification semantics.
 
⸻
 
7. HISTORICAL GUARD TREATMENT
Existing Population Guard tidak boleh dihapus sebagai historical evidence.
Existing implementation tidak boleh diam-diam ditimpa sehingga historical meaning hilang.
Jika repository architecture memerlukan predecessor tetap tersedia, predecessor harus tetap dapat diidentifikasi sebagai:
P12 HISTORICAL POPULATION GUARD
dan successor sebagai:
P12 POPULATION GUARD SUCCESSOR
Relationship harus eksplisit.
 
⸻
 
8. CURRENT FAILURE CLASSIFICATION
Current state:
tools:
1919 / 1920

Failing check:
test_the_narrower_population_is_not_better
Founder menetapkan bahwa failure tersebut bukan diklasifikasikan sebagai:
CODE DEFECT
melainkan sebagai:
CURRENT GOVERNANCE PROPERTY INVERSION
dengan status:
EXPECTED / CLASSIFIED GOVERNANCE SIGNAL
until successor lifecycle is implemented and verified.
Important distinction:
TEST EXECUTION
        ≠
PROPERTY RESULT
Test dapat berfungsi dengan benar sekalipun property yang diukur menghasilkan FAIL.
 
⸻
 
9. FS-08 FULL REGRESSION TREATMENT
DECISION D4
Founder memilih:
R2 — CLASSIFIED EXCEPTION
FS-08 full-regression requirement dapat dianggap satisfied with explicit classified exception terhadap current Population Guard failure, tetapi hanya setelah seluruh conditions berikut dipenuhi.
Required Conditions
1. Population Guard execution tetap dilakukan.
2. Failure tetap terlihat.
3. Failure tidak di-skip.
4. Failure tidak di-suppressed.
5. Failure tidak diubah secara artificial menjadi PASS.
6. Test implementation harus terbukti functioning correctly.
7. Historical P12 evidence tetap immutable.
8. Successor lifecycle harus tercatat.
9. Exception harus tercatat dalam FS-08 evidence.
10. Semua regression suites lain yang diwajibkan harus PASS.
11. No unrelated regression may be hidden under this exception.
12. FS-08 gate harus mencatat exception secara eksplisit.
D4 RESULT
RATIFIED
FS-08 = MAY PASS WITH EXPLICIT CLASSIFIED EXCEPTION
D4 Important Limitation
R2 bukan blanket rule bahwa:
“one failing test is always acceptable.”
R2 hanya berlaku terhadap:
P12 Population Guard yang telah independently classified sebagai legitimate living governance signal berdasarkan FD-P12-007.
Jika test lain gagal, exception ini tidak berlaku.
Jika Population Guard failure berubah sifat menjadi implementation defect, exception ini tidak berlaku.
 
⸻
 
10. FS-08 GATE SEMANTICS
Setelah FD-P12-007 diterapkan, FS-08 gate harus membedakan:
PASS
FAIL
BLOCKED
CLASSIFIED EXCEPTION
Population Guard current state dapat menghasilkan:
CLASSIFIED EXCEPTION
dan bukan:
PASS
The distinction must remain visible in evidence.
FS-08 may reach:
PASS WITH CLASSIFIED EXCEPTION
only when every other required FS-08 condition is satisfied.
 
⸻
 
11. TOOLS/ MODIFICATION AUTHORITY
DECISION D5
Founder memberikan:
EXPLICIT LIMITED MODIFICATION AUTHORIZATION
tetapi hanya untuk implementation yang diperlukan untuk menjalankan lifecycle:
L2 — Versioned Successor
Authorization ini bukan blanket authorization untuk:
tools/
Authorization hanya mencakup:
* existing P12 Population Guard implementation;
* successor Population Guard implementation;
* directly related test/support code required for successor;
* documentation required to establish predecessor/successor relationship;
* narrowly required FS-08 evidence integration for the classified exception.
Tidak termasuk:
* unrelated tests;
* unrelated verification machinery;
* P12 historical records;
* P12 certified manifest;
* governance baseline;
* FS-08 architecture;
* Runtime;
* Backend;
* Frontend;
* Supabase;
* Vercel;
* production deployment.
 
⸻
 
12. TOOLS/ AUTHORITY BOUNDARY
Claude Code SHALL NOT interpret D5 as:
permission to modify any file under tools/.
Before modifying any file, Claude Code must identify:
1. exact file;
2. current role;
3. relationship to Population Guard;
4. exact semantic change;
5. authority basis;
6. expected verification effect.
Only files directly implementing or supporting the P12 Population Guard successor are within D5.
If a required file is not clearly within this boundary:
STOP
  ↓
DOCUMENT AUTHORITY GAP
  ↓
ESCALATE
No modification by inference.
 
⸻
 
13. FORBIDDEN MODIFICATIONS
Under D5, Claude Code SHALL NOT:
1. rewrite P12-W6;
2. rewrite P12 certification evidence;
3. modify P12 manifest;
4. alter historical figures;
5. delete historical Founder records;
6. hide the current Population Guard failure;
7. skip the test;
8. suppress the test;
9. move Status: labels;
10. alter unrelated governance records;
11. change unrelated tests;
12. modify FS-08 gate semantics beyond the explicit classified-exception treatment;
13. modify production deployment;
14. modify Vercel infrastructure;
15. modify Supabase infrastructure;
16. modify authentication architecture;
17. modify FS-DP-02;
18. modify FS-DP-05;
19. modify Runtime architecture;
20. create a new Micro-Act merely because a bounded implementation detail is encountered.
 
⸻
 
14. SUCCESSOR SEMANTIC BOUNDARY
The successor may change:
* population measurement semantics;
* population classification semantics;
* current governance property being monitored;
* threshold only where explicitly justified by the successor specification;
* expected current-corpus behavior.
The successor may NOT:
* rewrite historical interpretation;
* pretend the old test had different semantics;
* erase evidence that the original property inverted;
* convert historical failure into historical PASS.
 
⸻
 
15. CLASSIFIER EVOLUTION
Discovery identified:
76366be
as a commit affecting governance identifier classification.
Therefore the successor specification must explicitly state whether the population classifier:
1. preserves the current classifier;
2. adopts a successor classifier;
3. or separates corpus evolution from classifier evolution.
The successor must not silently mix historical classifier semantics with current classifier semantics.
Any classifier change must be documented as a semantic change.
 
⸻
 
16. CURRENT CORPUS EFFECT
The Founder accepts the discovery conclusion that the current failure is associated with legitimate governance corpus evolution.
The following distinction is therefore canonical for this decision:
Historical P12 Condition
        ↓
Founder acts scored under original property
        ↓
Governance corpus evolved
        ↓
Property inverted
        ↓
Living guard detected inversion
        ↓
Current classified failure
This does not invalidate the historical measurement.
It also does not prove that the current property is desirable or undesirable.
The Population Guard’s role is measurement and detection.
 
⸻
 
17. P12 HISTORICAL EVIDENCE PROTECTION
Regardless of successor implementation:
P12 historical evidence = IMMUTABLE
Specifically protected:
* P12-W6;
* P12 manifest;
* certification commit;
* historical population figures;
* historical Founder-act figures;
* dated historical conclusions.
No successor may modify them.
 
⸻
 
18. FDR-G1 SUCCESSOR MODEL
FD-P12-007 explicitly adopts the existing AIOS architectural evolution principle:
Versioned Successor + Immutable Historical Baseline + Re-certification
for this verification lifecycle.
Therefore:
Historical Verification
        │
        └── immutable
               │
               ▼
      Versioned Successor
               │
               ▼
        Fresh Verification
               │
               ▼
       Evidence / Certification
The successor is not automatically certified merely because this Founder Decision authorizes its construction.
Successor verification remains mandatory.
 
⸻
 
19. SUCCESSOR CERTIFICATION
The successor must not be treated as certified until:
1. implementation is complete;
2. semantic delta is recorded;
3. tests pass under successor semantics;
4. historical evidence remains intact;
5. negative controls pass;
6. full regression is executed;
7. FS-08 evidence is refreshed;
8. appropriate certification/acceptance authority is satisfied.
 
⸻
 
20. FS-08 INTERIM STATE
Until successor verification is complete:
P12 Historical Evidence:
IMMUTABLE

Population Guard:
LIVING

Current Population Guard:
CLASSIFIED FAILURE

Lifecycle:
VERSIONED SUCCESSOR AUTHORIZED

FS-08:
BLOCKED BY OTHER OPEN ITEMS
WITH P12 FAILURE TREATED AS CLASSIFIED EXCEPTION

FS-09:
NOT STARTED

Production:
UNTOUCHED
The classified exception does not independently close FS-08.
Other FS-08 blockers remain independently binding.
 
⸻
 
21. RELATION TO EXT-03 AND EXT-05
FD-P12-007 does not resolve:
EXT-03
Vercel Preview access.
EXT-05
SUPABASE_SECRET_KEY Preview configuration.
Those remain external operational dependencies under ACT-002.
Their status remains:
EXT-03 = BLOCKED / EXTERNAL
EXT-05 = BLOCKED / EXTERNAL
 
⸻
 
22. RELATION TO FS-DP-02 AND FS-DP-05
FD-P12-007 does not ratify:
* FS-DP-02 Authentication;
* FS-DP-05 Run Identity.
Those remain separate Architect decision packages.
Their lifecycle remains:
FS-DP-05 = AWAITING ARCHITECT DECISION
FS-DP-02 = AWAITING ARCHITECT DECISION
No semantic overlap is created by FD-P12-007.
 
⸻
 
23. IMPLEMENTATION SEQUENCE
After recording FD-P12-007, Claude Code may execute:
1. Re-read FD-P12-007
        ↓
2. Verify D5 authority boundary
        ↓
3. Identify exact Population Guard implementation files
        ↓
4. Preserve predecessor
        ↓
5. Construct versioned successor
        ↓
6. Define successor population semantics
        ↓
7. Define successor property
        ↓
8. Add required successor tests
        ↓
9. Verify historical P12 evidence unchanged
        ↓
10. Run negative controls
        ↓
11. Run full regression
        ↓
12. Rediscover governance corpus
        ↓
13. Update FS-08 evidence
        ↓
14. Re-run FS-08 gate
No additional Micro-Act is required for ordinary execution within D5.
 
⸻
 
24. FAILURE ESCALATION
If implementation reveals that the selected successor requires authority outside D5:
STOP
  ↓
CLASSIFY
  ↓
DOCUMENT
  ↓
ESCALATE
Claude Code must not expand D5 by inference.
 
⸻
 
25. GOVERNANCE REGISTER RECORD
The following record shall be entered into the Governance Register:
Identifier:
FD-P12-007

Type:
Founder Decision

Subject:
P12 Population Guard Lifecycle & Disposition

Founder:
Moriarty

Date:
27 September 2026

Historical P12 Evidence:
IMMUTABLE

Population Guard:
LIVING GOVERNANCE-CORPUS CHECK

Lifecycle:
L2 — VERSIONED SUCCESSOR

Current Failure:
EXPECTED / CLASSIFIED GOVERNANCE SIGNAL

FS-08 Treatment:
R2 — CLASSIFIED EXCEPTION

Tools Modification:
EXPLICIT LIMITED MODIFICATION AUTHORIZATION

Modification Scope:
P12 Population Guard successor and directly related verification support only

Blanket Tools Authority:
NOT GRANTED

P12 Historical Modification:
FORBIDDEN

P12 Certification Reopening:
NOT AUTHORIZED

FS-DP-02:
UNCHANGED / ARCHITECT DECISION PENDING

FS-DP-05:
UNCHANGED / ARCHITECT DECISION PENDING

EXT-03:
UNCHANGED / EXTERNAL BLOCKER

EXT-05:
UNCHANGED / EXTERNAL BLOCKER

FS-09:
NOT STARTED

Production:
UNTOUCHED
 
⸻
 
26. DECISION RATIONALE
Founder selects:
D1 — Immutable Historical Record
Because historical P12 evidence represents a completed historical verification state and must not be rewritten by later corpus evolution.
D2 — Living Population Guard
Because discovery directly established that the guard was designed to observe the governance corpus as it evolves.
D3 — Versioned Successor
Because the current directional property has inverted while historical evidence remains valid.
A versioned successor preserves both truths:
Historical property
        +
Current governance state
without rewriting either.
D4 — Classified Exception
Because the Population Guard is functioning as designed and its FAIL represents a governance signal rather than a software defect.
The exception preserves visibility rather than suppressing the failure.
D5 — Limited Modification Authority
Because successor implementation requires bounded technical changes, but Founder authority over semantic disposition must not be interpreted as unrestricted authority over verification machinery.
 
⸻
 
27. NO RETROACTIVE REINTERPRETATION
This Decision explicitly rejects the following interpretations:
Current failure means P12 certification was wrong.
False.
Current corpus must be forced back into the P12 historical population.
Not authorized.
The historical P12 test must be rewritten to PASS.
Not authorized.
Founder Decision grants unrestricted tools/ authority.
False.
A classified exception hides the failing test.
False.
Versioned successor automatically becomes certified.
False.
 
⸻
 
28. ACCEPTANCE CONDITIONS FOR D3/D5 IMPLEMENTATION
Implementation is considered correctly executed only if:
1. predecessor semantics remain identifiable;
2. successor identity is explicit;
3. historical P12 files remain byte-for-byte unchanged;
4. P12 manifest remains unchanged;
5. unrelated tools/ files remain unchanged;
6. current failure is not artificially suppressed;
7. successor tests validate the new semantics;
8. classifier semantics are explicit;
9. full regression is rerun;
10. FS-08 evidence records the classified exception;
11. rediscovery confirms no unauthorized scope expansion;
12. production remains untouched.
 
⸻
 
29. FINAL DECISION STATE
FD-P12-007 establishes:
D1 = RATIFIED
Historical P12 Evidence = IMMUTABLE

D2 = RATIFIED
Population Guard = LIVING CHECK

D3 = RATIFIED
Lifecycle = VERSIONED SUCCESSOR

D4 = RATIFIED
FS-08 Treatment = CLASSIFIED EXCEPTION

D5 = RATIFIED
Tools Modification = EXPLICIT LIMITED AUTHORIZATION
 
⸻
 
30. POST-DECISION STATE
P12 Historical Record
        ↓
IMMUTABLE
        │
        ▼
Living Population Guard
        ↓
CURRENT PROPERTY INVERTED
        │
        ▼
CLASSIFIED GOVERNANCE SIGNAL
        │
        ▼
VERSIONED SUCCESSOR
AUTHORIZED
        │
        ▼
BOUNDED IMPLEMENTATION
        │
        ▼
FRESH VERIFICATION
        │
        ▼
FS-08 RECONCILIATION
Current independent blockers remain:
EXT-03 = BLOCKED
EXT-05 = BLOCKED

FS-DP-05 = AWAITING ARCHITECT
FS-DP-02 = AWAITING ARCHITECT
Therefore:
FS-08 = NOT CLOSED
FS-09 = NOT STARTED
PRODUCTION = UNTOUCHED
 
⸻
 
31. FOUNDER AUTHORIZATION STATEMENT
I, Moriarty, as Founder, decide and authorize the following:
1. The historical P12 record remains immutable.
2. The P12 Population Guard remains recognized as a living governance-corpus check.
3. The Population Guard lifecycle shall use a Versioned Successor model rather than in-place rewriting or historical pinning.
4. The current Population Guard failure is recognized as a classified governance signal caused by the current corpus no longer satisfying the original directional property.
5. FS-08 may treat this specific Population Guard failure as a classified exception, provided the conditions in this decision are satisfied and the failure remains visible.
6. Claude Code is authorized to implement the versioned successor within the explicit bounded scope of this decision.
7. This authorization does not grant unrestricted modification authority over tools/.
8. Any change outside the P12 Population Guard successor boundary must stop and follow the applicable authority route.
9. No P12 historical evidence may be modified.
10. No P12 certification may be reopened.
11. No production deployment is authorized by this decision.
12. FS-DP-02 and FS-DP-05 remain subject to their separate Architect decisions.
13. EXT-03 and EXT-05 remain independent external dependencies.
14. FS-08 must be re-verified after the authorized successor work and all remaining dependencies are resolved.
Founder:
Moriarty
Date:
27 September 2026
Decision:
CERTIFY / AUTHORIZE FD-P12-007
````
