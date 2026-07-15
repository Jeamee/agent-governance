# GOV-CLI-M1 architecture design

## Module boundaries

`cli/src/governance/verify/` owns result aggregation, run binding, JSON output, and mode mapping. `cli/src/governance/subchecks/` owns the eight independent deterministic checks. `cli/src/governance/reports/` owns report parsing only. No adapter contains governance logic.

## Data and state model

The authorization record on protected main is the sole schema-version authority. Design and implementation-plan digests are recomputed from canonical, sorted path-and-content records. A verify invocation accepts only a report directory which was empty at invocation start; every accepted report must be below it.

Each subcheck returns `pass`, `fail`, `unverifiable`, or `needs_review`, missing IDs, source paths and a reproduction command. The aggregator preserves all results. CI maps any `unverifiable` result to final `fail`.

## Architecture and operational requirements

| ID | Requirement | Verifier |
|---|---|---|
| ARC-M1-002 | Each DECISION module has `covered_branches == num_branches`; independent frozen-blob and dogfood evidence agree. | TEST-M1-COVERAGE |
| ARC-M1-003 | CLI output conforms to v2 verify-output and run binding contract. | TEST-M1-SUITE |
| OPS-M1-001 | Required GitHub context executes suite, fixtures, compatibility groups, and coverage; a deliberately failing PR cannot merge. | EVIDENCE-M1-CI |
| OPS-M1-002 | An incremental mutation run covers both DECISION modules and records each surviving mutation. | EVIDENCE-M1-MUTATION |

## Rollout and rollback

The new required context first protects subsequent PRs; it cannot retrospectively gate its own bootstrap PR. Rollback is an append-only authorization revocation followed by a revert of delivery commits. It does not rewrite historical attestation conclusions.
