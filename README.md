# Aegis v5.2.2

AI 开发治理工具链。从需求登记到验收，全流程状态可追踪、阶段有检查、断点可恢复。

> 每次对话前先跑 `python -m aegis_toolchain start "需求" -l L2`。别手写 INDEX.md，登记、推进、记录由 CLI 管理。

---

## 动机

用 AI 写代码时常见的问题：

- AI 跳过方案讨论直接写代码，方向不对全白做
- 下次对话换了一个实例，上次做到哪全部重来
- AI 改一个 bug 顺带改了不相干的代码
- 改完不留记录，后续维护不知道改了什么
- 需求分类、阶段检查依赖 AI 自觉，没有工具约束

Aegis 的解法：每次改动前先登记需求，CLI 自动分类（L1/L2/L3），每个阶段结束时执行 BOUNDARY CHECK，所有进度写入 state.json。不满足条件不能推进，断线后读 state 恢复进度。

---

## 安装

```powershell
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

安装后通过 `python -m aegis_toolchain` 调用（不在 PATH 中，`python -m` 是 Python 自带机制，无需配置）：

```powershell
cd 你的项目
python -m aegis_toolchain init
python -m aegis_toolchain start "需求" -l L2
python -m aegis_toolchain status
python -m aegis_toolchain check
python -m aegis_toolchain advance
```

---

## AI 工作流

AI 进入项目后读到 `AGENTS.md` → 加载 `Aegis/skills/aegis-boot/SKILL.md` → 按 SKILL.md 执行流程：

1. `python -m aegis_toolchain start "需求" -l L2` — 登记需求，自动创建 state.json
2. 写设计文档、子代理审查 — 人类确认
3. `python -m aegis_toolchain check` — BOUNDARY CHECK
4. `python -m aegis_toolchain advance` — 推进阶段
5. 写代码、代码审查、验证 — 人类确认
6. `python -m aegis_toolchain devlog write REQ-001 -m "done"`

AI 不需要知道 CLI 的位置、classifier 的实现、state.json 的格式。SKILL.md 里写了完整的命令序列。

---

## 需求分级

### L1 — 小改动

```
start → 直接改 → devlog → advance → done
```

| 检查项 | 方式 |
|--------|------|
| INDEX.md 已登记 | 自动 |
| DevLog 已写入 | 自动 |

### L2 — 功能/模块

5 阶段：

```
📐 design    →  写 design.md，人类确认
📋 review    →  4 子代理审查设计，修复问题
🔨 implement →  写代码，展示改动，人类确认
📋 review    →  4 子代理审查代码，修复问题
✅ verify    →  逐条验收，devlog，advance
```

每个阶段间执行 BOUNDARY CHECK，不满足项必须补齐才能推进。

### L3 — 架构改造

7 阶段，含 brainstorm 和 proposal。完整流程见 `Aegis/skills/dev-workflow/SKILL.md`。

---

## 命令列表

| 命令 | 作用 |
|------|------|
| `python -m aegis_toolchain init` | 生成 Aegis/ 规则文件和 AGENTS.md |
| `python -m aegis_toolchain start "标题" -l L2` | 登记需求，自动创建 state.json |
| `python -m aegis_toolchain check` | BOUNDARY CHECK |
| `python -m aegis_toolchain advance` | 推进阶段（内置 check，不通过则拒绝） |
| `python -m aegis_toolchain status` | 查看所有需求进度 |
| `python -m aegis_toolchain upgrade` | Aegis 升级后同步项目规则 |
| `python -m aegis_toolchain devlog write REQ-001 -m "msg"` | 写 DevLog |
| `python -m aegis_toolchain devlog list` | 列出所有 DevLog |
| `python -m aegis_toolchain devlog show` | 查看最近一条 DevLog |

---

## 项目文件结构

`aegis init` 生成：

```
AGENTS.md
Aegis/
  rules/           → 全局规范、技术栈
  skills/          → aegis-boot + dev-workflow 引擎
  state/
    state.json     → 需求进度（第一次 start 后创建）
Aegis_Specs/
  INDEX.md         → 需求索引表
```

`state.json` 在 `start` 命令中创建，不是 init 时生成。

---

## 版本路线图

| Phase | 内容 | 状态 |
|-------|------|------|
| 1 | CLI + state.json + classifier + 测试覆盖 | 核心完成 (v5.2.2) |
| 2 | MCP Server + YAML 状态机 | 规划中 |
| 3 | 全 MCP 生态、跨 AI 工具兼容 | 设想 |

### Phase 1 范围说明

**已完成**：
- CLI 覆盖 8 个命令（init/start/check/advance/status/upgrade/devlog write/list/show）
- state.json 管理需求阶段、进度追踪、断点恢复
- classifier 自动判定 L1/L2/L3，嵌入 start 命令
- BOUNDARY CHECK 按阶段验证
- AGENTS.md + SKILL.md 模板，AI 可自动加载工作流
- 240 测试 + ruff + mypy

**折中**：
- CLI 通过 `python -m aegis_toolchain` 调用，不在 PATH 中（无需配置，需要用户知道该命令）
- classifier（原 preprocessor 模块）不再有独立 `preprocess` 命令，功能内嵌到 `start` 中

**未完成**：
- pre-commit hook：暂缓。依赖链长（需预装 pre-commit + 手动 install），当前方案不成熟

---

MIT
