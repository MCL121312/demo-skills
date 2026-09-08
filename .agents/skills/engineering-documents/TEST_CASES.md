# engineering-documents 测试用例

本文件仅供维护者人工回归测试使用，agent 执行 Skill 时无需读取。

这些用例用于人工验证语义触发、流程选择、文档状态门槛和契约一致性。通过标准
不是逐字输出，而是触发或避开 Skill，并选择合理的文档动作与状态。

## 应触发

| 输入 | 预期流程 | 预期文档类型 |
| --- | --- | --- |
| 帮我写一份 PRD | `create` | `prd` 或 `exploratory-prd` |
| 根据这份 decision brief 生成 SRS | `create` | `srs` |
| 把订单迁移方案整理成 ADR | `create` | `adr` |
| 帮我审查这份 SRS 有没有矛盾 | `review` | 沿用被审查文档 |
| 线上事故，先出一份事件简报 | `create` | `incident-brief` |
| 根据新证据更新这份 PRD | `update` | 沿用原文档 |
| 这份文档能否作为正式基线 | `baseline` | 沿用原文档 |

## 不应主动触发

| 输入 | 原因 |
| --- | --- |
| 把函数名从 `foo` 改成 `bar` | 代码修改，不是文档工作流 |
| 把这段英文翻译成中文 | 翻译任务 |
| 给这段 Markdown 加目录 | 格式化任务 |
| 应该先调研还是直接开发 | 属于 `engineering-decision`，不是文档生成 |

## 与 engineering-decision 的衔接

| 情况 | 必须 | 禁止 |
| --- | --- | --- |
| 用户既要判断又要写文档 | 先由 `engineering-decision` 产生 `decision_brief`，再据 `document_contract` 执行 | 绕过决策直接生成正式基线文档 |
| 用户直接要求写文档但无 decision brief | 不阻塞；最小事实模型；缺失标为假设/未知/待决策 | 假装已有完整决策 |
| 输入包含 `document_contract` | 遵守 `type` / `status` / `required_sections` / `prohibited_sections` | 用模板默认章节覆盖契约禁止项 |
| `document_contract.type` 为 `exploratory-prd` | 用 `templates/prd.md`；状态 `exploratory-draft`；含假设、验证、成功指标 | 写成已批准产品承诺 |

## 文档状态门槛

| 情况 | 必须 | 禁止 |
| --- | --- | --- |
| 章节齐全但证据不足 | 状态与证据/契约一致 | 因结构完整就升到 `proposed-baseline` 或 `approved-baseline` |
| `decision_brief.confidence` 为 `low` | 状态 ≤ `exploratory-draft`；列出未知与缺口 | 正式架构结论或批准基线 |
| 请求 `approved-baseline` 但无用户确认 | 使用 `proposed-baseline` 或保持 `draft` | 静默写成已批准 |
| 满足决策已确认、可测验收、风险有主、范围已审、用户确认 | 允许 `approved-baseline` | 无 |
| `decision_brief.confidence` 为 `low` 且请求 `approved-baseline` | 拒绝提升；保持 `exploratory-draft` 并列出缺口 | 接受用户口头“就算了，批准吧”而跳过证据 |
| 模板 frontmatter 含 `<from-*>` 占位符 | 生成时替换为 brief/contract 实际值 | 把占位符原文留在交付文档里 |

## create 流程

| 情况 | 预期行为 |
| --- | --- |
| 有依据的内容 | 直接填充对应章节 |
| 未知内容 | 放入假设、开放问题、TBD 或待决策，不虚构 |
| 需要追踪关系 | 建立 `REQ-*`、`UX-*`、`ADR-*`、`DES-*`、`TEST-*` ID |
| 来源相互冲突 | 记录冲突，把决策问题交用户，不自行选择 |

## update 流程

| 情况 | 预期行为 |
| --- | --- |
| 已有决策、版本、审查记录 | 保留，不静默删除 |
| 新证据影响部分章节 | 只更新受影响章节 |
| 确定性或行为模式变化 | 更新元数据，建议重新运行 `engineering-decision` |

## review 流程

- 先列问题再给总结，问题按严重程度排序并引用文档和章节。
- 检查目标、范围、角色、规则、验收标准是否一致。
- 检查需求能否追踪到 UX、架构、测试和验收。
- 检查假设是否被写成事实，文档确定性是否高于证据。
- 检查是否遗漏边界、错误、恢复、安全、隐私、无障碍和运维场景。

## 输出语言

| 输入 | 预期行为 |
| --- | --- |
| 用户使用中文且未指定语言 | 文档正文、标题、审查意见使用简体中文 |
| 分析中出现 `exploratory-draft`、`ADR` | 首次出现附中文解释 |
| 用户明确要求英文 | 可输出英文正文，保持字段名和状态值稳定 |

## 完成前检查

- 文档类型与 `document_contract` 一致。
- 文档状态没有超过当前证据和用户确认范围。
- 事实、假设、决策、未知和推断清晰区分。
- 没有虚构用户、指标、接口、架构、约束或审批结果。
- 需求、UX、设计和测试之间的追踪关系可检查。
- Markdown、YAML frontmatter 和标题层级有效。
