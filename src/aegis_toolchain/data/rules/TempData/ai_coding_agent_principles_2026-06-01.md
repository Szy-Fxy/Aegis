# AI 编码代理原则 — Agentic Coding 6 Principles & 28 Practices

## 原始来源
- [Agentic Coding Principles](https://agentic-coding.github.io/) — 6 原则 28 实践，从 Vibe Coding 到 Agentic Coding 的进阶指南
- [GitHub Copilot Coding Agent 最佳实践](https://github.github.io/awesome-copilot/learning-hub/using-copilot-coding-agent/) — 官方指南：如何写好 Issue、结构化 PR、Agent Skills vs Instructions vs Agents
- [GitHub Copilot Custom Agents](https://github.github.io/awesome-copilot/learning-hub/building-custom-agents/) — 自定义 Agent 的完整指南：Persona + Tool Access + Guardrails

## 审查结论
- ✅ **可复用 — 6 大原则**：开发者问责、理解验证、安全优先、代码质量、人主导设计、持续改进，可作为 Aegis global.md 的 AI 行为准则补充
- ✅ **可复用 — Custom Agent 三要素**：Persona + Tool Access + Guardrails，Aegis 子代理架构可参考
- ✅ **可复用 — Good Issue Structure**：定义 Done、适当范围、包含约束，与 Aegis 的 spec 模板高度一致
- ⚠️ **有条件可用 — Skills vs Instructions vs Agents 区分**：Aegis 当前混合了这三种概念，可考虑分离

## 关键要点

### 1. Agentic Coding 六大原则

**原则 1：开发者问责（Developer Accountability）**
- AI 只是工具，人类是最终负责人
- "AI 写的"不是有效借口
- 开发者对代码质量、功能、性能、安全、可维护性负全责

**原则 2：理解与验证（Understand and Verify）**
- 不理解代码就不要接受
- 集成前必须完全理解并验证（包括代码审查和测试）
- 禁止盲目接受 AI 生成的代码

**原则 3：安全与保密优先（Prioritize Security and Confidentiality）**
- 不要将敏感信息（源码、API Key、内部数据、客户信息、知识产权）直接输入未批准的外部 AI
- 即使使用已批准工具，也要警惕通过代理或中间服务器意外泄漏数据
- 严格遵守公司安全政策和指南

**原则 4：保持代码质量与一致性（Maintain Code Quality, Standards, Consistency）**
- 开发者负责确保 AI 生成的代码符合项目既定标准
- 代码必须通过 linting、formatting、静态分析
- 不低于人工编写的质量标准

**原则 5：人主导设计与关键思维（Human-Led Design and Critical Thinking）**
- 核心系统设计、架构决策、关键业务逻辑必须由人类主导
- AI 在支持角色中使用（构思、实现辅助）
- 始终批判性评估 AI 建议，避免盲目接受
- 认识 AI 的局限性，基于人类洞察和经验做关键决策

**原则 6：持续改进（Continuous Improvement）**
- 定期回顾 AI 辅助开发流程
- 从错误中学习，优化提示词和规则
- 记录 AI 协作中的经验教训

### 2. AI 编码代理的 28 个实践

核心实践分类：
- **准备阶段**：定义项目上下文、设置编码标准、配置规则文件
- **需求阶段**：结构化 Issue、明确验收标准、包含约束条件
- **实现阶段**：增量构建、持续验证、保持 PR 小而可审查
- **审查阶段**：逐行审查、运行测试、检查安全漏洞
- **交付阶段**：文档更新、知识沉淀、流程回顾

### 3. Custom Agent 三要素架构

GitHub Copilot 的 Custom Agent 使用 `.agent.md` 文件定义：

```
---
name: 'Security Reviewer'
description: 'Expert security auditor...'
model: Claude Sonnet 4
tools: ['codebase', 'terminal', 'github']
---

# Agent 行为指令（Markdown）
## 你的专长
## 审查清单
## 输出格式
```

**三要素**：
- **Persona（角色）**：专长、语气、工作风格
- **Tool Access（工具权限）**：能访问哪些内置工具和 MCP 服务器
- **Guardrails（护栏）**：遵循的边界和约定

**Agent vs Instructions vs Skills 的区别**：
| 类型 | 特点 | 触发方式 |
|---|---|---|
| Instructions | 被动背景上下文，对所有匹配文件自动应用 | 自动 |
| Skills | 单任务能力，处理特定类型工作 | 按需调用 |
| Agents | 完整角色定义，持久 Persona + 工具权限 | 显式选择 |

**对 Aegis 的启发**：Aegis 的 global.md 是 Instructions，SKILL.md 是 Skill，子代理审查是 Agent。三者的职责边界可以更清晰。

### 4. 写好 Issue 的结构（让 AI 编码代理理解）

```
一个好的 Issue 结构：
1. 清晰的标题（做什么）
2. 背景与动机（为什么）
3. 验收标准（Definition of Done）
4. 技术约束（不能做什么）
5. 相关文件/模块（在哪里改）
```

**关键原则**：
- 定义 Done：列出验收标准或测试用例，验证工作是否完成
- 适当范围：单功能 Issue 效果最好，大型功能拆分为小 Issue
- 包含约束：明确告诉 AI 不要做什么（"不要修改数据库 Schema"）

### 5. 对比：Aegis 当前原则覆盖度

| Agentic Coding 原则 | Aegis 当前覆盖 | 差距 |
|---|---|---|
| 1. 开发者问责 | global.md 有提及 | 可以更明确强调 |
| 2. 理解与验证 | 子代理审查 | 缺少"不理解就不要接受"的硬性约束 |
| 3. 安全与保密 | ❌ 缺失 | **需要新增** |
| 4. 代码质量 | global.md 有编码规范 | 缺少 lint/format 检查步骤 |
| 5. 人主导设计 | Aegis_Protocol 有审核步骤 | 可以更明确人机分工 |
| 6. 持续改进 | DevLog → TechStack 闭环 | 已有，但缺少定期回顾机制 |