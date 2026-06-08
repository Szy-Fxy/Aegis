# Aegis Toolchain v5.2.1

> AI 开发治理工具链。从需求登记到验收，全流程自动化。

## 安装

```powershell
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

## 怎么用（最重要）

安装后不用管 PATH，直接 `python -m aegis_toolchain` 就能用：

```powershell
cd 你的项目
python -m aegis_toolchain init          # 初始化规则文件
python -m aegis_toolchain start "需求" -l L2  # 登记需求（自动判定 L1/L2/L3）
python -m aegis_toolchain status         # 查看进度
python -m aegis_toolchain check          # BOUNDARY CHECK
python -m aegis_toolchain advance         # 推进到下一阶段
```

写一个需求的完整流程：**init → start → check → advance → devlog → done**

## 东西都在哪

| 你关心的 | 位置 | 作用 |
|---------|------|------|
| CLI | `python -m aegis_toolchain` | 7 个命令：init/start/check/advance/status/upgrade/devlog |
| 分类器（自动判定 L1/L2/L3） | 内嵌在 `aegis start` 里，不需要手动调 | 根据修改范围自动分类 |
| state.json | `项目/Aegis/state/state.json` | 记录需求 ID、阶段、时间。断点续做的基础 |
| 规则文件 | `项目/Aegis/rules/` + `Aegis/skills/` | 系统自动读取，不需要人管 |
| AGENTS.md | 项目根目录 | 给 AI 看的入口文件 |

## AI 怎么跟这个工具配合

AI 进入项目后读到 `AGENTS.md` → 加载 `Aegis/skills/aegis-boot/SKILL.md` → 按要求走流程：分类需求 → `aegis start` 登记 → `aegis check` 检查 → `aegis advance` 推进 → `aegis devlog` 记录。

## 命令速查

| 命令 | 作用 |
|------|------|
| `python -m aegis_toolchain init` | 初始化项目 |
| `python -m aegis_toolchain start "标题" -l L2` | 登记需求 |
| `python -m aegis_toolchain check` | BOUNDARY CHECK |
| `python -m aegis_toolchain advance` | 推进阶段 |
| `python -m aegis_toolchain status` | 查看状态 |
| `python -m aegis_toolchain upgrade` | 升级后同步规则 |
| `python -m aegis_toolchain devlog write REQ-001 -m "日志"` | 写 DevLog |

## 许可证

MIT
