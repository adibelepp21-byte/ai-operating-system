# Evidence Correction — Script Hashes of S-6, TD and FR-1 Baseline Evidence

| Field | Value |
|---|---|
| **Authority** | FD-FR1-001 `§7` (Register `§159`) |
| **What it corrects** | three evidence outputs whose recorded `script_sha256` no longer matches the script now in the repository |
| **What it does not do** | overwrite, edit or re-date any original output. The originals are preserved byte-for-byte; the corrected outputs sit beside them with the suffix `.CORRECTED.json` |
| **Result** | **No finding changed.** Each corrected output equals its original in every field except `checked_at` / `captured_at`, `script_sha256` and `head` |

## 1. Cause

During FR-1 (Register `§158`) I changed how my evidence scripts load P12-W2:
- **Before:** `from tools import p12_operational_state as w2`.
- **After:** `importlib.import_module("tools.p12_operational_state")`. This is the pattern the certified P12-W2 verifier discloses, and it stops an evidence tool from being counted as a system consumer by the certified P12 consumer measurement.

That fixed a real regression, but it changed script bytes after their outputs had been produced:

| Output (original, preserved) | Recorded `script_sha256` | Script that produced it | Script now |
|---|---|---|---|
| `S6-FRONTIER-DISCOVERY-2026-10-03.json` | `7ffb6b33…` | `s6_frontier_discovery.py` as committed in `a7a0860` (sha matches) | `23d1a1c4…` |
| `TD-STATE-AUTHORITY-DISCOVERY-2026-10-04.json` | `32676289…` | `td_state_authority_discovery.py` as committed in `a046f9c` (sha matches) | `c46f7159…` |
| `FR1-BASELINE-2026-10-03.json` | `d397d92b…` | an uncommitted earlier `fr1_baseline.py`: the output was captured, then the script was edited before the FR-1 commit | `d32d9ac2…` (as committed in `8600e12`) |

**The originals' chain is intact:**
- S-6 and TD each match the script committed with them.
- FR-1's baseline matches a script version that was never committed. Its *output* was committed in `8600e12`.

## 2. Method: reproduce, do not rewrite

Each current script was run in a **separate git worktree** checked out at the state its original was produced in, so the reading is of the same repository state:

| Corrected output | Worktree state | sha256 |
|---|---|---|
| `S6-FRONTIER-DISCOVERY-2026-10-03.CORRECTED.json` | `a7a0860` (the S-6 commit) | `400ab86b6b4cdba558dd43dcb346fded4015f054a43cda48a3a30fb3c634de9e` |
| `TD-STATE-AUTHORITY-DISCOVERY-2026-10-04.CORRECTED.json` | `a046f9c` (the TD commit) | `0909a7b16da46b779d0448ac8cf20d7e1d119317b34b74d52a3a26ebe22fb348` |
| `FR1-BASELINE-2026-10-03.CORRECTED.json` | `a046f9c` + the FD-TD-001 act + the Register through `§157`. This is exactly the state at capture, before any FR-1 code changed | `97a546ade8d7f6f3eb1de372256458233c12be60d706fa622a0a638d353d858e` |

Each output was compared field by field with its original. The only fields excluded from the comparison are the volatile ones (timestamp, `script_sha256`, `head`). **Differences: 0, 0 and 0.** All three corrected outputs carry the current script's sha, so the chain *output → script* is whole again for the current scripts. The worktrees were removed afterwards.

## 3. Disposition

- **The originals remain the evidence of record** for S-6 (`§154`), TD (`§156`) and FR-1 (`§158`). The corrected outputs establish that the current scripts reproduce them exactly.
- **The S-6 and TD findings are not materially affected.** FD-FR1-001 `§7` therefore requires no change to them, and none was made.

## 4. Also found, not corrected here

`AGENCY-E2E-SANDBOX-2026-10-02.json` records `script_sha256` `a30c71b3…` for a sandbox script that was **never in the repository** (`AIOS-EXECUTIVE-AGENCY-INTEGRITY-TEST.md`, Register `§130`). This is not a modification. It is a pre-existing provenance limit of that run: its script is not resident and cannot be re-run. It is outside FD-FR1-001 `§7` and is reported, not altered.
