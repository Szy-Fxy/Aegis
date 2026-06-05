# 任务清单：Aegis Toolchain Phase 1

> L3-5 | 2026-06-05 | 实施任务拆分

## 验收标准对照（从 02-proposal + 04-spec 摘录）

| # | 验收标准 | 来源 | 对应任务 |
|---|----------|------|----------|
| 1 | `aegis start` 1s 内完成登记 | 04-spec | Task 3.1 |
| 2 | `aegis check` 对 L2-design 检查 100% 准确 | 04-spec | Task 2.2, 3.2 |
| 3 | 并发 save 数据不损坏 | 04-spec | Task 2.1 |
| 4 | `aegis preprocess` 分类准确率 ≥80% | 04-spec | Task 4.1 |
| 5 | pre-commit hook 阻断不合规提交 | 04-spec | Task 5.1 |
| 6 | `aegis status` 精确到缺失 BOUNDARY CHECK 项 | 04-spec | Task 3.4 |
| 7 | CLI 在 Win/macOS/Linux 彩色输出正常 | 04-spec | Task 3, 6 |
| 8 | state.json 损坏时给出修复建议 | 04-spec | Task 2.1 |
| 9 | 用户说"帮我修bug"→Aegis 规则自动注入 | 02-proposal | Task 4 |

---

## Task 1: 项目脚手架 — 新增

- [ ] 1.1 创建 `aegis-toolchain/` 目录结构（src-layout、pyproject.toml、tests/）
  - 验收条件：`poetry install` 成功，`poetry run aegis --help` 输出占位帮助
- [ ] 1.2 配置 pyproject.toml（依赖：typer, pydantic, filelock, loguru, PyYAML；dev: pytest, ruff, mypy）
  - 验收条件：`ruff check` 零错误，`mypy src/` 零错误
- [ ] 1.3 配置 loguru（src/aegis_toolchain/utils/logging.py）
  - 验收条件：`from aegis_toolchain.utils.logging import logger` 可用，stderr 彩色输出

---

## Task 2: Core 核心模块 — 新增

- [ ] 2.1 `StateManager` (src/aegis_toolchain/core/state_manager.py)
  - 依赖 Pydantic models (Task 5 先？不，models 没有外部依赖，随 core 一起做)
  - 验收条件（对应验收标准 #1, #3, #8）：load/save/get_active/add_requirement 全部通过单元测试；并发锁测试通过；损坏 JSON 抛出 StateCorruptedError
- [ ] 2.2 `BoundaryChecker` (src/aegis_toolchain/core/boundary_checker.py)
  - 验收条件（对应验收标准 #2）：L1/L2-design/L2-implement/L2-verify/L3 各阶段 check 返回正确 BoundaryReport；所有 report.all_passed 逻辑正确
- [ ] 2.3 `RuleLoader` (src/aegis_toolchain/core/rule_loader.py)
  - 验收条件：load_global/load_workflow/load_techstack/load_all 返回正确内容；文件缺失时不崩溃
- [ ] 2.4 `IndexManager` (src/aegis_toolchain/core/index_manager.py)
  - 验收条件：add_entry/update_status/read_all 正确解析和生成 INDEX.md；INDEX.md 不存在时自动创建

---

## Task 3: CLI 命令 — 新增

- [ ] 3.1 `aegis start` (src/aegis_toolchain/cli/start.py)
  - 验收条件（对应验收标准 #1）：`aegis start "测试" --level L1` → state.json 和 INDEX.md 同时更新；并发保护测试通过
- [ ] 3.2 `aegis check` (src/aegis_toolchain/cli/check.py)
  - 验收条件（对应验收标准 #2）：`aegis check REQ-003` → 输出通过/失败明细，退出码正确；全部通过时退出码 0，部分失败时 1
- [ ] 3.3 `aegis advance` (src/aegis_toolchain/cli/advance.py)
  - 验收条件：check 全部通过 → 成功推进；check 未通过 → 拒绝；`--force` → 跳过
- [ ] 3.4 `aegis status` (src/aegis_toolchain/cli/status.py)
  - 验收条件（对应验收标准 #6）：无参显示全部活跃需求；指定 ID 显示详情；`--json` 输出合法 JSON
- [ ] 3.5 `aegis devlog` (src/aegis_toolchain/cli/devlog.py)
  - 验收条件：`aegis devlog REQ-003 -m "xxx"` → DevLog 文件写入正确格式；`aegis devlog show` → 显示内容
- [ ] 3.6 `aegis preprocess` (src/aegis_toolchain/cli/preprocess_cmd.py)
  - 验收条件（对应验收标准 #4, #9）：分类准确率 ≥80%；输出完整 system prompt；置信度 <0.5 时给出提示
- [ ] 3.7 CLI 入口 (src/aegis_toolchain/cli/main.py) 注册所有子命令
  - 验收条件：`aegis --help` 显示完整命令树；`aegis start --help` 显示参数说明

---

## Task 4: 预处理器 — 新增

- [ ] 4.1 `Classifier` (src/aegis_toolchain/preprocessor/classifier.py)
  - 验收条件（对应验收标准 #4）：20 条测试用例 L1/L2/L3 准确率 ≥80%
- [ ] 4.2 `Injector` (src/aegis_toolchain/preprocessor/injector.py)
  - 验收条件（对应验收标准 #9）：生成的 system prompt 包含 [AEGIS MANDATORY] 前缀 + 等级 + 流程要求 + global.md 摘要

---

## Task 5: Models 数据模型 — 新增

- [ ] 5.1 `state.py` — AegisState, Requirement, BoundaryChecks, RequirementPhase, RequirementLevel
  - 验收条件：Pydantic schema 校验覆盖所有字段类型约束；Level=L4 时抛出 ValidationError
- [ ] 5.2 `config.py` — AegisConfig
  - 验收条件：默认值正确；自定义路径覆盖有效

---

## Task 6: Git Hook — 新增

- [ ] 6.1 pre-commit hook 脚本 (src/aegis_toolchain/hooks/pre_commit.py)
  - 验收条件（对应验收标准 #5）：有 implementing 需求且 check 失败 → 退出码 1；无需求 → 退出码 0
- [ ] 6.2 `.pre-commit-config.yaml` + install 脚本
  - 验收条件：`pre-commit install` 后 `git commit` 自动触发 hook

---

## Task 7: SKILL.md 修改

- [ ] 7.1 修改 `Aegis/skills/aegis-boot/SKILL.md` — 加入自检指令块 + CLI 调用要求
  - 验收条件：SKILL.md 包含硬编码自检清单（每次回复前检查）；提及 `aegis check` / `aegis start` 命令

---

## Task 8: 集成验证

- [ ] 8.1 端到端测试：用 CLI 完成一个完整的 L2 需求模拟流程
  - 验收条件：start → check → advance → implement → check → advance → devlog → status，全程无报错
- [ ] 8.2 pre-commit hook 端到端：创建 L1 需求但跳过 DevLog → git commit 被阻断
  - 验收条件：阻断 + 正确错误信息
- [ ] 8.3 跨平台验证：Windows PowerShell + Git Bash
  - 验收条件（对应验收标准 #7）：彩色输出正常，中文不乱码

---

## Task 9: 文档

- [ ] 9.1 README.md — 安装、使用、命令速查
  - 验收条件：新用户按 README 能 5 分钟内跑通 `aegis start` + `aegis check`
- [ ] 9.2 CHANGELOG.md — 初始版本 v0.1.0
  - 验收条件：记录所有功能

---

> 9 个 Task，30 个子任务。按依赖排序。Task 1-2 是基础，必须最先完成。
> 每个 Task 均附带验收条件，可追溯到 02-proposal 和 04-spec。
