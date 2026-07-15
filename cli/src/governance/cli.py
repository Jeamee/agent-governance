"""Command entry point reserved for the M1 governance verifier."""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(prog="governance")
    parser.add_argument("--version", action="version", version="agent-governance 0.0.1")
    parser.add_argument("command", nargs="?", default="help")
    args = parser.parse_args()

    if args.command == "help":
        parser.print_help()
        return 0

    parser.error("`governance verify` is intentionally reserved for M1")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
