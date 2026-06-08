# 已知问题

> 当前版本 v5.2.0 记录在案的已知问题和限制。

## aegis init 未覆盖所有边缘情况

`aegis init` 依赖 `importlib.resources.files()` 从包内读取数据文件。在常规 Python 安装环境下已测试通过，但在以下场景未测试：

- 从 wheel 安装后运行 init
- 在非 Windows 平台运行
- 目标目录已存在部分 Aegis 文件

**建议**：在新目录跑一次 `aegis init`，目测输出的文件数量和日志是否有异常。

## pre-commit hook 的异常处理策略

pre-commit hook 在以下异常情况下选择"放行（fail open）"而非阻断：

- `state.json` 损坏或无法解析 → 放行
- BOUNDARY CHECK 抛异常（非预期错误）→ 放行

这是有意为之（避免 hook 本身故障阻塞正常开发），但意味着如果 `state.json` 损坏，hook 不会提醒你。

## INDEX.md 锁文件残留

INDEX.md 写入使用 `INDEX.md.lock` 作为文件锁。如果进程在写入时被强制终止（如 `Ctrl+C`、崩溃），锁文件可能残留。下次写入时会覆盖锁文件，不影响功能。

## Phase 2/3（MCP Server + YAML 状态机）未实现

路线图中规划的 Phase 2（MCP Server + YAML 状态机）和 Phase 3（全 MCP 生态）仅有设计文档，无任何代码实现。

- 当前 INDEX.md 中 REQ-003 和 REQ-004 处于 `📋 brainstorm` 状态
- 不影响 Phase 1 CLI 工具链的使用

## 测试覆盖缺口

- CLI 命令的核心路径已覆盖，但不包含所有可能的错误提示路径
- `aegis init` 在 CliRunner 中集成测试有限，因为它依赖 `Path.cwd()`
- `pre_commit.main()` 使用了 `os.chdir` 来切换目录，在 pytest 中测试不方便，核心逻辑通过 `invoke_hook()` 方法验证

## AGENTS.md 模板的可靠性边界

`aegis init` 生成的 AGENTS.md 模板依赖 `importlib.resources.files()` 从包内读取。在 editable install 和文件系统安装下已验证通过，但 pip wheel（zip 形式）安装时 `Traversable.is_file()` 行为因 Python 版本而异。模板缺失时 init 会输出警告并继续（不阻断）。

## AGENTS.md 模板篡改风险

如果攻击者能写入 site-packages 目录（已有任意代码执行权限），可篡改 `data/AGENTS.md` 模板向所有下游项目注入 AI 行为指令（Prompt Injection）。威胁模型不现实（能改 site-packages 的权限远大于篡改模板），但理论上存在。

## 已修复（v5.2.0）

以下问题已在 v5.2.0 中修复：

- `_check_index_status` 硬编码 `"implementing"` → 改为按阶段匹配 INDEX.md 状态
- 版本号 `main.py` 硬编码 → 引用 `__version__`
- `BoundaryChecks` 中 `index_registered / design_created / user_approved` 三个从不更新的字段 → 已删除
- `state.json` load 无锁模式 fallback（可能读到不一致数据）→ 已移除，改为抛 RuntimeError
- `state.json` save 指数退避重试（最坏 9.5s）→ 简化为单次 2s 超时
- `add_requirement` TOCTOU 竞态 → 用 `transaction()` 锁住 load→modify→save 全程
- INDEX.md 写入缺少文件锁 → 已加 `_write_locked()`
- DevLogs 不在 `.gitignore` → `aegis init` 在 DevLogs 目录生成 `.gitignore`
- INDEX.md 同步失败被静默吞掉 → 改为 visible warning
- PAUSED/CANCELLED 阶段 check 真空通过 → 已加明确检查
