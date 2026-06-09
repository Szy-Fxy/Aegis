# Aegis v5.2.2

> 让 AI 写代码不再放飞自我。自动分类 → 边界检查 → 阶段推进，全流程管住。

## 这是什么

Aegis 是一套 CLI 工具 + 规则文件。你装好之后，每次让 AI 写代码前跑一个命令，它就会自动判定需求等级，在 state.json 里记录进度，在每个阶段结束时强制做 BOUNDARY CHECK。写一半断掉了，下次 AI 读 state.json 就知道做到哪了。

## 装一个试试

```powershell
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

不用配 PATH，直接用：

```powershell
cd 你的项目
python -m aegis_toolchain init       # 生成 Aegis/ 规则文件和 AGENTS.md
python -m aegis_toolchain start "玩家背包系统" -l L2  # 登记一个需求
python -m aegis_toolchain status      # 看进度
python -m aegis_toolchain check       # 阶段检查
```

## AI 怎么用

1. AI 进入项目 → 读到 `AGENTS.md`
2. AGENTS.md 告诉它去读 `Aegis/skills/aegis-boot/SKILL.md`
3. SKILL.md 里写了每一步该执行什么命令：

```
python -m aegis_toolchain start "需求" -l L2   → 自动分类、登记到 state.json
python -m aegis_toolchain check                → BOUNDARY CHECK
python -m aegis_toolchain advance              → 推进到下一阶段
python -m aegis_toolchain devlog write REQ-001 -m "完成日志"
```

AI 不需要知道 CLI 在哪、classifier 在哪、state.json 怎么读——SKILL.md 里全写了。

## 命令速查

| 命令 | 作用 |
|------|------|
| `python -m aegis_toolchain init` | 初始化项目，生成规则文件和 AGENTS.md |
| `python -m aegis_toolchain start "标题" -l L2` | 登记新需求，自动分类（L1/L2/L3），创建 state.json |
| `python -m aegis_toolchain check` | 执行当前阶段的 BOUNDARY CHECK |
| `python -m aegis_toolchain advance` | 推进到下一阶段（内置 check，不通过不让过） |
| `python -m aegis_toolchain status` | 查看所有需求和当前状态 |
| `python -m aegis_toolchain upgrade` | 升级 Aegis 后同步项目规则文件 |
| `python -m aegis_toolchain devlog write REQ-001 -m "日志"` | 写开发日志 |
| `python -m aegis_toolchain devlog list` | 列出所有日志 |
| `python -m aegis_toolchain devlog show` | 查看最近一条日志 |

## 项目文件结构

`aegis init` 之后你的项目根目录会多出：

```
Aegis/
  rules/           # 全局规范、技术栈规则
  skills/          # AI 工作流引擎 (aegis-boot + dev-workflow)
  state/
    state.json     # 需求进度追踪（断点续做的基础）
Aegis_Specs/
  INDEX.md         # 需求索引表
AGENTS.md          # AI 入口文件
```

`state.json` 在第一次 `aegis start` 之后才会创建，不是 init 时生成的。

## 需求分级

| 级别 | 什么情况用 | 流程 |
|:---:|------|------|
| L1 | 改个 typo、修个配置、一行补丁 | 直接改，一条 devlog |
| L2 | 加功能、优化模块 | 5 阶段：设计 → 设计审查 → 实现 → 代码审查 → 验收 |
| L3 | 重构架构、大改动 | 7 阶段，带多轮审查 |

## 许可证

MIT
