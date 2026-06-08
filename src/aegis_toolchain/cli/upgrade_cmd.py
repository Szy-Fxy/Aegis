"""python -m aegis_toolchain upgrade — 升级后同步项目规则文件，保留用户数据"""

import hashlib
import shutil
from datetime import datetime
from pathlib import Path

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

import typer

# 升级时跳过的用户数据目录
SKIP_DIRS = {"DevLogs", "TempData"}
# 保留的最近备份数
MAX_BACKUPS = 5


def _file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def _cleanup_old_backups(backup_root: Path) -> None:
    if not backup_root.exists():
        return
    dirs = sorted(
        [d for d in backup_root.iterdir() if d.is_dir()],
        key=lambda d: d.name, reverse=True,
    )
    for old in dirs[MAX_BACKUPS:]:
        shutil.rmtree(old, ignore_errors=True)


def cmd_upgrade(
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="预览变更，不实际执行"),
) -> None:
    """升级项目中的 Aegis 规则文件，保留用户数据。"""
    cwd = project.resolve()
    target = cwd / "Aegis"
    if not target.exists():
        typer.secho("❌ 项目尚未初始化。请先运行 python -m aegis_toolchain init", fg="red")
        raise typer.Exit(1)

    try:
        data_root = files("aegis_toolchain.data")
    except Exception as e:
        typer.secho(f"❌ 无法找到内置规则数据: {e}", fg="red")
        raise typer.Exit(1)

    # 收集变更
    new_files, user_changed_files, skipped_ts = _collect(data_root, target)
    has_work = bool(new_files or user_changed_files)

    if not has_work:
        if skipped_ts > 0:
            typer.secho(f"\n[OK] Aegis 已是最新版本，无需升级", fg="green", bold=True)
            typer.secho(f"\n  保留 {skipped_ts} 个 TechStack 文件（用户定制）", fg="blue")
        else:
            typer.secho(f"\n[OK] Aegis 已是最新版本，无需升级", fg="green", bold=True)
        return

    if dry_run:
        typer.secho(f"\n[DRY-RUN] Aegis 升级预览", fg="cyan", bold=True)
    else:
        typer.secho(f"\n[OK] Aegis 升级完成", fg="green", bold=True)

    if new_files:
        typer.secho(f"\n  新增 {len(new_files)} 个文件:", fg="blue")
        for f in new_files:
            typer.secho(f"     + {f}", fg="blue")

    if user_changed_files:
        typer.secho(f"\n  ⚠  以下文件内容不同，旧版已备份:", fg="yellow")
        for f in user_changed_files:
            typer.secho(f"     {f}", fg="yellow")

    if skipped_ts > 0:
        typer.secho(f"\n  保留 {skipped_ts} 个 TechStack 文件（用户定制）", fg="blue")

    if dry_run:
        typer.secho(f"\n  预览完成，运行 python -m aegis_toolchain upgrade 确认执行", fg="cyan")
        return

    # 确认
    try:
        typer.confirm("\n  确认执行升级？", default=True, abort=True)
    except typer.Abort:
        typer.secho("已取消", fg="yellow")
        raise typer.Exit(0)

    # 执行
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = target / ".backup" / now
    had_backup = _execute(data_root, target, backup_dir, new_files, user_changed_files)
    if had_backup:
        _cleanup_old_backups(target / ".backup")
        _ensure_backup_in_gitignore(target)

    typer.secho(f"\n  保留未动:", fg="blue")
    typer.secho(f"     DevLogs / state / TempData / Aegis_Specs / INDEX.md / AGENTS.md", fg="blue")


def _walk_src(data_root: str) -> list[tuple[str, Path, bool]]:
    """遍历 data/，返回 (rel_path, src_path, is_techstack) 列表。"""
    items = []
    def _recurse(rel: str):
        src = data_root / rel
        if not src.exists():
            return
        for item in src.iterdir():
            if item.name == "__pycache__":
                continue
            child_rel = f"{rel}/{item.name}"
            if item.is_dir():
                if item.name in SKIP_DIRS:
                    continue
                _recurse(child_rel)
            elif item.suffix == ".md":
                items.append((child_rel, item, rel.startswith("rules/TechStack")))
    _recurse("rules")
    _recurse("skills")
    return items


def _collect(data_root: Path, target: Path) -> tuple[list, list, int]:
    """遍历对比，返回 (new, user_changed, skipped_ts)。"""
    new_files, user_changed_files = [], []
    skipped_ts = 0

    for rel, src_path, is_ts in _walk_src(data_root):
        target_file = target / rel
        if not target_file.exists():
            new_files.append(rel)
        elif is_ts:
            skipped_ts += 1
        elif _file_hash(src_path) != _file_hash(target_file):
            user_changed_files.append(rel)
        # else: 内容相同，静默跳过

    return new_files, user_changed_files, skipped_ts


def _execute(data_root: Path, target: Path, backup_dir: Path,
             new_files: list, user_changed_files: list) -> bool:
    """执行文件操作。返回是否产生了备份。"""
    had_backup = False
    for rel, src_path, _ in _walk_src(data_root):
        target_file = target / rel
        target_file.parent.mkdir(parents=True, exist_ok=True)

        if rel in new_files:
            shutil.copy2(src_path, target_file)
        elif rel in user_changed_files:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_file, backup_dir / rel.replace("/", "_").replace("\\", "_"))
            shutil.copy2(src_path, target_file)
            had_backup = True
        # else: TechStack → skip

    return had_backup


def _ensure_backup_in_gitignore(target: Path) -> None:
    """确保 .backup/ 在 Aegis/.gitignore 中，防止备份文件被意外提交。"""
    gitignore = target / ".gitignore"
    entry = ".backup/"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if entry not in content:
            gitignore.write_text(content.rstrip() + f"\n{entry}\n", encoding="utf-8")
    else:
        gitignore.write_text(f"{entry}\n", encoding="utf-8")
