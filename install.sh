#!/usr/bin/env bash
# Aegis Toolchain 安装脚本 (macOS / Linux)
# chmod +x install.sh && ./install.sh

echo "🔧 Aegis Toolchain 安装中..."
PYTHON=""
for cmd in python3 python; do
    command -v "$cmd" &> /dev/null && PYTHON="$cmd" && break
done
if [ -z "$PYTHON" ]; then
    echo "❌ 需要 Python 3.11+: https://www.python.org/downloads/"
    exit 1
fi

"$PYTHON" -m pip install "git+https://github.com/Szy-Fxy/Aegis.git" --quiet
echo ""
echo "✅ 装好了！试试:"
echo ""
echo "   cd 你的项目目录"
echo "   aegis start '我的需求'"
echo ""
echo "📖 教程: https://github.com/Szy-Fxy/Aegis/blob/main/USAGE.md"
