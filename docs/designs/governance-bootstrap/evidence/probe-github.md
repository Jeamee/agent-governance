# GitHub trust-chain probe

Date: 2026-07-15. Isolated public repository:
`Jeamee/agent-governance-probe-github`, protected default branch `master`.

## Results

| # | Attack / observation | Raw record | Verdict |
| --- | --- | --- | --- |
| 1 | Direct push to protected branch | `GH006 protected branch update failed`; GitHub required approval from someone other than the last pusher. | Supported: direct push is rejected. |
| 2 | Pull-request head changes workflow content | Run `29419974503` printed `ATTACK: workflow content from the pull-request head executed`. | Not supported as a trust root: PR workflow content is executable attacker input. |
| 3 | Same required check name forged by changed workflow | PR #2, run `29426514194`, printed `ATTACK: changed protected workflow still reports governance-gate success`; the named check was successful, while the PR remained `BLOCKED` / `REVIEW_REQUIRED`. | Named status alone is forgeable; CODEOWNERS/review stops merge, but the check is not source-bound. |

## Configuration and conclusion

The probe protection required `governance-gate`, pull requests, one review,
and CODEOWNERS. GitHub branch protection did not expose a ruleset binding the
required context to a trusted workflow source in this test. Therefore GitHub
also requires protected governance paths and the human Proof Gate; a passing
same-name status must not be treated as an independent trust root.

Raw links:

- PR #2: https://github.com/Jeamee/agent-governance-probe-github/pull/2
- attacker-head run: https://github.com/Jeamee/agent-governance-probe-github/actions/runs/29419974503
- same-name forged run: https://github.com/Jeamee/agent-governance-probe-github/actions/runs/29426514194
