#!/usr/bin/env bash
# Aegis Toolchain v4.0.1 一键安装脚本 (macOS / Linux)
# ───────────────────────────────────────────────────
# 用法: chmod +x install.sh && ./install.sh
#
# 两种安装模式:
#   [A] 极速安装 — 直接在终端用 aegis 命令，不下载源码
#   [B] 完整安装 — 下载全部源码到你的项目目录

REPO_URL="https://github.com/Szy-Fxy/Aegis.git"

echo ""
echo "  🔧 Aegis Toolchain v4.0.1 安装向导"
echo "  ─────────────────────────────────────"
echo ""

# 1. 检查 Python
echo "[1/3] 检查 Python..."
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &> /dev/null; then
        PYTHON="$cmd"
        break
    fi
done
if [ -z "$PYTHON" ]; then
    echo "  ❌ 未找到 Python，请先安装 Python 3.11+"
    exit 1
fi
echo "  ✅ $($PYTHON --version)"

# 2. 选择模式
echo ""
echo "  选一种安装方式:"
echo "  [A] 极速安装 — 2 秒完成，任何目录都能用 aegis 命令"
echo "  [B] 完整安装 — 下载全部源码到当前目录"
read -p "  输入 A 或 B（直接回车 = A）: " mode
mode=${mode:-A}
echo ""

if [ "$mode" = "B" ] || [ "$mode" = "b" ]; then
    # 完整安装
    TARGET_DIR="${PWD}/aegis-toolchain"
    echo "  📂 下载到: ${TARGET_DIR}"
    echo ""
    echo "  你会看到这些文件:"
    echo "    aegis-toolchain/"
    echo "    ├── README.md"
    echo "    ├── USAGE.md"
    echo "    ├── install.ps1 / install.sh"
    echo "    ├── LICENSE"
    echo "    ├── pyproject.toml"
    echo "    ├── src/  (26 个 .py 文件)"
    echo "    └── ..."
    echo ""

    echo "[2/3] 下载源码..."
    if [ -d "$TARGET_DIR" ]; then
        cd "$TARGET_DIR" && git pull
    else
        git clone "$REPO_URL" "$TARGET_DIR"
        cd "$TARGET_DIR"
    fi
    echo "  ✅ 下载完成"

    echo "[3/3] 安装依赖..."
    $PYTHON -m pip install -e . --quiet
    echo "  ✅ 安装完成"

    echo ""
    echo "  📖 完整教程: open ${TARGET_DIR}/USAGE.md"
else
    # 极速安装
    echo "  ⚡ 极速安装：不下载源码，任何目录都能用 aegis"
    echo ""
    echo "[2/3] 下载并安装..."
    $PYTHON -m pip install "aegis-toolchain @ git+${REPO_URL}" --quiet
    echo "  ✅ 安装完成"
fi

# 验证
if command -v aegis &> /dev/null; then
    echo ""
    echo "  🎉 安装成功！Aegis Toolchain 已就绪。"
    echo ""
    echo "  试试这些命令："
    echo "    aegis --help"
    echo "    aegis start '我的需求' --level auto"
    echo "    aegis status"
    echo ""
    echo "  📖 教程: https://github.com/Szy-Fxy/Aegis/blob/main/USAGE.md"
else
    echo ""
    echo "  ⚠️ aegis 命令未找到"
    echo "  试试: \$HOME/.local/bin 添加到 PATH"
fi
