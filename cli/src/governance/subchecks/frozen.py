"""Digest and frozen-path checks use projections built from git objects."""

from __future__ import annotations

from typing import Any

from governance.subchecks.common import mapping
from governance.subchecks.common import result


def check_frozen(payload: dict[str, Any]):
    data = mapping(payload, "frozen")
    valid = (
        data.get("base_reachable") is True
        and data.get("design_digest_matches") is True
        and data.get("plan_digest_matches") is True
        and data.get("frozen_paths_changed") == []
        and data.get("oracle_manifest_matches") is True
    )
    return result("frozen", valid, "frozen", "ACC-FRZ-001")
