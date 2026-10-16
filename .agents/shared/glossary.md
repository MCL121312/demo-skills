# 框架用词表

框架自造词的唯一登记处。规则见 `conventions.md`「用词」一节：不登记的词不得在
SKILL.md 与 `references/` 里使用；同名不同义必须改名。

「用户可见」一列指该词能否出现在面向实施人员、客户或评审者的文字里。

| 词 | 含义 | 用在哪 | 用户可见 |
| --- | --- | --- | --- |
| Cynefin 域 | 问题当前属于 clear / complicated / complex / chaotic / confused 哪一类 | `engineering-decision` | 否 |
| 信息分层 | 把输入按 facts / goals / constraints / assumptions / unknowns / conflicts / risks / decisions 归类 | 全部 Skill | 否 |
| 行为模式 | 本轮采取的工作方式（直接推进、专家分析、迭代探索、止损、澄清、评审对齐） | `engineering-decision` | 否 |
| 参与度 | 用户需要介入的程度（L0–L4） | `engineering-decision` | 否 |
| 目的门槛 | 开始分析前必须先确认评估目的、项目阶段、当前目标 | `engineering-decision` | 否 |
| 快速通道 | 满足条件时跳过完整决策流程，直接给建议 | `engineering-decision` | 否 |
| 止损 | 存在正在扩大的伤害时，先恢复与安全，不做常规需求分析 | `engineering-decision` | 是（用大白话说「先止血」） |
| 决策简报 | 决策判断的结构化结果（`decision_brief`），默认渲染成中文摘要给用户 | `engineering-decision` | 否 |
| 问题记录 | 决策流程里的最小问题单（`issue-schema.yaml`，状态 `intake`） | `engineering-decision`、`implementation-intake` | 否 |
| 文档契约 | 决策传给文档工作流的结构（`document_contract`）：类型、状态、目的、必需与禁止章节 | 两个文档 Skill 之间 | 否 |
| 正文 | 交付物里给人读的那份（`<slug>.md`） | `engineering-documents` | 是 |
| 约束文件 | 交付物里给执行者与机器读的那份（`<slug>.constraints.yaml`）：清单、断言、字段、ID、状态 | `engineering-documents` | 是 |
| profile | 交付物的受众开关：`solo / team / external`，决定是否生成治理与对外内容 | `engineering-documents` | 否 |
| 现场记录 | 实施场景下从群聊、工单整理出的结构化条目 | `implementation-intake` | 是（它本身就是产出） |
| 触发词 | 决定某个 Skill 是否启动的输入特征 | 全部 Skill | 否 |
