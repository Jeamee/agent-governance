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

## Real-trial interpretation

The user clarified that implementing GOV-BOOTSTRAP-M0 itself is the real trial;
no `eligibility-filter` business implementation is authorized. The previously
created local eligibility-filter implementation worktree and branch were
deleted without merge or deployment.

This differs from the frozen STEP-109 wording, which calls for a second,
eligibility-filter instance. The difference is declared as `DEV-002` in the
delivery request with `verification_impact: needs_review`. It cannot be
silently treated as two completed instantiations.

Accordingly, the bootstrap instance supplies the actual end-to-end artifacts
(frozen package, authorization, implementation commits, evidence, and delivery
request). The task owner explicitly delegated technical governance decisions to
the implementation agent; the approval records under `.governance/approvals/`
record the resulting Proof Gate assessment.
