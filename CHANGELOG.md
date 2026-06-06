# Changelog

## v4.0.1 (2026-06-05)

### Fixed
- 修复 start.py 重复实例化 StateManager
- 修复 preprocess_cmd.py 异常静默吞噬
- 修复 git 分支追踪配置错误
- 移除空测试目录
- 补齐 LICENSE、USAGE.md、07-verify.md
- 补齐 pyproject.toml 元数据（classifiers, urls, keywords）

## v4.0.0 (2026-06-05)

### Added
- Aegis Toolchain Phase 1：从纯 SKILL.md 升级为 CLI 工具链
- `aegis start` — 开始新需求，支持 L1/L2/L3 自动分类
- `aegis check` — 独立执行 BOUNDARY CHECK
- `aegis advance` — 推进需求到下一阶段
- `aegis status` — 查看项目状态（支持 JSON 输出）
- `aegis devlog write/show` — DevLog 的生成和查看
- `aegis preprocess` — 消息预处理（分类 + 规则注入）
- Pydantic v2 数据模型（AegisState, Requirement, BoundaryChecks）
- filelock 并发安全的 state.json 读写
- pre-commit hook 阻断不合规提交
- 用户友好的中文错误提示

### Changed
- Aegis 纯 SKILL.md 版本（v3.1.x）归档到 legacy-v3.1 分支
- main 分支切换为 Aegis Toolchain
