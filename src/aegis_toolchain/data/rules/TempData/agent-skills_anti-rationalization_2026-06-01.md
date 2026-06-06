# Agent Skills — Addy Osmani 的 AI 工程纪律框架

## 原始来源
- [Agent Skills 官方博客](https://addyosmani.com/blog/agent-skills/) — Addy Osmani 亲自讲解设计哲学和五大原则
- [GitHub: addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — 30,800+ Stars，20 个结构化技能文件
- [Agent Skills 详解](https://www.rushis.com/agent-skills-teaching-ai-agents-to-code-like-senior-engineers/) — 深度解析七大命令和 Google 工程原则
- [Skills Framework 实践分析](https://danielkeller.com/tech/skills-framework-vibe-engineering/) — 实战对比：Agent Skills vs Spec Kit，实测效果数据

## 审查结论
- ✅ **可复用 — 反借口表（Anti-Rationalization）设计**：这是整个项目中最具创新性的设计，可直接借鉴到 Aegis 的 SKILL.md 和子代理中
- ✅ **可复用 — 流程优于散文（Process over Prose）原则**：技能文件应定义为可执行的工作流步骤，而非参考文档。Aegis 的 SKILL.md 已部分遵循此原则，可进一步强化
- ✅ **可复用 — 7 个斜杠命令覆盖全生命周期**：`/spec → /plan → /build → /test → /review → /code-simplify → /ship`，与 Aegis 的 L3 流程高度对应
- ⚠️ **有条件可用 — 渐进式加载（Progressive Disclosure）**：技能按需加载而非全部注入，适合 Aegis 的 L1/L2/L3 分级场景
- ⚠️ **有条件可用 — 三个专家角色**：code-reviewer、test-engineer、security-auditor，与 Aegis 子代理审查模式类似但更聚焦

## 关键要点

### 1. 核心洞察：AI 默认走"最短路径"

AI 编码代理的默认行为是跳过所有"麻烦但必要"的工程步骤：
- 跳过写 spec → 直接写代码
- 跳过写测试 → 功能"看起来能跑"就行
- 跳过安全审查 → 没提到安全问题就不检查
- 跳过代码审查 → 生成即完成

**这恰恰是 Aegis 要解决的核心问题。** Agent Skills 的方法是：把高级工程师的隐性纪律编码成 AI 可执行的工作流步骤。

### 2. 反借口表（Anti-Rationalization Table）— 最重要创新

每个技能文件包含一个「反借口表」，列出 AI（或疲劳的工程师）可能找的借口和对应的反驳：

| AI 常见借口 | 工程纪律的反驳 |
|---|---|
| "这个功能很简单，不需要 spec" | 简单性是主观判断。没有 spec 就没有验收标准。5 行 spec 可以，0 行不行。 |
| "测试之后再补" | "之后"是 load-bearing word。没有"之后"。先写失败的测试。 |
| "测试都通过了，发布吧" | 通过 ≠ 充分。覆盖了边界条件吗？安全路径呢？ |
| "只是临时方案" | 临时方案总是变成永久方案。按生产标准写。 |
| "这个改动太小，不需要审查" | 小改动造成大事故。每一行都要审查。 |

**对 Aegis 的启发**：可以在 SKILL.md 的每个阶段都加入类似的"反借口表"，防止 AI 在 L1/L2 级别跳过必要步骤。

### 3. 五大设计原则

1. **流程优于散文（Process over Prose）**：技能文件是 workflow（步骤+检查点+退出条件），不是参考文档（2000 字的最佳实践论文）
2. **反借口表（Anti-Rationalization）**：针对 LLM 训练数据中常见的"合理化偷懒"模式，提供反驳
3. **渐进式加载（Progressive Disclosure）**：技能按需激活，避免上下文膨胀。路由技能决定激活哪些
4. **证据产出（Evidence Production）**：每个步骤必须产出可验证的证据（diff、测试报告、spec 文件），不能只是"我检查过了"
5. **工具链无关（Tool-Agnostic）**：纯 Markdown 文件，不依赖特定运行时，支持 Claude Code、Cursor、Windsurf、Gemini CLI 等

### 4. 七个斜杠命令的 SDLC 映射

| 命令 | 阶段 | 对应 Aegis L3 | 关键产出 |
|---|---|---|---|
| `/spec` | 定义需求 | 00-MetaSpec + 01-braindstorm | PRD / API 契约 |
| `/plan` | 任务拆解 | 05-tasks | 原子化子任务列表 |
| `/build` | 增量构建 | 06-implement | 一次一个功能切片 |
| `/test` | 验证驱动 | 07-verify | TDD：先写测试再写实现 |
| `/review` | 代码审查 | 子代理审查 | 健康度、安全性、性能 |
| `/code-simplify` | 代码简化 | 横向贯穿 | 移除过度工程化 |
| `/ship` | 发布上线 | 收尾仪式 | Git 工作流、CI/CD 检查清单 |

### 5. Google 工程原则内置

Agent Skills 内置了 Google 的工程文化原则：
- **Hyrum's Law**：接口的隐性依赖会被滥用 → 变更影响分析
- **Chesterton's Fence**：不理解为什么存在的东西不要删除 → 重构前先理解
- **Beyonce Rule**：如果喜欢它就应该给它写测试 → 测试覆盖率
- **Shift Left**：安全、测试、审查尽可能左移 → 早期发现问题
- **测试金字塔 80/15/5**：80% 单元测试、15% 集成测试、5% E2E
- **变更大小 ~100 行**：单次 PR 不超过约 100 行，便于人类审查

### 6. SKILL.md 的标准解剖结构

有效的技能文件结构：
```markdown
---
name: skill-name
description: 何时触发、做什么
---

# 技能名称
## 触发条件
## 工作流步骤（每步包含：做什么 + 产出什么 + 如何验证）
## 反借口表
## 红旗警告（什么情况下说明技能没被正确执行）
## 验证标准（如何确认技能已正确执行）
```

**对 Aegis 的启发**：Aegis 的 SKILL.md 可以引入「反借口表」和「红旗警告」section，增强 AI 对规则的遵守率。