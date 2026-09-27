"""Serve the AIOS Full Stack locally.

    python -m fullstack.backend serve --data-dir <dir> [--host 127.0.0.1] [--port 8765]

With no command it prints this usage and exits, so tooling that runs every
entry point (`tools/certified_write_probe.py`) starts no server.

    python -m fullstack.backend operator-token --subject <name> [--scope <scope> ...]

The server binds loopback unless `--host` says otherwise: networking is
Architect-reserved (`FS-DP-03`). Authentication is `FS-DP-02` B3, operator
bearer tokens (Register `§81`), configured by `AIOS_OPERATOR_TOKENS` in the
environment; without it every protected route answers 401.

`operator-token` is for the operator, on their own machine: it prints a new
random token once, for the console, and the configuration entry holding only
its hash, for the host. Nothing is written to disk.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
from pathlib import Path
from wsgiref.simple_server import make_server

from .api import create_app
from .security import OBSERVE, SCOPES, OperatorTokenAuthenticator, token_sha256

REPO_ROOT = Path(__file__).resolve().parents[2]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m fullstack.backend")
    commands = parser.add_subparsers(dest="command")
    serve = commands.add_parser("serve", help="serve the API and the console")
    serve.add_argument("--data-dir", required=True, type=Path,
                       help="where the append-only store lives; created if absent")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", default=8765, type=int)
    issue = commands.add_parser("operator-token",
                                help="make a new operator token and its hash entry")
    issue.add_argument("--subject", required=True)
    issue.add_argument("--scope", action="append", choices=SCOPES,
                       help=f"repeat for each scope; default {OBSERVE} only")
    args = parser.parse_args(argv)
    if args.command == "operator-token":
        token = secrets.token_urlsafe(32)
        entry = {"subject": args.subject, "sha256": token_sha256(token),
                 "scopes": sorted(set(args.scope or [OBSERVE]))}
        print("token (give it to the console; it is not stored anywhere):")
        print(token)
        print("entry (add it to the JSON array in AIOS_OPERATOR_TOKENS):")
        print(json.dumps(entry))
        return 0
    if args.command != "serve":
        parser.print_help()
        return 0
    authenticator = OperatorTokenAuthenticator.from_environment(os.environ)
    app, aios = create_app(args.data_dir, REPO_ROOT, authenticator)
    with make_server(args.host, args.port, app) as server:
        print(f"AIOS Full Stack on http://{args.host}:{args.port}/ "
              f"(runtime {aios.runtime_id}; authentication: {authenticator.mechanism}"
              f", {authenticator.configuration_error or 'configured'})",
              file=sys.stderr)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            aios.stop()
    return 0


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before the server can
    # write, so a data directory inside certified evidence is refused.
    import tools  # noqa: F401
    raise SystemExit(main())
