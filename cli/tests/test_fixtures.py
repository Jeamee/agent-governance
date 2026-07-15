from __future__ import annotations

import json
from pathlib import Path

import yaml

from governance.fixtures_runner import matrix_errors
from governance.fixtures_runner import run


ROOT = Path(__file__).resolve().parents[2]
ORACLE = ROOT / "docs/designs/governance-m1/fixture-oracle.yaml"
FIXTURES = ROOT / "fixtures/m1"


def test_acc_m1_oracle_001_matrix_and_results_pass() -> None:
    output = run(FIXTURES, ORACLE)
    assert output["status"] == "pass"
    assert len(output["results"]) == 32


def test_acc_m1_oracle_001_missing_cell_fails(tmp_path: Path) -> None:
    oracle = yaml.safe_load(ORACLE.read_text(encoding="utf-8"))
    oracle["fixtures"] = oracle["fixtures"][1:]
    assert matrix_errors(oracle) == ["missing oracle cell: schema/pass"]
    broken = tmp_path / "oracle.yaml"
    broken.write_text(yaml.safe_dump(oracle), encoding="utf-8")
    assert run(FIXTURES, broken)["status"] == "fail"


def test_fixture_runner_rejects_wrong_result(tmp_path: Path) -> None:
    results = json.loads((FIXTURES / "results.json").read_text(encoding="utf-8"))
    results["FIX-SCHEMA-PASS-001"] = "fail"
    (tmp_path / "results.json").write_text(json.dumps(results), encoding="utf-8")
    assert run(tmp_path, ORACLE)["status"] == "fail"
