# Aegis v3.0.3 — 一键安装脚本
# 用法: irm https://raw.githubusercontent.com/{你的用户名}/aegis/main/install.ps1 | iex
#
# 在你项目根目录运行。脚本会下载最新版 Aegis 到当前目录。

param(
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/Szy-Fxy/Aegis"
$ZipUrl  = "$RepoUrl/archive/refs/heads/$Branch.zip"
$TempZip = "$env:TEMP\aegis-$Branch.zip"
$TempDir = "$env:TEMP\aegis-$Branch"

Write-Host "🛡️  Aegis v3.0.3 — 一键安装" -ForegroundColor Cyan
Write-Host "   仓库: $RepoUrl" -ForegroundColor Gray
Write-Host ""

# 1. 检查是否已安装
if (Test-Path "Aegis") {
    Write-Host "⚠️  Aegis/ 已存在。如需重新安装请先删除。" -ForegroundColor Yellow
    exit 1
}

# 2. 下载
Write-Host "📥 下载中..." -ForegroundColor Gray
try {
    Invoke-WebRequest -Uri $ZipUrl -OutFile $TempZip -UseBasicParsing
} catch {
    Write-Host "❌ 下载失败: $_" -ForegroundColor Red
    Write-Host "   请检查仓库地址是否正确: $RepoUrl" -ForegroundColor Yellow
    exit 1
}

# 3. 解压
Write-Host "📦 解压中..." -ForegroundColor Gray
if (Test-Path $TempDir) { Remove-Item -Recurse -Force $TempDir }
Expand-Archive -Path $TempZip -DestinationPath "$env:TEMP" -Force

# GitHub 解压后的文件夹名是 "仓库名-分支名"
$ExtractedDir = Get-ChildItem "$env:TEMP" -Directory | 
    Where-Object { $_.Name -like "Aegis-*" -or $_.Name -like "aegis-*" } |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $ExtractedDir) {
    Write-Host "❌ 未找到解压后的 Aegis 文件夹" -ForegroundColor Red
    exit 1
}

# 4. 移动 Aegis/ 到当前目录
Move-Item $ExtractedDir.FullName "Aegis" -Force

# 5. 创建 Aegis_Protocol.md 入口（强制 Checklist + 行为准则）
$claudeContent = @"
# Aegis_Protocol.md

> ⚠️ **Aegis AI 开发治理系统 — 强制协议入口。本文件每项 Checklist 不可跳过。**
> AI 同时必须加载 `Aegis/skills/dev-workflow/SKILL.md` 获取完整工作流规则。
> **Tradeoff**: 简单任务（单行改值、typo 修复、L1 级别）不必全部执行。

---

## ⚠️ 强制 Checklist

### A. 对话启动（每轮对话开始时）

```
□ 1. 读取 Aegis/rules/DevLogs/ 下最新日期的 DevLog
□ 2. 告知用户：「上次您在 {需求名} 的 {阶段}，是否继续？」
□ 3. 如果 DevLog 为空，检查 Aegis_Specs/INDEX.md 是否有未完成的需求
```

### B. 需求操作（每次用户提需求时）

```
□ 4. 判定需求级别（L1 / L2 / L3）并告知用户
□ 5. 立刻更新 Aegis_Specs/INDEX.md（新需求登记）
□ 6. L2/L3：先出方案等你确认，不要直接写代码
```

### C. 阶段操作（每完成一个阶段时）

```
□ 7. L2/L3 每阶段结束 → 写 DevLog 到 Aegis/rules/DevLogs/
□ 8. 每阶段结束 → 告知用户当前阶段号和下一步
□ 9. L3 全部完成 → 执行收尾仪式（SKILL.md 中定义的 5 步骤）
```

### D. 自检（每次响应前过一遍）

```
□ 当前在哪个阶段？INDEX 更新了没？DevLog 写了没？
  → 有遗漏先补，再继续。
```

---

## AI 行为准则

### 1. 先想再做 (Think Before Coding)

**不假设、不隐藏困惑、呈现权衡。**

- 明确列出假设。不确定就问。
- 如果存在多种理解，呈现它们 — 不要默默选一种。
- 如果有更简单的方案，说出来。该反驳时就反驳。
- 如果不清楚，停下来。指出哪里困惑。问。

### 2. 简洁至上 (Simplicity First)

**最小代码解决问题。不写推测性代码。**

- 不加没被要求的功能
- 不给只使用一次的代码写抽象
- 不加没被要求的「灵活性」或「可配置性」
- 不对不可能发生的场景做错误处理
- 200 行能写成 50 行就重写

自问：「一个高级工程师会觉得这是过度设计吗？」如果是，简化。

### 3. 精准修改 (Surgical Changes)

**只动必须动的。只清理你自己造成的烂摊子。**

- 不要「顺便优化」相邻代码、注释、格式
- 不要重构没坏的东西
- 匹配已有风格，即使你有不同偏好
- 如果注意到无关死代码，提出来 — 不要删
- 移除你的修改导致不再使用的 import / 变量 / 函数

测试标准：每一行改动都应该能追溯到用户的需求。

### 4. 目标驱动 (Goal-Driven Execution)

**定义成功标准。循环直到验证通过。**

| 模糊任务 | 可验证目标 |
|----------|-----------|
| "加校验" | "写无效输入测试 → 让测试通过" |
| "修Bug" | "写能复现的测试 → 让测试通过" |
| "重构X" | "重构前后测试全部通过" |

多步骤任务输出计划：
```
1. [步骤] → 验证: [检查点]
2. [步骤] → 验证: [检查点]
3. [步骤] → 验证: [检查点]
```

---

**这些准则生效的标志：** diff 里不再有无关改动、不再因过度设计而重写、澄清性问题出现在实现之前。
"@
if (-not (Test-Path "Aegis_Protocol.md")) {
    Set-Content -Path "Aegis_Protocol.md" -Value $claudeContent
    Write-Host "✅ Aegis_Protocol.md（入口 + 行为准则）" -ForegroundColor Green
} else {
    Write-Host "⚠️  Aegis_Protocol.md 已存在，跳过。" -ForegroundColor Yellow
}

# 6. 创建 Aegis_Specs/INDEX.md
New-Item -ItemType Directory -Force -Path "Aegis_Specs" | Out-Null
if (-not (Test-Path "Aegis_Specs/INDEX.md")) {
    Set-Content -Path "Aegis_Specs/INDEX.md" -Value @"
# 需求索引

| ID | 需求名 | 级别 | 状态 | 开始日期 | 最后活动 |
|----|--------|------|------|----------|----------|
"@
    Write-Host "✅ Aegis_Specs/INDEX.md" -ForegroundColor Green
}

# 7. 清理安装脚本（不留在用户项目里）
Remove-Item "Aegis/install.ps1" -Force -ErrorAction SilentlyContinue
Remove-Item "Aegis/install-aegis.ps1" -Force -ErrorAction SilentlyContinue
Write-Host "🧹 已清理安装脚本" -ForegroundColor Gray

# 8. 清理临时文件
Remove-Item $TempZip -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🛡️  Aegis v3.0.3 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "   下一步：打开 AI 对话，正常提需求。AI 会自动按 Aegis 流程工作。"