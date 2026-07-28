# 工程决策案例

本文档用于说明 `engineering-decision` 的典型判断方式和边界。案例中的 YAML
是内部 `decision_brief` 的简化表示，不是默认展示给用户的格式。面向用户时，
应将它渲染成中文摘要。

## 如何使用案例

每个案例关注四件事：

1. 当前问题是什么，而不是项目整体看起来多大。
2. 哪些证据支持当前判断。
3. 应该采用什么行为模式。
4. 下一步允许做什么，哪些事情应该暂缓。

## 案例一：清晰域（`clear`）

### 用户输入

> 给已有订单列表增加一个按订单号精确搜索的输入框，后端已有查询接口，
> 搜索结果和现有列表复用同一套分页规则，写一个 SRS 草稿。

### 信息判断

- 目标明确：增加精确搜索。
- 接口已有：不需要探索技术路线。
- 分页规则明确：验收边界基本清楚。
- 缺少字段校验和错误提示细节，但不阻止生成草稿。

### 内部判断

```yaml
classification:
  problem_type: specified-change
  cynefin_domain: clear
  confidence: high
behavior:
  mode: direct-execution
  engagement_level: L1
document_contract:
  needed: true
  type: srs
  status: draft
  purpose: specify-search-behavior
  required_sections:
    - functional_requirements
    - validation
    - acceptance_criteria
```

### 面向用户的结果

当前需求属于清晰域（`clear`），可以直接整理成 SRS 草稿。字段校验和错误提示
仍需补充，但不会阻塞初稿。

### 不应做的事

- 不需要先做用户访谈。
- 不需要把它升级成完整架构评估。
- 不应因为项目整体很大，就提高这个小变更的处理复杂度。

## 案例二：繁杂域（`complicated`）

### 用户输入

> 需要把订单数据从单体数据库迁移到独立服务。业务规则、接口契约和迁移目标
> 已经确定，但需要在双写、停机迁移和 CDC 之间选择方案。

### 信息判断

- 目标、业务规则和接口契约已经确定。
- 难点是技术方案、性能、回滚和运维权衡。
- 不是用户需求探索问题。

### 内部判断

```yaml
classification:
  problem_type: architecture-choice
  cynefin_domain: complicated
  confidence: high
behavior:
  mode: expert-analysis
  engagement_level: L2
document_contract:
  needed: true
  type: adr
  status: draft
  purpose: compare-migration-options
  required_sections:
    - decision_drivers
    - alternatives
    - tradeoffs
    - rollback
```

### 面向用户的结果

当前属于繁杂域（`complicated`），适合进行专家分析。先明确评价标准，比较三种
迁移方案，再由授权决策者确认，不应由 Agent 静默替用户选择。

### 不应做的事

- 不应因为技术难就判为复杂域（`complex`）。
- 不应直接生成已经选定方案的详细设计。
- 不应把候选方案写成已确认决策。

## 案例三：复杂域（`complex`）

### 用户输入

> 想做一个 AI 助手帮助新员工熟悉公司流程，但不知道他们最需要什么，
> 也不知道应该做聊天、搜索还是任务清单。

### 信息判断

- 目标用户的核心任务还没有验证。
- 产品形态存在多个方向。
- 成功指标和用户采用行为未知。

### 内部判断

```yaml
classification:
  problem_type: product-discovery
  cynefin_domain: complex
  confidence: high
behavior:
  mode: iterative-discovery
  engagement_level: L3
  allowed_actions:
    - ask_targeted_questions
    - create_hypotheses
    - design_experiment
  confirmation_gates:
    - target_user
    - primary_success_metric
document_contract:
  needed: true
  type: exploratory-prd
  status: exploratory-draft
  purpose: validate-user-problem
  required_sections:
    - problem
    - target_users
    - hypotheses
    - experiment_plan
    - success_metrics
```

### 面向用户的结果

当前属于复杂域（`complex`），应采用迭代探索（`iterative-discovery`）。先确认
目标用户，提出假设并设计最小实验，不直接锁定详细设计。

### 不应做的事

- 不应直接选择聊天、搜索或任务清单。
- 不应把用户偏好写成事实。
- 不应生成看似正式的最终 PRD。

## 案例四：混乱域（`chaotic`）

### 用户输入

> 新版本上线后订单重复扣款，客服投诉正在增加，需要先处理问题，再讨论
> 长期改造方案。

### 信息判断

- 正在发生实际财务影响。
- 影响范围可能继续扩大。
- 当前第一目标是止损和恢复，不是完整理解系统。

### 内部判断

```yaml
classification:
  problem_type: production-incident
  cynefin_domain: chaotic
  confidence: high
behavior:
  mode: stabilization
  engagement_level: L4
  allowed_actions:
    - contain_harm
    - assess_impact
    - recover_service
    - record_decisions
  blocked_actions:
    - baseline_long_term_design
document_contract:
  needed: true
  type: incident-brief
  status: draft
  purpose: contain-and-recover
  required_sections:
    - impact
    - containment
    - recovery
    - timeline
```

### 面向用户的结果

当前属于混乱域（`chaotic`），先进行稳定化和止损。优先确认影响范围、暂停或
隔离有问题的流程、恢复服务并记录决策；稳定后再进入根因分析和长期改造。

### 不应做的事

- 不应先写普通 PRD。
- 不应在事故过程中承诺长期架构方案。
- 不应为了完善分析而延误止损。

## 案例五：未明状态（`confused`）

### 用户输入

> 我给你一个健康管理后端项目地址，帮我评估一下项目复杂度。

### 信息判断

即使可以读取仓库，也缺少决定评估意义所需的上下文：

- 这次评估要支持什么决策？
- 项目目前处于什么阶段？
- 当前最重要的目标是什么？
- 哪些团队参与？
- 谁拥有最终决策权？
- 项目是教学、试用、内部使用还是生产系统？

### 内部判断

```yaml
classification:
  problem_type: project-assessment
  cynefin_domain: confused
  confidence: high
behavior:
  mode: clarification
  engagement_level: L3
next_action:
  description: collect-purpose-and-context
document_contract:
  needed: true
  type: issue-brief
  status: exploratory-draft
  purpose: establish-assessment-context
  required_sections:
    - assessment_purpose
    - project_stage
    - current_goal
    - organization_and_decision_rights
```

### 面向用户的结果

在评估仓库前，需要先确认四件事：评估目的、项目阶段、当前目标、参与团队和
决策者。补齐这些信息前，只建立问题单和上下文缺口，不输出项目复杂度等级或
最终推进建议。

### 不应做的事

- 不应仅凭仓库文件数量给出项目复杂度。
- 不应从组织名称推断组织架构。
- 不应把代码结构直接等同于项目目标。

## 边界案例一：技术很难，但不是复杂域

> 需要实现高并发批处理，但协议、输入输出、性能指标和验收标准都已明确，
> 已有成熟的分片和重试方案。

判断：倾向繁杂域（`complicated`），行为模式为专家分析。技术困难只说明需要
专业分析，不代表用户结果或因果关系未知。

## 边界案例二：项目很大，但当前变更是清晰域

> 大型支付系统中，将已有字段 `mobile` 重命名为 `phone_number`，接口兼容策略、
> 迁移脚本和验收条件都已经确定。

判断：当前变更可以是清晰域（`clear`）。项目整体规模不会自动改变当前问题的域。

## 边界案例三：项目很小，但当前问题是复杂域

> 一个只有两名开发者的内部工具，团队还不知道用户更需要搜索、导出还是提醒功能。

判断：项目规模小，但用户结果未知，当前问题仍可能是复杂域（`complex`）。

## 边界案例四：需求混乱但不是事故

> 产品、运营和技术对“客户画像功能”有不同理解，但系统没有线上故障或数据损失。

判断：倾向未明状态（`confused`），先澄清目标、范围和决策权，不应判为混乱域
（`chaotic`）。

## 边界案例五：用户要求全自动，但行动不可逆

> 用户要求 Agent 自动执行生产数据库迁移，并删除旧字段。

判断：即使用户要求全自动，也要因为不可逆、高风险和数据影响提高参与度，要求
明确确认、备份、回滚方案和授权人。

## 边界案例六：只要求仓库静态分析

> 只根据仓库代码和配置做静态复杂度分析，不需要询问组织和项目目标。

判断：可以执行，但必须标记为 `repository-only-assessment`。报告只能说明仓库
中观察到的技术事实，不能推断真实项目目标、组织架构、决策权或最终行为模式。

## 边界案例七：新增信息后重新分类

初始信息：用户说“想做一个退款系统”，信息不足，属于未明状态（`confused`）。

后续信息：退款规则和成功指标已经确认，但需要比较多渠道一致性方案，迁移和
回滚要求也已明确。

判断：可以从 `confused` 迁移到繁杂域（`complicated`），行为模式从澄清变成专家
分析。分类不是一次性结论。
