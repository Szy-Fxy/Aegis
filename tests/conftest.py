"""Pytest shared fixtures for aegis-toolchain tests."""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from aegis_toolchain.models.state import (
    AegisState,
    BoundaryChecks,
    Requirement,
    RequirementLevel,
    RequirementPhase,
)
from aegis_toolchain.core.state_manager import StateManager
from aegis_toolchain.core.index_manager import IndexManager
from helpers import make_req, make_state


@pytest.fixture
def temp_project():
    """临时空项目目录"""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


@pytest.fixture
def clean_project(temp_project):
    """带 Aegis 目录结构的临时项目"""
    aegis_dir = temp_project / "Aegis" / "state"
    aegis_dir.mkdir(parents=True, exist_ok=True)
    specs_dir = temp_project / "Aegis_Specs"
    specs_dir.mkdir(exist_ok=True)
    # 写默认 INDEX.md（6列格式: id | title | level | status | start | last）
    index = specs_dir / "INDEX.md"
    index.write_text(
        "# Aegis Spec Index\n\n"
        "| ID | Title | Level | Status | Start | Last Updated |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| REQ-001 | 测试需求 | L1 | 🔨 implementing | 2026-06-01 | 2026-06-07 |\n",
        encoding="utf-8",
    )
    # DevLogs 目录
    (temp_project / "Aegis" / "rules" / "DevLogs").mkdir(parents=True, exist_ok=True)
    return temp_project


@pytest.fixture
def state_manager(clean_project):
    """预创建的 StateManager"""
    return StateManager(clean_project)


@pytest.fixture
def index_manager(clean_project):
    """预创建的 IndexManager"""
    return IndexManager(clean_project)


@pytest.fixture
def sample_requirement():
    """示例 L1 需求"""
    return Requirement(
        id="REQ-001",
        title="测试需求",
        level=RequirementLevel.L1,
        phase=RequirementPhase.IMPLEMENTING,
    )


@pytest.fixture
def sample_state(sample_requirement):
    """含一个 active 需求的 AegisState"""
    return AegisState(active_requirements=[sample_requirement])
