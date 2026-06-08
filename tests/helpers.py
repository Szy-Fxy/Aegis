"""测试辅助函数：快速构造 Requirement 和 AegisState"""

from datetime import datetime

from aegis_toolchain.models.state import (
    AegisState,
    Requirement,
    RequirementLevel,
    RequirementPhase,
)


def make_req(title="测试需求", level=RequirementLevel.L1, phase=RequirementPhase.IMPLEMENTING, req_id="REQ-001"):
    """快捷构造 Requirement"""
    return Requirement(
        id=req_id,
        title=title,
        level=level,
        phase=phase,
        description=f"{title}的描述",
    )


def make_state(*reqs):
    """快捷构造 AegisState"""
    return AegisState(active_requirements=list(reqs))
