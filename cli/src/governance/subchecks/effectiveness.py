"""Task-type-specific proof of test effectiveness."""

from __future__ import annotations

from typing import Any

from governance.subchecks.common import mapping
from governance.subchecks.common import result


def check_effectiveness(payload: dict[str, Any]):
    data = mapping(payload, "effectiveness")
    task_type = data.get("task_type")
    valid = (
        task_type in {"feature", "refactor"}
        or (task_type == "bugfix" and data.get("base_failed") is True and data.get("head_passed") is True)
    )
    return result("effectiveness", valid, "effectiveness", "ACC-EFF-001")
