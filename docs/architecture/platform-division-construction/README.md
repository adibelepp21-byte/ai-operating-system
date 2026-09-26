# Platform Division Construction — PD-05 … PD-10

| Field | Value |
|---|---|
| **Authority** | `ACT-CC-POST-P13-PLATFORM-ORG-003` as amended by v1.1 (Register `§47`, `§48`), authorized for execution by `FD-PO-003-01` (`§49`) |
| **Status** | CONSTRUCTED — NOT CANONICAL · NOT FROZEN · NOT ACTIVATED |
| **Verifier** | `tools/platform_division_construction.py` (read-only). The gate reports its result under `construction` |
| **Tests** | `tools/tests/test_platform_division_construction.py` |

## What this namespace is

It holds the construction volumes for the six Platform Divisions that had no
definitional corpus (`G-01`):
- built under the Amendment's rule, *"DISCOVER → CLASSIFY → ESTABLISH
  IDENTITY … EVOLUTION → VERIFY"* (v1.1 `§20`);
- placed **outside** `docs/architecture/volume-N/`, the resident-corpus
  namespace, so that no reader can take a constructed volume for a supplied
  canonical one (v1.1 `§23` NC-15);
- placed **outside** the certified P10 root, which is not modified (v1.1 `§24`).

| CPID | Volume |
|---|---|
| PD-05 | [`pd-05-runtime-and-execution/VOLUME.md`](pd-05-runtime-and-execution/VOLUME.md) |
| PD-06 | [`pd-06-ai-engineering/VOLUME.md`](pd-06-ai-engineering/VOLUME.md) |
| PD-07 | [`pd-07-infrastructure-and-platform/VOLUME.md`](pd-07-infrastructure-and-platform/VOLUME.md) |
| PD-08 | [`pd-08-security/VOLUME.md`](pd-08-security/VOLUME.md) |
| PD-09 | [`pd-09-quality-and-evaluation/VOLUME.md`](pd-09-quality-and-evaluation/VOLUME.md) |
| PD-10 | [`pd-10/VOLUME.md`](pd-10/VOLUME.md): the directory carries the CPID only, because the name is held open (`G-02`) |

The other documents here:
- [`F5-EVIDENCE-CLASSIFICATION-MATRIX.md`](F5-EVIDENCE-CLASSIFICATION-MATRIX.md): v1.1 `§14`;
- [`CROSS-PD-RECONCILIATION-AND-MAP.md`](CROSS-PD-RECONCILIATION-AND-MAP.md): v1.1 `§21`, and the PD-01 … PD-10 construction map;
- `CONSTRUCTION-MANIFEST.json`: the volumes' bytes.

## The rules every volume satisfies, checked by the verifier

1. **One class per section.** Each section states one `§20` dimension (or `—`)
   and one `§10` class. All eleven dimensions are present.
2. **Quotations are real.** Every `Source:` and `Reference:` line quotes text
   found in the cited file.
3. **Roadmap and derived material is never source.** ACT-003's own section
   lists, the P10 division records and this namespace can only be a
   `Reference:` (`§11`, `§18`).
4. **Reservations are recorded.** Each named reservation is a gate open item,
   or one of the four recorded here, and is still recorded in its source:

   | Reservation | Holder | Recorded in |
   |---|---|---|
   | `FRZ-10` | Architect | Freeze §10, deferred architecture |
   | `FRZ-2` | Architect | Freeze §2, reserved concepts |
   | `DM-6` | Architect | Domain Model §6, division and Capability lifecycle |
   | `DM-8` | Architect | Domain Model §8, Spine depth |

5. **No reserved binding is asserted:**
   - Security Owner → PD-08;
   - Quality authority → PD-09;
   - Governance Authority → PD-03;
   - Sub Division as a unit;
   - a division bound to `native_core` or `tools/`.
6. **No frozen text is copied.** No line of a frozen PD-01 body appears in a
   volume.
7. **Cross-PD reconciliation passes** (`reconcile()`).

## What the volumes are not

- **Not canonical.** Canonicalization, certification and freeze are
  Founder-reserved (v1.1 `§24`). The volumes are prepared for that step, and
  nothing here takes it.
- **Not a closure of `G-01`.** `G-01` records that no *definitional corpus*
  was supplied. These volumes are constructed, not supplied, so `G-01` closes
  only by its holder's decision. The gate's `§33` states for PD-05 … PD-10
  therefore do not move.
- **Not an assignment.** No Capability, Agent Definition, internal unit or
  implementation boundary is assigned to any division.
