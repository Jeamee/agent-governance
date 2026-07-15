"""Authorization and revocation checks consume protected-record projections."""

from __future__ import annotations

from typing import Any

from governance.subchecks.common import mapping
from governance.subchecks.common import result


def check_authorization(payload: dict[str, Any]):
    data = mapping(payload, "authorization")
    valid = (
        data.get("delivery_matches") is True
        and data.get("on_protected_main") is True
        and data.get("revoked") is False
        and data.get("conflicting_revocations") is False
        and data.get("same_pr_revocation") is False
        and data.get("replacement_auto_selected") is False
    )
    return result("authorization", valid, "authorization", "ACC-AUTH-001")
