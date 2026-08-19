# 工程增强技能框架

这是一个面向 AI Agent 的工程能力增强项目。它的目标不是教 AI 写代码，而是教 AI 像高级软件工程师一样**思考**：在动手之前先判断问题、识别不确定性、选择正确的工作方式，并把思考过程变成可追踪的文档。

## 受众

| 适合 | 不适合作为主用户 |
| --- | --- |
| 研发、Tech Lead、架构：判断先验证还是先做、选型、事故止损、ADR/设计 | 纯翻译、格式化、按完整规格机械写代码的任务（本框架明确不触发） |
| 产品 / 业务分析：在不确定时写探索版 PRD、SRS，避免把想法写成已批准规格 | 期望“不问上下文直接给复杂度/架构结论”的一次性仓库扫描 |
| 实施：群聊/工单 → 现场记录（角色·模块·现象·诉求 + 验证）（走 `implementation-intake`） | 把实施现场问题默认升级成 Cynefin/架构评估 |
| 用 AI Agent 做工程协作、需要文档纪律与证据分层的人 | — |

实施主路径是 `implementation-intake`。仅当实施问题升级为先验证还是先做、技术选型、事故止损时，再走 `engineering-decision`。

## 设计哲学

### 问题：AI 不会"先想后做"

大多数 AI Agent 在收到请求后会立即执行：直接生成代码、直接写 PRD、直接给出架构方案。这在问题清晰时效率很高，但在以下情况下会造成严重错误：

- 需求模糊，AI 却假装理解然后生成一份"看起来完整"的文档；
- 问题属于探索阶段，AI 却跳过验证直接给出详细设计；
- 线上发生事故，AI 却在做需求分析；
- 用户只有一个想法，AI 却把它写成了已批准的规格。

### 解决方案：行为建模，而非提示词堆砌

本框架的核心是让 AI 在每次处理工程问题时，先完成三个判断再行动：

1. **这是什么类型的问题？** 是已知答案的执行任务，还是需要探索的未知问题？
2. **现在应该用什么行为模式？** 直接推进、专家分析、迭代探索，还是先澄清？
3. **用户需要参与到什么程度？** 自动报告结果，还是每一步都需要用户确认？

这三个判断由 `engineering-decision` 技能完成，并通过结构化契约（`document_contract`）将结论传递给下游的文档生成工作流。

## 技能拓扑

```
用户输入
    │
    ├─ 实施群聊/工单/现场口述 ──► implementation-intake
    │                                现场记录（条目四元组 + 验证 + 待确认）
    │
    └─ 研发决策/不确定怎么推进 ──► engineering-decision
                                       │  decision_brief + document_contract
                                       ▼
                                 engineering-documents
                                       按契约生成/更新/审查/基线化工程文档
```

工程链两个技能之间通过 `document_contract` 握手。实施链默认独立输出现场记录；仅在明确升级时进入工程链。

## 核心机制

### Cynefin 框架

用于判断当前问题所处的域，决定行为模式：

| 域 | 典型场景 | 行为模式 |
| --- | --- | --- |
| 清晰域（`clear`） | 需求、规则、验收标准都已明确 | 直接推进 |
| 繁杂域（`complicated`） | 需要专家比较多个技术方案 | 专家分析 |
| 复杂域（`complex`） | 用户需求、采用行为未经验证 | 迭代探索 |
| 混乱域（`chaotic`） | 线上事故、数据损失、安全事件 | 先止损 |
| 未明状态（`confused`） | 信息严重不足，无法判断 | 先澄清 |

Cynefin 域针对**当前问题**，而非整个项目。大型项目中的一个字段重命名可以是清晰域；小型项目中的未知用户需求也可以是复杂域。

### 信息分层

所有输入信息必须被分层，不允许把推断写成事实：

| 层 | 含义 |
| --- | --- |
| `facts` | 已提供或已验证的信息 |
| `goals` | 期望达成的结果 |
| `constraints` | 业务、技术、组织或合规限制 |
| `assumptions` | 暂时相信但尚未验证的判断 |
| `unknowns` | 当前不知道的信息 |
| `conflicts` | 目标或利益相关者之间的冲突 |
| `risks` | 可能的负面结果 |
| `decisions` | 有授权确认的选择 |

### 文档生命周期

文档状态必须与实际确定性一致，不能因为章节齐全就提升状态：

```
exploratory-draft → draft → proposed-baseline → approved-baseline
```

### 用户参与度（L0–L4）

| 级别 | 含义 |
| --- | --- |
| `L0` | 自动推进并报告结果 |
| `L1` | 自动推进，公开关键假设 |
| `L2` | 提供少量方案，让用户选择 |
| `L3` | 以假设、问题、证据组成短循环 |
| `L4` | 用户主导，Agent 负责整理和起草 |

高风险、不可逆、跨团队或安全相关的操作必须提高参与度，不受 Cynefin 域限制。

## 技能目录

| 技能 | 职责 | 位置 |
| --- | --- | --- |
| `implementation-intake` | 实施现场记录：群聊/工单 → 角色·模块·现象·诉求条目、验证与待确认 | `.agents/skills/implementation-intake/` |
| `engineering-decision` | 决策入口：判断问题类型、Cynefin 域、行为模式和参与度，输出 `decision_brief` | `.agents/skills/engineering-decision/` |
| `engineering-documents` | 文档工作流：根据契约生成、更新、审查或基线化工程文档 | `.agents/skills/engineering-documents/` |

## 使用方式

技能由支持 Agent Skills 规范的 Agent 自动发现和触发（Cursor 会扫描
`.agents/skills/` 与 `.cursor/skills/`）。Agent **是否调用**取决于
`SKILL.md` 的 `description` 是否匹配用户意图；发现成功不等于每次都会触发。

建议用显式斜杠命令或下面短句做触发回归。常见场景：

- **"这段群聊整理成现场记录"** / **"有啥现象和诉求"** → 触发 `implementation-intake`
- **"预约填过了激活还要填，整理一下要改什么"** → 触发 `implementation-intake`
- **"这个需求应该先调研还是直接开发？"** → 触发 `engineering-decision`
- **"帮我写一份 PRD"** → 若有 `decision_brief` 则触发 `engineering-documents`；若没有，先触发 `engineering-decision`
- **"线上正在发生重复扣款"** → 触发 `engineering-decision`，进入 `stabilization` 模式
- **"帮我审查这份 SRS"** → 触发 `engineering-documents` 的 `review` 流程

不应触发任何技能的场景：代码修改、翻译、格式化、按完整规格生成代码。

## 本地校验

需要 Python 3.9 或更高版本。安装依赖后，可从任意工作目录执行：

```bash
python3 -m pip install -e .
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests
```

后两条校验命令由 `.github/workflows/validate.yml` 在 main 分支和 PR 上执行，
使用的 Python 版本与 `requires-python` 的下限一致。

跨 Skill 的完整示例见 `docs/skill-flow-example.md`，触发边界见
`docs/skill-trigger-matrix.md`。

## 关键约束

- **目的门槛优先**：在分析代码仓库之前，必须先确认评估目的、项目阶段、当前目标和决策权。
- **置信度限制行为**：置信度 `low` 时，只输出问题单和澄清问题，不给正式架构结论。
- **高风险操作必须确认**：不可逆、高影响的操作始终需要明确的确认门槛。
- **中文优先**：面向用户的所有内容默认使用简体中文；英文只保留固定字段名、代码和必要技术专名。
- **受众文案**：内部状态机与“暂不做某某分析”是 agent 约束，不要写进用户可见回复；用户只需要结论、边界和下一步问题。
- **快速通道优先**：低风险、可逆、上下文给全的小问题直接回答，不强制完整决策流程；发现隐藏风险立即退出快速通道。
- **决策有保质期**：decision brief 记录有效期与重评信号；假设被证伪或环境变化时降级或重评，不沿用过期结论。
- **基线可覆盖，但必须显式**：`.agents/shared/` 给出的是基线默认值，各技能可按阶段覆盖，覆盖时必须写明阶段、数值和单位；硬底线不接受覆盖。约定见 `.agents/shared/conventions.md`。
