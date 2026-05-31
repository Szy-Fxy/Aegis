# Aegis v3.0.2 — 一键安装脚本
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

Write-Host "🛡️  Aegis v3.0.2 — 一键安装" -ForegroundColor Cyan
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

# 5. 创建 CLAUDE.md 入口（含完整行为准则）
$claudeContent = @"
# CLAUDE.md

> Aegis AI 开发治理系统 — 行为准则入口。AI 请同时加载 Aegis/skills/dev-workflow/SKILL.md。
> **Tradeoff**: 这些准则偏向工程严谨而非交付速度。对于简单任务，不必全部执行。

## 1. 先想再做 (Think Before Coding)

**不假设、不隐藏困惑、呈现权衡。**

- 明确列出假设。不确定就问。
- 如果存在多种理解，呈现它们 — 不要默默选一种。
- 如果有更简单的方案，说出来。该反驳时就反驳。
- 如果不清楚，停下来。指出哪里困惑。问。

## 2. 简洁至上 (Simplicity First)

**最小代码解决问题。不写推测性代码。**

- 不加没被要求的功能
- 不给只使用一次的代码写抽象
- 不加没被要求的「灵活性」或「可配置性」
- 不对不可能发生的场景做错误处理
- 200 行能写成 50 行就重写

自问：「一个高级工程师会觉得这是过度设计吗？」如果是，简化。

## 3. 精准修改 (Surgical Changes)

**只动必须动的。只清理你自己造成的烂摊子。**

- 不要「顺便优化」相邻代码、注释、格式
- 不要重构没坏的东西
- 匹配已有风格，即使你有不同偏好
- 如果注意到无关死代码，提出来 — 不要删
- 移除你的修改导致不再使用的 import / 变量 / 函数

测试标准：每一行改动都应该能追溯到用户的需求。

## 4. 目标驱动 (Goal-Driven Execution)

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

强成功标准让 AI 能独立循环验证。弱标准需要不断人工澄清。

---

**这些准则生效的标志：** diff 里不再有无关改动、不再因过度设计而重写、澄清性问题出现在实现之前。
"@
if (-not (Test-Path "CLAUDE.md")) {
    Set-Content -Path "CLAUDE.md" -Value $claudeContent
    Write-Host "✅ CLAUDE.md（入口 + 行为准则）" -ForegroundColor Green
} else {
    Write-Host "⚠️  CLAUDE.md 已存在，跳过。" -ForegroundColor Yellow
}

# 6. 创建 specs/INDEX.md
New-Item -ItemType Directory -Force -Path "specs" | Out-Null
if (-not (Test-Path "specs/INDEX.md")) {
    Set-Content -Path "specs/INDEX.md" -Value @"
# 需求索引

| ID | 需求名 | 级别 | 状态 | 开始日期 | 最后活动 |
|----|--------|------|------|----------|----------|
"@
    Write-Host "✅ specs/INDEX.md" -ForegroundColor Green
}

# 7. 清理
Remove-Item $TempZip -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🛡️  Aegis v3.0.2 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "   下一步：打开 AI 对话，正常提需求。AI 会自动按 Aegis 流程工作。"