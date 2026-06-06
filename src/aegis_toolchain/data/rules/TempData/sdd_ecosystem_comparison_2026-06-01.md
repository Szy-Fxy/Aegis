# SDD 生态系统对比 — Spec Kit / OpenSpec / BMAD / SPARC

## 原始来源
- [GitHub Spec Kit](https://github.com/github/spec-kit) — GitHub 官方 SDD 工具包，Python CLI，五阶段工作流
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) — 51.9K Stars，最轻量级 SDD 框架，Node.js CLI
- [BMAD Method](https://bmadcodes.com/bmad-method/) — 多智能体敏捷开发框架，两阶段 AI-first 流程
- [SPARC Framework](https://github.com/ruvnet/sparc) — 规范→伪代码→架构→细化→完成，Prompt 工程方法论
- [SDD 生态全景分析](https://arceapps.com/blog/spec-driven-development-ai/) — 六大 SDD 框架对比，包含生产级 Spec 解剖
- [SDD 工业工具对比](https://www.marvinzhang.dev/blog/sdd-tools-practices) — 四类 SDD 解决方案（Toolkit/IDE/Platform/Framework）

## 审查结论
- ✅ **可复用 — Spec Kit 的宪法机制（constitution.md）**：项目级不可协商原则，可作为 Aegis global.md 的增强版
- ✅ **可复用 — OpenSpec 的 Delta 规范（Spec Delta）**：变更前后对比，用于存量项目变更管理
- ✅ **可复用 — OpenSpec 的 changes/ 与 specs/ 分离**：当前状态与变更提案分离，清晰的变更管理模型
- ⚠️ **有条件可用 — BMAD 的多智能体编排**：PM→Architect→SM→Dev→QA 专精分工，Aegis 子代理可借鉴
- ⚠️ **有条件可用 — Spec Kit 的 /clarify 命令**：强制消除 spec 中的 [NEEDS CLARIFICATION] 标记
- ❌ **暂不可用 — BMAD 的 CLI + Web UI**：依赖 Node.js 生态，与 Aegis 纯 Markdown 理念冲突

## 关键要点

### 1. SDD 生态四类解决方案

| 类别 | 代表 | 特点 | 适合场景 |
|---|---|---|---|
| **Toolkit（工具包）** | Spec Kit, OpenSpec | 集成到现有 IDE，最大灵活性 | 有强工具偏好的团队 |
| **IDE（集成环境）** | AWS Kiro | SDD 内建于 IDE 核心 | 绿场项目，追求一体化体验 |
| **Platform（平台）** | Tessl | Spec-as-Source，AI 生成所有代码 | 长期项目，spec 质量优先 |
| **Framework（框架）** | BMAD, AG2 | 自定义多智能体工作流 | 复杂项目，需合规/质量门 |

Aegis 属于 **Toolkit 类别**，与 Spec Kit 和 OpenSpec 定位最接近。

### 2. GitHub Spec Kit — 五阶段结构化工作流

```
📋 constitution → 📝 specify → 🎯 plan → ✅ tasks → 🚀 implement
   (项目原则)      (需求规范)    (技术方案)   (任务拆分)    (代码实现)
```

**核心命令**：
| 命令 | 作用 | Aegis 对应 |
|---|---|---|
| `/speckit.constitution` | 建立项目不可协商原则 | global.md |
| `/speckit.specify` | 从自然语言生成 spec.md | 00-MetaSpec |
| `/speckit.clarify` | 消除 spec 中的模糊标记 | 01-brainstorm |
| `/speckit.plan` | 生成技术方案 plan.md | 03-design |
| `/speckit.tasks` | 拆分为可执行任务 tasks.md | 05-tasks |
| `/speckit.analyze` | 一致性检查（宪法+spec+plan 三方对齐） | 子代理审查 |
| `/speckit.implement` | 执行任务实现代码 | 06-implement |

**宪法（constitution.md）的关键内容**：
- 安全与合规：认证、数据处理、日志、PII、加密
- 编码规范：命名、目录结构、代码风格
- 架构规则：接口优先、简单性、集成测试优先
- 组织策略：已批准服务、地理限制、禁用库、许可证

**对 Aegis 的启发**：Aegis 的 global.md 缺少「安全与合规」和「组织策略」维度，可以引入类似 constitution 的概念。

### 3. OpenSpec — 最轻量级 SDD，存量项目优先

**设计哲学**：流动而非僵化、迭代而非瀑布、简单而非复杂、存量项目优先

**三阶段工作流**：
```
/opsx:new → /opsx:ff → /opsx:apply → /opsx:archive
 (创建变更)  (生成规划)  (实现)        (归档)
```

**核心创新：Spec Delta 格式**
```
# 变更前
- The system SHALL expire sessions after a configured duration.
# 变更后
+ The system SHALL support configurable session expiration periods.
```
- `-` 表示移除的需求
- `+` 表示新增的需求
- 审查者无需翻代码，直接从 spec delta 看懂变更意图

**目录结构**：
```
openspec/
├── specs/          # 当前已实现的能力（单一事实来源）
│   └── auth-session/spec.md
├── changes/        # 变更提案
│   ├── add-dark-mode/
│   │   ├── proposal.md
│   │   ├── design.md
│   │   ├── tasks.md
│   │   └── specs/  # spec delta
│   └── archive/    # 已完成变更归档
```

**对 Aegis 的启发**：
1. Aegis 的 Aegis_Specs 目录可以借鉴 OpenSpec 的 `specs/` + `changes/` 分离模型
2. Spec Delta 格式可以用于 Aegis 的变更追踪，让用户快速理解改了什么
3. OpenSpec 的「存量项目优先」哲学与 Aegis 的定位一致

### 4. BMAD Method — 多智能体专精分工

**两阶段流程**：
- Phase 1 规划：Analyst → PM → Architect → PRD + 架构文档
- Phase 2 执行：Scrum Master → Dev → QA → 代码实现

**智能体分工**：
| 智能体 | 职责 | 产出 |
|---|---|---|
| Analyst | 市场研究、竞品分析 | 项目简报 |
| PM | 需求转化 | PRD、用户故事、成功指标 |
| Architect | 系统设计 | 架构图、技术栈、DB Schema、API Spec |
| Scrum Master | 任务拆分 | 超详细实现 Story（含架构上下文+实现指南+测试标准） |
| Dev | 代码实现 | 一次一个 Story |
| QA | 代码审查 | 质量重构、测试验证 |

**核心创新：Context-Engineered Story Files**
每个 Story 文件包含：
- 完整架构上下文 → 不需要 Dev agent 自己去查
- 实现指南 → 明确怎么做
- 内嵌推理：What、Why、How → 零上下文丢失
- 测试标准 → QA agent 知道验证什么

**对 Aegis 的启发**：BMAD 的「Story 文件 = 架构上下文 + 实现指南 + 测试标准」模式可以让 Aegis 的 tasks.md 模板更丰富，不仅记录任务清单，还包含实现上下文。

### 5. SPARC — Prompt 工程方法论

```
S - Specification:  定义问题和约束
P - Pseudocode:     语言无关的逻辑表达
A - Architecture:   组件和数据布局设计
R - Refinement:     与 AI 的迭代审查循环
C - Completion:     最终集成、测试和文档
```

SPARC 更偏向 Prompt 工程纪律而非项目框架，教开发者如何结构化地与 AI 交互。

### 6. Aegis 在 SDD 生态中的定位

| 维度 | Spec Kit | OpenSpec | BMAD | **Aegis** |
|---|---|---|---|---|
| 复杂度 | 中高 | 低 | 高 | 中 |
| 依赖 | Python CLI | Node.js CLI | Node.js | 无（纯 Markdown） |
| 阶段门控 | 严格 | 宽松 | 严格 | 灵活（L1/L2/L3 分级） |
| 存量项目 | 一般 | **优秀** | 一般 | 优秀 |
| 多智能体 | 无 | 无 | **核心** | 子代理审查 |
| 反借口机制 | 无 | 无 | 无 | 计划引入 |
| 学习曲线 | 中 | 低 | 高 | 低-中 |

**Aegis 的差异化优势**：
1. 零依赖 — 纯 Markdown，无需安装任何 CLI 工具
2. 需求分级 — L1/L2/L3 灵活应对不同复杂度
3. 子代理审查 — 内置唱反调、备选方案、UX 审查
4. 持续进化 — DevLog + TempData → TechStack 提炼闭环