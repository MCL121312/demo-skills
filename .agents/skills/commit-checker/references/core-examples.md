---
name: core-examples
description: Common valid and invalid commit message examples
---

# Examples

Common examples of valid and invalid commit messages with expected validation results.

## Valid Examples

### Basic Valid

**Input:** `feat: 添加用户登录功能`

**Output:** `已调用 commit-checker Skill。✅ 通过。type 合法，省略 scope 合理，subject 清晰且未以句号结尾。`

---

**Input:** `fix(api): 修复登录接口超时问题`

**Output:** `已调用 commit-checker Skill。✅ 通过。格式正确，type 与 scope 规范，subject 表达明确。`

### Mixed Language (Valid)

**Input:** `docs: 更新 README 中的安装说明`

**Output:** `已调用 commit-checker Skill。✅ 通过。type 合法，subject 中英混合允许，语义清晰。`

---

**Input:** `feat(auth模块): 支持 OAuth login 回调处理`

**Output:** `已调用 commit-checker Skill。✅ 通过。type 合法，scope 与 subject 允许中英文混合，语义清晰，格式规范。`

---

**Input:** `chore(user中心): upgrade ESLint 配置`

**Output:** `已调用 commit-checker Skill。✅ 通过。type 合法，中英混合允许，格式规范。`

### Breaking Change (Valid)

**Input:** `feat(api)!: 重构认证逻辑`

**Output:** `已调用 commit-checker Skill。✅ 通过。使用了合法的 breaking change 标题格式，type、scope 与 subject 均规范。`

### Multi-line (Valid)

**Input:**
```
feat(auth): 支持 OAuth login

补充 callback 校验逻辑，避免 token mismatch

Refs: #123
```

**Output:** `已调用 commit-checker Skill。✅ 通过。格式正确，header、body、footer 结构规范，中英文混合语义清晰。`

## Invalid Examples

### Missing Type

**Input:** `修复了一个bug`

**Output:** `已调用 commit-checker Skill。❌ 不通过。缺少合法的 type 前缀。建议改为：fix: 修复登录接口报错问题`

### Chinese Type

**Input:** `功能: 添加登录功能`

**Output:** `已调用 commit-checker Skill。❌ 不通过。type 不在允许列表中，必须使用规范英文关键字。建议改为：feat: 添加登录功能`

### Invalid Type

**Input:** `update: 修改首页样式`

**Output:** `已调用 commit-checker Skill。❌ 不通过。type 不在允许列表中。建议改为：style: 调整首页样式`

### Period Ending

**Input:** `docs: 更新安装说明。`

**Output:** `已调用 commit-checker Skill。❌ 不通过。subject 以句号结尾。建议改为：docs: 更新安装说明`

---

**Input:** `fix: 修复登录报错.`

**Output:** `已调用 commit-checker Skill。❌ 不通过。subject 以英文句号结尾。建议改为：fix: 修复登录报错`

### Vague Subject

**Input:** `fix: fix bug`

**Output:** `已调用 commit-checker Skill。❌ 不通过。subject 过于空泛，应具体说明改动内容。建议改为：fix: 修复登录接口超时问题`

---

**Input:** `chore: 修改代码`

**Output:** `已调用 commit-checker Skill。❌ 不通过。subject 不清晰，应具体说明改动内容。建议改为：chore: 更新依赖版本`

### Semantic Conflict

**Input:** `feat: 修复一个bug`

**Output:**
```
已调用 commit-checker Skill。

❌ 不通过

问题：
1. type 与 subject 语义冲突：使用了 'feat'（新功能）但描述的是修复
2. subject 过于空泛，应具体说明改动内容

建议：
fix: 修复登录接口超时问题
```

### Too Long Subject

**Input:** `feat: 添加一个用于统一处理用户登录鉴权状态并兼容历史接口行为的功能模块`

**Output:** `已调用 commit-checker Skill。❌ 不通过。subject 过长（38 字符），建议压缩为 50 字符以内。建议改为：feat: 添加统一登录鉴权模块`

### Missing Blank Line

**Input:**
```
fix(api): 修复 login 超时
补充重试逻辑
```

**Output:** `已调用 commit-checker Skill。❌ 不通过。header 与 body 之间缺少空行。建议在标题行后添加一个空行。`

## Edge Cases

### Only Type and Colon

**Input:** `feat:`

**Output:** `已调用 commit-checker Skill。❌ 不通过。缺少 subject 描述。建议改为：feat: 添加具体功能描述`

### Scope with Spaces

**Input:** `fix( api ): 修复问题`

**Output:** `已调用 commit-checker Skill。❌ 不通过。scope 中包含多余空格。建议改为：fix(api): 修复问题`

<!--
Source references:
- Test cases from TEST_CASES.md
- Conventional Commits examples
-->

