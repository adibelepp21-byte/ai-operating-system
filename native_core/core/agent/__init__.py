"""
Agent boundary (Native Core Blueprint §3 root tree, §8 Agent Package; agent_spec;
Freeze INV-2/INV-3/INV-4/INV-8/INV-12/INV-13).

Agent is one of the **eleven frozen subsystem boundaries** and is a sibling of
`runtime/` in the core region — Blueprint §3 fixes the tree as
`core/{trace, memory, knowledge, governance, runtime, agent, capability, skill,
workflow, infrastructure, optimization}`, and "[E] each `core/<subsystem>`
boundary corresponds to a frozen subsystem and its engineering spec". Agent is
therefore **not** nested inside Runtime: Runtime does not own Agent (Blueprint §8
fixes Agent's own ownership — Definitions owned by one Department, Instances not
owned).

Phase 4.4 establishes the **contract only**:

    Infrastructure → Knowledge → Runtime → Execution → ExecutionConsumer → [Agent]
                                                                            → Workflow (future)
                                                                            → Skill (future)

`Agent` extends `ExecutionConsumer`, so an Agent participates **exclusively
through the Execution boundary** and never touches Runtime directly. Runtime
remains entirely unaware of Agent — there is no `Runtime → Agent` dependency and
no cycle.

NOT implemented here (later authorized phases): Agent behavior, reasoning,
prompts, LLM/model invocation, providers, inference, planning, Workflow, Skill,
Planner, Scheduler, execution logic, orchestration.

Ownership: this boundary owns **only the Agent abstraction**. Execution owns the
execution boundary · Runtime owns hosting · Knowledge owns semantics · Memory
owns promotion candidates · Governance owns authority · Trace owns history ·
Infrastructure owns facilities. No ownership transfer.

Public surface:
  - agent: Agent
"""

from .agent import Agent

__all__ = ["Agent"]
