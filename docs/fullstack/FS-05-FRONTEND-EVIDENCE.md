# FS-05 — Frontend: Evidence

| Field | Value |
|---|---|
| **Stage** | FS-05 Frontend (Act `§16`) |
| **Code** | `fullstack/frontend/`: `index.html`, `styles.css`, `app.js` (DOM), `api.js` (the only route to the backend), `model.js` (pure presentation logic) |
| **Tests** | `fullstack/frontend/tests/*.test.mjs` (13, `node --test`); the browser run in `fullstack/tests/e2e/console.e2e.mjs` (12 checks, Chromium via Playwright) |
| **Screenshots** | `docs/fullstack/evidence/e2e/` (from the browser run) |

## Surfaces

| Surface | Shows | Acts |
|---|---|---|
| Overview | Runtime state, identity, hosted subsystems; run counts; the authentication mechanism in force | — |
| Workflows & runs | the catalog and its steps; every run with states, steps, criteria, failure reason, Trace range | start a run (enabled only with `aios.workflow.run`) |
| Tools | registered Tools and lifecycle; the governance ledger with all four dispositions | — |
| Traces | every Trace record, paged | — |
| Audit | every access decision | — |
| Session | who the backend says you are, and your scopes | enter or clear a credential |

The roadmap's advice is followed: an operating console, not a chat box, and
its sections mirror AIOS (Runtime, Workflows, Tools, Traces, Governance).

## Boundary

- The frontend talks only to `/api/v1` on its own origin (`api.js`). It
  never reaches AIOS.
- It holds no authority. It disables *Start run* for a principal without
  `aios.workflow.run`, for clarity only. The browser test re-enables the
  button, submits, and shows the backend's 403.
- Every backend value is written with `textContent`. The browser test submits
  `<img src=x onerror=…>` as a criterion; it renders as text and no element
  or dialog appears.
- The CSP forbids inline script; the test fails on any script error, CSP
  violation or dialog.

## Defect found and repaired (Act `§9`)

The first browser run's screenshot of the observer's Audit view showed the
refusal banner **above the audit rows loaded earlier under the operator's
credential**. Data rendered for one principal stayed on screen for another.
The backend had refused correctly; the console had not cleared.

- **Repair**: every view is cleared before it renders, and all views are
  cleared when the credential is set or cleared (`clearViews` in `app.js`).
- **Control**: the browser test now asserts that the refused Audit view holds
  no rows. It would have failed before the repair.

## Exit determination (`§16`)

| Criterion | Result |
|---|---|
| Frontend builds | No build step; served as files |
| Required application surfaces function | six surfaces, driven in Chromium |
| Backend integration works | every surface reads the live backend |
| State handling works | runs, states and Traces reflect the backend after each action |
| Authorization is respected | the observer is refused, in the UI and at the API |
| Meaningful runtime / execution states visible | lifecycle states, step statuses, failure reasons, Trace ranges |
| Error states represented | 401, 403, 503, offline, invalid input (`classifyError`) |
| Tests pass | 13 / 13 units; 12 / 12 browser checks |

**FS-05: EXIT CRITERIA MET.**
