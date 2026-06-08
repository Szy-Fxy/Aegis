"""BoundaryChecker — 各阶段 BOUNDARY CHECK 执行引擎"""

from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from aegis_toolchain.models.state import PHASE_DISPLAY_MAP, Requirement, RequirementLevel, RequirementPhase


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
        if req.phase == RequirementPhase.PAUSED:
            return [CheckResult(
                name="需求已暂停",
                passed=False,
                detail=f"{req.id} 处于 ⏸️ paused 状态，无法推进。请手动恢复或完成",
            )]
        if req.phase == RequirementPhase.CANCELLED:
            return [CheckResult(
                name="需求已取消",
                passed=False,
                detail=f"{req.id} 处于 ❌ cancelled 状态，无法推进",
            )]
        results = [
            self._check_index_registered(req.id),
            self._check_devlog_exists(req.id),
        ]
        return results

    # ── L2 ─────────────────────────────────────

    def _check_l2(self, req: Requirement) -> list[CheckResult]:
        if req.phase == RequirementPhase.DESIGN:
            return self._check_l2_design(req)
        elif req.phase == RequirementPhase.REVIEW_DESIGN:
            return self._check_l2_review_design(req)
        elif req.phase == RequirementPhase.IMPLEMENTING:
            return self._check_l2_implementing(req)
        elif req.phase == RequirementPhase.REVIEW_CODE:
            return self._check_l2_review_code(req)
        elif req.phase == RequirementPhase.VERIFY:
            return self._check_l2_verify(req)
        elif req.phase == RequirementPhase.DONE:
            return self._check_l2_done(req)
        elif req.phase == RequirementPhase.PAUSED:
            return [CheckResult(
                name="需求已暂停",
                passed=False,
                detail=f"{req.id} 处于 ⏸️ paused 状态，无法推进。请手动恢复或完成",
            )]
        elif req.phase == RequirementPhase.CANCELLED:
            return [CheckResult(
                name="需求已取消",
                passed=False,
                detail=f"{req.id} 处于 ❌ cancelled 状态，无法推进",
            )]
        return []

    def _check_l2_design(self, req: Requirement) -> list[CheckResult]:
        return [
            self._check_index_registered(req.id),
            self._check_design_file_exists(req),
        ]

    def _check_l2_review_design(self, req: Requirement) -> list[CheckResult]:
        review_path = self._review_path(req)
        design_path = self._spec_path(req) / "design.md"
        return [
            self._check_index_registered(req.id),
            self._check_file(design_path, "设计文档（前置验证）"),
            self._check_file(review_path, "审查文档"),
            CheckResult(
                name="设计审查",
                passed=self._file_has_content(review_path, "设计审查"),
                detail="review.md 需包含设计审查记录",
            ),
        ]

    def _check_l2_implementing(self, req: Requirement) -> list[CheckResult]:
        design_path = self._spec_path(req) / "design.md"
        review_path = self._review_path(req)
        return [
            self._check_index_status(req.id, req.phase),
            self._check_file(design_path, "设计文档（前置验证）"),
            self._check_file(review_path, "审查文档（前置验证）"),
        ]

    def _check_l2_review_code(self, req: Requirement) -> list[CheckResult]:
        review_path = self._review_path(req)
        design_path = self._spec_path(req) / "design.md"
        return [
            self._check_index_status(req.id, req.phase),
            self._check_file(design_path, "设计文档（前置验证）"),
            self._check_file(review_path, "审查文档"),
            CheckResult(
                name="代码审查",
                passed=self._file_has_content(review_path, "代码审查"),
                detail="review.md 需包含代码审查记录",
            ),
        ]

    def _check_l2_verify(self, req: Requirement) -> list[CheckResult]:
        verify_path = self._spec_path(req) / "verify.md"
        review_path = self._review_path(req)
        return [
            self._check_index_registered(req.id),
            self._check_file(review_path, "审查文档（前置验证）"),
            self._check_file(verify_path, "验收报告"),
        ]

    def _check_l2_done(self, req: Requirement) -> list[CheckResult]:
        done_display = PHASE_DISPLAY_MAP.get(RequirementPhase.DONE, "✅ done")
        return [
            CheckResult(
                name="INDEX.md 已更新",
                passed=self._is_index_status(req.id, done_display),
                detail=f"INDEX.md 状态应为 {done_display}",
            ),
            self._check_devlog_exists(req.id),
        ]

    # ── 辅助路径 ───────────────────────────

    def _spec_path(self, req: Requirement) -> Path:
        """根据需求等级返回 spec 目录路径，对标题做路径净化"""
        safe = req.title.replace("\\", "_").replace("/", "_").replace("..", "_")
        if req.level == RequirementLevel.L3:
            return self.project_path / "Aegis_Specs" / "L3" / safe
        return self.project_path / "Aegis_Specs" / "L2" / safe

    def _review_path(self, req: Requirement) -> Path:
        return self._spec_path(req) / "review.md"

    # ── L3 ─────────────────────────────────────

    def _check_l3(self, req: Requirement) -> list[CheckResult]:
        phase = req.phase
        l3_dir = self._spec_path(req)

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
        elif phase == RequirementPhase.DONE:
            return self._check_l2_done(req)
        elif phase == RequirementPhase.PAUSED:
            results.append(CheckResult(
                name="需求已暂停",
                passed=False,
                detail=f"{req.id} 处于 ⏸️ paused 状态",
            ))
        elif phase == RequirementPhase.CANCELLED:
            results.append(CheckResult(
                name="需求已取消",
                passed=False,
                detail=f"{req.id} 处于 ❌ cancelled 状态",
            ))
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

        content = self._read_safe(index_path)
        if content is None:
            return CheckResult(name="INDEX.md 登记", passed=False, detail="INDEX.md 无法读取")
        if req_id in content:
            return CheckResult(name="INDEX.md 登记", passed=True, detail=f"{req_id} 已登记")
        return CheckResult(
            name="INDEX.md 登记",
            passed=False,
            detail=f"INDEX.md 中未找到 {req_id}",
        )

    def _check_design_file_exists(self, req: Requirement) -> CheckResult:
        """检查 design.md 是否存在（L2/L3 统一使用 _spec_path 净化）"""
        if req.level == RequirementLevel.L3:
            path = self._spec_path(req) / "03-design.md"
        else:
            path = self._spec_path(req) / "design.md"

        return self._check_file(path, "设计文档")

    def _check_index_status(self, req_id: str, phase: RequirementPhase) -> CheckResult:
        """检查 INDEX.md 中指定需求的状态是否匹配当前阶段"""
        index_path = self.project_path / "Aegis_Specs" / "INDEX.md"
        if not index_path.exists():
            return CheckResult(name="INDEX.md 状态", passed=False, detail="INDEX.md 不存在")

        content = self._read_safe(index_path)
        if content is None:
            return CheckResult(name="INDEX.md 状态", passed=False, detail="INDEX.md 无法读取")

        expected = PHASE_DISPLAY_MAP.get(phase, phase.value)

        # 逐行检查：同一行内 req_id 和 expected 状态同时出现
        for line in content.split("\n"):
            if req_id in line and expected in line:
                return CheckResult(
                    name="INDEX.md 状态",
                    passed=True,
                    detail=f"{req_id} 状态为 {expected}",
                )

        return CheckResult(
            name="INDEX.md 状态",
            passed=False,
            detail=f"{req_id} 状态不是 {expected}（当前行: {expected}）",
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

    def _file_has_content(self, path: Path, keyword: str) -> bool:
        """检查文件是否包含指定关键词，兼容常见编码"""
        if not path.exists():
            return False
        for enc in ("utf-8", "utf-16", "gbk", "gb18030"):
            try:
                return keyword in path.read_text(encoding=enc)
            except (UnicodeDecodeError, LookupError):
                continue
        return False

    def _is_index_status(self, req_id: str, expected: str) -> bool:
        """检查 INDEX.md 中指定需求的状态"""
        index_path = self.project_path / "Aegis_Specs" / "INDEX.md"
        if not index_path.exists():
            return False
        content = self._read_safe(index_path)
        return content is not None and req_id in content and expected.lower() in content.lower()

    @staticmethod
    def _read_safe(path: Path) -> str | None:
        """安全读取文件，兼容 UTF-8/UTF-16/GBK/GB18030"""
        for enc in ("utf-8", "utf-16", "gbk", "gb18030"):
            try:
                return path.read_text(encoding=enc)
            except (UnicodeDecodeError, LookupError):
                continue
        return None
