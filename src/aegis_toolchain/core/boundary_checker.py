"""BoundaryChecker — 各阶段 BOUNDARY CHECK 执行引擎"""

from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from aegis_toolchain.models.state import Requirement, RequirementLevel, RequirementPhase


@dataclass
class CheckResult:
    """单条检查结果"""
    name: str
    passed: bool
    detail: str


@dataclass
class BoundaryReport:
    """BOUNDARY CHECK 完整报告"""
    requirement_id: str
    phase: str
    results: list[CheckResult] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def total_count(self) -> int:
        return len(self.results)


class BoundaryChecker:
    """执行各阶段 BOUNDARY CHECK"""

    def __init__(self, project_path: Path) -> None:
        self.project_path = project_path

    def check(self, requirement: Requirement) -> BoundaryReport:
        """根据需求等级和阶段执行对应检查"""
        level = requirement.level
        phase = requirement.phase

        report = BoundaryReport(
            requirement_id=requirement.id,
            phase=phase.value,
        )

        if level == RequirementLevel.L1:
            report.results = self._check_l1(requirement)
        elif level == RequirementLevel.L2:
            report.results = self._check_l2(requirement)
        elif level == RequirementLevel.L3:
            report.results = self._check_l3(requirement)

        return report

    # ── L1 ─────────────────────────────────────

    def _check_l1(self, req: Requirement) -> list[CheckResult]:
        results = [
            self._check_index_registered(req.id),
            self._check_devlog_exists(req.id),
        ]
        return results

    # ── L2 ─────────────────────────────────────

    def _check_l2(self, req: Requirement) -> list[CheckResult]:
        if req.phase == RequirementPhase.DESIGN:
            return self._check_l2_design(req)
        elif req.phase == RequirementPhase.IMPLEMENTING:
            return self._check_l2_implementing(req)
        elif req.phase == RequirementPhase.DONE:
            return self._check_l2_done(req)
        return []

    def _check_l2_design(self, req: Requirement) -> list[CheckResult]:
        return [
            self._check_index_registered(req.id),
            self._check_design_file_exists(req),
            self._check_user_language_ac(req),
        ]

    def _check_l2_implementing(self, req: Requirement) -> list[CheckResult]:
        return [
            self._check_index_status(req.id),
            # Phase 1 不做代码编译检查，留空
            CheckResult(
                name="代码编译",
                passed=True,
                detail="Phase 1 跳过代码编译检查（手动验证）",
            ),
        ]

    def _check_l2_done(self, req: Requirement) -> list[CheckResult]:
        return [
            CheckResult(
                name="INDEX.md 已更新",
                passed=self._is_index_status(req.id, "✅ done"),
                detail="INDEX.md 状态应为 ✅ done",
            ),
            self._check_devlog_exists(req.id),
        ]

    # ── L3 ─────────────────────────────────────

    def _check_l3(self, req: Requirement) -> list[CheckResult]:
        phase = req.phase
        l3_dir = self.project_path / "Aegis_Specs" / "L3" / "aegis-toolchain"

        phase_files: dict[RequirementPhase, tuple[str, str]] = {
            RequirementPhase.BRAINSTORM: ("01-brainstorm.md", "头脑风暴"),
            RequirementPhase.PROPOSAL: ("02-proposal.md", "提案"),
            RequirementPhase.DESIGN: ("03-design.md", "技术设计"),
            RequirementPhase.SPEC: ("04-spec.md", "需求规格"),
            RequirementPhase.REVIEW: ("06-review.md", "集成审核"),
        }

        results: list[CheckResult] = [self._check_index_registered(req.id)]

        if phase == RequirementPhase.REVIEW:
            # review 阶段还需检查 05-tasks.md
            for fname, label in [("05-tasks.md", "任务拆分"), ("06-review.md", "集成审核")]:
                results.append(self._check_file(l3_dir / fname, label))
        elif phase in (RequirementPhase.IMPLEMENTING, RequirementPhase.DONE):
            return self._check_l2_implementing(req)
        elif phase in phase_files:
            fname, label = phase_files[phase]
            results.append(self._check_file(l3_dir / fname, label))

        return results

    # ── 基础检查函数 ───────────────────────────

    def _check_index_registered(self, req_id: str) -> CheckResult:
        """检查 INDEX.md 是否登记了该需求"""
        index_path = self.project_path / "Aegis_Specs" / "INDEX.md"
        if not index_path.exists():
            return CheckResult(
                name="INDEX.md 登记",
                passed=False,
                detail=f"INDEX.md 不存在",
            )

        content = index_path.read_text(encoding="utf-8")
        if req_id in content:
            return CheckResult(name="INDEX.md 登记", passed=True, detail=f"{req_id} 已登记")
        return CheckResult(
            name="INDEX.md 登记",
            passed=False,
            detail=f"INDEX.md 中未找到 {req_id}",
        )

    def _check_design_file_exists(self, req: Requirement) -> CheckResult:
        """检查 design.md 是否存在（L2 使用 L2 目录，L3 使用 L3 目录）"""
        if req.level == RequirementLevel.L3:
            path = self.project_path / "Aegis_Specs" / "L3" / "aegis-toolchain" / "03-design.md"
        else:
            path = self.project_path / "Aegis_Specs" / "L2" / req.title / "design.md"

        return self._check_file(path, "设计文档")

    def _check_user_language_ac(self, req: Requirement) -> CheckResult:
        """检查验收标准是否包含用户语言描述（Phase 1 为占位检查）"""
        return CheckResult(
            name="验收标准含用户语言",
            passed=True,
            detail="Phase 1 跳过用户语言检查（手动验证）",
        )

    def _check_index_status(self, req_id: str) -> CheckResult:
        """检查 INDEX.md 中状态是否为 implementing"""
        index_path = self.project_path / "Aegis_Specs" / "INDEX.md"
        if not index_path.exists():
            return CheckResult(name="INDEX.md 状态", passed=False, detail="INDEX.md 不存在")

        content = index_path.read_text(encoding="utf-8")
        if "implementing" in content.lower() and req_id in content:
            return CheckResult(
                name="INDEX.md 状态",
                passed=True,
                detail=f"{req_id} 状态为 implementing",
            )
        return CheckResult(
            name="INDEX.md 状态",
            passed=False,
            detail=f"{req_id} 状态不是 implementing",
        )

    def _check_devlog_exists(self, req_id: str) -> CheckResult:
        """检查 DevLog 是否已写入"""
        devlog_dir = self.project_path / "Aegis" / "rules" / "DevLogs"
        if not devlog_dir.exists():
            return CheckResult(name="DevLog 已写入", passed=False, detail="DevLogs 目录不存在")

        for f in devlog_dir.glob("*.md"):
            if req_id in f.name:
                return CheckResult(
                    name="DevLog 已写入",
                    passed=True,
                    detail=f"DevLog 已存在: {f.name}",
                )
        return CheckResult(
            name="DevLog 已写入",
            passed=False,
            detail=f"未找到 {req_id} 的 DevLog",
        )

    def _check_file(self, path: Path, label: str) -> CheckResult:
        """通用文件存在性检查"""
        if path.exists():
            return CheckResult(name=label, passed=True, detail=f"{label} 已创建: {path.name}")
        return CheckResult(name=label, passed=False, detail=f"{label} 不存在: {path}")

    def _is_index_status(self, req_id: str, expected: str) -> bool:
        """检查 INDEX.md 中指定需求的状态"""
        index_path = self.project_path / "Aegis_Specs" / "INDEX.md"
        if not index_path.exists():
            return False
        content = index_path.read_text(encoding="utf-8")
        return req_id in content and expected.lower() in content.lower()
