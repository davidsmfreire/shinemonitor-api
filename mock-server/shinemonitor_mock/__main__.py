"""CLI entrypoint: `python -m shinemonitor_mock --port 0`.

Binds to a free port if `--port 0`, then prints
`LISTENING http://<host>:<port>/` on a single line to stdout and
flushes. Test harnesses in any language can read that line to
discover the URL, then issue real HTTP requests.

Send SIGTERM / SIGINT to stop.
"""

from __future__ import annotations

import argparse
import socket
import sys

import uvicorn

from .server import create_app


def _pick_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> None:
    parser = argparse.ArgumentParser(prog="shinemonitor_mock")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="0 (default) picks a free port; nonzero binds explicitly.",
    )
    args = parser.parse_args()

    port = args.port or _pick_port()
    sys.stdout.write(f"LISTENING http://{args.host}:{port}/\n")
    sys.stdout.flush()
    uvicorn.run(
        create_app(),
        host=args.host,
        port=port,
        log_level="warning",
        access_log=False,
    )


if __name__ == "__main__":
    main()
