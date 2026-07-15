# Governance 系统实施设计包 v1.1

> 状态：**已冻结（主持人马俊 2026-07-15 批准；D1/D15/D16/D17/D18/D19 全部 CLOSED，进入 M0）**。不可变 commit SHA 引用于 M0 入仓后确立；入仓前本文件不得再修改（本次 r3+机械修正为冻结版）。
> 修订 r2（2026-07-15）：采纳 Codex 三层专项审议——第三层**文件基线不可变、执行路线可申报偏离**（撤回"改文件+申报非空=放行"）；结构闭合校验八条；diff↔targets 机器对账 + 结构化 DEV record；命令单真源；Markdown↔YAML 诚实条款；ARC/OPS 验证者放开。
> 修订 r3（2026-07-15）：采纳 Codex r2 核验四组意见——`incidental_paths` 改为**因果约束的 `derived_paths`**（免重复申报不免因果证明）；目录前缀 target 必须**绑定架构模块边界**（module_id + scope_reason，通用源码根非法）；计划机器真源定为 **implementation-plan.yaml**（.md 只作人类说明）；step 改 **verifier_ids + 按类型的 completion**（不强迫非命令 verifier 伪造 command）；DEV 按 category 条件校验，`needs_review` 强制 Proof Gate 人工待审。**D19 核心设计已过，本轮补齐机器接口后待主持人正式关闭。**
> 本轮修订来源：Codex 对抗审议 v2（中央/分布边界重画 + R1–R9）+ 用户新增三层设计结构。回应见同目录 `response-claude-v2.md`。
> 批准冻结后：实施 Worker 不得修改本文档；遇未覆盖分支必须暂停回流，不得自行补默认值。
> Bootstrap 特例：governance repo 自己就是自己的业务仓——本设计包与其治理实例（authorization / exceptions）住它自己的 `docs/designs/` 与 `.governance/` 下，M0 建仓后入仓获得不可变 commit SHA。这与"中央仓无业务实例"裁决自洽：那是它自己的实例。
> 方法论依据：`~/.agents/AI_DELIVERY_METHODOLOGY.md`（M0 迁入后以仓内版本为准）。

---

## 1. 目标与架构裁决

建一个 **中央 governance 工具仓 + 单一 governance CLI + GitHub/Gitea 薄适配器 + 各业务仓分散的治理实例**，使方法论四治理前提成立：冻结真源在 Worker 写权限外、gate 在 Worker 写权限外、跨仓组合验证存在、每条要求有验证者。

**核心架构裁决（审议定案，Worker 不得偏离）**：

1. 对项目暴露的稳定公共接口是 **CLI（`governance verify`）**，CI workflow 只是平台适配器；
2. 验收对账是 **verifier-driven**（每条要求声明自己需要哪些验证者），不是固定三方笛卡尔积；
3. delivery 产物**声明与证明分离**：Worker 只写 delivery request，gate 结果只能由 CI 在同一 run 内生成；
4. 机器只认**完整 commit SHA** 作冻结引用，tag 仅作人类别名；
5. **中央仓只中心化治理方法与执行工具**（methodology / schemas / cli / adapters / templates / fixtures / docs）；各项目的业务设计、架构决策、验收清单、证据、授权、例外、交付数据**一律分散在各业务仓的受保护路径**，中央仓不出现任何项目实例。

**威胁模型（D17 定案，双处申报见 §11/§12）**：v1 防"非恶意但会优化指标的 Worker + 人类误操作"。拥有任意代码执行能力的恶意 Worker（在 CI run 内伪造报告、逃逸沙箱）的隔离不在本期范围。

## 2. 术语

| 术语 | 定义 |
|---|---|
| `gate_ref` | 项目引用的 governance 工具版本：`{repository, commit(完整 SHA)}` |
| `design_ref` | 某任务冻结设计包的**复合引用**：`{repository, commit(完整 SHA), path, digest}`——同一 commit 可含多任务设计，仅 SHA 不够 |
| requirements manifest | 冻结的要求清单，每条含 `kind`（behavior / architecture / operability / ui_quality）+ 六元组（behavior 类）+ required_verifiers |
| verification plan | 冻结的验证执行计划：verifier → runner profile / command id / report slot / 环境要求 / 预期分片 / mock 政策 |
| authorization record | 业务仓受保护路径中、人审合入的实施授权：绑定 task ↔ 获批 design_ref ↔ gate_ref ↔ 允许仓库 ↔ required profiles |
| verifier | 一条要求的证明方式：`test / contract_test / real_db_test / browser_test / umbrella_e2e / mutation / evidence / human_approval / static_rule / regression_red / before_after` |
| delivery request | Worker 交付时的声明部分（只能复述 authorization，不能决定它） |
| CI attestation | CI 生成的证明部分（同 run 内） |
| runner profile / report slot | 受保护 policy 定义的执行环境档位与报告槽位；Worker 不得自选 |
| policy diff classifier | 反作弊 diff 分类器 |

## 3. 决议账本（v1.1 更新）

| D | 决议 |
|---|---|
| D1 **CLOSED** | 单一 **public** GitHub repo 为工具真源，不做镜像（中央仓无业务实例，Gitea runner 无需跨平台私有凭据，降低凭据泄露与分发复杂度）；本地 `~/.agents/` 为 checkout/symlink；Gitea 项目下载固定 SHA 执行 |
| D2（v1.1 改写） | 原"不拆 specs 信任域"撤销，由架构裁决 5 取代：业务实例分散各业务仓。`gate_ref` 与 `design_ref` 仍是两个独立引用，设计包提交不得顺带升级 gate 版本 |
| D3→D10（v1.1 改写） | 批准载体：平台原生 required reviewer / CODEOWNERS 人审优先；exception record 移入**业务仓 `.governance/exceptions/`（保护路径，人审合入 main 后方有效）**。中央仓托管例外的分支按"最弱链"推理关闭：平台保护不了 `.governance/` 就同样保护不了 workflow，机器链已断，中央托管修不好它 |
| D7 | verifier 关系：列表默认 `all_of`；显式 `any_of` 组作列表元素；不嵌套；human_approval 可与机器 verifier 共存于 all_of |
| D8 | TS patch coverage：先 POC diff-cover 统吃两栈（pytest-cov / vitest istanbul 均出 Cobertura），验证 sourcemap 后 TSX 行号与 git diff 对齐；失败再自研（M0，ACC-POC-001） |
| D9 | gate 结果存 CI artifact + 固定摘要 + 人类可读 check summary；不做签名系统 |
| D11 | Worker 会话与 CI token 一律无 repo admin scope；分支保护 / CODEOWNERS 修改权只在人类账号 |
| D12 | 远程 CI 按固定 SHA 执行为底线；本地 deny 治理真源写路径为防误操作加层 |
| D13 | 时延靶（M2 后调）：快 gate < 2min；集成 < 10min；umbrella/mutation/截图走 label 或 nightly；本地 verify 秒级预检 |
| D14 | CLI 用 Python 3.12 + uv；分发方式以 M0 uv POC 结论为准（`uvx --from git+…#subdirectory=cli` vs checkout@SHA + `uv run --project cli`，取真实吃到 uv.lock 的那种） |
| **D15 CLOSED** | 设计批准的机器载体 = **authorization record**（业务仓 `.governance/authorizations/<task>.yaml`，人审合入受保护 main 后生效）；protected tag 仅作人类别名。必须满足：先人审合入受保护 main（本 PR 自带无效，防自批）；绑定 design_ref、implementation_plan_digest、gate_ref、required profiles、允许仓库；**被撤销或替换后，旧记录不得继续授权新交付**；delivery request 与 record 不一致即 fail |
| **D16 CLOSED（降级分支预批准；是否触发由 M0 探针决定）** | 信任根按平台分别声明。GitHub = 分支保护 + CODEOWNERS 强制人审保护路径（workflows / .governance/ / docs/designs/）+ required check 来源绑定（探针确认）。Gitea = §7 九项探针实测。**主持人预裁决：若 Gitea 探针证明无法建立强信任根，v1 不建外部 status publisher，Prodream 侧降级为"审计留痕 + 人工 Proof Gate"**，且必须书面标记：该状态不是全机器硬 gate、不宣称已完全替代人工验证、人工只审证明包/偏离/例外不恢复逐行 code review、外部 publisher 建设与否未来单独立项 |
| **D17 CLOSED** | v1 威胁模型限定为：防会优化指标的 AI Worker + 防误操作与无意弱化 gate；**不防**任意恶意代码执行、CI 沙箱逃逸、主动伪造报告（已在 §5.5 attestation、§11、§12 三处诚实申报） |
| **D18 CLOSED** | 跨仓任务必须在设计阶段**显式指定 `lead_repository`**，机器不得自动猜测（默认建议给人：契约被依赖方/服务提供方所在仓）。主仓负责保存：umbrella authorization、跨仓契约、各仓 design_ref、实施 SHA 组合、umbrella E2E 与最终组合 attestation |
| **D19 CLOSED（r3）** | 设计分三层：业务设计 / 架构设计 / 实施方案。**一、二层：语义与文件均硬冻结**（实施 diff 触碰即 `frozen` fail，改动必回流人批）。**第三层：文件基线不可变（同样进 `frozen`），半冻结的是执行路线的遵循程度**——Worker 可不完全按方案执行，但每处偏离必须以结构化 DEV record 写入 delivery request，且实际 diff 与计划 step targets / DEV 机器对账；需要重写计划 = 新计划版本 + 新 `implementation_plan_digest` + 新 authorization（人批 PR），不得在实施 PR 中改。机器只承诺引用完整性与对账闭合，不承诺方案语义质量（归设计期人审 rubric）。最终验收判据是 requirements manifest。**完整规格见 §4.3** |
| R12 附加条款 | mutation 平台化在 M4，但高危模块（计费/权限/状态 reducer 类）任务从 M1 起 Proof Gate 必须含一次手动增量 mutation 证据——按风险事件触发 |
| 参数化测试 | 预期**分片清单**全量必填 fail-closed；实例计数仅高危模块 fail-closed 条目必填，其余 `instances: all`（收集到的全过）+ warn 级"缩小 discovery"启发式盯收集面 |
| hooks | 不建自动分发；中央仓只放安装文档 |

## 4. 两层 Repo 结构

### 4.1 中央 `agent-governance/`（M0 建立，只有这七个目录）

```
agent-governance/
├── methodology/AI_DELIVERY_METHODOLOGY.md   # 从 ~/.agents/ 迁入
├── schemas/                                 # requirements-manifest / verification-plan /
│                                            # authorization-record / evidence-scenes /
│                                            # delivery-request / ci-attestation /
│                                            # exception / human-approval
├── cli/                                     # governance CLI（Python 3.12 + uv 项目）
├── adapters/
│   ├── github/verify.yml
│   └── gitea/verify.yml
├── templates/
│   ├── design-package/                      # 三层骨架：业务设计 / 架构设计 / 实施方案 + 各 yaml
│   ├── debate.md
│   └── goal-prompt.md
├── fixtures/                                # 每个 gate 四类：应通过/应拒绝/边界/绕过尝试
└── docs/hooks-install.md
```

**不得包含**：`specs/<project>/`、`exceptions/<project>/`、approvals、delivery 数据、任何项目业务事实。（Bootstrap 特例见文件头。）

### 4.2 各业务仓治理实例

```
docs/designs/<task>/
├── business-design.md          # 第一层：业务事实、行为验收（六元组）、状态流转两表、D 题清零记录 —— 硬冻结
├── architecture-design.md      # 第二层：系统结构、模块边界、契约、数据模型、ARC-/OPS- 要求 —— 硬冻结
├── modules.yaml                # 第二层机器投影：module_id → 边界前缀清单 —— 硬冻结
├── implementation-plan.yaml    # 第三层机器真源：结构化步骤表 —— 文件不可变基线（D19）
├── implementation-plan.md      # 第三层人类说明（非规范副本，机器不读）—— 与 yaml 同 digest 锁定
├── requirements.yaml           # requirements manifest（kind 全集）
├── verification-plan.yaml
├── evidence-scenes.yaml
└── rollout.md
.governance/
├── policy.yaml                 # runner profiles / report slots / 保护路径清单 / derived_paths 因果规则 / 非法通用根名单 / 分类器参数
├── authorizations/<task>.yaml
├── exceptions/<id>.yaml
└── approvals/<id>.yaml         # human_approval 记录（与 exception 分立）
```

目录名可适配各仓惯例，但**五条不变量**必须成立：

1. 设计与代码同仓共存；
2. 设计包先于实现合入（经人审 PR）；
3. `docs/designs/` 与 `.governance/` 及 CI workflow 是平台保护路径，改动必经人审（GitHub：CODEOWNERS + required review；Gitea：按探针结论）；
4. 实施 Worker 触碰这些路径必然被发现（`frozen`/`policy` 子检查为第二道防线）；
5. CI 从 authorization 指定的冻结 SHA 读设计并核对 digest，**绝不读 PR head 上可能被改的版本**。

### 4.3 设计三层规格（主持人 2026-07-15 新增需求，本节为其完整方案）

三层分工一句话：第一层回答"做什么、凭什么验收"，第二层回答"系统怎么长"，第三层回答"Worker 按什么顺序动哪些文件"。三层单向依赖：三→二→一，下层不得反向改写上层语义。

#### 第一层：业务设计（business-design.md，硬冻结）

| 项 | 规格 |
|---|---|
| 必含内容 | Known/Unknown 四格结论；业务事实与用户流程；**行为验收清单六元组**（requirements.yaml 中 `kind: behavior` 条目的人类可读源头）；业务状态流转表；UI 证据场景（evidence-scenes.yaml 源头）；**D 题清零记录**（每个已决 D 题：问题/决议/决策人） |
| 产出者 | 设计期对抗审议，Claude 侧主导（业务/UX/异常路径视角），人为主持人 |
| 审查者（第零原则） | 对抗审议对方 agent + 主持人批准合入；机器侧由 `schema` 校验 requirements.yaml 投影完整、`frozen` 守不可变 |
| 禁止 | 出现未决 D 题；把分支决策藏进"实现时再定" |

#### 第二层：架构设计（architecture-design.md，硬冻结）

| 项 | 规格 |
|---|---|
| 必含内容 | 系统结构与**模块边界声明**（每个模块给 MODULE-<域>-<名> ID + 边界前缀，机器投影至 modules.yaml，供第三层 target 绑定与 ID 集合一致性校验）；**跨仓拆分**（哪个仓改什么，跨仓任务含契约 F 段）；API/数据契约；数据模型与迁移；数据状态流转表；`kind: architecture / operability` 条目源头（每条给 ARC-/OPS- ID）；技术选型与理由；rollout/rollback 策略（rollout.md 可并入或独立） |
| 产出者 | 对抗审议，Codex 侧主导（架构/数据/oracle 视角） |
| 审查者 | 对方 agent + 主持人；机器侧：每个 ARC/OPS ID 必须有**适合其性质的 verifier**（static_rule / test / umbrella_e2e / runtime・deployment evidence / human_approval rubric 均可）；仅 human_approval 时必须书面给出无法自动化的理由与 rubric |
| 禁止 | 与第一层验收冲突（冲突=回到审议，不得单方改第一层） |

#### 第三层：实施方案（implementation-plan.yaml 机器真源 + .md 人类说明；文件不可变基线 + 执行路线可申报偏离，D19 r3）

一句话定义：**冻结原计划，允许执行偏离；不允许 Worker 一边偏离、一边改写用于判断偏离的基线。**

| 项 | 规格 |
|---|---|
| 必含内容 | **机器真源 `implementation-plan.yaml`**：有序结构化步骤表（schema 见下）；`implementation-plan.md` 只作人类说明（非规范副本，机器不读，展示解析后命令须标注）。步骤间依赖用 `depends_on` 显式声明；测试先行点标注（bugfix 的红绿步骤显式在列）；预估风险步骤标注 |
| 产出者 | **默认设计期产出**（基于已冻结的一、二层，由审议双方之一起草、对方过目、人批准）——Worker 拿到即可执行。大型任务可选让实施 Worker 起草、经人批后入包，批准动作仍在人 |
| 文件不可变 | `implementation-plan.yaml` + `implementation-plan.md` 共同由 `implementation_plan_digest` 锁定，进 `frozen` 检查：**实施 diff 触碰任一即 fail**。需要重写计划 = 新计划文件版本 + 新 digest + 新 authorization record（人批 PR，与实施 PR 分离），一、二层与 design_ref 不动 |
| 执行偏离 | Worker 可不完全按方案执行（步骤顺序/文件划分/局部做法），但每处偏离必须以**结构化 DEV record**（schema 见 §5.4）写入 delivery request，Proof Gate 人工审。**不属于偏离、属于违规必须回流的**：引入清单外行为、跳过红绿步骤、触碰一、二层语义 |
| diff 对账 | CI 对实际修改文件做映射：被某 step `targets` 覆盖 = 正常；未覆盖但有对应 DEV record = 允许并留痕；命中 `derived_paths` 因果规则 = 免单独 DEV（规则见下）；三者皆无 = **fail** |
| derived_paths（因果豁免，非 blanket） | 受保护 policy.yaml 定义，**免重复申报不免因果证明**：① 派生文件仍出现在 attestation，不静默忽略；② 仅当声明的触发源（`requires_changed_any`）已被 step/DEV 覆盖时才免 DEV；③ lockfile 单独变化而 manifest 未变必须走 DEV（供应链信号）；④ generated 文件必须绑定 verification-plan 中的 `producer_command_id`；⑤ test snapshot 不做 blanket 豁免，必须被 verify step 或 DEV 认领；⑥ screenshot baseline、`.governance/`、CI、源码根目录禁止配置为 derived（配置即 schema fail）；⑦ 规则本身住受保护 policy |
| 命令单真源 | 步骤只引用 completion criteria / verifier ID / `command_id`；实际 shell 命令、runner profile、环境、report slot 只在受保护的 verification-plan.yaml 定义。人类文档展示解析后命令必须标注"非规范副本" |
| 边界诚实 | 机器只承诺**引用完整性与结构闭合**（见下八条）+ diff 对账，不承诺方案语义质量；语义质量归设计期人审 rubric（ACC-TPL-001）。方案本身错了，验收判据仍是 requirements manifest，**方案错误不得成为验收放水理由**。同理：一、二层 Markdown 与 requirements.yaml 的语义一致归人审，机器只校验两边 ID 集合一致；requirements.yaml 是 Proof Gate 唯一机器规范输入 |

**结构化步骤 schema（implementation-plan.yaml，机器唯一读取源）**：

```yaml
step_id: STEP-003                  # 唯一
kind: change | verify
depends_on: [STEP-001]             # 依赖无环；引用的前置步骤必须存在
targets:                           # change 步骤必填
  - path: src/domain/order/reducer.ts        # 精确文件路径默认允许；可为尚不存在的新文件
  - module_id: MODULE-ORDER-STATE             # 目录前缀必须绑定架构模块（modules.yaml 中存在）
    prefix: src/domain/order/                 # 前缀必须落在该模块声明的边界内
    scope_reason: 状态 reducer 与 transition 作为同一架构模块调整
requirement_ids: [ARC-STATE-001, ACC-STATE-004]
verifier_ids: [TEST-STATE-004, EVIDENCE-STATE-004, APPROVAL-MOTION-001]   # 全类型 verifier 均可认领
completion:                        # 按 verifier 类型分槽，不强迫非命令 verifier 伪造 command
  command_ids: [vitest-state]                 # 可执行 verifier：必须存在于 verification-plan.yaml
  evidence_scene_ids: [EVIDENCE-STATE-004]    # evidence：必须存在于 evidence-scenes.yaml
  approval_rubric_ids: [motion-quality-v1]    # human_approval：必须有 rubric
```

**targets 粒度规则**：精确文件默认允许（含新建）；目录前缀必须带 `module_id` + `scope_reason` 且前缀在模块边界内；**仓库根与通用源码根（`src/`、`app/`、`packages/` 等，名单在受保护 policy）直接非法，不是 warn**；不存在的新目录允许，但父级必须落在已声明模块边界内；跨多个架构模块必须拆多个 target 或走 DEV。这是语义边界不是数字阈值，不构成新 Goodhart 指标。

**结构闭合校验八条（`schema` 子检查执行，即 ACC-IPL-001"引用完整性与结构闭合校验"——只证明没有断链，不证明方案好）**：

1. 每个 requirement ID 至少被一个 `change` 步骤认领；
2. 每个 verifier ID（全类型）至少被一个 `verify` 步骤认领，且 completion 按类型校验：可执行 verifier 有 `command_id`、evidence 有 scene、human_approval 有 rubric；
3. 所有引用 ID 必须真实存在，禁止 `ALL`、范围表达式、通配 ID；
4. 每个 change 步骤有明确 target，且满足粒度规则（精确文件，或 module_id 绑定的边界内前缀）；
5. completion 引用的 `command_id`/scene/rubric 分别存在于 verification-plan / evidence-scenes / rubric 清单；步骤不得在计划内覆盖 verification-plan 的命令定义；
6. 实际修改文件 ↔ step targets / DEV / derived_paths 因果规则对账（见上表）；
7. 步骤 ID 唯一、`depends_on` 无环、前置步骤存在；
8. 禁止占位表达（`TBD`、"相关文件"、"全部模块"、"视情况处理"等 token 清单）。

**反 Goodhart 保留**：不设"一步骤最多认领几个 requirement"数字上限；高 fan-in 只 warn，交设计期人审。（目录 target 的约束是语义边界——模块绑定与非法根名单——不是数字阈值。）

#### 冻结与 digest 边界

- **硬冻结集合** = business-design.md + architecture-design.md + modules.yaml + requirements.yaml + verification-plan.yaml + evidence-scenes.yaml + rollout.md；`design_ref.digest` 覆盖此集合；实施 diff 触碰即 `frozen` fail。
- **implementation-plan.yaml + implementation-plan.md 同样不可在实施 diff 中修改**（`frozen` fail），以独立的 `implementation_plan_digest` 共同锁定（authorization record 字段）——digest 分离的价值：换计划走"新计划 + 新 digest + 新 authorization"，无需重冻结一、二层、无需新 design_ref。

#### 流程嵌入（与协作流程的对接顺序）

```
对抗审议产出一、二层 → 主持人批准，硬冻结集合合入（人审 PR）
  → 基于冻结的一、二层产出实施方案 → 人批合入
    → authorization record 合入（含 design_ref.digest + implementation_plan_digest）
      → /goal 指向 design_ref，Worker 按 implementation-plan 执行
        → delivery request（含偏离申报）→ CI verify → Proof Gate
```

#### 裁剪规则

按影响面裁剪：纯配置/typo/一句话 diff 不走本流程；业务分支 bug 可并三层为一份简版方案（业务事实+方案+证明策略三段）+ requirements + 偏离申报照常；新 feature / 新 handler / 跨仓契约变更三层全套。并层时冻结语义取严：并入的内容按其原层级的冻结强度对待。

`templates/design-package/` 提供三层骨架模板，模板本身是中央仓交付物（见 ACC-TPL-001）。

## 5. Schema 规格

### 5.1 requirements-manifest

```yaml
id: ACC-<域>-<序号>              # kind=behavior 用 ACC；architecture 用 ARC；operability 用 OPS；ui_quality 用 UIQ
kind: behavior
preconditions: <前置状态>        # 六元组字段仅 behavior 类必填
action: <业务动作>
expected: <可观察结果>
forbidden: <禁止发生>
required_verifiers:              # 列表默认 all_of
  - type: test
    id: TEST-<域>-<序号>         # 冻结 planned ID，不冻结文件路径
  - type: evidence
    id: EVIDENCE-<域>-<序号>
  - type: human_approval
    rubric: <rubric-id>          # UI 审美 = evidence 且 human_approval（all_of），不是任选
```

`any_of` 仅用于真正可替代的证明方式，例如同一 API 契约要求：`any_of: [contract_test, umbrella_e2e 内含该契约断言]`。**禁止**把 evidence 与 human_approval 放进 any_of。

非 behavior 类示例：

```yaml
id: ARC-STATE-001
kind: architecture
requirement: 每次异步回写必须校验 revision
required_verifiers:
  - { type: static_rule, id: RULE-STATE-001 }
  - { type: test, id: TEST-STATE-009 }
```

### 5.2 verification-plan

```yaml
- id: TEST-DB-001
  type: real_db_test
  runner_profile: mysql-integration    # 来自受保护 policy.yaml，Worker 不得自选
  command_id: pytest-real-db
  report_slot: db-tests
  environment: { mysql: required }
  mock_policy: boundary_forbidden      # 执行强度诚实申报：warn 级 static_rule 扫 mock 导入 + 设计期人审；非硬 gate
  expected_shards: [db-tests]          # 分片清单 fail-closed
  expected_instances: all              # 高危模块 fail-closed 条目可写显式计数
```

### 5.3 authorization-record（业务仓保护路径，人审合入 main 后生效）

```yaml
task_id: FEATURE-001
design_ref:
  repository: <business-repo>
  commit: <full-sha>
  path: docs/designs/feature-001/
  digest: <sha256>
gate_ref:
  repository: <central-governance-repo>
  commit: <full-sha>
allowed_repositories: [prodream-next, prodream_backend]
implementation_plan_digest: <sha256>  # 计划基线锁定；换计划=新 digest+新 record，实施 PR 不得改文件（§4.3）
required_profiles: [fast, integration]
lead_repository: prodream_backend     # 跨仓任务必填（D18）
```

### 5.4 delivery-request（Worker 可写，只能复述不能决定）

字段：`task_id`、复述的 `design_ref`/`gate_ref`、`task_type: bugfix | feature | refactor`、实现 commit、**清单外分支申报（boolean + 说明）**、**结构化 DEV records（D19，不允许自由文本单独成条）**、已知剩余风险。与 authorization 任何不一致即 fail。

**DEV record schema**：

```yaml
id: DEV-001
plan_step_ids: [STEP-003]        # 偏离自哪些计划步骤（必填）
category: file_split | reorder | approach_change | extra_file
actual_files: [src/domain/order/transition.ts]
affected_requirements: [ARC-STATE-001]
reason: 原计划文件已同时承担 UI 状态，拆分后才能保持单一写入者   # 必填
verification_impact: none | tests_updated | needs_review
```

**按 category 条件校验**（ACC-IPL-004）：`file_split` / `extra_file` → `actual_files` 非空；`approach_change` → 列出实际涉及文件；`reorder` → 允许 `actual_files: []`（不迫使 Worker 填假数据），但 `plan_step_ids` 与 `reason` 必填。`verification_impact: needs_review` 时最终治理状态**不得自动 pass，强制进入 Proof Gate 人工待审**。

### 5.5 ci-attestation（仅 CI 同 run 生成）

字段：实际 checkout 各仓 SHA、实际 gate_ref、各 verifier 结果（含 attempts——重试通过必须留痕）、各 report slot 实际产出与运行 profile、coverage/effectiveness 数值、evidence artifact digest、runner 与工具版本、时间、最终状态。**仓库中预置的 attestation / 历史报告不得被识别为当前 run 结果**（威胁模型内的防伪边界，见 D17）。

### 5.6 exception（与 human-approval 分立）

exception = 批准一次违反普通 policy 的特殊改动，必须绑定：`repository`、base/head SHA 或 diff digest、违反的 policy rule、精确路径、理由、有效期、批准记录、撤销状态。缺绑定即可跨任务重放，故全部必填。
human-approval = 证明 UI/baseline/产品判断已获批：`rubric-id`、对象 digest（如 baseline 图 hash）、批准人、时间。

## 6. governance CLI 规格

入口：`governance verify --mode local|ci [--profile fast|integration] [--report-dir …]`。

**结论三态：`pass / fail / unverifiable`**。local 模式下平台依赖项（required check 配置、reviewer 身份、CI token 权限、真实 attestation）报 unverifiable；**ci 模式下 unverifiable 一律不折算 pass（fail-closed）**。只承诺"相同确定性输入的纯检查两模式同结论"。

| 子检查 | 职责 | fail-closed 规则 |
|---|---|---|
| `schema` | 校验全部 schema 实例合法；**实施方案引用完整性与结构闭合八条**（§4.3：change/verify 全类型 verifier 认领闭合、completion 按 verifier 类型校验、ID 真实存在、禁通配/占位、targets 粒度（精确文件或 module_id 绑定前缀，通用根非法）、依赖无环）；DEV record 按 category 条件校验；derived_paths 配置合法性（保护路径/源码根/baseline 配置为 derived 即 fail） | 非法/断链/占位/缺字段/非法 target/非法 derived 配置即 fail |
| `authorization` | delivery request ↔ authorization record 一致；record 已在受保护 main 历史中（非本 PR 引入） | 缺 record / 不一致 / 本 PR 自带 record 即 fail |
| `frozen` | 从 authorization 的 SHA+path 读设计并核对 digest（design_ref.digest + implementation_plan_digest 双核对）；实施 diff 未触碰硬冻结层（含 modules.yaml）、**implementation-plan.yaml/.md** 与治理路径；gate_ref 未被顺带变更 | diff base 不可达即 fail；任一 digest 不符即 fail；触碰计划文件即 fail |
| `acceptance` | requirements manifest（全 kind）↔ 各 report slot（pytest junit / vitest json / Playwright json）↔ evidence digest ↔ approvals 对账 | 任一 required verifier 缺产物即 fail；报告缺失/早退/分片丢失即 fail；参数化按 §3 规则 |
| `plan` | verification-plan 核对：每个 verifier 的报告来自声明的 slot，slot 运行于声明的 profile；expected_shards 齐全。**diff↔targets 对账**：实际修改文件映射到 step targets / DEV record / derived_paths 因果规则（含触发源已覆盖、lockfile 孤立变化走 DEV、generated 绑 producer_command_id、snapshot 必须被认领）；`needs_review` 存在时最终状态置人工待审 | slot/profile 不符或分片缺失即 fail；三者皆无的文件即 fail；derived 文件缺触发源/producer 即 fail |
| `coverage` | patch line coverage ≥90%（diff-cover）；纯决策模块 branch 100%；存量基线不倒退 | 报告缺失即 fail，不是空过 |
| `effectiveness` | 按 task_type：bugfix 红绿机器化（checkout base 跑指定测试期望 fail，head 期望 pass）；refactor 前后同套测试通过（before_after） | bugfix 无 regression_red 结果即 fail |
| `policy` | policy diff classifier | 保护路径触碰 = fail（除非有效 exception）；启发式 = 首期 warn |

**policy diff classifier 分级**：
- **fail 级**：CI workflow、gate 配置（coverage/mutation 阈值与 exclude）、test runner 配置、硬冻结设计文件、`.governance/`、screenshot baseline、gate_ref；
- **warn 级（M1 fixtures 校准后逐步升级）**：新增 `pragma: no cover`/`skip`/`xfail`/`.only`、删测试文件、改测试命令、缩小 discovery、新增 `|| true` 吞错、更换 diff base、real_db/contract slot 绑定测试中新增 mock 导入。

**输出**：机器读 JSON + 人类读 summary（缺什么 ID、来自哪份报告、本地复现命令）。

## 7. Trust chain 与平台探针

```
人类账号（唯一持有分支保护/CODEOWNERS 修改权；Worker 会话与 CI token 无 admin scope）
  → 业务仓受保护 main + 保护路径改动必经人审（第一道防线，平台层）
    → 设计包 PR 人审合入 → authorization record 人审合入
      → PR 触发 adapter workflow（GitHub 注意：pull_request 运行的是 PR head 副本，
         所以 workflow 的防篡改只能靠平台人审，classifier 只是第二道防线）
        → 按 gate_ref 拉取 pinned governance CLI
          → verify --mode ci（§6 八个子检查）
            → attestation 同 run 生成 → required check 决定可否合并
```

**GitHub 探针（M0，新增）**：① PR 内修改 workflow 后运行的是哪个版本（确认 PR head 生效问题的边界）；② required check 能否绑定来源 App/workflow（rulesets）；③ CODEOWNERS 对 `.github/workflows/`、`.governance/`、`docs/designs/` 的强制人审是否无旁路。

**Gitea 1.26.4 探针（M0，原五项 + 新四项）**：
1. required status check：workflow 被删/改名时是否阻止合并；
2. check 名称由分支保护持有时，改 job name 的后果；
3. Worker token 无 admin scope 时能否触碰分支保护；
4. Gitea runner 拉取 GitHub 中央仓（public / private+只读凭据）可行性，且项目代码步骤读不到凭据；
5. required reviewer / approval 的身份强度；
6. **修改 workflow 内容但保留 check 名，能否骗过 required check**；
7. **替换 gate_ref 后是否被发现**；
8. **另一个 job 伪造同名 check 的后果**；
9. **保护文件模式（protected file patterns）能否覆盖 `.governance/` 与 `docs/designs/`，对 PR 合并是否生效**。

**uv 分发 POC（M0，新增五项）**：准确安装命令（`#subdirectory=cli` vs checkout+`uv run --project`）；uv.lock 是否真实生效；uv 自身版本 pin；无缓存 runner 依赖复现；GitHub/Gitea runner 均可执行。

## 8. 实施阶段与完成判据（按 Codex v2 重排）

| 阶段 | 内容 | 完成判据（验证者） |
|---|---|---|
| M0 | 建 public GitHub 中央工具仓（无 specs/exceptions）+ 迁方法论 + 本设计包按 4.2 布局入仓；定业务仓设计目录与 authorization 机制；GitHub/Gitea 信任根探针（§7 全部项）；D8 diff-cover TSX POC；uv 分发 POC；选一个真实业务仓人工走完整三层设计→授权→实施→证明流程 | 真实任务交付含完整证明包（human_approval）；三类 POC/探针书面结论落档（evidence） |
| M1 | 确定性 CLI 全量：schema / authorization / frozen / acceptance / plan / coverage / effectiveness / policy 八子检查 + fixtures（每 gate 四类含绕过尝试）；R12 条款生效 | 全部 fixtures 通过（test）；确定性子检查 local/ci 同结论（test） |
| M2 | 两平台真实强制：一个 GitHub 个人项目 + 一个 Gitea prodream 仓；真实验证 workflow 删除/替换/同名伪造/错误 pin 均不能合并；补四仓 coverage 欠账（FE `--coverage`、BE pytest-cov+diff-cover、data-platform 补 `@vitest/coverage-v8`、school-data 阈值、Lighthouse 去 `\|\| echo`、改 FE AGENTS.md 假"挡 merge"表述） | 两平台各真实 fail 过 required check 且绕过尝试全部失败（平台实测 evidence） |
| M3 | 扩到 prodream 四仓；umbrella integration：主仓 umbrella authorization 定 SHA 组合 → 组合启动 → 契约+E2E | 一次真实跨仓任务：错误 SHA 组合失败、正确组合通过（umbrella_e2e）；umbrella design 住业务主仓 |
| M4 | 增量 mutation 平台化（label/nightly）；截图 baseline 批准流程（baseline 变更 = 独立 human-approval 记录）；evidence retention 规则；评估 hooks 文档是否需要增强 | 注入弱测试被 mutation 拦截（test）；未批准 baseline 变更被拒（browser_test + human_approval） |

## 9. 本项目自身的验收清单（dogfood）

| ID | 验收 | required_verifiers |
|---|---|---|
| ACC-REPO-001 | 中央仓 main 受保护，实施 token 无 admin scope，直接 push main 被拒 | 平台实测 evidence |
| ACC-REPO-002 | 中央仓不含任何项目实例数据（specs/exceptions/approvals/delivery）；结构审查通过 | human_approval |
| ACC-SCHEMA-001 | 非法 manifest（缺 verifier / 嵌套 any_of / 错 ID 格式 / evidence+human_approval 进 any_of）被 `schema` 拒绝 | test |
| ACC-AUTH-001 | delivery request 声明的 design_ref 与 authorization record 不符时 fail | test |
| ACC-AUTH-002 | authorization record 由本 PR 自带（未在 main 历史）时 fail | test |
| ACC-ACC-001 | required verifier 缺产物时 fail 并输出缺失 ID + 来源报告 + 复现命令 | test |
| ACC-ACC-002 | 报告缺失/早退/丢分片时 fail-closed，不是空过 | test |
| ACC-ACC-003 | Playwright 重试后通过在 attestation 留 attempts 痕迹 | test |
| ACC-ACC-004 | 高危条目显式实例计数不足时 fail；`instances: all` 条目任一收集实例失败即 fail | test |
| ACC-PLAN-001 | verifier 报告来自未声明的 slot / slot 运行于错误 profile 时 fail | test |
| ACC-IPL-001 | 引用完整性与结构闭合：requirements、steps、TEST/verifier、command ID 引用闭合；存在未认领或不存在的 ID、通配/占位表达时 fail | test |
| ACC-IPL-002 | 实施 diff 修改 implementation-plan.yaml 或 implementation-plan.md 任一文件均 `frozen` fail；换计划必须走新 digest + 新 authorization | test |
| ACC-IPL-003 | 实际修改文件不属于任何计划 step targets、无对应结构化 DEV、也不命中 derived_paths 因果规则时 fail | test |
| ACC-IPL-004 | DEV record 缺 plan_step_ids / actual_files / affected_requirements / reason / verification_impact 任一字段时 `schema` fail | test |
| ACC-IPL-005 | 实施步骤 completion 引用不存在的 command_id/scene/rubric，或试图在计划内覆盖 verification-plan 命令定义时 fail | test |
| ACC-IPL-006 | derived 文件缺已认领触发源或 producer command 时 fail；保护路径/源码根/baseline 被配置为 derived 时 `schema` fail | test |
| ACC-IPL-007 | 目录前缀 target 无 module_id 绑定、前缀越出模块边界、或命中非法通用根名单时 fail | test |
| ACC-IPL-008 | 存在 `verification_impact: needs_review` 的 DEV 时，最终治理状态不自动 pass，进入人工待审 | test |
| ACC-TPL-001 | 真实任务完成三层实例化，人工 rubric 确认：步骤具体、文件目标明确、完成判据可观察、无"大而全步骤"空壳认领全部 requirement | evidence + human_approval |
| ACC-FRZ-001 | 实施 diff 修改硬冻结集合任一文件（business-design、architecture-design、modules、requirements、verification-plan、evidence-scenes、rollout）时 fail | test |
| ACC-FRZ-002 | diff base 不可达时 fail 而非空 diff | test |
| ACC-FRZ-003 | design digest 与 authorization 声明不符时 fail | test |
| ACC-COV-001 | patch coverage <90% / 决策模块 branch <100% / 基线倒退 / 报告缺失，各自 fail | test |
| ACC-EFF-001 | bugfix 任务无 base-fail+head-pass 结果时 fail | test |
| ACC-POL-001 | 触碰保护路径且无有效 exception 时 fail | test |
| ACC-POL-002 | 每个 warn 级启发式各有四类 fixture 且分类正确 | test |
| ACC-POL-003 | 有效 exception（人审合入、绑定本 diff、未过期未撤销）放行；过期/错 diff/被撤销的 exception 不放行 | test |
| ACC-ATT-001 | 仓库中预置的 attestation 与历史报告不会被误识别为当前 run 的结果 | test |
| ACC-POC-001 | D8 POC 结论落档：TSX 行号映射对齐验证通过，或记录失败与自研决策 | evidence |
| ACC-POC-002 | uv 分发 POC 五项结论落档，选定真实吃到 lock 的分发方式 | evidence |
| ACC-PROBE-001 | GitHub 三项 + Gitea 九项探针各有书面结论与截图/日志 | evidence |
| ACC-CLI-001 | 确定性子检查 local 与 ci 模式同输入同结论；平台依赖项 local 报 unverifiable 且 ci 模式不折算 pass | test |
| ACC-E2E-001 | M2 判据：两平台真实 fail 一次 + workflow 删除/替换/同名伪造/错误 pin 均不能合并 | 平台实测 evidence |
| ACC-E2E-002 | M3 判据：跨仓错误 SHA 组合失败、正确组合通过 | umbrella_e2e |
| ACC-DOC-001 | hooks-install.md 按文档装配后，Claude Code deny 实际拦下对保护路径的编辑 | evidence |

## 10. 实施 Worker 约束（goal 模板实例）

```text
Outcome: 实现 design_ref={repository, commit, path, digest} 的 M<N> 阶段全部要求。
Constraints:
  不得修改硬冻结层（业务/架构设计、requirements、verification-plan、evidence-scenes）、
  implementation-plan.yaml/.md 文件本身、schemas、fixtures 语义、CI workflow、.governance/、
  coverage/mutation 配置；
  执行时允许偏离计划路线，但每处偏离必须以结构化 DEV record 写入 delivery request
  （plan_step_ids / category / actual_files / affected_requirements / reason / verification_impact）；
  需要重写计划：暂停回流，走新计划版本 + 新 authorization，不得在实施 PR 中改；
  遇设计外分支：暂停，写入申报栏，回流主持人，不得自行补默认值；
  未经有效 exception 不得新增 skip/xfail/.only/no cover、删测试、放宽阈值。
Verification:
  §9 中本阶段涉及的条目全部通过，required_verifiers 对账无缺；
  交付含 delivery request（声明）；attestation 由 CI 生成；
  交付说明包含：改了什么、证据、剩余风险。
```

## 11. 明确不在范围（本期不做，勿顺手建设）

恶意任意代码执行的隔离与报告防伪（D17）、外部 status publisher、hooks 自动分发、delivery 产物签名、双托管镜像、独立 reusable workflows 体系、mutation 全栈默认开启、截图 baseline 平台化（M4 前）、每仓文件数指标、中央仓托管任何项目实例。

## 12. 残余风险（诚实申报）

- CI 只证明产物存在且按声明环境执行，不证明断言语义正确——设计期审 oracle + R12 mutation + 真实 E2E 共同增强，不能证明；
- 威胁模型限定（D17）：能任意执行代码的恶意 Worker 可在 run 内伪造报告，本期不设防；
- `mock_policy` 只有 warn 级启发式 + 设计期人审，不是硬 gate；
- warn 级启发式校准期存在漏报窗口；
- Gitea 强制力以探针为准；若关键项不支持，该平台降级为"审计留痕 + 人工 Proof Gate"（D16，需主持人知情接受）；
- 实施方案的语义质量与 DEV 偏离的合理性由设计期人审 rubric + Proof Gate 人工审负责，机器只核引用闭合与 diff 对账（D19）；
- 一、二层 Markdown 与 requirements.yaml 的语义一致性归人审，机器只校验 ID 集合一致；
- evidence 体积与 retention 在 M4 前从简（保留最近 N 次）。
