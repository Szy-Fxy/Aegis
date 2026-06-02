# Aegis 用户手册

> 给人类看的。一步步教你如何在新项目中用上 Aegis。
> 预计阅读：3 分钟。操作：2 分钟。

---

## 新项目接入（从零开始）

### 方式一：一键安装（推荐）

在项目根目录打开终端，一条命令：

```powershell
irm https://raw.githubusercontent.com/Szy-Fxy/Aegis/main/install.ps1 | iex
```

不管在家、公司还是任何电脑，只要能上网，这条命令就能把最新版 Aegis 拉到当前项目。

### 方式二：手动复制

把 `Aegis/` 文件夹复制到新项目根目录。

```
你的新项目/
 Aegis/           安装脚本会自动创建
 src/             你原来的代码
 ...
```

一键安装会自动创建 `AGENTS.md`（跨平台 AI 通用入口）和 `Aegis_Specs/INDEX.md`。手动复制的话，在根目录创建 `AGENTS.md`，内容参考 `Aegis/AGENTS.md` 或直接写：

```
AI 请按 Aegis/skills/dev-workflow/SKILL.md 加载规则。
```

### 开始对话

打开 AI 对话，正常提需求就行了。

```
你：我要做一个背包系统，能拖拽物品、能堆叠
AI：好的，我判定这是 L2 需求，先出一份方案给你看...
```

你不用管 L1/L2/L3 是什么，AI 会自动判断。

---

## 激活 Aegis（不同平台）

### 安装时选择入口

安装脚本会让你选择 AI 入口。**只能选一个**，选你最常用的平台：

| 选项 | 入口文件 | 适用平台 |
|:----:|----------|----------|
| 1 | `AGENTS.md` | 通用标准，推荐 |
| 2 | `CLAUDE.md` | Claude Code |
| 3 | `.cursor/rules/aegis.mdc` | Cursor IDE |
| 4 | `.github/copilot-instructions.md` | GitHub Copilot |
| 5 | `.trae/rules/project_rules.md` | Trae IDE |
| 6 | `.windsurfrules` | Windsurf |
| 7 | Boot Skill | 兜底方案，所有平台通用 |

### 平台特定说明

| 平台 | 激活方式 |
|------|----------|
| **Claude Code** | 选择 [2] CLAUDE.md，Claude 自动读取 |
| **Cursor IDE** | 选择 [3] .cursor/rules/，Cursor 自动加载 |
| **Trae IDE** | 选择 [5] .trae/rules/，Trae 自动加载。或选 [7] Boot Skill 导入技能 |
| **GitHub Copilot** | 选择 [4] .github/copilot-，Copilot 自动读取 |
| **Windsurf** | 选择 [6] .windsurfrules，Windsurf 自动加载 |
| **其他工具** | 选择 [1] AGENTS.md（通用）或 [7] Boot Skill（技能导入） |

### Boot Skill（兜底方案）

**无论你选哪个入口，Boot Skill 都会被安装到 `Aegis/skills/aegis-boot/`。** 这是兜底机制——如果入口文件不生效，导入 Boot Skill 即可：

```powershell
# 1. 打开你的 AI 平台技能管理页面
# 2. 点击「导入技能」
# 3. 选择文件：Aegis/skills/aegis-boot/SKILL.md
# 4. 启用技能 → AI 处理开发任务时自动激活 Aegis
```

示例（Trae / HanaAgent）：
1. 打开平台 → 技能管理 → 导入
2. 选择 `Aegis/skills/aegis-boot/SKILL.md`
3. 启用后，AI 处理任何开发任务都会自动走 Aegis 流程

---

## 安装后你的项目长这样

```
你的新项目/
 Aegis/
    README.md               项目入口（AI 读这个）
    docs/
       USER_GUIDE.md        本文件
       QUICK_START.md       30 秒速览
       Aegis_Intro.md       项目详细介绍
    rules/
       global.md            全局代码规范
       TechStack/           9 个技术栈规范
       TempData/            临时资料（AI 自动管理）
       DevLogs/             开发日志（AI 自动写）
    skills/
       dev-workflow/        工作流引擎
       aegis-boot/          启动技能（兜底方案，始终安装）
 Aegis_Specs/
    INDEX.md                需求索引（含状态说明，AI 自动维护）
 AGENTS.md                  你选择的 AI 入口（安装时自选）
 你原来的代码...
```

大部分目录你不需要碰。你只管在 `Aegis_Specs/` 下看 AI 产出的需求文档就行。

---

## 日常使用

### 你只做三件事

| 你做什么 | AI 做什么 |
|----------|-----------|
| **提需求**：说你想做什么 | 判断大小、匹配技术栈、进入对应流程 |
| **审核**：AI 出方案后说 OK 或提出修改 | 生成方案文档，等你确认 |
| **验收**：功能做完后检查是否符合预期 | 出验证报告，写开发日志 |

### 审核时你怎么判断

AI 会给你看方案的「口语版」解释，你只需要判断：

- 这个方向对不对？
- 有没有漏掉什么？
- 有没有你不能接受的东西？

**不需要看懂技术细节。** 你是业务方，审的是「方向对不对」，不是「代码怎么写」。

---

## 三种需求、三种流程

你不需要主动选择。AI 根据你说的内容自动判定：

| 你说的 | AI 判定 | AI 做什么 |
|--------|:------:|-----------|
| 「把那个常量改成 100」 | L1 | 直接改代码，不废话 |
| 「加一个导出 CSV 的功能」 | L2 | 出方案  确认  写代码  验证 |
| 「我要重构整个架构」 | L3 | 分 7 步出文档  逐步审核  写代码  验证 |

---

## 常见场景

### 中途打断

你正在做一个大功能（L3），突然来了个紧急小修改。直接说：

> 「先停一下，帮我修个 XXX」

AI 会保存当前进度，插队修完小修改，然后问你是不是继续之前的大功能。

### 断线重连

你关了 IDE，明天再打开。AI 会自动读日志告诉你：

> 「上次您在 背包系统 的 方案设计阶段，是否继续？」

直接说「继续」就行。

### 方案不满意

> 「这个方案不行，重新想一个」
> 「回到阶段 2，用另一种思路」

AI 会退回重做，之前的文档不会丢。

---

## 你需要记住的只有三句话

```
「我要做 XXX」    提需求
「好」            审核通过
「回到上一步」    不满意、退回去
```

就这三句。其他全交给 AI。

---

## VCS 忽略配置

将以下内容添加到你的 `.gitignore`（可选但推荐）：

```
# Aegis 本地数据（不提交）
Aegis/rules/DevLogs/*.md
!Aegis/rules/DevLogs/README.md
Aegis/rules/TempData/*.md
!Aegis/rules/TempData/README.md
```

**建议提交**的文件：`AGENTS.md`、`Aegis_Specs/`、`Aegis/`（除 DevLogs/ 和 TempData/ 外）。

---

## FAQ

**Q: 我要换 AI 工具（从 A 换成 B）能用吗？**
A: 能。Aegis 不依赖任何特定 IDE 或 AI 工具。所有规则都是 Markdown 文件。

**Q: 技术栈文件里的东西不够用怎么办？**
A: AI 会自动上网搜索，搜到的资料存入 `TempData/`，用完后提炼精华写回 TechStack。

**Q: AI 会不会乱改我的代码？**
A: L2/L3 需求都会先出方案等你确认。L1 直接改但只改你指定的东西。

**Q: Aegis_Specs/ 目录下的文档谁看？**
A: 主要是 AI 看的，用来保证后续步骤不会偏离最初的设计。你也可以翻翻了解项目进展。

**Q: 我能跳过审核吗？**
A: 直接说「快速改」或「直接改」，AI 走 L1 通道跳过所有文档。
