"""aegis CLI 主入口"""

import typer

from aegis_toolchain.utils.logging import setup_logging

app = typer.Typer(
    name="aegis",
    help="Aegis 开发治理工具链 v5.1.0 — 让流程约束从 AI 自律转向工具强制",
    no_args_is_help=True,
)


@app.callback()
def main(verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出")):
    """Aegis Toolchain v0.1.0"""
    setup_logging(verbose=verbose)


# ── 单命令：直接注册 ──────────────────────
from aegis_toolchain.cli.start import cmd_start
from aegis_toolchain.cli.check import cmd_check
from aegis_toolchain.cli.advance import cmd_advance
from aegis_toolchain.cli.status import cmd_status
from aegis_toolchain.cli.preprocess_cmd import cmd_preprocess
from aegis_toolchain.cli.init_cmd import init_project

app.command(name="start", help="开始一个新需求")(cmd_start)
app.command(name="check", help="执行 BOUNDARY CHECK")(cmd_check)
app.command(name="advance", help="推进到下一阶段")(cmd_advance)
app.command(name="status", help="查看项目状态")(cmd_status)
app.command(name="preprocess", help="消息预处理器")(cmd_preprocess)
app.command(name="init", help="初始化项目 Aegis 规则文件")(init_project)

# ── 多命令组：add_typer ──────────────────
from aegis_toolchain.cli.devlog import app as devlog_app

app.add_typer(devlog_app, name="devlog", help="DevLog 操作")
