---
name: engineering-documents
description: >-
  Use when the user asks to create, update, review, or baseline a software
  engineering document such as an issue brief, PRD, SRS, ADR, UX
  specification, experiment plan, incident brief, high-level design, or
  detailed design. Follow an existing decision brief or document contract
  when available; preserve facts, assumptions, decisions, uncertainty,
  traceability, and document status. Do not independently override the
  recommended engineering behavior or turn exploratory evidence into a formal
  baseline.
---

# Engineering Documents

这是软件工程系列中的文档工作流。它负责“决定怎么写”：根据用户请求、已有
`decision_brief`、统一模型和模板，生成、更新、审查或基线化工程文档。

## 输出语言

默认使用简体中文生成文档正文、章节标题、审查意见、风险和开放问题。英文只保留
YAML/JSON 字段名、固定状态值、代码标识、文件路径和必要技术专名。首次出现英文
术语时附中文解释，例如“架构决策记录（ADR）”或“探索草稿（`exploratory-draft`）”。

除非用户明确要求英文，不要生成英文版分析报告或英文文档正文。

## 与 engineering-decision 的关系

如果用户只要求判断“应该怎么推进”，使用 `engineering-decision`。

如果用户要求判断并写文档，优先使用 `engineering-decision` 产生
`decision_brief`，再根据其中的 `document_contract` 执行本 Skill。

如果用户直接要求写文档但没有 decision brief：

1. 不要阻塞用户。
2. 根据现有内容建立最小事实模型。
3. 将缺失内容标成假设、未知或待决策。
4. 只做轻量的确定性判断，必要时建议先运行 `engineering-decision`。

本 Skill 不得静默把探索性需求写成批准的正式规格，也不得覆盖已有授权决策。

## 支持的文档

| 用户说法 | 类型 | 模板 |
| --- | --- | --- |
| 问题单、问题简报 | `issue-brief` | `templates/issue-brief.md` |
| 产品需求文档、PRD | `prd` | `templates/prd.md` |
| 探索版产品需求文档 | `exploratory-prd` | `templates/prd.md`，状态必须为 `exploratory-draft` |
| 软件需求规格说明书、SRS | `srs` | `templates/srs.md` |
| 架构决策记录、ADR | `adr` | `templates/adr.md` |
| UX 规格、用户体验说明 | `ux-spec` | `templates/ux-spec.md` |
| 实验计划、验证计划 | `experiment-plan` | `templates/experiment-plan.md` |
| 事件简报、事故说明 | `incident-brief` | `templates/incident-brief.md` |
| 概要设计、高层设计 | `high-level-design` | `templates/high-level-design.md` |
| 详细设计 | `detailed-design` | `templates/detailed-design.md` |

## 文档生命周期

使用统一元数据 `references/document-metadata.yaml`：

- `exploratory-draft`：用于探索、假设和实验，不代表承诺。
- `draft`：内容基本成形，仍需审查或决策。
- `proposed-baseline`：已完成审查，等待授权确认。
- `approved-baseline`：授权用户已确认范围、决策、风险和验收标准。

文档状态必须与 `decision_brief.classification.confidence` 和
`document_contract.status` 一致。不能仅因为章节齐全就提高状态。

## 输入优先级

内容来源按以下优先级处理：

1. 已确认的 `decisions`。
2. 已验证的 `facts`。
3. 明确的 `goals` 和 `constraints`。
4. 标记清晰的 `assumptions`。
5. Agent 推断，必须标记为推断或待确认。

若来源互相冲突，不要自行选择；在文档中记录冲突，并将决策问题交给授权人。

## 生成流程

### `create`

1. 读取 decision brief、需求模型和目标模板。
2. 检查文档契约中的类型、目的、状态和必需章节。
3. 只填充有依据的内容。
4. 把未知内容放入假设、开放问题、TBD 或待决策章节。
5. 根据需要建立 `REQ-*`、`UX-*`、`ADR-*`、`DES-*` 和 `TEST-*` 追踪 ID。
6. 在末尾列出风险、开放问题和下一步。

### `update`

1. 保留已有决策、版本和审查记录。
2. 根据新证据更新受影响章节。
3. 不要静默删除冲突、假设或历史决策。
4. 如果确定性或行为模式发生变化，更新元数据并建议重新运行
   `engineering-decision`。

### `review`

读取 `references/review-checklist.md`。先报告问题，再给总结。重点检查：

- 目标、范围、角色、规则和验收标准是否一致。
- 需求是否能追踪到 UX、架构、测试和验收。
- 假设是否被错误写成事实。
- 文档确定性是否高于证据。
- 是否遗漏边界、错误、恢复、安全、隐私、无障碍和运维场景。
- 是否存在阻止基线化的开放问题。

### `baseline`

只有在以下条件满足时才能使用 `approved-baseline`：

- 必要决策有授权负责人和理由。
- 验收标准可测试。
- 重要风险有处理方案和责任人。
- 范围、依赖和非目标已审查。
- 授权用户明确确认。

否则使用 `proposed-baseline` 或保持 `draft`。若置信度为 `low`，不得高于
`exploratory-draft`。

## 文档结构契约

如果输入包含：

```yaml
document_contract:
  type: exploratory-prd
  status: exploratory-draft
  purpose: validate-user-problem
  required_sections:
    - problem
    - target_users
    - hypotheses
```

必须优先遵守该契约。`type` 决定模板；`exploratory-prd` 复用 `templates/prd.md`，
但必须使用 `exploratory-draft`，并包含假设、验证计划和成功指标。`status` 决定文档承诺程度，`purpose`
决定内容重点，`required_sections` 决定最低结构，`prohibited_sections` 用于
避免超出当前证据的内容。

文档类型和行为模式的默认关系：

| 行为模式 | 优先文档 |
| --- | --- |
| `clarification` | `issue-brief` |
| `direct-execution` | `srs`、`high-level-design`、`detailed-design` |
| `expert-analysis` | `adr`、`high-level-design`、方案分析附件 |
| `iterative-discovery` | `exploratory-prd`、`prd`、`ux-spec`、`experiment-plan` |
| `stabilization` | `incident-brief` |
| `review-and-alignment` | `adr`、`issue-brief`（作为冲突整理载体） |

## 输出协议

默认输出：

1. 文档元数据和状态。
2. 文档正文。
3. 假设、风险和开放问题。
4. 追踪关系和待确认决策。
5. 推荐下一步。

用户要求只输出文档时，省略解释性前言，但仍保留文档内的状态、假设和不确定性。

## 完成前检查

- 文档类型和 `document_contract` 一致。
- 文档状态没有超过当前证据和授权范围。
- 面向用户的正文默认使用简体中文，英文仅用于固定字段、代码和必要专名。
- 事实、假设、决策、未知和推断清晰区分。
- 没有虚构用户、指标、接口、架构、约束或审批结果。
- 需求、UX、设计和测试之间的追踪关系可检查。
- 文档没有重复定义与 decision brief 冲突的行为模式。
- Markdown、YAML frontmatter 和标题层级有效。
