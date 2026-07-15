# GOV-BOOTSTRAP-M0 rollout / rollback（硬冻结）

## Rollout

M0 完成（STEP-110 三 rubric + 全 evidence 落档）→ 主持人 Proof Gate → 出 M1 计划 + 新 authorization → M1 确定性 CLI → M2 两平台真实强制（含 prodream 四仓 coverage 欠账）→ M3 四仓 umbrella → M4 mutation/baseline/retention。每阶段一计划一授权，上一阶段 Proof Gate 通过才放下一阶段。

M0 期间无任何项目被强制接入：本阶段产物只影响中央仓自身，现有各仓 CI 零变化。

## Rollback

- 仓库层面：M0 无生产依赖，rollback = 删仓重建，成本可忽略。
- 唯一不可逆点：方法论真源迁移（STEP-002）。控制手段：迁移前后 sha256 逐字节核对（EVIDENCE-MIG），核对通过前不得改动 `~/.agents/` 原件；核对后原件降为 symlink，任何时刻仓内版本可完整还原本地。
- 探针/POC 失败不触发 rollback：失败结论本身是合法交付（D16/D14 的预裁决分支据此落地）。

## Authorization record 草案（正式版在 STEP-007 以真实 SHA/digest 生成，人审合入 .governance/authorizations/）

```yaml
task_id: GOV-BOOTSTRAP-M0
design_ref:
  repository: <github-owner>/agent-governance
  commit: <STEP-006 合入后的 full-sha>
  path: docs/designs/governance-bootstrap/
  digest: <硬冻结集合 sha256，STEP-007 计算>
gate_ref:
  repository: <github-owner>/agent-governance
  commit: <同上——bootstrap 特例：本任务的 gate 与设计同仓同 SHA>
allowed_repositories: [agent-governance, <探针仓×2>, <POC 样例仓×2>]
implementation_plan_digest: <sha256，STEP-007 计算>
required_profiles: [local-python]
lead_repository: agent-governance
```
