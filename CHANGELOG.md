# Changelog

## v5.0.0 (2026-06-06)

### Added
- `aegis init` — 一键初始化项目 Aegis 规则文件（34 个文件）
- L2 从 3 阶段升级为 5 阶段：design → review_design → implementing → review_code → verify → done
- L2 每次审查启动 4 个子代理（code-reviewer, devils-advocate, security-auditor, ux-reviewer）× 2 轮
- L1 加入 2 个子代理审查（code-reviewer + devils-advocate）
- TechStack 缺失时研究流程加入子代理验证
- 新建模板：review-L2.md、verify-L2.md
- RequirementPhase 新增 3 个枚举：REVIEW_DESIGN, REVIEW_CODE, VERIFY
- `phase.display` 统一属性用于所有命令的 emoji 显示
- `--force` 加入 `typer.confirm` 确认提示 + `--yes` 旗标
- `__version__` = "5.0.0"

### Changed
- UNIFIED 所有 CLI 命令的 PHASE_DISPLAY 到 `RequirementPhase.display`
- 更新 INDEX.md 模板：状态说明表 12 项全覆盖
- save() 指数退避重试从 3 次增加到 5 次
- LOCK_TIMEOUT 从 5s 缩短到 2s

### Fixed
- F1: L1 advance 路由缺失 → +`PHASE_NEXT_L1` 三路分叉
- M1: `_spec_path()` 路径遍历净化（`../`、`\`、`/`）
- M2: INDEX.md 表格注入（`|`、`\n`、`\r`）
- M3: DevLog 文件名非法字符过滤
- H1: state_manager load() 超时回退 + 重试
- H2: save() TOCTOU 指数退避重试
- W1: 删除死代码 PHASE_NEXT
- W2: PHASE_INDEX_STATUS 补全 PAUSED/CANCELLED
- W4: templates/spec-L2.md 描述从 L3 阶段修正为 L2
- W5: L3 DONE 不复用 `_check_l2_implementing`
- BoundaryChecker: 编码兼容 UTF-8/UTF-16/GBK/GB18030
- B-2: 所有 L2 阶段加入前置文件验证
- M5: pip install URL 锁定 `@v5.0.0`
- M6: `--force` 加确认 + `--yes` 支持 CI/CD
- M7: 移除未使用的 pyyaml、gitpython 依赖
- Y-3: 版本号全局统一 v5.0.0
- Q5: DevLog 写入时机修正（用户确认→DevLog→advance）
- Y-2: verify-L2.md 签名栏改为 checkbox
- 修复 `_check_design_file_exists` 裸用 req.title 的路径遍历
- 修复 L3 IMPLEMENTING 复用 L2 checker 的路径错配
- `check.py` 使用 `phase.display` 统一显示

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

### Fixed
- 修复 start.py 重复实例化 StateManager
- 修复 preprocess_cmd.py 异常静默吞噬
- 修复 git 分支追踪配置错误
- 补齐 LICENSE、USAGE.md、07-verify.md
- 补齐 pyproject.toml 元数据（classifiers, urls, keywords）
