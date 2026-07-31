"""
Memory consumption experiment.

Tests whether supplying previously-extracted Memory observations to a
new execution measurably changes anything real — not a Memory
Framework, not a permanent change to the production execution path.

Run A: normal execution, exactly as orchestrator.run() already does.
Every Skill's Tool invocation is a real, live call.

Run B: an input-keyed cache is built from real prior Trace records
(keyed generically, per Tool — see below — not by output, since a
decision about whether to skip a live call can only be made from the
input available *before* that call runs). tool.invoke is monkeypatched
for the duration of Run B only, so Run A's code path — and the
production harness generally — is completely unaffected outside this
experiment. A cache hit returns the remembered evidence without a live
call; a cache miss falls through to a real one, identical to Run A.

This monkeypatch-based substitution is deliberate and disclosed: wiring
Memory into skill.py's production path permanently was not asked for
and is not done here. This experiment proves whether doing so would be
worthwhile, without doing it.

Tier 1 (Stage 6) change: cache-key derivation is no longer hardcoded to
one Tool's parameter names (`reference_target`/`expected_reference`).
Both `build_input_keyed_cache()` and the memory-aware invoke wrapper now
look up each Tool's own registered `cache_key_fn` (tool.py's
CACHE_KEY_FNS, introduced Tier 1 Stages 3-5) via the tool_key persisted
in each evidence entry (orchestrator.py's `_evidence_to_dict`, extended
this stage). This directly closed the gap the Memory Expansion
Validation Phase measured: a cache with 4 entries, all from one Tool,
and 0-of-1 real-call reduction for a Skill using a different Tool.

Tier 2 change: the memory-aware invoke wrapper no longer hand-rolls its
own cache check. It now constructs a real `tool_executor.ToolExecutor`
with `cache` attached and calls its `execute()` — the exact same
Evidence Verification Layer the (still cache-free-by-default) production
`tool.invoke()` path uses. This means verification logic exists in
exactly one place (tool_executor.py / verification.py), not duplicated
here — a cache hit this experiment serves is now verified, not trusted
unconditionally, and a verification failure transparently falls through
to a real call and updates the cache, exactly like production would if
a cache were ever attached there.
"""

import time
from dataclasses import dataclass
from unittest import mock

from . import extractor as extractor_mod
from .. import tool as tool_mod
from ..tool_executor import ToolExecutor


@dataclass(frozen=True)
class ToolCallRecord:
    real_call: bool  # True = live Tool invocation; False = served from memory cache
    parameters: dict
    resolved: object
    detail: str


def _derive_key(tool_key, parameters):
    """The one place this experiment converts (tool_key, parameters)
    into a cache key, for both cache-building and cache-lookup, so the
    two can never drift apart. Returns None if the Tool has no
    registered cache_key_fn (nothing to key on) or isn't registered at
    all."""
    registration = tool_mod._registry().get(tool_key)
    if registration is None or registration.cache_key_fn is None:
        return None
    request = tool_mod.ToolRequest(tool_canonical_key=tool_key, action="", parameters=parameters)
    return registration.cache_key_fn(request)


def build_input_keyed_cache(trace_records):
    """Maps a generic, per-Tool cache key -> remembered evidence
    (including the fingerprint recorded at write time), from real prior
    Tool call parameters and their outcomes. Only entries whose
    parameters were actually persisted *and* whose Tool has a
    registered cache_key_fn can populate this cache — either gap is
    reported as an absent entry, not silently guessed at.

    Tier 2: `fingerprint` is read from the evidence entry when present
    (records written after this phase); absent for older records,
    which is correct, not a bug — an entry with no recorded fingerprint
    cannot be proven fresh and will fail verification closed (see
    verification.py), forcing a live re-check exactly as it should for
    data nothing ever confirmed the freshness of."""
    cache = {}
    for record in trace_records:
        for ev in (record.get("outputs") or {}).get("evidence") or []:
            if ev.get("source") != "tool":
                continue
            tool_key = ev.get("tool_key")
            if tool_key is None:
                continue
            params = ev.get("parameters") or {}
            key = _derive_key(tool_key, params)
            if key is None:
                continue
            fingerprint = ev.get("fingerprint")
            cache[key] = {
                "resolved": ev.get("resolved"),
                "detail": ev.get("detail"),
                "fingerprint": tuple(fingerprint) if isinstance(fingerprint, list) else fingerprint,
            }
    return cache


def _make_memory_aware_invoke(cache, call_log):
    """Tier 2: delegates to a real ToolExecutor with `cache` attached,
    instead of hand-checking the cache here. This is the exact same
    Evidence Verification Layer path production tool.invoke() would use
    if a cache were ever attached to the default executor — a cache hit
    here is verified, not trusted unconditionally."""
    executor = ToolExecutor(tool_mod._registry(), cache=cache)

    def memory_aware_invoke(tool_path, action, **parameters):
        tool_key = tool_mod.load_canonical_key(tool_path)
        request = tool_mod.ToolRequest(tool_canonical_key=tool_key, action=action, parameters=parameters)
        result = executor.execute(request)
        ev = result.raw or {}
        call_log.append(ToolCallRecord(
            real_call=not result.from_cache, parameters=parameters,
            resolved=ev.get("resolved"), detail=ev.get("failure_reason") or "resolved",
        ))
        return tool_mod.ToolExecution(
            request=request, succeeded=result.succeeded, evidence=result.raw, error=result.error,
            fingerprint=result.fingerprint, from_cache=result.from_cache, verification_status=result.verification_status,
        )

    return memory_aware_invoke


def run_comparison(orchestrator_module, cache, **run_kwargs):
    """Runs Run A (unpatched) then Run B (patched with the memory-aware
    invoke built from `cache`) and returns both raw results plus the
    per-call logs needed to measure the difference."""
    call_log_a = []
    real_invoke = tool_mod.invoke

    def counting_invoke(tool_path, action, **parameters):
        execution = real_invoke(tool_path, action, **parameters)
        ev = execution.evidence or {}
        call_log_a.append(ToolCallRecord(real_call=True, parameters=parameters, resolved=ev.get("resolved"), detail=ev.get("failure_reason") or "resolved"))
        return execution

    started_a = time.time()
    with mock.patch.object(tool_mod, "invoke", counting_invoke):
        result_a = orchestrator_module.run(**run_kwargs)
    duration_a = (time.time() - started_a) * 1000

    call_log_b = []
    memory_aware_invoke = _make_memory_aware_invoke(cache, call_log_b)
    started_b = time.time()
    with mock.patch.object(tool_mod, "invoke", memory_aware_invoke):
        result_b = orchestrator_module.run(**run_kwargs)
    duration_b = (time.time() - started_b) * 1000

    return {
        "run_a": {"result": result_a, "call_log": call_log_a, "duration_ms": duration_a},
        "run_b": {"result": result_b, "call_log": call_log_b, "duration_ms": duration_b},
    }
