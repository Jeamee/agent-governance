"""Report completeness checks retain retries and reject stale report slots."""

from __future__ import annotations

from typing import Any

from governance.subchecks.common import mapping
from governance.subchecks.common import result


def check_acceptance(payload: dict[str, Any]):
    data = mapping(payload, "acceptance")
    valid = (
        data.get("fresh_reports") is True
        and data.get("required_ids_missing") == []
        and data.get("missing_shards") == []
        and data.get("instances_complete") is True
        and data.get("attempts_preserved") is True
    )
    return result("acceptance", valid, "acceptance", "ACC-ACC-001")
