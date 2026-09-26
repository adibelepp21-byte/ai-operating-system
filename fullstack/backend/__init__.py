"""The AIOS Full Stack backend (FS-03): a standard-library WSGI application.

Modules:

* `aios`      — the single adapter from the application layer onto AIOS contracts;
* `docs_tool` — the one Tool the application registers: read-only `docs.read`;
* `security`  — principals, the authenticator port, scope authorization, audit;
* `api`       — HTTP routing, the API contract, the static frontend;
* `__main__`  — `python -m fullstack.backend serve …`.
"""
