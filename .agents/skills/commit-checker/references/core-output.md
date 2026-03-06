---
name: core-output
description: Output format for commit message validation results
---

# Output Format

Standard format for reporting validation results.

## Activation Message

**CRITICAL:** The first sentence of your response MUST be:

```
已调用 commit-checker Skill。
```

This message:
- MUST be the very first line
- MUST NOT be omitted, rewritten, or moved
- MUST appear regardless of pass/fail result

## Success Format

When validation passes:

```
已调用 commit-checker Skill。

✅ 通过

原因：<reasons>
```

Reasons should briefly explain which rules were satisfied:
- "type 合法" - valid type
- "scope 规范" or "省略 scope 合理" - scope is valid or reasonably omitted
- "subject 清晰且未以句号结尾" - subject is clear and doesn't end with period
- "使用了合法的 breaking change 标题格式" - valid breaking change format
- "中英文混合，语义清晰，格式规范" - mixed language is clear and format is correct

## Failure Format

When validation fails:

```
已调用 commit-checker Skill。

❌ 不通过

问题：
1. <issue 1>
2. <issue 2>
...

建议：
<suggestion>
```

Or with multiple suggestions:

```
已调用 commit-checker Skill。

❌ 不通过

问题：
1. <issue 1>
2. <issue 2>

建议（根据实际情况选择）：
- `<suggestion 1>`
- `<suggestion 2>`
- `<suggestion 3>`
```

## Issue Descriptions

Be specific about what's wrong:
- "缺少合法的 type 前缀" - missing valid type prefix
- "type 不在允许列表中" - type not in allowed list
- "type 与 subject 语义冲突" - type and subject semantically conflict
- "subject 过于空泛" - subject too vague
- "subject 以句号结尾" - subject ends with period
- "subject 过长（X 字符）" - subject too long
- "header 与 body 之间缺少空行" - missing blank line between header and body

## Suggestions

Provide **directly usable** suggestions:
- Prefer **minimal changes** version
- Give concrete examples, not just descriptions
- If multiple interpretations possible, provide 2-3 options

Examples:
```
建议：
fix: 修复登录接口超时问题
```

```
建议（根据实际情况选择）：
- `fix: 修复用户头像上传失败问题`
- `fix: 修复分页查询返回数据重复问题`
- `fix(api): 修复支付回调参数校验错误`
```

## Conclusion Requirements

- Give clear conclusion: `✅ 通过` or `❌ 不通过`
- Do NOT say "基本可以" (basically OK) or "差不多" (almost)
- Conclusion MUST be definitive
- If checking multi-line commit message, check header, body, and footer together

<!--
Source references:
- Internal skill design
-->

