"""Optimization boundary conformance tests (Native Core Blueprint §27).

Baseline 06 — L10 Optimization. The eleventh and last frozen subsystem
boundary. Unlike Baselines 04A–04C this is an **implementation** baseline: the
boundary is built here, and this suite verifies what was built.

Tests assert the requirements optimization_spec, Blueprint §15, and Roadmap
§9.11 name for this boundary:

  - **PR-3 — Detect, Don't Decide.** Optimization informs; Governance decides.
    Roadmap §9.11 rates *"automation acquiring a decision"* the **Critical**
    risk of this boundary, so the property is verified structurally rather than
    by documentation: no decision verb, authority surface, or approval path is
    representable.
  - **INV-8 — promotion only via governed review.** No promotion path exists;
    nothing here can move Memory into Knowledge.
  - **INV-5 — Trace immutable.** Optimization reads Trace and never writes it;
    no write surface is reachable from this boundary.
  - **INV-12 — no external dependency.** Cross-boundary imports are limited to
    the Trace and Memory public surfaces.
  - **PR-4 — fail closed.** An observation or proposal that cannot be formed
    accountably is refused, never degraded.

together with the two governance rulings that fixed this baseline's scope:

  - **P7-I27 Conflict A** — Optimization publishes for optional future
    consumption and holds **no Governance dependency**. Verified structurally:
    no governance import, and no submit/send/notify/request identifier exists.
  - **P7-I27 Conflict B** — the signal catalogue, evaluation scoring,
    prioritization, ranking, recommendation, decision heuristics, and promotion
    strategy remain **Architect Reserved**. Verified as *absent*: the suite
    asserts the reserved design space was preserved, not filled.

and **P7-I27 Conflict C** — the legacy assets were not imported, copied, or
migrated. Verified by dependency sweep.

Verification is **structural wherever possible** — AST inspection, dataclass
inspection, `inspect.signature`, abstract-interface inspection, public-API
inspection — in preference to runtime simulation.

Standard-library `unittest` only. No external dependency (INV-12).
"""
