"""任务等级分类器 — 关键词匹配 + 规则"""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class ClassificationResult:
    """分类结果"""
    level: str  # "L1" / "L2" / "L3"
    confidence: float  # 0.0 ~ 1.0
    keywords_matched: list[str]
    reason: str

    @property
    def is_uncertain(self) -> bool:
        return self.confidence < 0.5


# 关键词表：按优先级从高到低
L3_KEYWORDS: list[str] = ["架构", "重构", "重写", "大改", "重新设计"]
L2_KEYWORDS: list[str] = ["新增", "功能", "模块", "优化", "feature", "实现", "添加", "增加", "开发"]
L1_KEYWORDS: list[str] = ["修复", "fix", "改个", "小改", "配置", "typo", "颜色", "文案", "bug", "改一下", "改下"]


def classify(user_message: str) -> ClassificationResult:
    """根据关键词匹配分类任务等级"""
    msg_lower = user_message.lower()

    # L3 关键词（优先级最高）
    matched_l3 = [kw for kw in L3_KEYWORDS if kw.lower() in msg_lower]
    if matched_l3:
        return ClassificationResult(
            level="L3",
            confidence=0.7,
            keywords_matched=matched_l3,
            reason=f"匹配 L3 关键词: {', '.join(matched_l3)}",
        )

    # L1 关键词
    matched_l1 = [kw for kw in L1_KEYWORDS if kw.lower() in msg_lower]
    if matched_l1:
        return ClassificationResult(
            level="L1",
            confidence=0.75,
            keywords_matched=matched_l1,
            reason=f"匹配 L1 关键词: {', '.join(matched_l1)}",
        )

    # L2 关键词
    matched_l2 = [kw for kw in L2_KEYWORDS if kw.lower() in msg_lower]
    if matched_l2:
        return ClassificationResult(
            level="L2",
            confidence=0.65,
            keywords_matched=matched_l2,
            reason=f"匹配 L2 关键词: {', '.join(matched_l2)}",
        )

    # 默认 L2
    return ClassificationResult(
        level="L2",
        confidence=0.3,
        keywords_matched=[],
        reason="未匹配到明确关键词，默认 L2（置信度低，请 AI 自行确认）",
    )
