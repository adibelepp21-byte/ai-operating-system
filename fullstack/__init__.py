"""AIOS Full Stack — the application and access layer over AIOS.

Built under `ACT-CC-POST-P13-AIOS-FULL-STACK-001` (authorized by `FD-FS-001`).
The layer *consumes* AIOS; it does not define it:

```text
Frontend  →  Backend API  →  AIOS contract adapter  →  Runtime / Execution / services
```

`native_core/` and `consumers/` are imported, never modified. Nothing in
`native_core/` or `tools/` imports this package.
"""
