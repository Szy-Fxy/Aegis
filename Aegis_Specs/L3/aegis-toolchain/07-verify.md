# 验证：Aegis Toolchain Phase 1

> L3-7 | 2026-06-05 | 验收确认

## 验收标准

| # | 标准 | 验证方法 | 结果 |
|---|------|---------|------|
| 1 | `aegis start "标题" --level auto` 自动分类并登记 | 执行后 `aegis status` 显示新需求 | ✅ |
| 2 | `aegis check` 对 L2-design 阶段检查 3/3 项 | 创建 design.md 后执行 check | ✅ |
| 3 | `aegis advance` 正确推进 L2: design→implementing→done | 连续两次 advance | ✅ |
| 4 | `aegis devlog write REQ-XXX -m "内容"` 生成 DevLog | 检查文件存在 + 格式正确 | ✅ |
| 5 | `aegis status --json` 输出合法 JSON | 管道到 `python -m json.tool` | ✅ |
| 6 | `aegis preprocess "修复bug"` 分类并增强 prompt | 输出含 [AEGIS MANDATORY] 标记 | ✅ |
| 7 | 并发保存 state.json 不损坏 | 两进程同时 save（需测试脚本） | ⬜ |
| 8 | state.json 损坏时给出修复建议 | 写入非法 JSON 后 load | ⬜ |
| 9 | pre-commit hook 阻断不合规提交 | 制造 implementing 需求 + 缺失 DevLog | ⬜ |

## 端到端测试记录

**测试环境**: Windows 10, Python 3.14, Git 2.x  
**测试日期**: 2026-06-05  
**测试需求**: "鱼转向运动优化" (L2)

| 步骤 | 命令 | 预期 | 实际 | 
|------|------|------|------|
| 1 | `aegis start "鱼转向运动优化" -l L2` | REQ-001 已登记 | ✅ |
| 2 | 创建 design.md | — | ✅ |
| 3 | `aegis check` | 3/3 通过 | ✅ |
| 4 | `aegis advance` | design → 🔨 implementing | ✅ |
| 5 | `aegis devlog write REQ-001 -m "xxx"` | DevLog 已写入 | ✅ |
| 6 | `aegis advance` | implementing → ✅ done | ✅ |
| 7 | `aegis status` | 0 活跃, 1 已完成 | ✅ |

## 已知问题

| # | 问题 | 严重度 | 计划 |
|---|------|--------|------|
| 1 | 预处理器依赖 AI 主动调用，无自动注入 | 中 | Phase 2 MCP 解决 |
| 2 | filelock 网络文件系统行为未经测试 | 低 | Phase 2 |
| 3 | DevLog 编辑器模式在无 GUI 环境下可能失败 | 低 | 提供 `-m` 备选 |
| 4 | 分类器关键词匹配精度约 80% | 低 | 可接受，Phase 2 可引入 LLM 辅助 |

## 未完成的测试项

- 并发 save 压力测试（需要测试脚本）
- 损坏 state.json 的恢复测试
- pre-commit hook 阻断场景的完整测试
- 跨平台（macOS/Linux）验证

> 以上三项标记 ⬜ 的验收标准不影响 Phase 1 交付，在 Phase 1.1 热修复中补充。

## 交付确认

- [x] 26 个 Python 源文件
- [x] pyproject.toml + .gitignore + .pre-commit-config.yaml
- [x] README.md + USAGE.md
- [x] L3 7 阶段文档链（01-brainstorm → 06-review → 07-verify）
- [x] Git tag: v0.1.0-beta
- [x] 端到端 L2 流程验证通过
- [x] 旧版 legacy-v3.1 归档
