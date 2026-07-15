# GOV-BOOTSTRAP-M0 架构设计（第二层，硬冻结）

> task_id: GOV-BOOTSTRAP-M0。系统整体架构真源是 `design-package-v1.1.md`（§1 五条裁决、§4 两层 repo 结构、§6 CLI 规格、§7 trust chain）；本文件不复述，只补 M0 实施所需的模块边界、契约与 ARC/OPS 要求。

## 1. 模块边界声明（机器投影：modules.yaml）

| module_id | 边界前缀 | M0 内容 |
|---|---|---|
| MODULE-GOV-METHODOLOGY | `methodology/` | AI_DELIVERY_METHODOLOGY.md 迁入（真源，本地降为 checkout/symlink） |
| MODULE-GOV-SCHEMAS | `schemas/` | 八个 schema 草案（requirements-manifest / verification-plan / authorization-record / evidence-scenes / delivery-request / ci-attestation / exception / human-approval），JSON Schema 格式 |
| MODULE-GOV-CLI | `cli/` | M0 仅占位骨架（pyproject + 空入口，供 uv 分发 POC 用）；实现在 M1 |
| MODULE-GOV-ADAPTERS | `adapters/` | M0 仅骨架注释版；正式形态待探针结论（M2） |
| MODULE-GOV-TEMPLATES | `templates/` | design-package 三层骨架（含全部 yaml 骨架）、debate.md、goal-prompt.md |
| MODULE-GOV-FIXTURES | `fixtures/` | M0 仅建目录与 README（四类 fixture 约定）；填充在 M1 |
| MODULE-GOV-DOCS | `docs/` | hooks-install.md + `docs/designs/governance-bootstrap/`（本任务治理实例，保护路径） |
| MODULE-GOV-GOVERNANCE | `.governance/` | policy.yaml + authorizations/（bootstrap 自身实例，保护路径） |
| MODULE-GOV-CI | `.github/` | CODEOWNERS + 最小 CI（M0 只跑 schema 自校验脚本占位；正式 verify workflow 在 M2） |

探针与 POC 在**独立探针仓/样例仓**执行（不在中央仓内），结论以 evidence 文档落到 `docs/designs/governance-bootstrap/evidence/`。

## 2. 契约

- **schema 家族即系统契约**：字段规格以设计包 §5 为准；M0 草案与 §5 的任何偏差必须书面申报并经主持人批准（否则 ACC-SCH-001 不过）。
- **数据模型/迁移**：不适用（本仓无数据库）。
- **数据状态流转表**：不适用，理由同 business-design §4 豁免声明。

## 3. ARC / OPS 要求（机器规范源：requirements.yaml）

| ID | kind | 要求 | verifier |
|---|---|---|---|
| ARC-GOV-001 | architecture | 中央仓只含七个白名单目录 + bootstrap 自身治理实例；不得出现任何其他项目实例数据 | human_approval（M1 起加 static_rule） |
| ARC-GOV-002 | architecture | CLI 是唯一公共接口的结构就位：adapters 骨架内除 checkout + 调用 CLI 外无治理逻辑 | human_approval（M1 起加 static_rule） |
| ARC-GOV-003 | architecture | 方法论单一真源：仓内为真源，`~/.agents/` 侧不可能出现可独立编辑的第二份 | evidence（EVIDENCE-MIG） |
| ARC-GOV-004 | architecture | schema 草案能校验 bootstrap 自身实例（自举一致性：本任务的 yaml 全部过自己的 schema） | evidence（EVIDENCE-SCH）+ human_approval |
| OPS-GOV-001 | operability | main 分支保护 + CODEOWNERS 覆盖 `.github/`、`.governance/`、`docs/designs/`；Worker 会话与 CI token 无 admin scope | evidence（EVIDENCE-REPO-PROT） |
| OPS-GOV-002 | operability | 选定的 uv 分发方式在无缓存环境复现同一依赖集（lock 真实生效） | evidence（EVIDENCE-POC-UV） |
| OPS-GOV-003 | operability | 探针结论足以让 D16/D14 的预裁决分支落地（每项探针有明确"支持/不支持"判定，无含糊结论） | evidence（EVIDENCE-PROBE-GH / GITEA）+ human_approval |

## 4. 技术选型（已在决议账本定案，此处只引用）

Python 3.12 + uv（D14，分发方式待 POC）；JSON Schema 作 schema 格式；GitHub public 单仓（D1）；平台信任根 GitHub = 分支保护 + CODEOWNERS（D16）。

## 5. rollout / rollback

见同目录 `rollout.md`。M0 无生产流量，rollback = 删仓重来，成本可忽略；唯一不可逆点是方法论真源迁移，故 EVIDENCE-MIG 要求逐字节一致核对后才删除本地原件（改 symlink）。
