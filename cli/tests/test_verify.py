from __future__ import annotations

import json
from pathlib import Path

import pytest

from governance.cli import main
from governance.verify.runner import verify
from governance.verify.types import Status


def valid_payload() -> dict[str, object]:
    return {
        "schema": {
            "authorization_version": 2,
            "worker_versions": [2, 2],
            "references_closed": True,
        },
        "authorization": {
            "delivery_matches": True,
            "on_protected_main": True,
            "revoked": False,
            "conflicting_revocations": False,
            "same_pr_revocation": False,
            "replacement_auto_selected": False,
        },
        "frozen": {
            "base_reachable": True,
            "design_digest_matches": True,
            "plan_digest_matches": True,
            "frozen_paths_changed": [],
            "oracle_manifest_matches": True,
        },
        "acceptance": {
            "fresh_reports": True,
            "required_ids_missing": [],
            "missing_shards": [],
            "instances_complete": True,
            "attempts_preserved": True,
        },
        "plan": {
            "slots_match": True,
            "profiles_match": True,
            "missing_shards": [],
            "unmapped_paths": [],
            "derived_paths_valid": True,
        },
        "coverage": {
            "report_present": True,
            "patch_percent": 90,
            "decision_branches_exact": True,
            "independent_matches_dogfood": True,
        },
        "effectiveness": {"task_type": "feature"},
        "policy": {
            "protected_paths_changed": [],
            "valid_exception": False,
            "warning_fixtures_complete": True,
        },
    }


def test_acc_cli_001_writes_v2_output(tmp_path: Path) -> None:
    output = verify("ci", valid_payload(), tmp_path)
    assert output["status"] == "pass"
    assert output["exit_code"] == 0
    assert len(output["subchecks"]) == 8
    assert json.loads((tmp_path / "verify-output.json").read_text()) == output


@pytest.mark.parametrize(
    ("section", "key"),
    [
        ("schema", "references_closed"),
        ("authorization", "delivery_matches"),
        ("frozen", "base_reachable"),
        ("acceptance", "fresh_reports"),
        ("plan", "slots_match"),
        ("coverage", "report_present"),
        ("policy", "warning_fixtures_complete"),
    ],
)
def test_acceptance_failures_are_not_hidden(
    tmp_path: Path,
    section: str,
    key: str,
) -> None:
    payload = valid_payload()
    payload[section][key] = False
    output = verify("ci", payload, tmp_path)
    assert output["status"] == "fail"
    assert any(item["status"] == "fail" for item in output["subchecks"])


def test_acc_eff_001_requires_bugfix_red_green(tmp_path: Path) -> None:
    payload = valid_payload()
    payload["effectiveness"] = {"task_type": "bugfix", "base_failed": False, "head_passed": True}
    assert verify("ci", payload, tmp_path)["status"] == "fail"
    payload["effectiveness"] = {"task_type": "bugfix", "base_failed": True, "head_passed": True}
    assert verify("ci", payload, tmp_path)["status"] == "pass"


def test_acc_ipl_008_needs_review_is_not_pass(tmp_path: Path) -> None:
    payload = valid_payload()
    payload["plan"]["needs_review"] = True
    output = verify("ci", payload, tmp_path)
    assert output["status"] == Status.NEEDS_REVIEW.value


def test_local_unverifiable_is_ci_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from governance.verify import runner
    from governance.verify.types import CheckResult

    monkeypatch.setattr(
        runner,
        "CHECKS",
        (lambda _: CheckResult(name="schema", status=Status.UNVERIFIABLE),),
    )
    assert verify("local", {}, tmp_path)["exit_code"] == 3
    assert verify("ci", {}, tmp_path / "ci")["exit_code"] == 1


@pytest.mark.dualmode
def test_acc_cli_001_deterministic_checks_match_across_modes(tmp_path: Path) -> None:
    local = verify("local", valid_payload(), tmp_path / "local")
    ci = verify("ci", valid_payload(), tmp_path / "ci")
    assert [item["status"] for item in local["subchecks"]] == [
        item["status"] for item in ci["subchecks"]
    ]


def test_cli_rejects_nonempty_report_dir(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(valid_payload()), encoding="utf-8")
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    (report_dir / "old.txt").write_text("old", encoding="utf-8")
    with pytest.raises(SystemExit) as error:
        main(["verify", "--mode", "ci", "--input", str(input_path), "--report-dir", str(report_dir)])
    assert error.value.code == 2


def test_cli_executes_run_bound_verification(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(valid_payload()), encoding="utf-8")
    report_dir = tmp_path / "reports"
    assert main(["verify", "--mode", "ci", "--input", str(input_path), "--report-dir", str(report_dir)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "pass"
    assert (report_dir / "verify-output.json").exists()


@pytest.mark.parametrize("argv", [[], ["verify", "--mode", "ci", "--input", "missing.json", "--report-dir", "reports"]])
def test_cli_rejects_missing_command_or_invalid_input(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(argv)
    assert error.value.code == 2
