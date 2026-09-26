# `FD-PO-004` — Founder Selections: D1-A · D2-A · D3-A · D4-A

**Document type:** Founder Decision, recorded from the Founder's answers
**Decided by:** Founder · **Date:** 2026-09-26
**Instrument:** `acts/FD-PO-004-PLATFORM-ORGANIZATION-CANONICALIZATION-DISPOSITION.md`
(content sha256 `166d6a25…`; Register `§52`)

## Provenance

The instrument arrived with every selection blank. Its `§15` says *"No blank
field may be interpreted as approval."* So the Founder was asked the four
questions through the session's question tool.

**The questions and the Founder's selected answers are reproduced exactly
below.**
- Claude wrote the questions and the option labels.
- Each option restated the instrument's own option, with the boundary the
  instrument attaches to it.
- The Founder chose the answers. No notes accompanied them.

````text
Q (D1): FD-PO-004 D1: how should the six PD-05 to PD-10 volumes be disposed? (Every UNKNOWN, RESERVED-DECISION and BOUNDED-RECONSTRUCTION section stays exactly as classified whichever option you pick.)
A: D1-A Certify w/ residual

Q (D2): FD-PO-004 D2: what is the residency disposition for PD-03 and PD-04 (Volumes 3 and 4, ESC-C7-01)?
A: D2-A Supply volumes

Q (D3): FD-PO-004 D3: should the Security Owner role be bound to PD-08 (FDP-P10-001)?
A: D3-A Bind

Q (D4): FD-PO-004 D4: should the Quality authority be bound to PD-09 (FDP-P10-002)?
A: D4-A Bind
````

## The decision, in the instrument's terms

| Matter | Selection | Instrument text it selects |
|---|---|---|
| D1 | **D1-A — CERTIFY WITH CLASSIFIED RESIDUAL** | the six volumes become *"canonical Platform Organization construction baselines while preserving every UNKNOWN, RESERVED-DECISION, BOUNDED-RECONSTRUCTION classification exactly as recorded"*. It does not mean *"ALL ARCHITECTURAL QUESTIONS FINALLY RESOLVED"* |
| D2 | **D2-A — SUPPLY / TRANSMIT VOLUMES 3 AND 4** | *"Provide or authorize the source bodies"*. Claude Code then *"RECEIVE → VERIFY → RECONCILE → CHECK FN-1 → UPDATE EVIDENCE"*. *"No source content may be reconstructed"* |
| D3 | **D3-A — BIND SECURITY OWNER → PD-08** | *"within the existing governance model and stated boundaries"*, and *"does not grant authority beyond the established Security Owner boundary"* |
| D4 | **D4-A — BIND QUALITY AUTHORITY → PD-09** | *"within the existing governance model and stated boundaries"*, and *"does not expand Quality authority beyond its established boundary"* |

## Effect, stated narrowly

- **D1-A closes `G-01`.**
  - `G-01` recorded that no definitional corpus existed for PD-05 … PD-10.
    The Founder has now certified the constructed volumes as that corpus.
  - The certification is of a **construction baseline**. The volumes are not
    frozen and not activated.
  - Every section keeps the class it had when certified.
- **D3-A closes `FDP-P10-001`, and D4-A closes `FDP-P10-002`.**
  - Each role is bound within the boundary the frozen corpus already gives it.
  - The volumes' A3 and A4 sections keep the class RESERVED-DECISION,
    because classifications are preserved (instrument `§2`, `§8`). The binding
    is recorded beside them, in the volume header, and not rewritten into
    them.
- **D2-A authorizes supply. It does not close `ESC-C7-01`.** The Volume 3 and
  4 bodies have not been transmitted.
  - Until they are received and verified, the absence stays an explicit
    evidence condition, and `FN-1` stays unassessable.
  - On receipt, the E-29 precedent applies: a named Founder instrument (this
    one) and the `volume-N/` namespace convention of `ADR-0012`.
  - Nothing is reconstructed in the meantime.

## What this does not decide

Under the instrument's `§8`, the following stay as they were:
- `G-10` and `G-02`;
- the Part structure (`C6-A1`);
- `ADR-0029`;
- deferred architecture (`FRZ-10`) and reserved concepts (`FRZ-2`);
- every UNKNOWN section, and every Architect-reserved matter;
- P13 (still CLOSED), P14 (not created), the Constitution, Founder authority
  and the Delegation Charter.

It also does not decide `FDP-P10-003` (the Governance Authority binding) or
PD-01's activation (`RG-1`).
