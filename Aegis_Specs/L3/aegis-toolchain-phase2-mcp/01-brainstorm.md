# 头脑风暴：Aegis Toolchain Phase 2 — MCP + YAML 状态机

> L3-1 | 2026-06-05 | REQ-003

## 问题

Phase 1 的 CLI 仍然依赖 AI 主动调用——`aegis check`、`aegis start` 需要 AI 记得执行。MCP Server 可以把这些变成 LLM 的工具调用，由协议层强制执行。

## 方案

### 方案 A — MCP Server + 现有 CLI 内核

将 Phase 1 的 core 模块（StateManager、BoundaryChecker、RuleLoader、IndexManager）包装为 MCP Server 的 Tools：

```
MCP Tools:
  aegis_start(title, level) → 复用 StateManager.add_requirement()
  aegis_check(requirement_id) → 复用 BoundaryChecker.check()
  aegis_advance(requirement_id) → 复用 StateManager + BoundaryChecker
  aegis_status() → 复用 StateManager.load()
  aegis_devlog(requirement_id, message) → 复用 CLI devlog 逻辑
  aegis_classify(message) → 复用 Classifier.classify()

MCP Resources:
  aegis://rules/global → RuleLoader.load_global()
  aegis://rules/techstack/{name} → RuleLoader.load_techstack()
  aegis://state → StateManager.load()
```

传输层：stdio（Claude Desktop 模式，按需启动）

### 方案 B — MCP Server + YAML 状态机 + python-statemachine

在方案 A 基础上，用 python-statemachine 替代当前手写的阶段推进逻辑：

```yaml
# L2-workflow.yaml
states: [registered, design, implementing, verify, done]
transitions:
  - trigger: start → design
  - trigger: design_approved → implementing
  - trigger: code_done → verify
  - trigger: verified → done
guards:
  design_approved: [index_registered, design_created, user_approved]
  code_done: [compile_pass]
  verified: [devlog_written]
```

状态机引擎自动执行 BOUNDARY CHECK 作为 guard，guard 不通过则拒绝状态转换。

### 方案 C — 纯 MCP，放弃独立 CLI

MCP Server 作为唯一入口，彻底淘汰 Phase 1 的 Typer CLI。用户和 AI 都通过 MCP 协议交互。CLI 降级为开发者调试用的 thin wrapper。

## 推荐

**推荐方案 B（MCP + YAML 状态机）**。

理由：
1. 调研报告确认 python-statemachine 是 2026 年最活跃的 Python 状态机库
2. MCP Python SDK v1.x 生产就绪，stdio 传输零配置
3. HanaAgent 需要插件桥接层（短期用 full-access 插件）
4. CLI 保留为 stio 启动入口，不冲突

## 关键风险

- HanaAgent 的 MCP 插件桥接是最大不确定性。如果桥接不可行，MCP Server 只能在 Claude Desktop 等工具上验证，无法在 Hana 上生效。
- MCP SDK v2（pre-alpha）可能引入 breaking changes，建议锁定 v1.x。
