# FS-DP-03 — Networking

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-03` (provisional) |
| **Area** | Networking — Freeze `§10`, Architect-reserved |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A) |
| **Founder constraints** | Vercel hosting; Supabase database; no spending (D3-A) |
| **Prepared by** | Claude Code, 2026-09-26 |

## Context

- The Frontend talks only to the Backend; the Backend alone reaches AIOS and
  the database (FS-02 `§1`).
- Locally the backend binds `127.0.0.1` only; `--host` must be given to bind
  anything else.
- No CORS is configured: the frontend is served from the same origin.

## Part A — Architectural decision (ADR-eligible)

**Question.** What may reach what?

**Recommended rule set:**

1. **One ingress**: the application edge serving the Frontend and
   `/api/v1` on **one origin**. No cross-origin API access.
2. **AIOS is never network-addressable.** It runs inside the backend process
   and has no listener of its own.
3. **The browser never reaches the database.** Only the backend holds a
   database credential (FS-DP-01 Part B, RLS with no browser policy).
4. **Egress** from the backend only to the database and, if chosen, the
   identity provider (FS-DP-02). Tools reach nothing external today; any
   future external Tool is its own decision (INV-12).

Alternative: a separate API origin with CORS. Not recommended; it widens the
attack surface for no requirement found in FS-01.

## Part B — Implementation decision (not ADR-eligible)

- TLS terminated by the host; HTTPS only; HSTS set at the edge.
- The host's default domain first. A custom domain needs DNS ownership, which
  is an external dependency, and may need a paid plan.
- Supabase reached over its TLS endpoint; connection pooling per FS-DP-05.

## Until decided

Local loopback only. Nothing is exposed.

## Exact decision required

- [ ] Part A rule set: as written · amended
- [ ] Part B: as written · amended; custom domain yes/no
- [ ] Decided as: Architect · Founder as Architect
