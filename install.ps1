# Aegis Toolchain 安装脚本
# 右键 → "使用 PowerShell 运行"，几秒钟完事

Write-Host "🔧 Aegis Toolchain 安装中..." -ForegroundColor Cyan

$ok = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 需要 Python 3.11+，请先安装: https://www.python.org/downloads/" -ForegroundColor Red
    Read-Host "按回车退出"
    exit 1
}

pip install "git+https://github.com/Szy-Fxy/Aegis.git" --quiet 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ 装好了！现在打开终端，试试:" -ForegroundColor Green
    Write-Host ""
    Write-Host "   cd 你的项目目录" -ForegroundColor White
    Write-Host "   aegis start '我的需求'" -ForegroundColor White
    Write-Host ""
    Write-Host "📖 教程: https://github.com/Szy-Fxy/Aegis/blob/main/USAGE.md" -ForegroundColor Cyan
} else {
    Write-Host "❌ 安装失败，试试手动装:" -ForegroundColor Red
    Write-Host "   pip install git+https://github.com/Szy-Fxy/Aegis.git" -ForegroundColor Yellow
}

Read-Host "按回车退出"
