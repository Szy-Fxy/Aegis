---
name: "dev-workflow"
description: "Aegis 开发工作流核心引擎。定义需求分级(L1/L2/L3)、阶段流程、规则加载、进程恢复、TempData 管理、DevLogs 记录等全部工作流规则。"
---

# 开发工作流引擎 v3.0.7

## 概述

本文件是 Aegis 开发工作流的核心引擎。它定义了 AI 从接收到需求到完成交付的完整流程，包括需求分级、阶段规范、规则加载、进程恢复和收尾仪式。

**核心设计原则**：不同规模的需求走不同深度的流程，避免一刀切。简单修复不应被过度流程阻碍，大型重构不应被简化流程导致失控。

---

## 规则加载协议

### 加载顺序

```
1. Aegis/rules/global.md                      → 全局通用准则（始终加载）
2. Aegis/rules/TechStack/{匹配的技术栈}.md      → 技术栈规范
3. 项目根目录 AGENTS.md / README.md             → 项目级入口规则
```

### 技术栈自动匹配

AI 根据需求关键词自动匹配技术栈文件，加载对应规则：

| 需求关键词 | 对应技术栈 |
|--------|----------|
| Unity/C#/MonoBehaviour/GameObject | `TechStack/unity.md` |
| Python/Django/FastAPI/pytest/数据处理 | `TechStack/python.md` |
| TypeScript/React/Vue/Node/Express/前端/Web | `TechStack/typescript.md` |
| Unreal/UE5/Blueprint/Actor | `TechStack/unreal.md` |
| C++/CMake/vcpkg/引擎/底层/UE | `TechStack/cpp.md` |
| Go/Golang/gRPC/并发/云原生 | `TechStack/go.md` |
| Rust/Cargo/tokio/actix/系统编程 | `TechStack/rust.md` |
| Java/Spring Boot/Maven/Gradle/Kotlin | `TechStack/java.md` |
| Docker/容器/K8s/k8s/镜像/部署 | `TechStack/docker.md` |

### 技术栈缺失时的处理

当 AI 发现需求涉及的技术栈在 TechStack 中不存在时：

```
1. [搜索阶段] 上网搜索该技术栈的最佳实践和编码规范
   - 优先搜索官方文档和知名社区（GitHub、Stack Overflow）
   - 记录搜索来源链接和关键摘要
   - 项目自有代码库优先于外部资料
2. [审查阶段] 用审查代理验证搜索结果的质量和适用性
   - 是否来自可靠来源（官方文档 > 知名技术博客 > 社区讨论）
   - 是否与项目现有代码风格一致
   - 是否有明显过时或错误
3. [暂存阶段] 审查通过后暂存到 TempData
   Aegis/rules/TempData/{技术栈名}_research_{YYYY-MM-DD}.md
   命名格式见 conventions/naming-and-formats.md

4. [提炼阶段] 功能开发完成后提炼核心要点写入 TechStack
   Aegis/rules/TechStack/{技术栈名}.md
   提炼标准见 conventions/naming-and-formats.md 中「提炼到 TechStack 的标准」
5. [清理阶段] 确认 TempData 中的资料已提炼或不再需要后清理
   清理规则见 naming-and-formats.md 中「清理规则」
```

### TempData 使用规范

存放开发过程中临时查找的资料，经审查代理验证后暂存于此。命名格式和完整规范见 `conventions/naming-and-formats.md`。

**关键原则**：
- TempData 是临时缓存，不是永久知识库
- 技术栈知识最终要提炼到 TechStack，而非长期留在 TempData
- 提炼时遵循「广泛通用」原则：写入 TechStack 的是通用知识，不是具体实现
- 提炼标准：概念 + 参考链接 + 常见陷阱，不超过 TechStack 原文件的 30%

---

## 进程状态管理（Process State）

每次对话按以下流程恢复上下文：

```
1. 读取 Aegis/rules/DevLogs/ 下最新日期的 DevLog
2. 检查 DevLog 中的「当前进度」+「下一动作」+「步骤 N.当前状态」
3. 如果 DevLog 为空或信息不足，检查 Aegis_Specs/INDEX.md 是否有未完成的需求
4. 告知用户上次进度：「上次您在 {需求名} 的 {阶段}，是否继续？」
```

DevLog 命名格式见 `conventions/naming-and-formats.md`。日志必须包含当前进度、下一动作、步骤状态标记和时间戳，确保跨会话断点续传。

---

## 需求分级

### AI 判定需求等级的规则

AI 根据需求特征自动判定 L1/L2/L3，并在对话中告知用户判定结果：

```
判定维度          →     L1         →     L2         →     L3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
影响范围/涉及文件数  →  1 个文件      →  2-5 个文件    →  5+ 个文件
单行改值/配置调整    →  L1           →  L1           →  L2
新增 API / Bug 修复  →  L2           →  L2           →  L3
模块重构/架构调整    →  L2           →  L3           →  L3
跨模块改造           →  —            →  L3           →  L3
安全相关             →  L2           →  L3           →  L3
跨技术栈/数据库 schema →  L2           →  L3           →  L3
性能优化/算法替换     →  L2           →  L2           →  L3
第三方 SDK 集成      →  L2           →  L2           →  L3
```

### 判定兜底

判定优先级：安全相关 > 跨模块/跨技术栈 > 文件数量 > 功能复杂度。当判定标准模糊时，向上取整（L1→L2 模糊时取 L2），确保不会因流程过轻而遗漏关键步骤。

---

## 需求索引管理

### Aegis_Specs/INDEX.md

需求索引格式见 `conventions/naming-and-formats.md`。INDEX.md 的维护规则：
- 新需求登记时立即更新 INDEX.md
- 同时只有一个需求处于 `🔨 implementing`
- L1 需求可插队执行，不阻塞当前 L2/L3
- L3 过程中收到 L2 需求：完成后从 DevLog 恢复 L3 进度

---

## L1 极轻量需求  — 快速通道

```
需求确认 → AI 直接修改代码 → 展示改动摘要 → 等用户确认
```

**规则**：
- 不生成 Markdown 文档
- 修改完成后展示**改动摘要**（修改的文件路径 + 增删行数 + 改动点简述），**不得擅自执行任何 git/svn 操作**
- 必须记录 DevLog 到 Aegis/rules/DevLogs/，并在 Aegis_Specs/INDEX.md 中将需求状态更新为 ✅ done（即使是 L1 需求也必须记录）

### 反借口表

| AI 可能的借口 | 反驳 |
|---|---|
| "这个改动小，我顺便优化一下别的" | 不。精准修改。只改需求范围的代码。 |
| "一个文件而已，不需要展示改动摘要" | 不。任何修改必须展示改动摘要。 |
| "很简单不需要确认" | 不。修改后必须等用户确认。 |
| "我用 git add/commit 帮你先暂存" | 不。**不得擅自执行任何 git/svn 操作**，除非用户明确要求。 |
| "L1 不需要写 DevLog" | 不。即使是 L1，也须记录 DevLog 和更新 INDEX.md。 |

---

## L2 标准需求 — 3 阶段（不可跳过任何阶段）

```
阶段 [1/3] 方案设计 → 阶段 [2/3] 实现 → 阶段 [3/3] 验证 + 收尾
```

### 阶段 L2-1：方案设计

```
Step 1: 创建 Aegis_Specs/L2/{feature-name}/design.md（模板见 templates/spec-L2.md）
Step 2: 在聊天中向用户展示方案内容
Step 3: 等待用户明确确认（如 "OK"、"可以"、"go ahead"）
```

**BOUNDARY CHECK**（用 `read` 工具确认）：
- [ ] `Aegis_Specs/L2/{feature-name}/design.md` 存在？
- [ ] 用户已明确确认？

**任一不满足 → STOP。不进入 L2-2。**

### 阶段 L2-2：实现

```
Step 1: 按 design.md 写代码
Step 2: 运行 typecheck / lint / build 验证
Step 3: 向用户展示改动摘要（修改的文件路径 + 增删行数 + 改动点简述）
Step 4: 等待用户确认（**不得擅自执行任何 git/svn 操作**）
```

**BOUNDARY CHECK**（用 `read` 工具确认）：
- [ ] 代码编译通过 / lint 无报错？
- [ ] 改动摘要已展示给用户？

**任一不满足 → 修复后重新验证，不进入 L2-3。**

### 阶段 L2-3：验证 + 收尾

```
Step 1: 更新 Aegis_Specs/INDEX.md（标记为 ✅ done）
Step 2: 写 DevLog 到 Aegis/rules/DevLogs/
Step 3: 告知用户完成
```

**BOUNDARY CHECK**（用 `read` 工具确认）：
- [ ] `Aegis_Specs/INDEX.md` 已更新？
- [ ] `Aegis/rules/DevLogs/` 有新条目？

**任一不满足 → 补全后再声明完成。**

### 阶段边界检查（强制）

L2 的每个阶段之间，AI 必须停止并验证：

```
□ 前一阶段要求的文件是否存在？（用 read 工具确认）
□ 缺少文件 → 退回前一阶段补文件，不前进
□ 所有文件齐备 → 进入下一阶段
```

### 失败恢复

如果 AI 发现跳过了某个阶段或文件未创建：

```
STOP。不要继续。
创建缺失的文件。
告知用户："上一阶段缺少 [文件名]，已补创建。可以继续。"
确认无误后才继续。
```

### 反借口表

| AI 可能的借口 | 反驳 |
|---|---|
| "L2 不需要 design.md，直接写代码就行" | 不。L2 的 design.md 就是轻量 spec。没有它就没有验收标准，也跳过了 BOUNDARY CHECK。 |
| "方案很明显，不需要等确认" | 不。用户可能看到你没看到的约束。BOUNDARY CHECK 要求用户确认。 |
| "BOUNDARY CHECK 太啰嗦，跳过" | 不。BOUNDARY CHECK 是唯一防止阶段跳跃的机制。跳过它 = L2 流程形同虚设。 |
| "验证通过了就行" | 不。确保覆盖了边界条件和错误路径。 |
| "代码写完了 = L2-3 自动完成" | 不。INDEX.md 更新 + DevLog 写入是独立步骤，不可省略。 |

---

## L3 重型需求  — 7 阶段

```
阶段 [1/7] 头脑风暴 → 阶段 [2/7] 提案 → 阶段 [3/7] 技术设计 → 阶段 [4/7] 需求规格 → 阶段 [5/7] 任务拆分 → 阶段 [6/7] 集成审核 → 阶段 [7/7] 实现验证 → 收尾仪式 + DevLog
```

### 阶段 L3-1：头脑风暴

输出 `Aegis_Specs/L3/{feature-name}/01-brainstorm.md`，模板见 `templates/brainstorm.md`。

### 阶段 L3-2：提案

输出 `Aegis_Specs/L3/{feature-name}/02-proposal.md`，模板见 `templates/proposal.md`。

**验收标准同步**：proposal 中的验收标准将被摘录到 05-tasks.md 和 07-verify.md 顶部，确保用户验收时无需翻回 02。AI 在编写 proposal 时必须确保验收标准是具体可度量的。

### 阶段 L3-3：技术设计

输出 `Aegis_Specs/L3/{feature-name}/03-design.md`，模板见 `templates/design.md`。

### 阶段 L3-4：需求规格

输出 `Aegis_Specs/L3/{feature-name}/04-spec.md`，模板见 `templates/spec-L3.md`。

**00-MetaSpec 的关系**：对于 L3 重构类需求，在阶段 1 之前先产出 `00-{MetaSpec}.md`，模板见 `templates/meta-spec.md`。00 定义「宪法」— 跨批次、跨模块的不可妥协约束。04-spec 是「法律」— 当前批次的具体功能需求。04 不能违反 00，冲突时以 00 为准。

### 阶段 L3-5：任务拆分

输出 `Aegis_Specs/L3/{feature-name}/05-tasks.md`，模板见 `templates/tasks.md`。

### 阶段 L3-6：集成审核

输出 `Aegis_Specs/L3/{feature-name}/06-review.md`，模板见 `templates/review.md`。

**子代理审查流程**：AI 在写 06-review.md 之前，必须启动以下子代理审查：

  a) **审查纠错子代理**：检查技术设计与 spec 的一致性，检查 API 签名是否合理，检查是否有遗漏的边界条件

  b) **唱反调子代理**：质疑设计决策，寻找更简单的替代方案，指出潜在的过度设计。子代理定义见 `sub-agents/devils-advocate.md`

  c) **备选方案子代理**：对照 brainstorm 中的方案，确认选定方案是否最优，提供 GitHub 上类似问题的解决方案作为参考

  d) **用户体验子代理**：从用户视角审查验收标准是否清晰，检查文档是否包含用户需要的信息（验收标准速查表），确保用户不需要查看技术细节就能验收

- 子代理审查结果写入 06-review.md 的「交叉检查」部分
- 审查发现的问题必须在进入阶段 7 之前解决
- 审查过程要点记录到 DevLog

### 阶段 L3-7：实现验证

1. AI 按 `05-tasks.md` 逐任务实现代码
2. AI 运行 lint → typecheck → build → test
3. 输出 `07-verify.md`，模板见 `templates/verify.md`

### 迭代退回机制

L3 流程支持在任意阶段退回到上一个阶段。退回规则：

```
需求阶段 N 退回 → 阶段 N 的文档标记为 .deprecated
     ├── 阶段 1 ~ (N-1) 的文档保持不变
     ├── 阶段 N 需要重新产出
     ├── 阶段 (N+1) ~ 最终 的文档全部加 .deprecated 标记
     └── 重新开始推进
```

AI 在退回时保留已通过的文档不变，后续文档加 `.deprecated` 标记，不会丢失数据。

### 反借口表

| AI 可能的借口 | 反驳 |
|---|---|
| "这个功能很复杂，不需要 brainstorm，我直接写方案" | 不。复杂功能更需要 brainstorm 来探索多种方案。 |
| "proposal 和 spec 差不多，合并写一个就行" | 不。proposal 是方案决策（选哪个），spec 是需求规格（做什么）。职责不同。 |
| "design 模板太简单了，我口头说明就行" | 不。design 必须文档化，包含 API 签名、数据流、保留项。 |
| "spec 太长，AI 生成质量差，跳过吧" | 不。spec 是 AI 实现代码的唯一依据。没有 spec 就没有验收标准。 |
| "review 我自己看一遍就行，不需要子代理" | 不。同一个 AI 难以同时切换"生成模式"和"审查模式"。子代理分离视角。 |
| "测试都通过了，发布吧" | 不。通过 ≠ 充分。覆盖了边界条件吗？安全路径呢？ |
| "只是个小改动，不需要子代理审查" | 不。小改动造成大事故。每一行都要审查。 |
| "用户已经口头确认了，不用写 verify.md" | 不。口头确认不能替代文档。verify.md 是验收的唯一凭证。 |

---

## 阶段边界检查（全局强制）

无论是 L2 还是 L3，每个阶段之间 AI 必须执行以下检查：

```
□ 前一阶段要求的文件是否存在？（用 read 工具确认）
□ 缺少文件 → 退回前一阶段补文件，不前进
□ 所有文件齐备 → 进入下一阶段
```

## 失败恢复（全局）

如果 AI 在任何阶段发现跳过了某个步骤或文件未创建：

```
STOP。不要继续。
创建缺失的文件。
告知用户："上一阶段缺少 [文件名]，已补创建。可以继续。"
确认无误后才继续。
```

---

## 收尾仪式（Close-out）

L3 需求全部完成后，AI 必须执行以下收尾步骤：

```
□ 0. 文档完整性检查（逐阶段回溯 — 口头确认不能替代）：
     □ Aegis_Specs/L3/{name}/01-brainstorm.md 存在？
     □ Aegis_Specs/L3/{name}/02-proposal.md 存在？
     □ Aegis_Specs/L3/{name}/03-design.md 存在？
     □ Aegis_Specs/L3/{name}/04-spec.md 存在？
     □ Aegis_Specs/L3/{name}/05-tasks.md 存在？
     □ Aegis_Specs/L3/{name}/06-review.md 存在？
     □ Aegis_Specs/L3/{name}/07-verify.md 存在？  ← 最容易被遗漏的
     → 缺失的立刻补写，不补写不进下一步

□ 1. 写 DevLog 到 Aegis/rules/DevLogs/（含背景、改动清单、提交记录、教训）
     → 如果 DevLog 写入失败（权限问题等），AI 必须告知用户并建议手动记录

□ 2. 更新 Aegis_Specs/INDEX.md 将需求状态改为 ✅ done
     → 如果 INDEX.md 不存在，AI 必须创建它
     → 如果 INDEX.md 更新失败，AI 必须告知用户当前状态

□ 3. TempData 清理：检查本次需求相关的 TempData 文件，提炼到 TechStack 或删除
     → 提炼标准见 naming-and-formats.md
     → 不需要提炼的（一次性的、网上已有权威文档的）直接删除
     → 如果清理失败，告知用户建议手动清理

□ 4. 5 维审视：从目录结构、文档职责边界、流程冗余/缺失、AI 误解风险、用户认知负担五方面审查
     → 审视结果记录到 DevLog 的「教训」section

□ 5. 告知用户项目完成，总结本次需求的全过程
```

---

## 更新日志

| 日期 | 版本 | 改动 |
|------|------|------|
| 2026-05-31 | v3.0 | 路径重构、SKILL.md 拆分、进程恢复、迭代退回、收尾仪式、并发 INDEX |
| 2026-06-01 | v3.0.4 | 收尾加步骤 0 文档完整性检查；各阶段新增反借口表；L3-6 子代理审查落地 |
| 2026-06-02 | v3.0.5 | 文件结构重构：根目录 .md 移入 docs/；移除内置 .cursor；新增 .trae/rules/ 入口；安装选项扩至 7 个；Boot Skill 改为兜底方案；INDEX.md 模板加状态说明；版本号全局统一 |
| 2026-06-02 | v3.0.5 | Hotfix：Set-Content 全体加 -Encoding UTF8（解决中文乱码）；install-aegis.ps1 TechStack 补全至 9 个 |
| 2026-06-02 | v3.0.5 | 自举规范化：建立 CHANGELOG.md + BOOTSTRAP.md；INDEX.md 恢复纯模板；子代理增加「大白话」讲解；模板补全并发规则 |
| 2026-06-02 | v3.0.6 | L2 强化：每阶段增加 BOUNDARY CHECK + 失败恢复 + 阶段边界检查；aegis-boot 全面升级（MANDATORY SEQUENCE + 可执行边界检查）；全局版本号 3.0.5 → 3.0.6 |
| 2026-06-03 | v3.0.6 | 规则改进：L1/L2 diff 展示改为改动摘要 + 不得擅自执行 git/svn；反借口表同步更新 |
| 2026-06-03 | v3.0.7 | 版本号规范化：采用 L1→patch / L2→minor / L3→major 规则；全局版本号 3.0.6 → 3.0.7 |