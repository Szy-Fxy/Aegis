# Aegis v3.0.5

## AI Development Governance System

> 规范驱动 · 设计先行 · 验证闭环 · 持续进化

---

# 项目简介

Aegis 是一套面向 AI 编程助手的开发治理系统（AI Development Governance System）。

它的目标不是让 AI 写代码更快，而是确保 AI 以可审计、可追溯、可维护的软件工程方式进行开发。

Aegis 通过需求分级、规格驱动、设计评审、任务拆分、验证闭环和经验沉淀等机制，为 AI 提供明确的工程约束，避免需求偏移、设计失控和代码质量下降等问题。

---

# 核心理念

传统 AI Coding Assistant 关注的是：

```text
更快写代码
```

Aegis 关注的是：

```text
更正确地开发软件
```

Aegis 认为：

- 编码只是软件开发过程中的一个环节
- 需求分析比编码更重要
- 设计质量决定系统上限
- 验证机制决定最终质量
- 经验沉淀决定长期效率

因此：

```text
需求
 ↓
规格
 ↓
设计
 ↓
任务
 ↓
实现
 ↓
验证
 ↓
沉淀
```

应形成完整的软件工程闭环。

---

# 项目使命（Mission）

> Not to make AI write code faster,
> but to ensure AI develops software through structured, auditable and maintainable engineering workflows.

中文：

> Aegis 的目标不是让 AI 写代码更快，
> 而是确保 AI 通过结构化、可审计、可维护的软件工程流程进行开发。

---

# 核心目标

## 1. 规范驱动

所有开发活动必须基于明确规范进行。

避免：

- 边开发边设计
- 需求理解偏差
- AI 自行扩展需求

## 2. 设计先行

先完成设计，再进入编码。

避免：

- 边写边改
- 架构失控
- 技术债快速累积

## 3. 验证闭环

所有需求都必须具备明确验收标准。

确保：

- 功能正确
- 行为符合预期
- 变更可验证

## 4. 持续进化

Aegis 本身也是持续进化的系统。

每次开发结束后：

- 总结经验
- 修正规范
- 优化模板
- 沉淀最佳实践

使工作流不断完善。

---

# 工作流架构

## L1 - 极轻量需求

适用于：

- 小型修复
- 配置调整
- 简单改动
- 单文件单行修改

流程：

```text
需求
 ↓
确认
 ↓
实现
 ↓
Diff Review
```

**输出**：无文档，仅 git diff

---

## L2 - 标准需求

适用于：

- 功能开发
- 模块优化
- 普通重构
- Bug 修复（有明确复现路径）

流程：

```text
需求引导
 ↓
方案设计（合并文档：背景+目标+非目标+接口+验收场景）
 ↓
实现
 ↓
验证 + 开发日志
```

**输出**：`design.md`（8 段式合并文档）+ `verify.md` + DevLog

---

## L3 - 重型需求

适用于：

- 大型功能
- 架构重构
- 跨模块改造
- 跨技术栈
- 安全相关

流程：

```text
需求引导
 ↓
Brainstorm（问题探索）
 ↓
Proposal（方案提案）
 ↓
Design（技术设计）
 ↓
Spec（需求规格）
 ↓
Tasks（任务拆分）
 ↓
Review（集成审核）
 ↓
Implementation（AI 执行代码）
 ↓
Verify（验证闭环）
 ↓
DevLogs（经验沉淀）
```

**输出**：`01-brainstorm.md` ~ `07-verify.md` + DevLog

---

# 需求输入引导

用户不必写出完美需求。AI 在进入分级判定之前，先帮助用户把需求讲清楚：

```
AI: 我理解你想 [做某件事]。在开始之前，帮我确认几个关键信息：

1. 这个功能是解决什么问题的？（业务背景）
2. 完成后谁会用？怎么用？（用户场景）
3. 有什么绝对不能变的东西吗？（约束条件）
4. 你已经有具体方案了，还是需要我先想几个方案供你选？
```

用户也可以直接按以下模板提交需求：

```markdown
## 需求
[一句话描述要什么]

## 背景
[为什么需要？]

## 约束
- [不能改的东西]
- [必须兼容的东西]
```

---

# 核心原则

> 以下原则指导 Aegis 的日常运行。

## Requirement First

先理解需求，不要直接写代码。

## Specification First

先形成规格说明，不要边开发边确认需求。

## Design Before Code

设计优先于实现，不要让代码成为设计文档。

## Verify Everything

所有需求都必须可验证，无法验证的需求视为不完整。

## Document the Experience

所有经验都应沉淀，避免重复踩坑。

## Rule Loading Protocol

每次对话按以下顺序加载规则：

```
1. global.md              ← 全局通用准则（始终加载）
2. TechStack/{匹配栈}.md   ← 按需加载（Python / Unity / TypeScript / Unreal / C++）
3. docs/Aegis_Protocol.md              ← 项目入口（可能含子项目特定覆盖规则）
```

## One-Click Install

在任何电脑上，一条命令安装 Aegis：

```powershell
irm https://raw.githubusercontent.com/Szy-Fxy/Aegis/main/install.ps1 | iex
```

无需手动复制文件夹。克隆仓库后也可直接复制 `Aegis/` 目录使用。

## Cross-IDE 支持

Aegis 不依赖任何特定 IDE 或 AI 工具。所有规则均为 Markdown 文件：

| 环境 | 入口方式 |
|------|----------|
| Claude Code | `Aegis_Protocol.md`（安装脚本自动生成，含完整行为准则） |
| Cursor | `.cursor/rules/aegis.mdc`（`alwaysApply: true`，自动加载） |
| OpenHanako / OpenCode | `skills/dev-workflow/` 目录（Skill 格式） |
| 其他 AI 工具 | 直接读取 `Aegis/` 下的 Markdown 规则文件 |

## Auto-TechStack Discovery

AI 根据需求关键词自动匹配技术栈文件。如果匹配不到：

```
搜索代理上网查 → 审查代理唱反调验证 → TempData 暂存 → 通过后生成正式 TechStack 文件
```

## Pause & Review

每阶段生成文档后必须暂停，等待用户审核。审核未通过不能进入下一阶段。

## Progress Recovery

AI 在每次对话开始时自动读取最新 DevLog 恢复上下文。日志含时间戳（HH:MM）和当前进度标记，支持跨会话断点续传。

## Concurrent Index

`Aegis_Specs/INDEX.md` 追踪所有需求的状态。同时只有一个需求处于 `🔨 implementing`，L1 可插队不阻塞 L2/L3。

## Rollback Safety

任何阶段可退回上一个阶段。保留已通过的文档不变，后续文档加 `.deprecated` 标记，不会丢数据。

## Close-out Checklist

L3 需求完成后执行 5 步收尾：写日志 → 更新索引 → 清理临时资料 → 5 维审视 → 经验沉淀。每步有兜底失败处理。

---

# 目录结构

```
{项目根目录}/
├── Aegis/                               ← Aegis 核心（可跨项目、跨 IDE 复制）
│   ├── README.md                        ← 项目入口 + 规则索引（GitHub 展示页）
│   ├── install.ps1                      ← 一键安装脚本
│   ├── install-aegis.ps1                ← 跨 IDE 安装脚本
│   ├── .gitignore
│   │
│   ├── docs/                            ← 项目文档
│   │   ├── Aegis_Intro.md               ← 项目介绍文档（本文件）
│   │   ├── Aegis_Protocol.md            ← 强制协议入口
│   │   ├── USER_GUIDE.md                ← 人类用户手册
│   │   └── QUICK_START.md               ← 30 秒快速开始
│   │
│   ├── .cursor/
│   │   └── rules/
│   │       └── aegis.mdc                ← Cursor IDE 自动规则（alwaysApply）
│   │
│   ├── rules/
│   │   ├── global.md                    ← 全局通用准则（SOLID + 安全与合规 + 代码风格）
│   │   ├── TechStack/                   ← 技术栈规范（AI 自动匹配加载）
│   │   │   ├── python.md
│   │   │   ├── unity.md
│   │   │   ├── typescript.md
│   │   │   ├── unreal.md
│   │   │   ├── cpp.md
│   │   │   ├── go.md
│   │   │   ├── rust.md
│   │   │   ├── java.md
│   │   │   └── docker.md
│   │   ├── TempData/                    ← 临时参考资料
│   │   │   └── {主题}_{YYYY-MM-DD}.md
│   │   └── DevLogs/                     ← 开发日志存档
│   │       └── {项目名}_P{两位数字}_{描述}_{YYYY-MM-DD}.md
│   │
│   └── skills/
│       └── dev-workflow/
│           ├── SKILL.md                 ← 核心引擎
│           ├── templates/               ← 阶段文档模板
│           ├── conventions/             ← 命名和格式约定
│           └── sub-agents/              ← 子代理审查定义
│
├── Aegis_Specs/
│   ├── INDEX.md                         ← 需求索引
│   ├── L1/                              ← L1 需求（通常无文档）
│   ├── L2/
│   │   └── {feature-name}/
│   │       ├── design.md
│   │       └── verify.md
│   └── L3/
│       └── {feature-name}/
│           ├── 00-{MetaSpec}.md         ← （可选）重构总规 / 项目级约束
│           ├── 01-brainstorm.md
│           ├── 02-proposal.md
│           ├── 03-design.md
│           ├── 04-spec.md               ← 8 段式需求规格
│           ├── 05-tasks.md
│           ├── 06-review.md
│           └── 07-verify.md
│
└── {项目原有文件}...
```

## 文档职责

| 文档 | 职责 |
|------|------|
| `00-{MetaSpec}.md` | 整个需求的"宪法"— 不可妥协的架构约束和原则 |
| `01-brainstorm.md` | 问题探索与方案发散 |
| `02-proposal.md` | 方案提案与决策 |
| `03-design.md` | 技术设计 |
| `04-spec.md` | 需求规格（8 段式） |
| `05-tasks.md` | 任务拆分 |
| `06-review.md` | 集成审核 |
| `07-verify.md` | 验证结果 |
| `design.md`（L2） | 合并文档（brainstorm + proposal + design + spec 一体） |

## 00-MetaSpec vs 04-spec

| 维度 | 00-MetaSpec.md | 04-spec.md |
|------|----------------|------------|
| 定位 | 宪法 | 法律 |
| 粒度 | 粗 | 细 |
| 覆盖范围 | 跨批次、跨模块 | 当前批次/模块 |
| 何时有 | L3 重构类需求（可选） | 所有 L3 需求（必须） |

**关键规则**：`04-spec.md` 不能违反 `00-MetaSpec.md`，冲突时以 `00` 为准。

---

# TempData 临时资料

存放开发过程中临时查找的资料，经审查代理验证后暂存于此。

- 技术调研的原始搜索结果
- 外部博客/文档的摘要笔记
- 备选方案的对比材料
- 排查 Bug 时查到的链接

命名格式：`{主题}_{YYYY-MM-DD}.md`

注意：TempData 中的资料同样需要经过审查代理验证，确保是可复用的技术栈知识，而非一次性偏方。

---

# DevLogs 开发日志

功能完成后自动写入的详细开发日志。

命名格式：`{项目名}_P{两位数字}_{功能描述}_{YYYY-MM-DD}.md`

示例：
- `My_Fish_01_P01_ProjectRefactor_2026-05-30.md`
- `Aegis_P02_WorkflowOptimization_2026-05-30.md`

日志内容：

- 需求背景
- 问题原因
- 逐步解决过程
- 参考资源链接（博客/知乎/StackOverflow/官方文档）
- 经验教训
- 产出文件清单

---

# 开发治理原则

Aegis 不治理开发者。

Aegis 治理开发过程。

关注：

- 需求是否清晰
- 设计是否合理
- 实现是否符合规范
- 验证是否完整
- 经验是否沉淀

而不是单纯关注代码产出。

---

# 持续改进机制

Aegis 本身按 L3 流程升级自己：

```
用户："我想升级 Aegis 规则"
 → Aegis_Specs/L3/aegis-upgrade/
    ├── 00-Constraints.md     ← 不可改的底线
    ├── 01-brainstorm.md      ← 当前问题
    ├── 02-proposal.md        ← 改什么怎么改
    ├── 03-design.md          ← 新规则长什么样
    ├── 04-spec.md            ← 新规则的验收场景
    ├── 05-tasks.md           ← 改哪些文件
    ├── 06-review.md          ← 审核
    └── 07-verify.md          ← 验证
```

每次需求完成后，AI 主动审视：

| 审视维度 | 具体问题 |
|----------|----------|
| 目录结构 | `Aegis_Specs/` 下是否出现不该放在一起的文件？命名是否一致？ |
| 文档职责边界 | 有没有两份文档写了同一件事？有没有该写的没写？ |
| 流程冗余/缺失 | 有没有某个阶段产出读者从不看？有没有缺一个必要的决策点？ |
| AI 误解风险 | 有没有哪条指令可能在特定条件下被误读？ |
| 用户认知负担 | 有没有某个文档用户明显不想看但被迫审？ |

---

# 最终愿景（Vision）

构建一套能够长期演进的 AI 软件工程体系。

让 AI 从：

```text
Code Generator
```

进化为：

```text
Engineering Partner
```

最终实现：

```text
规范驱动
设计先行
验证闭环
持续进化
```

这就是 Aegis 的价值所在。

---

# 如何判断 Aegis 生效了

这些准则生效的标志：

- **diff 里没有无关改动** — 只出现被请求的修改
- **不再因过度设计重写** — 代码第一次就简洁
- **澄清性问题出现在实现之前** — 而不是出错之后
- **PR 干净精炼** — 没有顺手重构或"优化"
- **DevLog 自动生成** — 每次功能完成后日志自动写入
- **断线重连无缝** — 重新打开 AI 对话，AI 能准确恢复上次进度

---

# 版本历史

| 日期 | 版本 | 改动 |
|------|------|------|
| 2026-05-30 | v1.0 | 初始版本：7 阶段线性流程 |
| 2026-05-30 | v1.1 | 加入 L1/L2/L3 三级分级触发、技术栈自动发现 |
| 2026-05-30 | v1.2 | 分层重构（global + TechStack + TempData + DevLogs） |
| 2026-05-30 | v1.3 | 修复架构原则（完整 SOLID + GoF）+ My_Fish_01 实战测试 |
| 2026-05-30 | v2.0 | 完整 spec 格式 + 00/04 边界 + 需求输入引导 + 持续改进机制 |
| 2026-05-31 | v3.0 | 路径 .trae→Aegis；SKILL.md 拆分；审查双版本；进程恢复；迭代退回；收尾仪式；并发 INDEX；存量代码协作；跨 IDE 安装脚本 |
| 2026-05-31 | v3.0.1 | 四代理审查修复：命名规范化、消除 DRY、矩阵补维度、DevLog 强化、收尾失败处理、用户手册、提炼标准简化、一键安装 |
| 2026-05-31 | v3.0.3 | 命名重构：Aegis_Protocol.md + Aegis_Specs/ + Aegis_Intro.md；安装脚本不复制到项目；强制 Checklist 协议入口 |
| 2026-05-31 | v3.0.4 | L3-7 强化：07-verify 顶部强制验收标准速查表；收尾加步骤 0（文档完整性检查）；05-tasks 加验收对照；Protocol 加文档产出约束 |
| 2026-06-01 | v3.0.4 | Critical 修复：SKILL.md 编码修复（GB2312→UTF-8）；global.md 安全与合规（6 子章节）；4 个子代理审查定义；TechStack 补全 Go/Rust/Java/Docker；design.md 和 spec-L3.md 模板增强；DevLog 标准化 |
| 2026-06-01 | v3.0.5 | 文件结构重构：根目录 .md 文件移入 docs/ 子目录；版本号统一；所有引用路径更新 |
| 2026-05-31 | v3.0.2 | 融合 Karpathy Skills：完整 Aegis_Protocol.md 生成、.cursor/rules/aegis.mdc、Anti-Patterns 速查表、Key Insight 循环验证、README 升级、跨 IDE 支持矩阵、How to Know It's Working |

---

🛡️ Aegis
AI Development Governance System

规范驱动 · 设计先行 · 验证闭环 · 持续进化