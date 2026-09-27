"""Vercel's Python function entrypoint for the AIOS Full Stack API.

A shim: `vercel.json` rewrites `/api/v1/*` here, and the WSGI callable `app`
is `fullstack.deploy.vercel.app` (per-request Runtime; FS-DP-04 A1).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# GOAL-V2-004: install the certified-write barrier before anything can write.
import tools  # noqa: E402,F401

from fullstack.deploy.vercel import app  # noqa: E402,F401
