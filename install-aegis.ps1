<#
.SYNOPSIS
    Aegis v3.0.5 — 跨 IDE AI 编程助手开发治理系统安装脚本
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

$AllTechStacks = @("python", "unity", "typescript", "unreal", "cpp", "go", "rust", "java", "docker")

if (-not $ProjectName) {
    $ProjectName = Split-Path -Leaf (Get-Location)
}

if ($TechStack -eq "") {
    $TechStack = $AllTechStacks -join ","
}

Write-Host "🛡️  Aegis v3.0.5 — 安装中..." -ForegroundColor Cyan
Write-Host "   项目名: $ProjectName" -ForegroundColor Gray
Write-Host "   技术栈: $($AllTechStacks -join ', ')（全部）" -ForegroundColor Gray
Write-Host ""

# Core directory structure
$Dirs = @(
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
    "Aegis/docs/Aegis_Intro.md"           = "$ScriptDir/docs/Aegis_Intro.md"
    "Aegis/AGENTS.md" = "$ScriptDir/AGENTS.md"
}

# Skill files
$SkillFiles = @{
    "Aegis/skills/dev-workflow/SKILL.md" = "$ScriptDir/skills/dev-workflow/SKILL.md"
}

# Boot Skill files (optional, for platforms that support Skill auto-trigger)
$BootSkillFiles = @{
    "Aegis/skills/aegis-boot/SKILL.md" = "$ScriptDir/skills/aegis-boot/SKILL.md"
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
    "go"         = "$ScriptDir/rules/TechStack/go.md"
    "rust"       = "$ScriptDir/rules/TechStack/rust.md"
    "java"       = "$ScriptDir/rules/TechStack/java.md"
    "docker"     = "$ScriptDir/rules/TechStack/docker.md"
}

if ($DryRun) {
    Write-Host "[DRY RUN] 将创建以下目录和文件：" -ForegroundColor Yellow
    Write-Host ""
    foreach ($dir in $Dirs) { Write-Host "  📁 $dir" }
    foreach ($key in $CoreFiles.Keys) { Write-Host "  📄 $key" }
    foreach ($key in $SkillFiles.Keys) { Write-Host "  📄 $key" }
    foreach ($key in $BootSkillFiles.Keys) { Write-Host "  📄 $key" }
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

# Copy Boot Skill (always available, regardless of entry choice)
foreach ($dest in $BootSkillFiles.Keys) {
    $src = $BootSkillFiles[$dest]
    if (Test-Path $src) {
        Copy-Item $src $dest -Force
        Write-Host "  ✅ $dest"
    } else {
        Write-Host "  ⚠️  Boot Skill 源文件不存在: $src" -ForegroundColor Yellow
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

# Create Aegis_Specs directory and INDEX.md
New-Item -ItemType Directory -Force -Path "Aegis_Specs" | Out-Null
$indexContent = @"
# 需求索引

> 项目需求追踪。新需求登记时立即更新此文件。

| ID | 需求名 | 级别 | 状态 | 开始日期 | 最后活动 |
|----|--------|------|------|----------|----------|

---

## 状态说明

| 状态 | 含义 |
|------|------|
| 📋 brainstorm | 方案讨论中 |
| 📋 proposal | 方案已定，待审核 |
| 📐 design | 技术设计中 |
| 📝 spec | 需求规格编写中 |
| 📋 review | 审核中 |
| 🔨 implementing | 代码实现中 |
| ✅ done | 已完成 |
| ⏸️ paused | 暂停 |
| ❌ cancelled | 取消 |

## 并发规则

- 同时只有一个需求处于 `🔨 implementing`
- L1 需求可插队执行，不阻塞当前 L2/L3
- L3 过程中收到 L2 需求：完成后从 DevLog 恢复 L3 进度

> AI 会在需求状态变更时自动更新此表。
"@
$indexPath = "Aegis_Specs/INDEX.md"
if (-not (Test-Path $indexPath)) {
    Set-Content -Encoding UTF8 -Path $indexPath -Value $indexContent
    Write-Host "  ✅ Aegis_Specs/INDEX.md"
} else {
    Write-Host "  ⚠️  Aegis_Specs/INDEX.md 已存在，跳过"
}

# Generate README.md
$readmeContent = @"
# $ProjectName — 项目入口

> 本项目使用 [Aegis v3.0.5](docs/Aegis_Intro.md) AI 开发治理系统。
> AI 请按 `Aegis/skills/dev-workflow/SKILL.md` 加载规则。

---

## 规则文件索引

| 文件 | 用途 | 触发条件 |
|------|------|----------|
| [Aegis/rules/global.md](rules/global.md) | 全局通用准则 | 始终加载 |
"@

if ($TechStack) {
    $stacks = $TechStack -split ',' | ForEach-Object { $_.Trim().ToLower() }
    foreach ($stack in $stacks) {
        $readmeContent += "| [Aegis/rules/TechStack/$stack.md](rules/TechStack/$stack.md) | $stack | $stack 相关需求 |`n"
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
详见 [Aegis/skills/dev-workflow/SKILL.md](skills/dev-workflow/SKILL.md)。
"@

Set-Content -Encoding UTF8 -Path "Aegis/README.md" -Value $readmeContent
Write-Host "  ✅ Aegis/README.md"

# ============================================================
# AI 入口选择
# ============================================================

# AGENTS.md content (universal entry)
$agentsContent = @"
# AI Agent Instructions

> This project uses **Aegis v3.0.5** — AI Development Governance System.

## BEFORE ANY CODE CHANGE

1. **Load the workflow engine**: `Aegis/skills/dev-workflow/SKILL.md`
2. **Classify the request**: L1 (trivial fix) / L2 (feature) / L3 (major refactor)
3. **L2 / L3**: Propose plan → get user approval → then code
4. **After each phase**: Write DevLog to `Aegis/rules/DevLogs/`

## Quick Self-Check (every response)

- [ ] What phase am I in? Updated `Aegis_Specs/INDEX.md`? Wrote DevLog?
- [ ] Any hardcoded credentials in my code?
- [ ] Did I expose production data or real secrets to AI?

## Core Rules

- Design before code (L2/L3)
- No hardcoded secrets — use `.env`
- Verify before closing — run tests, check acceptance criteria
- Always update `Aegis_Specs/INDEX.md`
- Every requirement (including L1) must be recorded in INDEX.md and DevLog

See `Aegis/docs/USER_GUIDE.md` for human documentation.
"@

$cursorContent = @"
---
description: Aegis v3.0.5 — AI 开发治理系统。行为准则 + 工程规范 + 工作流规则。始终生效。
alwaysApply: true
---

# Aegis v3.0.5 — AI 开发治理系统

> 规范驱动 · 设计先行 · 验证闭环 · 持续进化

## BEFORE ANY CODE CHANGE

1. **Load the workflow engine**: `Aegis/skills/dev-workflow/SKILL.md`
2. **Classify the request**: L1 (trivial fix) / L2 (feature) / L3 (major refactor)
3. **L2 / L3**: Propose plan → get user approval → then code
4. **After each phase**: Write DevLog to `Aegis/rules/DevLogs/`

## Quick Self-Check

- [ ] What phase am I in? Updated `Aegis_Specs/INDEX.md`? Wrote DevLog?
- [ ] Any hardcoded credentials in my code?
- [ ] Did I expose production data or real secrets to AI?

## Core Rules

- Design before code (L2/L3)
- No hardcoded secrets — use `.env`
- Verify before closing
- Always update `Aegis_Specs/INDEX.md`
- Every requirement (including L1) must be recorded in INDEX.md and DevLog

See `Aegis/docs/USER_GUIDE.md` for documentation.
"@

Write-Host ""
Write-Host "📋 选择 AI 入口（只能选一个）" -ForegroundColor Cyan
Write-Host "   [1] AGENTS.md          ← 通用标准，推荐"
Write-Host "   [2] CLAUDE.md          ← Claude Code"
Write-Host "   [3] .cursor/rules/     ← Cursor IDE"
Write-Host "   [4] .github/copilot-   ← GitHub Copilot"
Write-Host "   [5] .trae/rules/       ← Trae IDE"
Write-Host "   [6] .windsurfrules     ← Windsurf"
Write-Host "   [7] Boot Skill         ← 兜底方案，所有平台通用"
Write-Host "   [0] 跳过（手动配置）"
Write-Host ""

$entryChoice = Read-Host "输入数字（默认 1）"
if ($entryChoice -eq "") { $entryChoice = "1" }

switch ($entryChoice) {
    "1" {
        if (-not (Test-Path "AGENTS.md")) {
            Set-Content -Encoding UTF8 -Path "AGENTS.md" -Value $agentsContent
            Write-Host "  ✅ AGENTS.md（通用 AI 入口）"
        } else {
            Write-Host "  ⚠️  AGENTS.md 已存在，跳过"
        }
    }
    "2" {
        if (-not (Test-Path "CLAUDE.md")) {
            Set-Content -Encoding UTF8 -Path "CLAUDE.md" -Value $agentsContent
            Write-Host "  ✅ CLAUDE.md（Claude Code 入口）"
        } else {
            Write-Host "  ⚠️  CLAUDE.md 已存在，跳过"
        }
    }
    "3" {
        New-Item -ItemType Directory -Force -Path ".cursor/rules" | Out-Null
        Set-Content -Encoding UTF8 -Path ".cursor/rules/aegis.mdc" -Value $cursorContent
        Write-Host "  ✅ .cursor/rules/aegis.mdc（Cursor IDE 入口）"
    }
    "4" {
        New-Item -ItemType Directory -Force -Path ".github" | Out-Null
        if (-not (Test-Path ".github/copilot-instructions.md")) {
            Set-Content -Encoding UTF8 -Path ".github/copilot-instructions.md" -Value $agentsContent
            Write-Host "  ✅ .github/copilot-instructions.md（Copilot 入口）"
        } else {
            Write-Host "  ⚠️  .github/copilot-instructions.md 已存在，跳过"
        }
    }
    "5" {
        New-Item -ItemType Directory -Force -Path ".trae/rules" | Out-Null
        if (-not (Test-Path ".trae/rules/project_rules.md")) {
            Set-Content -Encoding UTF8 -Path ".trae/rules/project_rules.md" -Value $agentsContent
            Write-Host "  ✅ .trae/rules/project_rules.md（Trae IDE 入口）"
        } else {
            Write-Host "  ⚠️  .trae/rules/project_rules.md 已存在，跳过"
        }
    }
    "6" {
        if (-not (Test-Path ".windsurfrules")) {
            Set-Content -Encoding UTF8 -Path ".windsurfrules" -Value $agentsContent
            Write-Host "  ✅ .windsurfrules（Windsurf 入口）"
        } else {
            Write-Host "  ⚠️  .windsurfrules 已存在，跳过"
        }
    }
    "7" {
        Write-Host "  ✅ Boot Skill 已就绪（见下方导入说明）"
    }
    "0" {
        Write-Host "  ℹ️  已跳过入口安装。请手动配置。"
    }
}

# 清理 Aegis/ 内的 AGENTS.md（入口文件已在项目根目录）
Remove-Item "Aegis/AGENTS.md" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🛡️  Aegis v3.0.5 安装完成！" -ForegroundColor Green
Write-Host "   项目: $ProjectName"

# Boot Skill 导入说明
if ($entryChoice -eq "7") {
    Write-Host ""
    Write-Host "📋 Boot Skill 导入方法：" -ForegroundColor Cyan
    Write-Host "   1. 打开你的 AI 平台技能管理页面"
    Write-Host "   2. 点击「导入技能」"
    Write-Host "   3. 选择文件：Aegis/skills/aegis-boot/SKILL.md"
    Write-Host "   4. 启用技能 → AI 处理开发任务时自动激活 Aegis"
} else {
    Write-Host ""
    Write-Host "💡 提示：如果你的 AI 平台不支持入口文件，" -ForegroundColor Gray
    Write-Host "   可导入 Boot Skill：Aegis/skills/aegis-boot/SKILL.md" -ForegroundColor Gray
}

Write-Host ""

# VCS 忽略提示
Write-Host "📋 版本控制建议" -ForegroundColor Cyan
Write-Host "   以下文件建议纳入版本控制："
Write-Host "     ✅ AGENTS.md / CLAUDE.md（AI 入口）"
Write-Host "     ✅ Aegis/（规则引擎，DevLogs/ 和 TempData/ 除外）"
Write-Host "     ✅ Aegis_Specs/（需求文档）"
Write-Host "   以下文件建议忽略（不提交）："
Write-Host "     ❌ Aegis/rules/DevLogs/*.md（本地开发日志）"
Write-Host "     ❌ Aegis/rules/TempData/*.md（临时参考资料）"
Write-Host ""
Write-Host "   Git 用户：将以下内容复制到 .gitignore："
Write-Host "   ─────────────────────────"
Write-Host "   # Aegis 本地数据"
Write-Host "   Aegis/rules/DevLogs/*.md"
Write-Host "   !Aegis/rules/DevLogs/README.md"
Write-Host "   Aegis/rules/TempData/*.md"
Write-Host "   !Aegis/rules/TempData/README.md"
Write-Host "   ─────────────────────────"
Write-Host ""
Write-Host "   下一步：打开 AI 对话，正常提需求即可。"