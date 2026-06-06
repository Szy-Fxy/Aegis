# Cursor Rules / AGENTS.md / Claude Code 斜杠命令 — 规则文件最佳实践

## 原始来源
- [AGENTS.md 完整指南](https://www.morphllm.com/agents-md-guide) — AGENTS.md 规范、SKILL.md 定义、与 CLAUDE.md/.cursorrules 对比
- [AGENTS.md 研究数据](https://arxiv.org/abs/2601.20404) — Princeton 研究：AGENTS.md 减少 28.6% 运行时间、16.6% Token 消耗
- [Cursor Rules 配置指南](https://cursor.zone/faq/cursor-rules-configuration-guide.html) — 4 种规则类型（Always/Auto/Agent/Manual）、.mdc 文件格式
- [Claude Code 自定义斜杠命令](https://docs.claude.com/en/docs/claude-code/slash-commands) — 官方文档：项目命令 vs 个人命令、参数、Bash 执行
- [Claude Code Slash Commands 参考](https://dotclaude.com/commands) — 30+ 内置命令、自定义命令结构、Frontmatter 配置

## 审查结论
- ✅ **可复用 — AGENTS.md 的六段式结构**：构建命令、代码风格、项目结构、测试说明、边界约束、依赖管理
- ✅ **可复用 — AGENTS.md 核心原则**：写可复制的命令而非模糊工具名、写真实代码片段而非描述性散文、写显式边界而非隐式假设
- ✅ **可复用 — Cursor Rules 的四种触发模式**：Always / Auto Attached / Agent Requested / Manual，Aegis 可借鉴为规则分级
- ✅ **可复用 — Claude Code 斜杠命令的项目级配置**：`.claude/commands/` 目录，Aegis 可创建类似目录结构
- ⚠️ **有条件可用 — .mdc 文件格式**：Cursor 专用，但 glob patterns 按文件模式触发规则的思路可借鉴

## 关键要点

### 1. AGENTS.md — 跨平台 AI 编码代理的上下文标准

**研究数据**（Princeton 大学，124 个 PR，10 个仓库）：
- 运行时间中位数减少 **28.6%**（98.6s → 70.3s）
- Token 输出中位数减少 **16.6%**（2,925 → 2,440）
- 原因：AGENTS.md 提供了上下文，代理跳过了探索性步骤

**关键发现**：
- 人类写的 AGENTS.md 有效（成功率提升 ~4%）
- LLM 生成的 AGENTS.md 反而有害（增加 23% 成本，降低成功率）
- **结论**：好的 AGENTS.md 有帮助，但充满冗余信息的自动生成版本有害

**六段式结构**（GitHub 工程团队分析 2,500+ 仓库）：
1. **构建与测试命令**：精确命令 + 参数。`uv run pytest tests/unit/ -v`，而非"运行测试"
2. **代码风格规则**：仅写与语言默认不同的规则。"只用命名导出，不用默认导出"
3. **项目结构**：目录到职责的映射。`/src/api/` 是路由处理器（薄层，委托给 services）
4. **测试说明**：测试运行器、如何运行单个测试、mock 什么不 mock 什么
5. **边界约束**：代理绝对不能碰的文件或目录
6. **依赖管理**：使用的包管理器、版本锁定策略

**核心原则**：
- 写可复制的命令，而非模糊的工具名
- 写真实的代码片段，而非描述性散文
- 写显式边界，而非隐式假设

**目录层级**：AGENTS.md 可存在于多个目录级别，代理读取离被编辑文件最近的那个。

### 2. Cursor Rules — 四种触发模式

| 类型 | 触发方式 | 适用场景 |
|---|---|---|
| **Always** | 所有 AI 交互自动加载 | 全局编码规范 |
| **Auto Attached** | 匹配 glob pattern 的文件被引用时自动激活 | 特定文件类型的规则 |
| **Agent Requested** | AI 根据描述判断是否需要 | 按需使用的规则 |
| **Manual** | 用户明确提到时才激活 | 模板、参考文档 |

**.mdc 文件格式**：
```
---
description: 规则描述
globs: src/**/*.tsx,src/**/*.jsx
alwaysApply: false
---

# 规则内容（Markdown）
```

**命名建议**：数字前缀控制优先级
- 001-099：核心规则
- 100-199：集成规则
- 200-299：模式规则

**对 Aegis 的启发**：Aegis 的 global.md 相当于 Always 类型，可以引入 Auto Attached 类型的规则（按文件类型自动应用不同规则）。

### 3. Claude Code 自定义斜杠命令

**目录结构**：
```
.claude/commands/       # 项目级命令（最高优先级）
~/.claude/commands/     # 个人命令（跨项目）
```

**命令文件结构**：
```markdown
---
description: 运行测试套件
allowed-tools: Bash
argument-hint: test-pattern
---

执行测试：!`npm test -- $ARGUMENTS`
```

**参数系统**：
- `$ARGUMENTS`：所有参数
- `$1`, `$2`, `$3`：位置参数
- `!`command``：执行 Bash 命令
- `@filename`：引用文件内容

**Frontmatter 配置**：
| 字段 | 必填 | 说明 |
|---|---|---|
| `description` | 否 | 命令描述 |
| `allowed-tools` | 否 | 允许的工具（Bash, Read, Grep, Edit 等） |
| `argument-hint` | 否 | 参数提示 |
| `disable-model-invocation` | 否 | 禁止 AI 模型自动调用此命令 |

**对 Aegis 的启发**：Aegis 可以创建类似 `.claude/commands/` 的目录结构，存放常用的 AI 工作流命令。

### 4. AGENTS.md vs CLAUDE.md vs .cursorrules 对比

| 维度 | AGENTS.md | CLAUDE.md | .cursorrules |
|---|---|---|---|
| 标准化程度 | 跨平台标准（Agentic AI Foundation） | Claude Code 专用 | Cursor 专用 |
| 工具支持 | 20+ 编码代理 | Claude Code | Cursor |
| 目录层级 | 支持多级 | 项目根目录 | 项目根目录 |
| 格式 | 纯 Markdown | 纯 Markdown | Markdown + YAML frontmatter |
| 触发模式 | 自动 | 自动 | 4 种模式 |

**趋势**：AGENTS.md 正在成为跨平台标准，建议 Aegis 在项目根目录提供 AGENTS.md。

### 5. 对 Aegis 规则体系的优化建议

基于上述研究，Aegis 的规则体系可以优化：

1. **引入规则分级**：借鉴 Cursor 的四种触发模式，将 Aegis 规则分为：
   - Always（如 global.md）
   - Auto（按文件类型，如 `.tsx` 触发 React 规则）
   - On-Demand（如子代理审查规则）

2. **补充 AGENTS.md**：在项目根目录添加 AGENTS.md，包含构建命令、测试命令、项目结构、边界约束

3. **创建斜杠命令目录**：为常用 Aegis 工作流创建 `.claude/commands/` 或类似目录

4. **命令标准化**：所有命令写精确的可执行命令，而非模糊描述