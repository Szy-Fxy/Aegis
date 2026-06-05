"""System Prompt 注入器 — 根据分类结果构建增强版 prompt"""

from aegis_toolchain.models.state import AegisState
from aegis_toolchain.preprocessor.classifier import ClassificationResult

L1_FLOW = (
    "登记 INDEX.md (🔨 implementing) → 改代码 → "
    "展示改动摘要 → 等用户确认 → DevLog → INDEX.md (✅ done)"
)

L2_FLOW = (
    "登记 INDEX.md (📐 design) → 创建设计文档 → 等用户确认 → "
    "INDEX.md (🔨 implementing) → 写代码 → BOUNDARY CHECK → "
    "INDEX.md (✅ done) → DevLog"
)

L3_FLOW = (
    "头脑风暴 → 提案 → 技术设计 → 需求规格 → 任务拆分 → "
    "集成审核（子代理审查）→ 实现验证 → 收尾仪式"
)

FLOW_MAP = {"L1": L1_FLOW, "L2": L2_FLOW, "L3": L3_FLOW}


def build_system_prompt(
    classification: ClassificationResult,
    rules: dict[str, str],
    project_state: AegisState | None = None,
) -> str:
    """根据分类结果和规则构建增强版 system prompt"""

    flow = FLOW_MAP.get(classification.level, L2_FLOW)
    level_note = ""
    if classification.is_uncertain:
        level_note = (
            "\n⚠️ 分类置信度较低，请根据实际任务复杂度自行确认等级。"
            "如果确实是简单修改，可降级为 L1。"
        )

    # 规则摘要（取 global.md 前 800 字）
    global_rules = rules.get("global.md", "")
    rules_summary = global_rules[:800]
    if len(global_rules) > 800:
        rules_summary += "\n... (完整规则请读取 Aegis/rules/global.md)"

    # 活跃需求提示
    active_info = ""
    if project_state and project_state.active_requirements:
        active_info = "\n当前活跃需求:\n"
        for r in project_state.active_requirements:
            active_info += f"  - {r.id} [{r.level.value}] {r.phase.value}: {r.title}\n"

    prompt = f"""[AEGIS MANDATORY RULES — DO NOT IGNORE]
任务等级: {classification.level}
置信度: {classification.confidence:.2f}
分类理由: {classification.reason}{level_note}

该等级的要求流程:
{flow}
{active_info}
关键规则摘要:
{rules_summary}

BOUNDARY CHECK 要求:
- 每个阶段结束时，必须运行 `aegis check` 验证文件存在性和 INDEX.md 状态。
- Git 提交前 pre-commit hook 会自动验证 Aegis 合规性，不通过会阻断提交。

可用命令（按流程调用）:
  aegis start "<标题>" --level {classification.level}  开始新需求
  aegis check                                          执行 BOUNDARY CHECK
  aegis advance                                        推进到下一阶段
  aegis status                                         查看当前状态
  aegis devlog <REQ-ID> -m "<内容>"                   写入 DevLog

请严格遵守以上流程。"""
    return prompt
