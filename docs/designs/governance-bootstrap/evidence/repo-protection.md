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

The central authorization PR is intentionally blocked until an independent
human review; its own author cannot self-satisfy the required review.
