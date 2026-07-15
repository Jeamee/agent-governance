"""Small immutable model shared by deterministic subchecks."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Status(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    UNVERIFIABLE = "unverifiable"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: Status
    missing_ids: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    reproduction: str = "governance verify --mode ci"

    def output(self) -> dict[str, object]:
        return {
            "name": self.name,
            "status": self.status.value,
            "missing_ids": list(self.missing_ids),
            "sources": list(self.sources),
            "reproduction": self.reproduction,
        }
