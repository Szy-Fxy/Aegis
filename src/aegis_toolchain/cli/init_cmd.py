"""aegis init — 初始化项目 Aegis 规则文件"""

import shutil
from pathlib import Path

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # Python < 3.11 fallback

import typer


def init_project(
    force: bool = typer.Option(False, "--force", "-f", help="覆盖已有 Aegis/ 目录"),
) -> None:
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
            typer.secho("⚠️  Aegis/ 已存在且非空。使用 --force 覆盖", fg="yellow")
            raise typer.Exit(0)

    try:
        data_root = files("aegis_toolchain.data")
    except Exception as e:
        typer.secho(f"❌ 无法找到内置规则数据: {e}", fg="red")
        raise typer.Exit(1)

    # 复制 rules（含 TempData、DevLogs、TechStack、global.md）
    if force:
        shutil.rmtree(target / "rules", ignore_errors=True)
    _copy_dir(data_root, "rules", target / "rules")

    # 复制 skills（含 dev-workflow、aegis-boot）
    if force:
        shutil.rmtree(target / "skills", ignore_errors=True)
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

    # 创建 DevLogs 目录（带 .gitignore 防止开发日志意外提交到公开仓库）
    devlog_dir = target / "rules" / "DevLogs"
    devlog_dir.mkdir(parents=True, exist_ok=True)
    (devlog_dir / ".gitignore").write_text(
        "# DevLog 是开发过程中的详细记录，默认不入版本库\n"
        "*.md\n"
        "!.gitignore\n",
        encoding="utf-8",
    )

    # 复制 AGENTS.md 到项目根目录（引导非 Hana AI 工具发现 Aegis 规则）
    agents_status = None  # None=未知, "created"=新建, "skipped"=跳过, "overwritten"=覆盖
    agents_src = data_root / "AGENTS.md"
    agents_dst = cwd / "AGENTS.md"
    if agents_src.exists() and agents_src.is_file():
        if agents_dst.exists() and not force:
            typer.secho("⚠️  AGENTS.md 已存在，跳过", fg="yellow")
            agents_status = "skipped"
        else:
            existed_before = agents_dst.exists()
            if existed_before and force:
                typer.secho("⚠️  AGENTS.md 将被覆盖", fg="yellow")
            content = agents_src.read_text(encoding="utf-8")
            agents_dst.write_text(content, encoding="utf-8")
            agents_status = "overwritten" if existed_before else "created"
    else:
        typer.secho("⚠️  内置 AGENTS.md 模板缺失", fg="yellow")

    # 报告
    file_count = _count_files(target)
    if agents_status in ("created", "overwritten"):
        file_count += 1  # AGENTS.md 在 Aegis/ 目录外，单独计数
    typer.secho(f"\n[OK] Aegis 初始化完成 ({file_count} 个文件)", fg="green", bold=True)
    typer.secho(f"\n  >> 项目已配置:", fg="blue")
    typer.secho(f"     开发流程规则     Aegis/rules/", fg="blue")
    typer.secho(f"     AI 协作规范      Aegis/skills/", fg="blue")
    if agents_status == "skipped":
        typer.secho(f"     协作入口文件      AGENTS.md (已存在，跳过)", fg="blue")
    elif agents_status in ("created", "overwritten"):
        typer.secho(f"     协作入口文件      AGENTS.md", fg="blue")
    typer.secho(f"     需求追踪          Aegis_Specs/", fg="blue")
    typer.secho(f"\n  >> 下一步:", fg="blue")
    typer.secho(f"     aegis start \"需求标题\" -l L2", fg="blue")
    typer.secho(f"\n  >> 使用指南: https://github.com/Szy-Fxy/Aegis/blob/main/USAGE.md", fg="blue")


def _copy_dir(data_root, rel_src: str, dst: Path) -> None:
    """递归复制 data 子目录到目标路径。"""
    src = data_root / rel_src
    if not src.exists():
        typer.secho(f"⚠️  内置数据缺少: {rel_src}", fg="yellow")
        return

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        if item.name == "__pycache__":
            continue
        target_item = dst / item.name
        if item.is_dir():
            _copy_dir(src, item.name, target_item)
        elif item.is_file() and item.suffix == ".md":
            if not target_item.exists():
                shutil.copy2(item, target_item)


def _count_files(root: Path) -> int:
    return sum(1 for _ in root.rglob("*") if _.is_file())
