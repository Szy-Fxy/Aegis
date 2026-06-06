# Aegis Toolchain 一键安装脚本
# 用法: 右键 → "使用 PowerShell 运行"，或在终端输入 .\install.ps1

Write-Host ""
Write-Host "  🔧 Aegis Toolchain v4.0.1 安装向导" -ForegroundColor Cyan
Write-Host "  ─────────────────────────────────────" -ForegroundColor Cyan
Write-Host ""

# 1. 检查 Python
Write-Host "[1/4] 检查 Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ 未找到 Python，请先安装 Python 3.11+" -ForegroundColor Red
    Write-Host "  下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按回车退出"
    exit 1
}
Write-Host "  ✅ $pythonVersion" -ForegroundColor Green

# 2. 选择安装目录
Write-Host ""
Write-Host "[2/4] 安装位置（直接回车 = 当前目录）" -ForegroundColor Yellow
$installPath = Read-Host "  路径"
if (-not $installPath) { $installPath = Get-Location }
Write-Host "  安装到: $installPath" -ForegroundColor Cyan

# 3. 克隆 / 更新
Write-Host ""
Write-Host "[3/4] 下载 Aegis Toolchain..." -ForegroundColor Yellow
$toolchainDir = Join-Path $installPath "aegis-toolchain"

if (Test-Path $toolchainDir) {
    Write-Host "  目录已存在，正在更新..." -ForegroundColor Cyan
    Set-Location $toolchainDir
    git pull 2>&1 | Out-Null
} else {
    git clone https://github.com/Szy-Fxy/Aegis.git $toolchainDir 2>&1
    Set-Location $toolchainDir
}
Write-Host "  ✅ 代码已就位" -ForegroundColor Green

# 4. 安装
Write-Host ""
Write-Host "[4/4] 安装依赖..." -ForegroundColor Yellow
pip install -e . 2>&1 | Select-Object -Last 3
Write-Host "  ✅ 安装完成" -ForegroundColor Green

# 验证
Write-Host ""
$aegisHelp = aegis --help 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  🎉 安装成功！Aegis Toolchain 已就绪。" -ForegroundColor Green
    Write-Host ""
    Write-Host "  下一步：" -ForegroundColor Cyan
    Write-Host "    1. 进入你的项目目录: cd 你的项目路径" -ForegroundColor White
    Write-Host "    2. 创建第一个需求: aegis start '我的需求' --level auto" -ForegroundColor White
    Write-Host "    3. 查看帮助: aegis --help" -ForegroundColor White
    Write-Host "    4. 完整教程: 打开 USAGE.md" -ForegroundColor White
} else {
    Write-Host "  ⚠️ 安装可能有问题，请检查 Python 版本（需要 3.11+）" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "按回车退出"
