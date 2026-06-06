"""aegis init — 初始化项目 Aegis 规则文件"""

import shutil
from pathlib import Path

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # Python < 3.11 fallback

import typer
from loguru import logger


def init_project(force: bool = False) -> None:
    """将 Aegis 规则文件安装到当前项目目录。

    从 aegis-toolchain 包内 data/ 目录复制到当前工作目录下的 Aegis/，
    同时创建空的 Aegis_Specs/ 和 INDEX.md。
    """
    cwd = Path.cwd()
    target = cwd / "Aegis"
    specs = cwd / "Aegis_Specs"

    # 检查是否已初始化
    if target.exists() and not force:
        existing = list(target.rglob("*"))
        if any(f.is_file() for f in existing):
            logger.warning(f"Aegis/ 已存在且非空。使用 --force 覆盖")
            raise typer.Exit(0)

    try:
        data_root = files("aegis_toolchain.data")
    except Exception as e:
        logger.error(f"无法找到内置规则数据: {e}")
        raise typer.Exit(1)

    # 复制 rules
    _copy_dir(data_root, "rules", target / "rules")

    # 复制 skills
    _copy_dir(data_root, "skills", target / "skills")

    # 创建 specs 目录和 INDEX.md
    specs.mkdir(parents=True, exist_ok=True)
    index_path = specs / "INDEX.md"
    if not index_path.exists():
        index_path.write_text(
            "# 需求索引\n\n"
            "> Aegis 项目需求追踪。新需求登记时立即更新此文件。\n\n"
            "| ID | 需求名 | 级别 | 状态 | 开始日期 | 最后活动 |\n"
            "|----|--------|------|------|----------|----------|\n\n"
            "---\n\n"
            "## 状态说明\n\n"
            "| 状态 | 含义 |\n"
            "|------|------|\n"
            "| 📋 brainstorm | 方案讨论中 |\n"
            "| 📋 proposal | 方案已定，待审核 |\n"
            "| 📐 design | 技术设计中 |\n"
            "| 📋 review_design | 设计审查中 |\n"
            "| 📝 spec | 需求规格编写中 |\n"
            "| 📋 review | 审核中 |\n"
            "| 🔨 implementing | 代码实现中 |\n"
            "| 📋 review_code | 代码审查中 |\n"
            "| ✅ verify | 验收中 |\n"
            "| ✅ done | 已完成 |\n"
            "| ⏸️ paused | 暂停 |\n"
            "| ❌ cancelled | 取消 |\n\n"
            "## 并发规则\n\n"
            "- 同时只有一个需求处于 `🔨 implementing`\n"
            "- L1 需求可插队执行，不阻塞当前 L2/L3\n"
            "- L3 过程中收到 L2 需求：完成后从 DevLog 恢复 L3 进度\n\n"
            "> AI 会在需求状态变更时自动更新此表。\n",
            encoding="utf-8",
        )

    # 创建 DevLogs 目录
    (target / "rules" / "DevLogs").mkdir(parents=True, exist_ok=True)

    # 报告
    file_count = _count_files(target)
    logger.success(f"已初始化 {file_count} 个文件")
    logger.info(f"  规则目录: {target / 'rules'}")
    logger.info(f"  技能目录: {target / 'skills'}")
    logger.info(f"  需求目录: {specs}")
    logger.info("  现在可以开始使用: aegis start \"需求标题\"")


def _copy_dir(data_root, rel_src: str, dst: Path) -> None:
    """递归复制 data 子目录到目标路径。"""
    src = data_root / rel_src
    if not src.exists():
        logger.warning(f"内置数据缺少: {rel_src}")
        return

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        if item.name == "__pycache__":
            continue
        target_item = dst / item.name
        if item.is_dir():
            _copy_dir(src, item.name, target_item)
        elif item.is_file() and item.suffix == ".md":
            # 跳过已存在的文件
            if not target_item.exists():
                shutil.copy2(item, target_item)


def _count_files(root: Path) -> int:
    return sum(1 for _ in root.rglob("*") if _.is_file())
