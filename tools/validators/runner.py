"""Orchestrates all six validators and produces a single structured
Report (see models.py)."""

from . import agent_integration, canonical_key, cross_reference, duplicate_key, integrity, orphan, relative_link
from .catalog import catalog_files
from .models import Report, ValidatorResult

VALIDATORS = [
    (canonical_key.NAME, canonical_key.run),
    (cross_reference.NAME, cross_reference.run),
    (relative_link.NAME, relative_link.run),
    (duplicate_key.NAME, duplicate_key.run),
    (orphan.NAME, orphan.run),
    (integrity.NAME, integrity.run),
    (agent_integration.NAME, agent_integration.run),
]


def run_all():
    results = [ValidatorResult(name, fn()) for name, fn in VALIDATORS]
    return Report(artifacts_scanned=len(catalog_files()), results=results)
