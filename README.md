# Aegis  AI 开发治理系统

> 规范驱动  设计先行  验证闭环  持续进化

Aegis 是一套面向 AI 编程助手的开发治理系统。它的目标不是让 AI 写代码更快，而是确保 AI 以可审计、可追溯、可维护的软件工程方式进行开发。

---

## 解决的问题

AI 编程助手常见的问题：

- **默默假设、不问澄清**  选了错误的理解就开始写代码
- **过度设计、臃肿抽象**  100 行能搞定的事写成 1000 行
- **顺手改动无关代码**  修 Bug 时改了注释、格式、变量名
- **模糊目标、无验证**  "把认证系统修好" 没有成功标准

Aegis 通过**行为准则 + 分级流程 + 验证闭环**直接解决这些问题。

---

## 四大原则

| 原则 | 解决的问题 |
|------|-----------|
| **先想再做** | 错误假设、隐藏困惑、缺少权衡 |
| **简洁至上** | 过度设计、臃肿抽象、推测性功能 |
| **精准修改** | 无关改动、顺手重构、风格漂移 |
| **目标驱动** | 模糊目标  可验证成功标准  循环验证 |

> 来自 [Andrej Karpathy 对 LLM 编程错误的观察](https://x.com/karpathy/status/2015883857489522876)，融入 Aegis 工作流。

---

## 三种需求、三种流程

| 你说的话 | AI 判定 | AI 做什么 |
|----------|:------:|-----------|
| "把常量改成 100" | L1 | 直接改代码，不废话 |
| "加一个导出 CSV 的功能" | L2 | 出方案  确认  写代码  验证 |
| "重构整个架构" | L3 | 7 阶段文档  逐步审核  实现  收尾 |

你不用管 L1/L2/L3 是什么，AI 自动判断。

---

## 安装

### 一键安装（推荐）

在你项目根目录打开终端：

```powershell
irm https://raw.githubusercontent.com/Szy-Fxy/Aegis/main/install.ps1 | iex
```

不管在家、公司还是任何电脑，只要能上网就能安装。

### Cursor IDE

Aegis 内置 `.cursor/rules/aegis.mdc`，复制到项目后 Cursor 自动加载。

### 手动复制

把 `Aegis/` 文件夹复制到新项目根目录。安装脚本会自动生成含完整行为准则的 `CLAUDE.md`。手动复制时，在根目录创建 `CLAUDE.md`，推荐复制 `Aegis/README.md` 中的行为准则内容，或最少写一句：

```
AI 请按 Aegis/skills/dev-workflow/SKILL.md 加载规则。
```

---

## 支持的环境

| 环境 | 支持方式 |
|------|----------|
| Claude Code | `CLAUDE.md` 入口文件 |
| Cursor | `.cursor/rules/aegis.mdc`（自动加载） |
| OpenHanako / OpenCode | `skills/dev-workflow/SKILL.md`（Skill 目录） |
| 其他 AI 工具 | 所有规则均为 Markdown，任意工具可读 |

---

## 如何判断生效了

这些准则生效的标志：

- **diff 里没有无关改动**  只出现被请求的修改
- **不再因过度设计重写**  代码第一次就简洁
- **澄清性问题出现在实现之前**  而不是出错之后
- **PR 干净精炼**  没有顺手重构或 "优化"

---

## 目录结构

```
Aegis/
 README.md                         本文件（AI 入口）
 Aegis.md                          项目详细介绍
 USER_GUIDE.md                     人类用户手册
 QUICK_START.md                    30 秒快速开始
 install.ps1                       一键安装脚本

 rules/
    global.md                     全局准则（SOLID + 安全 + 行为准则）
    TechStack/                    5 个技术栈规范（引子）
    TempData/                     临时参考资料
    DevLogs/                      开发日志存档

 skills/dev-workflow/
    SKILL.md                      核心工作流引擎
    templates/                    阶段文档模板（9个）
    conventions/                  命名和格式约定

 .cursor/rules/aegis.mdc          Cursor IDE 自动规则
```

---

## 快速开始

📖 人类用户：[QUICK_START.md](QUICK_START.md)（30秒）或 [USER_GUIDE.md](USER_GUIDE.md)（5分钟）

🤖 AI 用户：直接对话提需求，AI 自动按 Aegis 流程工作。

---

## 技术栈覆盖

| 技术栈 | 文件 |
|--------|------|
| Python | [rules/TechStack/python.md](rules/TechStack/python.md) |
| Unity / C# | [rules/TechStack/unity.md](rules/TechStack/unity.md) |
| TypeScript / Node.js | [rules/TechStack/typescript.md](rules/TechStack/typescript.md) |
| Unreal Engine | [rules/TechStack/unreal.md](rules/TechStack/unreal.md) |
| C++ | [rules/TechStack/cpp.md](rules/TechStack/cpp.md) |

遇到不在列表中的技术栈，AI 会自动搜索  审查  生成新的 TechStack 文件。

---

## 版本

v3.0.2  完整介绍见 [Aegis.md](Aegis.md)
