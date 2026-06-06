#!/usr/bin/env bash
# Aegis Toolchain 一键安装脚本 (macOS / Linux)
# 用法: chmod +x install.sh && ./install.sh

set -e

echo ""
echo "  🔧 Aegis Toolchain v4.0.1 安装向导"
echo "  ─────────────────────────────────────"
echo ""

# 1. 检查 Python
echo "[1/4] 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "  ❌ 未找到 Python3，请先安装 Python 3.11+"
    echo "  下载地址: https://www.python.org/downloads/"
    exit 1
fi
echo "  ✅ $(python3 --version)"

# 2. 安装目录
echo ""
echo "[2/4] 安装位置（直接回车 = 当前目录 ~/aegis-toolchain）"
read -p "  路径: " installPath
installPath=${installPath:-$HOME/aegis-toolchain}
echo "  安装到: $installPath"

# 3. 克隆 / 更新
echo ""
echo "[3/4] 下载 Aegis Toolchain..."
if [ -d "$installPath" ]; then
    echo "  目录已存在，正在更新..."
    cd "$installPath"
    git pull
else
    git clone https://github.com/Szy-Fxy/Aegis.git "$installPath"
    cd "$installPath"
fi
echo "  ✅ 代码已就位"

# 4. 安装
echo ""
echo "[4/4] 安装依赖..."
python3 -m pip install -e . --quiet
echo "  ✅ 安装完成"

# 验证
echo ""
if aegis --help &> /dev/null; then
    echo "  🎉 安装成功！Aegis Toolchain 已就绪。"
    echo ""
    echo "  下一步："
    echo "    1. 进入你的项目目录: cd 你的项目路径"
    echo "    2. 创建第一个需求: aegis start '我的需求' --level auto"
    echo "    3. 查看帮助: aegis --help"
    echo "    4. 完整教程: open USAGE.md"
else
    echo "  ⚠️ aegis 命令未找到，请确认 ~/.local/bin 在 PATH 中"
fi
