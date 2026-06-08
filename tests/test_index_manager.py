"""Tests for core/index_manager.py — INDEX.md 读写"""

import pytest

from aegis_toolchain.core.index_manager import IndexManager


@pytest.fixture
def prepared_project(tmp_path):
    """带有默认 INDEX.md 的临时项目"""
    project = tmp_path / "project"
    project.mkdir()
    (project / "Aegis_Specs").mkdir()
    (project / "Aegis_Specs" / "INDEX.md").write_text(
        "# Aegis Spec Index\n\n"
        "| ID | Title | Level | Status | Start | Last Updated |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| REQ-001 | 测试需求 | L1 | 📐 design | 2026-06-01 | 2026-06-07 |\n"
        "| REQ-002 | 另一个需求 | L2 | 🔨 implementing | 2026-06-02 | 2026-06-07 |\n",
        encoding="utf-8",
    )
    return project


class TestIndexManager:
    def test_read_all(self, prepared_project):
        mgr = IndexManager(prepared_project)
        entries = mgr.read_all()
        assert len(entries) >= 2
        ids = [e["id"] for e in entries]
        assert "REQ-001" in ids
        assert "REQ-002" in ids

    def test_get_entry(self, prepared_project):
        mgr = IndexManager(prepared_project)
        entry = mgr.find_entry("REQ-001")
        assert entry is not None
        assert entry["id"] == "REQ-001"
        assert entry["title"] == "测试需求"

    def test_get_nonexistent(self, prepared_project):
        mgr = IndexManager(prepared_project)
        assert mgr.find_entry("REQ-999") is None

    def test_add_entry(self, prepared_project):
        mgr = IndexManager(prepared_project)
        mgr.add_entry("REQ-003", "新增需求", "L1", "🔨 implementing")

        entries = mgr.read_all()
        ids = [e["id"] for e in entries]
        assert "REQ-003" in ids

        found = [e for e in entries if e["id"] == "REQ-003"][0]
        assert found["title"] == "新增需求"
        assert found["level"] == "L1"
        assert "implementing" in found["status"]

    def test_update_status(self, prepared_project):
        mgr = IndexManager(prepared_project)
        mgr.update_status("REQ-001", "🔨 implementing")

        entry = mgr.find_entry("REQ-001")
        assert "implementing" in entry["status"]

    def test_update_only_affects_target(self, prepared_project):
        """只更新目标行，不影响其他行"""
        mgr = IndexManager(prepared_project)
        mgr.update_status("REQ-002", "✅ done")

        assert "done" in mgr.find_entry("REQ-002")["status"]
        assert "design" in mgr.find_entry("REQ-001")["status"]

    def test_read_nonexistent(self, tmp_path):
        """不存在的 INDEX.md 返回空列表"""
        project = tmp_path / "no_index"
        project.mkdir()
        mgr = IndexManager(project)
        assert mgr.read_all() == []

    def test_empty_index(self, prepared_project):
        """已存在的 INDEX.md 可以正确读取"""
        mgr = IndexManager(prepared_project)
        entries = mgr.read_all()
        # 至少有 header row 后的数据
        assert isinstance(entries, list)
