# 提案：Aegis Toolchain

> L3-2 | 2026-06-05 | Phase 1 提案

## 为什么

Aegis v3.1.0 的核心矛盾：**用文本文档约束 AI 行为，但 AI 不是编译器。** 三个致命缺陷：
1. 触发不可靠：依赖 AI 主动读取 SKILL.md，没有技术手段保证 100%
2. 检查形同虚设：BOUNDARY CHECK 由 AI 用 read 自查自证
3. 状态不可靠：DevLog 纯文本记录进度，AI 写错就断点丢失

不做的后果：Aegis 永远停留在"AI 自律"层面，流程执行全靠运气。

## 选定方案

基于 brainstorm 三方案对比 + 四份技术调研，选定 **方案 C：渐进演进**。

**Phase 1（当前提案范围）**：构建 CLI 工具链，包含预处理器、命令工具、状态管理、Git Hook，全部用 Python。
**Phase 2（后续）**：MCP Server 包装 + YAML 状态机，在 Phase 1 基础上自然升级。

选定理由：
- MCP 调研确认 HanaAgent 无原生支持，需要插件桥接，不宜押注 Phase 1
- python-statemachine 调研确认可替代停维的 transitions，Phase 2 有可靠基础
- pre-commit 框架调研确认是跨平台 Git Hook 的最佳实践

## 技术选型（调研确认）

| 模块 | 选定 | 调研来源 | 关键依据 |
|------|------|---------|---------|
| 语言 | Python 3.11+ | — | 跨平台，CLI 生态成熟 |
| CLI 框架 | **Typer** | 调研一 | 类型注解驱动，Rich 集成，学习成本最低 |
| 项目管理 | **Poetry** | 调研一 | 成熟稳妥，依赖锁定，src-layout |
| 状态管理 | **Pydantic v2 + JSON** | 调研一 | Rust 核心快，自动 schema 校验 |
| 文件锁 | **filelock** | 调研一 | 跨平台（Windows/Mac/Linux），tox 团队维护 |
| 日志 | **loguru** | 调研一 | 比标准库简洁，CLI 场景最优 |
| Git 操作 | **GitPython** | 调研三 | 对象化 API，无需 subprocess 解析 |
| Git Hook | **pre-commit 框架** | 调研三 | 跨平台最好，社区标准，Python 编写 hook |
| 状态机 | **python-statemachine** | 调研四 | **2026 最活跃**，transitions 已停维 |
| YAML | **PyYAML + Pydantic 校验** | 调研四 | 配置与代码分离，跨字段校验 |
| MCP | **暂缓至 Phase 2** | 调研二 | HanaAgent 需插件桥接，SDK v1.x 成熟但先不押注 |
| 测试 | **pytest + pytest-mock** | 调研一 | 社区标准 |
| 代码质量 | **ruff + mypy** | 调研一 | 一站式格式化和 lint |

## 变更概要

### 新增模块

1. **aegis-toolchain 项目** — 独立 Python 项目，与 Aegis 核心并行
2. **preprocessor.py** — 消息预处理器，截获用户输入，自动注入 Aegis 规则到 system prompt
3. **aegis CLI 命令组** — `aegis start` / `aegis check` / `aegis advance` / `aegis status` / `aegis devlog`
4. **state.json 状态管理** — Pydantic schema + filelock，替代文本 DevLog 的状态追踪
5. **pre-commit hook** — 在 git commit 时自动验证 Aegis 合规性
6. **aegis-boot SKILL.md 修改** — 加入自检指令 + CLI 调用要求

### 修改模块

7. **Aegis_Specs/INDEX.md** — 不再纯手工维护，由 CLI 辅助更新
8. **Aegis/rules/DevLogs/** — 保留文本 DevLog，但增加 CLI 自动生成能力

### 删除/废弃

9. （无删除，Phase 1 是增量添加，不破坏现有 Aegis 结构）

## 影响范围

| 文件/目录 | 操作 | 所属模块 |
|-----------|------|---------|
| `aegis-toolchain/` | 新增目录 | 项目根 |
| `aegis-toolchain/pyproject.toml` | 新增 | 项目配置 |
| `aegis-toolchain/src/aegis_toolchain/` | 新增 | 源码目录 |
| `aegis-toolchain/src/aegis_toolchain/cli/` | 新增 | CLI 命令 |
| `aegis-toolchain/src/aegis_toolchain/core/` | 新增 | 核心逻辑 |
| `aegis-toolchain/src/aegis_toolchain/preprocessor/` | 新增 | 预处理器 |
| `aegis-toolchain/src/aegis_toolchain/hooks/` | 新增 | Git Hook |
| `aegis-toolchain/src/aegis_toolchain/models/` | 新增 | Pydantic schema |
| `aegis-toolchain/tests/` | 新增 | 测试 |
| `.pre-commit-config.yaml` | 新增 | pre-commit 配置 |
| `Aegis/skills/aegis-boot/SKILL.md` | 修改 | 加入自检指令+CLI 调用 |
| `Aegis/Aegis_Specs/INDEX.md` | 修改 | 模板微调 |

## 不在本次范围

- MCP Server 开发（Phase 2）
- YAML 状态机引擎（Phase 2）
- HanaAgent 插件开发（Phase 2）
- 可视化 Dashboard（Phase 3）
- CI/CD 集成（Phase 3）
- 多项目聚合管理（Phase 3）
- 现有 Aegis 核心流程的重构（只加外挂，不改内核）

## 方案风险边界

### 风险场景

| 什么情况下这个方案会失败？ | 为什么？ |
|---|---|
| Hana 不支持用户消息前置钩子 | 预处理器无法截获消息，规则注入失效。**降级方案**：预处理器改为独立脚本，手动运行或集成到 CLI 的 `aegis start` 中 |
| AI 不主动调用 `aegis check` | CLI 仍然依赖 AI 记得调用。**降级方案**：SKILL.md 中强化自检指令 + Git Hook 作为兜底防线 |
| pre-commit hook 被 `--no-verify` 跳过 | 开发者可以绕过 Hook。**缓解**：CI 端增加二次检查；控制台警告"你跳过了 Aegis 检查" |
| state.json 在 Windows 上文件锁行为异常 | filelock 的 Windows 实现可能有 corner case。**缓解**：加超时重试 + 错误降级（锁失败时只读模式） |

### 已知限制

- 预处理器目前是独立 Python 脚本，需要 Hana 平台配合才能实现自动注入；在平台支持前，预处理器以 CLI 子命令形式存在，由 AI 在流程中主动调用
- CLI 工具的检查仍然需要 AI "记得调用"，没有做到零依赖的强制检查（那是 Phase 2 MCP 的目标）
- 不作现有 Aegis 核心流程的重构——只做外挂式增强，不与内核耦合
- state.json 和文本 DevLog 会并存一段时间，存在信息重复/不一致的可能

---

## 项目结构

```
aegis-toolchain/                     # 独立 Python 项目
├── pyproject.toml                   # Poetry 配置 + 依赖 + entry points
├── README.md
├── LICENSE
├── src/
│   └── aegis_toolchain/
│       ├── __init__.py
│       ├── __main__.py             # python -m aegis_toolchain
│       │
│       ├── cli/                     # CLI 入口层
│       │   ├── __init__.py
│       │   ├── main.py             # Typer app 入口，注册所有子命令
│       │   ├── start.py            # aegis start <req-id>
│       │   ├── check.py            # aegis check
│       │   ├── advance.py          # aegis advance
│       │   ├── status.py           # aegis status
│       │   └── devlog.py           # aegis devlog
│       │
│       ├── core/                    # 核心逻辑（不依赖 CLI）
│       │   ├── __init__.py
│       │   ├── state_manager.py    # state.json 读写 + filelock
│       │   ├── boundary_checker.py # BOUNDARY CHECK 执行引擎
│       │   ├── rule_loader.py      # 读取 Aegis 规则文件
│       │   └── index_manager.py    # INDEX.md 结构化操作
│       │
│       ├── preprocessor/            # 预处理器
│       │   ├── __init__.py
│       │   ├── classifier.py       # L1/L2/L3 分类引擎
│       │   └── injector.py         # 规则注入到 system prompt
│       │
│       ├── hooks/                   # Git Hook 实现
│       │   ├── __init__.py
│       │   └── pre_commit.py       # pre-commit hook 入口
│       │
│       ├── models/                  # Pydantic 数据模型
│       │   ├── __init__.py
│       │   ├── state.py            # AegisState, Requirement 模型
│       │   ├── config.py           # AegisConfig 模型
│       │   └── workflow.py         # WorkflowDefinition (Phase 2 用)
│       │
│       └── utils/                   # 工具函数
│           ├── __init__.py
│           ├── logging.py          # loguru 配置
│           └── fs.py               # 文件系统辅助
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # pytest fixtures
│   ├── test_cli/
│   ├── test_core/
│   ├── test_preprocessor/
│   └── test_hooks/
│
└── .pre-commit-config.yaml         # pre-commit 配置（此项目自身也用）
```

## 验收标准（用户视角）

| # | 标准 | 验证方式 | 备注 |
|---|------|---------|------|
| 1 | AI 通过 `aegis preprocess` 获取增强 prompt 后，遵守 Aegis 流程的阶段纪律 | `aegis check` 各阶段通过率 | Phase 1 为 CLI 手动调用；自动注入为 Phase 2 目标（需 Hana 平台支持） |
| 2 | 我用 `aegis start "炮台系统" --level auto` 就能开始一个新需求，state.json 精确记录状态 | 执行后 `aegis status` 显示新需求 | 参数为需求名称，系统自动生成 REQ-ID |
| 3 | 我执行 `aegis check` 就能看到当前阶段的 BOUNDARY CHECK 是否通过（✅/✗ + 明细） | 终端输出有明确的通过/失败明细 | |
| 4 | 我 `git commit` 时，pre-commit hook 自动检查 Aegis 合规性，不通过就阻断 commit | 手动制造不合规场景验证阻断 | |
| 5 | 中断后恢复时，`aegis status` 精确告诉我上次做到哪个阶段、缺失哪些 BOUNDARY CHECK | 查看 status 输出与实际状态对照 | |
| 6 | DevLog 可以用 `aegis devlog REQ-XXX -m "内容"` 自动生成模板，不需要手写格式 | 检查生成的 DevLog 文件格式 | |

## 快速开始 (Quick Start)

```bash
# 前提条件：Python ≥ 3.11, Git ≥ 2.30, Poetry

# 1. 安装
git clone <repo-url> aegis-toolchain
cd aegis-toolchain
poetry install

# 2. 安装 Git Hook
pre-commit install

# 3. 首次使用（在任意 Aegis 项目目录下）
cd /path/to/your-aegis-project
aegis start "我的第一个需求" --level auto
aegis status

# 4. 更多命令
aegis --help
```

> 预期输出示例：
> ```
> $ aegis start "测试需求" --level L1
> ✅ 已登记 REQ-003 [L1] 🔨 implementing
> 
> $ aegis status
> 活跃需求:
>   REQ-003  测试需求  [L1]  🔨 implementing
>   BOUNDARY CHECK: 0/2 (L1 仅需 INDEX.md + DevLog)
> ```

---

> 基于四份调研报告整合：Python CLI 最佳实践 / MCP 可行性 / Git Hook 方案 / YAML 状态机选型
> 提案日期：2026-06-05
