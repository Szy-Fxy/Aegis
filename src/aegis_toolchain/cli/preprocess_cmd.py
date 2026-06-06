"""aegis preprocess — 消息预处理器"""

from pathlib import Path

import typer

from aegis_toolchain.core.state_manager import StateManager
from aegis_toolchain.core.rule_loader import RuleLoader
from aegis_toolchain.preprocessor.classifier import classify
from aegis_toolchain.preprocessor.injector import build_system_prompt


def cmd_preprocess(
    user_message: str = typer.Argument(..., help="用户原始消息"),
    project: Path = typer.Option(Path("."), "--project", "-p", help="项目路径"),
) -> None:
    """预处理用户消息，输出增强后的 system prompt"""
    classification = classify(user_message)
    typer.secho(f"分类: {classification.level} (置信度 {classification.confidence:.0%})", fg="cyan")
    typer.secho(f"理由: {classification.reason}\n", fg="cyan")

    loader = RuleLoader(project)
    rules = loader.load_all()
    if not rules:
        typer.secho("⚠️ 未找到 Aegis 规则文件", fg="yellow")

    state = None
    try:
        state = StateManager(project).load()
    except Exception as e:
        from loguru import logger
        logger.debug(f"preprocess: 无法加载项目状态 ({e})")
        typer.secho(f"⚠️ 无法加载项目状态（非致命）", fg="yellow")

    prompt = build_system_prompt(classification, rules, state)
    typer.secho("=" * 60, fg="cyan")
    typer.echo(prompt)
    typer.secho("=" * 60, fg="cyan")
