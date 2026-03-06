# 🛠 Skills Demo

AI Agent Skills 示例项目，参考 [antfu/skills](https://github.com/antfu/skills) 的设计理念。

## 📁 项目结构

```
.
├── .agents/
│   └── skills/                    # Skills 目录
│       └── commit-checker/        # Commit 检查 Skill
│           ├── SKILL.md           # Skill 主索引文件
│           ├── TEST_CASES.md      # 测试用例
│           └── references/        # 具体的技能参考文档
│               ├── core-validation.md
│               ├── core-output.md
│               └── core-examples.md
└── README.md
```

## 🧠 设计理念

这个项目采用 **纯文档形式** 的 Skill 设计，由 AI 大模型直接读取和执行：

1. **纯 Markdown 文档** - 没有可执行代码，只有结构化的文档
2. **AI 直接读取** - 大模型通过 codebase-retrieval 读取这些文档
3. **Frontmatter 元数据** - 使用 YAML frontmatter 定义 name、description 等
4. **结构化组织** - 通过表格和分类组织技能引用

## 🚀 如何使用

在与 AI 助手对话时，直接提问：

```
帮我检查这个提交信息：feat: 添加用户登录功能
```

```
这条提交信息规范吗：修复了一个bug
```

AI 助手会：
1. 通过 codebase-retrieval 读取 `.agents/skills/commit-checker/SKILL.md`
2. 根据 SKILL.md 中的规则执行检查
3. 按照规定的格式输出结果（以 `已调用 commit-checker Skill。` 开头）

## 📝 Skill 开发指南

### Skill 目录结构

每个 Skill 应该包含以下文件：

```
.agents/skills/your-skill/
├── SKILL.md           # Skill 主索引文件（必需）
├── TEST_CASES.md      # 测试用例文档（推荐）
└── references/        # 具体的技能参考文档（推荐）
    ├── core-*.md      # 核心功能
    ├── feature-*.md   # 特性功能
    └── advanced-*.md  # 高级功能
```

### SKILL.md 格式

```markdown
---
name: skill-name
description: Brief description of what this skill does. Use when...
metadata:
  author: Your Name
  version: "2026.03.06"
  source: https://github.com/your/repo
---

# Skill Title

Brief introduction of the skill.

## When to Use

- Scenario 1
- Scenario 2
- Scenario 3

**Important:** Any special instructions for AI when this skill is triggered.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Topic 1 | Description | [core-topic1](references/core-topic1.md) |
| Topic 2 | Description | [core-topic2](references/core-topic2.md) |

<!--
Source references:
- https://source-url-1
- https://source-url-2
-->
```

### references/*.md 格式

```markdown
---
name: reference-name
description: What this reference covers
---

# Reference Title

Detailed content here.

## Usage

Code examples and practical patterns.

## Key Points

- Important detail 1
- Important detail 2

<!--
Source references:
- https://source-url
-->
```

## 🎯 现有 Skills

### commit-checker

检查 Git 提交信息是否符合 Conventional Commits 规范。

**触发场景：**
- 用户要求检查/验证提交信息
- 用户想 review 提交信息合规性
- 用户需要修复/改写提交信息
- 用户提到 "Conventional Commits" 或提交信息标准

**示例对话：**

```
用户：帮我检查这个提交信息：feat: 添加用户登录功能
AI：已调用 commit-checker Skill。

✅ 通过

原因：type 合法，省略 scope 合理，subject 清晰且未以句号结尾。
```

```
用户：这条提交信息规范吗：修复了一个bug
AI：已调用 commit-checker Skill。

❌ 不通过

问题：
1. 缺少合法的 type 前缀

建议：
fix: 修复登录接口报错问题
```

## 🔍 如何验证 Skill 是否生效

当你向 AI 助手提问时，如果 Skill 被正确调用，你会看到：

1. **特定的开头** - 回复以 `已调用 commit-checker Skill。` 开头
2. **结构化输出** - 按照 SKILL.md 中定义的格式输出
3. **明确结论** - 给出 `✅ 通过` 或 `❌ 不通过`
4. **具体建议** - 如果不通过，提供可直接使用的修改建议

## 📚 参考资料

- [antfu/skills](https://github.com/antfu/skills) - Anthony Fu 的 Agent Skills 集合
- [Agent Skills](https://agentskills.io/) - Agent Skills 官方网站
- [Conventional Commits](https://www.conventionalcommits.org/) - 提交信息规范

## 📝 License

MIT
