"""Shared fail-closed result helpers."""

from __future__ import annotations

from typing import Any

from governance.verify.types import CheckResult
from governance.verify.types import Status


def result(name: str, condition: bool, source: str, missing: str = "") -> CheckResult:
    return CheckResult(
        name=name,
        status=Status.PASS if condition else Status.FAIL,
        missing_ids=() if condition else (missing or name,),
        sources=(source,),
        reproduction=f"governance verify --mode ci --input {source} --report-dir reports",
    )


def mapping(payload: dict[str, Any], name: str) -> dict[str, Any]:
    value = payload.get(name)
    return value if isinstance(value, dict) else {}
