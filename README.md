# Aegis v5.2.2

> 🛡️ AI 写代码，你来拍板。Aegis 替你把关每一步。

> 💡 **每次跟 AI 对话前先跑 `python -m aegis_toolchain start "需求" -l L2`。别手写 INDEX.md，登记、推进、记录全自动。**

---

## AI 开发的现状：六个痛点

用 AI 写代码的人，迟早撞上这些：

| 痛点 | 具体表现 |
|------|----------|
| 😵 **跳步骤** | AI 上来就写代码，跳过设计、跳过方案讨论。写完发现方向错了。 |
| 🤷 **不认账** | 下次对话 AI 换了一个实例，完全不知道上次做到哪了。你得花 20 分钟复述。 |
| 🎯 **跑偏题** | 你让改一个 bug，它顺手重构了三个模块。改完你都不敢合入。 |
| 📝 **不留痕** | 改完不写记录。三个月后你忘了为什么改了那段代码，AI 也忘了。 |
| 🧩 **哑铃式对话** | 人类说需求，AI 出代码，中间缺了方案确认、优化建议这些环节。 |
| 🔀 **工具不通用** | 你用 Hana，别人用 Cursor，项目规则散落在各个工具的配置里，标准不一致。 |

>Aegis 就是用来堵这些口的。

## Aegis 是什么

一句话：**给 AI 套上缰绳。**

你用 AI 写代码的时候最怕什么？它跳步骤、瞎改、改完不记录、下次来不知道做到哪了。Aegis 解决的就是这个：每次 AI 动代码之前先登记需求，每个阶段结束时强制 BOUNDARY CHECK，所有状态写进 state.json。断点续做、进度回看、合规检查，全部自动化。

人类只负责两件事：提需求、拍板。

---

## 装一个试试

```powershell
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

装完就能用，不用配任何东西：

```powershell
cd 你的项目
python -m aegis_toolchain init                                # 生成规则文件 + AGENTS.md
python -m aegis_toolchain start "玩家背包系统" -l L2            # 登记需求，自动写入 state.json
python -m aegis_toolchain status                               # 看看当前进度
python -m aegis_toolchain check                                # 当前阶段 BOUNDARY CHECK
python -m aegis_toolchain advance                              # 推进到下一阶段（不通过不让过）
```

---

## AI 怎么用这套东西

AI 进项目之后看到 `AGENTS.md` → 按指引加载 `Aegis/skills/aegis-boot/SKILL.md` → SKILL.md 里写了每一步：

```
1. python -m aegis_toolchain start "需求" -l L2   → 自动分类登记
2. 创建设计文档、子代理审查                        → 人类确认
3. python -m aegis_toolchain check                → BOUNDARY CHECK
4. python -m aegis_toolchain advance              → 推进阶段
5. 写代码、代码审查、验证                          → 人类确认
6. python -m aegis_toolchain devlog write REQ-001 -m "done"
```

AI 不需要知道 CLI 在哪、classifier 怎么工作、state.json 怎么读写——SKILL.md 里全写了，它照着执行就行。

---

## 需求分级与阶段流程

Aegis 把需求分成三级，每级有对应的流程。等级越高，审查越严。

### L1 急救模式 — 小修小补

改个 typo、换个配置值、一行补丁。1 阶段，快速收工。

```
start → 直接改 → devlog → advance → done
```

| 检查项 | |
|--------|------|
| INDEX.md 有登记 | ✅ 自动检查 |
| DevLog 已写入 | ✅ 自动检查 |


### L2 标准流程 — 功能开发

加个背包系统、优化碰撞检测、模块重构。5 阶段，层层把关。

```
┌─ L2-1 📐 设计 ────────────────────────────────────┐
│  start → 写 design.md → 人类确认                   │
│  检查：INDEX.md ✓ | design.md ✓                    │
├─ L2-2 📋 设计审查 ────────────────────────────────┤
│  advance → 4 子代理审查 → 修复问题                  │
│  检查：review.md ✓ | 审查记录 ✓                     │
├─ L2-3 🔨 实现 ─────────────────────────────────────┤
│  advance → 写代码 → 展示改动摘要 → 人类确认         │
│  检查：代码编译 ✓ | lint 通过 ✓                     │
├─ L2-4 📋 代码审查 ────────────────────────────────┤
│  advance → 4 子代理审查代码 → 修复问题              │
│  检查：审查记录 ✓ | 问题已修复 ✓                    │
├─ L2-5 ✅ 验收 ────────────────────────────────────┤
│  advance → 逐条验收 → devlog → advance              │
│  检查：verify.md ✓ | DevLog ✓ | 人类确认 ✓          │
└───────────────────────────────────────────────────┘
```

### L3 重型流程 — 架构重构

重写渲染管线、换数据库、跨模块改造。7 阶段，带 brainstorm 和 proposal。

```
brainstorm → proposal → 设计 → 设计审查 → 实现 → 代码审查 → 验收
```

（完整 L3 流程见 `Aegis/skills/dev-workflow/SKILL.md`）


## 命令速查

| 命令 | 干什么 |
|------|--------|
| `python -m aegis_toolchain init` | 初始化项目 |
| `python -m aegis_toolchain start "标题" -l L2` | 登记需求，自动分类 |
| `python -m aegis_toolchain check` | BOUNDARY CHECK |
| `python -m aegis_toolchain advance` | 推进阶段（不通过不让过） |
| `python -m aegis_toolchain status` | 查看所有需求进度 |
| `python -m aegis_toolchain upgrade` | 升级后同步规则文件 |
| `python -m aegis_toolchain devlog write REQ-001 -m "日志"` | 写 DevLog |
| `python -m aegis_toolchain devlog list` | 列出所有日志 |
| `python -m aegis_toolchain devlog show` | 查看最近日志 |


## 项目里会多出什么

`aegis init` 之后，你的项目根目录会多出这些：

```
AGENTS.md                      ← AI 进门的入口
Aegis/
  rules/                       ← 全局规范 + 技术栈规则
  skills/                      ← AI 工作流引擎
  state/
    state.json                 ← 所有需求的进度追踪
Aegis_Specs/
  INDEX.md                     ← 需求索引表
```

**state.json 在第一次 `aegis start` 后才会出现**，不是 init 时生成的。


## 版本路线图

| Phase | 计划内容 | 当前状态 |
|-------|---------|----------|
| **Phase 1** | CLI + state.json + classifier + 测试覆盖 | ✅ **v5.2.2 核心完成** |
| **Phase 2** | MCP Server + YAML 状态机 | 📋 规划中 |
| **Phase 3** | 全 MCP 生态：跨 AI 工具兼容 | 💡 设想 |

### 当前版本的边界（Phase 1）

✅ **做到了**
- CLI 覆盖核心流程：init/start/check/advance/status/devlog/upgrade
- state.json 自动管理需求阶段、进度追踪、断点续做
- classifier 自动判定 L1/L2/L3，内嵌在 `start` 命令中
- BOUNDARY CHECK 强制阶段约束，不满足条件不推进
- AGENTS.md + skills 模板，AI 进项目就能自动读
- 240 测试覆盖 + ruff + mypy 全绿

⚠️ **已确认但有折中的**
- CLI 通过 `python -m aegis_toolchain` 调用，不在 PATH（无需配置，但用户需要知道这个命令）
- classifier（原 preprocessor 模块）不再有独立的 `aegis preprocess` 命令，内嵌在 `start` 中自动执行

❌ **Phase 1 承诺但未完成的**
- pre-commit hook → 暂缓：用户环境依赖链太长（需 pre-commit 包 + 手动 install），方案尚未成熟


## 许可证

MIT
