---
name: "dev-workflow"
description: "Aegis 开发工作流核心引擎 v5.0.0。定义需求分级(L1/L2/L3)、阶段流程、规则加载、进程恢复、TempData 管理、DevLogs 记录等全部工作流规则。"
---

# 开发工作流引擎 v5.0.0

## 概述

本文件定义了 AI 从接收到需求到完成交付的完整流程，包括需求分级、阶段规范、规则加载、进程恢复和收尾仪式。

**核心变更**：状态管理（INDEX.md 登记/更新、DevLog 写入、BOUNDARY CHECK）全部通过 `aegis` CLI 命令自动完成，AI 不再手动编辑这些文件。AI 的职责是创建内容性文档（design.md、review.md、verify.md）和执行子代理审查。

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

当 AI 发现需求涉及的技术栈在 TechStack 中不存在时，走搜索 → 审查 → 暂存 TempData → 提炼 → 清理流程（见 `conventions/naming-and-formats.md`）。

---

## 进程状态管理（Process State）

```
1. 读取 Aegis/rules/DevLogs/ 下最新日期的 DevLog
2. 检查 DevLog 中的「当前进度」+「下一动作」
3. 如果 DevLog 为空或信息不足，运行 aegis status 查看是否有未完成的需求
4. 告知用户上次进度：「上次您在 {需求名} 的 {阶段}，是否继续？」
```

DevLog 命名格式见 `conventions/naming-and-formats.md`。

---

## 需求分级

### AI 判定需求等级的规则

| 判定维度 | L1 | L2 | L3 |
|---------|----|----|----|
| 影响范围/涉及文件数 | 1 个文件 | 2-5 个文件 | 5+ 个文件 |
| 单行改值/配置调整 | L1 | L1 | L2 |
| 新增 API / Bug 修复 | L2 | L2 | L3 |
| 模块重构/架构调整 | L2 | L3 | L3 |
| 跨模块改造 | — | L3 | L3 |
| 安全相关 | L2 | L3 | L3 |
| 跨技术栈/数据库 schema | L2 | L3 | L3 |
| 性能优化/算法替换 | L2 | L2 | L3 |
| 第三方 SDK 集成 | L2 | L2 | L3 |

### 判定兜底

判定优先级：安全相关 > 跨模块/跨技术栈 > 文件数量 > 功能复杂度。标准模糊时向上取整。

---

## L1 极轻量需求 — 快速通道

```
1. aegis start "需求名" -l L1     ← 自动登记到 INDEX.md（🔨 implementing）
2. AI 直接修改代码
3. 调用 code-reviewer + devils-advocate 子代理审查
4. 展示审查结果 + 改动摘要 → 等用户确认
   (**不得擅自执行任何 git/svn 操作**)
5. aegis devlog write REQ-xxx -m "改动说明"   ← 自动写 DevLog
6. aegis advance                               ← 自动更新 INDEX.md 为 ✅ done
```

**BOUNDARY CHECK**（运行 `aegis check`）：
- [ ] INDEX.md 已有当前需求条目？
- [ ] INDEX.md 状态 = ✅ done？
- [ ] DevLog 已写入？

### 反借口表

| AI 可能的借口 | 反驳 |
|---|---|
| "这个改动小，我顺便优化一下别的" | 不。精准修改。只改需求范围的代码。 |
| "我直接用 git add/commit 帮你暂存" | 不。**不得擅自执行任何 git/svn 操作**。 |
| "L1 不需要登记 INDEX.md" | 不。L1 也必须 aegis start 登记。 |
| "L1 不需要写 DevLog" | 不。L1 也必须 aegis devlog write。 |

---

## L2 标准需求 — 5 阶段（不可跳过任何阶段）

```
[1/5] 方案设计 → [2/5] 设计审查 → [3/5] 实现 → [4/5] 代码审查 → [5/5] 验收
```

产出文件：
```
Aegis_Specs/L2/{feature-name}/
  ├── design.md      ← 设计方案（API 签名、数据结构、验收标准）
  ├── review.md      ← 审查记录（设计审查 + 代码审查）
  └── verify.md      ← 验收报告
```

### 阶段 L2-1：方案设计

```
Step 0: aegis start "需求名" -l L2   ← 自动登记到 INDEX.md（📐 design）
Step 1: 创建 Aegis_Specs/L2/{feature-name}/design.md（模板见 templates/spec-L2.md）
Step 2: 在聊天中向用户展示方案
Step 3: 验收标准检查 — 验收标准是否用了用户自己的语言描述？
Step 4: 等待用户明确确认（如 "OK"、"可以"、"go ahead"）
```

**BOUNDARY CHECK**（运行 `aegis check`）：
- [ ] INDEX.md 中已有当前需求条目（状态 📐 design）？
- [ ] design.md 存在？
- [ ] 验收标准已用用户语言表述？
- [ ] 用户已明确确认？

**任一不满足 → STOP。不进入 L2-2。**

### 阶段 L2-2：设计审查

```
Step 0: aegis advance               ← 自动更新 INDEX.md 为 📋 review_design
Step 1: 创建 Aegis_Specs/L2/{feature-name}/review.md（模板见 templates/review-L2.md）
Step 2: 启动 4 个子代理审查设计方案：
  a) code-reviewer（审查纠错）：API 签名、数据结构、边界条件
  b) devils-advocate（唱反调）：质疑设计决策，找更简单的方案
  c) security-auditor（安全审计）：检查安全隐患
  d) ux-reviewer（用户体验）：验收标准是否用户语言
Step 3: 将 4 个子代理的输出汇总到 review.md「设计审查」部分
Step 4: 所有问题必须修复或记录为已知风险后方可推进
```

**BOUNDARY CHECK**（运行 `aegis check`）：
- [ ] review.md 存在且包含「设计审查」记录？
- [ ] 4 个子代理均已输出？
- [ ] 发现的问题已修复或记录？

### 阶段 L2-3：实现

```
Step 0: aegis advance               ← 自动更新 INDEX.md 为 🔨 implementing
Step 1: 按 design.md 写代码（参考 review.md 中设计审查建议）
Step 2: 运行 typecheck / lint / build 验证
```

**BOUNDARY CHECK**（运行 `aegis check`）：
- [ ] INDEX.md 状态 = 🔨 implementing？
- [ ] 代码编译通过 / lint 无报错？

### 阶段 L2-4：代码审查

```
Step 0: aegis advance               ← 自动更新 INDEX.md 为 📋 review_code
Step 1: 启动 4 个子代理审查代码实现
Step 2: 将审查结果追加到 review.md「代码审查」部分
Step 3: 所有问题修复后方可进入验收
```

**BOUNDARY CHECK**（运行 `aegis check`）：
- [ ] review.md 包含「代码审查」记录？
- [ ] 4 个子代理均已输出？
- [ ] 发现的问题已修复？

### 阶段 L2-5：验收

```
Step 0: aegis advance               ← 自动更新 INDEX.md 为 ✅ verify
Step 1: 创建 verify.md（模板见 templates/verify-L2.md）
Step 2: 逐条对照 design.md 中定义的验收标准，填写验证结果
Step 3: 汇总改动摘要 → 向用户展示 → 等待确认
        (**不得擅自执行任何 git/svn 操作**)
Step 4: aegis devlog write REQ-xxx -m "done"   ← 自动写 DevLog
Step 5: aegis advance                           ← 自动更新 INDEX.md 为 ✅ done
```

**BOUNDARY CHECK**（运行 `aegis check`）：
- [ ] verify.md 存在且验收标准已逐条验证？
- [ ] 用户已明确确认？
- [ ] INDEX.md 已更新为 ✅ done？
- [ ] DevLog 已写入？

### 阶段边界检查（强制）

每个阶段之间，运行 `aegis check` 验证。`aegis check` 会自动检查当前阶段要求的所有文件是否存在。

### 反借口表

| AI 可能的借口 | 反驳 |
|---|---|
| "L2 不需要 design.md，直接写代码" | 不。L2 的 design.md 就是轻量 spec。 |
| "方案很明显，不需要等确认" | 不。用户可能看到你没看到的约束。 |
| "BOUNDARY CHECK 太啰嗦，跳过" | 不。aegis check 是一条命令，不啰嗦。 |
| "L2-1 不需要 aegis start" | 不。aegis start 是入口，不登记=需求不可追踪。 |

---

## L3 重型需求 — 7 阶段

```
[1/7] 头脑风暴 → [2/7] 提案 → [3/7] 技术设计 → [4/7] 需求规格
→ [5/7] 任务拆分 → [6/7] 集成审核 → [7/7] 实现验证 → 收尾仪式
```

### 阶段 L3-1 ~ L3-7

每个阶段 AI 负责创建对应的文档内容，状态管理通过 `aegis` CLI 命令：

- **L3-1 开始前**: `aegis start "需求名" -l L3`（自动登记到 INDEX.md）
- **每个阶段推进**: AI 创建该阶段的文档 → `aegis advance`
- **每次推进前验证**: `aegis check`
- **收尾**: `aegis devlog write` → `aegis advance`（最终 ✅ done）

子代理审查在 L3-6（集成审核）启动，同 L2 的 4 个子代理。

### 迭代退回机制

L3 流程支持在任意阶段退回到上一个阶段。退回后重新创建该阶段文档，然后 `aegis advance` 推进。

---

## 收尾仪式（Close-out）

L2/L3 需求全部完成后，AI 必须执行以下收尾步骤：

```
□ 0. 文档完整性检查（运行 aegis check 验证所有阶段文件）
□ 1. aegis devlog write REQ-xxx -m "完整总结"（含背景、改动清单、教训）
□ 2. TempData 清理：检查本次需求相关的 TempData 文件，提炼到 TechStack 或删除
□ 3. 5 维审视：从目录结构、文档职责边界、流程冗余/缺失、AI 误解风险、用户认知负担
□ 4. 告知用户项目完成
```

---

## 更新日志

| 日期 | 版本 | 改动 |
|------|------|------|
| 2026-06-06 | v5.0.0 | 全流程迁移到 CLI 工具链：INDEX.md 登记 → `aegis start`，状态推进 → `aegis advance`，边界检查 → `aegis check`，DevLog → `aegis devlog write`；L2 5 阶段 + 4 子代理 × 2 轮；L1 新增 2 子代理审查 |
