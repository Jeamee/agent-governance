from __future__ import annotations

import json
from pathlib import Path
import runpy
import sys

import pytest

from governance.subchecks.coverage import branch_exact
from governance.subchecks.coverage import changed_source_files
from governance.subchecks.coverage import changed_sources_present
from governance.subchecks.coverage import main


def test_arc_m1_002_branch_exact_accepts_exact_modules(tmp_path: Path) -> None:
    report = tmp_path / "coverage.json"
    report.write_text(
        json.dumps(
            {
                "files": {
                    "cli/src/governance/verify/runner.py": {"summary": {"covered_branches": 2, "num_branches": 2}},
                    "cli/src/governance/subchecks/schema.py": {"summary": {"covered_branches": 3, "num_branches": 3}},
                }
            }
        ),
        encoding="utf-8",
    )
    assert branch_exact(
        report,
        ["cli/src/governance/verify/", "cli/src/governance/subchecks/"],
    )


def test_arc_m1_002_branch_exact_rejects_missing_or_partial_modules(tmp_path: Path) -> None:
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {}}), encoding="utf-8")
    assert not branch_exact(report, ["cli/src/governance/verify/"])


def test_dogfood_command_requires_all_requested_modules(tmp_path: Path) -> None:
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {}}), encoding="utf-8")
    modules = tmp_path / "modules.yaml"
    modules.write_text(
        "modules:\n  - module_id: MODULE-ONLY\n    prefix: cli/src/governance/verify/\n",
        encoding="utf-8",
    )
    assert main(["--report", str(report), "--modules", str(modules), "--branch-exact", "MISSING"]) == 1


def test_dogfood_command_accepts_exact_and_rejects_partial(tmp_path: Path) -> None:
    report = tmp_path / "coverage.json"
    modules = tmp_path / "modules.yaml"
    modules.write_text(
        "modules:\n  - module_id: MODULE-VERIFY\n    prefix: cli/src/governance/verify/\n",
        encoding="utf-8",
    )
    report.write_text(
        json.dumps(
            {"files": {"cli/src/governance/verify/runner.py": {"summary": {"covered_branches": 1, "num_branches": 1}}}}
        ),
        encoding="utf-8",
    )
    assert main(["--report", str(report), "--modules", str(modules), "--branch-exact", "MODULE-VERIFY"]) == 0
    report.write_text(
        json.dumps(
            {"files": {"cli/src/governance/verify/runner.py": {"summary": {"covered_branches": 0, "num_branches": 1}}}}
        ),
        encoding="utf-8",
    )
    assert main(["--report", str(report), "--modules", str(modules), "--branch-exact", "MODULE-VERIFY"]) == 1


def test_module_entrypoint_executes_main(tmp_path: Path, monkeypatch) -> None:
    report = tmp_path / "coverage.json"
    report.write_text(json.dumps({"files": {}}), encoding="utf-8")
    modules = tmp_path / "modules.yaml"
    modules.write_text("modules: []\n", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["coverage", "--report", str(report), "--modules", str(modules), "--branch-exact", "MISSING"],
    )
    with pytest.raises(SystemExit) as error:
        runpy.run_module("governance.subchecks.coverage", run_name="__main__")
    assert error.value.code == 1


def test_coverage_rejects_changed_source_absent_from_report(tmp_path: Path) -> None:
    report = tmp_path / "coverage.json"
    report.write_text(
        json.dumps({"files": {"cli/src/governance/cli.py": {"summary": {}}}}),
        encoding="utf-8",
    )
    assert changed_sources_present(report, ["cli/src/governance/cli.py"])
    assert not changed_sources_present(report, ["cli/src/governance/new_file.py"])


def test_changed_source_files_filters_git_output(monkeypatch) -> None:
    from governance.subchecks import coverage

    monkeypatch.setattr(
        coverage.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0, "stdout": "cli/src/governance/new.py\nREADME.md\ncli/tests/test.py\n"},
        )(),
    )
    assert changed_source_files("base") == ["cli/src/governance/new.py"]
    monkeypatch.setattr(
        coverage.subprocess,
        "run",
        lambda *args, **kwargs: type("Result", (), {"returncode": 1, "stdout": ""})(),
    )
    with pytest.raises(ValueError, match="unreachable"):
        changed_source_files("missing")


def test_changed_source_cli_paths_fail_closed(tmp_path: Path, monkeypatch) -> None:
    from governance.subchecks import coverage

    report = tmp_path / "coverage.json"
    report.write_text(
        json.dumps(
            {"files": {"cli/src/governance/verify/runner.py": {"summary": {"covered_branches": 1, "num_branches": 1}}}}
        ),
        encoding="utf-8",
    )
    modules = tmp_path / "modules.yaml"
    modules.write_text(
        "modules:\n  - module_id: MODULE-VERIFY\n    prefix: cli/src/governance/verify/\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit):
        main(["--report", str(report), "--modules", str(modules), "--branch-exact", "MODULE-VERIFY", "--changed-sources"])
    monkeypatch.setattr(coverage, "changed_source_files", lambda _: ["cli/src/governance/verify/runner.py"])
    assert main(["--report", str(report), "--modules", str(modules), "--branch-exact", "MODULE-VERIFY", "--changed-sources", "--base", "base"]) == 0
    monkeypatch.setattr(coverage, "changed_source_files", lambda _: ["cli/src/governance/missing.py"])
    assert main(["--report", str(report), "--modules", str(modules), "--branch-exact", "MODULE-VERIFY", "--changed-sources", "--base", "base"]) == 1
    monkeypatch.setattr(coverage, "changed_source_files", lambda _: (_ for _ in ()).throw(ValueError("bad base")))
    assert main(["--report", str(report), "--modules", str(modules), "--branch-exact", "MODULE-VERIFY", "--changed-sources", "--base", "base"]) == 1
    report.write_text(
        json.dumps(
            {"files": {"cli/src/governance/verify/runner.py": {"summary": {"covered_branches": 1, "num_branches": 2}}}}
        ),
        encoding="utf-8",
    )
    assert not branch_exact(report, ["cli/src/governance/verify/"])
