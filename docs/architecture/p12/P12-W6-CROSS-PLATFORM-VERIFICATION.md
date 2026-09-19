# P12-W6 — cross-platform relationship evidence over the resident corpora (`§48` v1.1)

> Every cross-platform relationship that **can** be read from a resident
> canonical corpus **is** evidenced: 18 of 18. The remaining 72 ordered pairs are
> `SOURCE-ABSENT`, and every one of them belongs to a division whose corpus is
> non-resident (`ESC-C7-01`) or absent (`G-01`). The gap is supply, not
> verification.

---

## 1. Why this did not exist until `ACT-CC-P12-024`

[E] `§48` was **revised**. v1.0 gave one list that merged phase surfaces with
division names and, doing so, omitted four Platform Divisions. `v1.1 §48`
(`C-03`) splits it into two populations and restores `PD-01`, `PD-02`, `PD-06`
and `PD-07`.

[D] P12 measured the phase-surface half — `p12_cross_phase_verification`, 8/8
exercised — and measured the division half **only through the
`CROSS-PD-INTERFACE-REGISTRY`**. That registry was built from the `E-33`/`E-24`
propagation, both sourced in `PD-03`/`PD-04`, so **`PD-01` and `PD-02` appear in
no registry edge at all** — while their canonical corpora have been resident
since Volume 1 and Volume 2 landed.

[E] `PD-01 C8` is titled **Cross Platform Governance**. Its `§6` carries a
Platform Relationship Model naming all nine other divisions under Governance,
Alignment, Coordination and Review. Its `§7` defines three **Cross Platform
Interaction Types** — Alignment, Dependency, Collaboration — each with an
ownership rule. Its `§8` Shared Responsibility table is declared *"authoritative
source"*.

[C] **None of that had reached any P12 measurement.** Classified `P12
VERIFICATION GAP` under `ACT-CC-P12-024 §3`, which makes it P12 construction
work, and closed here.

---

## 2. Result

```text
python3 -m tools.p12_cross_platform_verification
{'divisions': 10, 'resident_corpora': ('PD-01', 'PD-02'),
 'source_absent_divisions': ('PD-03','PD-04','PD-05','PD-06',
                             'PD-07','PD-08','PD-09','PD-10'),
 'ordered_pairs': 90, 'RECIPROCATED': 2, 'SELF-DECLARED': 16,
 'MENTIONED': 0, 'SOURCE-ABSENT': 72, 'evidenced_pairs': 18,
 'interfaces_defined': 0, 'interfaces_verified': 0}
```

| State | Count | Meaning |
|---|---|---|
| `RECIPROCATED` | **2** | `PD-01 ↔ PD-02` — each corpus states the relationship in a section whose own heading is about relationships |
| `SELF-DECLARED` | **16** | one resident corpus states it; the counterpart's corpus cannot be read |
| `MENTIONED` | **0** | named, but not in a relationship-bearing section |
| `SOURCE-ABSENT` | **72** | `8 divisions × 9` — no resident corpus to read |

**18 of 18 readable pairs are evidenced.** `2 × 9 = 18`, and `MENTIONED` is zero:
where a division's own corpus is resident, it states its relationship to every
other division, without exception.

---

## 3. What is deliberately not claimed

[C] `§48`'s rule is unchanged — *"A relationship is not considered verified
merely because both surfaces exist"* — and nothing here returns `VERIFIED` or
`DEFINED`.

```text
DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL
```

`RECIPROCATED` is a stronger claim than *both surfaces exist* and a weaker one
than verified: each side's own corpus states the relationship, in a section
whose own heading is about relationships. That is **evidence of a relationship**,
which is what `§6.11` asks for. It is **not an interface definition**, which is
what `F-18` lacks and what `ADR-0029` reserves. `interfaces_defined: 0` is
stated, not computed, because no resident body defines one.

[C] `SOURCE-ABSENT` is never *no relationship*. `§43`: `UNKNOWN ≠ FALSE`.

---

## 4. Falsification

| Hypothesis | Result |
|---|---|
| the module returns a constant | **FALSIFIED** — six tests drive the state to `MENTIONED`, `SELF-DECLARED`, `RECIPROCATED` and `SOURCE-ABSENT` against constructed corpora |
| residency is a hardcoded list | **FALSIFIED** — `resident_corpora` scans `volume-*`; a test finds `PD-07` under a `volume-9` it invents |
| a bare mention counts as a relationship | **FALSIFIED** — a `PD-02` reference inside `E4 — KPI & Success Metrics Framework` reports `MENTIONED`, not evidence |
| no resident corpus reports zero rather than failing | **FALSIFIED** — `CorpusUnavailable` is raised (`PR-4`) |
| the module promotes anything to verified | **FALSIFIED** — asserted absent from the state vocabulary |

## 4.1 A defect in this instrument, disclosed

[E] The first run reported `PD-01 → PD-02` as `SELF-DECLARED` and
`RECIPROCATED: 0`. The heading reader took each file's first non-empty line,
which across most of `PD-02`'s corpus is the **Part banner** — *"Part C —
Governance Architecture"* — while the section's own title sits on the next line.
`C8 — Cross-Platform Architecture Governance` was therefore read as ordinary
governance prose.

[D] An instrument that cannot locate the heading, reporting a **weaker** state
than the evidence supports, is the `UNKNOWN ≠ FALSE` failure committed inside
the module built to measure evidence — the same class this programme has
corrected in `p12_e12_measurement` and in the `duplicate delegation` probe.
Corrected to match the section's own identifier over the opening lines, with the
Part banner as fallback, and pinned by a test that constructs both layouts.

---

## 5. Effect on `§6.11`

[U] **`§6.11` remains `NO`.** The looser reading was considered and declined:
one could argue that `§43`'s `UNKNOWN ≠ FALSE` makes 18-of-18-readable
sufficient, since the unreadable 72 are a supply problem P12 cannot solve. That
reading is not taken. *"Cross-platform relationships have evidence"* is not
satisfied when eight of ten divisions cannot be read at all, and a condition is
not met by being met wherever it was possible to meet it.

[C] Declining costs nothing — `§6.8` and `§6.9` block completion regardless — so
the call is made on the merits rather than on what it would buy.

[E] What changed is the quality of the statement. `§6.11`'s cross-platform half
was previously measured by a five-row registry reporting `5.6%` coverage. It is
now measured over the full ten-division population, and the finding is sharper:
**the shortfall is entirely residency and absence, and zero of it is unevidenced
resident material.**
