"""Plan checks require every changed file to have an explicit causal mapping."""

from __future__ import annotations

from typing import Any

from governance.subchecks.common import mapping
from governance.subchecks.common import result
from governance.verify.types import CheckResult
from governance.verify.types import Status


def check_plan(payload: dict[str, Any]) -> CheckResult:
    data = mapping(payload, "plan")
    if data.get("needs_review") is True:
        return CheckResult(
            name="plan",
            status=Status.NEEDS_REVIEW,
            sources=("plan",),
            reproduction="governance verify --mode ci --input plan --report-dir reports",
        )
    valid = (
        data.get("slots_match") is True
        and data.get("profiles_match") is True
        and data.get("missing_shards") == []
        and data.get("unmapped_paths") == []
        and data.get("derived_paths_valid") is True
    )
    return result("plan", valid, "plan", "ACC-PLAN-001")
