# Template instantiation record

## Bootstrap instance

The bootstrap instance is complete in
`docs/designs/governance-bootstrap/` and contains the three-layer package:

- `business-design.md`;
- `architecture-design.md`;
- `requirements.yaml`, `modules.yaml`, `verification-plan.yaml`,
  `evidence-scenes.yaml`, `implementation-plan.yaml`, and `rollout.md`.

Its frozen import and authorization are documented in
`package-freeze.md`; schema self-validation is documented in
`schema-self-validation.md`.

## Real-trial instance: eligibility-filter

The selected real task is `eligibility-filter`, as required by STEP-109.
Its existing reviewed design sources are:

- `/Users/jun/Codes/prodream/filter-system-design.md` (business design v7);
- `/Users/jun/Codes/prodream/filter-system-architecture.md` (architecture v2.1).

The trial has **not** completed all required stages: its trial-specific frozen
three-layer instance, authorization, implementation delivery request, and
human fail-closed Proof Gate record are absent. This document intentionally
does not substitute the existing design documents for those required artifacts.

Consequently `ACC-TRIAL-001`, `ACC-TPL-001`, STEP-109, and STEP-110 remain
open pending a real, human-reviewed trial. This is a fail-closed result, not a
passing template claim.
