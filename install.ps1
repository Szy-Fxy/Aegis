# Aegis v3.0.5 — 交互式安装脚本
# 用法: irm https://raw.githubusercontent.com/Szy-Fxy/Aegis/main/install.ps1 | iex
#
# 在你项目根目录运行。下载最新版 Aegis，让你选择 AI 入口。

param(
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/Szy-Fxy/Aegis"
$ZipUrl  = "$RepoUrl/archive/refs/heads/$Branch.zip"
$TempZip = "$env:TEMP\aegis-$Branch.zip"
$TempDir = "$env:TEMP\aegis-$Branch"

Write-Host "🛡️  Aegis v3.0.5 — 交互式安装" -ForegroundColor Cyan
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
    exit 1
}

# 3. 解压
Write-Host "📦 解压中..." -ForegroundColor Gray
if (Test-Path $TempDir) { Remove-Item -Recurse -Force $TempDir }
Expand-Archive -Path $TempZip -DestinationPath "$env:TEMP" -Force

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

# 5. 创建 Aegis_Specs/INDEX.md（含状态说明）
New-Item -ItemType Directory -Force -Path "Aegis_Specs" | Out-Null
if (-not (Test-Path "Aegis_Specs/INDEX.md")) {
    Set-Content -Encoding UTF8 -Path "Aegis_Specs/INDEX.md" -Value @"
# 需求索引

| ID | 需求名 | 级别 | 状态 | 开始日期 | 最后活动 |
|----|--------|------|------|----------|----------|

## 状态说明

| 状态 | 含义 |
|------|------|
| 🔨 implementing | 正在开发中 |
| ⏸️ paused | 已暂停（插队或阻塞） |
| ✅ done | 已完成并验收 |
| ❌ cancelled | 已取消 |
| 🔄 review | 等待审核 |

> AI 会在需求状态变更时自动更新此表。
"@
    Write-Host "✅ Aegis_Specs/INDEX.md" -ForegroundColor Green
}

# ============================================================
# 6. AI 入口选择
# ============================================================

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
            Write-Host "✅ AGENTS.md（通用 AI 入口）" -ForegroundColor Green
        } else {
            Write-Host "⚠️  AGENTS.md 已存在，跳过" -ForegroundColor Yellow
        }
    }
    "2" {
        if (-not (Test-Path "CLAUDE.md")) {
            Set-Content -Encoding UTF8 -Path "CLAUDE.md" -Value $agentsContent
            Write-Host "✅ CLAUDE.md（Claude Code 入口）" -ForegroundColor Green
        } else {
            Write-Host "⚠️  CLAUDE.md 已存在，跳过" -ForegroundColor Yellow
        }
    }
    "3" {
        New-Item -ItemType Directory -Force -Path ".cursor/rules" | Out-Null
        Set-Content -Encoding UTF8 -Path ".cursor/rules/aegis.mdc" -Value $cursorContent
        Write-Host "✅ .cursor/rules/aegis.mdc（Cursor IDE 入口）" -ForegroundColor Green
    }
    "4" {
        New-Item -ItemType Directory -Force -Path ".github" | Out-Null
        if (-not (Test-Path ".github/copilot-instructions.md")) {
            Set-Content -Encoding UTF8 -Path ".github/copilot-instructions.md" -Value $agentsContent
            Write-Host "✅ .github/copilot-instructions.md（Copilot 入口）" -ForegroundColor Green
        } else {
            Write-Host "⚠️  .github/copilot-instructions.md 已存在，跳过" -ForegroundColor Yellow
        }
    }
    "5" {
        New-Item -ItemType Directory -Force -Path ".trae/rules" | Out-Null
        if (-not (Test-Path ".trae/rules/project_rules.md")) {
            Set-Content -Encoding UTF8 -Path ".trae/rules/project_rules.md" -Value $agentsContent
            Write-Host "✅ .trae/rules/project_rules.md（Trae IDE 入口）" -ForegroundColor Green
        } else {
            Write-Host "⚠️  .trae/rules/project_rules.md 已存在，跳过" -ForegroundColor Yellow
        }
    }
    "6" {
        if (-not (Test-Path ".windsurfrules")) {
            Set-Content -Encoding UTF8 -Path ".windsurfrules" -Value $agentsContent
            Write-Host "✅ .windsurfrules（Windsurf 入口）" -ForegroundColor Green
        } else {
            Write-Host "⚠️  .windsurfrules 已存在，跳过" -ForegroundColor Yellow
        }
    }
    "7" {
        Write-Host "✅ Boot Skill 已就绪（见下方导入说明）" -ForegroundColor Green
    }
    "0" {
        Write-Host "ℹ️  已跳过入口安装。请手动配置。" -ForegroundColor Gray
    }
}

# 7. 清理 Aegis/ 内的 AGENTS.md（入口文件已在项目根目录）
Remove-Item "Aegis/AGENTS.md" -Force -ErrorAction SilentlyContinue

# 8. 清理 Aegis 仓库自身文件
Remove-Item "Aegis/Aegis_Specs" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "Aegis/install.ps1" -Force -ErrorAction SilentlyContinue
Remove-Item "Aegis/install-aegis.ps1" -Force -ErrorAction SilentlyContinue
Write-Host "🧹 已清理仓库自身文件" -ForegroundColor Gray

# 9. 清理临时文件
Remove-Item $TempZip -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🛡️  Aegis v3.0.5 安装完成！" -ForegroundColor Green

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
Write-Host "   下一步：打开 AI 对话，正常提需求即可。"