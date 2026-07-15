# Optional local hooks

M0 does not distribute hooks automatically. CI and protected paths remain the
enforcement boundary. A future hook may warn before an implementation worker
edits a protected design, `.governance/`, CI, coverage, mutation, or baseline
path; it must never be presented as the sole enforcement mechanism.

M0 has no Claude Code deny hook to install. `ACC-DOC-001` is intentionally an
M1+ verification target and is not claimed by this bootstrap.
