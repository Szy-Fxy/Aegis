# Aegis Toolchain v4.0.1 一键安装脚本
# ──────────────────────────────────────────
# 用法 1: 右键 → "使用 PowerShell 运行" （推荐给小白）
# 用法 2: 在终端输入 .\install.ps1
#
# 两种安装模式:
#   [A] 极速安装（推荐）— 直接在终端用 aegis 命令，不下载源码
#   [B] 完整安装 — 下载全部源码到你的项目，方便修改和查看

$REPO_URL = "https://github.com/Szy-Fxy/Aegis.git"

Write-Host ""
Write-Host "  🔧 Aegis Toolchain v4.0.1 安装向导" -ForegroundColor Cyan
Write-Host "  ─────────────────────────────────────" -ForegroundColor Cyan
Write-Host ""

# ── 1. 检查 Python ──
Write-Host "[1/3] 检查 Python..." -ForegroundColor Yellow
$py = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ 未找到 Python，请先安装 Python 3.11+" -ForegroundColor Red
    Write-Host "  下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按回车退出"
    exit 1
}
Write-Host "  ✅ $py" -ForegroundColor Green

# ── 2. 选择模式 ──
Write-Host ""
Write-Host "  选一种安装方式:" -ForegroundColor Yellow
Write-Host "  [A] 极速安装 — 2 秒完成，任何目录都能用 aegis 命令" -ForegroundColor Cyan
Write-Host "  [B] 完整安装 — 下载全部源码到当前目录" -ForegroundColor Cyan
$mode = Read-Host "  输入 A 或 B（直接回车 = A）"
Write-Host ""

if ($mode -eq "B") {
    # ── 模式 B：完整安装（下载源码）──
    $targetDir = Join-Path (Get-Location) "aegis-toolchain"
    Write-Host "  📂 下载到: $targetDir" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  下载后你会看到这些文件:" -ForegroundColor Cyan
    Write-Host "    aegis-toolchain/" -ForegroundColor White
    Write-Host "    ├── README.md        ← 项目介绍" -ForegroundColor White
    Write-Host "    ├── USAGE.md         ← 使用教程（小白版 + 极客版）" -ForegroundColor White
    Write-Host "    ├── install.ps1      ← 这个安装脚本" -ForegroundColor White
    Write-Host "    ├── install.sh       ← Mac/Linux 安装脚本" -ForegroundColor White
    Write-Host "    ├── LICENSE          ← MIT 开源协议" -ForegroundColor White
    Write-Host "    ├── pyproject.toml   ← Python 项目配置" -ForegroundColor White
    Write-Host "    ├── CHANGELOG.md     ← 版本更新记录" -ForegroundColor White
    Write-Host "    ├── src/             ← 核心代码（26 个 .py 文件）" -ForegroundColor White
    Write-Host "    ├── tests/           ← 测试" -ForegroundColor White
    Write-Host "    └── docs/            ← 验收文档" -ForegroundColor White
    Write-Host ""

    Write-Host "[2/3] 下载源码..." -ForegroundColor Yellow
    if (Test-Path $targetDir) {
        Write-Host "  目录已存在，更新中..." -ForegroundColor Cyan
        Set-Location $targetDir
        git pull 2>&1 | Out-Null
    } else {
        git clone $REPO_URL $targetDir 2>&1
        Set-Location $targetDir
    }
    Write-Host "  ✅ 下载完成" -ForegroundColor Green

    Write-Host "[3/3] 安装依赖..." -ForegroundColor Yellow
    pip install -e . --quiet 2>&1 | Out-Null
    Write-Host "  ✅ 安装完成" -ForegroundColor Green

} else {
    # ── 模式 A：极速安装（不下载源码）──
    Write-Host "  ⚡ 极速安装：直接在终端用 aegis 命令，不下载源码" -ForegroundColor Cyan
    Write-Host "  这样你可以在任何目录下直接输入 aegis start xxx" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "[2/3] 下载并安装..." -ForegroundColor Yellow
    pip install "aegis-toolchain @ git+$REPO_URL" --quiet 2>&1 | Out-Null
    Write-Host "  ✅ 安装完成" -ForegroundColor Green
}

# ── 验证 ──
Write-Host ""
$ok = aegis --help 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  🎉 安装成功！Aegis Toolchain 已就绪。" -ForegroundColor Green
    Write-Host ""
    Write-Host "  试试这些命令：" -ForegroundColor Cyan
    Write-Host "    打开终端（任意目录）:" -ForegroundColor White
    Write-Host "      aegis --help          ← 查看所有命令" -ForegroundColor White
    Write-Host "      aegis start '我的需求' --level auto  ← 开始第一个需求" -ForegroundColor White
    Write-Host "      aegis status          ← 查看进度" -ForegroundColor White
    Write-Host ""

    if ($mode -eq "B") {
        Write-Host "  📖 完整教程打开: .\aegis-toolchain\USAGE.md" -ForegroundColor Cyan
    } else {
        Write-Host "  📖 查看教程: https://github.com/Szy-Fxy/Aegis/blob/main/USAGE.md" -ForegroundColor Cyan
    }
} else {
    Write-Host "  ⚠️ 安装可能有问题" -ForegroundColor Yellow
    Write-Host "  试试手动安装：pip install git+$REPO_URL" -ForegroundColor Yellow
}

Read-Host "`n按回车退出"
