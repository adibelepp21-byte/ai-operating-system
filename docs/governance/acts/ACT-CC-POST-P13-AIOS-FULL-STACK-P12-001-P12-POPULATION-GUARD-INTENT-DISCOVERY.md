# `ACT-CC-POST-P13-AIOS-FULL-STACK-P12-001` — P12 Population Guard Intent Discovery Act (as received)

**Received:** from the Founder, 2026-09-27, in the message body.
**Stated status:** *"Status: PROPOSED FOR FOUNDER AUTHORIZATION"*; *"Authority
Class: DISCOVERY / EVIDENCE ONLY"*; *"Construction Authority: NONE"*; *"Test
Modification Authority: NONE"*. Register `§72` records how it was executed:
read-only, under the escalation route ACT-002 already authorizes.

Reproduced below as received, in the Act's own mixed Indonesian and English.
The message's formatting is kept as sent, including a code fence opened in
`§5.4` and not closed.

````text
# ACT-CC-POST-P13-AIOS-FULL-STACK-P12-001
# P12 POPULATION GUARD INTENT DISCOVERY ACT

Document Type: Governance / Evidence Discovery Act
Program: AIOS Full Stack Development & Operationalization
Parent Program: ACT-CC-POST-P13-AIOS-FULL-STACK-001
Related Act: ACT-CC-POST-P13-AIOS-FULL-STACK-002
Related Gate: FS-08
Related Historical Gate: P12
Status: PROPOSED FOR FOUNDER AUTHORIZATION
Authority Class: DISCOVERY / EVIDENCE ONLY
Construction Authority: NONE
Test Modification Authority: NONE

---

# 1. PURPOSE

Act ini memberikan otorisasi yang sempit dan eksplisit kepada Claude Code untuk melakukan:

> **P12 Population Guard Intent Discovery**

Tujuannya adalah menentukan, berdasarkan evidence yang sudah ada di repository AIOS dan canonical governance corpus, apa sebenarnya intent dan lifecycle semantics dari population guard P12 yang sekarang gagal setelah governance corpus berkembang.

Act ini TIDAK memberikan otorisasi untuk memperbaiki test.

Act ini TIDAK memberikan otorisasi untuk mengubah `tools/`.

Act ini TIDAK memberikan otorisasi untuk mengubah threshold.

Act ini TIDAK memberikan otorisasi untuk mengubah historical baseline.

Act ini TIDAK memberikan otorisasi untuk melakukan re-measurement sebagai keputusan governance.

Act ini hanya menghasilkan:

> evidence-based determination package mengenai intent, population semantics, baseline semantics, dan lifecycle treatment dari P12 Population Guard.

---

# 2. CONTEXT

Pada continuation execution ACT-CC-POST-P13-AIOS-FULL-STACK-002 ditemukan regression pada:

`test_the_narrower_population_is_not_better`

Observed state:

- tools suite: 1919 / 1920 passing;
- failing test berada di `tools/`;
- failure muncul setelah ACT-002 governance record menjadi tracked corpus;
- Founder instrument population sekarang menghasilkan:
  - 45 / 90 = 0.500;
  - configured limit = 0.496;
- failure telah ditelusuri sebagai perubahan population terhadap statistical guard;
- tidak ada perubahan pada test machinery yang dilakukan;
- tidak ada governance evidence yang boleh dimanipulasi untuk membuat test kembali PASS.

Historical report sebelumnya yang menyatakan tools suite `1920` passing juga telah dikoreksi karena pengukuran sebelumnya dilakukan sebelum ACT-002 file masuk tracked state.

Act ini dibuat untuk menjawab pertanyaan yang lebih fundamental:

> **Apakah population guard tersebut merupakan immutable historical integrity assertion terhadap P12 certification corpus, atau merupakan living governance-corpus property yang memang harus berubah ketika corpus berkembang?**

Jawaban tidak boleh diasumsikan.

---

# 3. SCOPE

Scope Act terbatas pada:

1. discovery terhadap test implementation dan test history;
2. discovery terhadap P12 certification evidence;
3. discovery terhadap population definition;
4. discovery terhadap baseline/hash/snapshot evidence;
5. discovery terhadap lifecycle rules untuk certified tests;
6. discovery terhadap treatment atas governance corpus growth;
7. classification atas evidence;
8. penyusunan recommendation/disposition package.

Tidak termasuk:

- perubahan `tools/`;
- perubahan test;
- perubahan threshold;
- perubahan governance baseline;
- perubahan Founder Decision;
- perubahan Architect Decision;
- perubahan P12 certified artifacts;
- perubahan FS-08 gate implementation;
- perubahan population;
- penghapusan atau pemindahan governance records;
- rewriting Founder instruments;
- production deployment;
- database changes;
- Vercel changes.

---

# 4. AUTHORITY MODEL

## 4.1 Claude Code Authority

Claude Code berwenang untuk:

- membaca repository;
- membaca historical git history;
- membaca P12 evidence;
- membaca governance register;
- membaca test source;
- membaca test history;
- membaca manifest;
- membaca hash/snapshot records;
- melakukan static analysis;
- melakukan read-only measurements;
- melakukan comparative analysis;
- membuat discovery/evidence report;
- membuat proposed disposition options.

## 4.2 Claude Code Tidak Berwenang

Claude Code TIDAK berwenang untuk:

- mengubah `tools/`;
- mengubah failing test;
- mengubah threshold;
- mengubah baseline;
- membuat successor test;
- membuat Founder Decision;
- membuat Architect Decision;
- mereclassify certified evidence;
- mengubah historical record;
- menghapus governance instrument;
- memindahkan `Status:` line;
- mengubah format Founder record untuk memengaruhi measurement;
- menyatakan P12 test invalid tanpa evidence;
- menyatakan P12 test tetap valid tanpa evidence.

---

# 5. GOVERNING PRINCIPLES

## 5.1 Evidence Before Disposition

Tidak boleh ada perubahan hanya karena test FAIL.

FAILURE adalah evidence untuk discovery, bukan otomatis evidence bahwa test salah.

---

## 5.2 Historical Evidence Is Not Rewritten

Historical P12 evidence harus diperlakukan sebagai historical evidence.

Jika ditemukan bahwa sebuah measurement menggunakan population tertentu pada saat certification, population tersebut tidak boleh diubah retroaktif hanya agar current corpus kembali PASS.

---

## 5.3 Current Corpus Is Not Automatically Historical Corpus

Governance documents yang muncul setelah P12 certification tidak boleh otomatis dianggap:

- bagian dari P12 certification population; atau
- bukan bagian dari P12 certification population.

Hal tersebut harus dibuktikan.

---

## 5.4 Test Failure Is Not Automatically a Defect

Classification harus menggunakan:

```text
TEST DEFECT
TEST ASSUMPTION
CORPUS EVOLUTION
BASELINE DRIFT
INTENT AMBIGUITY
EXPECTED EVOLUTION
UNKNOWN
Tidak boleh memilih classification tanpa evidence.
 
⸻
 
5.5 No Evidence → No Claim
Jika evidence tidak ditemukan, hasil harus:
UNKNOWN / EVIDENCE NOT FOUND
bukan reconstruction.
 
⸻
 
5.6 No Tool Modification
Selama Act ini berjalan:
tools/ = READ ONLY
Tidak ada exception.
 
⸻
 
6. PRIMARY QUESTIONS
Claude Code wajib menjawab enam pertanyaan berikut berdasarkan evidence.
 
⸻
 
Q1 — HISTORICAL VS LIVING INTENT
Tentukan apakah P12 Population Guard pada saat dibuat dimaksudkan untuk:
A. Historical P12 Corpus Integrity
Test dimaksudkan untuk memverifikasi property dari corpus pada saat P12 certification.
atau:
B. Living Governance Corpus
Test dimaksudkan untuk terus mengukur current governance corpus setiap kali corpus berkembang.
atau:
C. Hybrid
Test memiliki historical baseline tetapi juga dimaksudkan untuk current-corpus monitoring.
atau:
D. UNKNOWN
Evidence tidak cukup.
Required Evidence
Cari:
* test comments;
* test naming;
* surrounding test architecture;
* P12 gate;
* P12 verification records;
* P12 certification records;
* baseline documents;
* manifests;
* git history;
* governance decisions;
* test introduction commit;
* later modifications;
* documentation referencing the test.
 
⸻
 
7. Q2 — POPULATION DEFINITION AT CREATION
Tentukan secara evidence-based:
Population apa yang dimaksud ketika test pertama kali dibuat?
Wajib mencari:
* exact population source;
* file/path selection logic;
* inclusion rules;
* exclusion rules;
* filename patterns;
* document classification;
* Status: detection logic;
* baseline corpus;
* commit/tree yang digunakan;
* date/time atau certification event;
* population count;
* Founder instrument classification;
* non-Founder governance document population.
Jika exact population tidak dapat direkonstruksi secara evidence-based:
Population Definition = UNKNOWN
Jangan melakukan bounded reconstruction untuk mengisi kekosongan tersebut.
 
⸻
 
8. Q3 — POST-CERTIFICATION FOUNDER INSTRUMENTS
Tentukan apakah Founder instruments yang dibuat setelah P12 certification:
* memang seharusnya masuk population P12;
* memang seharusnya tidak masuk population P12;
* masuk population current/living test tetapi bukan historical P12 baseline;
* atau statusnya UNKNOWN.
Wajib membedakan:
P12 HISTORICAL POPULATION
        ≠
CURRENT GOVERNANCE CORPUS
kecuali evidence menunjukkan keduanya memang identik secara semantic.
Periksa minimal:
* Founder Decisions;
* Founder Authorization records;
* governance Register;
* post-P12 records;
* successor/certification rules;
* corpus inclusion rules;
* git chronology.
 
⸻
 
9. Q4 — BASELINE / HASH / SNAPSHOT
Tentukan apakah P12 Population Guard memiliki:
* explicit baseline;
* hash;
* manifest;
* snapshot;
* pinned commit;
* pinned tree;
* document list;
* population count;
* certification-time corpus;
* equivalent immutable reference.
Classification:
EXPLICIT BASELINE
DERIVABLE BASELINE
NO BASELINE FOUND
AMBIGUOUS
Jika explicit hash atau snapshot ditemukan, catat:
* identifier;
* commit;
* file/path;
* hash;
* population count;
* date;
* authority;
* relation terhadap P12 certification.
Jangan mengubah baseline.
 
⸻
 
10. Q5 — CERTIFIED TEST IMMUTABILITY AGAINST CORPUS GROWTH
Cari canonical evidence yang menjawab:
Apakah certified governance tests harus tetap immutable ketika governance corpus berkembang?
Periksa:
* Governance Baseline;
* P12 closure/certification records;
* FDR/GDR records;
* Versioned Successor model;
* Immutable Historical Baseline rules;
* test governance rules;
* certification rules;
* post-certification change management;
* repository protection rules;
* successor/re-certification semantics.
Classification:
EXPLICITLY REQUIRED
EXPLICITLY NOT REQUIRED
CONDITIONALLY REQUIRED
INFERRED ONLY
UNKNOWN
Penting:
INFERRED ONLY tidak boleh diperlakukan sebagai canonical rule.
 
⸻
 
11. Q6 — CORPUS CHANGE LIFECYCLE
Tentukan berdasarkan evidence apa lifecycle yang benar ketika population berubah.
Candidate dispositions:
A — TEST REVISION
Existing test diubah untuk mengikuti corpus baru.
B — SUCCESSOR TEST
Existing certified test tetap immutable.
Test baru dibuat sebagai versioned successor untuk population/corpus baru.
C — BASELINE PINNING
Test tetap mengukur historical population yang dipin pada baseline tertentu.
Current corpus growth tidak mengubah historical test.
D — RE-MEASUREMENT
Existing measurement dire-run terhadap current corpus berdasarkan canonical rule.
E — HYBRID
Historical test tetap pinned, sementara separate living measurement dibuat.
F — UNKNOWN
Evidence tidak cukup untuk memilih.
Claude Code tidak boleh memilih salah satu hanya berdasarkan architectural preference.
Pilihan harus:
SOURCE EVIDENCE
        ↓
CLASSIFICATION
        ↓
PROPOSED DISPOSITION
 
⸻
 
12. REQUIRED DISCOVERY ORDER
Claude Code wajib menggunakan urutan:
1. Locate failing test
        ↓
2. Read current implementation
        ↓
3. Locate test introduction history
        ↓
4. Locate P12 verification record
        ↓
5. Locate P12 certification / closure evidence
        ↓
6. Locate baseline / manifest / hash
        ↓
7. Locate population definition
        ↓
8. Locate corpus evolution rules
        ↓
9. Compare historical vs current population
        ↓
10. Classify intent
        ↓
11. Classify lifecycle
        ↓
12. Produce disposition package
Tidak boleh langsung melompat ke solusi.
 
⸻
 
13. GIT / HISTORY REQUIREMENT
Jika test history tersedia, Claude Code wajib mencari:
* introducing commit;
* modifying commits;
* relevant rename;
* baseline commits;
* P12 certification commit;
* first appearance of population guard;
* subsequent changes affecting population;
* relationship between certification and test.
Jika history tidak cukup:
HISTORY INSUFFICIENT
Jangan reconstruct intent dari naming semata.
 
⸻
 
14. CURRENT VS HISTORICAL MEASUREMENT
Claude Code boleh melakukan read-only measurement untuk membandingkan:
P12 baseline population
vs
current tracked population
Tetapi hasilnya hanya evidence.
Tidak boleh:
* update test;
* update threshold;
* commit generated changes;
* change baseline;
* mark PASS;
* suppress failure.
Required output:
Measurement	Historical Baseline	Current Corpus
Total population	?	?
Founder instruments	?	?
Founder Status labels	?	?
Ratio	?	?
Threshold	?	?
Test result	?	?
Jika historical population tidak dapat ditentukan secara exact:
NOT MEASURABLE WITHOUT RECONSTRUCTION
 
⸻
 
15. EVIDENCE CLASSIFICATION
Setiap finding harus diberi salah satu classification:
CANONICAL
CERTIFIED HISTORICAL
DIRECT REPOSITORY EVIDENCE
GIT HISTORY EVIDENCE
DERIVED MEASUREMENT
INFERENCE
UNKNOWN
CONFLICT
Rules:
* CANONICAL > CERTIFIED HISTORICAL > direct evidence;
* INFERENCE tidak boleh digunakan sebagai authorization;
* UNKNOWN tidak boleh diubah menjadi assumption;
* CONFLICT harus dilaporkan, bukan diselesaikan secara diam-diam.
 
⸻
 
16. NEGATIVE CONTROLS
Claude Code wajib memastikan:
NC-01
No changes under tools/.
NC-02
No threshold changes.
NC-03
No baseline changes.
NC-04
No P12 certification record changes.
NC-05
No Founder instrument rewriting.
NC-06
No governance corpus deletion.
NC-07
No file renaming to alter population.
NC-08
No status-line relocation.
NC-09
No test suppression.
NC-10
No test skip.
NC-11
No self-ratification.
NC-12
No Founder Decision manufacture.
NC-13
No Architect Decision manufacture.
NC-14
No FS-08 gate override.
NC-15
No production modification.
 
⸻
 
17. REQUIRED OUTPUT
Claude Code wajib menghasilkan:
A. Intent Determination
P12 Population Guard Intent:
[HISTORICAL / LIVING / HYBRID / UNKNOWN]

Confidence:
[HIGH / MEDIUM / LOW]

Evidence:
...
 
⸻
 
B. Population Determination
P12 Original Population:
...

Population Source:
...

Population Definition:
...

Population Baseline:
...

Population Count:
...
 
⸻
 
C. Founder Instrument Treatment
Post-P12 Founder Instruments:

Historical Population:
[INCLUDED / EXCLUDED / UNKNOWN]

Current Living Population:
[INCLUDED / EXCLUDED / UNKNOWN]

Evidence:
...
 
⸻
 
D. Baseline Determination
Baseline Type:
[EXPLICIT / DERIVABLE / NONE / AMBIGUOUS]

Baseline Commit:
...

Manifest:
...

Hash:
...

Population Count:
...
 
⸻
 
E. Immutability Determination
Certified Test Immutability:
[REQUIRED / NOT REQUIRED / CONDITIONAL / UNKNOWN]

Canonical Basis:
...
 
⸻
 
F. Lifecycle Determination
Population Change Treatment:

[TEST REVISION]
[SUCCESSOR TEST]
[BASELINE PINNING]
[RE-MEASUREMENT]
[HYBRID]
[UNKNOWN]

Evidence:
...
 
⸻
 
18. DISPOSITION MATRIX
Claude Code wajib membuat matrix:
Question	Finding	Evidence	Classification	Confidence
Q1 Historical vs Living				
Q2 Original Population				
Q3 Post-P12 Founder Instruments				
Q4 Baseline/Hash/Snapshot				
Q5 Certified Test Immutability				
Q6 Population Change Lifecycle				
Tidak boleh ada cell penting yang diisi berdasarkan assumption.
 
⸻
 
19. CONCLUSION STATES
Act hanya boleh menghasilkan salah satu:
STATE A — INTENT DETERMINED
Evidence cukup untuk menentukan semantics.
STATE B — INTENT DETERMINED WITH RESIDUAL
Intent dapat ditentukan tetapi terdapat unresolved historical evidence.
STATE C — AMBIGUOUS
Evidence menunjukkan lebih dari satu interpretation yang credible.
STATE D — UNKNOWN
Evidence tidak cukup.
 
⸻
 
20. DISPOSITION RECOMMENDATION
Jika evidence cukup, Claude Code boleh memberikan:
PROPOSED DISPOSITION
dengan pilihan:
A — Preserve Historical Test / Pin Baseline

B — Create Versioned Successor Test

C — Re-measure Current Corpus

D — Maintain Historical Test + Separate Living Measurement

E — Revise Test Under Existing Authority

F — Founder Decision Required

G — Architect Decision Required

H — UNKNOWN / Further Evidence Required
Namun:
Proposed Disposition ≠ Decision.
Claude Code tidak boleh menerapkan disposition tersebut dalam Act ini.
 
⸻
 
21. NO-CHANGE GUARANTEE
Pada akhir execution wajib diverifikasi:
tools/ changes: 0
P12 certified artifacts changes: 0
Governance baseline changes: 0
Founder records changes: 0
FS-08 gate changes: 0
Production changes: 0
Jika salah satu bukan zero:
STOP AND ESCALATE
 
⸻
 
22. REGRESSION REQUIREMENT
Karena Act ini discovery-only, Claude Code tidak perlu memperbaiki failing test.
Namun setelah discovery:
* jalankan relevant read-only validation;
* jika diperlukan jalankan existing test suite tanpa modification;
* catat current result;
* jangan mengubah result menjadi PASS secara artificial.
Jika test tetap:
1919 / 1920
maka hasil tersebut harus tetap dilaporkan.
 
⸻
 
23. GOVERNANCE REGISTER
Setelah execution, Claude Code wajib membuat satu Register entry untuk Act ini.
Register entry harus membedakan:
ACT
P12 DISCOVERY
FINDINGS
PROPOSED DISPOSITION
Tidak boleh membuat:
Founder Decision
Architect Decision
Ratification
sebagai efek samping Act ini.
 
⸻
 
24. RETURN PACKAGE
Return package wajib mencakup:
A — Act Identity
B — Execution Status
C — Six Question Findings
D — Evidence Inventory
E — Historical Population
F — Current Population
G — Baseline / Hash / Snapshot
H — Test History
I — P12 Certification Relationship
J — Corpus Growth Analysis
K — Immutability Rule
L — Lifecycle Determination
M — Disposition Matrix
N — Proposed Disposition
O — Unknowns
P — Conflicts
Q — Negative-Control Results
R — Repository Change Report
S — Regression Result
T — Required Next Decision, if any
 
⸻
 
25. ESCALATION RULE
Jika hasil discovery menunjukkan bahwa keputusan berikutnya membutuhkan authority yang tidak dimiliki Claude Code:
STOP AT DECISION BOUNDARY
        ↓
DOCUMENT EVIDENCE
        ↓
DOCUMENT OPTIONS
        ↓
ROUTE TO APPROPRIATE AUTHORITY
Jangan membuat Micro-Act baru hanya karena discovery menemukan unresolved decision.
Gunakan existing governance route:
* Founder → Founder-reserved matter;
* Architect → architecture/test lifecycle matter where Architect authority applies;
* existing Act → implementation after authorized decision.
 
⸻
 
26. RELATION TO ACT-002
Act ini adalah discovery support untuk:
ACT-CC-POST-P13-AIOS-FULL-STACK-002
Act ini tidak menggantikan ACT-002.
Act ini tidak membuka FS-09.
Act ini tidak menutup FS-08.
Act ini tidak mengubah:
* EXT-03;
* EXT-05;
* FS-DP-02;
* FS-DP-05;
* FS-DP-01;
* FS-DP-04.
Hasilnya hanya memberikan evidence untuk menentukan treatment yang benar terhadap P12 Population Guard.
 
⸻
 
27. AUTO-ADVANCE BOUNDARY
Setelah P12 Population Guard Intent Discovery selesai:
Jika intent dan lifecycle sudah definitif:
Claude Code:
1. record findings;
2. record proposed disposition;
3. identify required authority;
4. route decision;
5. STOP at decision boundary if authorization is required.
Jika evidence tidak cukup:
Claude Code:
1. record UNKNOWN;
2. identify exact missing evidence;
3. do not reconstruct;
4. do not modify tools;
5. return package.
Tidak ada auto-implementation dalam Act ini.
 
⸻
 
28. FINAL DIRECTIVE
Claude Code shall execute:
P12 Population Guard Intent Discovery
strictly as an evidence-discovery activity.
Claude Code SHALL NOT modify tools/.
Claude Code SHALL NOT modify the P12 test.
Claude Code SHALL NOT alter thresholds.
Claude Code SHALL NOT alter historical baselines.
Claude Code SHALL NOT rewrite Founder instruments.
Claude Code SHALL NOT manufacture Founder or Architect decisions.
Claude Code SHALL determine, from existing evidence, whether the P12 Population Guard represents:
* historical P12 corpus integrity,
* living governance corpus monitoring,
* a hybrid model,
* or an unresolved/unknown intent.
Claude Code SHALL determine the original population, post-certification Founder instrument treatment, baseline/hash/snapshot semantics, certified-test immutability semantics, and population-change lifecycle.
Claude Code SHALL return the evidence and proposed disposition without implementing any disposition.
No change to tools/. No change to P12 certification. No change to FS-08 gate. No production change.
 
⸻
 
29. COMPLETION CONDITION
This Act is complete when:
1. Q1–Q6 have been investigated;
2. evidence has been classified;
3. historical vs current population has been distinguished;
4. baseline/hash/snapshot status has been determined;
5. test lifecycle semantics have been determined or explicitly marked UNKNOWN;
6. proposed disposition has been documented;
7. required authority has been identified;
8. negative controls pass;
9. tools/ remains unchanged;
10. P12 certified artifacts remain unchanged;
11. no Founder/Architect decision has been manufactured;
12. complete return package has been produced.
Final status must be one of:
INTENT DETERMINED
INTENT DETERMINED WITH RESIDUAL
AMBIGUOUS
UNKNOWN
 
⸻
 
30. GOVERNANCE STATEMENT
The purpose of this Act is not to make the P12 Population Guard pass.
The purpose is to determine what the P12 Population Guard was actually designed to assert, what population it was designed to measure, and how that assertion is supposed to behave when the AIOS governance corpus evolves.
Evidence determines intent. Intent determines lifecycle. Authority determines change.
Until that chain is established, the existing test remains untouched.
````
