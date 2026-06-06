"""aegis check — 执行 BOUNDARY CHECK"""

from pathlib import Path

import typer

from aegis_toolchain.core.state_manager import StateManager
from aegis_toolchain.core.boundary_checker import BoundaryChecker


def cmd_check(
    requirement_id: str = typer.Argument(None, help="需求 ID，默认当前活跃需求"),
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
) -> None:
    """执行当前阶段的 BOUNDARY CHECK"""

    manager = StateManager(project)
    state = manager.load()

    if requirement_id is None:
        if not state.active_requirements:
            typer.secho("❌ 没有活跃需求", fg="red")
            typer.secho("   提示: 运行 'aegis start \"<标题>\"' 开始一个需求", fg="yellow")
            raise typer.Exit(1)
        req = state.active_requirements[0]
    else:
        req = state.get_requirement(requirement_id)
        if req is None:
            typer.secho(f"❌ 未找到需求: {requirement_id}", fg="red")
            typer.secho(f"   提示: 运行 'aegis status' 查看所有已登记的需求", fg="yellow")
            raise typer.Exit(1)

    checker = BoundaryChecker(project)
    report = checker.check(req)

    typer.secho(f"\n{'='*50}", fg="cyan")
    typer.secho(f"  BOUNDARY CHECK: {req.id} [{req.level.value}] {req.phase.display}", fg="cyan")
    typer.secho(f"{'='*50}\n", fg="cyan")

    for r in report.results:
        icon = "✅" if r.passed else "✗"
        color = "green" if r.passed else "red"
        typer.secho(f"  {icon} {r.name}", fg=color, bold=True)
        typer.secho(f"     {r.detail}", fg=color)

    typer.secho(f"\n{'─'*50}", fg="cyan")
    if report.all_passed:
        typer.secho(f"  ✅ 全部通过 ({report.passed_count}/{report.total_count})", fg="green", bold=True)
        typer.secho(f"  可以继续: aegis advance", fg="blue")
    else:
        typer.secho(f"  ❌ 未通过 ({report.passed_count}/{report.total_count})", fg="red", bold=True)
        typer.secho(f"  请完成缺失项后重试", fg="yellow")
        raise typer.Exit(1)
