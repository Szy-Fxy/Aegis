"""pytest 共享 fixtures"""
import json
import tempfile
from pathlib import Path

import pytest

from aegis_toolchain.models.state import AegisState, Requirement, RequirementLevel, RequirementPhase


@pytest.fixture
def temp_project():
    """创建临时 Aegis 项目目录"""
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        # 创建 Aegis 目录结构
        (project / "Aegis" / "state").mkdir(parents=True)
        (project / "Aegis" / "rules" / "DevLogs").mkdir(parents=True)
        (project / "Aegis_Specs").mkdir(parents=True)
        yield project


@pytest.fixture
def sample_state():
    """返回一个示例 AegisState"""
    return AegisState(
        active_requirements=[
            Requirement(
                id="REQ-001",
                title="测试需求",
                level=RequirementLevel.L2,
                phase=RequirementPhase.DESIGN,
            )
        ]
    )


@pytest.fixture
def empty_state():
    """返回空 AegisState"""
    return AegisState()
