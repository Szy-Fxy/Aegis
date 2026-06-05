"""日志配置 — 基于 loguru"""

from loguru import logger
import sys


def setup_logging(verbose: bool = False) -> None:
    """配置 loguru，移除默认 handler，添加自定义格式"""
    logger.remove()
    level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=level,
        colorize=True,
    )


__all__ = ["logger", "setup_logging"]
