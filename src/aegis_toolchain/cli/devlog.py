"""aegis devlog — DevLog 的生成、写入和查看"""

import os
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import typer
from loguru import logger

from aegis_toolchain.core.state_manager import StateManager, StateCorruptedError
from aegis_toolchain.utils.fs import ensure_dir

app = typer.Typer(help="DevLog 操作", no_args_is_help=True)

DEVLOG_TEMPLATE = """# DevLog: {title} ({req_id})

> 日期: {date}
> 需求: {req_id} — {title}
> 等级: {level}
> 阶段: {phase}

## 改动摘要
{message}

## 当前进度
{phase}

## 下一动作
{next_action}

## 步骤状态
- [ ] / [x] 根据实际情况填写
"""


@app.command()
def write(
    requirement_id: str = typer.Argument(..., help="需求 ID"),
    message: str = typer.Option("", "--message", "-m", help="DevLog 内容"),
    editor: bool = typer.Option(False, "--editor", "-e", help="打开编辑器编写"),
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
) -> None:
    """写入 DevLog 条目"""
    manager = StateManager(project)
    try:
        state = manager.load()
    except StateCorruptedError as e:
        typer.secho(f"❌ 状态文件异常: {e.detail}", fg="red")
        typer.secho("   建议: 检查 Aegis/state/state.json 或删除后重新运行 python -m aegis_toolchain start", fg="yellow")
        raise typer.Exit(1)

    req = manager.get_requirement(requirement_id)
    if req is None:
        typer.secho(f"❌ 未找到需求: {requirement_id}", fg="red")
        raise typer.Exit(1)

    # 编辑器模式
    if editor or not message:
        message = _open_editor(req, message)

    if not message.strip():
        typer.secho("❌ DevLog 内容为空，已取消", fg="red")
        raise typer.Exit(1)

    # 生成 DevLog 文件
    devlog_dir = project / "Aegis" / "rules" / "DevLogs"
    ensure_dir(devlog_dir)

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', req.title[:20])
    filename = f"{date_str}-{requirement_id}-{safe_title}.md"
    filepath = devlog_dir / filename

    content = DEVLOG_TEMPLATE.format(
        title=req.title,
        req_id=req.id,
        date=date_str,
        level=req.level.value,
        phase=req.phase.value,
        message=message,
        next_action="等用户确认" if req.phase.value in ("design", "spec", "review") else "继续实现",
    )

    filepath.write_text(content, encoding="utf-8")
    typer.secho(f"✅ DevLog 已写入: {filepath}", fg="green")

    # 更新 boundary_checks
    manager.update_requirement(req.id, devlog_written=True)


@app.command()
def show(
    requirement_id: str = typer.Argument(None, help="需求 ID，默认显示最近"),
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
) -> None:
    """查看 DevLog"""
    devlog_dir = project / "Aegis" / "rules" / "DevLogs"

    if not devlog_dir.exists():
        typer.secho("ℹ️  尚无 DevLog 记录", fg="blue")
        return

    files = sorted(devlog_dir.glob("*.md"), reverse=True)

    if requirement_id:
        files = [f for f in files if requirement_id in f.name]

    if not files:
        typer.secho(f"ℹ️  未找到 {'REQ-' + requirement_id if requirement_id else '任何'} DevLog", fg="blue")
        return

    # 显示最近一个
    target = files[0]
    typer.secho(f"\n{'='*60}", fg="cyan")
    typer.echo(target.read_text(encoding="utf-8"))
    typer.secho(f"{'='*60}\n", fg="cyan")


def _open_editor(req, initial_message: str) -> str:
    """打开编辑器让用户编写 DevLog"""
    editor_cmd = os.environ.get("EDITOR", os.environ.get("VISUAL", "notepad" if os.name == "nt" else "vi"))

    template = DEVLOG_TEMPLATE.format(
        title=req.title,
        req_id=req.id,
        date=datetime.now().strftime("%Y-%m-%d"),
        level=req.level.value,
        phase=req.phase.value,
        message=initial_message,
        next_action="等用户确认",
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(template)
        tmp_path = f.name

    try:
        subprocess.run([editor_cmd, tmp_path], check=False)
        return Path(tmp_path).read_text(encoding="utf-8")
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
