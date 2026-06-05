"""Aegis 规则文件加载器"""

from pathlib import Path

from loguru import logger


class RuleLoader:
    """加载 Aegis 规则文件"""

    # 技术栈关键词映射
    TECHSTACK_MAP = {
        "unity": "unity.md",
        "c#": "unity.md",
        "monobehaviour": "unity.md",
        "gameobject": "unity.md",
        "python": "python.md",
        "django": "python.md",
        "fastapi": "python.md",
        "typescript": "typescript.md",
        "react": "typescript.md",
        "vue": "typescript.md",
        "node": "typescript.md",
        "javascript": "typescript.md",
        "unreal": "unreal.md",
        "ue5": "unreal.md",
        "blueprint": "unreal.md",
        "cpp": "cpp.md",
        "c++": "cpp.md",
        "cmake": "cpp.md",
        "go": "go.md",
        "golang": "go.md",
        "rust": "rust.md",
        "cargo": "rust.md",
        "java": "java.md",
        "spring": "java.md",
        "kotlin": "java.md",
        "docker": "docker.md",
        "容器": "docker.md",
        "k8s": "docker.md",
        "kubernetes": "docker.md",
    }

    def __init__(self, project_path: Path) -> None:
        self.project_path = project_path
        self.rules_path = project_path / "Aegis" / "rules"
        self.techstack_path = self.rules_path / "TechStack"
        self.skills_path = project_path / "Aegis" / "skills"

    def load_all(self) -> dict[str, str]:
        """加载所有规则，返回 {文件名: 内容}"""
        rules: dict[str, str] = {}

        global_content = self.load_global()
        if global_content:
            rules["global.md"] = global_content

        workflow_content = self.load_workflow()
        if workflow_content:
            rules["dev-workflow.md"] = workflow_content

        return rules

    def load_global(self) -> str:
        """加载 Aegis/rules/global.md"""
        return self._read_file(self.rules_path / "global.md")

    def load_workflow(self) -> str:
        """加载 Aegis/skills/dev-workflow/SKILL.md"""
        return self._read_file(self.skills_path / "dev-workflow" / "SKILL.md")

    def load_techstack(self, keywords: list[str]) -> str:
        """根据关键词匹配技术栈文件"""
        matched_files: set[str] = set()
        for kw in keywords:
            kw_lower = kw.lower()
            for pattern, filename in self.TECHSTACK_MAP.items():
                if pattern in kw_lower:
                    matched_files.add(filename)

        if not matched_files:
            logger.debug(f"未匹配到技术栈文件（关键词: {keywords}）")
            return ""

        contents = []
        for filename in sorted(matched_files):
            content = self._read_file(self.techstack_path / filename)
            if content:
                contents.append(content)

        return "\n\n---\n\n".join(contents)

    def load_project_context(self) -> str:
        """加载项目 AGENTS.md / README.md"""
        agents = self.project_path / "AGENTS.md"
        if agents.exists():
            return agents.read_text(encoding="utf-8")

        readme = self.project_path / "README.md"
        if readme.exists():
            return readme.read_text(encoding="utf-8")

        return ""

    def _read_file(self, path: Path) -> str:
        """安全读取文件"""
        if not path.exists():
            logger.debug(f"规则文件不存在: {path}")
            return ""
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"读取规则文件失败 {path}: {e}")
            return ""
