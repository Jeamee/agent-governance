"""Command line interface for the deterministic governance verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from governance.verify.runner import verify


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="governance")
    parser.add_argument("--version", action="version", version="agent-governance 0.1.0")
    subparsers = parser.add_subparsers(dest="command")
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--mode", choices=("local", "ci"), required=True)
    verify_parser.add_argument("--input", type=Path, required=True)
    verify_parser.add_argument("--report-dir", type=Path, required=True)
    verify_parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.command != "verify":
        parser.error("a command is required")
    if args.report_dir.exists() and any(args.report_dir.iterdir()):
        parser.error("--report-dir must be empty when verification starts")
    args.report_dir.mkdir(parents=True, exist_ok=True)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        parser.error(f"invalid --input: {error}")
    output = verify(mode=args.mode, payload=payload, report_dir=args.report_dir)
    rendered = json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True)
    print(rendered)
    return int(output["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
