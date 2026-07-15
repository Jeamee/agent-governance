# Repository protection evidence

GitHub repository `Jeamee/agent-governance`, branch `main`:

- pull requests required;
- one approving review and CODEOWNERS review required;
- stale review dismissal and last-push approval required;
- required check `validate-bootstrap-instances` is strict;
- administrators are included; force pushes and branch deletion are disabled.

Direct-push attack evidence from the public isolated GitHub probe:

```text
remote: error: GH006: Protected branch update failed for refs/heads/master.
remote: - New changes require approval from someone other than the last pusher.
! [remote rejected] HEAD -> master (protected branch hook declined)
```

The central authorization and domestic-lock PRs were merged after the user
explicitly authorized direct technical operation. During those merges the
required review count was temporarily reduced to zero, then restored to one
with CODEOWNERS and last-push approval re-enabled. Therefore this record is
**not** evidence of an independent human review for those two PRs; that gap
must remain visible to the M0 Proof Gate.
