---
name: core-validation
description: Validation rules for Conventional Commits format
---

# Validation Rules

Complete validation rules for checking commit messages against Conventional Commits specification.

## Structure Recognition

### Header Format

Recommended format: `<type>(<scope>): <subject>`

Also allowed:
- Without scope: `<type>: <subject>`
- Breaking change: `<type>!: <subject>` or `<type>(<scope>)!: <subject>`

## Type Validation

**Required field.** Must be one of:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, etc.)
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Test changes
- `build` - Build system changes
- `ci` - CI configuration changes
- `chore` - Other changes
- `revert` - Revert previous commit

**Important:**
- Type MUST be in English (规范英文关键字)
- Chinese types like `功能:`, `修复:` are NOT allowed
- Non-standard types like `update`, `add` are NOT allowed

If type is invalid, suggest the closest valid type.

## Language Usage

- **Type:** MUST be English keywords only
- **Scope, Subject, Body, Footer:** Can use Chinese, English, or mixed (中英文混合允许)
- Do NOT fail validation just because of mixed languages
- Focus on format, legality, clarity, and readability

## Scope Validation

**Optional field.**

If present:
- Should be concise and clear
- Can use Chinese, English, or mixed
- If English, recommend lowercase or project conventions
- Should NOT contain extra spaces

## Subject Validation

**Required field.**

Rules:
- Can use Chinese, English, or mixed (as long as semantically clear)
- Should be concise, **preferably under 50 characters**
- Should NOT end with period (`.` or `。`)
- Should NOT be too vague

Vague examples to avoid:
- `update`
- `fix bug`
- `修改代码`
- `修复了一个bug`
- `添加了一个功能`

If subject is obviously too long, mark as non-compliant and suggest compression.

## Semantic Consistency

Check type and subject match:
- `feat` (new feature) should NOT describe fixes
- `fix` (bug fix) should NOT describe new features

Example of conflict:
- ❌ `feat: 修复一个bug` - type says "feature" but subject says "fix"
- ✅ `fix: 修复登录接口超时问题` - type and subject match

## Body Validation (Optional)

If body exists:
- MUST have one blank line between header and body
- Can use Chinese, English, or mixed
- Used to explain reasons, background, or implementation details

## Footer Validation (Optional)

If footer exists:
- MUST have one blank line between body and footer
- Can use Chinese, English, or mixed
- Keywords like `BREAKING CHANGE:` can remain in standard English
- Used for linking issues or declaring breaking changes

Examples:
- `Refs: #123`
- `Closes: #456`
- `BREAKING CHANGE: API signature changed`

## Multi-line Format

For multi-line commit messages:
```
<header>
<blank line>
<body>
<blank line>
<footer>
```

Common error: Missing blank line between header and body.

<!--
Source references:
- https://www.conventionalcommits.org/
- https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit
-->

