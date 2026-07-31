"""
Trace schema version handling — an experiment, not a Framework.

Tests whether the disposable JSON-Lines Trace format from trace.py can
tolerate real schema evolution: old records read by new code, and new
fields introduced without breaking existing consumers. This does not
ratify a storage convention or a versioning rule; it exists to generate
evidence about whether schema evolution is survivable in this format at
all, informing — not deciding — whether a future Trace Framework would
ever need one.

Three real, on-disk `outputs` shapes have now been observed across this
harness's phases (confirmed directly against every file under
execution/traces/, not assumed):

  1. **Unversioned, pre-tool-execution-contract**: no `schema_version`
     key; per-tool-execution evidence keyed `{"resolves", "match_type",
     "detail"}`; action outputs shaped `{"flagged", "tool_executions",
     "error"}` (Execution Foundation Stabilization Phase, Real
     Capability Integration Phase).
  2. **1.1**: `schema_version` present; adds `duration_ms`; action
     outputs shaped `{"evidence", "failure_class", "error"}`, where each
     evidence entry already carries the unified `{"source", "kind",
     "resolved", "detail"}` shape (Capability Hardening Phase).
  3. Event-only outputs (`{"event": ...}`, optionally with
     `workflow_completion_state`) — spawn/terminate/escalation records,
     present in every generation, nothing to normalize.

normalize_record() upgrades any of these into one common shape: every
record's `outputs`, if it represents an action, ends up carrying an
`evidence` list in the current per-entry shape — regardless of which
generation wrote it. Consumers (memory/history.py, memory/extractor.py)
rely on this rather than each re-deriving it independently.
"""

CURRENT_SCHEMA_VERSION = "1.1"


def _normalize_tool_execution(te: dict) -> dict:
    evidence = te.get("evidence")
    if isinstance(evidence, dict) and "resolves" in evidence and "resolved" not in evidence:
        old = evidence
        evidence = {
            "resolved": old.get("resolves"),
            "evidence": {"match_type": old.get("match_type")} if old.get("match_type") else None,
            "failure_reason": old.get("detail") if not old.get("resolves") else None,
        }
        te = dict(te)
        te["evidence"] = evidence
    return te


def _normalize_tool_parameters(params: dict) -> dict:
    """Two real, on-disk parameter-key generations exist for the
    cross-reference-check Tool, confirmed directly against trace files:
    an Execution Foundation Stabilization Phase shape
    (citing_document/cited_document/cited_section) and the current shape
    (citing_document/repository_path/reference_target/expected_reference,
    unchanged since Real Capability Integration Phase). Maps the older
    shape onto the current one so a cache keyed on current names works
    uniformly across generations. `repository_path` is None for the
    older shape — it wasn't recorded separately, since cited_document
    was already an absolute path."""
    if not params:
        return params
    if "reference_target" in params:
        return params
    if "cited_document" in params:
        return {
            "citing_document": params.get("citing_document"),
            "repository_path": None,
            "reference_target": params.get("cited_document"),
            "expected_reference": params.get("cited_section"),
        }
    return params


def _normalize_outputs(outputs):
    """Ensures `outputs["evidence"]` exists, in the current per-entry
    shape, for any action-shaped outputs dict, regardless of which of
    the three observed generations produced it. Leaves event-only
    outputs (spawn/terminate/escalation) untouched — they have no
    evidence to normalize, honestly, not by omission."""
    if not outputs:
        return outputs
    if "evidence" in outputs:
        return outputs  # already current shape

    if "flagged" not in outputs and "tool_executions" not in outputs:
        return outputs  # event-only outputs; nothing to normalize

    evidence = []
    for flag in outputs.get("flagged") or []:
        # The pre-1.1 "flagged" list carried no origin tag distinguishing
        # which heuristic produced it, so this cannot be honestly
        # upgraded to a specific kind like "authority_claim_flag" —
        # labeled generically rather than guessed.
        evidence.append({"source": "heuristic", "kind": "legacy_flag", "resolved": None, "detail": flag})
    for te in outputs.get("tool_executions") or []:
        te = _normalize_tool_execution(te)
        ev = te.get("evidence") or {}
        detail = te.get("error") or ev.get("failure_reason") or "resolved"
        evidence.append({
            "source": "tool", "kind": "cross_reference_check",
            # Every generation using this "tool_executions" outputs shape
            # (Execution Foundation Stabilization Phase through Real
            # Capability Integration Phase) predates the second and third
            # Tools entirely -- cross-reference-link-validator-interface
            # is the only Tool that could have produced this evidence,
            # so this is a fact, not a guess.
            "tool_key": "tool.cross-reference-link-validator-interface",
            "resolved": ev.get("resolved"), "detail": detail,
            "parameters": _normalize_tool_parameters(te.get("parameters") or {}),
        })

    normalized = dict(outputs)
    normalized["evidence"] = evidence
    return normalized


def normalize_record(raw: dict) -> dict:
    """Given a raw dict loaded from any trace .jsonl line, regardless of
    which generation wrote it, returns a normalized dict guaranteed to
    carry every current-shape key, with reasonable defaults for
    anything an older record didn't have. Never mutates `raw`."""
    normalized = dict(raw)
    normalized.setdefault("schema_version", "1.0")  # unversioned records predate this field entirely
    normalized.setdefault("workflow", None)
    normalized.setdefault("inputs", None)
    normalized.setdefault("duration_ms", None)
    normalized.setdefault("agent_definition_name", "unknown")
    normalized["outputs"] = _normalize_outputs(normalized.get("outputs"))
    return normalized


def is_current(raw: dict) -> bool:
    return raw.get("schema_version") == CURRENT_SCHEMA_VERSION
