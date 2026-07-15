# Gitea 1.26.4 trust-chain probe

Date: 2026-07-15. Repository: `Prodream/agent-governance-probe-gitea`.
All attacks use isolated branches and remain unmerged.

## Results

| # | Attack / observation | Raw record | Verdict |
| --- | --- | --- | --- |
| 1 | Delete required workflow | PR #2 merge API: `Not all required status checks successful` | Supported: missing required context blocks merge. |
| 2 | Rename required job | PR #3 run 895 succeeded with context `governance-gate / renamed-governance-gate (pull_request)`; merge API rejected it. | Supported: exact context name is enforced. |
| 3 | Non-admin Worker direct push | Temporary normal account with repository write permission pushed `main`; server replied `Not allowed to push to protected branch main`. Account and token were removed after the test. | Supported: protection rejects unwhitelisted write tokens. |
| 4 | China Runner accesses public governance revision | Run 886 downloaded fixed GitHub commit and executed `uv lock --check` plus `uv run --locked`; output `agent-governance 0.0.1`. | Supported for public fixed-SHA archive. Private-read credential isolation remains unverified. |
| 5 | Author self-approval | PR #4 review API returned `approve your own pull is not allowed`. | Supported: author self-approval is rejected. |
| 6 | Alter workflow while retaining check name | PR #4 / run 890 printed `ATTACK: altered workflow retains governance-gate name` and emitted successful required context. | Not supported: status checks are not bound to immutable workflow content. |
| 7 | Replace gate_ref | PR #5 / run 892 replaced the gate reference with forty zeroes and still succeeded. | Not supported: platform does not independently detect changed gate references. |
| 8 | Duplicate same-name status | PR #6 ran one success and one failure with identical context; commit status was failure and merge was rejected. | Supported: a failed duplicate is not overwritten by a successful duplicate. |
| 9 | Protected file patterns | Protection API reports `.gitea/workflows/**,.governance/**,docs/designs/**`; PRs #4 and #5 modify the first two and cannot self-approve. | Partially supported: patterns are configured, but strong enforcement cannot compensate for #6/#7. |

## D16 decision

D16 downgrade is triggered. Gitea can block direct pushes, missing/renamed contexts, self-approval, and duplicate-status failure, but it cannot bind a required context to trusted workflow content or an immutable `gate_ref`. Prodream v1 therefore remains **audit evidence plus human Proof Gate**, not an all-machine hard gate. This does not restore line-by-line review; the human review is limited to the evidence package, deviations, and exceptions.

## Raw links

- PR #2: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/pulls/2
- PR #3: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/pulls/3
- PR #4: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/pulls/4
- PR #5: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/pulls/5
- PR #6: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/pulls/6
- Run 886: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/actions/runs/886
- Run 890: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/actions/runs/890
- Run 892: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/actions/runs/892
- Runs 893/894: https://git.prodream.cn/Prodream/agent-governance-probe-gitea/actions/runs/893
