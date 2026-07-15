"""Coverage subcheck keeps patch and branch-exact evidence separate."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

from governance.subchecks.common import mapping
from governance.subchecks.common import result


def branch_exact(report: Path, module_prefixes: list[str]) -> bool:
    import json

    coverage = json.loads(report.read_text(encoding="utf-8"))
    files = coverage.get("files", {})
    for prefix in module_prefixes:
        summaries = [
            data.get("summary", {})
            for path, data in files.items()
            if path.replace("\\", "/").startswith(prefix)
            or path.replace("\\", "/").endswith(prefix)
            or f"/{prefix}" in path.replace("\\", "/")
        ]
        if not summaries:
            return False
        if sum(item.get("covered_branches", 0) for item in summaries) != sum(
            item.get("num_branches", 0) for item in summaries
        ):
            return False
    return True


def check_coverage(payload: dict[str, Any]):
    data = mapping(payload, "coverage")
    valid = (
        data.get("report_present") is True
        and data.get("patch_percent", 0) >= 90
        and data.get("decision_branches_exact") is True
        and data.get("independent_matches_dogfood") is True
    )
    return result("coverage", valid, "coverage", "ACC-COV-001")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--modules", required=True, type=Path)
    parser.add_argument("--branch-exact", nargs="+", required=True)
    args = parser.parse_args(argv)
    modules = yaml.safe_load(args.modules.read_text(encoding="utf-8"))["modules"]
    prefixes = [
        module["prefix"]
        for module in modules
        if module["module_id"] in set(args.branch_exact)
    ]
    if len(prefixes) != len(set(args.branch_exact)):
        print("branch exact: FAIL")
        print("requested module is absent from modules.yaml")
        return 1
    if not branch_exact(args.report, prefixes):
        print("branch exact: FAIL")
        return 1
    print("branch exact: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
