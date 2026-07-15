# GOV-CLI-M1 Proof Gate

## Frozen inputs

- Design reference: `cd020e9b9ac5fa5b5c53c3f76ed2a81072418dec`.
- Design digest: `9ba0993c6c000b7a2f1a28d9aa85d83e3130d293ed9b88ffcb5bce9e7340540e`.
- Implementation-plan digest: `408b60251dca5f729113ece8493f63c79a536c0a540630706a2f226d10f54b84`.
- Authorization: `.governance/authorizations/GOV-CLI-M1.yaml`, merged in PR #14.

## Executed evidence

| Proof | Result |
|---|---|
| Full suite with branch coverage | 24 tests passed locally; CI job `m1-governance` passed on PR #18. |
| Dual mode | `pytest -m dualmode` passed. |
| Oracle | Frozen 8×4 fixture matrix (32 cells) passed. |
| Patch coverage | `diff-cover` used authorization `coverage_base_commit=cd020e9`; latest CI passed threshold 90. |
| Branch exact | Frozen blob read from `design_ref.commit` and dogfood command both passed. |
| Required context | Main now requires `validate-bootstrap-instances` and `m1-governance`. |
| Canary | PR #19 added an unimported changed source file; `m1-governance` failed and GitHub refused merge. PR was closed without merge. |

## Incremental mutation triage

| Module | Mutation | Test that killed it | Disposition |
|---|---|---|---|
| `subchecks` | `patch_percent >= 90` changed to `> 90` | `test_acc_cli_001_writes_v2_output` failed | Killed; restored without commit. |
| `verify` | final status tested `PASS` instead of `FAIL` first | `test_acceptance_failures_are_not_hidden` failed | Killed; restored without commit. |

## Technical decision record

The implementation uses the user's standing authorization for this Delivery
Goal. No post-hoc `human_approval` record is fabricated for technical evidence.
The first whole-repository coverage baseline is evidence only; M2 must bind its
object digest before enabling baseline non-regression enforcement.
