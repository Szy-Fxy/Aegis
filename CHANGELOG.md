# Changelog

## v0.1.0-beta (2026-06-05)

### Added
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
