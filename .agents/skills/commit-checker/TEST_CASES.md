## Commit Checker 测试文档

### 1. 测试目标

验证 `skills/commit-checker/SKILL.md` 是否满足以下要求：

- 能在“检查 / 修复 commit message”语境下被正确触发
- 触发后第一句话会明确输出：`已调用 commit-checker Skill。`
- 能输出明确结论：`✅ 通过` 或 `❌ 不通过`
- `type` 必须为规范英文关键字
- `scope`、`subject`、正文、页脚允许中文、英文或中英文混合
- 不会把中英文混合作为不通过原因
- 不通过时能给出可直接使用的修改建议

### 2. 测试方法

按下面的“输入”逐条向模型提问，观察“预期结果”是否满足。

推荐提问方式：

- `帮我检查这个 commit message：<输入>`
- `这条提交信息符合规范吗：<输入>`
- `帮我修复这条 commit message：<输入>`

### 3. 技能调用测试（优先执行）

这组样例**只测试是否调用 Skill**，不检查 commit message 判定结果是否正确。

统一检查点：

- 回复的第一句话包含 `已调用 commit-checker Skill。`
- 不要求本轮测试同时验证 `✅ 通过` / `❌ 不通过` 的结论正确性

| 编号 | 用户提问 | 预期 |
|---|---|---|
| S1 | 帮我检查这个 commit message：feat: 添加用户登录功能 | 第一句话包含 `已调用 commit-checker Skill。` |
| S2 | 这条提交信息规范吗：fix(api): 修复 login callback 超时 | 第一句话包含 `已调用 commit-checker Skill。` |
| S3 | 帮我修复这个提交信息：修复了一个bug | 第一句话包含 `已调用 commit-checker Skill。` |
| S4 | review 一下这条 commit message 是否符合 Conventional Commits | 第一句话包含 `已调用 commit-checker Skill。` |
| S5 | 帮我把这条提交信息改成 Conventional Commits：更新登录逻辑 | 第一句话包含 `已调用 commit-checker Skill。` |

### 4. 触发测试

| 编号 | 用户提问 | 预期 |
|---|---|---|
| T1 | 帮我检查这个 commit message：feat: 添加用户登录功能 | 应触发 Skill，且第一句话包含 `已调用 commit-checker Skill。` |
| T2 | 这条提交信息规范吗：fix(api): 修复 login callback 超时 | 应触发 Skill，且第一句话包含 `已调用 commit-checker Skill。` |
| T3 | 帮我修复这个提交信息：修复了一个bug | 应触发 Skill，且第一句话包含 `已调用 commit-checker Skill。` |
| T4 | review 一下这条 commit message 是否符合 Conventional Commits | 应触发 Skill，且第一句话包含 `已调用 commit-checker Skill。` |
| T5 | 帮我写一个登录接口 | 不应触发该 Skill |
| T6 | 解释一下什么是 Git rebase | 不应触发该 Skill |

### 5. 规则测试

| 编号 | 输入 | 预期结果 | 关注点 |
|---|---|---|---|
| R1 | `feat: 添加用户登录功能` | ✅ 通过 | 基础通过 |
| R2 | `fix(api): 修复登录接口超时问题` | ✅ 通过 | scope 合法 |
| R3 | `docs: 更新 README 中的安装说明` | ✅ 通过 | 中英混合 subject |
| R4 | `feat(auth模块): 支持 OAuth login 回调处理` | ✅ 通过 | scope / subject 中英混合允许 |
| R5 | `chore(user中心): upgrade ESLint 配置` | ✅ 通过 | 中英混合允许 |
| R6 | `feat(api)!: 重构认证逻辑` | ✅ 通过 | breaking change header |
| R7 | `修复了一个bug` | ❌ 不通过 | 缺少 type |
| R8 | `功能: 添加登录功能` | ❌ 不通过 | type 不能是中文 |
| R9 | `update: 修改首页样式` | ❌ 不通过 | 非法 type |
| R10 | `docs: 更新安装说明。` | ❌ 不通过 | subject 以中文句号结尾 |
| R11 | `fix: 修复登录报错.` | ❌ 不通过 | subject 以英文句号结尾 |
| R12 | `fix: fix bug` | ❌ 不通过 | subject 过于空泛 |
| R13 | `chore: 修改代码` | ❌ 不通过 | subject 不清晰 |
| R14 | `feat: 添加一个用于统一处理用户登录鉴权状态并兼容历史接口行为的功能模块` | ❌ 或提示不够规范 | subject 过长 |

### 6. 多行 commit message 测试

#### M1：应通过

输入：

`feat(auth): 支持 OAuth login`

空行

`补充 callback 校验逻辑，避免 token mismatch`

空行

`Refs: #123`

预期：

- 第一句话包含 `已调用 commit-checker Skill。`
- ✅ 通过
- 能识别 header / body / footer
- 不会因为中英文混合判错

#### M2：应不通过

输入：

`fix(api): 修复 login 超时`
`补充重试逻辑`

预期：

- 第一句话包含 `已调用 commit-checker Skill。`
- ❌ 不通过
- 指出 header 与 body 之间缺少空行

### 7. 验收标准

每条测试至少检查以下 5 点：

1. 第一句话是否包含 `已调用 commit-checker Skill。`
2. 结论是否明确
3. 理由是否正确
4. 是否误把中英文混合作为错误
5. 修改建议是否可直接使用
6. 检查重点是否集中在格式、type、subject、空行和清晰度

### 8. 测试记录模板

| 编号 | 输入/提问 | 预期 | 实际 | 是否通过 | 备注 |
|---|---|---|---|---|---|
| R1 | feat: 添加用户登录功能 | ✅ |  |  |  |
| R4 | feat(auth模块): 支持 OAuth login 回调处理 | ✅ |  |  |  |
| R8 | 功能: 添加登录功能 | ❌ |  |  |  |

### 9. 最终判定标准

若以下条件都稳定满足，则该 Skill 可认为测试通过：

- 触发后第一句话稳定输出 `已调用 commit-checker Skill。`
- 仅 `type` 强制要求规范英文关键字
- 其余部分允许中英文混合
- 中英文混合不会被误判为不通过
- 不通过时能提供清晰且可直接使用的建议

