# 头脑风暴：Aegis Toolchain Phase 3 — 全 MCP 生态

> L3-1 | 2026-06-05 | REQ-004

## 问题

Phase 2 虽然引入了 MCP Server，但 CLI 仍然并存。Phase 3 的目标是让 MCP 成为唯一入口，淘汰独立 Python CLI 脚本，形成完整的 MCP 工具生态。

## 方案

### 方案 A — MCP 一统

```
          ┌─────────────┐
          │ Hana / LLM  │
          └──────┬──────┘
                 │ MCP Protocol (stdio/HTTP)
          ┌──────┴──────┐
          │ Aegis MCP    │  ← 唯一入口
          │   Server     │
          │              │
          │ Tools:       │
          │  start       │
          │  check       │
          │  advance     │
          │  status      │
          │  devlog      │
          │  classify    │
          │  review      │  ← 新增：触发子代理审查
          │              │
          │ Resources:   │
          │  rules/*     │
          │  state       │
          │  index       │
          │              │
          │ YAML 引擎:   │
          │  L1/L2/L3    │
          │  workflows   │
          └──────────────┘
```

淘汰项：
- Phase 1 的 Typer CLI → 降级为开发者调试工具，不再推荐给用户
- 独立 preprocessor.py → 其功能由 MCP 的 Resources 自动提供
- 手动 INDEX.md 维护 → MCP Server 自动管理

### 方案 B — MCP + Hana 原生集成

推动 HanaAgent/Pi SDK 内核加入原生 MCP Client 支持（像 VS Code 那样），使 Aegis MCP Server 无需插件桥接即可被 HanaAgent 消费。

## 推荐

推荐方案 A（MCP 一统），方案 B 作为长期方向（取决于 Hana 团队）。

Phase 3 的核心价值：AI 不再需要"记得调用"任何命令。MCP Server 的 Tools 在 AI 的工具列表里天然可见，AI 调用工具时自动经过 BOUNDARY CHECK 的 guard。

## 关键风险

- MCP Server 常驻进程的资源消耗
- HanaAgent 如果没有 MCP 支持，Phase 3 等于没有交付
