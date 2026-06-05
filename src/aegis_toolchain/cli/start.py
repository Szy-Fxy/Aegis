"""aegis start — 开始一个新需求"""

from pathlib import Path

import typer
from loguru import logger

from aegis_toolchain.core.state_manager import StateManager
from aegis_toolchain.core.index_manager import IndexManager
from aegis_toolchain.models.state import Requirement, RequirementLevel, RequirementPhase
from aegis_toolchain.preprocessor.classifier import classify


def cmd_start(
    title: str = typer.Argument(..., help="需求名称"),
    level: str = typer.Option("auto", "--level", "-l", help="需求等级: L1 / L2 / L3 / auto"),
    description: str = typer.Option("", "--desc", "-d", help="需求描述"),
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
) -> None:
    """开始一个新需求，自动分类并登记到 INDEX.md 和 state.json"""

    # 1. 自动分类
    if level == "auto":
        result = classify(title + " " + description)
        level = result.level
        typer.secho(f"🔍 自动分类: {level} (置信度 {result.confidence:.0%})", fg="cyan")
        typer.secho(f"   理由: {result.reason}", fg="cyan")
        if result.is_uncertain:
            typer.secho(f"   ⚠️ 置信度较低，如需修改请指定 --level", fg="yellow")

    # 2. 校验 level
    level_upper = level.upper()
    if level_upper not in ("L1", "L2", "L3"):
        typer.secho(f"❌ 无效等级: {level}。请使用 L1 / L2 / L3 / auto", fg="red")
        raise typer.Exit(1)

    req_level = RequirementLevel(level_upper)

    # 3. 分配 ID 并创建需求
    try:
        manager = StateManager(project)
        next_id = manager.get_next_id()
    except Exception as e:
        typer.secho(f"❌ 状态文件异常: {e}", fg="red")
        raise typer.Exit(1)

    req = Requirement(
        id=next_id,
        title=title,
        level=req_level,
        description=description,
    )

    # 4. 注册到 state.json
    try:
        manager = StateManager(project)
        req = manager.add_requirement(req)
    except RuntimeError as e:
        typer.secho(f"❌ {e}", fg="red")
        raise typer.Exit(1)
    except Exception as e:
        typer.secho(f"❌ 状态文件异常: {e}", fg="red")
        raise typer.Exit(1)

    # 5. 更新 INDEX.md
    phase_display = _phase_display(req.phase)
    try:
        index = IndexManager(project)
        index.add_entry(req.id, req.title, req_level.value, phase_display)
    except Exception as e:
        logger.warning(f"INDEX.md 更新失败: {e}")
        typer.secho(f"⚠️ INDEX.md 更新失败（state.json 已保存）: {e}", fg="yellow")

    # 6. 输出结果
    typer.secho(f"\n✅ 已登记 {req.id} [{req.level.value}] {req.title}", fg="green", bold=True)
    typer.secho(f"   阶段: {phase_display}", fg="green")
    typer.secho(f"   下一步: aegis check", fg="blue")


def _phase_display(phase: RequirementPhase) -> str:
    display = {
        RequirementPhase.BRAINSTORM: "📋 brainstorm",
        RequirementPhase.PROPOSAL: "📋 proposal",
        RequirementPhase.DESIGN: "📐 design",
        RequirementPhase.SPEC: "📝 spec",
        RequirementPhase.REVIEW: "📋 review",
        RequirementPhase.IMPLEMENTING: "🔨 implementing",
        RequirementPhase.DONE: "✅ done",
    }
    return display.get(phase, phase.value)
