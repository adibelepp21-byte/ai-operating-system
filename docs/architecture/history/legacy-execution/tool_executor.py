"""
Tool Executor — Tier 1 Universal Tool Contract, extended in Tier 2 with
the Evidence Verification Layer.

Owns everything Tool Registry deliberately does not: request execution,
cache integration, response normalization, and — as of Tier 2 —
verifying a cache hit is still trustworthy before returning it.

`execute()` returns an `ExecutorResult` carrying both the adapter's
*exact, untouched* raw return value (`raw`) and a best-effort normalized
`response`. This split exists because the three real adapters' legacy
dict shapes are not uniform (`{"evidence": ...}`,
`{"elements": ...}`, `{"similarity": ...}`) — collapsing them through
`ToolResponse` and reconstructing would silently change the shape
existing Skill handlers already read. `raw` remains the source of truth
for backward compatibility; `response` is the forward-looking view.

Tier 2 verification flow, on a cache hit:
  1. Look up the cache entry for this request's derived key.
  2. Ask verification.verify(cached_fingerprint, request.parameters).
  3. If verified: return the cached evidence unchanged
     (`from_cache=True`, `verification_status="verified"`).
  4. If not verified: invalidate the entry, execute the Tool live,
     store the fresh evidence *and* a fresh fingerprint, return the new
     result (`from_cache=False`, `verification_status="invalidated"`).
Verification logic is isolated in verification.py; nothing here knows
which Tool it's checking, only whether the request's parameters
reference real files that may have changed.

Retry, timeout, and telemetry remain explicitly NOT implemented, per
the Tier 1 directive — unchanged this phase.
"""

from dataclasses import dataclass
from typing import Optional

from . import verification
from .tool_contract import ToolResponse


@dataclass(frozen=True)
class ExecutorResult:
    succeeded: bool
    raw: Optional[dict]
    response: Optional[ToolResponse]
    error: Optional[str] = None
    fingerprint: Optional[tuple] = None
    from_cache: bool = False
    # "not_applicable" (no cache/no cache_key_fn), "no_entry" (cache
    # miss), "verified" (cache hit, trusted), "invalidated" (cache hit,
    # rejected, live call ran instead)
    verification_status: str = "not_applicable"


class ToolExecutor:
    def __init__(self, registry, cache=None):
        self.registry = registry
        # Optional externally-supplied read-through cache (e.g. an
        # input-keyed dict from memory/consumption.py). None means "no
        # cache available" -- every call executes live. Executor
        # integrates a cache; it does not build or own one.
        self.cache = cache

    def execute(self, request):
        registration = self.registry.get(request.tool_canonical_key)
        if registration is None:
            return ExecutorResult(succeeded=False, raw=None, response=None, error="not_implemented")

        cache_key = None
        verification_status = "not_applicable"
        if self.cache is not None and registration.cache_key_fn is not None:
            cache_key = registration.cache_key_fn(request)
            cached = self.cache.get(cache_key)
            if cached is None:
                verification_status = "no_entry"
            elif verification.verify(cached.get("fingerprint"), request.parameters):
                return self._from_cache(cached, verification_status="verified")
            else:
                verification_status = "invalidated"
                del self.cache[cache_key]  # explicit invalidation step, not left to be silently overwritten

        self._apply_retry_policy(registration)   # extension point, no-op today
        self._apply_timeout(registration)         # extension point, no-op today

        try:
            raw = registration.adapter(**request.parameters)
        except Exception as exc:
            return ExecutorResult(succeeded=False, raw=None, response=None, error=f"{type(exc).__name__}: {exc}", verification_status=verification_status)

        response = self._normalize(raw)
        self._emit_telemetry(request, response)   # extension point, no-op today

        fingerprint = verification.compute_fingerprint(request.parameters)
        if self.cache is not None and cache_key is not None:
            self.cache[cache_key] = {
                "resolved": response.status,
                "detail": response.failure_reason if not response.status else "resolved",
                "fingerprint": fingerprint,
            }

        return ExecutorResult(
            succeeded=True, raw=raw if isinstance(raw, dict) else None, response=response, error=None,
            fingerprint=fingerprint, from_cache=False, verification_status=verification_status,
        )

    def _from_cache(self, cached, verification_status):
        resolved = cached.get("resolved")
        raw = {"resolved": resolved, "failure_reason": cached.get("detail") if not resolved else None}
        response = ToolResponse(status=resolved, payload={}, failure_reason=raw["failure_reason"])
        return ExecutorResult(
            succeeded=True, raw=raw, response=response, error=None,
            fingerprint=cached.get("fingerprint"), from_cache=True, verification_status=verification_status,
        )

    def _normalize(self, raw):
        """Migrated adapters already return a ToolResponse; legacy
        adapters still return a Tool-specific dict — normalized here so
        `response` is uniform regardless of which kind of adapter ran."""
        if isinstance(raw, ToolResponse):
            return raw
        if isinstance(raw, dict):
            return ToolResponse(
                status=raw.get("resolved", False),
                payload={k: v for k, v in raw.items() if k not in ("resolved", "failure_reason")},
                failure_reason=raw.get("failure_reason"),
            )
        raise TypeError(f"adapter returned unrecognized type: {type(raw).__name__}")

    # --- future extension points, deliberately unimplemented ---

    def _apply_retry_policy(self, registration):
        """No-op. Real retry semantics (attempt counts, backoff) are
        explicitly out of scope; this method exists so adding them
        later touches one place, not every call site."""
        return None

    def _apply_timeout(self, registration):
        """No-op. Same rationale as _apply_retry_policy."""
        return None

    def _emit_telemetry(self, request, response):
        """No-op. Same rationale as _apply_retry_policy."""
        return None
