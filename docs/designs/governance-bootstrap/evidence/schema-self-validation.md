# Schema self-validation

Command:

```text
uv run --project cli python -m governance.schema_check docs/designs/governance-bootstrap/
```

Observed output on 2026-07-15:

```text
schema self-validation: PASS
validated: requirements.yaml
validated: modules.yaml
validated: verification-plan.yaml
validated: evidence-scenes.yaml
validated: implementation-plan.yaml
```

No design-package §5 deviation was made.
