"""Execute the frozen fixture oracle without allowing matrix shrinkage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


SUBCHECKS = {
    "schema",
    "authorization",
    "frozen",
    "acceptance",
    "plan",
    "coverage",
    "effectiveness",
    "policy",
}
CLASSES = {"pass", "reject", "boundary", "bypass"}


def matrix_errors(oracle: dict[str, Any]) -> list[str]:
    fixtures = oracle.get("fixtures", [])
    seen = {(item.get("subcheck"), item.get("class")) for item in fixtures}
    expected = {(subcheck, fixture_class) for subcheck in SUBCHECKS for fixture_class in CLASSES}
    errors = [f"missing oracle cell: {subcheck}/{fixture_class}" for subcheck, fixture_class in sorted(expected - seen)]
    identifiers = [item.get("id") for item in fixtures]
    if len(identifiers) != len(set(identifiers)):
        errors.append("fixture oracle contains duplicate ids")
    return errors


def run(fixtures_root: Path, oracle_path: Path) -> dict[str, Any]:
    oracle = yaml.safe_load(oracle_path.read_text(encoding="utf-8"))
    errors = matrix_errors(oracle)
    try:
        fixture_results = json.loads((fixtures_root / "results.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        fixture_results = {}
    results: list[dict[str, str]] = []
    for fixture in oracle.get("fixtures", []):
        actual = fixture_results.get(fixture["id"], "missing")
        expected = fixture["expected_status"]
        if actual != expected:
            errors.append(f"{fixture['id']}: expected {expected}, got {actual}")
        if actual in fixture["forbidden_misclassification"]:
            errors.append(f"{fixture['id']}: forbidden classification {actual}")
        results.append({"id": fixture["id"], "status": actual})
    return {"status": "pass" if not errors else "fail", "errors": errors, "results": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixtures_root", type=Path)
    parser.add_argument("--oracle", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args(argv)
    output = run(args.fixtures_root, args.oracle)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0 if output["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
