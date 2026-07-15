# GOV-CLI-M1 rollout and rollback

## Rollout

1. Merge the frozen design package and authorization before any implementation commit.
2. Add the M1 workflow job without deleting `validate-bootstrap-instances`.
3. Run a canary PR whose fixture and coverage failures keep it unmergeable.
4. Record the first full-repository baseline as digest-addressed evidence and bind it only in M2.

## Rollback

Merge a v2 authorization-revocation record, revert the implementation commits, and retain all prior evidence. Do not alter frozen M1 verification-plan content to retrofit the M2 baseline.
