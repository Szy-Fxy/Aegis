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

# 5. 复制 Aegis_Protocol.md 到项目根目录（然后删除 Aegis/ 内的副本）
if (-not (Test-Path "Aegis_Protocol.md")) {
    Copy-Item "Aegis/Aegis_Protocol.md" "." -Force
    Remove-Item "Aegis/Aegis_Protocol.md" -Force
    Write-Host "✅ Aegis_Protocol.md（入口 + 行为准则）" -ForegroundColor Green
} else {
    Write-Host "⚠️  Aegis_Protocol.md 已存在，跳过。" -ForegroundColor Yellow
    Remove-Item "Aegis/Aegis_Protocol.md" -Force -ErrorAction SilentlyContinue
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