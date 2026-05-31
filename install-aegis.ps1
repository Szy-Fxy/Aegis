<#
.SYNOPSIS
    Aegis v3.0.2 — 跨 IDE AI 编程助手开发治理系统安装脚本
.DESCRIPTION
    在新项目根目录运行此脚本，自动创建 Aegis 全套目录结构和规则文件。
    不依赖任何特定 IDE（支持 SOLO / OpenHanako / OpenCode 等）。
.PARAMETER TechStack
    逗号分隔的技术栈列表。可选值：python, unity, typescript, unreal, cpp
    不指定则默认安装全部技术栈。
    示例：-TechStack "unity,python"
.PARAMETER ProjectName
    项目名称，用于 DevLog 默认前缀。不提供则使用当前目录名。
.PARAMETER DryRun
    仅显示将创建的文件，不实际创建。
.EXAMPLE
    .\install-aegis.ps1
    .\install-aegis.ps1 -TechStack "unity,python"
    .\install-aegis.ps1 -TechStack "typescript" -ProjectName "MyWebApp"
#>

param(
    [string]$TechStack = "",
    [string]$ProjectName = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$AllTechStacks = @("python", "unity", "typescript", "unreal", "cpp")

if (-not $ProjectName) {
    $ProjectName = Split-Path -Leaf (Get-Location)
}

if ($TechStack -eq "") {
    $TechStack = $AllTechStacks -join ","
}

Write-Host "🛡️  Aegis v3.0.2 — 安装中..." -ForegroundColor Cyan
Write-Host "   项目名: $ProjectName" -ForegroundColor Gray
Write-Host "   技术栈: $($AllTechStacks -join ', ')（全部）" -ForegroundColor Gray
Write-Host ""

# Core directory structure
$Dirs = @(
    "Aegis/.cursor/rules",
    "Aegis/rules/TechStack",
    "Aegis/rules/TempData",
    "Aegis/rules/DevLogs",
    "Aegis/skills/dev-workflow/templates",
    "Aegis/skills/dev-workflow/conventions"
)

# Core files to copy from the source Aegis installation
$CoreFiles = @{
    "Aegis/rules/global.md"    = "$ScriptDir/rules/global.md"
    "Aegis/rules/DevLogs/README.md" = "$ScriptDir/rules/DevLogs/README.md"
    "Aegis/rules/TempData/README.md" = "$ScriptDir/rules/TempData/README.md"
    "Aegis/.cursor/rules/aegis.mdc" = "$ScriptDir/.cursor/rules/aegis.mdc"
    "Aegis/Aegis.md"           = "$ScriptDir/Aegis.md"
}

# Skill files
$SkillFiles = @{
    "Aegis/skills/dev-workflow/SKILL.md" = "$ScriptDir/skills/dev-workflow/SKILL.md"
}

# Template files
$TemplateFiles = @{
    "Aegis/skills/dev-workflow/templates/meta-spec.md"   = "$ScriptDir/skills/dev-workflow/templates/meta-spec.md"
    "Aegis/skills/dev-workflow/templates/brainstorm.md"  = "$ScriptDir/skills/dev-workflow/templates/brainstorm.md"
    "Aegis/skills/dev-workflow/templates/proposal.md"    = "$ScriptDir/skills/dev-workflow/templates/proposal.md"
    "Aegis/skills/dev-workflow/templates/design.md"      = "$ScriptDir/skills/dev-workflow/templates/design.md"
    "Aegis/skills/dev-workflow/templates/spec-L3.md"     = "$ScriptDir/skills/dev-workflow/templates/spec-L3.md"
    "Aegis/skills/dev-workflow/templates/spec-L2.md"     = "$ScriptDir/skills/dev-workflow/templates/spec-L2.md"
    "Aegis/skills/dev-workflow/templates/tasks.md"       = "$ScriptDir/skills/dev-workflow/templates/tasks.md"
    "Aegis/skills/dev-workflow/templates/review.md"      = "$ScriptDir/skills/dev-workflow/templates/review.md"
    "Aegis/skills/dev-workflow/templates/verify.md"      = "$ScriptDir/skills/dev-workflow/templates/verify.md"
    "Aegis/skills/dev-workflow/conventions/naming-and-formats.md" = "$ScriptDir/skills/dev-workflow/conventions/naming-and-formats.md"
}

# TechStack file mapping
$TechStackFiles = @{
    "python"     = "$ScriptDir/rules/TechStack/python.md"
    "unity"      = "$ScriptDir/rules/TechStack/unity.md"
    "typescript" = "$ScriptDir/rules/TechStack/typescript.md"
    "unreal"     = "$ScriptDir/rules/TechStack/unreal.md"
    "cpp"        = "$ScriptDir/rules/TechStack/cpp.md"
}

if ($DryRun) {
    Write-Host "[DRY RUN] 将创建以下目录和文件：" -ForegroundColor Yellow
    Write-Host ""
    foreach ($dir in $Dirs) { Write-Host "  📁 $dir" }
    foreach ($key in $CoreFiles.Keys) { Write-Host "  📄 $key" }
    foreach ($key in $SkillFiles.Keys) { Write-Host "  📄 $key" }
    foreach ($key in $TemplateFiles.Keys) { Write-Host "  📄 $key" }

    if ($TechStack) {
        $stacks = $TechStack -split ',' | ForEach-Object { $_.Trim().ToLower() }
        foreach ($stack in $stacks) {
            if ($TechStackFiles.ContainsKey($stack)) {
                Write-Host "  📄 Aegis/rules/TechStack/$stack.md"
            }
        }
    }

    Write-Host ""
    Write-Host "  📄 Aegis/README.md"
    exit 0
}

# Create directories
foreach ($dir in $Dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Write-Host "  ✅ $dir"
}

# Copy core files
foreach ($dest in $CoreFiles.Keys) {
    $src = $CoreFiles[$dest]
    if (Test-Path $src) {
        Copy-Item $src $dest -Force
        Write-Host "  ✅ $dest"
    } else {
        Write-Host "  ⚠️  跳过（源文件不存在）: $src"
    }
}

# Copy skill files
foreach ($dest in $SkillFiles.Keys) {
    $src = $SkillFiles[$dest]
    if (Test-Path $src) {
        Copy-Item $src $dest -Force
        Write-Host "  ✅ $dest"
    }
}

# Copy template files
foreach ($dest in $TemplateFiles.Keys) {
    $src = $TemplateFiles[$dest]
    if (Test-Path $src) {
        Copy-Item $src $dest -Force
        Write-Host "  ✅ $dest"
    }
}

# Copy TechStack files
if ($TechStack) {
    $stacks = $TechStack -split ',' | ForEach-Object { $_.Trim().ToLower() }
    foreach ($stack in $stacks) {
        if ($TechStackFiles.ContainsKey($stack)) {
            $src = $TechStackFiles[$stack]
            if (Test-Path $src) {
                Copy-Item $src "Aegis/rules/TechStack/$stack.md" -Force
                Write-Host "  ✅ Aegis/rules/TechStack/$stack.md"
            }
        } else {
            Write-Host "  ⚠️  未知技术栈（跳过）: $stack"
        }
    }
}

# Copy install script itself
Copy-Item $MyInvocation.MyCommand.Path "Aegis/install-aegis.ps1" -Force
Write-Host "  ✅ Aegis/install-aegis.ps1"

# Create specs directory and INDEX.md
New-Item -ItemType Directory -Force -Path "specs" | Out-Null
$indexContent = @"
# 需求索引

| ID | 需求名 | 级别 | 状态 | 开始日期 | 最后活动 |
|----|--------|------|------|----------|----------|
"@
$indexPath = "specs/INDEX.md"
if (-not (Test-Path $indexPath)) {
    Set-Content -Path $indexPath -Value $indexContent
    Write-Host "  ✅ specs/INDEX.md"
} else {
    Write-Host "  ⚠️  specs/INDEX.md 已存在，跳过"
}

# Generate README.md
$readmeContent = @"
# $ProjectName — 项目入口

> 本项目使用 [Aegis v3.0.2](Aegis/Aegis.md) AI 开发治理系统。
> AI 请按 `Aegis/skills/dev-workflow/SKILL.md` 加载规则。

---

## 规则文件索引

| 文件 | 用途 | 触发条件 |
|------|------|----------|
| [Aegis/rules/global.md](Aegis/rules/global.md) | 全局通用准则 | 始终加载 |
"@

if ($TechStack) {
    $stacks = $TechStack -split ',' | ForEach-Object { $_.Trim().ToLower() }
    foreach ($stack in $stacks) {
        $readmeContent += "| [Aegis/rules/TechStack/$stack.md](Aegis/rules/TechStack/$stack.md) | $stack | $stack 相关需求 |`n"
    }
}

$readmeContent += @"

---

## 项目特殊规则

> 在此处追加项目级覆盖规则。

- 示例：Unity 版本固定为 2022.3 LTS
- 示例：Python 最低版本 3.11

---

## 工作流

所有需求遵循 Aegis L1 / L2 / L3 分级流程。
详见 [Aegis/skills/dev-workflow/SKILL.md](Aegis/skills/dev-workflow/SKILL.md)。
"@

Set-Content -Path "Aegis/README.md" -Value $readmeContent
Write-Host "  ✅ Aegis/README.md"

# Create CLAUDE.md with full behavioral guidelines
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
    Write-Host "  ✅ CLAUDE.md（入口 + 行为准则）"
} else {
    Write-Host "  ⚠️  CLAUDE.md 已存在，跳过"
}

Write-Host ""
Write-Host "🛡️  Aegis v3.0.2 安装完成！" -ForegroundColor Green
Write-Host "   项目: $ProjectName"
Write-Host "   技术栈: $($AllTechStacks -join ', ')（全部）"
Write-Host ""
Write-Host "   下一步：在项目根目录创建 specs/INDEX.md 开始使用"