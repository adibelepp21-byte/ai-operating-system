# PD-02 — Architecture Office

> **Status: DERIVED — integration record.** Constructed under
> `FDE-P10-FRONTIER-02 §18`, which requires construction involving PD-02 to
> remain compatible with the Architecture Baseline, applicable ADRs, the
> Architecture Freeze and applicable Architecture Change Control, and states
> that **the event does not enlarge Architecture Authority**. PD-02's 50 frozen
> bodies are the authority for PD-02. **This file is not one of them.**

| | |
|---|---|
| **CPID** | `PD-02` — permanent |
| **Established name** | Architecture Office |
| **Established domain** | Architecture authority |
| **Primary construction target** | Architecture, ADR, blueprint, standards |
| **Resident corpus** | `docs/architecture/volume-2/pd-02-architecture-office/` — 50 bodies, `Status: FROZEN`, + `RESIDENCY-MANIFEST.md` |
| **Lifecycle** | **FROZEN** (`GDR-0026`) · **ACTIVE** (`GDR-0036`) |
| **Maturity** | **VERIFIED** — not advanced by this record |

---

## 1. The only activated division

PD-02 is the sole Platform Division that has completed the activation chain:

```text
P7-I99 review PASS   GDR-0025
        ↓
Volume-level FROZEN  GDR-0026
        ↓
Eligibility          GDR-0034   AE-01…AE-06 all SATISFIED
        ↓
Activation Gate PASS GDR-0035   5 AGC criteria, 2 GER rules
        ↓
ACTIVE               GDR-0036   Founder authorization, ACT-CC-R15A
```

Corpus integrity re-verified at gate time: **50/50 per-section SHA-256 match,
1,435,864 bytes — the manifest's exact figure.** The freeze holds; activation
changed the Volume's activation state, not its content.

## 2. Operative authority — enumerated, and bounded

`GDR-0027 §4` enumerates `OA-01`…`OA-07`, each content-anchored to the frozen
corpus at gate time: Domain Authority (`A5 §5`) · Decision Authority (`§6`) ·
Architecture Review Authority (`§8`) · Approval Authority (`§9`, valid **only**
where Decision Domain = Architecture Domain) · Override Authority, limited ·
Cross-platform architectural **responsibility** (`C8`) · and `OA-07`: the above
become **effective** upon activation rather than remaining designated.

**Bounded by `GDR-0027 §5`'s non-conferrals**, and by PD-02's own frozen text:
`A4:289` — *"PD-02 tidak menjadi owner atas domain tersebut"*; `D8 §70` —
*"PD-02 tidak menjadi implementation owner hanya karena mengontrol architecture
change."*

## 3. The open boundary that matters most

**`OB-01` — through which actor is PD-02's operative authority exercised?**

`GDR-0027`: *"A Platform Division is an organizational unit, not an actor…
**OB-01 does not block the enumeration above; it blocks exercise, not
definition.**"*

So `OA-01…OA-07` are **effective and unexercisable**: activation made them
operative, and no determined actor exercises them. `GDR-0027` anticipated this
exactly — it is not a contradiction — but it is the live constraint on PD-02
today, and it is distinct from the **Architecture Authority role**
(`APT-CD1.1-AA-001`), which is appointed, ACTIVE, and exercisable within its own
28 exclusions. **Two different things that are easy to conflate.**

## 4. PD-02's relationship to the other nine

PD-02's frozen corpus is, in practice, the largest resident source **about** the
other divisions — which is how eight of them could be constructed at all. But
what it records is consistently PD-02's **own limits**:

| Toward | Frozen statement |
|---|---|
| all domains | owns none of them (`A4:289`) |
| Runtime · AI Eng · Infrastructure · Security | `Execution │ NONE │ <domain> owner` (`A5:327-330`) |
| Governance | `ADVISE`; Governance Authority remains applicable (`A5:324`) |
| Quality | `ADVISE / INTERFACE` (`A5:331`) |
| Security · Quality · Governance | override may not take these authorities over (`A5 §12`) |

**This is why the owner roles are so well defined and their CPID bindings so
absent:** the corpus was written from PD-02's side, and PD-02 needed to say what
it may not do — not who each domain belongs to.

## 5. Change control

Material change to PD-02's architectural content is **architectural-tier**,
governed through the applicable Architecture Change Control and effected through
an **ADR** under `Constitution §3.4` (`GDR-0032`). Volume **lifecycle** state
remains Founder-reserved (`GDR-0026 §1`) — a boundary `GDR-0032 §6` expressly
prohibits inferring across.

`D8 §70` states the six elements an architecture change must carry: change
context · affected architecture · impact · applicable review · applicable
decision · implementation/follow-up reference.

## 6. Not constructed

PD-02 was **not** reconstructed, modified, or restated; its 50 frozen bodies are
untouched and byte-identical. **No Architecture Authority was enlarged** (`§18`).
`OB-01` was not resolved. No ADR was drafted, proposed or implied.
