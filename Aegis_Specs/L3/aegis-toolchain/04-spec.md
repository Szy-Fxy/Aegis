# 规格：Aegis Toolchain Phase 1

> L3-4 | 2026-06-05 | 功能需求规格

## 背景

Aegis v3.1.0 是 AI 开发治理系统，定义了 L1/L2/L3 三级开发流程和 BOUNDARY CHECK 机制。当前全部依赖 AI 自律：AI 自己读规则、自己查文件验证 BOUNDARY CHECK、自己在 INDEX.md 和 DevLog 中写进度。三个致命缺陷：触发不可靠、检查形同虚设、状态不可恢复。

Aegis Toolchain 是 Aegis 的外挂工具链，目标是把关键流程约束从"AI 自律"转向"工具强制"。Phase 1 聚焦 CLI 工具 + 预处理器 + Git Hook。

## 问题陈述

没有工具链时：
- AI 可能跳过 Aegis 规则直接写代码，用户需要反复提醒
- BOUNDARY CHECK 由 AI 用 read 自查自证，AI 可以作假或遗漏
- 会话中断后，靠 DevLog 文本恢复状态，AI 写错就断点丢失
- 没有机制阻止开发者 commit 未通过 Aegis 检查的代码

## 目标

1. `aegis start` 一键登记需求，state.json 精确记录状态
2. `aegis check` 独立执行 BOUNDARY CHECK，结果不由 AI 自查
3. `aegis status` 精确展示当前阶段和缺失项
4. `aegis preprocess` 自动分类 + 注入规则
5. pre-commit hook 阻断未通过 Aegis 检查的提交
6. 断点续做准确率 100%（state.json 结构化状态）

## 非目标

- 不修改 Aegis 核心流程文件（SKILL.md 仅加自检指令块）
- 不实现 MCP Server（Phase 2）
- 不实现 YAML 状态机引擎（Phase 2）
- 不实现可视化 Dashboard（Phase 3）
- 不做 CI/CD 集成（Phase 3）

---

## 功能需求

### REQ-F01: 需求生命周期管理

`aegis start` / `aegis advance` / `aegis status` — 需求的创建、推进和状态查询。

#### 场景: 正常创建 L2 需求
- **当** 用户执行 `aegis start "炮台系统" --level L2`
- **则** 系统生成 ID REQ-XXX，在 state.json 中注册需求（level=L2, phase=design），在 INDEX.md 表格新增一行，输出"已登记 REQ-XXX [L2] 📐 design"

#### 场景: 自动分类
- **当** 用户执行 `aegis start "修复登录页按钮颜色" --level auto`
- **则** 系统分类为 L1，输出分类依据（匹配关键词: 修复, 颜色）

#### 场景: 并发保护
- **当** state.json 已有一个 `🔨 implementing` 需求，用户执行 `aegis start "新功能"`
- **则** 系统拒绝，提示"REQ-XXX 仍在 implementing 中，请先完成或暂停"

#### 场景: 正常推进阶段
- **当** 用户执行 `aegis advance REQ-003`，且当前阶段 BOUNDARY CHECK 全部通过
- **则** 需求 phase 推进到下一阶段，state.json 和 INDEX.md 同步更新

#### 场景: CHECK 未通过时拒绝推进
- **当** 用户执行 `aegis advance REQ-003`，但 BOUNDARY CHECK 有未通过项
- **则** 系统拒绝，输出具体缺失项

#### 场景: 强制推进
- **当** 用户执行 `aegis advance REQ-003 --force`
- **则** 跳过 BOUNDARY CHECK，强制推进，输出 ⚠️ 警告

#### 场景: 查看全部状态
- **当** 用户执行 `aegis status`
- **则** 输出所有活跃需求列表（ID / 标题 / 等级 / 阶段 / CHECK 状态）

#### 场景: 查看单个需求
- **当** 用户执行 `aegis status REQ-003`
- **则** 输出该需求的详细信息（创建时间、阶段、文件变更、各 BOUNDARY CHECK 明细）

#### 场景: JSON 输出
- **当** 用户执行 `aegis status --json`
- **则** 输出完整 state.json 内容到 stdout

---

### REQ-F02: BOUNDARY CHECK 执行

`aegis check` — 独立于 AI 的检查执行器。

#### 场景: 检查 L2 设计阶段
- **当** 用户执行 `aegis check REQ-003`，当前 phase=design
- **则** 系统检查：INDEX.md 登记 ✓/✗、design.md 存在 ✓/✗、验收标准含用户语言 ✓/✗，输出 BoundaryReport

#### 场景: 检查 L2 实现阶段
- **当** 当前 phase=implementing
- **则** 系统检查：INDEX.md 状态 ✓/✗、代码编译 ✓/✗

#### 场景: 检查 L2 验证阶段
- **当** 当前 phase=verify
- **则** 系统检查：INDEX.md 已更新 ✓/✗、DevLog 已写入 ✓/✗

#### 场景: 检查 L1 需求
- **当** 当前 level=L1
- **则** 系统检查：INDEX.md 登记 ✓/✗、DevLog 已写入 ✓/✗

#### 场景: 检查 L3 需求各阶段
- **当** 当前 level=L3, phase=brainstorm
- **则** 系统检查 01-brainstorm.md 存在 ✓/✗；proposal → 02-proposal.md；design → 03-design.md；以此类推

#### 场景: 需求不存在
- **当** 用户执行 `aegis check REQ-999`
- **则** 系统报错"REQ-999 不存在于 state.json 中"

#### 场景: 检查项全部通过
- **当** 所有检查项通过
- **则** 输出 ✅ 全部通过，退出码 0

#### 场景: 部分检查失败
- **当** 部分检查未通过
- **则** 输出 ✗ 详细明细，退出码 1

---

### REQ-F03: DevLog 操作

`aegis devlog` — DevLog 的生成和查看。

#### 场景: 生成 DevLog 模板
- **当** 用户执行 `aegis devlog REQ-003 --editor`
- **则** 系统生成带模板的临时文件，打开默认编辑器（$EDITOR / notepad），用户编辑保存后写入 DevLog 目录

#### 场景: 快速写入
- **当** 用户执行 `aegis devlog REQ-003 -m "完成鱼转向优化，调整了 TurnDuration 参数"`
- **则** 系统生成 DevLog 文件，内容包含：需求信息、时间戳、message、状态变更

#### 场景: 查看最新 DevLog
- **当** 用户执行 `aegis devlog show`
- **则** 显示最近一次 DevLog 的内容

#### 场景: 查看指定需求 DevLog
- **当** 用户执行 `aegis devlog show REQ-003`
- **则** 显示 REQ-003 的所有 DevLog

---

### REQ-F04: 消息预处理

`aegis preprocess` — 用户消息分类 + 规则注入。

#### 场景: 正常分类并注入
- **当** 用户执行 `aegis preprocess "帮我加一个捕鱼炮台系统" --project .`
- **则** 系统输出分类结果（L2, confidence=0.85），然后输出注入 Aegis 规则后的完整 system prompt

#### 场景: 分类置信度低
- **当** 消息模糊（如"改一下"），confidence < 0.5
- **则** 输出分类结果 + 标记"不确定，默认 L2"，规则中提示"AI 请自行确认等级"

#### 场景: 非 Aegis 项目
- **当** `--project` 指向的目录没有 Aegis 目录结构
- **则** 输出提示"非 Aegis 项目，只有 global.md 可用"

#### 场景: 复合任务
- **当** 消息含"修完 bug 再加个功能"
- **则** 拆分输出："检测到复合任务。建议: 先 L1（修bug），再 L2（加功能）"

---

### REQ-F05: Git pre-commit Hook

pre-commit hook — commit 前的 Aegis 合规检查。

#### 场景: 有活跃需求，检查通过
- **当** `git commit` 触发 hook，state.json 中 REQ-003 为 implementing
- **则** Hook 执行相当于 `aegis check REQ-003`，全部通过 → 放行，退出码 0

#### 场景: 有活跃需求，检查失败
- **当** Hook 发现 BOUNDARY CHECK 未通过
- **则** 阻断 commit，输出失败明细

#### 场景: 无活跃需求
- **当** state.json 中无 implementing 需求
- **则** 放行（非 Aegis 变更，跳过检查）

#### 场景: Git 不可用
- **当** 环境没有 git 命令
- **则** 输出警告"Git not found"，放行，退出码 0

#### 场景: state.json 不存在
- **当** 项目不是 Aegis 项目
- **则** 静默放行，退出码 0

---

### REQ-F06: 状态持久化

StateManager — state.json 的并发安全读写。

#### 场景: 正常加载
- **当** state.json 存在且格式正确
- **则** 返回 AegisState 对象

#### 场景: 文件不存在
- **当** state.json 不存在
- **则** 返回默认空 AegisState（version="1.0.0", 空列表）

#### 场景: JSON 损坏
- **当** state.json 内容非合法 JSON
- **则** 抛出 StateCorruptedError，错误信息包含损坏位置和修复建议

#### 场景: Schema 校验失败
- **当** JSON 合法但不符合 Pydantic schema（如 level=L4）
- **则** 抛出 StateCorruptedError，错误信息列出所有校验失败字段

#### 场景: 并发保护（正常写入）
- **当** 进程 A 持有锁期间，进程 B 尝试 save
- **则** 进程 B 等待（默认超时 5s），A 释放后 B 获取锁写入

#### 场景: 并发保护（超时降级）
- **当** 进程 B 等待超过 5s
- **则** 进程 B 输出警告，放弃写入，return False

#### 场景: 原子写入
- **当** save 执行中进程崩溃
- **则** state.json 保持旧内容不变（先写 .tmp 再 rename）

---

### REQ-F07: 规则加载

RuleLoader — Aegis 规则文件的读取。

#### 场景: 加载全部规则
- **当** 调用 load_all()
- **则** 返回 {"global.md": "...", "dev-workflow": "...", "unity.md": "..."}

#### 场景: 技术栈自动匹配
- **当** 调用 load_techstack(["Unity", "C#"])
- **则** 匹配并加载 TechStack/unity.md

#### 场景: 技术栈无匹配
- **当** 关键词无匹配的技术栈文件
- **则** 返回空字符串，不报错

#### 场景: 规则文件缺失
- **当** 某个规则文件路径指向的文件不存在
- **则** 跳过该文件，输出 warning，不影响其他文件加载

---

### REQ-F08: INDEX.md 管理

IndexManager — INDEX.md 表格的结构化操作。

#### 场景: 新增条目
- **当** 调用 add_entry("REQ-003", "炮台系统", "L2", "📐 design")
- **则** 在 INDEX.md 表格末尾新增行，保留原有格式

#### 场景: 更新状态
- **当** 调用 update_status("REQ-003", "🔨 implementing")
- **则** 更新对应行的状态列和最后活动日期

#### 场景: 读取全部
- **当** 调用 read_all()
- **则** 解析 INDEX.md 表格，返回 dict 列表

#### 场景: INDEX.md 不存在
- **当** INDEX.md 不存在
- **则** 返回空列表，read_all() 不报错；add_entry() 自动创建 INDEX.md 并写入表头

---

### REQ-F09: CLI 全局行为

#### 场景: --help 自动生成
- **当** 用户执行 `aegis --help`
- **则** 显示所有子命令和描述，格式清晰，有彩色输出

#### 场景: 未知命令
- **当** 用户执行 `aegis unknown_command`
- **则** 显示 "No such command"，建议最相似的命令

#### 场景: 缺少必填参数
- **当** 用户执行 `aegis start` 不带参数
- **则** 显示 "Missing argument 'TITLE'"，展示用法

---

## 验收标准

| # | 标准 | 验证方式 |
|---|------|----------|
| 1 | `aegis start` 能在 1s 内完成登记（state.json + INDEX.md 写入） | 手动计时 |
| 2 | `aegis check` 对 L2-design 阶段的检查项 100% 准确（和手动对照） | 自动化测试 |
| 3 | 两个进程同时 save state.json 时，数据不损坏、不丢失 | 并发测试脚本 |
| 4 | `aegis preprocess` 分类 L1/L2/L3 准确率 ≥80%（20 条测试用例） | 自动化测试 |
| 5 | pre-commit hook 在 BOUNDARY CHECK 失败时阻断 commit，退出码非0 | 手动测试 |
| 6 | `aegis status` 输出信息精确到当前阶段和缺失 BOUNDARY CHECK 项 | 手动对照 |
| 7 | CLI 在 Windows PowerShell 和 Git Bash 上均正常显示彩色输出 | 跨平台验证 |
| 8 | state.json 损坏时给出可操作的修复建议（而非崩溃或静默错误） | 故障注入测试 |

## 非功能需求

### 性能
- CLI 启动时间 < 500ms（含 Python 解释器启动）
- state.json 读写 < 100ms（文件 < 1MB 时）
- 预处理器输出 < 2s

### 安全
- 所有文件路径限制在项目根目录内，拒绝 `../` 穿越
- JSON 反序列化前用 Pydantic schema 校验
- 无硬编码密钥、无网络请求、无数据外传

### 兼容性
- Python 3.11+
- Windows 10/11、macOS、Linux
- Git 2.30+

## 风险与备注

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| filelock 在 Windows 上边缘行为与 Unix 不一致 | 中 | 测试覆盖 Windows 环境，超时设置为 5s 兜底 |
| INDEX.md 表格格式被人手动修改后 IndexManager 解析失败 | 低 | 解析用宽松正则，解析失败时提示"INDEX.md 格式异常，请检查" |
| 预处理器在 Hana 中无法自动触发 | 高 | 降级为 `aegis preprocess` 命令，AI 流程中主动调用 |
| 用户绕过 CLI 直接手动改 INDEX.md | 低 | `aegis status` 会检测 state.json 和 INDEX.md 的一致性差异 |
| poetry 依赖解析慢 | 低 | 锁定具体版本，减少解析时间 |

- Phase 1 完成后需要进行至少 3 个真实 Aegis 需求的完整流程演练（吃自己的狗粮）
- CI/CD 集成推迟到 Phase 3，Phase 1 仅本地 Git Hook

---

> 基于 03-design.md 的完整功能规格
> 覆盖 9 个功能需求，每个含正常路径 + 边界条件 + 错误处理
