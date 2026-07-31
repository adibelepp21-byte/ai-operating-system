"""
First Execution Harness — minimal, implementation-tier execution layer.

Lives entirely outside docs/, alongside tools/. It does not modify, and
is not itself, a governance artifact: no Framework, no Domain Model
content, no Constitution content. It exists to run one real path through
already-ratified artifacts and produce the first real Trace record, per
the AIOS Chief Architect Directive — Initiate First Execution Harness
Phase.

Governance boundaries this package respects, by construction:

- Agent Instance is materialized as an in-memory, ephemeral object only
  (agent_instance.py). It is never written to disk as a persistent
  document — Domain Model §5/§6 mark it unowned and "no governance
  overhead per instance."
- Runtime binding (runtime.py) reads the three already-documented
  Runtime instances; it does not add any new Runtime relationship or
  governance content.
- Workflow execution (workflow.py) follows a Workflow's already-declared
  Contains Skill order; Workflow Framework §10 explicitly excludes
  execution-order semantics from governance, so document order is used
  here as an implementation-tier choice, not a governance assertion.
- Skill and Tool invocation (skill.py, tool.py) are deliberately crude,
  honestly-labeled stubs — this harness exists to prove the
  orchestration path and produce real evidence, not to implement
  genuine governance-review reasoning.
- Trace production (trace.py) implements Domain Model §2.1's required
  content shape and Constitution §14.2's unconditional-production rule
  as real code for the first time. It is not a Trace Framework: no
  governance document is created, and its storage format is an
  explicit, disposable implementation choice.

No retries, scheduling, distributed execution, authentication, rate
limiting, or resource allocation are implemented. Those are explicitly
out of scope for this phase.
"""
