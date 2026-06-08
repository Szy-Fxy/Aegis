"""aegis status — 查看项目当前状态"""

import json
from pathlib import Path

import typer

from aegis_toolchain.core.state_manager import StateManager, StateCorruptedError


def cmd_status(
    requirement_id: str = typer.Argument(None, help="需求 ID，默认显示全部"),
    json_output: bool = typer.Option(False, "--json", "-j", help="JSON 格式输出"),
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
) -> None:
    """查看项目当前状态"""

    manager = StateManager(project)
    try:
        state = manager.load()
    except StateCorruptedError as e:
        typer.secho(f"❌ 状态文件异常: {e.detail}", fg="red")
        typer.secho("   建议: 检查 Aegis/state/state.json 或删除后重新运行 aegis start", fg="yellow")
        raise typer.Exit(1)

    if json_output:
        typer.echo(state.model_dump_json(indent=2, ensure_ascii=False))
        return

    if requirement_id is not None:
        req = manager.get_requirement(requirement_id)
        if req is None:
            typer.secho(f"❌ 未找到需求: {requirement_id}", fg="red")
            raise typer.Exit(1)
        _print_requirement_detail(req)
        return

    if not state.active_requirements and not state.completed_requirements:
        typer.secho("ℹ️  暂无需求记录", fg="blue")
        typer.secho("   运行 'aegis start \"<标题>\"' 开始第一个需求", fg="blue")
        return

    if state.active_requirements:
        typer.secho("\n活跃需求:", fg="cyan", bold=True)
        typer.secho(f"{'─'*70}", fg="cyan")
        for req in state.active_requirements:
            _print_requirement_row(req)

    if state.completed_requirements:
        typer.secho(f"\n已完成 ({len(state.completed_requirements)}):", fg="green", bold=True)
        typer.secho(f"{'─'*70}", fg="green")
        for req in state.completed_requirements[-5:]:
            _print_requirement_row(req)

    typer.secho(f"\n总计: {state.get_active_count()} 活跃, {len(state.completed_requirements)} 已完成", fg="cyan")


def _print_requirement_row(req) -> None:
    typer.secho(
        f"  {req.id}  {req.title:<30}  [{req.level.value}]  {req.phase.display}",
        fg="white",
    )


def _print_requirement_detail(req) -> None:
    typer.secho(f"\n{'='*50}", fg="cyan")
    typer.secho(f"  {req.id} — {req.title}", fg="cyan", bold=True)
    typer.secho(f"{'='*50}\n", fg="cyan")

    typer.secho(f"  等级:     {req.level.value}")
    typer.secho(f"  阶段:     {req.phase.display}")
    typer.secho(f"  创建:     {req.created.strftime('%Y-%m-%d %H:%M')}")
    typer.secho(f"  最后活动: {req.last_activity.strftime('%Y-%m-%d %H:%M')}")

    if req.description:
        typer.secho(f"  描述:     {req.description}")

    if req.files_changed:
        typer.secho(f"  变更文件: {', '.join(req.files_changed)}")

    bc = req.boundary_checks
    typer.secho(f"\n  BOUNDARY CHECK:", fg="yellow")
    checks = [
        ("DevLog 已写入", bc.devlog_written),
    ]
    for name, passed in checks:
        icon = "✅" if passed else "⬜"
        typer.secho(f"    {icon} {name}")
