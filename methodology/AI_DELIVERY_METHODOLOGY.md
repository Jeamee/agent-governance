# AI Worker 双模式交付方法论（泛化真源）

> 定稿 2026-07-15；同日补充无人值守端到端交付模式。本文档是跨项目泛化方法论，不绑定任何特定仓库；仓库现状与工具链欠账不写在这里。
> 适用对象：任何承担端到端交付的 AI coding agent（Claude Code / Codex / 其他）。
> **真源位置：`~/.agents/AI_DELIVERY_METHODOLOGY.md`（用户全局层）。** 各项目引用方式：symlink 或在项目 AGENTS.md 写指针，禁止复制成第二份维护。
> 将来独立 specs/governance repo 建立后，真源迁移过去，此处保留指针。

## 交付模式选择 Gate

凡是会修改代码、配置、文档、数据、外部系统或其他持久状态的任务，Agent 在实施前必须先问人：“这次采用三步式交付，还是简单步骤？”Agent 可以先做最小只读调查并给出推荐，但最终模式由人决定。人已在当前上下文明确说“三步式”“简单步骤”“简单修复”或同义表达时，不重复询问。

- **三步式**：执行本文后续设计收敛、Gate、冻结与 Proof Gate，适合人希望完整冻结或高风险交付的任务。
- **简单步骤**：直接执行“调查事实 → 声明证明策略 → 聚焦实施 → 自检与验证 → 交付证明”，不要求设计三件套、授权范围卡或后续 Gate。

简单步骤不降低正确性、安全性、授权和实际验证标准；出现关键歧义、不可逆风险或未获授权的范围扩张时仍须停下询问。人可以在实施过程中切换模式。本文后续 Gate 的强制要求仅适用于人选择三步式的任务。

## 第零原则

**给每一条 gate 指定一个不依赖模型自觉的发现者。** 对任何规则问同一个问题："Worker 不遵守时，谁在哪一步发现？"答不出来的规则只是愿望，不是机制。

### 三步式交付模式：无人值守端到端

用户给出明确目标与范围后，先由 Claude Code 与 Codex 围绕**业务设计、架构设计、实施方案**完成三层对抗审议。人只在这个设计收敛窗口内裁决 taste 与纯业务 D 题；Agent 自主裁决技术 D 题。三层结论收敛、全部 D 题清零后，默认形成该范围内的 **standing authorization**，并允许创建一个 Implementation Delivery Goal。

Implementation Delivery Goal 负责把 control-plane 前置 PR、其余前置工作、设计冻结、authorization、实现、验证、PR 合入、canary、rollback 准备和 Proof Gate 编排成一次无人值守端到端交付，持续推进到最终业务结果。内部阶段、PR 与 gate 是 Agent 的状态机，不是用户的人工接力清单。

**人只参与两类决定**：

1. **Taste 决定**：审美、风格、节奏、质感、品牌表达，以及机器无法替人作出的主观品质取舍；
2. **纯业务决定**：目标用户、业务规则、政策口径、优先级、商业风险承受度，以及多个合理行为分支之间的产品选择。

架构、实现路线、schema、测试、阈值、发布编排、技术风险处置、PR 创建与合入都由 Agent 自主完成。技术问题不得包装成 D 题上抛给用户；Agent 应基于事实、最小风险原则和可验证证据自行裁决并记录理由。

未决 taste / 纯业务决定只允许出现在 Implementation Delivery Goal 创建之前的三层设计收敛阶段。外部权限、凭据、自动合入身份与不可逆操作授权也必须在开 Goal 前完成 preflight。**Goal 一旦创建，不再设置任何现场人工决策点、人工 verifier 或等待点击的交接步骤。** 普通测试失败、代码冲突、CI 修复或技术选型始终由 Agent 自行处理，不得变成用户待办。

若实施中实际发现仍需新的 taste / 纯业务决定，说明入口条件和设计冻结失真；这属于交付不变量被破坏，不是实施阶段的正常 D 题。Agent 不得伪造决定或补业务默认值，应 fail-closed、保全证据并将当前 Goal 标为设计失效。该异常边界不能被用来预设常规人工检查点。

主 gate 是三个问题，覆盖率只是告警器：

1. 需求是否被测试表达（行为清单 100% 对应到测试）；
2. 测试是否真的能拦住错误（按任务类型证明有效性）；
3. 真实系统是否端到端走通（契约测试 + 真实 E2E）。

拒绝"全仓 100% 行覆盖率"这类目标：行覆盖率是最容易被 Agent 刷的指标（执行过 ≠ 断言过），给 AI 定指标比给人更危险——Agent 会精确优化指标本身（Goodhart）。

---

## 一、测试交付标准（五个 Gate）

### Gate 1 — 行为验收清单（可追溯、编码前冻结）

每条验收是六元组：

| 验收 ID | 前置状态 | 业务动作 | 可观察结果 | 禁止发生 | 对应测试 |
|---|---|---|---|---|---|

- 清单在编码前由 Agent 根据已确认业务事实冻结；所有 taste / 纯业务分支必须在 Implementation Delivery Goal 创建前由人裁决并写入设计包。Worker 不得静默删除或缩小范围；冻结后修改必然留痕（清单文件进版本控制，交付 diff 动它即现形）。
- **已确认场景的测试对应率要求 100%——这是唯一合理的"100%"。**
- 清单内容按**风险类型**派生，不机械套用单一场景集：
  - 状态流：失败 / 取消 / 重试 / 迟到 / 乱序 / 重复事件；
  - 计算逻辑：等价类 / 边界值 / 不变量 / 非法输入；
  - 权限：未登录 / 无权限 / 越权 / 资源归属；
  - 数据层：事务回滚 / 约束 / 幂等 / 并发写 / 迁移前后兼容；
  - API：状态码 / 错误结构 / 空值 / 枚举 / 鉴权 / 幂等；
  - UI：真实操作 / 加载空错态 / 刷新重进；
  - LLM 功能：固定评测集 + 质量阈值，**不用代码覆盖率衡量**。

### Gate 2 — 覆盖率（四个精确指标，不混为一谈）

1. 新增/修改可执行行：**patch line coverage ≥90%**（diff-cover 类工具测的是变更行覆盖，不是变更分支覆盖，不要混称）；
2. 新增业务决策：每个分支走向必须有显式行为测试（设计期审议判定，覆盖率工具测不了）；
3. 纯决策模块（reducer、transition table、权限/计费规则）：**branch coverage = 100%**；
4. 存量全仓覆盖率：只做基线防倒退，不要求一次补齐。

### Gate 3 — 二维矩阵定证明位置

横轴：行为风险类型；纵轴：执行环境（FE / API / Worker / DB / 外部服务）。技术层（BE/FE/data）不做一级分类，只做执行环境与责任边界。数据层特有风险（约束、事务、迁移、回填、并发写）必须在真实 DB 环境证明，不许用 mock 单测顶替。跨仓契约必须有两边共享的契约测试。

### Gate 4 — 测试有效性证明（按任务类型）

- **Bug fix**：回归测试必须在旧代码上失败、修复后通过（强制，交付物附旧代码失败输出）；
- **新 feature**：先红后绿可要求但证明力有限，重点靠 Gate 1 的"禁止发生"断言；
- **重构**：同一测试集修改前后均通过；
- **核心纯逻辑**：mutation testing 增量抽查（存活突变超阈值即 fail）。

**mutation 的适用边界必须诚实**：它只证明"测试对工具能生成的局部代码变异敏感"，不证明功能没漏实现、不证明符合架构设计、不证明链路整体正确、不证明测试没过度绑定实现细节。定位：权限/计费/状态 reducer/纯计算做 PR 级硬 gate；普通业务逻辑按风险触发；UI/DB 集成/外部服务/LLM 不强行依赖。mutation 之外继续用 fail-before-fix、property-based、状态机/不变量、契约、真实 E2E。

### Gate 5 — 反作弊禁令

未经有效 exception authorization，Worker 不得：降低覆盖率阈值、扩大 coverage exclude、新增 `pragma: no cover` / coverage ignore / `skip` / `xfail` / `.only`、删除已有测试变绿、mock 掉本次任务要证明的边界、把 E2E 重试后通过当稳定通过。这些操作不绝对禁止，但必须形成绑定具体 diff、有效期和验证影响的结构化例外。技术性例外由 Agent 依据冻结 rubric、独立证据与 fail-closed 原则裁决；implementation 阶段不得自批，必须由顶层 Goal 自动退回 control-plane 阶段生成、验证、冻结 exception 并更新 authorization 后才能继续。会改变业务验收或引入新 taste 选择的例外不属于当前 Goal 的授权范围；它意味着设计入口失效，不能在实施中临时找人补批。**发现者：CI diff 扫描脚本（必备），过程内 hook 只是提前预警。**

---

## 二、UI/UX Gate（Gate 3 中 FE 行的展开，五层）

UI/UX 没有"覆盖率 100%"这回事。自动化负责证明"行为正确、动效可靠、画面未退化、无障碍降级有效"；人只在三层设计收敛阶段决定并批准设计目标、节奏、质感、品牌表达等 taste，不在实施后现场验收。设计参考、rubric 与验收场景必须在 Implementation Delivery Goal 创建前充分具体并完成批准；否则 Goal 不具备入口条件。

1. **交互语义硬 gate**：鼠标 / 键盘 / 触屏 / 焦点 / ARIA / disabled / loading / 防重复提交 / 错误恢复。断言 DOM 语义状态（`data-state` / aria / 可见性），**禁止断言像素或动画中间帧**（必 flaky）。
2. **动效工程硬 gate**——审美不能自动判断，但工程质量可以测：按下立即反馈（不等 click 完成）；快速重复触发不跳帧不重启；动画中可被 ESC / 反向操作打断并正确反转；动画期间不锁死输入；弹层空间来源与退出路径一致；拖拽跟随指针且落点正确；reduced-motion 下移除位移/缩放/弹簧/视差但保留必要反馈；touch 不残留伪 hover；动画结束后焦点、滚动锁、DOM 状态归位。**边界：自动化不判断"缓动是否优雅"，判断它是否及时、连续、可打断、可访问、空间一致、不破坏交互。**
3. **视觉回归 gate**：关键已批准状态的稳定截图 diff，防退化不判审美。Playwright `toHaveScreenshot()` 默认已禁动画（有限动画快进终态、无限动画回初态），无需另注 CSS；reduced-motion 是**独立验证场景**，不是截图稳定化手段。承载新 taste 选择的参考与 baseline 必须在设计收敛阶段经人批准才有资格当 gate；从既有已批准设计机械派生的 baseline 可由 Agent 自动生成、核对和冻结，不要求人重复点击。截图环境固定（浏览器/OS/viewport/DPR/locale/字体/数据/mask 范围）；优先组件/区域截图，全页只给少量关键流程。
4. **性能信号**：输入延迟、长任务、掉帧、布局抖动（CLS）；高风险动效做专项基线，不假装等于"顺滑度评分"。
5. **品质证据 gate**：证据场景表编码前冻结，防 Worker 自选证据：

| 证据 ID | viewport | locale | 输入方式 | 起始状态 | 操作脚本 | 必须展示 |
|---|---|---|---|---|---|---|

录屏由固定 Playwright 场景生成；附正常速度录像、必要时慢速/逐帧、before/after 并排、commit + 命令 + 浏览器版本、手势类交互的真实触屏证据。taste rubric 及其目标值在设计收敛阶段由人批准，实施阶段只按冻结参考生成证据并运行 gate，不产生新的 taste 决定；纯工程结论由自动化 gate 判定。

---

## 三、协作流程：无人值守编排 + 设计期对抗审议 + 独立实施 + Proof Gate

> 取消通用的实施后同行代码审查，**不取消独立验证**。人的决策窗口止于 Claude Code × Codex 三层方案对抗审议完成之时；Implementation Delivery Goal 创建后默认无人值守推进。实施阶段独立执行；不可在实施阶段修改的 CI、契约、mutation、真实 E2E 和证据系统负责验收。

### 顶层 Delivery Goal 与 standing authorization

Implementation Delivery Goal 可以在设计文件尚未合入和正式冻结时启动，但前提是业务设计、架构设计、实施方案已经完成对抗审议，所有技术、taste 与纯业务 D 题均已清零，所需人工决定已有可校验记录。它描述最终业务结果，而不是要求用户逐段启动前置 PR goal、冻结 goal、authorization goal 和 implementation goal。Agent 在同一个交付目标内自动完成：

1. 校验三层方案、D 题清零记录、人工决定与外部权限 preflight；
2. 起草、验证并按依赖顺序合入 control-plane PR；
3. 自动完成其余前置工作并留存可复现证据；
4. 冻结三层设计包、计算 digest、生成并合入 authorization；
5. 自动进入 implementation 阶段，完成实现、验证、canary 与修复循环；
6. required gates 全绿后自动合入交付 PR；
7. 执行 Proof Gate、准备 rollback，并交付最终证明报告。

设计冻结、authorization 生效和 required checks 仍是不可跳过的内部状态转换，但默认不要求用户同步触发、转发、批准或点击 merge。若平台要求独立 reviewer，应预先配置受控的自动化 reviewer / merge 身份；缺少该身份是外部权限阻塞，不得通过临时降低保护规则解决。

standing authorization 只覆盖用户明确置于范围内的仓库、系统和业务目标。它允许 Agent 在既有保护规则内创建及合入 PR、生成治理记录并执行可逆技术操作；不自动授权扩大业务范围、改变业务口径、作 taste 选择、弱化 gate、提升权限或执行未声明的不可逆外部操作。

### 审批真实性

standing authorization 是对执行过程的预授权，不等于人逐项看过未来产物。只有人实际作出的 taste / 纯业务判断才能记录为 `human_approval`；Agent 的技术裁决应记录为 `technical_approval`、对抗审议结论或机器 evidence，不得伪造人工审核。所有必需的 `human_approval` 必须在 Implementation Delivery Goal 创建前完成，并作为不可变设计输入由 Goal 校验 digest；实施与 Proof Gate 不得现场等待新的人工审核。若现有 schema 尚无对应载体，应先补充真实表达能力，不能借用 `human_approval` 冒充。

### 三层设计收敛阶段（Claude Code × Codex 对抗审议，人只处理 taste / 纯业务 D 题）

对抗审议默认由编排 Agent 自主推进，依次覆盖业务设计、架构设计、实施方案三层。编排方负责隔离首轮观点、保真转发、维护 running 决议账本、识别伪收敛并验证全部 D 题清零。用户不是 Agent 之间的消息总线，也不负责决定何时触发下一轮；只在这个阶段裁决 Agent 无权替代的 taste 与纯业务选择。

1. **先独立后互审（避免锚定）**：先分别拿到两方的独立第一版——Agent A（产品/前端强项）出业务、用户流程、UI/UX、异常路径；Agent B（架构/后端强项）出架构、数据、状态、并发、测试 oracle、可实施性盲区清单——再开始交叉转发；
2. **每轮回复必须是结构化分歧清单**，不许散文：同意什么 / 反对什么 + 理由 / 新增 D 题 / 撤回的旧立场。方便自动编排、审计与收敛判断；
3. **转发保真**：优先文件中转（双方读写同一个 debate 文件），由编排 Agent 传递原文并校验账本，避免摘要转述引入失真；
4. **指定一方维护 running 决议账本**（接受 / 拒绝 / D 题 / 理由），每轮更新，防止论证蒸发在对话里；
5. **收敛信号**：连续一轮无新增实质分歧。技术 D 题由 Agent 依据事实、POC 与验证者自主裁决；taste / 纯业务 D 题必须由人裁决。全部 D 题清零并形成可校验记录后，才能创建 Implementation Delivery Goal。

互审的退出 rubric 由编排 Agent 逐项核对：Known/Unknown 四格是否闭合、状态流转表反向路径是否完备、**每条验收是否机器可自动断言**（taste / 纯业务判断除外）、每条要求是否标注了验证者。

待冻结设计包至少包含：业务流程与状态表、架构与跨仓契约、实施方案、acceptance manifest、UI evidence scenes、架构约束、rollout/rollback/observability、设计版本 hash。**每一项必须标注验证者**（CI / E2E / mutation / static rule / runtime evidence）或引用已完成的冻结人工决定。Implementation Goal 内不得存在 pending human verifier；没有自动验证者或既有冻结决定的设计要求就是未覆盖项。

### 实施阶段（单 Agent 长任务，如 Codex `/goal`）

Implementation Delivery Goal 的入口 gate 必须先证明：三层方案已收敛、D 题为零、全部人工决定已记录、control-plane 合入权限与自动 merge 身份可用、外部凭据可用。设计文件可以尚未正式冻结，因为冻结本身属于 Goal 内部步骤；语义决定不得尚未完成。

实施子阶段不复制整份设计，指向顶层 Goal 自动产出的不可变版本；不要求用户重新发起第二个 goal：

```text
Outcome: 实现 design_ref=<不可变版本> 的全部要求，完成所有涉及仓库的独立提交。
Constraints: 不得修改冻结设计、gate、coverage、mutation、CI 和 baseline；
  设计外技术分支由顶层 Goal 自动回流 control-plane、重新冻结并更新 authorization；
  不得自行补业务默认值，不得创建现场人工决策点。
Verification: 所有 required acceptance IDs 已执行并通过；
  patch coverage、指定 mutation、契约、跨仓 E2E、UI evidence 全部通过；
  各仓 commit 与设计版本形成 delivery manifest。
```

交付对照表必须含强制申报栏："本次实施是否遇到清单外分支"。

实施、修复、重跑验证、技术性 control-plane 回流与普通 PR 合入持续自动执行。Implementation Delivery Goal 中不存在“等人判断 taste / 业务”“等人审证明包”或“等人点击 merge”的正常状态；普通 CI 失败、merge conflict、测试不稳定和可修复环境问题全部由 Agent 自行处理。

### 验收阶段（Proof Gate，审证明包不逐行审代码）

Proof Gate 由 Agent 自动执行并在全部 required verifiers 闭合后完成合入与交付。taste / 纯业务决定在这里是已冻结、可校验 digest 的输入，不是等待中的 verifier；manifest 若仍含 pending human verifier，入口检查就必须拒绝创建 Implementation Delivery Goal。不得把证明包审核重新变成用户的同步工作。

- design hash 未变化；
- architecture IDs 全部有验证结果；acceptance IDs 全部执行并通过；
- bugfix 附旧代码失败、新代码通过证据；
- coverage / mutation / contract / E2E 全绿；
- 跨仓按指定 SHA 组合真实运行（umbrella integration，防"每一半都对、组合不工作"）；
- UI evidence 场景齐全；
- 无新增 skip / ignore / gate 弱化；
- staging / canary / rollback 条件满足。

### 验收 ID 对账（稳定 ID，不用脆弱的行号映射）

```text
ACC-<域>-<序号>  ↔  TEST-<域>-<序号>  ↔  EVIDENCE-<域>-<序号>
```

测试名称或 marker 携带验收 ID；CI 三方对账：冻结 manifest 的 required IDs ↔ 测试报告中 executed+passed IDs ↔ 证据包 evidence IDs。**CI 只能证明"存在且执行"，不能证明"断言语义正确"**——语义正确性由设计期双 Agent 审 oracle + 红绿证明 + mutation + 不变量 + 真实 E2E 共同增强，不宣称完全机器证明。

---

## 四、四层执行机制与工具能力差异

| 层 | 机制 | 执行力 |
|---|---|---|
| 0 | 规则文本（AGENTS.md 单一真源，双工具共享） | 告知，不保证 |
| 1 | 任务级流程产物（acceptance manifest / evidence scenes，冻结进版本控制） | 违规必留痕 |
| 2 | 过程内 hooks（预警 / turn 内自纠） | 提前发现，非硬拦 |
| 3 | CI 硬 gate（agent 无关） | 最终强制层 |

工具差异（以当前版本为准，过时即更新）：

| 能力 | Claude Code | Codex |
|---|---|---|
| 编辑前检查 | PreToolUse | PreToolUse |
| 编辑前硬拒绝 | 可 deny 阻止调用 | 仅告警，不阻止 |
| 编辑后校验/停止 | PostToolUse / Stop | PostToolUse / Stop |
| 真正不可绕过 | managed policy / CI | managed requirements / 权限边界 / CI |

推论：**凡必须硬执行的规则不能停在层 2，必须下沉到层 3**——CI 是所有工具唯一共享的强制层。

---

## 五、治理前提（四条，未成立前只算"减少 review"，不能说"机制替代 review"）

1. **冻结设计真源在 implementation 阶段写权限之外**；
2. **gate 本身在 implementation 阶段写权限之外**——CI workflow、gate 脚本、coverage/mutation 配置、acceptance schema、screenshot baseline、test runner 配置、设计冻结引用，全部保护；手段：独立 governance repo / 外部 reusable workflow 固定版本 / protected path + CODEOWNERS / 仓库外配置的 required status check；
3. **跨仓组合验证存在**（umbrella integration：设计版本 → 各仓指定 SHA → 契约 + E2E + evidence）；
4. **每条业务与架构要求都有明确验证者**。

**为什么 implementation 阶段不能有 gate 写权限**：不是能力问题，是审计独立性的结构要求——被验收阶段不能同时改写验收规则。Agent 冲验收时（不需要恶意，"让 CI 变绿"的目标函数使然）会放宽阈值、改脚本、更新 baseline；Gate 5 列的行为全部是真实风险。精确表述：**同一个顶层 Delivery Goal 可以跨越 control-plane 与 implementation 阶段，但权限必须随阶段切换。** Agent 可在设计 / control-plane 阶段起草、验证并自动合入治理内容；一旦冻结并进入 implementation，该阶段不得再修改 gate。写入冻结仓依赖受保护 PR、required checks、不可变 digest 与审计记录，不依赖用户逐个点击。推荐形态：独立 specs/governance repo 同时充当冻结真源与 gate 治理仓，各项目 CI 以固定版本引用它。

---

## 六、边界诚实条款（机器证明不了的，不假装能证明）

- 审美、节奏、质感的目标：永远由人在三层设计收敛阶段按 rubric 决定；Implementation Goal 只执行冻结目标，不冒充新的 taste 判断；
- 纯业务目标、政策口径与多个合理业务行为之间的取舍：永远由人在三层设计收敛阶段决定，实施阶段不得保留开放项；
- "测试正确但设计理解偏了"：mutation 抓不到，靠 Gate 1 清单写得足够具体来压缩；
- 断言语义与验收的对应正确性：CI 只查存在性，语义靠设计期审 oracle；
- 覆盖率、mutation 得分、截图 diff 全绿 ≠ 正确，它们是告警器不是证书。交付说明必须包含：改了什么、用什么证据证明、剩余风险是什么。
