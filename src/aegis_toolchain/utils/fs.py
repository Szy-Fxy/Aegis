"""文件系统辅助函数"""

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    """确保目录存在，不存在则创建"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_path(base: Path, relative: str) -> Path:
    """安全路径拼接，拒绝 ../ 穿越"""
    resolved = (base / relative).resolve()
    base_resolved = base.resolve()
    if not str(resolved).startswith(str(base_resolved)):
        raise ValueError(f"路径穿越拒绝: {relative}")
    return resolved


def atomic_write(path: Path, content: str) -> None:
    """原子写入：先写临时文件，再 rename"""
    tmp = path.with_suffix(path.suffix + ".tmp")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
