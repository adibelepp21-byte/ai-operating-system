# AIOS Operations — live operational state

This directory holds **live** operational state: records that are meant to
change as the system runs. It is deliberately outside every phase directory.

**Why it exists.** Until `GOAL-V2-002`, runtime observations were published into
`docs/architecture/p12/runtime-observations/`. `FD-P12-006` certified P12, so
that directory became certified evidence. An observation is a live projection
(*"these files state what was last observed"*), so each run rewrote certified
evidence. A phase's certification must freeze its evidence and nothing live.
Live state therefore lives here, where no phase certification can capture it.

| Path | What it holds | Writer | Readers |
|---|---|---|---|
| `runtime-observations/` | The latest published observation per runtime or workflow id | `tools/p12_runtime_observation.publish` (default root) | `tools/p12_runtime_observation.observations` and everything built on it (self-model *"What is running?"*, operational state, integration graph) |

**How the live and certified observations relate.**
`p12_runtime_observation.observations()` reads P12's certified observations
(`docs/architecture/p12/runtime-observations/`, origin `certified-p12`) and this
live root (origin `live`). A live record supersedes a certified one for the same
id. The certified files are never written: `publish` routes through
`tools/p12_certified_evidence_guard.guard`, which refuses them. They are
verified byte-for-byte against
`docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json`.

**It started empty.** At the move, the certified root held two observations
written after certification, from commits `7f6120c` and `d18bac4`. Both came
from test-suite runs, not from real operation. They were not carried into this
root, and the certified files were restored to their certified bytes. The later
values remain in git history. The record is
`docs/governance/AIOS_GOAL_V2_002_P12_CERTIFICATION_INTEGRITY_RECORD_v1.0.md`.

This file carries no authority.
