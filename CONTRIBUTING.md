# 贡献指南

感谢你对 Aegis 的关注！无论是报告 Bug、提出建议还是提交代码，都是对项目的贡献。

---

## 报告 Bug

请在 [Issues](https://github.com/Szy-Fxy/Aegis/issues) 页面使用 **Bug Report** 模板。

报告前请确认：
- 你使用的是最新版本（`irm https://raw.githubusercontent.com/Szy-Fxy/Aegis/main/install.ps1 | iex` 安装的即最新版）
- 该 Bug 尚未被其他人报告（搜索已有 Issue）

一个好的 Bug 报告应该包含：
- Aegis 版本号、AI 平台/IDE、安装方式
- 清晰的问题描述和复现步骤
- 期望行为 vs 实际行为

---

## 提出功能建议

请在 [Issues](https://github.com/Szy-Fxy/Aegis/issues) 页面使用 **Feature Request** 模板。

建议前请思考：
- 这个功能解决什么问题？
- 谁会用？在什么场景下用？
- 是否与 Aegis 的核心理念一致（规范驱动、设计先行、验证闭环）？

---

## 提交代码

### 分支策略

```
main          ← 稳定发布分支（始终可用）
feat/xxx      ← 新功能分支，从 main 切出
fix/xxx       ← Bug 修复分支，从 main 切出
```

### 提交流程

1. Fork 本仓库
2. 从 `main` 切出你的分支：`git checkout -b feat/your-feature`
3. 在本地测试你的改动
4. 提交（遵循下方的提交规范）
5. 推送到你的 Fork
6. 发起 Pull Request 到本仓库的 `main` 分支

### 提交信息规范

```
vX.Y.Z [类型]: 简短描述（中文）

类型:
  Feature    — 新功能
  Fix        — Bug 修复
  Hotfix     — 紧急小修
  Refactor   — 重构（不改变行为）
  Docs       — 文档更新
```

示例：
```
v3.0.6 Feature: 新增 GitHub Issue 模板
v3.0.6 Hotfix: 修复安装脚本编码问题
```

### 代码风格

| 文件类型 | 规范 |
|----------|------|
| Markdown (.md) | UTF-8 编码，中文为主，关键术语保留英文 |
| PowerShell (.ps1) | `Set-Content` 必须加 `-Encoding UTF8`，变量用 `$CamelCase` |
| 所有文件 | 行尾不留空格，文件末尾一个空行 |

### 本地测试

改动安装脚本后，在本地测试：

```powershell
# 在测试目录中运行
cd D:\Test
.\Aegis\install.ps1

# 验证安装结果
.\Aegis\install.ps1 -Verify
```

### 改动 Aegis 自身规则时

Aegis 开发遵循自身的 [BOOTSTRAP.md](BOOTSTRAP.md) 规范。改动涉及安装脚本行为变更时，需要：
1. 更新 `CHANGELOG.md`（版本号 + 改动描述）
2. 更新 `docs/Aegis_Intro.md` 中的版本日志
3. 更新 `skills/dev-workflow/SKILL.md` 中的版本日志
4. 全局同步版本号（所有引用 `vX.Y.Z` 的文件）

---

## 文档贡献

文档改进同样是重要贡献。Aegis 的文档包括：

| 文件 | 面向读者 |
|------|----------|
| `README.md` | 所有人（项目首页） |
| `docs/QUICK_START.md` | 新用户（30 秒上手） |
| `docs/USER_GUIDE.md` | 用户（完整操作指南） |
| `docs/Aegis_Intro.md` | 开发者（项目介绍 + 版本历史） |
| `BOOTSTRAP.md` | Aegis 自身开发者（自举规范） |

文档原则：
- 用户文档用中文，面向不懂技术的用户
- 技术文档可以中英混用，但关键概念必须清晰
- 所有文档 UTF-8 编码

---

## 行为准则

- 尊重他人，友善交流
- 就事论事，关注代码和设计本身
- 帮助新人，分享经验

---

## 联系我们

- [GitHub Issues](https://github.com/Szy-Fxy/Aegis/issues) — Bug 报告和功能建议
- [GitHub Discussions](https://github.com/Szy-Fxy/Aegis/discussions) — 使用交流、经验分享