# 头脑风暴：Aegis Toolchain

> L3-1 | 2026-06-05 | 项目立项

## 问题

Aegis 是 AI 开发治理系统，核心矛盾在于：**试图用纯文本文档约束 AI 行为，但 AI 不是编译器**。当前存在三个致命缺陷：

1. **触发不可靠**：依赖 AI 主动读取规则文件（AGENTS.md、SKILL.md），没有技术手段保证 100% 触发
2. **检查形同虚设**：BOUNDARY CHECK 要求 AI 用 `read` 自查自证，AI 可以跳过或作假
3. **状态不可靠**：DevLog 用纯文本描述进度，AI 写错或遗漏就断点丢失

上一次分析整理出 7 个改进方案（预处理/CLI/GitHook/Plugin/MCP/YAML引擎/自检），现在需要将这些方案落地为正式工程。

## 目标

构建 **Aegis Toolchain**——一套独立于 AI 的工具链，将流程约束从"AI 自律"转向"工具强制"。

## 方案

### 方案 A — 轻量集成：CLI + 预处理器 + Git Hook

**核心思路**：三个独立模块各自管一个入口点

```
preprocessor.py  →  消息预处理，自动注入规则到 system prompt
aegis CLI        →  check/start/advance/devlog，强制执行 BOUNDARY CHECK
Git Hook         →  pre-commit/pre-push，阻断不合规提交
```

- **特点**：开发快（3-5天），各自独立，可渐进部署
- **风险**：三个模块各自维护，长期可能职责重叠；CLI 仍依赖 AI 主动调用

### 方案 B — 平台集成：MCP Server + YAML 状态机

**核心思路**：一套 MCP Server 统一对外，内部用 YAML 状态机驱动

```
MCP Server ── 提供 Tools(aegis_classify, aegis_check, aegis_advance, aegis_devlog)
           ── 提供 Resources(global rules, tech stack rules, workflow engine)
           ── 内部状态机：YAML 定义 L1/L2/L3 工作流，引擎强制执行阶段转换
```

- **特点**：单一入口，AI 通过标准 MCP 协议调用；状态机确保流程不可跳过；跨平台（MCP 是开放标准）
- **风险**：MCP 较新，Python SDK 成熟度待验证；Hana 支持 MCP 的程度不明

### 方案 C — 渐进演进：A → 逐步升级到 B

**核心思路**：先落地方案 A 的模块，同时保留 MCP 接口设计，未来自然升级

```
Phase 1（本周）: preprocessor.py + aegis CLI + state.json
Phase 2（本月）: 用 MCP Server 包装 CLI 功能，内部引入 YAML 状态机
Phase 3（下月）: 淘汰独立 preprocessor，全部走 MCP
```

- **特点**：风险最低，每阶段有可用的交付物；架构预留 MCP 升级路径
- **风险**：Phase 1 到 Phase 2 可能需要部分重构；如果 MCP 最终不可行，停在 Phase 1 也够用

## 推荐

**推荐方案 C（渐进演进）**。

理由：
1. 当前最痛的是"触发不可靠"和"检查不可跳过"，方案 A 的 preprocessor + CLI 能立即解决
2. MCP 方向正确但成熟度待验证，不能押注在一个新协议上
3. 渐进架构让每一步都有交付物，不会出现"做了两个月什么都没出来"
4. 即使 MCP 最终不能用，Phase 1 的工具链本身也足够改善 Aegis

## 技术选型（初步）

| 模块 | 技术选型 | 理由 |
|------|---------|------|
| 语言 | Python 3.11+ | 跨平台，生态丰富，CLI 开发效率高 |
| CLI 框架 | typer | 类型注解驱动，自动生成 help，比 click 更现代 |
| 项目管理 | Poetry | 依赖锁定，打包分发方便 |
| 状态管理 | Pydantic v2 + JSON | 类型安全 + schema 校验，比纯 dict 可靠 |
| 文件锁 | filelock | 轻量，跨平台，多进程安全 |
| 日志 | loguru | 比标准库 logging 简洁，CLI 友好 |
| Git 操作 | GitPython | 读 git 状态，不需要 subprocess |
| MCP Server | mcp (Python SDK) | Anthropic 官方，待验证 |
| 状态机 | transitions | 轻量，YAML 集成方便 |

> 注：以上为初步选型，等待四个调研子代理返回后最终确定。
