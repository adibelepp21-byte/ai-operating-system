# Citation-Warning Disposition

> **Required by:** `ACT-CC-AIOS-FULL-SYSTEM-RESOLUTION-AND-AUTONOMOUS-CONTINUATION-GATE-v1.0 §15`
> — *"Every active gap SHALL ultimately become one of…"* · **2026-09-09**
>
> The citation auditor reports **45 WARN** findings. Previous returns called them
> *"technical debt, held deliberately."* **That is not one of `§15`'s
> dispositions**, and `§15` forbids a gap disappearing because its status became
> ambiguous. This record classifies all 45.

---

## 1. Result

| Disposition | Count |
|---|---:|
| **NOT-A-GAP** | **44** |
| **UNKNOWN WITH DOCUMENTED BASIS** | **1** |
| Total | **45** |

**Nothing was reclassified to make the number smaller.** 30 were settled by
context in the citing passage; **15 were read individually**, and 14 of those
turned out not to be citations at all.

## 2. The 30 settled by context

The citing passage names the volume, division, or directory that fixes the
referent — for example `AIOS_APPOINTMENT_REGISTER_v1.0.md:84`:

> *"a Final-Authority role in four **Volume 1** table cells — `C6.md:68`,
> `C8.md:178`, `E5.md:199`, `E6.md:91`"*

**`C6.md` is ambiguous to the tool and unambiguous to a reader.** The tool
resolves a bare basename against the whole repository; it does not read the
sentence the basename sits in.

**Disposition: `NOT-A-GAP`.** The citations are correct as written.

## 3. The 15 read individually — and what four of them turned out to be

| Site | What the line actually does | Disposition |
|---|---|---|
| `AIOS_FINDING_REGISTER:296` | *"04C verified structurally: **no** `composition.py`, **no** `bootstrap.py`"* — a **negative existence claim** about a region | **NOT-A-GAP** — asserting absence, not pointing |
| `Register:1922` | *"`admission.py`, `repository.py` and `retrieval.py` are **not** authorized for modification"* — names files as the **subject of an authorization scope** | **NOT-A-GAP** — subject naming, not a pointer |
| `Register:2106` | The same four F-03 cells that `APPOINTMENT_REGISTER:84` places in **Volume 1** | **NOT-A-GAP** — disambiguated by the corpus, not by the line |
| `Register:3260` | *"NON-MATERIAL GAP 1 — R1, `D2.md` metadata schema variance"* — no volume, division, or path anywhere near it | **UNKNOWN WITH DOCUMENTED BASIS** |
| `VERIFICATION:3721` | *"`B4.md` — **genuinely ambiguous across both volumes**"* | **NOT-A-GAP** — see `§4` |
| `VERIFICATION:3888` | *"`D4.md` / `E3.md` references that the auditor **immediately flagged as ambiguous**"* | **NOT-A-GAP** — see `§4` |
| `VERIFICATION:5104` | *"the real `B3.md` as the positive [test case]"* — describing a fixture | **NOT-A-GAP** — see `§4` |
| `VOLUME_ACTIVATION_MODEL:215` | *"`E8.md` = Architecture Gaps · `C4.md` = …"* — a **legend** mapping section codes to meanings | **NOT-A-GAP** — a glossary row, not a citation |

## 4. The meta-finding — the checker flags prose *about* citations

**Four of the fifteen are text discussing basename ambiguity, flagged for
basename ambiguity.** Two of those four are this programme's own record
describing the very warning being raised.

**The checker cannot distinguish a citation from a mention of a citation.**

**That is not a defect to fix. It is the reason the finding is `WARN`.**
`WARN` means *could not confirm* — never *is wrong* — and the auditor's own
docstring says overstating that would be the error. **A detector that tried to
tell a pointer from a mention would have to interpret prose, and would then be
wrong silently instead of uncertain loudly.**

It is also why the `CD-RESOLUTION-GATE` report was **reworded rather than
exempted** when it tripped this same check: a report about ambiguous citations
should not contain ambiguous citations.

## 5. The one real item

```text
Register:3260   `D2.md` — R1 metadata schema variance
DISPOSITION     UNKNOWN WITH DOCUMENTED BASIS
BASIS           Two files carry the basename. The line names no volume,
                division, or path, and the surrounding rows do not either.
AUTHORITY       Resolvable by evidence — but the resolving evidence is the
                R1 review's own working context, which is not resident.
WHY NOT FIXED   Choosing a volume would be guessing which file was meant.
                `§15` forbids a gap disappearing because it was inconvenient;
                it does not require inventing a referent.
```

**One undisambiguated citation out of 678 checked.**

## 6. This record raises 17 warnings of its own — measured, not predicted

**Writing this document took the corpus from 45 warnings to 62.** Seventeen of
them come from this file, because classifying a basename requires naming it, and
naming it is indistinguishable to the checker from citing it.

**That is `§4` demonstrated rather than asserted**, and it is the third time the
property has been observed: first when the `CD-RESOLUTION-GATE` report tripped
it, then in the four sites in `§3`, and now here.

| Source | WARN |
|---|---:|
| The corpus | **45** |
| **This record** | **17** |
| Total on a clean run | **62** |

**All 17 are `NOT-A-GAP` under `§4`** — every one is a basename quoted inside a
classification row. **They are not exempted, hidden, or suppressed**; they are
classified by the same rule as the four sites in `§3`, and they report on every
run like everything else.

**A claim in the first draft of this section was wrong and is corrected here.**
It read *"Re-running the auditor tomorrow must produce the same 45."* **It
produces 62**, and it did so on the first run after this file was written. The
draft asserted a number without re-measuring after the change that altered it —
the exact failure this programme has recorded six times. **Seventh.**

## 7. What this disposition does not do

It does not suppress a warning, lower a severity, or narrow the detector.
**All 62 report on every run**, and they should: a classification says what
findings *mean*; it is not an instruction to stop making them.
