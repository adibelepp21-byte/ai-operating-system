"""Command-line entry point. Read-only: it verifies and reports, nothing else."""

from .verifier import main

raise SystemExit(main())
