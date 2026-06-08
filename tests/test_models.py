"""Tests for models/state.py — Requirement, AegisState, BoundaryChecks, enums"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from aegis_toolchain.models.state import (
    AegisState,
    BoundaryChecks,
    Requirement,
    RequirementLevel,
    RequirementPhase,
    PHASE_DISPLAY_MAP,
)


class TestRequirementLevel:
    def test_level_values(self):
        assert RequirementLevel.L1.value == "L1"
        assert RequirementLevel.L2.value == "L2"
        assert RequirementLevel.L3.value == "L3"

    def test_string_coercion(self):
        assert RequirementLevel("L1") == RequirementLevel.L1
        assert RequirementLevel("L2") == RequirementLevel.L2

    def test_invalid_level(self):
        with pytest.raises(ValueError):
            RequirementLevel("L4")


class TestRequirementPhase:
    def test_phase_values(self):
        assert RequirementPhase.IMPLEMENTING.value == "implementing"
        assert RequirementPhase.DONE.value == "done"
        assert RequirementPhase.DESIGN.value == "design"
        assert RequirementPhase.BRAINSTORM.value == "brainstorm"
        assert RequirementPhase.PAUSED.value == "paused"
        assert RequirementPhase.CANCELLED.value == "cancelled"

    def test_display_property(self):
        assert "🔨 implementing" in RequirementPhase.IMPLEMENTING.display
        assert "✅ done" in RequirementPhase.DONE.display
        assert "📐 design" in RequirementPhase.DESIGN.display
        assert "⏸️ paused" in RequirementPhase.PAUSED.display
        assert "❌ cancelled" in RequirementPhase.CANCELLED.display

    def test_all_phases_have_display(self):
        """每个枚举值都有 display"""
        for p in RequirementPhase:
            assert len(p.display) > 0

    def test_phase_display_map(self):
        assert PHASE_DISPLAY_MAP[RequirementPhase.IMPLEMENTING] == RequirementPhase.IMPLEMENTING.display
        assert PHASE_DISPLAY_MAP[RequirementPhase.DONE] == RequirementPhase.DONE.display


class TestBoundaryChecks:
    def test_default_false(self):
        bc = BoundaryChecks()
        assert bc.devlog_written is False

    def test_set_fields(self):
        bc = BoundaryChecks(devlog_written=True)
        assert bc.devlog_written is True

    def test_serialization(self):
        bc = BoundaryChecks(devlog_written=True)
        data = bc.model_dump()
        assert data == {"devlog_written": True}


class TestRequirement:
    def test_minimal_construction(self):
        """最小字段构造"""
        req = Requirement(id="REQ-001", title="测试", level=RequirementLevel.L1)
        assert req.id == "REQ-001"
        assert req.title == "测试"
        assert req.level == RequirementLevel.L1
        assert req.phase == RequirementPhase.IMPLEMENTING

    def test_full_construction(self):
        """所有字段都指定"""
        req = Requirement(
            id="REQ-042",
            title="完整构造测试",
            level=RequirementLevel.L3,
            phase=RequirementPhase.DESIGN,
            description="这是一个测试需求",
            files_changed=["file1.py", "file2.ts"],
            boundary_checks=BoundaryChecks(devlog_written=True),
        )
        assert req.id == "REQ-042"
        assert req.title == "完整构造测试"
        assert req.level == RequirementLevel.L3
        assert req.phase == RequirementPhase.DESIGN
        assert req.description == "这是一个测试需求"
        assert req.files_changed == ["file1.py", "file2.ts"]
        assert req.boundary_checks.devlog_written is True

    def test_id_pattern(self):
        """ID 必须匹配 REQ-NNN"""
        with pytest.raises(ValidationError):
            Requirement(id="invalid", title="x", level=RequirementLevel.L1)

    def test_title_min_length(self):
        with pytest.raises(ValidationError):
            Requirement(id="REQ-001", title="", level=RequirementLevel.L1)

    def test_title_too_long(self):
        with pytest.raises(ValidationError):
            Requirement(id="REQ-001", title="x" * 101, level=RequirementLevel.L1)

    def test_l1_phase_restriction(self):
        """L1 只能 implementing 或 done"""
        req = Requirement(id="REQ-001", title="L1 test", level=RequirementLevel.L1, phase=RequirementPhase.DONE)
        assert req.phase == RequirementPhase.DONE

        with pytest.raises(ValidationError):
            Requirement(id="REQ-002", title="L1 design", level=RequirementLevel.L1, phase=RequirementPhase.DESIGN)

    def test_l2_allowed_phases(self):
        """L2 可以处于任意合法阶段"""
        req = Requirement(id="REQ-001", title="L2 design", level=RequirementLevel.L2, phase=RequirementPhase.DESIGN)
        assert req.phase == RequirementPhase.DESIGN
        assert req.level == RequirementLevel.L2

    def test_serialization(self):
        req = Requirement(
            id="REQ-005",
            title="序列化测试",
            level=RequirementLevel.L2,
            phase=RequirementPhase.DESIGN,
            description="测试描述",
            files_changed=["a.py", "b.py"],
        )
        data = req.model_dump()
        assert data["id"] == "REQ-005"
        assert data["title"] == "序列化测试"
        assert data["level"] == "L2"
        assert data["phase"] == "design"
        assert data["description"] == "测试描述"
        assert data["files_changed"] == ["a.py", "b.py"]
        assert data["boundary_checks"]["devlog_written"] is False
        assert "created" in data
        assert "last_activity" in data

    def test_default_fields(self):
        req = Requirement(id="REQ-001", title="默认值测试", level=RequirementLevel.L1)
        assert req.description == ""
        assert req.files_changed == []
        assert isinstance(req.created, datetime)
        assert isinstance(req.boundary_checks, BoundaryChecks)


class TestAegisState:
    def test_empty_state(self):
        state = AegisState()
        assert state.active_requirements == []
        assert state.completed_requirements == []
        assert state.version == "1.0.0"
        assert state.get_active_count() == 0

    def test_get_next_id_empty(self):
        state = AegisState()
        assert state.get_next_id() == "REQ-001"

    def test_get_next_id_multiple(self):
        r1 = Requirement(id="REQ-001", title="A", level=RequirementLevel.L1)
        r2 = Requirement(id="REQ-003", title="B", level=RequirementLevel.L1)
        r3 = Requirement(id="REQ-005", title="C", level=RequirementLevel.L1)
        state = AegisState(active_requirements=[r1], completed_requirements=[r2, r3])
        assert state.get_next_id() == "REQ-006"

    def test_get_next_id_with_gaps(self):
        r1 = Requirement(id="REQ-001", title="A", level=RequirementLevel.L1)
        r2 = Requirement(id="REQ-002", title="B", level=RequirementLevel.L1)
        state = AegisState(completed_requirements=[r1, r2])
        assert state.get_next_id() == "REQ-003"

    def test_find_implementing(self):
        """查找正在 implementing 的需求"""
        r1 = Requirement(id="REQ-002", title="implementing中用", level=RequirementLevel.L2,
                         phase=RequirementPhase.IMPLEMENTING)
        r2 = Requirement(id="REQ-001", title="设计中", level=RequirementLevel.L2,
                         phase=RequirementPhase.DESIGN)
        state = AegisState(active_requirements=[r2, r1])
        found = state.find_implementing()
        assert found is not None
        assert found.id == "REQ-002"

    def test_find_implementing_none(self):
        state = AegisState()
        assert state.find_implementing() is None

    def test_find_implementing_all_done(self):
        r1 = Requirement(id="REQ-001", title="done了", level=RequirementLevel.L1,
                         phase=RequirementPhase.DONE)
        state = AegisState(active_requirements=[r1])
        assert state.find_implementing() is None

    def test_serialization_roundtrip(self):
        state = AegisState(
            active_requirements=[
                Requirement(id="REQ-001", title="测试", level=RequirementLevel.L1)
            ],
            completed_requirements=[
                Requirement(id="REQ-000", title="古老",
                            level=RequirementLevel.L1, phase=RequirementPhase.DONE)
            ],
        )
        data = state.model_dump()
        restored = AegisState.model_validate(data)
        assert restored.get_active_count() == 1
        assert len(restored.completed_requirements) == 1
        assert restored.active_requirements[0].id == "REQ-001"
        assert restored.completed_requirements[0].id == "REQ-000"
