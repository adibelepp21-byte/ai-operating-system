"""AIOS tools.

Importing this package installs the certified-write barrier
(`tools/certified_write_barrier.py`, `GOAL-V2-004`). Every resident entry point
imports it before it can write, so no entry point can modify certified evidence
without being refused first.
"""

from tools import certified_write_barrier as _certified_write_barrier

_certified_write_barrier.install()
