"""Agent boundary conformance tests (Native Core Blueprint §27).

Baseline 04C — Agent Conformance. A **verification** baseline: it verifies the
Agent boundary's existing architectural structure and adds no behavior.

Tests assert the invariants agent_spec and Blueprint §8 name for this boundary:

  - **INV-2** — an Agent Definition is owned by exactly one Department and
    implements at least one Capability. Neither binding is modelled here:
    agent_spec §12/§13 reserve governed construction (the *Agent Factory*) to
    the Architect. The suite verifies the reservation is intact — no
    unreserved binding, factory, or registry was introduced.
  - **INV-3** — an Agent Instance instantiates **exactly one** Agent
    Definition. This is enforced structurally: `AgentInstance` holds a single
    required `AgentDefinition` and cannot be constructed without it. The
    invariant's second clause — *hosted by exactly one Runtime* — is
    deliberately not modelled, because binding an Instance to its host is
    Runtime's concern; the suite verifies that absence rather than inventing it.
  - **INV-4** — every Agent-Instance action produces exactly one Trace. Agent
    authors none: it imports nothing from Trace, and Trace imports nothing from
    Agent. The identity fields Trace records (`agent_definition_version`,
    `agent_instance`) are name-identical here, so no terminology drift exists.
  - **INV-12** — Tool is the only entity permitted an external dependency, so
    this boundary holds none. Its sole cross-boundary import is the
    `ExecutionConsumer` contract.
  - **INV-13** — coordination runs through Workflow only. An Agent's single
    entry point is the inherited `participate(execution)`, and the Execution
    boundary carries no route to another Agent.

together with the boundary's dependency direction (Agent → Execution only, with
no reverse edge and therefore no cycle), its repository placement as a sibling
of `runtime/` rather than a child of it (Blueprint §3/§8), and the reserved
status of Agent behavior, identity attribution, and the Agent Factory
(agent_spec §12/§13/§14).

Verification is **structural wherever possible** — AST inspection, dataclass
inspection, `inspect.signature`, abstract-interface inspection, public-API
inspection — in preference to runtime simulation.

**Finding F-3 is record-only.** The package public surface exports `Agent`
alone while `AgentDefinition`, `AgentInstance`, and their fail-closed errors are
defined but undeclared. This suite records that state as found. It is not a
repair, and not a judgement that the exports are required — disposition is
reserved to the Architect.

**No source file in this boundary is modified by this baseline.** Any
requirement or defect discovered is reported as evidence, never repaired here.

Standard-library `unittest` only. No external dependency (INV-12).
"""
