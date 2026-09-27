# AIOS Full Stack

The application and access layer over AIOS: a standard-library WSGI backend
and a dependency-free console. Records and decisions: `docs/fullstack/`.

```text
Frontend (fullstack/frontend) → API v1 (fullstack/backend/api.py)
  → AIOS adapter (fullstack/backend/aios.py) → Runtime · Execution · Workflow · Tools · Trace
```

## Run

```bash
python -m fullstack.backend serve --data-dir /path/outside/the/repo   # http://127.0.0.1:8765/
python -m fullstack.readiness evaluate                               # the FS-09 gate, as JSON
```

## Deploy (Vercel + Supabase; FS-DP-01, FS-DP-04, ratified `FS-ARCH-RAT-001`)

```text
vercel.json → static console (fullstack/frontend) + /api/v1/* → api/index.py
  → fullstack/deploy/vercel.py: one Runtime per request over SupabaseStorage
  → aios_records in Supabase project scfymftfzkpilqbgmfwv
```

The schema is `fullstack/deploy/supabase/migrations/`. The function needs the
server-side key in `SUPABASE_SECRET_KEY` (set by the operator in Vercel, never
committed); without it every API route answers 503. There is no filesystem
fallback. A preview is not a release: production is the Founder's decision
(`FD-FS-001` D4-A).

Authentication is **operator bearer tokens** (`FS-DP-02` B3, Architect decision,
Register `§81`). The server reads `AIOS_OPERATOR_TOKENS` from the environment:
a JSON array of `{"subject", "sha256", "scopes"}`, holding the SHA-256 of each
token, never the token. `scopes` defaults to `aios.observe`. Without that
variable, or if it does not parse exactly, nobody is authenticated and every
route except `/api/v1/health` answers 401.

To issue a token, on your own machine:

    python -m fullstack.backend operator-token --subject founder \
        --scope aios.observe --scope aios.workflow.run --scope aios.audit

It prints the token once, for the console's credential field, and the entry
for `AIOS_OPERATOR_TOKENS`. Put the entry (only the entry) in the host's
environment as a sensitive variable. Rotate by issuing a new token and
replacing its entry.

## Test

```bash
python -m unittest discover -s fullstack/tests -t .        # includes the frontend and browser tests
node --test fullstack/frontend/tests/*.test.mjs            # frontend units alone
```

The browser test needs Node.js and Playwright; it is skipped, and says so,
where they are absent.
