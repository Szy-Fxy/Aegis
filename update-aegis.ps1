# Aegis 版本升级脚本
# 用法: ./update-aegis.ps1
# 在已有 Aegis 的项目根目录运行。下载最新版并替换 Aegis/，保留用户数据。

param(
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Get-Location).Path

# 1. 检查是否已安装 Aegis
if (-not (Test-Path "$ProjectRoot\Aegis")) {
    Write-Host "❌ 未找到 Aegis/ 目录。请先运行 install.ps1 安装。" -ForegroundColor Red
    exit 1
}

# 2. 检测当前版本
$CurrentVersion = "未知"
if (Test-Path "$ProjectRoot\Aegis\README.md") {
    $readmeContent = Get-Content "$ProjectRoot\Aegis\README.md" -Raw
    if ($readmeContent -match 'v(\d+\.\d+\.\d+)') {
        $CurrentVersion = "v$($matches[1])"
    }
}

Write-Host "🔄 Aegis 版本升级" -ForegroundColor Cyan
Write-Host "   当前版本: $CurrentVersion" -ForegroundColor Gray
Write-Host "   项目目录: $ProjectRoot" -ForegroundColor Gray
Write-Host ""

# 3. 确认升级
$confirm = Read-Host "确认升级到最新版？(y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "❌ 已取消。" -ForegroundColor Yellow
    exit 0
}

# 4. 备份用户数据
Write-Host "📦 备份用户数据..." -ForegroundColor Gray
$BackupDir = "$env:TEMP\aegis-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

$UserData = @(
    "Aegis/rules/DevLogs",
    "Aegis/rules/TempData",
    "Aegis_Specs"
)

foreach ($item in $UserData) {
    $src = Join-Path $ProjectRoot $item
    if (Test-Path $src) {
        $dst = Join-Path $BackupDir $item
        New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
        Copy-Item -Recurse -Force $src $dst
        Write-Host "  ✅ $item" -ForegroundColor Green
    }
}

# 备份入口文件
$EntryFiles = @("AGENTS.md", "CLAUDE.md", ".windsurfrules")
$EntryDirs  = @(".cursor", ".trae", ".github")

foreach ($entry in $EntryFiles) {
    $src = Join-Path $ProjectRoot $entry
    if (Test-Path $src) {
        Copy-Item -Force $src "$BackupDir\$entry"
        Write-Host "  ✅ $entry" -ForegroundColor Green
    }
}
foreach ($dir in $EntryDirs) {
    $src = Join-Path $ProjectRoot $dir
    if (Test-Path $src) {
        $dst = Join-Path $BackupDir $dir
        Copy-Item -Recurse -Force $src $dst
        Write-Host "  ✅ $dir/" -ForegroundColor Green
    }
}

Write-Host ""

# 5. 下载最新版
Write-Host "📥 下载最新版..." -ForegroundColor Gray
$RepoUrl = "https://github.com/Szy-Fxy/Aegis"
$ZipUrl  = "$RepoUrl/archive/refs/heads/$Branch.zip"
$TempZip = "$env:TEMP\aegis-update-$Branch.zip"
$TempDir = "$env:TEMP\aegis-update-$Branch"

try {
    Invoke-WebRequest -Uri $ZipUrl -OutFile $TempZip -UseBasicParsing
} catch {
    Write-Host "❌ 下载失败: $_" -ForegroundColor Red
    exit 1
}

# 6. 解压
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

# 7. 替换 Aegis/ 目录
Write-Host "🔄 替换 Aegis/ 目录..." -ForegroundColor Gray
Remove-Item -Recurse -Force "$ProjectRoot\Aegis"
Move-Item $ExtractedDir.FullName "$ProjectRoot\Aegis" -Force

# 8. 清理 Aegis 仓库自身文件
Remove-Item "$ProjectRoot\Aegis\Aegis_Specs" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$ProjectRoot\Aegis\install.ps1" -Force -ErrorAction SilentlyContinue
Remove-Item "$ProjectRoot\Aegis\install-aegis.ps1" -Force -ErrorAction SilentlyContinue
Remove-Item "$ProjectRoot\Aegis\CHANGELOG.md" -Force -ErrorAction SilentlyContinue
Remove-Item "$ProjectRoot\Aegis\BOOTSTRAP.md" -Force -ErrorAction SilentlyContinue
Remove-Item "$ProjectRoot\Aegis\AGENTS.md" -Force -ErrorAction SilentlyContinue
Remove-Item "$ProjectRoot\Aegis\CONTRIBUTING.md" -Force -ErrorAction SilentlyContinue
# 清理 .github/（Aegis 仓库的 Issue 模板，不是用户项目的）
Remove-Item "$ProjectRoot\Aegis\.github" -Recurse -Force -ErrorAction SilentlyContinue

# 9. 恢复用户数据
Write-Host "📦 恢复用户数据..." -ForegroundColor Gray
foreach ($item in $UserData) {
    $src = Join-Path $BackupDir $item
    $dst = Join-Path $ProjectRoot $item
    if (Test-Path $src) {
        if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
        New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
        Copy-Item -Recurse -Force $src $dst
        Write-Host "  ✅ $item" -ForegroundColor Green
    }
}

# 恢复入口文件
foreach ($entry in $EntryFiles) {
    $src = Join-Path $BackupDir $entry
    $dst = Join-Path $ProjectRoot $entry
    if (Test-Path $src) {
        Copy-Item -Force $src $dst
        Write-Host "  ✅ $entry" -ForegroundColor Green
    }
}
foreach ($dir in $EntryDirs) {
    $src = Join-Path $BackupDir $dir
    $dst = Join-Path $ProjectRoot $dir
    if (Test-Path $src) {
        if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
        Copy-Item -Recurse -Force $src $dst
        Write-Host "  ✅ $dir/" -ForegroundColor Green
    }
}

# 10. 清理备份
Remove-Item -Recurse -Force $BackupDir -ErrorAction SilentlyContinue
Remove-Item $TempZip -Force -ErrorAction SilentlyContinue

# 11. 验证升级结果
Write-Host ""
Write-Host "🔍 验证升级结果..." -ForegroundColor Gray
$VerifyScript = Join-Path $ProjectRoot "Aegis\install.ps1"
if (Test-Path $VerifyScript) {
    & $VerifyScript -Verify
} else {
    Write-Host "⚠️  无法运行验证脚本，请手动检查。" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🛡️  Aegis 升级完成！" -ForegroundColor Green
Write-Host "   旧版本: $CurrentVersion" -ForegroundColor Gray
Write-Host "   新版本: 最新版" -ForegroundColor Gray
Write-Host "   用户数据已保留：Aegis_Specs/、DevLogs/、TempData/、入口文件" -ForegroundColor Gray