"""Serve the AIOS Full Stack locally.

    python -m fullstack.backend serve --data-dir <dir> [--host 127.0.0.1] [--port 8765]

With no command it prints this usage and exits, so tooling that runs every
entry point (`tools/certified_write_probe.py`) starts no server.

The server binds loopback unless `--host` says otherwise: networking is
Architect-reserved (`FS-DP-03`). Authentication is the shipped
`NoAuthenticator` (`FS-DP-02` not ratified), so every protected route answers
401. That is the correct production posture until the decision exists.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from wsgiref.simple_server import make_server

from .api import create_app
from .security import NoAuthenticator

REPO_ROOT = Path(__file__).resolve().parents[2]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m fullstack.backend")
    commands = parser.add_subparsers(dest="command")
    serve = commands.add_parser("serve", help="serve the API and the console")
    serve.add_argument("--data-dir", required=True, type=Path,
                       help="where the append-only store lives; created if absent")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", default=8765, type=int)
    args = parser.parse_args(argv)
    if args.command != "serve":
        parser.print_help()
        return 0
    app, aios = create_app(args.data_dir, REPO_ROOT, NoAuthenticator())
    with make_server(args.host, args.port, app) as server:
        print(f"AIOS Full Stack on http://{args.host}:{args.port}/ "
              f"(runtime {aios.runtime_id}; authentication: none, FS-DP-02 not ratified)",
              file=sys.stderr)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            aios.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
