# Aegis Toolchain

> 🛠️ Aegis AI 开发治理工具链 v0.1.0-beta
> 让流程约束从 AI 自律转向工具强制

---

## ⚠️ Aegis 纯 SKILL.md 版本已弃用

Aegis v3.1.x（纯 SKILL.md 文档驱动版本）已于 2026-06-05 起弃用，不再维护。

如需继续使用旧版本，请在 [Releases/Tags](https://github.com/Szy-Fxy/Aegis/releases) 中查找 `v3.1.0` 标签下载。

**推荐升级到 Aegis Toolchain**，获得结构化状态管理、独立 BOUNDARY CHECK 和 Git Hook 兜底防线。

---

## 什么是 Aegis Toolchain

Aegis AI 开发治理系统的外挂工具链。解决纯 SKILL.md 方案的三个致命缺陷：

| 旧方案（纯 SKILL.md） | 新方案（Toolchain） |
|---|---|
| AI 可能跳过规则，触发不可靠 | 预处理器 + CLI 辅助注入规则 |
| BOUNDARY CHECK 由 AI 自查自证 | `aegis check` 独立执行验证 |
| DevLog 文本描述，断点恢复不可靠 | `state.json` 结构化状态，精确断点续做 |
| 无 Git 层兜底 | pre-commit hook 阻断不合规提交 |

## 安装

**前提条件**: Python ≥ 3.11, Git ≥ 2.30, Poetry

```bash
git clone -b toolchain https://github.com/Szy-Fxy/Aegis.git aegis-toolchain
cd aegis-toolchain
pip install -e .

# 在 Aegis 项目中安装 Git Hook（可选）
cd /path/to/your-aegis-project
pre-commit install
```

## 快速开始

```bash
# 1. 开始一个需求
aegis start "鱼转向运动优化" --level L2

# 2. 查看状态
aegis status

# 3. BOUNDARY CHECK（设计文档创建后）
aegis check

# 4. 推进阶段
aegis advance

# 5. 写入 DevLog
aegis devlog write REQ-001 -m "完成转向优化"

# 6. 推进到完成
aegis advance

# 查看完整帮助
aegis --help
```

## 命令速查

| 命令 | 说明 |
|------|------|
| `aegis start <标题> -l <L1/L2/L3/auto>` | 开始新需求，自动分类 |
| `aegis check [REQ-ID]` | 执行 BOUNDARY CHECK |
| `aegis advance [REQ-ID] [-f]` | 推进到下一阶段 |
| `aegis status [REQ-ID] [--json]` | 查看项目状态 |
| `aegis devlog write <REQ-ID> -m <内容>` | 写入 DevLog |
| `aegis devlog show [REQ-ID]` | 查看 DevLog |
| `aegis preprocess <消息>` | 预处理用户消息 |

## 架构

```
src/aegis_toolchain/
├── cli/              # Typer CLI 命令
├── core/             # 核心逻辑（StateManager, BoundaryChecker, RuleLoader, IndexManager）
├── preprocessor/     # 预处理器（Classifier, Injector）
├── hooks/            # Git pre-commit hook
├── models/           # Pydantic 数据模型（AegisState, Requirement）
└── utils/            # 工具函数（loguru, 文件系统）
```

## 路线图

| 阶段 | 内容 | 状态 |
|------|------|------|
| Phase 1 | CLI + state.json + pre-commit hook | ✅ v0.1.0-beta |
| Phase 2 | MCP Server + YAML 状态机 | 📋 规划中 |
| Phase 3 | 全 MCP 生态 | 📋 规划中 |

## 许可

MIT
