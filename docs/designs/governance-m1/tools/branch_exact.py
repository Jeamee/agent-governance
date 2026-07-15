"""Independent branch-exact coverage proof for frozen M1 design sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


def module_files(modules_path: Path, module_ids: set[str]) -> set[str]:
    modules = yaml.safe_load(modules_path.read_text(encoding="utf-8"))["modules"]
    prefixes = {
        module["prefix"]
        for module in modules
        if module["module_id"] in module_ids
    }
    if len(prefixes) != len(module_ids):
        raise ValueError("requested module is absent from modules.yaml")
    return prefixes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage-json", type=Path, required=True)
    parser.add_argument("--modules", type=Path, required=True)
    parser.add_argument("module_ids", nargs="+", help="DECISION module IDs")
    args = parser.parse_args()

    prefixes = module_files(args.modules, set(args.module_ids))
    coverage = json.loads(args.coverage_json.read_text(encoding="utf-8"))
    files = coverage.get("files", {})
    failures: list[str] = []
    for prefix in sorted(prefixes):
        matching = [data for path, data in files.items() if path.replace("\\", "/").startswith(prefix)]
        if not matching:
            failures.append(f"{prefix}: no coverage file")
            continue
        branches = [data.get("summary", {}) for data in matching]
        covered = sum(item.get("covered_branches", 0) for item in branches)
        total = sum(item.get("num_branches", 0) for item in branches)
        if total == 0 or covered != total:
            failures.append(f"{prefix}: covered_branches={covered}, num_branches={total}")
    if failures:
        print("branch exact: FAIL")
        print("\n".join(failures))
        return 1
    print("branch exact: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
