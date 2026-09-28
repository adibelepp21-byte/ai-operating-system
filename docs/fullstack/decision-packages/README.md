# Full Stack Decision Packages (`FD-FS-001` D2-A)

**Status when prepared: PROPOSED — NOT RATIFIED** (each package's own Status row gives its current state). Prepared by Claude Code
under `FD-FS-001` D2-A: *"Claude Code shall prepare ADR/decision packages for
Architect ratification; Claude Code shall not treat preparation as
ratification."* The holder of Architect authority decides. `FD-2` (Founder ≡
Architect) is open, so each decision records in which capacity it is made.

## Why each package has two parts

Two rules meet here:

- **Freeze `§10`** reserves these areas to the Architect: each *"awaits an
  Architect decision before it enters any freeze."*
- **Engineering Constitution `§3.4`**: an ADR *"may not … introduce a
  technology, language, framework, or infrastructure decision."*

So each package separates:

- **Part A — Architectural decision.** ADR-eligible. Written as the ADR it
  would become. It carries no provider or technology.
- **Part B — Implementation and infrastructure decision.** Not ADR-eligible
  (`§3.4`). Presented for an Architect decision under Freeze `§10`, within the
  Founder's constraints: Vercel for hosting, Supabase for the database, no
  spending (D3-A); a separate Founder release decision (D4-A).

**Identifiers are provisional** (`FS-DP-nn`). The ADR README assigns ADR
numbers *"by the approving authority when an ADR enters Under Review"*, so no
ADR number is taken here.

| Package | Area | Blocks |
|---|---|---|
| [`FS-DP-01`](FS-DP-01-DATABASE.md) | Database implementation | FS-04 production persistence; FS-08; FS-09 data criteria |
| [`FS-DP-02`](FS-DP-02-IDENTITY-AND-AUTHENTICATION.md) | Identity and Authentication | FS-06 authentication; every authenticated route in production |
| [`FS-DP-03`](FS-DP-03-NETWORKING.md) | Networking | FS-08 ingress and TLS |
| [`FS-DP-04`](FS-DP-04-DEPLOYMENT.md) | Deployment | FS-08; FS-10 |
| [`FS-DP-05`](FS-DP-05-SCALING.md) | Scaling | FS-08; FS-09 performance |
| [`FS-DP-06`](FS-DP-06-OBSERVABILITY.md) | Observability implementation | FS-08; FS-09 observability |
| [`FS-DP-07`](FS-DP-07-AGENT-CREATION.md) | Agent creation through the application (Agent Factory boundary) | FS-07 Scenario A |
| [`FS-09-ENV`](FS-09-ENV-ENVIRONMENT-SEPARATION.md) | Environment separation (Production data apart from Preview data) | FS-09 environment separation |
| [`FS-09-RUNTIME`](FS-09-RUNTIME-PYTHON-RUNTIME-REPRODUCIBILITY.md) | Python runtime reproducibility | FS-09 runtime pin; reproducible deployment |

`FS-DP-03`, `FS-DP-06` and `FS-DP-07` carry a **Revision 2** (FS-09 Architect
review, Register `§89`); `FS-09-ENV` and `FS-09-RUNTIME` were prepared at `§89`.
Each package's analytical recommendation was **UNRATIFIED** until decided.
**All five were decided by the Founder in ACT-004** (Register `§93`: FS-DP-03 N1,
FS-DP-06 L1/M1/R2 with alerting undecided, FS-DP-07 A1, FS-09-ENV E1, FS-09-RUNTIME P2).

## Minimum decision set

To reach a first deployable system, the minimum is **FS-DP-01, 02, 03, 04 and
06**. FS-DP-05 can take its recommended "no scaling decision beyond host
defaults" as written. FS-DP-07 can stay reserved without blocking any other
stage.
