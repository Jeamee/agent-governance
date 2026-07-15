"""Validate frozen design instances with the authorization-selected schema version."""

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
VERSIONED_SCHEMA_FILENAMES = {
    **SCHEMA_BY_FILENAME,
    "authorization-record.yaml": "authorization-record.schema.json",
    "delivery-request.yaml": "delivery-request.schema.json",
    "ci-attestation.yaml": "ci-attestation.schema.json",
    "authorization-revocation.yaml": "authorization-revocation.schema.json",
}


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def authorization_schema_version(authorization_path: Path) -> int:
    authorization = load_yaml(authorization_path)
    version = authorization.get("schema_version", 1)
    if version not in {1, 2}:
        raise ValueError(
            f"{authorization_path}: unsupported authorization schema_version {version!r}"
        )
    return version


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


def schema_path(repository_root: Path, version: int, filename: str) -> Path:
    return repository_root / "schemas" / f"v{version}" / filename


def validate_version_declarations(
    instance_dir: Path,
    version: int,
) -> list[str]:
    if version == 1:
        return []

    errors: list[str] = []
    for filename in VERSIONED_SCHEMA_FILENAMES:
        instance_path = instance_dir / filename
        if not instance_path.exists() or filename == "authorization-record.yaml":
            continue
        instance = load_yaml(instance_path)
        declared_version = instance.get("schema_version")
        if declared_version != version:
            errors.append(
                f"{filename}: worker-writable schema_version {declared_version!r} "
                f"does not match authorization version {version}"
            )
    return errors


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


def find_authorization(instance_dir: Path, repository_root: Path, supplied: Path | None) -> Path:
    if supplied is not None:
        return supplied.resolve()
    fixture_authorization = instance_dir / "authorization-record.yaml"
    if fixture_authorization.exists():
        return fixture_authorization
    task_id = load_yaml(instance_dir / "requirements.yaml").get("task_id")
    authorizations = sorted((repository_root / ".governance" / "authorizations").glob("*.yaml"))
    matches = [
        authorization
        for authorization in authorizations
        if load_yaml(authorization).get("task_id") == task_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one protected authorization for task {task_id!r} or --authorization"
        )
    return matches[0]


def validate_instance(
    instance_dir: Path,
    authorization_path: Path,
) -> tuple[int, list[str]]:
    repository_root = find_repository_root(instance_dir)
    version = authorization_schema_version(authorization_path)
    errors = validate_file(
        authorization_path,
        schema_path(repository_root, version, "authorization-record.schema.json"),
    )
    errors.extend(validate_version_declarations(instance_dir, version))

    for filename, schema_filename in SCHEMA_BY_FILENAME.items():
        instance_path = instance_dir / filename
        if not instance_path.exists():
            errors.append(f"missing required design instance: {instance_path}")
            continue
        errors.extend(
            validate_file(instance_path, schema_path(repository_root, version, schema_filename))
        )

    if not errors:
        errors.extend(validate_cross_references(instance_dir))
    return version, errors


def validate_examples(repository_root: Path) -> list[str]:
    errors: list[str] = []
    for version in (1, 2):
        cases = load_yaml(repository_root / "schemas" / "examples" / f"v{version}" / "cases.yaml")
        for schema_name, pair in cases.items():
            validator = Draft202012Validator(
                load_json(schema_path(repository_root, version, f"{schema_name}.schema.json")),
                format_checker=FormatChecker(),
            )
            if list(validator.iter_errors(pair["valid"])):
                errors.append(f"v{version}/{schema_name}: valid example was rejected")
            if not list(validator.iter_errors(pair["invalid"])):
                errors.append(f"v{version}/{schema_name}: invalid example was accepted")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_dir", type=Path, nargs="?")
    parser.add_argument("--authorization", type=Path)
    parser.add_argument("--validate-examples", action="store_true")
    args = parser.parse_args(argv)

    if args.instance_dir is None and not args.validate_examples:
        parser.error("instance_dir is required unless --validate-examples is used")

    errors: list[str] = []
    versions: list[int] = []
    repository_root: Path | None = None
    if args.instance_dir is not None:
        instance_dir = args.instance_dir.resolve()
        repository_root = find_repository_root(instance_dir)
        authorization_path = find_authorization(instance_dir, repository_root, args.authorization)
        version, instance_errors = validate_instance(instance_dir, authorization_path)
        versions.append(version)
        errors.extend(instance_errors)

    if args.validate_examples:
        examples_root = repository_root or Path.cwd()
        if not (examples_root / "schemas").exists():
            examples_root = find_repository_root(examples_root)
        errors.extend(validate_examples(examples_root))

    if errors:
        print("schema self-validation: FAIL")
        print("\n".join(errors))
        return 1

    print("schema self-validation: PASS")
    for version in versions:
        print(f"validated schema version: v{version}")
    if args.validate_examples:
        print("validated: schema examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
