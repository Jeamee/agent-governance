# GOV-BOOTSTRAP-M0 实施方案说明（人类可读，非规范副本——机器真源是 implementation-plan.yaml）

执行主线分三波，Worker 按 `depends_on` 拓扑即可并行：

**第一波（骨架）**：STEP-001 建仓配保护 → STEP-002/003/004/005 四路并行（迁方法论 / schema 草案 / 模板 / cli 占位 + adapters 骨架 + fixtures 目录 + hooks 文档）。

**第二波（自举入仓）**：STEP-006 把冻结设计包与本三层实例经人审 PR 合入 → STEP-007 按合入 SHA 计算两个 digest、人审合入 authorization record（bootstrap 顺序特例：授权必须在冻结内容拿到 SHA 之后才能产生，这是本任务独有的先后关系，后续任务一律先授权后实施）→ STEP-008 在独立探针仓/样例仓执行实验，结论文档落 evidence/ 目录。

**第三波（验证）**：STEP-101~108 对应各 evidence 的核验（schema 自校验有唯一可执行命令 `validate-bootstrap-instances`，解析后命令见 verification-plan.yaml——此处不复述，命令单真源）；STEP-109 真实任务人工全流程试跑；STEP-110 三项 rubric 收口，等价于 M0 的 Proof Gate。

风险步骤标注：STEP-002（方法论迁移是唯一不可逆点，先核 sha256 再动原件）；STEP-104（Gitea 九项探针可能触发 D16 降级分支——触发即按预裁决执行并书面标记，不回流重议）；STEP-105/106（POC 失败是合法结果，落档失败结论 + 建议即可，不算步骤失败）。

偏离规则照 D19：可调顺序与文件划分，结构化 DEV 申报；重写本计划 = 新版本 + 新 authorization。
