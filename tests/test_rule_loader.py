"""Tests for core/rule_loader.py — 规则文件加载"""

import pytest
from pathlib import Path

from aegis_toolchain.core.rule_loader import RuleLoader


@pytest.fixture
def project_with_rules(tmp_path):
    """带规则文件的项目"""
    project = tmp_path / "project"
    project.mkdir()

    # global.md
    rules_dir = project / "Aegis" / "rules"
    rules_dir.mkdir(parents=True)
    (rules_dir / "global.md").write_text("## Global Rules\n\n- 遵守 SOLID 原则", encoding="utf-8")

    # TechStack
    ts_dir = rules_dir / "TechStack"
    ts_dir.mkdir()
    (ts_dir / "python.md").write_text("## Python Rules\n\n- 使用 type hints", encoding="utf-8")
    (ts_dir / "cpp.md").write_text("## C++ Rules\n\n- RAII", encoding="utf-8")
    (ts_dir / "unity.md").write_text("## Unity Rules\n\n- MonoBehaviour 生命周期", encoding="utf-8")

    # skills
    skills_dir = project / "Aegis" / "skills" / "dev-workflow"
    skills_dir.mkdir(parents=True)
    (skills_dir / "SKILL.md").write_text("## Workflow\n\n- L1/L2/L3", encoding="utf-8")

    # AGENTS.md
    (project / "AGENTS.md").write_text("# Project Context\n\nThis is a test project.", encoding="utf-8")

    return project


class TestRuleLoader:
    def test_load_global(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_global()
        assert "SOLID" in content

    def test_load_global_missing(self, tmp_path):
        loader = RuleLoader(tmp_path)
        assert loader.load_global() == ""

    def test_load_workflow(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_workflow()
        assert "L1/L2/L3" in content

    def test_load_workflow_missing(self, tmp_path):
        loader = RuleLoader(tmp_path)
        assert loader.load_workflow() == ""

    def test_load_all(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        all_rules = loader.load_all()
        assert "global.md" in all_rules
        assert "dev-workflow.md" in all_rules

    def test_techstack_match_python(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_techstack(["python", "fastapi"])
        assert "type hints" in content

    def test_techstack_match_cpp(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_techstack(["cpp", "cmake"])
        assert "RAII" in content

    def test_techstack_no_match(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_techstack(["ruby", "php"])
        assert content == ""

    def test_techstack_multiple(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_techstack(["python", "cpp"])
        assert "type hints" in content
        assert "RAII" in content

    def test_techstack_with_unity(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_techstack(["unity", "c#"])
        assert len(content) > 0

    def test_load_project_context(self, project_with_rules):
        loader = RuleLoader(project_with_rules)
        content = loader.load_project_context()
        assert "test project" in content

    def test_load_project_context_readme(self, tmp_path):
        (tmp_path / "README.md").write_text("# My Project", encoding="utf-8")
        loader = RuleLoader(tmp_path)
        content = loader.load_project_context()
        assert "My Project" in content

    def test_load_project_context_none(self, tmp_path):
        loader = RuleLoader(tmp_path)
        assert loader.load_project_context() == ""
