"""
Orchestrator: the one place this harness assembles Agent Definition,
Runtime, Workflow, Skill, and Tool loading into a single executed path,
producing a Trace record for every action per Constitution §14.2's
unconditional-production rule and Domain Model invariant 4 ("Every
Agent Instance action produces exactly one Trace record").

Capability Hardening Phase changes: reads skill.py's new unified
`SkillOutput.evidence` (replacing the old separate flagged/tool_executions
fields) to build Trace outputs and to derive `tools_used`; records
`failure_class` when a Skill fails; times each Skill invocation and
passes `duration_ms` into every Trace record for that action.

This remains the entire execution engine for this phase. It does not
schedule, retry, allocate resources, or authenticate anything.
Authorization is checked for real: a Workflow or Skill not listed in the
Agent Definition's Permitted Workflows/Permitted Skills is refused and
recorded as an escalation Trace record, per Constitution §14.2.
"""

import time
from pathlib import Path

from . import agent_definition, agent_instance as agent_instance_mod, runtime as runtime_mod, skill, trace, workflow


class AuthorizationError(Exception):
    pass


def _evidence_to_dict(e):
    d = {"source": e.source, "kind": e.kind, "resolved": e.resolved, "detail": e.detail}
    # Cognitive Foundation Validation Phase: persist the real Tool call's
    # own request parameters for tool-sourced evidence. Previously only
    # the *output* (detail string) was written to Trace; the *input* that
    # produced it was discarded once the run ended. Without this, a
    # Memory consumption experiment has no way to know, from Trace files
    # alone, what a later Tool call would need to match against to be
    # served from Memory instead of invoked live.
    #
    # Tier 1 addition: also persist which Tool produced this evidence
    # (`tool_key`). Generic cache-key derivation (tool.py's
    # CACHE_KEY_FNS, Stage 6) needs to know which Tool's deriver to call
    # for a given evidence entry; parameters alone don't say which Tool
    # they belonged to.
    #
    # Tier 2 addition: also persist the fingerprint the Evidence
    # Verification Layer computed for this call (`e.raw` is a
    # ToolExecution, which now carries one — see tool.py/tool_executor.py).
    # Without this, a cache entry rebuilt from a historical Trace file
    # could never be verified against anything and would always fail
    # closed — which is the *correct* fallback for Trace records written
    # before this field existed, but real verification for new records
    # requires the fingerprint to actually survive to disk.
    #
    # Tier 3 addition: also persist `from_cache` and `verification_status`
    # (ToolExecution has carried both since Tier 2, but nothing wrote
    # them to Trace until now). Without this, cache-hit/miss and
    # verification telemetry could not be derived from Trace at all —
    # not because the data didn't exist, but because it was computed
    # in-process and discarded at run end, same class of gap Tier 1's
    # `parameters` field and Tier 2's `fingerprint` field each closed in
    # turn. In production runs (no cache attached to the default
    # executor) these will always read `from_cache=False,
    # verification_status="not_applicable"` — an honest, correct
    # recording of "no cache was consulted here today," not a
    # placeholder. Trace records written before this addition report
    # both as absent (None on read), not fabricated.
    if e.source == "tool" and e.raw is not None:
        d["parameters"] = dict(e.raw.request.parameters)
        d["tool_key"] = e.raw.request.tool_canonical_key
        d["fingerprint"] = e.raw.fingerprint
        d["from_cache"] = e.raw.from_cache
        d["verification_status"] = e.raw.verification_status
    return d


def run(target_document=None, workflow_key="workflow.pre-ratification-validation", runtime_selector=None):
    trace_writer = trace.TraceWriter()

    agent_def = agent_definition.load()
    rt = runtime_mod.bind_runtime(agent_def.name, selector=runtime_selector)
    instance = agent_instance_mod.spawn(agent_def, rt)
    trace_writer.write(trace.new_record(instance, rt, outputs={"event": "spawned"}))
    instance.activate()

    wf = workflow.load(workflow_key)
    wf_exec = workflow.WorkflowExecution(workflow_key=wf.canonical_key)

    if wf.path.resolve() not in agent_def.permitted_workflows:
        trace_writer.write(trace.new_record(
            instance, rt, workflow=wf.canonical_key,
            outputs={"event": "workflow_not_permitted"}, status="escalation",
        ))
        wf_exec.complete("escalated")
        instance.terminate()
        trace_writer.write(trace.new_record(
            instance, rt, workflow=wf.canonical_key,
            outputs={"event": "terminated", "workflow_completion_state": wf_exec.completion_state},
        ))
        raise AuthorizationError(f"{wf.canonical_key} is not listed in this Agent Definition's Permitted Workflows")

    target = Path(target_document).resolve() if target_document else agent_def.path

    skill_reports = []
    for skill_path in wf.skill_paths:
        key = skill.load_canonical_key(skill_path)

        if skill_path.resolve() not in agent_def.permitted_skills:
            trace_writer.write(trace.new_record(
                instance, rt, workflow=wf.canonical_key, skills_used=(key,),
                outputs={"event": "skill_not_permitted"}, status="escalation",
            ))
            wf_exec.record_skill(key, "escalation")
            skill_reports.append({"skill": key, "status": "escalation"})
            continue

        started = time.time()
        result = skill.invoke(skill_path, target)
        duration_ms = (time.time() - started) * 1000

        evidence = result.output.evidence if result.output else ()
        tools_used = tuple(e.raw.request.tool_canonical_key for e in evidence if e.source == "tool")
        trace_status = "success" if result.status == "success" else "failure"

        trace_writer.write(trace.new_record(
            instance, rt, workflow=wf.canonical_key, skills_used=(key,), tools_used=tools_used,
            inputs={"target_document": str(target)},
            outputs={
                "evidence": [_evidence_to_dict(e) for e in evidence],
                "failure_class": result.failure_class,
                "error": result.error,
            },
            status=trace_status,
            duration_ms=duration_ms,
        ))
        wf_exec.record_skill(key, result.status)
        skill_reports.append({
            "skill": key,
            "status": result.status,
            "failure_class": result.failure_class,
            "error": result.error,
            "evidence_count": len(evidence),
            "duration_ms": duration_ms,
        })

    if any(r["status"] == "escalation" for r in skill_reports):
        final_state = "escalated"
    elif any(r["status"] == "failure" for r in skill_reports):
        final_state = "failed"
    else:
        final_state = "completed"
    wf_exec.complete(final_state)

    instance.terminate()
    trace_writer.write(trace.new_record(
        instance, rt, workflow=wf.canonical_key,
        outputs={"event": "terminated", "workflow_completion_state": wf_exec.completion_state},
    ))

    return {
        "agent_instance_id": instance.instance_id,
        "agent_definition_version": agent_def.version,
        "runtime": rt.canonical_key,
        "workflow": wf.canonical_key,
        "workflow_completion_state": wf_exec.completion_state,
        "target_document": str(target),
        "skill_reports": skill_reports,
        "trace_file": str(trace_writer.path),
    }
