# Aegis Toolchain

> 🛠️ Aegis AI 开发治理工具链 v5.0.0
> 让流程约束从 AI 自律转向工具强制

---

## ⚠️ Aegis 纯 SKILL.md 版本已弃用

Aegis v3.1.x（纯 SKILL.md 文档驱动版本）已于 2026-06-05 起弃用。
旧版代码已归档到 [`legacy-v3.1`](../../tree/legacy-v3.1) 分支，tag `v3.1.0` 可下载。

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
详细指南：https://github.com/Szy-Fxy/Aegis/blob/main/USAGE.md
```bash
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

> 如果你电脑上没有 Python：打开 https://python.org 下载安装，安装时记得勾 "Add Python to PATH"。
> 安装完成后关掉 CMD 重新打开。

## 在你的项目里初始化

```bash
cd 你的游戏项目
 aegis init
```

## 开始开发

打开 Hana，打开你的项目文件夹，正常对话就行。
AI 会自动走 Aegis 流程：分类 → 设计 → 审查 → 实现 → 验收。

> 📘 **详细说明**: [USAGE.md](USAGE.md) — 从零开始的逐步教程

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
| Phase 1 | CLI + state.json + pre-commit hook | ✅ v5.0.0 |
| Phase 2 | MCP Server + YAML 状态机 | 📋 规划中 |
| Phase 3 | 全 MCP 生态 | 📋 规划中 |

## 许可

MIT
