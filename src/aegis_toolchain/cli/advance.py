"""aegis advance — 推进需求到下一阶段"""

from pathlib import Path

import typer
from loguru import logger

from aegis_toolchain.core.state_manager import StateManager
from aegis_toolchain.core.boundary_checker import BoundaryChecker
from aegis_toolchain.core.index_manager import IndexManager
from aegis_toolchain.models.state import RequirementPhase

PHASE_NEXT_L1: dict[RequirementPhase, RequirementPhase] = {
    RequirementPhase.IMPLEMENTING: RequirementPhase.DONE,
}

PHASE_NEXT_L2: dict[RequirementPhase, RequirementPhase] = {
    RequirementPhase.DESIGN: RequirementPhase.REVIEW_DESIGN,
    RequirementPhase.REVIEW_DESIGN: RequirementPhase.IMPLEMENTING,
    RequirementPhase.IMPLEMENTING: RequirementPhase.REVIEW_CODE,
    RequirementPhase.REVIEW_CODE: RequirementPhase.VERIFY,
    RequirementPhase.VERIFY: RequirementPhase.DONE,
}

PHASE_NEXT_L3: dict[RequirementPhase, RequirementPhase] = {
    RequirementPhase.BRAINSTORM: RequirementPhase.PROPOSAL,
    RequirementPhase.PROPOSAL: RequirementPhase.DESIGN,
    RequirementPhase.DESIGN: RequirementPhase.SPEC,
    RequirementPhase.SPEC: RequirementPhase.REVIEW,
    RequirementPhase.REVIEW: RequirementPhase.IMPLEMENTING,
    RequirementPhase.IMPLEMENTING: RequirementPhase.DONE,
}

PHASE_INDEX_STATUS: dict[RequirementPhase, str] = {
    RequirementPhase.BRAINSTORM: "📋 brainstorm",
    RequirementPhase.PROPOSAL: "📋 proposal",
    RequirementPhase.DESIGN: "📐 design",
    RequirementPhase.REVIEW_DESIGN: "📋 review_design",
    RequirementPhase.SPEC: "📝 spec",
    RequirementPhase.REVIEW: "📋 review",
    RequirementPhase.IMPLEMENTING: "🔨 implementing",
    RequirementPhase.REVIEW_CODE: "📋 review_code",
    RequirementPhase.VERIFY: "✅ verify",
    RequirementPhase.DONE: "✅ done",
    RequirementPhase.PAUSED: "⏸️ paused",
    RequirementPhase.CANCELLED: "❌ cancelled",
}

PHASE_DISPLAY = {p: p.display for p in RequirementPhase}


def cmd_advance(
    requirement_id: str = typer.Argument(None, help="需求 ID，默认当前活跃需求"),
    force: bool = typer.Option(False, "--force", "-f", help="跳过 BOUNDARY CHECK 强制推进"),
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
) -> None:
    """推进需求到下一阶段"""
    manager = StateManager(project)
    state = manager.load()

    if requirement_id is None:
        if not state.active_requirements:
            typer.secho("❌ 没有活跃需求", fg="red")
            raise typer.Exit(1)
        req = state.active_requirements[0]
    else:
        req = manager.get_requirement(requirement_id)
        if req is None:
            typer.secho(f"❌ 未找到需求: {requirement_id}", fg="red")
            raise typer.Exit(1)

    if not force:
        checker = BoundaryChecker(project)
        report = checker.check(req)
        if not report.all_passed:
            typer.secho(f"❌ BOUNDARY CHECK 未通过 ({report.passed_count}/{report.total_count}):", fg="red")
            for r in report.results:
                icon = "✅" if r.passed else "✗"
                color = "green" if r.passed else "red"
                typer.secho(f"  {icon} {r.name}: {r.detail}", fg=color)
            typer.secho("\n请完成缺失项后重试，或使用 --force 强制推进", fg="yellow")
            raise typer.Exit(1)
        typer.secho(f"✅ BOUNDARY CHECK 全部通过 ({report.total_count}/{report.total_count})", fg="green")
    else:
        confirm = typer.confirm(f"⚠️  跳过 BOUNDARY CHECK 强制推进 {req.id}？")
        if not confirm:
            typer.secho("已取消", fg="yellow")
            raise typer.Exit(0)
        logger.warning(f"FORCE ADVANCE: {req.id} {req.phase.value} → (跳过检查)")
        typer.secho("⚠️  --force: 跳过 BOUNDARY CHECK，强制推进", fg="yellow")

    old_phase = req.phase
    if req.level.value == "L3":
        phase_map = PHASE_NEXT_L3
    elif req.level.value == "L2":
        phase_map = PHASE_NEXT_L2
    else:
        phase_map = PHASE_NEXT_L1
    next_phase = phase_map.get(old_phase)
    if next_phase is None:
        typer.secho(f"ℹ️  {req.id} 已处于终态 ({old_phase.value})", fg="blue")
        return

    manager.update_requirement(req.id, phase=next_phase)

    # 同步更新 INDEX.md
    status = PHASE_INDEX_STATUS.get(next_phase, next_phase.value)
    try:
        idx = IndexManager(project)
        idx.update_status(req.id, status)
    except Exception:
        pass  # INDEX.md 不存在时不阻塞
    next_display = PHASE_DISPLAY.get(next_phase, next_phase.value)
    typer.secho(f"✅ {req.id} {req.title}: {old_phase.value} → {next_display}", fg="green")

    if next_phase == RequirementPhase.DONE:
        req.phase = RequirementPhase.DONE  # 更新本地对象
        state = manager.load()
        state.active_requirements = [r for r in state.active_requirements if r.id != req.id]
        state.completed_requirements.append(req)
        manager.save(state)
        typer.secho(f"🎉 {req.id} 已完成！", fg="green")
