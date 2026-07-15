# Governance schemas

`v1/` is the ten-file, byte-for-byte immutable M0 snapshot. Root-level entries
are compatibility symlinks to that snapshot so existing M0 commands retain one
source of truth. `v2/` is selected only by a protected authorization record.

Each version has valid and invalid examples in `examples/`; the schema
compatibility fixtures exercise M0 on v1 and a synthetic M1 instance on v2.
Policy semantics such as forbidden roots remain solely in `.governance/policy.yaml`.
