# Aegis Toolchain

> 🛠️ Aegis AI 开发治理工具链 v5.2.1<br>
> 让 AI 辅助开发的流程从「自律」转向「工具强制」

> 💡 **初次对话前请先`aegis start`，别手写 INDEX.md。登记、推进、记录自动化。**
=======
> 💡 **由于当前第一阶段的局限性，对话轮数过长或上下文太多时，每提一个需求前加一句 'aegis'**
## 前置条件

- Python 3.11+
- Git

## 安装

```powershell
pip install git+https://github.com/Szy-Fxy/Aegis.git
```

Windows 用户注意：安装后如果 `aegis` 命令找不到，需要把 `%USERPROFILE%\AppData\Roaming\Python\Python3XX\Scripts` 加到 PATH。详见 [USAGE.md](USAGE.md)。

## 命令速查

| 命令 | 作用 |
|------|------|
| `aegis init` | 初始化项目 Aegis 规则 |
| `aegis start "<标题>" -l L2` | 开始一个新需求 |
| `aegis check` | 执行 BOUNDARY CHECK |
| `aegis advance` | 推进到下一阶段 |
| `aegis status` | 查看项目状态 |
| `aegis devlog write REQ-001 -m "..."` | 写开发日志 |

## 需求分级

| 级别 | 说明 | 阶段数 | 示例 |
|:---:|------|:---:|------|
| L1 | 小修复 | 1 阶段 | 改配置、修 typo |
| L2 | 功能/模块 | 5 阶段 | 加背包系统 |
| L3 | 架构改造 | 7 阶段 | 重写渲染管线 |

## 路线图

| Phase   | 内容                                      | 状态       |
| ------- | --------------------------------------- | -------- |
| Phase 1 | CLI + state.json + pre-commit hook + 测试 | ✅ v5.2.1 |
| Phase 2 | MCP Server + YAML 状态机                   | 📋 规划中   |
| Phase 3 | 全 MCP 生态                                | 💡 设想    |

## 开发

```powershell
python -m pytest tests/ -q
```

## 已知问题

[KNOWN_ISSUES.md](KNOWN_ISSUES.md)

## 许可证

MIT — 详见 [LICENSE](LICENSE)
