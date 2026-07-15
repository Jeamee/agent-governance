"""Intentional M1 canary: this branch must fail patch coverage."""


def uncovered_decision(value: bool) -> str:
    if value:
        return "true"
    return "false"
