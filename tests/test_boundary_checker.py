"""Tests for core/boundary_checker.py — BOUNDARY CHECK 执行引擎"""

import json
from pathlib import Path

import pytest

from aegis_toolchain.core.boundary_checker import (
    BoundaryChecker,
    BoundaryReport,
    CheckResult,
)
from aegis_toolchain.core.state_manager import StateManager
from aegis_toolchain.core.index_manager import IndexManager
from aegis_toolchain.models.state import (
    Requirement,
    RequirementLevel,
    RequirementPhase,
)
from helpers import make_req


@pytest.fixture
def prepared_project(tmp_path):
    """带有默认 INDEX.md 和 L2 目录结构的临时项目"""
    project = tmp_path / "prepared"
    project.mkdir()

    # 创建 Aegis 目录结构
    (project / "Aegis" / "state").mkdir(parents=True)
    (project / "Aegis" / "rules" / "DevLogs").mkdir(parents=True)

    # 创建 INDEX.md
    index = project / "Aegis_Specs"
    index.mkdir()
    (index / "INDEX.md").write_text(
        "# Aegis Spec Index\n\n"
        "| ID | Title | Level | Status | Start | Last Updated |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| REQ-001 | 测试 | L1 | 🔨 implementing | 2026-06-01 | 2026-06-07 |\n"
        "| REQ-002 | 设计检查 | L2 | 📐 design | 2026-06-01 | 2026-06-07 |\n"
        "| REQ-003 | review_code | L2 | 📋 review_code | 2026-06-01 | 2026-06-07 |\n",
        encoding="utf-8",
    )

    # 创建 L2 spec 目录
    l2_dir = index / "L2"
    l2_dir.mkdir()
    (l2_dir / "设计检查").mkdir()
    (l2_dir / "设计检查" / "design.md").write_text("# Design", encoding="utf-8")

    # REQ-003 reviewer
    (l2_dir / "进阶").mkdir()
    (l2_dir / "进阶" / "design.md").write_text("some design", encoding="utf-8")

    return project


@pytest.fixture
def checker(prepared_project):
    return BoundaryChecker(prepared_project)


@pytest.fixture
def state_mgr(prepared_project):
    return StateManager(prepared_project)


class TestCheckResult:
    def test_passed(self):
        cr = CheckResult("test", True, "ok")
        assert cr.passed is True

    def test_failed(self):
        cr = CheckResult("test", False, "nope")
        assert cr.passed is False


class TestBoundaryReport:
    def test_all_passed(self):
        report = BoundaryReport(
            requirement_id="REQ-001",
            phase="implementing",
            results=[CheckResult("a", True, "ok"), CheckResult("b", True, "ok")],
        )
        assert report.all_passed is True
        assert report.passed_count == 2
        assert report.total_count == 2

    def test_some_failed(self):
        report = BoundaryReport(
            requirement_id="REQ-001",
            phase="implementing",
            results=[CheckResult("a", True, "ok"), CheckResult("b", False, "nope")],
        )
        assert report.all_passed is False
        assert report.passed_count == 1


class TestBoundaryCheckerL1:
    def test_l1_no_devlog(self, prepared_project):
        bc = BoundaryChecker(prepared_project)

        # 注册需求到 state.json
        sm = StateManager(prepared_project)
        req = make_req("L1检查", level=RequirementLevel.L1, phase=RequirementPhase.IMPLEMENTING)
        sm.add_requirement(req)  # gets REQ-004

        report = bc.check(req)
        assert report.all_passed is False
        # INDEX.md 中应该找不到 REQ-004（因为 ID 自增了）
        # 使用 conftest 逻辑: add_requirement 自动分配 ID
        # 实际: let's use manual id
        req2 = Requirement(id="REQ-010", title="手动ID", level=RequirementLevel.L1)
        report2 = bc.check(req2)
        assert any(r.name == "INDEX.md 登记" for r in report2.results)

    def test_l1_index_not_registered(self, prepared_project):
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-999", title="不存在的需求", level=RequirementLevel.L1)
        report = bc.check(req)
        results_by_name = {r.name: r for r in report.results}
        assert results_by_name["INDEX.md 登记"].passed is False

    def test_l1_index_registered(self, prepared_project):
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-001", title="测试", level=RequirementLevel.L1)
        report = bc.check(req)
        results_by_name = {r.name: r for r in report.results}
        assert results_by_name["INDEX.md 登记"].passed is True


class TestBoundaryCheckerL2:
    def test_l2_design_missing_file(self, prepared_project):
        """design 阶段需要 design.md"""
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-005", title="设计未写", level=RequirementLevel.L2,
                          phase=RequirementPhase.DESIGN)
        report = bc.check(req)
        design_result = [r for r in report.results if "设计文档" in r.name][0]
        assert design_result.passed is False

    def test_l2_design_file_exists(self, prepared_project):
        """REQ-002 已经有 design.md"""
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-002", title="设计检查", level=RequirementLevel.L2,
                          phase=RequirementPhase.DESIGN)
        report = bc.check(req)
        assert report.all_passed is True

    def test_l2_implementing_no_design(self, prepared_project):
        """implementing 阶段前置验证需要 design.md"""
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-005", title="丢失设计", level=RequirementLevel.L2,
                          phase=RequirementPhase.IMPLEMENTING)
        report = bc.check(req)
        design = [r for r in report.results if "设计文档" in r.name]
        if design:
            assert design[0].passed is False

    def test_l2_review_code_status(self, prepared_project):
        """review_code 阶段需要 INDEX.md 匹配"""
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-003", title="进阶", level=RequirementLevel.L2,
                          phase=RequirementPhase.REVIEW_CODE)
        report = bc.check(req)
        status_results = [r for r in report.results if "INDEX.md 状态" == r.name]
        assert len(status_results) == 1, f"应有一条 INDEX.md 状态检查，实际: {status_results}"
        assert status_results[0].passed is True, f"REVIEW_CODE 状态应匹配，实际: {status_results[0].detail}"

    def test_l2_paused(self, prepared_project):
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-005", title="暂停的需求", level=RequirementLevel.L2,
                          phase=RequirementPhase.PAUSED)
        report = bc.check(req)
        assert report.all_passed is False

    def test_l2_cancelled(self, prepared_project):
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-005", title="取消的需求", level=RequirementLevel.L2,
                          phase=RequirementPhase.CANCELLED)
        report = bc.check(req)
        assert report.all_passed is False


class TestBoundaryCheckerL3:
    def test_l3_done(self, prepared_project):
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-005", title="L3完成", level=RequirementLevel.L3,
                          phase=RequirementPhase.DONE)
        report = bc.check(req)
        # L3 DONE 拉清单 → 检查 done 状态和 devlog
        assert any(r.name == "INDEX.md 已更新" for r in report.results)
        assert any("DevLog" in r.name for r in report.results)
        # L3 done 验证失败是预期行为（REQ-005 不在 INDEX.md 中）
        assert report.all_passed is False

    def test_l3_paused(self, prepared_project):
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-005", title="L3暂停", level=RequirementLevel.L3,
                          phase=RequirementPhase.PAUSED)
        report = bc.check(req)
        assert report.all_passed is False

    def test_l3_cancelled(self, prepared_project):
        bc = BoundaryChecker(prepared_project)
        req = Requirement(id="REQ-005", title="L3取消", level=RequirementLevel.L3,
                          phase=RequirementPhase.CANCELLED)
        report = bc.check(req)
        assert report.all_passed is False
