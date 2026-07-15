"""Schema-version authority and implementation-plan closure checks."""

from __future__ import annotations

from typing import Any

from governance.subchecks.common import mapping
from governance.subchecks.common import result


def check_schema(payload: dict[str, Any]):
    data = mapping(payload, "schema")
    authorization_version = data.get("authorization_version")
    worker_versions = data.get("worker_versions", [])
    closed = data.get("references_closed", False)
    valid = (
        authorization_version in {1, 2}
        and all(version == authorization_version for version in worker_versions)
        and closed
    )
    return result("schema", valid, "schema", "ACC-M1-SCHEMAVER-001")
