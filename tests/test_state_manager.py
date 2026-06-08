"""Tests for core/state_manager.py — state.json CRUD"""

import pytest

from aegis_toolchain.models.state import (
    Requirement,
    RequirementLevel,
    RequirementPhase,
)
from aegis_toolchain.core.state_manager import StateManager, StateCorruptedError
from conftest import make_req


class TestStateManagerInit:
    def test_init_creates_dir(self, temp_project):
        sm = StateManager(temp_project)
        assert sm.state_dir.exists()
        assert sm.state_path.parent.exists()

    def test_load_empty(self, temp_project):
        sm = StateManager(temp_project)
        state = sm.load()
        assert state.active_requirements == []
        assert state.completed_requirements == []

    def test_save_and_load(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("保存测试", level=RequirementLevel.L1)
        sm.add_requirement(req)

        sm2 = StateManager(temp_project)
        state2 = sm2.load()
        assert len(state2.active_requirements) == 1
        assert state2.active_requirements[0].title == "保存测试"
        assert state2.active_requirements[0].id == "REQ-001"

    def test_get_next_id_empty(self, temp_project):
        sm = StateManager(temp_project)
        assert sm.get_next_id() == "REQ-001"

    def test_get_next_id_after_add(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("A", level=RequirementLevel.L1)
        sm.add_requirement(req)
        assert sm.get_next_id() == "REQ-002"

    def test_get_active_requirement(self, temp_project):
        sm = StateManager(temp_project)
        # L1 不修改 phase，保持 IMPLEMENTING
        req = make_req("活跃", level=RequirementLevel.L1, phase=RequirementPhase.IMPLEMENTING)
        sm.add_requirement(req)
        found = sm.get_active_requirement()
        assert found is not None
        assert found.title == "活跃"

    def test_get_active_requirement_none(self, temp_project):
        sm = StateManager(temp_project)
        assert sm.get_active_requirement() is None

    def test_get_requirement_by_id(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("查找测试", level=RequirementLevel.L1)
        sm.add_requirement(req)
        found = sm.get_requirement("REQ-001")
        assert found is not None
        assert found.title == "查找测试"

    def test_get_requirement_not_found(self, temp_project):
        sm = StateManager(temp_project)
        assert sm.get_requirement("REQ-999") is None

    def test_lock_timeout_constants(self, temp_project):
        sm = StateManager(temp_project)
        assert sm.LOCK_TIMEOUT == 2


class TestStateManagerAddRequirement:
    def test_add_l1(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("L1需求", level=RequirementLevel.L1, phase=RequirementPhase.IMPLEMENTING)
        result = sm.add_requirement(req)
        assert result.id == "REQ-001"
        assert result.phase == RequirementPhase.IMPLEMENTING

    def test_add_l2_sets_design(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("L2需求", level=RequirementLevel.L2, phase=RequirementPhase.IMPLEMENTING)
        result = sm.add_requirement(req)
        assert result.id == "REQ-001"
        assert result.phase == RequirementPhase.DESIGN

    def test_add_l3_sets_brainstorm(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("L3需求", level=RequirementLevel.L3, phase=RequirementPhase.IMPLEMENTING)
        result = sm.add_requirement(req)
        assert result.id == "REQ-001"
        assert result.phase == RequirementPhase.BRAINSTORM

    def test_add_concurrent_l2_blocks_if_implementing_exists(self, temp_project):
        """已有 implementing 中的需求时，禁止加新 L2"""
        sm = StateManager(temp_project)
        # 先加一个 L1 让它处于 implementing
        r1 = make_req("实现中", level=RequirementLevel.L1)
        sm.add_requirement(r1)

        # 再加 L2 应该被阻止（因为有 L1 implementing）
        r2 = make_req("新L2", level=RequirementLevel.L2)
        with pytest.raises(RuntimeError, match="仍在 implementing"):
            sm.add_requirement(r2)

    def test_add_l1_doesnt_check_concurrent(self, temp_project):
        """L1 不受并发检查限制"""
        sm = StateManager(temp_project)
        r1 = make_req("L1-1", level=RequirementLevel.L1)
        sm.add_requirement(r1)
        r2 = make_req("L1-2", level=RequirementLevel.L1)
        result = sm.add_requirement(r2)
        assert result.id == "REQ-002"

    def test_auto_id_increment(self, temp_project):
        sm = StateManager(temp_project)
        for i in range(1, 6):
            req = make_req(f"需求{i}", level=RequirementLevel.L1)
            result = sm.add_requirement(req)
            assert result.id == f"REQ-{i:03d}"


class TestStateManagerUpdateRequirement:
    def test_update_phase(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("更新测试", level=RequirementLevel.L2)
        sm.add_requirement(req)

        sm.update_requirement("REQ-001", phase=RequirementPhase.IMPLEMENTING)
        found = sm.get_requirement("REQ-001")
        assert found.phase == RequirementPhase.IMPLEMENTING

    def test_update_blocked_by_implementing(self, temp_project):
        """不能在已有 implementing 的情况下开始新 L2"""
        sm = StateManager(temp_project)
        # L1 进入 implementing
        r1 = make_req("A", level=RequirementLevel.L1)
        sm.add_requirement(r1)

        # 添加新 L2 会被阻止
        with pytest.raises(RuntimeError):
            r2 = make_req("B", level=RequirementLevel.L2)
            sm.add_requirement(r2)

    def test_update_boundary_checks(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("检查更新", level=RequirementLevel.L2)
        sm.add_requirement(req)

        sm.update_requirement("REQ-001", boundary_checks={"devlog_written": True})
        state = sm.load()
        assert state.active_requirements[0].boundary_checks.devlog_written is True

    def test_update_nonexistent(self, temp_project):
        sm = StateManager(temp_project)
        sm.update_requirement("REQ-999", phase=RequirementPhase.DONE)
        # 不应抛异常

    def test_update_files_changed(self, temp_project):
        sm = StateManager(temp_project)
        req = make_req("文件变更", level=RequirementLevel.L1)
        sm.add_requirement(req)

        sm.update_requirement("REQ-001", files_changed=["a.py", "b.py"])
        found = sm.get_requirement("REQ-001")
        assert found.files_changed == ["a.py", "b.py"]


class TestStateManagerTransaction:
    def test_transaction_saves(self, temp_project):
        sm = StateManager(temp_project)
        with sm.transaction() as state:
            req = make_req("事务测试", level=RequirementLevel.L1)
            state.active_requirements.append(req)

        state2 = sm.load()
        assert len(state2.active_requirements) == 1
        assert state2.active_requirements[0].title == "事务测试"


class TestStateCorruptedError:
    def test_corrupted_json(self, temp_project):
        sm = StateManager(temp_project)
        sm.state_dir.mkdir(parents=True, exist_ok=True)
        sm.state_path.write_text("not valid json {{{")

        with pytest.raises(StateCorruptedError) as exc:
            sm.load()
        assert "JSON" in str(exc.value)
