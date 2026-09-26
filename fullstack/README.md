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

The shipped server authenticates **nobody** (`NoAuthenticator`): the
authentication mechanism is Architect-reserved (`FS-DP-02`). Every route except
`/api/v1/health` answers 401 until it is decided.

## Test

```bash
python -m unittest discover -s fullstack/tests -t .        # includes the frontend and browser tests
node --test fullstack/frontend/tests/*.test.mjs            # frontend units alone
```

The browser test needs Node.js and Playwright; it is skipped, and says so,
where they are absent.
