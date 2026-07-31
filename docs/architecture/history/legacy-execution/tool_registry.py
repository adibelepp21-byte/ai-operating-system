"""
Tool Registry — Tier 1 Universal Tool Contract.

Per the Architect's Tier 1 directive, Registry is responsible ONLY for
adapter discovery and registration: given a Tool's Canonical Key, find
its adapter function and (once migrated) its cache-key deriver. It does
not execute anything — that is Tool Executor's job (tool_executor.py).

This stage introduces the Registry as a pure addition. Nothing in
tool.py or skill.py calls it yet; existing behavior is completely
unchanged. `legacy=True` marks a Tool whose adapter still uses the
pre-Tier-1 `**kwargs` signature and has no registered cache-key deriver
— true for all three real Tools at this stage.
"""

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class ToolRegistration:
    tool_key: str
    adapter: Callable
    cache_key_fn: Optional[Callable] = None
    legacy: bool = True


class ToolRegistry:
    def __init__(self):
        self._registrations = {}

    def register(self, tool_key, adapter, cache_key_fn=None, legacy=True):
        self._registrations[tool_key] = ToolRegistration(
            tool_key=tool_key, adapter=adapter, cache_key_fn=cache_key_fn, legacy=legacy,
        )

    def get(self, tool_key):
        return self._registrations.get(tool_key)

    def all(self):
        return dict(self._registrations)
