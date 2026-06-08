# Changelog

## v5.2.1 (2026-06-08) — 完善入口与升级

- `aegis upgrade` 命令：升级后同步项目规则文件，备份旧版，保留用户数据
- aegis-boot SKILL.md 所有命令改为 `python -m aegis_toolchain`，AI 可正确调用
- README 重写：所有命令改为 `python -m aegis_toolchain`，解决 PATH 问题
- USAGE.md 补充本地安装路径和升级说明
- AGENTS.md、KNOWN_ISSUES.md 首次纳入仓库

## v5.2.0 (2026-06-08) — Phase 1 Complete

- aegis init 新增 AGENTS.md 自动生成，引导非 Hana AI 工具发现 Aegis 规则
- init 输出重设计：从路径清单改为欢迎引导式（[OK] / >> ASCII 标记）
- 240 pytests 覆盖所有核心模块和 CLI 命令
- 修复 `_check_index_status` 硬编码 implementing 导致的 L2 review_code→verify 阻断
- 修复 `status.py` 引用已删除的 `code_compiles` 字段
- 统一 `PHASE_INDEX_STATUS` 到 `models/state.py`
- 版本号全局统一为 5.2.0（`__init__.py`、`pyproject.toml`、CLI help）
- 统一 ✗ → ❌ 在所有 CLI 输出
- 修复 `BoundaryChecks` 残留字段（删除 index_registered/design_created/user_approved）
- `state_manager.py` 加 `transaction()` 上下文管理器，修复 TOCTOU 竞态
- INDEX.md 写入加文件锁 `_write_locked()`
- DevLogs 目录自动加 `.gitignore`
- KNOWN_ISSUES.md 记录已知问题和限制
- PAUSED/CANCELLED 阶段 check 明确处理
- INDEX.md 同步失败改为 visible warning
- 新增 `.github/workflows/test.yml` CI

## v5.1.1 (2026-06-06)

- 重构 `state_manager.py`：加载、保存、并发安全
- 重构 `boundary_checker.py`：L1/L2/L3 边界检查
- 重构 `index_manager.py`：INDEX.md 读写
- 重构 CLI 命令：start、check、advance、status、devlog、init

## v5.1.0 (2026-06-06)

- 初始 CLI 工具链实现
- L1/L2/L3 需求分级
- state.json 持久化
- pre-commit hook

## v5.0.0 (2026-06-06)

- 项目初始化
- 设计文档完成
- SKILL.md v5.0.0 更新
