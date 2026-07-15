"""Aggregate all eight checks without allowing an early check to hide another."""

from __future__ import annotations

from collections.abc import Callable
import json
from pathlib import Path
from typing import Any

from governance.subchecks.acceptance import check_acceptance
from governance.subchecks.authorization import check_authorization
from governance.subchecks.coverage import check_coverage
from governance.subchecks.effectiveness import check_effectiveness
from governance.subchecks.frozen import check_frozen
from governance.subchecks.plan import check_plan
from governance.subchecks.policy import check_policy
from governance.subchecks.schema import check_schema
from governance.verify.types import CheckResult
from governance.verify.types import Status


CHECKS: tuple[Callable[[dict[str, Any]], CheckResult], ...] = (
    check_schema,
    check_authorization,
    check_frozen,
    check_acceptance,
    check_plan,
    check_coverage,
    check_effectiveness,
    check_policy,
)


def final_status(mode: str, results: list[CheckResult]) -> Status:
    statuses = {result.status for result in results}
    if Status.FAIL in statuses:
        return Status.FAIL
    if mode == "ci" and Status.UNVERIFIABLE in statuses:
        return Status.FAIL
    if Status.NEEDS_REVIEW in statuses:
        return Status.NEEDS_REVIEW
    if Status.UNVERIFIABLE in statuses:
        return Status.UNVERIFIABLE
    return Status.PASS


def exit_code(status: Status) -> int:
    if status is Status.PASS:
        return 0
    if status is Status.UNVERIFIABLE:
        return 3
    return 1


def verify(mode: str, payload: dict[str, Any], report_dir: Path) -> dict[str, object]:
    report_dir.mkdir(parents=True, exist_ok=True)
    results = [check(payload) for check in CHECKS]
    status = final_status(mode, results)
    output = {
        "schema_version": 2,
        "mode": mode,
        "status": status.value,
        "exit_code": exit_code(status),
        "subchecks": [result.output() for result in results],
    }
    (report_dir / "verify-output.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return output
