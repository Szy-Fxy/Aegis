"""Tests for core/classifier.py — 任务分类"""

from aegis_toolchain.core.classifier import classify, ClassificationResult


class TestClassifier:
    def test_l1_trivial_fix(self):
        result = classify("修复一个 typo")
        assert result.level == "L1"
        assert result.confidence > 0

    def test_l1_single_line(self):
        result = classify("改一下配置文件的端口号")
        assert result.level == "L1"
        assert result.confidence > 0

    def test_l1_fix(self):
        result = classify("修复登录页面的 bug")
        assert result.level == "L1"
        assert result.confidence > 0

    def test_l2_feature(self):
        result = classify("添加用户注册功能")
        assert result.level == "L2"
        assert result.confidence > 0

    def test_l2_module(self):
        result = classify("实现评论模块")
        assert result.level == "L2"
        assert result.confidence > 0

    def test_l2_optimize(self):
        result = classify("优化数据库查询性能")
        assert result.level == "L2"
        assert result.confidence > 0

    def test_l3_architecture(self):
        result = classify("重构整个后端服务架构")
        assert result.level == "L3"
        assert result.confidence > 0

    def test_l3_redesign(self):
        result = classify("重新设计渲染管线")
        assert result.level == "L3"
        assert result.confidence > 0

    def test_result_has_reason(self):
        result = classify("添加背包系统")
        assert isinstance(result, ClassificationResult)
        assert len(result.reason) > 0

    def test_result_has_matches(self):
        result = classify("修复配置错误")
        assert isinstance(result.keywords_matched, list)
