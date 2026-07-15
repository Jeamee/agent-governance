"""Protected-path and warning-classifier policy checks."""

from __future__ import annotations

from typing import Any

from governance.subchecks.common import mapping
from governance.subchecks.common import result


def check_policy(payload: dict[str, Any]):
    data = mapping(payload, "policy")
    valid = (
        data.get("protected_paths_changed") == []
        or data.get("valid_exception") is True
    ) and data.get("warning_fixtures_complete") is True
    return result("policy", valid, "policy", "ACC-POL-001")


def intentional_uncovered_canary() -> str:
    return "this branch must fail patch coverage"
