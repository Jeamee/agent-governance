"""Validate an M0 design instance against the published JSON Schema drafts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from jsonschema import FormatChecker


SCHEMA_BY_FILENAME = {
    "requirements.yaml": "requirements-manifest.schema.json",
    "modules.yaml": "modules.schema.json",
    "verification-plan.yaml": "verification-plan.schema.json",
    "evidence-scenes.yaml": "evidence-scenes.schema.json",
    "implementation-plan.yaml": "implementation-plan.schema.json",
}


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def validate_file(instance_path: Path, schema_path: Path) -> list[str]:
    instance = load_yaml(instance_path)
    validator = Draft202012Validator(
        load_json(schema_path),
        format_checker=FormatChecker(),
    )
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    return [
        f"{instance_path.name}: {'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in errors
    ]


def collect_ids(items: list[dict[str, Any]], key: str) -> set[str]:
    return {item[key] for item in items if key in item}


def validate_cross_references(instance_dir: Path) -> list[str]:
    requirements = load_yaml(instance_dir / "requirements.yaml")["requirements"]
    verification_plan = load_yaml(instance_dir / "verification-plan.yaml")
    scenes = load_yaml(instance_dir / "evidence-scenes.yaml")["scenes"]
    plan = load_yaml(instance_dir / "implementation-plan.yaml")["steps"]

    requirement_ids = collect_ids(requirements, "id")
    verifier_ids = collect_ids(verification_plan["verifiers"], "id")
    command_ids = collect_ids(verification_plan["commands"], "command_id")
    rubric_ids = collect_ids(verification_plan["rubrics"], "rubric_id")
    scene_ids = collect_ids(scenes, "id")
    step_ids = collect_ids(plan, "step_id")
    errors: list[str] = []

    change_requirements = {
        requirement_id
        for step in plan
        if step["kind"] == "change"
        for requirement_id in step.get("requirement_ids", [])
    }
    for requirement_id in sorted(requirement_ids - change_requirements):
        errors.append(f"cross-reference: requirement is not claimed by a change step: {requirement_id}")

    for step in plan:
        step_id = step["step_id"]
        unknown_dependencies = set(step["depends_on"]) - step_ids
        for dependency in sorted(unknown_dependencies):
            errors.append(f"cross-reference: {step_id} depends on unknown step {dependency}")

        for requirement_id in step.get("requirement_ids", []):
            if requirement_id not in requirement_ids:
                errors.append(f"cross-reference: {step_id} has unknown requirement {requirement_id}")

        for verifier_id in step.get("verifier_ids", []):
            if verifier_id not in verifier_ids:
                errors.append(f"cross-reference: {step_id} has unknown verifier {verifier_id}")

        completion = step.get("completion", {})
        for command_id in completion.get("command_ids", []):
            if command_id not in command_ids:
                errors.append(f"cross-reference: {step_id} has unknown command {command_id}")
        for scene_id in completion.get("evidence_scene_ids", []):
            if scene_id not in scene_ids:
                errors.append(f"cross-reference: {step_id} has unknown scene {scene_id}")
        for rubric_id in completion.get("approval_rubric_ids", []):
            if rubric_id not in rubric_ids:
                errors.append(f"cross-reference: {step_id} has unknown rubric {rubric_id}")

    return errors


def find_repository_root(instance_dir: Path) -> Path:
    for candidate in (instance_dir, *instance_dir.parents):
        if (candidate / ".git").exists():
            return candidate
    raise ValueError("could not locate repository root from instance directory")


def validate_authorizations(repository_root: Path, schema_dir: Path) -> list[str]:
    authorization_dir = repository_root / ".governance" / "authorizations"
    if not authorization_dir.exists():
        return []

    schema_path = schema_dir / "authorization-record.schema.json"
    errors: list[str] = []
    for instance_path in sorted(authorization_dir.glob("*.yaml")):
        errors.extend(validate_file(instance_path, schema_path))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_dir", type=Path)
    args = parser.parse_args(argv)

    instance_dir = args.instance_dir.resolve()
    repository_root = find_repository_root(instance_dir)
    schema_dir = repository_root / "schemas"
    errors: list[str] = []

    for filename, schema_filename in SCHEMA_BY_FILENAME.items():
        instance_path = instance_dir / filename
        if not instance_path.exists():
            errors.append(f"missing required bootstrap instance: {instance_path}")
            continue
        errors.extend(validate_file(instance_path, schema_dir / schema_filename))

    errors.extend(validate_authorizations(repository_root, schema_dir))
    if not errors:
        errors.extend(validate_cross_references(instance_dir))

    if errors:
        print("schema self-validation: FAIL")
        print("\n".join(errors))
        return 1

    print("schema self-validation: PASS")
    for filename in SCHEMA_BY_FILENAME:
        print(f"validated: {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
