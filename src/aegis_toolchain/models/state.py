"""Aegis Toolchain 数据模型 — Pydantic v2 schemas"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class RequirementLevel(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class RequirementPhase(str, Enum):
    BRAINSTORM = "brainstorm"
    PROPOSAL = "proposal"
    DESIGN = "design"
    SPEC = "spec"
    REVIEW = "review"
    IMPLEMENTING = "implementing"
    DONE = "done"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class BoundaryChecks(BaseModel):
    """各阶段 BOUNDARY CHECK 的记录"""
    index_registered: bool = False
    design_created: bool = False
    user_approved: bool = False
    code_compiles: bool = False
    devlog_written: bool = False


class Requirement(BaseModel):
    """单个需求条目"""
    id: str = Field(..., pattern=r"^REQ-\d{3}$")
    title: str = Field(..., min_length=1, max_length=100)
    level: RequirementLevel
    phase: RequirementPhase = RequirementPhase.IMPLEMENTING
    created: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    description: str = ""
    files_changed: list[str] = Field(default_factory=list)
    boundary_checks: BoundaryChecks = Field(default_factory=BoundaryChecks)

    @field_validator("phase")
    @classmethod
    def validate_level_phase_match(cls, v, info):
        """L1 不应有 brainstorm/proposal/design/spec/review 阶段"""
        level = info.data.get("level")
        if level == RequirementLevel.L1 and v in (
            RequirementPhase.BRAINSTORM,
            RequirementPhase.PROPOSAL,
            RequirementPhase.DESIGN,
            RequirementPhase.SPEC,
            RequirementPhase.REVIEW,
        ):
            raise ValueError(f"L1 需求不应处于 {v.value} 阶段，L1 只有 implementing 和 done")
        return v


class AegisState(BaseModel):
    """state.json 顶层 schema"""
    version: str = "1.0.0"
    active_requirements: list[Requirement] = Field(default_factory=list)
    completed_requirements: list[Requirement] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)

    def get_active_count(self) -> int:
        return len(self.active_requirements)

    def get_next_id(self) -> str:
        """生成下一个需求 ID"""
        all_ids = [r.id for r in self.active_requirements + self.completed_requirements]
        if not all_ids:
            return "REQ-001"
        max_num = max(int(rid.split("-")[1]) for rid in all_ids)
        return f"REQ-{max_num + 1:03d}"

    def find_implementing(self) -> Optional[Requirement]:
        """查找当前 implementing 的需求"""
        for r in self.active_requirements:
            if r.phase == RequirementPhase.IMPLEMENTING:
                return r
        return None
