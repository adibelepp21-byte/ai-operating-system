# FS-09-RUNTIME — Python Runtime Reproducibility

| Field | Value |
|---|---|
| **Identifier** | `FS-09-RUNTIME` (provisional) |
| **Area** | The Python version the deployed function runs, pinned in the repository; Architect-reserved (part of the deployment arrangement, `FS-DP-04`, and a conflict with the FS-02 blueprint) |
| **Status** | **RATIFIED — P2** (Python 3.12), by the Founder as Architect in `ACT-CC-POST-P13-AIOS-FULL-STACK-004` `§16` (Register `§93`, `ACT-004-DG-05`). Implemented: `.python-version` = 3.12; FS-02 amended; the Preview build reads *"Using Python 3.12 from .python-version"*. The analysis below is the package as reviewed (`§89`) |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | Vercel; no spending (D3-A); live re-verification needs Founder-authorized Preview access |
| **Prepared by** | Claude Code, 2026-09-27, on the Founder's *"FS-09 — DECISION PACKAGE PREPARATION"*. Options P1–P3 as recorded in `FS-09-DECISION-REGISTER.md` `§1.5` |

## 1. Decision ID

`FS-09-RUNTIME` (provisional). Register `§89`. Named `PYTHON-RUNTIME-VERSION`
in the `§88` records and in the readiness gate before this package.

## 2. Exact architectural question

Which Python version must the deployed AIOS Full Stack run, and must it be
pinned in the repository so that every build uses it?

## 3. Canonical sources

| Source | What it says |
|---|---|
| `FS-02` `§3` Technology (line 47) | *"Backend language \| Python 3.11 standard library \| AIOS is stdlib-only; the adapter calls it in-process"* |
| `FS-00` `§3` (line 37) | *"Measured on the entry commit. Python 3.11 standard library only"* |
| `FS-ARCH-RAT-001` (ratified `FS-DP-01`/`FS-DP-04`) | a *"Python backend"*, a *"Vercel Python Function"*: **no version** |
| ACT-001 `§20` | Reproducibility: clean build, reproducible deployment, known artifact |
| ACT-003 `§12` | configuration |
| The Founder's FS-09 Workstream D | *"If the exact version cannot be established from canonical evidence, STOP and report the ambiguity instead of inventing one"*. Stopped at `§88` |

## 4. Current implementation state: the reconciliation

The four facts, stated as they are and not reinterpreted:

| # | Fact | Evidence | Class |
|---|---|---|---|
| **F1** | **FS-02 names Python 3.11.** The text is a version, *"Python 3.11 standard library"*. It is not read here as "3.11 or later", nor as "whatever Python", nor as "standard library only, version immaterial". FS-02 was constructed under ACT-001 `§13` and is not Architect-ratified. The ratified `FS-ARCH-RAT-001` names no version, so FS-02 is the **only** canonical statement of a version | `docs/fullstack/FS-02-FULL-STACK-ARCHITECTURE-BLUEPRINT.md` line 47; `FS-00` line 37 | canonical text |
| **F2** | **Local and certified evidence uses 3.11.** Every certified phase (P10–P13), every regression run in this program, and the FS-09 gate ran on Python 3.11 (3.11.15 here). Latest full run (`§88`): native_core 801, consumers 276, bounded_exception 29, fullstack 172, tools 1933: all OK | regression logs; Register `§86`, `§88` | local-current / certified |
| **F3** | **Preview evidence uses 3.12.** The FS-08 Preview (`dpl_Gi3MbQkzo14aW4TriGwQ9TYMudgL`, commit `6469269`) was built with the host default: *"No Python version specified in .python-version, pyproject.toml, or Pipfile.lock. Using python version: 3.12"* (build log `bld_8ubuwdj02`). All 14 live checks passed on it. **The live evidence was therefore produced on a runtime that differs from F1 and F2** | Vercel build log | preview-recorded |
| **F4** | **Vercel's 3.11 support cannot be established from current evidence.** The Vercel documentation retrieved (three searches) shows the pinning mechanisms (`.python-version`; `requires-python` in `pyproject.toml`) with 3.12 and 3.13 in its examples, and no list of supported versions. Establishing it needs a build with 3.11 pinned, which is a deployment and is not done here | `search_vercel_documentation`, 2026-09-27 | none |

Additional evidence gathered for this package (it decides nothing):

| Interpreter | native_core | consumers | bounded_exception | fullstack | tools |
|---|---|---|---|---|---|
| 3.11.15 | 801 OK | 276 OK | 29 OK | 172 OK | 1933 OK (`§88`) |
| 3.12.3 (local) | 801 OK | 276 OK | 29 OK | 172 OK | 1933 OK (1 skipped) |
| 3.13.12 (local) | 801 OK | 276 OK | 29 OK | 172 OK | not run |

**The conflict, stated plainly:** the canonical text (F1) and all certified
evidence (F2) say 3.11. The only live evidence (F3) ran on 3.12, because
nothing pins the version. Whether the host can run 3.11 at all is unknown (F4).
No single version is established by canonical evidence together with verified
live evidence.

## 5. Authority required

**Architect** (or the Founder acting as Architect): the version is part of the
deployment arrangement, and choosing anything other than 3.11 **amends FS-02**
explicitly. **Founder**: Preview access for the live re-verification each
option needs.

## 6. Available options (P1–P3, exactly as registered)

| ID | Option |
|---|---|
| **P1** | pin **3.11**: the blueprint (F1) and all local and certified evidence (F2); host availability to be verified (F4) |
| **P2** | pin **3.12**: the version the live evidence ran on (F3); **FS-02 amended** to say so, by explicit decision |
| **P3** | leave **unpinned**: the host's default decides, and may change without a commit |

## 7. Architectural consequences

| Option | Consequence |
|---|---|
| P1 | architecture, local evidence and deployment agree on one version, provided the host builds it. FS-02 unchanged |
| P2 | architecture amended to follow the deployment; FS-02's technology row changes by decision, not by drift |
| P3 | the deployed runtime is outside the architecture's control. The FS-02 row stays true only by accident |

## 8. Data and state consequences

None for any option. The records are JSON produced by the standard library
with sorted keys and fixed separators, and the restore tests (which check
per-partition digests of the live export) pass on 3.11, 3.12 and 3.13. The
store's bytes do not depend on the choice.

## 9. Security consequences

| Option | Consequence |
|---|---|
| P1 | CPython 3.11 is in its security-fix-only phase; upstream end of life is October 2027 (PEP 664), about 13 months from now |
| P2 | CPython 3.12: security fixes until October 2028 (PEP 693) |
| P3 | the version, and its patch level, change whenever the host changes its default. An unreviewed interpreter change reaches the deployment with no commit |

## 10. Operational consequences

| Option | Consequence |
|---|---|
| P1 | if the host refuses 3.11, the Preview build fails (Production unaffected), and the decision must be revisited. Upgrading before October 2027 becomes a planned change |
| P2 | local development and the regression move to 3.12 as the reference, so the certified-evidence runs must be repeated on 3.12. All five suites already pass there locally (`§4`) |
| P3 | nothing to maintain, and nothing guaranteed |

## 11. Verification requirements

1. The pin file (`.python-version`, or `requires-python` in `pyproject.toml`; which mechanism is part of the implementation) contains the decided version.
2. A Preview build log that reads *"Using python version: X"* for the decided X (and not *"No Python version specified"*).
3. A full local regression on the decided version: all five suites.
4. **If the decided version is not 3.12**, the FS-08 live suite is re-run on the Preview, because the recorded live evidence ran on 3.12 (F3). This needs Founder-authorized temporary access.
5. The readiness gate checks the pin file against the decision, and its *runtime version pinned* row changes from BLOCKED only after 1–4 are recorded.

## 12. Rollback implications

* A Vercel deployment keeps the runtime it was built with. Instant rollback to an earlier deployment serves that deployment's runtime (3.12 for every Preview so far).
* **Rebuilding** an older commit without a pin uses the host default at rebuild time, not the version it first ran on.
* Removing a pin (rolling back its commit) returns the build to P3.

## 13. Explicit non-scope

No pin is added. FS-02 is not edited. No test build or deployment is made. No
version is assumed from the host's behaviour. The 3.11 reference is not
reinterpreted.

## 14. Dependencies

| On | Why |
|---|---|
| `FS-DP-04` A1 (ratified) | the deployment arrangement this completes |
| Founder | Preview access for re-verification (`§11` item 4) |
| `FS-DP-03` | none directly; a protected Preview needs authorized access for item 4 |

## 15. Whether it blocks FS-09

**Yes.** Gate row *Reproducibility: runtime version pinned* is BLOCKED on this
package. Without a pin, the deployed runtime is not reproducible from the
repository (ACT-001 `§20`).

## 16. Analytical recommendation (**UNRATIFIED**)

> *Not a decision. Stands only as analysis until the Architect decides.*
> **P2** (pin 3.12, with FS-02 amended explicitly). Its stated condition, a
> full `tools` pass on 3.12, is met locally (1933 OK, `§4`). It is the only version on which live evidence
> exists (F3), it needs no unverified host capability (F4), and it has the
> longer security support. **P1** stays fully valid if the Architect prefers
> the blueprint as written; it then needs a Preview build proving 3.11 is
> available, and the FS-08 suite re-run on it.

## 17. Exact decision required

- [ ] P1 (3.11) · P2 (3.12, FS-02 amended) · P3 (unpinned)
- [ ] Mechanism: `.python-version` · `requires-python` (implementation, may be delegated)
- [ ] Decided as: Architect · Founder as Architect
