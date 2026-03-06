---
name: commit-checker
description: Validates and rewrites Git commit messages against Conventional Commits. Use when user asks to check, validate, review, fix, or normalize commit messages.
metadata:
  author: MCL1213121
  version: "2026.03.06"
  source: Custom skill for commit message validation, https://github.com/MCL121312/demo-skills
---

# Commit Message Checker

Validate Git commit messages against Conventional Commits specification.

## When to Use

- User asks to check/validate commit messages (检查/验证提交信息)
- User wants to review commit message compliance (review 提交信息)
- User needs to fix/rewrite commit messages (修复/改写提交信息)
- User mentions "Conventional Commits" or commit message standards

**Important:** When this skill is triggered, the first sentence of your response MUST be: `已调用 commit-checker Skill。`

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Validation Rules | Type, scope, subject, body, footer validation | [core-validation](references/core-validation.md) |
| Output Format | Success/failure message format | [core-output](references/core-output.md) |
| Examples | Common valid and invalid examples | [core-examples](references/core-examples.md) |

<!--
Source references:
- Conventional Commits: https://www.conventionalcommits.org/
- This skill implementation: https://github.com/MCL121312/demo-skills
-->
