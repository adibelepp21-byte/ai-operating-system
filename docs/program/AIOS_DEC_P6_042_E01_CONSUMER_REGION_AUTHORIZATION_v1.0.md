# `DEC-P6-042` — E-01 Consumer Region Authorization · Decision Record

**Identifier:** `DEC-P6-042`
**Subject:** Authorization of a fourth top-level repository region as canonical
residency for product/application consumer implementations
**Decision Type:** Founder architectural authorization
**Authority:** **Founder** · **Decision Owner:** Founder / Moriarty
**Status:** **AUTHORIZED**
**Consumed by:** `ACT-CC-P6-057` (issued as `ACT-CC-P6-055`) → `ADR-0028`

**Recorded by:** Co-Founder office under `ACT-CC-P6-059`
**Provenance:** transcribed faithfully from the Founder-issued instrument. The
Decision was issued inline, as §3 *"Founder Decision Consumed"* of the Act that
carried it. §1 below is that Founder-issued text, reproduced verbatim. The header
above and §§2–3 are repository metadata added by the recording office and are
marked as such.

---

## 1. Decision — Founder-issued text, verbatim

The Founder authorizes one fourth top-level repository region as canonical
residency for product/application consumer implementations outside:

- `docs/`
- `native_core/`
- `tools/`

The region is authorized specifically to provide canonical residency for E-01.

The authorization does not:

- change AIOS Mission;
- change Constitution;
- change Canonical Architecture;
- weaken the `native_core/core/agent/` boundary;
- change C1–C4;
- authorize use of `tools/` as product residency.

The exact name, layout, package structure, and implementation approach remain
delegated architecture decisions.

---

## 2. Issuance context — repository metadata, not Decision text

[A] Added by the recording office; **not part of the Founder-issued instrument.**

[E] The selection this Decision records was stated by the Founder in §1 of the
issuing Act:

> *"The Founder has selected: **A — Authorize a fourth top-level repository
> region for product/application consumer implementations.**"*

[A] That sentence is Act text, not Decision body, and is quoted here as
provenance only. It is **not** merged into §1 — the Decision body is exactly the
block the Founder placed under `## DEC-P6-042`, and nothing surrounding it in the
issuing Act has been absorbed into the Decision.

[E] The issuing Act carried the identifier `ACT-CC-P6-055`, which was already
consumed (E-01 Consumer Phase Authorization Gate → `ADR-0027`). By sequence it is
`ACT-CC-P6-057`. Recorded for traceability only; nothing is renumbered
(`ACT-CC-P6-058` §15).

## 3. Recording note — repository metadata, not Decision text

[A] Added by the recording office; **not part of the Founder-issued instrument.**

[E] **This is transcription, not recovery.** The complete text was issued
directly and is reproduced above; nothing was reconstructed, inferred,
paraphrased, or supplied. This Decision is therefore categorically unlike
`DEC-P6-034`–`041`, whose bodies are **UNRECOVERED** and which `DEC-P6-043`
ratified without asserting their wording. Nothing here bears on that gap.

[E] Formatting alone was normalised to the convention set by
`AIOS_DEC_P6_032_…`, `AIOS_DEC_P6_033_…` and `AIOS_DEC_P6_043_…`. No clause was
added, removed, reordered, summarised, or reworded (`ACT-CC-P6-059` §7).

[E] **Consumption is already complete and verified.** `ACT-CC-P6-057` built the
`consumers/` region and E-01 within this authorization; `ADR-0028` records the
architecture. Persisting this record changes nothing about that work and
re-opens nothing (`ACT-CC-P6-059` §5).
