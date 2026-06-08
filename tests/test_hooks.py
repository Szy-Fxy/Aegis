"""Tests for hooks/pre_commit.py — commit 前 Aegis 合规检查"""

import pytest
from unittest.mock import patch, MagicMock

from aegis_toolchain.hooks.pre_commit import main


class TestPreCommitMain:
    def test_not_aegis_project(self, tmp_path):
        """非 Aegis 项目直接返回 0"""
        with patch("aegis_toolchain.hooks.pre_commit.Path.cwd", return_value=tmp_path):
            assert main() == 0

    def test_no_implementing(self, tmp_path):
        """有 state.json 但没有 implementing 需求，返回 0"""
        # 创建 Aegis 目录
        state_dir = tmp_path / "Aegis" / "state"
        state_dir.mkdir(parents=True)
        state_json = state_dir / "state.json"
        state_json.write_text(
            '{"version":"1.0.0","active_requirements":[],"completed_requirements":[]}',
            encoding="utf-8",
        )

        with patch("aegis_toolchain.hooks.pre_commit.Path.cwd", return_value=tmp_path):
            assert main() == 0

    def test_corrupted_state_json(self, tmp_path):
        """state.json 损坏时 fail open（返回 0）"""
        state_dir = tmp_path / "Aegis" / "state"
        state_dir.mkdir(parents=True)
        (state_dir / "state.json").write_text("not valid json{{{", encoding="utf-8")

        with patch("aegis_toolchain.hooks.pre_commit.Path.cwd", return_value=tmp_path):
            assert main() == 0

    def test_implementing_not_passing(self, tmp_path):
        """有 implementing 需求但边界检查不通过，返回 1"""
        state_dir = tmp_path / "Aegis" / "state"
        state_dir.mkdir(parents=True)

        from aegis_toolchain.models.state import AegisState

        state = AegisState(
            active_requirements=[
                {
                    "id": "REQ-001",
                    "title": "测试需求",
                    "level": "L1",
                    "phase": "implementing",
                }
            ]
        )
        (state_dir / "state.json").write_text(
            state.model_dump_json(indent=2), encoding="utf-8"
        )

        with patch("aegis_toolchain.hooks.pre_commit.Path.cwd", return_value=tmp_path):
            result = main()
            # 边界检查不通过 → 1
            assert result == 1
