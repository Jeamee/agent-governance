# GOV-BOOTSTRAP-M0 业务设计（第一层，硬冻结）

> task_id: GOV-BOOTSTRAP-M0。任务：建立 agent-governance 中央工具仓并完成 M0 阶段（设计真源见 `design-package-v1.1.md`，冻结版，主持人马俊 2026-07-15 批准）。
> Bootstrap 声明：本任务交付的就是治理系统自身，CLI 尚不存在，本任务所有机器 verifier 由人工按同等规则执行（M0 的既定属性，非豁免作弊）。

## 1. Known / Unknown 四格结论

- **Known Knowns**：方法论真源 `~/.agents/AI_DELIVERY_METHODOLOGY.md` 已定稿；设计包 v1.1 已冻结，D1–D19 全 CLOSED；用户全栈、项目横跨 GitHub（个人）与 Gitea 1.26.4（公司 prodream 四仓）；四仓 coverage 欠账已核实（M2 处理，不在本任务）。
- **Known Unknowns**（本任务的实验对象，不是决策悬案）：Gitea 九项信任根能力；GitHub 三项自举边界；diff-cover 能否统吃两栈 patch coverage；uv 哪种分发方式真实吃到 lock。四者均以书面结论落档为交付物。
- **Unknown Knowns**：本仓惯例已显性化进设计包（AGENTS.md/CLAUDE.md symlink 模式、EXP 优先、monorepo 根非 git）。
- **Unknown Unknowns**：探针可能发现两平台都存在未预期的旁路——发现即回流主持人，不自行补救。

## 2. 业务事实与用户流程

- **用户**：马俊（主持人/批准人/审美与 D 题决策者）、Claude Code 与 Codex（设计期对抗审议双方）、第三方实施 Worker（按冻结设计施工）。
- **痛点**：现有 gate 依赖模型自觉，四治理前提（冻结真源在 Worker 写权限外、gate 在 Worker 写权限外、跨仓组合验证、每要求有验证者）无一机器成立。
- **本阶段（M0）交付**：中央工具仓存在且受保护；方法论迁入；schema/模板草案可用；三项实验（探针/diff-cover/uv）有书面结论；一个真实任务人工走通完整三层流程。
- **不做**（见设计包 §11）：CLI 实现（M1）、平台强制接入（M2）、跨仓 umbrella（M3）、mutation/baseline 平台化（M4）。

## 3. 行为验收清单

机器规范源 = 同目录 `requirements.yaml`（本文件是其人类可读源头，语义一致由主持人审定）。六元组示例（全集见 yaml）：

| 验收 ID | 前置状态 | 动作 | 可观察结果 | 禁止发生 | 对应验证者 |
|---|---|---|---|---|---|
| ACC-REPO-001 | 仓库已建、保护已配 | 以实施 token 直接 push main | 被平台拒绝 | push 成功 | EVIDENCE-REPO-PROT |
| ACC-REPO-002 | 七目录骨架就位 | 结构审查 | 仓内无任何项目实例数据（bootstrap 自身实例除外） | specs/exceptions/approvals 目录出现 | 主持人 human_approval |
| ACC-MIG-001 | 方法论在 ~/.agents/ | 迁移入仓 | 仓内为真源，本地是 checkout/symlink，内容逐字节一致 | 出现两份可分别编辑的副本 | EVIDENCE-MIG |
| ACC-PKG-001 | 设计包冻结版在本地 | 按 §4.2 布局入仓 | design-package + bootstrap 三层获得不可变 commit SHA | 入仓时内容被修改 | EVIDENCE-PKG |
| ACC-SCH-001 | 八个 schema 草案完成 | 用草案校验 bootstrap 自身全部 yaml 实例 | 全部通过或差异有书面解释 | 草案与设计包 §5 规格冲突未申报 | EVIDENCE-SCH + human_approval |
| ACC-PROBE-001 | 探针仓就绪 | 执行 GitHub 3 项 + Gitea 9 项 | 每项有结论 + 截图/日志 | 任何一项以推测代替实测 | EVIDENCE-PROBE-GH / EVIDENCE-PROBE-GITEA |
| ACC-POC-001 | 两栈样例仓就绪 | diff-cover 吃 pytest/vitest Cobertura | TSX 行号对齐结论落档（成或败+自研决策） | 只测 Python 侧就宣称统吃 | EVIDENCE-POC-DIFFCOVER |
| ACC-POC-002 | CLI 骨架占位存在 | 按两种方式分发执行 | 选定真实吃到 uv.lock 的方式，五项结论落档 | 未验证 lock 生效就选定 | EVIDENCE-POC-UV |
| ACC-TRIAL-001 | 模板就绪 | 选一真实业务任务人工走三层设计→授权→实施→证明 | 交付含完整证明包 | 试跑任务用简化版模板走过场 | 主持人 human_approval（rubric: bootstrap-trial-v1） |
| ACC-TPL-001 | 三层模板入仓 | 用 rubric 审 bootstrap + 试跑任务两次实例化 | 步骤具体/目标明确/判据可观察/无空壳步骤 | 大而全步骤认领全部 requirement | EVIDENCE-TPL + human_approval（rubric: plan-quality-v1） |

## 4. 状态流转设计 Gate 适用性声明

本任务为工具仓建设与实验，无运行时多步骤流程、异步任务、状态字段或缓存——按 prodream 根 AGENTS.md 状态 Gate 的豁免条款（轻量展示/无状态计算除外）**声明不适用**。此声明本身经主持人批准（本设计合入即批准）。

## 5. D 题清零记录

D1–D19 全部 CLOSED，决议全文见 `design-package-v1.1.md` §3（主持人马俊 2026-07-15 批准）。本任务无新增未决 D 题。探针/POC 是实验项不是决策悬案：其结论决定 D16 降级分支是否触发与 D14 分发方式选型，处置路径已预先裁决。
